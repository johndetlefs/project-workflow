from __future__ import annotations

import json
from pathlib import Path

from project_workflow import cli as workflow_cli
from tests.workflow_test_support import (
    ready_epic_retro,
    ready_implementation,
    ready_requirements,
    run_project,
    write_decomposition_plan,
    write_epic_contract,
    write_runtime_structured_evidence,
    write_structured_evidence,
)


def test_epic_audit_and_closeout_complete_only_when_gates_pass(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Closeout Ready"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Closeout Ready",
            ["- AC1: First parent outcome is delivered."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Closeout Ready")
    child_dir = epic_dir / "TASK-001-Ready-Child"
    child_dir.mkdir()
    child_impl = child_dir / "IMPLEMENTATION.md"
    child_impl.write_text(
        "## User Story\n\n"
        "As a maintainer, I want evidence.\n\n"
        "## Parent AC Evidence\n\n"
        "- AC1: Targeted validation passed.\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Targeted validation passed.\n"
        "- Findings: None.\n",
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Ready Child | Complete | Task | AC1 | tasks/EPIC-001-Closeout-Ready/TASK-001-Ready-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Ready Child", "Parent ACs": "AC1"}],
    )
    (epic_dir / "RETRO.md").write_text(
        ready_epic_retro("EPIC-001", "Closeout Ready"),
        encoding="utf-8",
    )

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "Epic acceptance audit passed." in audit.stdout
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "| AC1 | First parent outcome is delivered. | TASK-001 (Complete) |" in audit_text
    assert "TASK-001: parent AC evidence recorded; TASK-001: QA pass" in audit_text
    map_text = (epic_dir / "ACCEPTANCE-MAP.md").read_text(encoding="utf-8")
    assert (
        "| AC1 | First parent outcome is delivered. | TASK-001 (Complete) | TASK-001: parent AC evidence recorded; TASK-001: QA pass | None | Satisfied |"
        in map_text
    )

    validate_only = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert validate_only.returncode == 0, validate_only.stdout + validate_only.stderr
    assert "Epic closeout summary:" in validate_only.stdout
    assert "- Parent ACs: 1 total, 1 pass, 0 deferred, 0 gap" in validate_only.stdout
    assert "- Next action: rerun closeout with --complete" in validate_only.stdout
    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| EPIC-001 | Closeout Ready | To Do |" in tracker_text

    completed = run_project(
        ["epic", "closeout", "--epic-id", "EPIC-001", "--complete"],
        cwd=tmp_path,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "- Next action: global epic row can be marked Complete." in completed.stdout
    tracker_text = (tmp_path / ".project-workflow" / "TRACKER.md").read_text(encoding="utf-8")
    assert "| EPIC-001 | Closeout Ready | Complete |" in tracker_text

    doctor = run_project(["doctor", "--strict"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert (
        "EPIC-001 is Complete but lacks non-placeholder QA/code-review evidence"
        not in doctor.stdout
    )


def test_epic_audit_rejects_parent_evidence_from_unassigned_proof_owner(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Proof Owner"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Proof Owner",
            ["- AC1: Parent evidence must come from assigned proof owner."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(
        epic_dir,
        title="Proof Owner",
        ac_ids=["AC1"],
    )
    contract_text = (epic_dir / "EPIC-CONTRACT.md").read_text(encoding="utf-8")
    (epic_dir / "EPIC-CONTRACT.md").write_text(
        contract_text.replace("| AC1 | TASK-001 |", "| AC1 | TASK-999 |"),
        encoding="utf-8",
    )
    child_dir = epic_dir / "TASK-001-Wrong-Owner"
    child_dir.mkdir()
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Wrong Owner | Complete | Task | AC1 | tasks/EPIC-001-Proof-Owner/TASK-001-Wrong-Owner/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Wrong Owner", "Parent ACs": "AC1"}],
    )

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "TASK-001 is not assigned as proof owner" in audit.stdout
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "| Gap |" in audit_text


def test_visual_reference_recipe_requires_structured_evidence_before_review(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Visual Proof"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Visual Proof",
            ["- AC1: Production surface matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Visual Proof", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Visual Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Visual-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Visual Child",
            ["- AC1: Delivered UI matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Visual Child | Testing | Task | AC1 | tasks/EPIC-001-Visual-Proof/TASK-001-Visual-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    blocked = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Review"],
        cwd=tmp_path,
    )
    assert blocked.returncode != 0
    assert "structured evidence: EVIDENCE.json is missing" in blocked.stderr

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "structured evidence" not in doctor.stdout


def test_multi_parent_ac_structured_evidence_requires_one_claim_per_ac(
    tmp_path: Path,
) -> None:
    child_dir = tmp_path / "TASK-001-Multi-Ac"
    child_dir.mkdir()
    requirements_path = child_dir / "REQUIREMENTS.md"
    implementation_path = child_dir / "IMPLEMENTATION.md"
    requirements_path.write_text(
        ready_requirements(
            "TASK-001",
            "Multi AC",
            [
                "- AC1: Delivered UI matches the reference visual exactly.",
                "- AC2: Delivered UI matches the second reference visual exactly.",
            ],
        ),
        encoding="utf-8",
    )
    implementation_path.write_text(
        "## User Story\n\n"
        "As a maintainer, I want visual/reference fidelity proof, so that drift is caught.\n\n"
        "## Parent AC Coverage\n\n"
        "- AC1, AC2\n\n"
        "## Parent AC Evidence\n\n"
        "- AC1: Structured evidence recorded.\n"
        "- AC2: Structured evidence recorded.\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Visual/reference fidelity evidence recorded.\n"
        "- Findings: None.\n",
        encoding="utf-8",
    )
    evidence_dir = child_dir / "evidence"
    evidence_dir.mkdir()
    artifact = evidence_dir / "visual-comparison.txt"
    artifact.write_text("rendered comparison evidence", encoding="utf-8")
    artifact_hash = workflow_cli._sha256_file(artifact)

    base_record = {
        "id": "CLM-001",
        "claim": "Delivered surface matches the reference visual.",
        "recipe": "visual-reference-fidelity",
        "status": "pass",
        "commit": "abc123",
        "timestamp": "2026-07-09T00:00:00Z",
        "reference_artifact": "reference/playground.png",
        "delivered_artifact": "http://localhost:3000/widget",
        "comparison_method": "browser screenshot comparison",
        "evidence_artifact": "evidence/visual-comparison.txt",
        "evidence_artifact_hash": artifact_hash,
        "invalid_substitutes": [],
    }
    (child_dir / workflow_cli.STRUCTURED_EVIDENCE_FILENAME).write_text(
        json.dumps(
            {
                "task_id": "TASK-001",
                "claims": [{**base_record, "parent_ac": "AC1, AC2"}],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    comma_issues = workflow_cli._structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
        parent_ac_ids={"AC1", "AC2"},
    )
    assert (
        "structured evidence: missing passing claim records for parent ACs: AC1, AC2"
        in comma_issues
    )

    (child_dir / workflow_cli.STRUCTURED_EVIDENCE_FILENAME).write_text(
        json.dumps(
            {
                "task_id": "TASK-001",
                "claims": [
                    {**base_record, "id": "CLM-001", "parent_ac": "AC1"},
                    {**base_record, "id": "CLM-002", "parent_ac": "AC2"},
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    split_issues = workflow_cli._structured_evidence_issues(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
        parent_ac_ids={"AC1", "AC2"},
    )
    assert split_issues == []


def test_invalid_substitute_structured_evidence_blocks_doctor_and_audit(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Invalid Proof"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Invalid Proof",
            ["- AC1: Production surface matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Invalid Proof", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Invalid Visual Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Invalid-Visual-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Invalid Visual Child",
            ["- AC1: Delivered UI matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    write_structured_evidence(child_dir, invalid_substitutes=["unit tests"])
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Invalid Visual Child | Complete | Task | AC1 | tasks/EPIC-001-Invalid-Proof/TASK-001-Invalid-Visual-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "records invalid substitute evidence: unit tests" in doctor.stdout

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "uses invalid substitute for `visual-reference-fidelity`: unit test" in audit.stdout
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "| Gap |" in audit_text

    evidence_path = child_dir / workflow_cli.STRUCTURED_EVIDENCE_FILENAME
    evidence_payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    historical = evidence_payload["claims"][0]
    historical["id"] = "CLM-HISTORICAL-INVALID"
    historical["status"] = "fail"
    replacement = {
        **historical,
        "id": "CLM-VALID-REPLACEMENT",
        "status": "pass",
        "invalid_substitutes": [],
    }
    evidence_payload["claims"] = [historical, replacement]
    evidence_path.write_text(json.dumps(evidence_payload, indent=2) + "\n", encoding="utf-8")

    remediated_issues = workflow_cli._structured_evidence_issues(
        requirements_path=child_dir / "REQUIREMENTS.md",
        implementation_path=child_dir / "IMPLEMENTATION.md",
        parent_ac_ids={"AC1"},
    )
    assert remediated_issues == []


def test_valid_structured_visual_evidence_satisfies_epic_audit(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Valid Proof"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Valid Proof",
            ["- AC1: Production surface matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Valid Proof", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Valid Visual Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Valid-Visual-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Valid Visual Child",
            ["- AC1: Delivered UI matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    write_structured_evidence(child_dir)
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Valid Visual Child | Complete | Task | AC1 | tasks/EPIC-001-Valid-Proof/TASK-001-Valid-Visual-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "Epic acceptance audit passed." in audit.stdout


def test_stale_evidence_artifact_hash_blocks_doctor_and_audit(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Stale Evidence"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Stale Evidence",
            ["- AC1: Production surface matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Stale Evidence", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Stale Visual Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Stale-Visual-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Stale Visual Child",
            ["- AC1: Delivered UI matches the reference visual exactly."],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation("AC1", qa=True),
        encoding="utf-8",
    )
    write_structured_evidence(
        child_dir,
        evidence_artifact_hash="sha256:0000000000000000000000000000000000000000000000000000000000000000",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Stale Visual Child | Complete | Task | AC1 | tasks/EPIC-001-Stale-Evidence/TASK-001-Stale-Visual-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "evidence_artifact_hash is stale" in doctor.stdout

    audit = run_project(["epic", "audit", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    assert "evidence_artifact_hash is stale" in audit.stdout


def test_runtime_target_source_prose_contradiction_blocks_doctor(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Runtime Proof"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Runtime Proof",
            ["- AC1: Runtime target/source proof identifies the exact execution target."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Runtime Proof", ac_ids=["AC1"])
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Runtime Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Runtime-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Runtime Child",
            ["- AC1: Runtime target/source proof identifies the exact execution target."],
        ),
        encoding="utf-8",
    )
    impl_text = (
        ready_implementation("AC1", qa=True) + "\n## Runtime Proof Notes\n\n"
        "- Execution target: release/deployed\n"
        "- Source artifact: release bundle\n"
    )
    (child_dir / "IMPLEMENTATION.md").write_text(impl_text, encoding="utf-8")
    write_runtime_structured_evidence(
        child_dir,
        execution_target="working/local",
        source_artifact="local checkout",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Runtime Child | Complete | Task | AC1 | tasks/EPIC-001-Runtime-Proof/TASK-001-Runtime-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "prose claims execution_target release/deployed" in doctor.stdout
    assert "structured evidence proves working/local" in doctor.stdout


def test_epic_closeout_blocks_missing_parent_ac_evidence(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Closeout Blocked"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Closeout Blocked\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: First parent outcome is delivered.\n",
        encoding="utf-8",
    )
    child_dir = epic_dir / "TASK-001-Blocked-Child"
    child_dir.mkdir()
    (child_dir / "IMPLEMENTATION.md").write_text(
        "## User Story\n\n"
        "As a maintainer, I forgot evidence.\n\n"
        "## Parent AC Evidence\n\n"
        "- AC1: Pending implementation evidence.\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Local task validation only.\n"
        "- Findings: None.\n",
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Blocked Child | Complete | Task | AC1 | tasks/EPIC-001-Closeout-Blocked/TASK-001-Blocked-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    blocked = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert blocked.returncode != 0
    assert "Epic closeout summary:" in blocked.stdout
    assert "- Parent ACs: 1 total, 0 pass, 0 deferred, 1 gap" in blocked.stdout
    assert "- Missing parent evidence: AC1: TASK-001 lacks parent AC evidence" in blocked.stdout
    assert (
        "- Epic retro: epic retro section 'Lessons' is missing or still placeholder"
        in blocked.stdout
    )
    assert "- Next action: resolve the listed gaps or record approved deferrals" in blocked.stdout
    assert "Epic closeout blocked by acceptance gaps" in blocked.stdout
    assert "AC1: TASK-001 lacks parent AC evidence" in blocked.stdout


def test_epic_closeout_accepts_approved_deferral_with_follow_up(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Deferred Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    assert (epic_dir / "DEFERRALS.md").exists()
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Deferred Epic",
            ["- AC1: Deferred parent outcome is explicitly tracked."],
        ),
        encoding="utf-8",
    )
    (epic_dir / "DEFERRALS.md").write_text(
        "# Deferrals\n\n"
        "| Parent AC | Status | Owner | Decision Date | Reason | Follow-up | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
        "| AC1 | Approved | Product Owner | 2026-06-17 | Deferred from MVP | EPIC-002 | Owner approved follow-up |\n",
        encoding="utf-8",
    )
    (epic_dir / "RETRO.md").write_text(
        ready_epic_retro("EPIC-001", "Deferred Epic"),
        encoding="utf-8",
    )

    closeout = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert closeout.returncode == 0, closeout.stdout + closeout.stderr
    audit_text = (epic_dir / "ACCEPTANCE-AUDIT.md").read_text(encoding="utf-8")
    assert "Deferred from MVP" in audit_text
    assert (
        "| AC1 | Deferred parent outcome is explicitly tracked. | None | None | Approved:"
        in audit_text
    )
    assert "| Deferred |" in audit_text


def test_epic_closeout_blocks_incomplete_deferral_metadata(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Bad Deferral"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Bad Deferral\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: Deferred parent outcome is explicitly tracked.\n",
        encoding="utf-8",
    )
    (epic_dir / "DEFERRALS.md").write_text(
        "# Deferrals\n\n"
        "| Parent AC | Status | Owner | Decision Date | Reason | Follow-up | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
        "| AC1 | Approved | Product Owner | 2026-06-17 | Deferred from MVP |  | Missing follow-up |\n",
        encoding="utf-8",
    )

    closeout = run_project(["epic", "closeout", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert closeout.returncode != 0
    assert "AC1: no mapped child rows" in closeout.stdout
    assert "AC1: deferral is missing approval metadata or follow-up" in closeout.stdout


def test_epic_status_requires_parent_ac_evidence_before_complete(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Epic Status"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Epic Status",
            ["- AC1: Status gates enforce parent evidence."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Epic Status")
    child_dir = epic_dir / "TASK-001-Status-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "TASK-001",
            "Status Child",
            ["- AC1: Status gates enforce parent evidence."],
        ),
        encoding="utf-8",
    )
    child_impl = child_dir / "IMPLEMENTATION.md"
    child_impl.write_text(ready_implementation("AC1", qa=True), encoding="utf-8")
    child_impl.write_text(
        child_impl.read_text(encoding="utf-8").replace(
            "- AC1: Targeted parent evidence recorded.",
            "- AC1: Pending implementation evidence.",
        ),
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Status Child | In Progress | Task | AC1 | tasks/EPIC-001-Epic-Status/TASK-001-Status-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Status Child", "Parent ACs": "AC1"}],
    )

    testing = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Testing"],
        cwd=tmp_path,
    )
    assert testing.returncode == 0, testing.stdout + testing.stderr
    review = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Review"],
        cwd=tmp_path,
    )
    assert review.returncode == 0, review.stdout + review.stderr

    blocked = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert blocked.returncode != 0
    assert "cannot move to Complete without parent AC evidence for: AC1" in blocked.stderr

    child_impl.write_text(
        child_impl.read_text(encoding="utf-8").replace(
            "- AC1: Pending implementation evidence.",
            "- AC1: Targeted parent evidence recorded.",
        ),
        encoding="utf-8",
    )
    completed = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "Updated TASK-001: Review -> Complete" in completed.stdout


def test_task_ready_blocks_placeholders_and_allows_ready_docs(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Readiness Check", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr

    blocked = run_project(["task", "ready", "--id", "TASK-001"], cwd=tmp_path)
    assert blocked.returncode != 0
    assert "TASK-001 is not ready" in blocked.stderr
    assert "owner input required" in blocked.stderr
    assert "agent action required" in blocked.stderr

    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-001", "Readiness Check"),
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")

    ready = run_project(["task", "ready", "--id", "TASK-001"], cwd=tmp_path)
    assert ready.returncode == 0, ready.stdout + ready.stderr
    assert "TASK-001 readiness gate passed." in ready.stdout


def test_task_approval_envelope_command_and_stale_detection(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Approval Envelope", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    requirements_path = task_dir / "REQUIREMENTS.md"
    requirements_path.write_text(
        ready_requirements("TASK-001", "Approval Envelope"),
        encoding="utf-8",
    )
    implementation_path = task_dir / "IMPLEMENTATION.md"
    assert "____" in implementation_path.read_text(encoding="utf-8")

    # Simulate requirements drafted before command-written approval existed.
    requirements_path.write_text(
        workflow_cli._remove_markdown_section(
            requirements_path.read_text(encoding="utf-8"),
            workflow_cli.OWNER_APPROVAL_HEADING,
        ),
        encoding="utf-8",
    )

    blocked = run_project(["task", "status", "--id", "TASK-001", "--to", "Analysing"], cwd=tmp_path)
    assert blocked.returncode != 0
    assert "add `## Owner Approval`" in blocked.stderr

    approved = run_project(
        [
            "task",
            "approve-requirements",
            "--id",
            "TASK-001",
            "--approved-by",
            "Product Owner",
            "--source",
            "Owner approved TASK-001 requirements in planning thread.",
        ],
        cwd=tmp_path,
    )
    assert approved.returncode == 0, approved.stdout + approved.stderr
    approved_text = requirements_path.read_text(encoding="utf-8")
    assert "- Approved scope envelope: Yes" in approved_text
    assert "- Approved artifact identity: sha256:" in approved_text

    analysing = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Analysing"],
        cwd=tmp_path,
    )
    assert analysing.returncode == 0, analysing.stdout + analysing.stderr
    implementation_path.write_text(ready_implementation(), encoding="utf-8")
    ready = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Ready"],
        cwd=tmp_path,
    )
    assert ready.returncode == 0, ready.stdout + ready.stderr

    requirements_path.write_text(
        approved_text + "\n## Added Scope\n\n- This changes the approved requirements.\n",
        encoding="utf-8",
    )
    stale = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "In Progress"],
        cwd=tmp_path,
    )
    assert stale.returncode != 0
    assert "approval is stale because requirements or ACs changed" in stale.stderr


def test_task_adopt_records_approval_and_untrusted_evidence_gate(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(["task", "init", "--title", "Legacy Task", "--update-tracker"], cwd=tmp_path)
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: TASK-001\n"
        "- Title: Legacy Task\n\n"
        "## Goal\n\n"
        "- Adopt old work.\n\n"
        "## Non-Goals\n\n"
        "- Do not change product scope.\n\n"
        "## Users & Context\n\n"
        "- Maintainers need old work under gates.\n\n"
        "## Requirements (Outcome-Focused)\n\n"
        "- The old task can continue only after adoption.\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: Legacy adoption is recorded.\n\n"
        "## Open Questions (Answer Needed)\n\n"
        "- None.\n\n"
        "## Decisions (Resolved)\n\n"
        "- Adopt explicitly.\n\n"
        "## Validation Plan\n\n"
        "- Run workflow status gates.\n",
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(
        ready_implementation(qa=True),
        encoding="utf-8",
    )
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(
            "| TASK-001 | Legacy Task | To Do |",
            "| TASK-001 | Legacy Task | Analysing |",
        ),
        encoding="utf-8",
    )

    blocked = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Plan Confirmed"],
        cwd=tmp_path,
    )
    assert blocked.returncode != 0
    assert "Owner Approval" in blocked.stderr

    adopt = run_project(
        [
            "task",
            "adopt",
            "--id",
            "TASK-001",
            "--approved-by",
            "Test Owner",
            "--source",
            "Owner approved legacy adoption.",
        ],
        cwd=tmp_path,
    )
    assert adopt.returncode == 0, adopt.stdout + adopt.stderr
    requirements_text = (task_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    assert "## Legacy Adoption" in requirements_text
    assert "Evidence refreshed after adoption: No" in requirements_text

    confirmed = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Plan Confirmed"],
        cwd=tmp_path,
    )
    assert confirmed.returncode == 0, confirmed.stdout + confirmed.stderr

    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(
            "| TASK-001 | Legacy Task | Plan Confirmed |",
            "| TASK-001 | Legacy Task | Review |",
        ),
        encoding="utf-8",
    )
    complete_blocked = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert complete_blocked.returncode != 0
    assert "pre-adoption evidence as untrusted" in complete_blocked.stderr

    refreshed = run_project(
        [
            "task",
            "adopt",
            "--id",
            "TASK-001",
            "--approved-by",
            "Test Owner",
            "--source",
            "Owner approved refreshed legacy evidence.",
            "--evidence-refreshed",
        ],
        cwd=tmp_path,
    )
    assert refreshed.returncode == 0, refreshed.stdout + refreshed.stderr
    completed = run_project(
        ["task", "status", "--id", "TASK-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_epic_adopt_records_approval_and_amendments_file(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Legacy Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / workflow_cli.EPIC_AMENDMENTS_FILENAME).unlink()
    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: EPIC-001\n"
        "- Title: Legacy Epic\n\n"
        "## Goal\n\n"
        "- Adopt old epic.\n\n"
        "## Non-Goals\n\n"
        "- Do not infer closeout evidence.\n\n"
        "## Users & Context\n\n"
        "- Maintainers need old epic under gates.\n\n"
        "## Requirements (Outcome-Focused)\n\n"
        "- The old epic has explicit adoption metadata.\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        "- AC1: Legacy epic adoption is recorded.\n\n"
        "## Open Questions (Answer Needed)\n\n"
        "- None.\n\n"
        "## Decisions (Resolved)\n\n"
        "- Adopt explicitly.\n\n"
        "## Validation Plan\n\n"
        "- Run workflow status gates.\n",
        encoding="utf-8",
    )

    adopt = run_project(
        [
            "epic",
            "adopt",
            "--epic-id",
            "EPIC-001",
            "--approved-by",
            "Test Owner",
            "--source",
            "Owner approved legacy epic adoption.",
        ],
        cwd=tmp_path,
    )
    assert adopt.returncode == 0, adopt.stdout + adopt.stderr
    requirements_text = (epic_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    assert "## Owner Approval" in requirements_text
    assert "## Legacy Adoption" in requirements_text
    assert "Evidence refreshed after adoption: No" in requirements_text
    assert (epic_dir / workflow_cli.EPIC_AMENDMENTS_FILENAME).exists()


def test_doctor_flags_manual_active_task_without_approval_envelope(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Manual Bypass", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    requirements_text = workflow_cli._remove_markdown_section(
        ready_requirements("TASK-001", "Manual Bypass"),
        workflow_cli.OWNER_APPROVAL_HEADING,
    )
    (task_dir / "REQUIREMENTS.md").write_text(requirements_text, encoding="utf-8")
    (task_dir / "IMPLEMENTATION.md").write_text(ready_implementation(), encoding="utf-8")
    tracker_path = tmp_path / ".project-workflow" / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace(" | To Do | ", " | In Progress | "),
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "TASK-001 approval envelope" in doctor.stdout
    assert "add `## Owner Approval`" in doctor.stdout


def test_epic_child_ready_uses_parent_approval_envelope_without_child_approval(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Envelope Parent"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Envelope Parent",
            ["- AC1: In-envelope child work can proceed."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Envelope Parent")
    child_dir = epic_dir / "TASK-001-In-Envelope-Child"
    child_dir.mkdir()
    child_requirements = ready_requirements(
        "TASK-001",
        "In Envelope Child",
        ["- AC1: Child work is ready inside the parent envelope."],
    )
    child_requirements = workflow_cli._remove_markdown_section(
        child_requirements,
        workflow_cli.OWNER_APPROVAL_HEADING,
    )
    child_requirements = child_requirements.replace(
        "## Goal\n\n",
        "## Owner Approval\n\n"
        "- Requirements reviewed by owner: No\n"
        "- Acceptance criteria reviewed by owner: No\n"
        "- Approved for decomposition: No\n"
        "- Approved for implementation: No\n"
        "- Approved scope envelope: No\n"
        "- Approved by: Inherited from parent epic envelope when unchanged\n"
        "- Approval date: Inherited from parent epic envelope when unchanged\n"
        "- Approval note / source: Inherited from parent epic envelope when unchanged\n"
        "- Approved artifact identity: Inherited from parent epic envelope when unchanged\n\n"
        "## Goal\n\n",
    )
    (child_dir / "REQUIREMENTS.md").write_text(child_requirements, encoding="utf-8")
    (child_dir / "IMPLEMENTATION.md").write_text(ready_implementation("AC1"), encoding="utf-8")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | In Envelope Child | In Progress | Task | AC1 | tasks/EPIC-001-Envelope-Parent/TASK-001-In-Envelope-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "In Envelope Child", "Parent ACs": "AC1"}],
    )

    ready_child = run_project(
        ["epic", "ready-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert ready_child.returncode == 0, ready_child.stdout + ready_child.stderr
    assert "TASK-001 readiness gate passed" in ready_child.stdout


def test_epic_ready_blocks_vague_epic_and_decomposition(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Vague Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    ready = run_project(["epic", "ready", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert ready.returncode != 0
    assert "EPIC-001 is not ready" in ready.stderr

    decompose = run_project(["epic", "decompose", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert decompose.returncode != 0
    assert "EPIC-001 is not ready" in decompose.stderr


def test_epic_lifecycle_gates_global_epic_status(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Lifecycle Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))

    analysing = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Analysing"],
        cwd=tmp_path,
    )
    assert analysing.returncode == 0, analysing.stdout + analysing.stderr
    assert "Updated EPIC-001: To Do -> Analysing" in analysing.stdout

    ready_blocked = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Ready"],
        cwd=tmp_path,
    )
    assert ready_blocked.returncode != 0
    assert "EPIC-001 cannot move to Ready" in ready_blocked.stderr

    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Lifecycle Epic",
            ["- AC1: Lifecycle status is safely gated."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Lifecycle Epic")

    ready = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Ready"],
        cwd=tmp_path,
    )
    assert ready.returncode == 0, ready.stdout + ready.stderr
    assert "Updated EPIC-001: Analysing -> Ready" in ready.stdout

    in_progress_blocked = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "In Progress"],
        cwd=tmp_path,
    )
    assert in_progress_blocked.returncode != 0
    assert "AC1: no mapped child rows" in in_progress_blocked.stderr

    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Lifecycle Child | Proposed | Task | AC1 |  |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    in_progress = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "In Progress"],
        cwd=tmp_path,
    )
    assert in_progress.returncode == 0, in_progress.stdout + in_progress.stderr
    assert "Updated EPIC-001: Ready -> In Progress" in in_progress.stdout

    closeout_blocked = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Closeout"],
        cwd=tmp_path,
    )
    assert closeout_blocked.returncode != 0
    assert "TASK-001 is Proposed, not Complete" in closeout_blocked.stderr

    complete_blocked = run_project(
        ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Complete"],
        cwd=tmp_path,
    )
    assert complete_blocked.returncode != 0
    assert "use `epic closeout --epic-id <EPIC-ID> --complete`" in complete_blocked.stderr


def test_epic_ready_child_blocks_shallow_child_status(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Child Readiness"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Child Readiness",
            ["- AC1: Shallow child readiness is enforced."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Child Readiness")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Shallow Child | In Progress | Task | AC1 | tasks/EPIC-001-Child-Readiness/TASK-001-Shallow-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Shallow Child", "Parent ACs": "AC1"}],
    )
    child_dir = epic_dir / "TASK-001-Shallow-Child"
    child_dir.mkdir()
    (child_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: TASK-001\n"
        "- Title: Shallow Child\n\n"
        "## Goal\n\n"
        "Describe the user outcome.\n",
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        "## User Story\n\nAs a ____, I want ____, so that ____.\n",
        encoding="utf-8",
    )

    ready_child = run_project(
        ["epic", "ready-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert ready_child.returncode != 0
    assert "TASK-001 is not ready" in ready_child.stderr

    status = run_project(
        ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", "Testing"],
        cwd=tmp_path,
    )
    assert status.returncode != 0
    assert "TASK-001 is not ready" in status.stderr


def test_discovery_task_ready_allows_bounded_discovery(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    task = run_project(
        ["task", "init", "--title", "Discovery Spike", "--update-tracker"],
        cwd=tmp_path,
    )
    assert task.returncode == 0, task.stdout + task.stderr
    task_dir = next((tmp_path / ".project-workflow" / "tasks").glob("TASK-001-*"))
    discovery_text = (
        "# Requirements\n\n"
        "## Summary\n\n"
        "- Task: TASK-001\n"
        "- Title: Discovery Spike\n"
        "- Type: Discovery\n\n"
        "## Discovery Plan\n\n"
        "- Question: Which readiness command shape should ship first?\n"
        "- Decision: Choose the command shape for implementation.\n"
        "- Boundary: Limit to CLI and generated guidance review.\n"
        "- Output: A recommendation recorded in requirements.\n"
        "- Validation: Owner can approve the recommendation.\n"
    )
    (task_dir / "REQUIREMENTS.md").write_text(discovery_text, encoding="utf-8")
    (task_dir / "IMPLEMENTATION.md").write_text(
        "## Discovery Plan\n\n"
        "- Type: Discovery\n"
        "- Question: Which readiness command shape should ship first?\n"
        "- Decision: Choose the command shape for implementation.\n"
        "- Boundary: Limit to CLI and generated guidance review.\n"
        "- Output: A recommendation recorded in requirements.\n"
        "- Validation: Owner can approve the recommendation.\n",
        encoding="utf-8",
    )

    ready = run_project(["task", "ready", "--id", "TASK-001"], cwd=tmp_path)
    assert ready.returncode == 0, ready.stdout + ready.stderr
    assert "TASK-001 readiness gate passed." in ready.stdout
