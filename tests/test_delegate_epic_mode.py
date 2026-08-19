from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli


TOKEN = "epic-coordinator-only-token"
BASE = "a" * 40
HEAD_A = "b" * 40
HEAD_B = "c" * 40


def unit(
    unit_id: str,
    *,
    dependencies: tuple[str, ...] = (),
    parent_acs: tuple[str, ...] = ("AC3",),
    state: str = "pending",
    order: int = 0,
) -> workflow_cli.DelegationUnit:
    return workflow_cli.DelegationUnit(
        unit_id=unit_id,
        title=f"Child {unit_id}",
        dependencies=dependencies,
        write_scope=(),
        parallel_safe=True,
        canonical_state=state,
        source_order=order,
        source_path=".project-workflow/tasks/EPIC-001/DECOMPOSITION.md",
        authority_acs=parent_acs,
    )


def plan(
    *units: workflow_cli.DelegationUnit,
    authority: str | None = "owner-approved EPIC-001 envelope",
    capacity: int = 3,
) -> workflow_cli.DelegationPlan:
    return workflow_cli.build_delegation_plan(
        target=workflow_cli.DelegationTarget(
            target_id="EPIC-001",
            kind="epic",
            title="Epic mode",
            lifecycle="In Progress",
            source_path=".project-workflow/tasks/EPIC-001/DECOMPOSITION.md",
            source_hash="decomposition-hash",
        ),
        units=tuple(units),
        requested_concurrency=3,
        available_child_capacity=capacity,
        observed_capabilities=("persistent-task",),
        capability_source="current Codex app task tools",
        persistent_task_authority=authority,
    )


def duties(*unit_ids: str) -> dict[str, workflow_cli.EpicChildObligations]:
    return {
        unit_id: workflow_cli.EpicChildObligations(
            parent_acs=("AC3",),
            repositories=(".",),
            write_scope=(f"proof/{unit_id.lower()}",),
            validations=(f"validate-{unit_id}",),
            evidence=(f"evidence-{unit_id}",),
        )
        for unit_id in unit_ids
    }


def capabilities(
    *,
    verified: bool = True,
    persistent: bool = True,
    worktrees: bool = True,
    monitoring: bool = True,
    reconciliation: bool = True,
    capacity: int = 3,
) -> workflow_cli.EpicHostCapabilities:
    return workflow_cli.EpicHostCapabilities(
        source="current Codex app task tools" if verified else "",
        current_session_verified=verified,
        persistent_tasks=persistent,
        isolated_worktrees=worktrees,
        monitoring=monitoring,
        reconciliation=reconciliation if verified else False,
        available_child_capacity=capacity,
    )


def coordinator(
    built: workflow_cli.DelegationPlan,
    root: Path,
    *,
    host: workflow_cli.EpicHostCapabilities | None = None,
) -> workflow_cli.EpicOrchestrator:
    return workflow_cli.EpicOrchestrator(
        plan=built,
        obligations=duties(*(item.unit_id for item in built.units)),
        capabilities=host or capabilities(),
        coordinator_token=TOKEN,
        coordinator_worktree=root,
        base_commit=BASE,
    )


def register(
    run: workflow_cli.EpicOrchestrator,
    unit_id: str,
    root: Path,
    *,
    suffix: str | None = None,
) -> workflow_cli.EpicChildWorkPacket:
    intent = next(item for item in run.creation_intents() if item.unit_id == unit_id)
    marker = suffix or unit_id.lower()
    return run.register_creation(
        intent,
        handle=f"native-{marker}",
        branch=f"codex/{marker}",
        worktree=root.parent / f"worktree-{marker}",
        coordinator_token=TOKEN,
    )


def result(
    run: workflow_cli.EpicOrchestrator,
    unit_id: str,
    *,
    head: str = HEAD_A,
    success: bool = True,
    shared_premise_valid: bool = True,
) -> workflow_cli.EpicChildResult:
    state = run.state.units[unit_id]
    return workflow_cli.EpicChildResult(
        unit_id=unit_id,
        handle=str(state.handle),
        attempt=state.attempt,
        branch=str(state.branch),
        worktree=str(state.worktree),
        base_commit=BASE,
        head_commit=head,
        success=success,
        claimed_paths=(f"proof/{unit_id.lower()}/result.txt",),
        validations={f"validate-{unit_id}": True},
        evidence={f"evidence-{unit_id}": True},
        repositories=(".",),
        plan_fingerprint=run.state.plan_fingerprint,
        shared_premise_valid=shared_premise_valid,
        failure_reason="injected failure" if not success else "",
    )


def verify(
    run: workflow_cli.EpicOrchestrator,
    child_result: workflow_cli.EpicChildResult,
) -> workflow_cli.TaskVerificationResult:
    unit_id = child_result.unit_id
    return run.verify_result(
        child_result,
        observed_branch=child_result.branch,
        observed_worktree=Path(child_result.worktree),
        observed_base_commit=child_result.base_commit,
        observed_head_commit=child_result.head_commit,
        observed_repositories=(".",),
        observed_paths=(f"proof/{unit_id.lower()}/result.txt",),
        observed_validations={f"validate-{unit_id}": True},
        observed_evidence={f"evidence-{unit_id}": True},
        coordinator_token=TOKEN,
    )


def test_real_epic_010_resolver_binds_decomposition_identity_and_parent_acs() -> None:
    root = Path(__file__).resolve().parents[1]
    target, units = workflow_cli._resolve_delegation_target(root, ("EPIC-010",))
    by_id = {item.unit_id: item for item in units}

    assert target.kind == "epic"
    assert by_id["TASK-062"].authority_acs == (
        "AC3", "AC6", "AC7", "AC9", "AC10", "AC11", "AC12", "AC14", "AC19"
    )
    assert by_id["TASK-063"].dependencies == ("TASK-061", "TASK-062")


def test_packet_parent_ac_drift_is_rejected_before_any_intent(tmp_path: Path) -> None:
    built = plan(unit("A", parent_acs=("AC3",)))
    wrong = duties("A")
    wrong["A"] = replace(wrong["A"], parent_acs=("AC6",))

    with pytest.raises(workflow_cli.EpicOrchestrationError) as error:
        workflow_cli.EpicOrchestrator(
            plan=built,
            obligations=wrong,
            capabilities=capabilities(),
            coordinator_token=TOKEN,
            coordinator_worktree=tmp_path,
            base_commit=BASE,
        )

    assert error.value.code == "PW_EPIC_AUTHORITY_MISMATCH"


@pytest.mark.parametrize(
    ("authority", "verified", "persistent", "worktrees", "monitoring", "capacity"),
    [
        (None, True, True, True, True, 1),
        ("unknown", True, True, True, True, 1),
        ("approved", False, False, False, False, 1),
        ("approved", True, False, True, True, 1),
        ("approved", True, True, False, True, 1),
        ("approved", True, True, True, False, 1),
        ("approved", True, True, True, True, 0),
    ],
)
def test_creation_fails_closed_without_every_authority_capability_and_capacity(
    tmp_path: Path,
    authority: str | None,
    verified: bool,
    persistent: bool,
    worktrees: bool,
    monitoring: bool,
    capacity: int,
) -> None:
    built = plan(unit("A"), authority=authority)
    run = coordinator(
        built,
        tmp_path,
        host=capabilities(
            verified=verified,
            persistent=persistent,
            worktrees=worktrees,
            monitoring=monitoring,
            capacity=capacity,
        ),
    )

    assert run.creation_intents() == ()
    boundary = run.capability_boundary()
    assert boundary["creation_supported"] is False
    assert boundary["fallback"] == "safe-sequential-coordinator"
    assert run.state.create_count == 0


def test_packet_is_complete_and_capacity_bounds_two_independent_intents(tmp_path: Path) -> None:
    built = plan(unit("A", order=0), unit("B", order=1), unit("C", dependencies=("A",), order=2))
    run = coordinator(built, tmp_path, host=capabilities(capacity=2))

    intents = run.creation_intents()
    assert [item.unit_id for item in intents] == ["A", "B"]
    payload = intents[0].payload()
    packet = payload["work_packet"]
    assert payload["requires"] == ["persistent-task", "isolated-worktree", "task-monitoring"]
    assert packet["target"]["authority_source"].endswith("DECOMPOSITION.md")
    assert packet["unit"]["parent_acs"] == ["AC3"]
    assert packet["scope"]["isolated_worktree_required"] is True
    assert packet["obligations"] == {
        "validation": ["validate-A"],
        "evidence": ["evidence-A"],
    }
    assert len(packet["forbidden_actions"]) == 4
    assert len(packet["stop_conditions"]) == 4
    assert "handle" not in json.dumps(payload).lower()


def test_register_prevents_duplicate_intent_handle_branch_and_worktree(tmp_path: Path) -> None:
    built = plan(unit("A", order=0), unit("B", order=1))
    run = coordinator(built, tmp_path)
    first = run.creation_intents()[0]
    run.register_creation(
        first,
        handle="native-a",
        branch="codex/a",
        worktree=tmp_path.parent / "worktree-a",
        coordinator_token=TOKEN,
    )

    with pytest.raises(workflow_cli.EpicOrchestrationError) as duplicate:
        run.register_creation(
            first,
            handle="native-a-duplicate",
            branch="codex/a-duplicate",
            worktree=tmp_path.parent / "worktree-a-duplicate",
            coordinator_token=TOKEN,
        )
    assert duplicate.value.code == "PW_EPIC_CREATION_INTENT_INVALID"

    second = next(item for item in run.creation_intents() if item.unit_id == "B")
    with pytest.raises(workflow_cli.EpicOrchestrationError) as handle_reuse:
        run.register_creation(
            second,
            handle="native-a",
            branch="codex/b",
            worktree=tmp_path.parent / "worktree-b",
            coordinator_token=TOKEN,
        )
    assert handle_reuse.value.code == "PW_EPIC_HANDLE_REUSE"


def test_register_accepts_exact_host_observed_detached_checkout_identity(tmp_path: Path) -> None:
    built = plan(unit("A", order=0), unit("B", order=1))
    run = coordinator(built, tmp_path)
    first, second = run.creation_intents()

    packet = run.register_creation(
        first,
        handle="native-a",
        branch=f"detached@{BASE}",
        worktree=tmp_path.parent / "worktree-a",
        coordinator_token=TOKEN,
    )
    run.register_creation(
        second,
        handle="native-b",
        branch=f"detached@{BASE}",
        worktree=tmp_path.parent / "worktree-b",
        coordinator_token=TOKEN,
    )

    assert packet.base_commit == BASE
    assert run.state.units["A"].branch == f"detached@{BASE}"
    accepted = verify(run, result(run, "A", head=BASE))
    assert accepted.accepted
    assert run.state.units["B"].state == "active"


def test_dependent_intent_waits_for_coordinator_branch_diff_validation_and_evidence(
    tmp_path: Path,
) -> None:
    built = plan(unit("A", order=0), unit("C", dependencies=("A",), order=1))
    run = coordinator(built, tmp_path)
    register(run, "A", tmp_path)
    assert run.creation_intents() == ()

    accepted = verify(run, result(run, "A"))

    assert accepted.accepted
    assert accepted.newly_eligible == ("C",)
    assert [item.unit_id for item in run.creation_intents()] == ["C"]


def test_out_of_scope_or_identity_mismatch_never_releases_dependency(tmp_path: Path) -> None:
    built = plan(unit("A", order=0), unit("C", dependencies=("A",), order=1))
    run = coordinator(built, tmp_path)
    register(run, "A", tmp_path)
    child = result(run, "A")

    rejected = run.verify_result(
        child,
        observed_branch="codex/wrong",
        observed_worktree=Path(child.worktree),
        observed_base_commit=BASE,
        observed_head_commit=HEAD_A,
        observed_repositories=(".",),
        observed_paths=("outside/result.txt",),
        observed_validations={"validate-A": True},
        observed_evidence={"evidence-A": True},
        coordinator_token=TOKEN,
    )

    assert not rejected.accepted
    assert run.state.units["C"].state == "halted"
    assert run.creation_intents() == ()


def test_child_failure_blocks_descendants_but_unaffected_sibling_continues(tmp_path: Path) -> None:
    built = plan(
        unit("A", order=0),
        unit("B", order=1),
        unit("C", dependencies=("A",), order=2),
    )
    run = coordinator(built, tmp_path, host=capabilities(capacity=2))
    register(run, "A", tmp_path)
    register(run, "B", tmp_path)

    failed = result(run, "A", success=False)
    rejected = verify(run, failed)

    assert not rejected.accepted
    assert run.state.units["C"].state == "blocked"
    assert run.state.units["B"].state == "active"
    summary = run.summary()
    assert summary["failed"] == ["A"]
    assert summary["blocked"] == ["C"]
    assert summary["in_flight"] == ["B"]


def test_shared_premise_halts_new_work_and_checkpoints_in_flight(tmp_path: Path) -> None:
    built = plan(unit("A", order=0), unit("B", order=1), unit("C", order=2))
    run = coordinator(built, tmp_path, host=capabilities(capacity=2))
    register(run, "A", tmp_path)
    register(run, "B", tmp_path)
    rejected = verify(run, result(run, "A", shared_premise_valid=False))

    assert not rejected.accepted
    assert not run.state.shared_premise_valid
    assert run.state.units["B"].state == "active"
    assert run.state.units["C"].state == "halted"
    run.checkpoint("B", coordinator_token=TOKEN)
    assert run.state.units["B"].state == "halted"
    assert run.state.units["B"].checkpointed


def test_persist_resume_reuses_exact_handles_without_new_creation(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    # The runtime writer uses git check-ignore, so initialize the disposable repository.
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    built = plan(unit("A", order=0), unit("B", order=1))
    run = coordinator(built, tmp_path)
    register(run, "A", tmp_path)
    register(run, "B", tmp_path)
    run.persist(tmp_path, coordinator_token=TOKEN)
    create_count = run.state.create_count
    observations = {
        unit_id: {
            "handle": state.handle,
            "attempt": state.attempt,
            "branch": state.branch,
            "worktree": state.worktree,
            "state": "active",
        }
        for unit_id, state in run.state.units.items()
    }

    resumed = workflow_cli.EpicOrchestrator.resume(
        root=tmp_path,
        plan=built,
        obligations=duties("A", "B"),
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        observations=observations,
    )

    assert resumed.state.create_count == create_count == 2
    assert resumed.creation_intents() == ()
    assert resumed.summary()["in_flight"] == ["A", "B"]


def test_resume_requires_observed_reconciliation_and_missing_handle_orphans(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    built = plan(unit("A"))
    run = coordinator(built, tmp_path)
    register(run, "A", tmp_path)
    run.persist(tmp_path, coordinator_token=TOKEN)

    with pytest.raises(workflow_cli.EpicOrchestrationError) as unsupported:
        workflow_cli.EpicOrchestrator.resume(
            root=tmp_path,
            plan=built,
            obligations=duties("A"),
            capabilities=capabilities(reconciliation=False),
            coordinator_token=TOKEN,
            observations={},
        )
    assert unsupported.value.code == "PW_EPIC_RECONCILIATION_UNVERIFIED"

    orphaned = workflow_cli.EpicOrchestrator.resume(
        root=tmp_path,
        plan=built,
        obligations=duties("A"),
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        observations={},
    )
    assert orphaned.state.units["A"].state == "orphaned"
    assert orphaned.state.create_count == 1


def test_canonical_completion_wins_during_resume(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    original = plan(unit("A"))
    run = coordinator(original, tmp_path)
    register(run, "A", tmp_path)
    run.persist(tmp_path, coordinator_token=TOKEN)
    completed = plan(unit("A", state="complete"))

    resumed = workflow_cli.EpicOrchestrator.resume(
        root=tmp_path,
        plan=completed,
        obligations=duties("A"),
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        observations={},
    )

    assert resumed.state.units["A"].state == "verified"
    assert resumed.state.units["A"].completion_provenance.startswith("canonical:")


def test_lifecycle_gates_remain_independent_of_delegate_verification(tmp_path: Path) -> None:
    built = plan(unit("A"))
    run = coordinator(built, tmp_path)
    register(run, "A", tmp_path)
    assert verify(run, result(run, "A")).accepted

    with pytest.raises(workflow_cli.EpicOrchestrationError) as child_gate:
        run.assert_child_completion_observed(
            "A", canonical_lifecycle="Review", qa_passed=True
        )
    assert child_gate.value.code == "PW_EPIC_CHILD_COMPLETION_GATED"

    with pytest.raises(workflow_cli.EpicOrchestrationError) as parent_gate:
        run.assert_parent_closeout_allowed(
            children_complete=False,
            parent_audit_passed=False,
            deferrals_resolved=False,
            retro_complete=False,
            owner_completion_authority=False,
        )
    assert parent_gate.value.code == "PW_EPIC_CLOSEOUT_GATED"


def test_epic_runtime_rejects_transcripts_credentials_and_unknown_fields() -> None:
    payload = {
        "schema_version": 1,
        "target_id": "EPIC-001",
        "plan_fingerprint": "fingerprint",
        "coordinator_hash": "hash",
        "coordinator_worktree": "/tmp/coordinator",
        "base_commit": BASE,
        "shared_premise_valid": True,
        "failure_seen": False,
        "create_count": 0,
        "used_intents": [],
        "used_handles": [],
        "integrated_paths": [],
        "units": {},
        "transcript": "private content",
    }

    with pytest.raises(workflow_cli.EpicOrchestrationError) as error:
        workflow_cli._epic_orchestration_state_from_payload(payload)

    assert error.value.code == "PW_EPIC_RUNTIME_PRIVATE_FIELD"
