from __future__ import annotations

import json
from argparse import Namespace
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
    needs: str = "durable-resume, isolated-worktree",
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
        execution_needs=workflow_cli._delegation_execution_needs(needs, unit_id=unit_id),
    )


def plan(
    *units: workflow_cli.DelegationUnit,
    authority: str | None = "owner-approved EPIC-001 envelope",
    capacity: int = 3,
    requested: int = 3,
    observed: tuple[str, ...] = (
        "persistent-task",
        "isolated-worktree",
        "task-monitoring",
        "task-reconciliation",
        "task-retirement",
        "task-retirement-reconciliation",
    ),
    capability_source: str = "2026-08-19 current Codex app task tools",
    selected: tuple[str, ...] = (),
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
        selected_unit_ids=selected,
        requested_concurrency=requested,
        available_child_capacity=capacity,
        observed_capabilities=observed,
        capability_source=capability_source,
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
    retirement: bool = True,
    retirement_reconciliation: bool = True,
    capacity: int = 3,
) -> workflow_cli.EpicHostCapabilities:
    return workflow_cli.EpicHostCapabilities(
        source="2026-08-19 current Codex app task tools" if verified else "",
        current_session_verified=verified,
        persistent_tasks=persistent,
        isolated_worktrees=worktrees,
        monitoring=monitoring,
        reconciliation=reconciliation if verified else False,
        available_child_capacity=capacity,
        additional_capabilities=(
            tuple(
                capability
                for capability, supported in (
                    ("task-retirement", retirement),
                    ("task-retirement-reconciliation", retirement_reconciliation),
                )
                if supported
            )
            if verified
            else ()
        ),
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
        "AC3",
        "AC6",
        "AC7",
        "AC9",
        "AC10",
        "AC11",
        "AC12",
        "AC14",
        "AC19",
    )
    assert by_id["TASK-063"].dependencies == ("TASK-061", "TASK-062")


def test_epic_requires_full_git_object_identity_for_base_and_result(tmp_path: Path) -> None:
    built = plan(unit("A"))
    with pytest.raises(workflow_cli.EpicOrchestrationError) as base_error:
        workflow_cli.EpicOrchestrator(
            plan=built,
            obligations=duties("A"),
            capabilities=capabilities(),
            coordinator_token=TOKEN,
            coordinator_worktree=tmp_path,
            base_commit="abcdef0",
        )
    assert base_error.value.code == "PW_EPIC_BASE_INVALID"

    run = coordinator(built, tmp_path)
    register(run, "A", tmp_path)
    child = replace(result(run, "A"), head_commit="abcdef0")
    rejected = run.verify_result(
        child,
        observed_branch=child.branch,
        observed_worktree=Path(child.worktree),
        observed_base_commit=BASE,
        observed_head_commit="abcdef0",
        observed_repositories=(".",),
        observed_paths=("proof/a/result.txt",),
        observed_validations={"validate-A": True},
        observed_evidence={"evidence-A": True},
        coordinator_token=TOKEN,
    )
    assert not rejected.accepted
    assert "head commit identity" in " ".join(rejected.issues)


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
    (
        "authority",
        "verified",
        "persistent",
        "worktrees",
        "monitoring",
        "reconciliation",
        "capacity",
    ),
    [
        (None, True, True, True, True, True, 1),
        ("unknown", True, True, True, True, True, 1),
        ("approved", False, False, False, False, False, 1),
        ("approved", True, False, True, True, True, 1),
        ("approved", True, True, False, True, True, 1),
        ("approved", True, True, True, False, True, 1),
        ("approved", True, True, True, True, False, 1),
        ("approved", True, True, True, True, True, 0),
    ],
)
def test_creation_fails_closed_without_every_authority_capability_and_capacity(
    tmp_path: Path,
    authority: str | None,
    verified: bool,
    persistent: bool,
    worktrees: bool,
    monitoring: bool,
    reconciliation: bool,
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
            reconciliation=reconciliation,
            capacity=capacity,
        ),
    )

    assert run.creation_intents() == ()
    boundary = run.capability_boundary()
    assert boundary["creation_supported"] is False
    assert boundary["fallback"] == "safe-sequential-coordinator"
    assert run.state.create_count == 0


def test_creation_fails_closed_when_runtime_observation_exceeds_or_drifts_from_plan(
    tmp_path: Path,
) -> None:
    partial = plan(
        unit("A"),
        observed=("persistent-task",),
    )
    partial_run = coordinator(partial, tmp_path, host=capabilities())

    assert partial_run.creation_intents() == ()
    assert "immutable plan lacks" in " ".join(partial_run.capability_boundary()["reasons"])

    complete = plan(unit("A"))
    mismatched_source = replace(capabilities(), source="different host observation")
    drifted_run = coordinator(complete, tmp_path, host=mismatched_source)

    assert drifted_run.creation_intents() == ()
    assert "source does not match" in " ".join(drifted_run.capability_boundary()["reasons"])


def test_runtime_capacity_can_shrink_but_never_expand_immutable_plan_capacity(
    tmp_path: Path,
) -> None:
    units = (unit("A", order=0), unit("B", order=1), unit("C", order=2))
    plan_limited = coordinator(plan(*units, capacity=1), tmp_path, host=capabilities(capacity=3))
    runtime_limited = coordinator(plan(*units, capacity=3), tmp_path, host=capabilities(capacity=2))

    assert [item.unit_id for item in plan_limited.creation_intents()] == ["A"]
    assert [item.unit_id for item in runtime_limited.creation_intents()] == ["A", "B"]


def test_packet_is_complete_and_capacity_bounds_two_independent_intents(tmp_path: Path) -> None:
    built = plan(unit("A", order=0), unit("B", order=1), unit("C", dependencies=("A",), order=2))
    run = coordinator(built, tmp_path, host=capabilities(capacity=2))

    intents = run.creation_intents()
    assert [item.unit_id for item in intents] == ["A", "B"]
    payload = intents[0].payload()
    packet = payload["work_packet"]
    assert payload["requires"] == [
        "persistent-task",
        "task-monitoring",
        "task-reconciliation",
        "isolated-worktree",
        "task-retirement",
        "task-retirement-reconciliation",
    ]
    assert packet["target"]["authority_source"].endswith("DECOMPOSITION.md")
    assert packet["unit"]["parent_acs"] == ["AC3"]
    assert packet["scope"]["isolated_worktree_required"] is True
    assert packet["obligations"] == {
        "validation": ["validate-A"],
        "evidence": ["evidence-A"],
    }
    assert len(packet["forbidden_actions"]) == 4
    assert len(packet["stop_conditions"]) == 4
    assert "full conversation history" in packet["invalid_substitutes"][-1]
    assert "authority source and hash actually used" in packet["return_contract"]
    assert "handle" not in json.dumps(payload).lower()


def test_omitted_canonically_complete_dependency_is_verified_in_packet(tmp_path: Path) -> None:
    built = plan(
        unit("A", state="complete", order=0),
        unit("C", dependencies=("A",), order=1),
        selected=("C",),
    )
    run = coordinator(built, tmp_path)

    intent = run.creation_intents()[0]

    assert intent.unit_id == "C"
    assert intent.packet.verified_dependencies == ("A",)


def test_scope_collision_reduction_is_reported_and_repository_scoped(tmp_path: Path) -> None:
    built = plan(unit("A", order=0), unit("B", order=1))
    same_repository = duties("A", "B")
    same_repository["B"] = replace(
        same_repository["B"], write_scope=same_repository["A"].write_scope
    )
    serialized = workflow_cli.EpicOrchestrator(
        plan=built,
        obligations=same_repository,
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        coordinator_worktree=tmp_path,
        base_commit=BASE,
    )

    assert [item.unit_id for item in serialized.creation_intents()] == ["A"]
    assert "collision" in " ".join(serialized.summary()["creation_eligibility"]["B"]["reasons"])

    separate_repositories = duties("A", "B")
    separate_repositories["A"] = replace(
        separate_repositories["A"], repositories=("repo-a",), write_scope=("same/path",)
    )
    separate_repositories["B"] = replace(
        separate_repositories["B"], repositories=("repo-b",), write_scope=("same/path",)
    )
    parallel = workflow_cli.EpicOrchestrator(
        plan=built,
        obligations=separate_repositories,
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        coordinator_worktree=tmp_path,
        base_commit=BASE,
    )

    assert [item.unit_id for item in parallel.creation_intents()] == ["A", "B"]
    register(parallel, "A", tmp_path, suffix="repo-a")
    register(parallel, "B", tmp_path, suffix="repo-b")
    for unit_id, repository, head in (
        ("A", "repo-a", HEAD_A),
        ("B", "repo-b", HEAD_B),
    ):
        child = replace(
            result(parallel, unit_id, head=head),
            claimed_paths=("same/path/result.txt",),
            repositories=(repository,),
        )
        accepted = parallel.verify_result(
            child,
            observed_branch=child.branch,
            observed_worktree=Path(child.worktree),
            observed_base_commit=BASE,
            observed_head_commit=head,
            observed_repositories=(repository,),
            observed_paths=("same/path/result.txt",),
            observed_validations={f"validate-{unit_id}": True},
            observed_evidence={f"evidence-{unit_id}": True},
            coordinator_token=TOKEN,
        )
        assert accepted.accepted


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

    with pytest.raises(workflow_cli.EpicOrchestrationError) as unsafe_handle:
        run.register_creation(
            second,
            handle="credential or transcript text",
            branch="codex/b",
            worktree=tmp_path.parent / "worktree-b",
            coordinator_token=TOKEN,
        )
    assert unsafe_handle.value.code == "PW_EPIC_HANDLE_REUSE"


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
    assert accepted.newly_eligible == ()
    newly_eligible = run.record_durable_disposition(
        "A", kind="integrated", receipt=f"git:{HEAD_A}", coordinator_token=TOKEN
    )
    assert newly_eligible == ("C",)
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


def test_integrated_diff_collision_is_rejected_before_dependency_release(tmp_path: Path) -> None:
    built = plan(unit("A", order=0), unit("B", dependencies=("A",), order=1))
    obligations = duties("A", "B")
    obligations["A"] = replace(obligations["A"], write_scope=("proof/shared",))
    obligations["B"] = replace(obligations["B"], write_scope=("proof/shared",))
    run = workflow_cli.EpicOrchestrator(
        plan=built,
        obligations=obligations,
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        coordinator_worktree=tmp_path,
        base_commit=BASE,
    )
    register(run, "A", tmp_path)
    first = result(run, "A")
    first = replace(first, claimed_paths=("proof/shared/result.txt",))
    accepted = run.verify_result(
        first,
        observed_branch=first.branch,
        observed_worktree=Path(first.worktree),
        observed_base_commit=BASE,
        observed_head_commit=HEAD_A,
        observed_repositories=(".",),
        observed_paths=("proof/shared/result.txt",),
        observed_validations={"validate-A": True},
        observed_evidence={"evidence-A": True},
        coordinator_token=TOKEN,
    )
    assert accepted.accepted
    run.record_durable_disposition(
        "A", kind="integrated", receipt=f"git:{HEAD_A}", coordinator_token=TOKEN
    )
    register(run, "B", tmp_path)
    second = replace(
        result(run, "B", head=HEAD_B),
        claimed_paths=("proof/shared/result.txt",),
    )

    rejected = run.verify_result(
        second,
        observed_branch=second.branch,
        observed_worktree=Path(second.worktree),
        observed_base_commit=BASE,
        observed_head_commit=HEAD_B,
        observed_repositories=(".",),
        observed_paths=("proof/shared/result.txt",),
        observed_validations={"validate-B": True},
        observed_evidence={"evidence-B": True},
        coordinator_token=TOKEN,
    )

    assert not rejected.accepted
    assert "Integrated diff collision" in " ".join(rejected.issues)


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


def test_failed_attempt_retry_uses_new_intent_and_never_duplicates(tmp_path: Path) -> None:
    built = plan(unit("A"))
    run = coordinator(built, tmp_path)
    first_packet = register(run, "A", tmp_path)
    rejected = verify(run, result(run, "A", success=False))
    assert not rejected.accepted

    run.retry("A", coordinator_token=TOKEN)
    second_intent = run.creation_intents()[0]
    assert second_intent.attempt == first_packet.attempt + 1 == 2
    assert second_intent.intent_id not in run.state.used_intents
    run.register_creation(
        second_intent,
        handle="native-a-retry",
        branch="codex/a-retry",
        worktree=tmp_path.parent / "worktree-a-retry",
        coordinator_token=TOKEN,
    )

    assert run.state.create_count == 2
    assert run.state.units["A"].attempt == 2
    assert len(run.state.used_intents) == 2


def test_every_runtime_mutator_rejects_non_coordinator_token(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    built = plan(unit("A"))
    run = coordinator(built, tmp_path)
    intent = run.creation_intents()[0]

    with pytest.raises(workflow_cli.EpicOrchestrationError) as register_error:
        run.register_creation(
            intent,
            handle="native-a",
            branch="codex/a",
            worktree=tmp_path.parent / "worktree-a",
            coordinator_token="worker-token",
        )
    assert register_error.value.code == "PW_EPIC_COORDINATOR_ONLY"

    register(run, "A", tmp_path)
    child_result = result(run, "A", success=False)
    wrong_token_calls = (
        lambda: run.verify_result(
            child_result,
            observed_branch=child_result.branch,
            observed_worktree=Path(child_result.worktree),
            observed_base_commit=BASE,
            observed_head_commit=HEAD_A,
            observed_repositories=(".",),
            observed_paths=("proof/a/result.txt",),
            observed_validations={"validate-A": True},
            observed_evidence={"evidence-A": True},
            coordinator_token="worker-token",
        ),
        lambda: run.checkpoint("A", coordinator_token="worker-token"),
        lambda: run.reconcile({}, coordinator_token="worker-token"),
        lambda: run.persist(tmp_path, coordinator_token="worker-token"),
    )
    for call in wrong_token_calls:
        with pytest.raises(workflow_cli.EpicOrchestrationError) as error:
            call()
        assert error.value.code == "PW_EPIC_COORDINATOR_ONLY"

    verify(run, child_result)
    with pytest.raises(workflow_cli.EpicOrchestrationError) as retry_error:
        run.retry("A", coordinator_token="worker-token")
    assert retry_error.value.code == "PW_EPIC_COORDINATOR_ONLY"


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


def test_creation_rejects_runtime_reconciliation_not_authorized_by_plan(
    tmp_path: Path,
) -> None:
    creation_only = plan(
        unit("A"),
        observed=("persistent-task", "isolated-worktree", "task-monitoring"),
    )
    run = coordinator(creation_only, tmp_path)

    assert run.creation_intents() == ()
    boundary = run.capability_boundary()
    assert boundary["creation_supported"] is False
    assert "immutable plan lacks" in " ".join(boundary["reasons"])


def test_generic_reconcile_fails_closed_for_epic_exact_identity_state(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    built = plan(unit("A"))
    run = coordinator(built, tmp_path)
    register(run, "A", tmp_path)
    run.persist(tmp_path, coordinator_token=TOKEN)
    stored = workflow_cli._load_delegation_runtime_state(tmp_path, "EPIC-001")
    assert stored is not None

    with pytest.raises(workflow_cli.DelegationPlanError) as error:
        workflow_cli.reconcile_delegation_runtime_state(tmp_path, built, stored, {})

    assert error.value.code == "PW_EPIC_RECONCILIATION_REQUIRES_HOST"


def test_resume_rejects_copied_or_drifted_coordinator_worktree(tmp_path: Path) -> None:
    source = tmp_path / "source"
    copied = tmp_path / "copied"
    source.mkdir()
    copied.mkdir()
    for root in (source, copied):
        (root / ".gitignore").write_text(
            ".project-workflow/runtime/delegations/\n", encoding="utf-8"
        )
    import shutil
    import subprocess

    subprocess.run(["git", "init"], cwd=source, check=True, capture_output=True)
    subprocess.run(["git", "init"], cwd=copied, check=True, capture_output=True)
    built = plan(unit("A"))
    run = coordinator(built, source)
    register(run, "A", source)
    runtime_path = run.persist(source, coordinator_token=TOKEN)
    copied_runtime = copied / runtime_path.relative_to(source)
    copied_runtime.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(runtime_path, copied_runtime)

    with pytest.raises(workflow_cli.EpicOrchestrationError) as error:
        workflow_cli.EpicOrchestrator.resume(
            root=copied,
            plan=built,
            obligations=duties("A"),
            capabilities=capabilities(),
            coordinator_token=TOKEN,
            observations={},
        )

    assert error.value.code == "PW_EPIC_RUNTIME_TARGET_MISMATCH"


@pytest.mark.parametrize(
    "changed",
    [
        {"requested": 2},
        {"authority": "different owner authority provenance"},
    ],
)
def test_resume_rejects_immutable_concurrency_or_authority_drift(
    tmp_path: Path, changed: dict[str, object]
) -> None:
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    original = plan(unit("A"))
    run = coordinator(original, tmp_path)
    run.persist(tmp_path, coordinator_token=TOKEN)
    drifted = plan(unit("A"), **changed)

    with pytest.raises(workflow_cli.EpicOrchestrationError) as error:
        workflow_cli.EpicOrchestrator.resume(
            root=tmp_path,
            plan=drifted,
            obligations=duties("A"),
            capabilities=capabilities(),
            coordinator_token=TOKEN,
            observations={},
        )

    assert error.value.code in {
        "PW_EPIC_RUNTIME_TARGET_MISMATCH",
        "PW_EPIC_RUNTIME_PLAN_MISMATCH",
    }


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
        run.assert_child_completion_observed("A", canonical_lifecycle="Review", qa_passed=True)
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


def test_epic_runtime_consumes_subagent_surface_without_persistent_creation(
    tmp_path: Path,
) -> None:
    built = plan(
        unit("A", needs="bounded-return"),
        observed=("subagent",),
        authority=None,
        capacity=1,
        requested=1,
    )
    host = capabilities(
        persistent=False,
        worktrees=False,
        monitoring=False,
        reconciliation=False,
        retirement=False,
        retirement_reconciliation=False,
        capacity=1,
    )
    host = replace(host, additional_capabilities=("subagent",))
    run = coordinator(built, tmp_path, host=host)

    assert run.creation_intents() == ()
    launch = run.launch_intents()[0]
    assert launch.executor == "subagent"
    assert launch.packet.visibility_class == "ephemeral"
    run.register_launch(
        launch,
        handle="subagent-a",
        branch=f"detached@{BASE}",
        worktree=tmp_path,
        coordinator_token=TOKEN,
    )
    accepted = verify(run, result(run, "A"))

    assert accepted.accepted
    assert run.state.units["A"].handle is None
    assert run.state.units["A"].disposition_state == "pending"
    assert run.retirement_intents() == ()


def test_task_target_uses_shared_visible_surface_lifecycle_without_losing_handle(
    tmp_path: Path,
) -> None:
    task_target = workflow_cli.DelegationTarget(
        target_id="TASK-900",
        kind="task",
        title="Durable task unit",
        lifecycle="In Progress",
        source_path=".project-workflow/tasks/TASK-900/IMPLEMENTATION.md",
        source_hash="task-plan-hash",
    )
    built = workflow_cli.build_delegation_plan(
        target=task_target,
        units=(unit("A", needs="durable-resume"),),
        requested_concurrency=1,
        available_child_capacity=1,
        observed_capabilities=(
            "persistent-task",
            "task-monitoring",
            "task-reconciliation",
        ),
        unsupported_capabilities=(
            "task-retirement",
            "task-retirement-reconciliation",
        ),
        capability_source="2026-08-20 generic host adapter",
        persistent_task_authority="owner request for this run",
    )
    host = workflow_cli.EpicHostCapabilities(
        source="2026-08-20 generic host adapter",
        current_session_verified=True,
        persistent_tasks=True,
        isolated_worktrees=False,
        monitoring=True,
        reconciliation=True,
        available_child_capacity=1,
    )
    run = workflow_cli.DelegationSurfaceOrchestrator(
        plan=built,
        obligations=duties("A"),
        capabilities=host,
        coordinator_token=TOKEN,
        coordinator_worktree=tmp_path,
        base_commit=BASE,
    )

    intent = run.launch_intents()[0]
    assert intent.packet.payload()["target"]["kind"] == "task"
    assert run.creation_intents()[0].payload()["requires"] == [
        "persistent-task",
        "task-monitoring",
        "task-reconciliation",
    ]
    run.register_launch(
        intent,
        handle="task-visible-a",
        branch="codex/task-visible-a",
        worktree=tmp_path,
        coordinator_token=TOKEN,
    )
    accepted = verify(run, result(run, "A"))

    assert accepted.accepted
    assert run.state.units["A"].handle == "task-visible-a"
    assert run.state.units["A"].visibility_class == "visible-retained"
    assert run.state.units["A"].retirement_state == "retained"
    assert run.retirement_intents() == ()


def test_active_peer_team_and_runtime_free_capacity_are_not_double_counted_on_resume(
    tmp_path: Path,
) -> None:
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    built = plan(
        unit("A", needs="peer:pair", order=0),
        unit("B", needs="bounded-return", order=1),
        authority=None,
        capacity=3,
        requested=3,
        observed=("peer-team", "peer-messaging", "subagent"),
        capability_source="2026-08-20 mixed surface adapter",
    )
    host = workflow_cli.EpicHostCapabilities(
        source="2026-08-20 mixed surface adapter",
        current_session_verified=True,
        persistent_tasks=False,
        isolated_worktrees=False,
        monitoring=False,
        reconciliation=False,
        available_child_capacity=3,
        additional_capabilities=("peer-team", "peer-messaging", "subagent"),
    )
    run = coordinator(built, tmp_path, host=host)
    peer_intent = next(item for item in run.launch_intents() if item.unit_id == "A")
    run.register_launch(
        peer_intent,
        handle="peer-a",
        branch=f"detached@{BASE}",
        worktree=tmp_path,
        coordinator_token=TOKEN,
    )
    run.persist(tmp_path, coordinator_token=TOKEN)

    resumed_host = replace(host, available_child_capacity=1)
    resumed = workflow_cli.EpicOrchestrator.resume(
        root=tmp_path,
        plan=built,
        obligations=duties("A", "B"),
        capabilities=resumed_host,
        coordinator_token=TOKEN,
        observations={
            "A": {
                "handle": "peer-a",
                "attempt": 1,
                "branch": f"detached@{BASE}",
                "worktree": str(tmp_path),
                "state": "active",
            }
        },
    )
    assert [intent.unit_id for intent in resumed.launch_intents()] == ["B"]


def test_existing_persistent_child_resumes_without_new_creation_capacity(
    tmp_path: Path,
) -> None:
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    built = plan(unit("A"), capacity=1, requested=1)
    run = coordinator(built, tmp_path, host=capabilities(capacity=1))
    register(run, "A", tmp_path)
    run.persist(tmp_path, coordinator_token=TOKEN)
    observed = run.state.units["A"]
    resumed_host = capabilities(capacity=0)

    resumed = workflow_cli.EpicOrchestrator.resume(
        root=tmp_path,
        plan=built,
        obligations=duties("A"),
        capabilities=resumed_host,
        coordinator_token=TOKEN,
        observations={
            "A": {
                "handle": observed.handle,
                "attempt": observed.attempt,
                "branch": observed.branch,
                "worktree": observed.worktree,
                "state": "active",
            }
        },
    )

    assert resumed.capability_boundary()["creation_supported"] is False
    assert resumed.capability_boundary()["resume_supported"] is True
    assert resumed.state.units["A"].state == "active"
    assert resumed.state.units["A"].handle == observed.handle


def test_visible_task_verification_disposition_and_retirement_are_separate_idempotent_steps(
    tmp_path: Path,
) -> None:
    run = coordinator(plan(unit("A")), tmp_path)
    register(run, "A", tmp_path)
    native_handle = run.state.units["A"].handle

    assert verify(run, result(run, "A")).accepted
    assert run.state.units["A"].handle == native_handle
    assert run.state.units["A"].disposition_state == "pending"
    assert run.retirement_intents() == ()

    run.record_durable_disposition(
        "A", kind="integrated", receipt=f"git:{HEAD_A}", coordinator_token=TOKEN
    )
    first = run.retirement_intents()[0]
    assert run.retirement_intents()[0].intent_id == first.intent_id
    run.register_retirement_requested(first, coordinator_token=TOKEN)
    assert run.retirement_intents()[0].intent_id == first.intent_id
    run.register_retirement_outcome(
        first,
        observed_handle=str(native_handle),
        outcome="confirmed",
        acknowledgement="codex:archived",
        coordinator_token=TOKEN,
    )
    run.register_retirement_outcome(
        first,
        observed_handle=str(native_handle),
        outcome="confirmed",
        acknowledgement="codex:archived",
        coordinator_token=TOKEN,
    )

    assert run.retirement_intents() == ()
    assert run.state.units["A"].retirement_state == "confirmed"
    assert run.state.units["A"].handle == native_handle
    with pytest.raises(workflow_cli.EpicOrchestrationError) as conflict:
        run.register_retirement_outcome(
            first,
            observed_handle=str(native_handle),
            outcome="failed",
            acknowledgement="codex:visible",
            coordinator_token=TOKEN,
        )
    assert conflict.value.code == "PW_EPIC_RETIREMENT_CONFLICT"


def test_retirement_failure_and_unknown_resume_keep_exact_handle_and_intent(
    tmp_path: Path,
) -> None:
    run = coordinator(plan(unit("A")), tmp_path)
    register(run, "A", tmp_path)
    assert verify(run, result(run, "A")).accepted
    run.record_durable_disposition(
        "A", kind="no-integration", receipt="receipt:no-change", coordinator_token=TOKEN
    )
    intent = run.retirement_intents()[0]
    run.register_retirement_requested(intent, coordinator_token=TOKEN)
    run.register_retirement_outcome(
        intent,
        observed_handle=intent.handle,
        outcome="failed",
        acknowledgement="codex:archive-failed",
        coordinator_token=TOKEN,
    )

    assert run.state.units["A"].handle == intent.handle
    assert run.retirement_intents() == ()
    run.retry_retirement("A", coordinator_token=TOKEN)
    assert run.retirement_intents()[0].intent_id == intent.intent_id
    run.register_retirement_requested(intent, coordinator_token=TOKEN)
    run.reconcile_retirements({}, coordinator_token=TOKEN)

    assert run.state.units["A"].retirement_state == "unknown"
    assert run.state.units["A"].handle == intent.handle


def test_legacy_epic_runtime_migrates_visible_work_to_conservative_retention(
    tmp_path: Path,
) -> None:
    run = coordinator(plan(unit("A")), tmp_path)
    register(run, "A", tmp_path)
    legacy = workflow_cli._epic_orchestration_state_payload(run.state)
    legacy["schema_version"] = 1
    legacy["integrated_paths"] = legacy.pop("verified_paths")
    raw_unit = legacy["units"]["A"]
    for key in (
        "executor",
        "visibility_class",
        "retention_policy",
        "disposition_state",
        "disposition_receipt",
        "attention_reasons",
        "owner_promoted",
        "explicit_retain_reason",
        "retirement_state",
        "retirement_intent_id",
        "retirement_ack",
        "prior_handles",
    ):
        raw_unit.pop(key)

    migrated = workflow_cli._epic_orchestration_state_from_payload(legacy)
    restored = migrated.units["A"]

    assert migrated.schema_version == 2
    assert migrated.migrated_from_version == 1
    assert restored.visibility_class == "visible-retained"
    assert restored.retention_policy == "retain"
    assert restored.disposition_state == "pending"
    assert restored.retirement_state == "retained"
    assert restored.handle == "native-a"


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


def test_failed_and_orphaned_runtime_round_trip_without_worker_failure_text(
    tmp_path: Path,
) -> None:
    import subprocess

    failed_root = tmp_path / "failed"
    orphan_root = tmp_path / "orphan"
    for root in (failed_root, orphan_root):
        root.mkdir()
        (root / ".gitignore").write_text(
            ".project-workflow/runtime/delegations/\n", encoding="utf-8"
        )
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)

    built = plan(unit("A"))
    failed = coordinator(built, failed_root)
    register(failed, "A", failed_root, suffix="failed")
    private_text = "PRIVATE TOKEN transcript must never persist"
    returned = replace(result(failed, "A", success=False), failure_reason=private_text)
    rejected = verify(failed, returned)
    assert not rejected.accepted
    failed_payload = workflow_cli._epic_orchestration_state_payload(failed.state)
    assert private_text not in json.dumps(failed_payload)
    duplicated = dict(failed_payload)
    duplicated["create_count"] = 2
    duplicated["used_intents"] = failed_payload["used_intents"] * 2
    duplicated["used_handles"] = failed_payload["used_handles"] * 2
    with pytest.raises(workflow_cli.EpicOrchestrationError) as duplicate_identity:
        workflow_cli._epic_orchestration_state_from_payload(duplicated)
    assert duplicate_identity.value.code == "PW_EPIC_RUNTIME_INVALID"
    failed.persist(failed_root, coordinator_token=TOKEN)
    failed_resumed = workflow_cli.EpicOrchestrator.resume(
        root=failed_root,
        plan=built,
        obligations=duties("A"),
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        observations={},
    )
    assert failed_resumed.state.units["A"].issues == ("PW_EPIC_CHILD_FAILED",)

    orphan = coordinator(built, orphan_root)
    register(orphan, "A", orphan_root, suffix="orphan")
    orphan.persist(orphan_root, coordinator_token=TOKEN)
    orphaned = workflow_cli.EpicOrchestrator.resume(
        root=orphan_root,
        plan=built,
        obligations=duties("A"),
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        observations={},
    )
    assert orphaned.state.units["A"].issues == ("PW_EPIC_HANDLE_ORPHANED",)
    orphaned.persist(orphan_root, coordinator_token=TOKEN)
    reloaded = workflow_cli.EpicOrchestrator.resume(
        root=orphan_root,
        plan=built,
        obligations=duties("A"),
        capabilities=capabilities(),
        coordinator_token=TOKEN,
        observations={},
    )
    assert reloaded.state.units["A"].state == "orphaned"


@pytest.mark.parametrize("command", ["status", "state-init", "state-reconcile"])
def test_delegate_cli_surfaces_malformed_epic_runtime_as_stable_error(
    monkeypatch: pytest.MonkeyPatch, command: str
) -> None:
    built = plan(unit("A"))
    monkeypatch.setattr(workflow_cli, "_delegation_plan_from_args", lambda root, args: built)
    monkeypatch.setattr(
        workflow_cli,
        "_load_delegation_runtime_state",
        lambda root, target_id: (_ for _ in ()).throw(
            workflow_cli.EpicOrchestrationError(
                "PW_EPIC_RUNTIME_PRIVATE_FIELD", "Epic runtime contains forbidden fields."
            )
        ),
    )
    args = Namespace(format="json", observed_handles="unused.json")

    with pytest.raises(SystemExit) as error:
        if command == "status":
            workflow_cli.cmd_delegate_status(args)
        elif command == "state-init":
            workflow_cli.cmd_delegate_state_init(args)
        else:
            workflow_cli.cmd_delegate_state_reconcile(args)

    assert str(error.value).startswith("PW_EPIC_RUNTIME_PRIVATE_FIELD:")
