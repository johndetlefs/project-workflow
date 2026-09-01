"""Canonical Project Workflow contracts runtime."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

AGENT_CHOICES = {
    "github-copilot": "GitHub Copilot",
    "claude-code": "Claude Code",
    "codex": "OpenAI Codex",
    "cursor": "Cursor",
}

PROMPT_FILES = [
    "Architect.prompt.md",
    "Backlog.prompt.md",
    "Constitution.prompt.md",
    "Clarify.prompt.md",
    "Coordinator.prompt.md",
    "Delegate.prompt.md",
    "Epic.prompt.md",
    "Fix.prompt.md",
    "Implement.prompt.md",
    "Planner.prompt.md",
    "QAReview.prompt.md",
    "Requirements.prompt.md",
    "Retro.prompt.md",
    "SmokeBomb.prompt.md",
    "Task.prompt.md",
]

CODEX_SKILL_NAMES = [
    "project-architect",
    "project-backlog",
    "project-constitution",
    "project-task",
    "project-epic",
    "project-fix",
    "project-requirements",
    "project-planner",
    "project-clarify",
    "project-coordinator",
    "project-delegate",
    "project-implement",
    "project-qa-review",
    "project-retro",
    "project-smoke-bomb",
]

TASK_ID_PREFIX = "TASK"

EPIC_ID_PREFIX = "EPIC"

FIX_ID_PREFIX = "FIX"

BACKLOG_ID_PREFIX = "BL"

ID_PADDING = 3

WORKFLOW_CONFIG_FILENAME = "config.json"

WORKFLOW_MANIFEST_FILENAME = "manifest.json"

CURRENT_PACKAGE_VERSION = "0.9.2"

CURRENT_MANIFEST_VERSION = 1

CURRENT_ASSET_VERSION = 8

CURRENT_SCHEMA_VERSION = 1

COORDINATION_SCHEMA_VERSION = 2

COORDINATION_CONTRACT_VERSION = 2

COORDINATION_FILENAME = "COORDINATION.json"

COORDINATION_BOUNDARIES = (
    "after-plan-or-decomposition",
    "before-unit-start",
    "unit-return-or-dependency-join",
    "new-evidence-or-owner-reframe",
    "before-review-or-complete",
)

COORDINATION_DRIFT_CLASSIFICATIONS = (
    "inside-envelope",
    "drift-detected",
    "approved-change",
)

VERIFICATION_CAMPAIGN_SCHEMA_VERSION = 1

VERIFICATION_CAMPAIGN_MODES = ("certification", "diagnostic")

VERIFICATION_CAMPAIGN_STAGES = (
    "deterministic",
    "canary",
    "affected",
    "full",
)

VERIFICATION_RECEIPT_OUTCOMES = (
    "pass",
    "product-failure",
    "evaluator-failure",
    "provider-failure",
    "harness-failure",
    "limit-reached",
)

VERIFICATION_CAMPAIGN_OUTCOMES = (
    "pending",
    "pass",
    "blocked",
    "limit-reached",
)

VERIFICATION_OPERATIONAL_STATES = (
    "implementation-required",
    "verification-required",
    "qa-required",
    "delivery-ready",
    "blocked",
)

VERIFICATION_ADAPTER_CAPABILITIES = (
    "request-binding",
    "selection",
    "fail-fast",
    "limits",
    "typed-outcomes",
    "checkpoint-resume",
    "input-bound-receipts",
    "transcript-regrade",
)

EXECUTION_CONTROL_SCHEMA_VERSION = 1

EXECUTION_OPERATOR_CONFIG_SCHEMA_VERSION = 1

EXECUTION_PHASES = (
    "implementation",
    "verification",
    "qa-remediation",
    "candidate-promotion",
    "release",
)

EXECUTION_DIRECT_OPERATIONS = (
    "status",
    "doctor",
    "requirements",
    "inspection",
    "approval-summary",
    "cheap-deterministic",
)

EXECUTION_MATERIAL_OPERATIONS = (
    "material-execution",
    "broad-validation",
    "qa-remediation",
    "candidate-promotion",
    "release",
)

EXECUTION_REQUIRED_LIMIT_UNITS = (
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

EXECUTION_REQUIRED_CAPABILITY_CONTROLS = (
    "material-bypass",
    "interruption",
    "aggregate-activity",
    "write-scope",
    "operation-policy",
    "typed-receipts",
)

EXECUTION_CAPABILITY_STATES = ("verified", "unsupported", "unknown")

EXECUTION_RECEIPT_OUTCOMES = (
    "pass",
    "blocked",
    "limit-reached",
    "product-failure",
    "infrastructure-failure",
)

EARLY_OUTCOME_CLAIM_CLASSES = (
    "mechanical",
    "user-facing",
    "authoring",
    "visual",
    "gameplay-feel",
    "migration",
    "replacement",
)

SUPPORTED_ASSET_VERSIONS = (1, 2, 3, 4, 5, 6, 7, 8)

SUPPORTED_SCHEMA_VERSIONS = (0, 1)

REPOSITORY_COMPATIBILITY_STATES = (
    "current",
    "upgradeable",
    "legacy-unversioned",
    "unsupported-future",
    "invalid",
    "not-initialized",
)

DOCTOR_OUTPUT_SCHEMA_VERSION = 1

DOCTOR_REMEDIATION_OWNERS = ("project-workflow", "agent", "owner")

DOCTOR_FINDING_CODES = (
    "PW_APPROVAL_REQUIRED",
    "PW_BACKLOG_INVALID",
    "PW_CONFIG_INVALID",
    "PW_DECOMPOSITION_INVALID",
    "PW_DEFERRAL_INVALID",
    "PW_DUPLICATE_ID",
    "PW_EPIC_CONTRACT_INVALID",
    "PW_EVIDENCE_REQUIRED",
    "PW_FIX_INVALID",
    "PW_GENERATED_ASSET_DRIFT",
    "PW_GENERATED_UPDATE_PENDING",
    "PW_INTENT_AUDIT_NOT_CURRENT",
    "PW_OWNER_DECISION_REQUIRED",
    "PW_REPOSITORY_ASSETS_BEHIND",
    "PW_REPOSITORY_INVALID",
    "PW_REPOSITORY_LEGACY_UNVERSIONED",
    "PW_REPOSITORY_NOT_INITIALIZED",
    "PW_REPOSITORY_SCHEMA_BEHIND",
    "PW_REPOSITORY_UNSUPPORTED_FUTURE",
    "PW_TASK_DOCUMENT_INVALID",
    "PW_TRACKER_INVALID",
    "PW_WORKFLOW_INVALID",
    "PW_WORKSPACE_AUTHORITY_CONFLICT",
)

UPGRADE_PLAN_SCHEMA_VERSION = 1

UPGRADE_APPLY_RESULT_SCHEMA_VERSION = 1

ABSENT_FILE_HASH = "absent"

UPGRADE_BLOCKER_CODES = (
    "PW_UPGRADE_INVALID_REPOSITORY",
    "PW_UPGRADE_HANDLER_INVALID",
    "PW_UPGRADE_HANDLER_MISSING",
    "PW_UPGRADE_MANAGED_ASSET_INVALID_TARGET",
    "PW_UPGRADE_NOT_INITIALIZED",
    "PW_UPGRADE_PACKAGE_RESOURCE_UNAVAILABLE",
    "PW_UPGRADE_REGISTRY_AMBIGUOUS",
    "PW_UPGRADE_REGISTRY_CYCLE",
    "PW_UPGRADE_REGISTRY_DOWNGRADE",
    "PW_UPGRADE_REGISTRY_DUPLICATE_ID",
    "PW_UPGRADE_REGISTRY_INVALID_MIGRATION",
    "PW_UPGRADE_REGISTRY_INVALID_TARGET",
    "PW_UPGRADE_REGISTRY_PATH_MISSING",
    "PW_UPGRADE_UNSUPPORTED_FUTURE",
)

UPGRADE_APPLY_FAILURE_CODES = (
    "PW_UPGRADE_APPLY_BLOCKED",
    "PW_UPGRADE_APPLY_DIRTY_WORKTREE",
    "PW_UPGRADE_APPLY_FINAL_MANIFEST_INVALID",
    "PW_UPGRADE_APPLY_HANDLER_INVALID",
    "PW_UPGRADE_APPLY_HANDLER_MISSING",
    "PW_UPGRADE_MANAGED_ASSET_INVALID_TARGET",
    "PW_UPGRADE_APPLY_NOT_GIT",
    "PW_UPGRADE_PACKAGE_RESOURCE_UNAVAILABLE",
    "PW_UPGRADE_APPLY_REPLACEMENT_FAILED",
    "PW_UPGRADE_APPLY_STALE_FILE",
    "PW_UPGRADE_APPLY_STALE_PLAN",
    "PW_UPGRADE_APPLY_STALE_STATE",
)

SMOKE_BOMB_PLAN_SCHEMA_VERSION = 1

SMOKE_BOMB_RESULT_SCHEMA_VERSION = 1

SMOKE_BOMB_BLOCKER_CODES = (
    "PW_SMOKE_BOMB_AMBIGUOUS_ROOT",
    "PW_SMOKE_BOMB_CLIENT_GUIDANCE_REQUIRED",
    "PW_SMOKE_BOMB_DIRTY_WORKTREE",
    "PW_SMOKE_BOMB_OUTPUT_UNSAFE",
    "PW_SMOKE_BOMB_PRIVATE_RUNTIME_PRESENT",
    "PW_SMOKE_BOMB_RESIDUAL_REFERENCE",
    "PW_SMOKE_BOMB_UNSAFE_TARGET",
    "PW_SMOKE_BOMB_VALIDATION_REQUIRED",
)

SMOKE_BOMB_FAILURE_CODES = (
    "PW_SMOKE_BOMB_APPLY_BLOCKED",
    "PW_SMOKE_BOMB_APPLY_FAILED",
    "PW_SMOKE_BOMB_APPLY_STALE_PLAN",
    "PW_SMOKE_BOMB_ARCHIVE_BLOCKED",
    "PW_SMOKE_BOMB_VALIDATION_FAILED",
)

OPERATIONAL_STATUS_SCHEMA_VERSION = 1

OPERATIONAL_STATUS_SOURCE_KINDS = (
    "acceptance",
    "backlog",
    "coordination-state",
    "delivery-receipt",
    "doctor",
    "epic-tracker",
    "git",
    "global-tracker",
    "implementation",
    "intent-audit",
    "local-helper",
    "manifest",
    "repository-compatibility",
    "requirements",
    "repository-evidence",
    "structured-evidence",
    "workspace-config",
)

OPERATIONAL_STATUS_SOURCE_PRECEDENCE = (
    ("installation", ("repository-compatibility", "manifest", "local-helper")),
    ("workspace", ("workspace-config", "git")),
    ("work", ("epic-tracker", "global-tracker")),
    ("coordination", ("coordination-state",)),
    ("approval", ("requirements",)),
    ("intent", ("intent-audit",)),
    ("implementation", ("implementation",)),
    ("qa", ("implementation",)),
    ("repository-evidence", ("repository-evidence",)),
    ("acceptance", ("acceptance", "epic-tracker")),
    ("proof", ("structured-evidence", "implementation", "requirements")),
    ("integration", ("git",)),
    ("delivery", ("delivery-receipt", "structured-evidence", "git")),
    ("health", ("doctor", "repository-compatibility")),
    ("backlog", ("backlog",)),
)

OPERATIONAL_STATUS_DIMENSION_STATES = (
    (
        "installation",
        (
            "unknown",
            "current",
            "upgradeable",
            "legacy-unversioned",
            "unsupported-future",
            "invalid",
            "not-initialized",
            "helper-limited",
        ),
    ),
    ("git", ("unknown", "unavailable", "clean", "dirty", "detached")),
    ("health", ("unknown", "pass", "warning", "fail")),
    (
        "proof",
        (
            "unknown",
            "not-recorded",
            "declared",
            "approved",
            "ready",
            "implementation-recorded",
            "repository-validated",
            "recorded-evidence",
        ),
    ),
    (
        "delivery",
        (
            "unknown",
            "not-recorded",
            "repository-complete",
            "integrated",
            "released",
            "published",
            "deployed",
        ),
    ),
)

OPERATIONAL_STATUS_WORK_ITEM_KINDS = ("task", "fix", "epic", "epic-child")

OPERATIONAL_STATUS_FINDING_SEVERITIES = ("info", "warning", "error")

OPERATIONAL_STATUS_RESPONSIBLE_PARTIES = ("agent", "owner", "external-authority")

OPERATIONAL_STATUS_PROOF_LAYER_NAMES = (
    "requirements-approval",
    "readiness",
    "implementation",
    "qa-review",
    "parent-acceptance",
    "structured-evidence",
)

OPERATIONAL_STATUS_PROOF_LAYER_STATES = (
    "unknown",
    "not-recorded",
    "not-required",
    "pending",
    "pass",
    "fail",
)

VALIDATION_IMPACT_CLASSIFICATIONS = (
    "unaffected",
    "affected",
    "ambiguous",
)

VALIDATION_IMPACT_VERDICTS = ("pending", "pass", "fail", "not-required")

VALIDATION_IMPACT_IDENTITY_PREFIX = "sha256:"

VALIDATION_IMPACT_REQUIREMENTS = {
    "unaffected": "none",
    "affected": "affected-proof-layer",
    "ambiguous": "clarify",
}

OPERATIONAL_STATUS_ACTION_PRECEDENCE = (
    "installation-safety",
    "blocking-current-finding",
    "owner-decision",
    "missing-workflow-gate",
    "lifecycle-progress",
    "delivery-follow-up",
    "backlog-selection",
    "no-action",
)

OPERATIONAL_STATUS_GLOBAL_TERMINAL_STATES = ("Complete", "N/A")

OPERATIONAL_STATUS_EPIC_CHILD_TERMINAL_STATES = ("Complete",)

OPERATIONAL_STATUS_EPIC_CHILD_UNSCAFFOLDED_STATES = ("Proposed", "Approved")

OPERATIONAL_STATUS_GLOBAL_LIFECYCLE_MEANINGS = (
    ("To Do", "Requirements or triage have not begun."),
    ("Analysing", "Requirements or implementation planning is underway."),
    ("Ready", "Approved work is ready for implementation."),
    ("Plan Confirmed", "Legacy-compatible ready state; implementation may begin."),
    ("In Progress", "Implementation is underway."),
    ("Closeout", "Epic delivery is in acceptance and closeout."),
    ("Blocked", "Progress cannot continue until a named blocker is resolved."),
    ("Testing", "Implementation validation is underway."),
    ("Review", "QA and code review are underway."),
    ("Complete", "Repository work passed its completion gates."),
    ("N/A", "Work is closed without implementation."),
)

OPERATIONAL_STATUS_EPIC_CHILD_LIFECYCLE_MEANINGS = (
    ("Proposed", "The authorised child is planned but not approved for scaffolding."),
    ("Approved", "The child is approved and awaiting scaffold or implementation start."),
    ("In Progress", "Child implementation is underway."),
    ("Testing", "Child implementation validation is underway."),
    ("Review", "Child QA and code review are underway."),
    ("Blocked", "Child progress cannot continue until a named blocker is resolved."),
    ("Complete", "The child passed its completion gates."),
)

RECOGNIZED_WORKFLOW_PATHS = (
    "TRACKER.md",
    "BACKLOG.md",
    "config.json",
    "guidance.md",
    "tasks",
    "cli",
)

MIGRATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

EPIC_CONTRACT_FILENAME = "EPIC-CONTRACT.md"

DECOMPOSITION_PLAN_FILENAME = "DECOMPOSITION.md"

EPIC_AMENDMENTS_FILENAME = "AMENDMENTS.md"

INTENT_AUDIT_FILENAME = "INTENT-AUDIT.json"

INTENT_AUDIT_SCHEMA_VERSION = 1

STRUCTURED_EVIDENCE_FILENAME = "EVIDENCE.json"

ID_GENERATION_KINDS = ("tasks", "epics", "fixes", "backlog")

ID_GENERATION_MODES = ("sequential", "unique")

DEFAULT_ID_GENERATION = {
    "tasks": "sequential",
    "epics": "sequential",
    "fixes": "sequential",
    "backlog": "sequential",
}

UNIQUE_ID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DEFAULT_UNIQUE_ID_LENGTH = 5

DEFAULT_PREFIX_GUIDANCE = {
    TASK_ID_PREFIX: "General task work that does not need a repository-specific namespace.",
}

GLOBAL_TRACKER_COLUMNS = ("ID", "Title", "Status", "Docs")

BACKLOG_COLUMNS = (
    "ID",
    "Title",
    "Type",
    "Priority",
    "Status",
    "Outcome",
    "Promoted To",
    "Notes",
)

BACKLOG_TYPES = ("Idea", "Task Candidate", "Epic Candidate", "Discovery", "Follow-Up")

BACKLOG_PRIORITIES = ("High", "Medium", "Low", "Unset")

BACKLOG_STATUSES = (
    "Proposed",
    "Accepted",
    "Deferred",
    "Rejected",
    "Superseded",
    "Promoted",
)

IMPLEMENTATION_TASK_COLUMNS = (
    "ID",
    "Title",
    "Description",
    "Acceptance Criteria",
    "User Verification",
    "Status",
)

DELEGATION_IMPLEMENTATION_TASK_COLUMNS = (
    *IMPLEMENTATION_TASK_COLUMNS,
    "Dependencies",
    "Write Scope",
    "Parallel Safe",
)

DELEGATION_EXECUTION_NEEDS_TASK_COLUMNS = (
    *DELEGATION_IMPLEMENTATION_TASK_COLUMNS,
    "Execution Needs",
)

DELEGATION_SCHEMA_VERSION = 2

DELEGATION_RUNTIME_SCHEMA_VERSION = 1

DELEGATION_RUNTIME_RELATIVE_DIR = Path(".project-workflow/runtime/delegations")

DELEGATION_CAPABILITIES = (
    "persistent-task",
    "isolated-worktree",
    "task-monitoring",
    "task-reconciliation",
    "subagent",
    "worktree",
    "subagent-isolated-worktree",
    "persistent-task-isolated-worktree",
    "peer-team",
    "peer-messaging",
    "peer-team-isolated-worktree",
    "persistent-task-owner-steering",
    "task-retirement",
    "task-retirement-reconciliation",
)

DELEGATION_EXECUTOR_SURFACES = (
    "coordinator",
    "subagent",
    "persistent-task",
    "peer-team",
)

DELEGATION_EXECUTION_NEED_TOKENS = (
    "bounded-return",
    "durable-resume",
    "direct-owner-steering",
    "isolated-worktree",
)

DELEGATION_CAPABILITY_STATES = ("verified", "unsupported", "unknown")

DELEGATION_UNIT_STATES = ("pending", "active", "complete", "blocked", "orphaned")

TRACKER_STATUSES = (
    "To Do",
    "Analysing",
    "Ready",
    "Plan Confirmed",
    "In Progress",
    "Closeout",
    "Blocked",
    "Testing",
    "Review",
    "Complete",
    "N/A",
)

FIX_CLASSIFICATIONS = ("Defect", "Regression", "Change Request", "Incident")

FIX_MODES = ("Normal", "Hotfix")

FIX_SEVERITIES = ("Low", "Medium", "High", "Critical")

FIX_RISK_LEVELS = ("Low", "Medium", "High", "Critical")

FIX_ACTIVE_DISPOSITION = "Pending"

FIX_TERMINAL_DISPOSITIONS = ("Fixed", "Duplicate", "Rejected", "Deferred", "Promoted")

FIX_REPOSITORY_LINK_COLUMNS = ("Repo", "Branch", "PR", "Evidence")

FIX_STATUS_TRANSITIONS = {
    "To Do": {"Ready", "In Progress", "Blocked", "N/A"},
    "Ready": {"In Progress", "Blocked", "N/A"},
    "In Progress": {"Testing", "Blocked"},
    "Testing": {"Review", "In Progress", "Blocked"},
    "Review": {"Complete", "In Progress", "Blocked"},
    "Blocked": {"To Do", "Ready", "In Progress", "Testing", "Review", "N/A"},
    "Complete": set(),
    "N/A": set(),
}

EPIC_TRACKER_COLUMNS = (
    "ID",
    "Title",
    "Status",
    "Type",
    "Parent ACs",
    "Docs",
    "Branch",
    "Notes",
)

LEGACY_EPIC_TRACKER_COLUMNS = ("ID", "Title", "Status", "Type", "Docs", "Branch", "Notes")

EPIC_TRACKER_FORMAT_KEY = "_format_columns"

EPIC_TRACKER_STATUSES = (
    "Proposed",
    "Approved",
    "In Progress",
    "Testing",
    "Review",
    "Blocked",
    "Complete",
)

EPIC_STATUS_TRANSITIONS = {
    "Proposed": {"Approved", "Blocked"},
    "Approved": {"In Progress", "Blocked"},
    "In Progress": {"Testing", "Blocked"},
    "Testing": {"Review", "In Progress", "Blocked"},
    "Review": {"Complete", "In Progress", "Blocked"},
    "Blocked": {"Proposed", "Approved", "In Progress", "Testing", "Review"},
    "Complete": set(),
}

DECOMPOSITION_PLAN_COLUMNS = (
    "ID",
    "Title",
    "Parent ACs",
    "Source",
)

DELEGATION_DECOMPOSITION_PLAN_COLUMNS = (*DECOMPOSITION_PLAN_COLUMNS, "Dependencies")

DELEGATION_EXECUTION_NEEDS_DECOMPOSITION_PLAN_COLUMNS = (
    *DELEGATION_DECOMPOSITION_PLAN_COLUMNS,
    "Execution Needs",
)

EPIC_AMENDMENT_COLUMNS = (
    "ID",
    "Title",
    "Parent ACs",
    "Approved By",
    "Decision Date",
    "Reason",
    "Source",
)

EPIC_CONTRACT_PROOF_OWNER_COLUMNS = (
    "Parent AC",
    "Proof Owner",
    "Required Evidence",
)

EPIC_CONTRACT_REQUIRED_SECTIONS = (
    "Sources of Truth",
    "Invalid Substitutes",
    "Invariants",
    "Artifact Targets",
    "Parent AC Proof Ownership",
)

PROOF_RECIPE_REQUIRED_FIELDS = {
    "visual-reference-fidelity": (
        "commit",
        "timestamp",
        "parent_ac",
        "claim",
        "reference_artifact",
        "delivered_artifact",
        "comparison_method",
        "evidence_artifact",
        "evidence_artifact_hash",
    ),
    "external-contract-alignment": (
        "commit",
        "timestamp",
        "parent_ac",
        "claim",
        "contract_artifact",
        "implementation_artifact",
        "comparison_method",
        "evidence_artifact",
        "evidence_artifact_hash",
    ),
    "deployed-artifact-alignment": (
        "commit",
        "timestamp",
        "parent_ac",
        "claim",
        "execution_target",
        "source_artifact",
        "artifact_identity",
        "observation_method",
        "evidence_artifact",
        "evidence_artifact_hash",
    ),
    "runtime-target-source": (
        "commit",
        "timestamp",
        "parent_ac",
        "claim",
        "execution_target",
        "source_artifact",
        "observation_method",
        "target_used_source_proof",
        "evidence_artifact",
        "evidence_artifact_hash",
    ),
    "responsive-visual-behavior": (
        "commit",
        "timestamp",
        "parent_ac",
        "claim",
        "reference_artifact",
        "delivered_artifact",
        "viewports",
        "contexts",
        "comparison_method",
        "evidence_artifact",
        "evidence_artifact_hash",
    ),
    "user-outcome-journey": (
        "commit",
        "timestamp",
        "parent_ac",
        "claim",
        "claim_scope",
        "journey_scope",
        "actor",
        "normal_entry_point",
        "starting_state",
        "material_operations",
        "resulting_state_or_artifact",
        "outcome_observations",
        "source_artifact",
        "source_revision",
        "artifact_identity",
        "environment",
        "invalid_substitute_policy",
        "owner_acceptance_required",
        "owner_acceptance_status",
        "evidence_artifact",
        "evidence_artifact_hash",
    ),
}

PROOF_RECIPE_TRIGGER_PATTERNS = {
    "visual-reference-fidelity": (
        r"\bvisual/reference-fidelity\b",
        r"\bvisual reference fidelity\b",
        r"\bmatch(?:es|ed|ing)?\s+(?:the\s+)?(?:playground|design|reference|screenshot|visual)\b",
        r"\blooks?\s+like\s+(?:the\s+)?(?:playground|design|reference|screenshot)\b",
        r"\bfaithfully\s+reproduc(?:e|es|ed|ing)\b",
    ),
    "external-contract-alignment": (
        r"\bexternal-contract-alignment\b",
        r"\bexternal contract alignment\b",
        r"\b(?:api|mcp|external)\s+contract\b",
        r"\bcontract\s+align(?:s|ed|ment)?\b",
    ),
    "deployed-artifact-alignment": (
        r"\bdeployed-artifact-alignment\b",
        r"\bdeployed artifact alignment\b",
        r"\bdeployed\s+(?:artifact|surface|app|site)\b",
        r"\bpublished\s+(?:artifact|surface|app|site)\b",
    ),
    "runtime-target-source": (
        r"\bruntime-target-source\b",
        r"\bruntime target/source\b",
        r"\btarget/source\b",
        r"\bexecution target\b",
        r"\btarget\s+actually\s+used\s+(?:that\s+)?source\b",
    ),
    "responsive-visual-behavior": (
        r"\bresponsive-visual-behavior\b",
        r"\bresponsive visual behavior\b",
        r"\bresponsive\b",
        r"\bviewport(?:s)?\b",
        r"\bmobile\s+and\s+desktop\b",
        r"\bmulti-context\b",
    ),
    "user-outcome-journey": (
        r"\buser-outcome-journey\b",
        r"\buser outcome journey\b",
        r"\bnormal user journey\b",
        r"\buser-operable outcome\b",
        r"\brequested (?:user )?job\b",
    ),
}

PROOF_RECIPE_INVALID_SUBSTITUTE_PATTERNS = {
    "visual-reference-fidelity": (
        "unit test",
        "build passed",
        "code review only",
        "surrogate",
        "unrendered",
    ),
    "external-contract-alignment": (
        "manual skim",
        "shape looked right",
        "sample payload only",
    ),
    "deployed-artifact-alignment": (
        "local only",
        "deploy succeeded",
        "related environment",
    ),
    "runtime-target-source": (
        "relay running",
        "service running",
        "tunnel exists",
        "deploy succeeded",
        "related environment",
    ),
    "responsive-visual-behavior": (
        "single viewport",
        "desktop only",
        "mobile only",
        "unit test",
    ),
    "user-outcome-journey": (
        "debug-only evidence",
        "related environment evidence",
        "canary-only evidence",
        "internal-data-only evidence",
        "screenshot-only evidence",
        "build-only evidence",
        "test-only evidence",
    ),
}

USER_OUTCOME_INVALID_SUBSTITUTE_POLICY = {
    "tests",
    "builds",
    "screenshots",
    "internal-data",
    "debug-only",
    "related-environment",
    "canary",
}

EPIC_CHILD_GATED_STATUSES = (
    "Approved",
    "In Progress",
    "Testing",
    "Review",
    "Complete",
)

AC_MAPPED_IMPLEMENTATION_STATUSES = (
    "Plan Confirmed",
    "In Progress",
    "Blocked",
    "Testing",
    "Review",
    "Complete",
)

TASK_STATUS_TRANSITIONS = {
    "To Do": {"Analysing", "Blocked", "N/A"},
    "Analysing": {"Ready", "Plan Confirmed", "Blocked"},
    "Ready": {"In Progress", "Blocked"},
    "Plan Confirmed": {"In Progress", "Blocked"},
    "In Progress": {"Testing", "Blocked"},
    "Testing": {"Review", "In Progress", "Blocked"},
    "Review": {"Complete", "In Progress", "Blocked"},
    "Blocked": {"Ready", "In Progress", "Analysing", "Plan Confirmed", "Testing", "Review"},
    "Complete": set(),
    "N/A": set(),
}

GENERATED_MARKER = "project-workflow:generated"

GENERATED_MARKER_HTML = f"<!-- {GENERATED_MARKER} -->"

GENERATED_MARKER_COMMENT = f"# {GENERATED_MARKER}"

MANAGED_BLOCK_START = "<!-- project-workflow:start -->"

MANAGED_BLOCK_END = "<!-- project-workflow:end -->"

CANONICAL_PACKAGE_SPEC = f"project-workflow=={CURRENT_PACKAGE_VERSION}"

CANONICAL_INIT_COMMAND = f"uvx --from {CANONICAL_PACKAGE_SPEC} project init"

CANONICAL_UPGRADE_COMMAND = f"uvx --from {CANONICAL_PACKAGE_SPEC} project upgrade"


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    title: str
    folder_suffix: str

    @property
    def task_folder_name(self) -> str:
        return f"{self.task_id}-{self.folder_suffix}"


@dataclass(frozen=True)
class DoctorIssue:
    code: str
    severity: str
    path: str
    message: str
    remediation_owner: str
    mechanically_upgradeable: bool

    def __post_init__(self) -> None:
        if self.code not in DOCTOR_FINDING_CODES:
            raise ValueError(f"Unknown Doctor finding code: {self.code}")
        if self.remediation_owner not in DOCTOR_REMEDIATION_OWNERS:
            raise ValueError(f"Unknown Doctor remediation owner: {self.remediation_owner}")


@dataclass(frozen=True)
class DoctorEvaluation:
    issues: tuple[DoctorIssue, ...]
    visible_issues: tuple[DoctorIssue, ...]
    accepted_issues: tuple[DoctorIssue, ...]
    blocking_issues: tuple[DoctorIssue, ...]
    current_issues: tuple[DoctorIssue, ...]
    legacy_issues: tuple[DoctorIssue, ...]
    strict: bool

    @property
    def status(self) -> str:
        if self.blocking_issues:
            return "fail"
        if self.visible_issues:
            return "warning"
        return "pass"


@dataclass(frozen=True)
class WorkspaceRepository:
    repository_id: str
    path: str
    role: str
    resolved_path: Path


@dataclass(frozen=True)
class WorkspaceDefinition:
    authority_repository: str
    repositories: tuple[WorkspaceRepository, ...]

    def repository(self, repository_id: str) -> WorkspaceRepository:
        for repository in self.repositories:
            if repository.repository_id == repository_id:
                return repository
        raise KeyError(repository_id)


@dataclass(frozen=True)
class WorkflowConfig:
    task_id_prefixes: tuple[str, ...]
    default_task_id_prefix: str
    prefix_guidance: dict[str, str]
    id_generation: dict[str, str]
    unique_id_length: int
    accepted_doctor_warnings: dict[str, str]
    workspace: WorkspaceDefinition | None = None


@dataclass(frozen=True)
class WorkflowManifest:
    manifest_version: int
    package_version: str
    asset_version: int
    schema_version: int
    applied_migrations: tuple[str, ...]


@dataclass(frozen=True)
class RepositoryCompatibility:
    state: str
    reason: str
    manifest: WorkflowManifest | None = None

    def __post_init__(self) -> None:
        if self.state not in REPOSITORY_COMPATIBILITY_STATES:
            raise ValueError(f"Unknown repository compatibility state: {self.state}")


class ManifestValidationError(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class MigrationDefinition:
    migration_id: str
    source_schema: int
    target_schema: int
    target_files: tuple[str, ...]
    transformations: tuple[str, ...]


@dataclass(frozen=True)
class UpgradeBlocker:
    code: str
    message: str

    def __post_init__(self) -> None:
        if self.code not in UPGRADE_BLOCKER_CODES:
            raise ValueError(f"Unknown upgrade blocker code: {self.code}")


class UpgradeApplyFailure(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        if code not in UPGRADE_APPLY_FAILURE_CODES:
            raise ValueError(f"Unknown upgrade apply failure code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class SmokeBombBlocker:
    code: str
    message: str

    def __post_init__(self) -> None:
        if self.code not in SMOKE_BOMB_BLOCKER_CODES:
            raise ValueError(f"Unknown Smoke Bomb blocker code: {self.code}")


class SmokeBombFailure(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        if code not in SMOKE_BOMB_FAILURE_CODES:
            raise ValueError(f"Unknown Smoke Bomb failure code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message


def _operational_status_choices(
    entries: tuple[tuple[str, tuple[str, ...]], ...],
    key: str,
) -> tuple[str, ...]:
    for entry_key, values in entries:
        if entry_key == key:
            return values
    return ()


def _require_operational_status_text(label: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Operational status {label} must be non-empty text.")


def _require_operational_status_choice(
    label: str,
    value: str,
    choices: tuple[str, ...],
) -> None:
    if value not in choices:
        raise ValueError(
            f"Unknown operational status {label}: {value}. Allowed: {', '.join(choices)}."
        )


def _require_operational_status_sources(
    label: str,
    sources: tuple[OperationalStatusSource, ...],
    *,
    allow_empty: bool,
) -> None:
    if not isinstance(sources, tuple):
        raise ValueError(f"Operational status {label} sources must be a tuple.")
    if not allow_empty and not sources:
        raise ValueError(f"Operational status {label} sources must be a non-empty tuple.")
    if any(not isinstance(source, OperationalStatusSource) for source in sources):
        raise ValueError(
            f"Operational status {label} sources must contain OperationalStatusSource records."
        )


@dataclass(frozen=True)
class OperationalStatusSource:
    kind: str
    artifact: str
    detail: str = ""

    def __post_init__(self) -> None:
        _require_operational_status_choice(
            "source kind", self.kind, OPERATIONAL_STATUS_SOURCE_KINDS
        )
        _require_operational_status_text("source artifact", self.artifact)
        if not isinstance(self.detail, str):
            raise ValueError("Operational status source detail must be text.")


@dataclass(frozen=True)
class OperationalStatusFact:
    key: str
    value: str | int | bool | None | tuple[str, ...]

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9_]*", self.key):
            raise ValueError(f"Invalid operational status fact key: {self.key}")
        if isinstance(self.value, str) and not self.value.strip():
            raise ValueError("Operational status string fact values must be non-empty.")
        if isinstance(self.value, tuple) and any(
            not isinstance(entry, str) or not entry.strip() for entry in self.value
        ):
            raise ValueError("Operational status tuple fact values must contain non-empty strings.")
        if not isinstance(self.value, (str, int, bool, tuple)) and self.value is not None:
            raise ValueError(
                "Operational status fact values must be text, integer, boolean, "
                "a string tuple, or None."
            )


@dataclass(frozen=True)
class OperationalStatusValue:
    dimension: str
    state: str
    summary: str
    sources: tuple[OperationalStatusSource, ...] = ()
    facts: tuple[OperationalStatusFact, ...] = ()

    def __post_init__(self) -> None:
        allowed_states = _operational_status_choices(
            OPERATIONAL_STATUS_DIMENSION_STATES, self.dimension
        )
        if not allowed_states:
            dimensions = tuple(key for key, _values in OPERATIONAL_STATUS_DIMENSION_STATES)
            _require_operational_status_choice("dimension", self.dimension, dimensions)
        _require_operational_status_choice(f"{self.dimension} state", self.state, allowed_states)
        _require_operational_status_text("state summary", self.summary)
        _require_operational_status_sources("value", self.sources, allow_empty=True)
        if not isinstance(self.facts, tuple) or any(
            not isinstance(fact, OperationalStatusFact) for fact in self.facts
        ):
            raise ValueError(
                "Operational status value facts must be a tuple of OperationalStatusFact records."
            )
        fact_keys = [fact.key for fact in self.facts]
        if len(fact_keys) != len(set(fact_keys)):
            raise ValueError("Operational status value fact keys must be unique.")


@dataclass(frozen=True)
class OperationalStatusRepository:
    repository_id: str
    path: str
    role: str
    authority: bool
    git: OperationalStatusValue
    evidence: tuple[OperationalStatusFact, ...] = ()
    sources: tuple[OperationalStatusSource, ...] = ()

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9-]*", self.repository_id):
            raise ValueError("Operational status repository ID must be a lowercase slug.")
        _require_operational_status_text("repository path", self.path)
        _require_operational_status_choice(
            "repository role", self.role, ("control", "implementation")
        )
        if not isinstance(self.authority, bool):
            raise ValueError("Operational status repository authority must be boolean.")
        if not isinstance(self.git, OperationalStatusValue) or self.git.dimension != "git":
            raise ValueError("Operational status repository Git state is invalid.")
        if not isinstance(self.evidence, tuple) or any(
            not isinstance(fact, OperationalStatusFact) for fact in self.evidence
        ):
            raise ValueError("Operational status repository evidence is invalid.")
        _require_operational_status_sources("repository evidence", self.sources, allow_empty=True)


@dataclass(frozen=True)
class OperationalStatusProofLayer:
    name: str
    state: str
    summary: str
    sources: tuple[OperationalStatusSource, ...]

    def __post_init__(self) -> None:
        _require_operational_status_choice(
            "proof layer name", self.name, OPERATIONAL_STATUS_PROOF_LAYER_NAMES
        )
        _require_operational_status_choice(
            "proof layer state", self.state, OPERATIONAL_STATUS_PROOF_LAYER_STATES
        )
        _require_operational_status_text("proof layer summary", self.summary)
        _require_operational_status_sources("proof layer", self.sources, allow_empty=False)


@dataclass(frozen=True)
class OperationalStatusWorkItem:
    item_id: str
    title: str
    kind: str
    lifecycle: str
    operational_meaning: str
    sources: tuple[OperationalStatusSource, ...]
    facts: tuple[OperationalStatusFact, ...] = ()
    proof_layers: tuple[OperationalStatusProofLayer, ...] = ()
    delivery: OperationalStatusValue | None = None

    def __post_init__(self) -> None:
        _require_operational_status_text("work item ID", self.item_id)
        _require_operational_status_text("work item title", self.title)
        _require_operational_status_choice(
            "work item kind", self.kind, OPERATIONAL_STATUS_WORK_ITEM_KINDS
        )
        _require_operational_status_text("work item lifecycle", self.lifecycle)
        _require_operational_status_text("work item operational meaning", self.operational_meaning)
        _require_operational_status_sources("work item", self.sources, allow_empty=False)
        if not isinstance(self.facts, tuple) or any(
            not isinstance(fact, OperationalStatusFact) for fact in self.facts
        ):
            raise ValueError("Operational status work item facts contain an invalid record.")
        fact_keys = [fact.key for fact in self.facts]
        if len(fact_keys) != len(set(fact_keys)):
            raise ValueError("Operational status work item fact keys must be unique.")
        if not isinstance(self.proof_layers, tuple) or any(
            not isinstance(layer, OperationalStatusProofLayer) for layer in self.proof_layers
        ):
            raise ValueError("Operational status work item proof layers contain an invalid record.")
        layer_names = [layer.name for layer in self.proof_layers]
        if len(layer_names) != len(set(layer_names)):
            raise ValueError("Operational status work item proof layer names must be unique.")
        if self.delivery is not None:
            if not isinstance(self.delivery, OperationalStatusValue):
                raise ValueError("Operational status work item delivery must be a status value.")
            if self.delivery.dimension != "delivery":
                raise ValueError("Operational status work item delivery has the wrong dimension.")


@dataclass(frozen=True)
class OperationalStatusFinding:
    code: str
    severity: str
    message: str
    sources: tuple[OperationalStatusSource, ...]

    def __post_init__(self) -> None:
        if not re.fullmatch(r"PW_[A-Z0-9_]+", self.code):
            raise ValueError(f"Invalid operational status finding code: {self.code}")
        _require_operational_status_choice(
            "finding severity", self.severity, OPERATIONAL_STATUS_FINDING_SEVERITIES
        )
        _require_operational_status_text("finding message", self.message)
        _require_operational_status_sources("finding", self.sources, allow_empty=False)


@dataclass(frozen=True)
class OperationalStatusAction:
    code: str
    title: str
    responsible_party: str
    reason: str
    sources: tuple[OperationalStatusSource, ...]
    command: str | None = None
    request: str | None = None

    def __post_init__(self) -> None:
        if not re.fullmatch(r"PW_STATUS_[A-Z0-9_]+", self.code):
            raise ValueError(f"Invalid operational status action code: {self.code}")
        _require_operational_status_text("action title", self.title)
        _require_operational_status_choice(
            "responsible party",
            self.responsible_party,
            OPERATIONAL_STATUS_RESPONSIBLE_PARTIES,
        )
        _require_operational_status_text("action reason", self.reason)
        _require_operational_status_sources("action", self.sources, allow_empty=False)
        if self.command is not None and not isinstance(self.command, str):
            raise ValueError("Operational status action command must be text or None.")
        if self.request is not None and not isinstance(self.request, str):
            raise ValueError("Operational status action request must be text or None.")
        if isinstance(self.command, str) and not self.command.strip():
            raise ValueError("Operational status action command must be non-empty text or None.")
        if isinstance(self.request, str) and not self.request.strip():
            raise ValueError("Operational status action request must be non-empty text or None.")
        has_command = self.command is not None
        has_request = self.request is not None
        if has_command == has_request:
            raise ValueError(
                "Operational status action must define exactly one non-empty command or request."
            )


@dataclass(frozen=True)
class _OperationalStatusActionCandidate:
    precedence: str
    work_order: int
    item_id: str
    action: OperationalStatusAction

    def __post_init__(self) -> None:
        _require_operational_status_choice(
            "action precedence", self.precedence, OPERATIONAL_STATUS_ACTION_PRECEDENCE
        )
        if self.work_order < 0:
            raise ValueError("Operational status action work order cannot be negative.")
        if not isinstance(self.item_id, str):
            raise ValueError("Operational status action item ID must be text.")


@dataclass(frozen=True)
class OperationalStatusSnapshot:
    root: str
    installation: OperationalStatusValue
    git: OperationalStatusValue
    health: OperationalStatusValue
    proof: OperationalStatusValue
    delivery: OperationalStatusValue
    active_work: tuple[OperationalStatusWorkItem, ...] = ()
    findings: tuple[OperationalStatusFinding, ...] = ()
    blockers: tuple[OperationalStatusFinding, ...] = ()
    primary_action: OperationalStatusAction | None = None
    secondary_actions: tuple[OperationalStatusAction, ...] = ()
    workspace_authority: str | None = None
    repositories: tuple[OperationalStatusRepository, ...] = ()

    def __post_init__(self) -> None:
        _require_operational_status_text("root", self.root)
        expected_dimensions = (
            ("installation", self.installation),
            ("git", self.git),
            ("health", self.health),
            ("proof", self.proof),
            ("delivery", self.delivery),
        )
        for expected, dimension_value in expected_dimensions:
            if not isinstance(dimension_value, OperationalStatusValue):
                raise ValueError(
                    f"Operational status snapshot field '{expected}' must be an "
                    "OperationalStatusValue."
                )
            if dimension_value.dimension != expected:
                raise ValueError(
                    f"Operational status snapshot field '{expected}' received "
                    f"dimension '{dimension_value.dimension}'."
                )
        tuple_fields = (
            ("active work", self.active_work),
            ("findings", self.findings),
            ("blockers", self.blockers),
            ("secondary actions", self.secondary_actions),
            ("repositories", self.repositories),
        )
        for label, tuple_value in tuple_fields:
            if not isinstance(tuple_value, tuple):
                raise ValueError(f"Operational status snapshot {label} must be a tuple.")
        expected_types: tuple[tuple[str, tuple[object, ...], type[object]], ...] = (
            ("active work", self.active_work, OperationalStatusWorkItem),
            ("findings", self.findings, OperationalStatusFinding),
            ("blockers", self.blockers, OperationalStatusFinding),
            ("secondary actions", self.secondary_actions, OperationalStatusAction),
            ("repositories", self.repositories, OperationalStatusRepository),
        )
        for label, values, expected_type in expected_types:
            if any(not isinstance(value, expected_type) for value in values):
                raise ValueError(f"Operational status snapshot {label} contains an invalid record.")
        if self.primary_action is not None and not isinstance(
            self.primary_action, OperationalStatusAction
        ):
            raise ValueError(
                "Operational status snapshot primary action must be an "
                "OperationalStatusAction or None."
            )


@dataclass(frozen=True)
class OperationalStatusInspection:
    installation: OperationalStatusValue
    git: OperationalStatusValue
    active_work: tuple[OperationalStatusWorkItem, ...]
    findings: tuple[OperationalStatusFinding, ...]
    workspace_authority: str | None = None
    repositories: tuple[OperationalStatusRepository, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.installation, OperationalStatusValue):
            raise ValueError("Operational inspection installation must be a status value.")
        if self.installation.dimension != "installation":
            raise ValueError("Operational inspection installation has the wrong dimension.")
        if not isinstance(self.git, OperationalStatusValue):
            raise ValueError("Operational inspection Git state must be a status value.")
        if self.git.dimension != "git":
            raise ValueError("Operational inspection Git state has the wrong dimension.")
        if not isinstance(self.active_work, tuple) or any(
            not isinstance(item, OperationalStatusWorkItem) for item in self.active_work
        ):
            raise ValueError("Operational inspection active work contains an invalid record.")
        if not isinstance(self.findings, tuple) or any(
            not isinstance(finding, OperationalStatusFinding) for finding in self.findings
        ):
            raise ValueError("Operational inspection findings contain an invalid record.")
        if self.workspace_authority is not None:
            _require_operational_status_text(
                "inspection workspace authority", self.workspace_authority
            )
        if not isinstance(self.repositories, tuple) or any(
            not isinstance(repository, OperationalStatusRepository)
            for repository in self.repositories
        ):
            raise ValueError("Operational inspection repositories contain an invalid record.")
