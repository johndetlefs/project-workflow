"""Proportionate repository architecture contracts."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from .repository import _markdown_section, _parse_key_value_section

ARCHITECTURE_IMPACT_VALUES = ("no", "local", "material")
ARCHITECTURE_SPINE_HEADINGS = (
    "Responsibilities",
    "Dependency Direction",
    "Source Ownership",
    "Shared State Boundaries",
    "Extension Points",
    "Measurable Constraints",
)
ARCHITECTURE_PLACEHOLDERS = {"", "____", "todo", "tbd", "not recorded"}


@dataclass(frozen=True)
class ArchitectureImpact:
    classification: str
    reason: str
    authority: str
    authority_identity: str
    architect_invocation: str
    architect_decision_identity: str
    affected_boundaries: str
    decision: str
    measurable_constraints: str
    conformance_plan: str


def architecture_authority_identity(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def architecture_decision_identity(impact: ArchitectureImpact) -> str:
    """Bind the Architect return to the authority and material plan it approved."""
    payload = "\n".join(
        (
            impact.authority,
            impact.authority_identity,
            impact.affected_boundaries,
            impact.decision,
            impact.measurable_constraints,
            impact.conformance_plan,
        )
    )
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _architecture_value_missing(value: str) -> bool:
    return value.strip().lower() in ARCHITECTURE_PLACEHOLDERS


def _architecture_field_values(section: str, field: str) -> list[str]:
    pattern = re.compile(
        rf"^\s*[-*]\s+{re.escape(field)}\s*:\s*(.*?)\s*$",
        flags=re.IGNORECASE | re.MULTILINE,
    )
    return [match.group(1).strip() for match in pattern.finditer(section)]


def architecture_impact_from_text(text: str) -> ArchitectureImpact | None:
    section = _markdown_section(text, "Architecture Impact")
    if not section:
        return None
    values = _parse_key_value_section(section)
    return ArchitectureImpact(
        classification=values.get("classification", "").strip().lower(),
        reason=values.get("reason", "").strip(),
        authority=values.get("architecture authority", "").strip().strip("`"),
        authority_identity=values.get("authority identity", "").strip(),
        architect_invocation=values.get("architect invocation", "").strip(),
        architect_decision_identity=values.get("architect decision identity", "").strip(),
        affected_boundaries=values.get("affected boundaries", "").strip(),
        decision=values.get("architecture decision", "").strip(),
        measurable_constraints=values.get("measurable constraints", "").strip(),
        conformance_plan=values.get("conformance plan", "").strip(),
    )


def _architecture_authority_path(root: Path, authority: str) -> Path | None:
    candidate = Path(authority)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    resolved_root = root.resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return None
    return resolved


def architecture_spine_issues(text: str) -> list[str]:
    issues: list[str] = []
    for heading in ARCHITECTURE_SPINE_HEADINGS:
        section = _markdown_section(text, heading)
        words = re.findall(r"[A-Za-z0-9]+", section)
        if not section or len(words) < 3 or "____" in section:
            issues.append(f"architecture spine must contain substantive ## {heading} content")
    return issues


def architecture_readiness_issues(root: Path, implementation_text: str) -> list[str]:
    impact_sections = re.findall(r"(?im)^##\s+Architecture Impact\s*$", implementation_text)
    if len(impact_sections) != 1:
        return ["record exactly one Architecture Impact section before readiness"]
    section = _markdown_section(implementation_text, "Architecture Impact")
    impact = architecture_impact_from_text(implementation_text)
    if impact is None:
        return ["record one Architecture Impact classification before readiness"]
    issues: list[str] = []
    classifications = _architecture_field_values(section, "Classification")
    if len(classifications) != 1:
        issues.append("record exactly one Architecture Impact Classification")
        return issues
    if impact.classification not in ARCHITECTURE_IMPACT_VALUES:
        issues.append("set Architecture Impact Classification to no, local, or material")
        return issues
    if _architecture_value_missing(impact.reason):
        issues.append("record a substantive Architecture Impact Reason")
    if impact.classification == "no":
        if impact.authority.lower() not in {"not applicable", "none"}:
            issues.append(
                "architecture-neutral work must record Architecture authority: Not applicable"
            )
        return issues

    if _architecture_value_missing(impact.authority):
        issues.append("record the repository-owned Architecture authority")
        return issues
    authority_path = _architecture_authority_path(root, impact.authority)
    if authority_path is None or not authority_path.is_file():
        issues.append(
            f"architecture authority does not exist inside the repository: {impact.authority}"
        )
        return issues
    try:
        spine_text = authority_path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(f"cannot read architecture authority {impact.authority}: {exc}")
    else:
        issues.extend(architecture_spine_issues(spine_text))
    if impact.classification == "local":
        return issues

    expected_identity = architecture_authority_identity(authority_path)
    if impact.authority_identity != expected_identity:
        issues.append(
            "material architecture authority is stale or missing: "
            f"expected {expected_identity} for {impact.authority}"
        )
    if not re.fullmatch(
        r"project-architect:[a-z0-9_-]+:[^\s]{8,}",
        impact.architect_invocation,
        flags=re.IGNORECASE,
    ):
        issues.append(
            "material architecture work must record Architect invocation as "
            "project-architect:<host>:<receipt>"
        )
    for label, value in (
        ("Affected boundaries", impact.affected_boundaries),
        ("Architecture decision", impact.decision),
        ("Measurable constraints", impact.measurable_constraints),
        ("Conformance plan", impact.conformance_plan),
    ):
        if _architecture_value_missing(value):
            issues.append(f"material architecture work must record substantive {label}")
    if impact.architect_decision_identity != architecture_decision_identity(impact):
        issues.append(
            "material Architect decision identity is missing or does not bind the current plan"
        )
    return issues


def material_architecture_integrity_issues(root: Path, implementation_text: str) -> list[str]:
    """Return non-bypassable material integrity issues for forced recovery transitions.

    Ordinary readiness still requires an explicit no/local/material classification. This narrower
    gate preserves audited recovery of legacy rows that predate the field while preventing force
    from bypassing an explicit or contradictory material contract.
    """
    impact_sections = re.findall(r"(?im)^##\s+Architecture Impact\s*$", implementation_text)
    if len(impact_sections) > 1:
        return ["record exactly one Architecture Impact section before readiness"]
    impact = architecture_impact_from_text(implementation_text)
    if impact is None or impact.classification != "material":
        return []
    return architecture_readiness_issues(root, implementation_text)


def architecture_conformance_issues(root: Path, implementation_text: str) -> list[str]:
    impact = architecture_impact_from_text(implementation_text)
    if impact is None or impact.classification != "material":
        return []
    readiness = architecture_readiness_issues(root, implementation_text)
    if readiness:
        return readiness
    values = _parse_key_value_section(
        _markdown_section(implementation_text, "Architecture Conformance")
    )
    issues: list[str] = []
    if values.get("authority identity", "").strip() != impact.authority_identity:
        issues.append("Architecture Conformance Authority identity must match the material plan")
    candidate = values.get("candidate", "").strip()
    if not re.fullmatch(r"(?:git:[0-9a-f]{40,64}|sha256:[0-9a-f]{64})", candidate):
        issues.append(
            "Architecture Conformance Candidate must be an exact git:<sha> or sha256:<digest> identity"
        )
    mechanical_checks = values.get("mechanical checks", "").strip()
    candidate_binding = f"candidate={candidate}"
    receipt_match = re.search(r"(?:^|;)\s*receipt=([^;]+)", mechanical_checks)
    if candidate_binding not in mechanical_checks or receipt_match is None:
        issues.append(
            "Architecture Conformance Mechanical checks must bind candidate=<identity> and "
            "receipt=<repository path>"
        )
    elif candidate:
        receipt_path = _architecture_authority_path(root, receipt_match.group(1).strip().strip("`"))
        if receipt_path is None or not receipt_path.is_file():
            issues.append("Architecture Conformance receipt must exist inside the repository")
        else:
            receipt_text = receipt_path.read_text(encoding="utf-8")
            if candidate not in receipt_text or not re.search(
                r"(?im)^\s*(?:[-*]\s*)?Verdict\s*:\s*Pass\s*$", receipt_text
            ):
                issues.append(
                    "Architecture Conformance receipt must bind the exact candidate and record Verdict: Pass"
                )
    deviations = values.get("deviations", "").strip()
    if _architecture_value_missing(deviations):
        issues.append("record Architecture Conformance Deviations as None or a resolved decision")
    elif deviations.lower() not in {"none", "none."} and "resolved" not in deviations.lower():
        issues.append("architecture deviations must be explicitly resolved before Review")
    if values.get("verdict", "").strip().lower() != "pass":
        issues.append("record Architecture Conformance Verdict: Pass before Review")
    return issues
