#!/usr/bin/env python3
"""project-workflow CLI: Bootstrap and task scaffolding for spec-driven development."""

from __future__ import annotations

import argparse
import re
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
    "Constitution.prompt.md",
    "Clarify.prompt.md",
    "Delegate.prompt.md",
    "Epic.prompt.md",
    "Implement.prompt.md",
    "Planner.prompt.md",
    "QAReview.prompt.md",
    "Requirements.prompt.md",
    "Retro.prompt.md",
    "Task.prompt.md",
]

CODEX_SKILL_NAMES = [
    "project-constitution",
    "project-task",
    "project-epic",
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
ID_PADDING = 3
GLOBAL_TRACKER_COLUMNS = ("ID", "Title", "Status", "Docs")
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
    "Plan Confirmed",
    "In Progress",
    "Blocked",
    "Testing",
    "Review",
    "Complete",
    "N/A",
)
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
    "Analysing": {"Plan Confirmed", "Blocked"},
    "Plan Confirmed": {"In Progress", "Blocked"},
    "In Progress": {"Testing", "Blocked"},
    "Testing": {"Review", "In Progress", "Blocked"},
    "Review": {"Complete", "In Progress", "Blocked"},
    "Blocked": {"In Progress", "Analysing", "Plan Confirmed", "Testing", "Review"},
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


def _managed_project_workflow_block() -> str:
    return (
        f"{MANAGED_BLOCK_START}\n"
        "## Project Workflow\n\n"
        "This repository uses project-workflow. Keep workflow state in "
        "`.project-workflow/TRACKER.md` and `.project-workflow/tasks/`.\n\n"
        "- Read repo-specific workflow guidance from `.project-workflow/guidance.md`.\n"
        f"- To install or refresh project-workflow itself, run `{CANONICAL_INIT_COMMAND}` "
        "from the repository root; add `--agent codex`, `--agent cursor`, "
        "`--agent claude-code`, or `--agent github-copilot` when selecting a mode. "
        "Do not use bare `project init` unless the package is intentionally installed "
        "and known to be current.\n"
        "- Use `./.project-workflow/cli/workflow` for supported task and validation commands.\n"
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


def _tracker_template() -> str:
    return (
        "# Stories\n\n"
        "| ID | Title | Status | Docs |\n"
        "|---|---|---|---|\n"
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
            evidence_present = _parent_ac_evidence_present(docs_text, ac_id)
            qa_passed = _qa_passed(docs_text)
            if evidence_present:
                evidence_bits.append(f"{row_id}: parent AC evidence recorded")
            elif not has_approved_deferral:
                verdict = "Gap"
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
    task_id: str, title: str, parent_ac_coverage: str
) -> str:
    parent_ac_value = parent_ac_coverage or "____"
    return (
        f"## User Story\n\n"
        f"As a ____, I want ____, so that ____.\n\n"
        f"## Parent AC Coverage\n\n"
        f"- {parent_ac_value}\n\n"
        f"## Acceptance Criteria\n\n"
        f"- [ ] AC1: Covers parent AC(s) {parent_ac_value}: ____\n\n"
        f"## Validation\n\n"
        f"- AC1 / parent AC(s) {parent_ac_value}: ____\n\n"
        f"## Task List\n\n"
        f"| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        f"| --: | ----- | ----------- | ------------------- | ----------------- | ------ |\n"
        f"| 1 | ____ | ____ | AC1 / parent AC(s) {parent_ac_value}: ____ | ____ | To Do |\n\n"
        f"## Parent AC Evidence\n\n"
        f"- {parent_ac_value}: Pending implementation evidence.\n\n"
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


def _epic_child_requirements_template(
    task_id: str, title: str, parent_ac_coverage: str
) -> str:
    parent_ac_value = parent_ac_coverage or "____"
    return (
        f"# Requirements\n\n"
        f"## Summary\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n"
        f"- Parent AC Coverage: {parent_ac_value}\n"
        f"- Last updated: {date.today().isoformat()}\n\n"
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


def _normalize_task_status_id(row_id: str) -> str:
    match = re.match(rf"^({re.escape(TASK_ID_PREFIX)}-\d+)(?:-.+)?$", row_id)
    if not match:
        raise SystemExit(f"Task status only supports {TASK_ID_PREFIX}-### IDs; got '{row_id}'.")
    return match.group(1)


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
    return new_status in {"Plan Confirmed", "In Progress", "Testing", "Review", "Complete"}


def _status_requires_epic_child_readiness(new_status: str) -> bool:
    return new_status in {"Testing", "Review", "Complete"}


def _resolve_global_task_docs(
    *, root: Path, tracker_path: Path, task_id: str
) -> tuple[Path, Path, dict[str, str]]:
    normalized_task_id = _normalize_task_status_id(task_id)
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


def _update_global_tracker_row_status(
    *,
    root: Path,
    tracker_path: Path,
    row_id: str,
    new_status: str,
    force: bool,
    reason: str | None,
) -> tuple[str, str]:
    normalized_row_id = _normalize_task_status_id(row_id)

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
        if new_status == "Complete":
            if current_status != "Review":
                raise SystemExit(
                    f"{row_id} can only move to Complete from Review; "
                    f"current status is '{current_status}'."
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

        if (
            _status_requires_task_readiness(new_status)
            and not force
            and normalized_row_id.startswith(f"{TASK_ID_PREFIX}-")
        ):
            requirements_path = docs_path.parent / "REQUIREMENTS.md"
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


def _next_task_id_from_used(used_ids: set[str]) -> str:
    max_value = 0
    row_re = re.compile(rf"^{re.escape(TASK_ID_PREFIX)}-(\d+)$")
    for used_id in used_ids:
        match = row_re.match(used_id)
        if match:
            max_value = max(max_value, int(match.group(1)))
    return f"{TASK_ID_PREFIX}-{max_value + 1:0{ID_PADDING}d}"


def _used_ids_for_prefix(tasks_dir: Path, tracker_path: Path, *, prefix: str) -> set[str]:
    used_ids: set[str] = set()
    id_re = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
    dir_re = re.compile(rf"^{re.escape(prefix)}-(\d+)-")
    row_re = re.compile(rf"\|\s*({re.escape(prefix)}-\d+)\s*\|")

    if tasks_dir.exists():
        for path in tasks_dir.rglob("*"):
            if not path.is_dir():
                continue
            match = dir_re.match(path.name)
            if match:
                used_ids.add(f"{prefix}-{int(match.group(1)):0{ID_PADDING}d}")

    tracker_paths = [tracker_path]
    if tasks_dir.exists():
        tracker_paths.extend(sorted(tasks_dir.rglob("TRACKER.md")))

    for candidate_tracker in tracker_paths:
        if not candidate_tracker.exists():
            continue
        try:
            tracker_text = candidate_tracker.read_text(encoding="utf-8")
        except OSError:
            continue
        for match in row_re.finditer(tracker_text):
            candidate = match.group(1)
            if id_re.match(candidate):
                used_ids.add(candidate)

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
    max_value = 0
    for used_id in _used_ids_for_prefix(tasks_dir, tracker_path, prefix=prefix):
        _, _, numeric = used_id.partition("-")
        max_value = max(max_value, int(numeric))

    return f"{prefix}-{max_value + 1:0{ID_PADDING}d}"


def _resolve_epic_id(tasks_dir: Path, tracker_path: Path, *, title: str) -> str:
    suffix = slug_titlecase_dashes(title)
    match_re = re.compile(rf"^{re.escape(EPIC_ID_PREFIX)}-(\d+)-{re.escape(suffix)}$")

    matches: list[str] = []
    for path in tasks_dir.iterdir():
        if not path.is_dir():
            continue
        match = match_re.match(path.name)
        if match:
            matches.append(f"{EPIC_ID_PREFIX}-{int(match.group(1)):0{ID_PADDING}d}")

    if len(matches) > 1:
        raise SystemExit(
            "Multiple existing epic folders match this title. "
            "Use --folder-suffix to disambiguate title-to-folder mapping."
        )
    if len(matches) == 1:
        return matches[0]

    return _next_sequential_id(tasks_dir, tracker_path, prefix=EPIC_ID_PREFIX)


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


def _doctor_check_task_doc(
    *,
    root: Path,
    docs_rel: str,
    status: str,
    row_id: str,
    issues: list[DoctorIssue],
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


def _doctor_check_global_tracker(root: Path, issues: list[DoctorIssue]) -> None:
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
        status = row["Status"]
        if status not in TRACKER_STATUSES:
            _add_issue(
                issues,
                "error",
                tracker_path,
                f"{row_id} has invalid status '{status}'.",
            )
        docs_rel = _clean_markdown_cell_path(row["Docs"])
        _doctor_check_task_doc(
            root=root,
            docs_rel=docs_rel,
            status=status,
            row_id=row_id,
            issues=issues,
        )


def _doctor_check_epic_trackers(root: Path, issues: list[DoctorIssue]) -> None:
    tasks_dir = root / ".project-workflow" / "tasks"
    if not tasks_dir.exists():
        return

    for epic_tracker_path in sorted(tasks_dir.glob(f"{EPIC_ID_PREFIX}-*/TRACKER.md")):
        try:
            _lines, _header_idx, rows = _epic_tracker_rows(epic_tracker_path)
        except SystemExit as exc:
            _add_issue(issues, "error", epic_tracker_path, str(exc))
            continue
        for row in rows:
            row_id = row["ID"]
            status = row["Status"]
            if status not in EPIC_TRACKER_STATUSES:
                _add_issue(
                    issues,
                    "error",
                    epic_tracker_path,
                    f"{row_id} has invalid epic status '{status}'.",
                )
            docs_rel = _clean_markdown_cell_path(row["Docs"])
            if docs_rel:
                _doctor_check_task_doc(
                    root=root,
                    docs_rel=docs_rel,
                    status=status,
                    row_id=row_id,
                    issues=issues,
                )


def run_doctor(root: Path) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    _doctor_check_source_mirrors(root, issues)
    _doctor_check_pending_generated_updates(root, issues)
    _doctor_check_global_tracker(root, issues)
    _doctor_check_epic_trackers(root, issues)
    return issues


def _doctor_issue_is_blocking(issue: DoctorIssue, *, strict: bool) -> bool:
    return issue.severity == "error" or (strict and issue.severity == "warning")


def cmd_doctor(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve() if args.root else Path.cwd()
    issues = run_doctor(root)
    blocking = [issue for issue in issues if _doctor_issue_is_blocking(issue, strict=args.strict)]

    if not issues:
        print(f"project doctor: no issues found in {root}")
        return

    print(f"project doctor: checked {root}")
    for issue in issues:
        severity = "error" if args.strict and issue.severity == "warning" else issue.severity
        print(f"{severity.upper()}: {issue.path}: {issue.message}")

    if blocking:
        print(f"project doctor: failed with {len(blocking)} blocking issue(s).")
        raise SystemExit(1)

    print("project doctor: passed with warnings")


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
    guidance_path = project_workflow_dir / "guidance.md"

    # Create directories
    tasks_dir.mkdir(parents=True, exist_ok=True)
    cli_dir.mkdir(parents=True, exist_ok=True)

    # Create initial TRACKER.md if missing
    if not tracker_path.exists():
        tracker_path.write_text(_tracker_template(), encoding="utf-8")
        print(f"✓ Created: {tracker_path}")
    else:
        print(f"✓ Exists: {tracker_path}")

    print(f"✓ {_ensure_user_guidance_file(guidance_path)}")

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
    print("  • Validate workflow state: ./.project-workflow/cli/workflow doctor")


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

    task_id = _next_sequential_id(tasks_dir, tracker_path, prefix=TASK_ID_PREFIX)
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

    task_id = _normalize_task_status_id(args.id)
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

    task_id = _normalize_task_status_id(args.id)
    requirements_path, implementation_path, _row = _resolve_global_task_docs(
        root=cwd,
        tracker_path=tracker_path,
        task_id=task_id,
    )
    readiness_issues = _task_ready_issues_for_paths(
        requirements_path=requirements_path,
        implementation_path=implementation_path,
    )
    if readiness_issues:
        raise SystemExit(_format_readiness_block(task_id, readiness_issues))
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

    epic_id = _resolve_epic_id(tasks_dir, tracker_path, title=args.title)
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
    epic_tracker_path = epic_dir / "TRACKER.md"
    deferrals_path = epic_dir / "DEFERRALS.md"

    epic_dir.mkdir(parents=True, exist_ok=True)
    if args.overwrite or not reqs_path.exists():
        _write_file(reqs_path, _requirements_template(spec.task_id, spec.title), overwrite=True)
    if args.overwrite or not epic_tracker_path.exists():
        _write_file(epic_tracker_path, _epic_tracker_template(), overwrite=True)
    if args.overwrite or not deferrals_path.exists():
        _write_file(deferrals_path, _epic_deferrals_template(), overwrite=True)

    docs_rel = f"tasks/{spec.task_folder_name}/REQUIREMENTS.md"
    row_written = _update_tracker(
        tracker_path,
        spec=spec,
        status=args.status,
        docs_rel_path=docs_rel,
        on_duplicate="skip",
    )

    print(f"Created epic: {epic_dir}")
    if row_written:
        print(f"Updated tracker: {tracker_path}")
    else:
        print(f"Tracker already had row for ID {spec.task_id}; no duplicate added.")
    print(f"Assigned ID: {spec.task_id}")


def cmd_epic_approve(args: argparse.Namespace) -> None:
    """Approve a proposed epic child row by updating Status to Approved."""
    cwd = Path.cwd()
    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"

    epic_dir = _resolve_epic_dir(tasks_dir, args.epic_id)
    epic_tracker_path = epic_dir / "TRACKER.md"
    if not epic_tracker_path.exists():
        raise SystemExit(f"Missing epic tracker: {epic_tracker_path}")

    _update_epic_tracker_row_status(
        epic_tracker_path,
        row_id=args.id,
        expected_from="Proposed",
        new_status="Approved",
    )
    print(f"Approved epic row {args.id} in {epic_tracker_path}")


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
    readiness_issues = _epic_requirements_readiness_issues(requirements_text)
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

    requirements_path, implementation_path, row = _resolve_epic_child_docs(
        root=cwd,
        epic_tracker_path=epic_tracker_path,
        row_id=args.id,
    )
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


def cmd_epic_decompose(args: argparse.Namespace) -> None:
    """Generate Proposed child rows from epic REQUIREMENTS.md without scaffolding child folders."""
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
    if readiness_issues:
        raise SystemExit(_format_readiness_block(args.epic_id, readiness_issues))
    candidates = _decompose_epic_requirements_to_titles(requirements_text, limit=args.limit)
    if not candidates:
        raise SystemExit(
            "No decomposition candidates found in epic REQUIREMENTS.md. "
            "Add list items under '## Requirements (Outcome-Focused)' or "
            "'## Acceptance Criteria (Verifiable)' first."
        )

    occupied_ids = _used_ids_for_prefix(tasks_dir, tracker_path, prefix=TASK_ID_PREFIX)
    _lines, _header_idx, epic_rows = _epic_tracker_rows(epic_tracker_path)

    rows_to_add: list[dict[str, str]] = []
    for title, ac_id in candidates:
        next_id = _next_task_id_from_used(occupied_ids)
        occupied_ids.add(next_id)
        notes = f"Generated from {requirements_path.name}"
        if ac_id:
            notes = f"Covers {ac_id}; {notes}"
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

    _append_epic_tracker_rows(epic_tracker_path, rows_to_add)
    print(f"Added {len(rows_to_add)} Proposed row(s) to {epic_tracker_path}")
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
    parent_ac_coverage = _extract_parent_ac_coverage(target)

    child_dir.mkdir(parents=True, exist_ok=True)
    if args.overwrite or not impl_path.exists():
        _write_file(
            impl_path,
            _epic_child_implementation_template(
                child_spec.task_id,
                child_spec.title,
                parent_ac_coverage,
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
            ),
            overwrite=True,
        )

    target["Docs"] = f"tasks/{epic_dir.name}/{child_spec.task_folder_name}/IMPLEMENTATION.md"
    if branch_name is not None:
        target["Branch"] = branch_name
    target["Status"] = "In Progress"
    line_idx = int(target["_line_idx"])
    lines[line_idx] = _format_epic_tracker_row(target)
    epic_tracker_path.write_text("".join(lines), encoding="utf-8")

    print(f"Scaffolded epic child: {child_dir}")
    print(f"Updated epic tracker: {epic_tracker_path}")
    if branch_name is not None:
        print(f"Child branch active from epic branch {args.epic_branch}: {branch_name}")


def cmd_epic_audit(args: argparse.Namespace) -> None:
    """Generate an epic acceptance audit artifact."""
    cwd = Path.cwd()
    epic_dir, audit_rows, gaps = _epic_audit_rows(cwd, args.epic_id)
    audit_path = epic_dir / "ACCEPTANCE-AUDIT.md"
    audit_path.write_text(_format_acceptance_audit(args.epic_id, audit_rows), encoding="utf-8")
    print(f"Wrote acceptance audit: {audit_path}")
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
    audit_path = epic_dir / "ACCEPTANCE-AUDIT.md"
    audit_path.write_text(_format_acceptance_audit(args.epic_id, audit_rows), encoding="utf-8")
    if gaps:
        print(f"Wrote acceptance audit: {audit_path}")
        print("Epic closeout blocked by acceptance gaps:")
        for gap in gaps:
            print(f"- {gap}")
        raise SystemExit(1)

    print(f"Wrote acceptance audit: {audit_path}")
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
        doctor_parser.set_defaults(func=cmd_doctor)

    # ===== project task ... =====
    task_parser = subparsers.add_parser("task", help="Task-related commands")
    task_sub = task_parser.add_subparsers(dest="task_command", required=True)

    task_init_parser = task_sub.add_parser("init", help="Scaffold a new task folder + docs")
    task_init_parser.add_argument("--title", required=True, help="Human title (e.g. Super Admin Access)")
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

    epic_approve_parser = epic_sub.add_parser(
        "approve",
        help="Move one epic tracker row from Proposed to Approved",
    )
    epic_approve_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_approve_parser.add_argument("--id", required=True, help="Row ID in epic TRACKER.md")
    epic_approve_parser.set_defaults(func=cmd_epic_approve)

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

    epic_decompose_parser = epic_sub.add_parser(
        "decompose",
        help="Generate Proposed child rows only (no child scaffolding)",
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
