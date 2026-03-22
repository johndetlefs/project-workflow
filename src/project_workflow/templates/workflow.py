#!/usr/bin/env python3
"""Local task scaffolding CLI for project-workflow."""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional


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


def _rollback_file_changes(
    *,
    created_files: list[Path],
    overwritten_files: dict[Path, str],
    created_dirs: list[Path],
) -> list[str]:
    errors: list[str] = []

    for path, original_content in overwritten_files.items():
        try:
            path.write_text(original_content, encoding="utf-8")
        except OSError as exc:
            errors.append(f"restore {path}: {exc}")

    for path in reversed(created_files):
        try:
            if path.exists():
                path.unlink()
        except OSError as exc:
            errors.append(f"remove {path}: {exc}")

    for path in sorted(created_dirs, key=lambda p: len(p.parts), reverse=True):
        try:
            if path.exists() and not any(path.iterdir()):
                path.rmdir()
        except OSError as exc:
            errors.append(f"remove dir {path}: {exc}")

    return errors


def _rollback_git_state(
    cwd: Path,
    *,
    original_branch: str | None,
    created_branch: str | None,
) -> list[str]:
    errors: list[str] = []

    if original_branch:
        try:
            current_branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
            if current_branch != original_branch:
                _run_git(["checkout", original_branch], cwd=cwd)
        except (subprocess.CalledProcessError, OSError) as exc:
            errors.append(f"restore branch {original_branch}: {exc}")

    if created_branch:
        try:
            if _branch_exists(cwd, created_branch):
                _run_git(["branch", "-D", created_branch], cwd=cwd)
        except (subprocess.CalledProcessError, OSError) as exc:
            errors.append(f"delete branch {created_branch}: {exc}")

    return errors


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
    header_idx: int | None = None
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


def _collect_used_task_ids(
    *,
    tasks_dir: Path,
    global_tracker_path: Path,
    exclude_epic_tracker_path: Path | None = None,
    exclude_epic_tracker_line_idx: int | None = None,
) -> set[str]:
    used_ids: set[str] = set()
    task_re = re.compile(rf"^{re.escape(TASK_ID_PREFIX)}-\d+$")

    for path in tasks_dir.iterdir():
        if not path.is_dir():
            continue
        match = re.match(rf"^{re.escape(TASK_ID_PREFIX)}-(\d+)-", path.name)
        if match:
            used_ids.add(f"{TASK_ID_PREFIX}-{int(match.group(1)):0{ID_PADDING}d}")

    if global_tracker_path.exists():
        tracker_text = global_tracker_path.read_text(encoding="utf-8")
        for match in re.finditer(rf"\|\s*({re.escape(TASK_ID_PREFIX)}-\d+)\s*\|", tracker_text):
            candidate = match.group(1)
            if task_re.match(candidate):
                used_ids.add(candidate)

    for epic_dir in tasks_dir.iterdir():
        if not epic_dir.is_dir():
            continue
        epic_tracker_path = epic_dir / "TRACKER.md"
        if not epic_tracker_path.exists():
            continue
        _lines, _header_idx, epic_rows = _epic_tracker_rows(epic_tracker_path)
        for row in epic_rows:
            if (
                exclude_epic_tracker_path is not None
                and epic_tracker_path == exclude_epic_tracker_path
                and exclude_epic_tracker_line_idx is not None
                and int(row["_line_idx"]) == exclude_epic_tracker_line_idx
            ):
                continue
            candidate = row["ID"].strip()
            if task_re.match(candidate):
                used_ids.add(candidate)

    return used_ids


def _decompose_epic_requirements_to_titles(requirements_text: str, *, limit: int) -> list[str]:
    lines = requirements_text.splitlines()
    bullets: list[str] = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            in_section = heading.startswith("acceptance criteria") or heading.startswith(
                "requirements"
            )
            continue
        if not in_section:
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

    existing_row_idx: int | None = None
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


def cmd_task_init(args: argparse.Namespace) -> None:
    here = Path(__file__)
    repo_root = here.resolve().parents[2]

    workflow_dir = repo_root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"

    if not tracker_path.exists():
        raise SystemExit(f"Missing tracker file: {tracker_path}")

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
    branch_name: str | None = None

    if args.create_branch:
        _ensure_clean_git(repo_root)

        base_branch = args.base_branch
        branch_name = f"{args.branch_prefix}{spec.task_id}-{slug_kebab_lower(spec.title)}"

        # Ensure base branch exists locally and is checked out.
        _run_git(["checkout", base_branch], cwd=repo_root)
        _run_git(["pull"], cwd=repo_root)

        # Create and switch.
        _run_git(["checkout", "-b", branch_name], cwd=repo_root)

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
    here = Path(__file__)
    repo_root = here.resolve().parents[2]

    workflow_dir = repo_root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"

    if not tracker_path.exists():
        raise SystemExit(f"Missing tracker file: {tracker_path}")

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

    created_files: list[Path] = []
    overwritten_files: dict[Path, str] = {}
    created_dirs: list[Path] = []

    try:
        if not epic_dir.exists():
            epic_dir.mkdir(parents=True, exist_ok=True)
            created_dirs.append(epic_dir)

        if args.overwrite or not reqs_path.exists():
            if reqs_path.exists():
                overwritten_files[reqs_path] = reqs_path.read_text(encoding="utf-8")
            _write_file(reqs_path, _requirements_template(spec.task_id, spec.title), overwrite=True)
            if reqs_path not in overwritten_files:
                created_files.append(reqs_path)

        if args.overwrite or not epic_tracker_path.exists():
            if epic_tracker_path.exists():
                overwritten_files[epic_tracker_path] = epic_tracker_path.read_text(encoding="utf-8")
            _write_file(epic_tracker_path, _epic_tracker_template(), overwrite=True)
            if epic_tracker_path not in overwritten_files:
                created_files.append(epic_tracker_path)

        docs_rel = f"tasks/{spec.task_folder_name}/REQUIREMENTS.md"
        row_written = _update_tracker(
            tracker_path,
            spec=spec,
            status=args.status,
            docs_rel_path=docs_rel,
            on_duplicate="skip",
        )
    except (OSError, SystemExit) as exc:
        rollback_errors = _rollback_file_changes(
            created_files=created_files,
            overwritten_files=overwritten_files,
            created_dirs=created_dirs,
        )
        message = (
            "Epic scaffold failed before completion. "
            f"Cause: {exc}. "
            "State was rolled back for files/directories touched in this run."
        )
        if rollback_errors:
            raise SystemExit(
                message
                + " Manual cleanup may be required for: "
                + "; ".join(rollback_errors)
            )
        raise SystemExit(
            message
            + " Resolve the error and re-run the same command; no manual cleanup should be "
            "required."
        )

    print(f"Created epic: {epic_dir}")
    if row_written:
        print(f"Updated tracker: {tracker_path}")
    else:
        print(f"Tracker already had row for ID {spec.task_id}; no duplicate added.")
    print(f"Assigned ID: {spec.task_id}")


def cmd_epic_approve(args: argparse.Namespace) -> None:
    """Approve a proposed epic child row by updating Status to Approved."""
    here = Path(__file__)
    repo_root = here.resolve().parents[2]
    workflow_dir = repo_root / ".project-workflow"
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
    here = Path(__file__)
    repo_root = here.resolve().parents[2]
    workflow_dir = repo_root / ".project-workflow"
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
            "Add list items under '## Requirements (Outcome-Focused)' or "
            "'## Acceptance Criteria (Verifiable)' first."
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
    here = Path(__file__)
    repo_root = here.resolve().parents[2]
    workflow_dir = repo_root / ".project-workflow"
    tasks_dir = workflow_dir / "tasks"
    tracker_path = workflow_dir / "TRACKER.md"

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

    assigned_id = target["ID"]
    occupied_task_ids = _collect_used_task_ids(
        tasks_dir=tasks_dir,
        global_tracker_path=tracker_path,
        exclude_epic_tracker_path=epic_tracker_path,
        exclude_epic_tracker_line_idx=int(target["_line_idx"]),
    )
    if not re.match(rf"^{re.escape(TASK_ID_PREFIX)}-\d+$", assigned_id):
        reassigned_id = _next_task_id_from_used(occupied_task_ids)
        print(
            f"Row {args.id} used non-task ID '{assigned_id}'. "
            f"Assigned next available global ID: {reassigned_id}."
        )
        assigned_id = reassigned_id
    elif assigned_id in occupied_task_ids:
        reassigned_id = _next_task_id_from_used(occupied_task_ids)
        print(
            f"Detected ID collision for {assigned_id}. "
            f"Assigned next available global ID: {reassigned_id}."
        )
        assigned_id = reassigned_id

    child_spec = TaskSpec(
        task_id=assigned_id,
        title=target["Title"],
        folder_suffix=slug_titlecase_dashes(target["Title"]),
    )
    branch_name: str | None = None
    child_dir = epic_dir / child_spec.task_folder_name
    impl_path = child_dir / "IMPLEMENTATION.md"
    reqs_path = child_dir / "REQUIREMENTS.md"

    created_files: list[Path] = []
    overwritten_files: dict[Path, str] = {}
    created_dirs: list[Path] = []
    original_branch: str | None = None
    created_branch: str | None = None

    try:
        if args.create_branch:
            _ensure_clean_git(repo_root)
            original_branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root)
            epic_branch = args.epic_branch
            branch_name = (
                f"{args.branch_prefix}{child_spec.task_id}-{slug_kebab_lower(child_spec.title)}"
            )

            if not _branch_exists(repo_root, epic_branch):
                raise SystemExit(
                    f"Epic branch '{epic_branch}' was not found. "
                    "Child branches for epic-managed tasks must branch from the epic branch "
                    "and never fall back to a base branch. "
                    "Create or checkout the epic branch first, for example: "
                    f"git checkout -b {epic_branch} develop"
                )

            _run_git(["checkout", epic_branch], cwd=repo_root)
            if _branch_exists(repo_root, branch_name):
                _run_git(["checkout", branch_name], cwd=repo_root)
            else:
                _run_git(["checkout", "-b", branch_name], cwd=repo_root)
                created_branch = branch_name

        if not child_dir.exists():
            child_dir.mkdir(parents=True, exist_ok=True)
            created_dirs.append(child_dir)

        if args.overwrite or not impl_path.exists():
            if impl_path.exists():
                overwritten_files[impl_path] = impl_path.read_text(encoding="utf-8")
            _write_file(
                impl_path,
                _implementation_template(child_spec.task_id, child_spec.title),
                overwrite=True,
            )
            if impl_path not in overwritten_files:
                created_files.append(impl_path)

        if args.overwrite or not reqs_path.exists():
            if reqs_path.exists():
                overwritten_files[reqs_path] = reqs_path.read_text(encoding="utf-8")
            _write_file(
                reqs_path,
                _requirements_template(child_spec.task_id, child_spec.title),
                overwrite=True,
            )
            if reqs_path not in overwritten_files:
                created_files.append(reqs_path)

        if target["ID"] != assigned_id:
            prior_id = target["ID"]
            target["ID"] = assigned_id
            note = target["Notes"].strip()
            collision_note = f"Reassigned from {prior_id} due to ID collision"
            target["Notes"] = f"{note}; {collision_note}" if note else collision_note

        target["Docs"] = f"tasks/{epic_dir.name}/{child_spec.task_folder_name}/IMPLEMENTATION.md"
        if branch_name is not None:
            target["Branch"] = branch_name
        target["Status"] = "In Progress"
        line_idx = int(target["_line_idx"])
        lines[line_idx] = _format_epic_tracker_row(target)
        epic_tracker_path.write_text("".join(lines), encoding="utf-8")
    except (subprocess.CalledProcessError, OSError, SystemExit) as exc:
        rollback_errors = _rollback_file_changes(
            created_files=created_files,
            overwritten_files=overwritten_files,
            created_dirs=created_dirs,
        )
        rollback_errors.extend(
            _rollback_git_state(
                repo_root,
                original_branch=original_branch,
                created_branch=created_branch,
            )
        )
        message = (
            "Epic child scaffold failed before completion. "
            f"Cause: {exc}. "
            "State was rolled back for files/directories and branch changes from this run."
        )
        if rollback_errors:
            raise SystemExit(
                message
                + " Manual cleanup may be required for: "
                + "; ".join(rollback_errors)
            )
        raise SystemExit(
            message
            + " Resolve the error and re-run the same command; no manual cleanup should be "
            "required."
        )

    print(f"Scaffolded epic child: {child_dir}")
    print(f"Updated epic tracker: {epic_tracker_path}")
    if branch_name is not None:
        print(f"Child branch active from epic branch {args.epic_branch}: {branch_name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="workflow",
        description="Local task scaffolding helper for project-workflow.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    task_parser = subparsers.add_parser("task", help="Task-related commands")
    task_sub = task_parser.add_subparsers(dest="task_command", required=True)

    init_parser = task_sub.add_parser("init", help="Scaffold a new task folder + docs")
    init_parser.add_argument("--title", required=True, help="Human title (e.g. Super Admin Access)")
    init_parser.add_argument(
        "--folder-suffix",
        help=(
            "Overrides the task folder suffix after the ID. "
            "Default: Title converted to Title-Case-With-Dashes"
        ),
    )
    init_parser.add_argument(
        "--status",
        default="To Do",
        help="Initial tracker status (default: To Do)",
    )
    init_parser.add_argument(
        "--update-tracker",
        action="store_true",
        help="Append the story to .project-workflow/TRACKER.md",
    )
    init_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing task docs if task folder already exists",
    )

    init_parser.add_argument(
        "--create-branch",
        action="store_true",
        help="Create and checkout a git branch for the task",
    )
    init_parser.add_argument(
        "--base-branch",
        default="develop",
        help="Base branch to branch from (default: develop)",
    )
    init_parser.add_argument(
        "--branch-prefix",
        default="feature/",
        help="Branch prefix (default: feature/)",
    )

    init_parser.set_defaults(func=cmd_task_init)

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

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
