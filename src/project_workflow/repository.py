"""Canonical Project Workflow repository runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from datetime import date
from importlib.resources import files
from pathlib import Path

from .contracts import (
    AGENT_CHOICES,
    BACKLOG_ID_PREFIX,
    BACKLOG_PRIORITIES,
    BACKLOG_STATUSES,
    BACKLOG_TYPES,
    CANONICAL_INIT_COMMAND,
    CANONICAL_UPGRADE_COMMAND,
    CURRENT_ASSET_VERSION,
    CURRENT_MANIFEST_VERSION,
    CURRENT_PACKAGE_VERSION,
    CURRENT_SCHEMA_VERSION,
    DECOMPOSITION_PLAN_COLUMNS,
    DECOMPOSITION_PLAN_FILENAME,
    DEFAULT_ID_GENERATION,
    DEFAULT_PREFIX_GUIDANCE,
    DEFAULT_UNIQUE_ID_LENGTH,
    DELEGATION_DECOMPOSITION_PLAN_COLUMNS,
    DELEGATION_EXECUTION_NEEDS_DECOMPOSITION_PLAN_COLUMNS,
    EPIC_AMENDMENT_COLUMNS,
    EPIC_AMENDMENTS_FILENAME,
    EPIC_CONTRACT_FILENAME,
    EPIC_CONTRACT_PROOF_OWNER_COLUMNS,
    EPIC_CONTRACT_REQUIRED_SECTIONS,
    EPIC_ID_PREFIX,
    FIX_ACTIVE_DISPOSITION,
    FIX_ID_PREFIX,
    GENERATED_MARKER,
    GENERATED_MARKER_COMMENT,
    GENERATED_MARKER_HTML,
    ID_GENERATION_KINDS,
    ID_GENERATION_MODES,
    MANAGED_BLOCK_END,
    MANAGED_BLOCK_START,
    MIGRATION_ID_PATTERN,
    RECOGNIZED_WORKFLOW_PATHS,
    SUPPORTED_ASSET_VERSIONS,
    SUPPORTED_SCHEMA_VERSIONS,
    TASK_ID_PREFIX,
    WORKFLOW_CONFIG_FILENAME,
    WORKFLOW_MANIFEST_FILENAME,
    ManifestValidationError,
    RepositoryCompatibility,
    WorkflowConfig,
    WorkflowManifest,
    WorkspaceDefinition,
    WorkspaceRepository,
)


def _words(value: str) -> list[str]:
    return [w for w in re.split(r"[^A-Za-z0-9]+", value.strip()) if w]


def slug_titlecase_dashes(value: str) -> str:
    parts = [w.capitalize() for w in _words(value)]
    return "-".join(parts) if parts else "Untitled"


def slug_kebab_lower(value: str) -> str:
    parts = [w.lower() for w in _words(value)]
    return "-".join(parts) if parts else "untitled"


def _run_git(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _ensure_clean_git(cwd: Path) -> None:
    status = _run_git(["status", "--porcelain"], cwd=cwd)
    if status:
        raise SystemExit(
            "Refusing to create/switch branches with a dirty working tree. "
            "Commit or stash your changes first."
        )


def _branch_exists(cwd: Path, branch: str) -> bool:
    completed = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=str(cwd),
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def _get_package_resource(resource_path: str) -> str:
    """Load a resource file from the package data."""
    try:
        # Try using importlib.resources for Python 3.9+
        files_ref = files("project_workflow").joinpath(resource_path)
        if hasattr(files_ref, "read_text"):
            return files_ref.read_text(encoding="utf-8")
        else:
            # Fallback for older API
            return files_ref.read_bytes().decode("utf-8")
    except Exception as e:
        raise SystemExit(f"Failed to load package resource {resource_path}: {e}")


def _is_generated_content(content: str) -> bool:
    return GENERATED_MARKER in content


def _markdown_has_frontmatter(content: str) -> re.Match[str] | None:
    return re.match(r"^(---\n.*?\n---\n)(.*)$", content, flags=re.DOTALL)


def _generated_marker_for_path(path: Path) -> str:
    if path.suffix in {".md", ".mdc"}:
        return GENERATED_MARKER_HTML
    return GENERATED_MARKER_COMMENT


def _with_generated_marker(path: Path, content: str) -> str:
    if _is_generated_content(content):
        return content

    marker = _generated_marker_for_path(path)
    if path.suffix in {".md", ".mdc"}:
        frontmatter_match = _markdown_has_frontmatter(content)
        if frontmatter_match:
            frontmatter, body = frontmatter_match.groups()
            return f"{frontmatter}{marker}\n\n{body.lstrip()}"
        return f"{marker}\n\n{content.lstrip()}"

    if content.startswith("#!"):
        first_line, sep, rest = content.partition("\n")
        if sep:
            return f"{first_line}\n{marker}\n{rest}"
    return f"{marker}\n{content.lstrip()}"


def _collision_path(path: Path) -> Path:
    candidate = path.with_name(f"{path.name}.new")
    if not candidate.exists():
        return candidate
    try:
        if _is_generated_content(candidate.read_text(encoding="utf-8")):
            return candidate
    except (OSError, UnicodeDecodeError):
        pass

    counter = 2
    while True:
        numbered = path.with_name(f"{path.name}.new.{counter}")
        if not numbered.exists():
            return numbered
        counter += 1


def _ensure_generated_file(path: Path, content: str, *, executable: bool = False) -> str:
    """Create or refresh a project-workflow-owned generated file without overwriting users."""
    path.parent.mkdir(parents=True, exist_ok=True)
    generated_content = _with_generated_marker(path, content)

    if not path.exists():
        path.write_text(generated_content, encoding="utf-8")
        if executable:
            path.chmod(0o755)
        return f"Created: {path}"

    existing_content = path.read_text(encoding="utf-8")
    if _is_generated_content(existing_content):
        if existing_content != generated_content:
            path.write_text(generated_content, encoding="utf-8")
            action = "Refreshed"
        else:
            action = "Exists"
        if executable:
            path.chmod(0o755)
        return f"{action}: {path}"

    new_path = _collision_path(path)
    new_path.write_text(generated_content, encoding="utf-8")
    if executable:
        new_path.chmod(0o755)
    return f"Kept existing unmarked file and wrote: {new_path}"


def _planned_generated_file(
    path: Path,
    content: str,
    *,
    executable: bool = False,
) -> tuple[Path, bytes, bool]:
    """Return the safe target and bytes that init would write without mutating the repository."""
    generated_content = _with_generated_marker(path, content)
    target = path
    if path.exists():
        try:
            existing_content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            existing_content = ""
        if not _is_generated_content(existing_content):
            target = _collision_path(path)
    return target, generated_content.encode("utf-8"), executable


def _ensure_user_guidance_file(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return f"Exists: {path}"

    path.write_text(
        "# Project Workflow Guidance\n\n"
        "Use this file for repo-specific workflow guidance that should survive "
        "project-workflow init refreshes.\n\n"
        "Add local conventions, validation commands, safety constraints, handoff "
        "rules, and agent notes here.\n",
        encoding="utf-8",
    )
    return f"Created: {path}"


def _default_workflow_config_text() -> str:
    return (
        json.dumps(
            {
                "task_id_prefixes": [TASK_ID_PREFIX],
                "default_task_id_prefix": TASK_ID_PREFIX,
                "id_generation": DEFAULT_ID_GENERATION,
                "unique_id_length": DEFAULT_UNIQUE_ID_LENGTH,
                "accepted_doctor_warnings": [],
                "prefix_guidance": DEFAULT_PREFIX_GUIDANCE,
            },
            indent=2,
        )
        + "\n"
    )


def _ensure_user_config_file(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return f"Exists: {path}"
    path.write_text(_default_workflow_config_text(), encoding="utf-8")
    return f"Created: {path}"


def _ensure_delegation_runtime_ignore(root: Path) -> str:
    ignore_path = root / ".project-workflow" / ".gitignore"
    ignore_path.parent.mkdir(parents=True, exist_ok=True)
    content = ignore_path.read_text(encoding="utf-8") if ignore_path.exists() else ""
    present = {line.strip() for line in content.splitlines()}
    sections = (
        ("# Machine-local delegation handles and leases", "runtime/delegations/"),
        ("# Package-owned Python bytecode", "cli/__pycache__/"),
    )
    missing = [(comment, entry) for comment, entry in sections if entry not in present]
    if not missing:
        return f"Exists: {ignore_path} runtime ignore entries"
    separator = "" if not content or content.endswith("\n") else "\n"
    addition = "\n".join(f"{comment}\n{entry}" for comment, entry in missing)
    ignore_path.write_text(
        content + separator + ("\n" if content else "") + addition + "\n",
        encoding="utf-8",
    )
    return f"Updated: {ignore_path} runtime ignore entries"


def _planned_delegation_runtime_ignore(root: Path) -> bytes:
    ignore_path = root / ".project-workflow" / ".gitignore"
    content = ignore_path.read_text(encoding="utf-8") if ignore_path.exists() else ""
    present = {line.strip() for line in content.splitlines()}
    sections = (
        ("# Machine-local delegation handles and leases", "runtime/delegations/"),
        ("# Package-owned Python bytecode", "cli/__pycache__/"),
    )
    missing = [(comment, entry) for comment, entry in sections if entry not in present]
    if not missing:
        return content.encode("utf-8")
    separator = "" if not content or content.endswith("\n") else "\n"
    addition = "\n".join(f"{comment}\n{entry}" for comment, entry in missing)
    return (content + separator + ("\n" if content else "") + addition + "\n").encode("utf-8")


def _managed_project_workflow_block() -> str:
    return (
        f"{MANAGED_BLOCK_START}\n"
        "## Project Workflow\n\n"
        "This repository uses project-workflow. Keep workflow state in "
        "`.project-workflow/BACKLOG.md`, `.project-workflow/TRACKER.md`, "
        "and `.project-workflow/tasks/`.\n\n"
        "- Read repo-specific workflow guidance from `.project-workflow/guidance.md`.\n"
        "- Use `.project-workflow/BACKLOG.md` for optional future intent before work is "
        "promoted into task or epic execution state. Promoted rows stay in the backlog; "
        "active execution status belongs in trackers and task/epic docs.\n"
        "- Read task ID namespace, generation config, and optional parent-workspace registry "
        "from `.project-workflow/config.json`.\n"
        "- In workspace mode, run workflow commands from the parent authority root, keep the "
        "only live workflow state there, and use registered repository IDs in task scope and "
        "evidence. Status Git inspection is read-only and never authorizes cross-repository "
        "mutation.\n"
        f"- To initialize a new repository, run `{CANONICAL_INIT_COMMAND}` from the repository "
        "root with `--agent codex`, `--agent cursor`, `--agent claude-code`, or "
        "`--agent github-copilot`.\n"
        f"- To upgrade an existing repository, run `{CANONICAL_UPGRADE_COMMAND}` with its "
        "agent mode. Authorized non-interactive agents add `--yes`; human invocation confirms "
        "before upgrade applies managed assets plus repository schema together. Do not run init "
        "first.\n"
        "- Use `./.project-workflow/cli/workflow` for supported backlog, Fix, task, epic, "
        "and validation commands.\n"
        "- Run `./.project-workflow/cli/workflow status` for a read-only operational summary "
        "and sourced next action. Use `--id <WORK-ID>` to focus active work, "
        "`--repository <REPOSITORY-ID>` to focus one registered workspace repository, `--strict` to "
        "make visible Doctor warnings blocking, and `--format json` for schema-versioned output. "
        "Status does not replace Doctor diagnosis, canonical upgrade, lifecycle gates, QA, Git "
        "integration, or service verification, and never executes its recommended action.\n"
        "- Route one bounded post-completion correction to a Fix, new outcomes or multiple "
        "independent items to a Task, and coordinated workstreams to an Epic. The user's label "
        "is evidence, not a binding classification. Fixes use one `FIX.md`, the shared tasks "
        "directory, and the global tracker; do not create a separate Fix tracker.\n"
        "- Use Coordinator as the single owner-facing role from conversational intake through "
        "delivery. Delegation is one Coordinator action, not a second role. The Coordinator alone "
        "writes shared workflow state and chooses the smallest sufficient context, execution, and "
        "proof surface for a named delivery need.\n"
        "- Begin current-contract Task and Epic requirements with a one- or two-sentence "
        "plain-language Intent and stable outcome commitments. Before planning, run "
        "`task approval-summary` or `epic approval-summary`, show its Intent/capability/"
        "boundary/proof synopsis, and ask whether that meaning accurately reflects what the "
        "owner wants. Do not ask the owner to approve IDs or hashes as a substitute for "
        "comprehension. Record the confirmation with `task approve-requirements` or "
        "`epic approve-requirements`; unchanged work inside that envelope should proceed "
        "without repeated approval prompts, while drift, stale requirements, or evidence gaps "
        "must be fixed or amended.\n"
        "- Full-contract epics keep sourced OC-to-AC/child/proof coverage and semantic "
        "classifications in `INTENT-AUDIT.json`. Run `epic intent-audit --epic-id <EPIC-ID>` "
        "to inspect `current`, `stale`, `unknown`, `review-required`, or `changes-requested` "
        "state without mutation. Child readiness, Review, and Complete fail closed on any "
        "non-current state; material narrowing, proxy substitution, omission, or broadening "
        "requires restoration or a current owner-approved capability amendment.\n"
        "- After requirements approval, the Coordinator runs Planner and bounded post-plan "
        "Clarify, then `task ready`, and move new tasks to `Ready` autonomously unless material "
        "drift or exceptional risk requires owner input. Clarify supports Epic parents and concrete "
        "Coordinator-routed ambiguity; it is boundary-triggered, not periodic, and never creates a "
        "QA/review loop. `Plan Confirmed` remains legacy-compatible.\n"
        "- For pre-existing work, use `task adopt` or `epic adopt`; pre-adoption inferred "
        "evidence stays untrusted until refreshed.\n"
        "- For epics, `epic decompose` writes `DECOMPOSITION.md`; child rows must match "
        "that plan before approval, scaffold, readiness, or status advancement.\n"
        "- Use `epic amend` for owner-approved mid-epic child rows outside the decomposition "
        "plan; direct tracker edits outside decomposition/amendment authority remain blocked.\n"
        "- New/adopted epics require non-placeholder `EPIC-CONTRACT.md` before "
        "decomposition, child approval/scaffolding, or movement into Ready/In Progress.\n"
        "- If requirements or claims trigger visual/reference, external contract, deployed "
        "artifact, runtime target/source, or responsive visual proof, fill child-local "
        "`EVIDENCE.json`; QA prose, tests, builds, or surrogate artifacts are invalid substitutes.\n"
        "- Use `./.project-workflow/cli/workflow task status --id <TASK-ID> --to <STATUS>` "
        "for tracker lifecycle changes.\n"
        "- Keep version command ownership explicit: init creates a new installation, Doctor "
        "diagnoses without mutation, and canonical UVX upgrade refreshes managed assets and "
        "transforms repository schema in one reviewed transaction. Use `upgrade --plan` and "
        "fingerprinted apply for automation.\n"
        "- For a sanitized client handoff, use canonical `project smoke-bomb` from a clean "
        "dedicated worktree to review exact removal, run explicit validations, preserve useful "
        "client agent guidance, and export a ZIP without Git or workflow internals.\n"
        "- `project-delegate` is the first-release compatibility entry for Coordinator execution "
        "of existing approved rows for exactly one Task or Epic; it does not create another role "
        "or writer. Select the "
        "lightest sufficient coordinator, subagent, persistent-task, or peer-team surface from "
        "approved Execution Needs rather than Task-versus-Epic kind. Resolve surface-specific "
        "isolation, monitoring, reconciliation, retirement, and capacity capabilities as "
        "runtime-observed `verified`, `unsupported`, or `unknown`; only verified capability plus "
        "current-host authority authorizes native launch, otherwise use a safe coordinator/"
        "sequential fallback or block. Never hard-code worker capacity.\n"
        "- In current-contract plans, verified capacity never earns a non-Coordinator surface "
        "alone. Require `benefit:<slug>`, `overhead:<slug>`, and `tradeoff:<slug>`; without all "
        "three, keep non-binding work Coordinator/sequential or block an unmet binding need.\n"
        "- Use `coordinate` durable state for material phase/repository/reframe/context handoffs, "
        "current Intent and source identity, material decisions, context declaration, the five "
        "named drift boundaries, one earliest material real-outcome checkpoint, and next action. "
        "Contract version `2` identifies this Coordinator contract. Keep execution units, "
        "dependencies, packets, returns, and worker lifecycle in the canonical plan and Delegate "
        "only. Repository upgrade never proves a loaded context refreshed; the same physical "
        "context may continue after explicitly loading the current contract when there is no "
        "conflict or isolation need. Existing lifecycle transitions fail closed on missing, "
        "stale, or drifted decisions; handoff, drift, and checkpoints never create QA.\n"
        "- At `coordinate init`, durably classify material verification as required or not required; "
        "required work also records exact claims, stages, and scope. Before any verifier call, use "
        "`coordinate verification-preflight`, then attach the matching exact-candidate campaign to "
        "the existing coordination state. Run canonical cheap-to-expensive stages, certification fail-fast, separately "
        "bounded diagnostics, finite non-waiving limits, input-bound typed receipts, and optional "
        "manual or generic command/JSON adapters. Source changes require fresh affected proof; "
        "evaluator-only changes regrade retained output with zero target calls; infrastructure gets "
        "one bounded retry; unknown material impact requires full proof. The derived "
        "implementation/verification/QA/delivery/blocked projection is read-only and never creates "
        "another lifecycle or QA. Cheap work needs no campaign.\n"
        "- The coordinator alone writes shared workflow state and verifies worker identity, source, "
        "scope, validation, and evidence before satisfying dependencies. A failure blocks its "
        "descendants; unrelated branches continue only while shared premises remain valid. "
        "Temporary visible subordinate tasks retire only after verified durable disposition; "
        "Codex maps retirement to reversible archival, while attention-bearing work stays visible. "
        "Delegate never replaces Implement, independent QA, Epic closeout, owner acceptance, or "
        "delivery proof.\n"
        "- Run `./.project-workflow/cli/workflow doctor` after tracker or task-doc changes.\n"
        f"{MANAGED_BLOCK_END}"
    )


def _ensure_managed_block(path: Path, block: str) -> str:
    """Append or refresh only the project-workflow managed block in a host-owned file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"{block}\n", encoding="utf-8")
        return f"Created managed block: {path}"

    content = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^{re.escape(MANAGED_BLOCK_START)}\n.*?^{re.escape(MANAGED_BLOCK_END)}$",
        flags=re.DOTALL | re.MULTILINE,
    )
    if pattern.search(content):
        updated = pattern.sub(block, content)
        if updated != content:
            path.write_text(updated, encoding="utf-8")
            return f"Refreshed managed block: {path}"
        return f"Exists managed block: {path}"

    separator = "\n\n"
    if content.endswith("\n\n"):
        separator = ""
    elif content.endswith("\n"):
        separator = "\n"
    path.write_text(f"{content}{separator}{block}\n", encoding="utf-8")
    return f"Appended managed block: {path}"


def _planned_managed_block(path: Path, block: str) -> bytes:
    """Return the host-file bytes that managed-block refresh would produce."""
    if not path.exists():
        return f"{block}\n".encode()

    content = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^{re.escape(MANAGED_BLOCK_START)}\n.*?^{re.escape(MANAGED_BLOCK_END)}$",
        flags=re.DOTALL | re.MULTILINE,
    )
    if pattern.search(content):
        return pattern.sub(block, content).encode("utf-8")

    separator = "\n\n"
    if content.endswith("\n\n"):
        separator = ""
    elif content.endswith("\n"):
        separator = "\n"
    return f"{content}{separator}{block}\n".encode()


def _remove_retired_project_workflow_path(path: Path) -> None:
    """Remove known retired project-workflow assets during init."""
    if not path.exists():
        return

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    print(f"✓ Removed retired project-workflow asset: {path}")


def _workflow_config_path(root: Path) -> Path:
    return root / ".project-workflow" / WORKFLOW_CONFIG_FILENAME


def _workflow_manifest_path(root: Path) -> Path:
    return root / ".project-workflow" / WORKFLOW_MANIFEST_FILENAME


def _current_workflow_manifest() -> WorkflowManifest:
    return WorkflowManifest(
        manifest_version=CURRENT_MANIFEST_VERSION,
        package_version=CURRENT_PACKAGE_VERSION,
        asset_version=CURRENT_ASSET_VERSION,
        schema_version=CURRENT_SCHEMA_VERSION,
        applied_migrations=(),
    )


def _workflow_manifest_payload(manifest: WorkflowManifest) -> dict[str, object]:
    return {
        "manifest_version": manifest.manifest_version,
        "package_version": manifest.package_version,
        "asset_version": manifest.asset_version,
        "schema_version": manifest.schema_version,
        "applied_migrations": list(manifest.applied_migrations),
    }


def _serialize_workflow_manifest(manifest: WorkflowManifest) -> str:
    payload = _workflow_manifest_payload(manifest)
    _parse_workflow_manifest(payload)
    return json.dumps(payload, indent=2) + "\n"


def _write_workflow_manifest(path: Path, manifest: WorkflowManifest) -> None:
    if not path.parent.is_dir():
        raise FileNotFoundError(f"Manifest parent directory does not exist: {path.parent}")
    path.write_text(_serialize_workflow_manifest(manifest), encoding="utf-8")


def _manifest_integer(raw: dict[str, object], field: str, *, minimum: int) -> int:
    value = raw[field]
    if type(value) is not int or value < minimum:
        raise ManifestValidationError(f"invalid-{field.replace('_', '-')}")
    return value


def _parse_workflow_manifest(raw: object) -> WorkflowManifest:
    if not isinstance(raw, dict):
        raise ManifestValidationError("invalid-manifest-object")

    required_fields = {
        "manifest_version",
        "package_version",
        "asset_version",
        "schema_version",
        "applied_migrations",
    }
    if set(raw) != required_fields:
        raise ManifestValidationError("invalid-manifest-fields")

    manifest_version = _manifest_integer(raw, "manifest_version", minimum=1)
    package_version = raw["package_version"]
    if not isinstance(package_version, str) or not package_version.strip():
        raise ManifestValidationError("invalid-package-version")

    asset_version = _manifest_integer(raw, "asset_version", minimum=1)
    schema_version = _manifest_integer(raw, "schema_version", minimum=0)

    raw_migrations = raw["applied_migrations"]
    if not isinstance(raw_migrations, list):
        raise ManifestValidationError("invalid-applied-migrations")
    migrations: list[str] = []
    for migration_id in raw_migrations:
        if not isinstance(migration_id, str) or not MIGRATION_ID_PATTERN.fullmatch(migration_id):
            raise ManifestValidationError("invalid-migration-id")
        if migration_id in migrations:
            raise ManifestValidationError("duplicate-migration-id")
        migrations.append(migration_id)

    return WorkflowManifest(
        manifest_version=manifest_version,
        package_version=package_version,
        asset_version=asset_version,
        schema_version=schema_version,
        applied_migrations=tuple(migrations),
    )


def _is_recognized_workflow_repository(root: Path) -> bool:
    workflow_dir = root / ".project-workflow"
    return workflow_dir.is_dir() and any(
        (workflow_dir / relative_path).exists() for relative_path in RECOGNIZED_WORKFLOW_PATHS
    )


def _repository_compatibility(root: Path) -> RepositoryCompatibility:
    manifest_path = _workflow_manifest_path(root)
    if not manifest_path.exists():
        if _is_recognized_workflow_repository(root):
            return RepositoryCompatibility("legacy-unversioned", "manifest-absent")
        return RepositoryCompatibility("not-initialized", "workflow-installation-absent")

    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return RepositoryCompatibility("invalid", "invalid-manifest-json")
    except OSError:
        return RepositoryCompatibility("invalid", "manifest-unreadable")

    if isinstance(raw, dict):
        manifest_version = raw.get("manifest_version")
        if type(manifest_version) is int and manifest_version > CURRENT_MANIFEST_VERSION:
            return RepositoryCompatibility("unsupported-future", "future-manifest-version")

    try:
        manifest = _parse_workflow_manifest(raw)
    except ManifestValidationError as exc:
        return RepositoryCompatibility("invalid", exc.code)

    if manifest.manifest_version < CURRENT_MANIFEST_VERSION:
        return RepositoryCompatibility("invalid", "unsupported-manifest-version", manifest)
    if manifest.asset_version > CURRENT_ASSET_VERSION:
        return RepositoryCompatibility("unsupported-future", "future-asset-version", manifest)
    if manifest.schema_version > CURRENT_SCHEMA_VERSION:
        return RepositoryCompatibility("unsupported-future", "future-schema-version", manifest)
    if manifest.asset_version not in SUPPORTED_ASSET_VERSIONS:
        return RepositoryCompatibility("invalid", "unknown-asset-version", manifest)
    if manifest.schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        return RepositoryCompatibility("invalid", "unknown-schema-version", manifest)

    asset_behind = manifest.asset_version < CURRENT_ASSET_VERSION
    schema_behind = manifest.schema_version < CURRENT_SCHEMA_VERSION
    if asset_behind and schema_behind:
        return RepositoryCompatibility("upgradeable", "assets-and-schema-behind", manifest)
    if asset_behind:
        return RepositoryCompatibility("upgradeable", "assets-behind", manifest)
    if schema_behind:
        return RepositoryCompatibility("upgradeable", "schema-behind", manifest)
    return RepositoryCompatibility("current", "versions-current", manifest)


def _operational_git_optional(args: list[str], root: Path) -> str | None:
    try:
        return _run_git(args, cwd=root)
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None


def _normalize_task_id_prefix(prefix: str) -> str:
    normalized = prefix.strip().upper()
    if not re.match(r"^[A-Z][A-Z0-9]*$", normalized):
        raise SystemExit(
            f"Invalid task ID prefix '{prefix}'. "
            "Use uppercase letters/numbers, starting with a letter."
        )
    reserved = {
        EPIC_ID_PREFIX: "epics",
        FIX_ID_PREFIX: "fixes",
    }
    if normalized in reserved:
        raise SystemExit(f"Task ID prefix '{normalized}' is reserved for {reserved[normalized]}.")
    return normalized


def _normalize_id_generation_mode(value: str) -> str:
    normalized = value.strip().lower().replace("-", "_")
    if normalized in {"guid", "uuid"}:
        normalized = "unique"
    if normalized not in ID_GENERATION_MODES:
        raise SystemExit(
            f"Invalid ID generation mode '{value}'. Allowed: {', '.join(ID_GENERATION_MODES)}."
        )
    return normalized


def _load_workspace_definition(
    root: Path,
    config_path: Path,
    raw_workspace: object,
) -> WorkspaceDefinition | None:
    if raw_workspace is None:
        return None
    if not isinstance(raw_workspace, dict):
        raise SystemExit(f"{config_path} field 'workspace' must be an object.")

    authority = raw_workspace.get("authority_repository")
    if not isinstance(authority, str) or not authority.strip():
        raise SystemExit(
            f"{config_path} field 'workspace.authority_repository' must be a non-empty string."
        )
    authority = authority.strip()

    raw_repositories = raw_workspace.get("repositories")
    if not isinstance(raw_repositories, list) or not raw_repositories:
        raise SystemExit(f"{config_path} field 'workspace.repositories' must be a non-empty list.")

    root_resolved = root.resolve()
    repositories: list[WorkspaceRepository] = []
    repository_ids: set[str] = set()
    repository_paths: set[str] = set()
    git_roots: set[Path] = set()
    for index, raw_repository in enumerate(raw_repositories, start=1):
        label = f"workspace.repositories entry {index}"
        if not isinstance(raw_repository, dict):
            raise SystemExit(f"{config_path} {label} must be an object.")
        repository_id = raw_repository.get("id")
        repository_path = raw_repository.get("path")
        role = raw_repository.get("role")
        if not isinstance(repository_id, str) or not re.fullmatch(
            r"[a-z][a-z0-9-]*", repository_id
        ):
            raise SystemExit(f"{config_path} {label} field 'id' must be a lowercase slug.")
        if repository_id in repository_ids:
            raise SystemExit(
                f"{config_path} workspace repository ID '{repository_id}' is duplicated."
            )
        if not isinstance(repository_path, str) or not repository_path.strip():
            raise SystemExit(f"{config_path} {label} field 'path' must be non-empty text.")
        path_value = Path(repository_path.strip())
        if path_value.is_absolute() or ".." in path_value.parts:
            raise SystemExit(
                f"{config_path} workspace repository path '{repository_path}' must be "
                "relative to the authority root and cannot contain '..'."
            )
        normalized_path = path_value.as_posix().rstrip("/") or "."
        if normalized_path in repository_paths:
            raise SystemExit(
                f"{config_path} workspace repository path '{normalized_path}' is duplicated."
            )
        if role not in {"control", "implementation"}:
            raise SystemExit(
                f"{config_path} {label} field 'role' must be 'control' or 'implementation'."
            )

        resolved_path = (root_resolved / path_value).resolve()
        try:
            resolved_path.relative_to(root_resolved)
        except ValueError as exc:
            raise SystemExit(
                f"{config_path} workspace repository path '{normalized_path}' escapes "
                "the authority root."
            ) from exc
        if not resolved_path.is_dir():
            raise SystemExit(
                f"{config_path} workspace repository path '{normalized_path}' "
                "does not exist as a directory."
            )
        git_root = _operational_git_optional(["rev-parse", "--show-toplevel"], resolved_path)
        if git_root is None:
            raise SystemExit(
                f"{config_path} workspace repository '{repository_id}' is not a readable "
                "Git worktree."
            )
        resolved_git_root = Path(git_root).resolve()
        if resolved_git_root != resolved_path:
            raise SystemExit(
                f"{config_path} workspace repository '{repository_id}' path "
                f"'{normalized_path}' is not an independent Git root."
            )
        if resolved_git_root in git_roots:
            raise SystemExit(
                f"{config_path} workspace repositories must resolve to unique Git roots; "
                f"'{repository_id}' aliases an existing repository."
            )

        repository_ids.add(repository_id)
        repository_paths.add(normalized_path)
        git_roots.add(resolved_git_root)
        repositories.append(
            WorkspaceRepository(
                repository_id,
                normalized_path,
                role,
                resolved_path,
            )
        )

    if authority not in repository_ids:
        raise SystemExit(
            f"{config_path} workspace authority repository '{authority}' is not registered."
        )
    authority_repository = next(
        repository for repository in repositories if repository.repository_id == authority
    )
    if authority_repository.resolved_path != root_resolved:
        raise SystemExit(
            f"{config_path} workspace authority repository '{authority}' must use path '.' "
            "because the parent repository owns .project-workflow."
        )
    control_repositories = [
        repository.repository_id for repository in repositories if repository.role == "control"
    ]
    if control_repositories != [authority]:
        raise SystemExit(
            f"{config_path} workspace must define exactly one control repository and it "
            f"must be authority_repository '{authority}'."
        )
    return WorkspaceDefinition(authority, tuple(repositories))


def _default_workflow_config() -> WorkflowConfig:
    return WorkflowConfig(
        task_id_prefixes=(TASK_ID_PREFIX,),
        default_task_id_prefix=TASK_ID_PREFIX,
        prefix_guidance=dict(DEFAULT_PREFIX_GUIDANCE),
        id_generation=dict(DEFAULT_ID_GENERATION),
        unique_id_length=DEFAULT_UNIQUE_ID_LENGTH,
        accepted_doctor_warnings={},
        workspace=None,
    )


def _load_workflow_config(root: Path) -> WorkflowConfig:
    config_path = _workflow_config_path(root)
    if not config_path.exists():
        return _default_workflow_config()

    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {config_path}: {exc}") from exc
    except OSError as exc:
        raise SystemExit(f"Could not read {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise SystemExit(f"{config_path} must contain a JSON object.")

    raw_prefixes = raw.get("task_id_prefixes", [TASK_ID_PREFIX])
    if not isinstance(raw_prefixes, list) or not raw_prefixes:
        raise SystemExit(f"{config_path} field 'task_id_prefixes' must be a non-empty list.")

    prefixes: list[str] = []
    for raw_prefix in raw_prefixes:
        if not isinstance(raw_prefix, str):
            raise SystemExit(f"{config_path} field 'task_id_prefixes' must contain strings.")
        prefix = _normalize_task_id_prefix(raw_prefix)
        if prefix not in prefixes:
            prefixes.append(prefix)

    raw_default = raw.get("default_task_id_prefix", prefixes[0])
    if not isinstance(raw_default, str):
        raise SystemExit(f"{config_path} field 'default_task_id_prefix' must be a string.")
    default_prefix = _normalize_task_id_prefix(raw_default)
    if default_prefix not in prefixes:
        raise SystemExit(
            f"{config_path} default_task_id_prefix '{default_prefix}' must appear in "
            "task_id_prefixes."
        )

    raw_guidance = raw.get("prefix_guidance", {})
    if not isinstance(raw_guidance, dict):
        raise SystemExit(f"{config_path} field 'prefix_guidance' must be an object.")

    prefix_guidance: dict[str, str] = {}
    for raw_prefix, raw_text in raw_guidance.items():
        if not isinstance(raw_prefix, str) or not isinstance(raw_text, str):
            raise SystemExit(f"{config_path} field 'prefix_guidance' must map strings to strings.")
        prefix = _normalize_task_id_prefix(raw_prefix)
        if prefix not in prefixes:
            raise SystemExit(
                f"{config_path} prefix_guidance key '{prefix}' must appear in task_id_prefixes."
            )
        prefix_guidance[prefix] = raw_text.strip()

    for prefix in prefixes:
        prefix_guidance.setdefault(prefix, "")

    raw_id_generation = raw.get("id_generation", DEFAULT_ID_GENERATION)
    id_generation = dict(DEFAULT_ID_GENERATION)
    if isinstance(raw_id_generation, str):
        mode = _normalize_id_generation_mode(raw_id_generation)
        id_generation = {kind: mode for kind in ID_GENERATION_KINDS}
    elif isinstance(raw_id_generation, dict):
        for raw_kind, raw_mode in raw_id_generation.items():
            if raw_kind not in ID_GENERATION_KINDS:
                raise SystemExit(
                    f"{config_path} field 'id_generation' has unknown key '{raw_kind}'. "
                    f"Allowed: {', '.join(ID_GENERATION_KINDS)}."
                )
            if not isinstance(raw_mode, str):
                raise SystemExit(
                    f"{config_path} field 'id_generation.{raw_kind}' must be a string."
                )
            id_generation[raw_kind] = _normalize_id_generation_mode(raw_mode)
    else:
        raise SystemExit(f"{config_path} field 'id_generation' must be a string or an object.")

    raw_unique_id_length = raw.get("unique_id_length", DEFAULT_UNIQUE_ID_LENGTH)
    if not isinstance(raw_unique_id_length, int) or isinstance(raw_unique_id_length, bool):
        raise SystemExit(f"{config_path} field 'unique_id_length' must be an integer.")
    if raw_unique_id_length < 1 or raw_unique_id_length > 32:
        raise SystemExit(f"{config_path} field 'unique_id_length' must be between 1 and 32.")

    raw_accepted_warnings = raw.get("accepted_doctor_warnings", [])
    if not isinstance(raw_accepted_warnings, list):
        raise SystemExit(f"{config_path} field 'accepted_doctor_warnings' must be a list.")

    accepted_doctor_warnings: dict[str, str] = {}
    for idx, raw_warning in enumerate(raw_accepted_warnings, start=1):
        if isinstance(raw_warning, str):
            fingerprint = raw_warning.strip()
            reason = ""
        elif isinstance(raw_warning, dict):
            raw_fingerprint = raw_warning.get("fingerprint")
            if not isinstance(raw_fingerprint, str):
                raise SystemExit(
                    f"{config_path} accepted_doctor_warnings entry {idx} must include "
                    "a string 'fingerprint'."
                )
            fingerprint = raw_fingerprint.strip()
            raw_reason = raw_warning.get("reason", "")
            if not isinstance(raw_reason, str):
                raise SystemExit(
                    f"{config_path} accepted_doctor_warnings entry {idx} field "
                    "'reason' must be a string."
                )
            reason = raw_reason.strip()
        else:
            raise SystemExit(
                f"{config_path} accepted_doctor_warnings entry {idx} must be "
                "a string fingerprint or object."
            )
        if not re.match(r"^[0-9a-f]{16}$", fingerprint):
            raise SystemExit(
                f"{config_path} accepted_doctor_warnings entry {idx} has invalid "
                "fingerprint. Expected 16 lowercase hex characters."
            )
        accepted_doctor_warnings[fingerprint] = reason

    workspace = _load_workspace_definition(root, config_path, raw.get("workspace"))

    return WorkflowConfig(
        task_id_prefixes=tuple(prefixes),
        default_task_id_prefix=default_prefix,
        prefix_guidance=prefix_guidance,
        id_generation=id_generation,
        unique_id_length=raw_unique_id_length,
        accepted_doctor_warnings=accepted_doctor_warnings,
        workspace=workspace,
    )


def _format_task_prefixes(prefixes: tuple[str, ...]) -> str:
    return " or ".join(f"{prefix}-###" for prefix in prefixes)


def _id_generation_mode(config: WorkflowConfig, kind: str) -> str:
    return config.id_generation.get(kind, DEFAULT_ID_GENERATION[kind])


def _configured_suffix_pattern(config: WorkflowConfig, kind: str) -> str:
    suffixes = [r"\d{3,}" if kind == "backlog" else r"\d+"]
    if _id_generation_mode(config, kind) == "unique":
        suffixes.append(rf"[A-Z0-9]{{{config.unique_id_length}}}")
    return "(?:" + "|".join(suffixes) + ")"


def _valid_id_for_prefix(row_id: str, *, prefix: str, config: WorkflowConfig, kind: str) -> bool:
    pattern = rf"^{re.escape(prefix)}-{_configured_suffix_pattern(config, kind)}$"
    return bool(re.match(pattern, row_id))


def _valid_task_id(row_id: str, *, config: WorkflowConfig) -> bool:
    prefix = _task_prefix_from_id(row_id)
    if prefix is None or prefix not in config.task_id_prefixes:
        return False
    return _valid_id_for_prefix(row_id, prefix=prefix, config=config, kind="tasks")


def _valid_epic_id(row_id: str, *, config: WorkflowConfig) -> bool:
    return _valid_id_for_prefix(row_id, prefix=EPIC_ID_PREFIX, config=config, kind="epics")


def _valid_fix_id(row_id: str, *, config: WorkflowConfig) -> bool:
    return _valid_id_for_prefix(row_id, prefix=FIX_ID_PREFIX, config=config, kind="fixes")


def _valid_backlog_id(row_id: str, *, config: WorkflowConfig) -> bool:
    return _valid_id_for_prefix(
        row_id,
        prefix=BACKLOG_ID_PREFIX,
        config=config,
        kind="backlog",
    )


def _valid_workflow_ref_id(row_id: str, *, config: WorkflowConfig) -> bool:
    return (
        _valid_epic_id(row_id, config=config)
        or _valid_fix_id(row_id, config=config)
        or _valid_task_id(row_id, config=config)
    )


def _normalize_fix_id(row_id: str, *, root: Path) -> str:
    config = _load_workflow_config(root)
    match = re.match(
        rf"^({FIX_ID_PREFIX}-{_configured_suffix_pattern(config, 'fixes')})(?:-.+)?$",
        row_id,
    )
    if not match:
        raise SystemExit(f"Fix commands require a {FIX_ID_PREFIX}-### ID; got '{row_id}'.")
    return match.group(1)


def _resolve_task_id_prefix(root: Path, requested_prefix: str | None) -> str:
    config = _load_workflow_config(root)
    prefix = (
        _normalize_task_id_prefix(requested_prefix)
        if requested_prefix
        else config.default_task_id_prefix
    )
    if prefix not in config.task_id_prefixes:
        raise SystemExit(
            f"Task ID prefix '{prefix}' is not configured in {_workflow_config_path(root)}."
        )
    return prefix


def _normalize_task_status_id(row_id: str, *, root: Path) -> str:
    config = _load_workflow_config(root)
    prefix_pattern = "|".join(
        re.escape(prefix) for prefix in sorted(config.task_id_prefixes, key=len, reverse=True)
    )
    match = re.match(
        rf"^(({prefix_pattern})-{_configured_suffix_pattern(config, 'tasks')})(?:-.+)?$",
        row_id,
    )
    if not match:
        raise SystemExit(
            f"Task status only supports {_format_task_prefixes(config.task_id_prefixes)} IDs; "
            f"got '{row_id}'."
        )
    return match.group(1)


def _task_prefix_from_id(row_id: str) -> str | None:
    match = re.match(r"^([A-Z][A-Z0-9]*)-[A-Z0-9]+(?:-.+)?$", row_id)
    return match.group(1) if match else None


def _write_file(path: Path, content: str, *, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _template_repository_id(root: Path | None) -> str:
    if root is None:
        return "."
    workspace = _load_workflow_config(root).workspace
    return workspace.authority_repository if workspace is not None else "."


def _implementation_template(
    task_id: str,
    title: str,
    *,
    root: Path | None = None,
) -> str:
    repository_id = _template_repository_id(root)
    return (
        f"## User Story\n\n"
        f"As a ____, I want ____, so that ____.\n\n"
        f"## Architecture Impact\n\n"
        f"- Classification: ____\n"
        f"- Reason: ____\n"
        f"- Architecture authority: ____\n"
        f"- Authority identity: ____\n"
        f"- Architect invocation: ____\n"
        f"- Architect decision identity: ____\n"
        f"- Affected boundaries: ____\n"
        f"- Architecture decision: ____\n"
        f"- Measurable constraints: ____\n"
        f"- Conformance plan: ____\n\n"
        f"## Acceptance Criteria\n\n"
        f"- [ ] AC1: ____\n\n"
        f"## Validation\n\n"
        f"- AC1: ____\n\n"
        f"## Repository Evidence\n\n"
        f"| Repository | Branch / PR | Validation | Delivery | Evidence |\n"
        f"| ---------- | ----------- | ---------- | -------- | -------- |\n"
        f"| {repository_id} | not recorded | not recorded | not recorded | not recorded |\n\n"
        f"## Task List\n\n"
        f"| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |\n"
        f"| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |\n"
        f"| 1 | ____ | ____ | AC1: ____ | ____ | To Do | | ____ | No | bounded-return |\n\n"
        f"## QA & Code Review\n\n"
        f"- Intent QA contract: adversarial\n"
        f"- Verdict: ____\n"
        f"- Intent adversarial verdict: ____\n"
        f"- Could every AC pass while the approved user job remains undone: ____\n"
        f"- Intent audit state: ____\n"
        f"- Outcome journey evidence: ____\n"
        f"- Reviewer independence: ____\n"
        f"- Evidence: ____\n"
        f"- Findings: ____\n\n"
        f"## Architecture Conformance\n\n"
        f"- Authority identity: ____\n"
        f"- Candidate: ____\n"
        f"- Mechanical checks: candidate=____; receipt=____\n"
        f"- Deviations: ____\n"
        f"- Verdict: ____\n\n"
        f"## Retro\n\n"
        f"- Reusable lessons: ____\n"
        f"- Conventions or agent assets updated: ____\n"
        f"- Follow-up tasks: ____\n\n"
        f"## Notes\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n"
        f"- Created: {date.today().isoformat()}\n"
    )


def _requirements_template(
    task_id: str,
    title: str,
    *,
    root: Path | None = None,
) -> str:
    repository_id = _template_repository_id(root)
    return (
        f"# Requirements\n\n"
        f"## Summary\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n"
        f"- Last updated: {date.today().isoformat()}\n"
        f"- Intent contract: full\n\n"
        f"## Intent\n\n"
        f"State the owner's desired outcome in one or two plain-language sentences.\n\n"
        f"## Intent Spine\n\n"
        f"- OC1 — Completion capability: ____\n"
        f"- OC2 — Material capabilities: ____\n"
        f"- OC3 — Success journey: ____\n"
        f"- OC4 — Successful-but-wrong result: ____\n"
        f"- OC5 — Exclusions: ____\n"
        f"- OC6 — Assumptions: ____\n"
        f"- OC7 — Authority source: ____\n\n"
        f"## Owner Approval\n\n"
        f"- Intent reviewed and accurately reflected: No\n"
        f"- Requirements reviewed by owner: No\n"
        f"- Acceptance criteria reviewed by owner: No\n"
        f"- Approved for decomposition: No\n"
        f"- Approved for implementation: No\n"
        f"- Approved scope envelope: No\n"
        f"- Approved by: Not approved\n"
        f"- Approval date: Not approved\n"
        f"- Approval note / source: Not approved\n"
        f"- Approved artifact identity: Not approved\n\n"
        f"## Goal\n\n"
        f"Describe the user outcome this change must deliver.\n\n"
        f"## Non-Goals\n\n"
        f"List what is explicitly out-of-scope.\n\n"
        f"## Users & Context\n\n"
        f"Who is affected and in what situation?\n\n"
        f"## Repository Scope\n\n"
        f"- Primary repository: {repository_id}\n"
        f"- Repositories touched: {repository_id}\n\n"
        f"## Requirements (Outcome-Focused)\n\n"
        f"- ____\n\n"
        f"## Acceptance Criteria (Verifiable)\n\n"
        f"- AC1: ____\n\n"
        f"## Open Questions (Answer Needed)\n\n"
        f"- ____\n\n"
        f"## Decisions (Resolved)\n\n"
        f"- ____\n\n"
        f"## Validation Plan\n\n"
        f"- How we will verify acceptance criteria: ____\n"
    )


def _fix_template(
    fix_id: str,
    title: str,
    *,
    root: Path | None = None,
) -> str:
    repository_id = _template_repository_id(root)
    return (
        f"# Fix\n\n"
        f"## Summary\n\n"
        f"- Fix: {fix_id}\n"
        f"- Title: {title}\n"
        f"- Status: To Do\n"
        f"- Created: {date.today().isoformat()}\n"
        f"- Intent contract: compact\n\n"
        f"## Intent\n\n"
        f"State the bounded correction and restored outcome in one or two plain-language sentences.\n\n"
        f"## Report\n\n"
        f"- Observed or requested: ____\n"
        f"- Expected: ____\n"
        f"- Affected users or systems: ____\n"
        f"- Delivered baseline: ____\n"
        f"- Report evidence: ____\n\n"
        f"## Routing\n\n"
        f"- Decision: Fix\n"
        f"- Rationale: ____\n"
        f"- Related work state: Not identified\n"
        f"- Bounded correction: ____\n"
        f"- New outcome or material decisions: No\n"
        f"- Independent work items: One\n\n"
        f"## Classification\n\n"
        f"- Type: ____\n"
        f"- Mode: Normal\n"
        f"- Severity: ____\n"
        f"- Impact: ____\n"
        f"- Urgency: ____\n"
        f"- Owner: ____\n\n"
        f"## Related Work\n\n"
        f"- Originating work: Not identified\n"
        f"- External links: None\n\n"
        f"## Risk\n\n"
        f"- Risk level: ____\n"
        f"- Risks: ____\n"
        f"- Rollback or containment: ____\n\n"
        f"## Fix Plan\n\n"
        f"- Scope: ____\n"
        f"- Non-goals: ____\n"
        f"- Affected target: ____\n"
        f"- Primary repo: {repository_id}\n"
        f"- Repos touched: {repository_id}\n"
        f"- Branch, PR, and evidence links: ____\n"
        f"- Verification plan: ____\n\n"
        f"### Repository Links\n\n"
        f"| Repo | Branch | PR | Evidence |\n"
        f"|---|---|---|---|\n"
        f"| {repository_id} | ____ | ____ | ____ |\n\n"
        f"## Repository Evidence\n\n"
        f"| Repository | Branch / PR | Validation | Delivery | Evidence |\n"
        f"| ---------- | ----------- | ---------- | -------- | -------- |\n"
        f"| {repository_id} | not recorded | not recorded | not recorded | not recorded |\n\n"
        f"## Verification\n\n"
        f"- Delivered scope: ____\n"
        f"- Verification result: ____\n"
        f"- Adjacent behavior checked: ____\n"
        f"- Original acceptance criteria result: Not applicable\n"
        f"- Regression evidence: ____\n"
        f"- Residual risk: ____\n\n"
        f"## Outcome\n\n"
        f"- Disposition: {FIX_ACTIVE_DISPOSITION}\n"
        f"- Decision: ____\n"
        f"- Closed by: ____\n"
        f"- Closed date: ____\n"
        f"- Promoted to: None\n"
    )


def _fix_values(text: str, heading: str) -> dict[str, str]:
    return _parse_key_value_section(_markdown_section(text, heading))


def _fix_value_missing(value: str | None) -> bool:
    normalized = (value or "").strip().lower()
    return not normalized or normalized in {"____", "pending", "tbd", "unknown"}


def _replace_fix_field(text: str, heading: str, key: str, value: str) -> str:
    lines = text.splitlines(keepends=True)
    target_heading = f"## {heading}".lower()
    in_section = False
    field_re = re.compile(rf"^(\s*[-*]\s*{re.escape(key)}\s*:\s*).*$", re.IGNORECASE)
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## "):
            if in_section:
                break
            in_section = stripped.lower() == target_heading
            continue
        if not in_section:
            continue
        match = field_re.match(line.rstrip("\n"))
        if match:
            newline = "\n" if line.endswith("\n") else ""
            lines[idx] = f"{match.group(1)}{value}{newline}"
            return "".join(lines)
    raise SystemExit(f"FIX.md is missing field '{key}' under '## {heading}'.")


def _tracker_template() -> str:
    return "# Stories\n\n| ID | Title | Status | Docs |\n|---|---|---|---|\n"


def _backlog_template() -> str:
    return (
        "# Backlog\n\n"
        "Use this file for future intent, rough priorities, and promotion history before "
        "work becomes an executable project-workflow task or epic.\n\n"
        "Backlog status is not implementation status. `Accepted` means worth keeping or "
        "preparing, not ready to implement. After promotion, active execution status lives "
        "in `.project-workflow/TRACKER.md` or the relevant epic tracker.\n\n"
        "Allowed `Type` values: " + ", ".join(f"`{value}`" for value in BACKLOG_TYPES) + ".\n\n"
        "Allowed `Priority` values: "
        + ", ".join(f"`{value}`" for value in BACKLOG_PRIORITIES)
        + ".\n\n"
        "Allowed `Status` values: "
        + ", ".join(f"`{value}`" for value in BACKLOG_STATUSES)
        + ".\n\n"
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )


def _epic_tracker_template() -> str:
    return (
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )


def _epic_deferrals_template() -> str:
    return (
        "# Deferrals\n\n"
        "| Parent AC | Status | Owner | Decision Date | Reason | Follow-up | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
    )


def _epic_amendments_template() -> str:
    return (
        "# Epic Amendments\n\n"
        "## Approved Child Row Amendments\n\n"
        "| ID | Title | Parent ACs | Approved By | Decision Date | Reason | Source |\n"
        "|---|---|---|---|---|---|---|\n"
    )


def _epic_retro_template(epic_id: str, title: str) -> str:
    return (
        "# Epic Retro\n\n"
        f"- Epic: {epic_id}\n"
        f"- Title: {title}\n"
        f"- Last updated: {date.today().isoformat()}\n\n"
        "## Lessons\n\n"
        "- ____\n\n"
        "## Follow-up Tasks\n\n"
        "- ____\n\n"
        "## Deferrals\n\n"
        "- ____\n\n"
        "## Missed In-Scope Work\n\n"
        "- ____\n"
    )


def _epic_contract_template(epic_id: str, title: str) -> str:
    return (
        "# Epic Contract\n\n"
        "## Summary\n\n"
        f"- Epic: {epic_id}\n"
        f"- Title: {title}\n"
        f"- Last updated: {date.today().isoformat()}\n\n"
        "## Sources of Truth\n\n"
        "- ____\n\n"
        "## Invalid Substitutes\n\n"
        "- ____\n\n"
        "## Invariants\n\n"
        "- ____\n\n"
        "## Artifact Targets\n\n"
        "- ____\n\n"
        "## Parent AC Proof Ownership\n\n"
        "| Parent AC | Proof Owner | Required Evidence |\n"
        "| --- | --- | --- |\n"
        "| AC1 | ____ | ____ |\n\n"
    )


def _parse_markdown_table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _clean_markdown_cell_path(value: str) -> str:
    return value.strip().strip("`").strip()


def _markdown_section(text: str, heading: str) -> str:
    target = f"## {heading}".lower()
    collecting = False
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            if collecting:
                break
            collecting = stripped.lower() == target
            continue
        if collecting:
            lines.append(line)
    return "\n".join(lines).strip()


def _extract_ac_ids(text: str) -> set[str]:
    return {
        f"AC{match.group(1)}" for match in re.finditer(r"\bAC\s*(\d+)\b", text, flags=re.IGNORECASE)
    }


def _extract_workflow_ref_ids(text: str, *, config: WorkflowConfig) -> set[str]:
    candidates = {
        match.group(0).upper()
        for match in re.finditer(r"\b[A-Z][A-Z0-9]*-[A-Z0-9]+\b", text, re.IGNORECASE)
    }
    return {
        candidate for candidate in candidates if _valid_workflow_ref_id(candidate, config=config)
    }


def _extract_declared_ac_ids(text: str) -> set[str]:
    declared: set[str] = set()
    for line in text.splitlines():
        match = re.match(
            r"^\s*[-*]\s*(?:\[[ xX]\]\s*)?(AC\s*\d+)\s*:",
            line,
            flags=re.IGNORECASE,
        )
        if match:
            declared.update(_extract_ac_ids(match.group(1)))
    return declared


def _extract_parent_ac_coverage(row: dict[str, str]) -> str:
    direct = row.get("Parent ACs", "").strip()
    if direct:
        return direct
    notes = row.get("Notes", "")
    match = re.search(
        r"\bCovers\s+((?:AC\s*\d+\s*,?\s*)+)",
        notes,
        flags=re.IGNORECASE,
    )
    if not match:
        return ""
    return ", ".join(sorted(_extract_ac_ids(match.group(1))))


def _extract_parent_ac_ids_from_requirements(requirements_text: str) -> set[str]:
    return _extract_ac_ids(
        _markdown_section(requirements_text, "Acceptance Criteria (Verifiable)")
    ) | _extract_ac_ids(_markdown_section(requirements_text, "Acceptance Criteria"))


def _extract_parent_ac_ids_from_epic_rows(rows: list[dict[str, str]]) -> set[str]:
    mapped: set[str] = set()
    for row in rows:
        mapped.update(_extract_ac_ids(_extract_parent_ac_coverage(row)))
    return mapped


def _normalize_ac_list(value: str) -> str:
    ac_ids = sorted(_extract_ac_ids(value), key=lambda ac_id: int(ac_id[2:]))
    return ", ".join(ac_ids)


def _markdown_table_rows_from_section(
    text: str,
    heading: str,
    *,
    expected_columns: tuple[str, ...],
) -> list[dict[str, str]]:
    section = _markdown_section(text, heading)
    if not section:
        return []

    lines = section.splitlines()
    header_idx: int | None = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        if cells == list(expected_columns):
            header_idx = idx
            break
    if header_idx is None:
        return []

    rows: list[dict[str, str]] = []
    row_idx = header_idx + 2
    while row_idx < len(lines):
        cells = _parse_markdown_table_cells(lines[row_idx])
        if cells is None or len(cells) != len(expected_columns):
            break
        rows.append(dict(zip(expected_columns, cells)))
        row_idx += 1
    return rows


def _proposed_child_work_rows(requirements_text: str) -> list[dict[str, str]]:
    rows = _markdown_table_rows_from_section(
        requirements_text,
        "Proposed Child Work",
        expected_columns=("Proposed Child", "Parent ACs", "Purpose", "Dependencies"),
    )
    if rows:
        return rows
    return _markdown_table_rows_from_section(
        requirements_text,
        "Proposed Child Work",
        expected_columns=("Proposed Child", "Parent ACs", "Purpose"),
    )


def _decomposition_plan_path(epic_dir: Path) -> Path:
    return epic_dir / DECOMPOSITION_PLAN_FILENAME


def _epic_amendments_path(epic_dir: Path) -> Path:
    return epic_dir / EPIC_AMENDMENTS_FILENAME


def _epic_contract_path(epic_dir: Path) -> Path:
    return epic_dir / EPIC_CONTRACT_FILENAME


def _epic_contract_proof_owner_rows(contract_text: str) -> list[dict[str, str]]:
    return _markdown_table_rows_from_section(
        contract_text,
        "Parent AC Proof Ownership",
        expected_columns=EPIC_CONTRACT_PROOF_OWNER_COLUMNS,
    )


def _extract_work_item_ids(text: str) -> set[str]:
    return set(re.findall(r"\b[A-Z][A-Z0-9]*-[A-Z0-9]+\b", text))


def _epic_contract_proof_owner_map(contract_text: str) -> dict[str, set[str]]:
    owner_map: dict[str, set[str]] = {}
    for row in _epic_contract_proof_owner_rows(contract_text):
        owners = _extract_work_item_ids(row.get("Proof Owner", ""))
        for ac_id in _extract_ac_ids(row.get("Parent AC", "")):
            owner_map.setdefault(ac_id, set()).update(owners)
    return owner_map


def _flat_markdown_bullet_records(section: str) -> list[tuple[str, str]]:
    """Return (logical item, first physical line) for a flat Markdown list."""
    records: list[tuple[str, str]] = []
    current_parts: list[str] = []
    first_physical_line = ""
    continuation_open = False

    def flush() -> None:
        nonlocal current_parts, first_physical_line, continuation_open
        if current_parts:
            records.append((" ".join(current_parts), first_physical_line))
        current_parts = []
        first_physical_line = ""
        continuation_open = False

    for line in section.splitlines():
        top_level = re.match(r"^[-*+]\s+(.+?)\s*$", line)
        if top_level:
            flush()
            first_physical_line = top_level.group(1).strip()
            current_parts = [first_physical_line]
            continuation_open = True
            continue
        if not line.strip():
            flush()
            continue
        if continuation_open:
            stripped = line.strip()
            if stripped.startswith(("#", "|")) or re.match(r"^[-*+]\s+", stripped):
                flush()
                continue
            current_parts.append(stripped)
    flush()
    return records


def _contract_section_bullet_records(
    contract_text: str,
    heading: str,
) -> list[tuple[str, str]]:
    return [
        (logical_item, first_physical_line)
        for logical_item, first_physical_line in _flat_markdown_bullet_records(
            _markdown_section(contract_text, heading)
        )
        if not _section_has_placeholder(logical_item)
    ]


def _contract_section_bullets(contract_text: str, heading: str) -> list[str]:
    return [
        logical_item
        for logical_item, _first_physical_line in _contract_section_bullet_records(
            contract_text,
            heading,
        )
    ]


def _markdown_subsection(text: str, parent_heading: str, heading: str) -> str:
    section = _markdown_section(text, parent_heading)
    target = f"### {heading}".lower()
    collecting = False
    lines: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("### "):
            if collecting:
                break
            collecting = stripped.lower() == target
            continue
        if collecting:
            lines.append(line)
    return "\n".join(lines).strip()


def _legacy_truncated_child_charter_issues(
    *,
    epic_dir: Path,
    requirements_text: str,
    implementation_text: str,
) -> list[str]:
    contract_path = _epic_contract_path(epic_dir)
    if not contract_path.exists():
        return []
    contract_text = contract_path.read_text(encoding="utf-8")
    section_pairs = (
        ("Invariants", "Inherited Invariants"),
        ("Invalid Substitutes", "Invalid Substitutes"),
        ("Artifact Targets", "Artifact Targets"),
    )
    issues: list[str] = []
    for contract_heading, child_heading in section_pairs:
        wrapped_records = [
            (logical_item, first_physical_line)
            for logical_item, first_physical_line in _contract_section_bullet_records(
                contract_text,
                contract_heading,
            )
            if logical_item != first_physical_line
        ]
        if not wrapped_records:
            continue
        for document_name, document_text in (
            ("REQUIREMENTS.md", requirements_text),
            ("IMPLEMENTATION.md", implementation_text),
        ):
            child_items = {
                logical_item
                for logical_item, _first_line in _flat_markdown_bullet_records(
                    _markdown_subsection(document_text, "Child Charter", child_heading)
                )
            }
            truncated = [
                (logical_item, legacy_fragment)
                for logical_item, legacy_fragment in wrapped_records
                if legacy_fragment in child_items and logical_item not in child_items
            ]
            if truncated:
                logical_item, legacy_fragment = truncated[0]
                issues.append(
                    "agent action required: "
                    f"`{document_name}` contains {len(truncated)} legacy truncated "
                    f"`{child_heading}` bullet(s), including `{legacy_fragment}`; restore "
                    "the complete logical parent-contract bullet(s), for example "
                    f"`{logical_item}`."
                )
    return issues


def _format_child_charter_from_contract(
    *,
    epic_dir: Path,
    parent_ac_coverage: str,
) -> str:
    contract_path = _epic_contract_path(epic_dir)
    if not contract_path.exists():
        return ""
    contract_text = contract_path.read_text(encoding="utf-8")
    parent_ac_ids = sorted(
        _extract_ac_ids(parent_ac_coverage),
        key=lambda ac_id: int(ac_id[2:]),
    )
    proof_rows = [
        row
        for row in _epic_contract_proof_owner_rows(contract_text)
        if _extract_ac_ids(row.get("Parent AC", "")) & set(parent_ac_ids)
    ]

    def bullet_lines(values: list[str]) -> str:
        return "\n".join(f"- {value}" for value in values) if values else "- None recorded."

    proof_lines = []
    for row in proof_rows:
        proof_lines.append(
            f"- {row.get('Parent AC', '').strip()}: owner `{row.get('Proof Owner', '').strip()}`; "
            f"required evidence: {row.get('Required Evidence', '').strip()}"
        )
    return (
        "## Child Charter\n\n"
        "### Inherited Invariants\n\n"
        f"{bullet_lines(_contract_section_bullets(contract_text, 'Invariants'))}\n\n"
        "### Invalid Substitutes\n\n"
        f"{bullet_lines(_contract_section_bullets(contract_text, 'Invalid Substitutes'))}\n\n"
        "### Artifact Targets\n\n"
        f"{bullet_lines(_contract_section_bullets(contract_text, 'Artifact Targets'))}\n\n"
        "### Parent AC Proof Ownership\n\n"
        f"{chr(10).join(proof_lines) if proof_lines else '- None assigned to this child.'}\n\n"
    )


def _epic_contract_issues(epic_dir: Path, requirements_text: str) -> list[str]:
    contract_path = _epic_contract_path(epic_dir)
    if not contract_path.exists():
        return [f"{EPIC_CONTRACT_FILENAME} is missing."]

    contract_text = contract_path.read_text(encoding="utf-8")
    issues: list[str] = []
    for heading in EPIC_CONTRACT_REQUIRED_SECTIONS:
        section = _markdown_section(contract_text, heading)
        if not _section_has_substantive_text(section):
            issues.append(
                f"{EPIC_CONTRACT_FILENAME} section `## {heading}` is missing or placeholder."
            )

    owner_rows = _epic_contract_proof_owner_rows(contract_text)
    if not owner_rows:
        issues.append(f"{EPIC_CONTRACT_FILENAME} must include parent AC proof owner rows.")
    else:
        for row in owner_rows:
            row_text = " ".join(row.values())
            if _section_has_placeholder(row_text):
                issues.append(
                    f"{EPIC_CONTRACT_FILENAME} proof owner row for "
                    f"{row.get('Parent AC', 'unknown AC')} is placeholder."
                )

    parent_ac_ids = _extract_parent_ac_ids_from_requirements(requirements_text)
    owned_ac_ids: set[str] = set()
    for row in owner_rows:
        owned_ac_ids.update(_extract_ac_ids(row.get("Parent AC", "")))
    missing_owners = sorted(parent_ac_ids - owned_ac_ids, key=lambda ac_id: int(ac_id[2:]))
    if missing_owners:
        issues.append(
            f"{EPIC_CONTRACT_FILENAME} lacks proof owners for parent ACs: "
            + ", ".join(missing_owners)
        )
    return issues


def _epic_contract_issues_for_path(epic_dir: Path) -> list[str]:
    requirements_path = epic_dir / "REQUIREMENTS.md"
    if not requirements_path.exists():
        return [f"missing epic requirements file: {requirements_path}"]
    return _epic_contract_issues(
        epic_dir,
        requirements_path.read_text(encoding="utf-8"),
    )


def _require_epic_contract(epic_dir: Path, epic_id: str) -> None:
    issues = _epic_contract_issues_for_path(epic_dir)
    if issues:
        raise SystemExit(
            f"{epic_id} is missing required epic contract authority:\n"
            + "\n".join(f"- {issue}" for issue in issues)
        )


def _decomposition_plan_source_identity(requirements_text: str) -> str:
    values = _parse_key_value_section(_markdown_section(requirements_text, OWNER_APPROVAL_HEADING))
    identity = values.get("approved artifact identity", "").strip()
    if identity.startswith(APPROVAL_IDENTITY_PREFIX):
        return identity
    return _approval_artifact_identity(requirements_text)


def _format_decomposition_plan(
    *,
    epic_id: str,
    requirements_text: str,
    rows: list[dict[str, str]],
) -> str:
    source_identity = _decomposition_plan_source_identity(requirements_text)
    lines = [
        "# Decomposition Plan",
        "",
        "## Summary",
        "",
        f"- Epic: {epic_id}",
        "- Status: Approved by parent requirements envelope",
        "- Authority source: Parent REQUIREMENTS.md Owner Approval",
        f"- Source requirements identity: {source_identity}",
        f"- Last updated: {date.today().isoformat()}",
        "",
        "## Authorized Child Rows",
        "",
        "| ID | Title | Parent ACs | Source | Dependencies | Execution Needs |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {id} | {title} | {parent_acs} | {source} | {dependencies} | "
            "{execution_needs} |".format(
                id=row["ID"],
                title=row["Title"],
                parent_acs=_normalize_ac_list(row.get("Parent ACs", "")),
                source=row.get("Source", "Decomposition plan"),
                dependencies=row.get("Dependencies", ""),
                execution_needs=row.get("Execution Needs", "bounded-return") or "bounded-return",
            )
        )
    lines.extend(
        [
            "",
            "## Authority Rules",
            "",
            "- Matching rows inside this plan may be approved and scaffolded without separate per-row owner approval.",
            "- Rows outside this plan require an approved amendment before gated lifecycle movement.",
            "- Matching is by ID, title, and parent AC coverage.",
            "",
        ]
    )
    return "\n".join(lines)


def _read_decomposition_plan_rows(plan_path: Path) -> list[dict[str, str]]:
    if not plan_path.exists():
        return []
    text = plan_path.read_text(encoding="utf-8")
    rows = _markdown_table_rows_from_section(
        text,
        "Authorized Child Rows",
        expected_columns=DELEGATION_EXECUTION_NEEDS_DECOMPOSITION_PLAN_COLUMNS,
    )
    if rows:
        return rows
    rows = _markdown_table_rows_from_section(
        text,
        "Authorized Child Rows",
        expected_columns=DELEGATION_DECOMPOSITION_PLAN_COLUMNS,
    )
    if rows:
        return rows
    return _markdown_table_rows_from_section(
        text,
        "Authorized Child Rows",
        expected_columns=DECOMPOSITION_PLAN_COLUMNS,
    )


def _read_epic_amendment_rows(amendments_path: Path) -> list[dict[str, str]]:
    if not amendments_path.exists():
        return []
    return _markdown_table_rows_from_section(
        amendments_path.read_text(encoding="utf-8"),
        "Approved Child Row Amendments",
        expected_columns=EPIC_AMENDMENT_COLUMNS,
    )


def _append_epic_amendment_row(amendments_path: Path, row: dict[str, str]) -> None:
    if not amendments_path.exists():
        amendments_path.write_text(_epic_amendments_template(), encoding="utf-8")
    lines = amendments_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_idx: int | None = None
    for idx, line in enumerate(lines):
        if _parse_markdown_table_cells(line) == list(EPIC_AMENDMENT_COLUMNS):
            header_idx = idx
            break
    if header_idx is None:
        raise SystemExit(
            f"{EPIC_AMENDMENTS_FILENAME} schema mismatch. Expected amendment table header."
        )
    existing_rows = _read_epic_amendment_rows(amendments_path)
    row_id = row.get("ID", "").strip()
    if row_id in {existing.get("ID", "").strip() for existing in existing_rows}:
        raise SystemExit(f"{row_id} is already recorded in {EPIC_AMENDMENTS_FILENAME}.")
    insert_at = header_idx + 2 + len(existing_rows)
    lines.insert(
        insert_at,
        "| "
        + " | ".join(_markdown_cell(row.get(column, "")) for column in EPIC_AMENDMENT_COLUMNS)
        + " |\n",
    )
    amendments_path.write_text("".join(lines), encoding="utf-8")


def _amendment_row_authority_issues(
    *,
    amendment_row: dict[str, str],
    tracker_row: dict[str, str],
) -> list[str]:
    row_id = tracker_row.get("ID", "").strip()
    issues: list[str] = []
    if amendment_row.get("Title", "").strip() != tracker_row.get("Title", "").strip():
        issues.append(
            f"{row_id} title differs from amendment ('{amendment_row.get('Title', '').strip()}')."
        )
    amended_acs = _normalize_ac_list(amendment_row.get("Parent ACs", ""))
    row_acs = _normalize_ac_list(_extract_parent_ac_coverage(tracker_row))
    if amended_acs != row_acs:
        issues.append(
            f"{row_id} parent ACs differ from amendment ('{amended_acs}' != '{row_acs}')."
        )
    for column in ("Approved By", "Decision Date", "Reason", "Source"):
        value = amendment_row.get(column, "").strip()
        if _approval_source_invalid(value):
            issues.append(f"{row_id} amendment column `{column}` is missing or placeholder.")
    return issues


def _amendment_authority_issues(
    *,
    epic_dir: Path,
    row: dict[str, str],
) -> list[str]:
    amendments_path = _epic_amendments_path(epic_dir)
    if not amendments_path.exists():
        return [f"{EPIC_AMENDMENTS_FILENAME} is missing."]
    row_id = row.get("ID", "").strip()
    for amendment_row in _read_epic_amendment_rows(amendments_path):
        if amendment_row.get("ID", "").strip() == row_id:
            return _amendment_row_authority_issues(
                amendment_row=amendment_row,
                tracker_row=row,
            )
    return [f"{row_id} is not recorded in {EPIC_AMENDMENTS_FILENAME}."]


def _decomposition_plan_authority_issues(
    *,
    epic_dir: Path,
    row: dict[str, str],
) -> list[str]:
    plan_path = _decomposition_plan_path(epic_dir)
    if not plan_path.exists():
        return [
            f"{DECOMPOSITION_PLAN_FILENAME} is missing; run `epic decompose` from "
            "owner-approved requirements or record an approved amendment before this row advances."
        ]

    plan_rows = _read_decomposition_plan_rows(plan_path)
    row_id = row.get("ID", "").strip()
    for plan_row in plan_rows:
        if plan_row.get("ID", "").strip() != row_id:
            continue
        issues: list[str] = []
        if plan_row.get("Title", "").strip() != row.get("Title", "").strip():
            issues.append(
                f"{row_id} title differs from decomposition plan "
                f"('{plan_row.get('Title', '').strip()}')."
            )
        planned_acs = _normalize_ac_list(plan_row.get("Parent ACs", ""))
        row_acs = _normalize_ac_list(_extract_parent_ac_coverage(row))
        if planned_acs != row_acs:
            issues.append(
                f"{row_id} parent ACs differ from decomposition plan "
                f"('{planned_acs}' != '{row_acs}')."
            )
        return issues

    amendment_issues = _amendment_authority_issues(epic_dir=epic_dir, row=row)
    if not amendment_issues:
        return []

    return [
        f"{row_id} is outside {DECOMPOSITION_PLAN_FILENAME}; record an approved "
        "amendment before this row advances.",
        *amendment_issues,
    ]


def _require_decomposition_plan_authority(epic_dir: Path, row: dict[str, str]) -> None:
    issues = _decomposition_plan_authority_issues(epic_dir=epic_dir, row=row)
    if issues:
        row_id = row.get("ID", "child row")
        raise SystemExit(
            f"{row_id} is outside the approved decomposition authority:\n"
            + "\n".join(f"- {issue}" for issue in issues)
        )


def _markdown_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value).replace("|", "\\|").strip()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


OWNER_APPROVAL_HEADING = "Owner Approval"

LEGACY_ADOPTION_HEADING = "Legacy Adoption"

APPROVAL_IDENTITY_PREFIX = "sha256:"

APPROVAL_TRUE_VALUES = {"yes", "true", "approved"}

APPROVAL_FALSE_VALUES = {"", "no", "false", "not approved", "pending"}


def _parse_key_value_section(section: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")):
            stripped = stripped[1:].strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        values[key.strip().lower()] = value.strip()
    return values


def _remove_markdown_section(text: str, heading: str) -> str:
    target = f"## {heading}".lower()
    lines = text.splitlines()
    output: list[str] = []
    skipping = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if stripped.lower() == target:
                skipping = True
                continue
            skipping = False
        if not skipping:
            output.append(line)
    return "\n".join(output).strip() + "\n"


def _approval_artifact_identity(requirements_text: str) -> str:
    comparable_text = _remove_markdown_section(requirements_text, OWNER_APPROVAL_HEADING)
    comparable_text = _remove_markdown_section(comparable_text, LEGACY_ADOPTION_HEADING)
    comparable_text = re.sub(r"\n{3,}", "\n\n", comparable_text).strip() + "\n"
    return APPROVAL_IDENTITY_PREFIX + hashlib.sha256(comparable_text.encode("utf-8")).hexdigest()


def _approval_value_is_yes(value: str) -> bool:
    return value.strip().lower() in APPROVAL_TRUE_VALUES


def _approval_value_is_no(value: str) -> bool:
    return value.strip().lower() in APPROVAL_FALSE_VALUES


def _approval_source_invalid(source: str) -> bool:
    lowered = source.strip().lower()
    invalid_fragments = (
        "____",
        "pending",
        "not approved",
        "awaiting owner",
        "agent-only",
        "agent approved",
        "approved by agent",
    )
    return not lowered or any(fragment in lowered for fragment in invalid_fragments)


def _section_has_placeholder(section: str) -> bool:
    lowered = section.lower()
    placeholder_phrases = (
        "____",
        "describe the user outcome",
        "list what is explicitly out-of-scope",
        "who is affected and in what situation",
        "how we will verify",
        "as a ____",
        "state the owner's desired outcome",
        "state the bounded correction and restored outcome",
        "state the child outcome",
    )
    return any(phrase in lowered for phrase in placeholder_phrases)


def _section_has_substantive_text(section: str) -> bool:
    cleaned_lines = [
        line.strip(" -\t")
        for line in section.splitlines()
        if line.strip() and not set(line.strip()) <= {"-", "|", " "}
    ]
    return any(line and not _section_has_placeholder(line) for line in cleaned_lines)


def _normalize_agent(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    aliases = {
        "copilot": "github-copilot",
        "github": "github-copilot",
        "github-copilot": "github-copilot",
        "claude": "claude-code",
        "claude-code": "claude-code",
        "codex": "codex",
        "openai": "codex",
        "openai-codex": "codex",
        "cursor": "cursor",
    }
    if normalized not in aliases:
        allowed = ", ".join(sorted(AGENT_CHOICES))
        raise argparse.ArgumentTypeError(f"Unsupported agent '{value}'. Choose one of: {allowed}.")
    return aliases[normalized]


def _split_frontmatter(content: str) -> tuple[str, str]:
    """Return (frontmatter, body) from markdown content with YAML frontmatter."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, flags=re.DOTALL)
    if not match:
        return "", content
    return match.group(1), match.group(2)


def _extract_frontmatter_value(frontmatter: str, key: str) -> str | None:
    pattern = rf"^{re.escape(key)}:\s*(.+)$"
    match = re.search(pattern, frontmatter, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def _prompt_filename_to_agent_name(prompt_file: str) -> str:
    base_name = prompt_file.replace(".prompt.md", "")
    canonical_slugs = {
        "QAReview": "qa-review",
    }
    return f"project-{canonical_slugs.get(base_name, slug_kebab_lower(base_name))}"


def _prompt_filename_to_claude_agent_name(prompt_file: str) -> str:
    return _prompt_filename_to_agent_name(prompt_file)


def _prompt_filename_to_cursor_agent_name(prompt_file: str) -> str:
    return _prompt_filename_to_agent_name(prompt_file)


def _host_native_prompt_body(body: str, *, host: str) -> str:
    """Replace Copilot input interpolation with explicit host-native request values."""
    rendered = re.sub(
        r"\$\{input:([A-Za-z][A-Za-z0-9_-]*)(?::[^}]*)?\}",
        lambda match: f"<{match.group(1)}>",
        body,
    )
    return (
        f"Invocation contract ({host}): supply values such as `<taskId>` or `<scope>` "
        "in the user request or current conversation. Treat angle-bracket values as required "
        "request fields, not literal text.\n\n" + rendered.lstrip()
    )


def _to_claude_agent_markdown(prompt_content: str, agent_name: str) -> str:
    """Convert packaged prompt markdown into Claude subagent markdown format."""
    frontmatter, body = _split_frontmatter(prompt_content)
    description = _extract_frontmatter_value(frontmatter, "description") or agent_name
    escaped_description = description.replace('"', r"\"")
    return (
        "---\n"
        f"name: {agent_name}\n"
        f'description: "{escaped_description}"\n'
        "---\n\n"
        f"{_host_native_prompt_body(body, host='Claude Code')}"
    )


def _to_cursor_agent_markdown(prompt_content: str, agent_name: str) -> str:
    """Convert packaged prompt markdown into Cursor subagent markdown format."""
    frontmatter, body = _split_frontmatter(prompt_content)
    description = _extract_frontmatter_value(frontmatter, "description") or agent_name
    escaped_description = description.replace('"', r"\"")
    return (
        "---\n"
        f"name: {agent_name}\n"
        f'description: "{escaped_description}"\n'
        "---\n\n"
        f"{_host_native_prompt_body(body, host='Cursor')}"
    )
