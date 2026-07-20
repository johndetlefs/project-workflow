#!/usr/bin/env python3
"""project-workflow CLI: Bootstrap and task scaffolding for spec-driven development."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import secrets
import shutil
import subprocess
from dataclasses import dataclass
from datetime import date
from importlib.resources import files
from pathlib import Path
from typing import Optional


AGENT_CHOICES = {
    "github-copilot": "GitHub Copilot",
    "claude-code": "Claude Code",
    "codex": "OpenAI Codex",
    "cursor": "Cursor",
}

PROMPT_FILES = [
    "Backlog.prompt.md",
    "Constitution.prompt.md",
    "Clarify.prompt.md",
    "Delegate.prompt.md",
    "Epic.prompt.md",
    "Fix.prompt.md",
    "Implement.prompt.md",
    "Planner.prompt.md",
    "QAReview.prompt.md",
    "Requirements.prompt.md",
    "Retro.prompt.md",
    "Task.prompt.md",
]

CODEX_SKILL_NAMES = [
    "project-backlog",
    "project-constitution",
    "project-task",
    "project-epic",
    "project-fix",
    "project-requirements",
    "project-planner",
    "project-clarify",
    "project-delegate",
    "project-implement",
    "project-qa-review",
    "project-retro",
]

TASK_ID_PREFIX = "TASK"
EPIC_ID_PREFIX = "EPIC"
FIX_ID_PREFIX = "FIX"
BACKLOG_ID_PREFIX = "BL"
ID_PADDING = 3
WORKFLOW_CONFIG_FILENAME = "config.json"
EPIC_CONTRACT_FILENAME = "EPIC-CONTRACT.md"
DECOMPOSITION_PLAN_FILENAME = "DECOMPOSITION.md"
EPIC_AMENDMENTS_FILENAME = "AMENDMENTS.md"
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
CANONICAL_INIT_COMMAND = "uvx --from git+https://github.com/johndetlefs/project-workflow.git project init"


def _words(value: str) -> list[str]:
    return [w for w in re.split(r"[^A-Za-z0-9]+", value.strip()) if w]


def slug_titlecase_dashes(value: str) -> str:
    parts = [w.capitalize() for w in _words(value)]
    return "-".join(parts) if parts else "Untitled"


def slug_kebab_lower(value: str) -> str:
    parts = [w.lower() for w in _words(value)]
    return "-".join(parts) if parts else "untitled"


def _run_git(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _ensure_clean_git(cwd: Path) -> None:
    status = _run_git(["status", "--porcelain"], cwd=cwd)
    if status:
        raise SystemExit(
            "Refusing to create/switch branches with a dirty working tree. "
            "Commit or stash your changes first."
        )


def _branch_exists(cwd: Path, branch: str) -> bool:
    completed = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=str(cwd),
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def _get_package_resource(resource_path: str) -> str:
    """Load a resource file from the package data."""
    try:
        # Try using importlib.resources for Python 3.9+
        files_ref = files("project_workflow").joinpath(resource_path)
        if hasattr(files_ref, "read_text"):
            return files_ref.read_text(encoding="utf-8")
        else:
            # Fallback for older API
            return files_ref.read_bytes().decode("utf-8")
    except Exception as e:
        raise SystemExit(f"Failed to load package resource {resource_path}: {e}")


def _is_generated_content(content: str) -> bool:
    return GENERATED_MARKER in content


def _markdown_has_frontmatter(content: str) -> re.Match[str] | None:
    return re.match(r"^(---\n.*?\n---\n)(.*)$", content, flags=re.DOTALL)


def _generated_marker_for_path(path: Path) -> str:
    if path.suffix in {".md", ".mdc"}:
        return GENERATED_MARKER_HTML
    return GENERATED_MARKER_COMMENT


def _with_generated_marker(path: Path, content: str) -> str:
    if _is_generated_content(content):
        return content

    marker = _generated_marker_for_path(path)
    if path.suffix in {".md", ".mdc"}:
        frontmatter_match = _markdown_has_frontmatter(content)
        if frontmatter_match:
            frontmatter, body = frontmatter_match.groups()
            return f"{frontmatter}{marker}\n\n{body.lstrip()}"
        return f"{marker}\n\n{content.lstrip()}"

    if content.startswith("#!"):
        first_line, sep, rest = content.partition("\n")
        if sep:
            return f"{first_line}\n{marker}\n{rest}"
    return f"{marker}\n{content.lstrip()}"


def _collision_path(path: Path) -> Path:
    candidate = path.with_name(f"{path.name}.new")
    if not candidate.exists():
        return candidate
    try:
        if _is_generated_content(candidate.read_text(encoding="utf-8")):
            return candidate
    except OSError:
        pass

    counter = 2
    while True:
        numbered = path.with_name(f"{path.name}.new.{counter}")
        if not numbered.exists():
            return numbered
        counter += 1


def _ensure_generated_file(path: Path, content: str, *, executable: bool = False) -> str:
    """Create or refresh a project-workflow-owned generated file without overwriting users."""
    path.parent.mkdir(parents=True, exist_ok=True)
    generated_content = _with_generated_marker(path, content)

    if not path.exists():
        path.write_text(generated_content, encoding="utf-8")
        if executable:
            path.chmod(0o755)
        return f"Created: {path}"

    existing_content = path.read_text(encoding="utf-8")
    if _is_generated_content(existing_content):
        if existing_content != generated_content:
            path.write_text(generated_content, encoding="utf-8")
            action = "Refreshed"
        else:
            action = "Exists"
        if executable:
            path.chmod(0o755)
        return f"{action}: {path}"

    new_path = _collision_path(path)
    new_path.write_text(generated_content, encoding="utf-8")
    if executable:
        new_path.chmod(0o755)
    return f"Kept existing unmarked file and wrote: {new_path}"


def _ensure_user_guidance_file(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return f"Exists: {path}"

    path.write_text(
        "# Project Workflow Guidance\n\n"
        "Use this file for repo-specific workflow guidance that should survive "
        "project-workflow init refreshes.\n\n"
        "Add local conventions, validation commands, safety constraints, handoff "
        "rules, and agent notes here.\n",
        encoding="utf-8",
    )
    return f"Created: {path}"


def _default_workflow_config_text() -> str:
    return json.dumps(
        {
            "task_id_prefixes": [TASK_ID_PREFIX],
            "default_task_id_prefix": TASK_ID_PREFIX,
            "id_generation": DEFAULT_ID_GENERATION,
            "unique_id_length": DEFAULT_UNIQUE_ID_LENGTH,
            "accepted_doctor_warnings": [],
            "prefix_guidance": DEFAULT_PREFIX_GUIDANCE,
        },
        indent=2,
    ) + "\n"


def _ensure_user_config_file(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return f"Exists: {path}"
    path.write_text(_default_workflow_config_text(), encoding="utf-8")
    return f"Created: {path}"


def _managed_project_workflow_block() -> str:
    return (
        f"{MANAGED_BLOCK_START}\n"
        "## Project Workflow\n\n"
        "This repository uses project-workflow. Keep workflow state in "
        "`.project-workflow/BACKLOG.md`, `.project-workflow/TRACKER.md`, "
        "and `.project-workflow/tasks/`.\n\n"
        "- Read repo-specific workflow guidance from `.project-workflow/guidance.md`.\n"
        "- Use `.project-workflow/BACKLOG.md` for optional future intent before work is "
        "promoted into task or epic execution state. Promoted rows stay in the backlog; "
        "active execution status belongs in trackers and task/epic docs.\n"
        "- Read task ID namespace and generation config from `.project-workflow/config.json`.\n"
        f"- To install or refresh project-workflow itself, run `{CANONICAL_INIT_COMMAND}` "
        "from the repository root; add `--agent codex`, `--agent cursor`, "
        "`--agent claude-code`, or `--agent github-copilot` when selecting a mode. "
        "Do not use bare `project init` unless the package is intentionally installed "
        "and known to be current.\n"
        "- Use `./.project-workflow/cli/workflow` for supported backlog, Fix, task, epic, "
        "and validation commands.\n"
        "- Route one bounded post-completion correction to a Fix, new outcomes or multiple "
        "independent items to a Task, and coordinated workstreams to an Epic. The user's label "
        "is evidence, not a binding classification. Fixes use one `FIX.md`, the shared tasks "
        "directory, and the global tracker; do not create a separate Fix tracker.\n"
        "- Before planning, record one owner approval envelope with "
        "`task approve-requirements` or `epic approve-requirements`; unchanged work inside "
        "that envelope should proceed without repeated approval prompts, while drift, stale "
        "requirements, or evidence gaps must be fixed or amended.\n"
        "- After requirements approval, run Planner, post-plan Clarify, `task ready`, and move "
        "new tasks to `Ready` autonomously unless material drift or exceptional risk requires "
        "owner input. `Plan Confirmed` remains legacy-compatible.\n"
        "- For pre-existing work, use `task adopt` or `epic adopt`; pre-adoption inferred "
        "evidence stays untrusted until refreshed.\n"
        "- For epics, `epic decompose` writes `DECOMPOSITION.md`; child rows must match "
        "that plan before approval, scaffold, readiness, or status advancement.\n"
        "- Use `epic amend` for owner-approved mid-epic child rows outside the decomposition "
        "plan; direct tracker edits outside decomposition/amendment authority remain blocked.\n"
        "- New/adopted epics require non-placeholder `EPIC-CONTRACT.md` before "
        "decomposition, child approval/scaffolding, or movement into Ready/In Progress.\n"
        "- If requirements or claims trigger visual/reference, external contract, deployed "
        "artifact, runtime target/source, or responsive visual proof, fill child-local "
        "`EVIDENCE.json`; QA prose, tests, builds, or surrogate artifacts are invalid substitutes.\n"
        "- Use `./.project-workflow/cli/workflow task status --id <TASK-ID> --to <STATUS>` "
        "for tracker lifecycle changes.\n"
        "- Run `./.project-workflow/cli/workflow doctor` after tracker or task-doc changes.\n"
        f"{MANAGED_BLOCK_END}"
    )


def _ensure_managed_block(path: Path, block: str) -> str:
    """Append or refresh only the project-workflow managed block in a host-owned file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"{block}\n", encoding="utf-8")
        return f"Created managed block: {path}"

    content = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^{re.escape(MANAGED_BLOCK_START)}\n.*?^{re.escape(MANAGED_BLOCK_END)}$",
        flags=re.DOTALL | re.MULTILINE,
    )
    if pattern.search(content):
        updated = pattern.sub(block, content)
        if updated != content:
            path.write_text(updated, encoding="utf-8")
            return f"Refreshed managed block: {path}"
        return f"Exists managed block: {path}"

    separator = "\n\n"
    if content.endswith("\n\n"):
        separator = ""
    elif content.endswith("\n"):
        separator = "\n"
    path.write_text(f"{content}{separator}{block}\n", encoding="utf-8")
    return f"Appended managed block: {path}"


def _remove_retired_project_workflow_path(path: Path) -> None:
    """Remove known retired project-workflow assets during init."""
    if not path.exists():
        return

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    print(f"✓ Removed retired project-workflow asset: {path}")


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
    severity: str
    path: str
    message: str


@dataclass(frozen=True)
class WorkflowConfig:
    task_id_prefixes: tuple[str, ...]
    default_task_id_prefix: str
    prefix_guidance: dict[str, str]
    id_generation: dict[str, str]
    unique_id_length: int
    accepted_doctor_warnings: dict[str, str]


def _workflow_config_path(root: Path) -> Path:
    return root / ".project-workflow" / WORKFLOW_CONFIG_FILENAME


def _normalize_task_id_prefix(prefix: str) -> str:
    normalized = prefix.strip().upper()
    if not re.match(r"^[A-Z][A-Z0-9]*$", normalized):
        raise SystemExit(
            f"Invalid task ID prefix '{prefix}'. "
            "Use uppercase letters/numbers, starting with a letter."
        )
    reserved = {
        EPIC_ID_PREFIX: "epics",
        FIX_ID_PREFIX: "fixes",
    }
    if normalized in reserved:
        raise SystemExit(
            f"Task ID prefix '{normalized}' is reserved for {reserved[normalized]}."
        )
    return normalized


def _normalize_id_generation_mode(value: str) -> str:
    normalized = value.strip().lower().replace("-", "_")
    if normalized in {"guid", "uuid"}:
        normalized = "unique"
    if normalized not in ID_GENERATION_MODES:
        raise SystemExit(
            f"Invalid ID generation mode '{value}'. "
            f"Allowed: {', '.join(ID_GENERATION_MODES)}."
        )
    return normalized


def _default_workflow_config() -> WorkflowConfig:
    return WorkflowConfig(
        task_id_prefixes=(TASK_ID_PREFIX,),
        default_task_id_prefix=TASK_ID_PREFIX,
        prefix_guidance=dict(DEFAULT_PREFIX_GUIDANCE),
        id_generation=dict(DEFAULT_ID_GENERATION),
        unique_id_length=DEFAULT_UNIQUE_ID_LENGTH,
        accepted_doctor_warnings={},
    )


def _load_workflow_config(root: Path) -> WorkflowConfig:
    config_path = _workflow_config_path(root)
    if not config_path.exists():
        return _default_workflow_config()

    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {config_path}: {exc}") from exc
    except OSError as exc:
        raise SystemExit(f"Could not read {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise SystemExit(f"{config_path} must contain a JSON object.")

    raw_prefixes = raw.get("task_id_prefixes", [TASK_ID_PREFIX])
    if not isinstance(raw_prefixes, list) or not raw_prefixes:
        raise SystemExit(f"{config_path} field 'task_id_prefixes' must be a non-empty list.")

    prefixes: list[str] = []
    for raw_prefix in raw_prefixes:
        if not isinstance(raw_prefix, str):
            raise SystemExit(f"{config_path} field 'task_id_prefixes' must contain strings.")
        prefix = _normalize_task_id_prefix(raw_prefix)
        if prefix not in prefixes:
            prefixes.append(prefix)

    raw_default = raw.get("default_task_id_prefix", prefixes[0])
    if not isinstance(raw_default, str):
        raise SystemExit(f"{config_path} field 'default_task_id_prefix' must be a string.")
    default_prefix = _normalize_task_id_prefix(raw_default)
    if default_prefix not in prefixes:
        raise SystemExit(
            f"{config_path} default_task_id_prefix '{default_prefix}' must appear in "
            "task_id_prefixes."
        )

    raw_guidance = raw.get("prefix_guidance", {})
    if not isinstance(raw_guidance, dict):
        raise SystemExit(f"{config_path} field 'prefix_guidance' must be an object.")

    prefix_guidance: dict[str, str] = {}
    for raw_prefix, raw_text in raw_guidance.items():
        if not isinstance(raw_prefix, str) or not isinstance(raw_text, str):
            raise SystemExit(f"{config_path} field 'prefix_guidance' must map strings to strings.")
        prefix = _normalize_task_id_prefix(raw_prefix)
        if prefix not in prefixes:
            raise SystemExit(
                f"{config_path} prefix_guidance key '{prefix}' must appear in task_id_prefixes."
            )
        prefix_guidance[prefix] = raw_text.strip()

    for prefix in prefixes:
        prefix_guidance.setdefault(prefix, "")

    raw_id_generation = raw.get("id_generation", DEFAULT_ID_GENERATION)
    id_generation = dict(DEFAULT_ID_GENERATION)
    if isinstance(raw_id_generation, str):
        mode = _normalize_id_generation_mode(raw_id_generation)
        id_generation = {kind: mode for kind in ID_GENERATION_KINDS}
    elif isinstance(raw_id_generation, dict):
        for raw_kind, raw_mode in raw_id_generation.items():
            if raw_kind not in ID_GENERATION_KINDS:
                raise SystemExit(
                    f"{config_path} field 'id_generation' has unknown key '{raw_kind}'. "
                    f"Allowed: {', '.join(ID_GENERATION_KINDS)}."
                )
            if not isinstance(raw_mode, str):
                raise SystemExit(
                    f"{config_path} field 'id_generation.{raw_kind}' must be a string."
                )
            id_generation[raw_kind] = _normalize_id_generation_mode(raw_mode)
    else:
        raise SystemExit(
            f"{config_path} field 'id_generation' must be a string or an object."
        )

    raw_unique_id_length = raw.get("unique_id_length", DEFAULT_UNIQUE_ID_LENGTH)
    if not isinstance(raw_unique_id_length, int) or isinstance(raw_unique_id_length, bool):
        raise SystemExit(f"{config_path} field 'unique_id_length' must be an integer.")
    if raw_unique_id_length < 1 or raw_unique_id_length > 32:
        raise SystemExit(f"{config_path} field 'unique_id_length' must be between 1 and 32.")

    raw_accepted_warnings = raw.get("accepted_doctor_warnings", [])
    if not isinstance(raw_accepted_warnings, list):
        raise SystemExit(f"{config_path} field 'accepted_doctor_warnings' must be a list.")

    accepted_doctor_warnings: dict[str, str] = {}
    for idx, raw_warning in enumerate(raw_accepted_warnings, start=1):
        if isinstance(raw_warning, str):
            fingerprint = raw_warning.strip()
            reason = ""
        elif isinstance(raw_warning, dict):
            raw_fingerprint = raw_warning.get("fingerprint")
            if not isinstance(raw_fingerprint, str):
                raise SystemExit(
                    f"{config_path} accepted_doctor_warnings entry {idx} must include "
                    "a string 'fingerprint'."
                )
            fingerprint = raw_fingerprint.strip()
            raw_reason = raw_warning.get("reason", "")
            if not isinstance(raw_reason, str):
                raise SystemExit(
                    f"{config_path} accepted_doctor_warnings entry {idx} field "
                    "'reason' must be a string."
                )
            reason = raw_reason.strip()
        else:
            raise SystemExit(
                f"{config_path} accepted_doctor_warnings entry {idx} must be "
                "a string fingerprint or object."
            )
        if not re.match(r"^[0-9a-f]{16}$", fingerprint):
            raise SystemExit(
                f"{config_path} accepted_doctor_warnings entry {idx} has invalid "
                "fingerprint. Expected 16 lowercase hex characters."
            )
        accepted_doctor_warnings[fingerprint] = reason

    return WorkflowConfig(
        task_id_prefixes=tuple(prefixes),
        default_task_id_prefix=default_prefix,
        prefix_guidance=prefix_guidance,
        id_generation=id_generation,
        unique_id_length=raw_unique_id_length,
        accepted_doctor_warnings=accepted_doctor_warnings,
    )


def _format_task_prefixes(prefixes: tuple[str, ...]) -> str:
    return " or ".join(f"{prefix}-###" for prefix in prefixes)


def _id_generation_mode(config: WorkflowConfig, kind: str) -> str:
    return config.id_generation.get(kind, DEFAULT_ID_GENERATION[kind])


def _configured_suffix_pattern(config: WorkflowConfig, kind: str) -> str:
    suffixes = [r"\d{3,}" if kind == "backlog" else r"\d+"]
    if _id_generation_mode(config, kind) == "unique":
        suffixes.append(rf"[A-Z0-9]{{{config.unique_id_length}}}")
    return "(?:" + "|".join(suffixes) + ")"


def _valid_id_for_prefix(row_id: str, *, prefix: str, config: WorkflowConfig, kind: str) -> bool:
    pattern = rf"^{re.escape(prefix)}-{_configured_suffix_pattern(config, kind)}$"
    return bool(re.match(pattern, row_id))


def _valid_task_id(row_id: str, *, config: WorkflowConfig) -> bool:
    prefix = _task_prefix_from_id(row_id)
    if prefix is None or prefix not in config.task_id_prefixes:
        return False
    return _valid_id_for_prefix(row_id, prefix=prefix, config=config, kind="tasks")


def _valid_epic_id(row_id: str, *, config: WorkflowConfig) -> bool:
    return _valid_id_for_prefix(row_id, prefix=EPIC_ID_PREFIX, config=config, kind="epics")


def _valid_fix_id(row_id: str, *, config: WorkflowConfig) -> bool:
    return _valid_id_for_prefix(row_id, prefix=FIX_ID_PREFIX, config=config, kind="fixes")


def _valid_backlog_id(row_id: str, *, config: WorkflowConfig) -> bool:
    return _valid_id_for_prefix(
        row_id,
        prefix=BACKLOG_ID_PREFIX,
        config=config,
        kind="backlog",
    )


def _valid_workflow_ref_id(row_id: str, *, config: WorkflowConfig) -> bool:
    return (
        _valid_epic_id(row_id, config=config)
        or _valid_fix_id(row_id, config=config)
        or _valid_task_id(row_id, config=config)
    )


def _normalize_fix_id(row_id: str, *, root: Path) -> str:
    config = _load_workflow_config(root)
    match = re.match(
        rf"^({FIX_ID_PREFIX}-{_configured_suffix_pattern(config, 'fixes')})(?:-.+)?$",
        row_id,
    )
    if not match:
        raise SystemExit(f"Fix commands require a {FIX_ID_PREFIX}-### ID; got '{row_id}'.")
    return match.group(1)


def _resolve_task_id_prefix(root: Path, requested_prefix: str | None) -> str:
    config = _load_workflow_config(root)
    prefix = (
        _normalize_task_id_prefix(requested_prefix)
        if requested_prefix
        else config.default_task_id_prefix
    )
    if prefix not in config.task_id_prefixes:
        raise SystemExit(
            f"Task ID prefix '{prefix}' is not configured in {_workflow_config_path(root)}."
        )
    return prefix


def _normalize_task_status_id(row_id: str, *, root: Path) -> str:
    config = _load_workflow_config(root)
    prefix_pattern = "|".join(
        re.escape(prefix) for prefix in sorted(config.task_id_prefixes, key=len, reverse=True)
    )
    match = re.match(
        rf"^(({prefix_pattern})-{_configured_suffix_pattern(config, 'tasks')})(?:-.+)?$",
        row_id,
    )
    if not match:
        raise SystemExit(
            f"Task status only supports {_format_task_prefixes(config.task_id_prefixes)} IDs; "
            f"got '{row_id}'."
        )
    return match.group(1)


def _task_prefix_from_id(row_id: str) -> str | None:
    match = re.match(r"^([A-Z][A-Z0-9]*)-[A-Z0-9]+(?:-.+)?$", row_id)
    return match.group(1) if match else None


def _write_file(path: Path, content: str, *, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _implementation_template(task_id: str, title: str) -> str:
    return (
        f"## User Story\n\n"
        f"As a ____, I want ____, so that ____.\n\n"
        f"## Acceptance Criteria\n\n"
        f"- [ ] AC1: ____\n\n"
        f"## Validation\n\n"
        f"- AC1: ____\n\n"
        f"## Task List\n\n"
        f"| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        f"| --: | ----- | ----------- | ------------------- | ----------------- | ------ |\n"
        f"| 1 | ____ | ____ | AC1: ____ | ____ | To Do |\n\n"
        f"## QA & Code Review\n\n"
        f"- Verdict: ____\n"
        f"- Evidence: ____\n"
        f"- Findings: ____\n\n"
        f"## Retro\n\n"
        f"- Reusable lessons: ____\n"
        f"- Conventions or agent assets updated: ____\n"
        f"- Follow-up tasks: ____\n\n"
        f"## Notes\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n"
        f"- Created: {date.today().isoformat()}\n"
    )


def _requirements_template(task_id: str, title: str) -> str:
    return (
        f"# Requirements\n\n"
        f"## Summary\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n"
        f"- Last updated: {date.today().isoformat()}\n\n"
        f"## Owner Approval\n\n"
        f"- Requirements reviewed by owner: No\n"
        f"- Acceptance criteria reviewed by owner: No\n"
        f"- Approved for decomposition: No\n"
        f"- Approved for implementation: No\n"
        f"- Approved scope envelope: No\n"
        f"- Approved by: Not approved\n"
        f"- Approval date: Not approved\n"
        f"- Approval note / source: Not approved\n"
        f"- Approved artifact identity: Not approved\n\n"
        f"## Goal\n\n"
        f"Describe the user outcome this change must deliver.\n\n"
        f"## Non-Goals\n\n"
        f"List what is explicitly out-of-scope.\n\n"
        f"## Users & Context\n\n"
        f"Who is affected and in what situation?\n\n"
        f"## Requirements (Outcome-Focused)\n\n"
        f"- ____\n\n"
        f"## Acceptance Criteria (Verifiable)\n\n"
        f"- AC1: ____\n\n"
        f"## Open Questions (Answer Needed)\n\n"
        f"- ____\n\n"
        f"## Decisions (Resolved)\n\n"
        f"- ____\n\n"
        f"## Validation Plan\n\n"
        f"- How we will verify acceptance criteria: ____\n"
    )


def _fix_template(fix_id: str, title: str) -> str:
    return (
        f"# Fix\n\n"
        f"## Summary\n\n"
        f"- Fix: {fix_id}\n"
        f"- Title: {title}\n"
        f"- Status: To Do\n"
        f"- Created: {date.today().isoformat()}\n\n"
        f"## Report\n\n"
        f"- Observed or requested: ____\n"
        f"- Expected: ____\n"
        f"- Affected users or systems: ____\n"
        f"- Delivered baseline: ____\n"
        f"- Report evidence: ____\n\n"
        f"## Routing\n\n"
        f"- Decision: Fix\n"
        f"- Rationale: ____\n"
        f"- Related work state: Not identified\n"
        f"- Bounded correction: ____\n"
        f"- New outcome or material decisions: No\n"
        f"- Independent work items: One\n\n"
        f"## Classification\n\n"
        f"- Type: ____\n"
        f"- Mode: Normal\n"
        f"- Severity: ____\n"
        f"- Impact: ____\n"
        f"- Urgency: ____\n"
        f"- Owner: ____\n\n"
        f"## Related Work\n\n"
        f"- Originating work: Not identified\n"
        f"- External links: None\n\n"
        f"## Risk\n\n"
        f"- Risk level: ____\n"
        f"- Risks: ____\n"
        f"- Rollback or containment: ____\n\n"
        f"## Fix Plan\n\n"
        f"- Scope: ____\n"
        f"- Non-goals: ____\n"
        f"- Affected target: ____\n"
        f"- Primary repo: .\n"
        f"- Repos touched: .\n"
        f"- Branch, PR, and evidence links: ____\n"
        f"- Verification plan: ____\n\n"
        f"### Repository Links\n\n"
        f"| Repo | Branch | PR | Evidence |\n"
        f"|---|---|---|---|\n"
        f"| . | ____ | ____ | ____ |\n\n"
        f"## Verification\n\n"
        f"- Delivered scope: ____\n"
        f"- Verification result: ____\n"
        f"- Adjacent behavior checked: ____\n"
        f"- Original acceptance criteria result: Not applicable\n"
        f"- Regression evidence: ____\n"
        f"- Residual risk: ____\n\n"
        f"## Outcome\n\n"
        f"- Disposition: {FIX_ACTIVE_DISPOSITION}\n"
        f"- Decision: ____\n"
        f"- Closed by: ____\n"
        f"- Closed date: ____\n"
        f"- Promoted to: None\n"
    )


def _fix_values(text: str, heading: str) -> dict[str, str]:
    return _parse_key_value_section(_markdown_section(text, heading))


def _fix_value_missing(value: str | None) -> bool:
    normalized = (value or "").strip().lower()
    return not normalized or normalized in {"____", "pending", "tbd", "unknown"}


def _replace_fix_field(text: str, heading: str, key: str, value: str) -> str:
    lines = text.splitlines(keepends=True)
    target_heading = f"## {heading}".lower()
    in_section = False
    field_re = re.compile(rf"^(\s*[-*]\s*{re.escape(key)}\s*:\s*).*$", re.IGNORECASE)
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## "):
            if in_section:
                break
            in_section = stripped.lower() == target_heading
            continue
        if not in_section:
            continue
        match = field_re.match(line.rstrip("\n"))
        if match:
            newline = "\n" if line.endswith("\n") else ""
            lines[idx] = f"{match.group(1)}{value}{newline}"
            return "".join(lines)
    raise SystemExit(f"FIX.md is missing field '{key}' under '## {heading}'.")


def _tracker_template() -> str:
    return (
        "# Stories\n\n"
        "| ID | Title | Status | Docs |\n"
        "|---|---|---|---|\n"
    )


def _backlog_template() -> str:
    return (
        "# Backlog\n\n"
        "Use this file for future intent, rough priorities, and promotion history before "
        "work becomes an executable project-workflow task or epic.\n\n"
        "Backlog status is not implementation status. `Accepted` means worth keeping or "
        "preparing, not ready to implement. After promotion, active execution status lives "
        "in `.project-workflow/TRACKER.md` or the relevant epic tracker.\n\n"
        "Allowed `Type` values: "
        + ", ".join(f"`{value}`" for value in BACKLOG_TYPES)
        + ".\n\n"
        "Allowed `Priority` values: "
        + ", ".join(f"`{value}`" for value in BACKLOG_PRIORITIES)
        + ".\n\n"
        "Allowed `Status` values: "
        + ", ".join(f"`{value}`" for value in BACKLOG_STATUSES)
        + ".\n\n"
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )


def _epic_tracker_template() -> str:
    return (
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )


def _epic_deferrals_template() -> str:
    return (
        "# Deferrals\n\n"
        "| Parent AC | Status | Owner | Decision Date | Reason | Follow-up | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
    )


def _epic_amendments_template() -> str:
    return (
        "# Epic Amendments\n\n"
        "## Approved Child Row Amendments\n\n"
        "| ID | Title | Parent ACs | Approved By | Decision Date | Reason | Source |\n"
        "|---|---|---|---|---|---|---|\n"
    )


def _epic_retro_template(epic_id: str, title: str) -> str:
    return (
        "# Epic Retro\n\n"
        f"- Epic: {epic_id}\n"
        f"- Title: {title}\n"
        f"- Last updated: {date.today().isoformat()}\n\n"
        "## Lessons\n\n"
        "- ____\n\n"
        "## Follow-up Tasks\n\n"
        "- ____\n\n"
        "## Deferrals\n\n"
        "- ____\n\n"
        "## Missed In-Scope Work\n\n"
        "- ____\n"
    )


def _epic_contract_template(epic_id: str, title: str) -> str:
    return (
        "# Epic Contract\n\n"
        "## Summary\n\n"
        f"- Epic: {epic_id}\n"
        f"- Title: {title}\n"
        f"- Last updated: {date.today().isoformat()}\n\n"
        "## Sources of Truth\n\n"
        "- ____\n\n"
        "## Invalid Substitutes\n\n"
        "- ____\n\n"
        "## Invariants\n\n"
        "- ____\n\n"
        "## Artifact Targets\n\n"
        "- ____\n\n"
        "## Parent AC Proof Ownership\n\n"
        "| Parent AC | Proof Owner | Required Evidence |\n"
        "| --- | --- | --- |\n"
        "| AC1 | ____ | ____ |\n\n"
    )


def _parse_markdown_table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _clean_markdown_cell_path(value: str) -> str:
    return value.strip().strip("`").strip()


def _markdown_section(text: str, heading: str) -> str:
    target = f"## {heading}".lower()
    collecting = False
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            if collecting:
                break
            collecting = stripped.lower() == target
            continue
        if collecting:
            lines.append(line)
    return "\n".join(lines).strip()


def _extract_ac_ids(text: str) -> set[str]:
    return {
        f"AC{match.group(1)}"
        for match in re.finditer(r"\bAC\s*(\d+)\b", text, flags=re.IGNORECASE)
    }


def _extract_workflow_ref_ids(text: str) -> set[str]:
    return {
        match.group(0).upper()
        for match in re.finditer(r"\b[A-Z][A-Z0-9]*-[A-Z0-9]+\b", text, re.IGNORECASE)
    }


def _extract_declared_ac_ids(text: str) -> set[str]:
    declared: set[str] = set()
    for line in text.splitlines():
        match = re.match(
            r"^\s*[-*]\s*(?:\[[ xX]\]\s*)?(AC\s*\d+)\s*:",
            line,
            flags=re.IGNORECASE,
        )
        if match:
            declared.update(_extract_ac_ids(match.group(1)))
    return declared


def _extract_parent_ac_coverage(row: dict[str, str]) -> str:
    direct = row.get("Parent ACs", "").strip()
    if direct:
        return direct
    notes = row.get("Notes", "")
    match = re.search(
        r"\bCovers\s+((?:AC\s*\d+\s*,?\s*)+)",
        notes,
        flags=re.IGNORECASE,
    )
    if not match:
        return ""
    return ", ".join(sorted(_extract_ac_ids(match.group(1))))


def _extract_parent_ac_ids_from_requirements(requirements_text: str) -> set[str]:
    return (
        _extract_ac_ids(_markdown_section(requirements_text, "Acceptance Criteria (Verifiable)"))
        | _extract_ac_ids(_markdown_section(requirements_text, "Acceptance Criteria"))
    )


def _extract_parent_ac_ids_from_epic_rows(rows: list[dict[str, str]]) -> set[str]:
    mapped: set[str] = set()
    for row in rows:
        mapped.update(_extract_ac_ids(_extract_parent_ac_coverage(row)))
    return mapped


def _normalize_ac_list(value: str) -> str:
    ac_ids = sorted(_extract_ac_ids(value), key=lambda ac_id: int(ac_id[2:]))
    return ", ".join(ac_ids)


def _markdown_table_rows_from_section(
    text: str,
    heading: str,
    *,
    expected_columns: tuple[str, ...],
) -> list[dict[str, str]]:
    section = _markdown_section(text, heading)
    if not section:
        return []

    lines = section.splitlines()
    header_idx: int | None = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        if cells == list(expected_columns):
            header_idx = idx
            break
    if header_idx is None:
        return []

    rows: list[dict[str, str]] = []
    row_idx = header_idx + 2
    while row_idx < len(lines):
        cells = _parse_markdown_table_cells(lines[row_idx])
        if cells is None or len(cells) != len(expected_columns):
            break
        rows.append(dict(zip(expected_columns, cells)))
        row_idx += 1
    return rows


def _proposed_child_work_rows(requirements_text: str) -> list[dict[str, str]]:
    return _markdown_table_rows_from_section(
        requirements_text,
        "Proposed Child Work",
        expected_columns=("Proposed Child", "Parent ACs", "Purpose"),
    )


def _decomposition_plan_path(epic_dir: Path) -> Path:
    return epic_dir / DECOMPOSITION_PLAN_FILENAME


def _epic_amendments_path(epic_dir: Path) -> Path:
    return epic_dir / EPIC_AMENDMENTS_FILENAME


def _epic_contract_path(epic_dir: Path) -> Path:
    return epic_dir / EPIC_CONTRACT_FILENAME


def _epic_contract_proof_owner_rows(contract_text: str) -> list[dict[str, str]]:
    return _markdown_table_rows_from_section(
        contract_text,
        "Parent AC Proof Ownership",
        expected_columns=EPIC_CONTRACT_PROOF_OWNER_COLUMNS,
    )


def _extract_work_item_ids(text: str) -> set[str]:
    return set(re.findall(r"\b[A-Z][A-Z0-9]*-[A-Z0-9]+\b", text))


def _epic_contract_proof_owner_map(contract_text: str) -> dict[str, set[str]]:
    owner_map: dict[str, set[str]] = {}
    for row in _epic_contract_proof_owner_rows(contract_text):
        owners = _extract_work_item_ids(row.get("Proof Owner", ""))
        for ac_id in _extract_ac_ids(row.get("Parent AC", "")):
            owner_map.setdefault(ac_id, set()).update(owners)
    return owner_map


def _contract_section_bullets(contract_text: str, heading: str) -> list[str]:
    section = _markdown_section(contract_text, heading)
    bullets: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")) and not _section_has_placeholder(stripped):
            bullets.append(stripped.lstrip("-*").strip())
    return bullets


def _format_child_charter_from_contract(
    *,
    epic_dir: Path,
    parent_ac_coverage: str,
) -> str:
    contract_path = _epic_contract_path(epic_dir)
    if not contract_path.exists():
        return ""
    contract_text = contract_path.read_text(encoding="utf-8")
    parent_ac_ids = sorted(
        _extract_ac_ids(parent_ac_coverage),
        key=lambda ac_id: int(ac_id[2:]),
    )
    proof_rows = [
        row
        for row in _epic_contract_proof_owner_rows(contract_text)
        if _extract_ac_ids(row.get("Parent AC", "")) & set(parent_ac_ids)
    ]

    def bullet_lines(values: list[str]) -> str:
        return "\n".join(f"- {value}" for value in values) if values else "- None recorded."

    proof_lines = []
    for row in proof_rows:
        proof_lines.append(
            f"- {row.get('Parent AC', '').strip()}: owner `{row.get('Proof Owner', '').strip()}`; "
            f"required evidence: {row.get('Required Evidence', '').strip()}"
        )
    return (
        "## Child Charter\n\n"
        "### Inherited Invariants\n\n"
        f"{bullet_lines(_contract_section_bullets(contract_text, 'Invariants'))}\n\n"
        "### Invalid Substitutes\n\n"
        f"{bullet_lines(_contract_section_bullets(contract_text, 'Invalid Substitutes'))}\n\n"
        "### Artifact Targets\n\n"
        f"{bullet_lines(_contract_section_bullets(contract_text, 'Artifact Targets'))}\n\n"
        "### Parent AC Proof Ownership\n\n"
        f"{chr(10).join(proof_lines) if proof_lines else '- None assigned to this child.'}\n\n"
    )


def _epic_contract_issues(epic_dir: Path, requirements_text: str) -> list[str]:
    contract_path = _epic_contract_path(epic_dir)
    if not contract_path.exists():
        return [f"{EPIC_CONTRACT_FILENAME} is missing."]

    contract_text = contract_path.read_text(encoding="utf-8")
    issues: list[str] = []
    for heading in EPIC_CONTRACT_REQUIRED_SECTIONS:
        section = _markdown_section(contract_text, heading)
        if not _section_has_substantive_text(section):
            issues.append(
                f"{EPIC_CONTRACT_FILENAME} section `## {heading}` is missing or placeholder."
            )

    owner_rows = _epic_contract_proof_owner_rows(contract_text)
    if not owner_rows:
        issues.append(
            f"{EPIC_CONTRACT_FILENAME} must include parent AC proof owner rows."
        )
    else:
        for row in owner_rows:
            row_text = " ".join(row.values())
            if _section_has_placeholder(row_text):
                issues.append(
                    f"{EPIC_CONTRACT_FILENAME} proof owner row for "
                    f"{row.get('Parent AC', 'unknown AC')} is placeholder."
                )

    parent_ac_ids = _extract_parent_ac_ids_from_requirements(requirements_text)
    owned_ac_ids: set[str] = set()
    for row in owner_rows:
        owned_ac_ids.update(_extract_ac_ids(row.get("Parent AC", "")))
    missing_owners = sorted(parent_ac_ids - owned_ac_ids, key=lambda ac_id: int(ac_id[2:]))
    if missing_owners:
        issues.append(
            f"{EPIC_CONTRACT_FILENAME} lacks proof owners for parent ACs: "
            + ", ".join(missing_owners)
        )
    return issues


def _epic_contract_issues_for_path(epic_dir: Path) -> list[str]:
    requirements_path = epic_dir / "REQUIREMENTS.md"
    if not requirements_path.exists():
        return [f"missing epic requirements file: {requirements_path}"]
    return _epic_contract_issues(
        epic_dir,
        requirements_path.read_text(encoding="utf-8"),
    )


def _require_epic_contract(epic_dir: Path, epic_id: str) -> None:
    issues = _epic_contract_issues_for_path(epic_dir)
    if issues:
        raise SystemExit(
            f"{epic_id} is missing required epic contract authority:\n"
            + "\n".join(f"- {issue}" for issue in issues)
        )


def _decomposition_plan_source_identity(requirements_text: str) -> str:
    values = _parse_key_value_section(_markdown_section(requirements_text, OWNER_APPROVAL_HEADING))
    identity = values.get("approved artifact identity", "").strip()
    if identity.startswith(APPROVAL_IDENTITY_PREFIX):
        return identity
    return _approval_artifact_identity(requirements_text)


def _format_decomposition_plan(
    *,
    epic_id: str,
    requirements_text: str,
    rows: list[dict[str, str]],
) -> str:
    source_identity = _decomposition_plan_source_identity(requirements_text)
    lines = [
        "# Decomposition Plan",
        "",
        "## Summary",
        "",
        f"- Epic: {epic_id}",
        "- Status: Approved by parent requirements envelope",
        "- Authority source: Parent REQUIREMENTS.md Owner Approval",
        f"- Source requirements identity: {source_identity}",
        f"- Last updated: {date.today().isoformat()}",
        "",
        "## Authorized Child Rows",
        "",
        "| ID | Title | Parent ACs | Source |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {id} | {title} | {parent_acs} | {source} |".format(
                id=row["ID"],
                title=row["Title"],
                parent_acs=_normalize_ac_list(row.get("Parent ACs", "")),
                source=row.get("Source", "Decomposition plan"),
            )
        )
    lines.extend(
        [
            "",
            "## Authority Rules",
            "",
            "- Matching rows inside this plan may be approved and scaffolded without separate per-row owner approval.",
            "- Rows outside this plan require an approved amendment before gated lifecycle movement.",
            "- Matching is by ID, title, and parent AC coverage.",
            "",
        ]
    )
    return "\n".join(lines)


def _read_decomposition_plan_rows(plan_path: Path) -> list[dict[str, str]]:
    if not plan_path.exists():
        return []
    return _markdown_table_rows_from_section(
        plan_path.read_text(encoding="utf-8"),
        "Authorized Child Rows",
        expected_columns=DECOMPOSITION_PLAN_COLUMNS,
    )


def _read_epic_amendment_rows(amendments_path: Path) -> list[dict[str, str]]:
    if not amendments_path.exists():
        return []
    return _markdown_table_rows_from_section(
        amendments_path.read_text(encoding="utf-8"),
        "Approved Child Row Amendments",
        expected_columns=EPIC_AMENDMENT_COLUMNS,
    )


def _append_epic_amendment_row(amendments_path: Path, row: dict[str, str]) -> None:
    if not amendments_path.exists():
        amendments_path.write_text(_epic_amendments_template(), encoding="utf-8")
    lines = amendments_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_idx: int | None = None
    for idx, line in enumerate(lines):
        if _parse_markdown_table_cells(line) == list(EPIC_AMENDMENT_COLUMNS):
            header_idx = idx
            break
    if header_idx is None:
        raise SystemExit(
            f"{EPIC_AMENDMENTS_FILENAME} schema mismatch. Expected amendment table header."
        )
    existing_rows = _read_epic_amendment_rows(amendments_path)
    row_id = row.get("ID", "").strip()
    if row_id in {existing.get("ID", "").strip() for existing in existing_rows}:
        raise SystemExit(f"{row_id} is already recorded in {EPIC_AMENDMENTS_FILENAME}.")
    insert_at = header_idx + 2 + len(existing_rows)
    lines.insert(
        insert_at,
        "| "
        + " | ".join(_markdown_cell(row.get(column, "")) for column in EPIC_AMENDMENT_COLUMNS)
        + " |\n",
    )
    amendments_path.write_text("".join(lines), encoding="utf-8")


def _amendment_row_authority_issues(
    *,
    amendment_row: dict[str, str],
    tracker_row: dict[str, str],
) -> list[str]:
    row_id = tracker_row.get("ID", "").strip()
    issues: list[str] = []
    if amendment_row.get("Title", "").strip() != tracker_row.get("Title", "").strip():
        issues.append(
            f"{row_id} title differs from amendment "
            f"('{amendment_row.get('Title', '').strip()}')."
        )
    amended_acs = _normalize_ac_list(amendment_row.get("Parent ACs", ""))
    row_acs = _normalize_ac_list(_extract_parent_ac_coverage(tracker_row))
    if amended_acs != row_acs:
        issues.append(
            f"{row_id} parent ACs differ from amendment ('{amended_acs}' != '{row_acs}')."
        )
    for column in ("Approved By", "Decision Date", "Reason", "Source"):
        value = amendment_row.get(column, "").strip()
        if _approval_source_invalid(value):
            issues.append(f"{row_id} amendment column `{column}` is missing or placeholder.")
    return issues


def _amendment_authority_issues(
    *,
    epic_dir: Path,
    row: dict[str, str],
) -> list[str]:
    amendments_path = _epic_amendments_path(epic_dir)
    if not amendments_path.exists():
        return [f"{EPIC_AMENDMENTS_FILENAME} is missing."]
    row_id = row.get("ID", "").strip()
    for amendment_row in _read_epic_amendment_rows(amendments_path):
        if amendment_row.get("ID", "").strip() == row_id:
            return _amendment_row_authority_issues(
                amendment_row=amendment_row,
                tracker_row=row,
            )
    return [f"{row_id} is not recorded in {EPIC_AMENDMENTS_FILENAME}."]


def _decomposition_plan_authority_issues(
    *,
    epic_dir: Path,
    row: dict[str, str],
) -> list[str]:
    plan_path = _decomposition_plan_path(epic_dir)
    if not plan_path.exists():
        return [
            f"{DECOMPOSITION_PLAN_FILENAME} is missing; run `epic decompose` from "
            "owner-approved requirements or record an approved amendment before this row advances."
        ]

    plan_rows = _read_decomposition_plan_rows(plan_path)
    row_id = row.get("ID", "").strip()
    for plan_row in plan_rows:
        if plan_row.get("ID", "").strip() != row_id:
            continue
        issues: list[str] = []
        if plan_row.get("Title", "").strip() != row.get("Title", "").strip():
            issues.append(
                f"{row_id} title differs from decomposition plan "
                f"('{plan_row.get('Title', '').strip()}')."
            )
        planned_acs = _normalize_ac_list(plan_row.get("Parent ACs", ""))
        row_acs = _normalize_ac_list(_extract_parent_ac_coverage(row))
        if planned_acs != row_acs:
            issues.append(
                f"{row_id} parent ACs differ from decomposition plan "
                f"('{planned_acs}' != '{row_acs}')."
            )
        return issues

    amendment_issues = _amendment_authority_issues(epic_dir=epic_dir, row=row)
    if not amendment_issues:
        return []

    return [
        f"{row_id} is outside {DECOMPOSITION_PLAN_FILENAME}; record an approved "
        "amendment before this row advances.",
        *amendment_issues,
    ]


def _require_decomposition_plan_authority(epic_dir: Path, row: dict[str, str]) -> None:
    issues = _decomposition_plan_authority_issues(epic_dir=epic_dir, row=row)
    if issues:
        row_id = row.get("ID", "child row")
        raise SystemExit(
            f"{row_id} is outside the approved decomposition authority:\n"
            + "\n".join(f"- {issue}" for issue in issues)
        )


def _duplicate_backlog_ids(rows: list[dict[str, str]]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        row_id = row.get("ID", "").strip()
        if not row_id:
            continue
        if row_id in seen:
            duplicates.add(row_id)
        seen.add(row_id)
    return sorted(duplicates)


def _backlog_rows(
    backlog_path: Path, issues: list[DoctorIssue] | None = None
) -> list[dict[str, str]]:
    return _parse_markdown_table(
        backlog_path,
        expected_columns=BACKLOG_COLUMNS,
        issues=issues if issues is not None else [],
        label="Backlog",
    )


def _backlog_rows_for_update(backlog_path: Path) -> tuple[list[str], int, list[dict[str, str]]]:
    lines = backlog_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_idx: int | None = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        if cells == list(BACKLOG_COLUMNS):
            header_idx = idx
            break

    if header_idx is None:
        expected = " | ".join(BACKLOG_COLUMNS)
        raise SystemExit(
            "Backlog schema mismatch. Expected header: "
            f"'| {expected} |' in {backlog_path}."
        )

    rows: list[dict[str, str]] = []
    row_idx = header_idx + 2
    while row_idx < len(lines):
        cells = _parse_markdown_table_cells(lines[row_idx])
        if cells is None:
            break
        if len(cells) != len(BACKLOG_COLUMNS):
            raise SystemExit(
                "Backlog row has wrong number of columns. "
                f"Expected {len(BACKLOG_COLUMNS)} columns in {backlog_path}: "
                f"{lines[row_idx].strip()}"
            )
        row = dict(zip(BACKLOG_COLUMNS, cells))
        row["_line_idx"] = str(row_idx)
        rows.append(row)
        row_idx += 1

    return lines, header_idx, rows


def _next_backlog_id_from_rows(rows: list[dict[str, str]]) -> str:
    max_value = 0
    row_re = re.compile(rf"^{re.escape(BACKLOG_ID_PREFIX)}-(\d+)$")
    for row in rows:
        match = row_re.match(row.get("ID", "").strip())
        if match:
            max_value = max(max_value, int(match.group(1)))
    return f"{BACKLOG_ID_PREFIX}-{max_value + 1:0{ID_PADDING}d}"


def _next_backlog_id(root: Path, rows: list[dict[str, str]]) -> str:
    config = _load_workflow_config(root)
    if _id_generation_mode(config, "backlog") == "sequential":
        return _next_backlog_id_from_rows(rows)

    workflow_dir = root / ".project-workflow"
    used_ids = _used_ids_for_prefix(
        workflow_dir / "tasks",
        workflow_dir / "TRACKER.md",
        prefix=BACKLOG_ID_PREFIX,
    )
    used_ids.update(row.get("ID", "").strip() for row in rows if row.get("ID", "").strip())
    return _next_unique_id_from_used(
        used_ids,
        prefix=BACKLOG_ID_PREFIX,
        length=config.unique_id_length,
    )


def _format_backlog_row(row: dict[str, str]) -> str:
    return "| " + " | ".join(_markdown_cell(row.get(col, "")) for col in BACKLOG_COLUMNS) + " |\n"


def _normalize_backlog_value(value: str, allowed: tuple[str, ...], label: str) -> str:
    for allowed_value in allowed:
        if value.strip().lower() == allowed_value.lower():
            return allowed_value
    raise SystemExit(f"Invalid backlog {label} '{value}'. Allowed: {', '.join(allowed)}.")


def _backlog_path(root: Path) -> Path:
    return root / ".project-workflow" / "BACKLOG.md"


def _ensure_backlog_file(backlog_path: Path) -> bool:
    backlog_path.parent.mkdir(parents=True, exist_ok=True)
    if backlog_path.exists():
        return False
    backlog_path.write_text(_backlog_template(), encoding="utf-8")
    return True


def _append_backlog_row(backlog_path: Path, row: dict[str, str]) -> None:
    lines, header_idx, _rows = _backlog_rows_for_update(backlog_path)
    insert_at = header_idx + 1
    while insert_at < len(lines) and lines[insert_at].lstrip().startswith("|"):
        insert_at += 1
    lines.insert(insert_at, _format_backlog_row(row))
    backlog_path.write_text("".join(lines), encoding="utf-8")


def _update_backlog_row(backlog_path: Path, row_id: str, updates: dict[str, str]) -> dict[str, str]:
    lines, _header_idx, rows = _backlog_rows_for_update(backlog_path)
    for row in rows:
        if row["ID"] != row_id:
            continue
        row.update(updates)
        lines[int(row["_line_idx"])] = _format_backlog_row(row)
        backlog_path.write_text("".join(lines), encoding="utf-8")
        return row
    raise SystemExit(f"No backlog row found for ID '{row_id}' in {backlog_path}.")


def _workflow_ref_exists(root: Path, ref: str) -> bool:
    workflow_dir = root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"
    if tracker_path.exists():
        rows = _parse_markdown_table(
            tracker_path,
            expected_columns=GLOBAL_TRACKER_COLUMNS,
            issues=[],
            label="Global tracker",
        )
        if any(row.get("ID") == ref for row in rows):
            return True

    if not tasks_dir.exists():
        return False
    return any(path.is_dir() and path.name.startswith(f"{ref}-") for path in tasks_dir.rglob("*"))


def _backlog_validation_issues(
    root: Path,
    backlog_path: Path,
    *,
    config: WorkflowConfig | None = None,
) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    if not backlog_path.exists():
        _add_issue(issues, "error", backlog_path, "Backlog is missing. Run `project backlog init`.")
        return issues
    config = config or _load_workflow_config(root)

    rows = _backlog_rows(backlog_path, issues)
    for duplicate_id in _duplicate_backlog_ids(rows):
        _add_issue(issues, "error", backlog_path, f"Backlog has duplicate ID '{duplicate_id}'.")

    required_columns = ("ID", "Title", "Type", "Priority", "Status", "Outcome")
    for row in rows:
        row_label = row.get("ID", "").strip() or f"line {row.get('_line_idx', '?')}"
        for column in required_columns:
            if not row.get(column, "").strip():
                _add_issue(issues, "error", backlog_path, f"{row_label} is missing {column}.")

        row_id = row.get("ID", "").strip()
        if row_id and not _valid_backlog_id(row_id, config=config):
            _add_issue(
                issues,
                "error",
                backlog_path,
                f"{row_label} has invalid ID '{row_id}'. Expected {BACKLOG_ID_PREFIX}-###.",
            )

        row_type = row.get("Type", "").strip()
        if row_type and row_type not in BACKLOG_TYPES:
            _add_issue(issues, "error", backlog_path, f"{row_label} has invalid Type '{row_type}'.")

        priority = row.get("Priority", "").strip()
        if priority and priority not in BACKLOG_PRIORITIES:
            _add_issue(
                issues,
                "error",
                backlog_path,
                f"{row_label} has invalid Priority '{priority}'.",
            )

        status = row.get("Status", "").strip()
        if status and status not in BACKLOG_STATUSES:
            _add_issue(issues, "error", backlog_path, f"{row_label} has invalid Status '{status}'.")

        promoted_to = row.get("Promoted To", "").strip()
        if status == "Promoted" and not promoted_to:
            _add_issue(issues, "error", backlog_path, f"{row_label} is Promoted but lacks Promoted To.")
        if promoted_to:
            if not _valid_workflow_ref_id(promoted_to, config=config):
                _add_issue(
                    issues,
                    "error",
                    backlog_path,
                    f"{row_label} has invalid Promoted To reference '{promoted_to}'.",
                )
            elif not _workflow_ref_exists(root, promoted_to):
                _add_issue(
                    issues,
                    "error",
                    backlog_path,
                    f"{row_label} Promoted To reference does not exist: {promoted_to}.",
                )
    return issues


def _backlog_source_section(row: dict[str, str]) -> str:
    notes = row.get("Notes", "").strip() or "None."
    promoted_from_status = row.get("Status", "").strip()
    return (
        "## Backlog Source\n\n"
        f"- ID: {row.get('ID', '').strip()}\n"
        f"- Title: {row.get('Title', '').strip()}\n"
        f"- Type: {row.get('Type', '').strip()}\n"
        f"- Priority: {row.get('Priority', '').strip()}\n"
        f"- Status before promotion: {promoted_from_status}\n"
        f"- Outcome: {row.get('Outcome', '').strip()}\n"
        f"- Notes: {notes}\n\n"
    )


def _requirements_with_backlog_source(requirements_text: str, row: dict[str, str]) -> str:
    marker = "## Goal\n\n"
    source = _backlog_source_section(row)
    if marker in requirements_text:
        return requirements_text.replace(marker, f"{source}{marker}", 1)
    return f"{requirements_text.rstrip()}\n\n{source}"


def _markdown_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value).replace("|", "\\|").strip()


def _extract_parent_ac_summaries(requirements_text: str) -> dict[str, str]:
    section = _markdown_section(requirements_text, "Acceptance Criteria (Verifiable)")
    if not section:
        section = _markdown_section(requirements_text, "Acceptance Criteria")
    summaries: dict[str, str] = {}
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")):
            stripped = stripped[1:].strip()
        match = re.match(r"^(AC\s*(\d+))\s*:\s*(.+)$", stripped, flags=re.IGNORECASE)
        if match:
            summaries[f"AC{match.group(2)}"] = match.group(3).strip()
    return summaries


DEFERRAL_COLUMNS = (
    "Parent AC",
    "Status",
    "Owner",
    "Decision Date",
    "Reason",
    "Follow-up",
    "Notes",
)


def _epic_deferrals(epic_dir: Path) -> dict[str, dict[str, str]]:
    deferrals_path = epic_dir / "DEFERRALS.md"
    if not deferrals_path.exists():
        return {}
    rows = _parse_markdown_table(
        deferrals_path,
        expected_columns=DEFERRAL_COLUMNS,
        issues=[],
        label="Epic deferrals",
    )
    return {row["Parent AC"]: row for row in rows if row.get("Parent AC")}


def _approved_deferral(row: dict[str, str] | None) -> bool:
    if not row:
        return False
    return (
        row.get("Status", "").strip().lower() == "approved"
        and bool(row.get("Owner", "").strip())
        and bool(row.get("Decision Date", "").strip())
        and bool(row.get("Reason", "").strip())
        and bool(row.get("Follow-up", "").strip())
    )


def _qa_passed(docs_text: str) -> bool:
    qa_section = _markdown_section(docs_text, "QA & Code Review").lower()
    return "verdict: pass" in qa_section


def _parent_ac_evidence_present(docs_text: str, ac_id: str) -> bool:
    evidence_section = _markdown_section(docs_text, "Parent AC Evidence")
    if not evidence_section or ac_id not in _extract_ac_ids(evidence_section):
        return False
    lowered = evidence_section.lower()
    return "pending" not in lowered and "____" not in evidence_section


def _evidence_value_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        stripped = value.strip()
        return not stripped or stripped == "____" or stripped.lower() in {"pending", "todo"}
    if isinstance(value, (list, tuple, set)):
        return not value
    return False


def _extract_explicit_recipe_ids(text: str) -> set[str]:
    recipes: set[str] = set()
    for recipe_id in PROOF_RECIPE_REQUIRED_FIELDS:
        if recipe_id in text:
            recipes.add(recipe_id)
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("| ---"):
            continue
        for recipe_id in PROOF_RECIPE_REQUIRED_FIELDS:
            if re.search(rf"\b{re.escape(recipe_id)}\b", stripped, flags=re.IGNORECASE):
                recipes.add(recipe_id)
    return recipes


def _triggered_proof_recipes(*texts: str) -> set[str]:
    combined = "\n".join(texts).lower()
    triggered = _extract_explicit_recipe_ids(combined)
    for recipe_id, patterns in PROOF_RECIPE_TRIGGER_PATTERNS.items():
        if any(re.search(pattern, combined, flags=re.IGNORECASE) for pattern in patterns):
            triggered.add(recipe_id)
    return triggered


def _load_structured_evidence(evidence_path: Path) -> tuple[list[dict[str, object]], list[str]]:
    if not evidence_path.exists():
        return [], [f"{STRUCTURED_EVIDENCE_FILENAME} is missing."]
    try:
        payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [f"{STRUCTURED_EVIDENCE_FILENAME} is not valid JSON: {exc}"]
    records = payload.get("claims") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        return [], [f"{STRUCTURED_EVIDENCE_FILENAME} must contain a `claims` array."]
    if not records:
        return [], [f"{STRUCTURED_EVIDENCE_FILENAME} contains no claim records."]
    typed_records: list[dict[str, object]] = []
    issues: list[str] = []
    for idx, record in enumerate(records, start=1):
        if isinstance(record, dict):
            typed_records.append(record)
        else:
            issues.append(f"claim record {idx} must be an object.")
    return typed_records, issues


def _evidence_artifact_exists(value: object, *, evidence_dir: Path) -> bool:
    if _evidence_value_missing(value):
        return False
    if not isinstance(value, str):
        return True
    stripped = value.strip()
    if re.match(r"^[a-z][a-z0-9+.-]*://", stripped, flags=re.IGNORECASE):
        return True
    artifact_path = Path(stripped)
    if not artifact_path.is_absolute():
        artifact_path = evidence_dir / artifact_path
    return artifact_path.exists()


def _local_evidence_artifact_path(value: object, *, evidence_dir: Path) -> Path | None:
    if _evidence_value_missing(value) or not isinstance(value, str):
        return None
    stripped = value.strip()
    if re.match(r"^[a-z][a-z0-9+.-]*://", stripped, flags=re.IGNORECASE):
        return None
    artifact_path = Path(stripped)
    if not artifact_path.is_absolute():
        artifact_path = evidence_dir / artifact_path
    return artifact_path if artifact_path.exists() else None


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def _normalized_evidence_hash(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if text.startswith("sha256:"):
        return text
    if re.fullmatch(r"[a-fA-F0-9]{64}", text):
        return f"sha256:{text.lower()}"
    return text


def _structured_doc_claims(text: str) -> dict[str, set[str]]:
    labels = {
        "reference artifact": "reference_artifact",
        "delivered artifact": "delivered_artifact",
        "execution target": "execution_target",
        "source artifact": "source_artifact",
        "source/artifact under test": "source_artifact",
        "artifact identity": "artifact_identity",
    }
    claims: dict[str, set[str]] = {}
    for line in text.splitlines():
        stripped = line.strip().lstrip("-*").strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        field = labels.get(key.strip().lower())
        if field and not _evidence_value_missing(value):
            claims.setdefault(field, set()).add(value.strip())
    return claims


def _structured_evidence_contradiction_issues(
    *, implementation_text: str, records: list[dict[str, object]]
) -> list[str]:
    doc_claims = _structured_doc_claims(implementation_text)
    if not doc_claims:
        return []
    evidence_values: dict[str, set[str]] = {}
    for record in records:
        for field in doc_claims:
            value = record.get(field)
            if not _evidence_value_missing(value):
                evidence_values.setdefault(field, set()).add(str(value).strip())
    issues: list[str] = []
    for field, claimed_values in sorted(doc_claims.items()):
        proven_values = evidence_values.get(field, set())
        contradictions = sorted(value for value in claimed_values if value not in proven_values)
        if contradictions and proven_values:
            issues.append(
                f"structured evidence: prose claims {field} "
                + ", ".join(contradictions)
                + " but structured evidence proves "
                + ", ".join(sorted(proven_values))
                + "."
            )
    return issues


def _structured_evidence_issues(
    *,
    requirements_path: Path,
    implementation_path: Path,
    parent_ac_ids: set[str] | None = None,
) -> list[str]:
    requirements_text = (
        requirements_path.read_text(encoding="utf-8") if requirements_path.exists() else ""
    )
    implementation_text = (
        implementation_path.read_text(encoding="utf-8") if implementation_path.exists() else ""
    )
    triggered_recipes = _triggered_proof_recipes(requirements_text, implementation_text)
    evidence_path = implementation_path.parent / STRUCTURED_EVIDENCE_FILENAME
    if not triggered_recipes:
        return []

    records, load_issues = _load_structured_evidence(evidence_path)
    issues = [f"structured evidence: {issue}" for issue in load_issues]
    if load_issues:
        return issues

    records_by_recipe: dict[str, list[dict[str, object]]] = {}
    passing_parent_acs: set[str] = set()
    for idx, record in enumerate(records, start=1):
        recipe_id = str(record.get("recipe", "")).strip()
        label = str(record.get("id", "")).strip() or f"claim record {idx}"
        if recipe_id not in PROOF_RECIPE_REQUIRED_FIELDS:
            issues.append(f"structured evidence: {label} has unknown recipe `{recipe_id}`.")
            continue
        records_by_recipe.setdefault(recipe_id, []).append(record)
        for field in PROOF_RECIPE_REQUIRED_FIELDS[recipe_id]:
            if _evidence_value_missing(record.get(field)):
                issues.append(
                    f"structured evidence: {label} missing required field `{field}` "
                    f"for recipe `{recipe_id}`."
                )
        invalid_substitutes = record.get("invalid_substitutes", [])
        if isinstance(invalid_substitutes, str):
            invalid_values = (
                []
                if invalid_substitutes.strip().lower() in {"", "none", "[]"}
                else [invalid_substitutes]
            )
        elif isinstance(invalid_substitutes, list):
            invalid_values = [str(value) for value in invalid_substitutes if str(value).strip()]
        else:
            invalid_values = [str(invalid_substitutes)]
        if invalid_values:
            issues.append(
                f"structured evidence: {label} records invalid substitute evidence: "
                + ", ".join(invalid_values)
            )
        text_blob = " ".join(str(value).lower() for value in record.values())
        for invalid_pattern in PROOF_RECIPE_INVALID_SUBSTITUTE_PATTERNS[recipe_id]:
            if invalid_pattern in text_blob:
                issues.append(
                    f"structured evidence: {label} uses invalid substitute for "
                    f"`{recipe_id}`: {invalid_pattern}."
                )
        if not _evidence_artifact_exists(
            record.get("evidence_artifact"),
            evidence_dir=implementation_path.parent,
        ):
            issues.append(
                f"structured evidence: {label} evidence_artifact does not exist or is empty."
            )
        local_artifact = _local_evidence_artifact_path(
            record.get("evidence_artifact"),
            evidence_dir=implementation_path.parent,
        )
        expected_hash = _normalized_evidence_hash(record.get("evidence_artifact_hash"))
        if local_artifact and expected_hash:
            actual_hash = _sha256_file(local_artifact)
            if expected_hash != actual_hash:
                issues.append(
                    f"structured evidence: {label} evidence_artifact_hash is stale "
                    f"(expected {actual_hash})."
                )
        if str(record.get("status", "")).strip().lower() == "pass":
            parent_ac = str(record.get("parent_ac", "")).strip()
            if parent_ac:
                passing_parent_acs.add(parent_ac)

    for recipe_id in sorted(triggered_recipes):
        passing_records = [
            record
            for record in records_by_recipe.get(recipe_id, [])
            if str(record.get("status", "")).strip().lower() == "pass"
        ]
        if not passing_records:
            issues.append(
                f"structured evidence: triggered recipe `{recipe_id}` has no passing claim record."
            )

    if parent_ac_ids:
        missing_parent_claims = sorted(parent_ac_ids - passing_parent_acs)
        if triggered_recipes and missing_parent_claims:
            issues.append(
                "structured evidence: missing passing claim records for parent ACs: "
                + ", ".join(missing_parent_claims)
            )
    issues.extend(
        _structured_evidence_contradiction_issues(
            implementation_text=implementation_text,
            records=records,
        )
    )
    return issues


def _epic_audit_rows(root: Path, epic_id: str) -> tuple[Path, list[dict[str, str]], list[str]]:
    workflow_dir = root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    epic_dir = _resolve_epic_dir(tasks_dir, epic_id)
    requirements_path = epic_dir / "REQUIREMENTS.md"
    epic_tracker_path = epic_dir / "TRACKER.md"
    if not requirements_path.exists():
        raise SystemExit(f"Missing epic requirements file: {requirements_path}")
    if not epic_tracker_path.exists():
        raise SystemExit(f"Missing epic tracker: {epic_tracker_path}")

    requirements_text = requirements_path.read_text(encoding="utf-8")
    ac_summaries = _extract_parent_ac_summaries(requirements_text)
    _lines, _header_idx, tracker_rows = _epic_tracker_rows(epic_tracker_path)
    deferrals = _epic_deferrals(epic_dir)
    proof_owner_map: dict[str, set[str]] = {}
    contract_path = _epic_contract_path(epic_dir)
    if contract_path.exists() and not _epic_contract_issues(epic_dir, requirements_text):
        proof_owner_map = _epic_contract_proof_owner_map(
            contract_path.read_text(encoding="utf-8")
        )
    audit_rows: list[dict[str, str]] = []
    gaps: list[str] = []

    for ac_id in sorted(ac_summaries):
        deferral = deferrals.get(ac_id)
        has_approved_deferral = _approved_deferral(deferral)
        mapped_rows = [
            row
            for row in tracker_rows
            if ac_id in _extract_ac_ids(_extract_parent_ac_coverage(row))
        ]
        child_labels: list[str] = []
        evidence_bits: list[str] = []
        verdict = "Deferred" if has_approved_deferral else "Pass"

        if not mapped_rows and not has_approved_deferral:
            verdict = "Gap"
            gaps.append(f"{ac_id}: no mapped child rows")

        for row in mapped_rows:
            row_id = row["ID"]
            status = row["Status"]
            child_labels.append(f"{row_id} ({status})")
            docs_rel = _clean_markdown_cell_path(row.get("Docs", ""))
            if status != "Complete" and not has_approved_deferral:
                verdict = "Gap"
                gaps.append(f"{ac_id}: {row_id} is {status}, not Complete")
            if not docs_rel:
                if not has_approved_deferral:
                    verdict = "Gap"
                    gaps.append(f"{ac_id}: {row_id} has no docs path")
                continue
            docs_path = root / ".project-workflow" / docs_rel
            if not docs_path.exists():
                if not has_approved_deferral:
                    verdict = "Gap"
                    gaps.append(f"{ac_id}: {row_id} docs path is missing")
                continue
            docs_text = docs_path.read_text(encoding="utf-8")
            requirements_path = docs_path.parent / "REQUIREMENTS.md"
            proof_owners = proof_owner_map.get(ac_id)
            if proof_owners is not None and row_id not in proof_owners:
                if not has_approved_deferral:
                    verdict = "Gap"
                    gaps.append(f"{ac_id}: {row_id} is not assigned as proof owner")
                continue
            structured_issues = _structured_evidence_issues(
                requirements_path=requirements_path,
                implementation_path=docs_path,
                parent_ac_ids={ac_id},
            )
            evidence_present = _parent_ac_evidence_present(docs_text, ac_id)
            qa_passed = _qa_passed(docs_text)
            if evidence_present and not structured_issues:
                evidence_bits.append(f"{row_id}: parent AC evidence recorded")
            elif not has_approved_deferral:
                verdict = "Gap"
                if structured_issues:
                    for issue in structured_issues:
                        gaps.append(f"{ac_id}: {row_id} {issue}")
                else:
                    gaps.append(f"{ac_id}: {row_id} lacks parent AC evidence")
            if qa_passed:
                evidence_bits.append(f"{row_id}: QA pass")
            elif not has_approved_deferral:
                verdict = "Gap"
                gaps.append(f"{ac_id}: {row_id} lacks QA pass verdict")

        deferral_text = "None"
        if deferral:
            deferral_text = (
                f"{deferral.get('Status', '')}: {deferral.get('Reason', '')} "
                f"(owner: {deferral.get('Owner', '')}; follow-up: {deferral.get('Follow-up', '')})"
            ).strip()
            if not has_approved_deferral:
                verdict = "Gap"
                gaps.append(f"{ac_id}: deferral is missing approval metadata or follow-up")

        audit_rows.append(
            {
                "Parent AC": ac_id,
                "Summary": ac_summaries[ac_id],
                "Child Rows": ", ".join(child_labels) if child_labels else "None",
                "Evidence": "; ".join(evidence_bits) if evidence_bits else "None",
                "Deferral": deferral_text,
                "Verdict": verdict,
            }
        )

    return epic_dir, audit_rows, gaps


def _format_acceptance_audit(epic_id: str, audit_rows: list[dict[str, str]]) -> str:
    lines = [
        "# Acceptance Audit\n",
        "\n",
        f"- Epic: {epic_id}\n",
        f"- Last updated: {date.today().isoformat()}\n",
        "\n",
        "| Parent AC | Summary | Child Rows | Evidence | Deferral | Verdict |\n",
        "| --- | --- | --- | --- | --- | --- |\n",
    ]
    for row in audit_rows:
        lines.append(
            "| "
            + " | ".join(
                _markdown_cell(row[column])
                for column in (
                    "Parent AC",
                    "Summary",
                    "Child Rows",
                    "Evidence",
                    "Deferral",
                    "Verdict",
                )
            )
            + " |\n"
        )
    return "".join(lines)


def _acceptance_map_status(row: dict[str, str]) -> str:
    verdict = row["Verdict"]
    child_rows = row["Child Rows"]
    evidence = row["Evidence"]
    deferral = row["Deferral"]
    if verdict == "Pass":
        return "Satisfied"
    if verdict == "Deferred":
        return "Deferred"
    if deferral != "None":
        return "Deferral needs metadata"
    if child_rows == "None":
        return "Unmapped"
    if evidence == "None":
        return "Mapped - evidence pending"
    return "Needs attention"


def _format_acceptance_map(epic_id: str, audit_rows: list[dict[str, str]]) -> str:
    lines = [
        "# Acceptance Map\n",
        "\n",
        f"- Epic: {epic_id}\n",
        f"- Last updated: {date.today().isoformat()}\n",
        "\n",
        "| Parent AC | Summary | Child Coverage | Evidence State | Deferral State | Status |\n",
        "| --- | --- | --- | --- | --- | --- |\n",
    ]
    for row in audit_rows:
        lines.append(
            "| "
            + " | ".join(
                _markdown_cell(value)
                for value in (
                    row["Parent AC"],
                    row["Summary"],
                    row["Child Rows"],
                    row["Evidence"],
                    row["Deferral"],
                    _acceptance_map_status(row),
                )
            )
            + " |\n"
        )
    lines.extend(
        [
            "\n",
            "## Notes\n",
            "\n",
            "- This is a working coverage map derived from requirements, the epic tracker, "
            "deferrals, and child task evidence.\n",
            "- `ACCEPTANCE-AUDIT.md` remains the closeout evidence artifact.\n",
        ]
    )
    return "".join(lines)


def _write_acceptance_map(root: Path, epic_id: str) -> Path:
    epic_dir, audit_rows, _gaps = _epic_audit_rows(root, epic_id)
    map_path = epic_dir / "ACCEPTANCE-MAP.md"
    map_path.write_text(_format_acceptance_map(epic_id, audit_rows), encoding="utf-8")
    return map_path


EPIC_RETRO_REQUIRED_SECTIONS = (
    "Lessons",
    "Follow-up Tasks",
    "Deferrals",
    "Missed In-Scope Work",
)

EPIC_GLOBAL_LIFECYCLE_STATUSES = (
    "Analysing",
    "Ready",
    "In Progress",
    "Closeout",
    "Complete",
)
OWNER_APPROVAL_HEADING = "Owner Approval"
LEGACY_ADOPTION_HEADING = "Legacy Adoption"
APPROVAL_IDENTITY_PREFIX = "sha256:"
APPROVAL_TRUE_VALUES = {"yes", "true", "approved"}
APPROVAL_FALSE_VALUES = {"", "no", "false", "not approved", "pending"}


def _epic_retro_issues(epic_dir: Path) -> list[str]:
    retro_path = epic_dir / "RETRO.md"
    if not retro_path.exists():
        return ["epic retro is missing RETRO.md"]
    retro_text = retro_path.read_text(encoding="utf-8")
    issues: list[str] = []
    for section in EPIC_RETRO_REQUIRED_SECTIONS:
        section_text = _markdown_section(retro_text, section)
        if not _section_has_substantive_text(section_text):
            issues.append(f"epic retro section '{section}' is missing or still placeholder")
    return issues


def _parse_key_value_section(section: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")):
            stripped = stripped[1:].strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        values[key.strip().lower()] = value.strip()
    return values


def _remove_markdown_section(text: str, heading: str) -> str:
    target = f"## {heading}".lower()
    lines = text.splitlines()
    output: list[str] = []
    skipping = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if stripped.lower() == target:
                skipping = True
                continue
            skipping = False
        if not skipping:
            output.append(line)
    return "\n".join(output).strip() + "\n"


def _approval_artifact_identity(requirements_text: str) -> str:
    comparable_text = _remove_markdown_section(requirements_text, OWNER_APPROVAL_HEADING)
    comparable_text = _remove_markdown_section(comparable_text, LEGACY_ADOPTION_HEADING)
    comparable_text = re.sub(r"\n{3,}", "\n\n", comparable_text).strip() + "\n"
    return APPROVAL_IDENTITY_PREFIX + hashlib.sha256(
        comparable_text.encode("utf-8")
    ).hexdigest()


def _approval_value_is_yes(value: str) -> bool:
    return value.strip().lower() in APPROVAL_TRUE_VALUES


def _approval_value_is_no(value: str) -> bool:
    return value.strip().lower() in APPROVAL_FALSE_VALUES


def _approval_source_invalid(source: str) -> bool:
    lowered = source.strip().lower()
    invalid_fragments = (
        "____",
        "pending",
        "not approved",
        "awaiting owner",
        "agent-only",
        "agent approved",
        "approved by agent",
    )
    return not lowered or any(fragment in lowered for fragment in invalid_fragments)


def _approval_envelope_issues(
    requirements_text: str,
    *,
    require_decomposition: bool = False,
    require_implementation: bool = False,
) -> list[str]:
    section = _markdown_section(requirements_text, OWNER_APPROVAL_HEADING)
    if not section:
        return [
            "owner input required: add `## Owner Approval` with an approved scope envelope."
        ]

    values = _parse_key_value_section(section)
    issues: list[str] = []

    if not _approval_value_is_yes(values.get("requirements reviewed by owner", "")):
        issues.append("owner input required: requirements have not been reviewed by the owner.")
    if not _approval_value_is_yes(values.get("acceptance criteria reviewed by owner", "")):
        issues.append(
            "owner input required: acceptance criteria have not been reviewed by the owner."
        )

    approved_for_decomposition = _approval_value_is_yes(
        values.get("approved for decomposition", "")
    )
    approved_for_implementation = _approval_value_is_yes(
        values.get("approved for implementation", "")
    )
    approved_for_envelope = _approval_value_is_yes(values.get("approved scope envelope", ""))

    if require_decomposition and not (approved_for_decomposition or approved_for_envelope):
        issues.append("owner input required: decomposition is outside the approved scope envelope.")
    if require_implementation and not (approved_for_implementation or approved_for_envelope):
        issues.append("owner input required: implementation is outside the approved scope envelope.")
    if (
        not require_decomposition
        and not require_implementation
        and not (approved_for_decomposition or approved_for_implementation or approved_for_envelope)
    ):
        issues.append("owner input required: no approved scope envelope is recorded.")

    if _approval_source_invalid(values.get("approved by", "")):
        issues.append("owner input required: approval must name the owner who approved it.")
    if _approval_source_invalid(values.get("approval date", "")):
        issues.append("owner input required: approval must include an approval date.")
    if _approval_source_invalid(values.get("approval note / source", "")):
        issues.append("owner input required: approval must include a non-agent approval source.")

    recorded_identity = values.get("approved artifact identity", "").strip()
    expected_identity = _approval_artifact_identity(requirements_text)
    if not recorded_identity:
        issues.append("owner input required: approval is missing approved artifact identity.")
    elif recorded_identity != expected_identity:
        issues.append(
            "owner input required: approval is stale because requirements or ACs changed "
            f"after approval (expected {expected_identity})."
        )
    return issues


def _approval_block(
    *,
    approved_by: str,
    source: str,
    approval_date: str,
    decomposition: bool,
    implementation: bool,
    artifact_identity: str,
) -> str:
    return (
        "## Owner Approval\n\n"
        "- Requirements reviewed by owner: Yes\n"
        "- Acceptance criteria reviewed by owner: Yes\n"
        f"- Approved for decomposition: {'Yes' if decomposition else 'No'}\n"
        f"- Approved for implementation: {'Yes' if implementation else 'No'}\n"
        "- Approved scope envelope: Yes\n"
        f"- Approved by: {approved_by.strip()}\n"
        f"- Approval date: {approval_date.strip()}\n"
        f"- Approval note / source: {source.strip()}\n"
        f"- Approved artifact identity: {artifact_identity}\n"
    )


def _requirements_with_approval_envelope(
    requirements_text: str,
    *,
    approved_by: str,
    source: str,
    decomposition: bool,
    implementation: bool,
) -> str:
    if _approval_source_invalid(approved_by):
        raise SystemExit("--approved-by must name the owner who approved the requirements.")
    if _approval_source_invalid(source):
        raise SystemExit("--source must describe the non-agent owner approval source.")
    without_approval = _remove_markdown_section(requirements_text, OWNER_APPROVAL_HEADING)
    artifact_identity = _approval_artifact_identity(without_approval)
    block = _approval_block(
        approved_by=approved_by,
        source=source,
        approval_date=date.today().isoformat(),
        decomposition=decomposition,
        implementation=implementation,
        artifact_identity=artifact_identity,
    )
    marker = "\n## Goal\n"
    if marker in without_approval:
        return without_approval.replace(marker, f"\n{block}{marker}", 1)
    return f"{without_approval.rstrip()}\n\n{block}"


def _legacy_adoption_block(
    *,
    approved_by: str,
    source: str,
    evidence_refreshed: bool,
) -> str:
    return (
        f"## {LEGACY_ADOPTION_HEADING}\n\n"
        "- Adopted legacy work: Yes\n"
        f"- Adopted by: {approved_by.strip()}\n"
        f"- Adoption date: {date.today().isoformat()}\n"
        f"- Adoption source: {source.strip()}\n"
        f"- Evidence refreshed after adoption: {'Yes' if evidence_refreshed else 'No'}\n"
        "- Evidence trust note: "
        + (
            "Existing evidence was refreshed after adoption."
            if evidence_refreshed
            else "Pre-adoption inferred evidence is untrusted until refreshed."
        )
        + "\n"
    )


def _requirements_with_legacy_adoption(
    requirements_text: str,
    *,
    approved_by: str,
    source: str,
    decomposition: bool,
    implementation: bool,
    evidence_refreshed: bool,
) -> str:
    requirements_text = _remove_markdown_section(requirements_text, LEGACY_ADOPTION_HEADING)
    approved_text = _requirements_with_approval_envelope(
        requirements_text,
        approved_by=approved_by,
        source=source,
        decomposition=decomposition,
        implementation=implementation,
    )
    without_adoption = _remove_markdown_section(approved_text, LEGACY_ADOPTION_HEADING)
    return (
        f"{without_adoption.rstrip()}\n\n"
        f"{_legacy_adoption_block(approved_by=approved_by, source=source, evidence_refreshed=evidence_refreshed)}"
    )


def _legacy_adoption_evidence_untrusted(requirements_text: str) -> bool:
    section = _markdown_section(requirements_text, LEGACY_ADOPTION_HEADING)
    if not section:
        return False
    values = _parse_key_value_section(section)
    adopted = _approval_value_is_yes(values.get("adopted legacy work", ""))
    refreshed = _approval_value_is_yes(values.get("evidence refreshed after adoption", ""))
    return adopted and not refreshed


def _requirements_approval_issues_for_path(
    requirements_path: Path,
    *,
    require_decomposition: bool = False,
    require_implementation: bool = False,
) -> list[str]:
    if not requirements_path.exists():
        return [f"missing requirements file: {requirements_path}"]
    requirements_text = requirements_path.read_text(encoding="utf-8")
    return _approval_envelope_issues(
        requirements_text,
        require_decomposition=require_decomposition,
        require_implementation=require_implementation,
    )


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
        return [*readiness_issues, *approval_issues, *contract_issues]

    epic_dir, audit_rows, audit_gaps = _epic_audit_rows(root, epic_id)
    mapping_gaps = [
        f"{row['Parent AC']}: no mapped child rows"
        for row in audit_rows
        if row["Child Rows"] == "None" and row["Deferral"] == "None"
    ]
    if target_status == "In Progress":
        return [*readiness_issues, *approval_issues, *contract_issues, *mapping_gaps]
    if target_status == "Closeout":
        return [*audit_gaps, *_epic_retro_issues(epic_dir)]
    return [f"unsupported epic lifecycle status: {target_status}"]


def _matching_gaps(gaps: list[str], pattern: str) -> list[str]:
    return [gap for gap in gaps if pattern in gap]


def _format_list_or_none(values: list[str]) -> str:
    return ", ".join(values) if values else "None"


def _epic_closeout_summary(
    audit_rows: list[dict[str, str]], gaps: list[str], *, complete_requested: bool
) -> str:
    total = len(audit_rows)
    passed = sum(1 for row in audit_rows if row["Verdict"] == "Pass")
    deferred = sum(1 for row in audit_rows if row["Verdict"] == "Deferred")
    gap_count = total - passed - deferred
    missing_mappings = [
        row["Parent AC"]
        for row in audit_rows
        if row["Child Rows"] == "None" and row["Deferral"] == "None"
    ]
    incomplete_children = _matching_gaps(gaps, " is ") + _matching_gaps(gaps, " has no docs path")
    missing_evidence = _matching_gaps(gaps, "lacks parent AC evidence")
    missing_qa = _matching_gaps(gaps, "lacks QA pass verdict")
    deferral_gaps = _matching_gaps(gaps, "deferral is missing")
    retro_gaps = _matching_gaps(gaps, "epic retro")
    approved_deferrals = [
        f"{row['Parent AC']}: {row['Deferral']}"
        for row in audit_rows
        if row["Deferral"] != "None" and row["Verdict"] == "Deferred"
    ]

    lines = [
        "Epic closeout summary:",
        f"- Parent ACs: {total} total, {passed} pass, {deferred} deferred, {gap_count} gap",
        f"- Missing mappings: {_format_list_or_none(missing_mappings)}",
        f"- Incomplete children/docs: {_format_list_or_none(incomplete_children)}",
        f"- Missing parent evidence: {_format_list_or_none(missing_evidence)}",
        f"- Missing QA pass: {_format_list_or_none(missing_qa)}",
        f"- Deferrals/follow-ups: {_format_list_or_none([*approved_deferrals, *deferral_gaps])}",
        f"- Epic retro: {_format_list_or_none(retro_gaps)}",
    ]
    if gaps:
        lines.append("- Next action: resolve the listed gaps or record approved deferrals with follow-up work.")
    elif complete_requested:
        lines.append("- Next action: global epic row can be marked Complete.")
    else:
        lines.append("- Next action: rerun closeout with --complete to mark the global epic row Complete.")
    return "\n".join(lines)


def _update_global_epic_status(
    tracker_path: Path, *, epic_id: str, new_status: str
) -> tuple[str, str]:
    lines, _header_idx, rows = _global_tracker_rows(tracker_path)
    for row in rows:
        if row["ID"] != epic_id:
            continue
        previous = row["Status"]
        row["Status"] = new_status
        lines[int(row["_line_idx"])] = _format_global_tracker_row(row)
        tracker_path.write_text("".join(lines), encoding="utf-8")
        return previous, new_status
    raise SystemExit(f"No global tracker row found for epic ID '{epic_id}' in {tracker_path}.")


def _epic_child_implementation_template(
    task_id: str, title: str, parent_ac_coverage: str, child_charter: str = ""
) -> str:
    parent_ac_value = parent_ac_coverage or "____"
    return (
        f"## User Story\n\n"
        f"As a ____, I want ____, so that ____.\n\n"
        f"## Parent AC Coverage\n\n"
        f"- {parent_ac_value}\n\n"
        f"{child_charter}"
        f"## Acceptance Criteria\n\n"
        f"- [ ] AC1: Covers parent AC(s) {parent_ac_value}: ____\n\n"
        f"## Validation\n\n"
        f"- AC1 / parent AC(s) {parent_ac_value}: ____\n\n"
        f"## Task List\n\n"
        f"| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        f"| --: | ----- | ----------- | ------------------- | ----------------- | ------ |\n"
        f"| 1 | ____ | ____ | AC1 / parent AC(s) {parent_ac_value}: ____ | ____ | To Do |\n\n"
        f"## Parent AC Evidence\n\n"
        f"- {parent_ac_value}: Pending implementation evidence. Recipe-triggered claims must "
        f"also be backed by `{STRUCTURED_EVIDENCE_FILENAME}`.\n\n"
        f"## QA & Code Review\n\n"
        f"- Verdict: ____\n"
        f"- Evidence: ____\n"
        f"- Findings: ____\n\n"
        f"## Retro\n\n"
        f"- Reusable lessons: ____\n"
        f"- Conventions or agent assets updated: ____\n"
        f"- Follow-up tasks: ____\n\n"
        f"## Notes\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n"
        f"- Created: {date.today().isoformat()}\n"
    )


def _structured_evidence_template(task_id: str, parent_ac_coverage: str) -> str:
    parent_ac_ids = sorted(
        _extract_ac_ids(parent_ac_coverage),
        key=lambda ac_id: int(ac_id[2:]),
    )
    if not parent_ac_ids:
        parent_ac_ids = [parent_ac_coverage or "____"]
    return json.dumps(
        {
            "task_id": task_id,
            "claims": [
                {
                    "id": f"CLM-{index:03d}",
                    "parent_ac": parent_ac,
                    "claim": "____",
                    "recipe": "visual-reference-fidelity",
                    "status": "pending",
                    "commit": "____",
                    "timestamp": "____",
                    "reference_artifact": "____",
                    "delivered_artifact": "____",
                    "comparison_method": "____",
                    "evidence_artifact": "____",
                    "evidence_artifact_hash": "____",
                    "invalid_substitutes": [],
                }
                for index, parent_ac in enumerate(parent_ac_ids, start=1)
            ],
        },
        indent=2,
    ) + "\n"


def _epic_child_requirements_template(
    task_id: str, title: str, parent_ac_coverage: str, child_charter: str = ""
) -> str:
    parent_ac_value = parent_ac_coverage or "____"
    return (
        f"# Requirements\n\n"
        f"## Summary\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n"
        f"- Parent AC Coverage: {parent_ac_value}\n"
        f"- Last updated: {date.today().isoformat()}\n\n"
        f"## Owner Approval\n\n"
        f"- Requirements reviewed by owner: No\n"
        f"- Acceptance criteria reviewed by owner: No\n"
        f"- Approved for decomposition: No\n"
        f"- Approved for implementation: No\n"
        f"- Approved scope envelope: No\n"
        f"- Approved by: Inherited from parent epic envelope when unchanged\n"
        f"- Approval date: Inherited from parent epic envelope when unchanged\n"
        f"- Approval note / source: Inherited from parent epic envelope when unchanged\n"
        f"- Approved artifact identity: Inherited from parent epic envelope when unchanged\n\n"
        f"{child_charter}"
        f"## Goal\n\n"
        f"Describe the user outcome this epic child must deliver for its parent AC coverage.\n\n"
        f"## Non-Goals\n\n"
        f"List what is explicitly out-of-scope.\n\n"
        f"## Users & Context\n\n"
        f"Who is affected and in what situation?\n\n"
        f"## Requirements (Outcome-Focused)\n\n"
        f"- ____\n\n"
        f"## Acceptance Criteria (Verifiable)\n\n"
        f"- AC1: Covers parent AC(s) {parent_ac_value}: ____\n\n"
        f"## Open Questions (Answer Needed)\n\n"
        f"- ____\n\n"
        f"## Decisions (Resolved)\n\n"
        f"- ____\n\n"
        f"## Validation Plan\n\n"
        f"- How we will verify child and parent acceptance criteria: ____\n"
    )


def _implementation_task_table_rows(
    docs_text: str,
) -> tuple[bool, list[dict[str, str]], list[int]]:
    lines = docs_text.splitlines()
    header_idx: int | None = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        if cells == list(IMPLEMENTATION_TASK_COLUMNS):
            header_idx = idx
            break

    if header_idx is None:
        return False, [], []

    rows: list[dict[str, str]] = []
    malformed_rows: list[int] = []
    row_idx = header_idx + 2
    while row_idx < len(lines):
        cells = _parse_markdown_table_cells(lines[row_idx])
        if cells is None:
            break
        if len(cells) != len(IMPLEMENTATION_TASK_COLUMNS):
            malformed_rows.append(row_idx + 1)
            row_idx += 1
            continue
        row = dict(zip(IMPLEMENTATION_TASK_COLUMNS, cells))
        row["_line_idx"] = str(row_idx + 1)
        rows.append(row)
        row_idx += 1

    return True, rows, malformed_rows


def _has_qa_review_evidence(text: str) -> bool:
    section = _markdown_section(text, "QA & Code Review")
    if not section or "____" in section:
        return False
    lowered = section.lower()
    return "verdict" in lowered and "evidence" in lowered


def _has_epic_acceptance_audit_evidence(docs_path: Path, row_id: str) -> bool:
    if not row_id.startswith("EPIC-"):
        return False
    audit_path = docs_path.parent / "ACCEPTANCE-AUDIT.md"
    if not audit_path.exists():
        return False
    try:
        audit_text = audit_path.read_text(encoding="utf-8")
    except OSError:
        return False
    if "| Parent AC |" not in audit_text or "____" in audit_text:
        return False
    return bool(re.search(r"\|\s*AC\d+\s*\|.*\|\s*Pass\s*\|", audit_text))


def _doctor_check_implementation_ac_mapping(
    *,
    docs_path: Path,
    docs_text: str,
    status: str,
    row_id: str,
    issues: list[DoctorIssue],
) -> None:
    if docs_path.name != "IMPLEMENTATION.md":
        return
    if status not in AC_MAPPED_IMPLEMENTATION_STATUSES:
        return

    criteria_ac_ids = _extract_declared_ac_ids(_markdown_section(docs_text, "Acceptance Criteria"))

    table_found, rows, malformed_rows = _implementation_task_table_rows(docs_text)
    if not table_found:
        if criteria_ac_ids:
            _add_issue(
                issues,
                "warning",
                docs_path,
                f"{row_id} has status '{status}' but no implementation task table maps work to AC IDs.",
            )
        return

    row_ac_ids: dict[str, set[str]] = {}
    for row in rows:
        row_label = row.get("ID") or f"line {row.get('_line_idx', '?')}"
        row_ac_ids[row_label] = _extract_ac_ids(row.get("Acceptance Criteria", ""))

    # Avoid adding warnings for historical plans that predate the AC-ID convention.
    if not criteria_ac_ids and not any(row_ac_ids.values()):
        return

    if malformed_rows:
        _add_issue(
            issues,
            "warning",
            docs_path,
            f"{row_id} has malformed implementation task table row(s): "
            + ", ".join(str(line) for line in malformed_rows),
        )

    missing_row_mappings = [row_label for row_label, ids in row_ac_ids.items() if not ids]
    if missing_row_mappings:
        _add_issue(
            issues,
            "warning",
            docs_path,
            f"{row_id} implementation task row(s) lack AC ID mapping: "
            + ", ".join(missing_row_mappings),
        )

    mapped_ids = {ac_id for ids in row_ac_ids.values() for ac_id in ids}
    if criteria_ac_ids:
        uncovered = sorted(criteria_ac_ids - mapped_ids)
        if uncovered:
            _add_issue(
                issues,
                "warning",
                docs_path,
                f"{row_id} acceptance criteria are not mapped to implementation tasks: "
                + ", ".join(uncovered),
            )

        unknown = sorted(mapped_ids - criteria_ac_ids)
        if unknown:
            _add_issue(
                issues,
                "warning",
                docs_path,
                f"{row_id} implementation task rows reference unknown AC IDs: "
                + ", ".join(unknown),
            )


def _add_issue(issues: list[DoctorIssue], severity: str, path: Path | str, message: str) -> None:
    issues.append(DoctorIssue(severity=severity, path=str(path), message=message))


def _parse_markdown_table(
    table_path: Path,
    *,
    expected_columns: tuple[str, ...],
    issues: list[DoctorIssue],
    label: str,
) -> list[dict[str, str]]:
    try:
        lines = table_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        _add_issue(issues, "error", table_path, f"Could not read {label}: {exc}")
        return []

    header_idx: int | None = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        if cells == list(expected_columns):
            header_idx = idx
            break

    if header_idx is None:
        expected = " | ".join(expected_columns)
        _add_issue(
            issues,
            "error",
            table_path,
            f"{label} schema mismatch. Expected header: '| {expected} |'.",
        )
        return []

    rows: list[dict[str, str]] = []
    row_idx = header_idx + 2
    while row_idx < len(lines):
        cells = _parse_markdown_table_cells(lines[row_idx])
        if cells is None:
            break
        if len(cells) != len(expected_columns):
            _add_issue(
                issues,
                "error",
                table_path,
                f"{label} row has {len(cells)} columns; expected {len(expected_columns)}.",
            )
            row_idx += 1
            continue
        row = dict(zip(expected_columns, cells))
        row["_line_idx"] = str(row_idx + 1)
        rows.append(row)
        row_idx += 1
    return rows


def _global_tracker_rows(tracker_path: Path) -> tuple[list[str], int, list[dict[str, str]]]:
    lines = tracker_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_idx: int | None = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        if cells == list(GLOBAL_TRACKER_COLUMNS):
            header_idx = idx
            break

    if header_idx is None:
        expected = " | ".join(GLOBAL_TRACKER_COLUMNS)
        raise SystemExit(
            "Global tracker schema mismatch. Expected header: "
            f"'| {expected} |' in {tracker_path}."
        )

    rows: list[dict[str, str]] = []
    row_idx = header_idx + 2
    while row_idx < len(lines):
        cells = _parse_markdown_table_cells(lines[row_idx])
        if cells is None:
            break
        if len(cells) != len(GLOBAL_TRACKER_COLUMNS):
            raise SystemExit(
                "Global tracker row has wrong number of columns. "
                f"Expected {len(GLOBAL_TRACKER_COLUMNS)} columns in {tracker_path}: "
                f"{lines[row_idx].strip()}"
            )
        row = dict(zip(GLOBAL_TRACKER_COLUMNS, cells))
        row["_line_idx"] = str(row_idx)
        rows.append(row)
        row_idx += 1

    return lines, header_idx, rows


def _format_global_tracker_row(row: dict[str, str]) -> str:
    return "| " + " | ".join(row[col] for col in GLOBAL_TRACKER_COLUMNS) + " |\n"


def _status_transition_allowed(current_status: str, new_status: str) -> bool:
    if current_status == new_status:
        return True
    return new_status in TASK_STATUS_TRANSITIONS.get(current_status, set())


def _validate_status_force_args(*, new_status: str, force: bool, reason: str | None) -> None:
    if reason and not force:
        raise SystemExit("--reason can only be used with --force.")
    if force and not (reason or "").strip():
        raise SystemExit("--force requires --reason with a short audit note.")
    if force and new_status == "Complete":
        raise SystemExit("--force is not supported for Complete transitions.")


READINESS_REQUIRED_SECTIONS = (
    "Goal",
    "Non-Goals",
    "Users & Context",
    "Requirements (Outcome-Focused)",
    "Acceptance Criteria (Verifiable)",
    "Open Questions (Answer Needed)",
    "Decisions (Resolved)",
    "Validation Plan",
)


def _section_has_placeholder(section: str) -> bool:
    lowered = section.lower()
    placeholder_phrases = (
        "____",
        "describe the user outcome",
        "list what is explicitly out-of-scope",
        "who is affected and in what situation",
        "how we will verify",
        "as a ____",
    )
    return any(phrase in lowered for phrase in placeholder_phrases)


def _section_has_substantive_text(section: str) -> bool:
    cleaned_lines = [
        line.strip(" -\t")
        for line in section.splitlines()
        if line.strip() and not set(line.strip()) <= {"-", "|", " "}
    ]
    return any(line and not _section_has_placeholder(line) for line in cleaned_lines)


def _is_discovery_work(requirements_text: str, implementation_text: str = "") -> bool:
    combined = f"{requirements_text}\n{implementation_text}".lower()
    return "type: discovery" in combined or "discovery: true" in combined


def _open_questions_resolved(section: str) -> bool:
    if _section_has_placeholder(section):
        return False
    lowered = section.lower()
    if "none" in lowered or "no blocking" in lowered:
        return True
    if "accepted risk" in lowered or "owner accepted" in lowered:
        return True
    return "?" not in section


def _requirements_readiness_issues(requirements_text: str) -> list[str]:
    issues: list[str] = []
    for heading in READINESS_REQUIRED_SECTIONS:
        section = _markdown_section(requirements_text, heading)
        if not section:
            issues.append(
                f"owner input required: add `## {heading}` to REQUIREMENTS.md."
            )
            continue
        if heading == "Open Questions (Answer Needed)":
            if not _open_questions_resolved(section):
                issues.append(
                    "owner input required: resolve open questions or record accepted risks "
                    "under `## Open Questions (Answer Needed)`."
                )
            continue
        if not _section_has_substantive_text(section):
            issues.append(
                f"owner input required: replace placeholder content under `## {heading}`."
            )

    if not _extract_ac_ids(_markdown_section(requirements_text, "Acceptance Criteria (Verifiable)")):
        issues.append(
            "owner input required: add stable acceptance criteria IDs under "
            "`## Acceptance Criteria (Verifiable)`."
        )
    return issues


def _implementation_readiness_issues(
    implementation_text: str, *, parent_ac_ids: set[str] | None = None
) -> list[str]:
    issues: list[str] = []
    required_sections = ("User Story", "Acceptance Criteria", "Validation", "Task List")
    for heading in required_sections:
        section = _markdown_section(implementation_text, heading)
        if not section:
            issues.append(f"agent action required: add `## {heading}` to IMPLEMENTATION.md.")
            continue
        if not _section_has_substantive_text(section):
            issues.append(
                f"agent action required: replace placeholder content under `## {heading}`."
            )

    criteria_ac_ids = _extract_declared_ac_ids(
        _markdown_section(implementation_text, "Acceptance Criteria")
    )
    if not criteria_ac_ids:
        issues.append("agent action required: add child AC IDs under `## Acceptance Criteria`.")

    table_found, rows, malformed_rows = _implementation_task_table_rows(implementation_text)
    if not table_found:
        issues.append("agent action required: add an AC-mapped implementation task table.")
    for line_number in malformed_rows:
        issues.append(
            f"agent action required: fix malformed implementation task table row at line {line_number}."
        )
    for row in rows:
        row_id = row.get("ID", "?")
        row_text = " ".join(row.get(col, "") for col in IMPLEMENTATION_TASK_COLUMNS)
        if _section_has_placeholder(row_text):
            issues.append(
                f"agent action required: replace placeholder content in implementation row {row_id}."
            )
        row_ac_ids = _extract_ac_ids(row.get("Acceptance Criteria", ""))
        if criteria_ac_ids and not row_ac_ids:
            issues.append(
                f"agent action required: map implementation row {row_id} to one or more child AC IDs."
            )

    if parent_ac_ids:
        parent_section = _markdown_section(implementation_text, "Parent AC Coverage")
        present_parent_ids = _extract_ac_ids(parent_section)
        missing_parent_ids = sorted(parent_ac_ids - present_parent_ids)
        if missing_parent_ids:
            issues.append(
                "agent action required: add parent AC coverage for "
                + ", ".join(missing_parent_ids)
                + " under `## Parent AC Coverage`."
            )
    return issues


def _discovery_readiness_issues(requirements_text: str, implementation_text: str = "") -> list[str]:
    combined = f"{requirements_text}\n{implementation_text}"
    issues: list[str] = []
    required_terms = {
        "question": "owner input required: record the discovery question to answer.",
        "decision": "owner input required: record the decision this discovery enables.",
        "boundary": "owner input required: record the discovery scope or time boundary.",
        "output": "owner input required: record the expected discovery output artifact.",
        "validation": "owner input required: record how the discovery output will be validated.",
    }
    lowered = combined.lower()
    for term, message in required_terms.items():
        if term not in lowered:
            issues.append(message)
    if _section_has_placeholder(combined):
        issues.append("agent action required: replace placeholders in the discovery artifact.")
    return issues


def _task_readiness_issues(
    *,
    requirements_text: str,
    implementation_text: str,
    parent_ac_ids: set[str] | None = None,
) -> list[str]:
    if _is_discovery_work(requirements_text, implementation_text):
        return _discovery_readiness_issues(requirements_text, implementation_text)
    return [
        *_requirements_readiness_issues(requirements_text),
        *_implementation_readiness_issues(implementation_text, parent_ac_ids=parent_ac_ids),
    ]


def _epic_requirements_readiness_issues(requirements_text: str) -> list[str]:
    if _is_discovery_work(requirements_text):
        return _discovery_readiness_issues(requirements_text)
    issues = _requirements_readiness_issues(requirements_text)
    parent_ac_ids = _extract_parent_ac_ids_from_requirements(requirements_text)
    if len(parent_ac_ids) < 1:
        issues.append(
            "owner input required: add stable parent AC IDs before epic decomposition."
        )
    return issues


def _format_readiness_block(label: str, issues: list[str]) -> str:
    lines = [f"{label} is not ready:"]
    lines.extend(f"- {issue}" for issue in issues)
    return "\n".join(lines)


def _status_requires_task_readiness(new_status: str) -> bool:
    return new_status in {"Ready", "Plan Confirmed", "In Progress", "Testing", "Review", "Complete"}


def _status_requires_epic_child_readiness(new_status: str) -> bool:
    return new_status in {"Testing", "Review", "Complete"}


def _resolve_global_task_docs(
    *, root: Path, tracker_path: Path, task_id: str
) -> tuple[Path, Path, dict[str, str]]:
    normalized_task_id = _normalize_task_status_id(task_id, root=root)
    _lines, _header_idx, rows = _global_tracker_rows(tracker_path)
    for row in rows:
        if row["ID"] != normalized_task_id:
            continue
        docs_rel = _clean_markdown_cell_path(row["Docs"])
        if not docs_rel:
            raise SystemExit(f"{task_id} has no docs path in {tracker_path}.")
        implementation_path = root / ".project-workflow" / docs_rel
        requirements_path = implementation_path.parent / "REQUIREMENTS.md"
        if not implementation_path.exists():
            raise SystemExit(f"{task_id} docs path does not exist: {implementation_path}")
        if not requirements_path.exists():
            raise SystemExit(f"{task_id} requirements path does not exist: {requirements_path}")
        return requirements_path, implementation_path, row
    raise SystemExit(f"No global tracker row found for ID '{task_id}' in {tracker_path}.")


def _resolve_epic_child_docs(
    *, root: Path, epic_tracker_path: Path, row_id: str
) -> tuple[Path, Path, dict[str, str]]:
    _lines, _header_idx, rows = _epic_tracker_rows(epic_tracker_path)
    for row in rows:
        if row["ID"] != row_id:
            continue
        docs_rel = _clean_markdown_cell_path(row.get("Docs", ""))
        if not docs_rel:
            raise SystemExit(f"{row_id} has no docs path in {epic_tracker_path}.")
        implementation_path = root / ".project-workflow" / docs_rel
        requirements_path = implementation_path.parent / "REQUIREMENTS.md"
        if not implementation_path.exists():
            raise SystemExit(f"{row_id} docs path does not exist: {implementation_path}")
        if not requirements_path.exists():
            raise SystemExit(f"{row_id} requirements path does not exist: {requirements_path}")
        return requirements_path, implementation_path, row
    raise SystemExit(f"No epic tracker row found for ID '{row_id}' in {epic_tracker_path}.")


def _task_ready_issues_for_paths(
    *, requirements_path: Path, implementation_path: Path, parent_ac_ids: set[str] | None = None
) -> list[str]:
    if not requirements_path.exists():
        return [f"agent action required: create requirements file `{requirements_path.name}`."]
    if not implementation_path.exists():
        return [f"agent action required: create implementation file `{implementation_path.name}`."]
    requirements_text = requirements_path.read_text(encoding="utf-8")
    implementation_text = implementation_path.read_text(encoding="utf-8")
    return _task_readiness_issues(
        requirements_text=requirements_text,
        implementation_text=implementation_text,
        parent_ac_ids=parent_ac_ids,
    )


def _resolve_fix_doc(
    *, root: Path, tracker_path: Path, fix_id: str
) -> tuple[Path, dict[str, str]]:
    normalized_fix_id = _normalize_fix_id(fix_id, root=root)
    _lines, _header_idx, rows = _global_tracker_rows(tracker_path)
    for row in rows:
        if row["ID"] != normalized_fix_id:
            continue
        docs_rel = _clean_markdown_cell_path(row["Docs"])
        if not docs_rel:
            raise SystemExit(f"{fix_id} has no docs path in {tracker_path}.")
        fix_path = root / ".project-workflow" / docs_rel
        if fix_path.name != "FIX.md" or not fix_path.exists():
            raise SystemExit(f"{fix_id} must point to an existing FIX.md: {fix_path}")
        return fix_path, row
    raise SystemExit(f"No global tracker row found for ID '{fix_id}' in {tracker_path}.")


def _fix_workspace_targets(root: Path) -> set[str] | None:
    workspace_path = root / ".project-workflow" / "workspace.json"
    if not workspace_path.exists():
        return None
    try:
        raw = json.loads(workspace_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid workspace metadata in {workspace_path}: {exc}") from exc
    components = raw.get("components", []) if isinstance(raw, dict) else []
    targets = {"."}
    if isinstance(components, dict):
        for component_id, component in components.items():
            targets.add(str(component_id))
            if isinstance(component, dict) and component.get("path"):
                targets.add(str(component["path"]))
    elif isinstance(components, list):
        for component in components:
            if not isinstance(component, dict):
                continue
            for field in ("id", "name", "path"):
                if component.get(field):
                    targets.add(str(component[field]))
    return targets


def _split_fix_repos(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,\n]", value) if part.strip()]


def _fix_triage_issues(
    root: Path, fix_text: str, *, require_active_disposition: bool = True
) -> list[str]:
    issues: list[str] = []
    required_fields = {
        "Report": (
            "observed or requested",
            "expected",
            "affected users or systems",
            "delivered baseline",
            "report evidence",
        ),
        "Routing": ("rationale", "bounded correction"),
        "Classification": ("type", "mode", "severity", "impact", "urgency", "owner"),
        "Risk": ("risk level", "risks", "rollback or containment"),
        "Fix Plan": (
            "scope",
            "non-goals",
            "affected target",
            "primary repo",
            "repos touched",
            "branch, pr, and evidence links",
            "verification plan",
        ),
    }
    parsed: dict[str, dict[str, str]] = {}
    for heading, fields in required_fields.items():
        values = _fix_values(fix_text, heading)
        parsed[heading] = values
        for field in fields:
            if _fix_value_missing(values.get(field)):
                issues.append(f"complete `{field}` under `## {heading}`")

    classification = parsed.get("Classification", {})
    if classification.get("type") not in FIX_CLASSIFICATIONS:
        issues.append("set classification `Type` to " + ", ".join(FIX_CLASSIFICATIONS))
    if classification.get("mode") not in FIX_MODES:
        issues.append("set classification `Mode` to Normal or Hotfix")
    if classification.get("severity") not in FIX_SEVERITIES:
        issues.append("set classification `Severity` to " + ", ".join(FIX_SEVERITIES))
    risk = parsed.get("Risk", {})
    if risk.get("risk level") not in FIX_RISK_LEVELS:
        issues.append("set `Risk level` to " + ", ".join(FIX_RISK_LEVELS))

    routing = _fix_values(fix_text, "Routing")
    if routing.get("decision", "").lower() != "fix":
        issues.append("record routing `Decision: Fix`")
    if routing.get("new outcome or material decisions", "").lower() not in {"no", "none"}:
        issues.append("promote work that requires a new outcome or material decision")
    if routing.get("independent work items", "").lower() not in {"one", "1"}:
        issues.append("promote work containing multiple independent work items")

    outcome = _fix_values(fix_text, "Outcome")
    if require_active_disposition and outcome.get("disposition") != FIX_ACTIVE_DISPOSITION:
        issues.append(f"keep active triage `Disposition: {FIX_ACTIVE_DISPOSITION}`")

    workspace_targets = _fix_workspace_targets(root)
    if workspace_targets is not None:
        plan = parsed.get("Fix Plan", {})
        primary_repo = plan.get("primary repo", "")
        repos_touched = _split_fix_repos(plan.get("repos touched", ""))
        invalid = [repo for repo in [primary_repo, *repos_touched] if repo not in workspace_targets]
        if invalid:
            issues.append(
                "use workspace component identities/paths for repo metadata; unknown: "
                + ", ".join(sorted(set(invalid)))
            )
        repo_rows = _markdown_table_rows_from_section(
            fix_text,
            "Fix Plan",
            expected_columns=FIX_REPOSITORY_LINK_COLUMNS,
        )
        rows_by_repo = {row["Repo"]: row for row in repo_rows}
        for repo in repos_touched:
            row = rows_by_repo.get(repo)
            if row is None:
                issues.append(f"add a repository-links row for workspace repo `{repo}`")
                continue
            for field in ("Branch", "PR", "Evidence"):
                if _fix_value_missing(row.get(field)):
                    issues.append(
                        f"record `{field}` (or an explicit None/N/A) for workspace repo `{repo}`"
                    )
    return issues


def _fix_hotfix_safety_issues(root: Path, fix_text: str) -> list[str]:
    issues = _fix_triage_issues(root, fix_text)
    classification = _fix_values(fix_text, "Classification")
    if classification.get("mode") != "Hotfix":
        issues.append("set classification `Mode: Hotfix` for emergency bypass")
    for heading, field in (
        ("Report", "report evidence"),
        ("Risk", "rollback or containment"),
        ("Fix Plan", "verification plan"),
    ):
        if _fix_value_missing(_fix_values(fix_text, heading).get(field)):
            issues.append(f"record emergency safety field `{field}`")
    return list(dict.fromkeys(issues))


def _fix_closeout_issues(fix_text: str) -> list[str]:
    issues: list[str] = []
    verification = _fix_values(fix_text, "Verification")
    for field in (
        "delivered scope",
        "verification result",
        "adjacent behavior checked",
        "regression evidence",
        "residual risk",
    ):
        if _fix_value_missing(verification.get(field)):
            issues.append(f"complete `{field}` under `## Verification`")
    original_result = verification.get("original acceptance criteria result", "")
    if _fix_value_missing(original_result):
        issues.append("complete `original acceptance criteria result` under `## Verification`")
    originating_work = _fix_values(fix_text, "Related Work").get("originating work", "")
    if (
        _extract_workflow_ref_ids(originating_work)
        and original_result.strip().lower() in {"not applicable", "n/a", "none"}
    ):
        issues.append(
            "record linked original acceptance-criteria results or an explicit reason "
            "they do not apply"
        )
    outcome = _fix_values(fix_text, "Outcome")
    if outcome.get("disposition") not in FIX_TERMINAL_DISPOSITIONS:
        issues.append("set a terminal Outcome disposition")
    for field in ("decision", "closed by", "closed date"):
        if _fix_value_missing(outcome.get(field)):
            issues.append(f"complete `{field}` under `## Outcome`")
    return issues


def _fix_non_delivery_closeout_issues(fix_text: str) -> list[str]:
    issues: list[str] = []
    outcome = _fix_values(fix_text, "Outcome")
    if outcome.get("disposition") not in {"Duplicate", "Rejected", "Deferred", "Promoted"}:
        issues.append("set a non-delivery terminal Outcome disposition")
    for field in ("decision", "closed by", "closed date"):
        if _fix_value_missing(outcome.get(field)):
            issues.append(f"complete `{field}` under `## Outcome`")
    if outcome.get("disposition") == "Promoted" and _fix_value_missing(
        outcome.get("promoted to")
    ):
        issues.append("complete `promoted to` under `## Outcome`")
    return issues


def _update_fix_tracker_status(
    *, root: Path, tracker_path: Path, fix_id: str, new_status: str
) -> tuple[str, str]:
    normalized_fix_id = _normalize_fix_id(fix_id, root=root)
    lines, _header_idx, rows = _global_tracker_rows(tracker_path)
    for row in rows:
        if row["ID"] != normalized_fix_id:
            continue
        current_status = row["Status"]
        if new_status not in FIX_STATUS_TRANSITIONS:
            raise SystemExit(f"Invalid Fix status '{new_status}'.")
        if new_status != current_status and new_status not in FIX_STATUS_TRANSITIONS.get(
            current_status, set()
        ):
            raise SystemExit(
                f"Illegal Fix status transition for {fix_id}: {current_status} -> {new_status}."
            )
        fix_path, _row = _resolve_fix_doc(
            root=root, tracker_path=tracker_path, fix_id=normalized_fix_id
        )
        fix_text = fix_path.read_text(encoding="utf-8")
        if current_status == "To Do" and new_status == "In Progress":
            issues = _fix_hotfix_safety_issues(root, fix_text)
            if issues:
                raise SystemExit(_format_readiness_block(fix_id, issues))
        if new_status == "Ready":
            issues = _fix_triage_issues(root, fix_text)
            if issues:
                raise SystemExit(_format_readiness_block(fix_id, issues))
        if new_status in {"In Progress", "Testing", "Review"} and current_status != "To Do":
            issues = _fix_triage_issues(root, fix_text)
            if issues:
                raise SystemExit(_format_readiness_block(fix_id, issues))
        if new_status == "Complete":
            raise SystemExit("Use `project fix close` to complete a Fix.")
        if new_status == "N/A":
            raise SystemExit(
                "Use `project fix close` for Duplicate/Rejected/Deferred or "
                "`project fix promote` for Promoted."
            )
        if current_status == new_status:
            return current_status, new_status
        row["Status"] = new_status
        lines[int(row["_line_idx"])] = _format_global_tracker_row(row)
        tracker_path.write_text("".join(lines), encoding="utf-8")
        fix_path.write_text(
            _replace_fix_field(fix_text, "Summary", "Status", new_status),
            encoding="utf-8",
        )
        return current_status, new_status
    raise SystemExit(f"No global tracker row found for ID '{fix_id}' in {tracker_path}.")


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
            )
            if structured_issues:
                raise SystemExit(_format_readiness_block(row_id, structured_issues))
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
            if not _has_qa_review_evidence(docs_text):
                raise SystemExit(
                    f"{row_id} cannot move to Complete without non-placeholder "
                    "QA/code-review evidence."
                )

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

        if current_status == new_status:
            return current_status, new_status

        row["Status"] = new_status
        line_idx = int(row["_line_idx"])
        lines[line_idx] = _format_global_tracker_row(row)
        tracker_path.write_text("".join(lines), encoding="utf-8")
        return current_status, new_status

    raise SystemExit(f"No global tracker row found for ID '{row_id}' in {tracker_path}.")


def _epic_tracker_header_columns(cells: list[str] | None) -> tuple[str, ...] | None:
    if cells == list(EPIC_TRACKER_COLUMNS):
        return EPIC_TRACKER_COLUMNS
    if cells == list(LEGACY_EPIC_TRACKER_COLUMNS):
        return LEGACY_EPIC_TRACKER_COLUMNS
    return None


def _epic_tracker_rows(epic_tracker_path: Path) -> tuple[list[str], int, list[dict[str, str]]]:
    lines = epic_tracker_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_idx: Optional[int] = None
    header_columns: tuple[str, ...] | None = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        columns = _epic_tracker_header_columns(cells)
        if columns is not None:
            header_idx = idx
            header_columns = columns
            break

    if header_idx is None or header_columns is None:
        expected = " | ".join(EPIC_TRACKER_COLUMNS)
        legacy = " | ".join(LEGACY_EPIC_TRACKER_COLUMNS)
        raise SystemExit(
            "Epic tracker schema mismatch. Expected header: "
            f"'| {expected} |' in {epic_tracker_path}. "
            f"Legacy header is still accepted: '| {legacy} |'."
        )

    rows: list[dict[str, str]] = []
    row_idx = header_idx + 2  # skip divider row
    while row_idx < len(lines):
        cells = _parse_markdown_table_cells(lines[row_idx])
        if cells is None:
            break
        if len(cells) != len(header_columns):
            raise SystemExit(
                "Epic tracker row has wrong number of columns. "
                f"Expected {len(header_columns)} columns in {epic_tracker_path}: "
                f"{lines[row_idx].strip()}"
            )
        row = dict(zip(header_columns, cells))
        row.setdefault("Parent ACs", "")
        status = row["Status"]
        if status and status not in EPIC_TRACKER_STATUSES:
            raise SystemExit(
                "Epic tracker contains invalid status "
                f"'{status}'. Allowed: {', '.join(EPIC_TRACKER_STATUSES)}."
            )
        row["_line_idx"] = str(row_idx)
        row[EPIC_TRACKER_FORMAT_KEY] = "\x1f".join(header_columns)
        rows.append(row)
        row_idx += 1

    return lines, header_idx, rows


def _format_epic_tracker_row(row: dict[str, str]) -> str:
    format_columns_value = row.get(EPIC_TRACKER_FORMAT_KEY)
    columns = (
        tuple(format_columns_value.split("\x1f"))
        if format_columns_value
        else EPIC_TRACKER_COLUMNS
    )
    return "| " + " | ".join(row.get(col, "") for col in columns) + " |\n"


def _update_epic_tracker_row_status(
    epic_tracker_path: Path,
    *,
    row_id: str,
    expected_from: str,
    new_status: str,
) -> dict[str, str]:
    lines, _header_idx, rows = _epic_tracker_rows(epic_tracker_path)

    for row in rows:
        if row["ID"] != row_id:
            continue
        current = row["Status"]
        if current != expected_from:
            raise SystemExit(
                f"Row {row_id} must be '{expected_from}' before this operation; "
                f"found '{current}'."
            )
        row["Status"] = new_status
        line_idx = int(row["_line_idx"])
        lines[line_idx] = _format_epic_tracker_row(row)
        epic_tracker_path.write_text("".join(lines), encoding="utf-8")
        return row

    raise SystemExit(f"No epic tracker row found for ID '{row_id}' in {epic_tracker_path}.")


def _epic_tracker_row_by_id(epic_tracker_path: Path, row_id: str) -> dict[str, str]:
    _lines, _header_idx, rows = _epic_tracker_rows(epic_tracker_path)
    for row in rows:
        if row["ID"] == row_id:
            return row
    raise SystemExit(f"No epic tracker row found for ID '{row_id}' in {epic_tracker_path}.")


def _epic_status_transition_allowed(current_status: str, new_status: str) -> bool:
    if current_status == new_status:
        return True
    return new_status in EPIC_STATUS_TRANSITIONS.get(current_status, set())


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
            )
            if structured_issues:
                raise SystemExit(_format_readiness_block(row_id, structured_issues))
            if not _has_qa_review_evidence(docs_text):
                raise SystemExit(
                    f"{row_id} cannot move to Complete without non-placeholder "
                    "QA/code-review evidence."
                )
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
                    )
                )
            if readiness_issues:
                raise SystemExit(_format_readiness_block(row_id, readiness_issues))
        row["Status"] = new_status
        lines[int(row["_line_idx"])] = _format_epic_tracker_row(row)
        epic_tracker_path.write_text("".join(lines), encoding="utf-8")
        return current_status, new_status

    raise SystemExit(f"No epic tracker row found for ID '{row_id}' in {epic_tracker_path}.")


def _resolve_epic_dir(tasks_dir: Path, epic_id: str) -> Path:
    matches = [p for p in tasks_dir.glob(f"{epic_id}-*") if p.is_dir()]
    if not matches:
        raise SystemExit(
            f"Could not find epic folder for {epic_id}. Expected a folder like '{epic_id}-...'."
        )
    if len(matches) > 1:
        raise SystemExit(
            f"Multiple epic folders found for {epic_id}: "
            + ", ".join(p.name for p in matches)
            + ". Use a unique epic ID."
        )
    return matches[0]


def _next_sequential_id_from_used(used_ids: set[str], *, prefix: str) -> str:
    max_value = 0
    row_re = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    for used_id in used_ids:
        match = row_re.match(used_id)
        if match:
            max_value = max(max_value, int(match.group(1)))
    return f"{prefix}-{max_value + 1:0{ID_PADDING}d}"


def _next_unique_id_from_used(used_ids: set[str], *, prefix: str, length: int) -> str:
    for _attempt in range(1000):
        suffix = "".join(secrets.choice(UNIQUE_ID_ALPHABET) for _ in range(length))
        if suffix.isdigit():
            continue
        candidate = f"{prefix}-{suffix}"
        if candidate not in used_ids:
            return candidate
    raise SystemExit(f"Could not allocate a unique {prefix} ID after 1000 attempts.")


def _next_task_id_from_used(
    used_ids: set[str], *, prefix: str, config: WorkflowConfig, kind: str
) -> str:
    if _id_generation_mode(config, kind) == "unique":
        return _next_unique_id_from_used(
            used_ids,
            prefix=prefix,
            length=config.unique_id_length,
        )
    return _next_sequential_id_from_used(used_ids, prefix=prefix)


def _used_ids_for_prefix(tasks_dir: Path, tracker_path: Path, *, prefix: str) -> set[str]:
    used_ids: set[str] = set()
    dir_re = re.compile(rf"^{re.escape(prefix)}-([A-Za-z0-9]+)(?:-|$)")
    id_re = re.compile(rf"\b({re.escape(prefix)}-[A-Za-z0-9]+)\b")

    if tasks_dir.exists():
        for path in tasks_dir.rglob("*"):
            if not path.is_dir():
                continue
            match = dir_re.match(path.name)
            if match:
                suffix = match.group(1).upper()
                if suffix.isdigit():
                    suffix = f"{int(suffix):0{ID_PADDING}d}"
                used_ids.add(f"{prefix}-{suffix}")

    tracker_paths = [tracker_path]
    if tasks_dir.exists():
        tracker_paths.extend(sorted(tasks_dir.rglob("TRACKER.md")))
    backlog_path = tracker_path.parent / "BACKLOG.md"
    if backlog_path.exists():
        tracker_paths.append(backlog_path)

    for candidate_tracker in tracker_paths:
        if not candidate_tracker.exists():
            continue
        try:
            tracker_text = candidate_tracker.read_text(encoding="utf-8")
        except OSError:
            continue
        for match in id_re.finditer(tracker_text):
            used_ids.add(match.group(1).upper())

    return used_ids


def _decompose_epic_requirements_to_titles(
    requirements_text: str, *, limit: int
) -> list[tuple[str, str | None]]:
    lines = requirements_text.splitlines()
    ac_bullets: list[tuple[str, str | None]] = []
    requirement_bullets: list[tuple[str, str | None]] = []
    active_section: str | None = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            if heading.startswith("acceptance criteria"):
                active_section = "acceptance"
            elif heading.startswith("requirements"):
                active_section = "requirements"
            else:
                active_section = None
            continue
        if active_section is None:
            continue

        bullet: Optional[str] = None
        if stripped.startswith(("-", "*")):
            bullet = stripped[1:].strip()
        else:
            numbered_match = re.match(r"^\d+[.)]\s+(.*)$", stripped)
            if numbered_match:
                bullet = numbered_match.group(1).strip()
            elif re.match(r"^(as a|as an)\b", stripped, flags=re.IGNORECASE):
                bullet = stripped

        if bullet is None:
            continue
        if not bullet or bullet == "____":
            continue

        bullet = re.sub(r"\s+", " ", bullet)
        ac_id: str | None = None
        ac_match = re.match(r"^AC\s*(\d+)\s*:\s*(.+)$", bullet, flags=re.IGNORECASE)
        if ac_match:
            ac_id = f"AC{ac_match.group(1)}"
            bullet = ac_match.group(2).strip()
        bullet = re.sub(r"^A user can\s+", "", bullet, flags=re.IGNORECASE)
        bullet = re.sub(r"^Users can\s+", "", bullet, flags=re.IGNORECASE)
        bullet = bullet[:1].upper() + bullet[1:] if bullet else bullet
        if active_section == "acceptance":
            ac_bullets.append((bullet.rstrip("."), ac_id))
        else:
            requirement_bullets.append((bullet.rstrip("."), ac_id))

    candidates = ac_bullets or requirement_bullets
    return candidates[:limit]


def _guidance_words(text: str) -> set[str]:
    ignored = {
        "and",
        "for",
        "the",
        "that",
        "with",
        "work",
        "task",
        "tasks",
        "into",
        "such",
        "from",
        "this",
    }
    return {
        word
        for word in re.split(r"[^a-z0-9]+", text.lower())
        if len(word) >= 3 and word not in ignored
    }


def _classify_task_prefix(title: str, config: WorkflowConfig) -> tuple[str, str]:
    title_words = _guidance_words(title)
    scored: list[tuple[int, str, list[str]]] = []
    for prefix in config.task_id_prefixes:
        score = 0
        reasons: list[str] = []
        if prefix.lower() in title.lower():
            score += 4
            reasons.append(f"title mentions {prefix}")

        guidance = config.prefix_guidance.get(prefix, "")
        matched_words = sorted(title_words & _guidance_words(guidance))
        if matched_words:
            score += len(matched_words)
            reasons.append("matched guidance: " + ", ".join(matched_words[:5]))
        scored.append((score, prefix, reasons))

    scored.sort(key=lambda item: (-item[0], config.task_id_prefixes.index(item[1])))
    best_score, best_prefix, best_reasons = scored[0]
    if best_score <= 0:
        return (
            config.default_task_id_prefix,
            f"Prefix {config.default_task_id_prefix}: default prefix; no guidance match",
        )
    return best_prefix, f"Prefix {best_prefix}: " + "; ".join(best_reasons)


def _append_epic_tracker_rows(epic_tracker_path: Path, rows_to_add: list[dict[str, str]]) -> None:
    lines, header_idx, rows = _epic_tracker_rows(epic_tracker_path)
    header_cells = _parse_markdown_table_cells(lines[header_idx])
    header_columns = _epic_tracker_header_columns(header_cells) or EPIC_TRACKER_COLUMNS
    existing_ids = {row["ID"] for row in rows}
    duplicate_ids = [row["ID"] for row in rows_to_add if row["ID"] in existing_ids]
    if duplicate_ids:
        raise SystemExit(
            "Cannot append decomposition proposals; epic tracker already contains IDs: "
            + ", ".join(sorted(set(duplicate_ids)))
        )

    insert_at = header_idx + 2 + len(rows)
    for row in rows_to_add:
        row[EPIC_TRACKER_FORMAT_KEY] = "\x1f".join(header_columns)
    formatted = [_format_epic_tracker_row(row) for row in rows_to_add]
    lines[insert_at:insert_at] = formatted
    epic_tracker_path.write_text("".join(lines), encoding="utf-8")


def _normalize_agent(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    aliases = {
        "copilot": "github-copilot",
        "github": "github-copilot",
        "github-copilot": "github-copilot",
        "claude": "claude-code",
        "claude-code": "claude-code",
        "codex": "codex",
        "openai": "codex",
        "openai-codex": "codex",
        "cursor": "cursor",
    }
    if normalized not in aliases:
        allowed = ", ".join(sorted(AGENT_CHOICES))
        raise argparse.ArgumentTypeError(
            f"Unsupported agent '{value}'. Choose one of: {allowed}."
        )
    return aliases[normalized]


def _split_frontmatter(content: str) -> tuple[str, str]:
    """Return (frontmatter, body) from markdown content with YAML frontmatter."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, flags=re.DOTALL)
    if not match:
        return "", content
    return match.group(1), match.group(2)


def _extract_frontmatter_value(frontmatter: str, key: str) -> Optional[str]:
    pattern = rf"^{re.escape(key)}:\s*(.+)$"
    match = re.search(pattern, frontmatter, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def _prompt_filename_to_agent_name(prompt_file: str) -> str:
    base_name = prompt_file.replace(".prompt.md", "")
    canonical_slugs = {
        "QAReview": "qa-review",
    }
    return f"project-{canonical_slugs.get(base_name, slug_kebab_lower(base_name))}"


def _prompt_filename_to_claude_agent_name(prompt_file: str) -> str:
    return _prompt_filename_to_agent_name(prompt_file)


def _prompt_filename_to_cursor_agent_name(prompt_file: str) -> str:
    return _prompt_filename_to_agent_name(prompt_file)


def _to_claude_agent_markdown(prompt_content: str, agent_name: str) -> str:
    """Convert packaged prompt markdown into Claude subagent markdown format."""
    frontmatter, body = _split_frontmatter(prompt_content)
    description = _extract_frontmatter_value(frontmatter, "description") or agent_name
    escaped_description = description.replace('"', r'\"')
    return (
        "---\n"
        f"name: {agent_name}\n"
        f"description: \"{escaped_description}\"\n"
        "---\n\n"
        f"{body.lstrip()}"
    )


def _to_cursor_agent_markdown(prompt_content: str, agent_name: str) -> str:
    """Convert packaged prompt markdown into Cursor subagent markdown format."""
    frontmatter, body = _split_frontmatter(prompt_content)
    description = _extract_frontmatter_value(frontmatter, "description") or agent_name
    escaped_description = description.replace('"', r'\"')
    return (
        "---\n"
        f"name: {agent_name}\n"
        f"description: \"{escaped_description}\"\n"
        "---\n\n"
        f"{body.lstrip()}"
    )


def _update_tracker(
    tracker_path: Path,
    *,
    spec: TaskSpec,
    status: str,
    docs_rel_path: str,
    on_duplicate: str = "error",
) -> bool:
    tracker = tracker_path.read_text(encoding="utf-8")
    row = f"| {spec.task_id} | {spec.title} | {status} | `{docs_rel_path}` |\n"
    lines = tracker.splitlines(keepends=True)

    # Find the stories table: insert after the last row in the table.
    table_header_idx = None
    header_re = re.compile(r"^\|\s*ID\s*\|\s*Title\s*\|\s*Status\s*\|\s*Docs\s*\|\s*$")
    for idx, line in enumerate(lines):
        if header_re.match(line.strip()):
            table_header_idx = idx
            break

    if table_header_idx is None:
        raise SystemExit(
            "Could not find Stories table header in TRACKER.md. "
            "Expected a line: '| ID | Title | Status | Docs |'"
        )

    existing_row_idx: Optional[int] = None
    id_row_re = re.compile(rf"^\|\s*{re.escape(spec.task_id)}\s*\|")
    for idx, line in enumerate(lines):
        if id_row_re.match(line.strip()):
            existing_row_idx = idx
            break

    if existing_row_idx is not None:
        if lines[existing_row_idx].strip() == row.strip() and on_duplicate == "skip":
            return False
        raise SystemExit(
            f"Tracker already contains ID {spec.task_id}. "
            "Update it manually or use a different task ID."
        )

    # Insert after the table divider row and any existing rows.
    insert_at = table_header_idx + 1
    while insert_at < len(lines) and lines[insert_at].lstrip().startswith("|"):
        insert_at += 1

    lines.insert(insert_at, row)
    tracker_path.write_text("".join(lines), encoding="utf-8")
    return True


def _next_sequential_id(tasks_dir: Path, tracker_path: Path, *, prefix: str) -> str:
    return _next_sequential_id_from_used(
        _used_ids_for_prefix(tasks_dir, tracker_path, prefix=prefix),
        prefix=prefix,
    )


def _next_workflow_id(
    root: Path, tasks_dir: Path, tracker_path: Path, *, prefix: str, kind: str
) -> str:
    config = _load_workflow_config(root)
    return _next_task_id_from_used(
        _used_ids_for_prefix(tasks_dir, tracker_path, prefix=prefix),
        prefix=prefix,
        config=config,
        kind=kind,
    )


def _resolve_epic_id(root: Path, tasks_dir: Path, tracker_path: Path, *, title: str) -> str:
    suffix = slug_titlecase_dashes(title)
    match_re = re.compile(
        rf"^{re.escape(EPIC_ID_PREFIX)}-([A-Za-z0-9]+)-{re.escape(suffix)}$"
    )

    matches: list[str] = []
    for path in tasks_dir.iterdir():
        if not path.is_dir():
            continue
        match = match_re.match(path.name)
        if match:
            id_suffix = match.group(1).upper()
            if id_suffix.isdigit():
                id_suffix = f"{int(id_suffix):0{ID_PADDING}d}"
            matches.append(f"{EPIC_ID_PREFIX}-{id_suffix}")

    if len(matches) > 1:
        raise SystemExit(
            "Multiple existing epic folders match this title. "
            "Use --folder-suffix to disambiguate title-to-folder mapping."
        )
    if len(matches) == 1:
        return matches[0]

    return _next_workflow_id(
        root,
        tasks_dir,
        tracker_path,
        prefix=EPIC_ID_PREFIX,
        kind="epics",
    )


def _doctor_check_source_mirrors(root: Path, issues: list[DoctorIssue]) -> None:
    def matches_packaged(local_path: Path, packaged_path: Path) -> bool:
        local_content = local_path.read_text(encoding="utf-8")
        packaged_content = packaged_path.read_text(encoding="utf-8")
        return local_content in {
            packaged_content,
            _with_generated_marker(local_path, packaged_content),
        }

    dev_prompts_dir = root / ".github" / "prompts"
    packaged_prompts_dir = root / "src" / "project_workflow" / "prompts"
    if dev_prompts_dir.exists() and packaged_prompts_dir.exists():
        for prompt_file in PROMPT_FILES:
            dev_path = dev_prompts_dir / prompt_file
            packaged_path = packaged_prompts_dir / prompt_file
            if not dev_path.exists():
                _add_issue(issues, "error", dev_path, "Development prompt is missing.")
                continue
            if not packaged_path.exists():
                _add_issue(issues, "error", packaged_path, "Packaged prompt is missing.")
                continue
            if not matches_packaged(dev_path, packaged_path):
                _add_issue(
                    issues,
                    "error",
                    dev_path,
                    f"Prompt differs from packaged mirror: {packaged_path}",
                )

    local_cli_dir = root / ".project-workflow" / "cli"
    packaged_template_dir = root / "src" / "project_workflow" / "templates"
    mirror_pairs = (
        (local_cli_dir / "workflow.py", packaged_template_dir / "workflow.py"),
        (local_cli_dir / "workflow", packaged_template_dir / "workflow"),
    )
    for local_path, packaged_path in mirror_pairs:
        if not local_path.exists() or not packaged_path.exists():
            continue
        if not matches_packaged(local_path, packaged_path):
            _add_issue(
                issues,
                "error",
                local_path,
                f"Local workflow CLI differs from packaged template: {packaged_path}",
            )


def _doctor_check_pending_generated_updates(root: Path, issues: list[DoctorIssue]) -> None:
    checked_roots = (
        root / ".project-workflow" / "cli",
        root / ".github" / "prompts",
        root / ".claude" / "agents",
        root / ".agents" / "skills",
        root / ".cursor" / "agents",
        root / ".cursor" / "rules",
    )
    for checked_root in checked_roots:
        if not checked_root.exists():
            continue
        for path in sorted(checked_root.rglob("*")):
            if ".new" not in path.name:
                continue
            _add_issue(
                issues,
                "warning",
                path,
                "Generated project-workflow update is pending because init preserved an unmarked existing file.",
            )


def _doctor_check_namespace_config(root: Path, issues: list[DoctorIssue]) -> WorkflowConfig | None:
    config_path = _workflow_config_path(root)
    try:
        return _load_workflow_config(root)
    except SystemExit as exc:
        _add_issue(issues, "error", config_path, str(exc))
        return None


def _doctor_check_row_namespace(
    row_id: str,
    *,
    config: WorkflowConfig | None,
    path: Path,
    issues: list[DoctorIssue],
) -> None:
    if config is None:
        return
    prefix = _task_prefix_from_id(row_id)
    if prefix is None or prefix in {EPIC_ID_PREFIX, FIX_ID_PREFIX}:
        return
    if prefix not in config.task_id_prefixes:
        _add_issue(
            issues,
            "warning",
            path,
            f"{row_id} uses unconfigured task ID prefix '{prefix}'. "
            f"Configured prefixes: {', '.join(config.task_id_prefixes)}.",
        )


def _doctor_check_row_id_format(
    row_id: str,
    *,
    config: WorkflowConfig | None,
    path: Path,
    issues: list[DoctorIssue],
    task_only: bool = False,
) -> None:
    if config is None:
        return
    if not task_only and row_id.startswith(f"{EPIC_ID_PREFIX}-"):
        if not _valid_epic_id(row_id, config=config):
            _add_issue(issues, "error", path, f"{row_id} has invalid epic ID format.")
        return
    if not task_only and row_id.startswith(f"{FIX_ID_PREFIX}-"):
        if not _valid_fix_id(row_id, config=config):
            _add_issue(issues, "error", path, f"{row_id} has invalid Fix ID format.")
        return

    prefix = _task_prefix_from_id(row_id)
    if prefix is None:
        _add_issue(issues, "error", path, f"{row_id} has invalid task ID format.")
        return
    if prefix in config.task_id_prefixes and not _valid_task_id(row_id, config=config):
        _add_issue(issues, "error", path, f"{row_id} has invalid task ID format.")


def _doctor_check_duplicate_tracker_ids(root: Path, issues: list[DoctorIssue]) -> None:
    workflow_dir = root / ".project-workflow"
    tracker_paths = [workflow_dir / "TRACKER.md"]
    tasks_dir = workflow_dir / "tasks"
    if tasks_dir.exists():
        tracker_paths.extend(sorted(tasks_dir.glob(f"{EPIC_ID_PREFIX}-*/TRACKER.md")))

    seen: dict[str, Path] = {}
    reported: set[str] = set()
    for tracker_path in tracker_paths:
        if not tracker_path.exists():
            continue
        try:
            if tracker_path.name == "TRACKER.md" and tracker_path.parent == workflow_dir:
                _lines, _header_idx, rows = _global_tracker_rows(tracker_path)
            else:
                _lines, _header_idx, rows = _epic_tracker_rows(tracker_path)
        except SystemExit:
            continue
        for row in rows:
            row_id = row.get("ID", "").strip()
            if not row_id:
                continue
            if row_id in seen and row_id not in reported:
                _add_issue(
                    issues,
                    "error",
                    tracker_path,
                    f"Duplicate workflow ID '{row_id}' also appears in {seen[row_id]}.",
                )
                reported.add(row_id)
            else:
                seen[row_id] = tracker_path


def _doctor_check_task_doc(
    *,
    root: Path,
    docs_rel: str,
    status: str,
    row_id: str,
    issues: list[DoctorIssue],
    parent_requirements_path: Path | None = None,
) -> None:
    if not docs_rel:
        _add_issue(issues, "warning", ".project-workflow/TRACKER.md", f"{row_id} has no docs path.")
        return

    docs_path = root / ".project-workflow" / docs_rel
    if not docs_path.exists():
        _add_issue(issues, "error", docs_path, f"{row_id} docs path does not exist.")
        return

    try:
        docs_text = docs_path.read_text(encoding="utf-8")
    except OSError as exc:
        _add_issue(issues, "error", docs_path, f"Could not read docs for {row_id}: {exc}")
        return

    has_completion_evidence = _has_qa_review_evidence(
        docs_text
    ) or _has_epic_acceptance_audit_evidence(docs_path, row_id)
    if status == "Complete" and not has_completion_evidence:
        _add_issue(
            issues,
            "warning",
            docs_path,
            f"{row_id} is Complete but lacks non-placeholder QA/code-review evidence.",
        )

    requirements_path = docs_path.parent / "REQUIREMENTS.md"
    requirements_text: str | None = None
    if requirements_path.exists():
        requirements_text = requirements_path.read_text(encoding="utf-8")
    if requirements_text is not None and status in ("Review", "Complete"):
        if _legacy_adoption_evidence_untrusted(requirements_text):
            _add_issue(
                issues,
                "warning",
                requirements_path,
                f"{row_id} adopted legacy evidence is untrusted until refreshed.",
            )
    if requirements_path.exists() and docs_path.name == "IMPLEMENTATION.md" and status in (
        "Review",
        "Complete",
    ):
        parent_ac_ids: set[str] | None = None
        if parent_requirements_path is not None:
            parent_section = _markdown_section(docs_text, "Parent AC Coverage")
            parent_ac_ids = _extract_ac_ids(parent_section)
        for evidence_issue in _structured_evidence_issues(
            requirements_path=requirements_path,
            implementation_path=docs_path,
            parent_ac_ids=parent_ac_ids,
        ):
            _add_issue(
                issues,
                "error",
                docs_path,
                f"{row_id} {evidence_issue}",
            )
    if parent_requirements_path is not None and status in (
        "Approved",
        "In Progress",
        "Testing",
        "Review",
        "Complete",
    ):
        for approval_issue in _requirements_approval_issues_for_path(
            parent_requirements_path,
            require_decomposition=True,
        ):
            _add_issue(
                issues,
                "warning",
                parent_requirements_path,
                f"{row_id} parent approval envelope: {approval_issue}",
            )
    elif requirements_text is not None and not _is_discovery_work(requirements_text, docs_text):
        approval_required = False
        require_decomposition = False
        require_implementation = False
        if row_id.startswith(f"{EPIC_ID_PREFIX}-"):
            approval_required = status in ("Ready", "In Progress", "Closeout", "Complete")
            require_decomposition = approval_required
        else:
            approval_required = _status_requires_task_readiness(status)
            require_implementation = approval_required
        if approval_required:
            for approval_issue in _approval_envelope_issues(
                requirements_text,
                require_decomposition=require_decomposition,
                require_implementation=require_implementation,
            ):
                _add_issue(
                    issues,
                    "warning",
                    requirements_path,
                    f"{row_id} approval envelope: {approval_issue}",
                )
    if status not in ("To Do", "N/A") and requirements_text is not None:
        if "____" in requirements_text:
            _add_issue(
                issues,
                "warning",
                requirements_path,
                f"{row_id} has active status '{status}' but requirements still contain placeholders.",
            )
    if (
        docs_path.name == "IMPLEMENTATION.md"
        and status != "Complete"
        and _status_requires_task_readiness(status)
    ):
        if requirements_text is not None:
            for readiness_issue in _task_readiness_issues(
                requirements_text=requirements_text,
                implementation_text=docs_text,
            ):
                _add_issue(
                    issues,
                    "warning",
                    docs_path,
                    f"{row_id} readiness gate: {readiness_issue}",
                )
    if docs_path.name == "REQUIREMENTS.md" and row_id.startswith(f"{EPIC_ID_PREFIX}-"):
        if status not in ("To Do", "N/A"):
            for readiness_issue in _epic_requirements_readiness_issues(docs_text):
                _add_issue(
                    issues,
                    "warning",
                    docs_path,
                    f"{row_id} epic readiness gate: {readiness_issue}",
                )

    _doctor_check_implementation_ac_mapping(
        docs_path=docs_path,
        docs_text=docs_text,
        status=status,
        row_id=row_id,
        issues=issues,
    )


def _doctor_check_fix_doc(
    *, root: Path, docs_rel: str, status: str, row_id: str, issues: list[DoctorIssue]
) -> None:
    fix_path = root / ".project-workflow" / docs_rel
    if fix_path.name != "FIX.md" or not fix_path.exists():
        _add_issue(issues, "error", fix_path, f"{row_id} must point to an existing FIX.md.")
        return
    try:
        fix_text = fix_path.read_text(encoding="utf-8")
    except OSError as exc:
        _add_issue(issues, "error", fix_path, f"Could not read {row_id}: {exc}")
        return
    summary = _fix_values(fix_text, "Summary")
    for heading in (
        "Summary",
        "Report",
        "Routing",
        "Classification",
        "Related Work",
        "Risk",
        "Fix Plan",
        "Verification",
        "Outcome",
    ):
        if not _markdown_section(fix_text, heading):
            _add_issue(issues, "error", fix_path, f"{row_id} is missing `## {heading}`.")
    if summary.get("fix") != row_id:
        _add_issue(issues, "error", fix_path, f"Summary Fix ID does not match {row_id}.")
    if summary.get("status") != status:
        _add_issue(
            issues,
            "error",
            fix_path,
            f"Summary status '{summary.get('status', '')}' does not match tracker '{status}'.",
        )
    classification = _fix_values(fix_text, "Classification")
    classification_type = classification.get("type")
    if (
        not _fix_value_missing(classification_type)
        and classification_type not in FIX_CLASSIFICATIONS
    ):
        _add_issue(
            issues,
            "error",
            fix_path,
            f"{row_id} has invalid classification Type '{classification_type}'.",
        )
    mode = classification.get("mode")
    if not _fix_value_missing(mode) and mode not in FIX_MODES:
        _add_issue(issues, "error", fix_path, f"{row_id} has invalid Mode '{mode}'.")
    severity = classification.get("severity")
    if not _fix_value_missing(severity) and severity not in FIX_SEVERITIES:
        _add_issue(issues, "error", fix_path, f"{row_id} has invalid Severity '{severity}'.")
    if status in {"Ready", "In Progress", "Testing", "Review", "Complete"}:
        try:
            triage_issues = _fix_triage_issues(
                root,
                fix_text,
                require_active_disposition=status != "Complete",
            )
        except SystemExit as exc:
            triage_issues = [str(exc)]
        for triage_issue in triage_issues:
            _add_issue(issues, "error", fix_path, f"{row_id} triage: {triage_issue}.")
    if status == "Complete":
        for closeout_issue in _fix_closeout_issues(fix_text):
            _add_issue(issues, "error", fix_path, f"{row_id} closeout: {closeout_issue}.")
    if status == "N/A":
        for closeout_issue in _fix_non_delivery_closeout_issues(fix_text):
            _add_issue(issues, "error", fix_path, f"{row_id} closeout: {closeout_issue}.")
    related = _fix_values(fix_text, "Related Work")
    refs = _extract_workflow_ref_ids(" ".join(related.values()))
    if refs:
        tracker_path = root / ".project-workflow" / "TRACKER.md"
        try:
            _lines, _header_idx, tracker_rows = _global_tracker_rows(tracker_path)
            known_ids = {row["ID"] for row in tracker_rows}
        except SystemExit:
            known_ids = set()
        for ref in sorted(refs - known_ids):
            _add_issue(
                issues,
                "warning",
                fix_path,
                f"{row_id} related work reference '{ref}' is not in the local global tracker.",
            )


def _doctor_check_global_tracker(
    root: Path, issues: list[DoctorIssue], *, config: WorkflowConfig | None
) -> None:
    workflow_dir = root / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    if not tracker_path.exists():
        _add_issue(issues, "error", tracker_path, "Global tracker is missing.")
        return

    rows = _parse_markdown_table(
        tracker_path,
        expected_columns=GLOBAL_TRACKER_COLUMNS,
        issues=issues,
        label="Global tracker",
    )
    for row in rows:
        row_id = row["ID"]
        _doctor_check_row_id_format(row_id, config=config, path=tracker_path, issues=issues)
        _doctor_check_row_namespace(row_id, config=config, path=tracker_path, issues=issues)
        status = row["Status"]
        if status not in TRACKER_STATUSES:
            _add_issue(
                issues,
                "error",
                tracker_path,
                f"{row_id} has invalid status '{status}'.",
            )
        docs_rel = _clean_markdown_cell_path(row["Docs"])
        if row_id.startswith(f"{FIX_ID_PREFIX}-"):
            _doctor_check_fix_doc(
                root=root,
                docs_rel=docs_rel,
                status=status,
                row_id=row_id,
                issues=issues,
            )
        else:
            _doctor_check_task_doc(
                root=root,
                docs_rel=docs_rel,
                status=status,
                row_id=row_id,
                issues=issues,
            )

def _doctor_check_backlog(
    root: Path, issues: list[DoctorIssue], *, config: WorkflowConfig | None
) -> None:
    backlog_path = _backlog_path(root)
    if not backlog_path.exists():
        return
    if config is None:
        return
    issues.extend(_backlog_validation_issues(root, backlog_path, config=config))


def _doctor_check_epic_trackers(
    root: Path, issues: list[DoctorIssue], *, config: WorkflowConfig | None
) -> None:
    tasks_dir = root / ".project-workflow" / "tasks"
    if not tasks_dir.exists():
        return

    for epic_tracker_path in sorted(tasks_dir.glob(f"{EPIC_ID_PREFIX}-*/TRACKER.md")):
        try:
            _lines, _header_idx, rows = _epic_tracker_rows(epic_tracker_path)
        except SystemExit as exc:
            _add_issue(issues, "error", epic_tracker_path, str(exc))
            continue
        parent_requirements_path = epic_tracker_path.parent / "REQUIREMENTS.md"
        parent_approval_issues = _requirements_approval_issues_for_path(
            parent_requirements_path,
            require_decomposition=True,
        )
        authority_severity = "warning" if parent_approval_issues else "error"
        for contract_issue in _epic_contract_issues_for_path(epic_tracker_path.parent):
            _add_issue(
                issues,
                authority_severity,
                _epic_contract_path(epic_tracker_path.parent),
                f"{epic_tracker_path.parent.name} epic contract: {contract_issue}",
            )
        for row in rows:
            row_id = row["ID"]
            _doctor_check_row_id_format(
                row_id,
                config=config,
                path=epic_tracker_path,
                issues=issues,
                task_only=True,
            )
            _doctor_check_row_namespace(
                row_id, config=config, path=epic_tracker_path, issues=issues
            )
            status = row["Status"]
            if status not in EPIC_TRACKER_STATUSES:
                _add_issue(
                    issues,
                    "error",
                    epic_tracker_path,
                    f"{row_id} has invalid epic status '{status}'.",
                )
            if status in EPIC_CHILD_GATED_STATUSES:
                for authority_issue in _decomposition_plan_authority_issues(
                    epic_dir=epic_tracker_path.parent,
                    row=row,
                ):
                    _add_issue(
                        issues,
                        authority_severity,
                        _decomposition_plan_path(epic_tracker_path.parent),
                        f"{row_id} decomposition authority: {authority_issue}",
                    )
            docs_rel = _clean_markdown_cell_path(row["Docs"])
            if not docs_rel and status in (
                "Approved",
                "In Progress",
                "Testing",
                "Review",
                "Complete",
            ):
                for approval_issue in parent_approval_issues:
                    _add_issue(
                        issues,
                        "warning",
                        parent_requirements_path,
                        f"{row_id} parent approval envelope: {approval_issue}",
                    )
            if docs_rel:
                _doctor_check_task_doc(
                    root=root,
                    docs_rel=docs_rel,
                    status=status,
                    row_id=row_id,
                    issues=issues,
                    parent_requirements_path=epic_tracker_path.parent / "REQUIREMENTS.md",
                )


def run_doctor(root: Path) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    config = _doctor_check_namespace_config(root, issues)
    _doctor_check_source_mirrors(root, issues)
    _doctor_check_pending_generated_updates(root, issues)
    _doctor_check_backlog(root, issues, config=config)
    _doctor_check_duplicate_tracker_ids(root, issues)
    _doctor_check_global_tracker(root, issues, config=config)
    _doctor_check_epic_trackers(root, issues, config=config)
    return issues


def _doctor_issue_is_blocking(issue: DoctorIssue, *, strict: bool) -> bool:
    return issue.severity == "error" or (strict and issue.severity == "warning")


def _doctor_issue_is_legacy(issue: DoctorIssue) -> bool:
    if issue.severity != "warning":
        return False
    path_text = str(issue.path)
    if ".project-workflow/tasks/APP-" in path_text:
        return True
    if "uses unconfigured task ID prefix 'APP'" in issue.message:
        return True
    match = re.search(r"\.project-workflow/tasks/EPIC-(\d+)-", path_text)
    return bool(match and int(match.group(1)) < 3)


def _doctor_issue_path_for_fingerprint(issue: DoctorIssue, root: Path) -> str:
    issue_path = Path(issue.path)
    if issue_path.is_absolute():
        try:
            return issue_path.relative_to(root).as_posix()
        except ValueError:
            return issue_path.as_posix()
    return str(issue.path).replace("\\", "/")


def _doctor_issue_fingerprint(issue: DoctorIssue, root: Path) -> str:
    payload = "\n".join(
        (
            issue.severity,
            _doctor_issue_path_for_fingerprint(issue, root),
            issue.message,
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _accepted_doctor_warning_fingerprints(root: Path) -> dict[str, str]:
    try:
        return _load_workflow_config(root).accepted_doctor_warnings
    except SystemExit:
        return {}


def _doctor_issue_is_accepted(
    issue: DoctorIssue, *, root: Path, accepted_fingerprints: dict[str, str]
) -> bool:
    return _doctor_issue_fingerprint(issue, root) in accepted_fingerprints


def _format_doctor_issue(
    issue: DoctorIssue,
    *,
    root: Path,
    strict: bool,
    accepted_fingerprints: dict[str, str],
    accepted: bool = False,
) -> str:
    if accepted:
        severity = "accepted"
    elif _doctor_issue_is_legacy(issue):
        severity = "error" if strict and issue.severity == "warning" else "legacy warning"
    else:
        severity = "error" if strict and issue.severity == "warning" else issue.severity
    fingerprint = _doctor_issue_fingerprint(issue, root)
    reason = accepted_fingerprints.get(fingerprint, "")
    reason_text = f" (accepted: {reason})" if accepted and reason else ""
    return (
        f"{severity.upper()}: {issue.path}: {issue.message} "
        f"[fingerprint: {fingerprint}]{reason_text}"
    )


def cmd_doctor(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve() if args.root else Path.cwd()
    issues = run_doctor(root)
    accepted_fingerprints = _accepted_doctor_warning_fingerprints(root)
    accepted_issues = [
        issue
        for issue in issues
        if _doctor_issue_is_accepted(
            issue,
            root=root,
            accepted_fingerprints=accepted_fingerprints,
        )
    ]
    visible_issues = [
        issue
        for issue in issues
        if not _doctor_issue_is_accepted(
            issue,
            root=root,
            accepted_fingerprints=accepted_fingerprints,
        )
    ]
    blocking = [
        issue for issue in visible_issues if _doctor_issue_is_blocking(issue, strict=args.strict)
    ]
    current_issues = [issue for issue in visible_issues if not _doctor_issue_is_legacy(issue)]
    legacy_issues = [issue for issue in visible_issues if _doctor_issue_is_legacy(issue)]

    if not visible_issues and not (args.show_accepted and accepted_issues):
        print(f"project doctor: no issues found in {root}")
        if accepted_issues:
            print(f"project doctor: {len(accepted_issues)} accepted warning(s) hidden.")
        return

    print(f"project doctor: checked {root}")
    for issue in current_issues:
        print(
            _format_doctor_issue(
                issue,
                root=root,
                strict=args.strict,
                accepted_fingerprints=accepted_fingerprints,
            )
        )
    for issue in legacy_issues:
        print(
            _format_doctor_issue(
                issue,
                root=root,
                strict=args.strict,
                accepted_fingerprints=accepted_fingerprints,
            )
        )
    if legacy_issues:
        print(f"project doctor: {len(legacy_issues)} legacy warning(s) shown separately.")
    if accepted_issues:
        if args.show_accepted:
            print(f"project doctor: {len(accepted_issues)} accepted warning(s):")
            for issue in accepted_issues:
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
            print(f"project doctor: {len(accepted_issues)} accepted warning(s) hidden.")

    if blocking:
        print(f"project doctor: failed with {len(blocking)} blocking issue(s).")
        raise SystemExit(1)

    if visible_issues:
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
            _implementation_template(spec.task_id, spec.title),
            overwrite=True,
        )
        _write_file(
            task_dir / "REQUIREMENTS.md",
            _requirements_with_backlog_source(
                _requirements_template(spec.task_id, spec.title),
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
                _requirements_template(spec.task_id, spec.title),
                source_row,
            ),
            overwrite=True,
        )
        _write_file(epic_dir / "TRACKER.md", _epic_tracker_template(), overwrite=True)
        _write_file(epic_dir / "DEFERRALS.md", _epic_deferrals_template(), overwrite=True)
        _write_file(epic_dir / EPIC_AMENDMENTS_FILENAME, _epic_amendments_template(), overwrite=True)
        _write_file(epic_dir / "RETRO.md", _epic_retro_template(spec.task_id, spec.title), overwrite=True)
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
    selected_agent = args.agent
    selected_agent_label = AGENT_CHOICES[selected_agent]
    managed_block = _managed_project_workflow_block()

    print(f"Selected agent mode: {selected_agent_label} ({selected_agent})")

    # Create .project-workflow structure
    project_workflow_dir = cwd / ".project-workflow"
    tasks_dir = project_workflow_dir / "tasks"
    cli_dir = project_workflow_dir / "cli"
    tracker_path = project_workflow_dir / "TRACKER.md"
    backlog_path = project_workflow_dir / "BACKLOG.md"
    guidance_path = project_workflow_dir / "guidance.md"
    config_path = project_workflow_dir / WORKFLOW_CONFIG_FILENAME

    # Create directories
    tasks_dir.mkdir(parents=True, exist_ok=True)
    cli_dir.mkdir(parents=True, exist_ok=True)

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

    print(f"\n✅ Project workflow initialized in {cwd}")
    print(f"   Agent mode applied: {selected_agent_label}")
    print(f"\nNext steps:")
    print(f"  • Review: .project-workflow/TRACKER.md")
    print(f"  • Customize user guidance: .project-workflow/guidance.md")
    print(f"  • Review generated agent assets: {customize_path_hint}")
    print(f"  • Create tasks: ./.project-workflow/cli/workflow task init --help")
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
    fix_text = _fix_template(fix_id, args.title)
    if args.classification:
        fix_text = _replace_fix_field(
            fix_text, "Classification", "Type", args.classification
        )
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
        _fix_closeout_issues(fix_text)
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
    fix_path, source_row = _resolve_fix_doc(
        root=root, tracker_path=tracker_path, fix_id=fix_id
    )
    if source_row["Status"] in {"Complete", "N/A"}:
        raise SystemExit(f"{fix_id} is already terminal and cannot be promoted.")
    title = args.title or source_row["Title"]
    if args.to == "task":
        prefix = _resolve_task_id_prefix(root, None)
        promoted_id = _next_workflow_id(
            root, tasks_dir, tracker_path, prefix=prefix, kind="tasks"
        )
        spec = TaskSpec(promoted_id, title, slug_titlecase_dashes(title))
        promoted_dir = tasks_dir / spec.task_folder_name
        promoted_dir.mkdir(parents=True, exist_ok=False)
        _write_file(
            promoted_dir / "IMPLEMENTATION.md",
            _implementation_template(promoted_id, title),
            overwrite=True,
        )
        _write_file(
            promoted_dir / "REQUIREMENTS.md",
            _requirements_with_fix_source(
                _requirements_template(promoted_id, title), fix_id, args.reason
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
                _requirements_template(promoted_id, title), fix_id, args.reason
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
    branch_name: Optional[str] = None

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
        _write_file(impl_path, _implementation_template(spec.task_id, spec.title), overwrite=True)
    if args.overwrite or not reqs_path.exists():
        _write_file(reqs_path, _requirements_template(spec.task_id, spec.title), overwrite=True)

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
        _write_file(reqs_path, _requirements_template(spec.task_id, spec.title), overwrite=True)
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
            )
            for row in proposed_child_rows[: args.limit]
        ]
    else:
        candidates = [
            (title, ac_id, "Generated from REQUIREMENTS.md")
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
    for title, ac_id, source in candidates:
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
        print(
            "WARNING: Unmapped parent ACs after decomposition: "
            + ", ".join(unmapped_ac_ids)
        )
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
    target: Optional[dict[str, str]] = None
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
    branch_name: Optional[str] = None

    if args.create_branch:
        _ensure_clean_git(cwd)
        epic_branch = args.epic_branch
        branch_name = f"{args.branch_prefix}{child_spec.task_id}-{slug_kebab_lower(child_spec.title)}"

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project",
        description=(
            "Project workflow: Spec-driven development for GitHub Copilot, "
            "Claude Code, OpenAI Codex, and Cursor."
        ),
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
        doctor_parser.set_defaults(func=cmd_doctor)

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

    fix_status_parser = fix_sub.add_parser(
        "status", help="Safely update a Fix lifecycle status"
    )
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
    fix_close_parser.add_argument(
        "--closed-date", help="ISO close date (default: today)"
    )
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
    task_init_parser.add_argument("--title", required=True, help="Human title (e.g. Super Admin Access)")
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
    epic_ready_child_parser.add_argument(
        "--epic-id", required=True, help="Epic ID (e.g. EPIC-001)"
    )
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
    epic_lifecycle_parser.add_argument(
        "--epic-id", required=True, help="Epic ID (e.g. EPIC-001)"
    )
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
    epic_decompose_parser.add_argument(
        "--epic-id", required=True, help="Epic ID (e.g. EPIC-001)"
    )
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
