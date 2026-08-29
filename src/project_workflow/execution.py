"""Canonical Project Workflow execution runtime."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from pathlib import Path

from .orchestration import (
    EPIC_CHILD_FORBIDDEN_ACTIONS,
    EPIC_CHILD_STOP_CONDITIONS,
    TASK_WORKER_FORBIDDEN_ACTIONS,
    TASK_WORKER_STOP_CONDITIONS,
    DelegationPlan,
    DelegationPlannedUnit,
    EpicChildObligations,
    EpicChildResult,
    EpicChildWorkPacket,
    EpicHostCapabilities,
    EpicLaunchIntent,
    EpicOrchestrationError,
    EpicOrchestrationState,
    EpicRetirementIntent,
    EpicUnitRun,
    PersistentTaskCreationIntent,
    TaskExecutionObligations,
    TaskExecutorDecision,
    TaskHostCapabilities,
    TaskOrchestrationError,
    TaskOrchestrationState,
    TaskUnitRun,
    TaskVerificationResult,
    TaskWorkerResult,
    TaskWorkPacket,
    _delegation_explicit_authority,
    _delegation_plan_fingerprint,
    _delegation_runtime_path,
    _delegation_scope_overlap,
    _epic_execution_fingerprint,
    _epic_execution_fingerprint_v1,
    _epic_opaque_handle_valid,
    _epic_orchestration_state_from_payload,
    _epic_orchestration_state_payload,
    _load_delegation_runtime_state,
    _normalize_orchestration_paths,
    _task_execution_fingerprint,
    _task_orchestration_state_from_payload,
    _task_orchestration_state_payload,
    _task_worker_path_forbidden,
    _write_delegation_runtime_state,
    initialize_delegation_runtime_state,
)


class TaskOrchestrator:
    """Coordinator-only state machine for one approved Task delegation plan."""

    def __init__(
        self,
        *,
        plan: DelegationPlan,
        obligations: Mapping[str, TaskExecutionObligations],
        capabilities: TaskHostCapabilities,
        coordinator_token: str,
        shared_state_hash: str,
    ) -> None:
        if plan.target.kind != "task":
            raise TaskOrchestrationError(
                "PW_TASK_TARGET_REQUIRED", "Task orchestration requires exactly one Task target."
            )
        durable_surfaces = sorted(
            unit.unit_id for unit in plan.units if unit.executor in {"persistent-task", "peer-team"}
        )
        if durable_surfaces:
            raise TaskOrchestrationError(
                "PW_TASK_SURFACE_RUNTIME_REQUIRED",
                "Task units selected for persistent-task or peer-team execution require "
                "DelegationSurfaceOrchestrator so visible handles, disposition, and retirement "
                "remain resumable: " + ", ".join(durable_surfaces) + ".",
            )
        if plan.target.lifecycle != "In Progress":
            raise TaskOrchestrationError(
                "PW_TASK_LIFECYCLE_INVALID",
                "The coordinator must move the Task to In Progress once before execution.",
            )
        if not coordinator_token:
            raise TaskOrchestrationError(
                "PW_TASK_COORDINATOR_REQUIRED", "A coordinator token is required."
            )
        self.plan = plan
        self.units = {unit.unit_id: unit for unit in plan.units}
        if set(self.units) != set(obligations):
            missing = sorted(set(self.units) - set(obligations))
            extra = sorted(set(obligations) - set(self.units))
            raise TaskOrchestrationError(
                "PW_TASK_PACKET_OBLIGATIONS_MISMATCH",
                f"Work packet obligations mismatch; missing={missing}, extra={extra}.",
            )
        self.obligations = dict(obligations)
        self.capabilities = capabilities
        self._dependants = {
            unit_id: tuple(
                candidate.unit_id for candidate in plan.units if unit_id in candidate.dependencies
            )
            for unit_id in self.units
        }
        plan_fingerprint = _task_execution_fingerprint(plan, obligations)
        self.state = TaskOrchestrationState(
            schema_version=1,
            target_id=plan.target.target_id,
            plan_fingerprint=plan_fingerprint,
            coordinator_hash=self._token_hash(coordinator_token),
            shared_state_hash=shared_state_hash,
            lifecycle="In Progress",
            units={
                unit.unit_id: TaskUnitRun(
                    state=(
                        "done"
                        if unit.canonical_state == "complete"
                        else "blocked"
                        if unit.canonical_state == "blocked"
                        else "pending"
                    ),
                    canonical_blocked=unit.canonical_state == "blocked",
                )
                for unit in plan.units
            },
        )

    @classmethod
    def resume(
        cls,
        *,
        root: Path,
        plan: DelegationPlan,
        obligations: Mapping[str, TaskExecutionObligations],
        capabilities: TaskHostCapabilities,
        coordinator_token: str,
    ) -> TaskOrchestrator:
        stored = _load_delegation_runtime_state(root, plan.target.target_id)
        if stored is None or "task_orchestration" not in stored:
            raise TaskOrchestrationError(
                "PW_TASK_RUNTIME_MISSING", "No persisted Task orchestration state exists."
            )
        restored = _task_orchestration_state_from_payload(stored["task_orchestration"])
        expected_fingerprint = _task_execution_fingerprint(plan, obligations)
        if (
            restored.target_id != plan.target.target_id
            or restored.plan_fingerprint != expected_fingerprint
        ):
            raise TaskOrchestrationError(
                "PW_TASK_RUNTIME_PLAN_MISMATCH",
                "Persisted Task runtime belongs to a different plan or capability bound.",
            )
        instance = cls(
            plan=plan,
            obligations=obligations,
            capabilities=capabilities,
            coordinator_token=coordinator_token,
            shared_state_hash=restored.shared_state_hash,
        )
        if set(restored.units) != set(instance.units):
            raise TaskOrchestrationError(
                "PW_TASK_RUNTIME_PLAN_MISMATCH",
                "Persisted Task runtime units do not match the canonical plan.",
            )
        if restored.coordinator_hash != instance.state.coordinator_hash:
            raise TaskOrchestrationError(
                "PW_TASK_COORDINATOR_ONLY",
                "The coordinator token does not own the persisted Task runtime.",
            )
        instance.state = restored
        for unit in plan.units:
            run = instance.state.units[unit.unit_id]
            if unit.canonical_state == "complete":
                run.state = "done"
                run.handle = None
                run.canonical_blocked = False
                run.blocked_by = ()
                run.completion_provenance = (
                    f"canonical:{plan.target.source_path}#{plan.target.source_hash}"
                )
            elif unit.canonical_state == "blocked":
                # Refreshed canonical authority wins over stale persisted runtime.
                # In particular, an active handle may not return and integrate after
                # the coordinator has blocked its implementation row.
                run.state = "blocked"
                run.handle = None
                run.canonical_blocked = True
                run.blocked_by = ()
                run.issues = ("Canonical implementation row is Blocked.",)
        return instance

    def persist(self, root: Path, *, coordinator_token: str) -> Path:
        self._require_coordinator(coordinator_token)
        state = _load_delegation_runtime_state(root, self.plan.target.target_id)
        if state is None:
            state = initialize_delegation_runtime_state(root, self.plan)
        else:
            if (
                state.get("target_id") != self.plan.target.target_id
                or state.get("target_kind") != "task"
                or Path(str(state.get("worktree", ""))).resolve() != root.resolve()
            ):
                raise TaskOrchestrationError(
                    "PW_TASK_RUNTIME_TARGET_MISMATCH",
                    "Persisted Task runtime target or worktree does not match this run.",
                )
            if "task_orchestration" in state:
                stored_task = _task_orchestration_state_from_payload(state["task_orchestration"])
                if stored_task.plan_fingerprint != self.state.plan_fingerprint:
                    raise TaskOrchestrationError(
                        "PW_TASK_RUNTIME_PLAN_MISMATCH",
                        "Persisted Task runtime belongs to different approved metadata.",
                    )
            state["plan_fingerprint"] = _delegation_plan_fingerprint(self.plan)
        state["task_orchestration"] = _task_orchestration_state_payload(self.state)
        stored_units = state.get("units")
        assert isinstance(stored_units, dict)
        for unit_id, run in self.state.units.items():
            projected = (
                "complete"
                if run.state == "done"
                else (
                    "active"
                    if run.state in {"active", "returned"}
                    else (
                        "orphaned"
                        if run.state == "orphaned"
                        else (
                            "blocked" if run.state in {"failed", "blocked", "halted"} else "pending"
                        )
                    )
                )
            )
            stored_units[unit_id] = {"state": projected, "handle": None}
        _write_delegation_runtime_state(root, self.plan, state)
        return _delegation_runtime_path(root, self.state.target_id)

    @staticmethod
    def _token_hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def _require_coordinator(self, token: str) -> None:
        if self._token_hash(token) != self.state.coordinator_hash:
            raise TaskOrchestrationError(
                "PW_TASK_COORDINATOR_ONLY",
                "Only the coordinator may mutate shared runtime state or Task lifecycle.",
            )

    def _active_ids(self) -> tuple[str, ...]:
        return tuple(
            unit_id
            for unit_id, run in self.state.units.items()
            if run.state in {"active", "returned"}
        )

    def _dependencies_done(self, unit: DelegationPlannedUnit) -> bool:
        return all(
            item not in self.state.units or self.state.units[item].state == "done"
            for item in unit.dependencies
        )

    def _scope_collision(self, left_id: str, right_id: str) -> bool:
        return any(
            _delegation_scope_overlap(left, right)
            for left in self.units[left_id].write_scope
            for right in self.units[right_id].write_scope
        )

    def decisions(self) -> tuple[TaskExecutorDecision, ...]:
        actual_active = self._active_ids()
        active = list(actual_active)
        reserved_slots = sum(
            self.units[unit_id].required_child_slots
            for unit_id in actual_active
            if self.units[unit_id].executor in {"subagent", "persistent-task", "peer-team"}
        )
        available_slots = max(
            0,
            min(
                self.plan.requested_concurrency - reserved_slots,
                self.plan.available_child_capacity - reserved_slots,
                self.capabilities.available_child_capacity,
            ),
        )
        exclusive_reserved = any(
            self.units[unit_id].executor == "coordinator"
            or self.units[unit_id].schedule == "sequential"
            for unit_id in actual_active
        )
        runtime_capabilities = self.capabilities.verified_capabilities
        decisions: list[TaskExecutorDecision] = []
        for unit in self.plan.units:
            run = self.state.units[unit.unit_id]
            if run.state in {"active", "returned", "done", "failed", "blocked", "halted"}:
                decisions.append(
                    TaskExecutorDecision(unit.unit_id, "none", False, f"Unit state is {run.state}.")
                )
                continue
            if run.state == "orphaned":
                decisions.append(
                    TaskExecutorDecision(
                        unit.unit_id,
                        "none",
                        False,
                        "Orphaned work requires an explicit coordinator retry.",
                    )
                )
                continue
            if not self.state.shared_premise_valid:
                decisions.append(
                    TaskExecutorDecision(unit.unit_id, "none", False, "Shared premise is invalid.")
                )
                continue
            if not self._dependencies_done(unit):
                decisions.append(
                    TaskExecutorDecision(
                        unit.unit_id, "none", False, "Dependencies are not verified Done."
                    )
                )
                continue
            if unit.executor == "none":
                decisions.append(
                    TaskExecutorDecision(
                        unit.unit_id,
                        "none",
                        False,
                        "Immutable delegation plan has no executable surface: "
                        + unit.executor_reason,
                    )
                )
                continue
            if unit.executor == "coordinator":
                launchable = not active and not exclusive_reserved
                decisions.append(
                    TaskExecutorDecision(
                        unit.unit_id,
                        "coordinator",
                        launchable,
                        "Write scope includes coordinator-owned workflow authority.",
                    )
                )
                if launchable:
                    active.append(unit.unit_id)
                    exclusive_reserved = True
                continue
            required: set[str]
            if unit.executor == "subagent":
                required = {"subagent"}
                if unit.execution_needs.isolated_worktree:
                    required.add("subagent-isolated-worktree")
            elif unit.executor == "persistent-task":
                required = {"persistent-task", "task-monitoring", "task-reconciliation"}
                if unit.execution_needs.isolated_worktree and not {
                    "persistent-task-isolated-worktree",
                    "isolated-worktree",
                }.intersection(runtime_capabilities):
                    required.add("persistent-task-isolated-worktree")
                if unit.execution_needs.direct_owner_steering:
                    required.add("persistent-task-owner-steering")
            elif unit.executor == "peer-team":
                required = {"peer-team", "peer-messaging"}
                if unit.execution_needs.isolated_worktree:
                    required.add("peer-team-isolated-worktree")
            else:
                decisions.append(
                    TaskExecutorDecision(
                        unit.unit_id,
                        "none",
                        False,
                        f"Immutable delegation plan executor {unit.executor} is unsupported.",
                    )
                )
                continue
            missing_plan = sorted(required - set(self.plan.observed_capabilities))
            missing_runtime = sorted(required - runtime_capabilities)
            source_mismatch = (
                self.plan.capability_source.strip() != self.capabilities.source.strip()
            )
            if missing_plan or missing_runtime or source_mismatch:
                reasons = [f"immutable plan lacks verified {item}" for item in missing_plan]
                reasons.extend(f"current runtime lacks verified {item}" for item in missing_runtime)
                if source_mismatch:
                    reasons.append("runtime capability source does not match the immutable plan")
                decisions.append(
                    TaskExecutorDecision(unit.unit_id, "none", False, "; ".join(reasons) + ".")
                )
                continue
            collision = any(self._scope_collision(unit.unit_id, item) for item in active)
            capacity = unit.required_child_slots <= available_slots
            parallel = unit.schedule == "parallel"
            launchable = (
                not collision and capacity and not exclusive_reserved and (parallel or not active)
            )
            if launchable:
                decisions.append(
                    TaskExecutorDecision(
                        unit.unit_id,
                        unit.executor,
                        True,
                        f"Immutable {unit.executor} selection is supported by current-session "
                        f"capacity from {self.capabilities.source}.",
                    )
                )
                active.append(unit.unit_id)
                reserved_slots += unit.required_child_slots
                available_slots -= unit.required_child_slots
                if not parallel:
                    exclusive_reserved = True
            else:
                reasons = []
                if collision:
                    reasons.append("write scope overlaps in-flight work")
                if not capacity:
                    reasons.append("requested or available child capacity is exhausted")
                if exclusive_reserved:
                    reasons.append("exclusive sequential/coordinator execution is reserved")
                if not parallel and active:
                    reasons.append("sequential schedule requires no in-flight work")
                decisions.append(
                    TaskExecutorDecision(
                        unit.unit_id,
                        unit.executor,
                        False,
                        "; ".join(dict.fromkeys(reasons)) + ".",
                    )
                )
        return tuple(decisions)

    def launch(self, unit_id: str, *, handle: str, coordinator_token: str) -> TaskWorkPacket:
        self._require_coordinator(coordinator_token)
        if unit_id not in self.units:
            raise TaskOrchestrationError("PW_TASK_UNIT_UNKNOWN", f"Unknown unit {unit_id}.")
        run = self.state.units[unit_id]
        if run.state in {"active", "returned", "done"}:
            raise TaskOrchestrationError(
                "PW_TASK_DUPLICATE_LAUNCH",
                f"{unit_id} is already {run.state}; duplicate launch is forbidden.",
            )
        if run.state in {"failed", "blocked", "halted", "orphaned"}:
            raise TaskOrchestrationError(
                "PW_TASK_RETRY_REQUIRED",
                f"{unit_id} is {run.state}; explicit coordinator recovery is required.",
            )
        if not handle.strip() or handle in self.state.used_handles:
            raise TaskOrchestrationError(
                "PW_TASK_HANDLE_REUSE",
                "Every bounded launch requires a non-empty handle unused by any prior attempt.",
            )
        decision = next(item for item in self.decisions() if item.unit_id == unit_id)
        if decision.executor == "coordinator":
            raise TaskOrchestrationError(
                "PW_TASK_COORDINATOR_EXECUTION_REQUIRED",
                f"{unit_id} is coordinator-owned and cannot receive a worker launch packet.",
            )
        if self.units[unit_id].schedule == "sequential" and any(
            self._scope_collision(unit_id, active) for active in self._active_ids()
        ):
            raise TaskOrchestrationError(
                "PW_TASK_WRITE_SCOPE_COLLISION",
                f"{unit_id} overlaps in-flight work and was rejected before launch.",
            )
        if not decision.launchable:
            raise TaskOrchestrationError("PW_TASK_NOT_LAUNCHABLE", f"{unit_id}: {decision.reason}")
        unit = self.units[unit_id]
        duty = self.obligations[unit_id]
        run.state = "active"
        run.attempt += 1
        run.handle = handle
        run.executor = decision.executor
        run.baseline_hash = self.state.shared_state_hash
        run.baseline_revision = self.state.integration_revision
        run.checkpointed = False
        run.issues = ()
        self.state.used_handles.add(handle)
        return TaskWorkPacket(
            target_id=self.state.target_id,
            target_source=self.plan.target.source_path,
            target_source_hash=self.plan.target.source_hash,
            unit_id=unit_id,
            unit_title=unit.title,
            acceptance_criteria=duty.acceptance_criteria,
            verified_dependencies=tuple(
                item
                for item in unit.dependencies
                if item not in self.state.units or self.state.units[item].state == "done"
            ),
            write_scope=unit.write_scope,
            repositories=duty.repositories,
            validations=duty.validations,
            evidence=duty.evidence,
            forbidden_actions=TASK_WORKER_FORBIDDEN_ACTIONS,
            stop_conditions=TASK_WORKER_STOP_CONDITIONS,
            baseline_hash=self.state.shared_state_hash,
            plan_fingerprint=self.state.plan_fingerprint,
            executor=decision.executor,
            attempt=run.attempt,
        )

    def _descendants(self, unit_id: str) -> tuple[str, ...]:
        pending = list(self._dependants[unit_id])
        seen: set[str] = set()
        while pending:
            current = pending.pop(0)
            if current in seen:
                continue
            seen.add(current)
            pending.extend(self._dependants[current])
        return tuple(unit.unit_id for unit in self.plan.units if unit.unit_id in seen)

    def _fail(self, unit_id: str, issues: Sequence[str], *, shared: bool) -> None:
        run = self.state.units[unit_id]
        run.state = "failed"
        run.handle = None
        run.issues = tuple(issues)
        self.state.failure_seen = True
        if shared:
            self.state.shared_premise_valid = False
            for other_id, other in self.state.units.items():
                if other_id != unit_id and other.state in {"pending", "blocked", "orphaned"}:
                    other.state = "halted"
        else:
            for descendant in self._descendants(unit_id):
                descendant_run = self.state.units[descendant]
                if descendant_run.canonical_blocked:
                    continue
                blockers = set(descendant_run.blocked_by)
                blockers.add(unit_id)
                descendant_run.blocked_by = tuple(sorted(blockers))
                if descendant_run.state == "pending":
                    descendant_run.state = "blocked"

    @staticmethod
    def _normalize_paths(paths: Sequence[str]) -> tuple[str, ...]:
        return _normalize_orchestration_paths(paths)

    def complete_coordinator_unit(
        self,
        unit_id: str,
        *,
        observed_paths: Sequence[str],
        observed_validations: Mapping[str, bool],
        observed_evidence: Mapping[str, bool],
        current_shared_state_hash: str,
        provenance: str,
        coordinator_token: str,
    ) -> TaskVerificationResult:
        self._require_coordinator(coordinator_token)
        if unit_id not in self.units:
            raise TaskOrchestrationError("PW_TASK_UNIT_UNKNOWN", f"Unknown unit {unit_id}.")
        decision = next(item for item in self.decisions() if item.unit_id == unit_id)
        if decision.executor != "coordinator" or not decision.launchable:
            raise TaskOrchestrationError(
                "PW_TASK_COORDINATOR_EXECUTION_INVALID",
                f"{unit_id} is not currently eligible for exclusive coordinator execution.",
            )
        if not provenance.strip() or current_shared_state_hash != self.state.shared_state_hash:
            raise TaskOrchestrationError(
                "PW_TASK_COORDINATOR_VERIFICATION_REQUIRED",
                "Coordinator execution requires matching shared state and durable provenance.",
            )
        unit = self.units[unit_id]
        observed = self._normalize_paths(observed_paths)
        outside = tuple(
            path
            for path in observed
            if not any(
                scope == "." or path == scope or path.startswith(scope + "/")
                for scope in unit.write_scope
            )
        )
        duty = self.obligations[unit_id]
        issues: list[str] = []
        if outside:
            issues.append("Out-of-scope paths: " + ", ".join(outside) + ".")
        missing_validation = tuple(
            item for item in duty.validations if observed_validations.get(item) is not True
        )
        missing_evidence = tuple(
            item for item in duty.evidence if observed_evidence.get(item) is not True
        )
        if missing_validation:
            issues.append(
                "Required validation did not pass: " + ", ".join(missing_validation) + "."
            )
        if missing_evidence:
            issues.append("Required evidence is absent: " + ", ".join(missing_evidence) + ".")
        if issues:
            self._fail(unit_id, issues, shared=bool(outside))
            return TaskVerificationResult(unit_id, False, "failed", tuple(issues), ())
        run = self.state.units[unit_id]
        run.state = "done"
        run.completion_provenance = provenance.strip()
        self.state.integration_revision += 1
        self.state.integrated_paths.append((self.state.integration_revision, unit_id, observed))
        newly_eligible = tuple(
            item.unit_id for item in self.decisions() if item.launchable and item.executor != "none"
        )
        return TaskVerificationResult(unit_id, True, "done", (), newly_eligible)

    def verify_result(
        self,
        result: TaskWorkerResult,
        *,
        observed_paths: Sequence[str],
        observed_validations: Mapping[str, bool],
        observed_evidence: Mapping[str, bool],
        current_shared_state_hash: str,
        coordinator_token: str,
    ) -> TaskVerificationResult:
        self._require_coordinator(coordinator_token)
        if result.unit_id not in self.units:
            raise TaskOrchestrationError("PW_TASK_UNIT_UNKNOWN", f"Unknown unit {result.unit_id}.")
        unit = self.units[result.unit_id]
        run = self.state.units[result.unit_id]
        if run.state not in {"active", "returned"} or run.handle != result.handle:
            raise TaskOrchestrationError(
                "PW_TASK_RESULT_UNMATCHED",
                "Returned work does not match the coordinator's active bounded handle.",
            )
        if result.plan_fingerprint != self.state.plan_fingerprint or result.attempt != run.attempt:
            raise TaskOrchestrationError(
                "PW_TASK_RESULT_STALE",
                "Returned work belongs to a different plan fingerprint or launch attempt.",
            )
        if not self.state.shared_premise_valid:
            run.state = "halted"
            run.handle = None
            run.checkpointed = True
            run.issues = ("Shared premise is invalid; returned work was halted, not integrated.",)
            return TaskVerificationResult(
                result.unit_id,
                False,
                "halted",
                run.issues,
                (),
            )
        issues: list[str] = []
        coordinator_integrity_failure = False
        try:
            claimed = self._normalize_paths(result.claimed_paths)
            observed = self._normalize_paths(observed_paths)
        except TaskOrchestrationError as error:
            claimed, observed = (), ()
            issues.append(error.message)
            coordinator_integrity_failure = True
        if claimed != observed:
            issues.append("Worker-claimed paths do not match the coordinator-observed diff.")
            coordinator_integrity_failure = True
        outside = tuple(
            path
            for path in observed
            if not any(
                scope == "." or path == scope or path.startswith(scope + "/")
                for scope in unit.write_scope
            )
        )
        if outside:
            issues.append("Out-of-scope paths: " + ", ".join(outside) + ".")
            coordinator_integrity_failure = True
        shared_paths = tuple(path for path in observed if _task_worker_path_forbidden(path))
        if shared_paths:
            issues.append(
                "Coordinator-only shared workflow paths: " + ", ".join(shared_paths) + "."
            )
            coordinator_integrity_failure = True
        if (
            result.baseline_hash != run.baseline_hash
            or result.shared_state_hash != run.baseline_hash
            or current_shared_state_hash != self.state.shared_state_hash
        ):
            issues.append("Coordinator-only shared state changed from the launch baseline.")
            coordinator_integrity_failure = True
        intervening = [
            paths
            for revision, _other_id, paths in self.state.integrated_paths
            if revision > run.baseline_revision
        ]
        collisions = tuple(
            path
            for path in observed
            if any(
                _delegation_scope_overlap(path, prior) for paths in intervening for prior in paths
            )
        )
        if collisions:
            issues.append("Intervening diff collision: " + ", ".join(collisions) + ".")
            coordinator_integrity_failure = True
        duty = self.obligations[result.unit_id]
        missing_validation = tuple(
            item for item in duty.validations if observed_validations.get(item) is not True
        )
        if missing_validation:
            issues.append(
                "Required validation did not pass: " + ", ".join(missing_validation) + "."
            )
        missing_evidence = tuple(
            item for item in duty.evidence if observed_evidence.get(item) is not True
        )
        if missing_evidence:
            issues.append("Required evidence is absent: " + ", ".join(missing_evidence) + ".")
        if not result.success:
            issues.append(result.failure_reason.strip() or "Worker reported failure.")
        if not result.shared_premise_valid:
            issues.append("Worker reported a shared-premise failure.")
        worker_claim_mismatch = tuple(
            item
            for item in duty.validations
            if result.validations.get(item) is not observed_validations.get(item)
        ) + tuple(
            item
            for item in duty.evidence
            if result.evidence.get(item) is not observed_evidence.get(item)
        )
        if worker_claim_mismatch:
            issues.append(
                "Worker claims disagree with coordinator observations: "
                + ", ".join(worker_claim_mismatch)
                + "."
            )
        if issues:
            self._fail(
                result.unit_id,
                issues,
                shared=coordinator_integrity_failure or not result.shared_premise_valid,
            )
            return TaskVerificationResult(result.unit_id, False, "failed", tuple(issues), ())
        run.state = "done"
        run.handle = None
        run.issues = ()
        self.state.integration_revision += 1
        self.state.integrated_paths.append(
            (self.state.integration_revision, result.unit_id, observed)
        )
        newly_eligible = tuple(
            item.unit_id for item in self.decisions() if item.launchable and item.executor != "none"
        )
        return TaskVerificationResult(result.unit_id, True, "done", (), newly_eligible)

    def rebaseline_shared_state(
        self,
        new_hash: str,
        *,
        reason: str,
        coordinator_token: str,
    ) -> None:
        """Record a coordinator-owned canonical write without rewriting worker baselines."""
        self._require_coordinator(coordinator_token)
        if not new_hash.strip() or not reason.strip():
            raise TaskOrchestrationError(
                "PW_TASK_REBASE_PROVENANCE_REQUIRED",
                "Shared-state rebaseline requires a new hash and durable reason.",
            )
        if new_hash == self.state.shared_state_hash:
            return
        self.state.shared_state_hash = new_hash
        self.state.shared_state_revisions.append((new_hash, reason.strip()))

    def checkpoint(self, unit_id: str, *, coordinator_token: str) -> None:
        self._require_coordinator(coordinator_token)
        run = self.state.units.get(unit_id)
        if run is None or run.state not in {"active", "returned"}:
            raise TaskOrchestrationError(
                "PW_TASK_CHECKPOINT_INVALID", f"{unit_id} is not in flight."
            )
        run.checkpointed = True
        if not self.state.shared_premise_valid:
            run.state = "halted"
            run.handle = None

    def reconcile(
        self,
        observations: Mapping[str, Mapping[str, str]],
        *,
        canonical_completed: Mapping[str, str] | None = None,
        coordinator_token: str,
    ) -> None:
        self._require_coordinator(coordinator_token)
        canonical = dict(canonical_completed or {})
        if any(not source.strip() for source in canonical.values()):
            raise TaskOrchestrationError(
                "PW_TASK_COMPLETION_PROVENANCE_REQUIRED",
                "Canonical completion requires a non-empty durable evidence reference.",
            )
        invalid_canonical = tuple(
            unit_id
            for unit_id in canonical
            if unit_id not in self.units or self.units[unit_id].canonical_state != "complete"
        )
        if invalid_canonical:
            raise TaskOrchestrationError(
                "PW_TASK_COMPLETION_PROVENANCE_INVALID",
                "Canonical completion is not present in the current plan for: "
                + ", ".join(invalid_canonical)
                + ".",
            )
        for unit_id, run in self.state.units.items():
            if unit_id in canonical:
                run.state = "done"
                run.handle = None
                run.completion_provenance = canonical[unit_id]
                continue
            if run.state not in {"active", "returned"}:
                continue
            observed = observations.get(unit_id)
            identity_matches = (
                observed is not None
                and observed.get("id") == run.handle
                and observed.get("kind") == "subagent"
            )
            observed_state = observed.get("state") if observed is not None else None
            if identity_matches and observed_state == "active":
                run.state = "active"
            elif identity_matches and observed_state in {"complete", "completed"}:
                run.state = "returned"
            elif identity_matches and observed_state == "failed":
                self._fail(unit_id, ("Observed worker failure.",), shared=False)
            else:
                run.state = "orphaned"
                run.handle = None
                run.issues = (
                    "Exact active handle identity was not observed in the current session.",
                )

    def retry(self, unit_id: str, *, coordinator_token: str) -> None:
        self._require_coordinator(coordinator_token)
        run = self.state.units.get(unit_id)
        if run is None:
            raise TaskOrchestrationError("PW_TASK_UNIT_UNKNOWN", f"Unknown unit {unit_id}.")
        if run.state not in {"failed", "orphaned"}:
            raise TaskOrchestrationError(
                "PW_TASK_RETRY_INVALID", f"{unit_id} is not failed or orphaned."
            )
        if not self.state.shared_premise_valid:
            raise TaskOrchestrationError(
                "PW_TASK_SHARED_PREMISE_INVALID", "A halted run cannot be retried in place."
            )
        run.state = "pending"
        run.issues = ()
        for descendant in self._descendants(unit_id):
            descendant_run = self.state.units[descendant]
            descendant_run.blocked_by = tuple(
                blocker for blocker in descendant_run.blocked_by if blocker != unit_id
            )
            if (
                descendant_run.state == "blocked"
                and not descendant_run.canonical_blocked
                and not descendant_run.blocked_by
            ):
                descendant_run.state = "pending"

    def assert_testing_allowed(self, *, force: bool = False) -> None:
        incomplete = tuple(
            unit_id for unit_id, run in self.state.units.items() if run.state != "done"
        )
        if incomplete:
            suffix = " Ordinary --force cannot bypass this integrity gate." if force else ""
            raise TaskOrchestrationError(
                "PW_TASK_TESTING_INCOMPLETE",
                "Task cannot move to Testing until every required implementation row is Done; "
                f"incomplete: {', '.join(incomplete)}.{suffix}",
            )

    def summary(self) -> dict[str, object]:
        groups: dict[str, list[str]] = {
            "completed": [],
            "failed": [],
            "blocked": [],
            "halted": [],
            "in_flight": [],
            "orphaned": [],
            "unaffected": [],
        }
        for unit in self.plan.units:
            state = self.state.units[unit.unit_id].state
            if state == "done":
                groups["completed"].append(unit.unit_id)
            elif state in {"active", "returned"}:
                groups["in_flight"].append(unit.unit_id)
            elif state in groups:
                groups[state].append(unit.unit_id)
            elif self.state.failure_seen and self.state.shared_premise_valid:
                groups["unaffected"].append(unit.unit_id)
        return {
            "schema_version": 1,
            "target_id": self.state.target_id,
            "shared_premise_valid": self.state.shared_premise_valid,
            "testing_allowed": all(run.state == "done" for run in self.state.units.values()),
            **groups,
        }


class EpicOrchestrator:
    """Coordinator-only state machine for durable capability-aware execution surfaces."""

    def __init__(
        self,
        *,
        plan: DelegationPlan,
        obligations: Mapping[str, EpicChildObligations],
        capabilities: EpicHostCapabilities,
        coordinator_token: str,
        coordinator_worktree: Path,
        base_commit: str,
    ) -> None:
        if plan.target.kind not in {"task", "epic"}:
            raise EpicOrchestrationError(
                "PW_EPIC_TARGET_REQUIRED",
                "Surface orchestration requires exactly one Task or Epic target.",
            )
        if plan.target.lifecycle != "In Progress":
            raise EpicOrchestrationError(
                "PW_EPIC_LIFECYCLE_INVALID", "The parent Epic must already be In Progress."
            )
        if not coordinator_token.strip():
            raise EpicOrchestrationError(
                "PW_EPIC_COORDINATOR_REQUIRED", "A coordinator token is required."
            )
        if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", base_commit):
            raise EpicOrchestrationError(
                "PW_EPIC_BASE_INVALID",
                "Epic execution requires an exact full-length hexadecimal Git object ID.",
            )
        self.plan = plan
        self.units = {unit.unit_id: unit for unit in plan.units}
        if set(self.units) != set(obligations):
            raise EpicOrchestrationError(
                "PW_EPIC_PACKET_OBLIGATIONS_MISMATCH",
                "Epic child obligations must match every selected canonical child exactly.",
            )
        for unit_id, duty in obligations.items():
            if plan.target.kind == "epic" and tuple(duty.parent_acs) != tuple(
                self.units[unit_id].authority_acs
            ):
                raise EpicOrchestrationError(
                    "PW_EPIC_AUTHORITY_MISMATCH",
                    f"{unit_id} packet parent ACs do not match decomposition authority.",
                )
        self.obligations = dict(obligations)
        self.capabilities = capabilities
        self._dependants = {
            unit_id: tuple(
                candidate.unit_id for candidate in plan.units if unit_id in candidate.dependencies
            )
            for unit_id in self.units
        }
        fingerprint = _epic_execution_fingerprint(plan, obligations, base_commit)
        self.state = EpicOrchestrationState(
            schema_version=2,
            target_id=plan.target.target_id,
            plan_fingerprint=fingerprint,
            coordinator_hash=self._token_hash(coordinator_token),
            coordinator_worktree=str(coordinator_worktree.resolve()),
            base_commit=base_commit,
            units={
                unit.unit_id: EpicUnitRun(
                    state=(
                        "verified"
                        if unit.canonical_state == "complete"
                        else "blocked"
                        if unit.canonical_state == "blocked"
                        else "pending"
                    ),
                    completion_provenance=(
                        f"canonical:{plan.target.source_path}#{plan.target.source_hash}"
                        if unit.canonical_state == "complete"
                        else None
                    ),
                    executor=unit.executor,
                    visibility_class=unit.visibility_class,
                    retention_policy=unit.retention_policy,
                    disposition_state=(
                        "integrated" if unit.canonical_state == "complete" else "pending"
                    ),
                    disposition_receipt=(
                        f"canonical:{plan.target.source_hash}"
                        if unit.canonical_state == "complete"
                        else None
                    ),
                    retirement_state=(
                        "pending"
                        if unit.visibility_class == "visible-retirable"
                        else (
                            "retained"
                            if unit.visibility_class == "visible-retained"
                            else "not-applicable"
                        )
                    ),
                )
                for unit in plan.units
            },
        )

    @staticmethod
    def _token_hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def _require_coordinator(self, token: str) -> None:
        if self._token_hash(token) != self.state.coordinator_hash:
            raise EpicOrchestrationError(
                "PW_EPIC_COORDINATOR_ONLY",
                "Only the parent coordinator may mutate Epic delegation runtime state.",
            )

    def _dependencies_verified(self, unit: DelegationPlannedUnit) -> bool:
        # build_delegation_plan permits an omitted dependency only when its canonical
        # lifecycle is already Complete. Missing selected-state entries therefore
        # represent verified canonical predecessors rather than unknown work.
        return all(
            dependency not in self.state.units
            or (
                self.state.units[dependency].state == "verified"
                and (
                    self.state.units[dependency].visibility_class == "ephemeral"
                    or self.state.units[dependency].disposition_state
                    in {"integrated", "no-integration"}
                )
            )
            for dependency in unit.dependencies
        )

    def _scope_collision(self, left_id: str, right_id: str) -> bool:
        if not set(self.obligations[left_id].repositories).intersection(
            self.obligations[right_id].repositories
        ):
            return False
        return any(
            _delegation_scope_overlap(left, right)
            for left in self.obligations[left_id].write_scope
            for right in self.obligations[right_id].write_scope
        )

    def capability_boundary(self) -> dict[str, object]:
        reasons: list[str] = []
        required = {
            "persistent-task",
            "task-monitoring",
            "task-reconciliation",
        }
        persistent_units = tuple(
            unit for unit in self.plan.units if unit.executor == "persistent-task"
        )
        isolation_required = any(
            unit.execution_needs.isolated_worktree for unit in persistent_units
        )
        if isolation_required:
            required.add("isolated-worktree")
        if not _delegation_explicit_authority(self.plan.persistent_task_authority):
            reasons.append("explicit owner authority is absent")
        if not required.issubset(self.plan.observed_capabilities):
            reasons.append("immutable plan lacks the verified persistent-task capability set")
        if self.plan.capability_source.strip() != self.capabilities.source.strip():
            reasons.append("runtime capability source does not match the immutable plan")
        if self.plan.available_child_capacity == 0:
            reasons.append("immutable plan authorizes no persistent child capacity")
        if not self.capabilities.current_session_verified:
            reasons.append("current-session capability observation is absent")
        if not self.capabilities.persistent_tasks:
            reasons.append("persistent task creation is unsupported or unknown")
        if isolation_required and not self.capabilities.isolated_worktrees:
            reasons.append("isolated worktree creation is unsupported or unknown")
        if not self.capabilities.monitoring:
            reasons.append("task monitoring is unsupported or unknown")
        if not self.capabilities.reconciliation:
            reasons.append("task reconciliation is unsupported or unknown")
        if self.capabilities.available_child_capacity == 0:
            reasons.append("available persistent-task capacity is zero")
        supported = not reasons
        resume_reasons: list[str] = []
        if self.plan.capability_source.strip() != self.capabilities.source.strip():
            resume_reasons.append("runtime capability source does not match the immutable plan")
        if not self.capabilities.current_session_verified:
            resume_reasons.append("current-session capability observation is absent")
        if "task-reconciliation" not in self.plan.observed_capabilities:
            resume_reasons.append("immutable plan lacks verified task reconciliation")
        if "task-monitoring" not in self.plan.observed_capabilities:
            resume_reasons.append("immutable plan lacks verified task monitoring")
        if not self.capabilities.monitoring:
            resume_reasons.append("current-session task monitoring is unsupported or unknown")
        if not self.capabilities.reconciliation:
            resume_reasons.append("current-session task reconciliation is unsupported or unknown")
        return {
            "creation_authorized": _delegation_explicit_authority(
                self.plan.persistent_task_authority
            ),
            "creation_supported": supported,
            "resume_supported": not resume_reasons,
            "resume_reasons": resume_reasons,
            "fallback": None if supported else "safe-sequential-coordinator",
            "reasons": reasons,
            "source": self.capabilities.source or "not observed",
        }

    def _surface_runtime_reasons(self, unit: DelegationPlannedUnit) -> tuple[str, ...]:
        runtime = self.capabilities.verified_capabilities
        if self.plan.capability_source.strip() != self.capabilities.source.strip():
            return ("runtime capability source does not match the immutable plan",)
        if not self.capabilities.current_session_verified:
            return ("current-session capability observation is absent",)
        required: set[str]
        if unit.executor == "subagent":
            required = {"subagent"}
            if unit.execution_needs.isolated_worktree:
                required.add("subagent-isolated-worktree")
        elif unit.executor == "persistent-task":
            required = {
                "persistent-task",
                "task-monitoring",
                "task-reconciliation",
            }
            if unit.execution_needs.isolated_worktree:
                if not {"persistent-task-isolated-worktree", "isolated-worktree"}.intersection(
                    runtime
                ):
                    required.add("persistent-task-isolated-worktree")
        elif unit.executor == "peer-team":
            required = {"peer-team", "peer-messaging"}
            if unit.execution_needs.isolated_worktree:
                required.add("peer-team-isolated-worktree")
        else:
            return ()
        missing_plan = sorted(required - set(self.plan.observed_capabilities))
        missing = sorted(required - runtime)
        reasons = [f"immutable plan lacks verified {item}" for item in missing_plan]
        reasons.extend(f"current runtime lacks verified {item}" for item in missing)
        if unit.executor == "persistent-task" and not _delegation_explicit_authority(
            self.plan.persistent_task_authority
        ):
            reasons.append("explicit owner authority is absent")
        return tuple(reasons)

    def _packet(self, unit_id: str, attempt: int) -> EpicChildWorkPacket:
        unit = self.units[unit_id]
        duty = self.obligations[unit_id]
        return EpicChildWorkPacket(
            target_id=self.state.target_id,
            target_kind=self.plan.target.kind,
            target_source=self.plan.target.source_path,
            target_source_hash=self.plan.target.source_hash,
            unit_id=unit_id,
            unit_title=unit.title,
            parent_acs=duty.parent_acs,
            verified_dependencies=tuple(
                dependency
                for dependency in unit.dependencies
                if dependency not in self.state.units
                or self.state.units[dependency].state == "verified"
            ),
            repositories=duty.repositories,
            write_scope=duty.write_scope,
            validations=duty.validations,
            evidence=duty.evidence,
            forbidden_actions=EPIC_CHILD_FORBIDDEN_ACTIONS,
            stop_conditions=EPIC_CHILD_STOP_CONDITIONS,
            base_commit=self.state.base_commit,
            plan_fingerprint=self.state.plan_fingerprint,
            executor=unit.executor,
            visibility_class=unit.visibility_class,
            retention_policy=unit.retention_policy,
            isolated_worktree_required=unit.execution_needs.isolated_worktree,
            attempt=attempt,
        )

    def _launch_evaluation(
        self,
    ) -> tuple[tuple[EpicLaunchIntent, ...], dict[str, tuple[str, ...]]]:
        reasons: dict[str, tuple[str, ...]] = {}
        if not self.state.shared_premise_valid:
            return (), {
                unit.unit_id: ("shared Epic premise is invalid",)
                for unit in self.plan.units
                if self.state.units[unit.unit_id].state == "pending"
            }
        active = [
            unit_id
            for unit_id, run in self.state.units.items()
            if run.state in {"active", "returned"}
        ]
        active_child_slots = sum(
            self.units[unit_id].required_child_slots
            for unit_id in active
            if self.units[unit_id].executor in {"subagent", "persistent-task", "peer-team"}
        )
        available = max(
            0,
            min(
                self.plan.requested_concurrency - active_child_slots,
                self.plan.available_child_capacity - active_child_slots,
                self.capabilities.available_child_capacity,
            ),
        )
        reserved = list(active)
        intents: list[EpicLaunchIntent] = []
        for unit in self.plan.units:
            run = self.state.units[unit.unit_id]
            if run.state != "pending":
                continue
            unit_reasons: list[str] = []
            if not self._dependencies_verified(unit):
                unit_reasons.append("waiting for coordinator-verified dependencies")
            if unit.executor not in {"subagent", "persistent-task", "peer-team"}:
                unit_reasons.append(
                    f"immutable plan executor is {unit.executor}, not a host-launched surface"
                )
            unit_reasons.extend(self._surface_runtime_reasons(unit))
            collisions = [
                other_id for other_id in reserved if self._scope_collision(unit.unit_id, other_id)
            ]
            if collisions:
                unit_reasons.append(
                    "repository/write-scope collision with active or reserved child: "
                    + ", ".join(collisions)
                )
            if available <= 0:
                unit_reasons.append("effective child capacity is exhausted")
            if unit.executor == "peer-team" and available < 2:
                unit_reasons.append("peer-team requires at least two available child slots")
            if unit_reasons:
                reasons[unit.unit_id] = tuple(unit_reasons)
                continue
            attempt = run.attempt + 1
            packet = self._packet(unit.unit_id, attempt)
            identity = f"{self.state.plan_fingerprint}:{unit.unit_id}:{attempt}"
            if unit.executor != "persistent-task":
                identity += f":{unit.executor}"
            intent_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()
            intents.append(
                EpicLaunchIntent(
                    intent_id=intent_id,
                    unit_id=unit.unit_id,
                    attempt=attempt,
                    executor=unit.executor,
                    packet=packet,
                    capability_source=self.capabilities.source,
                )
            )
            reserved.append(unit.unit_id)
            available -= 2 if unit.executor == "peer-team" else 1
        return tuple(intents), reasons

    def launch_intents(self) -> tuple[EpicLaunchIntent, ...]:
        intents, _reasons = self._launch_evaluation()
        return intents

    def creation_intents(self) -> tuple[PersistentTaskCreationIntent, ...]:
        return tuple(
            PersistentTaskCreationIntent(
                intent_id=intent.intent_id,
                unit_id=intent.unit_id,
                attempt=intent.attempt,
                packet=intent.packet,
                capability_source=intent.capability_source,
            )
            for intent in self.launch_intents()
            if intent.executor == "persistent-task"
        )

    def register_launch(
        self,
        intent: EpicLaunchIntent,
        *,
        handle: str,
        branch: str,
        worktree: Path,
        coordinator_token: str,
    ) -> EpicChildWorkPacket:
        self._require_coordinator(coordinator_token)
        expected = {item.intent_id: item for item in self.launch_intents()}
        if intent.intent_id not in expected or expected[intent.intent_id] != intent:
            raise EpicOrchestrationError(
                "PW_EPIC_LAUNCH_INTENT_INVALID",
                "Worker launch did not match a currently eligible bounded intent.",
            )
        run = self.state.units[intent.unit_id]
        if intent.intent_id in self.state.used_intents or run.state != "pending":
            raise EpicOrchestrationError(
                "PW_EPIC_DUPLICATE_CREATION", "A child intent may launch at most one worker."
            )
        if not _epic_opaque_handle_valid(handle) or handle in self.state.used_handles:
            raise EpicOrchestrationError(
                "PW_EPIC_HANDLE_REUSE",
                "Every delegated child requires a unique bounded opaque native handle.",
            )
        named_branch = bool(branch.strip() and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", branch))
        detached_identity = branch == f"detached@{self.state.base_commit}"
        if not named_branch and not detached_identity:
            raise EpicOrchestrationError(
                "PW_EPIC_BRANCH_INVALID",
                "Child checkout identity must be a named branch or exact detached base identity.",
            )
        resolved_worktree = worktree.resolve()
        coordinator_worktree = Path(self.state.coordinator_worktree).resolve()
        if intent.packet.isolated_worktree_required and resolved_worktree == coordinator_worktree:
            raise EpicOrchestrationError(
                "PW_EPIC_WORKTREE_NOT_ISOLATED",
                "This selected surface requires an isolated worktree.",
            )
        for other in self.state.units.values():
            if (
                resolved_worktree != coordinator_worktree
                and other.worktree
                and Path(other.worktree).resolve() == resolved_worktree
            ):
                raise EpicOrchestrationError(
                    "PW_EPIC_WORKTREE_REUSE", "Isolated child worktrees must be distinct."
                )
            if intent.executor == "persistent-task" and named_branch and other.branch == branch:
                raise EpicOrchestrationError(
                    "PW_EPIC_BRANCH_REUSE", "Persistent child branches must be distinct."
                )
        run.state = "active"
        run.attempt = intent.attempt
        run.intent_id = intent.intent_id
        run.handle = handle
        run.branch = branch
        run.worktree = str(resolved_worktree)
        run.base_commit = self.state.base_commit
        run.checkpointed = False
        run.issues = ()
        run.executor = intent.executor
        self.state.create_count += 1
        self.state.used_intents.add(intent.intent_id)
        self.state.used_handles.add(handle)
        return intent.packet

    def register_creation(
        self,
        intent: PersistentTaskCreationIntent,
        *,
        handle: str,
        branch: str,
        worktree: Path,
        coordinator_token: str,
    ) -> EpicChildWorkPacket:
        expected = {
            item.intent_id: item
            for item in self.launch_intents()
            if item.executor == "persistent-task"
        }
        launch = expected.get(intent.intent_id)
        if launch is None or launch.packet != intent.packet:
            raise EpicOrchestrationError(
                "PW_EPIC_CREATION_INTENT_INVALID",
                "Persistent task creation did not match a currently eligible bounded intent.",
            )
        return self.register_launch(
            launch,
            handle=handle,
            branch=branch,
            worktree=worktree,
            coordinator_token=coordinator_token,
        )

    def _descendants(self, unit_id: str) -> tuple[str, ...]:
        pending = list(self._dependants[unit_id])
        seen: set[str] = set()
        while pending:
            current = pending.pop(0)
            if current in seen:
                continue
            seen.add(current)
            pending.extend(self._dependants[current])
        return tuple(unit.unit_id for unit in self.plan.units if unit.unit_id in seen)

    def _fail(self, unit_id: str, issues: Sequence[str], *, shared: bool) -> None:
        run = self.state.units[unit_id]
        run.state = "failed"
        run.issues = ("PW_EPIC_SHARED_PREMISE_FAILED" if shared else "PW_EPIC_CHILD_FAILED",)
        if run.visibility_class == "ephemeral":
            run.handle = None
        self.state.failure_seen = True
        if shared:
            self.state.shared_premise_valid = False
            for other_id, other in self.state.units.items():
                if other_id != unit_id and other.state in {"pending", "blocked", "orphaned"}:
                    other.state = "halted"
        else:
            for descendant in self._descendants(unit_id):
                descendant_run = self.state.units[descendant]
                blockers = set(descendant_run.blocked_by)
                blockers.add(unit_id)
                descendant_run.blocked_by = tuple(sorted(blockers))
                if descendant_run.state == "pending":
                    descendant_run.state = "blocked"

    @staticmethod
    def _normalized_paths(paths: Sequence[str]) -> tuple[str, ...]:
        try:
            return _normalize_orchestration_paths(paths)
        except TaskOrchestrationError as error:
            raise EpicOrchestrationError("PW_EPIC_DIFF_INVALID", error.message) from error

    def verify_result(
        self,
        result: EpicChildResult,
        *,
        observed_branch: str,
        observed_worktree: Path,
        observed_base_commit: str,
        observed_head_commit: str,
        observed_repositories: Sequence[str],
        observed_paths: Sequence[str],
        observed_validations: Mapping[str, bool],
        observed_evidence: Mapping[str, bool],
        coordinator_token: str,
    ) -> TaskVerificationResult:
        self._require_coordinator(coordinator_token)
        if result.unit_id not in self.units:
            raise EpicOrchestrationError("PW_EPIC_UNIT_UNKNOWN", f"Unknown child {result.unit_id}.")
        run = self.state.units[result.unit_id]
        if (
            run.state not in {"active", "returned"}
            or run.handle != result.handle
            or run.attempt != result.attempt
            or result.plan_fingerprint != self.state.plan_fingerprint
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_RESULT_UNMATCHED",
                "Returned child result does not match the exact active attempt and native handle.",
            )
        if not self.state.shared_premise_valid:
            run.state = "halted"
            if run.visibility_class == "ephemeral":
                run.handle = None
            run.checkpointed = True
            run.issues = ("PW_EPIC_SHARED_PREMISE_INVALID",)
            return TaskVerificationResult(result.unit_id, False, "halted", run.issues, ())
        issues: list[str] = []
        shared_failure = False
        try:
            claimed = self._normalized_paths(result.claimed_paths)
            observed = self._normalized_paths(observed_paths)
        except EpicOrchestrationError as error:
            claimed, observed = (), ()
            issues.append(error.message)
            shared_failure = True
        if claimed != observed:
            issues.append("Child-claimed paths do not match the coordinator-observed diff.")
            shared_failure = True
        identity_pairs = (
            (result.branch, observed_branch, run.branch, "branch"),
            (
                str(Path(result.worktree).resolve()),
                str(observed_worktree.resolve()),
                run.worktree,
                "worktree",
            ),
            (result.base_commit, observed_base_commit, run.base_commit, "base commit"),
        )
        for claimed_value, observed_value, expected_value, label in identity_pairs:
            if claimed_value != observed_value or observed_value != expected_value:
                issues.append(f"Child {label} identity does not match coordinator observation.")
                shared_failure = True
        if result.head_commit != observed_head_commit or not re.fullmatch(
            r"(?:[0-9a-f]{40}|[0-9a-f]{64})", observed_head_commit
        ):
            issues.append("Child head commit identity is missing or does not match observation.")
            shared_failure = True
        duty = self.obligations[result.unit_id]
        normalized_repositories = tuple(item.strip() for item in observed_repositories)
        if (
            result.repositories != normalized_repositories
            or normalized_repositories != duty.repositories
        ):
            issues.append("Child repository scope does not match coordinator observation.")
            shared_failure = True
        if not observed:
            issues.append("Coordinator-observed child diff is empty.")
        outside = tuple(
            path
            for path in observed
            if not any(path == scope or path.startswith(scope + "/") for scope in duty.write_scope)
        )
        if outside:
            issues.append("Out-of-scope paths: " + ", ".join(outside) + ".")
            shared_failure = True
        collisions = tuple(
            path
            for path in observed
            if any(
                set(duty.repositories).intersection(self.obligations[other_id].repositories)
                and _delegation_scope_overlap(path, prior)
                for other_id, prior_paths in self.state.verified_paths
                for prior in prior_paths
            )
        )
        if collisions:
            issues.append("Integrated diff collision: " + ", ".join(collisions) + ".")
            shared_failure = True
        missing_validation = tuple(
            item for item in duty.validations if observed_validations.get(item) is not True
        )
        missing_evidence = tuple(
            item for item in duty.evidence if observed_evidence.get(item) is not True
        )
        if missing_validation:
            issues.append(
                "Required validation did not pass: " + ", ".join(missing_validation) + "."
            )
        if missing_evidence:
            issues.append("Required evidence is absent: " + ", ".join(missing_evidence) + ".")
        mismatched_claims = tuple(
            item
            for item in duty.validations
            if result.validations.get(item) is not observed_validations.get(item)
        ) + tuple(
            item
            for item in duty.evidence
            if result.evidence.get(item) is not observed_evidence.get(item)
        )
        if mismatched_claims:
            issues.append(
                "Child claims disagree with coordinator observations: "
                + ", ".join(mismatched_claims)
                + "."
            )
        if not result.success:
            issues.append("Child reported failure.")
        if not result.shared_premise_valid:
            issues.append("Child reported a shared-premise failure.")
            shared_failure = True
        if issues:
            self._fail(result.unit_id, issues, shared=shared_failure)
            return TaskVerificationResult(result.unit_id, False, "failed", tuple(issues), ())
        run.state = "verified"
        if run.visibility_class == "ephemeral":
            run.handle = None
        run.issues = ()
        run.completion_provenance = f"coordinator:{observed_head_commit}"
        self.state.verified_paths.append((result.unit_id, observed))
        newly_eligible = tuple(intent.unit_id for intent in self.launch_intents())
        return TaskVerificationResult(result.unit_id, True, "verified", (), newly_eligible)

    @staticmethod
    def _durable_reference(value: str) -> str:
        normalized = value.strip()
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/#@+-]{0,511}", normalized):
            raise EpicOrchestrationError(
                "PW_EPIC_DURABLE_RECEIPT_INVALID",
                "Durable disposition and retirement receipts must be compact opaque references.",
            )
        return normalized

    def complete_coordinator_unit(
        self,
        unit_id: str,
        *,
        observed_paths: Sequence[str],
        observed_validations: Mapping[str, bool],
        observed_evidence: Mapping[str, bool],
        provenance: str,
        coordinator_token: str,
    ) -> TaskVerificationResult:
        self._require_coordinator(coordinator_token)
        unit = self.units.get(unit_id)
        if unit is None:
            raise EpicOrchestrationError("PW_EPIC_UNIT_UNKNOWN", f"Unknown child {unit_id}.")
        run = self.state.units[unit_id]
        if (
            unit.executor != "coordinator"
            or run.state != "pending"
            or not self._dependencies_verified(unit)
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_COORDINATOR_EXECUTION_INVALID",
                f"{unit_id} is not an eligible coordinator-owned unit.",
            )
        durable_provenance = self._durable_reference(provenance)
        observed = self._normalized_paths(observed_paths)
        duty = self.obligations[unit_id]
        issues: list[str] = []
        outside = tuple(
            path
            for path in observed
            if not any(path == scope or path.startswith(scope + "/") for scope in duty.write_scope)
        )
        if outside:
            issues.append("Out-of-scope paths: " + ", ".join(outside) + ".")
        if any(observed_validations.get(item) is not True for item in duty.validations):
            issues.append("Required coordinator validation did not pass.")
        if any(observed_evidence.get(item) is not True for item in duty.evidence):
            issues.append("Required coordinator evidence is absent.")
        if issues:
            self._fail(unit_id, issues, shared=bool(outside))
            return TaskVerificationResult(unit_id, False, "failed", tuple(issues), ())
        run.state = "verified"
        run.completion_provenance = durable_provenance
        self.state.verified_paths.append((unit_id, observed))
        return TaskVerificationResult(
            unit_id,
            True,
            "verified",
            (),
            tuple(intent.unit_id for intent in self.launch_intents()),
        )

    def record_durable_disposition(
        self,
        unit_id: str,
        *,
        kind: str,
        receipt: str,
        coordinator_token: str,
    ) -> tuple[str, ...]:
        self._require_coordinator(coordinator_token)
        run = self.state.units.get(unit_id)
        if run is None:
            raise EpicOrchestrationError("PW_EPIC_UNIT_UNKNOWN", f"Unknown child {unit_id}.")
        if run.state != "verified":
            raise EpicOrchestrationError(
                "PW_EPIC_DISPOSITION_UNVERIFIED",
                "Durable disposition requires an exactly coordinator-verified result.",
            )
        if kind not in {"integrated", "no-integration"}:
            raise EpicOrchestrationError(
                "PW_EPIC_DISPOSITION_INVALID", "Disposition must be integrated or no-integration."
            )
        normalized = self._durable_reference(receipt)
        if run.disposition_state != "pending":
            if run.disposition_state == kind and run.disposition_receipt == normalized:
                return tuple(intent.unit_id for intent in self.launch_intents())
            raise EpicOrchestrationError(
                "PW_EPIC_DISPOSITION_CONFLICT", "Durable disposition cannot be rewritten."
            )
        run.disposition_state = kind
        run.disposition_receipt = normalized
        return tuple(intent.unit_id for intent in self.launch_intents())

    def retain_visible_task(
        self,
        unit_id: str,
        *,
        reason: str,
        coordinator_token: str,
        owner_promoted: bool = False,
        attention_reasons: Sequence[str] = (),
    ) -> None:
        self._require_coordinator(coordinator_token)
        run = self.state.units.get(unit_id)
        if run is None:
            raise EpicOrchestrationError("PW_EPIC_UNIT_UNKNOWN", f"Unknown child {unit_id}.")
        if run.visibility_class == "ephemeral":
            raise EpicOrchestrationError(
                "PW_EPIC_RETENTION_NOT_VISIBLE", f"{unit_id} has no visible task to retain."
            )
        normalized_reason = reason.strip().lower().replace("_", "-")
        normalized_attention = tuple(
            item.strip().lower().replace("_", "-") for item in attention_reasons
        )
        if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", normalized_reason) or any(
            not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", item) for item in normalized_attention
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_RETENTION_REASON_INVALID", "Retention reasons must be stable reason codes."
            )
        run.explicit_retain_reason = normalized_reason
        run.owner_promoted = owner_promoted
        run.attention_reasons = tuple(dict.fromkeys(normalized_attention))
        run.retirement_state = "retained"

    def _retirement_reasons(self, unit_id: str) -> tuple[str, ...]:
        run = self.state.units[unit_id]
        reasons: list[str] = []
        if run.visibility_class != "visible-retirable":
            reasons.append("task is not classified as visible-retirable")
        if run.retention_policy != "retire-on-verified":
            reasons.append("retention policy is not retire-on-verified")
        if run.state != "verified":
            reasons.append(f"execution state is {run.state}, not verified")
        if run.disposition_state not in {"integrated", "no-integration"}:
            reasons.append("durable disposition is not recorded")
        if run.handle is None:
            reasons.append("exact visible task handle is unavailable")
        if run.attention_reasons:
            reasons.append("owner attention remains: " + ", ".join(run.attention_reasons))
        if run.owner_promoted:
            reasons.append("task was owner-promoted")
        if run.explicit_retain_reason:
            reasons.append("task is explicitly retained: " + run.explicit_retain_reason)
        required = {"task-retirement", "task-retirement-reconciliation"}
        if not required.issubset(self.plan.observed_capabilities):
            reasons.append("immutable plan lacks verified retirement capability")
        if self.plan.capability_source.strip() != self.capabilities.source.strip():
            reasons.append("runtime capability source does not match the immutable plan")
        if not required.issubset(self.capabilities.verified_capabilities):
            reasons.append("current runtime lacks verified retirement capability")
        if run.retirement_state in {"confirmed", "failed", "unknown", "retained"}:
            reasons.append(f"retirement state is {run.retirement_state}")
        return tuple(reasons)

    def retirement_intents(self) -> tuple[EpicRetirementIntent, ...]:
        intents: list[EpicRetirementIntent] = []
        for unit in self.plan.units:
            run = self.state.units[unit.unit_id]
            if self._retirement_reasons(unit.unit_id):
                continue
            assert run.handle is not None
            intent_id = (
                run.retirement_intent_id
                or hashlib.sha256(
                    (
                        f"{self.state.plan_fingerprint}:{unit.unit_id}:{run.attempt}:"
                        f"{run.handle}:retire"
                    ).encode()
                ).hexdigest()
            )
            intents.append(
                EpicRetirementIntent(
                    intent_id=intent_id,
                    unit_id=unit.unit_id,
                    attempt=run.attempt,
                    handle=run.handle,
                    capability_source=self.capabilities.source,
                )
            )
        return tuple(intents)

    def register_retirement_requested(
        self,
        intent: EpicRetirementIntent,
        *,
        coordinator_token: str,
    ) -> None:
        self._require_coordinator(coordinator_token)
        expected = {item.intent_id: item for item in self.retirement_intents()}
        if expected.get(intent.intent_id) != intent:
            raise EpicOrchestrationError(
                "PW_EPIC_RETIREMENT_INTENT_INVALID",
                "Retirement request does not match one currently eligible exact task handle.",
            )
        run = self.state.units[intent.unit_id]
        if run.retirement_intent_id not in {None, intent.intent_id}:
            raise EpicOrchestrationError(
                "PW_EPIC_RETIREMENT_CONFLICT", "A visible task cannot receive a second intent."
            )
        run.retirement_intent_id = intent.intent_id
        run.retirement_state = "requested"

    def register_retirement_outcome(
        self,
        intent: EpicRetirementIntent,
        *,
        observed_handle: str,
        outcome: str,
        acknowledgement: str,
        coordinator_token: str,
    ) -> None:
        self._require_coordinator(coordinator_token)
        run = self.state.units.get(intent.unit_id)
        if run is None or run.retirement_intent_id != intent.intent_id:
            raise EpicOrchestrationError(
                "PW_EPIC_RETIREMENT_RESULT_UNMATCHED", "Retirement result has no exact request."
            )
        if observed_handle != intent.handle or observed_handle != run.handle:
            raise EpicOrchestrationError(
                "PW_EPIC_RETIREMENT_RESULT_UNMATCHED", "Retirement result handle does not match."
            )
        if outcome not in {"confirmed", "failed", "unknown"}:
            raise EpicOrchestrationError(
                "PW_EPIC_RETIREMENT_RESULT_INVALID", "Unknown retirement outcome."
            )
        normalized = self._durable_reference(acknowledgement)
        if run.retirement_state == "confirmed":
            if outcome == "confirmed" and run.retirement_ack == normalized:
                return
            raise EpicOrchestrationError(
                "PW_EPIC_RETIREMENT_CONFLICT", "Confirmed retirement cannot be rewritten."
            )
        if run.retirement_state not in {"requested", "unknown", "failed"}:
            raise EpicOrchestrationError(
                "PW_EPIC_RETIREMENT_RESULT_UNMATCHED", "Retirement result is out of sequence."
            )
        run.retirement_state = outcome
        run.retirement_ack = normalized

    def retry_retirement(self, unit_id: str, *, coordinator_token: str) -> None:
        self._require_coordinator(coordinator_token)
        run = self.state.units.get(unit_id)
        if run is None:
            raise EpicOrchestrationError("PW_EPIC_UNIT_UNKNOWN", f"Unknown child {unit_id}.")
        if run.retirement_state not in {"failed", "unknown"} or not run.retirement_intent_id:
            raise EpicOrchestrationError(
                "PW_EPIC_RETIREMENT_RETRY_INVALID", f"{unit_id} has no retryable retirement."
            )
        run.retirement_state = "pending"
        run.retirement_ack = None

    def reconcile_retirements(
        self,
        observations: Mapping[str, Mapping[str, object]],
        *,
        coordinator_token: str,
    ) -> None:
        self._require_coordinator(coordinator_token)
        for unit_id, run in self.state.units.items():
            if run.retirement_state not in {"requested", "unknown"}:
                continue
            observed = observations.get(unit_id)
            exact = bool(
                observed
                and observed.get("intent_id") == run.retirement_intent_id
                and observed.get("handle") == run.handle
            )
            observed_state = observed.get("state") if observed else None
            if exact and observed_state in {"retired", "archived", "confirmed"}:
                assert observed is not None
                acknowledgement = self._durable_reference(
                    str(observed.get("acknowledgement", "host-observed-retired"))
                )
                run.retirement_state = "confirmed"
                run.retirement_ack = acknowledgement
            elif exact and observed_state == "visible":
                run.retirement_state = "requested"
                run.retirement_ack = None
            else:
                run.retirement_state = "unknown"
                run.retirement_ack = None

    def checkpoint(self, unit_id: str, *, coordinator_token: str) -> None:
        self._require_coordinator(coordinator_token)
        run = self.state.units.get(unit_id)
        if run is None or run.state not in {"active", "returned"}:
            raise EpicOrchestrationError(
                "PW_EPIC_CHECKPOINT_INVALID", f"{unit_id} is not in flight."
            )
        run.checkpointed = True
        if not self.state.shared_premise_valid:
            run.state = "halted"
            if run.visibility_class == "ephemeral":
                run.handle = None

    def reconcile(
        self, observations: Mapping[str, Mapping[str, object]], *, coordinator_token: str
    ) -> None:
        self._require_coordinator(coordinator_token)
        active = [run for run in self.state.units.values() if run.state in {"active", "returned"}]
        persistent_active = [run for run in active if run.executor == "persistent-task"]
        if persistent_active and not self.capability_boundary()["resume_supported"]:
            raise EpicOrchestrationError(
                "PW_EPIC_RECONCILIATION_UNVERIFIED",
                "Resume requires current-session monitoring and reconciliation support.",
            )
        for unit in self.plan.units:
            run = self.state.units[unit.unit_id]
            if unit.canonical_state == "complete":
                run.state = "verified"
                if run.visibility_class == "ephemeral":
                    run.handle = None
                run.completion_provenance = (
                    f"canonical:{self.plan.target.source_path}#{self.plan.target.source_hash}"
                )
                if run.attempt == 0:
                    run.disposition_state = "integrated"
                    run.disposition_receipt = f"canonical:{self.plan.target.source_hash}"
                continue
            if run.state not in {"active", "returned"}:
                continue
            observed = observations.get(unit.unit_id)
            exact = bool(
                observed
                and observed.get("handle") == run.handle
                and observed.get("attempt") == run.attempt
                and observed.get("branch") == run.branch
                and str(Path(str(observed.get("worktree", ""))).resolve()) == run.worktree
            )
            state = observed.get("state") if observed else None
            if exact and state == "active":
                run.state = "active"
            elif exact and state in {"complete", "completed"}:
                run.state = "returned"
            elif exact and state == "failed":
                self._fail(unit.unit_id, ("Observed persistent child failure.",), shared=False)
            else:
                run.state = "orphaned"
                if run.visibility_class == "ephemeral":
                    run.handle = None
                run.issues = ("PW_EPIC_HANDLE_ORPHANED",)

    def retry(self, unit_id: str, *, coordinator_token: str) -> None:
        self._require_coordinator(coordinator_token)
        run = self.state.units.get(unit_id)
        if run is None:
            raise EpicOrchestrationError("PW_EPIC_UNIT_UNKNOWN", f"Unknown child {unit_id}.")
        if run.state not in {"failed", "orphaned"}:
            raise EpicOrchestrationError(
                "PW_EPIC_RETRY_INVALID", f"{unit_id} is not failed or orphaned."
            )
        if not self.state.shared_premise_valid:
            raise EpicOrchestrationError(
                "PW_EPIC_SHARED_PREMISE_INVALID", "A halted Epic run cannot retry in place."
            )
        if run.handle is not None and run.visibility_class != "ephemeral":
            run.prior_handles = (*run.prior_handles, run.handle)
        run.state = "pending"
        run.intent_id = None
        run.handle = None
        run.branch = None
        run.worktree = None
        run.base_commit = None
        run.issues = ()
        run.disposition_state = "pending"
        run.disposition_receipt = None
        run.retirement_intent_id = None
        run.retirement_ack = None
        run.retirement_state = (
            "pending"
            if run.visibility_class == "visible-retirable"
            else "retained"
            if run.visibility_class == "visible-retained"
            else "not-applicable"
        )
        for descendant in self._descendants(unit_id):
            descendant_run = self.state.units[descendant]
            descendant_run.blocked_by = tuple(
                blocker for blocker in descendant_run.blocked_by if blocker != unit_id
            )
            if descendant_run.state == "blocked" and not descendant_run.blocked_by:
                descendant_run.state = "pending"

    def persist(self, root: Path, *, coordinator_token: str) -> Path:
        self._require_coordinator(coordinator_token)
        stored = _load_delegation_runtime_state(root, self.plan.target.target_id)
        if stored is None:
            stored = initialize_delegation_runtime_state(root, self.plan)
        if (
            stored.get("target_id") != self.plan.target.target_id
            or stored.get("target_kind") != self.plan.target.kind
            or Path(str(stored.get("worktree", ""))).resolve() != root.resolve()
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_RUNTIME_TARGET_MISMATCH",
                "Persisted Epic runtime target or coordinator worktree does not match.",
            )
        if "epic_orchestration" in stored:
            previous = _epic_orchestration_state_from_payload(stored["epic_orchestration"])
            accepted_fingerprints = {self.state.plan_fingerprint}
            if previous.migrated_from_version == 1:
                accepted_fingerprints.add(
                    _epic_execution_fingerprint_v1(
                        self.plan, self.obligations, previous.base_commit
                    )
                )
            if previous.plan_fingerprint not in accepted_fingerprints:
                raise EpicOrchestrationError(
                    "PW_EPIC_RUNTIME_PLAN_MISMATCH",
                    "Persisted Epic runtime belongs to different approved metadata.",
                )
        stored["plan_fingerprint"] = _delegation_plan_fingerprint(self.plan)
        stored["epic_orchestration"] = _epic_orchestration_state_payload(self.state)
        projected = stored.get("units")
        assert isinstance(projected, dict)
        for unit_id, run in self.state.units.items():
            projected[unit_id] = {
                "state": (
                    "complete"
                    if run.state == "verified"
                    else (
                        "active"
                        if run.state in {"active", "returned"}
                        else (
                            "orphaned"
                            if run.state == "orphaned"
                            else (
                                "blocked"
                                if run.state in {"failed", "blocked", "halted"}
                                else "pending"
                            )
                        )
                    )
                ),
                "handle": None,
            }
        _write_delegation_runtime_state(root, self.plan, stored)
        return _delegation_runtime_path(root, self.state.target_id)

    @classmethod
    def resume(
        cls,
        *,
        root: Path,
        plan: DelegationPlan,
        obligations: Mapping[str, EpicChildObligations],
        capabilities: EpicHostCapabilities,
        coordinator_token: str,
        observations: Mapping[str, Mapping[str, object]],
        retirement_observations: Mapping[str, Mapping[str, object]] | None = None,
    ) -> EpicOrchestrator:
        stored = _load_delegation_runtime_state(root, plan.target.target_id)
        if stored is None or "epic_orchestration" not in stored:
            raise EpicOrchestrationError(
                "PW_EPIC_RUNTIME_MISSING", "No persisted Epic orchestration state exists."
            )
        restored = _epic_orchestration_state_from_payload(stored["epic_orchestration"])
        supplied_root = root.resolve()
        if (
            stored.get("target_id") != plan.target.target_id
            or stored.get("target_kind") != plan.target.kind
            or Path(str(stored.get("worktree", ""))).resolve() != supplied_root
            or Path(restored.coordinator_worktree).resolve() != supplied_root
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_RUNTIME_TARGET_MISMATCH",
                "Persisted Epic runtime target, plan, or coordinator worktree does not match.",
            )
        instance = cls(
            plan=plan,
            obligations=obligations,
            capabilities=capabilities,
            coordinator_token=coordinator_token,
            coordinator_worktree=supplied_root,
            base_commit=restored.base_commit,
        )
        accepted_fingerprints = {instance.state.plan_fingerprint}
        if restored.migrated_from_version == 1:
            accepted_fingerprints.add(
                _epic_execution_fingerprint_v1(plan, obligations, restored.base_commit)
            )
        if (
            restored.target_id != plan.target.target_id
            or restored.plan_fingerprint not in accepted_fingerprints
            or restored.coordinator_hash != instance.state.coordinator_hash
            or set(restored.units) != set(instance.units)
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_RUNTIME_PLAN_MISMATCH",
                "Persisted Epic runtime does not match the plan, units, or coordinator.",
            )
        restored.plan_fingerprint = instance.state.plan_fingerprint
        restored.migrated_from_version = None
        instance.state = restored
        instance.reconcile(observations, coordinator_token=coordinator_token)
        if retirement_observations is not None:
            instance.reconcile_retirements(
                retirement_observations, coordinator_token=coordinator_token
            )
        return instance

    def assert_child_completion_observed(
        self, unit_id: str, *, canonical_lifecycle: str, qa_passed: bool
    ) -> None:
        if unit_id not in self.units:
            raise EpicOrchestrationError("PW_EPIC_UNIT_UNKNOWN", f"Unknown child {unit_id}.")
        if canonical_lifecycle != "Complete" or not qa_passed:
            raise EpicOrchestrationError(
                "PW_EPIC_CHILD_COMPLETION_GATED",
                "Delegate verification cannot replace the child QA/Review and Complete gates.",
            )

    def assert_parent_closeout_allowed(
        self,
        *,
        children_complete: bool,
        parent_audit_passed: bool,
        deferrals_resolved: bool,
        retro_complete: bool,
        owner_completion_authority: bool,
    ) -> None:
        missing = []
        if not children_complete:
            missing.append("child completion")
        if not parent_audit_passed:
            missing.append("parent acceptance audit")
        if not deferrals_resolved:
            missing.append("deferral decisions")
        if not retro_complete:
            missing.append("Epic retro")
        if not owner_completion_authority:
            missing.append("owner completion authority")
        if missing:
            raise EpicOrchestrationError(
                "PW_EPIC_CLOSEOUT_GATED",
                "Delegate cannot certify Epic closeout; missing: " + ", ".join(missing) + ".",
            )

    def summary(self) -> dict[str, object]:
        groups: dict[str, list[str]] = {
            "verified": [],
            "failed": [],
            "blocked": [],
            "halted": [],
            "in_flight": [],
            "orphaned": [],
            "unaffected": [],
        }
        for unit in self.plan.units:
            state = self.state.units[unit.unit_id].state
            if state in {"active", "returned"}:
                groups["in_flight"].append(unit.unit_id)
            elif state in groups:
                groups[state].append(unit.unit_id)
            elif self.state.failure_seen and self.state.shared_premise_valid:
                groups["unaffected"].append(unit.unit_id)
        intents, eligibility_reasons = self._launch_evaluation()
        eligible_ids = {intent.unit_id for intent in intents}
        retirement_intents = self.retirement_intents()
        retirement_ids = {intent.unit_id for intent in retirement_intents}
        return {
            "schema_version": 2,
            "target_id": self.state.target_id,
            "shared_premise_valid": self.state.shared_premise_valid,
            "create_count": self.state.create_count,
            "capability_boundary": self.capability_boundary(),
            "eligible_creation_intents": [intent.unit_id for intent in intents],
            "creation_eligibility": {
                unit.unit_id: {
                    "eligible": unit.unit_id in eligible_ids,
                    "reasons": list(eligibility_reasons.get(unit.unit_id, ())),
                }
                for unit in self.plan.units
                if self.state.units[unit.unit_id].state == "pending"
            },
            "retirement_intents": [intent.unit_id for intent in retirement_intents],
            "lifecycle": {
                unit.unit_id: {
                    "executor": self.state.units[unit.unit_id].executor,
                    "visibility_class": self.state.units[unit.unit_id].visibility_class,
                    "retention_policy": self.state.units[unit.unit_id].retention_policy,
                    "disposition_state": self.state.units[unit.unit_id].disposition_state,
                    "retirement_state": self.state.units[unit.unit_id].retirement_state,
                    "retirement_eligible": unit.unit_id in retirement_ids,
                    "retention_reasons": list(self._retirement_reasons(unit.unit_id)),
                    "prior_visible_handles": len(self.state.units[unit.unit_id].prior_handles),
                }
                for unit in self.plan.units
            },
            **groups,
        }


DelegationSurfaceOrchestrator = EpicOrchestrator
