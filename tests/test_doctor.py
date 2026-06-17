from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]


def run_project(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*PROJECT_CMD, *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def test_doctor_passes_for_clean_initialized_repo(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    assert ".project-workflow/guidance.md" in init.stdout
    assert (tmp_path / ".project-workflow" / "guidance.md").exists()
    assert "<!-- project-workflow:start -->" in (
        tmp_path / ".github" / "copilot-instructions.md"
    ).read_text(encoding="utf-8")
    assert "project-workflow:generated" in (
        tmp_path / ".github" / "prompts" / "Task.prompt.md"
    ).read_text(encoding="utf-8")

    second_init = run_project(["init"], cwd=tmp_path)
    assert second_init.returncode == 0, second_init.stderr
    assert not list(tmp_path.rglob("*.new*"))

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "no issues found" in doctor.stdout

    validate = run_project(["validate"], cwd=tmp_path)
    assert validate.returncode == 0, validate.stdout + validate.stderr


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


def test_task_status_updates_packaged_and_local_workflow(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Lifecycle Status", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr

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
            "Plan Confirmed",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert local_status.returncode == 0, local_status.stdout + local_status.stderr
    assert "Updated TASK-001: Analysing -> Plan Confirmed" in local_status.stdout

    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-001 | Lifecycle Status | Plan Confirmed |" in tracker_text


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


def test_agent_mode_init_installs_doctor_guidance(tmp_path: Path) -> None:
    codex_root = tmp_path / "codex"
    codex_root.mkdir()
    (codex_root / "AGENTS.md").write_text("# Existing Agent Notes\n\nKeep this.\n", encoding="utf-8")
    codex_init = run_project(["init", "--agent", "codex"], cwd=codex_root)
    assert codex_init.returncode == 0, codex_init.stderr
    codex_agents = (codex_root / "AGENTS.md").read_text(encoding="utf-8")
    assert "# Existing Agent Notes" in codex_agents
    assert "<!-- project-workflow:start -->" in codex_agents
    assert "workflow doctor" in codex_agents
    assert "task status" in codex_agents
    assert "workflow doctor" in (
        codex_root / ".agents" / "skills" / "project-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "task status" in (
        codex_root / ".agents" / "skills" / "project-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    qa_skill = (
        codex_root / ".agents" / "skills" / "project-qa-review" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Do not ask the user to manually test behavior" in qa_skill
    assert "separate verified evidence from deferred setup" in qa_skill
    assert ".project-workflow/guidance.md" in (
        codex_root / ".agents" / "skills" / "project-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")

    cursor_root = tmp_path / "cursor"
    cursor_root.mkdir()
    cursor_init = run_project(["init", "--agent", "cursor"], cwd=cursor_root)
    assert cursor_init.returncode == 0, cursor_init.stderr
    assert "workflow doctor" in (
        cursor_root / ".cursor" / "rules" / "project-workflow.mdc"
    ).read_text(encoding="utf-8")
    assert "task status" in (
        cursor_root / ".cursor" / "rules" / "project-workflow.mdc"
    ).read_text(encoding="utf-8")
    assert "workflow doctor" in (
        cursor_root / ".cursor" / "agents" / "project-implement.md"
    ).read_text(encoding="utf-8")


def test_init_refreshes_marked_generated_files_and_managed_blocks(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    local_workflow = tmp_path / ".project-workflow" / "cli" / "workflow.py"
    local_workflow.write_text("# project-workflow:generated\n# old generated workflow helper\n", encoding="utf-8")
    instructions = tmp_path / ".github" / "copilot-instructions.md"
    instructions.write_text(
        "# Local Copilot Notes\n\n"
        "<!-- project-workflow:start -->\n"
        "old managed block\n"
        "<!-- project-workflow:end -->\n",
        encoding="utf-8",
    )

    refreshed = run_project(["init"], cwd=tmp_path)
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

    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Mapped Epic\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: First epic outcome is delivered.\n"
        "- AC2: Second epic outcome is delivered.\n",
        encoding="utf-8",
    )

    decompose = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-001", "--limit", "2"],
        cwd=tmp_path,
    )
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr
    assert "Parent AC coverage mapped: AC1, AC2" in decompose.stdout

    epic_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-001 | First epic outcome is delivered | Proposed | Task | AC1 |" in epic_tracker
    assert "| TASK-002 | Second epic outcome is delivered | Proposed | Task | AC2 |" in epic_tracker
    assert "Covers AC1; Generated from REQUIREMENTS.md" in epic_tracker
    assert "Covers AC2; Generated from REQUIREMENTS.md" in epic_tracker


def test_epic_decompose_reports_unmapped_parent_ac_ids(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Coverage Gap"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Coverage Gap\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: First epic outcome is delivered.\n"
        "- AC2: Second epic outcome is delivered.\n"
        "- AC3: Third epic outcome is delivered.\n",
        encoding="utf-8",
    )

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
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Child Evidence | Approved | Task | AC1, AC3 |  |  | Covers AC1, AC3 |\n",
        encoding="utf-8",
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
    assert "## Parent AC Evidence" in implementation_text
    assert "AC1 / parent AC(s) AC1, AC3" in implementation_text

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
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Closeout Ready\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: First parent outcome is delivered.\n",
        encoding="utf-8",
    )
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

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "Epic acceptance audit passed." in audit.stdout
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "| AC1 | First parent outcome is delivered. | TASK-001 (Complete) |" in audit_text
    assert "TASK-001: parent AC evidence recorded; TASK-001: QA pass" in audit_text

    validate_only = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert validate_only.returncode == 0, validate_only.stdout + validate_only.stderr
    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| EPIC-001 | Closeout Ready | To Do |" in tracker_text

    completed = run_project(
        ["epic", "closeout", "--epic-id", "EPIC-001", "--complete"],
        cwd=tmp_path,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| EPIC-001 | Closeout Ready | Complete |" in tracker_text

    doctor = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "EPIC-001 is Complete but lacks non-placeholder QA/code-review evidence" not in doctor.stdout


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
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Deferred Epic\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: Deferred parent outcome is explicitly tracked.\n",
        encoding="utf-8",
    )
    (epic_dir / "DEFERRALS.md").write_text(
        "# Deferrals\n\n"
        "| Parent AC | Status | Owner | Decision Date | Reason | Follow-up | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
        "| AC1 | Approved | Product Owner | 2026-06-17 | Deferred from MVP | EPIC-002 | Owner approved follow-up |\n",
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
    child_dir = epic_dir / "TASK-001-Status-Child"
    child_dir.mkdir()
    child_impl = child_dir / "IMPLEMENTATION.md"
    child_impl.write_text(
        "## User Story\n\n"
        "As a maintainer, I want status gates.\n\n"
        "## Parent AC Evidence\n\n"
        "- AC1: Pending implementation evidence.\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Local validation passed.\n"
        "- Findings: None.\n",
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Status Child | In Progress | Task | AC1 | tasks/EPIC-001-Epic-Status/TASK-001-Status-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
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
