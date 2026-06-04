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
    assert "workflow doctor" in (
        codex_root / ".agents" / "skills" / "project-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
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
    instructions_text = instructions.read_text(encoding="utf-8")
    assert "# Local Copilot Notes" in instructions_text
    assert "old managed block" not in instructions_text
    assert ".project-workflow/guidance.md" in instructions_text


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
