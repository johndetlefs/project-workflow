from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli


GLOBAL_HEADER = (
    "# Stories\n\n"
    "| ID | Title | Status | Docs |\n"
    "|---|---|---|---|\n"
)
EPIC_HEADER = (
    "# Stories\n\n"
    "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
    "|---|---|---|---|---|---|---|---|\n"
)
LEGACY_EPIC_HEADER = (
    "# Stories\n\n"
    "| ID | Title | Status | Type | Docs | Branch | Notes |\n"
    "|---|---|---|---|---|---|---|\n"
)


def write_manifest(root: Path, payload: dict[str, object]) -> None:
    workflow_dir = root / ".project-workflow"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "manifest.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def current_manifest(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "manifest_version": workflow_cli.CURRENT_MANIFEST_VERSION,
        "package_version": workflow_cli.CURRENT_PACKAGE_VERSION,
        "asset_version": workflow_cli.CURRENT_ASSET_VERSION,
        "schema_version": workflow_cli.CURRENT_SCHEMA_VERSION,
        "applied_migrations": [],
    }
    payload.update(overrides)
    return payload


def facts(value: workflow_cli.OperationalStatusValue) -> dict[str, object]:
    return {fact.key: fact.value for fact in value.facts}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def init_git(root: Path) -> None:
    git(root, "init", "-b", "main")
    git(root, "config", "user.email", "status-tests@example.com")
    git(root, "config", "user.name", "Status Tests")
    (root / "README.md").write_text("fixture\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-m", "fixture")


def non_git_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(path for path in root.rglob("*") if path.is_file()):
        if ".git" in path.relative_to(root).parts:
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def write_global_tracker(root: Path, rows: list[str]) -> None:
    workflow_dir = root / ".project-workflow"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "TRACKER.md").write_text(
        GLOBAL_HEADER + "".join(f"{row}\n" for row in rows),
        encoding="utf-8",
    )


def write_epic_tracker(root: Path, folder: str, rows: list[str]) -> Path:
    epic_dir = root / ".project-workflow" / "tasks" / folder
    epic_dir.mkdir(parents=True, exist_ok=True)
    (epic_dir / "TRACKER.md").write_text(
        EPIC_HEADER + "".join(f"{row}\n" for row in rows),
        encoding="utf-8",
    )
    return epic_dir


def write_legacy_epic_tracker(root: Path, folder: str, rows: list[str]) -> Path:
    epic_dir = root / ".project-workflow" / "tasks" / folder
    epic_dir.mkdir(parents=True, exist_ok=True)
    (epic_dir / "TRACKER.md").write_text(
        LEGACY_EPIC_HEADER + "".join(f"{row}\n" for row in rows),
        encoding="utf-8",
    )
    return epic_dir


def test_installation_inspection_covers_every_compatibility_state(tmp_path: Path) -> None:
    fixtures: list[tuple[str, str, str]] = []

    current = tmp_path / "current"
    write_manifest(current, current_manifest(applied_migrations=["PW-0001-legacy-manifest"]))
    fixtures.append(("current", "current", "versions-current"))

    upgradeable = tmp_path / "upgradeable"
    write_manifest(upgradeable, current_manifest(schema_version=0))
    fixtures.append(("upgradeable", "upgradeable", "schema-behind"))

    legacy = tmp_path / "legacy"
    write_global_tracker(legacy, [])
    fixtures.append(("legacy", "legacy-unversioned", "manifest-absent"))

    future = tmp_path / "future"
    write_manifest(future, current_manifest(schema_version=workflow_cli.CURRENT_SCHEMA_VERSION + 1))
    fixtures.append(("future", "unsupported-future", "future-schema-version"))

    invalid = tmp_path / "invalid"
    (invalid / ".project-workflow").mkdir(parents=True)
    (invalid / ".project-workflow" / "manifest.json").write_text("{bad", encoding="utf-8")
    fixtures.append(("invalid", "invalid", "invalid-manifest-json"))

    uninitialized = tmp_path / "uninitialized"
    uninitialized.mkdir()
    fixtures.append(("uninitialized", "not-initialized", "workflow-installation-absent"))

    for folder, expected_state, expected_reason in fixtures:
        root = tmp_path / folder
        before = non_git_tree_hash(root)
        inspected = workflow_cli._inspect_operational_installation(root)
        after = non_git_tree_hash(root)
        inspected_facts = facts(inspected)

        assert inspected.state == expected_state
        assert inspected_facts["compatibility_reason"] == expected_reason
        assert inspected_facts["helper_package_version"] == workflow_cli.CURRENT_PACKAGE_VERSION
        assert inspected_facts["helper_asset_version"] == workflow_cli.CURRENT_ASSET_VERSION
        assert inspected_facts["helper_schema_version"] == workflow_cli.CURRENT_SCHEMA_VERSION
        assert before == after

    assert facts(workflow_cli._inspect_operational_installation(current)) == {
        "compatibility_reason": "versions-current",
        "helper_package_version": workflow_cli.CURRENT_PACKAGE_VERSION,
        "helper_asset_version": workflow_cli.CURRENT_ASSET_VERSION,
        "helper_schema_version": workflow_cli.CURRENT_SCHEMA_VERSION,
        "manifest_present": True,
        "manifest_parsed": True,
        "manifest_version": workflow_cli.CURRENT_MANIFEST_VERSION,
        "package_version": workflow_cli.CURRENT_PACKAGE_VERSION,
        "asset_version": workflow_cli.CURRENT_ASSET_VERSION,
        "schema_version": workflow_cli.CURRENT_SCHEMA_VERSION,
        "applied_migrations": ("PW-0001-legacy-manifest",),
    }
    assert facts(workflow_cli._inspect_operational_installation(upgradeable))["upgrade_command"] == (
        workflow_cli.CANONICAL_UPGRADE_COMMAND
    )
    assert facts(workflow_cli._inspect_operational_installation(invalid))["manifest_present"] is True
    assert facts(workflow_cli._inspect_operational_installation(invalid))["manifest_parsed"] is False


def test_git_inspection_reports_clean_dirty_detached_and_read_only_commands(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    init_git(root)
    original_run_git = workflow_cli._run_git
    calls: list[tuple[str, ...]] = []

    def recording_run_git(args: list[str], cwd: Path) -> str:
        calls.append(tuple(args))
        return original_run_git(args, cwd)

    monkeypatch.setattr(workflow_cli, "_run_git", recording_run_git)
    before_head = git(root, "rev-parse", "HEAD")
    before_status = git(root, "status", "--porcelain")
    clean, clean_findings = workflow_cli._inspect_operational_git(root)

    assert clean.state == "clean"
    assert clean_findings == ()
    assert facts(clean) == {
        "available": True,
        "top_level": str(root.resolve()),
        "branch": "main",
        "detached": False,
        "head": before_head,
        "upstream": None,
        "clean": True,
    }
    assert set(calls) == {
        ("rev-parse", "--show-toplevel"),
        ("symbolic-ref", "--quiet", "--short", "HEAD"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"),
        ("status", "--porcelain"),
    }
    assert git(root, "rev-parse", "HEAD") == before_head
    assert git(root, "status", "--porcelain") == before_status

    (root / "README.md").write_text("dirty\n", encoding="utf-8")
    dirty, _dirty_findings = workflow_cli._inspect_operational_git(root)
    assert dirty.state == "dirty"
    assert facts(dirty)["clean"] is False

    git(root, "restore", "README.md")
    git(root, "checkout", "--detach")
    detached, _detached_findings = workflow_cli._inspect_operational_git(root)
    assert detached.state == "detached"
    assert facts(detached)["branch"] is None
    assert facts(detached)["detached"] is True


def test_git_inspection_handles_non_repository_and_missing_git(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "plain"
    root.mkdir()
    unavailable, findings = workflow_cli._inspect_operational_git(root)
    assert unavailable.state == "unavailable"
    assert facts(unavailable) == {"available": False}
    assert [finding.code for finding in findings] == ["PW_STATUS_GIT_UNAVAILABLE"]

    def missing_git(_args: list[str], cwd: Path) -> str:
        del cwd
        raise FileNotFoundError("git")

    monkeypatch.setattr(workflow_cli, "_run_git", missing_git)
    missing, missing_findings = workflow_cli._inspect_operational_git(root)
    assert missing.state == "unavailable"
    assert [finding.code for finding in missing_findings] == ["PW_STATUS_GIT_UNAVAILABLE"]


def test_active_work_inspection_preserves_order_and_lifecycle_meaning(tmp_path: Path) -> None:
    write_global_tracker(
        tmp_path,
        [
            "| TASK-001 | Finished task | Complete | `tasks/TASK-001/IMPLEMENTATION.md` |",
            "| TASK-002 | Ready task | Ready | `tasks/TASK-002/IMPLEMENTATION.md` |",
            "| WF-001 | Namespaced task | Analysing | `tasks/WF-001/IMPLEMENTATION.md` |",
            "| FIX-002 | Blocked fix | Blocked | `tasks/FIX-002/FIX.md` |",
            "| EPIC-001 | Active epic | In Progress | `tasks/EPIC-001/REQUIREMENTS.md` |",
            "| EPIC-002 | Closed epic | Complete | `tasks/EPIC-002/REQUIREMENTS.md` |",
        ],
    )
    write_epic_tracker(
        tmp_path,
        "EPIC-001-Active-Epic",
        [
            "| TASK-010 | Proposed child | Proposed | Task | AC1 |  |  | planned |",
            "| TASK-011 | Approved child | Approved | Task | AC1 |  |  | approved |",
            "| TASK-012 | Active child | In Progress | Task | AC1 | tasks/EPIC-001/TASK-012/IMPLEMENTATION.md |  | active |",
            "| TASK-013 | Finished child | Complete | Task | AC1 | tasks/EPIC-001/TASK-013/IMPLEMENTATION.md |  | done |",
        ],
    )
    write_legacy_epic_tracker(
        tmp_path,
        "EPIC-002-Closed-Epic",
        [
            "| TASK-020 | Contradictory child | In Progress | Task | tasks/EPIC-002/TASK-020/IMPLEMENTATION.md |  | active |",
        ],
    )

    active_work, findings = workflow_cli._inspect_operational_active_work(tmp_path)

    assert [item.item_id for item in active_work] == [
        "TASK-002",
        "WF-001",
        "FIX-002",
        "EPIC-001",
        "TASK-010",
        "TASK-011",
        "TASK-012",
    ]
    assert [item.kind for item in active_work] == [
        "task",
        "task",
        "fix",
        "epic",
        "epic-child",
        "epic-child",
        "epic-child",
    ]
    assert active_work[0].lifecycle == "Ready"
    assert active_work[0].operational_meaning == "Approved work is ready for implementation."
    assert active_work[-1].sources[0].detail == "owner EPIC-001"
    assert [finding.code for finding in findings] == [
        "PW_STATUS_CLOSED_EPIC_HAS_ACTIVE_CHILD"
    ]


def test_lifecycle_meaning_covers_every_supported_status() -> None:
    assert dict(workflow_cli.OPERATIONAL_STATUS_GLOBAL_LIFECYCLE_MEANINGS).keys() == set(
        workflow_cli.TRACKER_STATUSES
    )
    assert dict(workflow_cli.OPERATIONAL_STATUS_EPIC_CHILD_LIFECYCLE_MEANINGS).keys() == set(
        workflow_cli.EPIC_TRACKER_STATUSES
    )
    for lifecycle in workflow_cli.TRACKER_STATUSES:
        assert workflow_cli._operational_status_lifecycle_meaning("task", lifecycle)
    for lifecycle in workflow_cli.EPIC_TRACKER_STATUSES:
        assert workflow_cli._operational_status_lifecycle_meaning("epic-child", lifecycle)


def test_active_work_inspection_retains_partial_state_with_structural_findings(
    tmp_path: Path,
) -> None:
    write_global_tracker(
        tmp_path,
        [
            "| TASK-100 | First duplicate | Ready | `tasks/TASK-100/IMPLEMENTATION.md` |",
            "| TASK-100 | Second duplicate | In Progress | `tasks/TASK-100/IMPLEMENTATION.md` |",
            "| EPIC-001 | First owner | In Progress | `tasks/EPIC-001/REQUIREMENTS.md` |",
            "| EPIC-002 | Second owner | In Progress | `tasks/EPIC-002/REQUIREMENTS.md` |",
            "| EPIC-003 | Missing tracker | In Progress | `tasks/EPIC-003/REQUIREMENTS.md` |",
            "| malformed | row |",
        ],
    )
    shared_child = (
        "| TASK-999 | Shared child | In Progress | Task | AC1 |  |  | conflicting owner |"
    )
    write_epic_tracker(tmp_path, "EPIC-001-First-Owner", [shared_child])
    write_epic_tracker(tmp_path, "EPIC-002-Second-Owner", [shared_child])

    active_work, findings = workflow_cli._inspect_operational_active_work(tmp_path)
    codes = [finding.code for finding in findings]

    assert [item.item_id for item in active_work] == [
        "TASK-100",
        "TASK-100",
        "EPIC-001",
        "EPIC-002",
        "EPIC-003",
        "TASK-999",
        "TASK-999",
    ]
    assert "PW_TRACKER_INVALID" in codes
    assert "PW_STATUS_DUPLICATE_WORK_ITEM" in codes
    assert "PW_STATUS_MULTIPLE_EPIC_OWNERS" in codes
    assert "PW_STATUS_REQUIRED_DOCS_MISSING" in codes
    assert "PW_STATUS_EPIC_TRACKER_MISSING" in codes


def test_repository_inspection_is_non_mutating_and_serializable(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    write_manifest(root, current_manifest())
    write_global_tracker(
        root,
        ["| TASK-001 | Ready task | Ready | `tasks/TASK-001/IMPLEMENTATION.md` |"],
    )
    init_git(root)
    before_tree = non_git_tree_hash(root)
    before_head = git(root, "rev-parse", "HEAD")
    before_status = git(root, "status", "--porcelain")

    inspection = workflow_cli.inspect_operational_status_repository(root)
    payload = workflow_cli.operational_status_inspection_payload(inspection)

    assert payload["installation"]["state"] == "current"  # type: ignore[index]
    assert payload["git"]["state"] == "clean"  # type: ignore[index]
    assert [item["id"] for item in payload["active_work"]] == ["TASK-001"]  # type: ignore[index]
    assert before_tree == non_git_tree_hash(root)
    assert before_head == git(root, "rev-parse", "HEAD")
    assert before_status == git(root, "status", "--porcelain")
