from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]
POLICY_MARKERS = (
    "owner cannot accomplish the approved Intent",
    "material delivery claim is false",
    "required lifecycle stage is blocked",
    "affected proof layer",
    "additional reassurance",
)


def _run_project(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*PROJECT_CMD, *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _assert_policy(text: str) -> None:
    normalized = " ".join(text.split())
    for marker in POLICY_MARKERS:
        assert marker in normalized
    assert "follow-up" in normalized
    assert "broad or full-suite checks" in normalized


def test_continuation_cases_reject_both_overcooking_and_premature_stopping() -> None:
    payload = json.loads(
        (ROOT / "evaluations" / "intent_integrity" / "continuation-cases.json").read_text(
            encoding="utf-8"
        )
    )
    cases = {case["case_id"]: case for case in payload["cases"]}

    assert payload["suite"] == "continuation-sufficiency-v1"
    assert set(cases) == {
        "post-pass-adjacent-cleanup",
        "post-pass-material-contradiction",
    }
    assert cases["post-pass-adjacent-cleanup"]["expected"] == {
        "materiality": "non-material",
        "action": "record-follow-up",
        "validation_scope": "none",
    }
    assert cases["post-pass-material-contradiction"]["expected"] == {
        "materiality": "material",
        "action": "bounded-correction",
        "validation_scope": "affected-proof-layer",
    }

    sanitized = json.dumps(payload).lower()
    assert "/users/" not in sanitized
    assert "johndetlefs" not in sanitized
    assert "01a01d9d-15f5-7373-8e93-0cfd6633393f" not in sanitized


def test_packaged_and_repository_local_guidance_carry_the_same_policy() -> None:
    skill_pairs = (
        (
            ROOT / "src/project_workflow/codex/skills/project-implement/SKILL.md",
            ROOT / ".agents/skills/project-implement/SKILL.md",
        ),
        (
            ROOT / "src/project_workflow/codex/skills/project-qa-review/SKILL.md",
            ROOT / ".agents/skills/project-qa-review/SKILL.md",
        ),
    )
    for source, local in skill_pairs:
        source_text = source.read_text(encoding="utf-8")
        local_text = local.read_text(encoding="utf-8").replace(
            "<!-- project-workflow:generated -->\n", ""
        )
        assert local_text == source_text
        _assert_policy(source_text)

    for name in ("Implement.prompt.md", "QAReview.prompt.md"):
        source = (ROOT / "src/project_workflow/prompts" / name).read_text(encoding="utf-8")
        local = (ROOT / ".github/prompts" / name).read_text(encoding="utf-8")
        assert local == source
        _assert_policy(source)


def test_all_four_host_installs_receive_the_continuation_policy(tmp_path: Path) -> None:
    targets = {
        "codex": (
            ".agents/skills/project-implement/SKILL.md",
            ".agents/skills/project-qa-review/SKILL.md",
        ),
        "claude-code": (
            ".claude/agents/project-implement.md",
            ".claude/agents/project-qa-review.md",
        ),
        "cursor": (
            ".cursor/agents/project-implement.md",
            ".cursor/agents/project-qa-review.md",
        ),
        "github-copilot": (
            ".github/prompts/Implement.prompt.md",
            ".github/prompts/QAReview.prompt.md",
        ),
    }
    for host, relative_paths in targets.items():
        root = tmp_path / host
        root.mkdir()
        result = _run_project(["init", "--agent", host], cwd=root)
        assert result.returncode == 0, result.stdout + result.stderr
        for relative_path in relative_paths:
            _assert_policy((root / relative_path).read_text(encoding="utf-8"))
