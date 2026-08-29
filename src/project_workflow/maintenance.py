"""Canonical Project Workflow maintenance runtime."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from collections.abc import Mapping
from pathlib import Path
from typing import TypedDict

from .contracts import (
    ABSENT_FILE_HASH,
    AGENT_CHOICES,
    CANONICAL_UPGRADE_COMMAND,
    CODEX_SKILL_NAMES,
    CURRENT_ASSET_VERSION,
    CURRENT_MANIFEST_VERSION,
    CURRENT_PACKAGE_VERSION,
    CURRENT_SCHEMA_VERSION,
    DELEGATION_RUNTIME_RELATIVE_DIR,
    GENERATED_MARKER,
    MANAGED_BLOCK_END,
    MANAGED_BLOCK_START,
    MIGRATION_ID_PATTERN,
    PROMPT_FILES,
    SMOKE_BOMB_PLAN_SCHEMA_VERSION,
    SMOKE_BOMB_RESULT_SCHEMA_VERSION,
    UPGRADE_APPLY_RESULT_SCHEMA_VERSION,
    UPGRADE_PLAN_SCHEMA_VERSION,
    WORKFLOW_CONFIG_FILENAME,
    WORKFLOW_MANIFEST_FILENAME,
    ManifestValidationError,
    MigrationDefinition,
    RepositoryCompatibility,
    SmokeBombBlocker,
    SmokeBombFailure,
    UpgradeApplyFailure,
    UpgradeBlocker,
    WorkflowManifest,
)
from .inspection import (
    _accepted_doctor_warning_fingerprints,
    _doctor_issue_fingerprint,
    _doctor_issue_path_for_fingerprint,
    run_doctor,
)
from .repository import (
    _backlog_template,
    _default_workflow_config_text,
    _get_package_resource,
    _is_generated_content,
    _managed_project_workflow_block,
    _parse_workflow_manifest,
    _planned_delegation_runtime_ignore,
    _planned_generated_file,
    _planned_managed_block,
    _prompt_filename_to_agent_name,
    _prompt_filename_to_claude_agent_name,
    _prompt_filename_to_cursor_agent_name,
    _repository_compatibility,
    _run_git,
    _serialize_workflow_manifest,
    _sha256_file,
    _to_claude_agent_markdown,
    _to_cursor_agent_markdown,
    _tracker_template,
)


class UpgradeVersionRecord(TypedDict, total=False):
    package: str | None
    asset: int | None
    schema: int | None
    applied_migrations: list[str]


class UpgradeStepRecord(TypedDict):
    migration_id: str
    source_schema: int
    target_schema: int
    target_files: list[str]
    transformations: list[str]


class UpgradePreconditionRecord(TypedDict):
    kind: str
    artifact: str
    expected: str


class UpgradeBlockerRecord(TypedDict):
    code: str
    message: str


class UpgradeOwnerDecisionRecord(TypedDict):
    code: str
    artifact: str
    message: str
    accepted: bool
    fingerprint: str


class UpgradeOutputRecord(TypedDict):
    artifact: str
    expected: str


class UpgradePlan(TypedDict, total=False):
    schema_version: int
    repository_state: str
    repository_reason: str
    agent: str
    source: UpgradeVersionRecord
    target: UpgradeVersionRecord
    steps: list[UpgradeStepRecord]
    asset_changes: list[str]
    target_files: list[str]
    executable_files: list[str]
    preconditions: list[UpgradePreconditionRecord]
    blockers: list[UpgradeBlockerRecord]
    owner_decisions: list[UpgradeOwnerDecisionRecord]
    expected_outputs: list[UpgradeOutputRecord]
    plan_fingerprint: str


class UpgradeApplyFailureRecord(TypedDict):
    code: str
    message: str


class UpgradeApplyResult(TypedDict, total=False):
    schema_version: int
    status: str
    plan_fingerprint: str
    applied_migrations: list[str]
    changed_files: list[str]
    noop: bool
    failure: UpgradeApplyFailureRecord | None
    post_upgrade: dict[str, object]


class SmokeBombRepositoryRecord(TypedDict):
    root: str
    top_level: str | None
    branch: str | None
    commit: str | None
    default_branch: str | None
    on_default_branch: bool


class SmokeBombActionRecord(TypedDict):
    path: str
    action: str
    before_sha256: str
    after_sha256: str
    reason: str
    ownership: str
    source: str


class SmokeBombArchivePlan(TypedDict):
    source: str
    excluded: list[str]
    included_paths: list[str]
    entry_count: int


class SmokeBombPlan(TypedDict, total=False):
    schema_version: int
    operation: str
    package_version: str
    repository: SmokeBombRepositoryRecord
    workflow_installed: bool
    client_agents: list[str]
    validation_commands: list[str]
    output_path: str
    actions: list[SmokeBombActionRecord]
    archive: SmokeBombArchivePlan
    warnings: list[str]
    blockers: list[UpgradeBlockerRecord]
    plan_fingerprint: str


class SmokeBombValidationRecord(TypedDict):
    command: str
    exit_code: int
    stdout_bytes: int
    stdout_sha256: str
    stderr_bytes: int
    stderr_sha256: str


class SmokeBombArchiveResult(TypedDict, total=False):
    path: str
    sha256: str
    entries: list[str]
    entry_count: int
    source_repository: SmokeBombRepositoryRecord
    plan_fingerprint: str
    client_agents: list[str]
    exclusions: list[str]


class SmokeBombResult(TypedDict, total=False):
    schema_version: int
    status: str
    plan_fingerprint: str
    repository: SmokeBombRepositoryRecord
    client_agents: list[str]
    changed_files: list[str]
    validation: list[SmokeBombValidationRecord]
    archive: SmokeBombArchiveResult | None
    failure: UpgradeApplyFailureRecord | None


LEGACY_MANIFEST_MIGRATION_ID = "PW-0001-legacy-manifest"

LEGACY_MANIFEST_MIGRATION = MigrationDefinition(
    migration_id=LEGACY_MANIFEST_MIGRATION_ID,
    source_schema=0,
    target_schema=1,
    target_files=(".project-workflow/manifest.json",),
    transformations=("create-version-manifest",),
)


def _apply_legacy_manifest_migration(
    inputs: dict[str, bytes | None],
) -> dict[str, bytes | None]:
    target = ".project-workflow/manifest.json"
    if inputs.get(target) is not None:
        raise ValueError("Legacy manifest migration requires an absent manifest.")
    manifest = WorkflowManifest(
        manifest_version=CURRENT_MANIFEST_VERSION,
        package_version=CURRENT_PACKAGE_VERSION,
        asset_version=CURRENT_ASSET_VERSION,
        schema_version=CURRENT_SCHEMA_VERSION,
        applied_migrations=(LEGACY_MANIFEST_MIGRATION_ID,),
    )
    return {target: _serialize_workflow_manifest(manifest).encode("utf-8")}


PRODUCTION_MIGRATIONS: tuple[MigrationDefinition, ...] = (LEGACY_MANIFEST_MIGRATION,)

PRODUCTION_MIGRATION_HANDLERS: dict[str, object] = {
    LEGACY_MANIFEST_MIGRATION_ID: _apply_legacy_manifest_migration,
}


def _migration_target_is_safe(target: str) -> bool:
    path = Path(target)
    return bool(target) and not path.is_absolute() and ".." not in path.parts


def _resolve_migration_path(
    source_schema: int,
    target_schema: int,
    migrations: tuple[MigrationDefinition, ...],
) -> tuple[tuple[MigrationDefinition, ...], tuple[UpgradeBlocker, ...]]:
    blockers: list[UpgradeBlocker] = []
    migration_ids = [migration.migration_id for migration in migrations]
    duplicate_ids = sorted(
        migration_id for migration_id in set(migration_ids) if migration_ids.count(migration_id) > 1
    )
    if duplicate_ids:
        blockers.append(
            UpgradeBlocker(
                "PW_UPGRADE_REGISTRY_DUPLICATE_ID",
                "Duplicate migration IDs: " + ", ".join(duplicate_ids),
            )
        )

    by_source: dict[int, list[MigrationDefinition]] = {}
    for migration in migrations:
        by_source.setdefault(migration.source_schema, []).append(migration)
        if (
            not MIGRATION_ID_PATTERN.fullmatch(migration.migration_id)
            or not migration.target_files
            or not migration.transformations
            or any(not transformation.strip() for transformation in migration.transformations)
        ):
            blockers.append(
                UpgradeBlocker(
                    "PW_UPGRADE_REGISTRY_INVALID_MIGRATION",
                    f"Migration {migration.migration_id or '<empty>'} has invalid metadata.",
                )
            )
        if migration.target_schema <= migration.source_schema:
            blockers.append(
                UpgradeBlocker(
                    "PW_UPGRADE_REGISTRY_DOWNGRADE",
                    f"Migration {migration.migration_id} must advance the repository schema.",
                )
            )
        unsafe_targets = [
            target for target in migration.target_files if not _migration_target_is_safe(target)
        ]
        if unsafe_targets:
            blockers.append(
                UpgradeBlocker(
                    "PW_UPGRADE_REGISTRY_INVALID_TARGET",
                    f"Migration {migration.migration_id} has unsafe target files: "
                    + ", ".join(unsafe_targets),
                )
            )

    ambiguous_sources = sorted(source for source, entries in by_source.items() if len(entries) > 1)
    if ambiguous_sources:
        blockers.append(
            UpgradeBlocker(
                "PW_UPGRADE_REGISTRY_AMBIGUOUS",
                "Multiple migrations start at schema versions: "
                + ", ".join(str(source) for source in ambiguous_sources),
            )
        )
    cycle_schema: int | None = None
    for start_schema in sorted(by_source):
        current_schema = start_schema
        cycle_visited: set[int] = set()
        while len(by_source.get(current_schema, [])) == 1:
            if current_schema in cycle_visited:
                cycle_schema = current_schema
                break
            cycle_visited.add(current_schema)
            current_schema = by_source[current_schema][0].target_schema
        if cycle_schema is not None:
            break
    if cycle_schema is not None:
        blockers.append(
            UpgradeBlocker(
                "PW_UPGRADE_REGISTRY_CYCLE",
                f"Migration registry cycles at schema {cycle_schema}.",
            )
        )
    if blockers:
        return (), tuple(blockers)

    if source_schema == target_schema:
        return (), ()
    if source_schema > target_schema:
        return (
            (),
            (
                UpgradeBlocker(
                    "PW_UPGRADE_REGISTRY_DOWNGRADE",
                    f"Repository schema {source_schema} is newer than target {target_schema}.",
                ),
            ),
        )

    path: list[MigrationDefinition] = []
    visited: set[int] = set()
    current_schema = source_schema
    while current_schema != target_schema:
        if current_schema in visited:
            return (
                (),
                (
                    UpgradeBlocker(
                        "PW_UPGRADE_REGISTRY_CYCLE",
                        f"Migration path cycles at schema {current_schema}.",
                    ),
                ),
            )
        visited.add(current_schema)
        candidates = by_source.get(current_schema, [])
        if not candidates:
            return (
                (),
                (
                    UpgradeBlocker(
                        "PW_UPGRADE_REGISTRY_PATH_MISSING",
                        f"No migration path from schema {current_schema} to {target_schema}.",
                    ),
                ),
            )
        migration = candidates[0]
        if migration.target_schema > target_schema:
            return (
                (),
                (
                    UpgradeBlocker(
                        "PW_UPGRADE_REGISTRY_PATH_MISSING",
                        f"Migration {migration.migration_id} overshoots target schema "
                        f"{target_schema}.",
                    ),
                ),
            )
        path.append(migration)
        current_schema = migration.target_schema
    return tuple(path), ()


def _upgrade_file_hash(root: Path, relative_path: str) -> str:
    path = root / relative_path
    if not path.exists():
        return ABSENT_FILE_HASH
    if path.is_symlink() or not path.is_file():
        return "not-a-file"
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _upgrade_content_hash(content: bytes | None) -> str:
    if content is None:
        return ABSENT_FILE_HASH
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _upgrade_source_versions(
    compatibility: RepositoryCompatibility,
) -> UpgradeVersionRecord:
    if compatibility.manifest is not None:
        return {
            "package": compatibility.manifest.package_version,
            "asset": compatibility.manifest.asset_version,
            "schema": compatibility.manifest.schema_version,
            "applied_migrations": list(compatibility.manifest.applied_migrations),
        }
    if compatibility.state == "legacy-unversioned":
        return {
            "package": None,
            "asset": 0,
            "schema": 0,
            "applied_migrations": [],
        }
    return {
        "package": None,
        "asset": None,
        "schema": None,
        "applied_migrations": [],
    }


def _upgrade_state_blockers(
    compatibility: RepositoryCompatibility,
) -> tuple[UpgradeBlocker, ...]:
    mapping = {
        "invalid": (
            "PW_UPGRADE_INVALID_REPOSITORY",
            f"Repository manifest is invalid: {compatibility.reason}.",
        ),
        "unsupported-future": (
            "PW_UPGRADE_UNSUPPORTED_FUTURE",
            f"Repository uses an unsupported future contract: {compatibility.reason}.",
        ),
        "not-initialized": (
            "PW_UPGRADE_NOT_INITIALIZED",
            "Repository is not initialized with project-workflow.",
        ),
    }
    blocker = mapping.get(compatibility.state)
    if blocker is None:
        return ()
    return (UpgradeBlocker(*blocker),)


def _upgrade_owner_decisions(root: Path) -> list[UpgradeOwnerDecisionRecord]:
    accepted_fingerprints = _accepted_doctor_warning_fingerprints(root)
    decisions: list[UpgradeOwnerDecisionRecord] = []
    for issue in run_doctor(root):
        if issue.remediation_owner != "owner":
            continue
        fingerprint = _doctor_issue_fingerprint(issue, root)
        decisions.append(
            {
                "code": issue.code,
                "artifact": _doctor_issue_path_for_fingerprint(issue, root),
                "message": issue.message,
                "accepted": fingerprint in accepted_fingerprints,
                "fingerprint": fingerprint,
            }
        )
    return decisions


def _managed_asset_upgrade_outputs(
    root: Path,
    selected_agent: str,
) -> tuple[dict[str, bytes | None], tuple[str, ...]]:
    """Plan the exact managed-asset refresh that init previously performed."""
    outputs: dict[str, bytes | None] = {}
    executable_files: set[str] = set()

    def require_safe_target(path: Path, *, allow_directory: bool = False) -> None:
        relative = path.relative_to(root)
        current = root
        for part in relative.parts[:-1]:
            current /= part
            if current.is_symlink() or (current.exists() and not current.is_dir()):
                raise UpgradeApplyFailure(
                    "PW_UPGRADE_MANAGED_ASSET_INVALID_TARGET",
                    f"Managed asset target has an unsafe parent: {relative.as_posix()}.",
                )
        if path.is_symlink() or (
            path.exists() and not path.is_file() and not (allow_directory and path.is_dir())
        ):
            raise UpgradeApplyFailure(
                "PW_UPGRADE_MANAGED_ASSET_INVALID_TARGET",
                f"Managed asset target must be a regular file or absent: {relative.as_posix()}.",
            )

    def record(path: Path, content: bytes, *, executable: bool = False) -> None:
        require_safe_target(path)
        relative = path.relative_to(root).as_posix()
        existing = path.read_bytes() if path.exists() else None
        if existing != content:
            outputs[relative] = content
        if executable and (
            not path.exists() or not path.is_file() or not (path.stat().st_mode & 0o111)
        ):
            executable_files.add(relative)
            outputs.setdefault(relative, content)

    def record_generated(
        relative_path: str,
        resource_path: str,
        *,
        executable: bool = False,
        transform: object | None = None,
    ) -> None:
        path = root / relative_path
        require_safe_target(path)
        try:
            content = _get_package_resource(resource_path)
        except SystemExit as exc:
            raise UpgradeApplyFailure(
                "PW_UPGRADE_PACKAGE_RESOURCE_UNAVAILABLE",
                "Managed asset resources are unavailable in this local helper. Run: "
                f"{CANONICAL_UPGRADE_COMMAND} --agent {selected_agent}.",
            ) from exc
        if callable(transform):
            content = transform(content)
        target, generated_bytes, target_executable = _planned_generated_file(
            path,
            content,
            executable=executable,
        )
        require_safe_target(target)
        record(target, generated_bytes, executable=target_executable)

    def record_retired(path: Path) -> None:
        require_safe_target(path, allow_directory=True)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() or child.is_symlink():
                    outputs[child.relative_to(root).as_posix()] = None
        elif path.exists() or path.is_symlink():
            outputs[path.relative_to(root).as_posix()] = None

    workflow_dir = root / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    backlog_path = workflow_dir / "BACKLOG.md"
    guidance_path = workflow_dir / "guidance.md"
    config_path = workflow_dir / WORKFLOW_CONFIG_FILENAME
    manifest_path = workflow_dir / WORKFLOW_MANIFEST_FILENAME

    record(
        workflow_dir / ".gitignore",
        _planned_delegation_runtime_ignore(root),
    )

    if not tracker_path.exists():
        record(tracker_path, _tracker_template().encode("utf-8"))
    if not backlog_path.exists():
        record(backlog_path, _backlog_template().encode("utf-8"))
    if not guidance_path.exists():
        record(
            guidance_path,
            (
                b"# Project Workflow Guidance\n\n"
                b"Use this file for repo-specific workflow guidance that should survive "
                b"project-workflow upgrades.\n\n"
                b"Add local conventions, validation commands, safety constraints, handoff "
                b"rules, and agent notes here.\n"
            ),
        )
    if not config_path.exists():
        record(config_path, _default_workflow_config_text().encode("utf-8"))

    record_generated(
        ".project-workflow/cli/workflow.py",
        "templates/workflow.py",
    )
    record_generated(
        ".project-workflow/cli/workflow",
        "templates/workflow",
        executable=True,
    )
    record_generated(
        ".project-workflow/cli/adapter_common.py",
        "adapter_common.py",
    )
    record_generated(
        ".project-workflow/cli/codex_adapter.py",
        "codex_adapter.py",
    )
    record_generated(
        ".project-workflow/cli/claude_adapter.py",
        "claude_adapter.py",
    )
    for relative_path, executable in (
        (".claude-plugin/plugin.json", False),
        ("hooks/hooks.json", False),
        ("scripts/project-workflow-claude-hook", True),
        ("README.md", False),
    ):
        record_generated(
            ".project-workflow/cli/claude_plugin/"
            "project-workflow-execution-control/" + relative_path,
            "claude_plugin/project-workflow-execution-control/" + relative_path,
            executable=executable,
        )

    managed_block = _managed_project_workflow_block()
    if selected_agent == "claude-code":
        for prompt_file in PROMPT_FILES:
            agent_name = _prompt_filename_to_claude_agent_name(prompt_file)
            record_generated(
                f".claude/agents/{agent_name}.md",
                f"prompts/{prompt_file}",
                transform=lambda content, name=agent_name: _to_claude_agent_markdown(content, name),
            )
        record_retired(root / ".claude" / "agents" / "project-scaffold.md")
    elif selected_agent == "codex":
        agents_path = root / "AGENTS.md"
        require_safe_target(agents_path)
        record(agents_path, _planned_managed_block(agents_path, managed_block))
        for skill_name in CODEX_SKILL_NAMES:
            record_generated(
                f".agents/skills/{skill_name}/SKILL.md",
                f"codex/skills/{skill_name}/SKILL.md",
            )
        record_retired(root / ".agents" / "skills" / "project-scaffold")
    elif selected_agent == "cursor":
        for prompt_file in PROMPT_FILES:
            agent_name = _prompt_filename_to_cursor_agent_name(prompt_file)
            record_generated(
                f".cursor/agents/{agent_name}.md",
                f"prompts/{prompt_file}",
                transform=lambda content, name=agent_name: _to_cursor_agent_markdown(content, name),
            )
        record_retired(root / ".cursor" / "agents" / "project-scaffold.md")
        record_generated(
            ".cursor/rules/project-workflow.mdc",
            "cursor/rules/project-workflow.mdc",
        )
    else:
        copilot_path = root / ".github" / "copilot-instructions.md"
        require_safe_target(copilot_path)
        record(copilot_path, _planned_managed_block(copilot_path, managed_block))
        for prompt_file in PROMPT_FILES:
            record_generated(
                f".github/prompts/{prompt_file}",
                f"prompts/{prompt_file}",
            )
        record_retired(root / ".github" / "prompts" / "Scaffold.prompt.md")

    compatibility = _repository_compatibility(root)
    if compatibility.manifest is not None and compatibility.state in {"current", "upgradeable"}:
        existing_manifest = compatibility.manifest
        refreshed_manifest = WorkflowManifest(
            manifest_version=existing_manifest.manifest_version,
            package_version=CURRENT_PACKAGE_VERSION,
            asset_version=CURRENT_ASSET_VERSION,
            schema_version=existing_manifest.schema_version,
            applied_migrations=existing_manifest.applied_migrations,
        )
        if refreshed_manifest != existing_manifest:
            record(
                manifest_path,
                _serialize_workflow_manifest(refreshed_manifest).encode("utf-8"),
            )

    return outputs, tuple(sorted(executable_files))


def _upgrade_plan_fingerprint(payload: Mapping[str, object]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _build_upgrade_plan(
    root: Path,
    *,
    migrations: tuple[MigrationDefinition, ...] = PRODUCTION_MIGRATIONS,
    handlers: dict[str, object] | None = None,
) -> UpgradePlan:
    compatibility = _repository_compatibility(root)
    source = _upgrade_source_versions(compatibility)
    target: UpgradeVersionRecord = {
        "package": CURRENT_PACKAGE_VERSION,
        "asset": CURRENT_ASSET_VERSION,
        "schema": CURRENT_SCHEMA_VERSION,
    }
    blockers = list(_upgrade_state_blockers(compatibility))
    migration_path: tuple[MigrationDefinition, ...] = ()
    source_schema = source["schema"]
    if not blockers and isinstance(source_schema, int):
        migration_path, registry_blockers = _resolve_migration_path(
            source_schema,
            CURRENT_SCHEMA_VERSION,
            migrations,
        )
        blockers.extend(registry_blockers)

    steps: list[UpgradeStepRecord] = [
        {
            "migration_id": migration.migration_id,
            "source_schema": migration.source_schema,
            "target_schema": migration.target_schema,
            "target_files": list(migration.target_files),
            "transformations": list(migration.transformations),
        }
        for migration in migration_path
    ]
    target_files = list(
        dict.fromkeys(target for migration in migration_path for target in migration.target_files)
    )
    invalid_existing_targets = [
        target_file
        for target_file in target_files
        if _upgrade_file_hash(root, target_file) == "not-a-file"
    ]
    if invalid_existing_targets:
        blockers.append(
            UpgradeBlocker(
                "PW_UPGRADE_REGISTRY_INVALID_TARGET",
                "Planned targets must be regular files or absent: "
                + ", ".join(invalid_existing_targets),
            )
        )
    preconditions: list[UpgradePreconditionRecord] = [
        {
            "kind": "clean-worktree",
            "artifact": ".",
            "expected": "required-for-apply",
        },
        {
            "kind": "repository-state",
            "artifact": ".project-workflow/manifest.json",
            "expected": compatibility.state,
        },
    ]
    preconditions.extend(
        {
            "kind": "file-hash",
            "artifact": target_file,
            "expected": _upgrade_file_hash(root, target_file),
        }
        for target_file in target_files
        if target_file not in invalid_existing_targets
    )
    payload: UpgradePlan = {
        "schema_version": UPGRADE_PLAN_SCHEMA_VERSION,
        "repository_state": compatibility.state,
        "repository_reason": compatibility.reason,
        "source": source,
        "target": target,
        "steps": steps,
        "target_files": target_files,
        "preconditions": preconditions,
        "blockers": [{"code": blocker.code, "message": blocker.message} for blocker in blockers],
        "owner_decisions": _upgrade_owner_decisions(root),
        "expected_outputs": [],
    }
    if steps and handlers is not None and not blockers:
        try:
            outputs = _compute_upgrade_outputs(root, payload, handlers)
        except UpgradeApplyFailure as failure:
            code = (
                "PW_UPGRADE_HANDLER_MISSING"
                if failure.code == "PW_UPGRADE_APPLY_HANDLER_MISSING"
                else "PW_UPGRADE_HANDLER_INVALID"
            )
            blockers.append(UpgradeBlocker(code, failure.message))
            payload["blockers"] = [
                {"code": blocker.code, "message": blocker.message} for blocker in blockers
            ]
        else:
            payload["expected_outputs"] = [
                {
                    "artifact": target,
                    "expected": (
                        ABSENT_FILE_HASH
                        if content is None
                        else "sha256:" + hashlib.sha256(content).hexdigest()
                    ),
                }
                for target, content in outputs.items()
            ]
    return {"plan_fingerprint": _upgrade_plan_fingerprint(payload), **payload}


def _build_repository_upgrade_plan(root: Path, selected_agent: str) -> UpgradePlan:
    """Build one deterministic plan for managed assets and durable schema state."""
    schema_plan = _build_upgrade_plan(root, handlers=PRODUCTION_MIGRATION_HANDLERS)
    blockers = list(schema_plan["blockers"])
    asset_outputs: dict[str, bytes | None] = {}
    executable_files: tuple[str, ...] = ()
    if not blockers:
        try:
            asset_outputs, executable_files = _managed_asset_upgrade_outputs(root, selected_agent)
        except UpgradeApplyFailure as failure:
            blockers.append({"code": failure.code, "message": failure.message})

    schema_targets = list(schema_plan["target_files"])
    target_files = sorted(set(schema_targets) | set(asset_outputs))
    preconditions: list[UpgradePreconditionRecord] = [
        {
            "kind": "clean-worktree",
            "artifact": ".",
            "expected": "required-for-apply",
        },
        {
            "kind": "repository-state",
            "artifact": ".project-workflow/manifest.json",
            "expected": schema_plan["repository_state"],
        },
    ]
    preconditions.extend(
        {
            "kind": "file-hash",
            "artifact": target,
            "expected": _upgrade_file_hash(root, target),
        }
        for target in target_files
    )
    payload: UpgradePlan = {
        "schema_version": schema_plan["schema_version"],
        "repository_state": schema_plan["repository_state"],
        "repository_reason": schema_plan["repository_reason"],
        "agent": selected_agent,
        "source": schema_plan["source"],
        "target": schema_plan["target"],
        "steps": schema_plan["steps"],
        "asset_changes": sorted(asset_outputs),
        "target_files": target_files,
        "executable_files": list(executable_files),
        "preconditions": preconditions,
        "blockers": blockers,
        "owner_decisions": schema_plan["owner_decisions"],
        "expected_outputs": [],
    }
    if target_files and not blockers:
        try:
            outputs = _compute_upgrade_outputs(
                root,
                payload,
                PRODUCTION_MIGRATION_HANDLERS,
                initial_outputs=asset_outputs,
            )
        except UpgradeApplyFailure as failure:
            payload["blockers"] = [
                {
                    "code": "PW_UPGRADE_HANDLER_INVALID",
                    "message": failure.message,
                }
            ]
        else:
            payload["expected_outputs"] = [
                {
                    "artifact": target,
                    "expected": _upgrade_content_hash(outputs[target]),
                }
                for target in target_files
            ]
    return {"plan_fingerprint": _upgrade_plan_fingerprint(payload), **payload}


def _format_upgrade_plan_human(plan: UpgradePlan) -> str:
    source = plan["source"]
    target = plan["target"]
    assert isinstance(source, dict)
    assert isinstance(target, dict)
    lines = [
        f"project upgrade plan: {plan['repository_state']} -> schema {target['schema']}",
        f"plan fingerprint: {plan['plan_fingerprint']}",
        f"source versions: package={source['package']} asset={source['asset']} "
        f"schema={source['schema']}",
        f"target versions: package={target['package']} asset={target['asset']} "
        f"schema={target['schema']}",
    ]
    if plan.get("agent"):
        lines.append(f"agent mode: {plan['agent']}")
    steps = plan["steps"]
    blockers = plan["blockers"]
    owner_decisions = plan["owner_decisions"]
    assert isinstance(steps, list)
    assert isinstance(blockers, list)
    assert isinstance(owner_decisions, list)
    if steps:
        lines.append("migrations:")
        for step in steps:
            lines.append(
                f"- {step['migration_id']}: schema {step['source_schema']} -> "
                f"{step['target_schema']} ({', '.join(step['target_files'])})"
            )
    else:
        lines.append("migrations: none")
    asset_changes = plan.get("asset_changes", [])
    if asset_changes:
        lines.append("managed asset changes:")
        lines.extend(f"- {artifact}" for artifact in asset_changes)
    else:
        lines.append("managed asset changes: none")
    expected_outputs = plan.get("expected_outputs", [])
    if expected_outputs:
        lines.append("expected outputs:")
        lines.extend(f"- {output['artifact']}: {output['expected']}" for output in expected_outputs)
    if blockers:
        lines.append("blockers:")
        lines.extend(f"- {blocker['code']}: {blocker['message']}" for blocker in blockers)
    if owner_decisions:
        lines.append("owner decisions:")
        for decision in owner_decisions:
            accepted = "accepted" if decision["accepted"] else "open"
            lines.append(
                f"- {decision['code']} {decision['artifact']} [{accepted}]: {decision['message']}"
            )
    return "\n".join(lines)


def _require_clean_git_worktree(root: Path) -> None:
    try:
        inside = _run_git(["rev-parse", "--is-inside-work-tree"], cwd=root)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise UpgradeApplyFailure(
            "PW_UPGRADE_APPLY_NOT_GIT",
            "Upgrade apply requires a Git worktree.",
        ) from exc
    if inside != "true":
        raise UpgradeApplyFailure(
            "PW_UPGRADE_APPLY_NOT_GIT",
            "Upgrade apply requires a Git worktree.",
        )
    if _run_git(["status", "--porcelain"], cwd=root):
        raise UpgradeApplyFailure(
            "PW_UPGRADE_APPLY_DIRTY_WORKTREE",
            "Upgrade apply requires a clean worktree, including no untracked files.",
        )


def _validate_upgrade_apply_plan(
    root: Path,
    plan: UpgradePlan,
    supplied_fingerprint: str,
) -> None:
    if supplied_fingerprint != plan["plan_fingerprint"]:
        raise UpgradeApplyFailure(
            "PW_UPGRADE_APPLY_STALE_PLAN",
            "Supplied plan fingerprint does not match the current deterministic plan.",
        )
    if plan["blockers"]:
        raise UpgradeApplyFailure(
            "PW_UPGRADE_APPLY_BLOCKED",
            "The current upgrade plan contains blockers.",
        )
    for precondition in plan["preconditions"]:
        if precondition["kind"] == "repository-state":
            actual_state = _repository_compatibility(root).state
            if actual_state != precondition["expected"]:
                raise UpgradeApplyFailure(
                    "PW_UPGRADE_APPLY_STALE_STATE",
                    f"Repository state changed from {precondition['expected']} to {actual_state}.",
                )
        elif precondition["kind"] == "file-hash":
            actual_hash = _upgrade_file_hash(root, precondition["artifact"])
            if actual_hash != precondition["expected"]:
                raise UpgradeApplyFailure(
                    "PW_UPGRADE_APPLY_STALE_FILE",
                    f"Planned input changed: {precondition['artifact']}.",
                )


def _compute_upgrade_outputs(
    root: Path,
    plan: UpgradePlan,
    handlers: dict[str, object],
    *,
    initial_outputs: dict[str, bytes | None] | None = None,
) -> dict[str, bytes | None]:
    target_files = plan["target_files"]
    assert isinstance(target_files, list)
    declared_targets = set(target_files)
    outputs: dict[str, bytes | None] = {}
    for target in target_files:
        path = root / target
        outputs[target] = path.read_bytes() if path.exists() else None
    if initial_outputs:
        if not set(initial_outputs).issubset(declared_targets):
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_HANDLER_INVALID",
                "Managed asset planning returned an undeclared target.",
            )
        outputs.update(initial_outputs)

    for step in plan["steps"]:
        migration_id = step["migration_id"]
        handler = handlers.get(migration_id)
        if not callable(handler):
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_HANDLER_MISSING",
                f"No migration handler is registered for {migration_id}.",
            )
        handler_targets = set(step["target_files"])
        handler_inputs = {target: outputs[target] for target in step["target_files"]}
        try:
            result = handler(dict(handler_inputs))
        except Exception as exc:
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_HANDLER_INVALID",
                f"Migration {migration_id} handler failed: {exc}",
            ) from exc
        if not isinstance(result, dict) or set(result) != handler_targets:
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_HANDLER_INVALID",
                f"Migration {migration_id} must return exactly its declared targets.",
            )
        if not set(result).issubset(declared_targets) or any(
            value is not None and not isinstance(value, bytes) for value in result.values()
        ):
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_HANDLER_INVALID",
                f"Migration {migration_id} returned undeclared or non-bytes output.",
            )
        outputs.update(result)

    if plan["steps"]:
        manifest_target = ".project-workflow/manifest.json"
        manifest_bytes = outputs.get(manifest_target)
        if manifest_bytes is None:
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_FINAL_MANIFEST_INVALID",
                "A schema migration must produce the version manifest.",
            )
        try:
            manifest_raw = json.loads(manifest_bytes.decode("utf-8"))
            manifest = _parse_workflow_manifest(manifest_raw)
        except (UnicodeDecodeError, json.JSONDecodeError, ManifestValidationError) as exc:
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_FINAL_MANIFEST_INVALID",
                "Migration output contains an invalid final manifest.",
            ) from exc
        if manifest.schema_version != plan["target"]["schema"]:
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_FINAL_MANIFEST_INVALID",
                "Migration output manifest does not match the target schema.",
            )
    return outputs


def _atomic_replace_target(path: Path, content: bytes | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if content is None:
        if path.exists():
            path.unlink()
        return
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _apply_upgrade_outputs(
    root: Path,
    outputs: dict[str, bytes | None],
    *,
    executable_files: tuple[str, ...] = (),
    fail_after_replacements: int | None = None,
) -> list[str]:
    originals: dict[str, bytes | None] = {}
    original_modes: dict[str, int | None] = {}
    changed_files: list[str] = []
    for target, content in outputs.items():
        path = root / target
        originals[target] = path.read_bytes() if path.exists() else None
        original_modes[target] = path.stat().st_mode & 0o777 if path.exists() else None
        original_mode = original_modes[target]
        executable_change = target in executable_files and (
            original_mode is None or not (original_mode & 0o111)
        )
        if originals[target] != content or executable_change:
            changed_files.append(target)
    replaced: list[str] = []
    try:
        if fail_after_replacements == 0:
            raise OSError("injected replacement failure")
        for target in changed_files:
            path = root / target
            if originals[target] != outputs[target]:
                _atomic_replace_target(path, outputs[target])
            if target in executable_files and path.exists():
                path.chmod(0o755)
            replaced.append(target)
            if fail_after_replacements == len(replaced):
                raise OSError("injected replacement failure")
    except OSError as exc:
        rollback_errors: list[str] = []
        for target in reversed(replaced):
            try:
                _atomic_replace_target(root / target, originals[target])
                original_mode = original_modes[target]
                if original_mode is not None and (root / target).exists():
                    (root / target).chmod(original_mode)
            except OSError:
                rollback_errors.append(target)
        detail = f" Failed to restore: {', '.join(rollback_errors)}." if rollback_errors else ""
        raise UpgradeApplyFailure(
            "PW_UPGRADE_APPLY_REPLACEMENT_FAILED",
            "Upgrade replacement failed; touched targets were restored." + detail,
        ) from exc
    return changed_files


def _upgrade_apply_result(
    *,
    plan: UpgradePlan,
    status: str,
    changed_files: list[str] | None = None,
    failure: UpgradeApplyFailure | None = None,
) -> UpgradeApplyResult:
    return {
        "schema_version": UPGRADE_APPLY_RESULT_SCHEMA_VERSION,
        "status": status,
        "plan_fingerprint": plan["plan_fingerprint"],
        "applied_migrations": (
            [step["migration_id"] for step in plan["steps"]] if status == "applied" else []
        ),
        "changed_files": changed_files or [],
        "noop": status == "noop",
        "failure": None if failure is None else {"code": failure.code, "message": failure.message},
    }


def _apply_upgrade_plan(
    root: Path,
    supplied_fingerprint: str,
    *,
    migrations: tuple[MigrationDefinition, ...] = PRODUCTION_MIGRATIONS,
    handlers: dict[str, object] = PRODUCTION_MIGRATION_HANDLERS,
    fail_after_replacements: int | None = None,
) -> UpgradeApplyResult:
    plan = _build_upgrade_plan(root, migrations=migrations, handlers=handlers)
    try:
        _validate_upgrade_apply_plan(root, plan, supplied_fingerprint)
        _require_clean_git_worktree(root)
        if not plan["steps"]:
            return _upgrade_apply_result(plan=plan, status="noop")
        outputs = _compute_upgrade_outputs(root, plan, handlers)
        actual_outputs = [
            {
                "artifact": target,
                "expected": (
                    ABSENT_FILE_HASH
                    if content is None
                    else "sha256:" + hashlib.sha256(content).hexdigest()
                ),
            }
            for target, content in outputs.items()
        ]
        if actual_outputs != plan["expected_outputs"]:
            raise UpgradeApplyFailure(
                "PW_UPGRADE_APPLY_STALE_PLAN",
                "Computed migration outputs do not match the reviewed plan.",
            )
        _validate_upgrade_apply_plan(root, plan, supplied_fingerprint)
        _require_clean_git_worktree(root)
        changed_files = _apply_upgrade_outputs(
            root,
            outputs,
            fail_after_replacements=fail_after_replacements,
        )
        return _upgrade_apply_result(
            plan=plan,
            status="applied",
            changed_files=changed_files,
        )
    except UpgradeApplyFailure as failure:
        return _upgrade_apply_result(plan=plan, status="failed", failure=failure)


def _apply_repository_upgrade_plan(
    root: Path,
    selected_agent: str,
    supplied_fingerprint: str,
    *,
    fail_after_replacements: int | None = None,
) -> UpgradeApplyResult:
    """Apply the combined managed-asset and schema plan as one transaction."""
    plan = _build_repository_upgrade_plan(root, selected_agent)
    try:
        _validate_upgrade_apply_plan(root, plan, supplied_fingerprint)
        _require_clean_git_worktree(root)
        if not plan["target_files"]:
            result = _upgrade_apply_result(plan=plan, status="noop")
        else:
            asset_outputs, executable_files = _managed_asset_upgrade_outputs(root, selected_agent)
            outputs = _compute_upgrade_outputs(
                root,
                plan,
                PRODUCTION_MIGRATION_HANDLERS,
                initial_outputs=asset_outputs,
            )
            actual_outputs = [
                {
                    "artifact": target,
                    "expected": _upgrade_content_hash(outputs[target]),
                }
                for target in plan["target_files"]
            ]
            if actual_outputs != plan["expected_outputs"]:
                raise UpgradeApplyFailure(
                    "PW_UPGRADE_APPLY_STALE_PLAN",
                    "Computed managed-asset or migration outputs do not match the reviewed plan.",
                )
            if list(executable_files) != plan["executable_files"]:
                raise UpgradeApplyFailure(
                    "PW_UPGRADE_APPLY_STALE_PLAN",
                    "Computed executable targets do not match the reviewed plan.",
                )
            _validate_upgrade_apply_plan(root, plan, supplied_fingerprint)
            _require_clean_git_worktree(root)
            changed_files = _apply_upgrade_outputs(
                root,
                outputs,
                executable_files=executable_files,
                fail_after_replacements=fail_after_replacements,
            )
            result = _upgrade_apply_result(
                plan=plan,
                status="applied",
                changed_files=changed_files,
            )
        post_compatibility = _repository_compatibility(root)
        post_issues = run_doctor(root)
        result["post_upgrade"] = {
            "repository_state": post_compatibility.state,
            "finding_count": len(post_issues),
            "owner_finding_count": sum(issue.remediation_owner == "owner" for issue in post_issues),
        }
        return result
    except UpgradeApplyFailure as failure:
        return _upgrade_apply_result(plan=plan, status="failed", failure=failure)


def _format_upgrade_apply_human(result: UpgradeApplyResult) -> str:
    lines = [
        f"project upgrade apply: {result['status']}",
        f"plan fingerprint: {result['plan_fingerprint']}",
    ]
    if result["applied_migrations"]:
        lines.append("applied migrations: " + ", ".join(result["applied_migrations"]))
    if result["changed_files"]:
        lines.append("changed files: " + ", ".join(result["changed_files"]))
    if result["noop"]:
        lines.append("no changes required")
    if result["failure"]:
        lines.append(f"failure: {result['failure']['code']}: {result['failure']['message']}")
    post_upgrade = result.get("post_upgrade")
    if post_upgrade:
        lines.append(
            "post-upgrade validation: "
            f"{post_upgrade['repository_state']}; "
            f"{post_upgrade['finding_count']} finding(s), "
            f"{post_upgrade['owner_finding_count']} owner-owned"
        )
    return "\n".join(lines)


def _smoke_bomb_hash(content: bytes | None) -> str:
    if content is None:
        return ABSENT_FILE_HASH
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _smoke_bomb_git_optional(args: list[str], root: Path) -> str | None:
    try:
        return _run_git(args, cwd=root)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _smoke_bomb_repository_identity(
    root: Path,
) -> tuple[SmokeBombRepositoryRecord, list[SmokeBombBlocker]]:
    blockers: list[SmokeBombBlocker] = []
    top_level = _smoke_bomb_git_optional(["rev-parse", "--show-toplevel"], root)
    branch = _smoke_bomb_git_optional(["branch", "--show-current"], root)
    commit = _smoke_bomb_git_optional(["rev-parse", "HEAD"], root)
    if top_level is None or branch is None or commit is None:
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_AMBIGUOUS_ROOT",
                "Smoke Bomb requires an existing Git worktree with a current commit and branch.",
            )
        )
        return {
            "root": str(root),
            "top_level": top_level,
            "branch": branch,
            "commit": commit,
            "default_branch": None,
            "on_default_branch": False,
        }, blockers

    resolved_top = Path(top_level).resolve()
    if resolved_top != root:
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_AMBIGUOUS_ROOT",
                f"Requested root {root} is not the Git worktree root {resolved_top}.",
            )
        )

    remote_default = _smoke_bomb_git_optional(
        ["symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"], root
    )
    default_branch = remote_default.removeprefix("origin/") if remote_default else None
    if default_branch is None and branch in {"main", "master"}:
        default_branch = branch
    return {
        "root": str(root),
        "top_level": str(resolved_top),
        "branch": branch,
        "commit": commit,
        "default_branch": default_branch,
        "on_default_branch": bool(default_branch and branch == default_branch),
    }, blockers


def _smoke_bomb_remove_managed_block(content: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(MANAGED_BLOCK_START)}\n.*?^{re.escape(MANAGED_BLOCK_END)}(?:\n)?",
        flags=re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(content)
    if not match:
        return content
    before = content[: match.start()].rstrip("\n")
    after = content[match.end() :].lstrip("\n")
    if before and after:
        return f"{before}\n\n{after}"
    if before:
        return before + "\n"
    return after


def _smoke_bomb_useful_markdown(content: str) -> bool:
    stripped = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL).strip()
    if len(stripped) < 80:
        return False
    placeholders = (
        "Describe the user outcome",
        "Add local conventions, validation commands",
        "As a ____, I want ____, so that ____",
        "____",
    )
    return not any(value in stripped for value in placeholders)


def _smoke_bomb_client_agents_text(guidance: str, validation_commands: tuple[str, ...]) -> str:
    guidance_body = guidance.strip()
    if guidance_body.startswith("# Project Workflow Guidance"):
        guidance_body = guidance_body.removeprefix("# Project Workflow Guidance").strip()
    validations = "\n".join(f"- `{command}`" for command in validation_commands)
    return (
        "# Agent Instructions\n\n"
        "Read `README.md` before changing the project. Treat the repository's existing "
        "architecture and conventions as authoritative, and preserve user-owned content.\n\n"
        "## Repository Guidance\n\n"
        f"{guidance_body}\n\n"
        "## Validation\n\n"
        f"{validations}\n"
    )


def _smoke_bomb_adapter_text(agent: str) -> str:
    if agent == "claude-code":
        return (
            "# Claude Code Instructions\n\n"
            "Read `README.md` and `AGENTS.md` before making changes. "
            "Follow the repository guidance and validation commands in `AGENTS.md`.\n"
        )
    if agent == "cursor":
        return (
            "---\ndescription: Client project guidance\nalwaysApply: true\n---\n\n"
            "Read `README.md` and `AGENTS.md` before making changes. "
            "Follow the repository guidance and validation commands in `AGENTS.md`.\n"
        )
    if agent == "github-copilot":
        return (
            "# GitHub Copilot Instructions\n\n"
            "Read `README.md` and `AGENTS.md` before making changes. "
            "Follow the repository guidance and validation commands in `AGENTS.md`.\n"
        )
    return ""


def _smoke_bomb_generated_asset_paths(root: Path) -> set[Path]:
    candidates: set[Path] = set()
    for skill_name in CODEX_SKILL_NAMES:
        candidates.add(root / ".agents" / "skills" / skill_name / "SKILL.md")
    for prompt_file in PROMPT_FILES:
        name = _prompt_filename_to_agent_name(prompt_file)
        candidates.add(root / ".claude" / "agents" / f"{name}.md")
        candidates.add(root / ".cursor" / "agents" / f"{name}.md")
        candidates.add(root / ".github" / "prompts" / prompt_file)
    candidates.add(root / ".cursor" / "rules" / "project-workflow.mdc")

    expanded = set(candidates)
    for candidate in tuple(candidates):
        parent = candidate.parent
        if not parent.is_dir():
            continue
        for sibling in parent.glob(f"{candidate.name}.new*"):
            expanded.add(sibling)
    return expanded


def _smoke_bomb_action(
    root: Path,
    path: Path,
    after: bytes | None,
    *,
    reason: str,
    ownership: str,
    source: str,
) -> tuple[SmokeBombActionRecord, bytes | None]:
    relative = path.relative_to(root).as_posix()
    before = path.read_bytes() if path.exists() and path.is_file() else None
    return {
        "path": relative,
        "action": "delete" if after is None else ("create" if before is None else "replace"),
        "before_sha256": _smoke_bomb_hash(before),
        "after_sha256": _smoke_bomb_hash(after),
        "reason": reason,
        "ownership": ownership,
        "source": source,
    }, after


def _smoke_bomb_target_is_safe(root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(root)
        path.resolve(strict=False).relative_to(root)
    except ValueError:
        return False
    current = root
    for part in relative.parts[:-1]:
        current /= part
        if current.is_symlink() or (current.exists() and not current.is_dir()):
            return False
    return not path.is_symlink() and (not path.exists() or path.is_file())


def _smoke_bomb_plan_outputs(
    root: Path,
    client_agents: tuple[str, ...],
    validation_commands: tuple[str, ...],
) -> tuple[list[SmokeBombActionRecord], dict[str, bytes | None], list[SmokeBombBlocker]]:
    actions: list[SmokeBombActionRecord] = []
    outputs: dict[str, bytes | None] = {}
    blockers: list[SmokeBombBlocker] = []

    def record(
        path: Path, after: bytes | None, *, reason: str, ownership: str, source: str
    ) -> None:
        if not _smoke_bomb_target_is_safe(root, path):
            blockers.append(
                SmokeBombBlocker(
                    "PW_SMOKE_BOMB_UNSAFE_TARGET",
                    f"Planned target must be a regular file or absent: {path.relative_to(root)}.",
                )
            )
            return
        action, content = _smoke_bomb_action(
            root, path, after, reason=reason, ownership=ownership, source=source
        )
        if action["before_sha256"] != action["after_sha256"]:
            actions.append(action)
            outputs[action["path"]] = content

    workflow_dir = root / ".project-workflow"
    private_runtime_dir = root / DELEGATION_RUNTIME_RELATIVE_DIR
    private_runtime_present = private_runtime_dir.is_dir() and any(
        path.is_file() or path.is_symlink() for path in private_runtime_dir.rglob("*")
    )
    if private_runtime_present:
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_PRIVATE_RUNTIME_PRESENT",
                "Machine-local delegation runtime exists. Clear it outside the retained Smoke "
                "Bomb evidence flow before planning or export; private handle paths are redacted.",
            )
        )
    if (
        not _smoke_bomb_target_is_safe(root, workflow_dir / "sentinel")
        or workflow_dir.is_symlink()
        or (workflow_dir.exists() and not workflow_dir.is_dir())
    ):
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_UNSAFE_TARGET",
                ".project-workflow must be a real directory or absent.",
            )
        )
    elif workflow_dir.is_dir():
        for path in sorted(workflow_dir.rglob("*")):
            if path == private_runtime_dir or private_runtime_dir in path.parents:
                continue
            if path.is_symlink() or (path.exists() and not path.is_file() and not path.is_dir()):
                blockers.append(
                    SmokeBombBlocker(
                        "PW_SMOKE_BOMB_UNSAFE_TARGET",
                        f"Unsafe project-workflow entry: {path.relative_to(root)}.",
                    )
                )
            elif path.is_file():
                record(
                    path,
                    None,
                    reason="Remove agency-owned project-workflow internal state.",
                    ownership="project-workflow-directory",
                    source=".project-workflow",
                )

    ignore_path = root / ".gitignore"
    if ignore_path.is_file() and not ignore_path.is_symlink():
        try:
            ignore_lines = ignore_path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            ignore_lines = []
        runtime_comment = "# Machine-local delegation handles and leases"
        runtime_entry = f"{DELEGATION_RUNTIME_RELATIVE_DIR.as_posix()}/"
        sanitized_lines = [
            line for line in ignore_lines if line.strip() not in {runtime_comment, runtime_entry}
        ]
        while sanitized_lines and not sanitized_lines[-1].strip():
            sanitized_lines.pop()
        sanitized_ignore = ("\n".join(sanitized_lines) + "\n").encode("utf-8")
        record(
            ignore_path,
            sanitized_ignore,
            reason="Remove the ignored project-workflow runtime-state boundary from client output.",
            ownership="project-workflow-ignore-entry",
            source=runtime_entry,
        )

    for path in sorted(_smoke_bomb_generated_asset_paths(root)):
        if not path.exists():
            continue
        if not _smoke_bomb_target_is_safe(root, path):
            blockers.append(
                SmokeBombBlocker(
                    "PW_SMOKE_BOMB_UNSAFE_TARGET",
                    f"Generated asset target is unsafe: {path.relative_to(root)}.",
                )
            )
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            content = ""
        if not _is_generated_content(content):
            blockers.append(
                SmokeBombBlocker(
                    "PW_SMOKE_BOMB_UNSAFE_TARGET",
                    f"Known generated path lacks ownership marker: {path.relative_to(root)}.",
                )
            )
            continue
        record(
            path,
            None,
            reason="Remove generated project-workflow agent surface.",
            ownership="generated-marker",
            source=GENERATED_MARKER,
        )

    guidance_path = workflow_dir / "guidance.md"
    guidance = ""
    if guidance_path.is_file():
        try:
            guidance = guidance_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            guidance = ""

    agents_path = root / "AGENTS.md"
    existing_agents = ""
    if agents_path.is_file() and not agents_path.is_symlink():
        try:
            existing_agents = agents_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            existing_agents = ""
    stripped_agents = _smoke_bomb_remove_managed_block(existing_agents)
    if _smoke_bomb_useful_markdown(stripped_agents):
        client_agents_text = stripped_agents
        agent_source = "existing AGENTS.md outside the managed block"
    elif stripped_agents.strip():
        client_agents_text = stripped_agents
        agent_source = "existing AGENTS.md outside the managed block"
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_CLIENT_GUIDANCE_REQUIRED",
                "Existing user-authored AGENTS.md content is too limited for client handoff; "
                "review and improve it rather than allowing Smoke Bomb to replace it.",
            )
        )
    elif _smoke_bomb_useful_markdown(guidance):
        client_agents_text = _smoke_bomb_client_agents_text(guidance, validation_commands)
        agent_source = ".project-workflow/guidance.md and reviewed validation commands"
    else:
        client_agents_text = ""
        agent_source = "missing"
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_CLIENT_GUIDANCE_REQUIRED",
                "Useful client agent guidance is missing. Add substantive content outside the "
                "managed AGENTS.md block or to .project-workflow/guidance.md and re-plan.",
            )
        )
    if client_agents_text:
        record(
            agents_path,
            client_agents_text.encode("utf-8"),
            reason="Preserve one canonical client-facing agent guide.",
            ownership="mixed-host-file",
            source=agent_source,
        )

    adapter_paths = {
        "claude-code": root / "CLAUDE.md",
        "cursor": root / ".cursor" / "rules" / "client-project.mdc",
        "github-copilot": root / ".github" / "copilot-instructions.md",
    }
    for agent in client_agents:
        if agent == "codex":
            continue
        path = adapter_paths[agent]
        existing = ""
        if path.is_file() and not path.is_symlink():
            try:
                existing = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                existing = ""
        stripped = _smoke_bomb_remove_managed_block(existing)
        if _smoke_bomb_useful_markdown(stripped):
            after_text = stripped
        elif stripped.strip():
            after_text = stripped
            blockers.append(
                SmokeBombBlocker(
                    "PW_SMOKE_BOMB_CLIENT_GUIDANCE_REQUIRED",
                    f"Existing user-authored {path.relative_to(root)} is too limited for client "
                    "handoff; review and improve it rather than allowing replacement.",
                )
            )
        else:
            after_text = _smoke_bomb_adapter_text(agent)
        record(
            path,
            after_text.encode("utf-8"),
            reason=f"Provide client-facing instructions for {AGENT_CHOICES[agent]}.",
            ownership="client-agent-adapter",
            source="AGENTS.md",
        )

    copilot_path = root / ".github" / "copilot-instructions.md"
    if "github-copilot" not in client_agents and copilot_path.is_file():
        try:
            current = copilot_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            current = ""
        stripped = _smoke_bomb_remove_managed_block(current)
        record(
            copilot_path,
            stripped.encode("utf-8") if stripped else None,
            reason="Remove only the project-workflow managed host block.",
            ownership="mixed-host-file",
            source=MANAGED_BLOCK_START,
        )

    readme_path = root / "README.md"
    readme = ""
    if readme_path.is_file() and not readme_path.is_symlink():
        try:
            readme = readme_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            readme = ""
    if not _smoke_bomb_useful_markdown(readme):
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_CLIENT_GUIDANCE_REQUIRED",
                "A substantive client-facing README.md is required before sanitization.",
            )
        )
    return sorted(actions, key=lambda item: str(item["path"])), outputs, blockers


def _smoke_bomb_dirty(root: Path) -> bool:
    status = _smoke_bomb_git_optional(["status", "--porcelain"], root)
    return status is None or bool(status)


def _smoke_bomb_planned_archive(
    root: Path,
    outputs: dict[str, bytes | None],
    client_agents: tuple[str, ...],
) -> tuple[list[str], list[SmokeBombBlocker]]:
    blockers: list[SmokeBombBlocker] = []
    try:
        inventory = set(_smoke_bomb_inventory(root))
    except SmokeBombFailure:
        return [], blockers
    for relative, content in outputs.items():
        if content is None:
            inventory.discard(relative)
        else:
            inventory.add(relative)
    planned = sorted(inventory)
    residuals: list[str] = []
    for relative in planned:
        path = root / relative
        content = outputs.get(relative)
        if relative not in outputs:
            if path.is_symlink() or not path.is_file():
                blockers.append(
                    SmokeBombBlocker(
                        "PW_SMOKE_BOMB_UNSAFE_TARGET",
                        f"Unsafe archive file type requires resolution: {relative}.",
                    )
                )
                continue
            if path.stat().st_size > 2_000_000:
                continue
            try:
                content = path.read_bytes()
            except OSError:
                content = None
        if _smoke_bomb_secret_like(relative):
            blockers.append(
                SmokeBombBlocker(
                    "PW_SMOKE_BOMB_UNSAFE_TARGET",
                    f"Secret-like path requires explicit removal or review: {relative}.",
                )
            )
        if content is None:
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if "project-workflow" in text or ".project-workflow" in text:
            residuals.append(relative)
    if residuals:
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_RESIDUAL_REFERENCE",
                "Unclassified project-workflow references would remain in the ZIP: "
                + ", ".join(residuals),
            )
        )
    required_guidance = {"README.md", "AGENTS.md"}
    adapter_paths = {
        "claude-code": "CLAUDE.md",
        "cursor": ".cursor/rules/client-project.mdc",
        "github-copilot": ".github/copilot-instructions.md",
    }
    required_guidance.update(
        adapter_paths[agent] for agent in client_agents if agent in adapter_paths
    )
    inventory_set = set(planned)
    for relative in sorted(required_guidance):
        content = outputs.get(relative)
        if relative not in outputs:
            path = root / relative
            try:
                content = path.read_bytes()
            except OSError:
                content = None
        if content is None:
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if "____" in text or re.search(r"\b(?:TODO|TBD)\b", text):
            blockers.append(
                SmokeBombBlocker(
                    "PW_SMOKE_BOMB_CLIENT_GUIDANCE_REQUIRED",
                    f"Client guidance contains an unresolved placeholder: {relative}.",
                )
            )
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith(("#", "mailto:")):
                continue
            decoded = target.replace("%20", " ")
            resolved = (root / relative).parent.joinpath(decoded).resolve()
            try:
                target_relative = resolved.relative_to(root).as_posix()
            except ValueError:
                target_relative = ""
            target_present = target_relative in inventory_set or any(
                value.startswith(target_relative.rstrip("/") + "/") for value in inventory_set
            )
            if not target_relative or not target_present:
                blockers.append(
                    SmokeBombBlocker(
                        "PW_SMOKE_BOMB_CLIENT_GUIDANCE_REQUIRED",
                        f"Client guidance link would be broken: {relative} -> {target}.",
                    )
                )
    return planned, blockers


def _build_smoke_bomb_plan(
    root: Path,
    client_agents: tuple[str, ...],
    validation_commands: tuple[str, ...],
    output_path: Path,
) -> tuple[SmokeBombPlan, dict[str, bytes | None]]:
    identity, blockers = _smoke_bomb_repository_identity(root)
    if not validation_commands:
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_VALIDATION_REQUIRED",
                "At least one explicit --validation-command is required.",
            )
        )
    try:
        output_path.relative_to(root)
    except ValueError:
        pass
    else:
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_OUTPUT_UNSAFE",
                "The ZIP output must be outside the repository root.",
            )
        )
    if _smoke_bomb_dirty(root):
        blockers.append(
            SmokeBombBlocker(
                "PW_SMOKE_BOMB_DIRTY_WORKTREE",
                "Smoke Bomb apply requires a clean worktree, including no untracked files.",
            )
        )
    actions, outputs, output_blockers = _smoke_bomb_plan_outputs(
        root, client_agents, validation_commands
    )
    blockers.extend(output_blockers)
    planned_inventory, archive_blockers = _smoke_bomb_planned_archive(root, outputs, client_agents)
    blockers.extend(archive_blockers)
    plan: SmokeBombPlan = {
        "schema_version": SMOKE_BOMB_PLAN_SCHEMA_VERSION,
        "operation": "smoke-bomb",
        "package_version": CURRENT_PACKAGE_VERSION,
        "repository": identity,
        "workflow_installed": (root / ".project-workflow").is_dir(),
        "client_agents": list(client_agents),
        "validation_commands": list(validation_commands),
        "output_path": str(output_path),
        "actions": actions,
        "archive": {
            "source": "git tracked and non-ignored existing files after apply",
            "excluded": [".git", "ignored files", "unsafe or secret-like paths", "output ZIP"],
            "included_paths": planned_inventory,
            "entry_count": len(planned_inventory),
        },
        "warnings": (
            ["Current branch appears to be the default branch; use a disposable Smoke Bomb branch."]
            if identity["on_default_branch"]
            else []
        ),
        "blockers": [
            {"code": blocker.code, "message": blocker.message}
            for blocker in sorted(blockers, key=lambda value: (value.code, value.message))
        ],
    }
    fingerprint_payload = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode("utf-8")
    plan["plan_fingerprint"] = hashlib.sha256(fingerprint_payload).hexdigest()
    return plan, outputs


def _format_smoke_bomb_plan_human(plan: SmokeBombPlan) -> str:
    repository = plan["repository"]
    lines = [
        "project smoke-bomb plan",
        f"repository: {repository['root']}",
        f"branch: {repository['branch']} @ {repository['commit']}",
        f"plan fingerprint: {plan['plan_fingerprint']}",
        "client agents: " + ", ".join(plan["client_agents"]),
        f"output ZIP: {plan['output_path']}",
        f"planned actions: {len(plan['actions'])}",
    ]
    for warning in plan["warnings"]:
        lines.append(f"warning: {warning}")
    for action in plan["actions"]:
        lines.append(f"- {action['action']}: {action['path']} ({action['reason']})")
    for blocker in plan["blockers"]:
        lines.append(f"blocker: {blocker['code']}: {blocker['message']}")
    if not plan["blockers"]:
        lines.append(
            "Apply this exact plan with --apply --plan-fingerprint "
            f"{plan['plan_fingerprint']} (add --yes for authorized non-interactive use)."
        )
    return "\n".join(lines)


def _smoke_bomb_remove_empty_managed_dirs(root: Path) -> None:
    candidates = (
        root / ".project-workflow",
        root / ".agents" / "skills",
        root / ".agents",
        root / ".claude" / "agents",
        root / ".claude",
        root / ".cursor" / "agents",
        root / ".github" / "prompts",
    )
    for candidate in candidates:
        if not candidate.is_dir() or candidate.is_symlink():
            continue
        for directory in sorted(
            (path for path in candidate.rglob("*") if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            try:
                directory.rmdir()
            except OSError:
                pass
        try:
            candidate.rmdir()
        except OSError:
            pass


def _smoke_bomb_run_validations(
    root: Path, validation_commands: tuple[str, ...]
) -> list[SmokeBombValidationRecord]:
    results: list[SmokeBombValidationRecord] = []
    for command in validation_commands:
        completed = subprocess.run(
            command,
            cwd=root,
            shell=True,
            executable="/bin/sh",
            check=False,
            capture_output=True,
            text=True,
        )
        result: SmokeBombValidationRecord = {
            "command": command,
            "exit_code": completed.returncode,
            "stdout_bytes": len(completed.stdout.encode("utf-8")),
            "stdout_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
            "stderr_bytes": len(completed.stderr.encode("utf-8")),
            "stderr_sha256": hashlib.sha256(completed.stderr.encode("utf-8")).hexdigest(),
        }
        results.append(result)
        if completed.returncode != 0:
            raise SmokeBombFailure(
                "PW_SMOKE_BOMB_VALIDATION_FAILED",
                f"Reviewed validation command failed ({completed.returncode}): {command}",
            )
    return results


def _smoke_bomb_inventory(root: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise SmokeBombFailure(
            "PW_SMOKE_BOMB_ARCHIVE_BLOCKED",
            "Unable to inventory tracked and non-ignored worktree files.",
        ) from exc
    paths = sorted({value.decode("utf-8") for value in completed.stdout.split(b"\0") if value})
    return [relative for relative in paths if (root / relative).exists()]


def _smoke_bomb_secret_like(relative: str) -> bool:
    path = Path(relative)
    lower_name = path.name.lower()
    if lower_name == ".env.example" or lower_name.endswith(".example"):
        return False
    if lower_name == ".env" or lower_name.startswith(".env."):
        return True
    if path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
        return True
    return lower_name in {
        "id_rsa",
        "id_ed25519",
        "credentials.json",
        "service-account.json",
        "secrets.json",
    }


def _smoke_bomb_markdown_issues(root: Path, relative: str) -> list[str]:
    path = root / relative
    if path.suffix.lower() not in {".md", ".mdc"}:
        return []
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return [f"Client guidance is unreadable: {relative}"]
    issues: list[str] = []
    if "____" in content or re.search(r"\b(?:TODO|TBD)\b", content):
        issues.append(f"Client guidance contains an unresolved placeholder: {relative}")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
        target = target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("#", "mailto:")):
            continue
        decoded_target = target.replace("%20", " ")
        resolved = (path.parent / decoded_target).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            issues.append(f"Client guidance link escapes the repository: {relative} -> {target}")
            continue
        if not resolved.exists():
            issues.append(f"Client guidance link is broken: {relative} -> {target}")
    return issues


def _smoke_bomb_validate_inventory(
    root: Path,
    inventory: list[str],
    client_agents: tuple[str, ...],
) -> list[str]:
    issues: list[str] = []
    required = {"README.md", "AGENTS.md"}
    adapters = {
        "claude-code": "CLAUDE.md",
        "cursor": ".cursor/rules/client-project.mdc",
        "github-copilot": ".github/copilot-instructions.md",
    }
    required.update(adapters[agent] for agent in client_agents if agent in adapters)
    missing = sorted(required - set(inventory))
    if missing:
        issues.append("Required client guidance is missing: " + ", ".join(missing))
    if any(relative == ".git" or relative.startswith(".git/") for relative in inventory):
        issues.append("Git metadata is present in the archive inventory.")
    for relative in inventory:
        path = root / relative
        if path.is_symlink() or not path.is_file():
            issues.append(f"Unsafe archive file type: {relative}")
        if relative == ".project-workflow" or relative.startswith(".project-workflow/"):
            issues.append(f"Project-workflow internal state remains: {relative}")
        if _smoke_bomb_secret_like(relative):
            issues.append(f"Secret-like path requires explicit removal or review: {relative}")
        if relative in required:
            issues.extend(_smoke_bomb_markdown_issues(root, relative))
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if not _smoke_bomb_useful_markdown(content):
                issues.append(f"Client guidance is not substantive: {relative}")
    residuals: list[str] = []
    for relative in inventory:
        path = root / relative
        if path.stat().st_size > 2_000_000:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "project-workflow" in content or ".project-workflow" in content:
            residuals.append(relative)
    if residuals:
        issues.append(
            "Unclassified project-workflow references remain: " + ", ".join(sorted(residuals))
        )
    return issues


def _smoke_bomb_changed_paths(root: Path) -> set[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    paths: set[str] = set()
    entries = [entry for entry in completed.stdout.split(b"\0") if entry]
    index = 0
    while index < len(entries):
        entry = entries[index].decode("utf-8")
        status = entry[:2]
        paths.add(entry[3:])
        if "R" in status or "C" in status:
            index += 1
            if index < len(entries):
                paths.add(entries[index].decode("utf-8"))
        index += 1
    return paths


def _smoke_bomb_write_zip(
    root: Path, output_path: Path, inventory: list[str]
) -> SmokeBombArchiveResult:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.", suffix=".tmp", dir=output_path.parent
    )
    os.close(descriptor)
    temp_path = Path(temp_name)
    try:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for relative in inventory:
                path = root / relative
                info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                mode = path.stat().st_mode & 0o777
                info.external_attr = ((0o100000 | mode) & 0xFFFF) << 16
                archive.writestr(info, path.read_bytes())
        archive_sha256 = _sha256_file(temp_path)
        if output_path.exists() and _sha256_file(output_path) == archive_sha256:
            temp_path.unlink()
        else:
            os.replace(temp_path, output_path)
        return {
            "path": str(output_path),
            "sha256": archive_sha256,
            "entries": inventory,
            "entry_count": len(inventory),
        }
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _apply_smoke_bomb_plan(
    root: Path,
    plan: SmokeBombPlan,
    outputs: dict[str, bytes | None],
    supplied_fingerprint: str,
    *,
    fail_after_replacements: int | None = None,
) -> SmokeBombResult:
    base_result: SmokeBombResult = {
        "schema_version": SMOKE_BOMB_RESULT_SCHEMA_VERSION,
        "status": "failed",
        "plan_fingerprint": plan["plan_fingerprint"],
        "repository": plan["repository"],
        "client_agents": plan["client_agents"],
        "changed_files": [],
        "validation": [],
        "archive": None,
        "failure": None,
    }
    try:
        if supplied_fingerprint != plan["plan_fingerprint"]:
            raise SmokeBombFailure(
                "PW_SMOKE_BOMB_APPLY_STALE_PLAN",
                "Supplied plan fingerprint does not match the current deterministic plan.",
            )
        if plan["blockers"]:
            raise SmokeBombFailure(
                "PW_SMOKE_BOMB_APPLY_BLOCKED",
                "The current Smoke Bomb plan contains blockers.",
            )
        expected_outputs = {action["path"] for action in plan["actions"]}
        if expected_outputs != set(outputs):
            raise SmokeBombFailure(
                "PW_SMOKE_BOMB_APPLY_STALE_PLAN",
                "Computed outputs do not match the reviewed action inventory.",
            )
        try:
            changed = _apply_upgrade_outputs(
                root,
                outputs,
                fail_after_replacements=fail_after_replacements,
            )
        except UpgradeApplyFailure as exc:
            raise SmokeBombFailure("PW_SMOKE_BOMB_APPLY_FAILED", exc.message) from exc
        _smoke_bomb_remove_empty_managed_dirs(root)
        base_result["changed_files"] = changed
        validations = _smoke_bomb_run_validations(
            root, tuple(str(value) for value in plan["validation_commands"])
        )
        base_result["validation"] = validations
        actual_changed = _smoke_bomb_changed_paths(root)
        if actual_changed != set(changed):
            unexpected = sorted(actual_changed.symmetric_difference(set(changed)))
            raise SmokeBombFailure(
                "PW_SMOKE_BOMB_ARCHIVE_BLOCKED",
                "The post-validation worktree differs from the reviewed plan: "
                + ", ".join(unexpected),
            )
        stale_outputs: list[str] = []
        for action in plan["actions"]:
            path = root / action["path"]
            if path.exists() and (path.is_symlink() or not path.is_file()):
                actual_hash = "not-a-file"
            else:
                actual_content = path.read_bytes() if path.exists() else None
                actual_hash = _smoke_bomb_hash(actual_content)
            if actual_hash != action["after_sha256"]:
                stale_outputs.append(action["path"])
        if stale_outputs:
            raise SmokeBombFailure(
                "PW_SMOKE_BOMB_ARCHIVE_BLOCKED",
                "Post-validation content differs from the reviewed plan: "
                + ", ".join(sorted(stale_outputs)),
            )
        inventory = _smoke_bomb_inventory(root)
        planned_inventory = list(plan["archive"]["included_paths"])
        if inventory != planned_inventory:
            changed_inventory = sorted(set(inventory).symmetric_difference(planned_inventory))
            raise SmokeBombFailure(
                "PW_SMOKE_BOMB_ARCHIVE_BLOCKED",
                "The final archive inventory differs from the reviewed plan: "
                + ", ".join(changed_inventory),
            )
        inventory_issues = _smoke_bomb_validate_inventory(
            root, inventory, tuple(str(value) for value in plan["client_agents"])
        )
        if inventory_issues:
            raise SmokeBombFailure(
                "PW_SMOKE_BOMB_ARCHIVE_BLOCKED",
                " ".join(inventory_issues),
            )
        archive = _smoke_bomb_write_zip(root, Path(str(plan["output_path"])), inventory)
        archive["source_repository"] = plan["repository"]
        archive["plan_fingerprint"] = plan["plan_fingerprint"]
        archive["client_agents"] = plan["client_agents"]
        archive["exclusions"] = plan["archive"]["excluded"]
        base_result["archive"] = archive
        base_result["status"] = "exported"
    except SmokeBombFailure as failure:
        base_result["failure"] = {"code": failure.code, "message": failure.message}
    return base_result


def _format_smoke_bomb_result_human(result: SmokeBombResult) -> str:
    lines = [
        f"project smoke-bomb: {result['status']}",
        f"plan fingerprint: {result['plan_fingerprint']}",
    ]
    if result["changed_files"]:
        lines.append("changed files: " + ", ".join(result["changed_files"]))
    for validation in result["validation"]:
        lines.append(f"validation ({validation['exit_code']}): {validation['command']}")
    if result["archive"]:
        lines.append(f"ZIP: {result['archive']['path']}")
        lines.append(f"SHA-256: {result['archive']['sha256']}")
        lines.append(f"entries: {result['archive']['entry_count']}")
    if result["failure"]:
        lines.append(f"failure: {result['failure']['code']}: {result['failure']['message']}")
    return "\n".join(lines)
