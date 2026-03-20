#!/usr/bin/env python3
"""project-workflow CLI: Bootstrap and task scaffolding for spec-driven development."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from dataclasses import dataclass
from datetime import date
from importlib.resources import files
from pathlib import Path
from typing import Optional


AGENT_CHOICES = {
    "github-copilot": "GitHub Copilot",
    "claude-code": "Claude Code",
    "cursor": "Cursor",
}

PROMPT_FILES = [
    "Constitution.prompt.md",
    "Clarify.prompt.md",
    "Delegate.prompt.md",
    "Implement.prompt.md",
    "Planner.prompt.md",
    "Requirements.prompt.md",
    "Scaffold.prompt.md",
]

TASK_ID_PREFIX = "TASK"
EPIC_ID_PREFIX = "EPIC"
ID_PADDING = 3
EPIC_TRACKER_COLUMNS = ("ID", "Title", "Status", "Type", "Docs", "Branch", "Notes")
EPIC_TRACKER_STATUSES = ("Proposed", "Approved", "In Progress", "Testing", "Complete")


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


def _file_hash(content: str) -> str:
    """Compute SHA256 hash of file content for conflict detection."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _prompt_overwrite(file_path: Path, package_content: str) -> bool:
    """Ask user whether to keep local version or update to package version."""
    local_content = file_path.read_text(encoding="utf-8")
    local_hash = _file_hash(local_content)
    package_hash = _file_hash(package_content)

    if local_hash == package_hash:
        # Identical, silently succeed
        return False

    print(f"\n⚠️  Conflict detected: {file_path}")
    print(f"   Local version differs from package version.")
    while True:
        choice = input(f"   Keep your local version? [y/n]: ").strip().lower()
        if choice in ("y", "n"):
            return choice == "n"  # True = overwrite (n), False = keep local (y)
        print("   Please enter 'y' or 'n'.")


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


def _ensure_file(
    path: Path,
    content: str,
    *,
    allow_conflicts: bool = True,
) -> None:
    """Write file, with optional conflict detection."""
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        if allow_conflicts:
            should_overwrite = _prompt_overwrite(path, content)
            if not should_overwrite:
                return
        else:
            # Silent overwrite (for idempotent updates)
            return

    path.write_text(content, encoding="utf-8")


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    title: str
    folder_suffix: str

    @property
    def task_folder_name(self) -> str:
        return f"{self.task_id}-{self.folder_suffix}"


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
        f"- [ ] ____\n\n"
        f"## Validation\n\n"
        f"- ____\n\n"
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
        f"- ____\n\n"
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
        "| ID | Title | Status | Type | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
    )


def _parse_markdown_table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _epic_tracker_rows(epic_tracker_path: Path) -> tuple[list[str], int, list[dict[str, str]]]:
    lines = epic_tracker_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_idx: Optional[int] = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        if cells == list(EPIC_TRACKER_COLUMNS):
            header_idx = idx
            break

    if header_idx is None:
        expected = " | ".join(EPIC_TRACKER_COLUMNS)
        raise SystemExit(
            "Epic tracker schema mismatch. Expected header: "
            f"'| {expected} |' in {epic_tracker_path}."
        )

    rows: list[dict[str, str]] = []
    row_idx = header_idx + 2  # skip divider row
    while row_idx < len(lines):
        cells = _parse_markdown_table_cells(lines[row_idx])
        if cells is None:
            break
        if len(cells) != len(EPIC_TRACKER_COLUMNS):
            raise SystemExit(
                "Epic tracker row has wrong number of columns. "
                f"Expected {len(EPIC_TRACKER_COLUMNS)} columns in {epic_tracker_path}: "
                f"{lines[row_idx].strip()}"
            )
        row = dict(zip(EPIC_TRACKER_COLUMNS, cells))
        status = row["Status"]
        if status and status not in EPIC_TRACKER_STATUSES:
            raise SystemExit(
                "Epic tracker contains invalid status "
                f"'{status}'. Allowed: {', '.join(EPIC_TRACKER_STATUSES)}."
            )
        row["_line_idx"] = str(row_idx)
        rows.append(row)
        row_idx += 1

    return lines, header_idx, rows


def _format_epic_tracker_row(row: dict[str, str]) -> str:
    return "| " + " | ".join(row[col] for col in EPIC_TRACKER_COLUMNS) + " |\n"


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


def _decompose_epic_requirements_to_titles(requirements_text: str, *, limit: int) -> list[str]:
    lines = requirements_text.splitlines()
    bullets: list[str] = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            in_section = stripped in {"## Acceptance Criteria", "## Requirements"}
            continue
        if not in_section:
            continue
        if not stripped.startswith("-"):
            continue
        bullet = stripped.lstrip("-").strip()
        if not bullet or bullet == "____":
            continue
        bullet = re.sub(r"^AC\d+\s*:\s*", "", bullet, flags=re.IGNORECASE)
        bullet = re.sub(r"^A user can\s+", "", bullet, flags=re.IGNORECASE)
        bullet = re.sub(r"^Users can\s+", "", bullet, flags=re.IGNORECASE)
        bullet = bullet[:1].upper() + bullet[1:] if bullet else bullet
        bullets.append(bullet.rstrip("."))
        if len(bullets) >= limit:
            break
    return bullets


def _append_epic_tracker_rows(epic_tracker_path: Path, rows_to_add: list[dict[str, str]]) -> None:
    lines, header_idx, rows = _epic_tracker_rows(epic_tracker_path)
    existing_ids = {row["ID"] for row in rows}
    duplicate_ids = [row["ID"] for row in rows_to_add if row["ID"] in existing_ids]
    if duplicate_ids:
        raise SystemExit(
            "Cannot append decomposition proposals; epic tracker already contains IDs: "
            + ", ".join(sorted(set(duplicate_ids)))
        )

    insert_at = header_idx + 2 + len(rows)
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


def _prompt_filename_to_claude_agent_name(prompt_file: str) -> str:
    base_name = prompt_file.replace(".prompt.md", "")
    return f"project-{slug_kebab_lower(base_name)}"


def _prompt_filename_to_cursor_agent_name(prompt_file: str) -> str:
    base_name = prompt_file.replace(".prompt.md", "")
    return f"project-{slug_kebab_lower(base_name)}"


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

    dir_re = re.compile(rf"^{re.escape(prefix)}-(\d+)-")
    for path in tasks_dir.iterdir():
        if not path.is_dir():
            continue
        match = dir_re.match(path.name)
        if match:
            max_value = max(max_value, int(match.group(1)))

    tracker = tracker_path.read_text(encoding="utf-8")
    row_re = re.compile(rf"^\|\s*{re.escape(prefix)}-(\d+)\s*\|", flags=re.MULTILINE)
    for match in row_re.finditer(tracker):
        max_value = max(max_value, int(match.group(1)))

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


def cmd_project_init(args: argparse.Namespace) -> None:
    """Bootstrap project-workflow in the current directory."""
    cwd = Path.cwd()
    selected_agent = args.agent
    selected_agent_label = AGENT_CHOICES[selected_agent]

    print(f"Selected agent mode: {selected_agent_label} ({selected_agent})")

    # Create .project-workflow structure
    project_workflow_dir = cwd / ".project-workflow"
    tasks_dir = project_workflow_dir / "tasks"
    cli_dir = project_workflow_dir / "cli"
    tracker_path = project_workflow_dir / "TRACKER.md"

    # Create directories
    tasks_dir.mkdir(parents=True, exist_ok=True)
    cli_dir.mkdir(parents=True, exist_ok=True)

    # Create initial TRACKER.md if missing
    if not tracker_path.exists():
        tracker_path.write_text(_tracker_template(), encoding="utf-8")
        print(f"✓ Created: {tracker_path}")
    else:
        print(f"✓ Exists: {tracker_path}")

    # Create/update the workflow CLI files in .project-workflow/cli/
    workflow_py_path = cli_dir / "workflow.py"
    workflow_sh_path = cli_dir / "workflow"

    # Copy the workflow.py to the initialized project
    workflow_py_content = _get_package_resource("templates/workflow.py")
    _ensure_file(workflow_py_path, workflow_py_content, allow_conflicts=True)
    print(f"✓ Created/updated: {workflow_py_path}")

    # Copy the workflow shell wrapper
    workflow_sh_content = _get_package_resource("templates/workflow")
    _ensure_file(workflow_sh_path, workflow_sh_content, allow_conflicts=False)
    workflow_sh_path.chmod(0o755)  # Make executable
    print(f"✓ Created/updated: {workflow_sh_path}")

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
            _ensure_file(agent_path, agent_content, allow_conflicts=True)
            print(f"✓ Created/updated: {agent_path}")

        customize_path_hint = ".claude/agents/* files"
    elif selected_agent == "cursor":
        # Create canonical Cursor project subagent layout at .cursor/agents/*.md
        cursor_agents_dir = cwd / ".cursor" / "agents"
        cursor_agents_dir.mkdir(parents=True, exist_ok=True)

        for prompt_file in PROMPT_FILES:
            prompt_content = _get_package_resource(f"prompts/{prompt_file}")
            agent_name = _prompt_filename_to_cursor_agent_name(prompt_file)
            agent_path = cursor_agents_dir / f"{agent_name}.md"
            agent_content = _to_cursor_agent_markdown(prompt_content, agent_name)
            _ensure_file(agent_path, agent_content, allow_conflicts=True)
            print(f"✓ Created/updated: {agent_path}")

        customize_path_hint = ".cursor/agents/* files"
    else:
        # Keep existing GitHub Copilot scaffold contract for default mode.
        github_dir = cwd / ".github"
        prompts_dir = github_dir / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)

        for prompt_file in PROMPT_FILES:
            prompt_path = prompts_dir / prompt_file
            prompt_content = _get_package_resource(f"prompts/{prompt_file}")
            _ensure_file(prompt_path, prompt_content, allow_conflicts=True)
            print(f"✓ Created/updated: {prompt_path}")

    print(f"\n✅ Project workflow initialized in {cwd}")
    print(f"   Agent mode applied: {selected_agent_label}")
    print(f"\nNext steps:")
    print(f"  • Review: .project-workflow/TRACKER.md")
    print(f"  • Customize: {customize_path_hint}")
    print(f"  • Create tasks: ./.project-workflow/cli/workflow task init --help")


def cmd_task_init(args: argparse.Namespace) -> None:
    """Scaffold a new task in .project-workflow/tasks/"""
    cwd = Path.cwd()

    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"

    if not tracker_path.exists():
        raise SystemExit(
            f"Missing tracker file: {tracker_path}\n"
            f"Run 'project init' first to bootstrap the project workflow."
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


def cmd_epic_init(args: argparse.Namespace) -> None:
    """Scaffold a new epic in .project-workflow/tasks/."""
    cwd = Path.cwd()

    workflow_dir = cwd / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"

    if not tracker_path.exists():
        raise SystemExit(
            f"Missing tracker file: {tracker_path}\n"
            f"Run 'project init' first to bootstrap the project workflow."
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

    epic_dir.mkdir(parents=True, exist_ok=True)
    if args.overwrite or not reqs_path.exists():
        _write_file(reqs_path, _requirements_template(spec.task_id, spec.title), overwrite=True)
    if args.overwrite or not epic_tracker_path.exists():
        _write_file(epic_tracker_path, _epic_tracker_template(), overwrite=True)

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
    titles = _decompose_epic_requirements_to_titles(requirements_text, limit=args.limit)
    if not titles:
        raise SystemExit(
            "No decomposition candidates found in epic REQUIREMENTS.md. "
            "Add bullet points under '## Acceptance Criteria' or '## Requirements' first."
        )

    occupied_ids: set[str] = set()
    task_re = re.compile(rf"^{re.escape(TASK_ID_PREFIX)}-\d+$")

    for path in tasks_dir.iterdir():
        if not path.is_dir():
            continue
        match = re.match(rf"^{re.escape(TASK_ID_PREFIX)}-(\d+)-", path.name)
        if match:
            occupied_ids.add(f"{TASK_ID_PREFIX}-{int(match.group(1)):0{ID_PADDING}d}")

    tracker_text = tracker_path.read_text(encoding="utf-8")
    for match in re.finditer(rf"\|\s*({re.escape(TASK_ID_PREFIX)}-\d+)\s*\|", tracker_text):
        candidate = match.group(1)
        if task_re.match(candidate):
            occupied_ids.add(candidate)

    _lines, _header_idx, epic_rows = _epic_tracker_rows(epic_tracker_path)
    for row in epic_rows:
        candidate = row["ID"].strip()
        if task_re.match(candidate):
            occupied_ids.add(candidate)

    rows_to_add: list[dict[str, str]] = []
    for title in titles:
        next_id = _next_task_id_from_used(occupied_ids)
        occupied_ids.add(next_id)
        rows_to_add.append(
            {
                "ID": next_id,
                "Title": title,
                "Status": "Proposed",
                "Type": args.item_type,
                "Docs": "",
                "Branch": "",
                "Notes": f"Generated from {requirements_path.name}",
            }
        )

    _append_epic_tracker_rows(epic_tracker_path, rows_to_add)
    print(f"Added {len(rows_to_add)} Proposed row(s) to {epic_tracker_path}")
    print("No child task folders were created in this decomposition step.")


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

    child_dir.mkdir(parents=True, exist_ok=True)
    if args.overwrite or not impl_path.exists():
        _write_file(
            impl_path,
            _implementation_template(child_spec.task_id, child_spec.title),
            overwrite=True,
        )
    if args.overwrite or not reqs_path.exists():
        _write_file(
            reqs_path,
            _requirements_template(child_spec.task_id, child_spec.title),
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project",
        description="Project workflow: Spec-driven development for GitHub Copilot, Claude Code, and Cursor.",
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
            "Target agent ecosystem: github-copilot (default), claude-code, or cursor. "
            "Aliases accepted: copilot, claude, cursor."
        ),
    )
    init_parser.set_defaults(func=cmd_project_init)

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

    # ===== project epic ... =====
    epic_parser = subparsers.add_parser("epic", help="Epic-related commands")
    epic_sub = epic_parser.add_subparsers(dest="epic_command", required=True)

    epic_init_parser = epic_sub.add_parser(
        "init",
        help="Scaffold a new epic folder + REQUIREMENTS/TRACKER docs",
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
        help="Approve a Proposed row in an epic TRACKER.md",
    )
    epic_approve_parser.add_argument("--epic-id", required=True, help="Epic ID (e.g. EPIC-001)")
    epic_approve_parser.add_argument("--id", required=True, help="Row ID in epic TRACKER.md")
    epic_approve_parser.set_defaults(func=cmd_epic_approve)

    epic_decompose_parser = epic_sub.add_parser(
        "decompose",
        help="Generate Proposed child rows from an epic REQUIREMENTS.md",
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
        help="Scaffold one Approved child row from an epic TRACKER.md",
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
        help="Create and checkout a child branch from the epic branch",
    )
    epic_scaffold_child_parser.add_argument(
        "--epic-branch",
        default="epic/main",
        help=(
            "Existing epic branch to derive child branches from "
            "(default: epic/main)"
        ),
    )
    epic_scaffold_child_parser.add_argument(
        "--branch-prefix",
        default="feature/",
        help="Child branch prefix (default: feature/)",
    )
    epic_scaffold_child_parser.set_defaults(func=cmd_epic_scaffold_child)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
