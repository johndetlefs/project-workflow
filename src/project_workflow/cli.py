"""Canonical Project Workflow cli runtime."""

from __future__ import annotations

import argparse

from .commands import (
    _add_delegate_plan_arguments,
    cmd_backlog_add,
    cmd_backlog_init,
    cmd_backlog_list,
    cmd_backlog_promote,
    cmd_backlog_status,
    cmd_backlog_update,
    cmd_backlog_validate,
    cmd_coordinate_boundary,
    cmd_coordinate_checkpoint,
    cmd_coordinate_context_record,
    cmd_coordinate_init,
    cmd_coordinate_phase,
    cmd_coordinate_preflight,
    cmd_coordinate_status,
    cmd_coordinate_verification_capabilities,
    cmd_coordinate_verification_init,
    cmd_coordinate_verification_preflight,
    cmd_coordinate_verification_record,
    cmd_coordinate_verification_run,
    cmd_delegate_plan,
    cmd_delegate_state_init,
    cmd_delegate_state_reconcile,
    cmd_delegate_status,
    cmd_doctor,
    cmd_epic_adopt,
    cmd_epic_amend,
    cmd_epic_approval_summary,
    cmd_epic_approve,
    cmd_epic_approve_requirements,
    cmd_epic_audit,
    cmd_epic_closeout,
    cmd_epic_decompose,
    cmd_epic_init,
    cmd_epic_intent_audit,
    cmd_epic_lifecycle,
    cmd_epic_ready,
    cmd_epic_ready_child,
    cmd_epic_scaffold_child,
    cmd_epic_status,
    cmd_execute,
    cmd_fix_close,
    cmd_fix_init,
    cmd_fix_promote,
    cmd_fix_status,
    cmd_fix_triage,
    cmd_project_init,
    cmd_release,
    cmd_smoke_bomb,
    cmd_status,
    cmd_task_adopt,
    cmd_task_approval_summary,
    cmd_task_approve_requirements,
    cmd_task_init,
    cmd_task_ready,
    cmd_task_status,
    cmd_upgrade,
    cmd_validation_impact,
)
from .contracts import (
    BACKLOG_PRIORITIES,
    BACKLOG_STATUSES,
    BACKLOG_TYPES,
    COORDINATION_BOUNDARIES,
    COORDINATION_DRIFT_CLASSIFICATIONS,
    CURRENT_PACKAGE_VERSION,
    EARLY_OUTCOME_CLAIM_CLASSES,
    EPIC_TRACKER_STATUSES,
    FIX_CLASSIFICATIONS,
    FIX_MODES,
    FIX_STATUS_TRANSITIONS,
    FIX_TERMINAL_DISPOSITIONS,
    OPERATIONAL_STATUS_PROOF_LAYER_NAMES,
    TRACKER_STATUSES,
    VALIDATION_IMPACT_CLASSIFICATIONS,
    VALIDATION_IMPACT_VERDICTS,
    VERIFICATION_ADAPTER_CAPABILITIES,
    VERIFICATION_CAMPAIGN_MODES,
    VERIFICATION_CAMPAIGN_STAGES,
    VERIFICATION_RECEIPT_OUTCOMES,
)
from .execution_config import (
    cmd_execution_configure,
    cmd_execution_disable,
    cmd_execution_status,
)
from .lifecycle import (
    EPIC_GLOBAL_LIFECYCLE_STATUSES,
)
from .repository import (
    _normalize_agent,
)

if __package__:
    import sys as _sys
    import types as _types

    from . import commands as _commands
    from . import contracts as _contracts
    from . import coordination as _coordination
    from . import execution as _execution
    from . import execution_config as _execution_config
    from . import inspection as _inspection
    from . import lifecycle as _lifecycle
    from . import maintenance as _maintenance
    from . import orchestration as _orchestration
    from . import repository as _repository

    _COMPAT_MODULES = (
        _contracts,
        _repository,
        _lifecycle,
        _orchestration,
        _execution,
        _coordination,
        _execution_config,
        _inspection,
        _maintenance,
        _commands,
    )
    for _module in _COMPAT_MODULES:
        for _name, _value in vars(_module).items():
            if not _name.startswith("__"):
                globals().setdefault(_name, _value)

    class _CompatibilityModule(_types.ModuleType):
        def __setattr__(self, name: str, value: object) -> None:
            for module in _COMPAT_MODULES:
                if name in vars(module):
                    setattr(module, name, value)
            super().__setattr__(name, value)

    _sys.modules[__name__].__class__ = _CompatibilityModule


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project",
        description=(
            "Project workflow: Spec-driven development for GitHub Copilot, "
            "Claude Code, OpenAI Codex, and Cursor."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {CURRENT_PACKAGE_VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ===== project init =====
    init_parser = subparsers.add_parser(
        "init",
        help="Bootstrap project-workflow in current directory (idempotent)",
    )
    init_parser.add_argument(
        "--agent",
        type=_normalize_agent,
        default="github-copilot",
        metavar="AGENT",
        help=(
            "Target agent ecosystem: github-copilot (default), claude-code, codex, or cursor. "
            "Aliases accepted: copilot, claude, codex, cursor."
        ),
    )
    init_parser.set_defaults(func=cmd_project_init)

    for command_name in ("doctor", "validate"):
        doctor_parser = subparsers.add_parser(
            command_name,
            help="Validate workflow tracker state and source-repo asset mirrors",
            description="Validate workflow tracker state and source-repo asset mirrors.",
        )
        doctor_parser.add_argument(
            "--root",
            help="Repository root to validate (default: current directory)",
        )
        doctor_parser.add_argument(
            "--strict",
            action="store_true",
            help="Treat safety warnings, such as missing completion evidence, as failures",
        )
        doctor_parser.add_argument(
            "--show-accepted",
            action="store_true",
            help="Show warnings accepted in .project-workflow/config.json",
        )
        doctor_parser.add_argument(
            "--format",
            choices=("human", "json"),
            default="human",
            help="Output format (default: human)",
        )
        doctor_parser.set_defaults(func=cmd_doctor)

    status_parser = subparsers.add_parser(
        "status",
        help="Report operational state and the next safe action without mutation",
        description=(
            "Report installation, Git, health, active work, proof, delivery, sources, "
            "and the next safe action without mutation."
        ),
    )
    status_parser.add_argument(
        "--root",
        help="Repository root to inspect (default: current directory)",
    )
    status_parser.add_argument(
        "--id",
        help="Focus the report and action resolver on one active work-item ID",
    )
    status_parser.add_argument(
        "--repository",
        help="Inspect one registered workspace repository by ID",
    )
    status_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat visible Doctor warnings as blocking health findings",
    )
    status_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format (default: human)",
    )
    status_parser.set_defaults(func=cmd_status)

    execute_parser = subparsers.add_parser(
        "execute",
        help="Preflight material work through the current sealed execution authority",
    )
    execute_parser.add_argument("--id", required=True, help="Current Task, Epic, or Fix ID")
    execute_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format (default: human)",
    )
    execute_parser.set_defaults(func=cmd_execute)

    execution_parser = subparsers.add_parser(
        "execution",
        help="Configure and inspect sealed packaged host execution",
    )
    execution_sub = execution_parser.add_subparsers(dest="execution_command", required=True)
    execution_configure_parser = execution_sub.add_parser(
        "configure",
        help="Create or refresh sealed execution authority from a public operator config",
    )
    execution_configure_parser.add_argument("--id", required=True)
    execution_configure_parser.add_argument("--config", required=True)
    execution_configure_parser.add_argument("--format", choices=("human", "json"), default="human")
    execution_configure_parser.set_defaults(func=cmd_execution_configure)
    execution_disable_parser = execution_sub.add_parser(
        "disable", help="Disable the current receipt-free packaged host authority"
    )
    execution_disable_parser.add_argument("--id", required=True)
    execution_disable_parser.add_argument("--format", choices=("human", "json"), default="human")
    execution_disable_parser.set_defaults(func=cmd_execution_disable)
    execution_status_parser = execution_sub.add_parser(
        "status", help="Inspect sealed execution authority without dispatching a model"
    )
    execution_status_parser.add_argument("--id", required=True)
    execution_status_parser.add_argument("--format", choices=("human", "json"), default="human")
    execution_status_parser.set_defaults(func=cmd_execution_status)

    release_parser = subparsers.add_parser(
        "release",
        help="Preflight the current clean frozen release candidate",
    )
    release_parser.add_argument("--id", required=True, help="Current Task, Epic, or Fix ID")
    release_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format (default: human)",
    )
    release_parser.set_defaults(func=cmd_release)

    validation_parser = subparsers.add_parser(
        "validation",
        help="Record whether a later change invalidates prior proof",
    )
    validation_sub = validation_parser.add_subparsers(dest="validation_command", required=True)
    validation_impact_parser = validation_sub.add_parser(
        "impact",
        help="Classify later change impact and record the smallest sufficient proof scope",
    )
    validation_impact_parser.add_argument(
        "--root", help="Repository root (default: current directory)"
    )
    validation_impact_parser.add_argument(
        "--id", required=True, help="Active Task, Epic child, or Fix ID"
    )
    validation_impact_parser.add_argument(
        "--baseline", required=True, help="Identity of the last sufficient passing proof"
    )
    validation_impact_parser.add_argument(
        "--change-summary", required=True, help="Exact change since the baseline proof"
    )
    validation_impact_parser.add_argument(
        "--classification",
        required=True,
        choices=VALIDATION_IMPACT_CLASSIFICATIONS,
        help="Whether the later change leaves proof unaffected, affects named proof, or is ambiguous",
    )
    validation_impact_parser.add_argument(
        "--proof-layer",
        action="append",
        choices=OPERATIONAL_STATUS_PROOF_LAYER_NAMES,
        help="Invalidated existing proof layer; repeat when more than one is affected",
    )
    validation_impact_parser.add_argument(
        "--validation-verdict",
        required=True,
        choices=VALIDATION_IMPACT_VERDICTS,
        help="Current result of the required validation scope",
    )
    validation_impact_parser.add_argument(
        "--decided-by", required=True, help="Identity recording the impact decision"
    )
    validation_impact_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format (default: human)",
    )
    validation_impact_parser.set_defaults(func=cmd_validation_impact)

    coordinate_parser = subparsers.add_parser(
        "coordinate",
        help=(
            "Maintain durable logical handoff, drift, outcome-checkpoint, and optional "
            "material-verification state"
        ),
    )
    coordinate_sub = coordinate_parser.add_subparsers(dest="coordinate_command", required=True)
    coordinate_init_parser = coordinate_sub.add_parser(
        "init", help="Initialize one durable coordination state"
    )
    coordinate_init_parser.add_argument("--id", required=True)
    coordinate_init_parser.add_argument("--phase", required=True)
    coordinate_init_parser.add_argument("--source-revision", required=True)
    coordinate_init_parser.add_argument("--loaded-package-version", required=True)
    coordinate_init_parser.add_argument("--loaded-asset-version", required=True)
    coordinate_init_parser.add_argument("--loaded-contract-version", required=True)
    coordinate_init_parser.add_argument("--context-id", required=True)
    coordinate_init_parser.add_argument("--next-action", required=True)
    coordinate_init_parser.add_argument(
        "--repository-source", action="append", metavar="REPOSITORY=REVISION"
    )
    coordinate_init_parser.add_argument("--decision", action="append")
    coordinate_init_parser.add_argument(
        "--claim-class", choices=EARLY_OUTCOME_CLAIM_CLASSES, default="mechanical"
    )
    coordinate_init_parser.add_argument(
        "--material-user-facing", choices=("yes", "no"), default="no"
    )
    coordinate_init_parser.add_argument("--checkpoint-unit")
    coordinate_init_parser.add_argument(
        "--material-verification", choices=("yes", "no"), required=True
    )
    coordinate_init_parser.add_argument("--verification-claims")
    coordinate_init_parser.add_argument("--verification-stages")
    coordinate_init_parser.add_argument("--verification-scope")
    coordinate_init_parser.add_argument("--force", action="store_true")
    coordinate_init_parser.set_defaults(func=cmd_coordinate_init)

    coordinate_context_parser = coordinate_sub.add_parser(
        "context-record", help="Declare the contract explicitly loaded by the physical context"
    )
    coordinate_context_parser.add_argument("--id", required=True)
    coordinate_context_parser.add_argument("--loaded-package-version", required=True)
    coordinate_context_parser.add_argument("--loaded-asset-version", required=True)
    coordinate_context_parser.add_argument("--loaded-contract-version", required=True)
    coordinate_context_parser.add_argument("--context-id", required=True)
    coordinate_context_parser.add_argument("--next-action", required=True)
    coordinate_context_parser.set_defaults(func=cmd_coordinate_context_record)

    coordinate_phase_parser = coordinate_sub.add_parser(
        "phase", help="Advance phase and exact repository/source identities without losing state"
    )
    coordinate_phase_parser.add_argument("--id", required=True)
    coordinate_phase_parser.add_argument("--phase", required=True)
    coordinate_phase_parser.add_argument("--source-revision", required=True)
    coordinate_phase_parser.add_argument(
        "--repository-source", action="append", metavar="REPOSITORY=REVISION"
    )
    coordinate_phase_parser.add_argument("--next-action", required=True)
    coordinate_phase_parser.set_defaults(func=cmd_coordinate_phase)

    coordinate_preflight_parser = coordinate_sub.add_parser(
        "preflight", help="Read loaded contract and Intent freshness without mutation"
    )
    coordinate_preflight_parser.add_argument("--id", required=True)
    coordinate_preflight_parser.add_argument("--format", choices=("human", "json"), default="human")
    coordinate_preflight_parser.set_defaults(func=cmd_coordinate_preflight)

    coordinate_boundary_parser = coordinate_sub.add_parser(
        "boundary", help="Record one of the five Coordinator-owned drift decisions"
    )
    coordinate_boundary_parser.add_argument("--id", required=True)
    coordinate_boundary_parser.add_argument(
        "--boundary", required=True, choices=COORDINATION_BOUNDARIES
    )
    coordinate_boundary_parser.add_argument(
        "--classification", required=True, choices=COORDINATION_DRIFT_CLASSIFICATIONS
    )
    coordinate_boundary_parser.add_argument("--ocs", required=True)
    coordinate_boundary_parser.add_argument("--capability-change", required=True)
    coordinate_boundary_parser.add_argument("--consequence", required=True)
    coordinate_boundary_parser.add_argument("--affected-units", default="none")
    coordinate_boundary_parser.add_argument("--amendment-identity")
    coordinate_boundary_parser.add_argument(
        "--shared-premises-valid", choices=("yes", "no", "unknown"), required=True
    )
    coordinate_boundary_parser.add_argument("--decided-by", required=True)
    coordinate_boundary_parser.add_argument("--next-action", default="Continue inside envelope.")
    coordinate_boundary_parser.set_defaults(func=cmd_coordinate_boundary)

    coordinate_checkpoint_parser = coordinate_sub.add_parser(
        "checkpoint",
        help="Record the earliest sufficient normal-user-journey result before fan-out",
    )
    coordinate_checkpoint_parser.add_argument("--id", required=True)
    coordinate_checkpoint_parser.add_argument("--unit", required=True)
    coordinate_checkpoint_parser.add_argument("--actor", required=True)
    coordinate_checkpoint_parser.add_argument("--entry-point", required=True)
    coordinate_checkpoint_parser.add_argument("--starting-state", required=True)
    coordinate_checkpoint_parser.add_argument("--operations", required=True)
    coordinate_checkpoint_parser.add_argument("--resulting-state", required=True)
    coordinate_checkpoint_parser.add_argument("--source-environment", required=True)
    coordinate_checkpoint_parser.add_argument("--observations", required=True)
    coordinate_checkpoint_parser.add_argument(
        "--owner-judgment", choices=("not-required", "required", "provided"), required=True
    )
    coordinate_checkpoint_parser.add_argument(
        "--verdict", choices=("pass", "fail", "pending"), required=True
    )
    coordinate_checkpoint_parser.add_argument("--affected-units", default="none")
    coordinate_checkpoint_parser.add_argument("--recorded-by", required=True)
    coordinate_checkpoint_parser.set_defaults(func=cmd_coordinate_checkpoint)

    coordinate_verification_capabilities_parser = coordinate_sub.add_parser(
        "verification-capabilities",
        help="Describe the framework-neutral optional verifier command/JSON contract",
    )
    coordinate_verification_capabilities_parser.add_argument(
        "--format", choices=("human", "json"), default="human"
    )
    coordinate_verification_capabilities_parser.set_defaults(
        func=cmd_coordinate_verification_capabilities
    )

    coordinate_verification_init_parser = coordinate_sub.add_parser(
        "verification-init",
        help="Initialize one current, finite material-verification campaign",
    )
    coordinate_verification_init_parser.add_argument("--id", required=True)
    coordinate_verification_init_parser.add_argument("--candidate-identity", required=True)
    coordinate_verification_init_parser.add_argument(
        "--mode", choices=VERIFICATION_CAMPAIGN_MODES, required=True
    )
    coordinate_verification_init_parser.add_argument("--claims", required=True)
    coordinate_verification_init_parser.add_argument("--stages", required=True)
    coordinate_verification_init_parser.add_argument("--affected-scope", required=True)
    coordinate_verification_init_parser.add_argument(
        "--impact", choices=("known", "unknown"), default="known"
    )
    coordinate_verification_init_parser.add_argument("--max-failures", type=int)
    coordinate_verification_init_parser.add_argument("--max-target-calls", type=int)
    coordinate_verification_init_parser.add_argument("--max-elapsed-seconds", type=int)
    coordinate_verification_init_parser.add_argument("--diagnostic-decision")
    coordinate_verification_init_parser.add_argument(
        "--adapter-kind", choices=("manual", "command"), default="manual"
    )
    coordinate_verification_init_parser.add_argument(
        "--adapter-capability",
        action="append",
        choices=VERIFICATION_ADAPTER_CAPABILITIES,
    )
    coordinate_verification_init_parser.add_argument(
        "--adapter-command-json",
        help="Command adapter argv as a JSON string list; requests are passed on stdin",
    )
    coordinate_verification_init_parser.add_argument(
        "--manual-command",
        help="Declared operator-run command for a manual/no-adapter campaign",
    )
    coordinate_verification_init_parser.add_argument("--force", action="store_true")
    coordinate_verification_init_parser.add_argument(
        "--format", choices=("human", "json"), default="human"
    )
    coordinate_verification_init_parser.set_defaults(func=cmd_coordinate_verification_init)

    coordinate_verification_record_parser = coordinate_sub.add_parser(
        "verification-record",
        help="Record one input-bound stage receipt without executing the verifier",
    )
    coordinate_verification_record_parser.add_argument("--id", required=True)
    coordinate_verification_record_parser.add_argument(
        "--stage", choices=VERIFICATION_CAMPAIGN_STAGES, required=True
    )
    coordinate_verification_record_parser.add_argument(
        "--outcome", choices=VERIFICATION_RECEIPT_OUTCOMES, required=True
    )
    coordinate_verification_record_parser.add_argument("--scope", required=True)
    coordinate_verification_record_parser.add_argument("--runtime-identity", required=True)
    coordinate_verification_record_parser.add_argument("--target-identity", required=True)
    coordinate_verification_record_parser.add_argument("--evaluator-identity", required=True)
    coordinate_verification_record_parser.add_argument("--artifact", required=True)
    coordinate_verification_record_parser.add_argument("--target-calls", type=int, required=True)
    coordinate_verification_record_parser.add_argument("--elapsed-seconds", type=int, required=True)
    coordinate_verification_record_parser.add_argument(
        "--stage-complete", choices=("yes", "no"), default="yes"
    )
    coordinate_verification_record_parser.add_argument("--regrade", action="store_true")
    coordinate_verification_record_parser.add_argument(
        "--format", choices=("human", "json"), default="human"
    )
    coordinate_verification_record_parser.set_defaults(func=cmd_coordinate_verification_record)

    coordinate_verification_run_parser = coordinate_sub.add_parser(
        "verification-run",
        help="Invoke one current command adapter stage through the generic JSON contract",
    )
    coordinate_verification_run_parser.add_argument("--id", required=True)
    coordinate_verification_run_parser.add_argument("--runtime-identity", required=True)
    coordinate_verification_run_parser.add_argument("--regrade", action="store_true")
    coordinate_verification_run_parser.add_argument("--stage", choices=VERIFICATION_CAMPAIGN_STAGES)
    coordinate_verification_run_parser.add_argument("--target-identity")
    coordinate_verification_run_parser.add_argument(
        "--format", choices=("human", "json"), default="human"
    )
    coordinate_verification_run_parser.set_defaults(func=cmd_coordinate_verification_run)

    coordinate_verification_preflight_parser = coordinate_sub.add_parser(
        "verification-preflight",
        help="Project the release/QA state without mutation or verifier invocation",
    )
    coordinate_verification_preflight_parser.add_argument("--id", required=True)
    coordinate_verification_preflight_parser.add_argument(
        "--material-verification", choices=("yes", "no")
    )
    coordinate_verification_preflight_parser.add_argument("--claim")
    coordinate_verification_preflight_parser.add_argument("--stage")
    coordinate_verification_preflight_parser.add_argument("--scope")
    coordinate_verification_preflight_parser.add_argument(
        "--format", choices=("human", "json"), default="human"
    )
    coordinate_verification_preflight_parser.set_defaults(
        func=cmd_coordinate_verification_preflight
    )

    coordinate_status_parser = coordinate_sub.add_parser(
        "status", help="Report sourced durable coordination state and one next action"
    )
    coordinate_status_parser.add_argument("--id", required=True)
    coordinate_status_parser.add_argument("--format", choices=("human", "json"), default="human")
    coordinate_status_parser.set_defaults(func=cmd_coordinate_status)

    delegate_parser = subparsers.add_parser(
        "delegate",
        help="Inspect a validated delegation graph and its ignored runtime state",
    )
    delegate_sub = delegate_parser.add_subparsers(dest="delegate_command", required=True)
    delegate_plan_parser = delegate_sub.add_parser(
        "plan", help="Build a deterministic read-only delegation plan"
    )
    _add_delegate_plan_arguments(delegate_plan_parser)
    delegate_plan_parser.set_defaults(func=cmd_delegate_plan)
    delegate_status_parser = delegate_sub.add_parser(
        "status", help="Report canonical plan and machine-local runtime state read-only"
    )
    _add_delegate_plan_arguments(delegate_status_parser)
    delegate_status_parser.set_defaults(func=cmd_delegate_status)
    delegate_state_init_parser = delegate_sub.add_parser(
        "state-init", help="Initialize ignored machine-local delegation runtime state"
    )
    _add_delegate_plan_arguments(delegate_state_init_parser)
    delegate_state_init_parser.set_defaults(func=cmd_delegate_state_init)
    delegate_state_reconcile_parser = delegate_sub.add_parser(
        "state-reconcile",
        help="Reconcile ignored runtime state with host-observed handles",
    )
    _add_delegate_plan_arguments(delegate_state_reconcile_parser)
    delegate_state_reconcile_parser.add_argument(
        "--observed-handles",
        required=True,
        help="JSON object mapping unit IDs to observed kind/id/worktree/state handles",
    )
    delegate_state_reconcile_parser.set_defaults(func=cmd_delegate_state_reconcile)

    upgrade_parser = subparsers.add_parser(
        "upgrade",
        help="Upgrade managed assets and repository schema with one reviewed transaction",
        description=(
            "Plan, confirm, apply, and validate one managed-asset and repository-schema upgrade."
        ),
    )
    upgrade_parser.add_argument(
        "--root",
        help="Repository root to inspect (default: current directory)",
    )
    upgrade_parser.add_argument(
        "--agent",
        type=_normalize_agent,
        default="github-copilot",
        metavar="AGENT",
        help=(
            "Target agent ecosystem: github-copilot (default), claude-code, codex, or cursor. "
            "Aliases accepted: copilot, claude, codex, cursor."
        ),
    )
    upgrade_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format (default: human)",
    )
    upgrade_parser.add_argument(
        "--plan",
        action="store_true",
        help="Print the complete non-mutating upgrade plan and exit",
    )
    upgrade_parser.add_argument(
        "--yes",
        action="store_true",
        help="Apply the generated plan without interactive confirmation",
    )
    upgrade_parser.add_argument(
        "--apply",
        action="store_true",
        help="Automation mode: apply an exact prior plan (requires --plan-fingerprint)",
    )
    upgrade_parser.add_argument(
        "--plan-fingerprint",
        help="Exact plan fingerprint previously reviewed by the caller",
    )
    upgrade_parser.set_defaults(func=cmd_upgrade)

    smoke_bomb_parser = subparsers.add_parser(
        "smoke-bomb",
        help="Sanitize one reviewed worktree and export a validated client ZIP",
        description=(
            "Plan and apply an ownership-safe removal of project-workflow internals, run "
            "reviewed validation commands, and export the sanitized Git-visible tree."
        ),
    )
    smoke_bomb_parser.add_argument(
        "--root",
        help="Git worktree root to sanitize (default: current directory)",
    )
    smoke_bomb_parser.add_argument(
        "--client-agent",
        action="append",
        type=_normalize_agent,
        required=True,
        metavar="AGENT",
        help=(
            "Client agent target; repeat for multiple targets: codex, claude-code, "
            "cursor, or github-copilot"
        ),
    )
    smoke_bomb_parser.add_argument(
        "--validation-command",
        action="append",
        required=True,
        metavar="COMMAND",
        help="Reviewed non-interactive validation command; repeat to add commands",
    )
    smoke_bomb_parser.add_argument(
        "--output",
        required=True,
        help="ZIP output path outside the repository root",
    )
    smoke_bomb_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format (default: human)",
    )
    smoke_bomb_parser.add_argument(
        "--plan",
        action="store_true",
        help="Print the complete non-mutating plan (the default without --apply)",
    )
    smoke_bomb_parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply an exact reviewed plan and export its validated ZIP",
    )
    smoke_bomb_parser.add_argument(
        "--plan-fingerprint",
        help="Exact plan fingerprint previously reviewed by the caller",
    )
    smoke_bomb_parser.add_argument(
        "--yes",
        action="store_true",
        help="Authorized non-interactive confirmation for --apply",
    )
    smoke_bomb_parser.add_argument(
        "--fail-after-replacements",
        type=int,
        help=argparse.SUPPRESS,
    )
    smoke_bomb_parser.set_defaults(func=cmd_smoke_bomb)

    # ===== project backlog ... =====
    backlog_parser = subparsers.add_parser(
        "backlog",
        help="Backlog-related commands",
        description="Backlog-related commands.",
    )
    backlog_sub = backlog_parser.add_subparsers(dest="backlog_command", required=True)

    backlog_init_parser = backlog_sub.add_parser(
        "init",
        help="Create .project-workflow/BACKLOG.md if missing",
    )
    backlog_init_parser.set_defaults(func=cmd_backlog_init)

    backlog_add_parser = backlog_sub.add_parser("add", help="Add one backlog row")
    backlog_add_parser.add_argument("--title", required=True, help="Backlog item title")
    backlog_add_parser.add_argument("--outcome", required=True, help="Desired outcome")
    backlog_add_parser.add_argument(
        "--type",
        default="Idea",
        choices=BACKLOG_TYPES,
        help="Backlog item type",
    )
    backlog_add_parser.add_argument(
        "--priority",
        default="Unset",
        choices=BACKLOG_PRIORITIES,
        help="Backlog item priority",
    )
    backlog_add_parser.add_argument(
        "--status",
        default="Proposed",
        choices=BACKLOG_STATUSES,
        help="Initial backlog item status",
    )
    backlog_add_parser.add_argument("--notes", help="Optional notes")
    backlog_add_parser.set_defaults(func=cmd_backlog_add)

    backlog_list_parser = backlog_sub.add_parser("list", help="List backlog rows")
    backlog_list_parser.set_defaults(func=cmd_backlog_list)

    backlog_status_parser = backlog_sub.add_parser(
        "status",
        help="Safely update one backlog row status",
    )
    backlog_status_parser.add_argument("--id", required=True, help="Backlog ID (e.g. BL-001)")
    backlog_status_parser.add_argument(
        "--to",
        required=True,
        choices=BACKLOG_STATUSES,
        help="Target backlog status",
    )
    backlog_status_parser.set_defaults(func=cmd_backlog_status)

    backlog_update_parser = backlog_sub.add_parser("update", help="Update one backlog row")
    backlog_update_parser.add_argument("--id", required=True, help="Backlog ID (e.g. BL-001)")
    backlog_update_parser.add_argument("--title", help="New title")
    backlog_update_parser.add_argument("--type", choices=BACKLOG_TYPES, help="New type")
    backlog_update_parser.add_argument(
        "--priority",
        choices=BACKLOG_PRIORITIES,
        help="New priority",
    )
    backlog_update_parser.add_argument("--outcome", help="New outcome")
    backlog_update_parser.add_argument("--promoted-to", help="Promoted task or epic ID")
    backlog_update_parser.add_argument("--notes", help="New notes")
    backlog_update_parser.set_defaults(func=cmd_backlog_update)

    backlog_promote_parser = backlog_sub.add_parser(
        "promote",
        help="Promote an accepted backlog row to a task or epic",
    )
    backlog_promote_parser.add_argument("--id", required=True, help="Backlog ID (e.g. BL-001)")
    backlog_promote_parser.add_argument(
        "--to",
        required=True,
        choices=("task", "epic"),
        help="Promotion target",
    )
    backlog_promote_parser.add_argument("--title", help="Override promoted task/epic title")
    backlog_promote_parser.add_argument(
        "--accept",
        action="store_true",
        help="Confirm accepting and promoting a non-Accepted row in one operation",
    )
    backlog_promote_parser.set_defaults(func=cmd_backlog_promote)

    backlog_validate_parser = backlog_sub.add_parser(
        "validate",
        help="Validate backlog structure and promoted references",
    )
    backlog_validate_parser.set_defaults(func=cmd_backlog_validate)

    # ===== project fix ... =====
    fix_parser = subparsers.add_parser(
        "fix",
        help="Lightweight post-completion correction commands",
        description=(
            "Manage bounded defects, regressions, change requests, and incidents as "
            "lightweight work items in the shared global tracker."
        ),
    )
    fix_sub = fix_parser.add_subparsers(dest="fix_command", required=True)

    fix_init_parser = fix_sub.add_parser("init", help="Scaffold a FIX.md and tracker row")
    fix_init_parser.add_argument("--title", required=True, help="Human title")
    fix_init_parser.add_argument(
        "--classification",
        choices=FIX_CLASSIFICATIONS,
        help="Optional initial classification; may be completed during triage",
    )
    fix_init_parser.add_argument(
        "--mode",
        choices=FIX_MODES,
        help="Optional Normal or Hotfix mode (default in FIX.md: Normal)",
    )
    fix_init_parser.set_defaults(func=cmd_fix_init)

    fix_triage_parser = fix_sub.add_parser(
        "triage", help="Validate triage and move a Fix from To Do to Ready"
    )
    fix_triage_parser.add_argument("--id", required=True, help="Fix ID (e.g. FIX-001)")
    fix_triage_parser.set_defaults(func=cmd_fix_triage)

    fix_status_parser = fix_sub.add_parser("status", help="Safely update a Fix lifecycle status")
    fix_status_parser.add_argument("--id", required=True, help="Fix ID (e.g. FIX-001)")
    fix_status_parser.add_argument(
        "--to",
        required=True,
        choices=tuple(FIX_STATUS_TRANSITIONS),
        help="Target Fix status",
    )
    fix_status_parser.set_defaults(func=cmd_fix_status)

    fix_close_parser = fix_sub.add_parser(
        "close", help="Validate evidence and close a reviewed Fix"
    )
    fix_close_parser.add_argument("--id", required=True, help="Fix ID (e.g. FIX-001)")
    fix_close_parser.add_argument(
        "--disposition",
        required=True,
        choices=tuple(value for value in FIX_TERMINAL_DISPOSITIONS if value != "Promoted"),
        help="Final closeout disposition",
    )
    fix_close_parser.add_argument("--decision", required=True, help="Closeout decision summary")
    fix_close_parser.add_argument("--closed-by", required=True, help="Closer identity")
    fix_close_parser.add_argument("--closed-date", help="ISO close date (default: today)")
    fix_close_parser.set_defaults(func=cmd_fix_close)

    fix_promote_parser = fix_sub.add_parser(
        "promote", help="Promote an oversized Fix to a full task or epic"
    )
    fix_promote_parser.add_argument("--id", required=True, help="Fix ID (e.g. FIX-001)")
    fix_promote_parser.add_argument(
        "--to", required=True, choices=("task", "epic"), help="Promotion target"
    )
    fix_promote_parser.add_argument("--title", help="Override promoted work title")
    fix_promote_parser.add_argument(
        "--reason", required=True, help="Why the lightweight Fix envelope is insufficient"
    )
    fix_promote_parser.add_argument(
        "--promoted-by", required=True, help="Owner or agent recording the promotion"
    )
    fix_promote_parser.set_defaults(func=cmd_fix_promote)

    # ===== project task ... =====
    task_parser = subparsers.add_parser("task", help="Task-related commands")
    task_sub = task_parser.add_subparsers(dest="task_command", required=True)

    task_init_parser = task_sub.add_parser("init", help="Scaffold a new task folder + docs")
    task_init_parser.add_argument(
        "--title", required=True, help="Human title (e.g. Super Admin Access)"
    )
    task_init_parser.add_argument(
        "--prefix",
        help=(
            "Task ID prefix to allocate, such as UI or MCP. "
            "Must be listed in .project-workflow/config.json. "
            "Default: configured default_task_id_prefix."
        ),
    )
    task_init_parser.add_argument(
        "--folder-suffix",
        help=(
            "Overrides the task folder suffix after the ID. "
            "Default: Title converted to Title-Case-With-Dashes"
        ),
    )
    task_init_parser.add_argument(
        "--status",
        default="To Do",
        help="Initial tracker status (default: To Do)",
    )
    task_init_parser.add_argument(
        "--update-tracker",
        action="store_true",
        help="Append the story to .project-workflow/TRACKER.md",
    )
    task_init_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing task docs if task folder already exists",
    )

    task_init_parser.add_argument(
        "--create-branch",
        action="store_true",
        help="Create and checkout a git branch for the task",
    )
    task_init_parser.add_argument(
        "--base-branch",
        default="develop",
        help="Base branch to branch from (default: develop)",
    )
    task_init_parser.add_argument(
        "--branch-prefix",
        default="feature/",
        help="Branch prefix (default: feature/)",
    )

    task_init_parser.set_defaults(func=cmd_task_init)

    task_status_parser = task_sub.add_parser(
        "status",
        help="Safely update one global tracker task status",
        description="Safely update one global tracker task status",
    )
    task_status_parser.add_argument("--id", required=True, help="Task ID (e.g. TASK-001)")
    task_status_parser.add_argument(
        "--to",
        required=True,
        choices=TRACKER_STATUSES,
        help="Target global tracker status",
    )
    task_status_parser.add_argument(
        "--force",
        action="store_true",
        help="Allow audited non-Complete lifecycle exceptions",
    )
    task_status_parser.add_argument(
        "--reason",
        help="Required with --force; short audit reason for the exception",
    )
    task_status_parser.set_defaults(func=cmd_task_status)

    task_approval_summary_parser = task_sub.add_parser(
        "approval-summary",
        help="Render the plain-language Intent synopsis for owner confirmation",
    )
    task_approval_summary_parser.add_argument("--id", required=True, help="Task ID (e.g. TASK-001)")
    task_approval_summary_parser.set_defaults(func=cmd_task_approval_summary)

    task_approve_requirements_parser = task_sub.add_parser(
        "approve-requirements",
        help="Record owner approval for one task requirements/AC envelope",
    )
    task_approve_requirements_parser.add_argument(
        "--id", required=True, help="Task ID (e.g. TASK-001)"
    )
    task_approve_requirements_parser.add_argument(
        "--approved-by", required=True, help="Owner who approved the requirements"
    )
    task_approve_requirements_parser.add_argument(
        "--source", required=True, help="Approval source, such as a Codex thread quote"
    )
    task_approve_requirements_parser.set_defaults(func=cmd_task_approve_requirements)

    task_adopt_parser = task_sub.add_parser(
        "adopt",
        help="Adopt a pre-existing task into current approval gates",
    )
    task_adopt_parser.add_argument("--id", required=True, help="Task ID (e.g. TASK-001)")
    task_adopt_parser.add_argument(
        "--approved-by", required=True, help="Owner who approved this legacy adoption"
    )
    task_adopt_parser.add_argument(
        "--source", required=True, help="Non-agent source of legacy adoption approval"
    )
    task_adopt_parser.add_argument(
        "--evidence-refreshed",
        action="store_true",
        help="Mark pre-existing evidence as refreshed after adoption",
    )
    task_adopt_parser.set_defaults(func=cmd_task_adopt)

    task_ready_parser = task_sub.add_parser(
        "ready",
        help="Validate standalone task readiness before implementation",
    )
    task_ready_parser.add_argument("--id", required=True, help="Task ID (e.g. TASK-001)")
    task_ready_parser.set_defaults(func=cmd_task_ready)

    # ===== project epic ... =====
    epic_parser = subparsers.add_parser("epic", help="Epic-related commands")
    epic_sub = epic_parser.add_subparsers(dest="epic_command", required=True)

    epic_init_parser = epic_sub.add_parser(
        "init",
        help="Scaffold a new epic with auto EPIC ID + REQUIREMENTS/TRACKER docs",
    )
    epic_init_parser.add_argument("--title", required=True, help="Epic title")
    epic_init_parser.add_argument(
        "--folder-suffix",
        help=(
            "Overrides the epic folder suffix after the ID. "
            "Default: Title converted to Title-Case-With-Dashes"
        ),
    )
    epic_init_parser.add_argument(
        "--status",
        default="To Do",
        help="Initial global tracker status (default: To Do)",
    )
    epic_init_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing epic docs if epic folder already exists",
    )
    epic_init_parser.set_defaults(func=cmd_epic_init)

    epic_amend_parser = epic_sub.add_parser(
        "amend",
        help="Record an approved amendment and add a Proposed epic child row",
    )
    epic_amend_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_amend_parser.add_argument("--id", required=True, help="New child row ID")
    epic_amend_parser.add_argument("--title", required=True, help="New child row title")
    epic_amend_parser.add_argument(
        "--parent-acs",
        required=True,
        help="Parent AC coverage for the amended child row (e.g. AC1, AC3)",
    )
    epic_amend_parser.add_argument(
        "--type",
        default="Task",
        choices=("Task", "Epic", "Milestone"),
        help="Epic child row type (default: Task)",
    )
    epic_amend_parser.add_argument(
        "--approved-by",
        required=True,
        help="Owner who approved this amendment",
    )
    epic_amend_parser.add_argument(
        "--reason",
        required=True,
        help="Material scope/provenance reason for the amendment",
    )
    epic_amend_parser.add_argument(
        "--source",
        required=True,
        help="Non-agent source of amendment approval",
    )
    epic_amend_parser.set_defaults(func=cmd_epic_amend)

    epic_approve_parser = epic_sub.add_parser(
        "approve",
        help="Move one epic tracker row from Proposed to Approved",
    )
    epic_approve_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_approve_parser.add_argument("--id", required=True, help="Row ID in epic TRACKER.md")
    epic_approve_parser.set_defaults(func=cmd_epic_approve)

    epic_approval_summary_parser = epic_sub.add_parser(
        "approval-summary",
        help="Render the plain-language Intent synopsis for owner confirmation",
    )
    epic_approval_summary_parser.add_argument(
        "--epic-id", required=True, help="Epic ID (e.g. EPIC-001)"
    )
    epic_approval_summary_parser.set_defaults(func=cmd_epic_approval_summary)

    epic_intent_audit_parser = epic_sub.add_parser(
        "intent-audit",
        help="Inspect sourced intent coverage, drift classifications, and freshness read-only",
    )
    epic_intent_audit_parser.add_argument(
        "--epic-id", required=True, help="Epic ID (e.g. EPIC-001)"
    )
    epic_intent_audit_parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format (default: human)",
    )
    epic_intent_audit_parser.set_defaults(func=cmd_epic_intent_audit)

    epic_approve_requirements_parser = epic_sub.add_parser(
        "approve-requirements",
        help="Record owner approval for one epic requirements/AC envelope",
    )
    epic_approve_requirements_parser.add_argument(
        "--epic-id", required=True, help="Epic ID (e.g. EPIC-001)"
    )
    epic_approve_requirements_parser.add_argument(
        "--approved-by", required=True, help="Owner who approved the requirements"
    )
    epic_approve_requirements_parser.add_argument(
        "--source", required=True, help="Approval source, such as a Codex thread quote"
    )
    epic_approve_requirements_parser.set_defaults(func=cmd_epic_approve_requirements)

    epic_adopt_parser = epic_sub.add_parser(
        "adopt",
        help="Adopt a pre-existing epic into current approval gates",
    )
    epic_adopt_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_adopt_parser.add_argument(
        "--approved-by", required=True, help="Owner who approved this legacy adoption"
    )
    epic_adopt_parser.add_argument(
        "--source", required=True, help="Non-agent source of legacy adoption approval"
    )
    epic_adopt_parser.add_argument(
        "--evidence-refreshed",
        action="store_true",
        help="Mark pre-existing evidence as refreshed after adoption",
    )
    epic_adopt_parser.set_defaults(func=cmd_epic_adopt)

    epic_ready_parser = epic_sub.add_parser(
        "ready",
        help="Validate epic requirements readiness before decomposition",
    )
    epic_ready_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_ready_parser.set_defaults(func=cmd_epic_ready)

    epic_ready_child_parser = epic_sub.add_parser(
        "ready-child",
        help="Validate one epic child task readiness before implementation/testing",
    )
    epic_ready_child_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_ready_child_parser.add_argument("--id", required=True, help="Row ID in epic TRACKER.md")
    epic_ready_child_parser.set_defaults(func=cmd_epic_ready_child)

    epic_status_parser = epic_sub.add_parser(
        "status",
        help="Safely update one epic tracker row status",
    )
    epic_status_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_status_parser.add_argument("--id", required=True, help="Row ID in epic TRACKER.md")
    epic_status_parser.add_argument(
        "--to",
        required=True,
        choices=EPIC_TRACKER_STATUSES,
        help="Target epic tracker status",
    )
    epic_status_parser.add_argument(
        "--force",
        action="store_true",
        help="Allow audited non-Complete lifecycle exceptions",
    )
    epic_status_parser.add_argument(
        "--reason",
        help="Required with --force; short audit reason for the exception",
    )
    epic_status_parser.set_defaults(func=cmd_epic_status)

    epic_lifecycle_parser = epic_sub.add_parser(
        "lifecycle",
        help="Safely update the global tracker lifecycle status for one epic",
    )
    epic_lifecycle_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_lifecycle_parser.add_argument(
        "--to",
        required=True,
        choices=EPIC_GLOBAL_LIFECYCLE_STATUSES,
        help="Target global epic lifecycle status",
    )
    epic_lifecycle_parser.set_defaults(func=cmd_epic_lifecycle)

    epic_decompose_parser = epic_sub.add_parser(
        "decompose",
        help="Generate Proposed child rows and DECOMPOSITION.md (no child scaffolding)",
    )
    epic_decompose_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_decompose_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of proposed rows to generate (default: 5)",
    )
    epic_decompose_parser.add_argument(
        "--type",
        dest="item_type",
        default="Task",
        help="Tracker Type column value for proposed rows (default: Task)",
    )
    epic_decompose_parser.add_argument(
        "--prefix",
        help=(
            "Force all proposed child rows to use one configured task prefix. "
            "Omit for config-guided mixed-prefix decomposition."
        ),
    )
    epic_decompose_parser.set_defaults(func=cmd_epic_decompose)

    epic_scaffold_child_parser = epic_sub.add_parser(
        "scaffold-child",
        help="Scaffold one Approved child row and move it to In Progress",
    )
    epic_scaffold_child_parser.add_argument(
        "--epic-id", required=True, help="Epic ID (e.g. EPIC-001)"
    )
    epic_scaffold_child_parser.add_argument("--id", required=True, help="Row ID in epic TRACKER.md")
    epic_scaffold_child_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing child docs if child folder already exists",
    )
    epic_scaffold_child_parser.add_argument(
        "--create-branch",
        action="store_true",
        help="Create and checkout a child branch from an existing epic branch",
    )
    epic_scaffold_child_parser.add_argument(
        "--epic-branch",
        default="epic/main",
        help=(
            "Existing epic branch to derive child branches from "
            "(default: epic/main). Must exist when --create-branch is used; "
            "no fallback branch is allowed."
        ),
    )
    epic_scaffold_child_parser.add_argument(
        "--branch-prefix",
        default="feature/",
        help="Child branch prefix (default: feature/)",
    )
    epic_scaffold_child_parser.set_defaults(func=cmd_epic_scaffold_child)

    epic_audit_parser = epic_sub.add_parser(
        "audit",
        help="Generate or refresh an epic ACCEPTANCE-AUDIT.md",
    )
    epic_audit_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_audit_parser.set_defaults(func=cmd_epic_audit)

    epic_closeout_parser = epic_sub.add_parser(
        "closeout",
        help="Validate epic acceptance gates before completion",
    )
    epic_closeout_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_closeout_parser.add_argument(
        "--complete",
        action="store_true",
        help="Mark the global epic tracker row Complete after all gates pass",
    )
    epic_closeout_parser.set_defaults(func=cmd_epic_closeout)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
