"""Canonical Project Workflow coordination runtime."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import time
from collections.abc import Callable, Mapping
from dataclasses import asdict
from pathlib import Path

from .contracts import (
    COORDINATION_BOUNDARIES,
    COORDINATION_CONTRACT_VERSION,
    COORDINATION_FILENAME,
    COORDINATION_SCHEMA_VERSION,
    CURRENT_ASSET_VERSION,
    CURRENT_PACKAGE_VERSION,
    DECOMPOSITION_PLAN_FILENAME,
    EPIC_AMENDMENTS_FILENAME,
    EPIC_CONTRACT_FILENAME,
    EPIC_TRACKER_STATUSES,
    EXECUTION_CAPABILITY_STATES,
    EXECUTION_CONTROL_SCHEMA_VERSION,
    EXECUTION_DIRECT_OPERATIONS,
    EXECUTION_MATERIAL_OPERATIONS,
    EXECUTION_PHASES,
    EXECUTION_RECEIPT_OUTCOMES,
    EXECUTION_REQUIRED_CAPABILITY_CONTROLS,
    EXECUTION_REQUIRED_LIMIT_UNITS,
    INTENT_AUDIT_FILENAME,
    STRUCTURED_EVIDENCE_FILENAME,
    TRACKER_STATUSES,
    VERIFICATION_ADAPTER_CAPABILITIES,
    VERIFICATION_CAMPAIGN_MODES,
    VERIFICATION_CAMPAIGN_OUTCOMES,
    VERIFICATION_CAMPAIGN_SCHEMA_VERSION,
    VERIFICATION_CAMPAIGN_STAGES,
    VERIFICATION_OPERATIONAL_STATES,
    VERIFICATION_RECEIPT_OUTCOMES,
    OperationalStatusProofLayer,
    OperationalStatusSource,
)
from .lifecycle import (
    _approval_envelope_issues,
    _epic_audit_rows,
    _epic_requirements_readiness_issues,
    _epic_retro_issues,
    _epic_status_transition_allowed,
    _epic_tracker_rows,
    _format_epic_tracker_row,
    _format_global_tracker_row,
    _format_readiness_block,
    _global_tracker_rows,
    _has_qa_review_evidence,
    _inspect_operational_active_work,
    _intent_audit_gate_issues,
    _intent_qa_review_issues,
    _is_discovery_work,
    _legacy_adoption_evidence_untrusted,
    _operational_item_proof_layers,
    _operational_status_global_kind,
    _operational_work_item_from_row,
    _owner_acceptance_completion_issues,
    _parent_ac_evidence_present,
    _repository_evidence_issues,
    _resolve_epic_dir,
    _status_requires_epic_child_readiness,
    _status_requires_task_readiness,
    _status_transition_allowed,
    _structured_evidence_issues,
    _task_ready_issues_for_paths,
    _task_testing_integrity_issues,
    _validate_status_force_args,
)
from .orchestration import (
    _delegation_relative_path,
)
from .repository import (
    _clean_markdown_cell_path,
    _decomposition_plan_path,
    _epic_contract_issues,
    _extract_ac_ids,
    _extract_parent_ac_coverage,
    _normalize_task_status_id,
    _operational_git_optional,
    _repository_compatibility,
)


def _coordination_work_item_dir(root: Path, target_id: str) -> Path:
    tasks_dir = root / ".project-workflow" / "tasks"
    matches = sorted(path for path in tasks_dir.rglob(f"{target_id}-*") if path.is_dir())
    if not matches:
        raise ValueError(f"No work-item folder found for {target_id}.")
    if len(matches) > 1:
        raise ValueError(
            f"Multiple work-item folders found for {target_id}: "
            + ", ".join(str(path) for path in matches)
        )
    return matches[0]


def _coordination_state_path(root: Path, target_id: str) -> Path:
    return _coordination_work_item_dir(root, target_id) / COORDINATION_FILENAME


def _coordination_artifact_identity(root: Path, target_id: str) -> str:
    work_dir = _coordination_work_item_dir(root, target_id)
    authority_paths = [work_dir / "REQUIREMENTS.md"]
    if (work_dir / EPIC_CONTRACT_FILENAME).is_file():
        authority_paths.extend(
            (
                work_dir / EPIC_CONTRACT_FILENAME,
                work_dir / DECOMPOSITION_PLAN_FILENAME,
                work_dir / EPIC_AMENDMENTS_FILENAME,
                work_dir / INTENT_AUDIT_FILENAME,
            )
        )
    elif (work_dir.parent / EPIC_CONTRACT_FILENAME).is_file():
        authority_paths.extend(
            (
                work_dir.parent / "REQUIREMENTS.md",
                work_dir.parent / EPIC_CONTRACT_FILENAME,
                work_dir.parent / DECOMPOSITION_PLAN_FILENAME,
                work_dir.parent / EPIC_AMENDMENTS_FILENAME,
                work_dir.parent / INTENT_AUDIT_FILENAME,
            )
        )
    digest = hashlib.sha256()
    existing = [path for path in authority_paths if path.is_file()]
    if not existing:
        raise ValueError(f"{target_id} has no readable requirements authority.")
    for path in sorted(dict.fromkeys(existing)):
        digest.update(_delegation_relative_path(root, path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def _coordination_required_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")
    return value.strip()


def _coordination_string_list(value: object, field_name: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise ValueError(f"{field_name} must be a non-empty string list.")
    return list(dict.fromkeys(item.strip() for item in value))


def _verification_optional_limit(value: object, field_name: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer or null.")
    return value


def _verification_identity(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _verification_receipt_ledger_identity(receipts: list[object]) -> str:
    return _verification_identity(
        {
            "receipt_identities": [
                receipt.get("receipt_identity") for receipt in receipts if isinstance(receipt, dict)
            ]
        }
    )


def _verification_validate_requirement(requirement: object) -> None:
    if not isinstance(requirement, dict) or not isinstance(requirement.get("required"), bool):
        raise ValueError("verification_requirement must declare required as boolean.")
    claims = requirement.get("claims")
    stages = requirement.get("stages")
    affected_scope = requirement.get("affected_scope")
    if requirement["required"] is False:
        if claims != [] or stages != [] or affected_scope != []:
            raise ValueError(
                "A non-material verification requirement cannot declare claims, stages, or scope."
            )
        if requirement.get("proof_contract_identity") is not None:
            raise ValueError(
                "A non-material verification requirement cannot declare a proof contract."
            )
        return
    parsed_claims = _coordination_string_list(claims, "verification_requirement.claims")
    parsed_stages = _coordination_string_list(stages, "verification_requirement.stages")
    unknown_stages = [stage for stage in parsed_stages if stage not in VERIFICATION_CAMPAIGN_STAGES]
    if unknown_stages:
        raise ValueError(
            "verification_requirement.stages contains unknown stages: " + ", ".join(unknown_stages)
        )
    indexes = [VERIFICATION_CAMPAIGN_STAGES.index(stage) for stage in parsed_stages]
    if indexes != sorted(indexes):
        raise ValueError("verification_requirement.stages must use canonical stage order.")
    parsed_scope = _coordination_string_list(
        affected_scope, "verification_requirement.affected_scope"
    )
    expected = _verification_identity(
        {
            "claims": parsed_claims,
            "stages": parsed_stages,
            "affected_scope": parsed_scope,
        }
    )
    if requirement.get("proof_contract_identity") != expected:
        raise ValueError("verification_requirement.proof_contract_identity is stale or malformed.")


def _execution_required_proof_obligations(requirement: object) -> list[str]:
    """Derive active execution obligations from Coordinator-owned verification authority."""
    if requirement is None:
        return []
    _verification_validate_requirement(requirement)
    assert isinstance(requirement, dict)
    if requirement["required"] is False:
        return []
    claims = requirement["claims"]
    assert isinstance(claims, list)
    proof_contract_identity = str(requirement["proof_contract_identity"])
    return [
        f"verification-contract:{proof_contract_identity}",
        *(f"verification-claim:{claim}" for claim in claims),
    ]


def _verification_validate_campaign(campaign: object) -> None:
    if not isinstance(campaign, dict):
        raise ValueError("verification_campaign must be an object when present.")
    if campaign.get("schema_version") != VERIFICATION_CAMPAIGN_SCHEMA_VERSION:
        raise ValueError(
            f"verification_campaign.schema_version must be {VERIFICATION_CAMPAIGN_SCHEMA_VERSION}."
        )
    for field_name in (
        "candidate_identity",
        "intent_identity",
        "source_identity",
        "proof_contract_identity",
        "next_action",
    ):
        _coordination_required_text(campaign.get(field_name), f"verification_campaign.{field_name}")
    mode = campaign.get("mode")
    if mode not in VERIFICATION_CAMPAIGN_MODES:
        raise ValueError("verification_campaign.mode is invalid.")
    if campaign.get("impact") not in {"known", "unknown"}:
        raise ValueError("verification_campaign.impact is invalid.")
    claims = _coordination_string_list(campaign.get("claims"), "verification_campaign.claims")
    stages = _coordination_string_list(campaign.get("stages"), "verification_campaign.stages")
    unknown_stages = [stage for stage in stages if stage not in VERIFICATION_CAMPAIGN_STAGES]
    if unknown_stages:
        raise ValueError(
            "verification_campaign.stages contains unknown stages: " + ", ".join(unknown_stages)
        )
    indexes = [VERIFICATION_CAMPAIGN_STAGES.index(stage) for stage in stages]
    if indexes != sorted(indexes):
        raise ValueError("verification_campaign.stages must use canonical stage order.")
    if mode == "certification" and "full" not in stages:
        raise ValueError("A certification campaign must include the full stage.")
    affected_scope = _coordination_string_list(
        campaign.get("affected_scope"), "verification_campaign.affected_scope"
    )
    limits = campaign.get("limits")
    if not isinstance(limits, dict):
        raise ValueError("verification_campaign.limits must be an object.")
    parsed_limits = {
        key: _verification_optional_limit(limits.get(key), f"verification_campaign.limits.{key}")
        for key in ("max_failures", "max_target_calls", "max_elapsed_seconds")
    }
    if not any(value is not None for value in parsed_limits.values()):
        raise ValueError("A material verification campaign requires at least one finite limit.")
    diagnostic_decision = campaign.get("diagnostic_decision")
    if mode == "diagnostic":
        _coordination_required_text(
            diagnostic_decision, "verification_campaign.diagnostic_decision"
        )
    elif diagnostic_decision is not None:
        raise ValueError(
            "verification_campaign.diagnostic_decision is valid only in diagnostic mode."
        )
    adapter = campaign.get("adapter")
    if not isinstance(adapter, dict) or adapter.get("kind") not in {"manual", "command"}:
        raise ValueError("verification_campaign.adapter.kind must be manual or command.")
    capabilities = adapter.get("capabilities")
    if not isinstance(capabilities, list) or any(
        capability not in VERIFICATION_ADAPTER_CAPABILITIES for capability in capabilities
    ):
        raise ValueError("verification_campaign.adapter.capabilities is invalid.")
    if len(capabilities) != len(set(capabilities)):
        raise ValueError("verification_campaign.adapter.capabilities contains duplicates.")
    adapter_command = adapter.get("command")
    manual_command = adapter.get("manual_command")
    if adapter.get("kind") == "command":
        if (
            not isinstance(adapter_command, list)
            or not adapter_command
            or any(not isinstance(part, str) or not part.strip() for part in adapter_command)
        ):
            raise ValueError(
                "verification_campaign.adapter.command must be a non-empty argument list."
            )
        if manual_command is not None:
            raise ValueError(
                "verification_campaign.adapter.manual_command is invalid for command adapters."
            )
    else:
        _coordination_required_text(manual_command, "verification_campaign.adapter.manual_command")
        if adapter_command is not None:
            raise ValueError(
                "verification_campaign.adapter.command is invalid for manual adapters."
            )
    receipts = campaign.get("receipts")
    if not isinstance(receipts, list):
        raise ValueError("verification_campaign.receipts must be a list.")
    seen_receipts: set[str] = set()
    for index, receipt in enumerate(receipts):
        prefix = f"verification_campaign.receipts[{index}]"
        if not isinstance(receipt, dict):
            raise ValueError(f"{prefix} must be an object.")
        for field_name in (
            "receipt_identity",
            "candidate_identity",
            "intent_identity",
            "source_identity",
            "proof_contract_identity",
            "stage",
            "runtime_identity",
            "target_identity",
            "evaluator_identity",
            "artifact",
            "recorded_at",
        ):
            _coordination_required_text(receipt.get(field_name), f"{prefix}.{field_name}")
        _coordination_string_list(receipt.get("scope"), f"{prefix}.scope")
        request_identity = receipt.get("request_identity")
        if adapter.get("kind") == "command":
            _coordination_required_text(request_identity, f"{prefix}.request_identity")
        elif request_identity is not None:
            raise ValueError(f"{prefix}.request_identity is valid only for command adapters.")
        if receipt["receipt_identity"] in seen_receipts:
            raise ValueError("verification_campaign contains duplicate receipt identities.")
        seen_receipts.add(str(receipt["receipt_identity"]))
        if receipt.get("stage") not in stages:
            raise ValueError(f"{prefix}.stage is outside the campaign stages.")
        if receipt.get("outcome") not in VERIFICATION_RECEIPT_OUTCOMES:
            raise ValueError(f"{prefix}.outcome is invalid.")
        for field_name in ("target_calls", "elapsed_seconds"):
            value = receipt.get(field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{prefix}.{field_name} must be a non-negative integer.")
        if not isinstance(receipt.get("stage_complete"), bool):
            raise ValueError(f"{prefix}.stage_complete must be boolean.")
        if not isinstance(receipt.get("regrade"), bool):
            raise ValueError(f"{prefix}.regrade must be boolean.")
        receipt_base = {key: value for key, value in receipt.items() if key != "receipt_identity"}
        if receipt.get("receipt_identity") != _verification_identity(receipt_base):
            raise ValueError(f"{prefix}.receipt_identity is stale or malformed.")
    if campaign.get("receipt_ledger_identity") != _verification_receipt_ledger_identity(receipts):
        raise ValueError("verification_campaign.receipt_ledger_identity is stale or malformed.")
    outcome = campaign.get("outcome")
    if outcome not in VERIFICATION_CAMPAIGN_OUTCOMES:
        raise ValueError("verification_campaign.outcome is invalid.")
    current_stage = campaign.get("current_stage")
    if current_stage is not None and current_stage not in stages:
        raise ValueError("verification_campaign.current_stage is invalid.")
    expected_contract_identity = _verification_identity(
        {
            "claims": claims,
            "stages": stages,
            "affected_scope": affected_scope,
        }
    )
    if campaign.get("proof_contract_identity") != expected_contract_identity:
        raise ValueError("verification_campaign.proof_contract_identity is stale or malformed.")


def _coordination_load_state(root: Path, target_id: str) -> dict[str, object]:
    path = _coordination_state_path(root, target_id)
    if not path.is_file():
        raise ValueError(
            f"Missing {COORDINATION_FILENAME} for {target_id}; run `coordinate init` first."
        )
    payload: object = json.loads(path.read_text(encoding="utf-8"))
    _coordination_validate_state(payload, target_id=target_id)
    assert isinstance(payload, dict)
    return payload


def _coordination_validate_state(payload: object, *, target_id: str | None = None) -> None:
    if not isinstance(payload, dict):
        raise ValueError("Coordination state must be a JSON object.")
    if payload.get("schema_version") != COORDINATION_SCHEMA_VERSION:
        raise ValueError(f"Coordination schema_version must be {COORDINATION_SCHEMA_VERSION}.")
    actual_target = _coordination_required_text(payload.get("target_id"), "target_id")
    if target_id is not None and actual_target != target_id:
        raise ValueError(
            f"Coordination target mismatch: expected {target_id}, found {actual_target}."
        )
    for field_name in (
        "work_item_path",
        "intent_identity",
        "phase",
        "source_revision",
        "next_action",
    ):
        _coordination_required_text(payload.get(field_name), field_name)
    loaded = payload.get("loaded_contract")
    if not isinstance(loaded, dict):
        raise ValueError("loaded_contract must be an object.")
    for field_name in (
        "package_version",
        "asset_version",
        "contract_version",
        "context_id",
        "recorded_at",
    ):
        _coordination_required_text(loaded.get(field_name), f"loaded_contract.{field_name}")
    for field_name in ("decisions", "boundary_decisions"):
        if not isinstance(payload.get(field_name), list):
            raise ValueError(f"{field_name} must be a list.")
    repositories = payload.get("repositories")
    if not isinstance(repositories, dict) or not repositories:
        raise ValueError("repositories must be a non-empty object.")
    for repository_id, repository in repositories.items():
        _coordination_required_text(repository_id, "repositories key")
        if not isinstance(repository, dict):
            raise ValueError("Each repositories entry must be an object.")
        _coordination_required_text(
            repository.get("source_revision"),
            f"repositories.{repository_id}.source_revision",
        )
    if not isinstance(payload.get("host_facts"), dict):
        raise ValueError("host_facts must be an object.")
    checkpoint = payload.get("outcome_checkpoint")
    if not isinstance(checkpoint, dict):
        raise ValueError("outcome_checkpoint must be an object.")
    if checkpoint.get("status") not in {"not-required", "pending", "pass", "fail"}:
        raise ValueError("outcome_checkpoint.status is invalid.")
    campaign = payload.get("verification_campaign")
    requirement = payload.get("verification_requirement")
    if requirement is not None:
        _verification_validate_requirement(requirement)
    if campaign is not None:
        _verification_validate_campaign(campaign)
        if isinstance(requirement, dict):
            if requirement.get("required") is not True:
                raise ValueError(
                    "A verification campaign cannot exist when material verification is not required."
                )
            for campaign_field, requirement_field in (
                ("claims", "claims"),
                ("stages", "stages"),
                ("affected_scope", "affected_scope"),
                ("proof_contract_identity", "proof_contract_identity"),
            ):
                if campaign.get(campaign_field) != requirement.get(requirement_field):
                    raise ValueError(
                        "verification_campaign does not match the durable verification requirement."
                    )
    execution_control = payload.get("execution_control")
    if execution_control is not None:
        validated_control = _execution_validate_control(execution_control, work_id=actual_target)
        required_obligations = _execution_required_proof_obligations(requirement)
        active_obligations = validated_control["proof_obligations"]
        assert isinstance(active_obligations, list)
        missing_obligations = [
            obligation
            for obligation in required_obligations
            if obligation not in active_obligations
        ]
        if missing_obligations:
            raise ValueError(
                "execution_control omits the durable verification requirement: "
                + ", ".join(missing_obligations)
            )
    execution_history = payload.get("execution_control_history")
    if execution_history is not None:
        if not isinstance(execution_history, list):
            raise ValueError("execution_control_history must be a list.")
        snapshot_identities: set[str] = set()
        for index, historical in enumerate(execution_history):
            try:
                validated = _execution_validate_control(historical, work_id=actual_target)
            except ValueError as exc:
                raise ValueError(f"execution_control_history[{index}] is invalid: {exc}") from exc
            snapshot_identity = _execution_hash(validated)
            if snapshot_identity in snapshot_identities:
                raise ValueError("execution_control_history contains a duplicate snapshot.")
            snapshot_identities.add(snapshot_identity)


def _coordination_write_state(root: Path, target_id: str, payload: dict[str, object]) -> Path:
    _coordination_validate_state(payload, target_id=target_id)
    path = _coordination_state_path(root, target_id)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _coordination_preflight_payload(
    root: Path, target_id: str, state: dict[str, object]
) -> dict[str, object]:
    loaded = state["loaded_contract"]
    assert isinstance(loaded, dict)
    loaded_package = str(loaded.get("package_version", "unknown")).strip()
    loaded_asset = str(loaded.get("asset_version", "unknown")).strip()
    loaded_contract = str(loaded.get("contract_version", "unknown")).strip()
    recorded_identity = str(state.get("intent_identity", ""))
    current_identity = _coordination_artifact_identity(root, target_id)
    repository_manifest = _repository_compatibility(root).manifest
    repository_identity = (
        {
            "package_version": repository_manifest.package_version,
            "asset_version": str(repository_manifest.asset_version),
            "contract_version": str(COORDINATION_CONTRACT_VERSION),
        }
        if repository_manifest is not None
        else {
            "package_version": "unknown",
            "asset_version": "unknown",
            "contract_version": str(COORDINATION_CONTRACT_VERSION),
        }
    )
    reasons: list[str] = []
    unknown_tokens = {"", "unknown", "not observed"}
    if (
        loaded_package.lower() in unknown_tokens
        or loaded_asset.lower() in unknown_tokens
        or loaded_contract.lower() in unknown_tokens
    ):
        contract_state = "unknown"
        reasons.append("Declared physical-context contract identity is unknown.")
    elif recorded_identity != current_identity:
        contract_state = "stale"
        reasons.append("Approved Intent authority changed after coordination state was recorded.")
    elif loaded_contract != str(COORDINATION_CONTRACT_VERSION):
        contract_state = "stale"
        reasons.append("Declared physical-context coordination contract is older or incompatible.")
    elif loaded_package == CURRENT_PACKAGE_VERSION and loaded_asset == str(CURRENT_ASSET_VERSION):
        contract_state = "current"
        reasons.append(
            "Declared physical-context package, assets, and coordination contract are current."
        )
    else:
        contract_state = "compatible"
        reasons.append(
            "Declared coordination contract is current; package or asset provenance differs."
        )
    if (
        contract_state == "stale"
        and repository_identity["package_version"] == CURRENT_PACKAGE_VERSION
        and repository_identity["asset_version"] == str(CURRENT_ASSET_VERSION)
    ):
        reasons.append(
            "Repository assets are current, but explicit contract loading has not been declared."
        )
    if contract_state in {"current", "compatible"}:
        action = "proceed"
        command = None
    else:
        action = "contract-load-required"
        command = (
            f"./.project-workflow/cli/workflow coordinate context-record --id {target_id} "
            f"--loaded-package-version {CURRENT_PACKAGE_VERSION} "
            f"--loaded-asset-version {CURRENT_ASSET_VERSION} "
            f"--loaded-contract-version {COORDINATION_CONTRACT_VERSION} "
            "--context-id <context-id-after-explicit-load> --next-action <bounded-next-action>"
        )
    return {
        "schema_version": COORDINATION_SCHEMA_VERSION,
        "target_id": target_id,
        "contract_state": contract_state,
        "loaded_contract": loaded,
        "repository_contract": repository_identity,
        "recorded_intent_identity": recorded_identity,
        "current_intent_identity": current_identity,
        "reasons": reasons,
        "next_action": action,
        "command": command,
    }


def _coordination_boundary_gate_issues(
    root: Path,
    target_id: str,
    *,
    boundary: str,
    subject_id: str | None = None,
) -> list[str]:
    """Require one current semantic decision without creating a second execution graph."""
    if boundary not in COORDINATION_BOUNDARIES:
        return [f"unknown coordination boundary: {boundary}"]
    try:
        path = _coordination_state_path(root, target_id)
    except ValueError:
        return []
    if not path.is_file():
        return []
    try:
        state = _coordination_load_state(root, target_id)
        preflight = _coordination_preflight_payload(root, target_id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return [f"coordination state is invalid: {exc}"]
    if preflight["contract_state"] not in {"current", "compatible"}:
        return [
            f"coordination contract is {preflight['contract_state']}; explicitly load and declare "
            "the applicable contract before continuing"
        ]
    current_identity = str(preflight["current_intent_identity"])
    current_source_identity = _coordination_source_identity(state)
    decisions = state.get("boundary_decisions", [])
    assert isinstance(decisions, list)
    stale_match = False
    stale_source_match = False
    for raw in reversed(decisions):
        if not isinstance(raw, dict) or raw.get("boundary") != boundary:
            continue
        subjects = raw.get("affected_units", [])
        if subject_id is not None and (
            not isinstance(subjects, list) or subject_id not in subjects
        ):
            continue
        if raw.get("intent_identity") != current_identity:
            stale_match = True
            continue
        if raw.get("source_identity") != current_source_identity:
            stale_source_match = True
            continue
        classification = raw.get("classification")
        if classification in {"inside-envelope", "approved-change"}:
            return []
        if classification == "drift-detected":
            consequence = str(raw.get("user_consequence", "material outcome drift"))
            return [
                f"{boundary} is blocked by recorded drift for {subject_id or target_id}: "
                f"{consequence}"
            ]
    subject = subject_id or target_id
    if stale_source_match:
        return [
            f"stale source-bound {boundary} decision for {subject}; record the bounded decision "
            "against current repository/source authority before continuing"
        ]
    if stale_match:
        return [
            f"stale {boundary} intent decision for {subject}; record the bounded decision against "
            "current authority before continuing"
        ]
    return [
        f"missing current {boundary} intent decision for {subject}; record the bounded decision "
        "before continuing"
    ]


def _coordination_checkpoint_gate_issues(
    root: Path, target_id: str, *, subject_id: str
) -> list[str]:
    try:
        path = _coordination_state_path(root, target_id)
    except ValueError:
        return []
    if not path.is_file():
        return []
    try:
        state = _coordination_load_state(root, target_id)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return [f"coordination state is invalid: {exc}"]
    checkpoint = state.get("outcome_checkpoint")
    if not isinstance(checkpoint, dict) or checkpoint.get("required") is not True:
        return []
    status = checkpoint.get("status")
    checkpoint_unit = str(checkpoint.get("checkpoint_unit") or "")
    if status == "pass":
        return []
    if status == "pending" and subject_id == checkpoint_unit:
        return []
    if status == "pending":
        return [
            f"early outcome checkpoint {checkpoint_unit} must pass before starting {subject_id}"
        ]
    if status == "fail":
        return ["early outcome checkpoint failed; restore or amend the approved outcome"]
    return ["early outcome checkpoint state is invalid"]


def _coordination_source_identity(state: Mapping[str, object]) -> str:
    payload = {
        "source_revision": state.get("source_revision"),
        "repositories": state.get("repositories"),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _verification_work_item_layers(
    root: Path, target_id: str
) -> tuple[str, dict[str, OperationalStatusProofLayer]]:
    work_items, _findings = _inspect_operational_active_work(root)
    matches = [item for item in work_items if item.item_id == target_id]
    if not matches:
        tracker_path = root / ".project-workflow" / "TRACKER.md"
        if tracker_path.is_file():
            _lines, _header, rows = _global_tracker_rows(tracker_path)
            terminal_rows = [row for row in rows if row.get("ID", "").strip() == target_id]
            if len(terminal_rows) == 1:
                item = _operational_work_item_from_row(
                    terminal_rows[0],
                    kind=_operational_status_global_kind(target_id),
                    source=OperationalStatusSource(
                        "global-tracker", ".project-workflow/TRACKER.md"
                    ),
                )
                if item is not None:
                    matches = [item]
    if len(matches) != 1:
        raise ValueError(
            f"Operational lifecycle contains {len(matches)} work items named {target_id}; "
            "exactly one is required."
        )
    item = matches[0]
    layers = {layer.name: layer for layer in _operational_item_proof_layers(root, item)}
    return item.lifecycle, layers


def _verification_completed_stages(campaign: Mapping[str, object]) -> list[str]:
    mode = str(campaign.get("mode"))
    completed: list[str] = []
    receipts = campaign.get("receipts", [])
    assert isinstance(receipts, list)
    raw_stages = campaign.get("stages", [])
    assert isinstance(raw_stages, list)
    for stage in raw_stages:
        stage_receipts = [
            receipt
            for receipt in receipts
            if isinstance(receipt, dict) and receipt.get("stage") == stage
        ]
        if mode == "certification":
            stage_complete = any(
                receipt.get("outcome") == "pass" and receipt.get("stage_complete") is True
                for receipt in stage_receipts
            )
        else:
            stage_complete = any(
                receipt.get("stage_complete") is True
                and receipt.get("outcome") in {"pass", "product-failure"}
                for receipt in stage_receipts
            )
        if stage_complete:
            completed.append(str(stage))
    return completed


def _verification_campaign_currentness(
    root: Path, target_id: str, state: Mapping[str, object], campaign: Mapping[str, object]
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    current_intent = _coordination_artifact_identity(root, target_id)
    current_source = _coordination_source_identity(state)
    if campaign.get("intent_identity") != current_intent:
        reasons.append("approved Intent authority changed after campaign initialization")
    if campaign.get("source_identity") != current_source:
        reasons.append("candidate source identity changed after campaign initialization")
    receipts = campaign.get("receipts", [])
    assert isinstance(receipts, list)
    for receipt in receipts:
        assert isinstance(receipt, dict)
        for field_name, expected in (
            ("candidate_identity", campaign.get("candidate_identity")),
            ("intent_identity", campaign.get("intent_identity")),
            ("source_identity", campaign.get("source_identity")),
            ("proof_contract_identity", campaign.get("proof_contract_identity")),
        ):
            if receipt.get(field_name) != expected:
                reasons.append(
                    f"receipt {receipt.get('receipt_identity', 'unknown')} has stale {field_name}"
                )
    return not reasons, reasons


def _verification_campaign_projection(
    root: Path,
    target_id: str,
    state: Mapping[str, object],
    *,
    material_verification: bool | None = None,
) -> dict[str, object]:
    campaign = state.get("verification_campaign")
    requirement = state.get("verification_requirement")
    if isinstance(requirement, dict):
        material_required = requirement.get("required") is True
        required_stages = [str(stage) for stage in requirement.get("stages", [])]
        required_scope = [str(scope) for scope in requirement.get("affected_scope", [])]
    else:
        material_required = bool(material_verification)
        required_stages = []
        required_scope = []
    lifecycle, layers = _verification_work_item_layers(root, target_id)
    implementation = layers.get("implementation")
    qa = layers.get("qa-review")
    implementation_pass = implementation is not None and implementation.state == "pass"
    qa_pass = qa is not None and qa.state == "pass"
    if campaign is None:
        if not implementation_pass:
            operational_state = "implementation-required"
            next_action = "Complete the approved implementation before material verification."
        elif material_required:
            operational_state = "verification-required"
            next_action = "Initialize the required material verification campaign."
        elif not qa_pass:
            operational_state = "qa-required"
            next_action = "Run the one existing independent QA gate."
        else:
            operational_state = "delivery-ready"
            next_action = "Use current delivery evidence; do not reopen unchanged proof."
        return {
            "operational_state": operational_state,
            "lifecycle": lifecycle,
            "campaign_required": material_required,
            "campaign_present": False,
            "campaign_current": None,
            "completed_stages": [],
            "missing_stages": required_stages,
            "required_scope": required_scope,
            "target_calls": 0,
            "elapsed_seconds": 0,
            "failures": 0,
            "qa_verdict": "pass" if qa_pass else "not-passed",
            "next_action": next_action,
            "reasons": [],
        }
    assert isinstance(campaign, dict)
    _verification_validate_campaign(campaign)
    current, currentness_reasons = _verification_campaign_currentness(
        root, target_id, state, campaign
    )
    raw_stages = campaign["stages"]
    assert isinstance(raw_stages, list)
    stages = [str(stage) for stage in raw_stages]
    completed = _verification_completed_stages(campaign)
    missing = [stage for stage in stages if stage not in completed]
    receipts = campaign["receipts"]
    assert isinstance(receipts, list)
    target_calls = sum(
        int(receipt["target_calls"]) for receipt in receipts if isinstance(receipt, dict)
    )
    elapsed_seconds = sum(
        int(receipt["elapsed_seconds"]) for receipt in receipts if isinstance(receipt, dict)
    )
    failures = sum(
        1
        for receipt in receipts
        if isinstance(receipt, dict) and receipt.get("outcome") == "product-failure"
    )
    campaign_outcome = str(campaign["outcome"])
    if not implementation_pass:
        operational_state = "implementation-required"
        next_action = "Complete the approved implementation; verifier invocation is not authorized."
    elif not current or campaign_outcome in {"blocked", "limit-reached"}:
        operational_state = "blocked"
        next_action = str(campaign["next_action"])
    elif campaign.get("mode") == "diagnostic":
        operational_state = "verification-required"
        next_action = (
            "Diagnostic evidence cannot certify delivery; initialize a current certification "
            "campaign after the named decision is resolved."
            if not missing
            else str(campaign["next_action"])
        )
    elif missing:
        operational_state = "verification-required"
        next_action = str(campaign["next_action"])
    elif not qa_pass:
        operational_state = "qa-required"
        next_action = "Run the one existing independent QA gate without broadening verification."
    else:
        operational_state = "delivery-ready"
        next_action = "Use current delivery evidence; do not rerun unchanged verification or QA."
    assert operational_state in VERIFICATION_OPERATIONAL_STATES
    return {
        "operational_state": operational_state,
        "lifecycle": lifecycle,
        "campaign_required": True,
        "campaign_present": True,
        "campaign_current": current,
        "candidate_identity": campaign["candidate_identity"],
        "mode": campaign["mode"],
        "certifying": campaign["mode"] == "certification",
        "campaign_outcome": campaign_outcome,
        "completed_stages": completed,
        "missing_stages": missing,
        "required_scope": campaign["affected_scope"],
        "limits": campaign["limits"],
        "target_calls": target_calls,
        "elapsed_seconds": elapsed_seconds,
        "failures": failures,
        "qa_verdict": "pass" if qa_pass else "not-passed",
        "next_action": next_action,
        "reasons": currentness_reasons,
    }


def _verification_adapter_required_capabilities(
    *, mode: str, stages: list[str], limits: Mapping[str, object]
) -> set[str]:
    required = {"request-binding", "typed-outcomes", "input-bound-receipts"}
    if any(stage in {"canary", "affected"} for stage in stages):
        required.add("selection")
    if mode == "certification":
        required.add("fail-fast")
    if any(value is not None for value in limits.values()):
        required.add("limits")
    return required


def _verification_recompute_campaign(campaign: dict[str, object]) -> None:
    completed = _verification_completed_stages(campaign)
    raw_stages = campaign["stages"]
    assert isinstance(raw_stages, list)
    stages = [str(stage) for stage in raw_stages]
    receipts = campaign["receipts"]
    assert isinstance(receipts, list)
    limits = campaign["limits"]
    assert isinstance(limits, dict)
    failures = sum(
        1
        for receipt in receipts
        if isinstance(receipt, dict) and receipt.get("outcome") == "product-failure"
    )
    target_calls = sum(
        int(receipt["target_calls"]) for receipt in receipts if isinstance(receipt, dict)
    )
    elapsed = sum(
        int(receipt["elapsed_seconds"]) for receipt in receipts if isinstance(receipt, dict)
    )
    limit_reasons: list[str] = []
    for key, actual in (
        ("max_failures", failures),
        ("max_target_calls", target_calls),
        ("max_elapsed_seconds", elapsed),
    ):
        maximum = limits.get(key)
        if maximum is not None and (
            actual > int(maximum) or (actual == int(maximum) and len(completed) < len(stages))
        ):
            limit_reasons.append(f"{key} reached or exceeded ({actual}/{maximum})")
    latest = receipts[-1] if receipts else None
    if isinstance(latest, dict) and latest.get("outcome") == "limit-reached":
        campaign["outcome"] = "limit-reached"
        campaign["next_action"] = (
            "Verifier limit reached with required proof still missing; record a current "
            "scope/limit decision. No pass is implied."
        )
    elif limit_reasons:
        campaign["outcome"] = "limit-reached"
        campaign["next_action"] = (
            "Campaign limit reached with required proof still missing: "
            + "; ".join(limit_reasons)
            + ". Record a current scope/limit decision; no pass is implied."
        )
    elif (
        isinstance(latest, dict)
        and latest.get("outcome") == "product-failure"
        and campaign["mode"] == "certification"
    ):
        campaign["outcome"] = "blocked"
        campaign["next_action"] = (
            "Return the blocking product/assertion failure to implementation; create a new "
            "candidate campaign after correction."
        )
    elif isinstance(latest, dict) and latest.get("outcome") == "evaluator-failure":
        campaign["outcome"] = "blocked"
        campaign["next_action"] = (
            "Repair the evaluator and regrade the retained target output with zero target calls."
        )
    elif isinstance(latest, dict) and latest.get("outcome") in {
        "provider-failure",
        "harness-failure",
    }:
        stage = latest.get("stage")
        infrastructure_failures = sum(
            1
            for receipt in receipts
            if isinstance(receipt, dict)
            and receipt.get("stage") == stage
            and receipt.get("outcome") in {"provider-failure", "harness-failure"}
        )
        if infrastructure_failures > 1:
            campaign["outcome"] = "blocked"
            campaign["next_action"] = (
                "The one bounded infrastructure retry is exhausted; repair or replan before "
                "further target execution."
            )
        else:
            campaign["outcome"] = "pending"
            campaign["next_action"] = (
                f"Resume {stage} once from the current checkpoint after infrastructure recovery."
            )
    elif len(completed) == len(stages):
        campaign["outcome"] = "pass"
        campaign["current_stage"] = None
        campaign["next_action"] = (
            "Diagnostic boundary reached; use the result only for the named decision."
            if campaign["mode"] == "diagnostic"
            else "Proceed to the one existing independent QA gate."
        )
    else:
        campaign["outcome"] = "pending"
        campaign["current_stage"] = next(stage for stage in stages if stage not in completed)
        campaign["next_action"] = f"Run only the current {campaign['current_stage']} stage."
    campaign["receipt_ledger_identity"] = _verification_receipt_ledger_identity(receipts)


def _coordination_verification_gate_issues(
    root: Path, target_id: str, *, new_status: str
) -> list[str]:
    try:
        path = _coordination_state_path(root, target_id)
    except ValueError:
        return []
    if not path.is_file():
        return []
    try:
        state = _coordination_load_state(root, target_id)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return [f"verification campaign state is invalid: {exc}"]
    campaign = state.get("verification_campaign")
    requirement = state.get("verification_requirement")
    if campaign is None and requirement is None:
        return []
    try:
        projection = _verification_campaign_projection(root, target_id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return [f"verification campaign state is invalid: {exc}"]
    operational_state = projection["operational_state"]
    if new_status == "Review" and operational_state not in {"qa-required", "delivery-ready"}:
        return [
            f"material verification is {operational_state}; complete the current campaign before QA"
        ]
    if new_status == "Complete" and operational_state != "delivery-ready":
        return [f"delivery is not ready because material verification is {operational_state}"]
    return []


def _coordination_transition_boundary(current_status: str, new_status: str) -> str | None:
    if current_status == new_status:
        return None
    if new_status == "In Progress":
        return "before-unit-start"
    if new_status == "Testing":
        return "unit-return-or-dependency-join"
    if new_status in {"Review", "Complete"}:
        return "before-review-or-complete"
    return None


def _coordination_csv(value: str | None, field_name: str) -> list[str]:
    if value is None:
        raise ValueError(f"--{field_name.replace('_', '-')} is required.")
    values = [item.strip() for item in value.split(",") if item.strip()]
    if not values:
        raise ValueError(f"--{field_name.replace('_', '-')} must not be empty.")
    return list(dict.fromkeys(values))


def _coordination_repository_sources(
    values: list[str] | None, source_revision: str
) -> dict[str, object]:
    if not values:
        return {".": {"source_revision": source_revision}}
    result: dict[str, object] = {}
    for raw in values:
        repository_id, separator, revision = raw.partition("=")
        if not separator or not repository_id.strip() or not revision.strip():
            raise ValueError("--repository-source must use REPOSITORY-ID=SOURCE-REVISION.")
        if repository_id.strip() in result:
            raise ValueError(f"Duplicate repository source: {repository_id.strip()}.")
        result[repository_id.strip()] = {"source_revision": revision.strip()}
    return result


def _verification_adapter_output_scope(
    adapter_output: Mapping[str, object],
    *,
    request: Mapping[str, object],
    request_binding: Mapping[str, object],
    campaign: Mapping[str, object],
) -> list[str]:
    scope = adapter_output.get(
        "scope", adapter_output.get("selected_scope", campaign["affected_scope"])
    )
    if (
        not isinstance(scope, list)
        or not scope
        or any(not isinstance(value, str) or not value.strip() for value in scope)
    ):
        raise ValueError("Adapter output scope must be a non-empty string list.")
    for field_name in (
        "request_identity",
        "candidate_identity",
        "source_identity",
        "proof_contract_identity",
        "stage",
        "outcome",
        "runtime_identity",
        "target_identity",
        "evaluator_identity",
        "artifact",
        "target_calls",
        "elapsed_seconds",
        "stage_complete",
    ):
        if field_name not in adapter_output:
            raise ValueError(f"Adapter output is missing {field_name}.")
    for field_name in request_binding:
        if adapter_output[field_name] != request[field_name]:
            raise ValueError(
                f"Adapter output {field_name} does not match the exact invocation request."
            )
    if adapter_output["outcome"] not in VERIFICATION_RECEIPT_OUTCOMES:
        raise ValueError("Adapter output outcome is invalid.")
    for field_name in (
        "runtime_identity",
        "target_identity",
        "evaluator_identity",
        "artifact",
    ):
        _coordination_required_text(adapter_output[field_name], f"adapter_output.{field_name}")
    for field_name in ("target_calls", "elapsed_seconds"):
        value = adapter_output[field_name]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"Adapter output {field_name} must be a non-negative integer.")
    if not isinstance(adapter_output["stage_complete"], bool):
        raise ValueError("Adapter output stage_complete must be boolean.")
    return [str(value) for value in scope]


def _execution_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _execution_string_list(value: object, field_name: str, *, empty: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"execution_control.{field_name} must be a string list.")
    values = [item.strip() for item in value]
    if any(not item for item in values):
        raise ValueError(f"execution_control.{field_name} contains an empty value.")
    if len(values) != len(set(values)):
        raise ValueError(f"execution_control.{field_name} contains duplicate values.")
    if not empty and not values:
        raise ValueError(f"execution_control.{field_name} must not be empty.")
    return values


def _execution_validate_relative_paths(value: object) -> list[str]:
    paths = _execution_string_list(value, "allowed_write_paths", empty=True)
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(
                "execution_control.allowed_write_paths must stay within the repository."
            )
    return paths


def _execution_validate_limits(value: object) -> dict[str, dict[str, object]]:
    if not isinstance(value, dict) or set(value) != set(EXECUTION_REQUIRED_LIMIT_UNITS):
        raise ValueError(
            "execution_control.limits must contain exactly: "
            + ", ".join(EXECUTION_REQUIRED_LIMIT_UNITS)
        )
    limits: dict[str, dict[str, object]] = {}
    for unit in EXECUTION_REQUIRED_LIMIT_UNITS:
        raw = value[unit]
        if not isinstance(raw, dict) or set(raw) != {
            "state",
            "maximum",
            "consumed",
            "native_unit",
            "source",
        }:
            raise ValueError(
                f"execution_control.limits.{unit} must contain state, maximum, consumed, "
                "native_unit, and source."
            )
        state = raw.get("state")
        if state not in EXECUTION_CAPABILITY_STATES:
            raise ValueError(f"execution_control.limits.{unit}.state is invalid.")
        maximum = raw.get("maximum")
        consumed = raw.get("consumed")
        if state == "verified":
            if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < 0:
                raise ValueError(
                    f"execution_control.limits.{unit}.maximum must be a finite "
                    "non-negative integer when verified."
                )
            if not isinstance(consumed, int) or isinstance(consumed, bool) or consumed < 0:
                raise ValueError(
                    f"execution_control.limits.{unit}.consumed must be a non-negative "
                    "integer when verified."
                )
        elif maximum is not None or consumed is not None:
            raise ValueError(
                f"execution_control.limits.{unit}.maximum and consumed must be null unless "
                "verified."
            )
        _coordination_required_text(raw.get("native_unit"), f"limits.{unit}.native_unit")
        _coordination_required_text(raw.get("source"), f"limits.{unit}.source")
        limits[unit] = dict(raw)
    return limits


def _execution_validate_authorized_findings(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        raise ValueError("execution_control.authorized_findings must be a list.")
    normalized: list[dict[str, object]] = []
    finding_ids: set[str] = set()
    required = {"id", "state", "material", "source_identity", "evidence_identity"}
    for raw in value:
        if not isinstance(raw, dict) or set(raw) != required:
            raise ValueError("execution_control.authorized_findings has an invalid shape.")
        finding_id = _coordination_required_text(raw.get("id"), "authorized_findings.id")
        if finding_id in finding_ids:
            raise ValueError("execution_control.authorized_findings contains a duplicate id.")
        if raw.get("state") not in {"unresolved", "resolved"}:
            raise ValueError("execution_control.authorized_findings.state is invalid.")
        if not isinstance(raw.get("material"), bool):
            raise ValueError("execution_control.authorized_findings.material must be boolean.")
        _coordination_required_text(
            raw.get("source_identity"), "authorized_findings.source_identity"
        )
        _coordination_required_text(
            raw.get("evidence_identity"), "authorized_findings.evidence_identity"
        )
        finding_ids.add(finding_id)
        normalized.append(dict(raw))
    return normalized


def _execution_validate_progress(
    value: object, authorized_findings: list[dict[str, object]]
) -> dict[str, object]:
    required = {
        "attempt",
        "finding_id",
        "baseline_source_identity",
        "baseline_evidence_identity",
        "current_source_identity",
        "current_evidence_identity",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("execution_control.progress has an invalid shape.")
    attempt = value.get("attempt")
    if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1:
        raise ValueError("execution_control.progress.attempt must be a positive integer.")
    for field_name in required - {"attempt"}:
        field_value = value.get(field_name)
        if field_value is not None and (
            not isinstance(field_value, str) or not field_value.strip()
        ):
            raise ValueError(f"execution_control.progress.{field_name} is invalid.")
    if attempt > 1:
        finding_id = _coordination_required_text(value.get("finding_id"), "progress.finding_id")
        matching = [
            finding
            for finding in authorized_findings
            if finding["id"] == finding_id
            and finding["state"] == "unresolved"
            and finding["material"] is True
        ]
        if len(matching) != 1:
            raise ValueError(
                "execution_control.progress repeat must name one sealed unresolved material "
                "finding."
            )
        source_changed = value.get("current_source_identity") != value.get(
            "baseline_source_identity"
        )
        evidence_changed = value.get("current_evidence_identity") != value.get(
            "baseline_evidence_identity"
        )
        if not source_changed and not evidence_changed:
            raise ValueError("execution_control.progress repeat has no changed source or evidence.")
    return dict(value)


def _execution_validate_candidate(
    value: object, field_name: str, required_fields: set[str]
) -> dict[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) != required_fields:
        raise ValueError(f"execution_control.candidates.{field_name} has an invalid shape.")
    for candidate_field in required_fields - {"obligations"}:
        _coordination_required_text(
            value.get(candidate_field), f"candidates.{field_name}.{candidate_field}"
        )
    return dict(value)


def _execution_validate_candidates(value: object) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != {
        "working_revision",
        "verification_candidate",
        "release_candidate",
    }:
        raise ValueError("execution_control.candidates has an invalid shape.")
    working_revision = _coordination_required_text(
        value.get("working_revision"), "candidates.working_revision"
    )
    verification = _execution_validate_candidate(
        value.get("verification_candidate"),
        "verification_candidate",
        {"identity", "source_revision", "proof_identity"},
    )
    release = _execution_validate_candidate(
        value.get("release_candidate"),
        "release_candidate",
        {"identity", "source_revision", "artifact_identity", "obligations"},
    )
    if release is not None:
        if verification is None or release["source_revision"] != verification["source_revision"]:
            raise ValueError(
                "execution_control release candidate must match a verification candidate."
            )
        obligations = release.get("obligations")
        required_obligations = {"implementation", "verification", "qa", "affected-proof"}
        if not isinstance(obligations, dict) or set(obligations) != required_obligations:
            raise ValueError("execution_control release obligations have an invalid shape.")
        for name in required_obligations:
            obligation = _coordination_required_text(
                obligations.get(name), f"candidates.release_candidate.obligations.{name}"
            )
            if not obligation.startswith("sha256:"):
                raise ValueError(
                    "execution_control release obligations must contain proof identities."
                )
    return {
        "working_revision": working_revision,
        "verification_candidate": verification,
        "release_candidate": release,
    }


def _execution_validate_capability(value: object) -> dict[str, object]:
    required = {
        "host",
        "version",
        "configuration_identity",
        "controls",
    }
    valid_fields = (required, required | {"settings"})
    if not isinstance(value, dict) or set(value) not in valid_fields:
        raise ValueError("execution_control.capability has an invalid shape.")
    _coordination_required_text(value.get("host"), "capability.host")
    _coordination_required_text(value.get("version"), "capability.version")
    _coordination_required_text(
        value.get("configuration_identity"), "capability.configuration_identity"
    )
    controls = value.get("controls")
    if not isinstance(controls, dict) or not set(EXECUTION_REQUIRED_CAPABILITY_CONTROLS).issubset(
        controls
    ):
        raise ValueError("execution_control.capability.controls is missing a binding control.")
    normalized_controls: dict[str, dict[str, str]] = {}
    for control_name, raw in controls.items():
        if not isinstance(raw, dict) or set(raw) != {"state", "unit", "source"}:
            raise ValueError(
                f"execution_control.capability.controls.{control_name} has an invalid shape."
            )
        if raw.get("state") not in EXECUTION_CAPABILITY_STATES:
            raise ValueError(
                f"execution_control.capability.controls.{control_name}.state is invalid."
            )
        unit = _coordination_required_text(
            raw.get("unit"), f"capability.controls.{control_name}.unit"
        )
        source = _coordination_required_text(
            raw.get("source"), f"capability.controls.{control_name}.source"
        )
        normalized_controls[control_name] = {
            "state": str(raw["state"]),
            "unit": unit,
            "source": source,
        }
    settings = value.get("settings")
    if settings is not None:
        if not isinstance(settings, dict):
            raise ValueError("execution_control.capability.settings must be an object.")
        try:
            json.dumps(settings, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "execution_control.capability.settings must be canonical JSON."
            ) from exc
        if value.get("configuration_identity") != _execution_hash(settings):
            raise ValueError(
                "execution_control capability configuration identity is stale or malformed."
            )
    normalized: dict[str, object] = {
        "host": str(value["host"]),
        "version": str(value["version"]),
        "configuration_identity": str(value["configuration_identity"]),
        "controls": normalized_controls,
    }
    if settings is not None:
        normalized["settings"] = _execution_copy(settings)
    return normalized


def _execution_validate_receipt(value: object, work_id: str) -> dict[str, object]:
    required = {
        "schema_version",
        "kind",
        "work_id",
        "sealed_identity",
        "capability_identity",
        "phase",
        "candidate_identity",
        "proof_obligations_identity",
        "source_revision",
        "operation",
        "outcome",
        "native_metrics",
        "evidence_identity",
        "receipt_identity",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("execution_control receipt has an invalid shape.")
    if value.get("schema_version") != EXECUTION_CONTROL_SCHEMA_VERSION:
        raise ValueError("execution_control receipt schema_version is invalid.")
    if value.get("work_id") != work_id:
        raise ValueError("execution_control receipt work_id does not match the envelope.")
    for field_name in (
        "kind",
        "sealed_identity",
        "capability_identity",
        "phase",
        "candidate_identity",
        "proof_obligations_identity",
        "source_revision",
        "operation",
        "evidence_identity",
    ):
        _coordination_required_text(value.get(field_name), f"receipt.{field_name}")
    if value.get("outcome") not in EXECUTION_RECEIPT_OUTCOMES:
        raise ValueError("execution_control receipt outcome is invalid.")
    native_metrics = value.get("native_metrics")
    if not isinstance(native_metrics, dict):
        raise ValueError("execution_control receipt native_metrics must be an object.")
    expected_identity = _execution_hash(
        {key: item for key, item in value.items() if key != "receipt_identity"}
    )
    if value.get("receipt_identity") != expected_identity:
        raise ValueError("execution_control receipt identity is stale or malformed.")
    return dict(value)


def _execution_sealed_payload(value: Mapping[str, object]) -> dict[str, object]:
    return {
        key: value[key]
        for key in (
            "schema_version",
            "work_id",
            "source_revision",
            "phase",
            "allowed_write_paths",
            "permitted_operations",
            "proof_obligations",
            "limits",
            "authorized_findings",
            "capability",
        )
    }


def _execution_validate_control(value: object, *, work_id: str) -> dict[str, object]:
    required = {
        "schema_version",
        "work_id",
        "source_revision",
        "phase",
        "allowed_write_paths",
        "permitted_operations",
        "proof_obligations",
        "limits",
        "authorized_findings",
        "progress",
        "candidates",
        "capability",
        "receipts",
        "sealed_identity",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("execution_control has an invalid shape.")
    if value.get("schema_version") != EXECUTION_CONTROL_SCHEMA_VERSION:
        raise ValueError("execution_control schema_version is invalid.")
    if value.get("work_id") != work_id:
        raise ValueError("execution_control work_id does not match the workflow item.")
    source_revision = _coordination_required_text(
        value.get("source_revision"), "execution_control.source_revision"
    )
    if value.get("phase") not in EXECUTION_PHASES:
        raise ValueError("execution_control phase is invalid.")
    allowed_write_paths = _execution_validate_relative_paths(value.get("allowed_write_paths"))
    permitted_operations = _execution_string_list(
        value.get("permitted_operations"), "permitted_operations"
    )
    if any(operation not in EXECUTION_MATERIAL_OPERATIONS for operation in permitted_operations):
        raise ValueError("execution_control.permitted_operations contains an unknown operation.")
    proof_obligations = _execution_string_list(value.get("proof_obligations"), "proof_obligations")
    limits = _execution_validate_limits(value.get("limits"))
    authorized_findings = _execution_validate_authorized_findings(value.get("authorized_findings"))
    progress = _execution_validate_progress(value.get("progress"), authorized_findings)
    candidates = _execution_validate_candidates(value.get("candidates"))
    if candidates["working_revision"] != source_revision:
        raise ValueError("execution_control working revision does not match sealed source.")
    verification_candidate = candidates.get("verification_candidate")
    if isinstance(verification_candidate, dict) and (
        verification_candidate.get("source_revision") != source_revision
    ):
        raise ValueError("execution_control verification candidate is stale.")
    capability = _execution_validate_capability(value.get("capability"))
    receipts = value.get("receipts")
    if not isinstance(receipts, list):
        raise ValueError("execution_control.receipts must be a list.")
    normalized_receipts = [_execution_validate_receipt(receipt, work_id) for receipt in receipts]
    sealed_identity = str(value.get("sealed_identity"))
    capability_identity = _execution_hash(capability)
    proof_obligations_identity = _execution_hash(proof_obligations)
    candidate_identities = {str(candidates["working_revision"])}
    for candidate_name in ("verification_candidate", "release_candidate"):
        candidate = candidates.get(candidate_name)
        if isinstance(candidate, dict):
            candidate_identities.add(str(candidate["identity"]))
    for receipt in normalized_receipts:
        if receipt["sealed_identity"] != sealed_identity:
            raise ValueError("execution_control receipt does not match the sealed envelope.")
        if receipt["capability_identity"] != capability_identity:
            raise ValueError("execution_control receipt does not match host capability.")
        if receipt["phase"] != value["phase"]:
            raise ValueError("execution_control receipt does not match the sealed phase.")
        if receipt["candidate_identity"] not in candidate_identities:
            raise ValueError("execution_control receipt does not match a sealed candidate.")
        if receipt["proof_obligations_identity"] != proof_obligations_identity:
            raise ValueError("execution_control receipt does not match proof obligations.")
    if any(receipt["source_revision"] != source_revision for receipt in normalized_receipts):
        raise ValueError("execution_control receipt source does not match sealed source.")
    if any(receipt["operation"] not in permitted_operations for receipt in normalized_receipts):
        raise ValueError("execution_control receipt operation was not permitted.")
    expected_identity = _execution_hash(_execution_sealed_payload(value))
    if value.get("sealed_identity") != expected_identity:
        raise ValueError("execution_control sealed identity is stale or malformed.")
    return {
        **value,
        "allowed_write_paths": allowed_write_paths,
        "permitted_operations": permitted_operations,
        "proof_obligations": proof_obligations,
        "limits": limits,
        "authorized_findings": authorized_findings,
        "progress": progress,
        "candidates": candidates,
        "capability": capability,
        "receipts": normalized_receipts,
    }


def _execution_effective_consumed(control: Mapping[str, object], unit: str) -> int:
    limits = control["limits"]
    assert isinstance(limits, dict)
    detail = limits[unit]
    assert isinstance(detail, dict)
    declared = int(detail["consumed"])
    receipts = control["receipts"]
    assert isinstance(receipts, list)
    observed = 0
    for receipt in receipts:
        if not isinstance(receipt, dict):
            continue
        metrics = receipt.get("native_metrics")
        if not isinstance(metrics, dict):
            continue
        value = metrics.get(unit)
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            observed += value
    return declared + observed


EXECUTION_QA_SCHEMA_VERSION = 1

FIXED_RELEASE_SCHEMA_VERSION = 1

EXECUTION_QA_STATES = {"findings-open", "ready-for-promotion", "blocked"}

FIXED_RELEASE_OPERATION_KINDS = {"build", "package", "verify", "publish", "tag", "deploy"}

FIXED_RELEASE_FORBIDDEN_TERMS = {
    "candidate-create",
    "candidate-promote",
    "fix-source",
    "qa",
    "repair",
    "review",
}


def _execution_copy(value: Mapping[str, object]) -> dict[str, object]:
    copied: object = json.loads(json.dumps(value))
    if not isinstance(copied, dict):
        raise ValueError("execution value must serialize to a JSON object")
    return {str(key): nested for key, nested in copied.items()}


def _execution_validate_qa_campaign(value: object, work_id: str) -> dict[str, object]:
    required = {
        "schema_version",
        "work_id",
        "source_revision",
        "verdict_identity",
        "broad_qa_invocations",
        "findings",
        "remediation_attempts",
        "state",
        "campaign_identity",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("execution_qa has an invalid shape.")
    if value.get("schema_version") != EXECUTION_QA_SCHEMA_VERSION:
        raise ValueError("execution_qa schema_version is invalid.")
    if value.get("work_id") != work_id:
        raise ValueError("execution_qa work_id does not match the workflow item.")
    for field_name in ("source_revision", "verdict_identity"):
        _coordination_required_text(value.get(field_name), f"execution_qa.{field_name}")
    if value.get("broad_qa_invocations") != 1:
        raise ValueError("execution_qa must retain exactly one broad QA invocation.")
    findings = value.get("findings")
    if not isinstance(findings, list) or not findings:
        raise ValueError("execution_qa.findings must contain at least one finding.")
    normalized_findings: list[dict[str, object]] = []
    finding_ids: set[str] = set()
    finding_fields = {
        "id",
        "severity",
        "material",
        "scope",
        "source_identity",
        "evidence_identity",
        "state",
        "correction_identity",
        "affected_proof_identity",
    }
    for raw in findings:
        if not isinstance(raw, dict) or set(raw) != finding_fields:
            raise ValueError("execution_qa finding has an invalid shape.")
        finding_id = _coordination_required_text(raw.get("id"), "execution_qa.finding.id")
        if finding_id in finding_ids:
            raise ValueError("execution_qa contains a duplicate finding id.")
        finding_ids.add(finding_id)
        if raw.get("severity") not in {"low", "medium", "high", "critical"}:
            raise ValueError("execution_qa finding severity is invalid.")
        if raw.get("material") is not True:
            raise ValueError("execution_qa may authorize only material findings.")
        _execution_validate_relative_paths(raw.get("scope"))
        for identity_field in ("source_identity", "evidence_identity"):
            _coordination_required_text(
                raw.get(identity_field), f"execution_qa.finding.{identity_field}"
            )
        state = raw.get("state")
        if state not in {"unresolved", "resolved", "blocked"}:
            raise ValueError("execution_qa finding state is invalid.")
        for optional_field in ("correction_identity", "affected_proof_identity"):
            optional_value = raw.get(optional_field)
            if optional_value is not None:
                _coordination_required_text(
                    optional_value, f"execution_qa.finding.{optional_field}"
                )
        if state == "resolved" and (
            raw.get("correction_identity") is None or raw.get("affected_proof_identity") is None
        ):
            raise ValueError(
                "execution_qa resolved finding requires correction and affected proof."
            )
        normalized_findings.append(dict(raw))
    attempts = value.get("remediation_attempts")
    if not isinstance(attempts, list):
        raise ValueError("execution_qa.remediation_attempts must be a list.")
    normalized_attempts: list[dict[str, object]] = []
    attempt_fields = {
        "finding_id",
        "baseline_source_identity",
        "baseline_evidence_identity",
        "current_source_identity",
        "current_evidence_identity",
        "authority_receipt_identity",
        "receipt_identity",
    }
    for raw in attempts:
        if not isinstance(raw, dict) or set(raw) != attempt_fields:
            raise ValueError("execution_qa remediation attempt has an invalid shape.")
        if raw.get("finding_id") not in finding_ids:
            raise ValueError("execution_qa remediation names an unknown finding.")
        for field_name in attempt_fields - {"receipt_identity"}:
            _coordination_required_text(raw.get(field_name), f"remediation.{field_name}")
        expected = _execution_hash(
            {key: item for key, item in raw.items() if key != "receipt_identity"}
        )
        if raw.get("receipt_identity") != expected:
            raise ValueError("execution_qa remediation receipt is stale or malformed.")
        normalized_attempts.append(dict(raw))
    derived_state = (
        "blocked"
        if any(finding["state"] == "blocked" for finding in normalized_findings)
        else (
            "ready-for-promotion"
            if all(finding["state"] == "resolved" for finding in normalized_findings)
            else "findings-open"
        )
    )
    if value.get("state") != derived_state or derived_state not in EXECUTION_QA_STATES:
        raise ValueError("execution_qa state does not match finding dispositions.")
    campaign_payload = {key: item for key, item in value.items() if key != "campaign_identity"}
    if value.get("campaign_identity") != _execution_hash(campaign_payload):
        raise ValueError("execution_qa campaign identity is stale or malformed.")
    return {
        **value,
        "findings": normalized_findings,
        "remediation_attempts": normalized_attempts,
    }


def _execution_create_qa_campaign(
    *, work_id: str, source_revision: str, verdict_identity: str, findings: list[dict[str, object]]
) -> dict[str, object]:
    campaign: dict[str, object] = {
        "schema_version": EXECUTION_QA_SCHEMA_VERSION,
        "work_id": work_id,
        "source_revision": source_revision,
        "verdict_identity": verdict_identity,
        "broad_qa_invocations": 1,
        "findings": findings,
        "remediation_attempts": [],
        "state": "findings-open",
        "campaign_identity": "pending",
    }
    campaign["campaign_identity"] = _execution_hash(
        {key: item for key, item in campaign.items() if key != "campaign_identity"}
    )
    return _execution_validate_qa_campaign(campaign, work_id)


def _execution_scope_within_envelope(scope: list[str], allowed_write_paths: list[str]) -> bool:
    return all(
        any(fnmatch.fnmatchcase(path, pattern) for pattern in allowed_write_paths) for path in scope
    )


def _execution_record_remediation(
    campaign: Mapping[str, object],
    control: Mapping[str, object],
    *,
    finding_id: str,
    current_source_identity: str,
    current_evidence_identity: str,
) -> dict[str, object]:
    normalized_campaign = _execution_validate_qa_campaign(campaign, str(control["work_id"]))
    normalized_control = _execution_validate_control(control, work_id=str(control["work_id"]))
    if normalized_campaign["source_revision"] != normalized_control["source_revision"]:
        raise ValueError("remediation QA campaign does not match sealed source authority.")
    if normalized_control["phase"] != "qa-remediation":
        raise ValueError("remediation requires the sealed qa-remediation phase.")
    permitted_operations = normalized_control["permitted_operations"]
    assert isinstance(permitted_operations, list)
    if "qa-remediation" not in permitted_operations:
        raise ValueError("remediation is absent from permitted operations.")
    limits = normalized_control["limits"]
    assert isinstance(limits, dict)
    exhausted = [
        name
        for name, detail in limits.items()
        if isinstance(detail, dict)
        and detail.get("state") == "verified"
        and _execution_effective_consumed(normalized_control, name) >= int(detail["maximum"])
    ]
    if exhausted:
        raise ValueError("remediation authority is exhausted: " + ", ".join(sorted(exhausted)))
    findings = normalized_campaign["findings"]
    assert isinstance(findings, list)
    matching = [
        finding
        for finding in findings
        if finding["id"] == finding_id and finding["state"] == "unresolved"
    ]
    if len(matching) != 1:
        raise ValueError("remediation requires one unresolved authorized finding.")
    finding = matching[0]
    authorized = normalized_control["authorized_findings"]
    assert isinstance(authorized, list)
    if not any(
        item["id"] == finding_id
        and item["state"] == "unresolved"
        and item["material"] is True
        and item["source_identity"] == finding["source_identity"]
        and item["evidence_identity"] == finding["evidence_identity"]
        for item in authorized
    ):
        raise ValueError("remediation finding is not sealed into execution authority.")
    scope = finding["scope"]
    allowed = normalized_control["allowed_write_paths"]
    assert isinstance(scope, list) and isinstance(allowed, list)
    if not _execution_scope_within_envelope(scope, allowed):
        raise ValueError("remediation finding is outside the sealed write scope.")
    baseline_source = str(finding["source_identity"])
    baseline_evidence = str(finding["evidence_identity"])
    if (
        current_source_identity == baseline_source
        and current_evidence_identity == baseline_evidence
    ):
        raise ValueError("remediation made no material source or evidence progress.")
    updated = _execution_copy(normalized_campaign)
    attempts = updated["remediation_attempts"]
    assert isinstance(attempts, list)
    if any(existing.get("finding_id") == finding_id for existing in attempts):
        raise ValueError("remediation finding already consumed its single affected attempt.")
    receipts = normalized_control["receipts"]
    assert isinstance(receipts, list)
    authority_receipts = [
        receipt
        for receipt in receipts
        if receipt["kind"] == "remediation"
        and receipt["operation"] == "qa-remediation"
        and receipt["outcome"] == "pass"
        and receipt["source_revision"] == current_source_identity
        and receipt["evidence_identity"] == current_evidence_identity
    ]
    if len(authority_receipts) != 1:
        raise ValueError(
            "remediation requires one passing input-bound remediation receipt for current proof."
        )
    attempt: dict[str, object] = {
        "finding_id": finding_id,
        "baseline_source_identity": baseline_source,
        "baseline_evidence_identity": baseline_evidence,
        "current_source_identity": current_source_identity,
        "current_evidence_identity": current_evidence_identity,
        "authority_receipt_identity": authority_receipts[0]["receipt_identity"],
        "receipt_identity": "pending",
    }
    attempt["receipt_identity"] = _execution_hash(
        {key: item for key, item in attempt.items() if key != "receipt_identity"}
    )
    if any(
        existing.get("receipt_identity") == attempt["receipt_identity"] for existing in attempts
    ):
        raise ValueError("identical remediation repeat is denied.")
    attempts.append(attempt)
    updated["campaign_identity"] = _execution_hash(
        {key: item for key, item in updated.items() if key != "campaign_identity"}
    )
    return _execution_validate_qa_campaign(updated, str(control["work_id"]))


def _execution_close_finding(
    campaign: Mapping[str, object],
    control: Mapping[str, object],
    *,
    finding_id: str,
    correction_identity: str,
    affected_proof_identity: str,
) -> dict[str, object]:
    work_id = str(campaign.get("work_id", ""))
    normalized = _execution_validate_qa_campaign(campaign, work_id)
    normalized_control = _execution_validate_control(control, work_id=work_id)
    if normalized["source_revision"] != normalized_control["source_revision"]:
        raise ValueError("affected proof does not match sealed source authority.")
    attempts = normalized["remediation_attempts"]
    assert isinstance(attempts, list)
    matching_attempts = [attempt for attempt in attempts if attempt["finding_id"] == finding_id]
    if len(matching_attempts) != 1:
        raise ValueError("finding cannot close without a remediation receipt.")
    attempt = matching_attempts[0]
    if correction_identity != attempt["authority_receipt_identity"]:
        raise ValueError("finding correction does not match its input-bound remediation receipt.")
    receipts = normalized_control["receipts"]
    assert isinstance(receipts, list)
    affected_receipts = [
        receipt
        for receipt in receipts
        if receipt["receipt_identity"] == affected_proof_identity
        and receipt["kind"] == "affected-proof"
        and receipt["operation"] == "qa-remediation"
        and receipt["outcome"] == "pass"
        and receipt["source_revision"] == attempt["current_source_identity"]
    ]
    if len(affected_receipts) != 1:
        raise ValueError("finding closure requires one passing input-bound affected-proof receipt.")
    updated = _execution_copy(normalized)
    findings = updated["findings"]
    assert isinstance(findings, list)
    matching = [finding for finding in findings if finding["id"] == finding_id]
    if len(matching) != 1 or matching[0]["state"] != "unresolved":
        raise ValueError("finding is not open for affected-proof closure.")
    matching[0]["state"] = "resolved"
    matching[0]["correction_identity"] = _coordination_required_text(
        correction_identity, "correction_identity"
    )
    matching[0]["affected_proof_identity"] = _coordination_required_text(
        affected_proof_identity, "affected_proof_identity"
    )
    updated["state"] = (
        "ready-for-promotion"
        if all(finding["state"] == "resolved" for finding in findings)
        else "findings-open"
    )
    updated["campaign_identity"] = _execution_hash(
        {key: item for key, item in updated.items() if key != "campaign_identity"}
    )
    return _execution_validate_qa_campaign(updated, work_id)


def _execution_promote_release_candidate(
    root: Path,
    target_id: str,
    coordination: Mapping[str, object],
    *,
    artifact_identity: str,
) -> dict[str, object]:
    artifact_identity = _coordination_required_text(artifact_identity, "artifact_identity")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", artifact_identity):
        raise ValueError("release promotion requires a content-addressed artifact identity.")
    campaign = _execution_validate_qa_campaign(coordination.get("execution_qa"), target_id)
    if campaign["state"] != "ready-for-promotion":
        raise ValueError("release promotion requires every QA finding and affected proof closed.")
    verification = _verification_campaign_projection(root, target_id, coordination)
    if verification["operational_state"] != "delivery-ready":
        raise ValueError(
            "release promotion requires current delivery-ready verification and QA authority."
        )
    control = _execution_validate_control(coordination.get("execution_control"), work_id=target_id)
    if campaign["source_revision"] != control["source_revision"] or (
        control["source_revision"] != coordination.get("source_revision")
    ):
        raise ValueError("release promotion requires current QA and coordinated source authority.")
    receipts = control["receipts"]
    assert isinstance(receipts, list)
    receipt_ids = {receipt["receipt_identity"] for receipt in receipts}
    findings = campaign["findings"]
    assert isinstance(findings, list)
    if any(
        finding["correction_identity"] not in receipt_ids
        or finding["affected_proof_identity"] not in receipt_ids
        for finding in findings
    ):
        raise ValueError("release promotion requires input-bound QA remediation proof receipts.")
    candidates = control["candidates"]
    assert isinstance(candidates, dict)
    existing = candidates.get("release_candidate")
    source_revision = str(control["source_revision"])
    candidate_identity = _execution_hash(
        {
            "work_id": target_id,
            "source_revision": source_revision,
            "artifact_identity": artifact_identity,
            "qa_campaign_identity": campaign["campaign_identity"],
            "verification_candidate": candidates.get("verification_candidate"),
        }
    )
    if isinstance(existing, dict):
        if existing.get("identity") == candidate_identity:
            return control
        raise ValueError("a different release candidate is already promoted.")
    updated = _execution_copy(control)
    updated_candidates = updated["candidates"]
    assert isinstance(updated_candidates, dict)
    _, proof_layers = _verification_work_item_layers(root, target_id)
    implementation_layer = proof_layers.get("implementation")
    qa_layer = proof_layers.get("qa-review")
    if implementation_layer is None or qa_layer is None:
        raise ValueError("release promotion requires implementation and QA proof layers.")
    verification_campaign = coordination.get("verification_campaign")
    verification_identity = _execution_hash(
        verification_campaign
        if isinstance(verification_campaign, dict)
        else {"required": False, "source_revision": source_revision}
    )
    updated_candidates["release_candidate"] = {
        "identity": candidate_identity,
        "source_revision": source_revision,
        "artifact_identity": artifact_identity,
        "obligations": {
            "implementation": _execution_hash(asdict(implementation_layer)),
            "verification": verification_identity,
            "qa": _execution_hash(
                {"layer": asdict(qa_layer), "verdict_identity": campaign["verdict_identity"]}
            ),
            "affected-proof": _execution_hash(
                [finding["affected_proof_identity"] for finding in findings]
            ),
        },
    }
    return _execution_validate_control(updated, work_id=target_id)


def _execution_file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _execution_validate_fixed_release(value: object, work_id: str) -> dict[str, object]:
    required = {
        "schema_version",
        "work_id",
        "candidate_identity",
        "source_revision",
        "artifacts",
        "operations",
        "elapsed_limit_seconds",
        "infrastructure_retry_limit",
        "attempt",
        "terminal_receipt",
        "plan_identity",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("fixed_release has an invalid shape.")
    if value.get("schema_version") != FIXED_RELEASE_SCHEMA_VERSION:
        raise ValueError("fixed_release schema_version is invalid.")
    if value.get("work_id") != work_id:
        raise ValueError("fixed_release work_id does not match the workflow item.")
    for field_name in ("candidate_identity", "source_revision"):
        _coordination_required_text(value.get(field_name), f"fixed_release.{field_name}")
    artifacts = value.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("fixed_release.artifacts must be a non-empty object.")
    for raw_path, identity in artifacts.items():
        _execution_validate_relative_paths([raw_path])
        _coordination_required_text(identity, f"fixed_release.artifacts.{raw_path}")
    operations = value.get("operations")
    if not isinstance(operations, list) or not operations:
        raise ValueError("fixed_release.operations must not be empty.")
    operation_names: set[str] = set()
    operation_fields = {"name", "kind", "argv", "timeout_seconds", "infrastructure_exit_codes"}
    for operation in operations:
        if not isinstance(operation, dict) or set(operation) != operation_fields:
            raise ValueError("fixed_release operation has an invalid shape.")
        name = _coordination_required_text(operation.get("name"), "fixed_release.operation.name")
        if name in operation_names:
            raise ValueError("fixed_release contains a duplicate operation name.")
        operation_names.add(name)
        if operation.get("kind") not in FIXED_RELEASE_OPERATION_KINDS:
            raise ValueError("fixed_release operation kind is not release-safe.")
        argv = _execution_string_list(operation.get("argv"), "fixed_release.operation.argv")
        normalized_tokens = {Path(token).name.lower() for token in argv}
        normalized_tokens.add(name.lower())
        if any(
            term in token for term in FIXED_RELEASE_FORBIDDEN_TERMS for token in normalized_tokens
        ):
            raise ValueError("fixed_release operation requests repair, QA, or candidate authority.")
        timeout = operation.get("timeout_seconds")
        if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0:
            raise ValueError("fixed_release operation timeout must be a positive integer.")
        exit_codes = operation.get("infrastructure_exit_codes")
        if not isinstance(exit_codes, list) or any(
            not isinstance(code, int) or isinstance(code, bool) or code == 0 for code in exit_codes
        ):
            raise ValueError("fixed_release infrastructure exit codes are invalid.")
    elapsed_limit = value.get("elapsed_limit_seconds")
    if not isinstance(elapsed_limit, int) or isinstance(elapsed_limit, bool) or elapsed_limit <= 0:
        raise ValueError("fixed_release elapsed limit must be a positive integer.")
    if value.get("infrastructure_retry_limit") != 1:
        raise ValueError("fixed_release permits exactly one unchanged-input infrastructure retry.")
    attempt = value.get("attempt")
    if not isinstance(attempt, dict) or set(attempt) != {
        "state",
        "operation_invocations",
        "infrastructure_retries",
    }:
        raise ValueError("fixed_release.attempt has an invalid shape.")
    if attempt.get("state") not in {"not-started", "running", "terminal"}:
        raise ValueError("fixed_release.attempt.state is invalid.")
    attempt_invocations = attempt.get("operation_invocations")
    if not isinstance(attempt_invocations, dict) or any(
        name not in operation_names
        or not isinstance(count, int)
        or isinstance(count, bool)
        or count < 0
        or count > 2
        for name, count in attempt_invocations.items()
    ):
        raise ValueError("fixed_release.attempt operation invocations are invalid.")
    attempt_retries = attempt.get("infrastructure_retries")
    if (
        not isinstance(attempt_retries, int)
        or isinstance(attempt_retries, bool)
        or attempt_retries < 0
        or attempt_retries > 1
    ):
        raise ValueError("fixed_release.attempt infrastructure retries are invalid.")
    receipt = value.get("terminal_receipt")
    if attempt["state"] == "not-started" and (
        receipt is not None or attempt_invocations or attempt_retries != 0
    ):
        raise ValueError("fixed_release not-started attempt contains consumed authority.")
    if attempt["state"] == "running" and receipt is not None:
        raise ValueError("fixed_release running attempt cannot contain a terminal receipt.")
    if attempt["state"] == "terminal" and not isinstance(receipt, dict):
        raise ValueError("fixed_release terminal attempt requires a typed receipt.")
    expected = _execution_hash(
        {
            key: item
            for key, item in value.items()
            if key not in {"plan_identity", "terminal_receipt", "attempt"}
        }
    )
    if value.get("plan_identity") != expected:
        raise ValueError("fixed_release plan identity is stale or malformed.")
    if isinstance(receipt, dict):
        _execution_validate_fixed_release_receipt(receipt, value)
        if receipt["operation_invocations"] != attempt_invocations or (
            receipt["infrastructure_retries"] != attempt_retries
        ):
            raise ValueError("fixed_release terminal receipt does not match consumed authority.")
    return _execution_copy(value)


def _execution_validate_fixed_release_receipt(
    value: object, plan: Mapping[str, object]
) -> dict[str, object]:
    required = {
        "schema_version",
        "work_id",
        "candidate_identity",
        "plan_identity",
        "status",
        "reason",
        "operation_invocations",
        "infrastructure_retries",
        "qa_invocations",
        "source_repairs",
        "replacement_candidates",
        "receipt_identity",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("fixed_release terminal receipt has an invalid shape.")
    if value.get("schema_version") != FIXED_RELEASE_SCHEMA_VERSION:
        raise ValueError("fixed_release terminal receipt schema_version is invalid.")
    for field_name in ("work_id", "candidate_identity", "plan_identity"):
        if value.get(field_name) != plan.get(field_name):
            raise ValueError(f"fixed_release terminal receipt {field_name} is not input-bound.")
    if value.get("status") not in {"pass", "fail"}:
        raise ValueError("fixed_release terminal receipt status is invalid.")
    _coordination_required_text(value.get("reason"), "fixed_release.terminal_receipt.reason")
    raw_operations = plan["operations"]
    assert isinstance(raw_operations, list)
    operation_names = {
        str(operation["name"]) for operation in raw_operations if isinstance(operation, dict)
    }
    invocations = value.get("operation_invocations")
    if not isinstance(invocations, dict) or any(
        name not in operation_names
        or not isinstance(count, int)
        or isinstance(count, bool)
        or count < 0
        or count > 2
        for name, count in invocations.items()
    ):
        raise ValueError("fixed_release terminal receipt invocations are invalid.")
    if value["status"] == "pass" and (
        set(invocations) != operation_names or any(count < 1 for count in invocations.values())
    ):
        raise ValueError("fixed_release passing receipt did not consume every operation.")
    retries = value.get("infrastructure_retries")
    if retries != sum(max(0, count - 1) for count in invocations.values()) or retries not in {
        0,
        1,
    }:
        raise ValueError("fixed_release terminal receipt retry count is invalid.")
    for field_name in ("qa_invocations", "source_repairs", "replacement_candidates"):
        if value.get(field_name) != 0:
            raise ValueError("fixed_release terminal receipt contains prohibited authority.")
    expected = _execution_hash(
        {key: item for key, item in value.items() if key != "receipt_identity"}
    )
    if value.get("receipt_identity") != expected:
        raise ValueError("fixed_release terminal receipt identity is stale or malformed.")
    return dict(value)


def _execution_verify_fixed_candidate(root: Path, plan: Mapping[str, object]) -> None:
    git_head = _operational_git_optional(["rev-parse", "HEAD"], root)
    if git_head is None:
        raise ValueError("fixed release requires readable Git source identity.")
    if git_head != plan["source_revision"]:
        raise ValueError("fixed release source revision changed.")
    changed = _operational_git_optional(["status", "--porcelain"], root)
    if changed is None:
        raise ValueError("fixed release requires readable Git worktree status.")
    coordination_paths = {
        path.relative_to(root).as_posix()
        for path in (root / ".project-workflow" / "tasks").rglob(
            f"{plan['work_id']}-*/{COORDINATION_FILENAME}"
        )
    }
    material_changes = [
        line
        for line in changed.splitlines()
        if line[3:].strip().strip('"') not in coordination_paths
    ]
    if material_changes:
        raise ValueError("fixed release candidate worktree is dirty.")
    artifacts = plan["artifacts"]
    assert isinstance(artifacts, dict)
    for raw_path, expected in artifacts.items():
        path = root / str(raw_path)
        if not path.is_file() or _execution_file_sha256(path) != expected:
            raise ValueError(f"fixed release artifact changed: {raw_path}")


def _execution_run_fixed_release(
    root: Path,
    value: Mapping[str, object],
    persist: Callable[[dict[str, object]], None],
) -> tuple[dict[str, object], dict[str, object]]:
    work_id = str(value.get("work_id", ""))
    plan = _execution_validate_fixed_release(value, work_id)
    attempt = plan["attempt"]
    assert isinstance(attempt, dict)
    if attempt["state"] != "not-started":
        raise ValueError("fixed release attempt is already consumed and cannot be retried.")
    running = _execution_copy(plan)
    running_attempt = running["attempt"]
    assert isinstance(running_attempt, dict)
    running_attempt["state"] = "running"
    persist(running)
    started = time.monotonic()
    status = "pass"
    reason = "Every fixed-candidate release operation completed against unchanged inputs."
    try:
        _execution_verify_fixed_candidate(root, running)
        operations = running["operations"]
        assert isinstance(operations, list)
        elapsed_limit_seconds = running["elapsed_limit_seconds"]
        assert isinstance(elapsed_limit_seconds, int)
        for operation in operations:
            assert isinstance(operation, dict)
            name = str(operation["name"])
            invocations = running_attempt["operation_invocations"]
            assert isinstance(invocations, dict)
            invocations[name] = 0
            while True:
                if time.monotonic() - started >= elapsed_limit_seconds:
                    raise ValueError("fixed release elapsed authority exhausted.")
                _execution_verify_fixed_candidate(root, running)
                invocations[name] += 1
                if invocations[name] > 2:
                    raise ValueError("fixed release operation authority exhausted.")
                persist(running)
                completed = subprocess.run(
                    [str(part) for part in operation["argv"]],
                    cwd=root,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=int(operation["timeout_seconds"]),
                )
                _execution_verify_fixed_candidate(root, running)
                if completed.returncode == 0:
                    break
                infrastructure_codes = operation["infrastructure_exit_codes"]
                assert isinstance(infrastructure_codes, list)
                if completed.returncode in infrastructure_codes and invocations[name] == 1:
                    running_attempt["infrastructure_retries"] = 1
                    continue
                raise ValueError(
                    f"fixed release operation {name} failed with {completed.returncode}."
                )
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        status = "fail"
        reason = str(exc)
    invocations = running_attempt["operation_invocations"]
    assert isinstance(invocations, dict)
    retries = int(running_attempt["infrastructure_retries"])
    receipt: dict[str, object] = {
        "schema_version": FIXED_RELEASE_SCHEMA_VERSION,
        "work_id": work_id,
        "candidate_identity": running["candidate_identity"],
        "plan_identity": running["plan_identity"],
        "status": status,
        "reason": reason,
        "operation_invocations": invocations,
        "infrastructure_retries": retries,
        "qa_invocations": 0,
        "source_repairs": 0,
        "replacement_candidates": 0,
        "receipt_identity": "pending",
    }
    receipt["receipt_identity"] = _execution_hash(
        {key: item for key, item in receipt.items() if key != "receipt_identity"}
    )
    running["terminal_receipt"] = receipt
    running_attempt["state"] = "terminal"
    persist(running)
    return _execution_validate_fixed_release(running, work_id), receipt


def _execution_operation_class(operation: str) -> str:
    if operation in EXECUTION_DIRECT_OPERATIONS:
        return "direct"
    if operation in EXECUTION_MATERIAL_OPERATIONS:
        return "controlled"
    raise ValueError(f"Unknown execution operation: {operation}")


def _execution_blocked_payload(
    target_id: str, operation: str, reason: str, next_action: str
) -> dict[str, object]:
    return {
        "schema_version": EXECUTION_CONTROL_SCHEMA_VERSION,
        "target_id": target_id,
        "operation": operation,
        "route": "controlled",
        "state": "blocked",
        "reason": reason,
        "next_action": next_action,
        "model_invocations": 0,
        "mutated": False,
        "executed": False,
    }


def _execution_control_projection(root: Path, target_id: str, operation: str) -> dict[str, object]:
    route = _execution_operation_class(operation)
    if route == "direct":
        return {
            "schema_version": EXECUTION_CONTROL_SCHEMA_VERSION,
            "target_id": target_id,
            "operation": operation,
            "route": "direct",
            "state": "ready",
            "reason": "Direct read-only or cheap deterministic work needs no envelope.",
            "next_action": "Run the direct operation without launching an adapter.",
            "model_invocations": 0,
            "mutated": False,
            "executed": False,
        }
    try:
        coordination = _coordination_load_state(root, target_id)
        coordination_preflight = _coordination_preflight_payload(root, target_id, coordination)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return _execution_blocked_payload(
            target_id,
            operation,
            f"coordination-invalid: {exc}",
            f"Initialize or repair current coordination state for {target_id}.",
        )
    if coordination_preflight["contract_state"] not in {"current", "compatible"}:
        return _execution_blocked_payload(
            target_id,
            operation,
            "coordination-contract-stale",
            "Explicitly load and declare the current coordination contract.",
        )
    raw_control = coordination.get("execution_control")
    if raw_control is None:
        command = "project release" if operation == "release" else "project execute"
        return _execution_blocked_payload(
            target_id,
            operation,
            "execution-control-not-configured",
            f"Seal current execution authority and retry `{command} --id {target_id}`.",
        )
    try:
        control = _execution_validate_control(raw_control, work_id=target_id)
    except ValueError as exc:
        return _execution_blocked_payload(
            target_id,
            operation,
            f"execution-control-invalid: {exc}",
            "Repair and reseal the current execution authority before material work.",
        )
    if control["source_revision"] != coordination["source_revision"]:
        return _execution_blocked_payload(
            target_id,
            operation,
            "execution-source-stale",
            "Create a successor envelope for the current coordinated source.",
        )
    git_head = _operational_git_optional(["rev-parse", "HEAD"], root)
    if git_head is not None and git_head != control["source_revision"]:
        return _execution_blocked_payload(
            target_id,
            operation,
            "execution-source-not-current-git-head",
            "Refresh coordination and create a successor envelope for the current Git source.",
        )
    permitted_operations = control["permitted_operations"]
    assert isinstance(permitted_operations, list)
    if operation not in permitted_operations:
        return _execution_blocked_payload(
            target_id,
            operation,
            "operation-not-permitted",
            "Return to the Coordinator for the currently permitted material action.",
        )
    capability = control["capability"]
    assert isinstance(capability, dict)
    capability_inspection: dict[str, object] | None = None
    settings = capability.get("settings")
    if settings is not None:
        host = capability.get("host")
        if host == "codex":
            try:
                from project_workflow.codex_adapter import inspect_codex_capability
            except ModuleNotFoundError:
                from codex_adapter import inspect_codex_capability  # type: ignore

            capability_inspection = inspect_codex_capability(settings)
            host_label = "Codex"
        elif host == "claude-code":
            try:
                from project_workflow.claude_adapter import inspect_claude_capability
            except ModuleNotFoundError:
                from claude_adapter import inspect_claude_capability  # type: ignore

            capability_inspection = inspect_claude_capability(settings)
            host_label = "Claude Code"
        else:
            return _execution_blocked_payload(
                target_id,
                operation,
                "execution-adapter-settings-host-mismatch",
                "Configure settings only for a packaged host adapter.",
            )
        if capability_inspection["state"] != "inspectable":
            return _execution_blocked_payload(
                target_id,
                operation,
                f"{host}-capability-unavailable: " + str(capability_inspection["reason"]),
                f"Repair the sealed {host_label} executable, trust, or adapter settings.",
            )
        if capability.get("version") != settings.get("expected_version"):
            return _execution_blocked_payload(
                target_id,
                operation,
                f"{host}-capability-declaration-stale",
                f"Reseal the adapter capability for the expected {host_label} version.",
            )
    controls = capability["controls"]
    assert isinstance(controls, dict)
    capability_gaps = [
        name
        for name, detail in controls.items()
        if not isinstance(detail, dict) or detail.get("state") != "verified"
    ]
    limits = control["limits"]
    assert isinstance(limits, dict)
    limit_gaps = [
        name
        for name, detail in limits.items()
        if not isinstance(detail, dict) or detail.get("state") != "verified"
    ]
    if capability_gaps or limit_gaps:
        gaps = capability_gaps + limit_gaps
        return _execution_blocked_payload(
            target_id,
            operation,
            "binding-capability-gap: " + ", ".join(sorted(gaps)),
            "Install or repair one supported host adapter for every binding control.",
        )
    exhausted_limits = [
        name
        for name, detail in limits.items()
        if isinstance(detail, dict)
        and detail.get("state") == "verified"
        and _execution_effective_consumed(control, name) >= int(detail["maximum"])
    ]
    if exhausted_limits:
        return _execution_blocked_payload(
            target_id,
            operation,
            "execution-limit-exhausted: " + ", ".join(sorted(exhausted_limits)),
            "Return to the Coordinator with required proof still visibly incomplete.",
        )
    if operation == "release":
        candidates = control["candidates"]
        assert isinstance(candidates, dict)
        if candidates.get("release_candidate") is None:
            return _execution_blocked_payload(
                target_id,
                operation,
                "release-candidate-not-promoted",
                "Complete implementation, verification, QA, and affected proof first.",
            )
        verification = _verification_campaign_projection(root, target_id, coordination)
        if verification["operational_state"] != "delivery-ready":
            return _execution_blocked_payload(
                target_id,
                operation,
                "release-authority-not-current: " + str(verification["operational_state"]),
                str(verification["next_action"]),
            )
        campaign = coordination.get("verification_campaign")
        verification_candidate = candidates.get("verification_candidate")
        if isinstance(campaign, dict) and (
            not isinstance(verification_candidate, dict)
            or verification_candidate.get("identity") != campaign.get("candidate_identity")
            or verification_candidate.get("proof_identity")
            != campaign.get("proof_contract_identity")
        ):
            return _execution_blocked_payload(
                target_id,
                operation,
                "release-candidate-not-bound-to-current-verification",
                "Promote only the exact current verification campaign candidate.",
            )
    payload: dict[str, object] = {
        "schema_version": EXECUTION_CONTROL_SCHEMA_VERSION,
        "target_id": target_id,
        "operation": operation,
        "route": "controlled",
        "state": "inspectable" if capability_inspection is not None else "preflight-ready",
        "reason": (
            "The sealed host executable is inspectable; runtime hook and interruption controls "
            "remain unverified until exact dispatch."
            if capability_inspection is not None
            else "Current sealed authority and binding host capability are valid."
        ),
        "next_action": (
            "Dispatch this exact control to probe the runtime contract and run only if verified."
            if capability_inspection is not None
            else "Dispatch this exact preflight through the verified host adapter."
        ),
        "source_revision": control["source_revision"],
        "sealed_identity": control["sealed_identity"],
        "candidate": control["candidates"],
        "capability": control["capability"],
        "model_invocations": 0,
        "mutated": False,
        "executed": False,
    }
    if capability_inspection is not None:
        payload["capability_inspection"] = capability_inspection
    return payload


def _print_execution_projection(payload: dict[str, object], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(f"Execution preflight: {payload['target_id']}")
    print(f"Route: {payload['route']}")
    print(f"State: {payload['state']}")
    print(f"Reason: {payload['reason']}")
    print("Model invocations: 0")
    print(f"Next action: {payload['next_action']}")


def _cmd_execution_preflight(args: argparse.Namespace, operation: str) -> None:
    payload = _execution_control_projection(Path.cwd(), args.id, operation)
    _print_execution_projection(payload, args.format)
    if payload["state"] == "blocked":
        raise SystemExit(2)


def _execution_qa_projection(value: object, work_id: str) -> dict[str, object] | None:
    if value is None:
        return None
    campaign = _execution_validate_qa_campaign(value, work_id)
    state = str(campaign["state"])
    next_action = {
        "findings-open": "Continue only named sealed findings through affected proof.",
        "ready-for-promotion": "Promote the exact current source and artifact candidate once.",
        "blocked": "Return the precise unresolved finding blocker to the Coordinator.",
    }[state]
    findings = campaign["findings"]
    assert isinstance(findings, list)
    return {
        "state": state,
        "broad_qa_invocations": 1,
        "open_findings": [finding["id"] for finding in findings if finding["state"] != "resolved"],
        "next_action": next_action,
        "campaign_identity": campaign["campaign_identity"],
    }


def _execution_fixed_release_projection(
    root: Path, value: object, work_id: str
) -> dict[str, object] | None:
    if value is None:
        return None
    plan = _execution_validate_fixed_release(value, work_id)
    receipt = plan["terminal_receipt"]
    if isinstance(receipt, dict):
        return {
            "state": "terminal-pass" if receipt.get("status") == "pass" else "terminal-fail",
            "next_action": "Do not retry or create a replacement candidate.",
            "receipt_identity": receipt.get("receipt_identity"),
        }
    try:
        _execution_verify_fixed_candidate(root, plan)
    except ValueError as exc:
        return {
            "state": "blocked",
            "next_action": str(exc),
            "receipt_identity": None,
        }
    return {
        "state": "ready",
        "next_action": "Run the predeclared fixed release operations once.",
        "receipt_identity": None,
    }


def _coordination_status_payload(root: Path, target_id: str) -> dict[str, object]:
    state = _coordination_load_state(root, target_id)
    preflight = _coordination_preflight_payload(root, target_id, state)
    next_action = str(state["next_action"])
    if preflight["contract_state"] not in {"current", "compatible"}:
        next_action = "Explicitly load and declare the applicable context contract."
    campaign = state.get("verification_campaign")
    verification = (
        _verification_campaign_projection(root, target_id, state)
        if campaign is not None or state.get("verification_requirement") is not None
        else None
    )
    execution = (
        _execution_control_projection(root, target_id, "material-execution")
        if state.get("execution_control") is not None
        else None
    )
    qa_campaign = _execution_qa_projection(state.get("execution_qa"), target_id)
    fixed_release = _execution_fixed_release_projection(root, state.get("fixed_release"), target_id)
    if isinstance(qa_campaign, dict) and qa_campaign["state"] != "ready-for-promotion":
        next_action = str(qa_campaign["next_action"])
    elif isinstance(fixed_release, dict):
        next_action = str(fixed_release["next_action"])
    elif isinstance(execution, dict):
        next_action = str(execution["next_action"])
    return {
        "schema_version": COORDINATION_SCHEMA_VERSION,
        "target_id": target_id,
        "contract_state": preflight["contract_state"],
        "phase": state["phase"],
        "source_revision": state["source_revision"],
        "repositories": state["repositories"],
        "decisions": state["decisions"],
        "last_boundary": state["last_boundary"],
        "boundary_decisions": state["boundary_decisions"],
        "host_facts": state["host_facts"],
        "outcome_checkpoint": state["outcome_checkpoint"],
        "verification": verification,
        "execution": execution,
        "qa_campaign": qa_campaign,
        "fixed_release": fixed_release,
        "next_action": next_action,
        "source": _delegation_relative_path(root, _coordination_state_path(root, target_id)),
    }


def _epic_lifecycle_gate_issues(root: Path, epic_id: str, target_status: str) -> list[str]:
    workflow_dir = root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    epic_dir = _resolve_epic_dir(tasks_dir, epic_id)
    requirements_path = epic_dir / "REQUIREMENTS.md"
    if target_status == "Complete":
        return ["use `epic closeout --epic-id <EPIC-ID> --complete` to mark an epic Complete"]
    if target_status == "Analysing":
        return []
    if not requirements_path.exists():
        return [f"missing epic requirements file: {requirements_path}"]
    requirements_text = requirements_path.read_text(encoding="utf-8")
    readiness_issues = _epic_requirements_readiness_issues(requirements_text)
    approval_issues = _approval_envelope_issues(
        requirements_text,
        require_decomposition=True,
    )
    contract_issues = _epic_contract_issues(epic_dir, requirements_text)
    if target_status == "Ready":
        audit_issues = (
            _intent_audit_gate_issues(epic_dir)
            if _decomposition_plan_path(epic_dir).exists()
            else []
        )
        return [*readiness_issues, *approval_issues, *contract_issues, *audit_issues]

    epic_dir, audit_rows, audit_gaps = _epic_audit_rows(root, epic_id)
    mapping_gaps = [
        f"{row['Parent AC']}: no mapped child rows"
        for row in audit_rows
        if row["Child Rows"] == "None" and row["Deferral"] == "None"
    ]
    if target_status == "In Progress":
        return [
            *readiness_issues,
            *approval_issues,
            *contract_issues,
            *mapping_gaps,
            *_intent_audit_gate_issues(epic_dir),
            *_coordination_boundary_gate_issues(
                root,
                epic_id,
                boundary="after-plan-or-decomposition",
            ),
        ]
    if target_status == "Closeout":
        return [*audit_gaps, *_epic_retro_issues(epic_dir)]
    return [f"unsupported epic lifecycle status: {target_status}"]


def _update_global_tracker_row_status(
    *,
    root: Path,
    tracker_path: Path,
    row_id: str,
    new_status: str,
    force: bool,
    reason: str | None,
) -> tuple[str, str]:
    normalized_row_id = _normalize_task_status_id(row_id, root=root)

    if new_status not in TRACKER_STATUSES:
        raise SystemExit(
            f"Invalid target status '{new_status}'. Allowed: {', '.join(TRACKER_STATUSES)}."
        )

    _validate_status_force_args(new_status=new_status, force=force, reason=reason)

    lines, _header_idx, rows = _global_tracker_rows(tracker_path)
    for row in rows:
        if row["ID"] != normalized_row_id:
            continue

        current_status = row["Status"]
        if current_status not in TRACKER_STATUSES:
            raise SystemExit(
                f"{row_id} has unknown current status '{current_status}'. "
                f"Allowed: {', '.join(TRACKER_STATUSES)}."
            )

        docs_rel = _clean_markdown_cell_path(row["Docs"])
        if not docs_rel:
            raise SystemExit(f"{row_id} has no docs path in {tracker_path}.")
        docs_path = root / ".project-workflow" / docs_rel
        if not docs_path.exists():
            raise SystemExit(f"{row_id} docs path does not exist: {docs_path}")

        docs_text = docs_path.read_text(encoding="utf-8")
        requirements_path = docs_path.parent / "REQUIREMENTS.md"
        requirements_text = (
            requirements_path.read_text(encoding="utf-8") if requirements_path.exists() else ""
        )
        if new_status == "Testing":
            testing_issues = _task_testing_integrity_issues(docs_text)
            if testing_issues:
                raise SystemExit(_format_readiness_block(row_id, list(testing_issues)))
        if new_status == "Analysing" and not force and not _is_discovery_work(requirements_text):
            approval_issues = _approval_envelope_issues(
                requirements_text,
                require_implementation=True,
            )
            if approval_issues:
                raise SystemExit(_format_readiness_block(row_id, approval_issues))
        if new_status in {"Review", "Complete"}:
            structured_issues = _structured_evidence_issues(
                requirements_path=requirements_path,
                implementation_path=docs_path,
                include_explicit_nonpassing=True,
            )
            if structured_issues:
                raise SystemExit(_format_readiness_block(row_id, structured_issues))
            repository_issues = _repository_evidence_issues(
                root,
                requirements_text,
                docs_text,
            )
            if repository_issues:
                raise SystemExit(_format_readiness_block(row_id, repository_issues))
        if new_status == "Complete":
            if current_status != "Review":
                raise SystemExit(
                    f"{row_id} can only move to Complete from Review; "
                    f"current status is '{current_status}'."
                )
            if _legacy_adoption_evidence_untrusted(requirements_text):
                raise SystemExit(
                    f"{row_id} cannot move to Complete because legacy adoption marks "
                    "pre-adoption evidence as untrusted; refresh evidence or re-adopt with "
                    "--evidence-refreshed."
                )
            if not _has_qa_review_evidence(
                docs_text,
                requirements_text=requirements_text,
            ):
                raise SystemExit(
                    f"{row_id} cannot move to Complete without non-placeholder "
                    "QA/code-review evidence."
                )
            intent_qa_issues = _intent_qa_review_issues(docs_text)
            if intent_qa_issues:
                raise SystemExit(_format_readiness_block(row_id, intent_qa_issues))
            owner_acceptance_issues = _owner_acceptance_completion_issues(
                docs_path.parent / STRUCTURED_EVIDENCE_FILENAME
            )
            if owner_acceptance_issues:
                raise SystemExit(_format_readiness_block(row_id, owner_acceptance_issues))

        if not _status_transition_allowed(current_status, new_status):
            if not force:
                raise SystemExit(
                    f"Illegal status transition for {row_id}: "
                    f"{current_status} -> {new_status}. "
                    "Use --force --reason for audited non-Complete exceptions."
                )

        if _status_requires_task_readiness(new_status) and not force:
            if not _is_discovery_work(requirements_text, docs_text):
                approval_issues = _approval_envelope_issues(
                    requirements_text,
                    require_implementation=True,
                )
                if approval_issues:
                    raise SystemExit(_format_readiness_block(row_id, approval_issues))
            readiness_issues = _task_ready_issues_for_paths(
                requirements_path=requirements_path,
                implementation_path=docs_path,
            )
            if readiness_issues:
                raise SystemExit(_format_readiness_block(row_id, readiness_issues))

        boundary = _coordination_transition_boundary(current_status, new_status)
        if boundary is not None and not force:
            coordination_issues = _coordination_boundary_gate_issues(
                root,
                normalized_row_id,
                boundary=boundary,
                subject_id=normalized_row_id,
            )
            if new_status == "In Progress":
                coordination_issues.extend(
                    _coordination_checkpoint_gate_issues(
                        root,
                        normalized_row_id,
                        subject_id=normalized_row_id,
                    )
                )
            if coordination_issues:
                raise SystemExit(_format_readiness_block(row_id, coordination_issues))
        if new_status in {"Review", "Complete"} and not force:
            verification_issues = _coordination_verification_gate_issues(
                root, normalized_row_id, new_status=new_status
            )
            if verification_issues:
                raise SystemExit(_format_readiness_block(row_id, verification_issues))

        if current_status == new_status:
            return current_status, new_status

        row["Status"] = new_status
        line_idx = int(row["_line_idx"])
        lines[line_idx] = _format_global_tracker_row(row)
        tracker_path.write_text("".join(lines), encoding="utf-8")
        return current_status, new_status

    raise SystemExit(f"No global tracker row found for ID '{row_id}' in {tracker_path}.")


def _update_epic_child_status(
    *,
    root: Path,
    epic_tracker_path: Path,
    row_id: str,
    new_status: str,
    force: bool,
    reason: str | None,
) -> tuple[str, str]:
    _validate_status_force_args(new_status=new_status, force=force, reason=reason)
    epic_name_parts = epic_tracker_path.parent.name.split("-", 2)
    epic_id = "-".join(epic_name_parts[:2]) if len(epic_name_parts) >= 2 else ""
    lines, _header_idx, rows = _epic_tracker_rows(epic_tracker_path)
    for row in rows:
        if row["ID"] != row_id:
            continue
        current_status = row["Status"]
        if current_status not in EPIC_TRACKER_STATUSES:
            raise SystemExit(
                f"{row_id} has invalid current status '{current_status}'. "
                f"Allowed: {', '.join(EPIC_TRACKER_STATUSES)}."
            )
        if new_status not in EPIC_TRACKER_STATUSES:
            raise SystemExit(
                f"Invalid target status '{new_status}'. "
                f"Allowed: {', '.join(EPIC_TRACKER_STATUSES)}."
            )
        if new_status == "Testing":
            docs_rel = _clean_markdown_cell_path(row.get("Docs", ""))
            if not docs_rel:
                raise SystemExit(f"{row_id} cannot move to Testing without a docs path.")
            docs_path = root / ".project-workflow" / docs_rel
            if not docs_path.exists():
                raise SystemExit(f"{row_id} docs path does not exist: {docs_path}")
            testing_issues = _task_testing_integrity_issues(docs_path.read_text(encoding="utf-8"))
            if testing_issues:
                raise SystemExit(_format_readiness_block(row_id, list(testing_issues)))
        if not force and not _epic_status_transition_allowed(current_status, new_status):
            raise SystemExit(
                f"Illegal epic status transition for {row_id}: "
                f"{current_status} -> {new_status}. Use --force --reason for audited "
                "non-Complete exceptions."
            )
        if new_status == "Complete":
            if current_status != "Review":
                raise SystemExit(
                    f"{row_id} can only move to Complete from Review; "
                    f"current status is {current_status}."
                )
            docs_rel = _clean_markdown_cell_path(row.get("Docs", ""))
            if not docs_rel:
                raise SystemExit(f"{row_id} cannot move to Complete without a docs path.")
            docs_path = root / ".project-workflow" / docs_rel
            if not docs_path.exists():
                raise SystemExit(f"{row_id} docs path does not exist: {docs_path}")
            docs_text = docs_path.read_text(encoding="utf-8")
            parent_ac_ids = _extract_ac_ids(_extract_parent_ac_coverage(row))
            requirements_path = docs_path.parent / "REQUIREMENTS.md"
            if requirements_path.exists():
                readiness_issues = _task_ready_issues_for_paths(
                    requirements_path=requirements_path,
                    implementation_path=docs_path,
                    parent_ac_ids=parent_ac_ids,
                )
                if readiness_issues:
                    raise SystemExit(_format_readiness_block(row_id, readiness_issues))
            structured_issues = _structured_evidence_issues(
                requirements_path=requirements_path,
                implementation_path=docs_path,
                parent_ac_ids=parent_ac_ids,
                include_explicit_nonpassing=True,
            )
            if structured_issues:
                raise SystemExit(_format_readiness_block(row_id, structured_issues))
            owner_acceptance_issues = _owner_acceptance_completion_issues(
                docs_path.parent / STRUCTURED_EVIDENCE_FILENAME
            )
            if owner_acceptance_issues:
                raise SystemExit(_format_readiness_block(row_id, owner_acceptance_issues))
            requirements_text = (
                requirements_path.read_text(encoding="utf-8") if requirements_path.exists() else ""
            )
            repository_issues = _repository_evidence_issues(
                root,
                requirements_text,
                docs_text,
            )
            if repository_issues:
                raise SystemExit(_format_readiness_block(row_id, repository_issues))
            if not _has_qa_review_evidence(
                docs_text,
                requirements_text=requirements_text,
            ):
                raise SystemExit(
                    f"{row_id} cannot move to Complete without non-placeholder "
                    "QA/code-review evidence."
                )
            intent_qa_issues = _intent_qa_review_issues(docs_text)
            if intent_qa_issues:
                raise SystemExit(_format_readiness_block(row_id, intent_qa_issues))
            missing_parent_evidence = [
                ac_id
                for ac_id in sorted(parent_ac_ids)
                if not _parent_ac_evidence_present(docs_text, ac_id)
            ]
            if missing_parent_evidence:
                raise SystemExit(
                    f"{row_id} cannot move to Complete without parent AC evidence for: "
                    + ", ".join(missing_parent_evidence)
                )
        if current_status == new_status:
            return current_status, new_status
        if (
            _status_requires_epic_child_readiness(new_status)
            and not force
            and new_status != "Complete"
        ):
            docs_rel = _clean_markdown_cell_path(row.get("Docs", ""))
            if not docs_rel:
                raise SystemExit(f"{row_id} cannot move to {new_status} without a docs path.")
            docs_path = root / ".project-workflow" / docs_rel
            requirements_path = docs_path.parent / "REQUIREMENTS.md"
            parent_ac_ids = _extract_ac_ids(_extract_parent_ac_coverage(row))
            readiness_issues = _task_ready_issues_for_paths(
                requirements_path=requirements_path,
                implementation_path=docs_path,
                parent_ac_ids=parent_ac_ids,
            )
            if new_status == "Review":
                readiness_issues.extend(
                    _structured_evidence_issues(
                        requirements_path=requirements_path,
                        implementation_path=docs_path,
                        parent_ac_ids=parent_ac_ids,
                        include_explicit_nonpassing=True,
                    )
                )
                requirements_text = requirements_path.read_text(encoding="utf-8")
                implementation_text = docs_path.read_text(encoding="utf-8")
                readiness_issues.extend(
                    _repository_evidence_issues(
                        root,
                        requirements_text,
                        implementation_text,
                    )
                )
            if readiness_issues:
                raise SystemExit(_format_readiness_block(row_id, readiness_issues))
        boundary = _coordination_transition_boundary(current_status, new_status)
        if boundary is not None and not force and epic_id:
            coordination_issues = _coordination_boundary_gate_issues(
                root,
                epic_id,
                boundary=boundary,
                subject_id=row_id,
            )
            if new_status == "In Progress":
                coordination_issues.extend(
                    _coordination_checkpoint_gate_issues(
                        root,
                        epic_id,
                        subject_id=row_id,
                    )
                )
            if coordination_issues:
                raise SystemExit(_format_readiness_block(row_id, coordination_issues))
        if new_status in {"Review", "Complete"} and not force:
            verification_issues = _coordination_verification_gate_issues(
                root, row_id, new_status=new_status
            )
            if verification_issues:
                raise SystemExit(_format_readiness_block(row_id, verification_issues))
        row["Status"] = new_status
        lines[int(row["_line_idx"])] = _format_epic_tracker_row(row)
        epic_tracker_path.write_text("".join(lines), encoding="utf-8")
        return current_status, new_status

    raise SystemExit(f"No epic tracker row found for ID '{row_id}' in {epic_tracker_path}.")
