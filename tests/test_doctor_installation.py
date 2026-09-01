from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli
from tests.workflow_test_support import (
    REPO_ROOT,
    add_accepted_doctor_warnings,
    commit_git_fixture,
    find_uvx_executable,
    init_git_fixture,
    ready_implementation,
    ready_requirements,
    run_project,
    write_unique_id_config,
)


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
    assert "uvx --from project-workflow==0.10.0 project init" in codex_agents
    assert "To initialize a new repository" in codex_agents
    assert "project upgrade" in codex_agents
    assert "Do not run init first" in codex_agents
    assert "workflow doctor" in codex_agents
    assert ".project-workflow/BACKLOG.md" in codex_agents
    assert "Promoted rows stay in the backlog" in codex_agents
    assert "task status" in codex_agents
    assert "task approve-requirements" in codex_agents
    assert "epic approve-requirements" in codex_agents
    assert "task approval-summary" in codex_agents
    assert "plain-language Intent" in codex_agents
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
    qa_skill = (codex_root / ".agents" / "skills" / "project-qa-review" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Do not ask the user to manually test behavior" in qa_skill
    assert "separate verified evidence from deferred setup" in qa_skill
    assert "EVIDENCE.json" in qa_skill
    assert "visual/reference fidelity" in qa_skill
    assert ".project-workflow/guidance.md" in (
        codex_root / ".agents" / "skills" / "project-implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    backlog_skill = (codex_root / ".agents" / "skills" / "project-backlog" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Promoted rows stay in the backlog" in backlog_skill
    assert "Existing roadmap/backlog documents" in backlog_skill
    requirements_skill = (
        codex_root / ".agents" / "skills" / "project-requirements" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Does this Intent" in requirements_skill
    assert "accurately capture what you want and what success means?" in requirements_skill
    assert "Do not replace that question" in requirements_skill

    cursor_root = tmp_path / "cursor"
    cursor_root.mkdir()
    cursor_init = run_project(["init", "--agent", "cursor"], cwd=cursor_root)
    assert cursor_init.returncode == 0, cursor_init.stderr
    cursor_rules = (cursor_root / ".cursor" / "rules" / "project-workflow.mdc").read_text(
        encoding="utf-8"
    )
    assert "workflow doctor" in cursor_rules
    assert "task status" in cursor_rules
    assert "owner-directed and agent-operated" in cursor_rules
    assert "task ready" in cursor_rules
    assert ".project-workflow/BACKLOG.md" in cursor_rules
    assert "Existing roadmap/backlog documents" in cursor_rules
    assert "task approve-requirements" in cursor_rules
    assert "epic approve-requirements" in cursor_rules
    assert "task approval-summary" in cursor_rules
    assert "one- or two-sentence Intent" in cursor_rules
    assert "EPIC-CONTRACT.md" in cursor_rules
    assert "DECOMPOSITION.md" in cursor_rules
    assert "EVIDENCE.json" in cursor_rules
    assert "one lightweight Fix" in cursor_rules
    assert (cursor_root / ".cursor" / "agents" / "project-fix.md").exists()
    assert (cursor_root / ".cursor" / "agents" / "project-backlog.md").exists()
    assert "workflow doctor" in (
        cursor_root / ".cursor" / "agents" / "project-implement.md"
    ).read_text(encoding="utf-8")

    claude_root = tmp_path / "claude"
    claude_root.mkdir()
    claude_init = run_project(["init", "--agent", "claude-code"], cwd=claude_root)
    assert claude_init.returncode == 0, claude_init.stderr
    assert (claude_root / ".claude" / "agents" / "project-backlog.md").exists()
    assert (claude_root / ".claude" / "agents" / "project-fix.md").exists()
    claude_implement = (claude_root / ".claude" / "agents" / "project-implement.md").read_text(
        encoding="utf-8"
    )
    assert "task approve-requirements" in claude_implement
    assert "approved envelope" in claude_implement
    assert "EVIDENCE.json" in claude_implement
    claude_requirements = (
        claude_root / ".claude" / "agents" / "project-requirements.md"
    ).read_text(encoding="utf-8")
    assert "task approval-summary" in claude_requirements
    assert "Do not ask the owner to approve task IDs" in claude_requirements

    copilot_root = tmp_path / "copilot"
    copilot_root.mkdir()
    copilot_init = run_project(["init", "--agent", "github-copilot"], cwd=copilot_root)
    assert copilot_init.returncode == 0, copilot_init.stderr
    copilot_requirements = (
        copilot_root / ".github" / "prompts" / "Requirements.prompt.md"
    ).read_text(encoding="utf-8")
    assert "task approval-summary" in copilot_requirements
    assert "Do not ask the owner to approve task IDs" in copilot_requirements


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

    refreshed = run_project(["upgrade", "--agent", "github-copilot", "--yes"], cwd=tmp_path)
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
        "Document the `<!-- project-workflow:start -->` / `<!-- project-workflow:end -->` markers"
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


def test_doctor_detects_installed_codex_delegate_skill_drift(tmp_path: Path) -> None:
    init = run_project(["init", "--agent", "codex"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    packaged_skill = tmp_path / "src/project_workflow/codex/skills/project-delegate/SKILL.md"
    packaged_skill.parent.mkdir(parents=True)
    shutil.copy2(
        REPO_ROOT / "src/project_workflow/codex/skills/project-delegate/SKILL.md",
        packaged_skill,
    )
    installed_skill = tmp_path / ".agents/skills/project-delegate/SKILL.md"
    installed_skill.write_text(
        installed_skill.read_text(encoding="utf-8") + "\nSemantic drift.\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)

    assert doctor.returncode != 0
    assert "Installed Codex Delegate skill differs from packaged source" in doctor.stdout


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
        "## User Story\n\nAs a maintainer, I have historical workflow state.\n\n",
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
    tracker_text += (
        "| WF-003 | Workflow Task | To Do | `tasks/WF-003-Workflow-Task/IMPLEMENTATION.md` |\n"
    )
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
