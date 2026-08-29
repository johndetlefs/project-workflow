from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]


def run_project(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*PROJECT_CMD, *args], cwd=root, check=False, capture_output=True, text=True
    )


def init_git(root: Path) -> None:
    for command in (
        ("git", "init", "-q"),
        ("git", "config", "user.email", "delegate-tests@example.invalid"),
        ("git", "config", "user.name", "Delegate Tests"),
        ("git", "add", "."),
        ("git", "commit", "-qm", "fixture"),
    ):
        completed = subprocess.run(command, cwd=root, check=False, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stdout + completed.stderr


def target() -> workflow_cli.DelegationTarget:
    return workflow_cli.DelegationTarget(
        target_id="TASK-001",
        kind="task",
        title="Host adapter contract",
        lifecycle="In Progress",
        source_path=".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",
        source_hash="abc123",
    )


def unit(unit_id: str, *, order: int = 0) -> workflow_cli.DelegationUnit:
    return workflow_cli.DelegationUnit(
        unit_id=unit_id,
        title=f"Unit {unit_id}",
        dependencies=(),
        write_scope=(f"src/{unit_id}",),
        parallel_safe=True,
        canonical_state="pending",
        source_order=order,
        source_path=".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",
    )


def test_tri_state_capabilities_are_truthful_and_capacity_is_runtime_bounded() -> None:
    fallback = workflow_cli.build_delegation_plan(
        target=target(),
        units=(unit("one"),),
        requested_concurrency=9,
        available_child_capacity=4,
        unsupported_capabilities=("subagent",),
        capability_source="2026-08-19 current host tool inspection",
    )
    states = {item.capability: (item.state, item.provenance) for item in fallback.capability_matrix}
    assert states["subagent"] == (
        "unsupported",
        "runtime-observed:2026-08-19 current host tool inspection",
    )
    assert states["persistent-task"] == ("unknown", "not observed")
    assert fallback.units[0].executor == "coordinator"
    assert fallback.effective_concurrency == 1

    verified = workflow_cli.build_delegation_plan(
        target=target(),
        units=(unit("one"), unit("two", order=1), unit("three", order=2)),
        requested_concurrency=9,
        available_child_capacity=2,
        observed_capabilities=("subagent",),
        capability_source="2026-08-19 current session subagent list",
    )
    assert verified.effective_concurrency == verified.effective_child_concurrency == 2
    assert {item.executor for item in verified.units} == {"subagent"}
    payload = workflow_cli.delegation_plan_payload(verified)
    assert payload["capabilities"]["matrix"][4] == {
        "capability": "subagent",
        "state": "verified",
        "provenance": "runtime-observed:2026-08-19 current session subagent list",
    }

    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        workflow_cli.build_delegation_plan(
            target=target(),
            units=(unit("one"),),
            observed_capabilities=("subagent",),
            unsupported_capabilities=("subagent",),
            capability_source="2026-08-19 current host inspection",
        )
    assert caught.value.code == "PW_DELEGATION_CAPABILITY_CONFLICT"


def test_delegate_source_and_development_assets_share_the_graph_contract() -> None:
    prompt = (REPO_ROOT / "src/project_workflow/prompts/Delegate.prompt.md").read_text()
    github = (REPO_ROOT / ".github/prompts/Delegate.prompt.md").read_text()
    skill = (REPO_ROOT / "src/project_workflow/codex/skills/project-delegate/SKILL.md").read_text()
    installed_skill = (REPO_ROOT / ".agents/skills/project-delegate/SKILL.md").read_text()

    assert prompt == github
    for text in (prompt, skill, installed_skill):
        lowered = text.lower()
        for required in (
            "task or epic",
            "verified",
            "unsupported",
            "unknown",
            "available child",
            "coordinator",
            "descendants",
            "unrelated",
            "independent qa",
            "dated",
            "bounded-return",
            "durable-resume",
            "direct-owner-steering",
            "isolated-worktree",
            "peer:<group-id>",
            "peer-team",
            "task-retirement",
            "task-retirement-reconciliation",
            "persistent-task-owner-steering",
            "visible-retirable",
            "archive-on-verified",
            "owner-promoted",
            "runtime-validated",
        ):
            assert required in lowered
        assert "workers:4" not in lowered
        assert "worker limit" not in lowered
        assert "on first work-item failure" not in lowered
        assert "enter fail-fast mode" not in lowered

    assert workflow_cli.GENERATED_MARKER in installed_skill
    assert "isolated-worktree creation for every persistent Codex child" in skill
    assert installed_skill == workflow_cli._with_generated_marker(
        REPO_ROOT / ".agents/skills/project-delegate/SKILL.md", skill
    )
    generated = (REPO_ROOT / "src/project_workflow/templates/workflow.py").read_bytes()
    assert generated == (REPO_ROOT / ".project-workflow/cli/workflow.py").read_bytes()
    assert b"# project-workflow:generated" in generated
    assert b"# source-manifest: scripts/runtime-modules.txt" in generated


def test_planner_assets_author_execution_needs_as_work_facts() -> None:
    prompt = (REPO_ROOT / "src/project_workflow/prompts/Planner.prompt.md").read_text()
    github = (REPO_ROOT / ".github/prompts/Planner.prompt.md").read_text()
    skill = (REPO_ROOT / "src/project_workflow/codex/skills/project-planner/SKILL.md").read_text()
    installed = (REPO_ROOT / ".agents/skills/project-planner/SKILL.md").read_text()
    assert prompt == github
    for text in (prompt, skill, installed):
        for required in (
            "Execution Needs",
            "bounded-return",
            "durable-resume",
            "direct-owner-steering",
            "isolated-worktree",
            "peer:<group-id>",
            "work facts",
        ):
            assert required in text
    assert installed == workflow_cli._with_generated_marker(
        REPO_ROOT / ".agents/skills/project-planner/SKILL.md", skill
    )


def test_managed_host_guidance_uses_property_selection_and_safe_retirement() -> None:
    codex_agents = (REPO_ROOT / "src/project_workflow/codex/AGENTS.md").read_text()
    cursor_rules = (
        REPO_ROOT / "src/project_workflow/cursor/rules/project-workflow.mdc"
    ).read_text()
    usage = (REPO_ROOT / "docs/using-project-workflow.md").read_text()

    for text in (codex_agents, cursor_rules, usage):
        lowered = " ".join(text.lower().split())
        assert "task-versus-epic" in lowered
        assert "durable-resume" in lowered
        assert "direct-owner-steering" in lowered
        assert "peer:<group-id>" in lowered
        assert "coordinator" in lowered
        assert "subagent" in lowered
        assert "persistent-task" in lowered
        assert "peer-team" in lowered
        assert "owner-promoted" in lowered
        assert (
            "never retire the coordinator" in lowered or "coordinator is never retired" in lowered
        )

    assert "Positive examples:" in usage
    assert "Negative examples:" in usage
    assert "archive-on-verified" in usage
    assert "not runtime-validated" in " ".join(usage.split())
    assert (
        "[Using Project Workflow](docs/using-project-workflow.md)"
        in (REPO_ROOT / "README.md").read_text()
    )


@pytest.mark.parametrize("agent", sorted(workflow_cli.AGENT_CHOICES))
def test_each_host_init_installs_native_truthful_delegate_asset(tmp_path: Path, agent: str) -> None:
    root = tmp_path / agent
    root.mkdir()
    initialized = run_project(root, "init", "--agent", agent)
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    init_git(root)

    ignored = subprocess.run(
        ("git", "check-ignore", "-q", ".project-workflow/runtime/delegations/private.json"),
        cwd=root,
        check=False,
    )
    assert ignored.returncode == 0
    assert "runtime/delegations/" in (root / ".project-workflow/.gitignore").read_text()

    if agent == "codex":
        delegate = (root / ".agents/skills/project-delegate/SKILL.md").read_text()
        assert "current Codex session" in delegate
        assert "current Codex task-archive capability" in delegate
        managed = (root / "AGENTS.md").read_text()
        assert "Task-versus-Epic kind" in managed
        assert "verified durable disposition" in managed
    elif agent == "github-copilot":
        delegate = (root / ".github/prompts/Delegate.prompt.md").read_text()
        assert "${input:targetId" in delegate
    else:
        host_dir = ".claude" if agent == "claude-code" else ".cursor"
        delegate = (root / host_dir / "agents/project-delegate.md").read_text()
        all_agents = "\n".join(
            path.read_text() for path in (root / host_dir / "agents").glob("*.md")
        )
        assert "${input:" not in all_agents
        assert "Invocation contract" in delegate
        expected_host = "Claude Code" if agent == "claude-code" else "Cursor"
        assert f"Invocation contract ({expected_host})" in delegate

    lowered = delegate.lower()
    assert "task or epic" in lowered
    assert all(state in lowered for state in ("verified", "unsupported", "unknown"))
    for required in (
        "bounded-return",
        "durable-resume",
        "direct-owner-steering",
        "peer:<group-id>",
        "peer-team",
        "visible-retirable",
        "archive-on-verified",
        "owner-promoted",
        "runtime-validated",
    ):
        assert required in lowered
    assert "worker limit" not in lowered
    assert "workers:4" not in lowered


def test_asset_v1_upgrade_preserves_user_delegate_collision_and_then_noops(
    tmp_path: Path,
) -> None:
    initialized = run_project(tmp_path, "init", "--agent", "codex")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    delegate = tmp_path / ".agents/skills/project-delegate/SKILL.md"
    delegate.write_text("# Owner Delegate Contract\n\nPreserve these bytes.\n")
    manifest = tmp_path / ".project-workflow/manifest.json"
    payload = json.loads(manifest.read_text())
    payload["asset_version"] = 1
    manifest.write_text(json.dumps(payload, indent=2) + "\n")
    init_git(tmp_path)

    planned = run_project(tmp_path, "upgrade", "--agent", "codex", "--plan", "--format", "json")
    assert planned.returncode == 0, planned.stdout + planned.stderr
    plan = json.loads(planned.stdout)
    assert ".agents/skills/project-delegate/SKILL.md.new" in plan["asset_changes"]
    assert ".project-workflow/manifest.json" in plan["asset_changes"]

    rolled_back = workflow_cli._apply_repository_upgrade_plan(
        tmp_path,
        "codex",
        plan["plan_fingerprint"],
        fail_after_replacements=1,
    )
    assert rolled_back["failure"]["code"] == "PW_UPGRADE_APPLY_REPLACEMENT_FAILED"
    assert delegate.read_text() == "# Owner Delegate Contract\n\nPreserve these bytes.\n"
    assert not delegate.with_name("SKILL.md.new").exists()
    assert json.loads(manifest.read_text())["asset_version"] == 1

    applied = run_project(
        tmp_path,
        "upgrade",
        "--agent",
        "codex",
        "--apply",
        "--plan-fingerprint",
        plan["plan_fingerprint"],
        "--format",
        "json",
    )
    assert applied.returncode == 0, applied.stdout + applied.stderr
    assert delegate.read_text() == "# Owner Delegate Contract\n\nPreserve these bytes.\n"
    pending = delegate.with_name("SKILL.md.new")
    assert pending.is_file()
    assert "Task or Epic" in pending.read_text()
    assert json.loads(manifest.read_text())["asset_version"] == workflow_cli.CURRENT_ASSET_VERSION

    subprocess.run(("git", "add", "."), cwd=tmp_path, check=True)
    subprocess.run(("git", "commit", "-qm", "upgrade"), cwd=tmp_path, check=True)
    repeated = run_project(tmp_path, "upgrade", "--agent", "codex", "--plan", "--format", "json")
    assert repeated.returncode == 0, repeated.stdout + repeated.stderr
    assert json.loads(repeated.stdout)["asset_changes"] == []
    assert not delegate.with_name("SKILL.md.new.2").exists()


def test_doctor_rejects_stale_delegate_semantics_and_cross_host_placeholders(
    tmp_path: Path,
) -> None:
    initialized = run_project(tmp_path, "init", "--agent", "claude-code")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    delegate = tmp_path / ".claude/agents/project-delegate.md"
    delegate.write_text(
        delegate.read_text().replace(
            "available child capacity", "Worker limit: 4 ${input:workers:4}"
        )
    )
    doctor = run_project(tmp_path, "doctor", "--strict")
    assert doctor.returncode != 0
    assert "Delegate semantic asset is invalid" in doctor.stdout
    assert "GitHub Copilot input placeholders" in doctor.stdout
