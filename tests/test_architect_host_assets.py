from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from tests.workflow_test_support import run_project

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts/build_architect_entrypoints.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("architect_entrypoints", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_architect_host_entrypoints_are_current_and_semantically_sourced() -> None:
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    generator = load_generator()
    outputs = generator.expected_outputs()
    assert all(path.read_text(encoding="utf-8") == expected for path, expected in outputs.items())
    assert outputs[generator.CODEX_OUTPUTS[0]] == outputs[generator.CODEX_OUTPUTS[1]]
    for content in outputs.values():
        assert "exactly one of" in content
        assert "subordinate to the Coordinator" in content
        assert "do not impose universal" in content


def test_one_copy_semantic_drift_is_detected() -> None:
    generator = load_generator()
    expected = generator.expected_outputs()
    actual = dict(expected)
    drifted = generator.CLAUDE_OUTPUT
    actual[drifted] += "\nOne-copy semantic drift.\n"

    assert generator.output_drift(expected, actual) == [drifted]


def test_project_init_discovers_generated_architect_for_codex_and_claude(
    tmp_path: Path,
) -> None:
    codex_root = tmp_path / "codex"
    codex_root.mkdir()
    codex = run_project(["init", "--agent", "codex"], cwd=codex_root)
    assert codex.returncode == 0, codex.stdout + codex.stderr
    codex_skill = codex_root / ".agents/skills/project-architect/SKILL.md"
    assert codex_skill.is_file()

    claude_root = tmp_path / "claude"
    claude_root.mkdir()
    claude = run_project(["init", "--agent", "claude-code"], cwd=claude_root)
    assert claude.returncode == 0, claude.stdout + claude.stderr
    claude_agent = claude_root / ".claude/agents/project-architect.md"
    assert claude_agent.is_file()

    assert "exactly one of" in codex_skill.read_text(encoding="utf-8")
    assert "exactly one of" in claude_agent.read_text(encoding="utf-8")
