"""Canonical Project Workflow orchestration runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from .contracts import (
    DECOMPOSITION_PLAN_COLUMNS,
    DECOMPOSITION_PLAN_FILENAME,
    DELEGATION_CAPABILITIES,
    DELEGATION_DECOMPOSITION_PLAN_COLUMNS,
    DELEGATION_EXECUTION_NEED_TOKENS,
    DELEGATION_EXECUTION_NEEDS_DECOMPOSITION_PLAN_COLUMNS,
    DELEGATION_EXECUTOR_SURFACES,
    DELEGATION_RUNTIME_RELATIVE_DIR,
    DELEGATION_RUNTIME_SCHEMA_VERSION,
    DELEGATION_SCHEMA_VERSION,
    DELEGATION_UNIT_STATES,
    EPIC_ID_PREFIX,
)
from .lifecycle import (
    _epic_tracker_rows,
    _global_tracker_rows,
    _implementation_task_table_rows,
    _repository_scope_values,
    _resolve_epic_dir,
)
from .repository import (
    _clean_markdown_cell_path,
    _decomposition_plan_authority_issues,
    _extract_ac_ids,
    _markdown_table_rows_from_section,
)


class DelegationPlanError(ValueError):
    """Stable fail-closed error raised before a delegation launch is possible."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class DelegationTarget:
    target_id: str
    kind: str
    title: str
    lifecycle: str
    source_path: str
    source_hash: str


@dataclass(frozen=True)
class DelegationExecutionNeeds:
    """Host-neutral work properties; these are plan facts, never capability claims."""

    tokens: tuple[str, ...] = ("bounded-return",)
    durable_resume: bool = False
    direct_owner_steering: bool = False
    isolated_worktree: bool = False
    peer_group: str | None = None
    execution_benefit: str | None = None
    expected_overhead: str | None = None
    benefit_overhead_basis: str | None = None
    earned_surface_required: bool = False

    @property
    def requested_executor(self) -> str:
        if self.peer_group is not None:
            return "peer-team"
        if self.durable_resume or self.direct_owner_steering:
            return "persistent-task"
        if self.earned_surface_required and self.execution_benefit is None:
            return "coordinator"
        return "subagent"

    def properties(self) -> dict[str, object]:
        properties: dict[str, object] = {
            "tokens": list(self.tokens),
            "durability": "durable-resume" if self.durable_resume else "bounded-return",
            "isolation": "isolated-worktree" if self.isolated_worktree else "shared-worktree",
            "communication": "peer" if self.peer_group is not None else "coordinator-mediated",
            "peer_group": self.peer_group,
            "owner_interaction": (
                "direct-owner-steering" if self.direct_owner_steering else "coordinator-mediated"
            ),
        }
        if self.earned_surface_required or any(
            (self.execution_benefit, self.expected_overhead, self.benefit_overhead_basis)
        ):
            properties.update(
                {
                    "execution_benefit": self.execution_benefit,
                    "expected_overhead": self.expected_overhead,
                    "benefit_overhead_basis": self.benefit_overhead_basis,
                }
            )
        return properties


@dataclass(frozen=True)
class DelegationUnit:
    unit_id: str
    title: str
    dependencies: tuple[str, ...]
    write_scope: tuple[str, ...]
    parallel_safe: bool
    canonical_state: str
    source_order: int
    source_path: str
    authority_acs: tuple[str, ...] = ()
    execution_needs: DelegationExecutionNeeds = field(default_factory=DelegationExecutionNeeds)
    repository_scope: tuple[str, ...] = (".",)


@dataclass(frozen=True)
class DelegationPlannedUnit:
    unit_id: str
    title: str
    dependencies: tuple[str, ...]
    write_scope: tuple[str, ...]
    parallel_safe: bool
    canonical_state: str
    readiness: str
    blocking_reasons: tuple[str, ...]
    execution_needs: DelegationExecutionNeeds
    repository_scope: tuple[str, ...]
    requested_executor: str
    executor: str
    schedule: str
    visibility_class: str
    retention_policy: str
    required_child_slots: int
    executor_reason: str
    source_path: str
    authority_acs: tuple[str, ...] = ()


@dataclass(frozen=True)
class DelegationPlan:
    target: DelegationTarget
    units: tuple[DelegationPlannedUnit, ...]
    selected_units: tuple[str, ...]
    eligible_units: tuple[str, ...]
    blocked_units: tuple[str, ...]
    requested_concurrency: int
    available_child_capacity: int
    effective_concurrency: int
    effective_child_concurrency: int
    effective_child_slots: int
    concurrency_reason: str
    observed_capabilities: tuple[str, ...]
    capability_matrix: tuple[DelegationCapabilityObservation, ...]
    capability_source: str
    persistent_task_authority: str | None
    provenance: tuple[str, ...]


@dataclass(frozen=True)
class DelegationCapabilityObservation:
    capability: str
    state: str
    provenance: str


class TaskOrchestrationError(ValueError):
    """Stable fail-closed error for Task work-item execution."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _normalize_orchestration_paths(paths: Sequence[str]) -> tuple[str, ...]:
    normalized: set[str] = set()
    for path in paths:
        value = path.strip().replace("\\", "/")
        parts = tuple(item for item in value.split("/") if item not in {"", "."})
        if (
            not parts
            or value.startswith("/")
            or ".." in parts
            or any(character in value for character in "*?[]{}")
        ):
            raise TaskOrchestrationError(
                "PW_TASK_DIFF_INVALID", f"Invalid repository-relative diff path: {path}."
            )
        normalized.add("/".join(parts))
    return tuple(sorted(normalized))


@dataclass(frozen=True)
class TaskHostCapabilities:
    source: str
    current_session_verified: bool
    bounded_subagents: bool
    available_child_capacity: int
    additional_capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.available_child_capacity < 0:
            raise TaskOrchestrationError(
                "PW_TASK_CAPACITY_INVALID", "Available child capacity cannot be negative."
            )
        if self.bounded_subagents and (
            not self.current_session_verified or not self.source.strip()
        ):
            raise TaskOrchestrationError(
                "PW_TASK_CAPABILITY_UNVERIFIED",
                "Bounded subagent execution requires verified current-session capabilities.",
            )
        unknown = sorted(set(self.additional_capabilities) - set(DELEGATION_CAPABILITIES))
        if unknown:
            raise TaskOrchestrationError(
                "PW_TASK_CAPABILITY_UNKNOWN",
                "Unknown Task runtime capability: " + ", ".join(unknown) + ".",
            )
        if self.additional_capabilities and (
            not self.current_session_verified or not self.source.strip()
        ):
            raise TaskOrchestrationError(
                "PW_TASK_CAPABILITY_UNVERIFIED",
                "Additional Task host capabilities require a named current-session observation source.",
            )

    @property
    def verified_capabilities(self) -> frozenset[str]:
        capabilities = set(self.additional_capabilities)
        if self.bounded_subagents:
            capabilities.add("subagent")
        return frozenset(capabilities) if self.current_session_verified else frozenset()


@dataclass(frozen=True)
class TaskExecutionObligations:
    acceptance_criteria: tuple[str, ...]
    validations: tuple[str, ...]
    evidence: tuple[str, ...]
    repositories: tuple[str, ...] = (".",)

    def __post_init__(self) -> None:
        fields = {
            "acceptance criteria": self.acceptance_criteria,
            "validations": self.validations,
            "evidence": self.evidence,
            "repositories": self.repositories,
        }
        for label, values in fields.items():
            normalized = tuple(value.strip() for value in values)
            if not normalized or any(not value for value in normalized):
                raise TaskOrchestrationError(
                    "PW_TASK_PACKET_OBLIGATIONS_INVALID",
                    f"Task work packet {label} must be non-empty.",
                )
            if len(set(normalized)) != len(normalized):
                raise TaskOrchestrationError(
                    "PW_TASK_PACKET_OBLIGATIONS_INVALID",
                    f"Task work packet {label} must not contain duplicates.",
                )
            object.__setattr__(self, label.replace(" ", "_"), normalized)
        if any(
            repository != "." and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", repository)
            for repository in self.repositories
        ):
            raise TaskOrchestrationError(
                "PW_TASK_PACKET_OBLIGATIONS_INVALID",
                "Task work packet repositories must be '.' or registered repository IDs.",
            )


@dataclass(frozen=True)
class TaskExecutorDecision:
    unit_id: str
    executor: str
    launchable: bool
    reason: str


@dataclass(frozen=True)
class TaskWorkPacket:
    target_id: str
    target_source: str
    target_source_hash: str
    unit_id: str
    unit_title: str
    acceptance_criteria: tuple[str, ...]
    verified_dependencies: tuple[str, ...]
    write_scope: tuple[str, ...]
    repositories: tuple[str, ...]
    validations: tuple[str, ...]
    evidence: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    baseline_hash: str
    plan_fingerprint: str
    executor: str
    attempt: int

    def payload(self) -> dict[str, object]:
        return {
            "schema_version": 2,
            "target": {
                "id": self.target_id,
                "kind": "task",
                "authority_source": self.target_source,
                "authority_hash": self.target_source_hash,
            },
            "unit": {"id": self.unit_id, "title": self.unit_title},
            "acceptance_criteria": list(self.acceptance_criteria),
            "verified_dependencies": list(self.verified_dependencies),
            "scope": {
                "write_prefixes": list(self.write_scope),
                "repositories": list(self.repositories),
            },
            "obligations": {
                "validation": list(self.validations),
                "evidence": list(self.evidence),
            },
            "forbidden_actions": list(self.forbidden_actions),
            "stop_conditions": list(self.stop_conditions),
            "invalid_substitutes": list(WORK_PACKET_INVALID_SUBSTITUTES),
            "return_contract": list(WORK_PACKET_RETURN_CONTRACT),
            "baseline_hash": self.baseline_hash,
            "plan_fingerprint": self.plan_fingerprint,
            "executor": self.executor,
            "attempt": self.attempt,
            "persistent_task_intent": None,
        }


@dataclass(frozen=True)
class TaskWorkerResult:
    unit_id: str
    handle: str
    success: bool
    claimed_paths: tuple[str, ...]
    validations: Mapping[str, bool]
    evidence: Mapping[str, bool]
    baseline_hash: str
    shared_state_hash: str
    plan_fingerprint: str
    attempt: int
    shared_premise_valid: bool = True
    failure_reason: str = ""


@dataclass(frozen=True)
class TaskVerificationResult:
    unit_id: str
    accepted: bool
    state: str
    issues: tuple[str, ...]
    newly_eligible: tuple[str, ...]


@dataclass
class TaskUnitRun:
    state: str = "pending"
    attempt: int = 0
    handle: str | None = None
    executor: str | None = None
    baseline_hash: str | None = None
    baseline_revision: int = 0
    checkpointed: bool = False
    issues: tuple[str, ...] = ()
    canonical_blocked: bool = False
    blocked_by: tuple[str, ...] = ()
    completion_provenance: str | None = None


@dataclass
class TaskOrchestrationState:
    schema_version: int
    target_id: str
    plan_fingerprint: str
    coordinator_hash: str
    shared_state_hash: str
    lifecycle: str
    units: dict[str, TaskUnitRun]
    shared_premise_valid: bool = True
    integration_revision: int = 0
    integrated_paths: list[tuple[int, str, tuple[str, ...]]] = field(default_factory=list)
    failure_seen: bool = False
    used_handles: set[str] = field(default_factory=set)
    shared_state_revisions: list[tuple[str, str]] = field(default_factory=list)


def _task_orchestration_state_payload(state: TaskOrchestrationState) -> dict[str, object]:
    return {
        "schema_version": state.schema_version,
        "target_id": state.target_id,
        "plan_fingerprint": state.plan_fingerprint,
        "coordinator_hash": state.coordinator_hash,
        "shared_state_hash": state.shared_state_hash,
        "lifecycle": state.lifecycle,
        "shared_premise_valid": state.shared_premise_valid,
        "integration_revision": state.integration_revision,
        "failure_seen": state.failure_seen,
        "used_handles": sorted(state.used_handles),
        "shared_state_revisions": [list(item) for item in state.shared_state_revisions],
        "integrated_paths": [
            [revision, unit_id, list(paths)] for revision, unit_id, paths in state.integrated_paths
        ],
        "units": {
            unit_id: {
                "state": run.state,
                "attempt": run.attempt,
                "handle": run.handle,
                "executor": run.executor,
                "baseline_hash": run.baseline_hash,
                "baseline_revision": run.baseline_revision,
                "checkpointed": run.checkpointed,
                "issues": list(run.issues),
                "canonical_blocked": run.canonical_blocked,
                "blocked_by": list(run.blocked_by),
                "completion_provenance": run.completion_provenance,
            }
            for unit_id, run in state.units.items()
        },
    }


def _task_orchestration_state_from_payload(payload: object) -> TaskOrchestrationState:
    if not isinstance(payload, dict):
        raise TaskOrchestrationError(
            "PW_TASK_RUNTIME_INVALID", "Task orchestration runtime must be an object."
        )
    allowed = {
        "schema_version",
        "target_id",
        "plan_fingerprint",
        "coordinator_hash",
        "shared_state_hash",
        "lifecycle",
        "shared_premise_valid",
        "integration_revision",
        "failure_seen",
        "used_handles",
        "shared_state_revisions",
        "integrated_paths",
        "units",
    }
    unknown = set(payload) - allowed
    if unknown:
        raise TaskOrchestrationError(
            "PW_TASK_RUNTIME_PRIVATE_FIELD",
            "Task runtime contains forbidden fields: " + ", ".join(sorted(unknown)) + ".",
        )
    if (
        payload.get("schema_version") != 1
        or not isinstance(payload.get("target_id"), str)
        or not isinstance(payload.get("plan_fingerprint"), str)
        or not isinstance(payload.get("coordinator_hash"), str)
        or not isinstance(payload.get("shared_state_hash"), str)
        or payload.get("lifecycle") != "In Progress"
        or not isinstance(payload.get("shared_premise_valid"), bool)
        or not isinstance(payload.get("integration_revision"), int)
        or not isinstance(payload.get("failure_seen"), bool)
        or not isinstance(payload.get("used_handles"), list)
        or not isinstance(payload.get("shared_state_revisions"), list)
        or not isinstance(payload.get("integrated_paths"), list)
        or not isinstance(payload.get("units"), dict)
    ):
        raise TaskOrchestrationError(
            "PW_TASK_RUNTIME_INVALID", "Task orchestration runtime schema is invalid."
        )
    raw_units = payload["units"]
    assert isinstance(raw_units, dict)
    units: dict[str, TaskUnitRun] = {}
    unit_allowed = {
        "state",
        "attempt",
        "handle",
        "executor",
        "baseline_hash",
        "baseline_revision",
        "checkpointed",
        "issues",
        "canonical_blocked",
        "blocked_by",
        "completion_provenance",
    }
    valid_states = {
        "pending",
        "active",
        "returned",
        "done",
        "failed",
        "blocked",
        "halted",
        "orphaned",
    }
    for unit_id, raw in raw_units.items():
        if not isinstance(unit_id, str) or not isinstance(raw, dict) or set(raw) - unit_allowed:
            raise TaskOrchestrationError(
                "PW_TASK_RUNTIME_PRIVATE_FIELD",
                f"{unit_id} runtime entry has forbidden or malformed fields.",
            )
        if (
            raw.get("state") not in valid_states
            or not isinstance(raw.get("attempt"), int)
            or raw.get("attempt", -1) < 0
            or raw.get("handle") is not None
            and not isinstance(raw.get("handle"), str)
            or raw.get("executor") is not None
            and not isinstance(raw.get("executor"), str)
            or raw.get("baseline_hash") is not None
            and not isinstance(raw.get("baseline_hash"), str)
            or not isinstance(raw.get("baseline_revision"), int)
            or not isinstance(raw.get("checkpointed"), bool)
            or not isinstance(raw.get("issues"), list)
            or not all(isinstance(item, str) for item in raw.get("issues", []))
            or not isinstance(raw.get("canonical_blocked"), bool)
            or not isinstance(raw.get("blocked_by"), list)
            or not all(isinstance(item, str) for item in raw.get("blocked_by", []))
            or raw.get("completion_provenance") is not None
            and not isinstance(raw.get("completion_provenance"), str)
        ):
            raise TaskOrchestrationError(
                "PW_TASK_RUNTIME_INVALID", f"{unit_id} runtime entry is invalid."
            )
        units[unit_id] = TaskUnitRun(
            state=str(raw["state"]),
            attempt=int(raw["attempt"]),
            handle=raw.get("handle"),
            executor=raw.get("executor"),
            baseline_hash=raw.get("baseline_hash"),
            baseline_revision=int(raw["baseline_revision"]),
            checkpointed=bool(raw["checkpointed"]),
            issues=tuple(raw["issues"]),
            canonical_blocked=bool(raw["canonical_blocked"]),
            blocked_by=tuple(raw["blocked_by"]),
            completion_provenance=raw.get("completion_provenance"),
        )
    used_handles = payload["used_handles"]
    assert isinstance(used_handles, list)
    if not all(isinstance(item, str) and item for item in used_handles):
        raise TaskOrchestrationError("PW_TASK_RUNTIME_INVALID", "Task runtime handles are invalid.")
    raw_integrated = payload["integrated_paths"]
    assert isinstance(raw_integrated, list)
    integrated_paths: list[tuple[int, str, tuple[str, ...]]] = []
    for item in raw_integrated:
        if (
            not isinstance(item, list)
            or len(item) != 3
            or not isinstance(item[0], int)
            or not isinstance(item[1], str)
            or not isinstance(item[2], list)
            or not all(isinstance(path, str) for path in item[2])
        ):
            raise TaskOrchestrationError(
                "PW_TASK_RUNTIME_INVALID", "Integrated path history is invalid."
            )
        integrated_paths.append((item[0], item[1], tuple(item[2])))
    raw_revisions = payload["shared_state_revisions"]
    assert isinstance(raw_revisions, list)
    revisions: list[tuple[str, str]] = []
    for item in raw_revisions:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not all(isinstance(value, str) and value for value in item)
        ):
            raise TaskOrchestrationError(
                "PW_TASK_RUNTIME_INVALID", "Shared-state revision history is invalid."
            )
        revisions.append((item[0], item[1]))
    return TaskOrchestrationState(
        schema_version=1,
        target_id=str(payload["target_id"]),
        plan_fingerprint=str(payload["plan_fingerprint"]),
        coordinator_hash=str(payload["coordinator_hash"]),
        shared_state_hash=str(payload["shared_state_hash"]),
        lifecycle="In Progress",
        units=units,
        shared_premise_valid=bool(payload["shared_premise_valid"]),
        integration_revision=int(payload["integration_revision"]),
        integrated_paths=integrated_paths,
        failure_seen=bool(payload["failure_seen"]),
        used_handles=set(used_handles),
        shared_state_revisions=revisions,
    )


TASK_WORKER_FORBIDDEN_ACTIONS = (
    "mutate shared workflow artifacts, runtime state, or Task lifecycle",
    "push, merge, release, deploy, or contact third parties",
    "create persistent Codex tasks or worktrees",
    "write outside the allowed repository-relative prefixes",
)

TASK_WORKER_STOP_CONDITIONS = (
    "scope, validation, or evidence obligations cannot be satisfied",
    "the observed diff leaves the allowed scope",
    "the shared baseline changes or another worker collides",
    "a shared-premise failure invalidates the run",
)

WORK_PACKET_INVALID_SUBSTITUTES = (
    "a worker completion claim without the required validation and evidence",
    "green lower-layer validation substituted for a higher proof obligation",
    "authority, evidence, or source from another revision or scope",
    "full conversation history substituted for this bounded authority packet",
)

WORK_PACKET_RETURN_CONTRACT = (
    "worker identity plus the exact launch identity and attempt",
    "authority source and hash actually used",
    "actual changed scope and coordinator-observable diff",
    "required validation and evidence results",
    "material decisions, risks, and blockers",
    "dependency result and shared-premise validity",
)


def _task_worker_path_forbidden(path: str) -> bool:
    if path == ".git" or path.startswith(".git/"):
        return True
    if path == ".project-workflow/cli/workflow.py":
        return False
    return path == ".project-workflow" or path.startswith(".project-workflow/")


def _task_worker_scope_forbidden(scope: str) -> bool:
    if scope == ".git" or scope.startswith(".git/"):
        return True
    if scope == ".project-workflow/cli/workflow.py":
        return False
    return scope == "." or scope == ".project-workflow" or scope.startswith(".project-workflow/")


def _task_execution_fingerprint(
    plan: DelegationPlan,
    obligations: Mapping[str, TaskExecutionObligations],
) -> str:
    payload = {
        "target": {
            "id": plan.target.target_id,
            "kind": plan.target.kind,
            "source": plan.target.source_path,
        },
        "units": [
            {
                "id": unit.unit_id,
                "title": unit.title,
                "dependencies": unit.dependencies,
                "write_scope": unit.write_scope,
                "parallel_safe": unit.parallel_safe,
                "execution_needs": unit.execution_needs.properties(),
                "requested_executor": unit.requested_executor,
                "executor": unit.executor,
                "schedule": unit.schedule,
                "visibility_class": unit.visibility_class,
                "retention_policy": unit.retention_policy,
                "obligations": {
                    "acceptance_criteria": obligations[unit.unit_id].acceptance_criteria,
                    "validations": obligations[unit.unit_id].validations,
                    "evidence": obligations[unit.unit_id].evidence,
                    "repositories": obligations[unit.unit_id].repositories,
                },
            }
            for unit in plan.units
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


class EpicOrchestrationError(ValueError):
    """Stable fail-closed error for Epic child-Task orchestration."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _epic_opaque_handle_valid(value: object) -> bool:
    return bool(
        isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}", value)
    )


@dataclass(frozen=True)
class EpicHostCapabilities:
    source: str
    current_session_verified: bool
    persistent_tasks: bool
    isolated_worktrees: bool
    monitoring: bool
    reconciliation: bool
    available_child_capacity: int
    additional_capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.available_child_capacity < 0:
            raise EpicOrchestrationError(
                "PW_EPIC_CAPACITY_INVALID", "Available persistent-task capacity cannot be negative."
            )
        claims_support = any(
            (
                self.persistent_tasks,
                self.isolated_worktrees,
                self.monitoring,
                self.reconciliation,
            )
        )
        if claims_support and (not self.current_session_verified or not self.source.strip()):
            raise EpicOrchestrationError(
                "PW_EPIC_CAPABILITY_UNVERIFIED",
                "Epic host capabilities require a named current-session observation source.",
            )
        unknown = sorted(set(self.additional_capabilities) - set(DELEGATION_CAPABILITIES))
        if unknown:
            raise EpicOrchestrationError(
                "PW_EPIC_CAPABILITY_UNKNOWN",
                "Unknown Epic runtime capability: " + ", ".join(unknown) + ".",
            )
        if self.additional_capabilities and (
            not self.current_session_verified or not self.source.strip()
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_CAPABILITY_UNVERIFIED",
                "Additional Epic host capabilities require a named current-session observation source.",
            )

    @property
    def creation_supported(self) -> bool:
        return bool(
            self.current_session_verified
            and self.persistent_tasks
            and self.monitoring
            and self.reconciliation
            and self.available_child_capacity > 0
        )

    @property
    def verified_capabilities(self) -> frozenset[str]:
        capabilities = set(self.additional_capabilities)
        if self.persistent_tasks:
            capabilities.add("persistent-task")
        if self.isolated_worktrees:
            capabilities.update({"isolated-worktree", "persistent-task-isolated-worktree"})
        if self.monitoring:
            capabilities.add("task-monitoring")
        if self.reconciliation:
            capabilities.add("task-reconciliation")
        return frozenset(capabilities) if self.current_session_verified else frozenset()


@dataclass(frozen=True)
class EpicChildObligations:
    parent_acs: tuple[str, ...]
    repositories: tuple[str, ...]
    write_scope: tuple[str, ...]
    validations: tuple[str, ...]
    evidence: tuple[str, ...]

    def __post_init__(self) -> None:
        fields = {
            "parent ACs": ("parent_acs", self.parent_acs),
            "repositories": ("repositories", self.repositories),
            "write scope": ("write_scope", self.write_scope),
            "validations": ("validations", self.validations),
            "evidence": ("evidence", self.evidence),
        }
        for label, (attribute, values) in fields.items():
            normalized = tuple(value.strip() for value in values)
            if not normalized or any(not value for value in normalized):
                raise EpicOrchestrationError(
                    "PW_EPIC_PACKET_OBLIGATIONS_INVALID",
                    f"Epic child packet {label} must be non-empty.",
                )
            if len(set(normalized)) != len(normalized):
                raise EpicOrchestrationError(
                    "PW_EPIC_PACKET_OBLIGATIONS_INVALID",
                    f"Epic child packet {label} must not contain duplicates.",
                )
            object.__setattr__(self, attribute, normalized)
        if any(not re.fullmatch(r"AC\d+", ac_id) for ac_id in self.parent_acs):
            raise EpicOrchestrationError(
                "PW_EPIC_PACKET_OBLIGATIONS_INVALID",
                "Epic child packet parent ACs must use canonical AC<number> identities.",
            )
        try:
            normalized_scope = _normalize_orchestration_paths(self.write_scope)
        except TaskOrchestrationError as error:
            raise EpicOrchestrationError(
                "PW_EPIC_PACKET_OBLIGATIONS_INVALID", error.message
            ) from error
        object.__setattr__(self, "write_scope", normalized_scope)
        if any(
            repository != "." and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", repository)
            for repository in self.repositories
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_PACKET_OBLIGATIONS_INVALID",
                "Epic child repositories must be '.' or registered repository IDs.",
            )


EPIC_CHILD_FORBIDDEN_ACTIONS = (
    "mutate the global or parent Epic tracker, acceptance map, lifecycle, or delegation runtime",
    "mutate another child Task or repository outside the packet scope",
    "mark the child Complete or self-certify parent Epic closeout",
    "push, merge, release, deploy, or contact third parties",
)

EPIC_CHILD_STOP_CONDITIONS = (
    "child authority, parent AC coverage, or dependency identity no longer matches",
    "branch, worktree, repository, validation, or evidence scope cannot be verified",
    "the observed diff leaves the permitted child scope or collides with integrated work",
    "a shared-premise failure invalidates the coordinator baseline",
)


@dataclass(frozen=True)
class EpicChildWorkPacket:
    target_id: str
    target_kind: str
    target_source: str
    target_source_hash: str
    unit_id: str
    unit_title: str
    parent_acs: tuple[str, ...]
    verified_dependencies: tuple[str, ...]
    repositories: tuple[str, ...]
    write_scope: tuple[str, ...]
    validations: tuple[str, ...]
    evidence: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    base_commit: str
    plan_fingerprint: str
    executor: str
    visibility_class: str
    retention_policy: str
    isolated_worktree_required: bool
    attempt: int

    def payload(self) -> dict[str, object]:
        return {
            "schema_version": 2,
            "target": {
                "id": self.target_id,
                "kind": self.target_kind,
                "authority_source": self.target_source,
                "authority_hash": self.target_source_hash,
            },
            "unit": {
                "id": self.unit_id,
                "kind": "epic-child" if self.target_kind == "epic" else "task-unit",
                "title": self.unit_title,
                "parent_acs": list(self.parent_acs),
            },
            "verified_dependencies": list(self.verified_dependencies),
            "scope": {
                "repositories": list(self.repositories),
                "write_prefixes": list(self.write_scope),
                "isolated_worktree_required": self.isolated_worktree_required,
            },
            "obligations": {
                "validation": list(self.validations),
                "evidence": list(self.evidence),
            },
            "forbidden_actions": list(self.forbidden_actions),
            "stop_conditions": list(self.stop_conditions),
            "invalid_substitutes": list(WORK_PACKET_INVALID_SUBSTITUTES),
            "return_contract": list(WORK_PACKET_RETURN_CONTRACT),
            "base_commit": self.base_commit,
            "plan_fingerprint": self.plan_fingerprint,
            "executor": self.executor,
            "visibility_class": self.visibility_class,
            "retention_policy": self.retention_policy,
            "attempt": self.attempt,
        }


@dataclass(frozen=True)
class EpicLaunchIntent:
    intent_id: str
    unit_id: str
    attempt: int
    executor: str
    packet: EpicChildWorkPacket
    capability_source: str

    def payload(self) -> dict[str, object]:
        operation = {
            "subagent": "launch-subagent",
            "persistent-task": "create-persistent-task",
            "peer-team": "launch-peer-team",
        }.get(self.executor, "launch-worker")
        return {
            "schema_version": 1,
            "intent_id": self.intent_id,
            "operation": operation,
            "unit_id": self.unit_id,
            "attempt": self.attempt,
            "executor": self.executor,
            "capability_source": self.capability_source,
            "work_packet": self.packet.payload(),
        }


@dataclass(frozen=True)
class PersistentTaskCreationIntent:
    intent_id: str
    unit_id: str
    attempt: int
    packet: EpicChildWorkPacket
    capability_source: str

    def payload(self) -> dict[str, object]:
        requires = ["persistent-task", "task-monitoring", "task-reconciliation"]
        if self.packet.isolated_worktree_required:
            requires.append("isolated-worktree")
        if self.packet.retention_policy == "retire-on-verified":
            requires.extend(("task-retirement", "task-retirement-reconciliation"))
        return {
            "schema_version": 1,
            "intent_id": self.intent_id,
            "operation": "create-persistent-task",
            "unit_id": self.unit_id,
            "attempt": self.attempt,
            "requires": requires,
            "capability_source": self.capability_source,
            "work_packet": self.packet.payload(),
        }


@dataclass(frozen=True)
class EpicRetirementIntent:
    intent_id: str
    unit_id: str
    attempt: int
    handle: str
    capability_source: str

    def payload(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "intent_id": self.intent_id,
            "operation": "retire-visible-task",
            "unit_id": self.unit_id,
            "attempt": self.attempt,
            "handle": self.handle,
            "requires": ["task-retirement", "task-retirement-reconciliation"],
            "capability_source": self.capability_source,
        }


@dataclass(frozen=True)
class EpicChildResult:
    unit_id: str
    handle: str
    attempt: int
    branch: str
    worktree: str
    base_commit: str
    head_commit: str
    success: bool
    claimed_paths: tuple[str, ...]
    validations: Mapping[str, bool]
    evidence: Mapping[str, bool]
    repositories: tuple[str, ...]
    plan_fingerprint: str
    shared_premise_valid: bool = True
    failure_reason: str = ""


@dataclass
class EpicUnitRun:
    state: str = "pending"
    attempt: int = 0
    intent_id: str | None = None
    handle: str | None = None
    branch: str | None = None
    worktree: str | None = None
    base_commit: str | None = None
    checkpointed: bool = False
    issues: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()
    completion_provenance: str | None = None
    executor: str = "coordinator"
    visibility_class: str = "ephemeral"
    retention_policy: str = "not-applicable"
    disposition_state: str = "pending"
    disposition_receipt: str | None = None
    attention_reasons: tuple[str, ...] = ()
    owner_promoted: bool = False
    explicit_retain_reason: str | None = None
    retirement_state: str = "not-applicable"
    retirement_intent_id: str | None = None
    retirement_ack: str | None = None
    prior_handles: tuple[str, ...] = ()


@dataclass
class EpicOrchestrationState:
    schema_version: int
    target_id: str
    plan_fingerprint: str
    coordinator_hash: str
    coordinator_worktree: str
    base_commit: str
    units: dict[str, EpicUnitRun]
    shared_premise_valid: bool = True
    failure_seen: bool = False
    create_count: int = 0
    used_intents: set[str] = field(default_factory=set)
    used_handles: set[str] = field(default_factory=set)
    verified_paths: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)
    migrated_from_version: int | None = None


def _epic_orchestration_state_payload(state: EpicOrchestrationState) -> dict[str, object]:
    return {
        "schema_version": 2,
        "target_id": state.target_id,
        "plan_fingerprint": state.plan_fingerprint,
        "coordinator_hash": state.coordinator_hash,
        "coordinator_worktree": state.coordinator_worktree,
        "base_commit": state.base_commit,
        "shared_premise_valid": state.shared_premise_valid,
        "failure_seen": state.failure_seen,
        "create_count": state.create_count,
        "used_intents": sorted(state.used_intents),
        "used_handles": sorted(state.used_handles),
        "verified_paths": [[unit_id, list(paths)] for unit_id, paths in state.verified_paths],
        "units": {
            unit_id: {
                "state": run.state,
                "attempt": run.attempt,
                "intent_id": run.intent_id,
                "handle": run.handle,
                "branch": run.branch,
                "worktree": run.worktree,
                "base_commit": run.base_commit,
                "checkpointed": run.checkpointed,
                "issues": list(run.issues),
                "blocked_by": list(run.blocked_by),
                "completion_provenance": run.completion_provenance,
                "executor": run.executor,
                "visibility_class": run.visibility_class,
                "retention_policy": run.retention_policy,
                "disposition_state": run.disposition_state,
                "disposition_receipt": run.disposition_receipt,
                "attention_reasons": list(run.attention_reasons),
                "owner_promoted": run.owner_promoted,
                "explicit_retain_reason": run.explicit_retain_reason,
                "retirement_state": run.retirement_state,
                "retirement_intent_id": run.retirement_intent_id,
                "retirement_ack": run.retirement_ack,
                "prior_handles": list(run.prior_handles),
            }
            for unit_id, run in state.units.items()
        },
    }


def _epic_orchestration_state_from_payload(payload: object) -> EpicOrchestrationState:
    if not isinstance(payload, dict):
        raise EpicOrchestrationError(
            "PW_EPIC_RUNTIME_INVALID", "Epic orchestration runtime must be an object."
        )
    schema_version = payload.get("schema_version")
    if schema_version not in {1, 2}:
        raise EpicOrchestrationError(
            "PW_EPIC_RUNTIME_INVALID", "Epic orchestration runtime schema is invalid."
        )
    allowed = {
        "schema_version",
        "target_id",
        "plan_fingerprint",
        "coordinator_hash",
        "coordinator_worktree",
        "base_commit",
        "shared_premise_valid",
        "failure_seen",
        "create_count",
        "used_intents",
        "used_handles",
        "units",
    }
    allowed.add("integrated_paths" if schema_version == 1 else "verified_paths")
    if set(payload) - allowed:
        raise EpicOrchestrationError(
            "PW_EPIC_RUNTIME_PRIVATE_FIELD",
            "Epic runtime contains forbidden fields: "
            + ", ".join(sorted(set(payload) - allowed))
            + ".",
        )
    required_strings = (
        "target_id",
        "plan_fingerprint",
        "coordinator_hash",
        "coordinator_worktree",
        "base_commit",
    )
    if (
        any(
            not isinstance(payload.get(key), str) or not payload.get(key)
            for key in required_strings
        )
        or not isinstance(payload.get("shared_premise_valid"), bool)
        or not isinstance(payload.get("failure_seen"), bool)
        or not isinstance(payload.get("create_count"), int)
        or int(payload.get("create_count", -1)) < 0
        or not isinstance(payload.get("used_intents"), list)
        or not isinstance(payload.get("used_handles"), list)
        or not isinstance(
            payload.get("integrated_paths" if schema_version == 1 else "verified_paths"),
            list,
        )
        or not isinstance(payload.get("units"), dict)
    ):
        raise EpicOrchestrationError(
            "PW_EPIC_RUNTIME_INVALID", "Epic orchestration runtime schema is invalid."
        )
    used_intents = payload["used_intents"]
    used_handles = payload["used_handles"]
    if not all(
        isinstance(item, str) and re.fullmatch(r"[0-9a-f]{64}", item) for item in used_intents
    ) or not all(_epic_opaque_handle_valid(item) for item in used_handles):
        raise EpicOrchestrationError(
            "PW_EPIC_RUNTIME_INVALID", "Epic runtime intent or handle identities are invalid."
        )
    if (
        int(payload["create_count"]) != len(used_intents)
        or len(used_intents) != len(used_handles)
        or len(set(used_intents)) != len(used_intents)
        or len(set(used_handles)) != len(used_handles)
    ):
        raise EpicOrchestrationError(
            "PW_EPIC_RUNTIME_INVALID", "Epic runtime creation identity counts are inconsistent."
        )
    raw_verified = payload["integrated_paths" if schema_version == 1 else "verified_paths"]
    verified_paths: list[tuple[str, tuple[str, ...]]] = []
    for item in raw_verified:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not isinstance(item[0], str)
            or not isinstance(item[1], list)
            or not all(isinstance(path, str) for path in item[1])
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_RUNTIME_INVALID", "Epic verified path history is invalid."
            )
        verified_paths.append((item[0], tuple(item[1])))
    units: dict[str, EpicUnitRun] = {}
    unit_allowed = {
        "state",
        "attempt",
        "intent_id",
        "handle",
        "branch",
        "worktree",
        "base_commit",
        "checkpointed",
        "issues",
        "blocked_by",
        "completion_provenance",
    }
    if schema_version == 2:
        unit_allowed.update(
            {
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
            }
        )
    valid_states = {
        "pending",
        "active",
        "returned",
        "verified",
        "failed",
        "blocked",
        "halted",
        "orphaned",
    }
    raw_units = payload["units"]
    assert isinstance(raw_units, dict)
    for unit_id, raw in raw_units.items():
        if not isinstance(unit_id, str) or not isinstance(raw, dict) or set(raw) - unit_allowed:
            raise EpicOrchestrationError(
                "PW_EPIC_RUNTIME_PRIVATE_FIELD", f"{unit_id} runtime entry is malformed."
            )
        optional_strings = (
            "intent_id",
            "handle",
            "branch",
            "worktree",
            "base_commit",
            "completion_provenance",
            "disposition_receipt",
            "explicit_retain_reason",
            "retirement_intent_id",
            "retirement_ack",
        )
        intent_id = raw.get("intent_id")
        handle = raw.get("handle")
        if (
            raw.get("state") not in valid_states
            or not isinstance(raw.get("attempt"), int)
            or raw.get("attempt", -1) < 0
            or any(
                raw.get(key) is not None and not isinstance(raw.get(key), str)
                for key in optional_strings
            )
            or not isinstance(raw.get("checkpointed"), bool)
            or not isinstance(raw.get("issues"), list)
            or not all(
                isinstance(item, str) and re.fullmatch(r"PW_EPIC_[A-Z0-9_]{1,64}", item)
                for item in raw.get("issues", [])
            )
            or not isinstance(raw.get("blocked_by"), list)
            or not all(isinstance(item, str) for item in raw.get("blocked_by", []))
            or intent_id is not None
            and (not re.fullmatch(r"[0-9a-f]{64}", intent_id) or intent_id not in used_intents)
            or handle is not None
            and (not _epic_opaque_handle_valid(handle) or handle not in used_handles)
        ):
            raise EpicOrchestrationError(
                "PW_EPIC_RUNTIME_INVALID", f"{unit_id} runtime entry is invalid."
            )
        if schema_version == 2:
            executor = raw.get("executor")
            visibility_class = raw.get("visibility_class")
            retention_policy = raw.get("retention_policy")
            disposition_state = raw.get("disposition_state")
            retirement_state = raw.get("retirement_state")
            attention_reasons = raw.get("attention_reasons")
            prior_handles = raw.get("prior_handles")
            retirement_intent_id = raw.get("retirement_intent_id")
            if (
                executor not in {*DELEGATION_EXECUTOR_SURFACES, "none"}
                or visibility_class not in {"ephemeral", "visible-retirable", "visible-retained"}
                or retention_policy not in {"not-applicable", "retire-on-verified", "retain"}
                or disposition_state not in {"pending", "integrated", "no-integration"}
                or retirement_state
                not in {
                    "not-applicable",
                    "pending",
                    "requested",
                    "confirmed",
                    "failed",
                    "unknown",
                    "retained",
                }
                or not isinstance(attention_reasons, list)
                or not all(
                    isinstance(item, str) and re.fullmatch(r"[a-z][a-z0-9-]{0,63}", item)
                    for item in attention_reasons
                )
                or not isinstance(raw.get("owner_promoted"), bool)
                or not isinstance(prior_handles, list)
                or not all(
                    _epic_opaque_handle_valid(item) and item in used_handles
                    for item in prior_handles
                )
                or retirement_intent_id is not None
                and not re.fullmatch(r"[0-9a-f]{64}", retirement_intent_id)
            ):
                raise EpicOrchestrationError(
                    "PW_EPIC_RUNTIME_INVALID", f"{unit_id} lifecycle entry is invalid."
                )
        else:
            launched = bool(intent_id or handle or raw.get("branch") or raw.get("worktree"))
            executor = "persistent-task" if launched else "coordinator"
            visibility_class = "visible-retained" if launched else "ephemeral"
            retention_policy = "retain" if launched else "not-applicable"
            disposition_state = "pending"
            retirement_state = "retained" if launched else "not-applicable"
            attention_reasons = ["legacy-handle-unavailable"] if launched and handle is None else []
            prior_handles = []
            retirement_intent_id = None
        units[unit_id] = EpicUnitRun(
            state=str(raw["state"]),
            attempt=int(raw["attempt"]),
            intent_id=raw.get("intent_id"),
            handle=raw.get("handle"),
            branch=raw.get("branch"),
            worktree=raw.get("worktree"),
            base_commit=raw.get("base_commit"),
            checkpointed=bool(raw["checkpointed"]),
            issues=tuple(raw["issues"]),
            blocked_by=tuple(raw["blocked_by"]),
            completion_provenance=raw.get("completion_provenance"),
            executor=str(executor),
            visibility_class=str(visibility_class),
            retention_policy=str(retention_policy),
            disposition_state=str(disposition_state),
            disposition_receipt=raw.get("disposition_receipt"),
            attention_reasons=tuple(attention_reasons),
            owner_promoted=bool(raw.get("owner_promoted", False)),
            explicit_retain_reason=raw.get("explicit_retain_reason"),
            retirement_state=str(retirement_state),
            retirement_intent_id=retirement_intent_id,
            retirement_ack=raw.get("retirement_ack"),
            prior_handles=tuple(prior_handles),
        )
    return EpicOrchestrationState(
        schema_version=2,
        target_id=str(payload["target_id"]),
        plan_fingerprint=str(payload["plan_fingerprint"]),
        coordinator_hash=str(payload["coordinator_hash"]),
        coordinator_worktree=str(payload["coordinator_worktree"]),
        base_commit=str(payload["base_commit"]),
        units=units,
        shared_premise_valid=bool(payload["shared_premise_valid"]),
        failure_seen=bool(payload["failure_seen"]),
        create_count=int(payload["create_count"]),
        used_intents=set(used_intents),
        used_handles=set(used_handles),
        verified_paths=verified_paths,
        migrated_from_version=1 if schema_version == 1 else None,
    )


def _epic_execution_fingerprint(
    plan: DelegationPlan, obligations: Mapping[str, EpicChildObligations], base_commit: str
) -> str:
    payload = {
        "target": {
            "id": plan.target.target_id,
            "source": plan.target.source_path,
            "source_hash": plan.target.source_hash,
        },
        "base_commit": base_commit,
        "execution_authority": {
            "requested_concurrency": plan.requested_concurrency,
            "available_child_capacity": plan.available_child_capacity,
            "observed_capabilities": plan.observed_capabilities,
            "capability_source": plan.capability_source,
            "persistent_task_authority": plan.persistent_task_authority,
        },
        "units": [
            {
                "id": unit.unit_id,
                "dependencies": unit.dependencies,
                "authority_acs": unit.authority_acs,
                "execution_needs": unit.execution_needs.properties(),
                "requested_executor": unit.requested_executor,
                "executor": unit.executor,
                "schedule": unit.schedule,
                "visibility_class": unit.visibility_class,
                "retention_policy": unit.retention_policy,
                "obligations": {
                    "parent_acs": obligations[unit.unit_id].parent_acs,
                    "repositories": obligations[unit.unit_id].repositories,
                    "write_scope": obligations[unit.unit_id].write_scope,
                    "validations": obligations[unit.unit_id].validations,
                    "evidence": obligations[unit.unit_id].evidence,
                },
            }
            for unit in plan.units
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _epic_execution_fingerprint_v1(
    plan: DelegationPlan, obligations: Mapping[str, EpicChildObligations], base_commit: str
) -> str:
    """Reproduce the 0.4 runtime identity solely to migrate exact legacy state."""
    payload = {
        "target": {
            "id": plan.target.target_id,
            "source": plan.target.source_path,
            "source_hash": plan.target.source_hash,
        },
        "base_commit": base_commit,
        "execution_authority": {
            "requested_concurrency": plan.requested_concurrency,
            "available_child_capacity": plan.available_child_capacity,
            "observed_capabilities": plan.observed_capabilities,
            "capability_source": plan.capability_source,
            "persistent_task_authority": plan.persistent_task_authority,
        },
        "units": [
            {
                "id": unit.unit_id,
                "dependencies": unit.dependencies,
                "authority_acs": unit.authority_acs,
                "obligations": {
                    "parent_acs": obligations[unit.unit_id].parent_acs,
                    "repositories": obligations[unit.unit_id].repositories,
                    "write_scope": obligations[unit.unit_id].write_scope,
                    "validations": obligations[unit.unit_id].validations,
                    "evidence": obligations[unit.unit_id].evidence,
                },
            }
            for unit in plan.units
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _delegation_error(code: str, message: str) -> DelegationPlanError:
    return DelegationPlanError(code, message)


def _delegation_source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _delegation_relative_path(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _delegation_dependency_ids(value: str, *, unit_id: str) -> tuple[str, ...]:
    normalized = value.strip()
    if not normalized or normalized.lower() in {"none", "n/a", "-"}:
        return ()
    dependencies: list[str] = []
    for item in normalized.split(","):
        dependency = item.strip()
        if not dependency or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", dependency):
            raise _delegation_error(
                "PW_DELEGATION_DEPENDENCY_MALFORMED",
                f"{unit_id} has malformed dependency metadata: '{value}'.",
            )
        if dependency not in dependencies:
            dependencies.append(dependency)
    return tuple(dependencies)


def _delegation_write_scope(value: str, *, unit_id: str) -> tuple[str, ...]:
    if not value.strip():
        raise _delegation_error(
            "PW_DELEGATION_METADATA_MISSING",
            f"{unit_id} must declare at least one repository-relative Write Scope prefix.",
        )
    scopes: list[str] = []
    for item in value.split(","):
        raw_scope = item.strip().replace("\\", "/")
        if not raw_scope or any(character in raw_scope for character in "*?[]{}"):
            raise _delegation_error(
                "PW_DELEGATION_WRITE_SCOPE_INVALID",
                f"{unit_id} has invalid Write Scope '{item.strip()}'; prefixes are not globs.",
            )
        if raw_scope.startswith("/"):
            raise _delegation_error(
                "PW_DELEGATION_WRITE_SCOPE_INVALID",
                f"{unit_id} Write Scope must be repository-relative: '{raw_scope}'.",
            )
        parts = [part for part in raw_scope.split("/") if part not in {"", "."}]
        if ".." in parts:
            raise _delegation_error(
                "PW_DELEGATION_WRITE_SCOPE_INVALID",
                f"{unit_id} Write Scope cannot escape the repository: '{raw_scope}'.",
            )
        scope = "." if not parts else "/".join(parts)
        if scope not in scopes:
            scopes.append(scope)
    return tuple(scopes)


def _delegation_parallel_safe(value: str, *, unit_id: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"yes", "true"}:
        return True
    if normalized in {"no", "false"}:
        return False
    raise _delegation_error(
        "PW_DELEGATION_METADATA_MISSING",
        f"{unit_id} Parallel Safe must be explicitly Yes or No.",
    )


def _delegation_execution_needs(
    value: str, *, unit_id: str, require_earned_surface: bool = False
) -> DelegationExecutionNeeds:
    """Parse optional execution needs without inferring any host capability."""
    normalized = value.strip()
    if not normalized or normalized.lower() in {"none", "n/a", "-"}:
        return DelegationExecutionNeeds(earned_surface_required=require_earned_surface)

    tokens: list[str] = []
    peer_group: str | None = None
    durable_resume = False
    direct_owner_steering = False
    isolated_worktree = False
    execution_benefit: str | None = None
    expected_overhead: str | None = None
    benefit_overhead_basis: str | None = None
    for raw_token in normalized.split(","):
        token = raw_token.strip().lower()
        if not token:
            raise _delegation_error(
                "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                f"{unit_id} has an empty Execution Needs token.",
            )
        if token.startswith("peer:"):
            group = token.removeprefix("peer:").strip()
            if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,63}", group):
                raise _delegation_error(
                    "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                    f"{unit_id} has invalid peer group '{group}'.",
                )
            if peer_group is not None and peer_group != group:
                raise _delegation_error(
                    "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                    f"{unit_id} declares more than one peer communication group.",
                )
            peer_group = group
            canonical = f"peer:{group}"
        elif token.startswith("benefit:"):
            value_text = token.removeprefix("benefit:").strip()
            if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,95}", value_text):
                raise _delegation_error(
                    "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                    f"{unit_id} has invalid execution benefit '{value_text}'.",
                )
            if execution_benefit is not None and execution_benefit != value_text:
                raise _delegation_error(
                    "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                    f"{unit_id} declares more than one execution benefit.",
                )
            execution_benefit = value_text
            canonical = f"benefit:{value_text}"
        elif token.startswith("overhead:"):
            value_text = token.removeprefix("overhead:").strip()
            if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,95}", value_text):
                raise _delegation_error(
                    "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                    f"{unit_id} has invalid expected overhead '{value_text}'.",
                )
            if expected_overhead is not None and expected_overhead != value_text:
                raise _delegation_error(
                    "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                    f"{unit_id} declares more than one expected overhead.",
                )
            expected_overhead = value_text
            canonical = f"overhead:{value_text}"
        elif token.startswith("tradeoff:"):
            value_text = token.removeprefix("tradeoff:").strip()
            if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,95}", value_text):
                raise _delegation_error(
                    "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                    f"{unit_id} has invalid benefit-overhead basis '{value_text}'.",
                )
            if benefit_overhead_basis is not None and benefit_overhead_basis != value_text:
                raise _delegation_error(
                    "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                    f"{unit_id} declares more than one benefit-overhead basis.",
                )
            benefit_overhead_basis = value_text
            canonical = f"tradeoff:{value_text}"
        elif token in DELEGATION_EXECUTION_NEED_TOKENS:
            canonical = token
            durable_resume = durable_resume or token == "durable-resume"
            direct_owner_steering = direct_owner_steering or token == "direct-owner-steering"
            isolated_worktree = isolated_worktree or token == "isolated-worktree"
        else:
            raise _delegation_error(
                "PW_DELEGATION_EXECUTION_NEEDS_INVALID",
                f"{unit_id} has unknown Execution Needs token '{raw_token.strip()}'.",
            )
        if canonical not in tokens:
            tokens.append(canonical)

    if any(token != "bounded-return" for token in tokens):
        tokens = [token for token in tokens if token != "bounded-return"]
    if not tokens:
        tokens = ["bounded-return"]
    return DelegationExecutionNeeds(
        tokens=tuple(tokens),
        durable_resume=durable_resume,
        direct_owner_steering=direct_owner_steering,
        isolated_worktree=isolated_worktree,
        peer_group=peer_group,
        execution_benefit=execution_benefit,
        expected_overhead=expected_overhead,
        benefit_overhead_basis=benefit_overhead_basis,
        earned_surface_required=require_earned_surface,
    )


def _delegation_explicit_authority(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.strip().lower()
    return bool(normalized) and normalized not in {
        "unknown",
        "not observed",
        "not authorized",
        "unsupported",
        "none",
        "false",
    }


def _delegation_canonical_state(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"done", "complete"}:
        return "complete"
    if normalized in {"blocked", "failed"}:
        return "blocked"
    return "pending"


def _delegation_task_units(root: Path, implementation_path: Path) -> tuple[DelegationUnit, ...]:
    text = implementation_path.read_text(encoding="utf-8")
    table_found, rows, malformed_rows = _implementation_task_table_rows(text)
    if not table_found:
        raise _delegation_error(
            "PW_DELEGATION_PLAN_MISSING",
            "Task IMPLEMENTATION.md has no supported Task List table.",
        )
    if malformed_rows:
        raise _delegation_error(
            "PW_DELEGATION_PLAN_MALFORMED",
            "Task List has malformed rows at lines: "
            + ", ".join(str(line) for line in malformed_rows)
            + ".",
        )
    if not rows:
        raise _delegation_error("PW_DELEGATION_PLAN_EMPTY", "Task List has no execution units.")
    if any(row.get("_delegation_metadata") != "present" for row in rows):
        raise _delegation_error(
            "PW_DELEGATION_METADATA_MISSING",
            "Delegate requires Task List columns Dependencies, Write Scope, and Parallel Safe; "
            "the legacy six-column plan remains valid for non-Delegate commands.",
        )
    source_path = _delegation_relative_path(root, implementation_path)
    repository_scope = _delegation_repository_scope(implementation_path)
    units: list[DelegationUnit] = []
    for order, row in enumerate(rows):
        unit_id = row.get("ID", "").strip()
        if not unit_id:
            raise _delegation_error(
                "PW_DELEGATION_UNIT_ID_MISSING", "Every Task List row requires a stable ID."
            )
        units.append(
            DelegationUnit(
                unit_id=unit_id,
                title=row.get("Title", "").strip(),
                dependencies=_delegation_dependency_ids(
                    row.get("Dependencies", ""), unit_id=unit_id
                ),
                write_scope=_delegation_write_scope(row.get("Write Scope", ""), unit_id=unit_id),
                parallel_safe=_delegation_parallel_safe(
                    row.get("Parallel Safe", ""), unit_id=unit_id
                ),
                canonical_state=_delegation_canonical_state(row.get("Status", "")),
                source_order=order,
                source_path=source_path,
                authority_acs=tuple(
                    sorted(
                        _extract_ac_ids(row.get("Acceptance Criteria", "")),
                        key=lambda ac_id: int(ac_id[2:]),
                    )
                ),
                execution_needs=_delegation_execution_needs(
                    row.get("Execution Needs", ""),
                    unit_id=unit_id,
                    require_earned_surface=(row.get("_execution_needs_metadata") == "present"),
                ),
                repository_scope=repository_scope,
            )
        )
    return tuple(units)


def _delegation_epic_units(
    root: Path, epic_dir: Path, plan_path: Path
) -> tuple[DelegationUnit, ...]:
    text = plan_path.read_text(encoding="utf-8")
    rows = _markdown_table_rows_from_section(
        text,
        "Authorized Child Rows",
        expected_columns=DELEGATION_EXECUTION_NEEDS_DECOMPOSITION_PLAN_COLUMNS,
    )
    earned_surface_required = bool(rows)
    if not rows:
        rows = _markdown_table_rows_from_section(
            text,
            "Authorized Child Rows",
            expected_columns=DELEGATION_DECOMPOSITION_PLAN_COLUMNS,
        )
        earned_surface_required = False
    if not rows:
        legacy_rows = _markdown_table_rows_from_section(
            text,
            "Authorized Child Rows",
            expected_columns=DECOMPOSITION_PLAN_COLUMNS,
        )
        if legacy_rows:
            raise _delegation_error(
                "PW_DELEGATION_METADATA_MISSING",
                "Delegate requires the Epic decomposition Dependencies column; the legacy "
                "four-column plan remains valid for non-Delegate commands.",
            )
        raise _delegation_error(
            "PW_DELEGATION_PLAN_MALFORMED",
            "Epic DECOMPOSITION.md has no supported Authorized Child Rows table.",
        )
    tracker_path = epic_dir / "TRACKER.md"
    if not tracker_path.exists():
        raise _delegation_error("PW_DELEGATION_AUTHORITY_MISSING", "Epic TRACKER.md is missing.")
    _lines, _header_idx, tracker_rows = _epic_tracker_rows(tracker_path)
    tracker_by_id = {row.get("ID", "").strip(): row for row in tracker_rows}
    source_path = _delegation_relative_path(root, plan_path)
    units: list[DelegationUnit] = []
    for order, row in enumerate(rows):
        unit_id = row.get("ID", "").strip()
        tracker_row = tracker_by_id.get(unit_id)
        if tracker_row is None:
            raise _delegation_error(
                "PW_DELEGATION_UNPLANNED_UNIT",
                f"Authorized child {unit_id} is missing from the Epic tracker.",
            )
        authority_issues = _decomposition_plan_authority_issues(epic_dir=epic_dir, row=tracker_row)
        if authority_issues:
            raise _delegation_error(
                "PW_DELEGATION_AUTHORITY_MISMATCH",
                f"{unit_id} does not match decomposition authority: " + "; ".join(authority_issues),
            )
        child_write_scope: tuple[str, ...] = ()
        child_repository_scope: tuple[str, ...] = (".",)
        docs_rel = _clean_markdown_cell_path(tracker_row.get("Docs", ""))
        if docs_rel:
            child_implementation = root / ".project-workflow" / docs_rel
            if child_implementation.exists():
                child_repository_scope = _delegation_repository_scope(child_implementation)
                _found, child_rows, child_malformed = _implementation_task_table_rows(
                    child_implementation.read_text(encoding="utf-8")
                )
                if (
                    not child_malformed
                    and child_rows
                    and all(child.get("_delegation_metadata") == "present" for child in child_rows)
                ):
                    child_write_scope = tuple(
                        dict.fromkeys(
                            scope
                            for child in child_rows
                            for scope in _delegation_write_scope(
                                child.get("Write Scope", ""),
                                unit_id=f"{unit_id}/{child.get('ID', '').strip() or '?'}",
                            )
                        )
                    )
        units.append(
            DelegationUnit(
                unit_id=unit_id,
                title=row.get("Title", "").strip(),
                dependencies=_delegation_dependency_ids(
                    row.get("Dependencies", ""), unit_id=unit_id
                ),
                write_scope=child_write_scope,
                parallel_safe=True,
                canonical_state=_delegation_canonical_state(tracker_row.get("Status", "")),
                source_order=order,
                source_path=source_path,
                authority_acs=tuple(
                    sorted(
                        _extract_ac_ids(row.get("Parent ACs", "")),
                        key=lambda ac_id: int(ac_id[2:]),
                    )
                ),
                execution_needs=_delegation_execution_needs(
                    row.get("Execution Needs", ""),
                    unit_id=unit_id,
                    require_earned_surface=earned_surface_required,
                ),
                repository_scope=child_repository_scope,
            )
        )
    return tuple(units)


def _delegation_scope_overlap(left: str, right: str) -> bool:
    if left == "." or right == ".":
        return True
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def _delegation_repository_scope(implementation_path: Path) -> tuple[str, ...]:
    requirements_path = implementation_path.parent / "REQUIREMENTS.md"
    if not requirements_path.exists():
        return (".",)
    primary, touched = _repository_scope_values(requirements_path.read_text(encoding="utf-8"))
    values = touched or ((primary,) if primary else ())
    normalized = tuple(dict.fromkeys(value for value in values if value))
    return normalized or (".",)


def _delegation_has_path(dependencies: dict[str, tuple[str, ...]], start: str, target: str) -> bool:
    pending = list(dependencies.get(start, ()))
    seen: set[str] = set()
    while pending:
        current = pending.pop()
        if current == target:
            return True
        if current in seen:
            continue
        seen.add(current)
        pending.extend(dependencies.get(current, ()))
    return False


def _delegation_capability_matrix(
    *,
    observed_capabilities: tuple[str, ...],
    unsupported_capabilities: tuple[str, ...],
    capability_source: str,
) -> tuple[DelegationCapabilityObservation, ...]:
    """Resolve verified/unsupported/unknown host capability truth without inference."""
    verified = set(observed_capabilities)
    unsupported = set(unsupported_capabilities)
    unknown_names = sorted((verified | unsupported) - set(DELEGATION_CAPABILITIES))
    if unknown_names:
        raise _delegation_error(
            "PW_DELEGATION_CAPABILITY_UNKNOWN",
            "Unknown capability: " + ", ".join(unknown_names) + ".",
        )
    conflicts = sorted(verified & unsupported)
    if conflicts:
        raise _delegation_error(
            "PW_DELEGATION_CAPABILITY_CONFLICT",
            "Capabilities cannot be both verified and unsupported: " + ", ".join(conflicts) + ".",
        )
    source = capability_source.strip()
    if (verified or unsupported) and source.lower() in {"", "not observed", "unknown"}:
        raise _delegation_error(
            "PW_DELEGATION_CAPABILITY_UNOBSERVED",
            "Verified or unsupported capabilities require current host observation provenance.",
        )
    if verified or unsupported:
        observed_date_match = re.search(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)", source)
        try:
            observed_date = (
                date.fromisoformat(observed_date_match.group(1))
                if observed_date_match is not None
                else None
            )
        except ValueError:
            observed_date = None
        if observed_date is None:
            raise _delegation_error(
                "PW_DELEGATION_CAPABILITY_PROVENANCE_UNDATED",
                "Verified or unsupported capabilities require provenance containing a valid "
                "ISO observation date (YYYY-MM-DD).",
            )
    observations: list[DelegationCapabilityObservation] = []
    for capability in DELEGATION_CAPABILITIES:
        if capability in verified:
            state = "verified"
            provenance = f"runtime-observed:{source}"
        elif capability in unsupported:
            state = "unsupported"
            provenance = f"runtime-observed:{source}"
        else:
            state = "unknown"
            provenance = "not observed"
        observations.append(
            DelegationCapabilityObservation(
                capability=capability,
                state=state,
                provenance=provenance,
            )
        )
    return tuple(observations)


@dataclass(frozen=True)
class DelegationExecutorDecision:
    requested_executor: str
    executor: str
    schedule: str
    visibility_class: str
    retention_policy: str
    required_child_slots: int
    reason: str
    blocking_reasons: tuple[str, ...] = ()


def _delegation_capability_issue(
    capability: str,
    observations: Mapping[str, DelegationCapabilityObservation],
) -> str:
    observation = observations[capability]
    return f"{capability} capability is {observation.state} ({observation.provenance})"


def _delegation_select_executor(
    *,
    unit: DelegationUnit,
    capability_matrix: tuple[DelegationCapabilityObservation, ...],
    available_child_capacity: int,
    requested_concurrency: int,
    persistent_task_authority: str | None,
) -> DelegationExecutorDecision:
    """Select one surface from work properties; target kind is deliberately absent."""
    observations = {item.capability: item for item in capability_matrix}

    def verified(capability: str) -> bool:
        return observations[capability].state == "verified"

    def result(
        executor: str,
        reason: str,
        *,
        requested_executor: str | None = None,
        blocking_reasons: tuple[str, ...] = (),
    ) -> DelegationExecutorDecision:
        required_child_slots = (
            2
            if executor == "peer-team"
            else (1 if executor in {"subagent", "persistent-task"} else 0)
        )
        schedule = (
            "parallel"
            if required_child_slots
            and unit.parallel_safe
            and requested_concurrency >= required_child_slots
            and available_child_capacity >= required_child_slots
            else "sequential"
        )
        if executor == "persistent-task":
            retirement_verified = verified("task-retirement") and verified(
                "task-retirement-reconciliation"
            )
            owner_retained = unit.execution_needs.direct_owner_steering
            visibility_class = (
                "visible-retained"
                if owner_retained
                else ("visible-retirable" if retirement_verified else "visible-retained")
            )
            retention_policy = (
                "retain"
                if owner_retained
                else ("retire-on-verified" if retirement_verified else "retain")
            )
        else:
            visibility_class = "ephemeral"
            retention_policy = "not-applicable"
        return DelegationExecutorDecision(
            requested_executor=requested_executor or unit.execution_needs.requested_executor,
            executor=executor,
            schedule=schedule,
            visibility_class=visibility_class,
            retention_policy=retention_policy,
            required_child_slots=required_child_slots,
            reason=reason,
            blocking_reasons=blocking_reasons,
        )

    needs = unit.execution_needs
    coordinator_owned = any(_task_worker_scope_forbidden(scope) for scope in unit.write_scope)
    binding_needs = (
        needs.durable_resume
        or needs.direct_owner_steering
        or needs.isolated_worktree
        or needs.peer_group is not None
    )
    earned_surface = all(
        (
            needs.execution_benefit,
            needs.expected_overhead,
            needs.benefit_overhead_basis,
        )
    )
    if coordinator_owned:
        if binding_needs:
            issue = (
                "Coordinator-owned workflow scope conflicts with binding execution needs: "
                + ", ".join(needs.tokens)
                + "."
            )
            return result("none", issue, blocking_reasons=(issue,))
        return result(
            "coordinator",
            "Coordinator-owned workflow scope requires the single shared-state writer.",
            requested_executor="coordinator",
        )

    if needs.earned_surface_required and not earned_surface:
        missing = [
            label
            for label, value in (
                ("benefit", needs.execution_benefit),
                ("overhead", needs.expected_overhead),
                ("tradeoff", needs.benefit_overhead_basis),
            )
            if value is None
        ]
        reason = (
            "Non-Coordinator execution has no complete earned-surface basis; missing "
            + ", ".join(missing)
            + "."
        )
        if binding_needs:
            return result("none", reason, blocking_reasons=(reason,))
        return result(
            "coordinator",
            reason + " Coordinator sequential execution is sufficient.",
            requested_executor="coordinator",
        )

    if needs.peer_group is not None:
        composite = tuple(
            token
            for token, enabled in (
                ("durable-resume", needs.durable_resume),
                ("direct-owner-steering", needs.direct_owner_steering),
            )
            if enabled
        )
        if composite:
            reason = (
                "Binding peer communication cannot satisfy additional persistent need(s): "
                + ", ".join(composite)
                + "."
            )
            return result("none", reason, blocking_reasons=(reason,))
        required = ["peer-team", "peer-messaging"]
        if needs.isolated_worktree:
            required.append("peer-team-isolated-worktree")
        issues = tuple(
            _delegation_capability_issue(capability, observations)
            for capability in required
            if not verified(capability)
        )
        if available_child_capacity < 2:
            issues += (
                "peer-team requires at least 2 available child slots; "
                f"observed {available_child_capacity}",
            )
        if requested_concurrency < 2:
            issues += (
                "peer-team requires requested concurrency of at least 2; "
                f"requested {requested_concurrency}",
            )
        if issues:
            reason = "Binding peer communication requirement is unmet: " + "; ".join(issues) + "."
            return result("none", reason, blocking_reasons=(reason,))
        return result(
            "peer-team",
            f"Selected verified peer-team surface for peer group {needs.peer_group}.",
        )

    persistent_required = needs.durable_resume or needs.direct_owner_steering
    persistent_capabilities: list[str] = [
        "persistent-task",
        "task-monitoring",
        "task-reconciliation",
    ]
    if needs.isolated_worktree:
        persistent_isolation_verified = verified("persistent-task-isolated-worktree") or verified(
            "isolated-worktree"
        )
    else:
        persistent_isolation_verified = True
    if needs.direct_owner_steering:
        persistent_capabilities.append("persistent-task-owner-steering")

    if needs.isolated_worktree and not persistent_required:
        subagent_isolated = verified("subagent") and verified("subagent-isolated-worktree")
        if subagent_isolated and available_child_capacity > 0:
            return result(
                "subagent",
                "Selected the lightest verified isolated subagent surface.",
            )
        persistent_required = True

    if persistent_required:
        persistent_issues = [
            _delegation_capability_issue(capability, observations)
            for capability in persistent_capabilities
            if not verified(capability)
        ]
        if needs.isolated_worktree and not persistent_isolation_verified:
            persistent_issues.append(
                _delegation_capability_issue("persistent-task-isolated-worktree", observations)
                + "; legacy isolated-worktree capability is also not verified"
            )
        if not _delegation_explicit_authority(persistent_task_authority):
            persistent_issues.append("explicit current-request persistent-task authority is absent")
        if available_child_capacity < 1:
            persistent_issues.append("persistent-task child capacity is exhausted")
        if persistent_issues:
            reason = (
                "Binding persistent execution requirement is unmet: "
                + "; ".join(persistent_issues)
                + "."
            )
            return result("none", reason, blocking_reasons=(reason,))
        return result(
            "persistent-task",
            "Selected verified persistent-task surface for " + ", ".join(needs.tokens) + ".",
        )

    if verified("subagent") and available_child_capacity > 0:
        return result(
            "subagent",
            "Selected the lightest verified bounded-return subagent surface.",
        )
    fallback_issues: list[str] = []
    if not verified("subagent"):
        fallback_issues.append(_delegation_capability_issue("subagent", observations))
    if available_child_capacity < 1:
        fallback_issues.append("subagent child capacity is exhausted")
    return result(
        "coordinator",
        "; ".join(fallback_issues) + "; coordinator sequential fallback satisfies bounded-return.",
    )


def build_delegation_plan(
    *,
    target: DelegationTarget,
    units: tuple[DelegationUnit, ...],
    selected_unit_ids: tuple[str, ...] = (),
    requested_concurrency: int = 1,
    available_child_capacity: int = 0,
    observed_capabilities: tuple[str, ...] = (),
    unsupported_capabilities: tuple[str, ...] = (),
    capability_source: str = "not observed",
    persistent_task_authority: str | None = None,
) -> DelegationPlan:
    """Build and validate a deterministic host-neutral delegation plan without I/O."""
    if requested_concurrency < 1:
        raise _delegation_error(
            "PW_DELEGATION_CONCURRENCY_INVALID", "Requested concurrency must be at least 1."
        )
    if available_child_capacity < 0:
        raise _delegation_error(
            "PW_DELEGATION_CAPACITY_INVALID", "Available child capacity cannot be negative."
        )
    capability_matrix = _delegation_capability_matrix(
        observed_capabilities=observed_capabilities,
        unsupported_capabilities=unsupported_capabilities,
        capability_source=capability_source,
    )
    capabilities = tuple(item.capability for item in capability_matrix if item.state == "verified")

    by_id: dict[str, DelegationUnit] = {}
    for unit in units:
        if unit.unit_id in by_id:
            raise _delegation_error(
                "PW_DELEGATION_UNIT_DUPLICATE", f"Duplicate execution unit ID: {unit.unit_id}."
            )
        by_id[unit.unit_id] = unit
    if not by_id:
        raise _delegation_error("PW_DELEGATION_PLAN_EMPTY", "Delegation plan has no units.")

    dependencies = {unit.unit_id: unit.dependencies for unit in units}
    for unit in units:
        for dependency in unit.dependencies:
            if dependency == unit.unit_id:
                raise _delegation_error(
                    "PW_DELEGATION_DEPENDENCY_SELF",
                    f"{unit.unit_id} cannot depend on itself.",
                )
            if dependency not in by_id:
                raise _delegation_error(
                    "PW_DELEGATION_DEPENDENCY_MISSING",
                    f"{unit.unit_id} depends on missing unit {dependency}.",
                )

    ordered_source_ids = [
        unit.unit_id for unit in sorted(units, key=lambda item: item.source_order)
    ]
    indegree = {unit_id: len(dependencies[unit_id]) for unit_id in ordered_source_ids}
    dependents: dict[str, list[str]] = {unit_id: [] for unit_id in ordered_source_ids}
    for unit_id, dependency_ids in dependencies.items():
        for dependency_id in dependency_ids:
            dependents[dependency_id].append(unit_id)
    ready = [unit_id for unit_id in ordered_source_ids if indegree[unit_id] == 0]
    topological: list[str] = []
    while ready:
        unit_id = ready.pop(0)
        topological.append(unit_id)
        for dependent in sorted(dependents[unit_id], key=lambda item: by_id[item].source_order):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
                ready.sort(key=lambda item: by_id[item].source_order)
    if len(topological) != len(units):
        cycle_units = [unit_id for unit_id in ordered_source_ids if unit_id not in topological]
        raise _delegation_error(
            "PW_DELEGATION_DEPENDENCY_CYCLE",
            "Dependency cycle detected: " + ", ".join(cycle_units) + ".",
        )

    if selected_unit_ids:
        selected_set = set(selected_unit_ids)
        unknown_selected = sorted(selected_set - set(by_id))
        if unknown_selected:
            raise _delegation_error(
                "PW_DELEGATION_UNIT_UNKNOWN",
                "Selected unit is not in the approved plan: " + ", ".join(unknown_selected) + ".",
            )
    else:
        selected_set = set(by_id)
    for unit_id in topological:
        if unit_id not in selected_set:
            continue
        for dependency in dependencies[unit_id]:
            if dependency not in selected_set and by_id[dependency].canonical_state != "complete":
                raise _delegation_error(
                    "PW_DELEGATION_SUBSET_DEPENDENCY_OMITTED",
                    f"Selected unit {unit_id} omits unfinished dependency {dependency}.",
                )

    selected_order = tuple(unit_id for unit_id in topological if unit_id in selected_set)
    selected_parallel = [
        by_id[unit_id]
        for unit_id in selected_order
        if by_id[unit_id].parallel_safe and by_id[unit_id].canonical_state != "complete"
    ]
    for index, left in enumerate(selected_parallel):
        for right in selected_parallel[index + 1 :]:
            if _delegation_has_path(
                dependencies, left.unit_id, right.unit_id
            ) or _delegation_has_path(dependencies, right.unit_id, left.unit_id):
                continue
            if not set(left.repository_scope).intersection(right.repository_scope):
                continue
            overlaps = sorted(
                {
                    f"{left_scope} <> {right_scope}"
                    for left_scope in left.write_scope
                    for right_scope in right.write_scope
                    if _delegation_scope_overlap(left_scope, right_scope)
                }
            )
            if overlaps:
                raise _delegation_error(
                    "PW_DELEGATION_WRITE_SCOPE_COLLISION",
                    f"Parallel-safe units {left.unit_id} and {right.unit_id} have overlapping "
                    "Write Scope prefixes: " + ", ".join(overlaps) + ".",
                )

    completed = {unit_id for unit_id, unit in by_id.items() if unit.canonical_state == "complete"}
    planned_units: list[DelegationPlannedUnit] = []
    eligible: list[str] = []
    blocked: list[str] = []
    for unit_id in selected_order:
        unit = by_id[unit_id]
        reasons: list[str] = []
        decision = _delegation_select_executor(
            unit=unit,
            capability_matrix=capability_matrix,
            available_child_capacity=available_child_capacity,
            requested_concurrency=requested_concurrency,
            persistent_task_authority=persistent_task_authority,
        )
        if unit.canonical_state == "complete":
            readiness = "complete"
            executor = decision.executor
            executor_reason = (
                "Canonical workflow state is complete; no launch is eligible. " + decision.reason
            )
            schedule = decision.schedule
            visibility_class = decision.visibility_class
            retention_policy = decision.retention_policy
        elif unit.canonical_state == "blocked":
            readiness = "blocked"
            reasons.append("Canonical workflow state is blocked.")
            executor = decision.executor
            executor_reason = "Blocked units are not executable. " + decision.reason
            schedule = decision.schedule
            visibility_class = decision.visibility_class
            retention_policy = decision.retention_policy
            blocked.append(unit_id)
        else:
            incomplete_dependencies = [
                dependency for dependency in unit.dependencies if dependency not in completed
            ]
            if incomplete_dependencies:
                readiness = "blocked"
                reasons.append(
                    "Waiting for dependencies: " + ", ".join(incomplete_dependencies) + "."
                )
                blocked.append(unit_id)
            elif decision.blocking_reasons:
                readiness = "blocked"
                reasons.extend(decision.blocking_reasons)
                blocked.append(unit_id)
            else:
                readiness = "eligible"
                eligible.append(unit_id)
            executor = decision.executor
            executor_reason = decision.reason
            schedule = decision.schedule
            visibility_class = decision.visibility_class
            retention_policy = decision.retention_policy
        planned_units.append(
            DelegationPlannedUnit(
                unit_id=unit.unit_id,
                title=unit.title,
                dependencies=unit.dependencies,
                write_scope=unit.write_scope,
                parallel_safe=unit.parallel_safe,
                canonical_state=unit.canonical_state,
                readiness=readiness,
                blocking_reasons=tuple(reasons),
                execution_needs=unit.execution_needs,
                repository_scope=unit.repository_scope,
                requested_executor=decision.requested_executor,
                executor=executor,
                schedule=schedule,
                visibility_class=visibility_class,
                retention_policy=retention_policy,
                required_child_slots=decision.required_child_slots,
                executor_reason=executor_reason,
                source_path=unit.source_path,
                authority_acs=unit.authority_acs,
            )
        )

    eligible_workers = [
        unit
        for unit in planned_units
        if unit.readiness == "eligible"
        and unit.executor in {"subagent", "persistent-task", "peer-team"}
    ]
    child_slot_budget = min(requested_concurrency, available_child_capacity)
    effective_child_concurrency = 0
    effective_child_slots = 0
    for eligible_worker in eligible_workers:
        if effective_child_slots + eligible_worker.required_child_slots > child_slot_budget:
            continue
        effective_child_concurrency += 1
        effective_child_slots += eligible_worker.required_child_slots
    if not eligible:
        effective_concurrency = 0
        concurrency_reason = "No units are currently eligible."
    elif effective_child_concurrency:
        effective_concurrency = effective_child_concurrency
        if effective_concurrency < requested_concurrency:
            concurrency_reason = (
                f"Reduced from requested {requested_concurrency} to {effective_concurrency}: "
                f"available child capacity is {available_child_capacity} and "
                f"{len(eligible_workers)} child-executable unit(s) require "
                f"{effective_child_slots} effective child slot(s)."
            )
        else:
            concurrency_reason = "Requested concurrency is supported by observed child capacity."
    else:
        effective_concurrency = 1
        if available_child_capacity == 0:
            concurrency_reason = (
                "Available child capacity is 0 (coordinator excluded); using coordinator "
                "sequential fallback."
            )
        elif not capabilities:
            concurrency_reason = (
                "No host executor capability was observed; using coordinator sequential fallback."
            )
        else:
            concurrency_reason = "Plan safety requires sequential execution."

    provenance = (
        f"target:{target.source_path}#{target.source_hash}",
        *(f"unit:{unit.source_path}" for unit in planned_units),
        f"capability:{capability_source}",
        *(
            (f"persistent-task-authority:{persistent_task_authority}",)
            if persistent_task_authority
            else ()
        ),
    )
    return DelegationPlan(
        target=target,
        units=tuple(planned_units),
        selected_units=selected_order,
        eligible_units=tuple(eligible),
        blocked_units=tuple(blocked),
        requested_concurrency=requested_concurrency,
        available_child_capacity=available_child_capacity,
        effective_concurrency=effective_concurrency,
        effective_child_concurrency=effective_child_concurrency,
        effective_child_slots=effective_child_slots,
        concurrency_reason=concurrency_reason,
        observed_capabilities=capabilities,
        capability_matrix=capability_matrix,
        capability_source=capability_source,
        persistent_task_authority=persistent_task_authority,
        provenance=tuple(dict.fromkeys(provenance)),
    )


def _delegation_approved_lifecycle(kind: str, lifecycle: str) -> bool:
    rejected = {"", "To Do", "Analysing", "Proposed", "N/A"}
    return lifecycle not in rejected and (kind in {"task", "epic-child", "epic"})


def _resolve_delegation_target(
    root: Path, target_ids: tuple[str, ...]
) -> tuple[DelegationTarget, tuple[DelegationUnit, ...]]:
    requested = tuple(target_id.strip() for target_id in target_ids if target_id.strip())
    if len(requested) != 1:
        raise _delegation_error(
            "PW_DELEGATION_TARGET_COUNT",
            "Delegate requires exactly one existing Epic or Task target; mixed or batched "
            "targets are not allowed.",
        )
    target_id = requested[0]
    workflow_dir = root / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    tasks_dir = workflow_dir / "tasks"
    if not tracker_path.exists():
        raise _delegation_error(
            "PW_DELEGATION_AUTHORITY_MISSING", f"Missing global tracker: {tracker_path}."
        )

    _lines, _header_idx, global_rows = _global_tracker_rows(tracker_path)
    matches: list[tuple[str, dict[str, str], Path | None]] = []
    for row in global_rows:
        if row.get("ID", "").strip() == target_id:
            kind = "epic" if target_id.startswith(f"{EPIC_ID_PREFIX}-") else "task"
            matches.append((kind, row, None))
    if tasks_dir.exists():
        for epic_tracker_path in sorted(tasks_dir.glob("EPIC-*/TRACKER.md")):
            try:
                _epic_lines, _epic_header, epic_rows = _epic_tracker_rows(epic_tracker_path)
            except SystemExit:
                continue
            for row in epic_rows:
                if row.get("ID", "").strip() == target_id:
                    matches.append(("epic-child", row, epic_tracker_path.parent))
    if not matches:
        raise _delegation_error(
            "PW_DELEGATION_TARGET_UNKNOWN",
            f"No existing Epic or Task target found for '{target_id}'.",
        )
    if len(matches) != 1:
        locations = ", ".join(
            _delegation_relative_path(root, epic_dir or tracker_path)
            for _kind, _row, epic_dir in matches
        )
        raise _delegation_error(
            "PW_DELEGATION_TARGET_AMBIGUOUS",
            f"Target '{target_id}' resolves to multiple workflow units: {locations}.",
        )

    kind, row, owner_epic_dir = matches[0]
    lifecycle = row.get("Status", "").strip()
    if not _delegation_approved_lifecycle(kind, lifecycle):
        raise _delegation_error(
            "PW_DELEGATION_TARGET_UNAPPROVED",
            f"{target_id} lifecycle '{lifecycle}' is outside approved delegation authority.",
        )
    if kind == "epic":
        epic_dir = _resolve_epic_dir(tasks_dir, target_id)
        source_path = epic_dir / DECOMPOSITION_PLAN_FILENAME
        if not source_path.exists():
            raise _delegation_error(
                "PW_DELEGATION_PLAN_MISSING", f"Missing delegation plan: {source_path}."
            )
        units = _delegation_epic_units(root, epic_dir, source_path)
    else:
        docs_rel = _clean_markdown_cell_path(row.get("Docs", ""))
        if not docs_rel:
            raise _delegation_error(
                "PW_DELEGATION_PLAN_MISSING", f"{target_id} has no implementation docs path."
            )
        source_path = workflow_dir / docs_rel
        if not source_path.exists():
            raise _delegation_error(
                "PW_DELEGATION_PLAN_MISSING", f"Missing implementation plan: {source_path}."
            )
        if kind == "epic-child" and owner_epic_dir is not None:
            authority_issues = _decomposition_plan_authority_issues(
                epic_dir=owner_epic_dir, row=row
            )
            if authority_issues:
                raise _delegation_error(
                    "PW_DELEGATION_AUTHORITY_MISMATCH",
                    f"{target_id} is outside its parent decomposition authority: "
                    + "; ".join(authority_issues),
                )
        units = _delegation_task_units(root, source_path)
    target = DelegationTarget(
        target_id=target_id,
        kind="task" if kind == "epic-child" else kind,
        title=row.get("Title", "").strip(),
        lifecycle=lifecycle,
        source_path=_delegation_relative_path(root, source_path),
        source_hash=_delegation_source_hash(source_path),
    )
    return target, units


def _delegation_plan_from_args(root: Path, args: argparse.Namespace) -> DelegationPlan:
    target, units = _resolve_delegation_target(root, tuple(args.id))
    return build_delegation_plan(
        target=target,
        units=units,
        selected_unit_ids=tuple(args.unit or ()),
        requested_concurrency=args.requested_concurrency,
        available_child_capacity=args.available_child_capacity,
        observed_capabilities=tuple(args.observed_capability or ()),
        unsupported_capabilities=tuple(args.unsupported_capability or ()),
        capability_source=args.capability_source,
        persistent_task_authority=args.persistent_task_authority,
    )


def delegation_plan_payload(plan: DelegationPlan) -> dict[str, object]:
    return {
        "schema_version": DELEGATION_SCHEMA_VERSION,
        "target": {
            "id": plan.target.target_id,
            "kind": plan.target.kind,
            "title": plan.target.title,
            "lifecycle": plan.target.lifecycle,
            "source": plan.target.source_path,
            "source_hash": plan.target.source_hash,
        },
        "units": [
            {
                "id": unit.unit_id,
                "title": unit.title,
                "dependencies": list(unit.dependencies),
                "write_scope": list(unit.write_scope),
                "parallel_safe": unit.parallel_safe,
                "canonical_state": unit.canonical_state,
                "readiness": unit.readiness,
                "blocking_reasons": list(unit.blocking_reasons),
                "required_properties": {
                    **unit.execution_needs.properties(),
                    "parallel_safe": unit.parallel_safe,
                    "write_scope": list(unit.write_scope),
                    "repository_scope": list(unit.repository_scope),
                },
                "requested_executor": unit.requested_executor,
                "effective_executor": unit.executor,
                "executor": unit.executor,
                "schedule": unit.schedule,
                "visibility_class": unit.visibility_class,
                "retention_policy": unit.retention_policy,
                "required_child_slots": unit.required_child_slots,
                "executor_reason": unit.executor_reason,
                "source": unit.source_path,
                "authority_acs": list(unit.authority_acs),
            }
            for unit in plan.units
        ],
        "selected_units": list(plan.selected_units),
        "eligible_units": list(plan.eligible_units),
        "blocked_units": list(plan.blocked_units),
        "concurrency": {
            "requested": plan.requested_concurrency,
            "available_child_capacity": plan.available_child_capacity,
            "effective": plan.effective_concurrency,
            "effective_child": plan.effective_child_concurrency,
            "effective_child_slots": plan.effective_child_slots,
            "reason": plan.concurrency_reason,
        },
        "capabilities": {
            "observed": list(plan.observed_capabilities),
            "matrix": [
                {
                    "capability": item.capability,
                    "state": item.state,
                    "provenance": item.provenance,
                }
                for item in plan.capability_matrix
            ],
            "source": plan.capability_source,
            "persistent_task_authority": plan.persistent_task_authority,
        },
        "provenance": list(plan.provenance),
    }


def _delegation_plan_fingerprint(plan: DelegationPlan) -> str:
    canonical = json.dumps(
        delegation_plan_payload(plan), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _format_delegation_plan_human(plan: DelegationPlan, *, heading: str = "Delegation Plan") -> str:
    lines = [
        heading,
        f"Target: {plan.target.target_id} ({plan.target.kind}, {plan.target.lifecycle})",
        f"Source: {plan.target.source_path}#{plan.target.source_hash}",
        "Units:",
    ]
    for unit in plan.units:
        dependencies = ", ".join(unit.dependencies) or "none"
        reasons = " ".join(unit.blocking_reasons)
        suffix = f" — {reasons}" if reasons else ""
        lines.append(
            f"- {unit.unit_id}: {unit.readiness}; dependencies={dependencies}; "
            f"needs={','.join(unit.execution_needs.tokens)}; "
            f"parallel-safe={'yes' if unit.parallel_safe else 'no'}; "
            f"write-scope={','.join(unit.write_scope) or 'none'}; "
            f"repositories={','.join(unit.repository_scope)}; "
            f"requested={unit.requested_executor}; effective={unit.executor}; "
            f"schedule={unit.schedule}; visibility={unit.visibility_class}; "
            f"retention={unit.retention_policy}; child-slots={unit.required_child_slots}{suffix}"
        )
        lines.append(f"  Reason: {unit.executor_reason}")
    lines.extend(
        [
            "Eligible: " + (", ".join(plan.eligible_units) or "none"),
            "Blocked: " + (", ".join(plan.blocked_units) or "none"),
            (
                f"Concurrency: requested={plan.requested_concurrency}, "
                f"available-child={plan.available_child_capacity}, "
                f"effective={plan.effective_concurrency}, "
                f"effective-child={plan.effective_child_concurrency}, "
                f"effective-child-slots={plan.effective_child_slots}"
            ),
            f"Concurrency reason: {plan.concurrency_reason}",
            "Capability source: " + plan.capability_source,
            "Capability matrix: "
            + ", ".join(
                f"{item.capability}={item.state} ({item.provenance})"
                for item in plan.capability_matrix
            ),
            "Persistent task authority: " + (plan.persistent_task_authority or "not authorized"),
        ]
    )
    return "\n".join(lines)


def _delegation_runtime_path(root: Path, target_id: str) -> Path:
    current = root
    for part in DELEGATION_RUNTIME_RELATIVE_DIR.parts:
        current /= part
        if current.is_symlink() or (current.exists() and not current.is_dir()):
            raise _delegation_error(
                "PW_DELEGATION_RUNTIME_UNSAFE_PATH",
                f"Delegation runtime boundary must use real directories: {current}.",
            )
    try:
        current.resolve(strict=False).relative_to(root.resolve())
    except ValueError as error:
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_UNSAFE_PATH",
            "Delegation runtime boundary escapes the repository root.",
        ) from error
    return current / f"{target_id}.json"


def _delegation_runtime_is_ignored(root: Path) -> bool:
    completed = subprocess.run(
        ["git", "check-ignore", "-q", str(DELEGATION_RUNTIME_RELATIVE_DIR / "probe.json")],
        cwd=str(root),
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def _validate_runtime_handle(handle: object, *, unit_id: str) -> dict[str, str]:
    if not isinstance(handle, dict):
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_INVALID", f"{unit_id} handle must be an object."
        )
    allowed = {"kind", "id", "worktree", "state"}
    unknown = set(handle) - allowed
    if unknown:
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_PRIVATE_FIELD",
            f"{unit_id} handle contains forbidden fields: {', '.join(sorted(unknown))}.",
        )
    normalized = {key: str(value).strip() for key, value in handle.items()}
    for key in ("kind", "id", "worktree", "state"):
        if not normalized.get(key):
            raise _delegation_error(
                "PW_DELEGATION_RUNTIME_INVALID", f"{unit_id} handle requires {key}."
            )
    if normalized["state"] not in {"active", "complete", "missing"}:
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_INVALID",
            f"{unit_id} handle state must be active, complete, or missing.",
        )
    return normalized


def initialize_delegation_runtime_state(root: Path, plan: DelegationPlan) -> dict[str, object]:
    if not _delegation_runtime_is_ignored(root):
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_NOT_IGNORED",
            f"{DELEGATION_RUNTIME_RELATIVE_DIR.as_posix()}/ must be ignored before state is written.",
        )
    existing = _load_delegation_runtime_state(root, plan.target.target_id)
    plan_fingerprint = _delegation_plan_fingerprint(plan)
    if existing is not None:
        if existing.get("plan_fingerprint") != plan_fingerprint:
            raise _delegation_error(
                "PW_DELEGATION_RUNTIME_PLAN_MISMATCH",
                "Existing runtime state belongs to a different canonical delegation plan; "
                "reconcile it instead of reinitializing and losing handles.",
            )
        return existing
    state = {
        "schema_version": DELEGATION_RUNTIME_SCHEMA_VERSION,
        "target_id": plan.target.target_id,
        "target_kind": plan.target.kind,
        "plan_fingerprint": plan_fingerprint,
        "worktree": str(root.resolve()),
        "units": {
            unit.unit_id: {
                "state": "complete" if unit.canonical_state == "complete" else "pending",
                "handle": None,
            }
            for unit in plan.units
        },
    }
    path = _delegation_runtime_path(root, plan.target.target_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as temporary:
        json.dump(state, temporary, indent=2, sort_keys=True)
        temporary.write("\n")
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, path)
    return state


def _load_delegation_runtime_state(root: Path, target_id: str) -> dict[str, object] | None:
    path = _delegation_runtime_path(root, target_id)
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema_version") != DELEGATION_RUNTIME_SCHEMA_VERSION:
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_INVALID", f"Unsupported runtime state in {path}."
        )
    allowed = {
        "schema_version",
        "target_id",
        "target_kind",
        "plan_fingerprint",
        "worktree",
        "units",
        "task_orchestration",
        "epic_orchestration",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_PRIVATE_FIELD",
            "Runtime state contains forbidden fields: " + ", ".join(sorted(unknown)) + ".",
        )
    if (
        raw.get("target_id") != target_id
        or not isinstance(raw.get("target_kind"), str)
        or not isinstance(raw.get("plan_fingerprint"), str)
        or not isinstance(raw.get("worktree"), str)
        or not isinstance(raw.get("units"), dict)
    ):
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_INVALID", "Runtime state target or units are invalid."
        )
    raw_units = raw["units"]
    assert isinstance(raw_units, dict)
    for unit_id, value in raw_units.items():
        if not isinstance(unit_id, str) or not isinstance(value, dict):
            raise _delegation_error(
                "PW_DELEGATION_RUNTIME_INVALID", "Runtime unit entries must be objects."
            )
        unit_unknown = set(value) - {"state", "handle"}
        if unit_unknown:
            raise _delegation_error(
                "PW_DELEGATION_RUNTIME_PRIVATE_FIELD",
                f"{unit_id} runtime entry contains forbidden fields: "
                + ", ".join(sorted(unit_unknown))
                + ".",
            )
        if value.get("state") not in DELEGATION_UNIT_STATES:
            raise _delegation_error(
                "PW_DELEGATION_RUNTIME_INVALID",
                f"{unit_id} has invalid runtime state '{value.get('state')}'.",
            )
        handle = value.get("handle")
        if handle is not None:
            _validate_runtime_handle(handle, unit_id=unit_id)
    if "task_orchestration" in raw:
        _task_orchestration_state_from_payload(raw["task_orchestration"])
    if "epic_orchestration" in raw:
        _epic_orchestration_state_from_payload(raw["epic_orchestration"])
    return raw


def reconcile_delegation_runtime_state(
    root: Path,
    plan: DelegationPlan,
    state: dict[str, object],
    observed_handles: dict[str, object],
) -> dict[str, object]:
    """Reconcile canonical state with host observations without inventing missing handles."""
    if "epic_orchestration" in state:
        raise _delegation_error(
            "PW_EPIC_RECONCILIATION_REQUIRES_HOST",
            "Epic persistent-task state requires exact attempt, handle, checkout, and "
            "worktree observations through EpicOrchestrator.resume/reconcile.",
        )
    if state.get("target_id") != plan.target.target_id:
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_TARGET_MISMATCH", "Runtime state target does not match plan."
        )
    stored_units = state.get("units")
    if not isinstance(stored_units, dict):
        raise _delegation_error("PW_DELEGATION_RUNTIME_INVALID", "Runtime units are invalid.")
    normalized_observed = {
        unit_id: _validate_runtime_handle(handle, unit_id=unit_id)
        for unit_id, handle in observed_handles.items()
    }
    plan_by_id = {unit.unit_id: unit for unit in plan.units}
    reconciled_units: dict[str, object] = {}
    for unit_id in plan.selected_units:
        unit = plan_by_id[unit_id]
        stored = stored_units.get(unit_id, {})
        if not isinstance(stored, dict):
            stored = {}
        stored_handle = stored.get("handle")
        observed = normalized_observed.get(unit_id)
        if unit.canonical_state == "complete":
            reconciled_units[unit_id] = {"state": "complete", "handle": stored_handle}
            continue
        if observed is not None and observed["state"] == "active":
            state_name = (
                "active" if Path(observed["worktree"]).resolve() == root.resolve() else "orphaned"
            )
            reconciled_units[unit_id] = {"state": state_name, "handle": observed}
            continue
        if stored.get("state") == "active" or stored_handle is not None:
            reconciled_units[unit_id] = {
                "state": "orphaned",
                "handle": observed if observed is not None else stored_handle,
            }
            continue
        reconciled_units[unit_id] = {"state": "pending", "handle": None}
    result = {
        "schema_version": DELEGATION_RUNTIME_SCHEMA_VERSION,
        "target_id": plan.target.target_id,
        "target_kind": plan.target.kind,
        "plan_fingerprint": _delegation_plan_fingerprint(plan),
        "worktree": str(root.resolve()),
        "units": reconciled_units,
    }
    if "task_orchestration" in state:
        task_runtime = _task_orchestration_state_from_payload(state["task_orchestration"])
        for unit in plan.units:
            run = task_runtime.units[unit.unit_id]
            observed = normalized_observed.get(unit.unit_id)
            if unit.canonical_state == "complete":
                run.state = "done"
                run.handle = None
                run.completion_provenance = (
                    f"canonical:{plan.target.source_path}#{plan.target.source_hash}"
                )
            elif run.state in {"active", "returned"}:
                expected_kind = (
                    "subagent"
                    if run.executor
                    in {
                        "bounded-subagent",
                        "sequential-worker",
                    }
                    else run.executor
                )
                identity_matches = (
                    observed is not None
                    and observed["id"] == run.handle
                    and observed["kind"] == expected_kind
                )
                if (
                    not identity_matches
                    or observed is None
                    or Path(observed["worktree"]).resolve() != root.resolve()
                ):
                    run.state = "orphaned"
                    run.handle = None
                elif observed["state"] == "active":
                    run.state = "active"
                elif observed["state"] == "complete":
                    run.state = "returned"
                else:
                    run.state = "failed"
                    run.handle = None
                    run.issues = ("Observed worker failure during CLI reconciliation.",)
                    task_runtime.failure_seen = True
        result["task_orchestration"] = _task_orchestration_state_payload(task_runtime)
        projected_units: dict[str, object] = {}
        for unit_id, run in task_runtime.units.items():
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
            projected_units[unit_id] = {"state": projected, "handle": None}
        result["units"] = projected_units
    return result


def _write_delegation_runtime_state(
    root: Path, plan: DelegationPlan, state: dict[str, object]
) -> None:
    if not _delegation_runtime_is_ignored(root):
        raise _delegation_error(
            "PW_DELEGATION_RUNTIME_NOT_IGNORED",
            f"{DELEGATION_RUNTIME_RELATIVE_DIR.as_posix()}/ must remain ignored.",
        )
    path = _delegation_runtime_path(root, plan.target.target_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as temporary:
        json.dump(state, temporary, indent=2, sort_keys=True)
        temporary.write("\n")
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, path)


def _delegation_status_payload(
    plan: DelegationPlan, state: dict[str, object] | None
) -> dict[str, object]:
    payload = delegation_plan_payload(plan)
    payload["runtime"] = state
    if state is None:
        payload["runtime_summary"] = {"initialized": False, "active": [], "orphaned": []}
    else:
        units = state.get("units", {})
        assert isinstance(units, dict)
        task_runtime = None
        epic_runtime = None
        if "task_orchestration" in state:
            task_runtime = _task_orchestration_state_from_payload(state["task_orchestration"])
            units = {
                unit_id: {"state": run.state, "handle": run.handle}
                for unit_id, run in task_runtime.units.items()
            }
        elif "epic_orchestration" in state:
            epic_runtime = _epic_orchestration_state_from_payload(state["epic_orchestration"])
            units = {
                unit_id: {"state": run.state, "handle": run.handle}
                for unit_id, run in epic_runtime.units.items()
            }
        unavailable = {
            unit_id
            for unit_id, value in units.items()
            if isinstance(value, dict) and value.get("state") != "pending"
        }
        payload["eligible_units"] = [
            unit_id for unit_id in plan.eligible_units if unit_id not in unavailable
        ]
        payload["blocked_units"] = list(dict.fromkeys([*plan.blocked_units, *sorted(unavailable)]))
        plan_units = payload["units"]
        assert isinstance(plan_units, list)
        for plan_unit in plan_units:
            assert isinstance(plan_unit, dict)
            runtime_unit = units.get(plan_unit["id"])
            if not isinstance(runtime_unit, dict):
                continue
            runtime_state = runtime_unit.get("state")
            if runtime_state != "pending":
                plan_unit["readiness"] = runtime_state
                plan_unit["blocking_reasons"] = [
                    (
                        "Runtime handle is active; resume without relaunch."
                        if runtime_state == "active"
                        else "Runtime Task state is not launch-eligible; reconcile or resume it."
                    )
                ]
        runtime_summary: dict[str, object] = {
            "initialized": True,
            "active": sorted(
                unit_id
                for unit_id, value in units.items()
                if isinstance(value, dict) and value.get("state") == "active"
            ),
            "orphaned": sorted(
                unit_id
                for unit_id, value in units.items()
                if isinstance(value, dict) and value.get("state") == "orphaned"
            ),
        }
        payload["runtime_summary"] = runtime_summary
        if task_runtime is not None:
            runtime_summary.update(
                {
                    "returned": sorted(
                        unit_id
                        for unit_id, run in task_runtime.units.items()
                        if run.state == "returned"
                    ),
                    "completed": sorted(
                        unit_id
                        for unit_id, run in task_runtime.units.items()
                        if run.state == "done"
                    ),
                    "attempts": {
                        unit_id: run.attempt for unit_id, run in sorted(task_runtime.units.items())
                    },
                    "no_relaunch": sorted(unavailable),
                }
            )
        if epic_runtime is not None:
            runtime_summary.update(
                {
                    "returned": sorted(
                        unit_id
                        for unit_id, run in epic_runtime.units.items()
                        if run.state == "returned"
                    ),
                    "completed": sorted(
                        unit_id
                        for unit_id, run in epic_runtime.units.items()
                        if run.state == "verified"
                    ),
                    "attempts": {
                        unit_id: run.attempt for unit_id, run in sorted(epic_runtime.units.items())
                    },
                    "create_count": epic_runtime.create_count,
                    "lifecycle": {
                        unit_id: {
                            "executor": run.executor,
                            "visibility_class": run.visibility_class,
                            "retention_policy": run.retention_policy,
                            "disposition_state": run.disposition_state,
                            "retirement_state": run.retirement_state,
                            "attention_reasons": list(run.attention_reasons),
                            "owner_promoted": run.owner_promoted,
                            "explicit_retain_reason": run.explicit_retain_reason,
                            "prior_visible_handles": len(run.prior_handles),
                        }
                        for unit_id, run in sorted(epic_runtime.units.items())
                    },
                    "retirement_confirmed": sorted(
                        unit_id
                        for unit_id, run in epic_runtime.units.items()
                        if run.retirement_state == "confirmed"
                    ),
                    "retirement_pending": sorted(
                        unit_id
                        for unit_id, run in epic_runtime.units.items()
                        if run.retirement_state in {"pending", "requested", "failed", "unknown"}
                    ),
                    "visible_retained": sorted(
                        unit_id
                        for unit_id, run in epic_runtime.units.items()
                        if run.visibility_class.startswith("visible-")
                        and run.retirement_state != "confirmed"
                    ),
                    "no_relaunch": sorted(
                        unit_id
                        for unit_id, run in epic_runtime.units.items()
                        if run.state != "pending"
                    ),
                }
            )
    return payload
