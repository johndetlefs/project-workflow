from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from project_workflow import cli as workflow_cli
from tests.workflow_test_support import (
    assert_unique_id,
    ready_fix_text,
    ready_implementation,
    ready_requirements,
    run_project,
    verified_fix_text,
    write_epic_contract,
    write_namespace_config,
    write_unique_id_config,
)


def test_doctor_passes_for_clean_initialized_repo(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    assert ".project-workflow/guidance.md" in init.stdout
    assert (tmp_path / ".project-workflow" / "guidance.md").exists()
    assert (tmp_path / ".project-workflow" / "config.json").exists()
    backlog_text = (tmp_path / ".project-workflow" / "BACKLOG.md").read_text(encoding="utf-8")
    assert (
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |" in backlog_text
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
    choices = iter("ABCDEFGHIJ")
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
    assert (
        "| TASK-001 | Export Ideas | To Do | `tasks/TASK-001-Export-Ideas/IMPLEMENTATION.md` |"
        in tracker_text
    )
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
    assert (tmp_path / ".project-workflow" / "config.json").read_text(
        encoding="utf-8"
    ) == custom_config

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
    (workflow_task_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")

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
    assert (
        "| WF-001 | Workflow Status | Analysing | `tasks/WF-001-Workflow-Status/IMPLEMENTATION.md` |"
        in tracker_text
    )
    assert (
        "| MCP-001 | Tool Contract | To Do | `tasks/MCP-001-Tool-Contract/IMPLEMENTATION.md` |"
        in tracker_text
    )


def test_task_status_force_cannot_bypass_incomplete_rows(tmp_path: Path) -> None:
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
    assert "every required implementation row is Done" in illegal.stderr

    missing_reason = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Testing", "--force"],
        cwd=tmp_path,
    )
    assert missing_reason.returncode != 0
    assert "--force requires --reason" in missing_reason.stderr

    forced_incomplete = run_project(
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
    assert forced_incomplete.returncode != 0
    assert "Ordinary --force cannot bypass this integrity gate" in forced_incomplete.stderr

    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    implementation_path = task_dir / "IMPLEMENTATION.md"
    implementation_path.write_text(
        implementation_path.read_text(encoding="utf-8").replace("| To Do |", "| Done |"),
        encoding="utf-8",
    )
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
    assert (
        "cannot move to Complete without non-placeholder QA/code-review evidence" in blocked.stderr
    )

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


def test_task_status_completes_resolved_changes_requested_without_second_qa(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    task = run_project(
        ["task", "init", "--title", "One QA Resolution", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-001", "One QA Resolution"), encoding="utf-8"
    )
    decision = workflow_cli._validation_impact_decision(
        classification="affected",
        proof_layers=("qa-review",),
        validation_verdict="pass",
    )
    impact = workflow_cli._validation_impact_section(
        baseline="Independent QA receipt QA-001",
        change_summary="Resolved the named finding.",
        decided_by="Coordinator",
        decision=decision,
    )
    qa = (
        "## QA & Code Review\n\n"
        "- Intent QA contract: adversarial\n"
        "- Verdict: Changes Requested\n"
        "- Intent adversarial verdict: Fail\n"
        "- Could every AC pass while the approved user job remains undone: Yes\n"
        "- Intent audit state: current\n"
        "- Outcome journey evidence: QA-001 inspected the normal user journey.\n"
        "- Reviewer independence: QA-001 was independent from implementation.\n"
        "- Evidence: QA-001 retained the original finding.\n"
        "- Findings: One blocking finding.\n"
        "- Findings disposition: Resolved\n"
        "- Affected validation verdict: Pass\n"
        "- Could every AC pass after affected validation while the approved user job remains undone: No\n"
        "- Affected validation evidence: The named regression and outcome journey pass.\n"
        "- Second QA commissioned: No\n\n"
    )
    implementation = ready_implementation().replace(
        "## QA & Code Review\n\n- Verdict: ____\n- Evidence: ____\n- Findings: ____\n\n",
        impact + "\n" + qa,
    )
    (task_dir / "IMPLEMENTATION.md").write_text(implementation, encoding="utf-8")

    for status in ("Analysing", "Plan Confirmed", "In Progress", "Testing", "Review"):
        moved = run_project(["task", "status", "--id", "TASK-001", "--to", status], cwd=tmp_path)
        assert moved.returncode == 0, moved.stdout + moved.stderr
    completed = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Complete"], cwd=tmp_path
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "Updated TASK-001: Review -> Complete" in completed.stdout


def test_task_status_validates_task_id_and_docs_path(tmp_path: Path) -> None:
    missing_tracker = run_project(
        ["task", "init", "--title", "Missing Tracker", "--update-tracker"],
        cwd=tmp_path,
    )
    assert missing_tracker.returncode != 0
    assert "uvx --from project-workflow==0.9.2 project init" in missing_tracker.stderr

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
    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
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
        moved = run_project(["fix", "status", "--id", "FIX-001", "--to", status], cwd=tmp_path)
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
        fix_path = (
            next((tmp_path / ".project-workflow" / "tasks").glob(f"FIX-{index:03d}-*")) / "FIX.md"
        )
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
        moved = run_project(["task", "status", "--id", "TASK-001", "--to", status], cwd=tmp_path)
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
        tmp_path / ".project-workflow" / "tasks" / "FIX-001-Delivered-Export-Regression" / "FIX.md"
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
    fix_path = (
        next((tmp_path / ".project-workflow" / "tasks").glob(f"{fix_id}-Related-Link-Parsing"))
        / "FIX.md"
    )

    missing_id = next(candidate for candidate in ("WF-ZZZZZ", "WF-YYYYY") if candidate != task_id)
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
    assert (
        f"related work reference '{missing_id}' is not in the local global tracker"
        in missing.stdout
    )
    assert "PROJECT-WORKFLOW" not in missing.stdout


def test_fix_hotfix_bypass_and_promotion(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr

    created = run_project(
        ["fix", "init", "--title", "Production Incident", "--mode", "Hotfix"],
        cwd=tmp_path,
    )
    assert created.returncode == 0, created.stdout + created.stderr
    fix_path = tmp_path / ".project-workflow" / "tasks" / "FIX-001-Production-Incident" / "FIX.md"
    bypass_blocked = run_project(
        ["fix", "status", "--id", "FIX-001", "--to", "In Progress"], cwd=tmp_path
    )
    assert bypass_blocked.returncode != 0
    fix_path.write_text(ready_fix_text(fix_path, hotfix=True), encoding="utf-8")
    bypass = run_project(["fix", "status", "--id", "FIX-001", "--to", "In Progress"], cwd=tmp_path)
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
        tmp_path / ".project-workflow" / "tasks" / "TASK-001-Expanded-Outcome" / "REQUIREMENTS.md"
    ).read_text(encoding="utf-8")
    assert "- Promoted from Fix: FIX-002" in promoted_requirements
    promoted_fix = (
        tmp_path / ".project-workflow" / "tasks" / "FIX-002-Expanded-Outcome" / "FIX.md"
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
    fix_path = tmp_path / ".project-workflow" / "tasks" / "FIX-001-Workspace-Regression" / "FIX.md"
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
        terminal_text = (
            next((tmp_path / ".project-workflow" / "tasks").glob(f"FIX-{index:03d}-*"))
            .joinpath("FIX.md")
            .read_text(encoding="utf-8")
        )
        assert "- Status: N/A" in terminal_text
        assert f"- Disposition: {disposition}" in terminal_text
