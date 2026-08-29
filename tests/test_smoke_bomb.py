from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli
from tests.workflow_test_support import (
    _run_git_for_test,
    commit_git_fixture,
    init_git_fixture,
    run_project,
)


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


def test_smoke_bomb_plan_inventory_omits_ignored_private_delegate_runtime(
    tmp_path: Path,
) -> None:
    root = create_smoke_bomb_fixture(tmp_path, "codex")
    private_runtime = root / ".project-workflow/runtime/delegations/private-handle.json"
    private_runtime.parent.mkdir(parents=True)
    private_runtime.write_text(
        '{"handle":"private-task-id","credential":"must-not-ship"}\n',
        encoding="utf-8",
    )
    assert _run_git_for_test(
        root,
        ["check-ignore", ".project-workflow/runtime/delegations/private-handle.json"],
    )
    planned = run_project(
        [*smoke_bomb_args(root, tmp_path / "client.zip", "codex"), "--plan"],
        cwd=root,
    )
    assert planned.returncode != 0
    plan = json.loads(planned.stdout)
    assert "private-handle" not in planned.stdout
    assert "must-not-ship" not in planned.stdout
    assert "PW_SMOKE_BOMB_PRIVATE_RUNTIME_PRESENT" in {
        blocker["code"] for blocker in plan["blockers"]
    }
    assert not any("private-handle" in path for path in plan["archive"]["included_paths"])


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
        workflow_cli._smoke_bomb_remove_managed_block(short_user_content + managed).encode("utf-8")
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
