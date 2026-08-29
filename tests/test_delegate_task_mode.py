from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli

TOKEN = "coordinator-only-token"
SHARED_HASH = "shared-state-sha256"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TASK_CAPABILITY_SOURCE = "2026-08-20 current Codex session"
COMMANDS = (
    (sys.executable, "-m", "project_workflow.cli"),
    (str(Path(sys.executable).parent / "project"),),
    (str(PROJECT_ROOT / ".project-workflow/cli/workflow"),),
)


def unit(
    unit_id: str,
    *,
    dependencies: tuple[str, ...] = (),
    scope: tuple[str, ...] | None = None,
    parallel_safe: bool = True,
    state: str = "pending",
    order: int = 0,
) -> workflow_cli.DelegationUnit:
    return workflow_cli.DelegationUnit(
        unit_id=unit_id,
        title=f"Unit {unit_id}",
        dependencies=dependencies,
        write_scope=scope or (f"src/{unit_id.lower()}",),
        parallel_safe=parallel_safe,
        canonical_state=state,
        source_order=order,
        source_path=".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",
    )


def plan(
    *units: workflow_cli.DelegationUnit,
    requested_concurrency: int | None = None,
) -> workflow_cli.DelegationPlan:
    requested = requested_concurrency or max(1, len(units))
    return workflow_cli.build_delegation_plan(
        target=workflow_cli.DelegationTarget(
            target_id="TASK-001",
            kind="task",
            title="Task mode",
            lifecycle="In Progress",
            source_path=".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",
            source_hash="plan-hash",
        ),
        units=tuple(units),
        requested_concurrency=requested,
        available_child_capacity=requested,
        observed_capabilities=("subagent",),
        capability_source=TASK_CAPABILITY_SOURCE,
    )


def duties(*unit_ids: str) -> dict[str, workflow_cli.TaskExecutionObligations]:
    return {
        unit_id: workflow_cli.TaskExecutionObligations(
            acceptance_criteria=(f"AC-{unit_id}",),
            validations=(f"test-{unit_id}",),
            evidence=(f"evidence-{unit_id}",),
        )
        for unit_id in unit_ids
    }


def coordinator(
    built: workflow_cli.DelegationPlan,
    *,
    capacity: int = 2,
    verified: bool = True,
    bounded_subagents: bool = True,
) -> workflow_cli.TaskOrchestrator:
    return workflow_cli.TaskOrchestrator(
        plan=built,
        obligations=duties(*(item.unit_id for item in built.units)),
        capabilities=workflow_cli.TaskHostCapabilities(
            source=built.capability_source if verified else "",
            current_session_verified=verified,
            bounded_subagents=bounded_subagents,
            available_child_capacity=capacity,
        ),
        coordinator_token=TOKEN,
        shared_state_hash=SHARED_HASH,
    )


def result(
    run: workflow_cli.TaskOrchestrator,
    unit_id: str,
    handle: str,
    path: str,
    *,
    success: bool = True,
    validation: bool = True,
    evidence: bool = True,
    shared_premise_valid: bool = True,
) -> workflow_cli.TaskWorkerResult:
    return workflow_cli.TaskWorkerResult(
        unit_id=unit_id,
        handle=handle,
        success=success,
        claimed_paths=(path,),
        validations={f"test-{unit_id}": validation},
        evidence={f"evidence-{unit_id}": evidence},
        baseline_hash=SHARED_HASH,
        shared_state_hash=SHARED_HASH,
        plan_fingerprint=run.state.plan_fingerprint,
        attempt=run.state.units[unit_id].attempt,
        shared_premise_valid=shared_premise_valid,
        failure_reason="injected failure" if not success else "",
    )


def test_executor_selection_uses_verified_capacity_safety_dependencies_and_no_tasks() -> None:
    built = plan(
        unit("A", order=0),
        unit("B", order=1),
        unit("C", parallel_safe=False, order=2),
        unit("D", dependencies=("A",), order=3),
    )
    run = coordinator(built, capacity=2)
    decisions = {item.unit_id: item for item in run.decisions()}

    assert decisions["A"].executor == decisions["B"].executor == "subagent"
    assert decisions["A"].launchable and decisions["B"].launchable
    assert decisions["C"].executor == "subagent"
    assert not decisions["C"].launchable
    assert decisions["D"].executor == "none"

    packet = run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    assert packet.payload()["persistent_task_intent"] is None

    fallback = coordinator(built, capacity=0, bounded_subagents=False)
    assert fallback.decisions()[0].executor == "none"
    assert "current runtime lacks verified subagent" in fallback.decisions()[0].reason


def test_subagent_capability_must_be_verified_in_the_current_session() -> None:
    with pytest.raises(workflow_cli.TaskOrchestrationError) as caught:
        workflow_cli.TaskHostCapabilities(
            source="",
            current_session_verified=False,
            bounded_subagents=True,
            available_child_capacity=2,
        )
    assert caught.value.code == "PW_TASK_CAPABILITY_UNVERIFIED"


def test_packet_is_complete_bounded_and_coordinator_is_single_writer() -> None:
    run = coordinator(plan(unit("A")))
    packet = run.launch("A", handle="bounded-a", coordinator_token=TOKEN).payload()

    assert packet["target"] == {
        "id": "TASK-001",
        "kind": "task",
        "authority_source": ".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",
        "authority_hash": "plan-hash",
    }
    assert packet["unit"] == {"id": "A", "title": "Unit A"}
    assert packet["acceptance_criteria"] == ["AC-A"]
    assert packet["scope"] == {"write_prefixes": ["src/a"], "repositories": ["."]}
    assert packet["obligations"] == {
        "validation": ["test-A"],
        "evidence": ["evidence-A"],
    }
    assert len(packet["forbidden_actions"]) == 4
    assert len(packet["stop_conditions"]) == 4
    assert "full conversation history" in packet["invalid_substitutes"][-1]
    assert packet["return_contract"][-1] == ("dependency result and shared-premise validity")

    with pytest.raises(workflow_cli.TaskOrchestrationError) as caught:
        run.checkpoint("A", coordinator_token="worker-token")
    assert caught.value.code == "PW_TASK_COORDINATOR_ONLY"


def test_packet_obligations_fail_closed_when_empty_duplicate_or_invalid() -> None:
    with pytest.raises(workflow_cli.TaskOrchestrationError) as empty:
        workflow_cli.TaskExecutionObligations((), (), (), ())
    assert empty.value.code == "PW_TASK_PACKET_OBLIGATIONS_INVALID"
    with pytest.raises(workflow_cli.TaskOrchestrationError) as duplicate:
        workflow_cli.TaskExecutionObligations(("AC1", "AC1"), ("test",), ("evidence",), (".",))
    assert duplicate.value.code == "PW_TASK_PACKET_OBLIGATIONS_INVALID"
    with pytest.raises(workflow_cli.TaskOrchestrationError) as invalid_repo:
        workflow_cli.TaskExecutionObligations(("AC1",), ("test",), ("evidence",), ("../repo",))
    assert invalid_repo.value.code == "PW_TASK_PACKET_OBLIGATIONS_INVALID"


def test_overlap_is_rejected_before_launch_and_capacity_is_bounded() -> None:
    built = plan(
        unit("A", scope=("src/shared",), order=0),
        unit("B", scope=("src/shared/child",), parallel_safe=False, order=1),
        unit("C", scope=("src/other",), order=2),
    )
    run = coordinator(built, capacity=2)
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)

    with pytest.raises(workflow_cli.TaskOrchestrationError) as caught:
        run.launch("B", handle="bounded-b", coordinator_token=TOKEN)
    assert caught.value.code == "PW_TASK_WRITE_SCOPE_COLLISION"
    assert run.state.units["B"].attempt == 0

    run.launch("C", handle="bounded-c", coordinator_token=TOKEN)
    assert len(run.summary()["in_flight"]) == 2
    assert not any(item.launchable for item in run.decisions())


def test_verification_rejects_scope_and_blocks_descendants_but_not_unrelated_work() -> None:
    built = plan(
        unit("A", order=0),
        unit("B", dependencies=("A",), order=1),
        unit("C", order=2),
    )
    run = coordinator(built)
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    outcome = run.verify_result(
        result(run, "A", "bounded-a", "outside/a.py"),
        observed_paths=("outside/a.py",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )

    assert not outcome.accepted
    summary = run.summary()
    assert summary["failed"] == ["A"]
    assert summary["halted"] == ["B", "C"]
    assert not any(item.launchable for item in run.decisions())


def test_failed_validation_requires_retry_and_corrected_verification_before_release() -> None:
    run = coordinator(plan(unit("A"), unit("B", dependencies=("A",), order=1)))
    run.launch("A", handle="bounded-a-1", coordinator_token=TOKEN)
    rejected = run.verify_result(
        result(run, "A", "bounded-a-1", "src/a/change.py", validation=False),
        observed_paths=("src/a/change.py",),
        observed_validations={"test-A": False},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    assert not rejected.accepted
    assert run.state.units["B"].state == "blocked"

    run.retry("A", coordinator_token=TOKEN)
    assert run.state.units["B"].state == "pending"
    packet = run.launch("A", handle="bounded-a-2", coordinator_token=TOKEN)
    assert packet.attempt == 2
    accepted = run.verify_result(
        result(run, "A", "bounded-a-2", "src/a/change.py"),
        observed_paths=("src/a/change.py",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    assert accepted.accepted
    assert accepted.newly_eligible == ("B",)


def test_intervening_diff_collision_is_rejected_before_dependency_release() -> None:
    built = plan(
        unit("A", scope=("src/a",), order=0),
        unit("B", scope=("src/b",), order=1),
    )
    run = coordinator(built)
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    run.launch("B", handle="bounded-b", coordinator_token=TOKEN)
    run.verify_result(
        result(run, "A", "bounded-a", "src/a/file.py"),
        observed_paths=("src/a/file.py",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    # Simulate a coordinator-observed collision despite the planned disjoint prefix.
    run.state.integrated_paths.append(
        (run.state.integration_revision, "external", ("src/b/file.py",))
    )
    run.state.integration_revision += 1
    rejected = run.verify_result(
        result(run, "B", "bounded-b", "src/b/file.py"),
        observed_paths=("src/b/file.py",),
        observed_validations={"test-B": True},
        observed_evidence={"evidence-B": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    assert not rejected.accepted
    assert "collision" in " ".join(rejected.issues).lower()


def test_shared_premise_failure_halts_new_launches_and_preserves_in_flight_checkpoint() -> None:
    run = coordinator(plan(unit("A"), unit("B", order=1), unit("C", order=2)))
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    run.launch("B", handle="bounded-b", coordinator_token=TOKEN)
    rejected = run.verify_result(
        result(
            run,
            "A",
            "bounded-a",
            "src/a/file.py",
            success=False,
            shared_premise_valid=False,
        ),
        observed_paths=("src/a/file.py",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    assert not rejected.accepted
    summary = run.summary()
    assert summary["failed"] == ["A"]
    assert summary["in_flight"] == ["B"]
    assert summary["halted"] == ["C"]
    run.checkpoint("B", coordinator_token=TOKEN)
    assert run.state.units["B"].checkpointed
    assert run.summary()["in_flight"] == []
    assert run.summary()["halted"] == ["B", "C"]
    assert not any(item.launchable for item in run.decisions())


def test_in_flight_return_after_shared_failure_is_halted_not_integrated() -> None:
    run = coordinator(plan(unit("A"), unit("B", order=1)))
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    run.launch("B", handle="bounded-b", coordinator_token=TOKEN)
    run.verify_result(
        result(
            run,
            "A",
            "bounded-a",
            "src/a/file.py",
            success=False,
            shared_premise_valid=False,
        ),
        observed_paths=("src/a/file.py",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    halted = run.verify_result(
        result(run, "B", "bounded-b", "src/b/file.py"),
        observed_paths=("src/b/file.py",),
        observed_validations={"test-B": True},
        observed_evidence={"evidence-B": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    assert not halted.accepted and halted.state == "halted"
    assert run.state.integration_revision == 0
    assert run.summary()["halted"] == ["B"]


def test_worker_scope_cannot_include_shared_workflow_state() -> None:
    for protected_scope in (
        ".project-workflow",
        ".project-workflow/BACKLOG.md",
        ".project-workflow/config.json",
        ".project-workflow/tasks/TASK-001/evidence/live.json",
    ):
        protected = coordinator(plan(unit("A", scope=(protected_scope,))))
        decision = protected.decisions()[0]
        assert decision.executor == "coordinator" and decision.launchable
        with pytest.raises(workflow_cli.TaskOrchestrationError) as caught:
            protected.launch("A", handle="must-not-launch", coordinator_token=TOKEN)
        assert caught.value.code == "PW_TASK_COORDINATOR_EXECUTION_REQUIRED"

    run = coordinator(plan(unit("A", scope=(".project-workflow/tasks/TASK-001",))))
    completed = run.complete_coordinator_unit(
        "A",
        observed_paths=(".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        provenance="coordinator reviewed canonical diff",
        coordinator_token=TOKEN,
    )
    assert completed.accepted

    allowed_helper = plan(unit("A", scope=(".project-workflow/cli/workflow.py",)))
    assert coordinator(allowed_helper).decisions()[0].executor == "subagent"

    git_control = coordinator(plan(unit("A", scope=(".git/config",))))
    assert git_control.decisions()[0].executor == "coordinator"
    with pytest.raises(workflow_cli.TaskOrchestrationError) as git_launch:
        git_control.launch("A", handle="must-not-launch", coordinator_token=TOKEN)
    assert git_launch.value.code == "PW_TASK_COORDINATOR_EXECUTION_REQUIRED"

    unexpected_shared_path = coordinator(plan(unit("A")))
    unexpected_shared_path.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    rejected = unexpected_shared_path.verify_result(
        result(
            unexpected_shared_path,
            "A",
            "bounded-a",
            ".project-workflow/BACKLOG.md",
        ),
        observed_paths=(".project-workflow/BACKLOG.md",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    assert not rejected.accepted
    assert not unexpected_shared_path.state.shared_premise_valid


def test_coordinator_observations_override_worker_validation_and_evidence_claims() -> None:
    run = coordinator(plan(unit("A")))
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    worker_claims_pass = result(run, "A", "bounded-a", "src/a/file.py")
    rejected = run.verify_result(
        worker_claims_pass,
        observed_paths=("src/a/file.py",),
        observed_validations={"test-A": False},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    assert not rejected.accepted
    assert "coordinator observations" in " ".join(rejected.issues)


def test_unsafe_execution_is_exclusive_in_both_launch_orders() -> None:
    unsafe_first = coordinator(plan(unit("A", parallel_safe=False), unit("B", order=1)), capacity=2)
    decisions = {item.unit_id: item for item in unsafe_first.decisions()}
    assert decisions["A"].executor == "subagent" and decisions["A"].launchable
    assert not decisions["B"].launchable
    unsafe_first.launch("A", handle="unsafe-a", coordinator_token=TOKEN)
    assert not next(item for item in unsafe_first.decisions() if item.unit_id == "B").launchable

    safe_first = coordinator(plan(unit("A"), unit("B", parallel_safe=False, order=1)), capacity=2)
    decisions = {item.unit_id: item for item in safe_first.decisions()}
    assert decisions["A"].launchable
    assert not decisions["B"].launchable


def test_requested_concurrency_bounds_larger_observed_capacity() -> None:
    run = coordinator(
        plan(unit("A"), unit("B", order=1), requested_concurrency=1),
        capacity=3,
    )
    decisions = {item.unit_id: item for item in run.decisions()}
    assert decisions["A"].launchable
    assert not decisions["B"].launchable
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    with pytest.raises(workflow_cli.TaskOrchestrationError) as caught:
        run.launch("B", handle="bounded-b", coordinator_token=TOKEN)
    assert caught.value.code == "PW_TASK_NOT_LAUNCHABLE"


def test_refreshed_task_capacity_is_free_capacity_not_total_capacity() -> None:
    run = coordinator(
        plan(unit("A"), unit("B", order=1), unit("C", order=2)),
        capacity=3,
    )
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    run.capabilities = workflow_cli.TaskHostCapabilities(
        source=TASK_CAPABILITY_SOURCE,
        current_session_verified=True,
        bounded_subagents=True,
        available_child_capacity=2,
    )

    decisions = {item.unit_id: item for item in run.decisions()}
    assert decisions["B"].launchable
    assert decisions["C"].launchable


def test_subset_plan_preserves_omitted_canonically_complete_dependency() -> None:
    target = workflow_cli.DelegationTarget(
        target_id="TASK-001",
        kind="task",
        title="Subset",
        lifecycle="In Progress",
        source_path=".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",
        source_hash="subset-hash",
    )
    built = workflow_cli.build_delegation_plan(
        target=target,
        units=(
            unit("A", state="complete"),
            unit("B", dependencies=("A",), order=1),
        ),
        selected_unit_ids=("B",),
        requested_concurrency=1,
        available_child_capacity=1,
        observed_capabilities=("subagent",),
        capability_source=TASK_CAPABILITY_SOURCE,
    )
    run = coordinator(built, capacity=1)
    packet = run.launch("B", handle="bounded-b", coordinator_token=TOKEN)
    assert packet.verified_dependencies == ("A",)


def test_retry_does_not_revive_canonically_blocked_descendant() -> None:
    run = coordinator(
        plan(
            unit("A"),
            unit("B", dependencies=("A",), state="blocked", order=1),
        )
    )
    run.launch("A", handle="bounded-a-1", coordinator_token=TOKEN)
    run.verify_result(
        result(run, "A", "bounded-a-1", "src/a/file.py", validation=False),
        observed_paths=("src/a/file.py",),
        observed_validations={"test-A": False},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    run.retry("A", coordinator_token=TOKEN)
    assert run.state.units["B"].canonical_blocked
    assert run.state.units["B"].state == "blocked"


def test_attempt_fingerprint_and_global_handle_ownership_reject_stale_results() -> None:
    run = coordinator(plan(unit("A"), unit("B", order=1)))
    run.launch("A", handle="bounded-a-1", coordinator_token=TOKEN)
    with pytest.raises(workflow_cli.TaskOrchestrationError) as reused:
        run.launch("B", handle="bounded-a-1", coordinator_token=TOKEN)
    assert reused.value.code == "PW_TASK_HANDLE_REUSE"

    run.verify_result(
        result(run, "A", "bounded-a-1", "src/a/file.py", validation=False),
        observed_paths=("src/a/file.py",),
        observed_validations={"test-A": False},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    run.retry("A", coordinator_token=TOKEN)
    run.launch("A", handle="bounded-a-2", coordinator_token=TOKEN)
    stale = result(run, "A", "bounded-a-2", "src/a/file.py")
    stale = workflow_cli.TaskWorkerResult(**{**stale.__dict__, "attempt": 1})
    with pytest.raises(workflow_cli.TaskOrchestrationError) as caught:
        run.verify_result(
            stale,
            observed_paths=("src/a/file.py",),
            observed_validations={"test-A": True},
            observed_evidence={"evidence-A": True},
            current_shared_state_hash=SHARED_HASH,
            coordinator_token=TOKEN,
        )
    assert caught.value.code == "PW_TASK_RESULT_STALE"


def test_coordinator_rebaseline_preserves_in_flight_baseline_and_updates_new_packets() -> None:
    run = coordinator(plan(unit("A"), unit("B", order=1), unit("C", order=2)), capacity=2)
    alpha = run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    beta = run.launch("B", handle="bounded-b", coordinator_token=TOKEN)
    run.verify_result(
        result(run, "A", "bounded-a", "src/a/file.py"),
        observed_paths=("src/a/file.py",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    run.rebaseline_shared_state(
        "shared-state-after-a",
        reason="IMPLEMENTATION row A marked Done",
        coordinator_token=TOKEN,
    )
    accepted_beta = run.verify_result(
        result(run, "B", "bounded-b", "src/b/file.py"),
        observed_paths=("src/b/file.py",),
        observed_validations={"test-B": True},
        observed_evidence={"evidence-B": True},
        current_shared_state_hash="shared-state-after-a",
        coordinator_token=TOKEN,
    )
    assert accepted_beta.accepted
    gamma = run.launch("C", handle="bounded-c", coordinator_token=TOKEN)
    assert alpha.baseline_hash == beta.baseline_hash == SHARED_HASH
    assert gamma.baseline_hash == "shared-state-after-a"


def test_persisted_resume_preserves_attempts_active_handles_and_orphans(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    workflow = tmp_path / ".project-workflow"
    task_dir = workflow / "tasks" / "TASK-001-Persisted"
    task_dir.mkdir(parents=True)
    (workflow / "TRACKER.md").write_text(
        "| ID | Title | Status | Docs |\n"
        "|---|---|---|---|\n"
        "| TASK-001 | Persisted | In Progress | "
        "tasks/TASK-001-Persisted/IMPLEMENTATION.md |\n",
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| A | A | Work | AC1 | Test | To Do | | src/a | Yes |\n"
        "| B | B | Work | AC1 | Test | To Do | A | src/b | Yes |\n",
        encoding="utf-8",
    )
    (task_dir / "REQUIREMENTS.md").write_text("# Requirements\n", encoding="utf-8")
    target, units = workflow_cli._resolve_delegation_target(tmp_path, ("TASK-001",))
    built = workflow_cli.build_delegation_plan(
        target=target,
        units=units,
        requested_concurrency=2,
        available_child_capacity=2,
        observed_capabilities=("subagent",),
        capability_source=TASK_CAPABILITY_SOURCE,
    )
    run = coordinator(built)
    run.launch("A", handle="bounded-a-1", coordinator_token=TOKEN)
    runtime_path = run.persist(tmp_path, coordinator_token=TOKEN)
    assert runtime_path.exists()
    status = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_workflow.cli",
            "delegate",
            "status",
            "--id",
            "TASK-001",
            "--requested-concurrency",
            "2",
            "--available-child-capacity",
            "2",
            "--observed-capability",
            "subagent",
            "--capability-source",
            "2026-08-19 refreshed current Codex session",
            "--format",
            "json",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert status.returncode == 0, status.stderr
    status_payload = json.loads(status.stdout)
    assert status_payload["runtime_summary"]["active"] == ["A"]
    assert status_payload["runtime_summary"]["attempts"]["A"] == 1
    assert "A" in status_payload["runtime_summary"]["no_relaunch"]
    stored = workflow_cli._load_delegation_runtime_state(tmp_path, "TASK-001")
    assert stored is not None
    mismatched = workflow_cli.reconcile_delegation_runtime_state(
        tmp_path,
        built,
        stored,
        {
            "A": {
                "kind": "subagent",
                "id": "different-worker",
                "worktree": str(tmp_path),
                "state": "active",
            }
        },
    )
    mismatch_state = workflow_cli._task_orchestration_state_from_payload(
        mismatched["task_orchestration"]
    )
    assert mismatch_state.units["A"].state == "orphaned"

    refreshed_capabilities = workflow_cli.TaskHostCapabilities(
        source="refreshed current Codex session",
        current_session_verified=True,
        bounded_subagents=True,
        available_child_capacity=1,
    )
    resumed = workflow_cli.TaskOrchestrator.resume(
        root=tmp_path,
        plan=built,
        obligations=duties("A", "B"),
        capabilities=refreshed_capabilities,
        coordinator_token=TOKEN,
    )
    assert resumed.state.units["A"].attempt == 1
    assert resumed.capabilities.available_child_capacity == 1
    with pytest.raises(workflow_cli.TaskOrchestrationError) as duplicate:
        resumed.launch("A", handle="duplicate", coordinator_token=TOKEN)
    assert duplicate.value.code == "PW_TASK_DUPLICATE_LAUNCH"

    resumed.reconcile({}, coordinator_token=TOKEN)
    resumed.persist(tmp_path, coordinator_token=TOKEN)
    restarted = workflow_cli.TaskOrchestrator.resume(
        root=tmp_path,
        plan=built,
        obligations=duties("A", "B"),
        capabilities=run.capabilities,
        coordinator_token=TOKEN,
    )
    assert restarted.summary()["orphaned"] == ["A"]
    restarted.retry("A", coordinator_token=TOKEN)
    packet = restarted.launch("A", handle="bounded-a-2", coordinator_token=TOKEN)
    assert packet.attempt == 2
    accepted = restarted.verify_result(
        result(restarted, "A", "bounded-a-2", "src/a/file.py"),
        observed_paths=("src/a/file.py",),
        observed_validations={"test-A": True},
        observed_evidence={"evidence-A": True},
        current_shared_state_hash=SHARED_HASH,
        coordinator_token=TOKEN,
    )
    assert accepted.accepted
    restarted.rebaseline_shared_state(
        "shared-after-canonical-a",
        reason="coordinator marked implementation row A Done",
        coordinator_token=TOKEN,
    )
    restarted.persist(tmp_path, coordinator_token=TOKEN)
    implementation_path = task_dir / "IMPLEMENTATION.md"
    implementation_path.write_text(
        implementation_path.read_text(encoding="utf-8").replace(
            "| A | A | Work | AC1 | Test | To Do |",
            "| A | A | Work | AC1 | Test | Done |",
        ),
        encoding="utf-8",
    )
    refreshed_target, refreshed_units = workflow_cli._resolve_delegation_target(
        tmp_path, ("TASK-001",)
    )
    refreshed_plan = workflow_cli.build_delegation_plan(
        target=refreshed_target,
        units=refreshed_units,
        requested_concurrency=2,
        available_child_capacity=2,
        observed_capabilities=("subagent",),
        capability_source=TASK_CAPABILITY_SOURCE,
    )
    after_canonical_write = workflow_cli.TaskOrchestrator.resume(
        root=tmp_path,
        plan=refreshed_plan,
        obligations=duties("A", "B"),
        capabilities=refreshed_capabilities,
        coordinator_token=TOKEN,
    )
    assert after_canonical_write.state.units["A"].state == "done"
    assert after_canonical_write.state.units["A"].completion_provenance.startswith("canonical:")
    after_canonical_write.persist(tmp_path, coordinator_token=TOKEN)
    resumed_again = workflow_cli.TaskOrchestrator.resume(
        root=tmp_path,
        plan=refreshed_plan,
        obligations=duties("A", "B"),
        capabilities=refreshed_capabilities,
        coordinator_token=TOKEN,
    )
    assert resumed_again.state.units["A"].state == "done"


@pytest.mark.parametrize("launch_before_block", (False, True))
def test_resume_applies_refreshed_canonical_block_without_relaunch(
    tmp_path: Path, launch_before_block: bool
) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    workflow = tmp_path / ".project-workflow"
    task_dir = workflow / "tasks" / "TASK-001-Blocked"
    task_dir.mkdir(parents=True)
    (workflow / "TRACKER.md").write_text(
        "| ID | Title | Status | Docs |\n"
        "|---|---|---|---|\n"
        "| TASK-001 | Blocked | In Progress | "
        "tasks/TASK-001-Blocked/IMPLEMENTATION.md |\n",
        encoding="utf-8",
    )
    implementation = task_dir / "IMPLEMENTATION.md"
    implementation.write_text(
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| A | A | Work | AC1 | Test | To Do | | src/a | Yes |\n",
        encoding="utf-8",
    )
    (task_dir / "REQUIREMENTS.md").write_text("# Requirements\n", encoding="utf-8")
    target, units = workflow_cli._resolve_delegation_target(tmp_path, ("TASK-001",))
    initial_plan = workflow_cli.build_delegation_plan(
        target=target,
        units=units,
        requested_concurrency=1,
        available_child_capacity=1,
        observed_capabilities=("subagent",),
        capability_source=TASK_CAPABILITY_SOURCE,
    )
    run = coordinator(initial_plan, capacity=1)
    if launch_before_block:
        run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    run.persist(tmp_path, coordinator_token=TOKEN)

    implementation.write_text(
        implementation.read_text(encoding="utf-8").replace("| To Do |", "| Blocked |"),
        encoding="utf-8",
    )
    refreshed_target, refreshed_units = workflow_cli._resolve_delegation_target(
        tmp_path, ("TASK-001",)
    )
    refreshed_plan = workflow_cli.build_delegation_plan(
        target=refreshed_target,
        units=refreshed_units,
        requested_concurrency=1,
        available_child_capacity=1,
        observed_capabilities=("subagent",),
        capability_source=TASK_CAPABILITY_SOURCE,
    )
    resumed = workflow_cli.TaskOrchestrator.resume(
        root=tmp_path,
        plan=refreshed_plan,
        obligations=duties("A"),
        capabilities=run.capabilities,
        coordinator_token=TOKEN,
    )
    assert resumed.state.units["A"].state == "blocked"
    assert resumed.state.units["A"].canonical_blocked
    assert resumed.state.units["A"].handle is None
    assert not resumed.decisions()[0].launchable
    with pytest.raises(workflow_cli.TaskOrchestrationError) as caught:
        resumed.launch("A", handle="replacement", coordinator_token=TOKEN)
    assert caught.value.code == "PW_TASK_RETRY_REQUIRED"


def test_reconcile_resume_orphan_retry_and_no_duplicate_semantics() -> None:
    run = coordinator(plan(unit("A"), unit("B", order=1)))
    run.launch("A", handle="bounded-a", coordinator_token=TOKEN)
    run.reconcile(
        {"A": {"id": "bounded-a", "kind": "subagent", "state": "active"}},
        coordinator_token=TOKEN,
    )
    with pytest.raises(workflow_cli.TaskOrchestrationError) as duplicate:
        run.launch("A", handle="bounded-a-duplicate", coordinator_token=TOKEN)
    assert duplicate.value.code == "PW_TASK_DUPLICATE_LAUNCH"

    run.reconcile({}, coordinator_token=TOKEN)
    assert run.summary()["orphaned"] == ["A"]
    run.retry("A", coordinator_token=TOKEN)
    run.launch("A", handle="bounded-a-retry", coordinator_token=TOKEN)
    run.reconcile(
        {"A": {"id": "bounded-a-retry", "kind": "subagent", "state": "completed"}},
        coordinator_token=TOKEN,
    )
    assert run.summary()["in_flight"] == ["A"]
    with pytest.raises(workflow_cli.TaskOrchestrationError) as returned_duplicate:
        run.launch("A", handle="duplicate", coordinator_token=TOKEN)
    assert returned_duplicate.value.code == "PW_TASK_DUPLICATE_LAUNCH"

    with pytest.raises(workflow_cli.TaskOrchestrationError) as unverified_canonical:
        run.reconcile(
            {},
            canonical_completed={"A": "unrefreshed assertion"},
            coordinator_token=TOKEN,
        )
    assert unverified_canonical.value.code == "PW_TASK_COMPLETION_PROVENANCE_INVALID"


def test_runtime_testing_gate_rejects_force_until_every_unit_is_done() -> None:
    run = coordinator(plan(unit("A"), unit("B", state="complete", order=1)))
    with pytest.raises(workflow_cli.TaskOrchestrationError) as caught:
        run.assert_testing_allowed(force=True)
    assert caught.value.code == "PW_TASK_TESTING_INCOMPLETE"
    assert "--force cannot bypass" in caught.value.message

    run.state.units["A"].state = "done"
    run.assert_testing_allowed(force=True)


def write_cli_fixture(root: Path, *, row_status: str | None, malformed: bool = False) -> Path:
    workflow = root / ".project-workflow"
    task_dir = workflow / "tasks" / "TASK-001-Task-Mode"
    task_dir.mkdir(parents=True)
    implementation = task_dir / "IMPLEMENTATION.md"
    row = ""
    if malformed:
        row = "| 1 | Work | Do work | AC1 | Verify |\n"
    elif row_status is not None:
        row = f"| 1 | Work | Do work | AC1 | Verify | {row_status} |\n"
    implementation.write_text(
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "|---|---|---|---|---|---|\n" + row,
        encoding="utf-8",
    )
    (task_dir / "REQUIREMENTS.md").write_text("# Requirements\n", encoding="utf-8")
    (workflow / "TRACKER.md").write_text(
        "| ID | Title | Status | Docs |\n"
        "|---|---|---|---|\n"
        "| TASK-001 | Task Mode | In Progress | "
        "tasks/TASK-001-Task-Mode/IMPLEMENTATION.md |\n",
        encoding="utf-8",
    )
    return workflow / "TRACKER.md"


def write_epic_child_cli_fixture(root: Path, *, row_status: str) -> Path:
    workflow = root / ".project-workflow"
    epic_dir = workflow / "tasks" / "EPIC-001-Task-Mode"
    child_dir = epic_dir / "TASK-001-Child"
    child_dir.mkdir(parents=True)
    parent_requirements = workflow_cli._requirements_with_approval_envelope(
        "# Requirements\n\n"
        "## Goal\n\nDeliver the approved epic outcome.\n\n"
        "## Acceptance Criteria (Verifiable)\n\n- AC1: Child outcome delivered.\n",
        approved_by="Test Owner",
        source="Owner-approved test fixture.",
        decomposition=True,
        implementation=False,
    )
    (epic_dir / "REQUIREMENTS.md").write_text(parent_requirements, encoding="utf-8")
    (epic_dir / workflow_cli.EPIC_CONTRACT_FILENAME).write_text(
        "# Epic Contract\n\n"
        "## Summary\n\n- Epic: EPIC-001\n- Title: Task Mode\n- Last updated: 2026-08-19\n\n"
        "## Sources of Truth\n\n- Owner-approved requirements.\n\n"
        "## Invalid Substitutes\n\n- Tracker-only claims.\n\n"
        "## Invariants\n\n- Parent AC IDs remain stable.\n\n"
        "## Artifact Targets\n\n- Child implementation artifacts.\n\n"
        "## Parent AC Proof Ownership\n\n"
        "| Parent AC | Proof Owner | Required Evidence |\n"
        "|---|---|---|\n"
        "| AC1 | TASK-001 | Verified child evidence |\n",
        encoding="utf-8",
    )
    (epic_dir / workflow_cli.DECOMPOSITION_PLAN_FILENAME).write_text(
        workflow_cli._format_decomposition_plan(
            epic_id="EPIC-001",
            requirements_text=parent_requirements,
            rows=[
                {
                    "ID": "TASK-001",
                    "Title": "Child",
                    "Parent ACs": "AC1",
                    "Source": "Test decomposition plan",
                }
            ],
        ),
        encoding="utf-8",
    )
    (child_dir / "IMPLEMENTATION.md").write_text(
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "|---|---|---|---|---|---|\n"
        f"| 1 | Work | Do work | AC1 | Verify | {row_status} |\n",
        encoding="utf-8",
    )
    (child_dir / "REQUIREMENTS.md").write_text("# Requirements\n", encoding="utf-8")
    tracker = epic_dir / "TRACKER.md"
    tracker.write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Child | In Progress | Task | AC1 | "
        "tasks/EPIC-001-Task-Mode/TASK-001-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    return tracker


@pytest.mark.parametrize(
    "command",
    COMMANDS,
)
def test_module_local_helper_and_installed_console_cannot_force_incomplete_testing(
    tmp_path: Path, command: tuple[str, ...]
) -> None:
    tracker = write_cli_fixture(tmp_path, row_status="To Do")
    before = hashlib.sha256(tracker.read_bytes()).hexdigest()
    rejected = subprocess.run(
        [
            *command,
            "task",
            "status",
            "--id",
            "TASK-001",
            "--to",
            "Testing",
            "--force",
            "--reason",
            "attempted bypass",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert rejected.returncode != 0
    assert "every required implementation row is Done" in rejected.stderr
    assert hashlib.sha256(tracker.read_bytes()).hexdigest() == before


@pytest.mark.parametrize("command", COMMANDS)
def test_epic_child_route_cannot_force_incomplete_task_to_testing(
    tmp_path: Path, command: tuple[str, ...]
) -> None:
    tracker = write_epic_child_cli_fixture(tmp_path, row_status="To Do")
    before = hashlib.sha256(tracker.read_bytes()).hexdigest()
    rejected = subprocess.run(
        [
            *command,
            "epic",
            "status",
            "--epic-id",
            "EPIC-001",
            "--id",
            "TASK-001",
            "--to",
            "Testing",
            "--force",
            "--reason",
            "attempted child bypass",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert rejected.returncode != 0
    assert "every required implementation row is Done" in rejected.stderr
    assert hashlib.sha256(tracker.read_bytes()).hexdigest() == before


@pytest.mark.parametrize("command", COMMANDS)
@pytest.mark.parametrize(
    ("row_status", "malformed", "expected"),
    (
        (None, False, "at least one required implementation row"),
        ("Complete", False, "every required implementation row is Done"),
        (None, True, "malformed rows"),
    ),
)
def test_testing_gate_rejects_empty_complete_and_malformed_tables_on_every_entrypoint(
    tmp_path: Path,
    command: tuple[str, ...],
    row_status: str | None,
    malformed: bool,
    expected: str,
) -> None:
    tracker = write_cli_fixture(tmp_path, row_status=row_status, malformed=malformed)
    before = tracker.read_bytes()
    rejected = subprocess.run(
        [
            *command,
            "task",
            "status",
            "--id",
            "TASK-001",
            "--to",
            "Testing",
            "--force",
            "--reason",
            "attempted integrity bypass",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert rejected.returncode != 0
    assert expected in rejected.stderr
    assert tracker.read_bytes() == before


@pytest.mark.parametrize("command", COMMANDS)
@pytest.mark.parametrize("bypass_kind", ("outside-section", "duplicate-table"))
def test_testing_gate_rejects_decoy_or_duplicate_tables_on_every_entrypoint(
    tmp_path: Path, command: tuple[str, ...], bypass_kind: str
) -> None:
    tracker = write_cli_fixture(tmp_path, row_status="To Do")
    implementation = tmp_path / ".project-workflow/tasks/TASK-001-Task-Mode/IMPLEMENTATION.md"
    done_table = (
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "|---|---|---|---|---|---|\n"
        "| decoy | Decoy | Decoy | AC1 | Verify | Done |\n"
    )
    if bypass_kind == "outside-section":
        implementation.write_text("## QA\n\n" + done_table, encoding="utf-8")
        expected = "exactly one canonical ## Task List"
    else:
        implementation.write_text(
            "## Task List\n\n"
            + done_table
            + "\n"
            + "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
            + "|---|---|---|---|---|---|\n"
            + "| real | Real | Work | AC1 | Verify | To Do |\n",
            encoding="utf-8",
        )
        expected = "exactly one supported implementation table"
    before = tracker.read_bytes()
    rejected = subprocess.run(
        [
            *command,
            "task",
            "status",
            "--id",
            "TASK-001",
            "--to",
            "Testing",
            "--force",
            "--reason",
            "attempted structural bypass",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert rejected.returncode != 0
    assert expected in rejected.stderr
    assert tracker.read_bytes() == before


def test_all_done_rows_allow_forced_recovery_transition(tmp_path: Path) -> None:
    tracker = write_cli_fixture(tmp_path, row_status="Done")
    accepted = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_workflow.cli",
            "task",
            "status",
            "--id",
            "TASK-001",
            "--to",
            "Testing",
            "--force",
            "--reason",
            "recover imported state",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert accepted.returncode == 0, accepted.stdout + accepted.stderr
    assert "| TASK-001 | Task Mode | Testing |" in tracker.read_text(encoding="utf-8")


def test_generated_python_helpers_are_byte_identical() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = (
        root / "src/project_workflow/templates/workflow.py",
        root / ".project-workflow/cli/workflow.py",
    )
    hashes = {hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    assert len(hashes) == 1
    assert b"# project-workflow:generated" in paths[0].read_bytes()
