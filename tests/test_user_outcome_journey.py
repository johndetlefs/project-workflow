from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from zipfile import ZipFile

from project_workflow import cli as workflow_cli


def make_journey_task(
    tmp_path: Path, task_dir: Path | None = None
) -> tuple[Path, Path, Path, dict[str, object]]:
    task_dir = task_dir or (
        tmp_path / ".project-workflow" / "tasks" / "TASK-001-Outcome-Journey"
    )
    evidence_dir = task_dir / "evidence"
    evidence_dir.mkdir(parents=True)
    requirements_path = task_dir / "REQUIREMENTS.md"
    implementation_path = task_dir / "IMPLEMENTATION.md"
    artifact_path = evidence_dir / "journey.txt"
    requirements_path.write_text(
        "# Requirements\n\n## Goal\n\nProve the user-outcome-journey for the requested job.\n",
        encoding="utf-8",
    )
    implementation_path.write_text(
        "## QA & Code Review\n\n"
        "- Intent QA contract: adversarial\n"
        "- Verdict: Pass\n"
        "- Intent adversarial verdict: Pass\n"
        "- Could every AC pass while the approved user job remains undone: No\n"
        "- Intent audit state: current\n"
        "- Outcome journey evidence: CLM-001 exercises the normal export journey.\n"
        "- Reviewer independence: Fresh QA phase reviewed sources and evidence separately.\n"
        "- Evidence: Structured journey record and artifact.\n"
        "- Findings: No unresolved findings.\n",
        encoding="utf-8",
    )
    artifact_path.write_text(
        "Actor entered Settings, exported the document, and opened the resulting file.",
        encoding="utf-8",
    )
    record: dict[str, object] = {
        "id": "CLM-001",
        "recipe": "user-outcome-journey",
        "status": "pass",
        "commit": "abc123",
        "timestamp": "2026-08-21T10:00:00Z",
        "parent_ac": "AC7",
        "claim": "A member can export and open the requested document.",
        "claim_scope": "member export from account settings",
        "journey_scope": "member export from account settings",
        "actor": "Signed-in member",
        "normal_entry_point": "Account settings > Export",
        "starting_state": "Member has an exportable document.",
        "material_operations": ["Open Export", "Confirm export", "Open downloaded document"],
        "resulting_state_or_artifact": "A readable downloaded document exists.",
        "outcome_observations": [
            "The export completed through the normal UI.",
            "The downloaded document opened with the expected content.",
        ],
        "source_artifact": "IMPLEMENTATION.md",
        "source_revision": workflow_cli._sha256_file(implementation_path),
        "artifact_identity": (
            "implementation-"
            + workflow_cli._sha256_file(implementation_path).removeprefix("sha256:")
        ),
        "environment": "Rendered production-like browser fixture",
        "invalid_substitute_policy": sorted(
            workflow_cli.USER_OUTCOME_INVALID_SUBSTITUTE_POLICY
        ),
        "invalid_substitutes": [],
        "owner_acceptance_required": False,
        "owner_acceptance_status": "not-required",
        "evidence_artifact": "evidence/journey.txt",
        "evidence_artifact_hash": workflow_cli._sha256_file(artifact_path),
    }
    (task_dir / "EVIDENCE.json").write_text(
        json.dumps({"task_id": "TASK-001", "claims": [record]}, indent=2) + "\n",
        encoding="utf-8",
    )
    return requirements_path, implementation_path, artifact_path, record


def write_record(task_dir: Path, record: dict[str, object]) -> None:
    (task_dir / "EVIDENCE.json").write_text(
        json.dumps({"task_id": "TASK-001", "claims": [record]}, indent=2) + "\n",
        encoding="utf-8",
    )


def test_user_outcome_journey_validates_claim_matched_normal_path(tmp_path: Path) -> None:
    requirements_path, implementation_path, _artifact_path, _record = make_journey_task(tmp_path)
    assert workflow_cli._structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
    ) == []


def test_user_outcome_journey_preserves_source_identity_from_recorded_ancestor(
    tmp_path: Path,
) -> None:
    requirements_path, implementation_path, _artifact_path, record = make_journey_task(tmp_path)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "record outcome evidence"], cwd=tmp_path, check=True)
    recorded_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True
    ).strip()
    record["commit"] = recorded_commit
    write_record(implementation_path.parent, record)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "bind evidence commit"], cwd=tmp_path, check=True)

    implementation_path.write_text(
        implementation_path.read_text(encoding="utf-8")
        + "\nThe implementation advanced after this historical proof.\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "advance implementation"], cwd=tmp_path, check=True)

    assert workflow_cli._structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
    ) == []


def test_user_outcome_journey_can_bind_a_retained_wheel_member(tmp_path: Path) -> None:
    requirements_path, implementation_path, _artifact_path, record = make_journey_task(tmp_path)
    source_wheel = implementation_path.parent / "evidence" / "candidate.whl"
    source_bytes = implementation_path.read_bytes()
    with ZipFile(source_wheel, "w") as archive:
        archive.writestr("project_workflow/cli.py", source_bytes)
    source_hash = "sha256:" + hashlib.sha256(source_bytes).hexdigest()
    record["source_artifact"] = "evidence/candidate.whl"
    record["source_artifact_member"] = "project_workflow/cli.py"
    record["source_revision"] = source_hash
    record["artifact_identity"] = "wheel-member-" + source_hash.removeprefix("sha256:")
    write_record(implementation_path.parent, record)

    implementation_path.write_text(
        implementation_path.read_text(encoding="utf-8") + "\nLater source change.\n",
        encoding="utf-8",
    )

    assert workflow_cli._structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
    ) == []


def test_user_outcome_journey_rejects_proxy_scope_and_invalid_substitute(
    tmp_path: Path,
) -> None:
    requirements_path, implementation_path, _artifact_path, record = make_journey_task(tmp_path)
    record["journey_scope"] = "one canary export control"
    record["normal_entry_point"] = "Debug-only export harness"
    record["invalid_substitutes"] = ["unit tests and a screenshot"]
    write_record(implementation_path.parent, record)

    issues = workflow_cli._structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
    )
    assert any("journey_scope must exactly match claim_scope" in issue for issue in issues)
    assert any("normal_entry_point cannot be" in issue for issue in issues)
    assert any("records invalid substitute evidence" in issue for issue in issues)


def test_outcome_proof_and_owner_acceptance_are_separate_states(tmp_path: Path) -> None:
    requirements_path, implementation_path, _artifact_path, record = make_journey_task(tmp_path)
    record["owner_acceptance_required"] = True
    record["owner_acceptance_status"] = "pending"
    write_record(implementation_path.parent, record)

    source = workflow_cli.OperationalStatusSource(
        "global-tracker", ".project-workflow/TRACKER.md"
    )
    item = workflow_cli.OperationalStatusWorkItem(
        "TASK-001",
        "Outcome Journey",
        "task",
        "Review",
        "QA is underway.",
        (source,),
        (
            workflow_cli._operational_status_fact(
                "docs_path",
                "tasks/TASK-001-Outcome-Journey/IMPLEMENTATION.md",
            ),
        ),
    )
    assert workflow_cli._operational_outcome_states(tmp_path, item) == (
        "outcome-proven",
        "ready-for-owner-acceptance",
    )
    assert workflow_cli._owner_acceptance_completion_issues(
        implementation_path.parent / "EVIDENCE.json"
    )

    record["owner_acceptance_status"] = "accepted"
    write_record(implementation_path.parent, record)
    assert workflow_cli._operational_outcome_states(tmp_path, item) == (
        "outcome-proven",
        "owner-accepted",
    )


def test_epic_status_aggregates_completed_child_qa_and_outcome_evidence(
    tmp_path: Path,
) -> None:
    epic_dir = tmp_path / ".project-workflow" / "tasks" / "EPIC-001-Aggregation"
    child_dir = epic_dir / "TASK-001-Outcome-Journey"
    requirements_path, implementation_path, _artifact_path, record = make_journey_task(
        tmp_path, child_dir
    )
    parent_requirements = epic_dir / "REQUIREMENTS.md"
    parent_requirements.write_text(
        "# Requirements\n\n## Goal\n\nRequire user-outcome-journey proof for this Epic.\n",
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Outcome Journey | Complete | Task | AC7 | "
        "tasks/EPIC-001-Aggregation/TASK-001-Outcome-Journey/IMPLEMENTATION.md | | |\n",
        encoding="utf-8",
    )
    source = workflow_cli.OperationalStatusSource(
        "global-tracker", ".project-workflow/TRACKER.md"
    )
    item = workflow_cli.OperationalStatusWorkItem(
        "EPIC-001",
        "Aggregation",
        "epic",
        "Closeout",
        "Epic closeout is underway.",
        (source,),
        (
            workflow_cli._operational_status_fact(
                "docs_path", "tasks/EPIC-001-Aggregation/REQUIREMENTS.md"
            ),
        ),
    )

    layers = {
        layer.name: layer for layer in workflow_cli._operational_item_proof_layers(tmp_path, item)
    }
    assert layers["qa-review"].state == "pass"
    assert layers["structured-evidence"].state == "pass"
    assert workflow_cli._operational_outcome_states(tmp_path, item) == (
        "outcome-proven",
        "not-required",
    )

    record["owner_acceptance_required"] = True
    record["owner_acceptance_status"] = "pending"
    write_record(child_dir, record)
    assert workflow_cli._operational_outcome_states(tmp_path, item) == (
        "outcome-proven",
        "ready-for-owner-acceptance",
    )

    record["evidence_artifact_hash"] = "sha256:" + "0" * 64
    write_record(child_dir, record)
    layers = {
        layer.name: layer for layer in workflow_cli._operational_item_proof_layers(tmp_path, item)
    }
    assert layers["structured-evidence"].state == "fail"
    assert workflow_cli._operational_outcome_states(tmp_path, item) == ("invalid", "unknown")


def test_intent_adversarial_qa_rejects_green_but_wrong_candidate() -> None:
    implementation = workflow_cli._implementation_template("TASK-001", "Outcome")
    assert "- Intent QA contract: adversarial" in implementation
    assert workflow_cli._intent_qa_review_issues(implementation)

    green_but_wrong = implementation.replace("- Verdict: ____", "- Verdict: Pass")
    green_but_wrong = green_but_wrong.replace(
        "- Intent adversarial verdict: ____",
        "- Intent adversarial verdict: Changes requested",
    )
    green_but_wrong = green_but_wrong.replace(
        "- Could every AC pass while the approved user job remains undone: ____",
        "- Could every AC pass while the approved user job remains undone: Yes",
    )
    issues = workflow_cli._intent_qa_review_issues(green_but_wrong)
    assert any("Intent adversarial verdict: Pass" in issue for issue in issues)
    assert any("Yes or unknown answer requires Changes requested" in issue for issue in issues)


def resolved_changes_requested_qa() -> str:
    decision = workflow_cli._validation_impact_decision(
        classification="affected",
        proof_layers=("qa-review",),
        validation_verdict="pass",
    )
    impact = workflow_cli._validation_impact_section(
        baseline="Independent QA receipt QA-001",
        change_summary="Resolved the three named blocking findings.",
        decided_by="Coordinator",
        decision=decision,
    )
    return (
        impact
        + "\n## QA & Code Review\n\n"
        "- Intent QA contract: adversarial\n"
        "- Verdict: Changes Requested\n"
        "- Intent adversarial verdict: Fail\n"
        "- Could every AC pass while the approved user job remains undone: Yes\n"
        "- Intent audit state: current\n"
        "- Outcome journey evidence: QA-001 inspected the exact normal journey.\n"
        "- Reviewer independence: Independent reviewer QA-001 did not implement the change.\n"
        "- Evidence: QA-001 retained the original blocking findings.\n"
        "- Findings: Three blocking findings were issued.\n"
        "- Findings disposition: Resolved\n"
        "- Affected validation verdict: Pass\n"
        "- Could every AC pass after affected validation while the approved user job remains undone: No\n"
        "- Affected validation evidence: Named regressions and the current outcome journey pass.\n"
        "- Second QA commissioned: No\n"
    )


def test_changes_requested_can_close_through_one_affected_validation_without_second_qa() -> None:
    implementation = resolved_changes_requested_qa()
    assert workflow_cli._intent_qa_review_issues(implementation) == []
    assert workflow_cli._qa_passed(implementation) is True


def test_changes_requested_resolution_fails_closed_without_exact_evidence() -> None:
    implementation = resolved_changes_requested_qa()
    missing_impact = "## QA & Code Review" + implementation.split(
        "## QA & Code Review", 1
    )[1]
    assert workflow_cli._qa_passed(missing_impact) is False

    second_qa = implementation.replace(
        "- Second QA commissioned: No", "- Second QA commissioned: Yes"
    )
    issues = workflow_cli._intent_qa_review_issues(second_qa)
    assert "record `Second QA commissioned: No`" in issues
    assert workflow_cli._qa_passed(second_qa) is False

    pending = implementation.replace(
        "- Affected validation verdict: Pass", "- Affected validation verdict: Pending"
    )
    assert workflow_cli._qa_passed(pending) is False
