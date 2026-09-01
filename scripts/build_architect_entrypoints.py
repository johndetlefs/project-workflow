#!/usr/bin/env python3
"""Generate Project Architect host entrypoints from one canonical prompt."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_workflow.repository import (  # noqa: E402
    _extract_frontmatter_value,
    _host_native_prompt_body,
    _split_frontmatter,
    _to_claude_agent_markdown,
)

SOURCE = ROOT / "src/project_workflow/prompts/Architect.prompt.md"
CODEX_OUTPUTS = (
    ROOT / "src/project_workflow/codex/skills/project-architect/SKILL.md",
    ROOT / ".agents/skills/project-architect/SKILL.md",
)
CLAUDE_OUTPUT = ROOT / "src/project_workflow/claude/agents/project-architect.md"
COPILOT_OUTPUT = ROOT / ".github/prompts/Architect.prompt.md"


def codex_markdown(prompt_content: str) -> str:
    frontmatter, body = _split_frontmatter(prompt_content)
    description = _extract_frontmatter_value(frontmatter, "description") or "Project Architect"
    return (
        "---\n"
        "name: project-architect\n"
        f"description: {description}\n"
        "---\n\n"
        "# Project Architect\n\n"
        f"{_host_native_prompt_body(body, host='Codex')}"
    )


def expected_outputs() -> dict[Path, str]:
    prompt_content = SOURCE.read_text(encoding="utf-8")
    codex = codex_markdown(prompt_content)
    claude = _to_claude_agent_markdown(prompt_content, "project-architect")
    return {
        CODEX_OUTPUTS[0]: codex,
        CLAUDE_OUTPUT: claude,
        COPILOT_OUTPUT: prompt_content,
        CODEX_OUTPUTS[1]: codex,
    }


def output_drift(expected: dict[Path, str], actual: dict[Path, str]) -> list[Path]:
    """Return missing or byte-drifted outputs for disposable negative tests and CI."""
    return [path for path, content in expected.items() if actual.get(path) != content]


def stale_outputs() -> list[Path]:
    expected = expected_outputs()
    actual = {path: path.read_text(encoding="utf-8") for path in expected if path.is_file()}
    return [path for path in output_drift(expected, actual)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    outputs = expected_outputs()
    if args.write:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"Wrote {path.relative_to(ROOT)}")
        return 0

    stale = stale_outputs()
    if stale:
        for path in stale:
            print(f"Stale generated Project Architect entrypoint: {path.relative_to(ROOT)}")
        return 1
    print("Generated Project Architect entrypoints are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
