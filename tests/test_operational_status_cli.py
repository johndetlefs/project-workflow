from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from project_workflow import cli as workflow_cli

PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]


def run_project(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*PROJECT_CMD, *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(path for path in root.rglob("*") if path.is_file()):
        if ".git" in path.relative_to(root).parts:
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def init_repository(root: Path) -> None:
    result = run_project(["init", "--agent", "codex"], root)
    assert result.returncode == 0, result.stdout + result.stderr


def run_local_helper(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(cwd / ".project-workflow" / "cli" / "workflow"), *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def test_status_parser_help_exposes_narrow_read_only_surface(tmp_path: Path) -> None:
    top_level = run_project(["--help"], tmp_path)
    status_help = run_project(["status", "--help"], tmp_path)

    assert top_level.returncode == 0
    assert "status" in top_level.stdout
    assert status_help.returncode == 0
    assert "--root" in status_help.stdout
    assert "--id" in status_help.stdout
    assert "--strict" in status_help.stdout
    assert "--format {human,json}" in status_help.stdout


def test_uninitialized_json_is_truthful_actionable_and_non_mutating(tmp_path: Path) -> None:
    before = tree_hash(tmp_path)

    result = run_project(["status", "--format", "json"], tmp_path)
    after = tree_hash(tmp_path)
    payload = json.loads(result.stdout)

    assert result.returncode == 0, result.stderr
    assert payload["schema_version"] == workflow_cli.OPERATIONAL_STATUS_SCHEMA_VERSION
    assert payload["installation"]["state"] == "not-initialized"
    assert payload["git"]["state"] == "unavailable"
    assert payload["health"]["state"] == "fail"
    assert payload["primary_action"] == {
        "code": "PW_STATUS_INIT_REQUIRED",
        "title": "Initialize project-workflow",
        "responsible_party": "agent",
        "reason": "Repository is not initialized with project-workflow.",
        "command": workflow_cli.CANONICAL_INIT_COMMAND,
        "request": None,
        "sources": [
            {
                "kind": "repository-compatibility",
                "artifact": ".project-workflow",
                "detail": "workflow-installation-absent",
            }
        ],
    }
    assert before == after


def test_initialized_human_and_json_share_one_deterministic_snapshot(
    tmp_path: Path,
) -> None:
    init_repository(tmp_path)
    before = tree_hash(tmp_path)

    first_json = run_project(["status", "--format", "json"], tmp_path)
    second_json = run_project(["status", "--format", "json"], tmp_path)
    human = run_project(["status"], tmp_path)

    assert first_json.returncode == second_json.returncode == human.returncode == 0
    assert first_json.stdout == second_json.stdout
    payload = json.loads(first_json.stdout)
    assert payload == workflow_cli.operational_status_payload(
        workflow_cli.build_operational_status_snapshot(tmp_path)
    )
    assert payload["installation"]["state"] == "current"
    assert payload["git"]["state"] == "unavailable"
    assert payload["health"]["state"] == "pass"
    assert payload["active_work"] == []
    assert payload["primary_action"]["code"] == "PW_STATUS_NO_ACTION"
    assert human.stdout.startswith("Next action\n- [PW_STATUS_NO_ACTION]")
    for heading in (
        "Status",
        "Active work",
        "Findings",
        "Secondary actions",
        "Sources",
    ):
        assert f"\n{heading}\n" in human.stdout
    assert "accepted warnings: 0" in human.stdout
    assert tree_hash(tmp_path) == before


def test_active_and_missing_focus_are_consistent_across_json_and_human(
    tmp_path: Path,
) -> None:
    init_repository(tmp_path)
    created = run_project(
        ["task", "init", "--title", "Focused Status", "--update-tracker"],
        tmp_path,
    )
    assert created.returncode == 0, created.stdout + created.stderr
    before = tree_hash(tmp_path)

    focused_json = run_project(["status", "--id", "TASK-001", "--format", "json"], tmp_path)
    focused_human = run_project(["status", "--id", "TASK-001"], tmp_path)
    missing = run_project(["status", "--id", "TASK-999", "--format", "json"], tmp_path)

    focused_payload = json.loads(focused_json.stdout)
    missing_payload = json.loads(missing.stdout)
    assert focused_json.returncode == focused_human.returncode == missing.returncode == 0
    assert [entry["id"] for entry in focused_payload["active_work"]] == ["TASK-001"]
    assert focused_payload["primary_action"]["code"] == ("PW_STATUS_REQUIREMENTS_APPROVAL_REQUIRED")
    assert focused_payload["primary_action"]["code"] in focused_human.stdout
    assert missing_payload["active_work"] == []
    assert missing_payload["primary_action"]["code"] == "PW_STATUS_FOCUS_NOT_FOUND"
    assert tree_hash(tmp_path) == before


def test_strict_mode_uses_same_snapshot_schema_and_marks_visible_warnings_blocking(
    tmp_path: Path,
) -> None:
    init_repository(tmp_path)
    created = run_project(["task", "init", "--title", "Strict Draft", "--update-tracker"], tmp_path)
    assert created.returncode == 0
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(" | To Do | ", " | Complete | "),
        encoding="utf-8",
    )

    normal = json.loads(run_project(["status", "--format", "json"], tmp_path).stdout)
    strict = json.loads(run_project(["status", "--strict", "--format", "json"], tmp_path).stdout)

    assert list(normal) == list(strict)
    assert normal["health"]["facts"][0] == {"key": "strict", "value": False}
    assert strict["health"]["facts"][0] == {"key": "strict", "value": True}
    assert normal["health"]["state"] == "warning"
    assert strict["health"]["state"] == "fail"
    assert strict["blockers"]
    assert normal["primary_action"]["code"] == "PW_STATUS_NO_ACTION"
    assert strict["primary_action"]["code"] == "PW_STATUS_REPAIR_BLOCKER"


def test_root_option_inspects_target_without_changing_calling_directory(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    caller = tmp_path / "caller"
    repository.mkdir()
    caller.mkdir()
    init_repository(repository)
    before_caller = tree_hash(caller)
    before_repository = tree_hash(repository)

    result = run_project(["status", "--root", str(repository), "--format", "json"], caller)
    payload = json.loads(result.stdout)

    assert result.returncode == 0
    assert payload["root"] == str(repository.resolve())
    assert payload["installation"]["state"] == "current"
    assert tree_hash(caller) == before_caller
    assert tree_hash(repository) == before_repository


def test_disposable_git_journey_uses_local_helper_without_mutation(tmp_path: Path) -> None:
    init_repository(tmp_path)
    for args in (
        ["init", "-b", "main"],
        ["config", "user.email", "status-journey@example.com"],
        ["config", "user.name", "Status Journey"],
        ["add", "."],
        ["commit", "-m", "initialized workflow"],
    ):
        completed = subprocess.run(
            ["git", *args],
            cwd=tmp_path,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr
    created = run_project(["task", "init", "--title", "Journey Task", "--update-tracker"], tmp_path)
    assert created.returncode == 0
    head_before = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status_before = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    tree_before = tree_hash(tmp_path)

    human = run_local_helper(["status", "--id", "TASK-001"], tmp_path)
    machine = run_local_helper(["status", "--id", "TASK-001", "--format", "json"], tmp_path)
    payload = json.loads(machine.stdout)

    assert human.returncode == machine.returncode == 0
    assert human.stdout.startswith("Next action\n- [PW_STATUS_REQUIREMENTS_APPROVAL_REQUIRED]")
    assert payload["git"]["state"] == "dirty"
    assert payload["active_work"][0]["id"] == "TASK-001"
    assert payload["proof"]["state"] == "declared"
    assert payload["delivery"]["state"] == "not-recorded"
    assert payload["primary_action"]["responsible_party"] == "owner"
    assert payload["primary_action"]["sources"][0]["kind"] == "requirements"
    assert tree_hash(tmp_path) == tree_before
    assert (
        subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        == head_before
    )
    assert (
        subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        == status_before
    )


def test_readme_and_generated_agent_guidance_teach_status_boundaries() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    usage = (root / "docs/using-project-workflow.md").read_text(encoding="utf-8")
    codex_guidance = (root / "src/project_workflow/codex/AGENTS.md").read_text(encoding="utf-8")
    cursor_guidance = (root / "src/project_workflow/cursor/rules/project-workflow.mdc").read_text(
        encoding="utf-8"
    )
    managed = workflow_cli._managed_project_workflow_block()

    for text in (codex_guidance, cursor_guidance, managed, usage):
        assert "workflow status" in text
        assert "--id <WORK-ID>" in text
        assert "--strict" in text
        assert "--format json" in text
        assert "Doctor" in text
        assert "upgrade" in text
        assert "QA" in text
    assert "never executes its recommended action" in managed
    assert "separate evidence layers" in readme
    assert "[Using Project Workflow](docs/using-project-workflow.md)" in readme
