from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from project_workflow import __version__
from project_workflow import cli as workflow_cli


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]


def find_uvx_executable() -> str | None:
    candidates = (
        shutil.which("uvx"),
        "/opt/homebrew/bin/uvx",
        "/usr/local/bin/uvx",
        str(Path.home() / ".local" / "bin" / "uvx"),
    )
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def run_project(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*PROJECT_CMD, *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _run_git_for_test(root: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def init_git_fixture(root: Path) -> None:
    commands = (
        ["git", "init"],
        ["git", "config", "user.email", "tests@example.com"],
        ["git", "config", "user.name", "Project Workflow Tests"],
        ["git", "add", "."],
        ["git", "commit", "-m", "fixture"],
    )
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr


def commit_git_fixture(root: Path, message: str) -> None:
    for command in (["git", "add", "."], ["git", "commit", "-m", message]):
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr


def write_namespace_config(root: Path) -> None:
    (root / ".project-workflow" / "config.json").write_text(
        "{\n"
        '  "task_id_prefixes": ["TASK", "UI", "MCP", "DEV", "WF"],\n'
        '  "default_task_id_prefix": "WF",\n'
        '  "prefix_guidance": {\n'
        '    "TASK": "General task work.",\n'
        '    "UI": "Frontend, widget, component, route, layout, visual, interaction, UX.",\n'
        '    "MCP": "MCP server, app tool, payload contract, fixture, orchestration.",\n'
        '    "DEV": "Local development, debug tooling, tunnels, build scripts.",\n'
        '    "WF": "Project workflow conventions, process automation, prompts, agent guidance."\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )


def write_unique_id_config(root: Path) -> None:
    (root / ".project-workflow" / "config.json").write_text(
        "{\n"
        '  "task_id_prefixes": ["TASK", "UI", "MCP", "DEV", "WF"],\n'
        '  "default_task_id_prefix": "WF",\n'
        '  "id_generation": {\n'
        '    "tasks": "unique",\n'
        '    "epics": "unique",\n'
        '    "fixes": "unique",\n'
        '    "backlog": "unique"\n'
        "  },\n"
        '  "unique_id_length": 5,\n'
        '  "prefix_guidance": {\n'
        '    "TASK": "General task work.",\n'
        '    "UI": "Frontend, widget, component, route, layout, visual, interaction, UX.",\n'
        '    "MCP": "MCP server, app tool, payload contract, fixture, orchestration.",\n'
        '    "DEV": "Local development, debug tooling, tunnels, build scripts.",\n'
        '    "WF": "Project workflow conventions, process automation, prompts, agent guidance."\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )


def add_accepted_doctor_warnings(root: Path, entries: list[object]) -> None:
    config_path = root / ".project-workflow" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["accepted_doctor_warnings"] = entries
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def assert_unique_id(value: str, prefix: str) -> None:
    match = re.fullmatch(rf"{re.escape(prefix)}-([0-9A-Z]{{5}})", value)
    assert match, value
    assert not match.group(1).isdigit()


def ready_requirements(task_id: str, title: str, ac_lines: list[str] | None = None) -> str:
    criteria = "\n".join(ac_lines or ["- AC1: Ready outcome is delivered."])
    requirements_text = (
        "# Requirements\n\n"
        "## Summary\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n\n"
        "## Goal\n\n"
        "- Deliver the requested ready outcome.\n\n"
        "## Non-Goals\n\n"
        "- Do not expand scope beyond this fixture.\n\n"
        "## Users & Context\n\n"
        "- Maintainers need a ready workflow artifact.\n\n"
        "## Requirements (Outcome-Focused)\n\n"
        "- The workflow artifact is specific enough to proceed.\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        f"{criteria}\n\n"
        "## Open Questions (Answer Needed)\n\n"
        "- None.\n\n"
        "## Decisions (Resolved)\n\n"
        "- Proceed with the ready fixture.\n\n"
        "## Validation Plan\n\n"
        "- Run targeted workflow validation.\n"
    )
    return workflow_cli._requirements_with_approval_envelope(
        requirements_text,
        approved_by="Test Owner",
        source="Owner approved fixture requirements.",
        decomposition=task_id.startswith("EPIC-"),
        implementation=not task_id.startswith("EPIC-"),
    )


def ready_fix_text(fix_path: Path, *, hotfix: bool = False) -> str:
    text = fix_path.read_text(encoding="utf-8")
    values = (
        ("Report", "Observed or requested", "Export fails after the delivered release."),
        ("Report", "Expected", "Export completes for supported accounts."),
        ("Report", "Affected users or systems", "Users of account export."),
        ("Report", "Delivered baseline", "The accepted export release."),
        ("Report", "Report evidence", "Reproduction log in the report."),
        ("Routing", "Rationale", "One bounded correction to delivered behavior."),
        ("Routing", "Bounded correction", "Yes; no new product outcome."),
        ("Classification", "Type", "Regression"),
        ("Classification", "Mode", "Hotfix" if hotfix else "Normal"),
        ("Classification", "Severity", "High"),
        ("Classification", "Impact", "Affected users cannot export."),
        ("Classification", "Urgency", "Resolve before the next release."),
        ("Classification", "Owner", "Workflow maintainer"),
        ("Risk", "Risk level", "Medium"),
        ("Risk", "Risks", "Export behavior could regress for adjacent account shapes."),
        ("Risk", "Rollback or containment", "Revert the bounded patch."),
        ("Fix Plan", "Scope", "Restore the delivered export behavior."),
        ("Fix Plan", "Non-goals", "No new export formats."),
        ("Fix Plan", "Affected target", "Packaged and local workflow CLI."),
        ("Fix Plan", "Branch, PR, and evidence links", "Branch plus targeted test evidence."),
        ("Fix Plan", "Verification plan", "Run targeted regression and doctor checks."),
    )
    for heading, key, value in values:
        text = workflow_cli._replace_fix_field(text, heading, key, value)
    return text


def verified_fix_text(fix_path: Path) -> str:
    text = fix_path.read_text(encoding="utf-8")
    values = (
        ("Verification", "Delivered scope", "Bounded export correction only."),
        ("Verification", "Verification result", "Targeted checks passed."),
        ("Verification", "Adjacent behavior checked", "Small and large accounts passed."),
        ("Verification", "Regression evidence", "Automated regression test passed."),
        ("Verification", "Residual risk", "Low; rollback remains available."),
    )
    for heading, key, value in values:
        text = workflow_cli._replace_fix_field(text, heading, key, value)
    return text


def write_decomposition_plan(
    epic_dir: Path,
    *,
    epic_id: str = "EPIC-001",
    rows: list[dict[str, str]],
) -> None:
    requirements_text = (epic_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    (epic_dir / workflow_cli.DECOMPOSITION_PLAN_FILENAME).write_text(
        workflow_cli._format_decomposition_plan(
            epic_id=epic_id,
            requirements_text=requirements_text,
            rows=[
                {
                    "ID": row["ID"],
                    "Title": row["Title"],
                    "Parent ACs": row.get("Parent ACs", ""),
                    "Source": row.get("Source", "Test decomposition plan"),
                }
                for row in rows
            ],
        ),
        encoding="utf-8",
    )


def write_epic_contract(
    epic_dir: Path,
    *,
    epic_id: str = "EPIC-001",
    title: str = "Ready Epic",
    ac_ids: list[str] | None = None,
) -> None:
    ac_ids = ac_ids or ["AC1"]
    rows = "\n".join(
        f"| {ac_id} | TASK-001 | Parent AC evidence plus QA pass |" for ac_id in ac_ids
    )
    (epic_dir / workflow_cli.EPIC_CONTRACT_FILENAME).write_text(
        "# Epic Contract\n\n"
        "## Summary\n\n"
        f"- Epic: {epic_id}\n"
        f"- Title: {title}\n"
        "- Last updated: 2026-07-09\n\n"
        "## Sources of Truth\n\n"
        "- Owner-approved requirements and acceptance criteria.\n\n"
        "## Invalid Substitutes\n\n"
        "- Tracker rows without matching contract and decomposition authority.\n\n"
        "## Invariants\n\n"
        "- Parent AC IDs remain stable across child work.\n\n"
        "## Artifact Targets\n\n"
        "- Workflow markdown artifacts in this epic folder.\n\n"
        "## Parent AC Proof Ownership\n\n"
        "| Parent AC | Proof Owner | Required Evidence |\n"
        "| --- | --- | --- |\n"
        f"{rows}\n",
        encoding="utf-8",
    )


def write_structured_evidence(
    child_dir: Path,
    *,
    recipe: str = "visual-reference-fidelity",
    parent_ac: str = "AC1",
    invalid_substitutes: list[str] | None = None,
    evidence_artifact_hash: str | None = None,
) -> None:
    evidence_dir = child_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    artifact = evidence_dir / "visual-comparison.txt"
    artifact.write_text("rendered comparison evidence", encoding="utf-8")
    artifact_hash = evidence_artifact_hash or workflow_cli._sha256_file(artifact)
    child_dir.joinpath(workflow_cli.STRUCTURED_EVIDENCE_FILENAME).write_text(
        json.dumps(
            {
                "task_id": "TASK-001",
                "claims": [
                    {
                        "id": "CLM-001",
                        "parent_ac": parent_ac,
                        "claim": "Delivered surface matches the reference visual.",
                        "recipe": recipe,
                        "status": "pass",
                        "commit": "abc123",
                        "timestamp": "2026-07-09T00:00:00Z",
                        "reference_artifact": "reference/playground.png",
                        "delivered_artifact": "http://localhost:3000/widget",
                        "comparison_method": "browser screenshot comparison",
                        "evidence_artifact": "evidence/visual-comparison.txt",
                        "evidence_artifact_hash": artifact_hash,
                        "invalid_substitutes": invalid_substitutes or [],
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def write_runtime_structured_evidence(
    child_dir: Path,
    *,
    execution_target: str = "working/local",
    source_artifact: str = "local checkout",
) -> None:
    evidence_dir = child_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    artifact = evidence_dir / "runtime-target-source.txt"
    artifact.write_text("runtime target used local checkout", encoding="utf-8")
    child_dir.joinpath(workflow_cli.STRUCTURED_EVIDENCE_FILENAME).write_text(
        json.dumps(
            {
                "task_id": "TASK-001",
                "claims": [
                    {
                        "id": "CLM-001",
                        "parent_ac": "AC1",
                        "claim": "Runtime target used the expected source.",
                        "recipe": "runtime-target-source",
                        "status": "pass",
                        "commit": "abc123",
                        "timestamp": "2026-07-09T00:00:00Z",
                        "execution_target": execution_target,
                        "source_artifact": source_artifact,
                        "observation_method": "browser proof plus process inspection",
                        "target_used_source_proof": "runtime response included local checkout marker",
                        "evidence_artifact": "evidence/runtime-target-source.txt",
                        "evidence_artifact_hash": workflow_cli._sha256_file(artifact),
                        "invalid_substitutes": [],
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def ready_implementation(parent_ac: str | None = None, *, qa: bool = False) -> str:
    parent_sections = ""
    if parent_ac:
        parent_sections = (
            "## Parent AC Coverage\n\n"
            f"- {parent_ac}\n\n"
            "## Parent AC Evidence\n\n"
            f"- {parent_ac}: Targeted parent evidence recorded.\n\n"
        )
    qa_section = (
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Targeted validation passed.\n"
        "- Findings: None.\n\n"
        if qa
        else "## QA & Code Review\n\n- Verdict: ____\n- Evidence: ____\n- Findings: ____\n\n"
    )
    return (
        "## User Story\n\n"
        "As a maintainer, I want a ready implementation plan, so that status gates pass.\n\n"
        f"{parent_sections}"
        "## Acceptance Criteria\n\n"
        "- [x] AC1: Ready outcome is delivered.\n\n"
        "## Validation\n\n"
        "- AC1: Targeted validation passed.\n\n"
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "| --: | ----- | ----------- | ------------------- | ----------------- | ------ |\n"
        "| 1 | Ready Work | Complete the ready fixture work. | AC1: Ready outcome is delivered. | Targeted validation. | Done |\n\n"
        f"{qa_section}"
        "## Retro\n\n"
        "- Reusable lessons: None.\n"
        "- Conventions or agent assets updated: None.\n"
        "- Follow-up tasks: None.\n"
    )


def ready_epic_retro(epic_id: str = "EPIC-001", title: str = "Ready Epic") -> str:
    return (
        "# Epic Retro\n\n"
        f"- Epic: {epic_id}\n"
        f"- Title: {title}\n"
        "- Last updated: 2026-06-17\n\n"
        "## Lessons\n\n"
        "- None.\n\n"
        "## Follow-up Tasks\n\n"
        "- None.\n\n"
        "## Deferrals\n\n"
        "- None.\n\n"
        "## Missed In-Scope Work\n\n"
        "- None.\n"
    )


def test_workflow_manifest_contract_is_deterministic() -> None:
    manifest = workflow_cli._current_workflow_manifest()

    assert manifest == workflow_cli.WorkflowManifest(
        manifest_version=1,
        package_version=__version__,
        asset_version=1,
        schema_version=1,
        applied_migrations=(),
    )
    assert workflow_cli._serialize_workflow_manifest(manifest) == (
        "{\n"
        '  "manifest_version": 1,\n'
        '  "package_version": "0.1.1",\n'
        '  "asset_version": 1,\n'
        '  "schema_version": 1,\n'
        '  "applied_migrations": []\n'
        "}\n"
    )
    assert workflow_cli._parse_workflow_manifest(
        workflow_cli._workflow_manifest_payload(manifest)
    ) == manifest


def test_repository_compatibility_classifies_supported_states(tmp_path: Path) -> None:
    assert workflow_cli._repository_compatibility(tmp_path) == workflow_cli.RepositoryCompatibility(
        "not-initialized",
        "workflow-installation-absent",
    )

    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    (workflow_dir / "TRACKER.md").write_text("# Tracker\n", encoding="utf-8")
    assert workflow_cli._repository_compatibility(tmp_path) == workflow_cli.RepositoryCompatibility(
        "legacy-unversioned",
        "manifest-absent",
    )

    manifest_path = workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME
    current_manifest = workflow_cli._current_workflow_manifest()
    workflow_cli._write_workflow_manifest(manifest_path, current_manifest)
    assert workflow_cli._repository_compatibility(tmp_path) == workflow_cli.RepositoryCompatibility(
        "current",
        "versions-current",
        current_manifest,
    )

    older_manifest = workflow_cli.WorkflowManifest(
        manifest_version=1,
        package_version="0.1.0",
        asset_version=1,
        schema_version=0,
        applied_migrations=(),
    )
    workflow_cli._write_workflow_manifest(manifest_path, older_manifest)
    assert workflow_cli._repository_compatibility(tmp_path) == workflow_cli.RepositoryCompatibility(
        "upgradeable",
        "schema-behind",
        older_manifest,
    )

    future_manifest = workflow_cli.WorkflowManifest(
        manifest_version=1,
        package_version="9.0.0",
        asset_version=1,
        schema_version=2,
        applied_migrations=("MIGRATION-001",),
    )
    workflow_cli._write_workflow_manifest(manifest_path, future_manifest)
    assert workflow_cli._repository_compatibility(tmp_path) == workflow_cli.RepositoryCompatibility(
        "unsupported-future",
        "future-schema-version",
        future_manifest,
    )

    manifest_path.write_text("{not-json}\n", encoding="utf-8")
    assert workflow_cli._repository_compatibility(tmp_path) == workflow_cli.RepositoryCompatibility(
        "invalid",
        "invalid-manifest-json",
    )


@pytest.mark.parametrize(
    ("update", "reason"),
    [
        ({"manifest_version": 2, "extension": "future"}, "future-manifest-version"),
        ({"asset_version": 2}, "future-asset-version"),
        ({"schema_version": 2}, "future-schema-version"),
    ],
)
def test_repository_compatibility_blocks_future_contracts(
    tmp_path: Path,
    update: dict[str, object],
    reason: str,
) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    payload = workflow_cli._workflow_manifest_payload(workflow_cli._current_workflow_manifest())
    payload.update(update)
    (workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME).write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    compatibility = workflow_cli._repository_compatibility(tmp_path)
    assert compatibility.state == "unsupported-future"
    assert compatibility.reason == reason


@pytest.mark.parametrize(
    ("update", "reason"),
    [
        ({"unexpected": True}, "invalid-manifest-fields"),
        ({"manifest_version": True}, "invalid-manifest-version"),
        ({"package_version": ""}, "invalid-package-version"),
        ({"asset_version": 0}, "invalid-asset-version"),
        ({"schema_version": -1}, "invalid-schema-version"),
        ({"applied_migrations": "MIGRATION-001"}, "invalid-applied-migrations"),
        ({"applied_migrations": ["bad migration"]}, "invalid-migration-id"),
        (
            {"applied_migrations": ["MIGRATION-001", "MIGRATION-001"]},
            "duplicate-migration-id",
        ),
    ],
)
def test_workflow_manifest_validation_is_strict(
    tmp_path: Path,
    update: dict[str, object],
    reason: str,
) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    payload = workflow_cli._workflow_manifest_payload(workflow_cli._current_workflow_manifest())
    payload.update(update)
    (workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME).write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    compatibility = workflow_cli._repository_compatibility(tmp_path)
    assert compatibility.state == "invalid"
    assert compatibility.reason == reason


def test_workflow_manifest_serialization_rejects_invalid_values() -> None:
    invalid_manifest = workflow_cli.WorkflowManifest(
        manifest_version=1,
        package_version="0.1.1",
        asset_version=1,
        schema_version=1,
        applied_migrations=("duplicate", "duplicate"),
    )

    with pytest.raises(workflow_cli.ManifestValidationError, match="duplicate-migration-id"):
        workflow_cli._serialize_workflow_manifest(invalid_manifest)


def test_manifest_inspection_and_writing_preserve_non_target_files(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    task_dir = workflow_dir / "tasks" / "TASK-001-Canary"
    task_dir.mkdir(parents=True)
    canaries = {
        workflow_dir / "config.json": b'{"user_setting": true}\n',
        workflow_dir / "TRACKER.md": b"# Historical tracker\n",
        workflow_dir / "BACKLOG.md": b"# User backlog\n",
        workflow_dir / "guidance.md": b"# Local guidance\n",
        task_dir / "REQUIREMENTS.md": b"# Approved requirements\n",
        task_dir / "EVIDENCE.json": b'{"claims": []}\n',
        tmp_path / "UNMARKED.txt": b"owner content\n",
    }
    for path, content in canaries.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    before = {path: path.read_bytes() for path in canaries}
    assert workflow_cli._repository_compatibility(tmp_path).state == "legacy-unversioned"
    assert {path: path.read_bytes() for path in canaries} == before
    assert not (workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME).exists()

    workflow_cli._write_workflow_manifest(
        workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME,
        workflow_cli._current_workflow_manifest(),
    )
    assert {path: path.read_bytes() for path in canaries} == before


def test_compatibility_policy_retains_legacy_and_current_schema() -> None:
    assert workflow_cli.SUPPORTED_SCHEMA_VERSIONS == (0, 1)
    assert workflow_cli.CURRENT_SCHEMA_VERSION in workflow_cli.SUPPORTED_SCHEMA_VERSIONS
    policy = " ".join(
        (REPO_ROOT / "COMPATIBILITY.md").read_text(encoding="utf-8").split()
    )
    assert "recognized pre-versioned repository shape" in policy
    assert "breaking release" in policy
    assert (
        "plans managed-asset refresh plus repository-schema transformation as one transaction"
        in policy
    )


def test_upgrade_documentation_and_agent_guidance_match_command_contract() -> None:
    readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme = " ".join(readme_text.split())
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    compatibility = (REPO_ROOT / "COMPATIBILITY.md").read_text(encoding="utf-8")
    guidance_paths = (
        REPO_ROOT / "src" / "project_workflow" / "codex" / "AGENTS.md",
        REPO_ROOT / "src" / "project_workflow" / "cursor" / "rules" / "project-workflow.mdc",
    )

    for required in (
        "doctor --format json",
        "project upgrade --agent codex",
        "--plan --format json",
        "--yes",
        "--apply",
        "--plan-fingerprint",
        "clean Git worktree",
        "PW-0001-legacy-manifest",
        "COMPATIBILITY.md",
    ):
        assert required in readme
    runbook_text = readme_text.split("### Normal Upgrade", 1)[1].split(
        "## IDs And Parallel Work", 1
    )[0]
    runbook = " ".join(runbook_text.split())
    for required in (
        "Do not run init first",
        "Doctor is not a prerequisite",
        "managed helper/agent-asset changes",
        "asks for confirmation",
        "applies the confirmed plan as one transaction",
        "Pre-versioned legacy",
        "Invalid or unsupported future manifest",
    ):
        assert required in runbook
    normal_commands = re.findall(r"```bash\n(.*?)```", runbook_text, flags=re.DOTALL)
    assert "project upgrade --agent codex" in " ".join(normal_commands[0].split())
    assert "project init" not in " ".join(normal_commands[0].split())
    assert "project upgrade --agent codex --yes" in " ".join(normal_commands[1].split())
    assert "canonical UVX `project upgrade`" in changelog
    assert "fingerprint-bound automation apply" in changelog
    assert "PW-0001-legacy-manifest" in changelog
    assert "PW-0001-legacy-manifest" in compatibility
    managed_guidance = workflow_cli._managed_project_workflow_block()
    assert "Authorized non-interactive agents add `--yes`" in managed_guidance
    assert "human invocation confirms" in managed_guidance
    for path in guidance_paths:
        guidance = path.read_text(encoding="utf-8")
        assert "init creates a new installation" in guidance
        assert "Doctor diagnoses without mutation" in guidance
        assert "canonical UVX upgrade" in guidance
        assert "managed assets and repository schema" in guidance
        assert "--apply --plan-fingerprint <SHA256>" in guidance


def test_project_init_creates_and_preserves_current_manifest(tmp_path: Path) -> None:
    first = run_project(["init"], cwd=tmp_path)
    assert first.returncode == 0, first.stdout + first.stderr
    manifest_path = tmp_path / ".project-workflow" / workflow_cli.WORKFLOW_MANIFEST_FILENAME
    expected = workflow_cli._serialize_workflow_manifest(
        workflow_cli._current_workflow_manifest()
    )
    assert manifest_path.read_text(encoding="utf-8") == expected
    assert "Repository state before init: not-initialized" in first.stdout
    assert "Repository state after init: current" in first.stdout

    before_second = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    second = run_project(["init", "--agent", "github-copilot"], cwd=tmp_path)
    assert second.returncode == 0, second.stdout + second.stderr
    assert manifest_path.read_text(encoding="utf-8") == expected
    assert "already initialized (current); init made no changes" in second.stdout
    assert "project upgrade --agent github-copilot" in second.stdout
    assert {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    } == before_second


def test_project_init_preserves_legacy_state_and_directs_upgrade(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    backlog_path = workflow_dir / "BACKLOG.md"
    backlog_path.write_text("# Historical backlog\n", encoding="utf-8")
    canary_path = tmp_path / "UNMARKED.txt"
    canary_path.write_text("owner content\n", encoding="utf-8")

    result = run_project(["init"], cwd=tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert backlog_path.read_text(encoding="utf-8") == "# Historical backlog\n"
    assert canary_path.read_text(encoding="utf-8") == "owner content\n"
    assert not (workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME).exists()
    assert "already initialized (legacy-unversioned); init made no changes" in result.stdout
    assert "project upgrade --agent github-copilot" in result.stdout


def test_project_init_never_refreshes_an_existing_versioned_repository(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    manifest_path = workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME
    behind = workflow_cli.WorkflowManifest(
        manifest_version=1,
        package_version="0.1.0",
        asset_version=1,
        schema_version=1,
        applied_migrations=(),
    )
    workflow_cli._write_workflow_manifest(manifest_path, behind)

    result = run_project(["init"], cwd=tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    preserved = workflow_cli._parse_workflow_manifest(
        json.loads(manifest_path.read_text(encoding="utf-8"))
    )
    assert preserved == behind
    assert "already initialized (current); init made no changes" in result.stdout
    assert "project upgrade --agent github-copilot" in result.stdout


@pytest.mark.parametrize("state", ["invalid", "future"])
def test_project_init_does_not_rewrite_invalid_or_future_manifest(
    tmp_path: Path,
    state: str,
) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    manifest_path = workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME
    content = b"{not-json}\n" if state == "invalid" else json.dumps(
        {
            "manifest_version": 2,
            "package_version": "9.0.0",
            "asset_version": 9,
            "schema_version": 9,
            "applied_migrations": [],
        }
    ).encode("utf-8")
    manifest_path.write_bytes(content)

    result = run_project(["init"], cwd=tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert manifest_path.read_bytes() == content
    assert "init made no changes" in result.stdout
    assert "project upgrade --agent github-copilot" in result.stdout


@pytest.mark.parametrize(
    ("setup", "expected_code", "owner", "mechanical"),
    [
        ("legacy", "PW_REPOSITORY_LEGACY_UNVERSIONED", "project-workflow", True),
        ("behind", "PW_REPOSITORY_SCHEMA_BEHIND", "project-workflow", True),
        ("invalid", "PW_REPOSITORY_INVALID", "owner", False),
        ("future", "PW_REPOSITORY_UNSUPPORTED_FUTURE", "owner", False),
    ],
)
def test_doctor_emits_structured_repository_version_findings(
    tmp_path: Path,
    setup: str,
    expected_code: str,
    owner: str,
    mechanical: bool,
) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    (workflow_dir / "TRACKER.md").write_text("# Tracker\n", encoding="utf-8")
    manifest_path = workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME
    if setup == "behind":
        workflow_cli._write_workflow_manifest(
            manifest_path,
            workflow_cli.WorkflowManifest(1, "0.1.0", 1, 0, ()),
        )
    elif setup == "invalid":
        manifest_path.write_text("{bad}\n", encoding="utf-8")
    elif setup == "future":
        workflow_cli._write_workflow_manifest(
            manifest_path,
            workflow_cli.WorkflowManifest(1, "9.0.0", 1, 9, ()),
        )

    finding = next(
        issue for issue in workflow_cli.run_doctor(tmp_path) if issue.code == expected_code
    )
    assert finding.remediation_owner == owner
    assert finding.mechanically_upgradeable is mechanical
    record = workflow_cli._doctor_issue_record(
        finding,
        root=tmp_path,
        strict=False,
        accepted_fingerprints={},
    )
    assert record["code"] == expected_code
    assert record["artifact"] == ".project-workflow/manifest.json"


def test_doctor_findings_classify_remediation_ownership() -> None:
    issues: list[workflow_cli.DoctorIssue] = []
    workflow_cli._add_issue(
        issues,
        "warning",
        ".project-workflow/tasks/TASK-001/REQUIREMENTS.md",
        "TASK-001 approval envelope is missing.",
    )
    workflow_cli._add_issue(
        issues,
        "warning",
        ".project-workflow/tasks/TASK-001/EVIDENCE.json",
        "TASK-001 evidence is stale.",
    )
    workflow_cli._add_issue(
        issues,
        "error",
        ".project-workflow/cli/workflow.py",
        "Local workflow CLI differs from packaged template.",
    )

    approval, evidence, generated_drift = issues
    assert approval.code == "PW_APPROVAL_REQUIRED"
    assert approval.remediation_owner == "owner"
    assert approval.mechanically_upgradeable is False
    assert evidence.code == "PW_EVIDENCE_REQUIRED"
    assert evidence.remediation_owner == "owner"
    assert evidence.mechanically_upgradeable is False
    assert generated_drift.code == "PW_GENERATED_ASSET_DRIFT"
    assert generated_drift.remediation_owner == "project-workflow"
    assert generated_drift.mechanically_upgradeable is True


def test_doctor_json_clean_output_is_versioned_and_deterministic(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    first = run_project(["doctor", "--format", "json"], cwd=tmp_path)
    second = run_project(["doctor", "--format", "json"], cwd=tmp_path)
    assert first.returncode == 0, first.stdout + first.stderr
    assert second.returncode == 0, second.stdout + second.stderr
    assert first.stdout == second.stdout

    payload = json.loads(first.stdout)
    assert payload == {
        "schema_version": 1,
        "root": str(tmp_path),
        "strict": False,
        "status": "pass",
        "summary": {
            "total": 0,
            "visible": 0,
            "accepted": 0,
            "errors": 0,
            "warnings": 0,
            "legacy": 0,
            "blocking": 0,
        },
        "findings": [],
    }


def test_doctor_json_matches_human_strict_failure(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    task = run_project(
        ["task", "init", "--title", "Structured Warning", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stderr
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace("| To Do |", "| In Progress |", 1),
        encoding="utf-8",
    )

    human = run_project(["doctor"], cwd=tmp_path)
    structured = run_project(["doctor", "--format", "json"], cwd=tmp_path)
    strict = run_project(["doctor", "--strict", "--format", "json"], cwd=tmp_path)
    assert human.returncode == 0
    assert "passed with warnings" in human.stdout
    assert structured.returncode == 0
    assert strict.returncode == 1

    payload = json.loads(structured.stdout)
    strict_payload = json.loads(strict.stdout)
    assert payload["status"] == "warning"
    assert strict_payload["status"] == "fail"
    assert payload["summary"]["visible"] == strict_payload["summary"]["visible"]
    assert strict_payload["summary"]["blocking"] == payload["summary"]["warnings"]
    assert strict_payload["summary"]["errors"] == strict_payload["summary"]["blocking"]
    assert strict_payload["summary"]["warnings"] == 0
    assert [finding["fingerprint"] for finding in payload["findings"]] == [
        finding["fingerprint"] for finding in strict_payload["findings"]
    ]
    assert all(finding["effective_severity"] == "error" for finding in strict_payload["findings"])
    assert "[code:" in human.stdout
    assert "[owner:" in human.stdout
    assert "[mechanical:" in human.stdout
    assert all(
        {
            "code",
            "severity",
            "effective_severity",
            "artifact",
            "message",
            "remediation_owner",
            "mechanically_upgradeable",
            "accepted",
            "accepted_reason",
            "legacy",
            "fingerprint",
        }
        == set(finding)
        for finding in payload["findings"]
    )


def test_doctor_json_includes_accepted_findings_when_human_hides_them(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    task = run_project(
        ["task", "init", "--title", "Accepted Structured Warning", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stderr
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace("| To Do |", "| In Progress |", 1),
        encoding="utf-8",
    )

    warning = next(issue for issue in workflow_cli.run_doctor(tmp_path) if issue.severity == "warning")
    fingerprint = workflow_cli._doctor_issue_fingerprint(warning, tmp_path)
    add_accepted_doctor_warnings(
        tmp_path,
        [{"fingerprint": fingerprint, "reason": "Owner retained this warning."}],
    )

    human = run_project(["doctor"], cwd=tmp_path)
    structured = run_project(["doctor", "--format", "json"], cwd=tmp_path)
    assert human.returncode == 0
    assert "accepted warning(s) hidden" in human.stdout
    payload = json.loads(structured.stdout)
    accepted = [finding for finding in payload["findings"] if finding["accepted"]]
    assert payload["summary"]["accepted"] == 1
    assert len(accepted) == 1
    assert accepted[0]["fingerprint"] == fingerprint
    assert accepted[0]["effective_severity"] == "accepted"
    assert accepted[0]["accepted_reason"] == "Owner retained this warning."


def test_generated_local_workflow_exposes_structured_doctor_output(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    local_workflow = tmp_path / ".project-workflow" / "cli" / "workflow.py"

    result = subprocess.run(
        [sys.executable, str(local_workflow), "doctor", "--format", "json"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == 1
    assert payload["status"] == "pass"


def test_upgrade_plan_is_deterministic_for_current_repository(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    workflow_cli._write_workflow_manifest(
        workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME,
        workflow_cli._current_workflow_manifest(),
    )

    first = workflow_cli._build_upgrade_plan(tmp_path)
    second = workflow_cli._build_upgrade_plan(tmp_path)
    assert first == second
    assert first["schema_version"] == 1
    assert first["repository_state"] == "current"
    assert first["steps"] == []
    assert first["target_files"] == []
    assert first["blockers"] == []
    assert first["plan_fingerprint"].startswith("sha256:")
    assert first["preconditions"] == [
        {
            "kind": "clean-worktree",
            "artifact": ".",
            "expected": "required-for-apply",
        },
        {
            "kind": "repository-state",
            "artifact": ".project-workflow/manifest.json",
            "expected": "current",
        },
    ]


def test_upgrade_plan_orders_synthetic_migrations_and_hashes_targets(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    tracker_path = workflow_dir / "TRACKER.md"
    tracker_path.write_text("# Legacy tracker\n", encoding="utf-8")
    migrations = (
        workflow_cli.MigrationDefinition(
            "MIG-0001-manifest",
            0,
            1,
            (".project-workflow/TRACKER.md", ".project-workflow/manifest.json"),
            ("normalize-tracker-header", "write-version-manifest"),
        ),
    )
    before = {path.relative_to(tmp_path): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}

    plan = workflow_cli._build_upgrade_plan(tmp_path, migrations=migrations)

    after = {path.relative_to(tmp_path): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    assert after == before
    assert [step["migration_id"] for step in plan["steps"]] == ["MIG-0001-manifest"]
    assert plan["target_files"] == [
        ".project-workflow/TRACKER.md",
        ".project-workflow/manifest.json",
    ]
    hashes = {
        item["artifact"]: item["expected"]
        for item in plan["preconditions"]
        if item["kind"] == "file-hash"
    }
    assert hashes[".project-workflow/TRACKER.md"] == (
        "sha256:" + hashlib.sha256(b"# Legacy tracker\n").hexdigest()
    )
    assert hashes[".project-workflow/manifest.json"] == workflow_cli.ABSENT_FILE_HASH
    assert plan["blockers"] == []


@pytest.mark.parametrize(
    ("migrations", "source", "target", "expected_code"),
    [
        (
            (
                workflow_cli.MigrationDefinition("DUP", 0, 1, ("a",), ("one",)),
                workflow_cli.MigrationDefinition("DUP", 1, 2, ("b",), ("two",)),
            ),
            0,
            2,
            "PW_UPGRADE_REGISTRY_DUPLICATE_ID",
        ),
        (
            (
                workflow_cli.MigrationDefinition("A", 0, 1, ("a",), ("one",)),
                workflow_cli.MigrationDefinition("B", 0, 2, ("b",), ("two",)),
            ),
            0,
            2,
            "PW_UPGRADE_REGISTRY_AMBIGUOUS",
        ),
        (
            (
                workflow_cli.MigrationDefinition("A", 0, 1, ("a",), ("one",)),
                workflow_cli.MigrationDefinition("B", 1, 0, ("b",), ("two",)),
            ),
            0,
            2,
            "PW_UPGRADE_REGISTRY_CYCLE",
        ),
        (
            (workflow_cli.MigrationDefinition("GAP", 1, 2, ("a",), ("one",)),),
            0,
            2,
            "PW_UPGRADE_REGISTRY_PATH_MISSING",
        ),
        (
            (workflow_cli.MigrationDefinition("DOWN", 1, 0, ("a",), ("one",)),),
            1,
            2,
            "PW_UPGRADE_REGISTRY_DOWNGRADE",
        ),
        (
            (workflow_cli.MigrationDefinition("UNSAFE", 0, 1, ("../secret",), ("one",)),),
            0,
            1,
            "PW_UPGRADE_REGISTRY_INVALID_TARGET",
        ),
        (
            (workflow_cli.MigrationDefinition("EMPTY", 0, 1, ("target",), ()),),
            0,
            1,
            "PW_UPGRADE_REGISTRY_INVALID_MIGRATION",
        ),
    ],
)
def test_upgrade_planner_blocks_invalid_migration_registries(
    migrations: tuple[workflow_cli.MigrationDefinition, ...],
    source: int,
    target: int,
    expected_code: str,
) -> None:
    _steps, blockers = workflow_cli._resolve_migration_path(source, target, migrations)
    assert expected_code in {blocker.code for blocker in blockers}


def test_upgrade_plan_preserves_owner_decisions_without_mutation(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    task = run_project(
        ["task", "init", "--title", "Owner Decision", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stderr
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace("| To Do |", "| In Progress |", 1),
        encoding="utf-8",
    )
    migrations = (
        workflow_cli.MigrationDefinition(
            "MIG-0001-manifest",
            0,
            1,
            (".project-workflow/manifest.json",),
            ("write-version-manifest",),
        ),
    )
    before = {path.relative_to(tmp_path): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    plan = workflow_cli._build_upgrade_plan(tmp_path, migrations=migrations)
    after = {path.relative_to(tmp_path): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}

    assert after == before
    assert plan["owner_decisions"]
    expected_owner_issues = [
        issue for issue in workflow_cli.run_doctor(tmp_path) if issue.remediation_owner == "owner"
    ]
    assert [decision["code"] for decision in plan["owner_decisions"]] == [
        issue.code for issue in expected_owner_issues
    ]
    assert [decision["message"] for decision in plan["owner_decisions"]] == [
        issue.message for issue in expected_owner_issues
    ]
    assert [decision["fingerprint"] for decision in plan["owner_decisions"]] == [
        workflow_cli._doctor_issue_fingerprint(issue, tmp_path) for issue in expected_owner_issues
    ]
    human_plan = workflow_cli._format_upgrade_plan_human(plan)
    for decision in plan["owner_decisions"]:
        assert decision["code"] in human_plan
        assert decision["artifact"] in human_plan
        assert decision["message"] in human_plan


def test_upgrade_command_plans_registered_legacy_without_mutation(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    (workflow_dir / "TRACKER.md").write_text("# Legacy tracker\n", encoding="utf-8")
    before = {path.relative_to(tmp_path): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}

    result = run_project(["upgrade", "--agent", "codex", "--plan", "--format", "json"], cwd=tmp_path)
    human = run_project(["upgrade", "--agent", "codex", "--plan"], cwd=tmp_path)

    after = {path.relative_to(tmp_path): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    assert result.returncode == 0
    assert human.returncode == 0
    assert after == before
    payload = json.loads(result.stdout)
    assert payload["repository_state"] == "legacy-unversioned"
    assert [step["migration_id"] for step in payload["steps"]] == [
        workflow_cli.LEGACY_MANIFEST_MIGRATION_ID
    ]
    assert payload["blockers"] == []
    assert ".project-workflow/manifest.json" in payload["target_files"]
    assert ".project-workflow/cli/workflow.py" in payload["asset_changes"]
    assert "AGENTS.md" in payload["asset_changes"]


def test_upgrade_default_human_flow_confirms_and_applies(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fixture = REPO_ROOT / "tests" / "fixtures" / "legacy-unversioned"
    shutil.copytree(fixture, tmp_path, dirs_exist_ok=True)
    init_git_fixture(tmp_path)

    noninteractive = run_project(["upgrade", "--agent", "codex"], cwd=tmp_path)
    assert noninteractive.returncode == 1
    assert "Non-interactive upgrade requires --yes" in noninteractive.stderr
    assert not (tmp_path / ".project-workflow" / "manifest.json").exists()

    args = workflow_cli.build_parser().parse_args(["upgrade", "--agent", "codex"])
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(workflow_cli.os, "isatty", lambda _fd: True)
    monkeypatch.setattr("builtins.input", lambda _prompt: "yes")

    args.func(args)

    output = capsys.readouterr().out
    assert "project upgrade plan: legacy-unversioned -> schema 1" in output
    assert "project upgrade apply: applied" in output
    assert "post-upgrade validation: current" in output
    assert (tmp_path / ".project-workflow" / "manifest.json").exists()
    assert (tmp_path / ".project-workflow" / "cli" / "workflow.py").exists()
    assert (tmp_path / "AGENTS.md").exists()


def test_upgrade_plan_blocks_unsafe_managed_asset_target(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    (workflow_dir / "cli" / "workflow.py").mkdir(parents=True)
    (workflow_dir / "TRACKER.md").write_text("# Legacy tracker\n", encoding="utf-8")

    plan = workflow_cli._build_repository_upgrade_plan(tmp_path, "codex")

    assert plan["target_files"] == [".project-workflow/manifest.json"]
    assert plan["blockers"] == [
        {
            "code": "PW_UPGRADE_MANAGED_ASSET_INVALID_TARGET",
            "message": (
                "Managed asset target must be a regular file or absent: "
                ".project-workflow/cli/workflow.py."
            ),
        }
    ]


def test_upgrade_plan_directs_uvx_when_package_resources_are_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    (workflow_dir / "TRACKER.md").write_text("# Legacy tracker\n", encoding="utf-8")

    def unavailable(_resource_path: str) -> str:
        raise SystemExit("package resources unavailable")

    monkeypatch.setattr(workflow_cli, "_get_package_resource", unavailable)
    plan = workflow_cli._build_repository_upgrade_plan(tmp_path, "codex")

    assert plan["blockers"] == [
        {
            "code": "PW_UPGRADE_PACKAGE_RESOURCE_UNAVAILABLE",
            "message": (
                "Managed asset resources are unavailable in this local helper. Run: "
                f"{workflow_cli.CANONICAL_UPGRADE_COMMAND} --agent codex."
            ),
        }
    ]


def test_upgrade_plan_blocks_non_file_targets(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    target_dir = workflow_dir / "not-a-file"
    target_dir.mkdir(parents=True)
    (workflow_dir / "TRACKER.md").write_text("# Tracker\n", encoding="utf-8")
    migrations = (
        workflow_cli.MigrationDefinition(
            "MIG-0001-invalid-target",
            0,
            1,
            (".project-workflow/not-a-file",),
            ("replace-target",),
        ),
    )

    plan = workflow_cli._build_upgrade_plan(tmp_path, migrations=migrations)

    assert "PW_UPGRADE_REGISTRY_INVALID_TARGET" in {
        blocker["code"] for blocker in plan["blockers"]
    }
    assert not any(
        precondition["artifact"] == ".project-workflow/not-a-file"
        and precondition["kind"] == "file-hash"
        for precondition in plan["preconditions"]
    )


def test_generated_local_workflow_exposes_upgrade_planner(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    workflow_cli._write_workflow_manifest(
        tmp_path / ".project-workflow" / workflow_cli.WORKFLOW_MANIFEST_FILENAME,
        workflow_cli._current_workflow_manifest(),
    )
    local_workflow = tmp_path / ".project-workflow" / "cli" / "workflow.py"

    result = subprocess.run(
        [sys.executable, str(local_workflow), "upgrade", "--format", "json"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["repository_state"] == "current"
    assert payload["blockers"] == []


def synthetic_manifest_migration() -> tuple[
    tuple[workflow_cli.MigrationDefinition, ...],
    dict[str, object],
]:
    migration = workflow_cli.MigrationDefinition(
        "MIG-0001-manifest",
        0,
        1,
        (
            ".project-workflow/TRACKER.md",
            ".project-workflow/manifest.json",
        ),
        ("normalize-tracker", "write-version-manifest"),
    )

    def handler(inputs: dict[str, bytes | None]) -> dict[str, bytes | None]:
        tracker = inputs[".project-workflow/TRACKER.md"] or b""
        return {
            ".project-workflow/TRACKER.md": tracker + b"\n<!-- upgraded -->\n",
            ".project-workflow/manifest.json": workflow_cli._serialize_workflow_manifest(
                workflow_cli._current_workflow_manifest()
            ).encode("utf-8"),
        }

    return (migration,), {migration.migration_id: handler}


def test_upgrade_apply_succeeds_then_current_apply_noops(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    tracker_path = workflow_dir / "TRACKER.md"
    tracker_path.write_text("# Legacy tracker\n", encoding="utf-8")
    canary_path = tmp_path / "UNMARKED.txt"
    canary_path.write_text("owner content\n", encoding="utf-8")
    migrations, handlers = synthetic_manifest_migration()
    init_git_fixture(tmp_path)
    plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=migrations,
        handlers=handlers,
    )

    result = workflow_cli._apply_upgrade_plan(
        tmp_path,
        plan["plan_fingerprint"],
        migrations=migrations,
        handlers=handlers,
    )

    assert result["status"] == "applied"
    assert result["applied_migrations"] == ["MIG-0001-manifest"]
    assert result["changed_files"] == [
        ".project-workflow/TRACKER.md",
        ".project-workflow/manifest.json",
    ]
    assert len(plan["expected_outputs"]) == 2
    human_plan = workflow_cli._format_upgrade_plan_human(plan)
    assert "expected outputs:" in human_plan
    assert plan["expected_outputs"][0]["expected"] in human_plan
    assert "<!-- upgraded -->" in tracker_path.read_text(encoding="utf-8")
    assert canary_path.read_text(encoding="utf-8") == "owner content\n"
    assert workflow_cli._repository_compatibility(tmp_path).state == "current"

    commit_git_fixture(tmp_path, "upgrade")
    current_plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=migrations,
        handlers=handlers,
    )
    noop = workflow_cli._apply_upgrade_plan(
        tmp_path,
        current_plan["plan_fingerprint"],
        migrations=migrations,
        handlers=handlers,
    )
    assert noop["status"] == "noop"
    assert noop["changed_files"] == []
    assert noop["applied_migrations"] == []


def test_upgrade_apply_rejects_changed_handler_fingerprint(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    (workflow_dir / "TRACKER.md").write_text("# Legacy tracker\n", encoding="utf-8")
    migrations, handlers = synthetic_manifest_migration()
    init_git_fixture(tmp_path)
    plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=migrations,
        handlers=handlers,
    )

    def changed_handler(inputs: dict[str, bytes | None]) -> dict[str, bytes | None]:
        original = handlers["MIG-0001-manifest"](inputs)
        original[".project-workflow/TRACKER.md"] += b"changed handler\n"
        return original

    result = workflow_cli._apply_upgrade_plan(
        tmp_path,
        plan["plan_fingerprint"],
        migrations=migrations,
        handlers={"MIG-0001-manifest": changed_handler},
    )

    assert result["status"] == "failed"
    assert result["failure"]["code"] == "PW_UPGRADE_APPLY_STALE_PLAN"


def test_upgrade_apply_cli_requires_fingerprint_and_noops_current_repo(tmp_path: Path) -> None:
    initialized = run_project(["init", "--agent", "github-copilot"], cwd=tmp_path)
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    init_git_fixture(tmp_path)
    plan_result = run_project(
        ["upgrade", "--agent", "github-copilot", "--plan", "--format", "json"],
        cwd=tmp_path,
    )
    assert plan_result.returncode == 0, plan_result.stdout + plan_result.stderr
    fingerprint = json.loads(plan_result.stdout)["plan_fingerprint"]

    missing = run_project(
        ["upgrade", "--agent", "github-copilot", "--apply"], cwd=tmp_path
    )
    assert missing.returncode == 1
    assert "--apply requires --plan-fingerprint" in missing.stderr

    applied = run_project(
        [
            "upgrade",
            "--agent",
            "github-copilot",
            "--apply",
            "--plan-fingerprint",
            fingerprint,
            "--format",
            "json",
        ],
        cwd=tmp_path,
    )
    assert applied.returncode == 0, applied.stdout + applied.stderr
    payload = json.loads(applied.stdout)
    assert payload["status"] == "noop"
    assert payload["noop"] is True


@pytest.mark.parametrize("fail_after", [0, 1, 2])
def test_upgrade_apply_failure_restores_all_targets(
    tmp_path: Path,
    fail_after: int,
) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    tracker_path = workflow_dir / "TRACKER.md"
    tracker_path.write_text("# Legacy tracker\n", encoding="utf-8")
    migrations, handlers = synthetic_manifest_migration()
    init_git_fixture(tmp_path)
    plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=migrations,
        handlers=handlers,
    )
    before = {path.relative_to(tmp_path): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file() and ".git" not in path.parts}

    result = workflow_cli._apply_upgrade_plan(
        tmp_path,
        plan["plan_fingerprint"],
        migrations=migrations,
        handlers=handlers,
        fail_after_replacements=fail_after,
    )

    after = {path.relative_to(tmp_path): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file() and ".git" not in path.parts}
    assert result["status"] == "failed"
    assert result["failure"]["code"] == "PW_UPGRADE_APPLY_REPLACEMENT_FAILED"
    assert after == before
    assert not list(tmp_path.rglob("*.tmp"))
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert status.stdout == ""


def test_upgrade_apply_rejects_stale_dirty_and_missing_handler(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    tracker_path = workflow_dir / "TRACKER.md"
    tracker_path.write_text("# Legacy tracker\n", encoding="utf-8")
    migrations, handlers = synthetic_manifest_migration()
    init_git_fixture(tmp_path)
    plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=migrations,
        handlers=handlers,
    )

    stale_plan = workflow_cli._apply_upgrade_plan(
        tmp_path,
        "sha256:" + "0" * 64,
        migrations=migrations,
        handlers=handlers,
    )
    assert stale_plan["failure"]["code"] == "PW_UPGRADE_APPLY_STALE_PLAN"

    missing_handler_plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=migrations,
        handlers={},
    )
    assert missing_handler_plan["blockers"][0]["code"] == "PW_UPGRADE_HANDLER_MISSING"
    missing_handler = workflow_cli._apply_upgrade_plan(
        tmp_path,
        missing_handler_plan["plan_fingerprint"],
        migrations=migrations,
        handlers={},
    )
    assert missing_handler["failure"]["code"] == "PW_UPGRADE_APPLY_BLOCKED"

    (tmp_path / "UNTRACKED.txt").write_text("dirty\n", encoding="utf-8")
    dirty_plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=migrations,
        handlers=handlers,
    )
    dirty = workflow_cli._apply_upgrade_plan(
        tmp_path,
        dirty_plan["plan_fingerprint"],
        migrations=migrations,
        handlers=handlers,
    )
    assert dirty["failure"]["code"] == "PW_UPGRADE_APPLY_DIRTY_WORKTREE"

    (tmp_path / "UNTRACKED.txt").unlink()
    tracker_path.write_text("changed after plan\n", encoding="utf-8")
    stale_file = workflow_cli._apply_upgrade_plan(
        tmp_path,
        plan["plan_fingerprint"],
        migrations=migrations,
        handlers=handlers,
    )
    assert stale_file["failure"]["code"] in {
        "PW_UPGRADE_APPLY_STALE_PLAN",
        "PW_UPGRADE_APPLY_STALE_FILE",
    }


def test_upgrade_apply_rejects_invalid_handler_without_mutation(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    tracker_path = workflow_dir / "TRACKER.md"
    tracker_path.write_text("# Legacy tracker\n", encoding="utf-8")
    migrations, _handlers = synthetic_manifest_migration()
    init_git_fixture(tmp_path)

    def invalid_handler(_inputs: dict[str, bytes | None]) -> dict[str, bytes | None]:
        return {"UNDECLARED.txt": b"invalid"}

    plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=migrations,
        handlers={"MIG-0001-manifest": invalid_handler},
    )
    before = tracker_path.read_bytes()
    assert plan["blockers"][0]["code"] == "PW_UPGRADE_HANDLER_INVALID"

    result = workflow_cli._apply_upgrade_plan(
        tmp_path,
        plan["plan_fingerprint"],
        migrations=migrations,
        handlers={"MIG-0001-manifest": invalid_handler},
    )

    assert result["status"] == "failed"
    assert result["failure"]["code"] == "PW_UPGRADE_APPLY_BLOCKED"
    assert tracker_path.read_bytes() == before
    assert not (tmp_path / "UNDECLARED.txt").exists()


def test_production_legacy_fixture_plan_apply_preservation_and_noop(tmp_path: Path) -> None:
    fixture = REPO_ROOT / "tests" / "fixtures" / "legacy-unversioned"
    shutil.copytree(fixture, tmp_path, dirs_exist_ok=True)
    fixture_files = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    init = run_project(["init", "--agent", "codex"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    assert "init made no changes" in init.stdout
    assert "project upgrade --agent codex" in init.stdout
    assert not (tmp_path / ".project-workflow" / "manifest.json").exists()
    for relative_path, content in fixture_files.items():
        assert (tmp_path / relative_path).read_bytes() == content

    init_git_fixture(tmp_path)
    before_plan = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }
    owner_findings_before = [
        (issue.code, issue.path, issue.message)
        for issue in workflow_cli.run_doctor(tmp_path)
        if issue.remediation_owner == "owner"
    ]
    human_plan = run_project(["upgrade", "--agent", "codex", "--plan"], cwd=tmp_path)
    assert human_plan.returncode == 0, human_plan.stdout + human_plan.stderr
    plan_result = run_project(
        ["upgrade", "--agent", "codex", "--plan", "--format", "json"],
        cwd=tmp_path,
    )
    assert plan_result.returncode == 0, plan_result.stdout + plan_result.stderr
    plan = json.loads(plan_result.stdout)
    assert [step["migration_id"] for step in plan["steps"]] == [
        workflow_cli.LEGACY_MANIFEST_MIGRATION_ID
    ]
    assert ".project-workflow/manifest.json" in plan["target_files"]
    assert ".project-workflow/cli/workflow.py" in plan["asset_changes"]
    assert "AGENTS.md" in plan["asset_changes"]
    assert plan["blockers"] == []
    assert {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file() and ".git" not in path.parts
    } == before_plan

    apply_result = run_project(
        ["upgrade", "--agent", "codex", "--yes", "--format", "json"],
        cwd=tmp_path,
    )
    assert apply_result.returncode == 0, apply_result.stdout + apply_result.stderr
    result = json.loads(apply_result.stdout)
    assert result["status"] == "applied"
    assert ".project-workflow/manifest.json" in result["changed_files"]
    assert ".project-workflow/cli/workflow.py" in result["changed_files"]
    assert "AGENTS.md" in result["changed_files"]
    assert result["post_upgrade"]["repository_state"] == "current"
    assert result["post_upgrade"]["owner_finding_count"] == len(owner_findings_before)
    manifest = workflow_cli._parse_workflow_manifest(
        json.loads(
            (tmp_path / ".project-workflow" / "manifest.json").read_text(encoding="utf-8")
        )
    )
    assert manifest.applied_migrations == (workflow_cli.LEGACY_MANIFEST_MIGRATION_ID,)
    for relative_path, content in before_plan.items():
        assert (tmp_path / relative_path).read_bytes() == content
    owner_findings_after = [
        (issue.code, issue.path, issue.message)
        for issue in workflow_cli.run_doctor(tmp_path)
        if issue.remediation_owner == "owner"
    ]
    assert owner_findings_after == owner_findings_before

    local_workflow = tmp_path / ".project-workflow" / "cli" / "workflow.py"
    strict_doctor = subprocess.run(
        [sys.executable, str(local_workflow), "doctor", "--strict"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert strict_doctor.returncode == 1
    assert "PW_APPROVAL_REQUIRED" in strict_doctor.stdout
    assert "project upgrade" not in strict_doctor.stdout

    commit_git_fixture(tmp_path, "production upgrade")
    current_plan_result = subprocess.run(
        [
            sys.executable,
            str(local_workflow),
            "upgrade",
            "--agent",
            "codex",
            "--plan",
            "--format",
            "json",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert current_plan_result.returncode == 0, (
        current_plan_result.stdout + current_plan_result.stderr
    )
    current_plan = json.loads(current_plan_result.stdout)
    assert current_plan["target_files"] == []
    noop_result = subprocess.run(
        [
            sys.executable,
            str(local_workflow),
            "upgrade",
            "--agent",
            "codex",
            "--yes",
            "--format",
            "json",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert noop_result.returncode == 0, noop_result.stdout + noop_result.stderr
    noop = json.loads(noop_result.stdout)
    assert noop["status"] == "noop"


def test_production_legacy_migration_failure_restores_manifest_absence(tmp_path: Path) -> None:
    fixture = REPO_ROOT / "tests" / "fixtures" / "legacy-unversioned"
    shutil.copytree(fixture, tmp_path, dirs_exist_ok=True)
    init = run_project(["init", "--agent", "codex"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    init_git_fixture(tmp_path)
    plan = workflow_cli._build_upgrade_plan(
        tmp_path,
        migrations=workflow_cli.PRODUCTION_MIGRATIONS,
        handlers=workflow_cli.PRODUCTION_MIGRATION_HANDLERS,
    )

    failed = workflow_cli._apply_upgrade_plan(
        tmp_path,
        plan["plan_fingerprint"],
        migrations=workflow_cli.PRODUCTION_MIGRATIONS,
        handlers=workflow_cli.PRODUCTION_MIGRATION_HANDLERS,
        fail_after_replacements=1,
    )

    assert failed["failure"]["code"] == "PW_UPGRADE_APPLY_REPLACEMENT_FAILED"
    assert not (tmp_path / ".project-workflow" / "manifest.json").exists()
    assert not list(tmp_path.rglob("*.tmp"))


def test_combined_upgrade_failure_restores_assets_and_schema(tmp_path: Path) -> None:
    fixture = REPO_ROOT / "tests" / "fixtures" / "legacy-unversioned"
    shutil.copytree(fixture, tmp_path, dirs_exist_ok=True)
    init_git_fixture(tmp_path)
    before = {
        path.relative_to(tmp_path): (path.read_bytes(), path.stat().st_mode & 0o777)
        for path in tmp_path.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }
    plan = workflow_cli._build_repository_upgrade_plan(tmp_path, "codex")

    failed = workflow_cli._apply_repository_upgrade_plan(
        tmp_path,
        "codex",
        plan["plan_fingerprint"],
        fail_after_replacements=2,
    )

    assert failed["status"] == "failed"
    assert failed["failure"]["code"] == "PW_UPGRADE_APPLY_REPLACEMENT_FAILED"
    assert {
        path.relative_to(tmp_path): (path.read_bytes(), path.stat().st_mode & 0o777)
        for path in tmp_path.rglob("*")
        if path.is_file() and ".git" not in path.parts
    } == before
    assert not (tmp_path / ".project-workflow" / "manifest.json").exists()
    assert not (tmp_path / ".project-workflow" / "cli" / "workflow.py").exists()


def test_doctor_passes_for_clean_initialized_repo(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    assert ".project-workflow/guidance.md" in init.stdout
    assert (tmp_path / ".project-workflow" / "guidance.md").exists()
    assert (tmp_path / ".project-workflow" / "config.json").exists()
    backlog_text = (tmp_path / ".project-workflow" / "BACKLOG.md").read_text(encoding="utf-8")
    assert (
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |"
        in backlog_text
    )
    assert "`Task Candidate`" in backlog_text
    assert "`Accepted` means worth keeping or preparing" in backlog_text
    assert "active execution status lives in `.project-workflow/TRACKER.md`" in backlog_text
    assert "<!-- project-workflow:start -->" in (
        tmp_path / ".github" / "copilot-instructions.md"
    ).read_text(encoding="utf-8")
    assert "project-workflow:generated" in (
        tmp_path / ".github" / "prompts" / "Task.prompt.md"
    ).read_text(encoding="utf-8")
    backlog_prompt = (tmp_path / ".github" / "prompts" / "Backlog.prompt.md").read_text(
        encoding="utf-8"
    )
    assert "project.backlog" in backlog_prompt
    assert "Promoted rows stay in the backlog" in backlog_prompt

    second_init = run_project(["init"], cwd=tmp_path)
    assert second_init.returncode == 0, second_init.stderr
    assert not list(tmp_path.rglob("*.new*"))

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "no issues found" in doctor.stdout

    validate = run_project(["validate"], cwd=tmp_path)
    assert validate.returncode == 0, validate.stdout + validate.stderr


def test_project_init_preserves_existing_backlog(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    backlog_path = workflow_dir / "BACKLOG.md"
    existing_backlog = (
        "# Backlog\n\n"
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| BL-007 | Existing Idea | Idea | High | Accepted | Keep this row. |  | User-owned. |\n"
    )
    backlog_path.write_text(existing_backlog, encoding="utf-8")

    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    assert backlog_path.read_text(encoding="utf-8") == existing_backlog


def test_backlog_helpers_allocate_ids_and_detect_duplicates(tmp_path: Path) -> None:
    backlog_path = tmp_path / "BACKLOG.md"
    backlog_path.write_text(
        "# Backlog\n\n"
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| BL-001 | First | Idea | Unset | Proposed | First outcome. |  |  |\n"
        "| BL-010 | Later | Follow-Up | Low | Deferred | Later outcome. |  |  |\n"
        "| BL-010 | Duplicate | Idea | High | Accepted | Duplicate outcome. |  |  |\n",
        encoding="utf-8",
    )

    rows = workflow_cli._backlog_rows(backlog_path)
    assert workflow_cli._next_backlog_id_from_rows(rows) == "BL-011"
    assert workflow_cli._duplicate_backlog_ids(rows) == ["BL-010"]


def test_backlog_cli_add_list_update_status_and_validate(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr

    add = run_project(
        [
            "backlog",
            "add",
            "--title",
            "Backlog UX",
            "--type",
            "Task Candidate",
            "--priority",
            "High",
            "--outcome",
            "Capture future UX work.",
            "--notes",
            "Owner requested.",
        ],
        cwd=tmp_path,
    )
    assert add.returncode == 0, add.stdout + add.stderr
    assert "Added backlog row BL-001" in add.stdout

    backlog_path = tmp_path / ".project-workflow" / "BACKLOG.md"
    before_list = backlog_path.read_text(encoding="utf-8")
    list_rows = run_project(["backlog", "list"], cwd=tmp_path)
    assert list_rows.returncode == 0, list_rows.stdout + list_rows.stderr
    assert "BL-001: Backlog UX [Task Candidate / High / Proposed]" in list_rows.stdout
    assert backlog_path.read_text(encoding="utf-8") == before_list

    invalid_status = run_project(
        ["backlog", "status", "--id", "BL-001", "--to", "In Progress"],
        cwd=tmp_path,
    )
    assert invalid_status.returncode != 0
    assert "invalid choice" in invalid_status.stderr
    assert backlog_path.read_text(encoding="utf-8") == before_list

    invalid_priority = run_project(
        ["backlog", "update", "--id", "BL-001", "--priority", "Urgent"],
        cwd=tmp_path,
    )
    assert invalid_priority.returncode != 0
    assert "invalid choice" in invalid_priority.stderr
    assert backlog_path.read_text(encoding="utf-8") == before_list

    update = run_project(
        [
            "backlog",
            "update",
            "--id",
            "BL-001",
            "--priority",
            "Medium",
            "--outcome",
            "Capture future UX work with clearer scope.",
        ],
        cwd=tmp_path,
    )
    assert update.returncode == 0, update.stdout + update.stderr

    status = run_project(["backlog", "status", "--id", "BL-001", "--to", "Accepted"], cwd=tmp_path)
    assert status.returncode == 0, status.stdout + status.stderr

    backlog_text = backlog_path.read_text(encoding="utf-8")
    assert "| BL-001 | Backlog UX | Task Candidate | Medium | Accepted |" in backlog_text

    validate = run_project(["backlog", "validate"], cwd=tmp_path)
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert "Backlog validation passed" in validate.stdout


def test_unique_id_generation_for_task_epic_backlog_and_promotion(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    write_unique_id_config(tmp_path)

    backlog_add = run_project(
        [
            "backlog",
            "add",
            "--title",
            "Unique Backlog",
            "--type",
            "Task Candidate",
            "--priority",
            "High",
            "--status",
            "Accepted",
            "--outcome",
            "A team-safe backlog row exists.",
        ],
        cwd=tmp_path,
    )
    assert backlog_add.returncode == 0, backlog_add.stdout + backlog_add.stderr
    backlog_match = re.search(r"Added backlog row (BL-[0-9A-Z]{5})", backlog_add.stdout)
    assert backlog_match, backlog_add.stdout
    backlog_id = backlog_match.group(1)
    assert_unique_id(backlog_id, "BL")

    task = run_project(
        ["task", "init", "--title", "Unique Task", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_match = re.search(r"Assigned ID: (WF-[0-9A-Z]{5})", task.stdout)
    assert task_match, task.stdout
    task_id = task_match.group(1)
    assert_unique_id(task_id, "WF")
    assert next((tmp_path / ".project-workflow" / "tasks").glob(f"{task_id}-Unique-Task"))

    epic = run_project(["epic", "init", "--title", "Unique Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_match = re.search(r"Assigned ID: (EPIC-[0-9A-Z]{5})", epic.stdout)
    assert epic_match, epic.stdout
    epic_id = epic_match.group(1)
    assert_unique_id(epic_id, "EPIC")
    assert next((tmp_path / ".project-workflow" / "tasks").glob(f"{epic_id}-Unique-Epic"))

    fix = run_project(["fix", "init", "--title", "Unique Fix"], cwd=tmp_path)
    assert fix.returncode == 0, fix.stdout + fix.stderr
    fix_match = re.search(r"Assigned ID: (FIX-[0-9A-Z]{5})", fix.stdout)
    assert fix_match, fix.stdout
    fix_id = fix_match.group(1)
    assert_unique_id(fix_id, "FIX")
    assert next((tmp_path / ".project-workflow" / "tasks").glob(f"{fix_id}-Unique-Fix"))

    promote = run_project(["backlog", "promote", "--id", backlog_id, "--to", "task"], cwd=tmp_path)
    assert promote.returncode == 0, promote.stdout + promote.stderr
    promoted_match = re.search(r"Promoted .* to task (WF-[0-9A-Z]{5})", promote.stdout)
    assert promoted_match, promote.stdout
    promoted_id = promoted_match.group(1)
    assert_unique_id(promoted_id, "WF")

    backlog_text = (tmp_path / ".project-workflow" / "BACKLOG.md").read_text(encoding="utf-8")
    assert f"| {backlog_id} | Unique Backlog | Task Candidate | High | Promoted |" in backlog_text
    assert (
        f"| {backlog_id} | Unique Backlog | Task Candidate | High | Promoted | "
        f"A team-safe backlog row exists. | {promoted_id} |"
    ) in backlog_text

    validate = run_project(["backlog", "validate"], cwd=tmp_path)
    assert validate.returncode == 0, validate.stdout + validate.stderr
    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr


def test_unique_id_allocator_retries_local_collisions(monkeypatch) -> None:
    choices = iter("ABCDE" "FGHIJ")
    monkeypatch.setattr(workflow_cli.secrets, "choice", lambda _alphabet: next(choices))

    allocated = workflow_cli._next_unique_id_from_used(
        {"TASK-ABCDE"},
        prefix="TASK",
        length=5,
    )

    assert allocated == "TASK-FGHIJ"


def test_backlog_validate_reports_invalid_rows_and_bad_promoted_refs(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    backlog_path = tmp_path / ".project-workflow" / "BACKLOG.md"
    backlog_path.write_text(
        "# Backlog\n\n"
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| BL-001 | Bad Type | Feature | High | Proposed | Outcome. |  |  |\n"
        "| BL-001 | Duplicate | Idea | Urgent | Done | Outcome. | TASK-999 |  |\n"
        "| BL-002 | Promoted Missing Ref | Idea | Low | Promoted | Outcome. |  |  |\n",
        encoding="utf-8",
    )

    validate = run_project(["backlog", "validate"], cwd=tmp_path)
    assert validate.returncode == 1, validate.stdout + validate.stderr
    assert "duplicate ID 'BL-001'" in validate.stdout
    assert "invalid Type 'Feature'" in validate.stdout
    assert "invalid Priority 'Urgent'" in validate.stdout
    assert "invalid Status 'Done'" in validate.stdout
    assert "Promoted To reference does not exist: TASK-999" in validate.stdout
    assert "BL-002 is Promoted but lacks Promoted To" in validate.stdout


def test_doctor_reports_existing_backlog_validation_errors(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    (tmp_path / ".project-workflow" / "BACKLOG.md").write_text(
        "# Backlog\n\n"
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| BL-001 | Bad Status | Idea | Unset | In Progress | Outcome. |  |  |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 1, doctor.stdout + doctor.stderr
    assert "BL-001 has invalid Status 'In Progress'" in doctor.stdout


def test_backlog_promote_to_task_preserves_source_and_row(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    add = run_project(
        [
            "backlog",
            "add",
            "--title",
            "Export Ideas",
            "--type",
            "Task Candidate",
            "--priority",
            "High",
            "--status",
            "Accepted",
            "--outcome",
            "A user can export ideas.",
            "--notes",
            "Source conversation.",
        ],
        cwd=tmp_path,
    )
    assert add.returncode == 0, add.stdout + add.stderr

    promote = run_project(["backlog", "promote", "--id", "BL-001", "--to", "task"], cwd=tmp_path)
    assert promote.returncode == 0, promote.stdout + promote.stderr
    assert "Promoted BL-001 to task TASK-001" in promote.stdout

    backlog_text = (tmp_path / ".project-workflow" / "BACKLOG.md").read_text(encoding="utf-8")
    assert "| BL-001 | Export Ideas | Task Candidate | High | Promoted |" in backlog_text
    assert "| TASK-001 |" in backlog_text

    task_dir = tmp_path / ".project-workflow" / "tasks" / "TASK-001-Export-Ideas"
    requirements_text = (task_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    assert "## Backlog Source" in requirements_text
    assert "- ID: BL-001" in requirements_text
    assert "- Outcome: A user can export ideas." in requirements_text

    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-001 | Export Ideas | To Do | `tasks/TASK-001-Export-Ideas/IMPLEMENTATION.md` |" in tracker_text
    validate = run_project(["backlog", "validate"], cwd=tmp_path)
    assert validate.returncode == 0, validate.stdout + validate.stderr


def test_backlog_promote_to_epic_preserves_source_and_row(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    add = run_project(
        [
            "backlog",
            "add",
            "--title",
            "Planning Foundation",
            "--type",
            "Epic Candidate",
            "--priority",
            "Medium",
            "--status",
            "Accepted",
            "--outcome",
            "Planning work has a parent epic.",
        ],
        cwd=tmp_path,
    )
    assert add.returncode == 0, add.stdout + add.stderr

    promote = run_project(["backlog", "promote", "--id", "BL-001", "--to", "epic"], cwd=tmp_path)
    assert promote.returncode == 0, promote.stdout + promote.stderr
    assert "Promoted BL-001 to epic EPIC-001" in promote.stdout

    epic_dir = tmp_path / ".project-workflow" / "tasks" / "EPIC-001-Planning-Foundation"
    assert (epic_dir / "TRACKER.md").exists()
    assert (epic_dir / "ACCEPTANCE-MAP.md").exists()
    requirements_text = (epic_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    assert "## Backlog Source" in requirements_text
    assert "- ID: BL-001" in requirements_text
    assert "- Type: Epic Candidate" in requirements_text

    backlog_text = (tmp_path / ".project-workflow" / "BACKLOG.md").read_text(encoding="utf-8")
    assert "| BL-001 | Planning Foundation | Epic Candidate | Medium | Promoted |" in backlog_text
    assert "| EPIC-001 |" in backlog_text
    validate = run_project(["backlog", "validate"], cwd=tmp_path)
    assert validate.returncode == 0, validate.stdout + validate.stderr


def test_backlog_promote_requires_accepted_or_explicit_accept(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    add = run_project(
        [
            "backlog",
            "add",
            "--title",
            "Unaccepted Work",
            "--outcome",
            "Potential work is captured.",
        ],
        cwd=tmp_path,
    )
    assert add.returncode == 0, add.stdout + add.stderr

    blocked = run_project(["backlog", "promote", "--id", "BL-001", "--to", "task"], cwd=tmp_path)
    assert blocked.returncode == 1, blocked.stdout + blocked.stderr
    assert "must be Accepted before promotion" in blocked.stderr
    assert not (tmp_path / ".project-workflow" / "tasks" / "TASK-001-Unaccepted-Work").exists()

    promoted = run_project(
        ["backlog", "promote", "--id", "BL-001", "--to", "task", "--accept"],
        cwd=tmp_path,
    )
    assert promoted.returncode == 0, promoted.stdout + promoted.stderr
    assert (tmp_path / ".project-workflow" / "tasks" / "TASK-001-Unaccepted-Work").exists()


def test_generated_local_workflow_exposes_doctor(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    local_workflow = tmp_path / ".project-workflow" / "cli" / "workflow.py"
    completed = subprocess.run(
        [sys.executable, str(local_workflow), "doctor", "--help"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "Validate workflow tracker state" in completed.stdout

    backlog_help = subprocess.run(
        [sys.executable, str(local_workflow), "backlog", "--help"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert backlog_help.returncode == 0, backlog_help.stdout + backlog_help.stderr
    assert "Backlog-related commands" in backlog_help.stdout
    assert "promote" in backlog_help.stdout


def test_task_scaffold_uses_ac_mapped_implementation_shape(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Mapped Implementation Shape", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr

    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    requirements_text = (task_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    implementation_text = (task_dir / "IMPLEMENTATION.md").read_text(encoding="utf-8")

    assert "- AC1: ____" in requirements_text
    assert "- [ ] AC1: ____" in implementation_text
    assert "| 1 | ____ | ____ | AC1: ____ | ____ | To Do |" in implementation_text


def test_task_init_allocates_after_epic_child_ids(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Nested Children"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "TASK-004-Existing-Child").mkdir()
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-009 | Existing Proposed Child | Proposed | Task | AC1 |  |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    task = run_project(
        ["task", "init", "--title", "After Epic Children", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    assert "Assigned ID: TASK-010" in task.stdout
    assert (tmp_path / ".project-workflow" / "tasks" / "TASK-010-After-Epic-Children").exists()


def test_epic_decompose_allocates_after_all_epic_child_ids(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    existing_epic = run_project(["epic", "init", "--title", "Existing Children"], cwd=tmp_path)
    assert existing_epic.returncode == 0, existing_epic.stdout + existing_epic.stderr
    existing_epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (existing_epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-009 | Existing Child | Complete | Task | AC1 | tasks/EPIC-001-Existing-Children/TASK-009-Existing-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    new_epic = run_project(["epic", "init", "--title", "New Children"], cwd=tmp_path)
    assert new_epic.returncode == 0, new_epic.stdout + new_epic.stderr
    new_epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-002-*"))
    (new_epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-002",
            "New Children",
            ["- AC1: First new child is mapped."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(new_epic_dir, epic_id="EPIC-002", title="New Children")

    decompose = run_project(["epic", "decompose", "--epic-id", "EPIC-002"], cwd=tmp_path)
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr
    tracker_text = (new_epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-010 | First new child is mapped | Proposed | Task | AC1 |" in tracker_text


def test_task_status_updates_packaged_and_local_workflow(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Lifecycle Status", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-001", "Lifecycle Status"),
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")

    packaged_status = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Analysing"],
        cwd=tmp_path,
    )
    assert packaged_status.returncode == 0, packaged_status.stdout + packaged_status.stderr
    assert "Updated TASK-001: To Do -> Analysing" in packaged_status.stdout

    local_workflow = tmp_path / ".project-workflow" / "cli" / "workflow.py"
    local_status = subprocess.run(
        [
            sys.executable,
            str(local_workflow),
            "task",
            "status",
            "--id",
            "TASK-001-Lifecycle-Status",
            "--to",
            "Ready",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert local_status.returncode == 0, local_status.stdout + local_status.stderr
    assert "Updated TASK-001: Analysing -> Ready" in local_status.stdout

    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-001 | Lifecycle Status | Ready |" in tracker_text


def test_configured_task_prefixes_work_for_packaged_and_local_workflow(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    write_namespace_config(tmp_path)
    custom_config = (tmp_path / ".project-workflow" / "config.json").read_text(encoding="utf-8")
    refresh = run_project(["init"], cwd=tmp_path)
    assert refresh.returncode == 0, refresh.stdout + refresh.stderr
    assert (tmp_path / ".project-workflow" / "config.json").read_text(encoding="utf-8") == custom_config

    packaged_task = run_project(
        ["task", "init", "--prefix", "WF", "--title", "Workflow Status", "--update-tracker"],
        cwd=tmp_path,
    )
    assert packaged_task.returncode == 0, packaged_task.stdout + packaged_task.stderr
    assert "Assigned ID: WF-001" in packaged_task.stdout
    workflow_task_dir = tmp_path / ".project-workflow" / "tasks" / "WF-001-Workflow-Status"
    assert workflow_task_dir.exists()
    (workflow_task_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("WF-001", "Workflow Status"),
        encoding="utf-8",
    )
    (workflow_task_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation(), encoding="utf-8"
    )

    status = run_project(
        ["task", "status", "--id", "WF-001-Workflow-Status", "--to", "Analysing"],
        cwd=tmp_path,
    )
    assert status.returncode == 0, status.stdout + status.stderr
    assert "Updated WF-001: To Do -> Analysing" in status.stdout

    local_workflow = tmp_path / ".project-workflow" / "cli" / "workflow.py"
    local_task = subprocess.run(
        [
            sys.executable,
            str(local_workflow),
            "task",
            "init",
            "--prefix",
            "MCP",
            "--title",
            "Tool Contract",
            "--update-tracker",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert local_task.returncode == 0, local_task.stdout + local_task.stderr
    assert "Assigned ID: MCP-001" in local_task.stdout

    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| WF-001 | Workflow Status | Analysing | `tasks/WF-001-Workflow-Status/IMPLEMENTATION.md` |" in tracker_text
    assert "| MCP-001 | Tool Contract | To Do | `tasks/MCP-001-Tool-Contract/IMPLEMENTATION.md` |" in tracker_text


def test_task_status_rejects_illegal_transition_without_force(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Illegal Lifecycle Jump", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr

    illegal = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Testing"],
        cwd=tmp_path,
    )
    assert illegal.returncode != 0
    assert "Illegal status transition for TASK-001: To Do -> Testing" in illegal.stderr

    missing_reason = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Testing", "--force"],
        cwd=tmp_path,
    )
    assert missing_reason.returncode != 0
    assert "--force requires --reason" in missing_reason.stderr

    forced = run_project(
        [
            "task",
            "status",
            "--id",
            "TASK-001",
            "--to",
            "Testing",
            "--force",
            "--reason",
            "Recovering imported tracker state",
        ],
        cwd=tmp_path,
    )
    assert forced.returncode == 0, forced.stdout + forced.stderr
    assert "Updated TASK-001: To Do -> Testing" in forced.stdout
    assert "Forced transition reason: Recovering imported tracker state" in forced.stdout


def test_task_status_blocks_complete_without_qa_evidence(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Completion Gate", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-001", "Completion Gate"),
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")

    for status in ("Analysing", "Plan Confirmed", "In Progress", "Testing", "Review"):
        status_result = run_project(
            ["task", "status", "--id", "TASK-001", "--to", status],
            cwd=tmp_path,
        )
        assert status_result.returncode == 0, status_result.stdout + status_result.stderr

    blocked = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert blocked.returncode != 0
    assert "cannot move to Complete without non-placeholder QA/code-review evidence" in blocked.stderr

    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    implementation_path = task_dir / "IMPLEMENTATION.md"
    implementation_text = implementation_path.read_text(encoding="utf-8")
    implementation_path.write_text(
        implementation_text.replace(
            "- Verdict: ____\n- Evidence: ____\n- Findings: ____",
            "- Verdict: Pass\n- Evidence: Targeted lifecycle validation passed.\n- Findings: None.",
        ),
        encoding="utf-8",
    )

    completed = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "Updated TASK-001: Review -> Complete" in completed.stdout


def test_task_status_validates_task_id_and_docs_path(tmp_path: Path) -> None:
    missing_tracker = run_project(
        ["task", "init", "--title", "Missing Tracker", "--update-tracker"],
        cwd=tmp_path,
    )
    assert missing_tracker.returncode != 0
    assert (
        "uvx --from git+https://github.com/johndetlefs/project-workflow.git project init"
        in missing_tracker.stderr
    )

    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Missing Docs", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr

    invalid_id = run_project(
        ["task", "status", "--id", "APP-001", "--to", "Analysing"],
        cwd=tmp_path,
    )
    assert invalid_id.returncode != 0
    assert "Task status only supports TASK-### IDs" in invalid_id.stderr

    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_text = tracker_path.read_text(encoding="utf-8")
    tracker_path.write_text(
        tracker_text.replace(
            "`tasks/TASK-001-Missing-Docs/IMPLEMENTATION.md`",
            "`tasks/TASK-001-Missing-Docs/NOPE.md`",
        ),
        encoding="utf-8",
    )

    missing_docs = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Analysing"],
        cwd=tmp_path,
    )
    assert missing_docs.returncode != 0
    assert "docs path does not exist" in missing_docs.stderr


def test_fix_lifecycle_uses_shared_tracker_and_single_document(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr

    created = run_project(
        ["fix", "init", "--title", "Export Regression", "--classification", "Regression"],
        cwd=tmp_path,
    )
    assert created.returncode == 0, created.stdout + created.stderr
    assert "Assigned ID: FIX-001" in created.stdout
    fix_dir = tmp_path / ".project-workflow" / "tasks" / "FIX-001-Export-Regression"
    fix_path = fix_dir / "FIX.md"
    assert fix_path.exists()
    assert sorted(path.name for path in fix_dir.iterdir()) == ["FIX.md"]
    assert not (tmp_path / ".project-workflow" / "fixes").exists()
    assert not (tmp_path / ".project-workflow" / "FIXES.md").exists()
    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(
        encoding="utf-8"
    )
    assert "| FIX-001 | Export Regression | To Do |" in tracker_text

    invalid_text = workflow_cli._replace_fix_field(
        fix_path.read_text(encoding="utf-8"), "Classification", "Type", "Bug"
    )
    fix_path.write_text(invalid_text, encoding="utf-8")
    invalid_doctor = run_project(["doctor"], cwd=tmp_path)
    assert invalid_doctor.returncode != 0
    assert "invalid classification Type 'Bug'" in invalid_doctor.stdout
    fix_path.write_text(
        workflow_cli._replace_fix_field(invalid_text, "Classification", "Type", "Regression"),
        encoding="utf-8",
    )

    blocked_triage = run_project(["fix", "triage", "--id", "FIX-001"], cwd=tmp_path)
    assert blocked_triage.returncode != 0
    assert "complete `observed or requested`" in blocked_triage.stderr

    fix_path.write_text(ready_fix_text(fix_path), encoding="utf-8")
    triaged = run_project(["fix", "triage", "--id", "FIX-001"], cwd=tmp_path)
    assert triaged.returncode == 0, triaged.stdout + triaged.stderr
    assert "To Do -> Ready" in triaged.stdout

    for status in ("In Progress", "Testing", "Review"):
        moved = run_project(
            ["fix", "status", "--id", "FIX-001", "--to", status], cwd=tmp_path
        )
        assert moved.returncode == 0, moved.stdout + moved.stderr

    direct_complete = run_project(
        ["fix", "status", "--id", "FIX-001", "--to", "Complete"], cwd=tmp_path
    )
    assert direct_complete.returncode != 0
    assert "Use `project fix close`" in direct_complete.stderr

    fix_path.write_text(verified_fix_text(fix_path), encoding="utf-8")
    closed = run_project(
        [
            "fix",
            "close",
            "--id",
            "FIX-001",
            "--disposition",
            "Fixed",
            "--decision",
            "Regression correction verified.",
            "--closed-by",
            "Test Owner",
        ],
        cwd=tmp_path,
    )
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "Closed FIX-001 with disposition Fixed" in closed.stdout
    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "no issues found" in doctor.stdout


def test_fix_init_preserves_supported_classification_taxonomy(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    for index, classification in enumerate(workflow_cli.FIX_CLASSIFICATIONS, start=1):
        created = run_project(
            [
                "fix",
                "init",
                "--title",
                f"{classification} Example",
                "--classification",
                classification,
            ],
            cwd=tmp_path,
        )
        assert created.returncode == 0, created.stdout + created.stderr
        fix_path = next(
            (tmp_path / ".project-workflow" / "tasks").glob(f"FIX-{index:03d}-*")
        ) / "FIX.md"
        assert f"- Type: {classification}" in fix_path.read_text(encoding="utf-8")
        assert "- Mode: Normal" in fix_path.read_text(encoding="utf-8")


def test_fix_link_does_not_mutate_completed_task_history(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    task = run_project(
        ["task", "init", "--title", "Delivered Export", "--update-tracker"], cwd=tmp_path
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = tmp_path / ".project-workflow" / "tasks" / "TASK-001-Delivered-Export"
    requirements_path = task_dir / "REQUIREMENTS.md"
    implementation_path = task_dir / "IMPLEMENTATION.md"
    requirements_path.write_text(
        ready_requirements("TASK-001", "Delivered Export"), encoding="utf-8"
    )
    implementation_path.write_text(ready_implementation(qa=True), encoding="utf-8")
    for status in ("Analysing", "Ready", "In Progress", "Testing", "Review", "Complete"):
        moved = run_project(
            ["task", "status", "--id", "TASK-001", "--to", status], cwd=tmp_path
        )
        assert moved.returncode == 0, moved.stdout + moved.stderr
    requirements_before = requirements_path.read_bytes()
    implementation_before = implementation_path.read_bytes()
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    source_row_before = next(
        line
        for line in tracker_path.read_text(encoding="utf-8").splitlines()
        if line.startswith("| TASK-001 |")
    )

    created = run_project(["fix", "init", "--title", "Delivered Export Regression"], cwd=tmp_path)
    assert created.returncode == 0, created.stdout + created.stderr
    fix_path = (
        tmp_path
        / ".project-workflow"
        / "tasks"
        / "FIX-001-Delivered-Export-Regression"
        / "FIX.md"
    )
    fix_text = ready_fix_text(fix_path)
    fix_text = workflow_cli._replace_fix_field(
        fix_text, "Related Work", "Originating work", "TASK-001"
    )
    fix_path.write_text(fix_text, encoding="utf-8")
    triaged = run_project(["fix", "triage", "--id", "FIX-001"], cwd=tmp_path)
    assert triaged.returncode == 0, triaged.stdout + triaged.stderr
    for status in ("In Progress", "Testing", "Review"):
        assert (
            run_project(
                ["fix", "status", "--id", "FIX-001", "--to", status], cwd=tmp_path
            ).returncode
            == 0
        )
    verified_text = verified_fix_text(fix_path)
    verified_text = workflow_cli._replace_fix_field(
        verified_text,
        "Verification",
        "Original acceptance criteria result",
        "TASK-001 AC1 passed its targeted regression check.",
    )
    fix_path.write_text(verified_text, encoding="utf-8")
    closed = run_project(
        [
            "fix",
            "close",
            "--id",
            "FIX-001",
            "--disposition",
            "Fixed",
            "--decision",
            "Linked regression verified.",
            "--closed-by",
            "Test Owner",
        ],
        cwd=tmp_path,
    )
    assert closed.returncode == 0, closed.stdout + closed.stderr

    assert requirements_path.read_bytes() == requirements_before
    assert implementation_path.read_bytes() == implementation_before
    source_row_after = next(
        line
        for line in tracker_path.read_text(encoding="utf-8").splitlines()
        if line.startswith("| TASK-001 |")
    )
    assert source_row_after == source_row_before


def test_fix_related_work_ignores_external_urls_and_checks_configured_ids(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    write_unique_id_config(tmp_path)

    task = run_project(
        ["task", "init", "--title", "Delivered Baseline", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_match = re.search(r"Assigned ID: (WF-[0-9A-Z]{5})", task.stdout)
    assert task_match, task.stdout
    task_id = task_match.group(1)

    created = run_project(["fix", "init", "--title", "Related Link Parsing"], cwd=tmp_path)
    assert created.returncode == 0, created.stdout + created.stderr
    fix_match = re.search(r"Assigned ID: (FIX-[0-9A-Z]{5})", created.stdout)
    assert fix_match, created.stdout
    fix_id = fix_match.group(1)
    fix_path = next(
        (tmp_path / ".project-workflow" / "tasks").glob(f"{fix_id}-Related-Link-Parsing")
    ) / "FIX.md"

    missing_id = next(
        candidate for candidate in ("WF-ZZZZZ", "WF-YYYYY") if candidate != task_id
    )
    fix_text = workflow_cli._replace_fix_field(
        fix_path.read_text(encoding="utf-8"),
        "Related Work",
        "Originating work",
        task_id,
    )
    fix_text = workflow_cli._replace_fix_field(
        fix_text,
        "Related Work",
        "External links",
        f"https://github.com/example/project-workflow/issues/{missing_id}",
    )
    fix_path.write_text(fix_text, encoding="utf-8")

    valid = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert valid.returncode == 0, valid.stdout + valid.stderr
    assert "PROJECT-WORKFLOW" not in valid.stdout
    assert missing_id not in valid.stdout

    fix_path.write_text(
        workflow_cli._replace_fix_field(
            fix_text,
            "Related Work",
            "Originating work",
            missing_id,
        ),
        encoding="utf-8",
    )
    missing = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert missing.returncode != 0
    assert f"related work reference '{missing_id}' is not in the local global tracker" in missing.stdout
    assert "PROJECT-WORKFLOW" not in missing.stdout


def test_fix_hotfix_bypass_and_promotion(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr

    created = run_project(
        ["fix", "init", "--title", "Production Incident", "--mode", "Hotfix"],
        cwd=tmp_path,
    )
    assert created.returncode == 0, created.stdout + created.stderr
    fix_path = (
        tmp_path
        / ".project-workflow"
        / "tasks"
        / "FIX-001-Production-Incident"
        / "FIX.md"
    )
    bypass_blocked = run_project(
        ["fix", "status", "--id", "FIX-001", "--to", "In Progress"], cwd=tmp_path
    )
    assert bypass_blocked.returncode != 0
    fix_path.write_text(ready_fix_text(fix_path, hotfix=True), encoding="utf-8")
    bypass = run_project(
        ["fix", "status", "--id", "FIX-001", "--to", "In Progress"], cwd=tmp_path
    )
    assert bypass.returncode == 0, bypass.stdout + bypass.stderr

    second = run_project(["fix", "init", "--title", "Expanded Outcome"], cwd=tmp_path)
    assert second.returncode == 0, second.stdout + second.stderr
    promoted = run_project(
        [
            "fix",
            "promote",
            "--id",
            "FIX-002",
            "--to",
            "task",
            "--reason",
            "The request now needs a new product outcome.",
            "--promoted-by",
            "Test Owner",
        ],
        cwd=tmp_path,
    )
    assert promoted.returncode == 0, promoted.stdout + promoted.stderr
    assert "Promoted FIX-002 to task TASK-001" in promoted.stdout
    promoted_requirements = (
        tmp_path
        / ".project-workflow"
        / "tasks"
        / "TASK-001-Expanded-Outcome"
        / "REQUIREMENTS.md"
    ).read_text(encoding="utf-8")
    assert "- Promoted from Fix: FIX-002" in promoted_requirements
    promoted_fix = (
        tmp_path
        / ".project-workflow"
        / "tasks"
        / "FIX-002-Expanded-Outcome"
        / "FIX.md"
    ).read_text(encoding="utf-8")
    assert "- Status: N/A" in promoted_fix
    assert "- Disposition: Promoted" in promoted_fix
    assert "- Promoted to: TASK-001" in promoted_fix

    third = run_project(["fix", "init", "--title", "Coordinated Outcomes"], cwd=tmp_path)
    assert third.returncode == 0, third.stdout + third.stderr
    promoted_epic = run_project(
        [
            "fix",
            "promote",
            "--id",
            "FIX-003",
            "--to",
            "epic",
            "--reason",
            "Several coordinated outcomes are now required.",
            "--promoted-by",
            "Test Owner",
        ],
        cwd=tmp_path,
    )
    assert promoted_epic.returncode == 0, promoted_epic.stdout + promoted_epic.stderr
    assert "Promoted FIX-003 to epic EPIC-001" in promoted_epic.stdout
    epic_requirements = (
        tmp_path
        / ".project-workflow"
        / "tasks"
        / "EPIC-001-Coordinated-Outcomes"
        / "REQUIREMENTS.md"
    ).read_text(encoding="utf-8")
    assert "- Promoted from Fix: FIX-003" in epic_requirements


def test_fix_workspace_metadata_and_non_delivery_disposition(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    workspace_path = tmp_path / ".project-workflow" / "workspace.json"
    workspace_path.write_text(
        json.dumps(
            {
                "components": [
                    {"id": "api", "path": "services/api"},
                    {"id": "web", "path": "apps/web"},
                ]
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    created = run_project(["fix", "init", "--title", "Workspace Regression"], cwd=tmp_path)
    assert created.returncode == 0, created.stdout + created.stderr
    fix_path = (
        tmp_path
        / ".project-workflow"
        / "tasks"
        / "FIX-001-Workspace-Regression"
        / "FIX.md"
    )
    text = ready_fix_text(fix_path)
    text = workflow_cli._replace_fix_field(text, "Fix Plan", "Primary repo", "api")
    text = workflow_cli._replace_fix_field(text, "Fix Plan", "Repos touched", "api, web")
    fix_path.write_text(text, encoding="utf-8")
    missing_rows = run_project(["fix", "triage", "--id", "FIX-001"], cwd=tmp_path)
    assert missing_rows.returncode != 0
    assert "repository-links row for workspace repo `api`" in missing_rows.stderr

    text = text.replace(
        "| . | ____ | ____ | ____ |",
        "| api | fix/api | PR-101 | evidence/api.txt |\n"
        "| web | fix/web | None | evidence/web.txt |",
    )
    fix_path.write_text(text, encoding="utf-8")
    triaged = run_project(["fix", "triage", "--id", "FIX-001"], cwd=tmp_path)
    assert triaged.returncode == 0, triaged.stdout + triaged.stderr

    for index, disposition in enumerate(("Duplicate", "Rejected", "Deferred"), start=2):
        title = f"{disposition} Report"
        created_terminal = run_project(["fix", "init", "--title", title], cwd=tmp_path)
        assert created_terminal.returncode == 0, created_terminal.stdout + created_terminal.stderr
        closed = run_project(
            [
                "fix",
                "close",
                "--id",
                f"FIX-{index:03d}",
                "--disposition",
                disposition,
                "--decision",
                f"Triage disposition: {disposition}.",
                "--closed-by",
                "Triage Owner",
            ],
            cwd=tmp_path,
        )
        assert closed.returncode == 0, closed.stdout + closed.stderr
        terminal_text = next(
            (tmp_path / ".project-workflow" / "tasks").glob(f"FIX-{index:03d}-*")
        ).joinpath("FIX.md").read_text(encoding="utf-8")
        assert "- Status: N/A" in terminal_text
        assert f"- Disposition: {disposition}" in terminal_text


def test_agent_mode_init_installs_doctor_guidance(tmp_path: Path) -> None:
    codex_root = tmp_path / "codex"
    codex_root.mkdir()
    (codex_root / "AGENTS.md").write_text(
        "# Existing Agent Notes\n\nKeep this.\n", encoding="utf-8"
    )
    codex_init = run_project(["init", "--agent", "codex"], cwd=codex_root)
    assert codex_init.returncode == 0, codex_init.stderr
    codex_agents = (codex_root / "AGENTS.md").read_text(encoding="utf-8")
    assert "# Existing Agent Notes" in codex_agents
    assert "<!-- project-workflow:start -->" in codex_agents
    assert (
        "uvx --from git+https://github.com/johndetlefs/project-workflow.git project init"
        in codex_agents
    )
    assert "To initialize a new repository" in codex_agents
    assert "project upgrade" in codex_agents
    assert "Do not run init first" in codex_agents
    assert "workflow doctor" in codex_agents
    assert ".project-workflow/BACKLOG.md" in codex_agents
    assert "Promoted rows stay in the backlog" in codex_agents
    assert "task status" in codex_agents
    assert "task approve-requirements" in codex_agents
    assert "epic approve-requirements" in codex_agents
    assert "EPIC-CONTRACT.md" in codex_agents
    assert "DECOMPOSITION.md" in codex_agents
    assert "EVIDENCE.json" in codex_agents
    assert "invalid substitutes" in codex_agents
    assert "bounded post-completion correction" in codex_agents
    assert "move new tasks to `Ready`" in codex_agents
    fix_skill_path = codex_root / ".agents" / "skills" / "project-fix" / "SKILL.md"
    assert fix_skill_path.exists()
    assert ".project-workflow/TRACKER.md" in fix_skill_path.read_text(encoding="utf-8")
    assert "workflow doctor" in (
        codex_root / ".agents" / "skills" / "project-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    implement_skill = (
        codex_root / ".agents" / "skills" / "project-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "task status" in implement_skill
    assert "task ready" in implement_skill
    assert "task approve-requirements" in implement_skill
    assert "approved envelope" in implement_skill
    qa_skill = (
        codex_root / ".agents" / "skills" / "project-qa-review" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Do not ask the user to manually test behavior" in qa_skill
    assert "separate verified evidence from deferred setup" in qa_skill
    assert "EVIDENCE.json" in qa_skill
    assert "visual/reference fidelity" in qa_skill
    assert ".project-workflow/guidance.md" in (
        codex_root / ".agents" / "skills" / "project-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    backlog_skill = (
        codex_root / ".agents" / "skills" / "project-backlog" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Promoted rows stay in the backlog" in backlog_skill
    assert "Existing roadmap/backlog documents" in backlog_skill

    cursor_root = tmp_path / "cursor"
    cursor_root.mkdir()
    cursor_init = run_project(["init", "--agent", "cursor"], cwd=cursor_root)
    assert cursor_init.returncode == 0, cursor_init.stderr
    cursor_rules = (
        cursor_root / ".cursor" / "rules" / "project-workflow.mdc"
    ).read_text(encoding="utf-8")
    assert "workflow doctor" in cursor_rules
    assert "task status" in cursor_rules
    assert "owner-directed and agent-operated" in cursor_rules
    assert "task ready" in cursor_rules
    assert ".project-workflow/BACKLOG.md" in cursor_rules
    assert "Existing roadmap/backlog documents" in cursor_rules
    assert "task approve-requirements" in cursor_rules
    assert "epic approve-requirements" in cursor_rules
    assert "EPIC-CONTRACT.md" in cursor_rules
    assert "DECOMPOSITION.md" in cursor_rules
    assert "EVIDENCE.json" in cursor_rules
    assert "one lightweight Fix" in cursor_rules
    assert (cursor_root / ".cursor" / "agents" / "project-fix.md").exists()
    assert (
        cursor_root / ".cursor" / "agents" / "project-backlog.md"
    ).exists()
    assert "workflow doctor" in (
        cursor_root / ".cursor" / "agents" / "project-implement.md"
    ).read_text(encoding="utf-8")

    claude_root = tmp_path / "claude"
    claude_root.mkdir()
    claude_init = run_project(["init", "--agent", "claude-code"], cwd=claude_root)
    assert claude_init.returncode == 0, claude_init.stderr
    assert (
        claude_root / ".claude" / "agents" / "project-backlog.md"
    ).exists()
    assert (claude_root / ".claude" / "agents" / "project-fix.md").exists()
    claude_implement = (
        claude_root / ".claude" / "agents" / "project-implement.md"
    ).read_text(encoding="utf-8")
    assert "task approve-requirements" in claude_implement
    assert "approved envelope" in claude_implement
    assert "EVIDENCE.json" in claude_implement


def test_upgrade_refreshes_marked_generated_files_and_managed_blocks(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    init_git_fixture(tmp_path)

    local_workflow = tmp_path / ".project-workflow" / "cli" / "workflow.py"
    local_workflow.write_text(
        "# project-workflow:generated\n# old generated workflow helper\n",
        encoding="utf-8",
    )
    instructions = tmp_path / ".github" / "copilot-instructions.md"
    instructions.write_text(
        "# Local Copilot Notes\n\n"
        "<!-- project-workflow:start -->\n"
        "old managed block\n"
        "<!-- project-workflow:end -->\n",
        encoding="utf-8",
    )
    commit_git_fixture(tmp_path, "legacy generated assets")

    refreshed = run_project(
        ["upgrade", "--agent", "github-copilot", "--yes"], cwd=tmp_path
    )
    assert refreshed.returncode == 0, refreshed.stdout + refreshed.stderr

    help_result = subprocess.run(
        [sys.executable, str(local_workflow), "doctor", "--help"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert help_result.returncode == 0, help_result.stdout + help_result.stderr
    assert "Validate workflow tracker state" in help_result.stdout
    status_help = subprocess.run(
        [sys.executable, str(local_workflow), "task", "status", "--help"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert status_help.returncode == 0, status_help.stdout + status_help.stderr
    assert "Safely update one global tracker task status" in status_help.stdout
    instructions_text = instructions.read_text(encoding="utf-8")
    assert "# Local Copilot Notes" in instructions_text
    assert "old managed block" not in instructions_text
    assert ".project-workflow/guidance.md" in instructions_text
    assert "task status" in instructions_text
    assert "task approve-requirements" in instructions_text
    assert "epic approve-requirements" in instructions_text
    assert "EPIC-CONTRACT.md" in instructions_text
    assert "DECOMPOSITION.md" in instructions_text
    assert "EVIDENCE.json" in instructions_text
    assert "invalid substitutes" in instructions_text
    fix_help = subprocess.run(
        [sys.executable, str(local_workflow), "fix", "--help"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert fix_help.returncode == 0, fix_help.stdout + fix_help.stderr
    assert "Manage bounded defects" in fix_help.stdout


def test_uvx_fresh_init_and_upgrade_deliver_fix_assets(tmp_path: Path) -> None:
    uvx = find_uvx_executable()
    if uvx is None:
        pytest.skip("uvx was not found on PATH or in standard installation locations")
    package_source = tmp_path / "package-source"
    shutil.copytree(
        REPO_ROOT,
        package_source,
        ignore=shutil.ignore_patterns(
            ".git",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            ".venv",
            "__pycache__",
            "*.pyc",
        ),
    )
    target = tmp_path / "uvx-target"
    target.mkdir()
    init_command = [
        uvx,
        "--from",
        str(package_source),
        "project",
        "init",
        "--agent",
        "codex",
    ]
    upgrade_command = [
        uvx,
        "--from",
        str(package_source),
        "project",
        "upgrade",
        "--agent",
        "codex",
        "--yes",
    ]
    uv_env = os.environ.copy()
    uv_env["UV_CACHE_DIR"] = str(tmp_path / "uv-cache")
    uv_env["UV_TOOL_DIR"] = str(tmp_path / "uv-tools")

    fresh = subprocess.run(
        init_command,
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
        env=uv_env,
    )
    assert fresh.returncode == 0, fresh.stdout + fresh.stderr
    init_git_fixture(target)
    local_workflow = target / ".project-workflow" / "cli" / "workflow.py"
    fix_skill = target / ".agents" / "skills" / "project-fix" / "SKILL.md"
    assert fix_skill.exists()
    fix_help = subprocess.run(
        [sys.executable, str(local_workflow), "fix", "--help"],
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
        env=uv_env,
    )
    assert fix_help.returncode == 0, fix_help.stdout + fix_help.stderr

    local_workflow.write_text(
        "# project-workflow:generated\n# legacy workflow helper\n", encoding="utf-8"
    )
    agents_path = target / "AGENTS.md"
    agents_path.write_text(
        "# User Notes\n\n"
        "<!-- project-workflow:start -->\nlegacy managed block\n"
        "<!-- project-workflow:end -->\n",
        encoding="utf-8",
    )
    fix_skill.write_text("# User-owned Fix guidance\n", encoding="utf-8")
    commit_git_fixture(target, "legacy generated assets")

    refreshed = subprocess.run(
        upgrade_command,
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
        env=uv_env,
    )
    assert refreshed.returncode == 0, refreshed.stdout + refreshed.stderr
    refreshed_help = subprocess.run(
        [sys.executable, str(local_workflow), "fix", "--help"],
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
    )
    assert refreshed_help.returncode == 0, refreshed_help.stdout + refreshed_help.stderr
    assert fix_skill.read_text(encoding="utf-8") == "# User-owned Fix guidance\n"
    fix_skill_new = fix_skill.with_name("SKILL.md.new")
    assert fix_skill_new.exists()
    assert "Project Fix" in fix_skill_new.read_text(encoding="utf-8")
    agents_text = agents_path.read_text(encoding="utf-8")
    assert "# User Notes" in agents_text
    assert "legacy managed block" not in agents_text
    assert "bounded post-completion correction" in agents_text

    workflow_after_refresh = local_workflow.read_text(encoding="utf-8")
    skill_new_after_refresh = fix_skill_new.read_text(encoding="utf-8")
    commit_git_fixture(target, "upgrade generated assets")
    repeated = subprocess.run(
        upgrade_command,
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
        env=uv_env,
    )
    assert repeated.returncode == 0, repeated.stdout + repeated.stderr
    assert local_workflow.read_text(encoding="utf-8") == workflow_after_refresh
    assert fix_skill.read_text(encoding="utf-8") == "# User-owned Fix guidance\n"
    assert fix_skill_new.read_text(encoding="utf-8") == skill_new_after_refresh
    assert not fix_skill.with_name("SKILL.md.new.2").exists()


def test_init_does_not_treat_inline_marker_mentions_as_managed_blocks(tmp_path: Path) -> None:
    instructions = tmp_path / ".github" / "copilot-instructions.md"
    instructions.parent.mkdir(parents=True)
    instructions.write_text(
        "# Local Copilot Notes\n\n"
        "Document the `<!-- project-workflow:start -->` / "
        "`<!-- project-workflow:end -->` markers, but do not treat this sentence as a block.\n",
        encoding="utf-8",
    )

    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr

    instructions_text = instructions.read_text(encoding="utf-8")
    assert (
        "Document the `<!-- project-workflow:start -->` / "
        "`<!-- project-workflow:end -->` markers"
    ) in instructions_text
    assert instructions_text.count("<!-- project-workflow:start -->") == 2
    assert instructions_text.count("<!-- project-workflow:end -->") == 2
    assert "\n<!-- project-workflow:start -->\n## Project Workflow" in instructions_text


def test_init_preserves_unmarked_generated_collision_and_writes_new(tmp_path: Path) -> None:
    prompt_path = tmp_path / ".github" / "prompts" / "Task.prompt.md"
    prompt_path.parent.mkdir(parents=True)
    prompt_path.write_text("# Custom task prompt\n", encoding="utf-8")

    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    assert prompt_path.read_text(encoding="utf-8") == "# Custom task prompt\n"

    new_path = tmp_path / ".github" / "prompts" / "Task.prompt.md.new"
    assert new_path.exists()
    assert "project-workflow:generated" in new_path.read_text(encoding="utf-8")

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0
    assert "Generated project-workflow update is pending" in doctor.stdout


def test_init_removes_retired_scaffold_assets(tmp_path: Path) -> None:
    legacy_path = tmp_path / ".github" / "prompts" / "Scaffold.prompt.md"
    legacy_path.parent.mkdir(parents=True)
    legacy_path.write_text("# Custom legacy scaffold prompt\n", encoding="utf-8")

    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    assert not legacy_path.exists()
    assert (tmp_path / ".github" / "prompts" / "Task.prompt.md").exists()

    codex_root = tmp_path / "codex"
    scaffold_skill = codex_root / ".agents" / "skills" / "project-scaffold" / "SKILL.md"
    scaffold_skill.parent.mkdir(parents=True)
    scaffold_skill.write_text("# Retired scaffold skill\n", encoding="utf-8")

    codex_init = run_project(["init", "--agent", "codex"], cwd=codex_root)
    assert codex_init.returncode == 0, codex_init.stdout + codex_init.stderr
    assert not scaffold_skill.parent.exists()
    assert (codex_root / ".agents" / "skills" / "project-task" / "SKILL.md").exists()


def test_doctor_detects_source_prompt_mirror_drift(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    source_root = tmp_path / "src" / "project_workflow"
    shutil.copytree(REPO_ROOT / "src" / "project_workflow" / "prompts", source_root / "prompts")
    shutil.copytree(
        REPO_ROOT / "src" / "project_workflow" / "templates",
        source_root / "templates",
    )

    prompt_path = tmp_path / ".github" / "prompts" / "Task.prompt.md"
    prompt_path.write_text(prompt_path.read_text(encoding="utf-8") + "\nDrift.\n", encoding="utf-8")

    doctor = run_project(["doctor"], cwd=tmp_path)

    assert doctor.returncode != 0
    assert "Prompt differs from packaged mirror" in doctor.stdout


def test_doctor_strict_fails_complete_task_without_qa_evidence(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Missing QA Evidence", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr

    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_text = tracker_path.read_text(encoding="utf-8")
    tracker_path.write_text(tracker_text.replace(" | To Do | ", " | Complete | "), encoding="utf-8")

    default_doctor = run_project(["doctor"], cwd=tmp_path)
    assert default_doctor.returncode == 0, default_doctor.stdout + default_doctor.stderr
    assert "WARNING" in default_doctor.stdout

    strict_doctor = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert strict_doctor.returncode != 0
    assert "ERROR" in strict_doctor.stdout
    assert "lacks non-placeholder QA/code-review evidence" in strict_doctor.stdout


def test_doctor_hides_accepted_warning_fingerprints_and_shows_on_request(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Accepted Warning", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-001", "Accepted Warning"),
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")

    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(" | To Do | ", " | Complete | "),
        encoding="utf-8",
    )

    issues = workflow_cli.run_doctor(tmp_path)
    target = next(issue for issue in issues if "lacks non-placeholder QA" in issue.message)
    fingerprint = workflow_cli._doctor_issue_fingerprint(target, tmp_path)
    add_accepted_doctor_warnings(
        tmp_path,
        [{"fingerprint": fingerprint, "reason": "Known historical fixture."}],
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "no issues found" in doctor.stdout
    assert "1 accepted warning(s) hidden" in doctor.stdout
    assert "lacks non-placeholder QA" not in doctor.stdout

    strict_doctor = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert strict_doctor.returncode == 0, strict_doctor.stdout + strict_doctor.stderr
    assert "1 accepted warning(s) hidden" in strict_doctor.stdout

    audit = run_project(["doctor", "--show-accepted"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "ACCEPTED:" in audit.stdout
    assert fingerprint in audit.stdout
    assert "Known historical fixture." in audit.stdout
    assert "lacks non-placeholder QA" in audit.stdout


def test_doctor_string_accepted_fingerprint_does_not_hide_different_warning(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    first = run_project(
        ["task", "init", "--title", "First Accepted Warning", "--update-tracker"],
        cwd=tmp_path,
    )
    assert first.returncode == 0, first.stdout + first.stderr
    second = run_project(
        ["task", "init", "--title", "Second Visible Warning", "--update-tracker"],
        cwd=tmp_path,
    )
    assert second.returncode == 0, second.stdout + second.stderr
    first_dir = next(
        (tmp_path / ".project-workflow" / "tasks").glob("TASK-001-First-Accepted-Warning")
    )
    second_dir = next(
        (tmp_path / ".project-workflow" / "tasks").glob("TASK-002-Second-Visible-Warning")
    )
    (first_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-001", "First Accepted Warning"),
        encoding="utf-8",
    )
    (first_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")
    (second_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-002", "Second Visible Warning"),
        encoding="utf-8",
    )
    (second_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")

    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(" | To Do | ", " | Complete | "),
        encoding="utf-8",
    )

    issues = workflow_cli.run_doctor(tmp_path)
    accepted_issue = next(issue for issue in issues if "First-Accepted-Warning" in issue.path)
    visible_issue = next(issue for issue in issues if "Second-Visible-Warning" in issue.path)
    accepted_fingerprint = workflow_cli._doctor_issue_fingerprint(accepted_issue, tmp_path)
    visible_fingerprint = workflow_cli._doctor_issue_fingerprint(visible_issue, tmp_path)
    add_accepted_doctor_warnings(tmp_path, [accepted_fingerprint])

    doctor = run_project(["doctor"], cwd=tmp_path)

    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "1 accepted warning(s) hidden" in doctor.stdout
    assert accepted_fingerprint not in doctor.stdout
    assert visible_fingerprint in doctor.stdout
    assert "Second-Visible-Warning" in doctor.stdout
    assert "First-Accepted-Warning" not in doctor.stdout


def test_doctor_separates_legacy_warnings_from_current_warnings(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    current = run_project(
        ["task", "init", "--title", "Current Missing QA", "--update-tracker"],
        cwd=tmp_path,
    )
    assert current.returncode == 0, current.stdout + current.stderr
    current_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    current_impl = current_dir / "IMPLEMENTATION.md"

    legacy_dir = tmp_path / ".project-workflow" / "tasks" / "APP-001-Legacy"
    legacy_dir.mkdir()
    legacy_impl = legacy_dir / "IMPLEMENTATION.md"
    legacy_impl.write_text(
        "## User Story\n\n"
        "As a maintainer, I have historical workflow state.\n\n",
        encoding="utf-8",
    )

    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_text = tracker_path.read_text(encoding="utf-8")
    tracker_text = tracker_text.replace(" | To Do | ", " | Complete | ")
    tracker_text += "| APP-001 | Legacy | Complete | `tasks/APP-001-Legacy/IMPLEMENTATION.md` |\n"
    tracker_path.write_text(tracker_text, encoding="utf-8")

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert f"WARNING: {current_impl}" in doctor.stdout
    assert f"LEGACY WARNING: {legacy_impl}" in doctor.stdout
    assert "LEGACY WARNING" in doctor.stdout
    assert "APP-001 uses unconfigured task ID prefix 'APP'" in doctor.stdout
    assert "project doctor: 2 legacy warning(s) shown separately." in doctor.stdout

    strict_doctor = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert strict_doctor.returncode != 0
    assert f"ERROR: {current_impl}" in strict_doctor.stdout
    assert f"ERROR: {legacy_impl}" in strict_doctor.stdout


def test_doctor_warns_for_unconfigured_task_prefixes(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    task_dir = tmp_path / ".project-workflow" / "tasks" / "WF-003-Workflow-Task"
    task_dir.mkdir()
    (task_dir / "IMPLEMENTATION.md").write_text(
        "## User Story\n\nAs a maintainer, I have namespace state.\n",
        encoding="utf-8",
    )
    tracker_text = tracker_path.read_text(encoding="utf-8")
    tracker_text += "| WF-003 | Workflow Task | To Do | `tasks/WF-003-Workflow-Task/IMPLEMENTATION.md` |\n"
    tracker_path.write_text(tracker_text, encoding="utf-8")

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "WF-003 uses unconfigured task ID prefix 'WF'" in doctor.stdout

    strict_doctor = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert strict_doctor.returncode != 0
    assert "ERROR" in strict_doctor.stdout
    assert "WF-003 uses unconfigured task ID prefix 'WF'" in strict_doctor.stdout


def test_doctor_detects_duplicate_configured_unique_tracker_ids(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    write_unique_id_config(tmp_path)

    tasks_dir = tmp_path / ".project-workflow" / "tasks"
    first_dir = tasks_dir / "WF-ABCDE-First"
    second_dir = tasks_dir / "WF-ABCDE-Second"
    first_dir.mkdir()
    second_dir.mkdir()
    (first_dir / "IMPLEMENTATION.md").write_text("## User Story\n\nFirst.\n", encoding="utf-8")
    (second_dir / "IMPLEMENTATION.md").write_text("## User Story\n\nSecond.\n", encoding="utf-8")
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8")
        + "| WF-ABCDE | First | To Do | `tasks/WF-ABCDE-First/IMPLEMENTATION.md` |\n"
        + "| WF-ABCDE | Second | To Do | `tasks/WF-ABCDE-Second/IMPLEMENTATION.md` |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)

    assert doctor.returncode == 1, doctor.stdout + doctor.stderr
    assert "Duplicate workflow ID 'WF-ABCDE'" in doctor.stdout


def test_doctor_warns_when_active_task_row_lacks_ac_mapping(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "AC Mapping Warning", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr

    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: TASK-001\n"
        "- Title: AC Mapping Warning\n\n"
        "## Requirements (Outcome-Focused)\n\n"
        "- Export behavior is controlled by the workflow.\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: Export succeeds for an authorized user.\n"
        "- AC2: Export fails with a clear error for an unauthorized user.\n",
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(
        "## User Story\n\n"
        "As a maintainer, I want mapped task rows, so QA can trace work.\n\n"
        "## Acceptance Criteria\n\n"
        "- [ ] AC1: Export succeeds for an authorized user.\n"
        "- [ ] AC2: Export fails with a clear error for an unauthorized user.\n\n"
        "## Validation\n\n"
        "- AC1: Run export success test.\n"
        "- AC2: Run export authorization failure test.\n\n"
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "| --: | ----- | ----------- | ------------------- | ----------------- | ------ |\n"
        "| 1 | Success path | Export works for authorized users. | Export succeeds. | Run success test. | To Do |\n"
        "| 2 | Failure path | Export rejects unauthorized users. | AC2: Clear failure. | Run failure test. | To Do |\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pending.\n"
        "- Evidence: Pending.\n"
        "- Findings: Pending.\n",
        encoding="utf-8",
    )

    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(" | To Do | ", " | In Progress | "),
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "implementation task row(s) lack AC ID mapping: 1" in doctor.stdout
    assert "acceptance criteria are not mapped to implementation tasks: AC1" in doctor.stdout

    strict_doctor = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert strict_doctor.returncode != 0
    assert "ERROR" in strict_doctor.stdout


def test_epic_decompose_preserves_source_ac_ids_in_notes(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Mapped Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    initialized_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |" in initialized_tracker
    assert (epic_dir / "EPIC-CONTRACT.md").exists()
    initialized_map = (epic_dir / "ACCEPTANCE-MAP.md").read_text(encoding="utf-8")
    assert "| AC1 | ____ | None | None | None | Unmapped |" in initialized_map
    initialized_retro = (epic_dir / "RETRO.md").read_text(encoding="utf-8")
    assert "## Lessons" in initialized_retro
    assert "## Missed In-Scope Work" in initialized_retro

    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Mapped Epic",
            [
                "- AC1: First epic outcome is delivered.",
                "- AC2: Second epic outcome is delivered.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Mapped Epic", ac_ids=["AC1", "AC2"])

    decompose = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-001", "--limit", "2"],
        cwd=tmp_path,
    )
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr
    assert "Parent AC coverage mapped: AC1, AC2" in decompose.stdout

    epic_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-001 | First epic outcome is delivered | Proposed | Task | AC1 |" in epic_tracker
    assert "| TASK-002 | Second epic outcome is delivered | Proposed | Task | AC2 |" in epic_tracker
    assert "Covers AC1; Prefix TASK:" in epic_tracker
    assert "Covers AC2; Prefix TASK:" in epic_tracker
    assert "Generated from REQUIREMENTS.md" in epic_tracker
    decomposition_plan = (epic_dir / "DECOMPOSITION.md").read_text(encoding="utf-8")
    assert "| TASK-001 | First epic outcome is delivered | AC1 | Generated from REQUIREMENTS.md |" in decomposition_plan
    assert "| TASK-002 | Second epic outcome is delivered | AC2 | Generated from REQUIREMENTS.md |" in decomposition_plan
    acceptance_map = (epic_dir / "ACCEPTANCE-MAP.md").read_text(encoding="utf-8")
    assert "| AC1 | First epic outcome is delivered. | TASK-001 (Proposed) | None | None | Mapped - evidence pending |" in acceptance_map
    assert "| AC2 | Second epic outcome is delivered. | TASK-002 (Proposed) | None | None | Mapped - evidence pending |" in acceptance_map


def test_epic_decompose_requires_ready_epic_contract(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Contract Required"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Contract Required",
            ["- AC1: Contract gate blocks decomposition."],
        ),
        encoding="utf-8",
    )

    decompose = run_project(["epic", "decompose", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert decompose.returncode != 0
    assert "EPIC-CONTRACT.md" in decompose.stderr
    assert "placeholder" in decompose.stderr


def test_doctor_fails_approved_epic_missing_contract(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Missing Contract"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Missing Contract",
            ["- AC1: Contract doctor failure is reported."],
        ),
        encoding="utf-8",
    )
    (epic_dir / "EPIC-CONTRACT.md").unlink()

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "epic contract: EPIC-CONTRACT.md is missing" in doctor.stdout


def test_epic_decompose_prefers_owner_proposed_child_work_plan(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Owner Plan"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))

    requirements_text = workflow_cli._remove_markdown_section(
        ready_requirements(
            "EPIC-001",
            "Owner Plan",
            ["- AC1: Owner-planned child work is authorized."],
        ),
        workflow_cli.OWNER_APPROVAL_HEADING,
    )
    requirements_text = (
        requirements_text
        + "\n## Proposed Child Work\n\n"
        "| Proposed Child | Parent ACs | Purpose |\n"
        "| --- | --- | --- |\n"
        "| Owner Named Child | AC1 | Use the owner-reviewed child title. |\n"
    )
    requirements_text = workflow_cli._requirements_with_approval_envelope(
        requirements_text,
        approved_by="Test Owner",
        source="Owner approved fixture requirements with decomposition plan.",
        decomposition=True,
        implementation=False,
    )
    (epic_dir / "REQUIREMENTS.md").write_text(requirements_text, encoding="utf-8")
    write_epic_contract(epic_dir, title="Owner Plan")

    decompose = run_project(["epic", "decompose", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr

    epic_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    decomposition_plan = (epic_dir / "DECOMPOSITION.md").read_text(encoding="utf-8")
    assert "| TASK-001 | Owner Named Child | Proposed | Task | AC1 |" in epic_tracker
    assert "| TASK-001 | Owner Named Child | AC1 | Proposed Child Work |" in decomposition_plan


def test_epic_approve_blocks_child_outside_decomposition_plan(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Manual Drift"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Manual Drift",
            ["- AC1: Planned child work is enforced."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Manual Drift")
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Planned Child", "Parent ACs": "AC1"}],
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-002 | Invented Child | Proposed | Task | AC1 |  |  | Manually invented row |\n",
        encoding="utf-8",
    )

    approve = run_project(
        ["epic", "approve", "--epic-id", "EPIC-001", "--id", "TASK-002"],
        cwd=tmp_path,
    )
    assert approve.returncode != 0
    assert "outside the approved decomposition authority" in approve.stderr
    assert "TASK-002 is outside DECOMPOSITION.md" in approve.stderr


def test_epic_amend_authorizes_child_outside_decomposition_plan(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Approved Amendment"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    assert (epic_dir / workflow_cli.EPIC_AMENDMENTS_FILENAME).exists()
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Approved Amendment",
            ["- AC1: Planned child work is enforced."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Approved Amendment")
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Planned Child", "Parent ACs": "AC1"}],
    )

    amend = run_project(
        [
            "epic",
            "amend",
            "--epic-id",
            "EPIC-001",
            "--id",
            "TASK-002",
            "--title",
            "Reactive Fix",
            "--parent-acs",
            "AC1",
            "--approved-by",
            "Test Owner",
            "--reason",
            "Owner approved reactive fix after drift audit.",
            "--source",
            "Owner approval in test thread.",
        ],
        cwd=tmp_path,
    )
    assert amend.returncode == 0, amend.stdout + amend.stderr
    amendments_text = (epic_dir / workflow_cli.EPIC_AMENDMENTS_FILENAME).read_text(
        encoding="utf-8"
    )
    assert "| TASK-002 | Reactive Fix | AC1 | Test Owner |" in amendments_text
    tracker_text = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-002 | Reactive Fix | Proposed | Task | AC1 |" in tracker_text

    approve = run_project(
        ["epic", "approve", "--epic-id", "EPIC-001", "--id", "TASK-002"],
        cwd=tmp_path,
    )
    assert approve.returncode == 0, approve.stdout + approve.stderr

    scaffold = run_project(
        ["epic", "scaffold-child", "--epic-id", "EPIC-001", "--id", "TASK-002"],
        cwd=tmp_path,
    )
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr


def test_doctor_fails_active_epic_child_without_decomposition_authority(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Manual Active Drift"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Manual Active Drift",
            ["- AC1: Active child rows are plan-authorized."],
        ),
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Manual Active Child | In Progress | Task | AC1 |  |  | Manual row |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "TASK-001 decomposition authority" in doctor.stdout
    assert "DECOMPOSITION.md is missing" in doctor.stdout


def test_epic_decompose_uses_configured_mixed_prefixes_and_prefix_override(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    write_namespace_config(tmp_path)

    epic = run_project(["epic", "init", "--title", "Mixed App Work"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Mixed App Work",
            [
                "- AC1: MCP server payload contract is delivered.",
                "- AC2: Frontend UI route interaction is delivered.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Mixed App Work", ac_ids=["AC1", "AC2"])

    decompose = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-001", "--limit", "2"],
        cwd=tmp_path,
    )
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr

    epic_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| MCP-001 | MCP server payload contract is delivered | Proposed | Task | AC1 |" in epic_tracker
    assert "| UI-001 | Frontend UI route interaction is delivered | Proposed | Task | AC2 |" in epic_tracker
    assert "Prefix MCP: " in epic_tracker
    assert "Prefix UI: " in epic_tracker

    second_epic = run_project(["epic", "init", "--title", "Forced Mcp Work"], cwd=tmp_path)
    assert second_epic.returncode == 0, second_epic.stdout + second_epic.stderr
    second_epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-002-*"))
    (second_epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-002",
            "Forced Mcp Work",
            [
                "- AC1: Frontend UI fixture is delivered.",
                "- AC2: Workflow prompt fixture is delivered.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(
        second_epic_dir,
        epic_id="EPIC-002",
        title="Forced Mcp Work",
        ac_ids=["AC1", "AC2"],
    )

    forced = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-002", "--limit", "2", "--prefix", "MCP"],
        cwd=tmp_path,
    )
    assert forced.returncode == 0, forced.stdout + forced.stderr
    forced_tracker = (second_epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| MCP-002 | Frontend UI fixture is delivered | Proposed | Task | AC1 |" in forced_tracker
    assert "| MCP-003 | Workflow prompt fixture is delivered | Proposed | Task | AC2 |" in forced_tracker
    assert "Prefix MCP: forced by --prefix" in forced_tracker


def test_epic_decompose_reports_unmapped_parent_ac_ids(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Coverage Gap"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Coverage Gap",
            [
                "- AC1: First epic outcome is delivered.",
                "- AC2: Second epic outcome is delivered.",
                "- AC3: Third epic outcome is delivered.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Coverage Gap", ac_ids=["AC1", "AC2", "AC3"])

    decompose = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-001", "--limit", "2"],
        cwd=tmp_path,
    )
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr
    assert "WARNING: Unmapped parent ACs after decomposition: AC3" in decompose.stdout


def test_epic_child_scaffold_carries_parent_ac_sections(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Parent Evidence"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Parent Evidence",
            [
                "- AC1: First parent evidence path is scaffolded.",
                "- AC3: Third parent evidence path is scaffolded.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Parent Evidence", ac_ids=["AC1", "AC3"])
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Child Evidence | Approved | Task | AC1, AC3 |  |  | Covers AC1, AC3 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Child Evidence", "Parent ACs": "AC1, AC3"}],
    )

    scaffold = run_project(
        ["epic", "scaffold-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr

    child_dir = epic_dir / "TASK-001-Child-Evidence"
    requirements_text = (child_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    implementation_text = (child_dir / "IMPLEMENTATION.md").read_text(encoding="utf-8")

    assert "- Parent AC Coverage: AC1, AC3" in requirements_text
    assert "## Parent AC Coverage" in implementation_text
    assert "- AC1, AC3" in implementation_text
    assert "## Child Charter" in requirements_text
    assert "### Invalid Substitutes" in requirements_text
    assert "### Parent AC Proof Ownership" in requirements_text
    assert "## Child Charter" in implementation_text
    assert "## Parent AC Evidence" in implementation_text
    assert "AC1 / parent AC(s) AC1, AC3" in implementation_text
    evidence = json.loads((child_dir / workflow_cli.STRUCTURED_EVIDENCE_FILENAME).read_text(encoding="utf-8"))
    assert [record["parent_ac"] for record in evidence["claims"]] == ["AC1", "AC3"]

    standalone = run_project(
        ["task", "init", "--title", "Standalone Quiet", "--update-tracker"],
        cwd=tmp_path,
    )
    assert standalone.returncode == 0, standalone.stdout + standalone.stderr
    standalone_dir = next(
        p
        for p in (tmp_path / ".project-workflow" / "tasks").glob("TASK-*-Standalone-Quiet")
        if p.is_dir()
    )
    standalone_impl = (standalone_dir / "IMPLEMENTATION.md").read_text(encoding="utf-8")
    assert "## Parent AC Coverage" not in standalone_impl
    assert "## Parent AC Evidence" not in standalone_impl


def test_epic_child_scaffold_preserves_configured_task_prefix(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    write_namespace_config(tmp_path)

    epic = run_project(["epic", "init", "--title", "Custom Prefix Child"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Custom Prefix Child",
            ["- AC1: Custom prefix child is scaffolded."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Custom Prefix Child")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| UI-008 | Widget Interaction | Approved | Task | AC1 |  |  | Prefix UI: owner selected UI child |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "UI-008", "Title": "Widget Interaction", "Parent ACs": "AC1"}],
    )

    scaffold = run_project(
        ["epic", "scaffold-child", "--epic-id", "EPIC-001", "--id", "UI-008"],
        cwd=tmp_path,
    )
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr

    child_dir = epic_dir / "UI-008-Widget-Interaction"
    assert child_dir.exists()
    requirements_text = (child_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    implementation_text = (child_dir / "IMPLEMENTATION.md").read_text(encoding="utf-8")
    tracker_text = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")

    assert "- Task: UI-008" in requirements_text
    assert "- Task: UI-008" in implementation_text
    assert "| UI-008 | Widget Interaction | In Progress | Task | AC1 | tasks/EPIC-001-Custom-Prefix-Child/UI-008-Widget-Interaction/IMPLEMENTATION.md |" in tracker_text


def test_doctor_accepts_legacy_epic_tracker_schema(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Legacy Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Legacy Child | Proposed | Task |  |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "Epic tracker schema mismatch" not in doctor.stdout


def test_epic_audit_and_closeout_complete_only_when_gates_pass(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Closeout Ready"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Closeout Ready",
            ["- AC1: First parent outcome is delivered."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Closeout Ready")
    child_dir = epic_dir / "TASK-001-Ready-Child"
    child_dir.mkdir()
    child_impl = child_dir / "IMPLEMENTATION.md"
    child_impl.write_text(
        "## User Story\n\n"
        "As a maintainer, I want evidence.\n\n"
        "## Parent AC Evidence\n\n"
        "- AC1: Targeted validation passed.\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Targeted validation passed.\n"
        "- Findings: None.\n",
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Ready Child | Complete | Task | AC1 | tasks/EPIC-001-Closeout-Ready/TASK-001-Ready-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Ready Child", "Parent ACs": "AC1"}],
    )
    (epic_dir / "RETRO.md").write_text(
        ready_epic_retro("EPIC-001", "Closeout Ready"),
        encoding="utf-8",
    )

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "Epic acceptance audit passed." in audit.stdout
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "| AC1 | First parent outcome is delivered. | TASK-001 (Complete) |" in audit_text
    assert "TASK-001: parent AC evidence recorded; TASK-001: QA pass" in audit_text
    map_text = (epic_dir / "ACCEPTANCE-MAP.md").read_text(encoding="utf-8")
    assert "| AC1 | First parent outcome is delivered. | TASK-001 (Complete) | TASK-001: parent AC evidence recorded; TASK-001: QA pass | None | Satisfied |" in map_text

    validate_only = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert validate_only.returncode == 0, validate_only.stdout + validate_only.stderr
    assert "Epic closeout summary:" in validate_only.stdout
    assert "- Parent ACs: 1 total, 1 pass, 0 deferred, 0 gap" in validate_only.stdout
    assert "- Next action: rerun closeout with --complete" in validate_only.stdout
    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| EPIC-001 | Closeout Ready | To Do |" in tracker_text

    completed = run_project(
        ["epic", "closeout", "--epic-id", "EPIC-001", "--complete"],
        cwd=tmp_path,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "- Next action: global epic row can be marked Complete." in completed.stdout
    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| EPIC-001 | Closeout Ready | Complete |" in tracker_text

    doctor = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "EPIC-001 is Complete but lacks non-placeholder QA/code-review evidence" not in doctor.stdout


def test_epic_audit_rejects_parent_evidence_from_unassigned_proof_owner(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Proof Owner"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Proof Owner",
            ["- AC1: Parent evidence must come from assigned proof owner."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(
        epic_dir,
        title="Proof Owner",
        ac_ids=["AC1"],
    )
    contract_text = (epic_dir / "EPIC-CONTRACT.md").read_text(encoding="utf-8")
    (epic_dir / "EPIC-CONTRACT.md").write_text(
        contract_text.replace("| AC1 | TASK-001 |", "| AC1 | TASK-999 |"),
        encoding="utf-8",
    )
    child_dir = epic_dir / "TASK-001-Wrong-Owner"
    child_dir.mkdir()
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Wrong Owner | Complete | Task | AC1 | tasks/EPIC-001-Proof-Owner/TASK-001-Wrong-Owner/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Wrong Owner", "Parent ACs": "AC1"}],
    )

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "TASK-001 is not assigned as proof owner" in audit.stdout
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "| Gap |" in audit_text


def test_visual_reference_recipe_requires_structured_evidence_before_review(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Visual Proof"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Visual Proof",
            ["- AC1: Production surface matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Visual Proof", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Visual Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Visual-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Visual Child",
            ["- AC1: Delivered UI matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Visual Child | Testing | Task | AC1 | tasks/EPIC-001-Visual-Proof/TASK-001-Visual-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    blocked = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Review"],
        cwd=tmp_path,
    )
    assert blocked.returncode != 0
    assert "structured evidence: EVIDENCE.json is missing" in blocked.stderr

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "structured evidence" not in doctor.stdout


def test_multi_parent_ac_structured_evidence_requires_one_claim_per_ac(
    tmp_path: Path,
) -> None:
    child_dir = tmp_path / "TASK-001-Multi-Ac"
    child_dir.mkdir()
    requirements_path = child_dir / "REQUIREMENTS.md"
    implementation_path = child_dir / "IMPLEMENTATION.md"
    requirements_path.write_text(
            ready_requirements(
                "TASK-001",
                "Multi AC",
                [
                    "- AC1: Delivered UI matches the reference visual exactly.",
                    "- AC2: Delivered UI matches the second reference visual exactly.",
                ],
            ),
            encoding="utf-8",
        )
    implementation_path.write_text(
        "## User Story\n\n"
        "As a maintainer, I want visual/reference fidelity proof, so that drift is caught.\n\n"
        "## Parent AC Coverage\n\n"
        "- AC1, AC2\n\n"
        "## Parent AC Evidence\n\n"
        "- AC1: Structured evidence recorded.\n"
        "- AC2: Structured evidence recorded.\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Visual/reference fidelity evidence recorded.\n"
        "- Findings: None.\n",
        encoding="utf-8",
    )
    evidence_dir = child_dir / "evidence"
    evidence_dir.mkdir()
    artifact = evidence_dir / "visual-comparison.txt"
    artifact.write_text("rendered comparison evidence", encoding="utf-8")
    artifact_hash = workflow_cli._sha256_file(artifact)

    base_record = {
        "id": "CLM-001",
        "claim": "Delivered surface matches the reference visual.",
        "recipe": "visual-reference-fidelity",
        "status": "pass",
        "commit": "abc123",
        "timestamp": "2026-07-09T00:00:00Z",
        "reference_artifact": "reference/playground.png",
        "delivered_artifact": "http://localhost:3000/widget",
        "comparison_method": "browser screenshot comparison",
        "evidence_artifact": "evidence/visual-comparison.txt",
        "evidence_artifact_hash": artifact_hash,
        "invalid_substitutes": [],
    }
    (child_dir / workflow_cli.STRUCTURED_EVIDENCE_FILENAME).write_text(
        json.dumps(
            {
                "task_id": "TASK-001",
                "claims": [{**base_record, "parent_ac": "AC1, AC2"}],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    comma_issues = workflow_cli._structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
        parent_ac_ids={"AC1", "AC2"},
    )
    assert "structured evidence: missing passing claim records for parent ACs: AC1, AC2" in comma_issues

    (child_dir / workflow_cli.STRUCTURED_EVIDENCE_FILENAME).write_text(
        json.dumps(
            {
                "task_id": "TASK-001",
                "claims": [
                    {**base_record, "id": "CLM-001", "parent_ac": "AC1"},
                    {**base_record, "id": "CLM-002", "parent_ac": "AC2"},
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    split_issues = workflow_cli._structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
        parent_ac_ids={"AC1", "AC2"},
    )
    assert split_issues == []


def test_invalid_substitute_structured_evidence_blocks_doctor_and_audit(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Invalid Proof"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Invalid Proof",
            ["- AC1: Production surface matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Invalid Proof", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Invalid Visual Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Invalid-Visual-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Invalid Visual Child",
            ["- AC1: Delivered UI matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    write_structured_evidence(child_dir, invalid_substitutes=["unit tests"])
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Invalid Visual Child | Complete | Task | AC1 | tasks/EPIC-001-Invalid-Proof/TASK-001-Invalid-Visual-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "records invalid substitute evidence: unit tests" in doctor.stdout

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "uses invalid substitute for `visual-reference-fidelity`: unit test" in audit.stdout
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "| Gap |" in audit_text


def test_valid_structured_visual_evidence_satisfies_epic_audit(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Valid Proof"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Valid Proof",
            ["- AC1: Production surface matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Valid Proof", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Valid Visual Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Valid-Visual-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Valid Visual Child",
            ["- AC1: Delivered UI matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    write_structured_evidence(child_dir)
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Valid Visual Child | Complete | Task | AC1 | tasks/EPIC-001-Valid-Proof/TASK-001-Valid-Visual-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "Epic acceptance audit passed." in audit.stdout


def test_stale_evidence_artifact_hash_blocks_doctor_and_audit(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Stale Evidence"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Stale Evidence",
            ["- AC1: Production surface matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Stale Evidence", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Stale Visual Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Stale-Visual-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Stale Visual Child",
            ["- AC1: Delivered UI matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    write_structured_evidence(
        child_dir,
        evidence_artifact_hash="sha256:0000000000000000000000000000000000000000000000000000000000000000",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Stale Visual Child | Complete | Task | AC1 | tasks/EPIC-001-Stale-Evidence/TASK-001-Stale-Visual-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "evidence_artifact_hash is stale" in doctor.stdout

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "evidence_artifact_hash is stale" in audit.stdout


def test_runtime_target_source_prose_contradiction_blocks_doctor(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Runtime Proof"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Runtime Proof",
            ["- AC1: Runtime target/source proof identifies the exact execution target."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Runtime Proof", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Runtime Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Runtime-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Runtime Child",
            ["- AC1: Runtime target/source proof identifies the exact execution target."],
        ),
        encoding="utf-8",
    )
    impl_text = (
        ready_implementation("AC1", qa=True)
        + "\n## Runtime Proof Notes\n\n"
        "- Execution target: release/deployed\n"
        "- Source artifact: release bundle\n"
    )
    (child_dir / "IMPLEMENTATION.md").write_text(impl_text, encoding="utf-8")
    write_runtime_structured_evidence(
        child_dir,
        execution_target="working/local",
        source_artifact="local checkout",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Runtime Child | Complete | Task | AC1 | tasks/EPIC-001-Runtime-Proof/TASK-001-Runtime-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "prose claims execution_target release/deployed" in doctor.stdout
    assert "structured evidence proves working/local" in doctor.stdout


def test_epic_closeout_blocks_missing_parent_ac_evidence(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Closeout Blocked"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Closeout Blocked\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: First parent outcome is delivered.\n",
        encoding="utf-8",
    )
    child_dir = epic_dir / "TASK-001-Blocked-Child"
    child_dir.mkdir()
    (child_dir / "IMPLEMENTATION.md").write_text(
        "## User Story\n\n"
        "As a maintainer, I forgot evidence.\n\n"
        "## Parent AC Evidence\n\n"
        "- AC1: Pending implementation evidence.\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Local task validation only.\n"
        "- Findings: None.\n",
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Blocked Child | Complete | Task | AC1 | tasks/EPIC-001-Closeout-Blocked/TASK-001-Blocked-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    blocked = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert blocked.returncode != 0
    assert "Epic closeout summary:" in blocked.stdout
    assert "- Parent ACs: 1 total, 0 pass, 0 deferred, 1 gap" in blocked.stdout
    assert "- Missing parent evidence: AC1: TASK-001 lacks parent AC evidence" in blocked.stdout
    assert "- Epic retro: epic retro section 'Lessons' is missing or still placeholder" in blocked.stdout
    assert "- Next action: resolve the listed gaps or record approved deferrals" in blocked.stdout
    assert "Epic closeout blocked by acceptance gaps" in blocked.stdout
    assert "AC1: TASK-001 lacks parent AC evidence" in blocked.stdout


def test_epic_closeout_accepts_approved_deferral_with_follow_up(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Deferred Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    assert (epic_dir / "DEFERRALS.md").exists()
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Deferred Epic",
            ["- AC1: Deferred parent outcome is explicitly tracked."],
        ),
        encoding="utf-8",
    )
    (epic_dir / "DEFERRALS.md").write_text(
        "# Deferrals\n\n"
        "| Parent AC | Status | Owner | Decision Date | Reason | Follow-up | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
        "| AC1 | Approved | Product Owner | 2026-06-17 | Deferred from MVP | EPIC-002 | Owner approved follow-up |\n",
        encoding="utf-8",
    )
    (epic_dir / "RETRO.md").write_text(
        ready_epic_retro("EPIC-001", "Deferred Epic"),
        encoding="utf-8",
    )

    closeout = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert closeout.returncode == 0, closeout.stdout + closeout.stderr
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "Deferred from MVP" in audit_text
    assert "| AC1 | Deferred parent outcome is explicitly tracked. | None | None | Approved:" in audit_text
    assert "| Deferred |" in audit_text


def test_epic_closeout_blocks_incomplete_deferral_metadata(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Bad Deferral"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Bad Deferral\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: Deferred parent outcome is explicitly tracked.\n",
        encoding="utf-8",
    )
    (epic_dir / "DEFERRALS.md").write_text(
        "# Deferrals\n\n"
        "| Parent AC | Status | Owner | Decision Date | Reason | Follow-up | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
        "| AC1 | Approved | Product Owner | 2026-06-17 | Deferred from MVP |  | Missing follow-up |\n",
        encoding="utf-8",
    )

    closeout = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert closeout.returncode != 0
    assert "AC1: no mapped child rows" in closeout.stdout
    assert "AC1: deferral is missing approval metadata or follow-up" in closeout.stdout


def test_epic_status_requires_parent_ac_evidence_before_complete(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Epic Status"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Epic Status",
            ["- AC1: Status gates enforce parent evidence."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Epic Status")
    child_dir = epic_dir / "TASK-001-Status-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Status Child",
            ["- AC1: Status gates enforce parent evidence."],
        ),
        encoding="utf-8",
    )
    child_impl = child_dir / "IMPLEMENTATION.md"
    child_impl.write_text(ready_implementation("AC1", qa=True), encoding="utf-8")
    child_impl.write_text(
        child_impl.read_text(encoding="utf-8").replace(
            "- AC1: Targeted parent evidence recorded.",
            "- AC1: Pending implementation evidence.",
        ),
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Status Child | In Progress | Task | AC1 | tasks/EPIC-001-Epic-Status/TASK-001-Status-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Status Child", "Parent ACs": "AC1"}],
    )

    testing = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Testing"],
        cwd=tmp_path,
    )
    assert testing.returncode == 0, testing.stdout + testing.stderr
    review = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Review"],
        cwd=tmp_path,
    )
    assert review.returncode == 0, review.stdout + review.stderr

    blocked = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert blocked.returncode != 0
    assert "cannot move to Complete without parent AC evidence for: AC1" in blocked.stderr

    child_impl.write_text(
        child_impl.read_text(encoding="utf-8").replace(
            "- AC1: Pending implementation evidence.",
            "- AC1: Targeted parent evidence recorded.",
        ),
        encoding="utf-8",
    )
    completed = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "Updated TASK-001: Review -> Complete" in completed.stdout


def test_task_ready_blocks_placeholders_and_allows_ready_docs(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Readiness Check", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr

    blocked = run_project(["task", "ready", "--id", "TASK-001"], cwd=tmp_path)
    assert blocked.returncode != 0
    assert "TASK-001 is not ready" in blocked.stderr
    assert "owner input required" in blocked.stderr
    assert "agent action required" in blocked.stderr

    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-001", "Readiness Check"),
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")

    ready = run_project(["task", "ready", "--id", "TASK-001"], cwd=tmp_path)
    assert ready.returncode == 0, ready.stdout + ready.stderr
    assert "TASK-001 readiness gate passed." in ready.stdout


def test_task_approval_envelope_command_and_stale_detection(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Approval Envelope", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    requirements_path = task_dir / "REQUIREMENTS.md"
    requirements_path.write_text(
        ready_requirements("TASK-001", "Approval Envelope"),
        encoding="utf-8",
    )
    implementation_path = task_dir / "IMPLEMENTATION.md"
    assert "____" in implementation_path.read_text(encoding="utf-8")

    # Simulate requirements drafted before command-written approval existed.
    requirements_path.write_text(
        workflow_cli._remove_markdown_section(
            requirements_path.read_text(encoding="utf-8"),
            workflow_cli.OWNER_APPROVAL_HEADING,
        ),
        encoding="utf-8",
    )

    blocked = run_project(["task", "status", "--id", "TASK-001", "--to", "Analysing"], cwd=tmp_path)
    assert blocked.returncode != 0
    assert "add `## Owner Approval`" in blocked.stderr

    approved = run_project(
        [
            "task",
            "approve-requirements",
            "--id",
            "TASK-001",
            "--approved-by",
            "Product Owner",
            "--source",
            "Owner approved TASK-001 requirements in planning thread.",
        ],
        cwd=tmp_path,
    )
    assert approved.returncode == 0, approved.stdout + approved.stderr
    approved_text = requirements_path.read_text(encoding="utf-8")
    assert "- Approved scope envelope: Yes" in approved_text
    assert "- Approved artifact identity: sha256:" in approved_text

    analysing = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Analysing"],
        cwd=tmp_path,
    )
    assert analysing.returncode == 0, analysing.stdout + analysing.stderr
    implementation_path.write_text(ready_implementation(), encoding="utf-8")
    ready = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Ready"],
        cwd=tmp_path,
    )
    assert ready.returncode == 0, ready.stdout + ready.stderr

    requirements_path.write_text(
        approved_text + "\n## Added Scope\n\n- This changes the approved requirements.\n",
        encoding="utf-8",
    )
    stale = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "In Progress"],
        cwd=tmp_path,
    )
    assert stale.returncode != 0
    assert "approval is stale because requirements or ACs changed" in stale.stderr


def test_task_adopt_records_approval_and_untrusted_evidence_gate(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(["task", "init", "--title", "Legacy Task", "--update-tracker"], cwd=tmp_path)
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: TASK-001\n"
        "- Title: Legacy Task\n\n"
        "## Goal\n\n"
        "- Adopt old work.\n\n"
        "## Non-Goals\n\n"
        "- Do not change product scope.\n\n"
        "## Users & Context\n\n"
        "- Maintainers need old work under gates.\n\n"
        "## Requirements (Outcome-Focused)\n\n"
        "- The old task can continue only after adoption.\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: Legacy adoption is recorded.\n\n"
        "## Open Questions (Answer Needed)\n\n"
        "- None.\n\n"
        "## Decisions (Resolved)\n\n"
        "- Adopt explicitly.\n\n"
        "## Validation Plan\n\n"
        "- Run workflow status gates.\n",
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation(qa=True),
        encoding="utf-8",
    )
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(
            "| TASK-001 | Legacy Task | To Do |",
            "| TASK-001 | Legacy Task | Analysing |",
        ),
        encoding="utf-8",
    )

    blocked = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Plan Confirmed"],
        cwd=tmp_path,
    )
    assert blocked.returncode != 0
    assert "Owner Approval" in blocked.stderr

    adopt = run_project(
        [
            "task",
            "adopt",
            "--id",
            "TASK-001",
            "--approved-by",
            "Test Owner",
            "--source",
            "Owner approved legacy adoption.",
        ],
        cwd=tmp_path,
    )
    assert adopt.returncode == 0, adopt.stdout + adopt.stderr
    requirements_text = (task_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    assert "## Legacy Adoption" in requirements_text
    assert "Evidence refreshed after adoption: No" in requirements_text

    confirmed = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Plan Confirmed"],
        cwd=tmp_path,
    )
    assert confirmed.returncode == 0, confirmed.stdout + confirmed.stderr

    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(
            "| TASK-001 | Legacy Task | Plan Confirmed |",
            "| TASK-001 | Legacy Task | Review |",
        ),
        encoding="utf-8",
    )
    complete_blocked = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert complete_blocked.returncode != 0
    assert "pre-adoption evidence as untrusted" in complete_blocked.stderr

    refreshed = run_project(
        [
            "task",
            "adopt",
            "--id",
            "TASK-001",
            "--approved-by",
            "Test Owner",
            "--source",
            "Owner approved refreshed legacy evidence.",
            "--evidence-refreshed",
        ],
        cwd=tmp_path,
    )
    assert refreshed.returncode == 0, refreshed.stdout + refreshed.stderr
    completed = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_epic_adopt_records_approval_and_amendments_file(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Legacy Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / workflow_cli.EPIC_AMENDMENTS_FILENAME).unlink()
    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Legacy Epic\n\n"
        "## Goal\n\n"
        "- Adopt old epic.\n\n"
        "## Non-Goals\n\n"
        "- Do not infer closeout evidence.\n\n"
        "## Users & Context\n\n"
        "- Maintainers need old epic under gates.\n\n"
        "## Requirements (Outcome-Focused)\n\n"
        "- The old epic has explicit adoption metadata.\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: Legacy epic adoption is recorded.\n\n"
        "## Open Questions (Answer Needed)\n\n"
        "- None.\n\n"
        "## Decisions (Resolved)\n\n"
        "- Adopt explicitly.\n\n"
        "## Validation Plan\n\n"
        "- Run workflow status gates.\n",
        encoding="utf-8",
    )

    adopt = run_project(
        [
            "epic",
            "adopt",
            "--epic-id",
            "EPIC-001",
            "--approved-by",
            "Test Owner",
            "--source",
            "Owner approved legacy epic adoption.",
        ],
        cwd=tmp_path,
    )
    assert adopt.returncode == 0, adopt.stdout + adopt.stderr
    requirements_text = (epic_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    assert "## Owner Approval" in requirements_text
    assert "## Legacy Adoption" in requirements_text
    assert "Evidence refreshed after adoption: No" in requirements_text
    assert (epic_dir / workflow_cli.EPIC_AMENDMENTS_FILENAME).exists()


def test_doctor_flags_manual_active_task_without_approval_envelope(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Manual Bypass", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    requirements_text = workflow_cli._remove_markdown_section(
        ready_requirements("TASK-001", "Manual Bypass"),
        workflow_cli.OWNER_APPROVAL_HEADING,
    )
    (task_dir / "REQUIREMENTS.md").write_text(requirements_text, encoding="utf-8")
    (task_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(" | To Do | ", " | In Progress | "),
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "TASK-001 approval envelope" in doctor.stdout
    assert "add `## Owner Approval`" in doctor.stdout


def test_epic_child_ready_uses_parent_approval_envelope_without_child_approval(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Envelope Parent"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Envelope Parent",
            ["- AC1: In-envelope child work can proceed."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Envelope Parent")
    child_dir = epic_dir / "TASK-001-In-Envelope-Child"
    child_dir.mkdir()
    child_requirements = ready_requirements(
        "TASK-001",
        "In Envelope Child",
        ["- AC1: Child work is ready inside the parent envelope."],
    )
    child_requirements = workflow_cli._remove_markdown_section(
        child_requirements,
        workflow_cli.OWNER_APPROVAL_HEADING,
    )
    child_requirements = child_requirements.replace(
        "## Goal\n\n",
        "## Owner Approval\n\n"
        "- Requirements reviewed by owner: No\n"
        "- Acceptance criteria reviewed by owner: No\n"
        "- Approved for decomposition: No\n"
        "- Approved for implementation: No\n"
        "- Approved scope envelope: No\n"
        "- Approved by: Inherited from parent epic envelope when unchanged\n"
        "- Approval date: Inherited from parent epic envelope when unchanged\n"
        "- Approval note / source: Inherited from parent epic envelope when unchanged\n"
        "- Approved artifact identity: Inherited from parent epic envelope when unchanged\n\n"
        "## Goal\n\n",
    )
    (child_dir / "REQUIREMENTS.md").write_text(child_requirements, encoding="utf-8")
    (child_dir / "IMPLEMENTATION.md").write_text(ready_implementation("AC1"), encoding="utf-8")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | In Envelope Child | In Progress | Task | AC1 | tasks/EPIC-001-Envelope-Parent/TASK-001-In-Envelope-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "In Envelope Child", "Parent ACs": "AC1"}],
    )

    ready_child = run_project(
        ["epic", "ready-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert ready_child.returncode == 0, ready_child.stdout + ready_child.stderr
    assert "TASK-001 readiness gate passed" in ready_child.stdout


def test_epic_ready_blocks_vague_epic_and_decomposition(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Vague Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    ready = run_project(["epic", "ready", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert ready.returncode != 0
    assert "EPIC-001 is not ready" in ready.stderr

    decompose = run_project(["epic", "decompose", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert decompose.returncode != 0
    assert "EPIC-001 is not ready" in decompose.stderr


def test_epic_lifecycle_gates_global_epic_status(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Lifecycle Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))

    analysing = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Analysing"],
        cwd=tmp_path,
    )
    assert analysing.returncode == 0, analysing.stdout + analysing.stderr
    assert "Updated EPIC-001: To Do -> Analysing" in analysing.stdout

    ready_blocked = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Ready"],
        cwd=tmp_path,
    )
    assert ready_blocked.returncode != 0
    assert "EPIC-001 cannot move to Ready" in ready_blocked.stderr

    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Lifecycle Epic",
            ["- AC1: Lifecycle status is safely gated."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Lifecycle Epic")

    ready = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Ready"],
        cwd=tmp_path,
    )
    assert ready.returncode == 0, ready.stdout + ready.stderr
    assert "Updated EPIC-001: Analysing -> Ready" in ready.stdout

    in_progress_blocked = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "In Progress"],
        cwd=tmp_path,
    )
    assert in_progress_blocked.returncode != 0
    assert "AC1: no mapped child rows" in in_progress_blocked.stderr

    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Lifecycle Child | Proposed | Task | AC1 |  |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    in_progress = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "In Progress"],
        cwd=tmp_path,
    )
    assert in_progress.returncode == 0, in_progress.stdout + in_progress.stderr
    assert "Updated EPIC-001: Ready -> In Progress" in in_progress.stdout

    closeout_blocked = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Closeout"],
        cwd=tmp_path,
    )
    assert closeout_blocked.returncode != 0
    assert "TASK-001 is Proposed, not Complete" in closeout_blocked.stderr

    complete_blocked = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert complete_blocked.returncode != 0
    assert "use `epic closeout --epic-id <EPIC-ID> --complete`" in complete_blocked.stderr


def test_epic_ready_child_blocks_shallow_child_status(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Child Readiness"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Child Readiness",
            ["- AC1: Shallow child readiness is enforced."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Child Readiness")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Shallow Child | In Progress | Task | AC1 | tasks/EPIC-001-Child-Readiness/TASK-001-Shallow-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Shallow Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Shallow-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: TASK-001\n"
        "- Title: Shallow Child\n\n"
        "## Goal\n\n"
        "Describe the user outcome.\n",
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        "## User Story\n\nAs a ____, I want ____, so that ____.\n",
        encoding="utf-8",
    )

    ready_child = run_project(
        ["epic", "ready-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert ready_child.returncode != 0
    assert "TASK-001 is not ready" in ready_child.stderr

    status = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Testing"],
        cwd=tmp_path,
    )
    assert status.returncode != 0
    assert "TASK-001 is not ready" in status.stderr


def test_discovery_task_ready_allows_bounded_discovery(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Discovery Spike", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    discovery_text = (
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: TASK-001\n"
        "- Title: Discovery Spike\n"
        "- Type: Discovery\n\n"
        "## Discovery Plan\n\n"
        "- Question: Which readiness command shape should ship first?\n"
        "- Decision: Choose the command shape for implementation.\n"
        "- Boundary: Limit to CLI and generated guidance review.\n"
        "- Output: A recommendation recorded in requirements.\n"
        "- Validation: Owner can approve the recommendation.\n"
    )
    (task_dir / "REQUIREMENTS.md").write_text(discovery_text, encoding="utf-8")
    (task_dir / "IMPLEMENTATION.md").write_text(
        "## Discovery Plan\n\n"
        "- Type: Discovery\n"
        "- Question: Which readiness command shape should ship first?\n"
        "- Decision: Choose the command shape for implementation.\n"
        "- Boundary: Limit to CLI and generated guidance review.\n"
        "- Output: A recommendation recorded in requirements.\n"
        "- Validation: Owner can approve the recommendation.\n",
        encoding="utf-8",
    )

    ready = run_project(["task", "ready", "--id", "TASK-001"], cwd=tmp_path)
    assert ready.returncode == 0, ready.stdout + ready.stderr
    assert "TASK-001 readiness gate passed." in ready.stdout


def create_smoke_bomb_fixture(tmp_path: Path, source_agent: str) -> Path:
    root = tmp_path / "agency-repo"
    root.mkdir()
    init = run_project(["init", "--agent", source_agent], cwd=root)
    assert init.returncode == 0, init.stdout + init.stderr
    (root / "README.md").write_text(
        "# Client Project\n\n"
        "This application serves the client's operational workflow. Install dependencies "
        "with the repository package manager, inspect `src/` for application code, and run "
        "the reviewed validation command before delivery.\n",
        encoding="utf-8",
    )
    (root / ".project-workflow" / "guidance.md").write_text(
        "# Project Workflow Guidance\n\n"
        "This repository keeps application code in `src/`. Preserve public interfaces and "
        "run the reviewed validation commands before handing changes over.\n",
        encoding="utf-8",
    )
    (root / "CLIENT-CANARY.txt").write_text("client-owned bytes\n", encoding="utf-8")
    init_git_fixture(root)
    return root


def smoke_bomb_args(root: Path, output: Path, client_agent: str) -> list[str]:
    return [
        "smoke-bomb",
        "--root",
        str(root),
        "--client-agent",
        client_agent,
        "--validation-command",
        "test -f README.md",
        "--output",
        str(output),
        "--format",
        "json",
    ]


@pytest.mark.parametrize("agent", sorted(workflow_cli.AGENT_CHOICES))
def test_smoke_bomb_plans_applies_and_exports_each_agent_surface(
    tmp_path: Path,
    agent: str,
) -> None:
    root = create_smoke_bomb_fixture(tmp_path, agent)
    output = tmp_path / f"{agent}-client.zip"
    before_canary = (root / "CLIENT-CANARY.txt").read_bytes()
    before_head = _run_git_for_test(root, ["rev-parse", "HEAD"])

    first_plan = run_project([*smoke_bomb_args(root, output, agent), "--plan"], cwd=root)
    assert first_plan.returncode == 0, first_plan.stdout + first_plan.stderr
    second_plan = run_project([*smoke_bomb_args(root, output, agent), "--plan"], cwd=root)
    assert second_plan.returncode == 0, second_plan.stdout + second_plan.stderr
    plan = json.loads(first_plan.stdout)
    assert json.loads(second_plan.stdout)["plan_fingerprint"] == plan["plan_fingerprint"]
    assert plan["repository"]["on_default_branch"] is True
    assert plan["warnings"]
    assert plan["blockers"] == []
    assert plan["archive"]["entry_count"] == len(plan["archive"]["included_paths"])
    assert _run_git_for_test(root, ["status", "--porcelain"]) == ""

    applied = run_project(
        [
            *smoke_bomb_args(root, output, agent),
            "--apply",
            "--plan-fingerprint",
            plan["plan_fingerprint"],
            "--yes",
        ],
        cwd=root,
    )
    assert applied.returncode == 0, applied.stdout + applied.stderr
    result = json.loads(applied.stdout)
    assert result["status"] == "exported"
    assert result["validation"][0]["exit_code"] == 0
    assert "stdout_sha256" in result["validation"][0]
    assert "stderr_sha256" in result["validation"][0]
    assert "stdout_tail" not in result["validation"][0]
    assert "stderr_tail" not in result["validation"][0]
    assert output.is_file()
    assert workflow_cli._sha256_file(output) == result["archive"]["sha256"]
    assert (root / "CLIENT-CANARY.txt").read_bytes() == before_canary
    assert _run_git_for_test(root, ["rev-parse", "HEAD"]) == before_head
    assert not (root / ".project-workflow").exists()

    with zipfile.ZipFile(output) as archive:
        entries = sorted(archive.namelist())
        assert entries == result["archive"]["entries"]
        assert "README.md" in entries
        assert "AGENTS.md" in entries
        assert not any(value == ".git" or value.startswith(".git/") for value in entries)
        assert not any(value.startswith(".project-workflow/") for value in entries)
        if agent == "claude-code":
            assert "CLAUDE.md" in entries
        elif agent == "cursor":
            assert ".cursor/rules/client-project.mdc" in entries
        elif agent == "github-copilot":
            assert ".github/copilot-instructions.md" in entries


def test_smoke_bomb_rolls_back_injected_apply_failure(tmp_path: Path) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    output = tmp_path / "client.zip"
    args = smoke_bomb_args(root, output, "codex")
    plan_result = run_project([*args, "--plan"], cwd=root)
    assert plan_result.returncode == 0, plan_result.stdout + plan_result.stderr
    plan = json.loads(plan_result.stdout)
    before = {
        path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mode & 0o777)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }

    failed = run_project(
        [
            *args,
            "--apply",
            "--plan-fingerprint",
            plan["plan_fingerprint"],
            "--yes",
            "--fail-after-replacements",
            "1",
        ],
        cwd=root,
    )
    assert failed.returncode != 0
    result = json.loads(failed.stdout)
    assert result["failure"]["code"] == "PW_SMOKE_BOMB_APPLY_FAILED"
    after = {
        path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mode & 0o777)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }
    assert after == before
    assert _run_git_for_test(root, ["status", "--porcelain"]) == ""
    assert not output.exists()


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("dirty", "PW_SMOKE_BOMB_DIRTY_WORKTREE"),
        ("secret", "PW_SMOKE_BOMB_UNSAFE_TARGET"),
        ("residual", "PW_SMOKE_BOMB_RESIDUAL_REFERENCE"),
    ],
)
def test_smoke_bomb_plan_blocks_unsafe_handoff_state(
    tmp_path: Path,
    mutation: str,
    expected_code: str,
) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    if mutation == "dirty":
        (root / "UNTRACKED.txt").write_text("dirty\n", encoding="utf-8")
    elif mutation == "secret":
        (root / ".env").write_text("TOKEN=fixture-only\n", encoding="utf-8")
        commit_git_fixture(root, "add secret-like fixture")
    else:
        (root / "AGENCY-NOTES.md").write_text(
            "This file still references project-workflow internal delivery state.\n",
            encoding="utf-8",
        )
        commit_git_fixture(root, "add residual reference fixture")

    planned = run_project(
        [*smoke_bomb_args(root, tmp_path / "client.zip", "codex"), "--plan"],
        cwd=root,
    )
    assert planned.returncode != 0
    plan = json.loads(planned.stdout)
    assert expected_code in {blocker["code"] for blocker in plan["blockers"]}


def test_smoke_bomb_repeat_export_is_content_idempotent(tmp_path: Path) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    output = tmp_path / "client.zip"
    args = smoke_bomb_args(root, output, "codex")
    plan = json.loads(run_project([*args, "--plan"], cwd=root).stdout)
    applied = run_project(
        [
            *args,
            "--apply",
            "--plan-fingerprint",
            plan["plan_fingerprint"],
            "--yes",
        ],
        cwd=root,
    )
    assert applied.returncode == 0, applied.stdout + applied.stderr
    first_sha = json.loads(applied.stdout)["archive"]["sha256"]
    commit_git_fixture(root, "sanitized client snapshot")

    repeat_plan_result = run_project([*args, "--plan"], cwd=root)
    assert repeat_plan_result.returncode == 0, repeat_plan_result.stdout + repeat_plan_result.stderr
    repeat_plan = json.loads(repeat_plan_result.stdout)
    assert repeat_plan["workflow_installed"] is False
    assert repeat_plan["actions"] == []
    repeated = run_project(
        [
            *args,
            "--apply",
            "--plan-fingerprint",
            repeat_plan["plan_fingerprint"],
            "--yes",
        ],
        cwd=root,
    )
    assert repeated.returncode == 0, repeated.stdout + repeated.stderr
    assert json.loads(repeated.stdout)["archive"]["sha256"] == first_sha
    assert _run_git_for_test(root, ["status", "--porcelain"]) == ""


def test_smoke_bomb_rejects_stale_fingerprint_before_mutation(tmp_path: Path) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    output = tmp_path / "client.zip"
    args = smoke_bomb_args(root, output, "codex")
    original_plan = json.loads(run_project([*args, "--plan"], cwd=root).stdout)
    (root / "README.md").write_text(
        (root / "README.md").read_text(encoding="utf-8") + "\nReviewed handoff note.\n",
        encoding="utf-8",
    )
    commit_git_fixture(root, "change planned input")

    failed = run_project(
        [
            *args,
            "--apply",
            "--plan-fingerprint",
            original_plan["plan_fingerprint"],
            "--yes",
        ],
        cwd=root,
    )
    assert failed.returncode != 0
    assert json.loads(failed.stdout)["failure"]["code"] == "PW_SMOKE_BOMB_APPLY_STALE_PLAN"
    assert (root / ".project-workflow").is_dir()
    assert _run_git_for_test(root, ["status", "--porcelain"]) == ""
    assert not output.exists()


def test_smoke_bomb_failed_reviewed_validation_refuses_zip(tmp_path: Path) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    output = tmp_path / "client.zip"
    args = smoke_bomb_args(root, output, "codex")
    command_index = args.index("test -f README.md")
    args[command_index] = "exit 7"
    plan_result = run_project([*args, "--plan"], cwd=root)
    assert plan_result.returncode == 0, plan_result.stdout + plan_result.stderr
    plan = json.loads(plan_result.stdout)

    failed = run_project(
        [
            *args,
            "--apply",
            "--plan-fingerprint",
            plan["plan_fingerprint"],
            "--yes",
        ],
        cwd=root,
    )
    assert failed.returncode != 0
    result = json.loads(failed.stdout)
    assert result["failure"]["code"] == "PW_SMOKE_BOMB_VALIDATION_FAILED"
    assert result["archive"] is None
    assert not output.exists()
    assert not (root / ".project-workflow").exists()


@pytest.mark.parametrize(
    "unsafe_state",
    ["wrong-root", "symlink", "symlink-parent", "unmarked-generated"],
)
def test_smoke_bomb_plan_blocks_ambiguous_or_unowned_targets(
    tmp_path: Path,
    unsafe_state: str,
) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    plan_root = root
    expected_code = "PW_SMOKE_BOMB_UNSAFE_TARGET"
    if unsafe_state == "wrong-root":
        plan_root = root / "nested"
        plan_root.mkdir()
        (plan_root / "README.md").write_text("Nested path fixture.\n", encoding="utf-8")
        commit_git_fixture(root, "add nested directory")
        expected_code = "PW_SMOKE_BOMB_AMBIGUOUS_ROOT"
    else:
        skill_path = root / ".agents" / "skills" / "project-task" / "SKILL.md"
        original = skill_path.read_text(encoding="utf-8")
        if unsafe_state == "symlink":
            target = root / "CLIENT-CANARY.txt"
            skill_path.unlink()
            skill_path.symlink_to(target)
        elif unsafe_state == "symlink-parent":
            outside_agents = tmp_path / "outside-agents"
            shutil.move(str(root / ".agents"), outside_agents)
            (root / ".agents").symlink_to(outside_agents, target_is_directory=True)
        else:
            skill_path.write_text(
                original.replace("<!-- project-workflow:generated -->\n\n", ""),
                encoding="utf-8",
            )
        commit_git_fixture(root, f"create {unsafe_state} fixture")

    planned = run_project(
        [
            *smoke_bomb_args(plan_root, tmp_path / "client.zip", "codex"),
            "--plan",
        ],
        cwd=root,
    )
    assert planned.returncode != 0
    plan = json.loads(planned.stdout)
    assert expected_code in {blocker["code"] for blocker in plan["blockers"]}


def test_smoke_bomb_preserves_short_user_agent_content_and_blocks(tmp_path: Path) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    agents_path = root / "AGENTS.md"
    managed = agents_path.read_text(encoding="utf-8")
    short_user_content = "# Local Rule\n\nPreserve this owner note.\n\n"
    agents_path.write_text(short_user_content + managed, encoding="utf-8")
    commit_git_fixture(root, "add short owner agent guidance")

    planned = run_project(
        [*smoke_bomb_args(root, tmp_path / "client.zip", "codex"), "--plan"],
        cwd=root,
    )
    assert planned.returncode != 0
    plan = json.loads(planned.stdout)
    assert "PW_SMOKE_BOMB_CLIENT_GUIDANCE_REQUIRED" in {
        blocker["code"] for blocker in plan["blockers"]
    }
    agents_action = next(action for action in plan["actions"] if action["path"] == "AGENTS.md")
    assert agents_action["after_sha256"] == workflow_cli._smoke_bomb_hash(
        workflow_cli._smoke_bomb_remove_managed_block(
            short_user_content + managed
        ).encode("utf-8")
    )


def test_smoke_bomb_blocks_archive_when_validation_mutates_planned_output(
    tmp_path: Path,
) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    output = tmp_path / "client.zip"
    args = smoke_bomb_args(root, output, "codex")
    command_index = args.index("test -f README.md")
    args[command_index] = "printf '\\nvalidation mutation\\n' >> AGENTS.md"
    plan_result = run_project([*args, "--plan"], cwd=root)
    assert plan_result.returncode == 0, plan_result.stdout + plan_result.stderr
    plan = json.loads(plan_result.stdout)

    failed = run_project(
        [
            *args,
            "--apply",
            "--plan-fingerprint",
            plan["plan_fingerprint"],
            "--yes",
        ],
        cwd=root,
    )
    assert failed.returncode != 0
    result = json.loads(failed.stdout)
    assert result["failure"]["code"] == "PW_SMOKE_BOMB_ARCHIVE_BLOCKED"
    assert "Post-validation content differs" in result["failure"]["message"]
    assert not output.exists()
