"""Canonical Project Workflow commands runtime."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import date
from pathlib import Path

from .contracts import (
    AGENT_CHOICES,
    BACKLOG_PRIORITIES,
    BACKLOG_STATUSES,
    BACKLOG_TYPES,
    CANONICAL_INIT_COMMAND,
    CANONICAL_UPGRADE_COMMAND,
    CODEX_SKILL_NAMES,
    COORDINATION_SCHEMA_VERSION,
    DELEGATION_CAPABILITIES,
    EPIC_AMENDMENTS_FILENAME,
    EPIC_CHILD_GATED_STATUSES,
    EPIC_CONTRACT_FILENAME,
    EPIC_ID_PREFIX,
    EXECUTION_CONTROL_SCHEMA_VERSION,
    FIX_ID_PREFIX,
    PROMPT_FILES,
    STRUCTURED_EVIDENCE_FILENAME,
    VERIFICATION_ADAPTER_CAPABILITIES,
    VERIFICATION_CAMPAIGN_MODES,
    VERIFICATION_CAMPAIGN_SCHEMA_VERSION,
    VERIFICATION_CAMPAIGN_STAGES,
    VERIFICATION_RECEIPT_OUTCOMES,
    WORKFLOW_CONFIG_FILENAME,
    WORKFLOW_MANIFEST_FILENAME,
    TaskSpec,
)
from .coordination import (
    _coordination_artifact_identity,
    _coordination_boundary_gate_issues,
    _coordination_csv,
    _coordination_load_state,
    _coordination_preflight_payload,
    _coordination_repository_sources,
    _coordination_required_text,
    _coordination_source_identity,
    _coordination_state_path,
    _coordination_status_payload,
    _coordination_write_state,
    _epic_lifecycle_gate_issues,
    _execution_control_projection,
    _execution_copy,
    _execution_hash,
    _execution_run_fixed_release,
    _execution_validate_control,
    _execution_validate_fixed_release,
    _print_execution_projection,
    _update_epic_child_status,
    _update_global_tracker_row_status,
    _verification_adapter_output_scope,
    _verification_adapter_required_capabilities,
    _verification_campaign_currentness,
    _verification_campaign_projection,
    _verification_completed_stages,
    _verification_identity,
    _verification_optional_limit,
    _verification_receipt_ledger_identity,
    _verification_recompute_campaign,
    _verification_validate_campaign,
)
from .inspection import (
    _accepted_doctor_warning_fingerprints,
    _doctor_json_payload,
    _evaluate_doctor,
    _format_doctor_issue,
    build_operational_status_snapshot,
    inspect_operational_status_repository,
    operational_status_payload,
    render_operational_status_human,
    run_doctor,
)
from .lifecycle import (
    _append_backlog_row,
    _append_epic_tracker_rows,
    _approval_envelope_issues,
    _backlog_path,
    _backlog_rows,
    _backlog_rows_for_update,
    _backlog_validation_issues,
    _classify_task_prefix,
    _decompose_epic_requirements_to_titles,
    _discovery_readiness_issues,
    _ensure_backlog_file,
    _epic_audit_rows,
    _epic_child_implementation_template,
    _epic_child_requirements_template,
    _epic_closeout_summary,
    _epic_requirements_readiness_issues,
    _epic_retro_issues,
    _epic_tracker_row_by_id,
    _epic_tracker_rows,
    _fix_closeout_issues,
    _fix_non_delivery_closeout_issues,
    _fix_triage_issues,
    _format_acceptance_audit,
    _format_epic_tracker_row,
    _format_global_tracker_row,
    _format_intent_approval_summary,
    _format_intent_audit_human,
    _format_readiness_block,
    _global_tracker_rows,
    _intent_audit_evaluation,
    _intent_audit_gate_issues,
    _intent_audit_path,
    _intent_audit_template,
    _intent_contract_mode,
    _intent_plain_text,
    _is_discovery_work,
    _next_backlog_id,
    _next_task_id_from_used,
    _next_workflow_id,
    _normalize_backlog_value,
    _operational_status_artifact,
    _operational_work_item_paths,
    _requirements_approval_issues_for_path,
    _requirements_readiness_issues,
    _requirements_with_approval_envelope,
    _requirements_with_backlog_source,
    _requirements_with_legacy_adoption,
    _resolve_epic_child_docs,
    _resolve_epic_dir,
    _resolve_epic_id,
    _resolve_fix_doc,
    _resolve_global_task_docs,
    _structured_evidence_template,
    _task_ready_issues_for_paths,
    _update_backlog_row,
    _update_epic_tracker_row_status,
    _update_fix_tracker_status,
    _update_global_epic_status,
    _update_tracker,
    _upsert_markdown_section,
    _used_ids_for_prefix,
    _validation_impact_decision,
    _validation_impact_identity,
    _validation_impact_section,
    _write_acceptance_map,
)
from .maintenance import (
    _apply_repository_upgrade_plan,
    _apply_smoke_bomb_plan,
    _build_repository_upgrade_plan,
    _build_smoke_bomb_plan,
    _format_smoke_bomb_plan_human,
    _format_smoke_bomb_result_human,
    _format_upgrade_apply_human,
    _format_upgrade_plan_human,
)
from .orchestration import (
    DelegationPlanError,
    EpicOrchestrationError,
    TaskOrchestrationError,
    _delegation_error,
    _delegation_plan_from_args,
    _delegation_relative_path,
    _delegation_runtime_path,
    _delegation_status_payload,
    _format_delegation_plan_human,
    _load_delegation_runtime_state,
    _write_delegation_runtime_state,
    delegation_plan_payload,
    initialize_delegation_runtime_state,
    reconcile_delegation_runtime_state,
)
from .repository import (
    _append_epic_amendment_row,
    _approval_source_invalid,
    _backlog_template,
    _branch_exists,
    _current_workflow_manifest,
    _decomposition_plan_path,
    _ensure_clean_git,
    _ensure_delegation_runtime_ignore,
    _ensure_generated_file,
    _ensure_managed_block,
    _ensure_user_config_file,
    _ensure_user_guidance_file,
    _epic_amendments_path,
    _epic_amendments_template,
    _epic_contract_issues,
    _epic_contract_issues_for_path,
    _epic_contract_template,
    _epic_deferrals_template,
    _epic_retro_template,
    _epic_tracker_template,
    _extract_ac_ids,
    _extract_parent_ac_coverage,
    _extract_parent_ac_ids_from_epic_rows,
    _extract_parent_ac_ids_from_requirements,
    _fix_template,
    _format_child_charter_from_contract,
    _format_decomposition_plan,
    _get_package_resource,
    _implementation_template,
    _load_workflow_config,
    _managed_project_workflow_block,
    _normalize_ac_list,
    _normalize_fix_id,
    _normalize_task_status_id,
    _prompt_filename_to_claude_agent_name,
    _prompt_filename_to_cursor_agent_name,
    _proposed_child_work_rows,
    _remove_retired_project_workflow_path,
    _replace_fix_field,
    _repository_compatibility,
    _require_decomposition_plan_authority,
    _requirements_template,
    _resolve_task_id_prefix,
    _run_git,
    _to_claude_agent_markdown,
    _to_cursor_agent_markdown,
    _tracker_template,
    _valid_workflow_ref_id,
    _write_file,
    _write_workflow_manifest,
    slug_kebab_lower,
    slug_titlecase_dashes,
)


def cmd_status(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve() if args.root else Path.cwd()
    snapshot = build_operational_status_snapshot(
        root,
        strict=args.strict,
        focus_id=args.id,
        repository_id=args.repository,
    )
    if args.format == "json":
        print(json.dumps(operational_status_payload(snapshot), indent=2))
    else:
        print(render_operational_status_human(snapshot), end="")


def cmd_validation_impact(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve() if args.root else Path.cwd()
    inspection = inspect_operational_status_repository(root)
    matches = tuple(item for item in inspection.active_work if item.item_id == args.id)
    if not matches:
        raise SystemExit(f"Active operational state contains no work item named '{args.id}'.")
    if len(matches) > 1:
        raise SystemExit(f"Active operational state contains duplicate ID '{args.id}'.")
    item = matches[0]
    requirements_path, implementation_path, _epic_dir = _operational_work_item_paths(root, item)
    if implementation_path is None or not implementation_path.exists():
        raise SystemExit(f"{args.id} has no implementation or Fix document for an impact decision.")
    try:
        decision = _validation_impact_decision(
            classification=args.classification,
            proof_layers=tuple(args.proof_layer or ()),
            validation_verdict=args.validation_verdict,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    section = _validation_impact_section(
        baseline=args.baseline,
        change_summary=args.change_summary,
        decided_by=args.decided_by,
        decision=decision,
    )
    docs_text = implementation_path.read_text(encoding="utf-8")
    updated = _upsert_markdown_section(
        docs_text,
        heading="Validation Impact",
        section=section,
        before_heading="QA & Code Review",
    )
    implementation_path.write_text(updated, encoding="utf-8")
    payload = {
        "work_item": item.item_id,
        "artifact": _operational_status_artifact(root, implementation_path),
        "baseline_proof": args.baseline.strip(),
        "change_summary": args.change_summary.strip(),
        "decided_by": args.decided_by.strip(),
        **decision,
    }
    payload["decision_identity"] = _validation_impact_identity(
        baseline=args.baseline,
        change_summary=args.change_summary,
        decided_by=args.decided_by,
        decision=decision,
    )
    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return
    print(f"Recorded validation impact for {item.item_id}:")
    print(f"- Classification: {decision['classification']}")
    print(f"- Required validation: {decision['required_validation']}")
    print(f"- Validation verdict: {decision['validation_verdict']}")
    print(f"- Artifact: {payload['artifact']}")


def cmd_smoke_bomb(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve() if args.root else Path.cwd().resolve()
    output_path = Path(args.output).expanduser().resolve()
    client_agents = tuple(sorted(set(args.client_agent)))
    validation_commands = tuple(args.validation_command)
    if args.plan and args.apply:
        raise SystemExit("--plan cannot be combined with --apply.")
    if args.yes and not args.apply:
        raise SystemExit("--yes requires --apply.")
    if args.plan_fingerprint and not args.apply:
        raise SystemExit("--plan-fingerprint requires --apply.")
    if args.apply and not args.plan_fingerprint:
        raise SystemExit("--apply requires --plan-fingerprint <SHA256>.")
    plan, outputs = _build_smoke_bomb_plan(root, client_agents, validation_commands, output_path)
    if not args.apply:
        if args.format == "json":
            print(json.dumps(plan, indent=2))
        else:
            print(_format_smoke_bomb_plan_human(plan))
        if plan["blockers"]:
            raise SystemExit(1)
        return

    if not args.yes:
        if not os.isatty(0):
            raise SystemExit("Interactive apply requires a TTY; authorized agents add --yes.")
        print(_format_smoke_bomb_plan_human(plan))
        confirmation = input("Apply this Smoke Bomb plan and export the client ZIP? [y/N] ")
        if confirmation.strip().lower() not in {"y", "yes"}:
            raise SystemExit("Smoke Bomb cancelled; no changes made.")
    result = _apply_smoke_bomb_plan(
        root,
        plan,
        outputs,
        args.plan_fingerprint,
        fail_after_replacements=args.fail_after_replacements,
    )
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(_format_smoke_bomb_result_human(result))
    if result["status"] != "exported":
        raise SystemExit(1)


def cmd_upgrade(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve() if args.root else Path.cwd()
    selected_agent = args.agent
    if args.plan and (args.apply or args.yes):
        raise SystemExit("--plan cannot be combined with --apply or --yes.")
    if args.apply and args.yes:
        raise SystemExit("--apply and --yes are separate upgrade modes.")
    if args.plan_fingerprint and not args.apply:
        raise SystemExit("--plan-fingerprint requires --apply.")
    if args.apply:
        if not args.plan_fingerprint:
            raise SystemExit("--apply requires --plan-fingerprint <SHA256>.")
        result = _apply_repository_upgrade_plan(
            root,
            selected_agent,
            args.plan_fingerprint,
        )
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(_format_upgrade_apply_human(result))
        if result["status"] == "failed":
            raise SystemExit(1)
        return
    plan = _build_repository_upgrade_plan(root, selected_agent)
    plan_only = args.plan or (args.format == "json" and not args.yes)
    if plan_only:
        if args.format == "json":
            print(json.dumps(plan, indent=2))
        else:
            print(_format_upgrade_plan_human(plan))
        if plan["blockers"]:
            raise SystemExit(1)
        return

    if args.format == "human":
        print(_format_upgrade_plan_human(plan))
    if plan["blockers"]:
        raise SystemExit(1)
    if not plan["target_files"]:
        result = _apply_repository_upgrade_plan(
            root,
            selected_agent,
            plan["plan_fingerprint"],
        )
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(_format_upgrade_apply_human(result))
        return

    confirmed = args.yes
    if not confirmed:
        if not os.isatty(0):
            raise SystemExit(
                "Non-interactive upgrade requires --yes, or use --plan for a non-mutating plan."
            )
        response = input("Apply this exact upgrade plan? [y/N] ").strip().lower()
        confirmed = response in {"y", "yes"}
    if not confirmed:
        print("project upgrade: cancelled; no changes applied")
        return

    result = _apply_repository_upgrade_plan(
        root,
        selected_agent,
        plan["plan_fingerprint"],
    )
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(_format_upgrade_apply_human(result))
    if result["status"] == "failed":
        raise SystemExit(1)


def cmd_coordinate_init(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        if (
            args.material_user_facing == "yes"
            and args.claim_class != "mechanical"
            and not args.checkpoint_unit
        ):
            raise ValueError(
                "Material user-facing coordination requires --checkpoint-unit for the earliest proof."
            )
        material_verification = args.material_verification == "yes"
        if material_verification:
            verification_claims = _coordination_csv(args.verification_claims, "verification_claims")
            verification_stages = _coordination_csv(args.verification_stages, "verification_stages")
            unknown_stages = [
                stage for stage in verification_stages if stage not in VERIFICATION_CAMPAIGN_STAGES
            ]
            if unknown_stages:
                raise ValueError("Unknown verification stages: " + ", ".join(unknown_stages))
            indexes = [VERIFICATION_CAMPAIGN_STAGES.index(stage) for stage in verification_stages]
            if indexes != sorted(indexes):
                raise ValueError("Verification requirement stages must use canonical stage order.")
            verification_scope = _coordination_csv(args.verification_scope, "verification_scope")
            verification_contract = _verification_identity(
                {
                    "claims": verification_claims,
                    "stages": verification_stages,
                    "affected_scope": verification_scope,
                }
            )
        else:
            if any(
                value is not None
                for value in (
                    args.verification_claims,
                    args.verification_stages,
                    args.verification_scope,
                )
            ):
                raise ValueError(
                    "Verification claims, stages, and scope are valid only when "
                    "--material-verification yes."
                )
            verification_claims = []
            verification_stages = []
            verification_scope = []
            verification_contract = None
        path = _coordination_state_path(root, args.id)
        if path.exists() and not args.force:
            raise ValueError(
                f"{path} already exists; use `coordinate status` or --force to replace it."
            )
        work_dir = path.parent
        payload: dict[str, object] = {
            "schema_version": COORDINATION_SCHEMA_VERSION,
            "target_id": args.id,
            "work_item_path": _delegation_relative_path(root, work_dir),
            "intent_identity": _coordination_artifact_identity(root, args.id),
            "loaded_contract": {
                "package_version": args.loaded_package_version,
                "asset_version": args.loaded_asset_version,
                "contract_version": args.loaded_contract_version,
                "context_id": args.context_id,
                "recorded_at": date.today().isoformat(),
            },
            "phase": args.phase,
            "source_revision": args.source_revision,
            "repositories": _coordination_repository_sources(
                args.repository_source, args.source_revision
            ),
            "decisions": list(dict.fromkeys(args.decision or [])),
            "boundary_decisions": [],
            "last_boundary": None,
            "outcome_checkpoint": {
                "required": args.material_user_facing == "yes" and args.claim_class != "mechanical",
                "claim_class": args.claim_class,
                "checkpoint_unit": args.checkpoint_unit,
                "status": (
                    "pending"
                    if args.material_user_facing == "yes" and args.claim_class != "mechanical"
                    else "not-required"
                ),
                "record": None,
            },
            "verification_requirement": {
                "required": material_verification,
                "claims": verification_claims,
                "stages": verification_stages,
                "affected_scope": verification_scope,
                "proof_contract_identity": verification_contract,
            },
            "verification_campaign": None,
            "next_action": args.next_action,
            "host_facts": {
                "context_contract": "declared",
                "telemetry": "unknown",
            },
        }
        _coordination_write_state(root, args.id, payload)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_COORDINATION_INVALID: {exc}") from exc
    print(f"Initialized durable coordination state: {path}")


def cmd_coordinate_context_record(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        current_intent_identity = _coordination_artifact_identity(root, args.id)
        if state.get("intent_identity") != current_intent_identity:
            issues = _coordination_boundary_gate_issues(
                root,
                args.id,
                boundary="new-evidence-or-owner-reframe",
            )
            if issues:
                raise ValueError(issues[0])
        state["loaded_contract"] = {
            "package_version": args.loaded_package_version,
            "asset_version": args.loaded_asset_version,
            "contract_version": args.loaded_contract_version,
            "context_id": args.context_id,
            "recorded_at": date.today().isoformat(),
        }
        state["intent_identity"] = current_intent_identity
        state["next_action"] = args.next_action
        path = _coordination_write_state(root, args.id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_COORDINATION_INVALID: {exc}") from exc
    print(f"Declared loaded physical-context contract: {path}")


def cmd_coordinate_phase(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        state["phase"] = args.phase
        state["source_revision"] = args.source_revision
        state["repositories"] = _coordination_repository_sources(
            args.repository_source, args.source_revision
        )
        state["next_action"] = args.next_action
        path = _coordination_write_state(root, args.id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_COORDINATION_INVALID: {exc}") from exc
    print(f"Advanced durable coordination phase: {path}")


def cmd_coordinate_preflight(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        payload = _coordination_preflight_payload(root, args.id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_COORDINATION_INVALID: {exc}") from exc
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Coordination preflight: {args.id}")
        print(f"Contract: {payload['contract_state']}")
        reasons = payload["reasons"]
        assert isinstance(reasons, list)
        for reason in reasons:
            print(f"- {reason}")
        print(f"Next action: {payload['next_action']}")
        if payload["command"]:
            print(f"Run: {payload['command']}")


def cmd_coordinate_boundary(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        if args.classification == "approved-change" and not args.amendment_identity:
            raise ValueError("approved-change requires --amendment-identity.")
        if args.classification != "approved-change" and args.amendment_identity:
            raise ValueError("--amendment-identity is valid only for approved-change.")
        affected = (
            []
            if not args.affected_units or args.affected_units.strip().lower() in {"none", "n/a"}
            else _coordination_csv(args.affected_units, "affected_units")
        )
        if (
            args.boundary
            in {
                "before-unit-start",
                "unit-return-or-dependency-join",
                "before-review-or-complete",
            }
            and not affected
        ):
            raise ValueError(f"{args.boundary} requires --affected-units for gate ownership.")
        current_intent_identity = _coordination_artifact_identity(root, args.id)
        decision = {
            "boundary": args.boundary,
            "classification": args.classification,
            "relevant_ocs": _coordination_csv(args.ocs, "ocs"),
            "capability_change": args.capability_change,
            "user_consequence": args.consequence,
            "affected_units": affected,
            "amendment_identity": args.amendment_identity,
            "shared_premises_valid": args.shared_premises_valid,
            "decided_by": args.decided_by,
            "decision_date": date.today().isoformat(),
            "intent_identity": current_intent_identity,
            "source_revision": state["source_revision"],
            "source_identity": _coordination_source_identity(state),
        }
        for field_name in ("capability_change", "user_consequence", "decided_by"):
            _coordination_required_text(decision[field_name], field_name)
        decisions = state["boundary_decisions"]
        assert isinstance(decisions, list)
        decisions.append(decision)
        state["last_boundary"] = decision
        if args.classification == "drift-detected":
            state["next_action"] = (
                "Restore approved intent or obtain an amendment before continuing affected units: "
                + (", ".join(affected) or "the coordination target")
            )
        elif args.classification == "approved-change":
            state["intent_identity"] = current_intent_identity
            state["next_action"] = (
                "Refresh the existing canonical plan and Delegate packet for affected units: "
                + (", ".join(affected) or "the coordination target")
            )
        else:
            if args.boundary == "new-evidence-or-owner-reframe":
                state["intent_identity"] = current_intent_identity
            state["next_action"] = args.next_action
        path = _coordination_write_state(root, args.id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_COORDINATION_DRIFT_INVALID: {exc}") from exc
    print(f"Recorded {args.classification} at {args.boundary}: {path}")


def cmd_coordinate_checkpoint(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        checkpoint = state["outcome_checkpoint"]
        assert isinstance(checkpoint, dict)
        required = checkpoint.get("required") is True
        if not required:
            raise ValueError("This work item does not require an early real-outcome checkpoint.")
        if args.unit != checkpoint.get("checkpoint_unit"):
            raise ValueError("Checkpoint unit does not match the recorded earliest proof unit.")
        if checkpoint.get("status") in {"pass", "fail"}:
            raise ValueError("Early outcome checkpoint is already terminal; do not repeat it.")
        for field_name in (
            "actor",
            "entry_point",
            "starting_state",
            "operations",
            "resulting_state",
            "source_environment",
            "observations",
        ):
            _coordination_required_text(getattr(args, field_name), field_name)
        if args.owner_judgment == "required" and args.verdict == "pass":
            raise ValueError(
                "Owner-only judgment cannot self-pass; use pending until owner evidence exists."
            )
        record = {
            "unit_id": args.unit,
            "claim_class": checkpoint.get("claim_class"),
            "actor": args.actor,
            "normal_entry_point": args.entry_point,
            "starting_state": args.starting_state,
            "material_operations": args.operations,
            "resulting_state_or_artifact": args.resulting_state,
            "source_environment": args.source_environment,
            "observations": args.observations,
            "owner_judgment": args.owner_judgment,
            "verdict": args.verdict,
            "recorded_by": args.recorded_by,
            "recorded_at": date.today().isoformat(),
        }
        checkpoint["record"] = record
        checkpoint["status"] = args.verdict
        if args.verdict == "fail":
            affected = (
                set(_coordination_csv(args.affected_units, "affected_units"))
                if args.affected_units
                and args.affected_units.strip().lower() not in {"none", "n/a"}
                else {str(checkpoint.get("checkpoint_unit"))}
            )
            state["next_action"] = (
                "Route the product contradiction through drift restoration/amendment; blocked: "
                + (", ".join(sorted(affected)) or "the coordination target")
            )
        elif args.verdict == "pending":
            state["next_action"] = "Obtain the named owner-only judgment before fan-out."
        else:
            state["next_action"] = "Continue dependent work; do not repeat unchanged checkpoint."
        path = _coordination_write_state(root, args.id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_COORDINATION_CHECKPOINT_INVALID: {exc}") from exc
    print(f"Recorded early outcome checkpoint {args.verdict}: {path}")


def cmd_coordinate_verification_capabilities(args: argparse.Namespace) -> None:
    payload = {
        "schema_version": VERIFICATION_CAMPAIGN_SCHEMA_VERSION,
        "contract": "project-workflow-verifier-adapter",
        "runtime_dependency_required": False,
        "capabilities": list(VERIFICATION_ADAPTER_CAPABILITIES),
        "invocation": {
            "input": {
                "request_identity": "sha256",
                "candidate_identity": "string",
                "source_identity": "sha256",
                "proof_contract_identity": "sha256",
                "mode": list(VERIFICATION_CAMPAIGN_MODES),
                "stage": list(VERIFICATION_CAMPAIGN_STAGES),
                "selected_scope": "string-list",
                "limits": "nullable-positive-integers",
                "checkpoint_identity": "optional-string",
            },
            "output": {
                "request_identity": "same-as-input",
                "candidate_identity": "same-as-input",
                "source_identity": "same-as-input",
                "proof_contract_identity": "same-as-input",
                "stage": "same-as-input",
                "outcome": list(VERIFICATION_RECEIPT_OUTCOMES),
                "target_calls": "non-negative-integer",
                "elapsed_seconds": "non-negative-integer",
                "target_identity": "string",
                "evaluator_identity": "string",
                "artifact": "reference",
            },
        },
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("Generic optional verifier adapter contract")
        print("Runtime dependency required: no")
        capabilities = payload["capabilities"]
        assert isinstance(capabilities, list)
        print("Capabilities: " + ", ".join(str(value) for value in capabilities))


def cmd_coordinate_verification_init(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        if state.get("verification_campaign") is not None and not args.force:
            raise ValueError(
                "A verification campaign already exists; inspect it or use --force for a "
                "new candidate/decision."
            )
        claims = _coordination_csv(args.claims, "claims")
        stages = _coordination_csv(args.stages, "stages")
        unknown_stages = [stage for stage in stages if stage not in VERIFICATION_CAMPAIGN_STAGES]
        if unknown_stages:
            raise ValueError("Unknown verification stages: " + ", ".join(unknown_stages))
        stage_indexes = [VERIFICATION_CAMPAIGN_STAGES.index(stage) for stage in stages]
        if stage_indexes != sorted(stage_indexes):
            raise ValueError("Verification stages must use canonical stage order.")
        if args.mode == "certification" and "full" not in stages:
            raise ValueError("A certification campaign must include the full stage.")
        affected_scope = _coordination_csv(args.affected_scope, "affected_scope")
        limits = {
            "max_failures": args.max_failures,
            "max_target_calls": args.max_target_calls,
            "max_elapsed_seconds": args.max_elapsed_seconds,
        }
        for key, value in limits.items():
            _verification_optional_limit(value, f"limits.{key}")
        if not any(value is not None for value in limits.values()):
            raise ValueError("A material verification campaign requires at least one finite limit.")
        if args.mode == "diagnostic":
            _coordination_required_text(args.diagnostic_decision, "diagnostic_decision")
        elif args.diagnostic_decision:
            raise ValueError("--diagnostic-decision is valid only in diagnostic mode.")
        if args.impact == "unknown" and "full" not in stages:
            raise ValueError("Unknown material impact requires the full proof stage.")
        capabilities = list(dict.fromkeys(args.adapter_capability or []))
        if args.adapter_kind == "command":
            if not args.adapter_command_json:
                raise ValueError("Command adapter requires --adapter-command-json.")
            try:
                adapter_command = json.loads(args.adapter_command_json)
            except json.JSONDecodeError as exc:
                raise ValueError("--adapter-command-json must be valid JSON.") from exc
            if (
                not isinstance(adapter_command, list)
                or not adapter_command
                or any(not isinstance(part, str) or not part.strip() for part in adapter_command)
            ):
                raise ValueError("--adapter-command-json must be a non-empty JSON string list.")
            if args.manual_command:
                raise ValueError("--manual-command is valid only for manual adapters.")
            if limits["max_elapsed_seconds"] is None:
                raise ValueError(
                    "Command adapter campaigns require --max-elapsed-seconds so the host "
                    "invocation cannot hang indefinitely."
                )
            required = _verification_adapter_required_capabilities(
                mode=args.mode,
                stages=stages,
                limits=limits,
            )
            missing = sorted(required - set(capabilities))
            if missing:
                raise ValueError(
                    "Command adapter does not declare required controls: " + ", ".join(missing)
                )
            manual_command = None
        else:
            adapter_command = None
            manual_command = _coordination_required_text(args.manual_command, "manual_command")
            if args.adapter_command_json:
                raise ValueError("--adapter-command-json is valid only for command adapters.")
        proof_contract_identity = _verification_identity(
            {
                "claims": claims,
                "stages": stages,
                "affected_scope": affected_scope,
            }
        )
        requirement = state.get("verification_requirement")
        if isinstance(requirement, dict):
            if requirement.get("required") is not True:
                raise ValueError(
                    "Material verification was durably classified as not required for this work item."
                )
            for actual, expected, label in (
                (claims, requirement.get("claims"), "claims"),
                (stages, requirement.get("stages"), "stages"),
                (affected_scope, requirement.get("affected_scope"), "affected scope"),
                (
                    proof_contract_identity,
                    requirement.get("proof_contract_identity"),
                    "proof contract",
                ),
            ):
                if actual != expected:
                    raise ValueError(
                        f"Campaign {label} does not match the durable verification requirement."
                    )
        campaign: dict[str, object] = {
            "schema_version": VERIFICATION_CAMPAIGN_SCHEMA_VERSION,
            "candidate_identity": args.candidate_identity,
            "intent_identity": _coordination_artifact_identity(root, args.id),
            "source_identity": _coordination_source_identity(state),
            "proof_contract_identity": proof_contract_identity,
            "mode": args.mode,
            "claims": claims,
            "stages": stages,
            "affected_scope": affected_scope,
            "impact": args.impact,
            "limits": limits,
            "diagnostic_decision": args.diagnostic_decision,
            "adapter": {
                "kind": args.adapter_kind,
                "capabilities": capabilities,
                "command": adapter_command,
                "manual_command": manual_command,
            },
            "receipts": [],
            "receipt_ledger_identity": _verification_receipt_ledger_identity([]),
            "current_stage": stages[0],
            "outcome": "pending",
            "next_action": (
                "Complete implementation before invoking the verifier."
                if _verification_campaign_projection(
                    root,
                    args.id,
                    {**state, "verification_campaign": None},
                    material_verification=True,
                )["operational_state"]
                == "implementation-required"
                else f"Run only the current {stages[0]} stage."
            ),
        }
        _verification_validate_campaign(campaign)
        state["verification_campaign"] = campaign
        state["next_action"] = str(campaign["next_action"])
        path = _coordination_write_state(root, args.id, state)
        projection = _verification_campaign_projection(root, args.id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_VERIFICATION_CAMPAIGN_INVALID: {exc}") from exc
    payload = {
        "target_id": args.id,
        "source": _delegation_relative_path(root, path),
        "campaign": campaign,
        "projection": projection,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Initialized verification campaign: {path}")
        print(f"Operational state: {projection['operational_state']}")
        print(f"Next action: {projection['next_action']}")


def cmd_coordinate_verification_record(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        campaign = state.get("verification_campaign")
        if not isinstance(campaign, dict):
            raise ValueError("No verification campaign exists; initialize one first.")
        current, reasons = _verification_campaign_currentness(root, args.id, state, campaign)
        if not current:
            raise ValueError("Campaign is stale: " + "; ".join(reasons))
        if args.stage not in campaign["stages"]:
            raise ValueError(f"Stage {args.stage} is outside the current campaign.")
        completed = _verification_completed_stages(campaign)
        stages = [str(stage) for stage in campaign["stages"]]
        next_stage = next((stage for stage in stages if stage not in completed), None)
        is_regrade = bool(args.regrade)
        if is_regrade:
            if args.target_calls != 0:
                raise ValueError("Evaluator-only regrade requires --target-calls 0.")
            receipts = campaign["receipts"]
            assert isinstance(receipts, list)
            retained = [
                receipt
                for receipt in receipts
                if isinstance(receipt, dict)
                and receipt.get("stage") == args.stage
                and receipt.get("target_identity") == args.target_identity
                and int(receipt.get("target_calls", 0)) > 0
            ]
            if not retained:
                raise ValueError(
                    "Evaluator-only regrade requires a retained current target identity."
                )
            if any(
                receipt.get("evaluator_identity") == args.evaluator_identity for receipt in retained
            ):
                raise ValueError("Evaluator-only regrade requires a changed evaluator identity.")
        else:
            if campaign.get("outcome") in {"blocked", "limit-reached", "pass"}:
                raise ValueError(
                    f"Campaign outcome is {campaign.get('outcome')}; further target work is blocked."
                )
            if args.stage != next_stage:
                raise ValueError(
                    f"Later-stage execution is blocked; current stage is {next_stage or 'none'}."
                )
            if args.outcome == "product-failure" and args.target_calls == 0:
                raise ValueError(
                    "A product/assertion failure must record at least one target call."
                )
        receipt_base: dict[str, object] = {
            "candidate_identity": campaign["candidate_identity"],
            "intent_identity": campaign["intent_identity"],
            "source_identity": campaign["source_identity"],
            "proof_contract_identity": campaign["proof_contract_identity"],
            "stage": args.stage,
            "scope": _coordination_csv(args.scope, "scope"),
            "runtime_identity": args.runtime_identity,
            "target_identity": args.target_identity,
            "evaluator_identity": args.evaluator_identity,
            "artifact": args.artifact,
            "outcome": args.outcome,
            "target_calls": args.target_calls,
            "elapsed_seconds": args.elapsed_seconds,
            "stage_complete": args.stage_complete == "yes",
            "regrade": is_regrade,
            "recorded_at": date.today().isoformat(),
        }
        request_identity = getattr(args, "request_identity", None)
        if request_identity is not None:
            receipt_base["request_identity"] = request_identity
        receipt = {
            **receipt_base,
            "receipt_identity": _verification_identity(receipt_base),
        }
        receipts = campaign["receipts"]
        assert isinstance(receipts, list)
        if any(
            isinstance(existing, dict)
            and existing.get("receipt_identity") == receipt["receipt_identity"]
            for existing in receipts
        ):
            raise ValueError("This exact verification receipt is already recorded.")
        receipts.append(receipt)
        _verification_recompute_campaign(campaign)
        state["next_action"] = str(campaign["next_action"])
        path = _coordination_write_state(root, args.id, state)
        projection = _verification_campaign_projection(root, args.id, state)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_VERIFICATION_RECEIPT_INVALID: {exc}") from exc
    payload = {
        "target_id": args.id,
        "source": _delegation_relative_path(root, path),
        "receipt": receipt,
        "projection": projection,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Recorded {args.outcome} for {args.stage}: {path}")
        print(f"Operational state: {projection['operational_state']}")
        print(f"Next action: {projection['next_action']}")


def cmd_coordinate_verification_run(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        campaign = state.get("verification_campaign")
        if not isinstance(campaign, dict):
            raise ValueError("No verification campaign exists; initialize one first.")
        adapter = campaign.get("adapter")
        if not isinstance(adapter, dict) or adapter.get("kind") != "command":
            raise ValueError(
                "The current campaign uses a declared manual command; run it explicitly and "
                "record its receipt with verification-record."
            )
        capabilities = set(adapter.get("capabilities", []))
        command = adapter.get("command")
        assert isinstance(command, list)
        current, reasons = _verification_campaign_currentness(root, args.id, state, campaign)
        if not current:
            raise ValueError("Campaign is stale: " + "; ".join(reasons))
        projection = _verification_campaign_projection(root, args.id, state)
        if args.regrade:
            if "transcript-regrade" not in capabilities:
                raise ValueError("Command adapter does not support transcript-regrade.")
            if not args.stage or not args.target_identity:
                raise ValueError("--regrade requires --stage and --target-identity.")
            stage = args.stage
            action = "regrade"
        else:
            if projection["operational_state"] != "verification-required":
                raise ValueError(
                    "Verifier invocation is not authorized while operational state is "
                    f"{projection['operational_state']}."
                )
            stage = str(campaign["current_stage"])
            action = "verify"
        limits = campaign["limits"]
        assert isinstance(limits, dict)
        maximum_elapsed = limits.get("max_elapsed_seconds")
        assert isinstance(maximum_elapsed, int)
        elapsed_so_far = projection["elapsed_seconds"]
        assert isinstance(elapsed_so_far, int)
        timeout_seconds = maximum_elapsed - elapsed_so_far
        if timeout_seconds <= 0:
            raise ValueError("The elapsed campaign limit is exhausted; no invocation is allowed.")
        receipts = campaign["receipts"]
        assert isinstance(receipts, list)
        request = {
            "schema_version": VERIFICATION_CAMPAIGN_SCHEMA_VERSION,
            "action": action,
            "candidate_identity": campaign["candidate_identity"],
            "source_identity": campaign["source_identity"],
            "proof_contract_identity": campaign["proof_contract_identity"],
            "mode": campaign["mode"],
            "stage": stage,
            "selected_scope": campaign["affected_scope"],
            "limits": limits,
            "prior_receipt_identities": [
                receipt["receipt_identity"] for receipt in receipts if isinstance(receipt, dict)
            ],
            "retained_target_identity": args.target_identity if args.regrade else None,
        }
        request["request_identity"] = _verification_identity(request)
        request_binding = {
            field_name: request[field_name]
            for field_name in (
                "request_identity",
                "candidate_identity",
                "source_identity",
                "proof_contract_identity",
                "stage",
            )
        }
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                input=json.dumps(request, sort_keys=True) + "\n",
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            adapter_output: dict[str, object] = {
                **request_binding,
                "outcome": "harness-failure",
                "scope": campaign["affected_scope"],
                "runtime_identity": args.runtime_identity,
                "target_identity": args.target_identity or "no-target-output",
                "evaluator_identity": "not-run",
                "artifact": f"adapter-timeout:{timeout_seconds}",
                "target_calls": 0,
                "elapsed_seconds": timeout_seconds,
                "stage_complete": False,
            }
        except OSError as exc:
            adapter_output = {
                **request_binding,
                "outcome": "harness-failure",
                "scope": campaign["affected_scope"],
                "runtime_identity": args.runtime_identity,
                "target_identity": args.target_identity or "no-target-output",
                "evaluator_identity": "not-run",
                "artifact": f"adapter-launch-error:{type(exc).__name__}",
                "target_calls": 0,
                "elapsed_seconds": 0,
                "stage_complete": False,
            }
        else:
            if completed.returncode != 0:
                adapter_output = {
                    **request_binding,
                    "outcome": "harness-failure",
                    "scope": campaign["affected_scope"],
                    "runtime_identity": args.runtime_identity,
                    "target_identity": args.target_identity or "no-target-output",
                    "evaluator_identity": "not-run",
                    "artifact": f"adapter-exit:{completed.returncode}",
                    "target_calls": 0,
                    "elapsed_seconds": 0,
                    "stage_complete": False,
                }
            else:
                try:
                    parsed_output = json.loads(completed.stdout)
                except json.JSONDecodeError:
                    parsed_output = None
                if not isinstance(parsed_output, dict):
                    adapter_output = {
                        **request_binding,
                        "outcome": "harness-failure",
                        "scope": campaign["affected_scope"],
                        "runtime_identity": args.runtime_identity,
                        "target_identity": args.target_identity or "no-target-output",
                        "evaluator_identity": "not-run",
                        "artifact": "adapter-invalid-json",
                        "target_calls": 0,
                        "elapsed_seconds": 0,
                        "stage_complete": False,
                    }
                else:
                    adapter_output = parsed_output
        try:
            scope = _verification_adapter_output_scope(
                adapter_output,
                request=request,
                request_binding=request_binding,
                campaign=campaign,
            )
        except ValueError as exc:
            # The adapter process was invoked, so a malformed or mismatched response must be
            # retained as an infrastructure attempt. Otherwise the same expensive invocation can
            # repeat forever outside the one-retry accounting.
            adapter_output = {
                **request_binding,
                "outcome": "harness-failure",
                "scope": campaign["affected_scope"],
                "runtime_identity": args.runtime_identity,
                "target_identity": args.target_identity or "untrusted-adapter-output",
                "evaluator_identity": "not-trusted",
                "artifact": "adapter-invalid-output:" + str(exc),
                "target_calls": 0,
                "elapsed_seconds": 0,
                "stage_complete": False,
            }
            scope = [str(value) for value in campaign["affected_scope"]]
        record_args = argparse.Namespace(
            id=args.id,
            stage=stage,
            outcome=adapter_output["outcome"],
            scope=",".join(scope),
            runtime_identity=adapter_output["runtime_identity"],
            target_identity=adapter_output["target_identity"],
            evaluator_identity=adapter_output["evaluator_identity"],
            artifact=adapter_output["artifact"],
            target_calls=adapter_output["target_calls"],
            elapsed_seconds=adapter_output["elapsed_seconds"],
            stage_complete="yes" if adapter_output["stage_complete"] is True else "no",
            regrade=args.regrade,
            request_identity=request["request_identity"],
            format=args.format,
        )
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_VERIFICATION_ADAPTER_INVALID: {exc}") from exc
    cmd_coordinate_verification_record(record_args)


def cmd_coordinate_verification_preflight(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        state = _coordination_load_state(root, args.id)
        requirement = state.get("verification_requirement")
        if isinstance(requirement, dict):
            if args.material_verification is not None and (
                (args.material_verification == "yes") != (requirement.get("required") is True)
            ):
                raise ValueError(
                    "Preflight materiality does not match the durable verification requirement."
                )
            for argument, field_name, label in (
                (args.claim, "claims", "claims"),
                (args.stage, "stages", "stages"),
                (args.scope, "affected_scope", "scope"),
            ):
                if argument is not None and _coordination_csv(argument, label) != requirement.get(
                    field_name
                ):
                    raise ValueError(
                        f"Preflight {label} does not match the durable verification requirement."
                    )
            material_override = None
        else:
            material_override = args.material_verification == "yes"
        projection = _verification_campaign_projection(
            root,
            args.id,
            state,
            material_verification=material_override,
        )
        campaign = state.get("verification_campaign")
        if isinstance(campaign, dict):
            required_campaign = {
                "claims": campaign["claims"],
                "stages": campaign["stages"],
                "affected_scope": campaign["affected_scope"],
                "limits": campaign["limits"],
            }
        elif isinstance(requirement, dict):
            required_campaign = {
                "claims": requirement["claims"],
                "stages": requirement["stages"],
                "affected_scope": requirement["affected_scope"],
                "limits": None,
                "proof_contract_identity": requirement["proof_contract_identity"],
            }
        else:
            required_campaign = {
                "claims": _coordination_csv(args.claim, "claim") if args.claim else [],
                "stages": (_coordination_csv(args.stage, "stage") if args.stage else []),
                "affected_scope": (_coordination_csv(args.scope, "scope") if args.scope else []),
                "limits": None,
            }
        payload = {
            "schema_version": VERIFICATION_CAMPAIGN_SCHEMA_VERSION,
            "target_id": args.id,
            "projection": projection,
            "required_campaign": required_campaign,
            "verifier_invocations": 0,
            "mutated": False,
        }
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_VERIFICATION_PREFLIGHT_INVALID: {exc}") from exc
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Verification preflight: {args.id}")
        print(f"Operational state: {projection['operational_state']}")
        print("Verifier invocations: 0")
        print(f"Next action: {projection['next_action']}")


def cmd_execute(args: argparse.Namespace) -> None:
    root = Path.cwd()
    projection = _execution_control_projection(root, args.id, "material-execution")
    if projection["state"] == "blocked":
        _print_execution_projection(projection, args.format)
        raise SystemExit(2)
    coordination = _coordination_load_state(root, args.id)
    control = _execution_validate_control(coordination.get("execution_control"), work_id=args.id)
    capability = control["capability"]
    assert isinstance(capability, dict)
    settings = capability.get("settings")
    if settings is None:
        _print_execution_projection(projection, args.format)
        return
    host = str(capability["host"])
    try:
        if host == "codex":
            try:
                from project_workflow.codex_adapter import run_codex_adapter
            except ModuleNotFoundError:
                from codex_adapter import run_codex_adapter  # type: ignore

            adapter_result = run_codex_adapter(root, control)
            receipt_kind = "codex-adapter"
            host_label = "Codex"
        elif host == "claude-code":
            try:
                from project_workflow.claude_adapter import run_claude_adapter
            except ModuleNotFoundError:
                from claude_adapter import run_claude_adapter  # type: ignore

            adapter_result = run_claude_adapter(root, control)
            receipt_kind = "claude-code-adapter"
            host_label = "Claude Code"
        else:
            raise SystemExit(
                "PW_EXECUTION_ADAPTER_UNSUPPORTED: configured host has no packaged adapter"
            )
    except Exception as exc:
        try:
            from project_workflow.claude_adapter import ClaudeAdapterError
            from project_workflow.codex_adapter import CodexAdapterError
        except ModuleNotFoundError:
            from claude_adapter import ClaudeAdapterError  # type: ignore
            from codex_adapter import CodexAdapterError  # type: ignore

        if isinstance(exc, (CodexAdapterError, ClaudeAdapterError)):
            prefix = "PW_CODEX_ADAPTER_BLOCKED" if host == "codex" else "PW_CLAUDE_ADAPTER_BLOCKED"
            adapter_result = {
                "terminal_status": "failed",
                "terminal_reason": f"{prefix}: {exc}",
                "native_metrics": {
                    name: 0
                    for name in (
                        "elapsed-seconds",
                        "agent-budget",
                        "turns",
                        "tool-calls",
                        "test-invocations",
                        "identical-retries",
                        "worker-launches",
                        "changed-paths",
                        "write-scope",
                    )
                },
            }
            adapter_result["evidence_identity"] = _execution_hash(adapter_result)
            receipt_kind = "codex-adapter" if host == "codex" else "claude-code-adapter"
            host_label = "Codex" if host == "codex" else "Claude Code"
        else:
            raise
    terminal_status = str(adapter_result["terminal_status"])
    outcome = {
        "completed": "pass",
        "interrupted": "blocked",
        "failed": "infrastructure-failure",
    }.get(terminal_status, "infrastructure-failure")
    candidates = control["candidates"]
    assert isinstance(candidates, dict)
    receipt: dict[str, object] = {
        "schema_version": EXECUTION_CONTROL_SCHEMA_VERSION,
        "kind": receipt_kind,
        "work_id": args.id,
        "sealed_identity": control["sealed_identity"],
        "capability_identity": _execution_hash(capability),
        "phase": control["phase"],
        "candidate_identity": candidates["working_revision"],
        "proof_obligations_identity": _execution_hash(control["proof_obligations"]),
        "source_revision": control["source_revision"],
        "operation": "material-execution",
        "outcome": outcome,
        "native_metrics": adapter_result["native_metrics"],
        "evidence_identity": adapter_result["evidence_identity"],
        "receipt_identity": "pending",
    }
    receipt["receipt_identity"] = _execution_hash(
        {key: item for key, item in receipt.items() if key != "receipt_identity"}
    )
    updated_control = _execution_copy(control)
    receipts = updated_control["receipts"]
    assert isinstance(receipts, list)
    receipts.append(receipt)
    _execution_validate_control(updated_control, work_id=args.id)
    updated_coordination = _execution_copy(coordination)
    updated_coordination["execution_control"] = updated_control
    _coordination_write_state(root, args.id, updated_coordination)
    payload = {
        **adapter_result,
        "core_receipt": receipt,
        "mutated": True,
        "executed": True,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"{host_label} execution: {args.id}")
        print(f"Status: {terminal_status}")
        print(f"Reason: {adapter_result['terminal_reason']}")
        print(f"Receipt: {receipt['receipt_identity']}")
    if outcome != "pass":
        raise SystemExit(2)


def cmd_release(args: argparse.Namespace) -> None:
    root = Path.cwd()
    projection = _execution_control_projection(root, args.id, "release")
    if projection["state"] == "blocked":
        _print_execution_projection(projection, args.format)
        raise SystemExit(2)
    coordination = _coordination_load_state(root, args.id)
    raw_plan = coordination.get("fixed_release")
    if raw_plan is None:
        _print_execution_projection(projection, args.format)
        return
    plan = _execution_validate_fixed_release(raw_plan, args.id)
    control = _execution_validate_control(coordination.get("execution_control"), work_id=args.id)
    candidates = control["candidates"]
    assert isinstance(candidates, dict)
    release_candidate = candidates.get("release_candidate")
    if not isinstance(release_candidate, dict) or (
        plan["candidate_identity"] != release_candidate["identity"]
        or plan["source_revision"] != release_candidate["source_revision"]
        or _execution_hash(plan["artifacts"]) != release_candidate["artifact_identity"]
    ):
        raise SystemExit("PW_FIXED_RELEASE_INVALID: plan does not match the promoted candidate")

    def persist_release(updated_plan: dict[str, object]) -> None:
        updated_coordination = _execution_copy(coordination)
        updated_coordination["fixed_release"] = updated_plan
        _coordination_write_state(root, args.id, updated_coordination)

    _, receipt = _execution_run_fixed_release(root, plan, persist_release)
    if args.format == "json":
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(f"Fixed release: {args.id}")
        print(f"Status: {receipt['status']}")
        print(f"Reason: {receipt['reason']}")
        print(f"Receipt: {receipt['receipt_identity']}")
    if receipt["status"] != "pass":
        raise SystemExit(2)


def cmd_coordinate_status(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        payload = _coordination_status_payload(root, args.id)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_COORDINATION_INVALID: {exc}") from exc
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Coordination status: {args.id}")
        print(f"Contract: {payload['contract_state']}")
        print(f"Phase: {payload['phase']}")
        verification = payload.get("verification")
        if isinstance(verification, dict):
            print(f"Verification: {verification['operational_state']}")
        execution = payload.get("execution")
        if isinstance(execution, dict):
            print(f"Execution: {execution['state']}")
        qa_campaign = payload.get("qa_campaign")
        if isinstance(qa_campaign, dict):
            print(f"QA campaign: {qa_campaign['state']}")
        fixed_release = payload.get("fixed_release")
        if isinstance(fixed_release, dict):
            print(f"Fixed release: {fixed_release['state']}")
        print(
            "Last boundary: "
            + (
                str(payload["last_boundary"].get("classification"))
                if isinstance(payload["last_boundary"], dict)
                else "none"
            )
        )
        print(f"Next action: {payload['next_action']}")
        print(f"Source: {payload['source']}")


def cmd_delegate_plan(args: argparse.Namespace) -> None:
    try:
        plan = _delegation_plan_from_args(Path.cwd(), args)
    except DelegationPlanError as error:
        raise SystemExit(f"{error.code}: {error.message}") from error
    if args.format == "json":
        print(json.dumps(delegation_plan_payload(plan), indent=2, sort_keys=True))
    else:
        print(_format_delegation_plan_human(plan))


def cmd_delegate_status(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        plan = _delegation_plan_from_args(root, args)
        state = _load_delegation_runtime_state(root, plan.target.target_id)
    except (
        DelegationPlanError,
        TaskOrchestrationError,
        EpicOrchestrationError,
        json.JSONDecodeError,
    ) as error:
        if isinstance(error, (DelegationPlanError, TaskOrchestrationError, EpicOrchestrationError)):
            message = f"{error.code}: {error.message}"
        else:
            message = f"PW_DELEGATION_RUNTIME_INVALID: {error}"
        raise SystemExit(message) from error
    if args.format == "json":
        print(json.dumps(_delegation_status_payload(plan, state), indent=2, sort_keys=True))
    else:
        print(_format_delegation_plan_human(plan, heading="Delegation Status"))
        if state is None:
            print("Runtime: not initialized")
        else:
            summary = _delegation_status_payload(plan, state)["runtime_summary"]
            assert isinstance(summary, dict)
            print("Runtime active: " + (", ".join(summary["active"]) or "none"))
            print("Runtime orphaned: " + (", ".join(summary["orphaned"]) or "none"))


def cmd_delegate_state_init(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        plan = _delegation_plan_from_args(root, args)
        state = initialize_delegation_runtime_state(root, plan)
    except (
        DelegationPlanError,
        TaskOrchestrationError,
        EpicOrchestrationError,
        json.JSONDecodeError,
        OSError,
    ) as error:
        if isinstance(error, (DelegationPlanError, TaskOrchestrationError, EpicOrchestrationError)):
            message = f"{error.code}: {error.message}"
        else:
            message = f"PW_DELEGATION_RUNTIME_INVALID: {error}"
        raise SystemExit(message) from error
    path = _delegation_runtime_path(root, plan.target.target_id)
    if args.format == "json":
        print(json.dumps(state, indent=2, sort_keys=True))
    else:
        print(f"Initialized ignored delegation runtime state: {path}")


def cmd_delegate_state_reconcile(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        plan = _delegation_plan_from_args(root, args)
        state = _load_delegation_runtime_state(root, plan.target.target_id)
        if state is None:
            raise _delegation_error(
                "PW_DELEGATION_RUNTIME_MISSING", "Initialize runtime state before reconciliation."
            )
        raw_observed = json.loads(Path(args.observed_handles).read_text(encoding="utf-8"))
        if not isinstance(raw_observed, dict):
            raise _delegation_error(
                "PW_DELEGATION_RUNTIME_INVALID", "Observed handles JSON must be an object."
            )
        reconciled = reconcile_delegation_runtime_state(root, plan, state, raw_observed)
        _write_delegation_runtime_state(root, plan, reconciled)
    except (
        DelegationPlanError,
        TaskOrchestrationError,
        EpicOrchestrationError,
        json.JSONDecodeError,
        OSError,
    ) as error:
        if isinstance(error, (DelegationPlanError, TaskOrchestrationError, EpicOrchestrationError)):
            message = f"{error.code}: {error.message}"
        else:
            message = f"PW_DELEGATION_RUNTIME_INVALID: {error}"
        raise SystemExit(message) from error
    if args.format == "json":
        print(json.dumps(reconciled, indent=2, sort_keys=True))
    else:
        print(f"Reconciled delegation runtime state for {plan.target.target_id}.")


def cmd_doctor(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve() if args.root else Path.cwd()
    issues = run_doctor(root)
    accepted_fingerprints = _accepted_doctor_warning_fingerprints(root)
    evaluation = _evaluate_doctor(
        issues,
        root=root,
        strict=args.strict,
        accepted_fingerprints=accepted_fingerprints,
    )

    if args.format == "json":
        print(
            json.dumps(
                _doctor_json_payload(
                    evaluation,
                    root=root,
                    accepted_fingerprints=accepted_fingerprints,
                ),
                indent=2,
            )
        )
        if evaluation.blocking_issues:
            raise SystemExit(1)
        return

    if not evaluation.visible_issues and not (args.show_accepted and evaluation.accepted_issues):
        print(f"project doctor: no issues found in {root}")
        if evaluation.accepted_issues:
            print(f"project doctor: {len(evaluation.accepted_issues)} accepted warning(s) hidden.")
        return

    print(f"project doctor: checked {root}")
    for issue in evaluation.current_issues:
        print(
            _format_doctor_issue(
                issue,
                root=root,
                strict=args.strict,
                accepted_fingerprints=accepted_fingerprints,
            )
        )
    for issue in evaluation.legacy_issues:
        print(
            _format_doctor_issue(
                issue,
                root=root,
                strict=args.strict,
                accepted_fingerprints=accepted_fingerprints,
            )
        )
    if evaluation.legacy_issues:
        print(
            f"project doctor: {len(evaluation.legacy_issues)} legacy warning(s) shown separately."
        )
    if evaluation.accepted_issues:
        if args.show_accepted:
            print(f"project doctor: {len(evaluation.accepted_issues)} accepted warning(s):")
            for issue in evaluation.accepted_issues:
                print(
                    _format_doctor_issue(
                        issue,
                        root=root,
                        strict=args.strict,
                        accepted_fingerprints=accepted_fingerprints,
                        accepted=True,
                    )
                )
        else:
            print(f"project doctor: {len(evaluation.accepted_issues)} accepted warning(s) hidden.")

    if evaluation.blocking_issues:
        print(f"project doctor: failed with {len(evaluation.blocking_issues)} blocking issue(s).")
        raise SystemExit(1)

    if evaluation.visible_issues:
        print("project doctor: passed with warnings")
    else:
        print("project doctor: passed")


def cmd_backlog_init(args: argparse.Namespace) -> None:
    """Create .project-workflow/BACKLOG.md if it is missing."""
    backlog_path = _backlog_path(Path.cwd())
    created = _ensure_backlog_file(backlog_path)
    if created:
        print(f"Created backlog: {backlog_path}")
    else:
        print(f"Backlog already exists: {backlog_path}")


def cmd_backlog_add(args: argparse.Namespace) -> None:
    """Append one backlog row with the next configured BL ID."""
    root = Path.cwd()
    backlog_path = _backlog_path(root)
    _ensure_backlog_file(backlog_path)
    rows = _backlog_rows(backlog_path)
    row_id = _next_backlog_id(root, rows)
    row = {
        "ID": row_id,
        "Title": args.title,
        "Type": _normalize_backlog_value(args.type, BACKLOG_TYPES, "type"),
        "Priority": _normalize_backlog_value(args.priority, BACKLOG_PRIORITIES, "priority"),
        "Status": _normalize_backlog_value(args.status, BACKLOG_STATUSES, "status"),
        "Outcome": args.outcome,
        "Promoted To": "",
        "Notes": args.notes or "",
    }
    _append_backlog_row(backlog_path, row)
    print(f"Added backlog row {row_id}: {args.title}")


def cmd_backlog_list(args: argparse.Namespace) -> None:
    """Print backlog rows without mutating the backlog file."""
    backlog_path = _backlog_path(Path.cwd())
    if not backlog_path.exists():
        raise SystemExit(f"Missing backlog file: {backlog_path}. Run `project backlog init`.")
    rows = _backlog_rows(backlog_path)
    if not rows:
        print("No backlog rows.")
        return
    for row in rows:
        print(
            f"{row['ID']}: {row['Title']} "
            f"[{row['Type']} / {row['Priority']} / {row['Status']}] "
            f"-> {row['Promoted To'] or 'not promoted'}"
        )


def cmd_backlog_status(args: argparse.Namespace) -> None:
    """Safely update one backlog row status."""
    backlog_path = _backlog_path(Path.cwd())
    if not backlog_path.exists():
        raise SystemExit(f"Missing backlog file: {backlog_path}. Run `project backlog init`.")
    status = _normalize_backlog_value(args.to, BACKLOG_STATUSES, "status")
    row = _update_backlog_row(backlog_path, args.id, {"Status": status})
    print(f"Updated {row['ID']} status to {row['Status']} in {backlog_path}")


def cmd_backlog_update(args: argparse.Namespace) -> None:
    """Update non-lifecycle fields for one backlog row."""
    backlog_path = _backlog_path(Path.cwd())
    if not backlog_path.exists():
        raise SystemExit(f"Missing backlog file: {backlog_path}. Run `project backlog init`.")
    updates: dict[str, str] = {}
    if args.title is not None:
        updates["Title"] = args.title
    if args.type is not None:
        updates["Type"] = _normalize_backlog_value(args.type, BACKLOG_TYPES, "type")
    if args.priority is not None:
        updates["Priority"] = _normalize_backlog_value(
            args.priority,
            BACKLOG_PRIORITIES,
            "priority",
        )
    if args.outcome is not None:
        updates["Outcome"] = args.outcome
    if args.promoted_to is not None:
        updates["Promoted To"] = args.promoted_to
    if args.notes is not None:
        updates["Notes"] = args.notes
    if not updates:
        raise SystemExit("No backlog updates supplied.")
    row = _update_backlog_row(backlog_path, args.id, updates)
    print(f"Updated backlog row {row['ID']}: {row['Title']}")


def cmd_backlog_promote(args: argparse.Namespace) -> None:
    """Promote an accepted backlog row to a normal task or epic scaffold."""
    root = Path.cwd()
    workflow_dir = root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"
    backlog_path = _backlog_path(root)
    if not backlog_path.exists():
        raise SystemExit(f"Missing backlog file: {backlog_path}. Run `project backlog init`.")
    if not tracker_path.exists():
        raise SystemExit(f"Missing global tracker file: {tracker_path}. Run `project init`.")

    validation_issues = _backlog_validation_issues(root, backlog_path)
    if validation_issues:
        raise SystemExit(
            "Backlog must validate before promotion:\n"
            + "\n".join(f"- {issue.message}" for issue in validation_issues)
        )

    _lines, _header_idx, rows = _backlog_rows_for_update(backlog_path)
    source_row = next((row for row in rows if row["ID"] == args.id), None)
    if source_row is None:
        raise SystemExit(f"No backlog row found for ID '{args.id}' in {backlog_path}.")

    source_status = source_row["Status"]
    if source_status == "Promoted":
        raise SystemExit(f"{args.id} is already Promoted.")
    if source_status in {"Rejected", "Superseded"}:
        raise SystemExit(f"{args.id} cannot be promoted from status {source_status}.")
    if source_status != "Accepted" and not args.accept:
        raise SystemExit(
            f"{args.id} must be Accepted before promotion. "
            "Pass --accept to confirm accepting and promoting in one operation."
        )

    title = args.title or source_row["Title"]
    tasks_dir.mkdir(parents=True, exist_ok=True)

    if args.to == "task":
        task_prefix = _resolve_task_id_prefix(root, None)
        task_id = _next_workflow_id(
            root,
            tasks_dir,
            tracker_path,
            prefix=task_prefix,
            kind="tasks",
        )
        spec = TaskSpec(
            task_id=task_id,
            title=title,
            folder_suffix=slug_titlecase_dashes(title),
        )
        task_dir = tasks_dir / spec.task_folder_name
        if task_dir.exists():
            raise SystemExit(f"Task folder already exists: {task_dir}")
        task_dir.mkdir(parents=True, exist_ok=True)
        _write_file(
            task_dir / "IMPLEMENTATION.md",
            _implementation_template(spec.task_id, spec.title, root=root),
            overwrite=True,
        )
        _write_file(
            task_dir / "REQUIREMENTS.md",
            _requirements_with_backlog_source(
                _requirements_template(spec.task_id, spec.title, root=root),
                source_row,
            ),
            overwrite=True,
        )
        docs_rel = f"tasks/{spec.task_folder_name}/IMPLEMENTATION.md"
        _update_tracker(
            tracker_path,
            spec=spec,
            status="To Do",
            docs_rel_path=docs_rel,
        )
        promoted_id = task_id
        promoted_path = task_dir
    else:
        epic_id = _next_workflow_id(
            root,
            tasks_dir,
            tracker_path,
            prefix=EPIC_ID_PREFIX,
            kind="epics",
        )
        spec = TaskSpec(
            task_id=epic_id,
            title=title,
            folder_suffix=slug_titlecase_dashes(title),
        )
        epic_dir = tasks_dir / spec.task_folder_name
        if epic_dir.exists():
            raise SystemExit(f"Epic folder already exists: {epic_dir}")
        epic_dir.mkdir(parents=True, exist_ok=True)
        _write_file(
            epic_dir / "REQUIREMENTS.md",
            _requirements_with_backlog_source(
                _requirements_template(spec.task_id, spec.title, root=root),
                source_row,
            ),
            overwrite=True,
        )
        _write_file(epic_dir / "TRACKER.md", _epic_tracker_template(), overwrite=True)
        _write_file(epic_dir / "DEFERRALS.md", _epic_deferrals_template(), overwrite=True)
        _write_file(
            epic_dir / EPIC_AMENDMENTS_FILENAME, _epic_amendments_template(), overwrite=True
        )
        _write_file(
            epic_dir / "RETRO.md", _epic_retro_template(spec.task_id, spec.title), overwrite=True
        )
        _write_file(
            _intent_audit_path(epic_dir),
            _intent_audit_template(epic_dir),
            overwrite=True,
        )
        _write_acceptance_map(root, spec.task_id)
        docs_rel = f"tasks/{spec.task_folder_name}/REQUIREMENTS.md"
        _update_tracker(
            tracker_path,
            spec=spec,
            status="To Do",
            docs_rel_path=docs_rel,
        )
        promoted_id = epic_id
        promoted_path = epic_dir

    _update_backlog_row(
        backlog_path,
        args.id,
        {
            "Status": "Promoted",
            "Promoted To": promoted_id,
        },
    )
    print(f"Promoted {args.id} to {args.to} {promoted_id}: {promoted_path}")


def cmd_backlog_validate(args: argparse.Namespace) -> None:
    """Validate .project-workflow/BACKLOG.md structure and references."""
    root = Path.cwd()
    backlog_path = _backlog_path(root)
    issues = _backlog_validation_issues(root, backlog_path)
    if not issues:
        print(f"Backlog validation passed: {backlog_path}")
        return
    print(f"Backlog validation failed: {backlog_path}")
    for issue in issues:
        print(f"- {issue.message}")
    raise SystemExit(1)


def cmd_project_init(args: argparse.Namespace) -> None:
    """Bootstrap project-workflow in the current directory."""
    cwd = Path.cwd()
    initial_compatibility = _repository_compatibility(cwd)
    selected_agent = args.agent
    selected_agent_label = AGENT_CHOICES[selected_agent]
    managed_block = _managed_project_workflow_block()

    print(f"Selected agent mode: {selected_agent_label} ({selected_agent})")
    if initial_compatibility.state != "not-initialized":
        print(
            f"Project workflow is already initialized ({initial_compatibility.state}); "
            "init made no changes."
        )
        print(
            "Upgrade the existing repository with: "
            f"{CANONICAL_UPGRADE_COMMAND} --agent {selected_agent}"
        )
        return

    # Create .project-workflow structure
    project_workflow_dir = cwd / ".project-workflow"
    tasks_dir = project_workflow_dir / "tasks"
    cli_dir = project_workflow_dir / "cli"
    tracker_path = project_workflow_dir / "TRACKER.md"
    backlog_path = project_workflow_dir / "BACKLOG.md"
    guidance_path = project_workflow_dir / "guidance.md"
    config_path = project_workflow_dir / WORKFLOW_CONFIG_FILENAME
    manifest_path = project_workflow_dir / WORKFLOW_MANIFEST_FILENAME

    # Create directories
    tasks_dir.mkdir(parents=True, exist_ok=True)
    cli_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ {_ensure_delegation_runtime_ignore(cwd)}")

    # Create initial TRACKER.md if missing
    if not tracker_path.exists():
        tracker_path.write_text(_tracker_template(), encoding="utf-8")
        print(f"✓ Created: {tracker_path}")
    else:
        print(f"✓ Exists: {tracker_path}")

    # Create initial BACKLOG.md if missing. Preserve it as user-owned workflow state.
    if not backlog_path.exists():
        backlog_path.write_text(_backlog_template(), encoding="utf-8")
        print(f"✓ Created: {backlog_path}")
    else:
        print(f"✓ Exists: {backlog_path}")

    print(f"✓ {_ensure_user_guidance_file(guidance_path)}")
    print(f"✓ {_ensure_user_config_file(config_path)}")

    # Create/update the workflow CLI files in .project-workflow/cli/
    workflow_py_path = cli_dir / "workflow.py"
    workflow_sh_path = cli_dir / "workflow"

    # Copy the workflow.py to the initialized project
    workflow_py_content = _get_package_resource("templates/workflow.py")
    print(f"✓ {_ensure_generated_file(workflow_py_path, workflow_py_content)}")

    # Copy the workflow shell wrapper
    workflow_sh_content = _get_package_resource("templates/workflow")
    print(f"✓ {_ensure_generated_file(workflow_sh_path, workflow_sh_content, executable=True)}")

    for target_name, resource_name, executable in (
        ("adapter_common.py", "adapter_common.py", False),
        ("codex_adapter.py", "codex_adapter.py", False),
        ("claude_adapter.py", "claude_adapter.py", False),
    ):
        content = _get_package_resource(resource_name)
        print(f"✓ {_ensure_generated_file(cli_dir / target_name, content, executable=executable)}")
    for relative_path, executable in (
        (".claude-plugin/plugin.json", False),
        ("hooks/hooks.json", False),
        ("scripts/project-workflow-claude-hook", True),
        ("README.md", False),
    ):
        content = _get_package_resource(
            "claude_plugin/project-workflow-execution-control/" + relative_path
        )
        target = cli_dir / "claude_plugin" / "project-workflow-execution-control" / relative_path
        print(f"✓ {_ensure_generated_file(target, content, executable=executable)}")

    customize_path_hint = ".github/prompts/* files"

    if selected_agent == "claude-code":
        # Create canonical Claude project subagent layout at .claude/agents/*.md
        claude_agents_dir = cwd / ".claude" / "agents"
        claude_agents_dir.mkdir(parents=True, exist_ok=True)

        for prompt_file in PROMPT_FILES:
            prompt_content = _get_package_resource(f"prompts/{prompt_file}")
            agent_name = _prompt_filename_to_claude_agent_name(prompt_file)
            agent_path = claude_agents_dir / f"{agent_name}.md"
            agent_content = _to_claude_agent_markdown(prompt_content, agent_name)
            print(f"✓ {_ensure_generated_file(agent_path, agent_content)}")

        _remove_retired_project_workflow_path(claude_agents_dir / "project-scaffold.md")

        customize_path_hint = ".claude/agents/* files"
    elif selected_agent == "codex":
        agents_path = cwd / "AGENTS.md"
        print(f"✓ {_ensure_managed_block(agents_path, managed_block)}")

        for skill_name in CODEX_SKILL_NAMES:
            skill_path = cwd / ".agents" / "skills" / skill_name / "SKILL.md"
            skill_content = _get_package_resource(f"codex/skills/{skill_name}/SKILL.md")
            print(f"✓ {_ensure_generated_file(skill_path, skill_content)}")
        _remove_retired_project_workflow_path(cwd / ".agents" / "skills" / "project-scaffold")

        customize_path_hint = "AGENTS.md and .agents/skills/project-*"
    elif selected_agent == "cursor":
        # Create canonical Cursor project subagent layout at .cursor/agents/*.md
        cursor_agents_dir = cwd / ".cursor" / "agents"
        cursor_agents_dir.mkdir(parents=True, exist_ok=True)

        for prompt_file in PROMPT_FILES:
            prompt_content = _get_package_resource(f"prompts/{prompt_file}")
            agent_name = _prompt_filename_to_cursor_agent_name(prompt_file)
            agent_path = cursor_agents_dir / f"{agent_name}.md"
            agent_content = _to_cursor_agent_markdown(prompt_content, agent_name)
            print(f"✓ {_ensure_generated_file(agent_path, agent_content)}")

        _remove_retired_project_workflow_path(cursor_agents_dir / "project-scaffold.md")

        cursor_rule_path = cwd / ".cursor" / "rules" / "project-workflow.mdc"
        cursor_rule_content = _get_package_resource("cursor/rules/project-workflow.mdc")
        print(f"✓ {_ensure_generated_file(cursor_rule_path, cursor_rule_content)}")

        customize_path_hint = ".cursor/agents/* files and .cursor/rules/project-workflow.mdc"
    else:
        # GitHub Copilot uses generated prompts plus a managed host-file block.
        github_dir = cwd / ".github"
        prompts_dir = github_dir / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)

        copilot_instructions_path = github_dir / "copilot-instructions.md"
        print(f"✓ {_ensure_managed_block(copilot_instructions_path, managed_block)}")

        for prompt_file in PROMPT_FILES:
            prompt_path = prompts_dir / prompt_file
            prompt_content = _get_package_resource(f"prompts/{prompt_file}")
            print(f"✓ {_ensure_generated_file(prompt_path, prompt_content)}")

        _remove_retired_project_workflow_path(prompts_dir / "Scaffold.prompt.md")

    _write_workflow_manifest(manifest_path, _current_workflow_manifest())
    print(f"✓ Created: {manifest_path}")

    resulting_compatibility = _repository_compatibility(cwd)
    print(f"Repository state before init: {initial_compatibility.state}")
    print(f"Repository state after init: {resulting_compatibility.state}")
    print(f"\n✅ Project workflow initialized in {cwd}")
    print(f"   Agent mode applied: {selected_agent_label}")
    print("\nNext steps:")
    print("  • Review: .project-workflow/TRACKER.md")
    print("  • Customize user guidance: .project-workflow/guidance.md")
    print(f"  • Review generated agent assets: {customize_path_hint}")
    print("  • Create tasks: ./.project-workflow/cli/workflow task init --help")
    print("  • Create fixes: ./.project-workflow/cli/workflow fix init --help")
    print("  • Validate workflow state: ./.project-workflow/cli/workflow doctor")


def cmd_fix_init(args: argparse.Namespace) -> None:
    """Scaffold one lightweight Fix record in the shared task namespace."""
    root = Path.cwd()
    workflow_dir = root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"
    if not tracker_path.exists():
        raise SystemExit(f"Missing global tracker file: {tracker_path}. Run `project init`.")
    fix_id = _next_workflow_id(
        root,
        tasks_dir,
        tracker_path,
        prefix=FIX_ID_PREFIX,
        kind="fixes",
    )
    spec = TaskSpec(
        task_id=fix_id,
        title=args.title,
        folder_suffix=slug_titlecase_dashes(args.title),
    )
    fix_dir = tasks_dir / spec.task_folder_name
    if fix_dir.exists():
        raise SystemExit(f"Fix folder already exists: {fix_dir}")
    fix_dir.mkdir(parents=True, exist_ok=False)
    fix_text = _fix_template(fix_id, args.title, root=root)
    if args.classification:
        fix_text = _replace_fix_field(fix_text, "Classification", "Type", args.classification)
    if args.mode:
        fix_text = _replace_fix_field(fix_text, "Classification", "Mode", args.mode)
    fix_path = fix_dir / "FIX.md"
    _write_file(fix_path, fix_text, overwrite=True)
    docs_rel = f"tasks/{spec.task_folder_name}/FIX.md"
    _update_tracker(
        tracker_path,
        spec=spec,
        status="To Do",
        docs_rel_path=docs_rel,
    )
    print(f"Created Fix: {fix_dir}")
    print(f"Updated tracker: {tracker_path}")
    print(f"Assigned ID: {fix_id}")


def cmd_fix_triage(args: argparse.Namespace) -> None:
    root = Path.cwd()
    tracker_path = root / ".project-workflow" / "TRACKER.md"
    fix_id = _normalize_fix_id(args.id, root=root)
    fix_path, row = _resolve_fix_doc(root=root, tracker_path=tracker_path, fix_id=fix_id)
    if row["Status"] == "Ready":
        issues = _fix_triage_issues(root, fix_path.read_text(encoding="utf-8"))
        if issues:
            raise SystemExit(_format_readiness_block(fix_id, issues))
        print(f"{fix_id} triage gate already passed; status is Ready.")
        return
    previous, current = _update_fix_tracker_status(
        root=root,
        tracker_path=tracker_path,
        fix_id=fix_id,
        new_status="Ready",
    )
    print(f"Triaged {fix_id}: {previous} -> {current}")


def cmd_fix_status(args: argparse.Namespace) -> None:
    root = Path.cwd()
    tracker_path = root / ".project-workflow" / "TRACKER.md"
    fix_id = _normalize_fix_id(args.id, root=root)
    previous, current = _update_fix_tracker_status(
        root=root,
        tracker_path=tracker_path,
        fix_id=fix_id,
        new_status=args.to,
    )
    if previous == current:
        print(f"{fix_id} already has status '{current}'.")
    else:
        print(f"Updated {fix_id}: {previous} -> {current}")


def cmd_fix_close(args: argparse.Namespace) -> None:
    root = Path.cwd()
    tracker_path = root / ".project-workflow" / "TRACKER.md"
    fix_id = _normalize_fix_id(args.id, root=root)
    fix_path, row = _resolve_fix_doc(root=root, tracker_path=tracker_path, fix_id=fix_id)
    delivering_fix = args.disposition == "Fixed"
    if delivering_fix and row["Status"] != "Review":
        raise SystemExit(
            f"{fix_id} can only close from Review; current status is '{row['Status']}'."
        )
    if not delivering_fix and row["Status"] in {"Complete", "N/A"}:
        raise SystemExit(f"{fix_id} is already terminal with status '{row['Status']}'.")
    fix_text = fix_path.read_text(encoding="utf-8")
    triage_issues = (
        _fix_triage_issues(root, fix_text)
        if delivering_fix or row["Status"] not in {"To Do", "Blocked"}
        else []
    )
    fix_text = _replace_fix_field(fix_text, "Outcome", "Disposition", args.disposition)
    fix_text = _replace_fix_field(fix_text, "Outcome", "Decision", args.decision)
    fix_text = _replace_fix_field(fix_text, "Outcome", "Closed by", args.closed_by)
    fix_text = _replace_fix_field(
        fix_text, "Outcome", "Closed date", args.closed_date or date.today().isoformat()
    )
    closeout_issues = (
        _fix_closeout_issues(root, fix_text)
        if delivering_fix
        else _fix_non_delivery_closeout_issues(fix_text)
    )
    issues = [*triage_issues, *closeout_issues]
    if issues:
        raise SystemExit(_format_readiness_block(fix_id, list(dict.fromkeys(issues))))
    lines, _header_idx, rows = _global_tracker_rows(tracker_path)
    tracker_row = next(row_item for row_item in rows if row_item["ID"] == fix_id)
    terminal_status = "Complete" if delivering_fix else "N/A"
    tracker_row["Status"] = terminal_status
    lines[int(tracker_row["_line_idx"])] = _format_global_tracker_row(tracker_row)
    tracker_path.write_text("".join(lines), encoding="utf-8")
    fix_path.write_text(
        _replace_fix_field(fix_text, "Summary", "Status", terminal_status),
        encoding="utf-8",
    )
    print(f"Closed {fix_id} with disposition {args.disposition}.")


def _requirements_with_fix_source(text: str, fix_id: str, reason: str) -> str:
    return (
        text.rstrip()
        + "\n\n## Promotion Source\n\n"
        + f"- Promoted from Fix: {fix_id}\n"
        + f"- Reason: {reason}\n"
    )


def cmd_fix_promote(args: argparse.Namespace) -> None:
    root = Path.cwd()
    workflow_dir = root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"
    fix_id = _normalize_fix_id(args.id, root=root)
    fix_path, source_row = _resolve_fix_doc(root=root, tracker_path=tracker_path, fix_id=fix_id)
    if source_row["Status"] in {"Complete", "N/A"}:
        raise SystemExit(f"{fix_id} is already terminal and cannot be promoted.")
    title = args.title or source_row["Title"]
    if args.to == "task":
        prefix = _resolve_task_id_prefix(root, None)
        promoted_id = _next_workflow_id(root, tasks_dir, tracker_path, prefix=prefix, kind="tasks")
        spec = TaskSpec(promoted_id, title, slug_titlecase_dashes(title))
        promoted_dir = tasks_dir / spec.task_folder_name
        promoted_dir.mkdir(parents=True, exist_ok=False)
        _write_file(
            promoted_dir / "IMPLEMENTATION.md",
            _implementation_template(promoted_id, title, root=root),
            overwrite=True,
        )
        _write_file(
            promoted_dir / "REQUIREMENTS.md",
            _requirements_with_fix_source(
                _requirements_template(promoted_id, title, root=root), fix_id, args.reason
            ),
            overwrite=True,
        )
        docs_rel = f"tasks/{spec.task_folder_name}/IMPLEMENTATION.md"
    else:
        promoted_id = _next_workflow_id(
            root, tasks_dir, tracker_path, prefix=EPIC_ID_PREFIX, kind="epics"
        )
        spec = TaskSpec(promoted_id, title, slug_titlecase_dashes(title))
        promoted_dir = tasks_dir / spec.task_folder_name
        promoted_dir.mkdir(parents=True, exist_ok=False)
        _write_file(
            promoted_dir / "REQUIREMENTS.md",
            _requirements_with_fix_source(
                _requirements_template(promoted_id, title, root=root), fix_id, args.reason
            ),
            overwrite=True,
        )
        _write_file(
            promoted_dir / EPIC_CONTRACT_FILENAME,
            _epic_contract_template(promoted_id, title),
            overwrite=True,
        )
        _write_file(promoted_dir / "TRACKER.md", _epic_tracker_template(), overwrite=True)
        _write_file(promoted_dir / "DEFERRALS.md", _epic_deferrals_template(), overwrite=True)
        _write_file(
            promoted_dir / EPIC_AMENDMENTS_FILENAME,
            _epic_amendments_template(),
            overwrite=True,
        )
        _write_file(
            promoted_dir / "RETRO.md",
            _epic_retro_template(promoted_id, title),
            overwrite=True,
        )
        _write_acceptance_map(root, promoted_id)
        docs_rel = f"tasks/{spec.task_folder_name}/REQUIREMENTS.md"
    _update_tracker(
        tracker_path,
        spec=spec,
        status="To Do",
        docs_rel_path=docs_rel,
    )
    fix_text = fix_path.read_text(encoding="utf-8")
    for heading, key, value in (
        ("Outcome", "Disposition", "Promoted"),
        ("Outcome", "Decision", args.reason),
        ("Outcome", "Closed by", args.promoted_by),
        ("Outcome", "Closed date", date.today().isoformat()),
        ("Outcome", "Promoted to", promoted_id),
        ("Summary", "Status", "N/A"),
    ):
        fix_text = _replace_fix_field(fix_text, heading, key, value)
    fix_path.write_text(fix_text, encoding="utf-8")
    lines, _header_idx, rows = _global_tracker_rows(tracker_path)
    fix_row = next(row_item for row_item in rows if row_item["ID"] == fix_id)
    fix_row["Status"] = "N/A"
    lines[int(fix_row["_line_idx"])] = _format_global_tracker_row(fix_row)
    tracker_path.write_text("".join(lines), encoding="utf-8")
    print(f"Promoted {fix_id} to {args.to} {promoted_id}: {promoted_dir}")


def cmd_task_init(args: argparse.Namespace) -> None:
    """Scaffold a new task in .project-workflow/tasks/"""
    cwd = Path.cwd()

    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"

    if not tracker_path.exists():
        raise SystemExit(
            f"Missing tracker file: {tracker_path}\n"
            f"Run `{CANONICAL_INIT_COMMAND}` from the repository root first to bootstrap "
            f"the project workflow."
        )

    task_prefix = _resolve_task_id_prefix(cwd, args.prefix)
    task_id = _next_workflow_id(
        cwd,
        tasks_dir,
        tracker_path,
        prefix=task_prefix,
        kind="tasks",
    )
    existing_task_dirs = [p for p in tasks_dir.glob(f"{task_id}-*") if p.is_dir()]
    if args.folder_suffix:
        folder_suffix = args.folder_suffix
    elif existing_task_dirs:
        if len(existing_task_dirs) > 1:
            raise SystemExit(
                f"Multiple existing task folders found for {task_id}: "
                + ", ".join(p.name for p in existing_task_dirs)
                + ". Use --folder-suffix to disambiguate."
            )
        folder_suffix = existing_task_dirs[0].name[len(task_id) + 1 :]
    else:
        folder_suffix = slug_titlecase_dashes(args.title)
    spec = TaskSpec(task_id=task_id, title=args.title, folder_suffix=folder_suffix)
    branch_name: str | None = None

    if args.create_branch:
        _ensure_clean_git(cwd)

        base_branch = args.base_branch
        branch_name = f"{args.branch_prefix}{spec.task_id}-{slug_kebab_lower(spec.title)}"

        # Ensure base branch exists locally and is checked out.
        _run_git(["checkout", base_branch], cwd=cwd)
        _run_git(["pull"], cwd=cwd)

        # Create and switch.
        _run_git(["checkout", "-b", branch_name], cwd=cwd)

    task_dir = tasks_dir / spec.task_folder_name
    impl_path = task_dir / "IMPLEMENTATION.md"
    reqs_path = task_dir / "REQUIREMENTS.md"

    task_dir.mkdir(parents=True, exist_ok=True)
    if args.overwrite or not impl_path.exists():
        _write_file(
            impl_path,
            _implementation_template(spec.task_id, spec.title, root=cwd),
            overwrite=True,
        )
    if args.overwrite or not reqs_path.exists():
        _write_file(
            reqs_path,
            _requirements_template(spec.task_id, spec.title, root=cwd),
            overwrite=True,
        )

    docs_rel = f"tasks/{spec.task_folder_name}/IMPLEMENTATION.md"
    if args.update_tracker:
        _update_tracker(tracker_path, spec=spec, status=args.status, docs_rel_path=docs_rel)

    print(f"Created task: {task_dir}")
    if args.update_tracker:
        print(f"Updated tracker: {tracker_path}")

    if branch_name is not None:
        print(f"Created branch: {branch_name}")
    print(f"Assigned ID: {spec.task_id}")


def cmd_task_status(args: argparse.Namespace) -> None:
    """Safely update one global tracker task status."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"

    if not tracker_path.exists():
        raise SystemExit(
            f"Missing tracker file: {tracker_path}\n"
            f"Run `{CANONICAL_INIT_COMMAND}` from the repository root first to bootstrap "
            f"the project workflow."
        )

    task_id = _normalize_task_status_id(args.id, root=cwd)
    previous, current = _update_global_tracker_row_status(
        root=cwd,
        tracker_path=tracker_path,
        row_id=task_id,
        new_status=args.to,
        force=args.force,
        reason=args.reason,
    )

    if previous == current:
        print(f"{task_id} already has status '{current}' in {tracker_path}")
    else:
        print(f"Updated {task_id}: {previous} -> {current} in {tracker_path}")
        if args.force:
            print(f"Forced transition reason: {args.reason.strip()}")


def cmd_task_approval_summary(args: argparse.Namespace) -> None:
    """Render the meaning-first approval synopsis for one standalone task."""
    cwd = Path.cwd()
    tracker_path = cwd / ".project-workflow" / "TRACKER.md"
    if not tracker_path.exists():
        raise SystemExit(f"Missing tracker file: {tracker_path}")
    task_id = _normalize_task_status_id(args.id, root=cwd)
    requirements_path, _implementation_path, _row = _resolve_global_task_docs(
        root=cwd,
        tracker_path=tracker_path,
        task_id=task_id,
    )
    requirements_text = requirements_path.read_text(encoding="utf-8")
    try:
        summary = _format_intent_approval_summary(requirements_text)
    except ValueError as exc:
        raise SystemExit(f"{task_id} approval synopsis is not ready: {exc}") from exc
    print(summary, end="")


def cmd_task_approve_requirements(args: argparse.Namespace) -> None:
    """Record an owner approval envelope for one standalone task."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    if not tracker_path.exists():
        raise SystemExit(
            f"Missing tracker file: {tracker_path}\n"
            f"Run `{CANONICAL_INIT_COMMAND}` from the repository root first to bootstrap "
            f"the project workflow."
        )

    task_id = _normalize_task_status_id(args.id, root=cwd)
    requirements_path, _implementation_path, _row = _resolve_global_task_docs(
        root=cwd,
        tracker_path=tracker_path,
        task_id=task_id,
    )
    requirements_text = requirements_path.read_text(encoding="utf-8")
    readiness_issues = (
        _discovery_readiness_issues(requirements_text)
        if _is_discovery_work(requirements_text)
        else _requirements_readiness_issues(requirements_text)
    )
    if readiness_issues:
        raise SystemExit(_format_readiness_block(task_id, readiness_issues))
    updated = _requirements_with_approval_envelope(
        requirements_text,
        approved_by=args.approved_by,
        source=args.source,
        decomposition=False,
        implementation=True,
    )
    requirements_path.write_text(updated, encoding="utf-8")
    print(f"Recorded owner approval envelope for {task_id}: {requirements_path}")
    if _intent_contract_mode(requirements_text) == "full":
        print(f"Approved Intent: {_intent_plain_text(requirements_text)}")


def cmd_task_adopt(args: argparse.Namespace) -> None:
    """Adopt one pre-existing standalone task into current approval gates."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    if not tracker_path.exists():
        raise SystemExit(
            f"Missing tracker file: {tracker_path}\n"
            f"Run `{CANONICAL_INIT_COMMAND}` from the repository root first to bootstrap "
            f"the project workflow."
        )

    task_id = _normalize_task_status_id(args.id, root=cwd)
    requirements_path, _implementation_path, _row = _resolve_global_task_docs(
        root=cwd,
        tracker_path=tracker_path,
        task_id=task_id,
    )
    requirements_text = requirements_path.read_text(encoding="utf-8")
    updated = _requirements_with_legacy_adoption(
        requirements_text,
        approved_by=args.approved_by,
        source=args.source,
        decomposition=False,
        implementation=True,
        evidence_refreshed=args.evidence_refreshed,
    )
    requirements_path.write_text(updated, encoding="utf-8")
    print(f"Adopted legacy task requirements for {task_id}: {requirements_path}")
    if not args.evidence_refreshed:
        print("Pre-adoption inferred evidence remains untrusted until refreshed.")


def cmd_task_ready(args: argparse.Namespace) -> None:
    """Validate standalone task implementation readiness."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    if not tracker_path.exists():
        raise SystemExit(
            f"Missing tracker file: {tracker_path}\n"
            f"Run `{CANONICAL_INIT_COMMAND}` from the repository root first to bootstrap "
            f"the project workflow."
        )

    task_id = _normalize_task_status_id(args.id, root=cwd)
    requirements_path, implementation_path, _row = _resolve_global_task_docs(
        root=cwd,
        tracker_path=tracker_path,
        task_id=task_id,
    )
    requirements_text = requirements_path.read_text(encoding="utf-8")
    implementation_text = implementation_path.read_text(encoding="utf-8")
    approval_issues: list[str] = []
    if not _is_discovery_work(requirements_text, implementation_text):
        approval_issues = _approval_envelope_issues(
            requirements_text,
            require_implementation=True,
        )
    readiness_issues = _task_ready_issues_for_paths(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
    )
    issues = [*approval_issues, *readiness_issues]
    if issues:
        raise SystemExit(_format_readiness_block(task_id, issues))
    print(f"{task_id} readiness gate passed.")


def cmd_epic_init(args: argparse.Namespace) -> None:
    """Scaffold a new epic in .project-workflow/tasks/."""
    cwd = Path.cwd()

    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"

    if not tracker_path.exists():
        raise SystemExit(
            f"Missing tracker file: {tracker_path}\n"
            f"Run `{CANONICAL_INIT_COMMAND}` from the repository root first to bootstrap "
            f"the project workflow."
        )

    epic_id = _resolve_epic_id(cwd, tasks_dir, tracker_path, title=args.title)
    existing_epic_dirs = [p for p in tasks_dir.glob(f"{epic_id}-*") if p.is_dir()]
    if args.folder_suffix:
        folder_suffix = args.folder_suffix
    elif existing_epic_dirs:
        if len(existing_epic_dirs) > 1:
            raise SystemExit(
                f"Multiple existing epic folders found for {epic_id}: "
                + ", ".join(p.name for p in existing_epic_dirs)
                + ". Use --folder-suffix to disambiguate."
            )
        folder_suffix = existing_epic_dirs[0].name[len(epic_id) + 1 :]
    else:
        folder_suffix = slug_titlecase_dashes(args.title)
    spec = TaskSpec(task_id=epic_id, title=args.title, folder_suffix=folder_suffix)

    epic_dir = tasks_dir / spec.task_folder_name
    reqs_path = epic_dir / "REQUIREMENTS.md"
    contract_path = epic_dir / EPIC_CONTRACT_FILENAME
    epic_tracker_path = epic_dir / "TRACKER.md"
    deferrals_path = epic_dir / "DEFERRALS.md"
    amendments_path = epic_dir / EPIC_AMENDMENTS_FILENAME
    retro_path = epic_dir / "RETRO.md"

    epic_dir.mkdir(parents=True, exist_ok=True)
    if args.overwrite or not reqs_path.exists():
        _write_file(
            reqs_path,
            _requirements_template(spec.task_id, spec.title, root=cwd),
            overwrite=True,
        )
    if args.overwrite or not contract_path.exists():
        _write_file(
            contract_path,
            _epic_contract_template(spec.task_id, spec.title),
            overwrite=True,
        )
    if args.overwrite or not epic_tracker_path.exists():
        _write_file(epic_tracker_path, _epic_tracker_template(), overwrite=True)
    if args.overwrite or not deferrals_path.exists():
        _write_file(deferrals_path, _epic_deferrals_template(), overwrite=True)
    if args.overwrite or not amendments_path.exists():
        _write_file(amendments_path, _epic_amendments_template(), overwrite=True)
    if args.overwrite or not retro_path.exists():
        _write_file(retro_path, _epic_retro_template(spec.task_id, spec.title), overwrite=True)
    intent_audit_path = _intent_audit_path(epic_dir)
    if args.overwrite or not intent_audit_path.exists():
        _write_file(
            intent_audit_path,
            _intent_audit_template(epic_dir),
            overwrite=True,
        )
    map_path = _write_acceptance_map(cwd, spec.task_id)

    docs_rel = f"tasks/{spec.task_folder_name}/REQUIREMENTS.md"
    row_written = _update_tracker(
        tracker_path,
        spec=spec,
        status=args.status,
        docs_rel_path=docs_rel,
        on_duplicate="skip",
    )

    print(f"Created epic: {epic_dir}")
    print(f"Wrote acceptance map: {map_path}")
    if row_written:
        print(f"Updated tracker: {tracker_path}")
    else:
        print(f"Tracker already had row for ID {spec.task_id}; no duplicate added.")
    print(f"Assigned ID: {spec.task_id}")


def cmd_epic_amend(args: argparse.Namespace) -> None:
    """Record an approved epic amendment and append its proposed child row."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    config = _load_workflow_config(cwd)

    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    requirements_issues = _requirements_approval_issues_for_path(
        epic_dir / "REQUIREMENTS.md",
        require_decomposition=True,
    )
    if requirements_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, requirements_issues))
    contract_issues = _epic_contract_issues_for_path(epic_dir)
    if contract_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, contract_issues))

    if _approval_source_invalid(args.approved_by):
        raise SystemExit("--approved-by must name the owner who approved the amendment.")
    if _approval_source_invalid(args.reason):
        raise SystemExit("--reason must describe the material scope/provenance decision.")
    if _approval_source_invalid(args.source):
        raise SystemExit("--source must identify the non-agent amendment approval source.")
    if not _valid_workflow_ref_id(args.id, config=config):
        raise SystemExit(f"{args.id} is not a valid configured workflow ID.")
    if not _extract_ac_ids(args.parent_acs):
        raise SystemExit("--parent-acs must include one or more parent AC IDs.")

    epic_tracker_path = epic_dir / "TRACKER.md"
    amendments_path = _epic_amendments_path(epic_dir)
    parent_acs = _normalize_ac_list(args.parent_acs)
    amendment_row = {
        "ID": args.id,
        "Title": args.title,
        "Parent ACs": parent_acs,
        "Approved By": args.approved_by,
        "Decision Date": date.today().isoformat(),
        "Reason": args.reason,
        "Source": args.source,
    }
    tracker_row = {
        "ID": args.id,
        "Title": args.title,
        "Status": "Proposed",
        "Type": args.type,
        "Parent ACs": parent_acs,
        "Docs": "",
        "Branch": "",
        "Notes": f"Amendment: {args.reason}",
    }

    _append_epic_amendment_row(amendments_path, amendment_row)
    _append_epic_tracker_rows(epic_tracker_path, [tracker_row])
    map_path = _write_acceptance_map(cwd, args.epic_id)
    print(f"Recorded amendment for {args.id}: {amendments_path}")
    print(f"Added Proposed child row to {epic_tracker_path}")
    print(f"Refreshed acceptance map: {map_path}")


def cmd_epic_approve(args: argparse.Namespace) -> None:
    """Approve a proposed epic child row by updating Status to Approved."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"

    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    epic_tracker_path = epic_dir / "TRACKER.md"
    if not epic_tracker_path.exists():
        raise SystemExit(f"Missing epic tracker: {epic_tracker_path}")
    requirements_path = epic_dir / "REQUIREMENTS.md"
    approval_issues = _requirements_approval_issues_for_path(
        requirements_path,
        require_decomposition=True,
    )
    if approval_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, approval_issues))
    contract_issues = _epic_contract_issues_for_path(epic_dir)
    if contract_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, contract_issues))

    target = _epic_tracker_row_by_id(epic_tracker_path, args.id)
    _require_decomposition_plan_authority(epic_dir, target)
    _update_epic_tracker_row_status(
        epic_tracker_path,
        row_id=args.id,
        expected_from="Proposed",
        new_status="Approved",
    )
    map_path = _write_acceptance_map(cwd, args.epic_id)
    print(f"Approved epic row {args.id} in {epic_tracker_path}")
    print(f"Refreshed acceptance map: {map_path}")


def cmd_epic_approval_summary(args: argparse.Namespace) -> None:
    """Render the meaning-first approval synopsis for one Epic."""
    cwd = Path.cwd()
    tasks_dir = cwd / ".project-workflow" / "tasks"
    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    requirements_path = epic_dir / "REQUIREMENTS.md"
    if not requirements_path.exists():
        raise SystemExit(f"Missing epic requirements file: {requirements_path}")
    requirements_text = requirements_path.read_text(encoding="utf-8")
    try:
        summary = _format_intent_approval_summary(requirements_text)
    except ValueError as exc:
        raise SystemExit(f"{args.epic_id} approval synopsis is not ready: {exc}") from exc
    print(summary, end="")


def cmd_epic_intent_audit(args: argparse.Namespace) -> None:
    """Inspect the current sourced Intent audit without mutating workflow state."""
    cwd = Path.cwd()
    epic_dir = _resolve_epic_dir(cwd / ".project-workflow" / "tasks", args.epic_id)
    evaluation = _intent_audit_evaluation(epic_dir)
    if args.format == "json":
        print(json.dumps(evaluation, indent=2, sort_keys=True))
    else:
        print(_format_intent_audit_human(args.epic_id, evaluation))


def cmd_epic_approve_requirements(args: argparse.Namespace) -> None:
    """Record an owner approval envelope for one epic."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"

    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    requirements_path = epic_dir / "REQUIREMENTS.md"
    if not requirements_path.exists():
        raise SystemExit(f"Missing epic requirements file: {requirements_path}")

    requirements_text = requirements_path.read_text(encoding="utf-8")
    readiness_issues = _epic_requirements_readiness_issues(requirements_text)
    if readiness_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, readiness_issues))
    updated = _requirements_with_approval_envelope(
        requirements_text,
        approved_by=args.approved_by,
        source=args.source,
        decomposition=True,
        implementation=False,
    )
    requirements_path.write_text(updated, encoding="utf-8")
    print(f"Recorded owner approval envelope for {args.epic_id}: {requirements_path}")
    if _intent_contract_mode(requirements_text) == "full":
        print(f"Approved Intent: {_intent_plain_text(requirements_text)}")


def cmd_epic_adopt(args: argparse.Namespace) -> None:
    """Adopt one pre-existing epic into current approval gates."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"

    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    requirements_path = epic_dir / "REQUIREMENTS.md"
    if not requirements_path.exists():
        raise SystemExit(f"Missing epic requirements file: {requirements_path}")
    requirements_text = requirements_path.read_text(encoding="utf-8")
    updated = _requirements_with_legacy_adoption(
        requirements_text,
        approved_by=args.approved_by,
        source=args.source,
        decomposition=True,
        implementation=False,
        evidence_refreshed=args.evidence_refreshed,
    )
    requirements_path.write_text(updated, encoding="utf-8")
    amendments_path = _epic_amendments_path(epic_dir)
    if not amendments_path.exists():
        amendments_path.write_text(_epic_amendments_template(), encoding="utf-8")
    print(f"Adopted legacy epic requirements for {args.epic_id}: {requirements_path}")
    print(f"Ensured amendment log exists: {amendments_path}")
    if not args.evidence_refreshed:
        print("Pre-adoption inferred evidence remains untrusted until refreshed.")


def cmd_epic_ready(args: argparse.Namespace) -> None:
    """Validate epic requirements readiness before decomposition."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    requirements_path = epic_dir / "REQUIREMENTS.md"
    if not requirements_path.exists():
        raise SystemExit(f"Missing epic requirements file: {requirements_path}")
    requirements_text = requirements_path.read_text(encoding="utf-8")
    readiness_issues = [
        *_epic_requirements_readiness_issues(requirements_text),
        *_approval_envelope_issues(requirements_text, require_decomposition=True),
        *_epic_contract_issues(epic_dir, requirements_text),
    ]
    if readiness_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, readiness_issues))
    print(f"{args.epic_id} epic readiness gate passed.")


def cmd_epic_ready_child(args: argparse.Namespace) -> None:
    """Validate one epic child task readiness before implementation/testing."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    epic_tracker_path = epic_dir / "TRACKER.md"
    if not epic_tracker_path.exists():
        raise SystemExit(f"Missing epic tracker: {epic_tracker_path}")
    parent_approval_issues = _requirements_approval_issues_for_path(
        epic_dir / "REQUIREMENTS.md",
        require_decomposition=True,
    )
    if parent_approval_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, parent_approval_issues))

    requirements_path, implementation_path, row = _resolve_epic_child_docs(
        root=cwd,
        epic_tracker_path=epic_tracker_path,
        row_id=args.id,
    )
    _require_decomposition_plan_authority(epic_dir, row)
    parent_ac_ids = _extract_ac_ids(_extract_parent_ac_coverage(row))
    readiness_issues = _task_ready_issues_for_paths(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
        parent_ac_ids=parent_ac_ids,
    )
    readiness_issues.extend(_intent_audit_gate_issues(epic_dir))
    if readiness_issues:
        raise SystemExit(_format_readiness_block(args.id, readiness_issues))
    print(f"{args.id} readiness gate passed.")


def cmd_epic_status(args: argparse.Namespace) -> None:
    """Safely update one epic tracker row status."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    epic_tracker_path = epic_dir / "TRACKER.md"
    if not epic_tracker_path.exists():
        raise SystemExit(f"Missing epic tracker: {epic_tracker_path}")
    parent_approval_issues = _requirements_approval_issues_for_path(
        epic_dir / "REQUIREMENTS.md",
        require_decomposition=True,
    )
    if parent_approval_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, parent_approval_issues))
    target = _epic_tracker_row_by_id(epic_tracker_path, args.id)
    if target["Status"] in EPIC_CHILD_GATED_STATUSES or args.to in EPIC_CHILD_GATED_STATUSES:
        contract_issues = _epic_contract_issues_for_path(epic_dir)
        if contract_issues:
            raise SystemExit(_format_readiness_block(args.epic_id, contract_issues))
        _require_decomposition_plan_authority(epic_dir, target)
    if args.to in {"Review", "Complete"}:
        audit_issues = _intent_audit_gate_issues(epic_dir)
        if audit_issues:
            raise SystemExit(_format_readiness_block(args.id, audit_issues))
    previous, current = _update_epic_child_status(
        root=cwd,
        epic_tracker_path=epic_tracker_path,
        row_id=args.id,
        new_status=args.to,
        force=args.force,
        reason=args.reason,
    )
    if previous == current:
        print(f"{args.id} already has status '{current}' in {epic_tracker_path}")
    else:
        print(f"Updated {args.id}: {previous} -> {current} in {epic_tracker_path}")
        if args.force:
            print(f"Forced transition reason: {args.reason.strip()}")
    map_path = _write_acceptance_map(cwd, args.epic_id)
    print(f"Refreshed acceptance map: {map_path}")


def cmd_epic_lifecycle(args: argparse.Namespace) -> None:
    """Safely update one global epic tracker lifecycle status."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    if not tracker_path.exists():
        raise SystemExit(f"Missing global tracker file: {tracker_path}")

    gate_issues = _epic_lifecycle_gate_issues(cwd, args.epic_id, args.to)
    if gate_issues:
        lines = [
            f"{args.epic_id} cannot move to {args.to}:",
            *[f"- {issue}" for issue in gate_issues],
        ]
        raise SystemExit("\n".join(lines))

    previous, current = _update_global_epic_status(
        tracker_path,
        epic_id=args.epic_id,
        new_status=args.to,
    )
    if previous == current:
        print(f"{args.epic_id} already has status '{current}' in {tracker_path}")
    else:
        print(f"Updated {args.epic_id}: {previous} -> {current} in {tracker_path}")


def cmd_epic_decompose(args: argparse.Namespace) -> None:
    """Generate Proposed child rows and DECOMPOSITION.md without scaffolding child folders."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"

    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    requirements_path = epic_dir / "REQUIREMENTS.md"
    epic_tracker_path = epic_dir / "TRACKER.md"

    if not requirements_path.exists():
        raise SystemExit(f"Missing epic requirements file: {requirements_path}")
    if not epic_tracker_path.exists():
        raise SystemExit(f"Missing epic tracker: {epic_tracker_path}")
    if not tracker_path.exists():
        raise SystemExit(f"Missing global tracker file: {tracker_path}")

    requirements_text = requirements_path.read_text(encoding="utf-8")
    readiness_issues = _epic_requirements_readiness_issues(requirements_text)
    approval_issues = _approval_envelope_issues(
        requirements_text,
        require_decomposition=True,
    )
    if approval_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, approval_issues))
    if readiness_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, readiness_issues))
    contract_issues = _epic_contract_issues(epic_dir, requirements_text)
    if contract_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, contract_issues))
    proposed_child_rows = _proposed_child_work_rows(requirements_text)
    if proposed_child_rows:
        candidates = [
            (
                row["Proposed Child"].rstrip("."),
                _normalize_ac_list(row["Parent ACs"]),
                "Proposed Child Work",
                row.get("Dependencies", ""),
            )
            for row in proposed_child_rows[: args.limit]
        ]
    else:
        candidates = [
            (title, ac_id or "", "Generated from REQUIREMENTS.md", "")
            for title, ac_id in _decompose_epic_requirements_to_titles(
                requirements_text, limit=args.limit
            )
        ]
    if not candidates:
        raise SystemExit(
            "No decomposition candidates found in epic REQUIREMENTS.md. "
            "Add list items under '## Requirements (Outcome-Focused)' or "
            "'## Acceptance Criteria (Verifiable)' first."
        )

    config = _load_workflow_config(cwd)
    forced_prefix = _resolve_task_id_prefix(cwd, args.prefix) if args.prefix else None
    occupied_ids_by_prefix = {
        prefix: _used_ids_for_prefix(tasks_dir, tracker_path, prefix=prefix)
        for prefix in config.task_id_prefixes
    }
    _lines, _header_idx, epic_rows = _epic_tracker_rows(epic_tracker_path)

    rows_to_add: list[dict[str, str]] = []
    plan_rows: list[dict[str, str]] = []
    for title, ac_id, source, dependencies in candidates:
        if forced_prefix:
            child_prefix = forced_prefix
            classification_note = f"Prefix {child_prefix}: forced by --prefix"
        else:
            child_prefix, classification_note = _classify_task_prefix(title, config)
        occupied_ids = occupied_ids_by_prefix.setdefault(
            child_prefix,
            _used_ids_for_prefix(tasks_dir, tracker_path, prefix=child_prefix),
        )
        next_id = _next_task_id_from_used(
            occupied_ids,
            prefix=child_prefix,
            config=config,
            kind="tasks",
        )
        occupied_ids.add(next_id)
        notes = f"{classification_note}; Decomposition plan: {source}"
        if ac_id:
            notes = f"Covers {ac_id}; {notes}"
        plan_rows.append(
            {
                "ID": next_id,
                "Title": title,
                "Parent ACs": ac_id or "",
                "Source": source,
                "Dependencies": dependencies,
            }
        )
        rows_to_add.append(
            {
                "ID": next_id,
                "Title": title,
                "Status": "Proposed",
                "Type": args.item_type,
                "Parent ACs": ac_id or "",
                "Docs": "",
                "Branch": "",
                "Notes": notes,
            }
        )

    plan_path = _decomposition_plan_path(epic_dir)
    plan_path.write_text(
        _format_decomposition_plan(
            epic_id=args.epic_id,
            requirements_text=requirements_text,
            rows=plan_rows,
        ),
        encoding="utf-8",
    )
    _append_epic_tracker_rows(epic_tracker_path, rows_to_add)
    map_path = _write_acceptance_map(cwd, args.epic_id)
    print(f"Added {len(rows_to_add)} Proposed row(s) to {epic_tracker_path}")
    print(f"Wrote decomposition plan: {plan_path}")
    print(f"Refreshed acceptance map: {map_path}")
    print("No child task folders were created in this decomposition step.")
    parent_ac_ids = _extract_parent_ac_ids_from_requirements(requirements_text)
    mapped_ac_ids = _extract_parent_ac_ids_from_epic_rows([*epic_rows, *rows_to_add])
    unmapped_ac_ids = sorted(parent_ac_ids - mapped_ac_ids)
    if unmapped_ac_ids:
        print("WARNING: Unmapped parent ACs after decomposition: " + ", ".join(unmapped_ac_ids))
    elif parent_ac_ids:
        print("Parent AC coverage mapped: " + ", ".join(sorted(parent_ac_ids)))


def cmd_epic_scaffold_child(args: argparse.Namespace) -> None:
    """Scaffold one approved child row from an epic tracker."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"

    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    epic_tracker_path = epic_dir / "TRACKER.md"
    if not epic_tracker_path.exists():
        raise SystemExit(f"Missing epic tracker: {epic_tracker_path}")

    lines, _header_idx, rows = _epic_tracker_rows(epic_tracker_path)
    target: dict[str, str] | None = None
    for row in rows:
        if row["ID"] == args.id:
            target = row
            break

    if target is None:
        raise SystemExit(f"No epic tracker row found for ID '{args.id}' in {epic_tracker_path}.")
    if target["Status"] != "Approved":
        raise SystemExit(
            f"Row {args.id} is '{target['Status']}'. "
            "Only rows with status 'Approved' can be scaffolded."
        )
    parent_approval_issues = _requirements_approval_issues_for_path(
        epic_dir / "REQUIREMENTS.md",
        require_decomposition=True,
    )
    if parent_approval_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, parent_approval_issues))
    contract_issues = _epic_contract_issues_for_path(epic_dir)
    if contract_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, contract_issues))
    _require_decomposition_plan_authority(epic_dir, target)

    child_spec = TaskSpec(
        task_id=target["ID"],
        title=target["Title"],
        folder_suffix=slug_titlecase_dashes(target["Title"]),
    )
    branch_name: str | None = None

    if args.create_branch:
        _ensure_clean_git(cwd)
        epic_branch = args.epic_branch
        branch_name = (
            f"{args.branch_prefix}{child_spec.task_id}-{slug_kebab_lower(child_spec.title)}"
        )

        if not _branch_exists(cwd, epic_branch):
            raise SystemExit(
                f"Epic branch '{epic_branch}' was not found. "
                "Child branches for epic-managed tasks must branch from the epic branch "
                "and never fall back to a base branch. "
                "Create or checkout the epic branch first, for example: "
                f"git checkout -b {epic_branch} develop"
            )

        _run_git(["checkout", epic_branch], cwd=cwd)
        if _branch_exists(cwd, branch_name):
            _run_git(["checkout", branch_name], cwd=cwd)
        else:
            _run_git(["checkout", "-b", branch_name], cwd=cwd)
    child_dir = epic_dir / child_spec.task_folder_name
    impl_path = child_dir / "IMPLEMENTATION.md"
    reqs_path = child_dir / "REQUIREMENTS.md"
    evidence_path = child_dir / STRUCTURED_EVIDENCE_FILENAME
    parent_ac_coverage = _extract_parent_ac_coverage(target)
    child_charter = _format_child_charter_from_contract(
        epic_dir=epic_dir,
        parent_ac_coverage=parent_ac_coverage,
    )

    child_dir.mkdir(parents=True, exist_ok=True)
    if args.overwrite or not impl_path.exists():
        _write_file(
            impl_path,
            _epic_child_implementation_template(
                child_spec.task_id,
                child_spec.title,
                parent_ac_coverage,
                child_charter,
                root=cwd,
            ),
            overwrite=True,
        )
    if args.overwrite or not reqs_path.exists():
        _write_file(
            reqs_path,
            _epic_child_requirements_template(
                child_spec.task_id,
                child_spec.title,
                parent_ac_coverage,
                child_charter,
                root=cwd,
            ),
            overwrite=True,
        )
    if args.overwrite or not evidence_path.exists():
        _write_file(
            evidence_path,
            _structured_evidence_template(child_spec.task_id, parent_ac_coverage),
            overwrite=True,
        )

    target["Docs"] = f"tasks/{epic_dir.name}/{child_spec.task_folder_name}/IMPLEMENTATION.md"
    if branch_name is not None:
        target["Branch"] = branch_name
    target["Status"] = "In Progress"
    line_idx = int(target["_line_idx"])
    lines[line_idx] = _format_epic_tracker_row(target)
    epic_tracker_path.write_text("".join(lines), encoding="utf-8")
    map_path = _write_acceptance_map(cwd, args.epic_id)

    print(f"Scaffolded epic child: {child_dir}")
    print(f"Updated epic tracker: {epic_tracker_path}")
    print(f"Refreshed acceptance map: {map_path}")
    if branch_name is not None:
        print(f"Child branch active from epic branch {args.epic_branch}: {branch_name}")


def cmd_epic_audit(args: argparse.Namespace) -> None:
    """Generate an epic acceptance audit artifact."""
    cwd = Path.cwd()
    epic_dir, audit_rows, gaps = _epic_audit_rows(cwd, args.epic_id)
    audit_path = epic_dir / "ACCEPTANCE-AUDIT.md"
    audit_path.write_text(_format_acceptance_audit(args.epic_id, audit_rows), encoding="utf-8")
    map_path = _write_acceptance_map(cwd, args.epic_id)
    print(f"Wrote acceptance audit: {audit_path}")
    print(f"Refreshed acceptance map: {map_path}")
    if gaps:
        print("WARNING: Epic acceptance gaps remain:")
        for gap in gaps:
            print(f"- {gap}")
    else:
        print("Epic acceptance audit passed.")


def cmd_epic_closeout(args: argparse.Namespace) -> None:
    """Validate epic closeout gates and optionally mark the global epic row Complete."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    epic_dir, audit_rows, gaps = _epic_audit_rows(cwd, args.epic_id)
    gaps = [
        *_requirements_approval_issues_for_path(
            epic_dir / "REQUIREMENTS.md",
            require_decomposition=True,
        ),
        *gaps,
    ]
    gaps = [*gaps, *_epic_retro_issues(epic_dir)]
    audit_path = epic_dir / "ACCEPTANCE-AUDIT.md"
    audit_path.write_text(_format_acceptance_audit(args.epic_id, audit_rows), encoding="utf-8")
    map_path = _write_acceptance_map(cwd, args.epic_id)
    if gaps:
        print(f"Wrote acceptance audit: {audit_path}")
        print(f"Refreshed acceptance map: {map_path}")
        print(_epic_closeout_summary(audit_rows, gaps, complete_requested=args.complete))
        print("Epic closeout blocked by acceptance gaps:")
        for gap in gaps:
            print(f"- {gap}")
        raise SystemExit(1)

    print(f"Wrote acceptance audit: {audit_path}")
    print(f"Refreshed acceptance map: {map_path}")
    print(_epic_closeout_summary(audit_rows, gaps, complete_requested=args.complete))
    print("Epic closeout gates passed.")
    if args.complete:
        previous, current = _update_global_epic_status(
            tracker_path,
            epic_id=args.epic_id,
            new_status="Complete",
        )
        print(f"Updated {args.epic_id}: {previous} -> {current} in {tracker_path}")
    else:
        print("Global epic status was not changed. Re-run with --complete to mark Complete.")


def _add_delegate_plan_arguments(command_parser: argparse.ArgumentParser) -> None:
    command_parser.add_argument(
        "--id",
        action="append",
        required=True,
        help="Exactly one existing approved Epic or Task ID; repeated IDs are rejected",
    )
    command_parser.add_argument(
        "--unit",
        action="append",
        help="Select one approved execution unit; repeat for a dependency-closed subset",
    )
    command_parser.add_argument(
        "--requested-concurrency",
        type=int,
        default=1,
        help="Requested execution concurrency (default: 1)",
    )
    command_parser.add_argument(
        "--available-child-capacity",
        type=int,
        default=0,
        help="Observed available child slots, excluding the coordinator (default: 0)",
    )
    command_parser.add_argument(
        "--observed-capability",
        action="append",
        choices=DELEGATION_CAPABILITIES,
        help=(
            "Runtime-observed verified host capability; repeat as needed. This legacy-compatible "
            "flag is the verified state in the tri-state capability matrix."
        ),
    )
    command_parser.add_argument(
        "--unsupported-capability",
        action="append",
        choices=DELEGATION_CAPABILITIES,
        help="Runtime-observed unsupported host capability; repeat as needed",
    )
    command_parser.add_argument(
        "--capability-source",
        default="not observed",
        help=(
            "Dated adapter observation provenance containing YYYY-MM-DD; required when "
            "capabilities are supplied"
        ),
    )
    command_parser.add_argument(
        "--persistent-task-authority",
        help=(
            "Explicit owner-authority provenance required before an Epic plan may advise "
            "persistent task execution"
        ),
    )
    command_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format (default: human)",
    )
