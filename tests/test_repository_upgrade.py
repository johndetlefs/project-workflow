from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from project_workflow import __version__
from project_workflow import cli as workflow_cli
from tests.workflow_test_support import (
    REPO_ROOT,
    add_accepted_doctor_warnings,
    commit_git_fixture,
    init_git_fixture,
    run_project,
)


def test_workflow_manifest_contract_is_deterministic() -> None:
    manifest = workflow_cli._current_workflow_manifest()

    assert manifest == workflow_cli.WorkflowManifest(
        manifest_version=1,
        package_version=__version__,
        asset_version=8,
        schema_version=1,
        applied_migrations=(),
    )
    assert workflow_cli._serialize_workflow_manifest(manifest) == (
        "{\n"
        '  "manifest_version": 1,\n'
        '  "package_version": "0.9.1",\n'
        '  "asset_version": 8,\n'
        '  "schema_version": 1,\n'
        '  "applied_migrations": []\n'
        "}\n"
    )
    assert (
        workflow_cli._parse_workflow_manifest(workflow_cli._workflow_manifest_payload(manifest))
        == manifest
    )


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
        "assets-and-schema-behind",
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
        ({"asset_version": 9}, "future-asset-version"),
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
    policy = " ".join((REPO_ROOT / "COMPATIBILITY.md").read_text(encoding="utf-8").split())
    assert "recognized pre-versioned repository shape" in policy
    assert "breaking release" in policy
    assert (
        "plans managed-asset refresh plus repository-schema transformation as one transaction"
        in policy
    )


def test_upgrade_documentation_and_agent_guidance_match_command_contract() -> None:
    readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme = " ".join(readme_text.split())
    maintenance_text = (REPO_ROOT / "docs/maintenance.md").read_text(encoding="utf-8")
    maintenance = " ".join(maintenance_text.split())
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    compatibility = (REPO_ROOT / "COMPATIBILITY.md").read_text(encoding="utf-8")
    guidance_paths = (
        REPO_ROOT / "src" / "project_workflow" / "codex" / "AGENTS.md",
        REPO_ROOT / "src" / "project_workflow" / "cursor" / "rules" / "project-workflow.mdc",
    )

    for required in (
        "project upgrade --agent codex",
        "--plan --format json",
        "--yes",
        "--apply",
        "--plan-fingerprint",
        "clean Git worktree",
        "PW-0001-legacy-manifest",
    ):
        assert required in maintenance
    assert "COMPATIBILITY.md" in maintenance
    assert "docs/maintenance.md" in readme
    runbook = maintenance
    for required in (
        "do not run init first",
        "Doctor is not a prerequisite",
        "managed helper/agent-asset changes",
        "asks for confirmation",
        "applies the confirmed plan as one transaction",
        "Pre-versioned legacy",
        "Invalid or unsupported future manifest",
    ):
        assert required in runbook
    assert "project upgrade --agent codex --yes" in maintenance
    assert "project upgrade --agent codex --plan --format json" in maintenance
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
    expected = workflow_cli._serialize_workflow_manifest(workflow_cli._current_workflow_manifest())
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
    assert "already initialized (upgradeable); init made no changes" in result.stdout
    assert "project upgrade --agent github-copilot" in result.stdout


@pytest.mark.parametrize("state", ["invalid", "future"])
def test_project_init_does_not_rewrite_invalid_or_future_manifest(
    tmp_path: Path,
    state: str,
) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    manifest_path = workflow_dir / workflow_cli.WORKFLOW_MANIFEST_FILENAME
    content = (
        b"{not-json}\n"
        if state == "invalid"
        else json.dumps(
            {
                "manifest_version": 2,
                "package_version": "9.0.0",
                "asset_version": 9,
                "schema_version": 9,
                "applied_migrations": [],
            }
        ).encode("utf-8")
    )
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

    warning = next(
        issue for issue in workflow_cli.run_doctor(tmp_path) if issue.severity == "warning"
    )
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
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    plan = workflow_cli._build_upgrade_plan(tmp_path, migrations=migrations)

    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
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
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    plan = workflow_cli._build_upgrade_plan(tmp_path, migrations=migrations)
    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

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
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    result = run_project(
        ["upgrade", "--agent", "codex", "--plan", "--format", "json"], cwd=tmp_path
    )
    human = run_project(["upgrade", "--agent", "codex", "--plan"], cwd=tmp_path)

    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
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

    assert "PW_UPGRADE_REGISTRY_INVALID_TARGET" in {blocker["code"] for blocker in plan["blockers"]}
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

    missing = run_project(["upgrade", "--agent", "github-copilot", "--apply"], cwd=tmp_path)
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
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }

    result = workflow_cli._apply_upgrade_plan(
        tmp_path,
        plan["plan_fingerprint"],
        migrations=migrations,
        handlers=handlers,
        fail_after_replacements=fail_after,
    )

    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }
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
        json.loads((tmp_path / ".project-workflow" / "manifest.json").read_text(encoding="utf-8"))
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
