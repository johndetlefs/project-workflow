from __future__ import annotations

from pathlib import Path

from project_workflow.architecture import (
    architecture_authority_identity,
    architecture_conformance_issues,
    architecture_decision_identity,
    architecture_impact_from_text,
    architecture_readiness_issues,
    architecture_spine_issues,
)

SPINE = """# Architecture

## Responsibilities

One component owns the workflow contract.

## Dependency Direction

Higher layers depend on lower layers only.

## Source Ownership

One authored source owns every derivative.

## Shared State Boundaries

Only the coordinator writes shared state.

## Extension Points

Adapters extend at explicit host boundaries.

## Measurable Constraints

Tests reject cycles and generated drift.
"""


def impact(
    classification: str,
    *,
    authority: str = "docs/architecture.md",
    identity: str = "",
) -> str:
    text = f"""## Architecture Impact

- Classification: {classification}
- Reason: This fixture exercises the selected architecture path.
- Architecture authority: {authority}
- Authority identity: {identity}
- Architect invocation: {"project-architect:codex:fixture-session" if classification == "material" else "Not required"}
- Architect decision identity: DECISION_IDENTITY
- Affected boundaries: runtime and lifecycle
- Architecture decision: Keep one source-bound contract.
- Measurable constraints: Reject dependency cycles.
- Conformance plan: Run the architecture checks.
"""
    if classification != "material":
        return text.replace("DECISION_IDENTITY", "Not required")
    parsed = architecture_impact_from_text(text)
    assert parsed is not None
    return text.replace("DECISION_IDENTITY", architecture_decision_identity(parsed))


def test_no_impact_is_cheap_and_needs_no_architecture_artifact(tmp_path: Path) -> None:
    text = impact("no", authority="Not applicable")
    assert architecture_readiness_issues(tmp_path, text) == []


def test_local_impact_cites_an_established_spine_without_material_ceremony(
    tmp_path: Path,
) -> None:
    authority = tmp_path / "docs" / "architecture.md"
    authority.parent.mkdir()
    authority.write_text(SPINE, encoding="utf-8")
    assert architecture_readiness_issues(tmp_path, impact("local")) == []


def test_local_impact_rejects_arbitrary_repository_file(tmp_path: Path) -> None:
    authority = tmp_path / "LICENSE"
    authority.write_text("A repository file that is not an architecture spine.\n", encoding="utf-8")
    issues = architecture_readiness_issues(tmp_path, impact("local", authority="LICENSE"))
    assert any("architecture spine" in issue for issue in issues)


def test_impact_rejects_duplicate_classifications(tmp_path: Path) -> None:
    contradictory = impact("material") + "\n- Classification: no\n"
    assert architecture_readiness_issues(tmp_path, contradictory) == [
        "record exactly one Architecture Impact Classification"
    ]


def test_impact_rejects_duplicate_sections(tmp_path: Path) -> None:
    contradictory = impact("material") + "\n" + impact("no", authority="Not applicable")
    assert architecture_readiness_issues(tmp_path, contradictory) == [
        "record exactly one Architecture Impact section before readiness"
    ]


def test_material_impact_requires_current_complete_authority(tmp_path: Path) -> None:
    authority = tmp_path / "docs" / "architecture.md"
    authority.parent.mkdir()
    authority.write_text(SPINE, encoding="utf-8")
    current = architecture_authority_identity(authority)
    assert architecture_readiness_issues(tmp_path, impact("material", identity=current)) == []

    stale = architecture_readiness_issues(
        tmp_path, impact("material", identity="sha256:" + "0" * 64)
    )
    assert any("stale or missing" in issue for issue in stale)


def test_material_impact_rejects_incomplete_spine(tmp_path: Path) -> None:
    authority = tmp_path / "docs" / "architecture.md"
    authority.parent.mkdir()
    authority.write_text(
        "# Architecture\n\n## Responsibilities\n\nOnly one concern.\n", encoding="utf-8"
    )
    issues = architecture_readiness_issues(
        tmp_path,
        impact("material", identity=architecture_authority_identity(authority)),
    )
    assert any("Dependency Direction" in issue for issue in issues)
    assert architecture_spine_issues(authority.read_text(encoding="utf-8"))


def test_material_conformance_is_required_before_review(tmp_path: Path) -> None:
    authority = tmp_path / "docs" / "architecture.md"
    authority.parent.mkdir()
    authority.write_text(SPINE, encoding="utf-8")
    identity = architecture_authority_identity(authority)
    plan = impact("material", identity=identity)
    assert any(
        "Verdict: Pass" in issue for issue in architecture_conformance_issues(tmp_path, plan)
    )

    candidate = "git:" + "a" * 40
    receipt = tmp_path / "evidence" / "architecture-conformance.md"
    receipt.parent.mkdir()
    receipt.write_text(
        f"# Architecture Conformance Receipt\n\n- Candidate: {candidate}\n- Verdict: Pass\n",
        encoding="utf-8",
    )
    conformance = f"""## Architecture Conformance

- Authority identity: {identity}
- Candidate: {candidate}
- Mechanical checks: candidate={candidate}; receipt=evidence/architecture-conformance.md
- Deviations: None
- Verdict: Pass
"""
    assert architecture_conformance_issues(tmp_path, plan + "\n" + conformance) == []


def test_material_conformance_rejects_unbound_prose(tmp_path: Path) -> None:
    authority = tmp_path / "docs" / "architecture.md"
    authority.parent.mkdir()
    authority.write_text(SPINE, encoding="utf-8")
    plan = impact("material", identity=architecture_authority_identity(authority))
    conformance = """## Architecture Conformance

- Authority identity: placeholder
- Candidate: x
- Mechanical checks: trust me
- Deviations: None
- Verdict: Pass
"""
    issues = architecture_conformance_issues(tmp_path, plan + "\n" + conformance)
    assert any("exact git:<sha>" in issue for issue in issues)
    assert any("candidate=<identity>" in issue for issue in issues)
