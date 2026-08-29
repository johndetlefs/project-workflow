from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli

ROOT = Path(__file__).resolve().parents[1]
PROJECT = [sys.executable, "-m", "project_workflow.cli"]


def run_project(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*PROJECT, *args], cwd=root, check=False, capture_output=True, text=True)


def test_coordinator_and_clarify_source_assets_hold_the_delivery_contract() -> None:
    coordinator_prompt = (ROOT / "src/project_workflow/prompts/Coordinator.prompt.md").read_text()
    coordinator_github = (ROOT / ".github/prompts/Coordinator.prompt.md").read_text()
    coordinator_skill = (
        ROOT / "src/project_workflow/codex/skills/project-coordinator/SKILL.md"
    ).read_text()
    coordinator_installed = (ROOT / ".agents/skills/project-coordinator/SKILL.md").read_text()

    assert coordinator_prompt == coordinator_github
    assert coordinator_installed == workflow_cli._with_generated_marker(
        ROOT / ".agents/skills/project-coordinator/SKILL.md", coordinator_skill
    )
    for text in (coordinator_prompt, coordinator_skill, coordinator_installed):
        normalized = " ".join(text.lower().split())
        for required in (
            "single owner-facing",
            "only writer",
            "smallest sufficient",
            "bounded packet",
            "independent qa",
            "stop after sufficient proof",
            "one full minor release",
        ):
            assert required in normalized
        assert "full task history by default" in normalized

    clarify_prompt = (ROOT / "src/project_workflow/prompts/Clarify.prompt.md").read_text()
    clarify_github = (ROOT / ".github/prompts/Clarify.prompt.md").read_text()
    clarify_skill = (
        ROOT / "src/project_workflow/codex/skills/project-clarify/SKILL.md"
    ).read_text()
    clarify_installed = (ROOT / ".agents/skills/project-clarify/SKILL.md").read_text()

    assert clarify_prompt == clarify_github
    assert clarify_installed == workflow_cli._with_generated_marker(
        ROOT / ".agents/skills/project-clarify/SKILL.md", clarify_skill
    )
    for text in (clarify_prompt, clarify_skill, clarify_installed):
        normalized = " ".join(text.lower().split())
        for required in (
            "pre-approval",
            "post-plan",
            "drift-ambiguity",
            "epic parent",
            "inside-envelope",
            "drift-detected",
            "approved-change",
            "does not monitor",
        ):
            assert required in normalized
        assert "parent `implementation.md` is not required" in normalized
        assert "run qa" in normalized


def test_delegate_is_a_one_coordinator_compatibility_entry() -> None:
    for path in (
        ROOT / "src/project_workflow/prompts/Delegate.prompt.md",
        ROOT / ".github/prompts/Delegate.prompt.md",
        ROOT / "src/project_workflow/codex/skills/project-delegate/SKILL.md",
        ROOT / ".agents/skills/project-delegate/SKILL.md",
    ):
        normalized = " ".join(path.read_text().lower().split())
        assert "compatibility entry" in normalized
        assert "second role" in normalized
        assert "one full minor release" in normalized
        assert "observed migration evidence" in normalized


@pytest.mark.parametrize("agent", sorted(workflow_cli.AGENT_CHOICES))
def test_each_host_init_installs_coordinator_and_corrected_clarify(
    tmp_path: Path, agent: str
) -> None:
    root = tmp_path / agent
    root.mkdir()
    initialized = run_project(root, "init", "--agent", agent)
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr

    if agent == "codex":
        coordinator = root / ".agents/skills/project-coordinator/SKILL.md"
        clarify = root / ".agents/skills/project-clarify/SKILL.md"
    elif agent == "github-copilot":
        coordinator = root / ".github/prompts/Coordinator.prompt.md"
        clarify = root / ".github/prompts/Clarify.prompt.md"
    else:
        host = ".claude" if agent == "claude-code" else ".cursor"
        coordinator = root / host / "agents/project-coordinator.md"
        clarify = root / host / "agents/project-clarify.md"

    assert coordinator.is_file()
    assert clarify.is_file()
    coordinator_text = " ".join(coordinator.read_text().lower().split())
    clarify_text = " ".join(clarify.read_text().lower().split())
    assert "single owner-facing" in coordinator_text
    assert "smallest sufficient" in coordinator_text
    assert "epic parent" in clarify_text
    assert "drift-ambiguity" in clarify_text
    assert "${input:" not in coordinator_text if agent in {"claude-code", "cursor"} else True

    doctor = run_project(root, "doctor", "--strict")
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr


def test_doctor_rejects_stale_coordinator_or_clarify_semantics(tmp_path: Path) -> None:
    initialized = run_project(tmp_path, "init", "--agent", "codex")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr

    coordinator = tmp_path / ".agents/skills/project-coordinator/SKILL.md"
    coordinator.write_text(
        coordinator.read_text().replace("smallest sufficient", "largest possible")
    )
    clarify = tmp_path / ".agents/skills/project-clarify/SKILL.md"
    clarify.write_text(clarify.read_text().replace("drift-ambiguity", "weekly review"))

    doctor = run_project(tmp_path, "doctor", "--strict")
    assert doctor.returncode != 0
    assert "Coordinator semantic asset is invalid" in doctor.stdout
    assert "Clarify semantic asset is invalid" in doctor.stdout
