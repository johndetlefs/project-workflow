from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli


ROOT = Path(__file__).parents[1]
PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]
POLICY_MARKERS = (
    "owner cannot accomplish the approved Intent",
    "material delivery claim is false",
    "required lifecycle stage is blocked",
    "affected proof layer",
    "additional reassurance",
    "workflow validation impact",
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


def test_continuation_cases_cover_the_post_proof_stop_gate() -> None:
    payload = json.loads(
        (ROOT / "evaluations" / "intent_integrity" / "continuation-cases.json").read_text(
            encoding="utf-8"
        )
    )
    cases = {case["case_id"]: case for case in payload["cases"]}

    assert payload["suite"] == "continuation-stop-gate-v3"
    assert set(cases) == {
        "post-pass-unaffected",
        "post-pass-affected-proof",
        "post-pass-affected-multiple-proof",
        "post-pass-affected-validation-passed",
        "post-pass-ambiguous-impact",
        "owner-observed-contradiction",
        "green-release-candidate",
    }
    assert cases["green-release-candidate"]["expected"] == {
        "impact": "unaffected",
        "validation": "none",
        "next_action": "release",
    }
    assert cases["owner-observed-contradiction"]["expected"] == {
        "impact": "affected",
        "validation": "affected-proof-layer",
        "next_action": "validate-once",
    }

    sanitized = json.dumps(payload).lower()
    assert "/users/" not in sanitized
    assert "johndetlefs" not in sanitized
    assert "01a01d9d-15f5-7373-8e93-0cfd6633393f" not in sanitized


@pytest.mark.parametrize(
    ("classification", "layers", "verdict", "validation"),
    [
        ("unaffected", (), "not-required", "none"),
        ("affected", ("implementation",), "pending", "affected-proof-layer"),
        ("affected", ("implementation", "structured-evidence"), "pass", "affected-proof-layer"),
        ("ambiguous", (), "pending", "clarify"),
    ],
)
def test_validation_impact_engine_selects_the_smallest_sufficient_scope(
    classification: str,
    layers: tuple[str, ...],
    verdict: str,
    validation: str,
) -> None:
    decision = workflow_cli._validation_impact_decision(
        classification=classification,
        proof_layers=layers,
        validation_verdict=verdict,
    )
    assert decision["required_validation"] == validation
    assert "required_independent_review" not in decision


@pytest.mark.parametrize(
    ("classification", "layers", "verdict"),
    [
        ("unaffected", ("implementation",), "not-required"),
        ("unaffected", (), "pass"),
        ("affected", (), "pending"),
        ("affected", ("implementation",), "not-required"),
        ("ambiguous", (), "pass"),
    ],
)
def test_validation_impact_engine_fails_closed_on_incoherent_decisions(
    classification: str,
    layers: tuple[str, ...],
    verdict: str,
) -> None:
    with pytest.raises(ValueError):
        workflow_cli._validation_impact_decision(
            classification=classification,
            proof_layers=layers,
            validation_verdict=verdict,
        )


def test_validation_impact_command_records_one_compact_existing_document_section(
    tmp_path: Path,
) -> None:
    init = _run_project(["init", "--agent", "codex"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    fix = _run_project(["fix", "init", "--title", "Impact Fixture"], cwd=tmp_path)
    assert fix.returncode == 0, fix.stdout + fix.stderr

    impact = _run_project(
        [
            "validation",
            "impact",
            "--id",
            "FIX-001",
            "--baseline",
            "passing proof abc123",
            "--change-summary",
            "later implementation correction",
            "--classification",
            "affected",
            "--proof-layer",
            "implementation",
            "--validation-verdict",
            "pass",
            "--decided-by",
            "test coordinator",
            "--format",
            "json",
        ],
        cwd=tmp_path,
    )
    assert impact.returncode == 0, impact.stdout + impact.stderr
    payload = json.loads(impact.stdout)
    assert payload["required_validation"] == "affected-proof-layer"
    assert "required_independent_review" not in payload
    fix_doc = next((tmp_path / ".project-workflow" / "tasks").glob("FIX-001-*/FIX.md"))
    assert fix_doc.read_text(encoding="utf-8").count("## Validation Impact") == 1


def _impact_item(tmp_path: Path, decision: dict[str, object]) -> workflow_cli.OperationalStatusWorkItem:
    implementation_path = tmp_path / ".project-workflow" / "tasks" / "TASK-001-Stop" / "IMPLEMENTATION.md"
    implementation_path.parent.mkdir(parents=True, exist_ok=True)
    implementation_path.write_text(
        workflow_cli._validation_impact_section(
            baseline="passing proof abc123",
            change_summary="one later change",
            decided_by="coordinator",
            decision=decision,
        ),
        encoding="utf-8",
    )
    source = workflow_cli.OperationalStatusSource("global-tracker", ".project-workflow/TRACKER.md")
    return workflow_cli.OperationalStatusWorkItem(
        "TASK-001",
        "Stop gate",
        "task",
        "Review",
        "Stop-gate fixture.",
        (source,),
        (workflow_cli.OperationalStatusFact("docs_path", "tasks/TASK-001-Stop/IMPLEMENTATION.md"),),
    )


def test_affected_change_requests_one_named_validation_and_never_qa(tmp_path: Path) -> None:
    decision = workflow_cli._validation_impact_decision(
        classification="affected",
        proof_layers=("implementation",),
        validation_verdict="pending",
    )
    item = _impact_item(tmp_path, decision)
    action = workflow_cli._operational_validation_impact_action(tmp_path, item, 0)
    assert action is not None
    assert action.action.code == "PW_STATUS_AFFECTED_VALIDATION_REQUIRED"
    assert "independent QA" in (action.action.request or "")
    assert "review" not in action.action.title.lower()


def test_passed_affected_validation_stops_for_the_same_change_identity(tmp_path: Path) -> None:
    decision = workflow_cli._validation_impact_decision(
        classification="affected",
        proof_layers=("implementation",),
        validation_verdict="pass",
    )
    item = _impact_item(tmp_path, decision)
    assert workflow_cli._operational_validation_impact_action(tmp_path, item, 0) is None
    assert workflow_cli._operational_validation_impact_action(tmp_path, item, 0) is None


def test_unaffected_change_advances_and_ambiguous_change_asks_owner(tmp_path: Path) -> None:
    unaffected = workflow_cli._validation_impact_decision(
        classification="unaffected",
        proof_layers=(),
        validation_verdict="not-required",
    )
    assert workflow_cli._operational_validation_impact_action(
        tmp_path, _impact_item(tmp_path, unaffected), 0
    ) is None

    ambiguous = workflow_cli._validation_impact_decision(
        classification="ambiguous",
        proof_layers=(),
        validation_verdict="pending",
    )
    action = workflow_cli._operational_validation_impact_action(
        tmp_path, _impact_item(tmp_path, ambiguous), 0
    )
    assert action is not None
    assert action.action.code == "PW_STATUS_VALIDATION_IMPACT_CLARIFICATION_REQUIRED"
    assert action.action.responsible_party == "owner"


def test_validation_impact_cannot_waive_the_existing_qa_gate() -> None:
    decision = workflow_cli._validation_impact_decision(
        classification="unaffected",
        proof_layers=(),
        validation_verdict="not-required",
    )
    docs = workflow_cli._validation_impact_section(
        baseline="passing proof",
        change_summary="no invalidating change",
        decided_by="agent",
        decision=decision,
    )
    assert not workflow_cli._has_qa_review_evidence(docs)


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
