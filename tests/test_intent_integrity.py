from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from project_workflow import cli as workflow_cli


PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]


def run_project(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*PROJECT_CMD, *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def full_intent_requirements(task_id: str = "TASK-001") -> str:
    return f"""\
# Requirements

## Summary

- Task: {task_id}
- Title: Preserve Owner Outcome
- Intent contract: full

## Intent

Keep the agent accountable to the outcome the owner actually requested. Prevent detailed
requirements from quietly replacing that outcome with an easier proxy.

## Intent Spine

- OC1 — Completion capability: The owner can verify the requested outcome directly.
- OC2 — Material capabilities: Intent remains visible and traceable through all derived work.
- OC3 — Success journey: The normal user journey performs the requested job and proves its result.
- OC4 — Successful-but-wrong result: Every checklist passes while the requested job remains impossible.
- OC5 — Exclusions: Do not require maximal scope or repeated approval for unchanged work.
- OC6 — Assumptions: Semantic judgment remains reviewable rather than mechanically certain.
- OC7 — Authority source: The owner's confirmation of this plain-language Intent.

## Goal

- Preserve the approved owner outcome.

## Non-Goals

- Do not expand beyond the requested outcome.

## Users & Context

- Owners need to catch narrowing before implementation.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Derived work remains subordinate to Intent.

## Acceptance Criteria (Verifiable)

- AC1: A proxy cannot replace the requested outcome silently.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Intent is the approval meaning.

## Validation Plan

- Run the exact owner journey and adversarial fixtures.
"""


def test_new_templates_put_plain_intent_before_approval_and_keep_fix_compact() -> None:
    task = workflow_cli._requirements_template("TASK-001", "Meaning First")
    child = workflow_cli._epic_child_requirements_template(
        "TASK-002", "Child Meaning", "AC1"
    )
    fix = workflow_cli._fix_template("FIX-001", "Bounded Repair")

    for requirements in (task, child):
        assert "- Intent contract: full" in requirements
        assert requirements.index("## Intent\n") < requirements.index("## Owner Approval")
        assert "- OC1 — Completion capability:" in requirements
        assert "- OC7 — Authority source:" in requirements
        assert "- Intent reviewed and accurately reflected:" in requirements

    assert "- Intent reviewed and accurately reflected: No" in task
    assert (
        "- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged"
        in child
    )

    assert "- Intent contract: compact" in fix
    assert fix.index("## Intent\n") < fix.index("## Report")
    assert "## Intent Spine" not in fix


def test_intent_contract_rejects_placeholder_procedural_and_incomplete_spine() -> None:
    valid = full_intent_requirements()
    assert workflow_cli._intent_contract_issues(valid) == []

    procedural = valid.replace(
        "Keep the agent accountable to the outcome the owner actually requested. Prevent detailed\n"
        "requirements from quietly replacing that outcome with an easier proxy.",
        "Implement the requirements.",
    )
    procedural_issues = workflow_cli._intent_contract_issues(procedural)
    assert any("procedural or circular" in issue for issue in procedural_issues)

    placeholder = workflow_cli._requirements_template("TASK-001", "Meaning First")
    placeholder_issues = workflow_cli._intent_contract_issues(placeholder)
    assert any("placeholder content under `## Intent`" in issue for issue in placeholder_issues)
    assert any("placeholder content for OC1" in issue for issue in placeholder_issues)

    missing_commitment = valid.replace(
        "- OC4 — Successful-but-wrong result: Every checklist passes while the requested job remains impossible.\n",
        "",
    )
    assert any(
        "add `OC4 — Successful-But-Wrong Result`" in issue
        for issue in workflow_cli._intent_contract_issues(missing_commitment)
    )

    invalid_mode = valid.replace("- Intent contract: full", "- Intent contract: ful")
    assert workflow_cli._intent_contract_issues(invalid_mode) == [
        "set `Intent contract` to `full` or `compact`"
    ]

    duplicate = valid.replace(
        "- OC2 — Material capabilities: Intent remains visible and traceable through all derived work.\n",
        "- OC1 — Completion capability: A duplicate cannot silently replace the first record.\n"
        "- OC2 — Material capabilities: Intent remains visible and traceable through all derived work.\n",
    )
    assert any(
        "remove duplicate Intent Spine commitment IDs: OC1" in issue
        for issue in workflow_cli._intent_contract_issues(duplicate)
    )


def test_legacy_requirements_remain_compatible_until_current_contract_is_adopted() -> None:
    legacy = full_intent_requirements().replace("- Intent contract: full\n", "")
    legacy = workflow_cli._remove_markdown_section(legacy, "Intent")
    legacy = workflow_cli._remove_markdown_section(legacy, "Intent Spine")

    assert workflow_cli._intent_contract_issues(legacy) == []
    assert workflow_cli._requirements_readiness_issues(legacy) == []


def test_approval_summary_leads_with_meaning_and_records_intent_confirmation(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr
    created = run_project(
        ["task", "init", "--title", "Preserve Owner Outcome", "--update-tracker"],
        cwd=tmp_path,
    )
    assert created.returncode == 0, created.stdout + created.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    requirements_path = task_dir / "REQUIREMENTS.md"
    requirements_path.write_text(full_intent_requirements(), encoding="utf-8")

    synopsis = run_project(
        ["task", "approval-summary", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert synopsis.returncode == 0, synopsis.stdout + synopsis.stderr
    assert synopsis.stdout.startswith("Approval synopsis\n\nIntent\n")
    assert "Does this Intent accurately capture what you want and what success means?" in synopsis.stdout
    assert "AC1" not in synopsis.stdout
    assert "TASK-001" not in synopsis.stdout
    assert "sha256:" not in synopsis.stdout

    approved = run_project(
        [
            "task",
            "approve-requirements",
            "--id",
            "TASK-001",
            "--approved-by",
            "Test Owner",
            "--source",
            "Owner confirmed the displayed Intent and asked to proceed.",
        ],
        cwd=tmp_path,
    )
    assert approved.returncode == 0, approved.stdout + approved.stderr
    assert "Approved Intent: Keep the agent accountable" in approved.stdout
    approved_text = requirements_path.read_text(encoding="utf-8")
    assert "- Intent reviewed and accurately reflected: Yes" in approved_text
    assert "- Approved artifact identity: sha256:" in approved_text


def test_compact_fix_intent_is_required_without_full_spine() -> None:
    fix = workflow_cli._fix_template("FIX-001", "Bounded Repair")
    assert workflow_cli._intent_contract_issues(fix) == [
        "replace placeholder content under `## Intent`"
    ]

    ready = fix.replace(
        "State the bounded correction and restored outcome in one or two plain-language sentences.",
        "Restore the previously accepted export behavior without adding a new export outcome.",
    )
    assert workflow_cli._intent_contract_issues(ready) == []


def test_approval_summary_is_visible_in_task_and_epic_help(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stdout + init.stderr

    task_help = run_project(["task", "--help"], cwd=tmp_path)
    epic_help = run_project(["epic", "--help"], cwd=tmp_path)

    assert task_help.returncode == 0
    assert "approval-summary" in task_help.stdout
    assert epic_help.returncode == 0
    assert "approval-summary" in epic_help.stdout
    assert "intent-audit" in epic_help.stdout


def test_new_epic_scaffolds_review_required_intent_audit(tmp_path: Path) -> None:
    assert run_project(["init"], cwd=tmp_path).returncode == 0
    created = run_project(["epic", "init", "--title", "Intent Audit"], cwd=tmp_path)
    assert created.returncode == 0, created.stdout + created.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    payload = json.loads((epic_dir / "INTENT-AUDIT.json").read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["verdict"] == "review-required"
    assert [record["id"] for record in payload["commitments"]] == [
        "OC1",
        "OC2",
        "OC3",
        "OC4",
        "OC5",
        "OC6",
        "OC7",
    ]


def make_intent_audit_epic(tmp_path: Path) -> Path:
    epic_dir = tmp_path / ".project-workflow" / "tasks" / "EPIC-001-Intent-Audit"
    child_dir = epic_dir / "TASK-001-Outcome-Child"
    child_dir.mkdir(parents=True)
    requirements = full_intent_requirements("EPIC-001").replace(
        "- Task: EPIC-001", "- Epic: EPIC-001"
    )
    (epic_dir / "REQUIREMENTS.md").write_text(requirements, encoding="utf-8")
    (epic_dir / "EPIC-CONTRACT.md").write_text("# Contract\n", encoding="utf-8")
    (epic_dir / "DECOMPOSITION.md").write_text("# Decomposition\n", encoding="utf-8")
    (epic_dir / "AMENDMENTS.md").write_text("# Amendments\n", encoding="utf-8")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Outcome Child | In Progress | Task | AC1 | "
        "tasks/EPIC-001-Intent-Audit/TASK-001-Outcome-Child/IMPLEMENTATION.md | | |\n",
        encoding="utf-8",
    )
    (child_dir / "REQUIREMENTS.md").write_text(
        "# Child requirements\n\nPreserve the complete requested outcome.\n",
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        "# Child implementation\n\nDeliver and prove the normal user journey.\n",
        encoding="utf-8",
    )
    return epic_dir


def write_passing_intent_audit(epic_dir: Path) -> dict[str, object]:
    payload = json.loads(workflow_cli._intent_audit_template(epic_dir))
    payload.update(
        {
            "artifact_identity": workflow_cli._intent_audit_source_identity(epic_dir),
            "reviewed_by": "Independent Reviewer",
            "reviewed_at": "2026-08-21",
            "review_source": "Independent sourced semantic review receipt",
            "verdict": "pass",
        }
    )
    for record in payload["commitments"]:
        record.update(
            {
                "classification": "preserved",
                "parent_acs": ["AC1"],
                "child_owners": ["TASK-001"],
                "required_outcome_proof": "Run the normal user journey and observe its result.",
                "target_locations": [
                    "TASK-001-Outcome-Child/IMPLEMENTATION.md#acceptance-criteria"
                ],
                "lost_capability": "",
                "amendment": None,
            }
        )
    (epic_dir / "INTENT-AUDIT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def test_intent_audit_is_sourced_complete_and_read_only(tmp_path: Path) -> None:
    epic_dir = make_intent_audit_epic(tmp_path)
    audit_path = epic_dir / "INTENT-AUDIT.json"
    audit_path.write_text(workflow_cli._intent_audit_template(epic_dir), encoding="utf-8")
    initial = workflow_cli._intent_audit_evaluation(epic_dir)
    assert initial["state"] == "review-required"
    assert any("map one or more parent ACs" in issue for issue in initial["issues"])

    write_passing_intent_audit(epic_dir)
    before = audit_path.read_bytes()
    result = run_project(
        ["epic", "intent-audit", "--epic-id", "EPIC-001", "--format", "json"],
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["state"] == "current"
    assert audit_path.read_bytes() == before


def test_intent_audit_detects_stale_sources_and_unknown_mapping(tmp_path: Path) -> None:
    epic_dir = make_intent_audit_epic(tmp_path)
    write_passing_intent_audit(epic_dir)
    implementation_path = epic_dir / "TASK-001-Outcome-Child" / "IMPLEMENTATION.md"
    implementation_path.write_text(
        implementation_path.read_text(encoding="utf-8") + "\nNarrowed to a preview.\n",
        encoding="utf-8",
    )

    evaluation = workflow_cli._intent_audit_evaluation(epic_dir)
    assert evaluation["state"] == "stale"
    assert workflow_cli._intent_audit_gate_issues(epic_dir)


def test_material_drift_issue_surfaces_the_lost_capability() -> None:
    issues = workflow_cli._intent_audit_amendment_issues(
        None,
        commitment_id="OC3",
        lost_capability="The member cannot open the complete exported archive.",
    )
    assert "The member cannot open the complete exported archive." in issues[0]


def test_narrowed_authoring_proxy_is_blocked_despite_green_downstream_claims(
    tmp_path: Path,
) -> None:
    epic_dir = make_intent_audit_epic(tmp_path)
    payload = write_passing_intent_audit(epic_dir)
    material = next(record for record in payload["commitments"] if record["id"] == "OC2")
    material.update(
        {
            "classification": "proxy",
            "user_visible_consequence": (
                "The user can preview the level and edit one canary control but cannot "
                "meaningfully author the level."
            ),
            "lost_capability": "Meaningful level authoring beyond one canary control.",
            "amendment": None,
        }
    )
    (epic_dir / "INTENT-AUDIT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    evaluation = workflow_cli._intent_audit_evaluation(epic_dir)
    assert evaluation["state"] == "changes-requested"
    assert evaluation["unresolved_drift"] == ["OC2"]
    assert any("owner-approved amendment" in issue for issue in evaluation["issues"])


def test_current_owner_amendment_can_authorize_plainly_identified_material_change(
    tmp_path: Path,
) -> None:
    epic_dir = make_intent_audit_epic(tmp_path)
    payload = write_passing_intent_audit(epic_dir)
    material = next(record for record in payload["commitments"] if record["id"] == "OC2")
    material.update(
        {
            "classification": "narrowed",
            "disposition": "deferred",
            "lost_capability": "Bulk authoring is deferred from this approved delivery.",
            "amendment": {
                "approved_by": "Test Owner",
                "decision_date": "2026-08-21",
                "source": "Owner approved the stated capability reduction",
                "capability_change": "Deliver single-item authoring now; defer bulk authoring.",
            },
        }
    )
    (epic_dir / "INTENT-AUDIT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    evaluation = workflow_cli._intent_audit_evaluation(epic_dir)
    assert evaluation["state"] == "current"
    assert workflow_cli._intent_audit_gate_issues(epic_dir) == []
