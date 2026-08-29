"""Canonical Project Workflow lifecycle runtime."""

from __future__ import annotations

import hashlib
import json
import re
import secrets
import subprocess
import zipfile
from collections.abc import Mapping
from datetime import date
from pathlib import Path
from typing import TypedDict

from .contracts import (
    AC_MAPPED_IMPLEMENTATION_STATUSES,
    BACKLOG_COLUMNS,
    BACKLOG_ID_PREFIX,
    BACKLOG_PRIORITIES,
    BACKLOG_STATUSES,
    BACKLOG_TYPES,
    DECOMPOSITION_PLAN_FILENAME,
    DELEGATION_EXECUTION_NEEDS_TASK_COLUMNS,
    DELEGATION_IMPLEMENTATION_TASK_COLUMNS,
    EPIC_AMENDMENTS_FILENAME,
    EPIC_CONTRACT_FILENAME,
    EPIC_ID_PREFIX,
    EPIC_STATUS_TRANSITIONS,
    EPIC_TRACKER_COLUMNS,
    EPIC_TRACKER_FORMAT_KEY,
    EPIC_TRACKER_STATUSES,
    FIX_ACTIVE_DISPOSITION,
    FIX_CLASSIFICATIONS,
    FIX_ID_PREFIX,
    FIX_MODES,
    FIX_REPOSITORY_LINK_COLUMNS,
    FIX_RISK_LEVELS,
    FIX_SEVERITIES,
    FIX_STATUS_TRANSITIONS,
    FIX_TERMINAL_DISPOSITIONS,
    GLOBAL_TRACKER_COLUMNS,
    ID_PADDING,
    IMPLEMENTATION_TASK_COLUMNS,
    INTENT_AUDIT_FILENAME,
    INTENT_AUDIT_SCHEMA_VERSION,
    LEGACY_EPIC_TRACKER_COLUMNS,
    OPERATIONAL_STATUS_EPIC_CHILD_LIFECYCLE_MEANINGS,
    OPERATIONAL_STATUS_EPIC_CHILD_TERMINAL_STATES,
    OPERATIONAL_STATUS_EPIC_CHILD_UNSCAFFOLDED_STATES,
    OPERATIONAL_STATUS_GLOBAL_LIFECYCLE_MEANINGS,
    OPERATIONAL_STATUS_GLOBAL_TERMINAL_STATES,
    OPERATIONAL_STATUS_PROOF_LAYER_NAMES,
    PROOF_RECIPE_INVALID_SUBSTITUTE_PATTERNS,
    PROOF_RECIPE_REQUIRED_FIELDS,
    PROOF_RECIPE_TRIGGER_PATTERNS,
    STRUCTURED_EVIDENCE_FILENAME,
    TASK_STATUS_TRANSITIONS,
    UNIQUE_ID_ALPHABET,
    USER_OUTCOME_INVALID_SUBSTITUTE_POLICY,
    VALIDATION_IMPACT_CLASSIFICATIONS,
    VALIDATION_IMPACT_IDENTITY_PREFIX,
    VALIDATION_IMPACT_REQUIREMENTS,
    VALIDATION_IMPACT_VERDICTS,
    DoctorIssue,
    OperationalStatusFact,
    OperationalStatusFinding,
    OperationalStatusProofLayer,
    OperationalStatusSource,
    OperationalStatusWorkItem,
    TaskSpec,
    WorkflowConfig,
)
from .repository import (
    APPROVAL_IDENTITY_PREFIX,
    LEGACY_ADOPTION_HEADING,
    OWNER_APPROVAL_HEADING,
    _approval_artifact_identity,
    _approval_source_invalid,
    _approval_value_is_yes,
    _backlog_template,
    _clean_markdown_cell_path,
    _epic_contract_issues,
    _epic_contract_path,
    _epic_contract_proof_owner_map,
    _extract_ac_ids,
    _extract_declared_ac_ids,
    _extract_parent_ac_coverage,
    _extract_parent_ac_ids_from_requirements,
    _extract_workflow_ref_ids,
    _fix_value_missing,
    _fix_values,
    _flat_markdown_bullet_records,
    _id_generation_mode,
    _legacy_truncated_child_charter_issues,
    _load_workflow_config,
    _markdown_cell,
    _markdown_section,
    _markdown_table_rows_from_section,
    _normalize_fix_id,
    _normalize_task_status_id,
    _parse_key_value_section,
    _parse_markdown_table_cells,
    _remove_markdown_section,
    _replace_fix_field,
    _run_git,
    _section_has_placeholder,
    _section_has_substantive_text,
    _sha256_file,
    _template_repository_id,
    _valid_backlog_id,
    _valid_workflow_ref_id,
    slug_titlecase_dashes,
)


def _operational_status_artifact(root: Path, path: Path | str) -> str:
    artifact_path = Path(path)
    if not artifact_path.is_absolute():
        return artifact_path.as_posix()
    try:
        return artifact_path.relative_to(root.resolve()).as_posix()
    except ValueError:
        return artifact_path.as_posix()


def _operational_status_fact(
    key: str,
    value: str | int | bool | None | tuple[str, ...],
) -> OperationalStatusFact:
    return OperationalStatusFact(key, value)


def _operational_status_lifecycle_meaning(kind: str, lifecycle: str) -> str | None:
    entries = (
        OPERATIONAL_STATUS_EPIC_CHILD_LIFECYCLE_MEANINGS
        if kind == "epic-child"
        else OPERATIONAL_STATUS_GLOBAL_LIFECYCLE_MEANINGS
    )
    for stored_status, meaning in entries:
        if stored_status == lifecycle:
            return meaning
    return None


def _operational_status_global_kind(item_id: str) -> str:
    if item_id.startswith(f"{FIX_ID_PREFIX}-"):
        return "fix"
    if item_id.startswith(f"{EPIC_ID_PREFIX}-"):
        return "epic"
    return "task"


def _operational_tracker_issue_finding(
    root: Path,
    issue: DoctorIssue,
    source_kind: str,
) -> OperationalStatusFinding:
    source = OperationalStatusSource(
        source_kind,
        _operational_status_artifact(root, issue.path),
        "tracker parsing",
    )
    severity = "error" if issue.severity == "error" else "warning"
    return OperationalStatusFinding(issue.code, severity, issue.message, (source,))


def _operational_work_item_from_row(
    row: dict[str, str],
    *,
    kind: str,
    source: OperationalStatusSource,
    owner_epic: str | None = None,
) -> OperationalStatusWorkItem | None:
    item_id = row.get("ID", "").strip()
    title = row.get("Title", "").strip()
    lifecycle = row.get("Status", "").strip()
    meaning = _operational_status_lifecycle_meaning(kind, lifecycle)
    if not item_id or not title or meaning is None:
        return None
    docs_path = _clean_markdown_cell_path(row.get("Docs", "")) or None
    tracker_branch = _clean_markdown_cell_path(row.get("Branch", "")) or None
    facts = [
        _operational_status_fact("docs_path", docs_path),
        _operational_status_fact("tracker_branch", tracker_branch),
    ]
    if owner_epic is not None:
        facts.extend(
            (
                _operational_status_fact("owner_epic", owner_epic),
                _operational_status_fact(
                    "parent_acs",
                    tuple(sorted(_extract_ac_ids(_extract_parent_ac_coverage(row)))),
                ),
            )
        )
    return OperationalStatusWorkItem(
        item_id,
        title,
        kind,
        lifecycle,
        meaning,
        (source,),
        tuple(facts),
    )


def _parse_operational_epic_tracker(
    tracker_path: Path,
    *,
    issues: list[DoctorIssue],
    label: str,
) -> list[dict[str, str]]:
    try:
        lines = tracker_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return _parse_markdown_table(
            tracker_path,
            expected_columns=EPIC_TRACKER_COLUMNS,
            issues=issues,
            label=label,
        )
    columns: tuple[str, ...] | None = None
    for line in lines:
        cells = _parse_markdown_table_cells(line)
        if cells == list(EPIC_TRACKER_COLUMNS):
            columns = EPIC_TRACKER_COLUMNS
            break
        if cells == list(LEGACY_EPIC_TRACKER_COLUMNS):
            columns = LEGACY_EPIC_TRACKER_COLUMNS
            break
    rows = _parse_markdown_table(
        tracker_path,
        expected_columns=columns or EPIC_TRACKER_COLUMNS,
        issues=issues,
        label=label,
    )
    for row in rows:
        row.setdefault("Parent ACs", "")
    return rows


def _inspect_operational_active_work(
    root: Path,
) -> tuple[tuple[OperationalStatusWorkItem, ...], tuple[OperationalStatusFinding, ...]]:
    workflow_dir = root / ".project-workflow"
    tracker_path = workflow_dir / "TRACKER.md"
    global_source = OperationalStatusSource("global-tracker", ".project-workflow/TRACKER.md")
    if not tracker_path.exists():
        return (), (
            OperationalStatusFinding(
                "PW_STATUS_GLOBAL_TRACKER_MISSING",
                "error",
                "Global workflow tracker is missing.",
                (global_source,),
            ),
        )

    parse_issues: list[DoctorIssue] = []
    global_rows = _parse_markdown_table(
        tracker_path,
        expected_columns=GLOBAL_TRACKER_COLUMNS,
        issues=parse_issues,
        label="Global tracker",
    )
    findings = [
        _operational_tracker_issue_finding(root, issue, "global-tracker") for issue in parse_issues
    ]
    active_work: list[OperationalStatusWorkItem] = []
    seen_ids: dict[str, list[tuple[str, OperationalStatusSource]]] = {}
    active_epic_rows: list[dict[str, str]] = []
    terminal_epic_rows: list[dict[str, str]] = []

    def record_id(item_id: str, owner: str, source: OperationalStatusSource) -> None:
        previous = seen_ids.setdefault(item_id, [])
        if previous:
            previous_owners = [previous_owner for previous_owner, _source in previous]
            finding_sources = tuple(
                dict.fromkeys([previous_source for _owner, previous_source in previous] + [source])
            )
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_DUPLICATE_WORK_ITEM",
                    "error",
                    f"Workflow ID {item_id} appears in multiple tracker records: "
                    + ", ".join([*previous_owners, owner])
                    + ".",
                    finding_sources,
                )
            )
            if owner.startswith("EPIC-") and any(
                previous_owner.startswith("EPIC-") for previous_owner in previous_owners
            ):
                findings.append(
                    OperationalStatusFinding(
                        "PW_STATUS_MULTIPLE_EPIC_OWNERS",
                        "error",
                        f"Epic child {item_id} is owned by multiple Epics: "
                        + ", ".join([*previous_owners, owner])
                        + ".",
                        finding_sources,
                    )
                )
        previous.append((owner, source))

    for row in global_rows:
        item_id = row.get("ID", "").strip()
        title = row.get("Title", "").strip()
        lifecycle = row.get("Status", "").strip()
        kind = _operational_status_global_kind(item_id)
        record_id(item_id or "<missing>", "global tracker", global_source)
        meaning = _operational_status_lifecycle_meaning(kind, lifecycle)
        if not item_id or not title or meaning is None:
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_WORK_ITEM_INVALID",
                    "error",
                    f"Global tracker line {row.get('_line_idx', '?')} has missing or invalid "
                    "ID, title, or lifecycle.",
                    (global_source,),
                )
            )
            continue
        docs_path = row.get("Docs", "").strip().strip("`")
        if lifecycle not in OPERATIONAL_STATUS_GLOBAL_TERMINAL_STATES and not docs_path:
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_REQUIRED_DOCS_MISSING",
                    "warning",
                    f"Active global item {item_id} has no docs path.",
                    (global_source,),
                )
            )
        if lifecycle not in OPERATIONAL_STATUS_GLOBAL_TERMINAL_STATES:
            work_item = _operational_work_item_from_row(row, kind=kind, source=global_source)
            if work_item is not None:
                active_work.append(work_item)
        if kind == "epic":
            if lifecycle in OPERATIONAL_STATUS_GLOBAL_TERMINAL_STATES:
                terminal_epic_rows.append(row)
            else:
                active_epic_rows.append(row)

    tasks_dir = workflow_dir / "tasks"
    for parent_row in [*active_epic_rows, *terminal_epic_rows]:
        epic_id = parent_row["ID"].strip()
        matches = sorted(path for path in tasks_dir.glob(f"{epic_id}-*") if path.is_dir())
        if len(matches) != 1:
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_EPIC_TRACKER_MISSING",
                    "error",
                    f"Epic {epic_id} does not resolve to exactly one task directory.",
                    (global_source,),
                )
            )
            continue
        epic_tracker_path = matches[0] / "TRACKER.md"
        epic_source = OperationalStatusSource(
            "epic-tracker",
            _operational_status_artifact(root, epic_tracker_path),
            f"owner {epic_id}",
        )
        if not epic_tracker_path.exists():
            findings.append(
                OperationalStatusFinding(
                    "PW_STATUS_EPIC_TRACKER_MISSING",
                    "error",
                    f"Epic {epic_id} tracker is missing.",
                    (epic_source,),
                )
            )
            continue
        epic_parse_issues: list[DoctorIssue] = []
        epic_rows = _parse_operational_epic_tracker(
            epic_tracker_path,
            issues=epic_parse_issues,
            label=f"{epic_id} tracker",
        )
        findings.extend(
            _operational_tracker_issue_finding(root, issue, "epic-tracker")
            for issue in epic_parse_issues
        )
        parent_is_active = parent_row["Status"].strip() not in (
            OPERATIONAL_STATUS_GLOBAL_TERMINAL_STATES
        )
        for row in epic_rows:
            item_id = row.get("ID", "").strip()
            title = row.get("Title", "").strip()
            lifecycle = row.get("Status", "").strip()
            record_id(item_id or "<missing>", epic_id, epic_source)
            meaning = _operational_status_lifecycle_meaning("epic-child", lifecycle)
            if not item_id or not title or meaning is None:
                findings.append(
                    OperationalStatusFinding(
                        "PW_STATUS_WORK_ITEM_INVALID",
                        "error",
                        f"{epic_id} tracker line {row.get('_line_idx', '?')} has missing or "
                        "invalid ID, title, or lifecycle.",
                        (epic_source,),
                    )
                )
                continue
            docs_path = row.get("Docs", "").strip().strip("`")
            if (
                lifecycle not in OPERATIONAL_STATUS_EPIC_CHILD_UNSCAFFOLDED_STATES
                and lifecycle not in OPERATIONAL_STATUS_EPIC_CHILD_TERMINAL_STATES
                and not docs_path
            ):
                findings.append(
                    OperationalStatusFinding(
                        "PW_STATUS_REQUIRED_DOCS_MISSING",
                        "warning",
                        f"Scaffolded Epic child {item_id} has no docs path.",
                        (epic_source,),
                    )
                )
            child_is_active = lifecycle not in OPERATIONAL_STATUS_EPIC_CHILD_TERMINAL_STATES
            if parent_is_active and child_is_active:
                work_item = _operational_work_item_from_row(
                    row,
                    kind="epic-child",
                    source=epic_source,
                    owner_epic=epic_id,
                )
                if work_item is not None:
                    active_work.append(work_item)
            elif not parent_is_active and child_is_active:
                findings.append(
                    OperationalStatusFinding(
                        "PW_STATUS_CLOSED_EPIC_HAS_ACTIVE_CHILD",
                        "error",
                        f"Closed Epic {epic_id} still owns non-terminal child {item_id} "
                        f"in status {lifecycle}.",
                        (epic_source, global_source),
                    )
                )

    return tuple(active_work), tuple(findings)


def _operational_work_item_facts(item: OperationalStatusWorkItem) -> dict[str, object]:
    return {fact.key: fact.value for fact in item.facts}


def _operational_string_tuple_fact(item: OperationalStatusWorkItem, key: str) -> tuple[str, ...]:
    value = _operational_work_item_facts(item).get(key)
    return value if isinstance(value, tuple) else ()


def _operational_proof_layer(
    name: str,
    state: str,
    summary: str,
    *sources: OperationalStatusSource,
) -> OperationalStatusProofLayer:
    return OperationalStatusProofLayer(name, state, summary, tuple(sources))


def _operational_work_item_paths(
    root: Path,
    item: OperationalStatusWorkItem,
) -> tuple[Path | None, Path | None, Path | None]:
    item_facts = _operational_work_item_facts(item)
    docs_value = item_facts.get("docs_path")
    docs_path = (
        root / ".project-workflow" / str(docs_value)
        if isinstance(docs_value, str) and docs_value
        else None
    )
    owner_value = item_facts.get("owner_epic")
    epic_dir: Path | None = None
    if isinstance(owner_value, str) and owner_value:
        matches = sorted(
            path
            for path in (root / ".project-workflow" / "tasks").glob(f"{owner_value}-*")
            if path.is_dir()
        )
        if len(matches) == 1:
            epic_dir = matches[0]
    elif item.kind == "epic" and docs_path is not None:
        epic_dir = docs_path.parent

    if item.kind == "epic":
        requirements_path = docs_path
        implementation_path = None
    elif item.kind == "fix":
        requirements_path = None
        implementation_path = docs_path
    else:
        implementation_path = docs_path
        requirements_path = docs_path.parent / "REQUIREMENTS.md" if docs_path else None
    return requirements_path, implementation_path, epic_dir


def _operational_status_document_source(
    root: Path,
    kind: str,
    path: Path | None,
    fallback: OperationalStatusSource,
) -> OperationalStatusSource:
    if path is None:
        return fallback
    return OperationalStatusSource(kind, _operational_status_artifact(root, path))


def _operational_implementation_complete(implementation_text: str) -> bool:
    table_found, rows, malformed_rows = _implementation_task_table_rows(implementation_text)
    return bool(
        table_found
        and rows
        and not malformed_rows
        and all(row.get("Status", "").strip() == "Done" for row in rows)
    )


def _operational_epic_child_documents(
    root: Path, epic_dir: Path
) -> tuple[tuple[dict[str, str], Path, Path], ...]:
    """Return tracker-bound child requirements and implementation paths for an Epic."""
    tracker_path = epic_dir / "TRACKER.md"
    if not tracker_path.exists():
        return ()
    try:
        _lines, _header, rows = _epic_tracker_rows(tracker_path)
    except (OSError, SystemExit):
        return ()
    children: list[tuple[dict[str, str], Path, Path]] = []
    for row in rows:
        docs_rel = _clean_markdown_cell_path(row.get("Docs", ""))
        if not docs_rel:
            continue
        implementation_path = root / ".project-workflow" / docs_rel
        requirements_path = implementation_path.parent / "REQUIREMENTS.md"
        if requirements_path.exists() and implementation_path.exists():
            children.append((row, requirements_path, implementation_path))
    return tuple(children)


def _operational_item_proof_layers(
    root: Path,
    item: OperationalStatusWorkItem,
) -> tuple[OperationalStatusProofLayer, ...]:
    fallback = item.sources[0]
    requirements_path, implementation_path, epic_dir = _operational_work_item_paths(root, item)
    requirements_source = _operational_status_document_source(
        root, "requirements", requirements_path, fallback
    )
    implementation_source = _operational_status_document_source(
        root, "implementation", implementation_path, fallback
    )
    owner_epic = _operational_work_item_facts(item).get("owner_epic")
    parent_requirements_path = epic_dir / "REQUIREMENTS.md" if epic_dir is not None else None
    parent_requirements_source = _operational_status_document_source(
        root, "requirements", parent_requirements_path, fallback
    )
    requirements_text = (
        requirements_path.read_text(encoding="utf-8")
        if requirements_path is not None and requirements_path.exists()
        else ""
    )
    implementation_text = (
        implementation_path.read_text(encoding="utf-8")
        if implementation_path is not None and implementation_path.exists()
        else ""
    )

    if item.kind == "fix":
        approval = _operational_proof_layer(
            "requirements-approval",
            "not-required",
            "Fix authority is recorded in FIX.md rather than a requirements approval envelope.",
            implementation_source,
        )
    elif item.kind == "epic-child" and parent_requirements_path is not None:
        parent_text = (
            parent_requirements_path.read_text(encoding="utf-8")
            if parent_requirements_path.exists()
            else ""
        )
        approval_issues = _approval_envelope_issues(
            parent_text,
            require_decomposition=True,
        )
        approval = _operational_proof_layer(
            "requirements-approval",
            "pass" if not approval_issues else "fail",
            (
                f"Child authority is inherited from approved Epic {owner_epic}."
                if not approval_issues
                else f"Parent Epic approval has {len(approval_issues)} blocking issue(s)."
            ),
            parent_requirements_source,
        )
    elif requirements_text:
        approval_issues = _approval_envelope_issues(
            requirements_text,
            require_decomposition=item.kind == "epic",
            require_implementation=item.kind == "task",
        )
        approval = _operational_proof_layer(
            "requirements-approval",
            "pass" if not approval_issues else "fail",
            (
                "Owner approval envelope is current."
                if not approval_issues
                else f"Approval envelope has {len(approval_issues)} blocking issue(s)."
            ),
            requirements_source,
        )
    else:
        approval = _operational_proof_layer(
            "requirements-approval",
            "not-recorded",
            "No requirements approval source is recorded.",
            fallback,
        )

    if item.kind == "epic-child" and item.lifecycle in {
        "Proposed",
        "Approved",
    }:
        readiness = _operational_proof_layer(
            "readiness",
            "pending",
            "Child readiness begins after scaffolding.",
            fallback,
        )
    elif item.kind == "fix":
        ready = item.lifecycle not in {"To Do", "N/A"}
        readiness = _operational_proof_layer(
            "readiness",
            "pass" if ready else "pending",
            "Fix triage has advanced beyond To Do." if ready else "Fix triage is pending.",
            implementation_source,
        )
    elif item.kind == "epic" and epic_dir is not None and requirements_text:
        ready_issues = [
            *_epic_requirements_readiness_issues(requirements_text),
            *_approval_envelope_issues(requirements_text, require_decomposition=True),
            *_epic_contract_issues(epic_dir, requirements_text),
        ]
        readiness = _operational_proof_layer(
            "readiness",
            "pass" if not ready_issues else "fail",
            (
                "Epic readiness requirements and contract pass."
                if not ready_issues
                else f"Epic readiness has {len(ready_issues)} blocking issue(s)."
            ),
            requirements_source,
        )
    elif requirements_path is not None and implementation_path is not None:
        ready_issues = _task_ready_issues_for_paths(
            requirements_path=requirements_path,
            implementation_path=implementation_path,
            parent_ac_ids=(
                set(_operational_string_tuple_fact(item, "parent_acs"))
                if item.kind == "epic-child"
                else None
            ),
        )
        readiness = _operational_proof_layer(
            "readiness",
            "pass" if not ready_issues else "fail",
            (
                "Task readiness gate passes."
                if not ready_issues
                else f"Task readiness has {len(ready_issues)} blocking issue(s)."
            ),
            implementation_source,
        )
    else:
        readiness = _operational_proof_layer(
            "readiness",
            "not-recorded",
            "No readiness source is recorded.",
            fallback,
        )

    if item.kind == "epic":
        child_rows: list[dict[str, str]] = []
        if epic_dir is not None and (epic_dir / "TRACKER.md").exists():
            try:
                _lines, _header, child_rows = _epic_tracker_rows(epic_dir / "TRACKER.md")
            except SystemExit:
                child_rows = []
        all_children_complete = bool(child_rows) and all(
            row.get("Status") == "Complete" for row in child_rows
        )
        implementation_state = "pass" if all_children_complete else "pending"
        implementation_summary = (
            "All Epic children are complete."
            if all_children_complete
            else "Epic child implementation remains in progress."
        )
    elif item.kind == "fix":
        implementation_state = (
            "pass" if item.lifecycle in {"Testing", "Review", "Complete"} else "pending"
        )
        implementation_summary = (
            "Fix implementation reached validation."
            if implementation_state == "pass"
            else "Fix implementation remains in progress."
        )
    elif not implementation_text:
        implementation_state = "not-recorded"
        implementation_summary = "No implementation document is recorded."
    else:
        complete = _operational_implementation_complete(implementation_text)
        if complete:
            implementation_state = "pass"
            implementation_summary = "Every implementation task row is Done."
        elif item.lifecycle in {"Testing", "Review", "Complete"}:
            implementation_state = "fail"
            implementation_summary = (
                "Lifecycle advanced beyond implementation with unfinished rows."
            )
        else:
            implementation_state = "pending"
            implementation_summary = "Implementation task rows remain in progress."
    implementation = _operational_proof_layer(
        "implementation",
        implementation_state,
        implementation_summary,
        implementation_source,
    )

    epic_children = (
        _operational_epic_child_documents(root, epic_dir)
        if item.kind == "epic" and epic_dir is not None
        else ()
    )
    if item.kind == "epic":
        qa_pass = (
            bool(epic_children)
            and len(epic_children) == len(child_rows)
            and all(
                row.get("Status") == "Complete"
                and _qa_passed(implementation_path.read_text(encoding="utf-8"))
                for row, _requirements_path, implementation_path in epic_children
            )
        )
        qa_summary_pass = "Every completed Epic child records a passing final QA disposition."
        qa_sources = tuple(
            _operational_status_document_source(
                root, "implementation", implementation_path, fallback
            )
            for _row, _requirements_path, implementation_path in epic_children
        ) or (fallback,)
    else:
        qa_pass = bool(implementation_text and _qa_passed(implementation_text))
        qa_summary_pass = "QA and code review has a passing final disposition."
        qa_sources = (implementation_source,)
    if qa_pass:
        qa_state = "pass"
        qa_summary = qa_summary_pass
    elif item.lifecycle in {"Review", "Closeout", "Complete"}:
        qa_state = "fail"
        qa_summary = "No passing QA verdict is recorded."
    else:
        qa_state = "not-recorded"
        qa_summary = "No passing QA verdict is recorded yet."
    qa = _operational_proof_layer(
        "qa-review",
        qa_state,
        qa_summary,
        *qa_sources,
    )

    if item.kind == "epic-child":
        parent_acs = set(_operational_string_tuple_fact(item, "parent_acs"))
        evidence_pass = (
            bool(parent_acs)
            and bool(implementation_text)
            and all(_parent_ac_evidence_present(implementation_text, ac_id) for ac_id in parent_acs)
        )
        acceptance_state = "pass" if evidence_pass else "pending"
        acceptance_summary = (
            "Parent AC evidence is recorded for every owned AC."
            if evidence_pass
            else "Parent AC evidence remains incomplete."
        )
        acceptance_source = implementation_source
    elif item.kind == "epic":
        audit_path = epic_dir / "ACCEPTANCE-AUDIT.md" if epic_dir is not None else None
        audit_text = (
            audit_path.read_text(encoding="utf-8")
            if audit_path is not None and audit_path.exists()
            else ""
        )
        audit_pass = bool(audit_text) and "| Pass |" in audit_text and "| Gap |" not in audit_text
        acceptance_state = "pass" if audit_pass else "pending"
        acceptance_summary = (
            "Epic acceptance audit records passing coverage."
            if audit_pass
            else "Epic acceptance audit is not yet passing."
        )
        acceptance_source = _operational_status_document_source(
            root, "acceptance", audit_path, fallback
        )
    else:
        acceptance_state = "not-required"
        acceptance_summary = "This work item has no parent Epic acceptance obligation."
        acceptance_source = fallback
    acceptance = _operational_proof_layer(
        "parent-acceptance",
        acceptance_state,
        acceptance_summary,
        acceptance_source,
    )

    triggered_recipes = _triggered_proof_recipes(requirements_text, implementation_text)
    current_evidence_path = (
        implementation_path.parent / STRUCTURED_EVIDENCE_FILENAME
        if implementation_path is not None
        else None
    )
    if current_evidence_path is not None and current_evidence_path.exists():
        explicit_records, _explicit_issues = _load_structured_evidence(current_evidence_path)
        explicit_nonpassing = [
            record
            for record in explicit_records
            if str(record.get("status", "")).strip().lower() in {"fail", "blocked"}
        ]
        triggered_recipes.update(
            str(record.get("recipe", "")).strip()
            for record in explicit_nonpassing
            if str(record.get("recipe", "")).strip() in PROOF_RECIPE_REQUIRED_FIELDS
        )
        if explicit_nonpassing and not triggered_recipes:
            triggered_recipes.add("explicit-evidence")
    evidence_sources: tuple[OperationalStatusSource, ...] = ()
    if not triggered_recipes:
        evidence_state = "not-required"
        evidence_summary = "No structured proof recipe is triggered."
    elif item.kind == "epic":
        passing_recipes: set[str] = set()
        evidence_issues: list[str] = []
        evidence_sources_list: list[OperationalStatusSource] = []
        for row, child_requirements, child_implementation in epic_children:
            child_requirements_text = child_requirements.read_text(encoding="utf-8")
            child_implementation_text = child_implementation.read_text(encoding="utf-8")
            child_triggered = _triggered_proof_recipes(
                child_requirements_text, child_implementation_text
            )
            relevant_recipes = triggered_recipes & child_triggered
            if not relevant_recipes:
                continue
            child_issues = _structured_evidence_issues(
                requirements_path=child_requirements,
                implementation_path=child_implementation,
                parent_ac_ids=_extract_ac_ids(_extract_parent_ac_coverage(row)),
                include_explicit_nonpassing=True,
            )
            if child_issues:
                evidence_issues.extend(child_issues)
                continue
            evidence_path = child_implementation.parent / STRUCTURED_EVIDENCE_FILENAME
            records, load_issues = _load_structured_evidence(evidence_path)
            if load_issues:
                evidence_issues.extend(load_issues)
                continue
            passing_recipes.update(
                str(record.get("recipe", "")).strip()
                for record in records
                if str(record.get("status", "")).strip().lower() == "pass"
                and str(record.get("recipe", "")).strip() in relevant_recipes
            )
            evidence_sources_list.append(
                _operational_status_document_source(
                    root, "structured-evidence", evidence_path, fallback
                )
            )
        missing_recipes = triggered_recipes - passing_recipes
        if missing_recipes:
            evidence_issues.append(
                "missing passing child evidence for: " + ", ".join(sorted(missing_recipes))
            )
        if evidence_issues:
            evidence_state = "fail" if item.lifecycle in {"Closeout", "Complete"} else "pending"
            evidence_summary = (
                f"Aggregated child structured evidence has {len(evidence_issues)} issue(s)."
            )
        else:
            evidence_state = "pass"
            evidence_summary = (
                "Every triggered parent proof recipe has valid passing child evidence."
            )
        evidence_sources = tuple(evidence_sources_list)
    else:
        evidence_issues = _structured_evidence_issues(
            requirements_path=requirements_path or Path("missing-requirements"),
            implementation_path=implementation_path or Path("missing-implementation"),
            parent_ac_ids=(
                set(_operational_string_tuple_fact(item, "parent_acs"))
                if item.kind == "epic-child"
                else None
            ),
            include_explicit_nonpassing=True,
        )
        if evidence_issues:
            evidence_state = "fail" if item.lifecycle in {"Review", "Complete"} else "pending"
            evidence_summary = f"Structured evidence has {len(evidence_issues)} issue(s)."
        else:
            evidence_state = "pass"
            evidence_summary = "Every triggered structured proof recipe has passing evidence."
    evidence = _operational_proof_layer(
        "structured-evidence",
        evidence_state,
        evidence_summary,
        *(
            evidence_sources
            or (
                _operational_status_document_source(
                    root,
                    "structured-evidence",
                    (
                        implementation_path.parent / STRUCTURED_EVIDENCE_FILENAME
                        if implementation_path is not None
                        else None
                    ),
                    fallback,
                ),
            )
        ),
    )
    return approval, readiness, implementation, qa, acceptance, evidence


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
            f"Backlog schema mismatch. Expected header: '| {expected} |' in {backlog_path}."
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
            _add_issue(
                issues, "error", backlog_path, f"{row_label} is Promoted but lacks Promoted To."
            )
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
    values = _parse_key_value_section(_markdown_section(docs_text, "QA & Code Review"))
    verdict = _qa_verdict_key(values.get("verdict", ""))
    return verdict in {"pass", "changes-requested"} and not _intent_qa_review_issues(docs_text)


def _qa_verdict_key(value: str) -> str:
    return re.sub(r"[\s_]+", "-", value.strip().lower())


def _resolved_changes_requested_issues(docs_text: str, values: Mapping[str, str]) -> list[str]:
    issues: list[str] = []
    if values.get("findings disposition", "").strip().lower() != "resolved":
        issues.append("record `Findings disposition: Resolved`")
    if values.get("affected validation verdict", "").strip().lower() != "pass":
        issues.append("record `Affected validation verdict: Pass`")
    after_undone = (
        values.get(
            "could every ac pass after affected validation while the approved user job remains undone",
            "",
        )
        .strip()
        .lower()
    )
    if after_undone != "no":
        issues.append(
            "record `Could every AC pass after affected validation while the approved user job "
            "remains undone: No`"
        )
    evidence = values.get("affected validation evidence", "")
    if _evidence_value_missing(evidence) or not _section_has_substantive_text(evidence):
        issues.append("record substantive `Affected validation evidence`")
    if values.get("second qa commissioned", "").strip().lower() != "no":
        issues.append("record `Second QA commissioned: No`")
    decision, impact_issues = _validation_impact_from_text(docs_text)
    if impact_issues:
        issues.extend(f"repair Validation Impact: {issue}" for issue in impact_issues)
    elif decision is None:
        issues.append("record one affected Validation Impact decision for the QA findings")
    elif (
        decision["classification"] != "affected"
        or decision["validation_verdict"] != "pass"
        or "qa-review" not in decision["affected_proof_layers"]
    ):
        issues.append(
            "Validation Impact must be affected, include `qa-review`, and record verdict `pass`"
        )
    return issues


def _intent_qa_review_issues(docs_text: str) -> list[str]:
    values = _parse_key_value_section(_markdown_section(docs_text, "QA & Code Review"))
    mode = values.get("intent qa contract", "").strip().lower()
    if not mode:
        return []
    if mode != "adversarial":
        return ["set `Intent QA contract` to `adversarial`"]
    issues: list[str] = []
    verdict = _qa_verdict_key(values.get("verdict", ""))
    resolved_changes = verdict == "changes-requested"
    if verdict not in {"pass", "changes-requested"}:
        issues.append("record `Verdict: Pass` or preserve `Verdict: Changes Requested`")
    intent_verdict = _qa_verdict_key(values.get("intent adversarial verdict", ""))
    if resolved_changes:
        if intent_verdict not in {"fail", "changes-requested"}:
            issues.append(
                "preserve the original failed `Intent adversarial verdict` for Changes Requested"
            )
    elif intent_verdict != "pass":
        issues.append(
            "record `Intent adversarial verdict: Pass` only when the user job is fulfilled"
        )
    undone = (
        values.get("could every ac pass while the approved user job remains undone", "")
        .strip()
        .lower()
    )
    if resolved_changes:
        if undone not in {"yes", "no", "unknown"}:
            issues.append(
                "preserve the original answer to whether every AC could pass while the user job "
                "remained undone"
            )
        issues.extend(_resolved_changes_requested_issues(docs_text, values))
    elif undone != "no":
        issues.append(
            "answer `Could every AC pass while the approved user job remains undone: No`; "
            "a Yes or unknown answer requires Changes requested"
        )
    if values.get("intent audit state", "").strip().lower() != "current":
        issues.append("record `Intent audit state: current`")
    for field in ("outcome journey evidence", "reviewer independence"):
        value = values.get(field, "")
        if _evidence_value_missing(value) or not _section_has_substantive_text(value):
            issues.append(f"record substantive `{field}`")
    independence = values.get("reviewer independence", "").lower()
    if any(phrase in independence for phrase in ("same implementation agent", "self review")):
        issues.append(
            "reviewer independence cannot be satisfied by implementation self-certification"
        )
    return issues


def _parent_ac_evidence_present(docs_text: str, ac_id: str) -> bool:
    evidence_section = _markdown_section(docs_text, "Parent AC Evidence")
    if not evidence_section or ac_id not in _extract_ac_ids(evidence_section):
        return False
    matching_lines = [
        line for line in evidence_section.splitlines() if ac_id in _extract_ac_ids(line)
    ]
    if not matching_lines:
        return False
    blocked_terms = ("blocked", "fail", "pending", "missing", "unproven", "____")
    return all(not any(term in line.lower() for term in blocked_terms) for line in matching_lines)


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
    user_outcome_sections = (
        "Goal",
        "Requirements (Outcome-Focused)",
        "Acceptance Criteria (Verifiable)",
        "Acceptance Criteria",
        "Validation",
        "Parent AC Evidence",
    )
    user_outcome_authority = "\n".join(
        _markdown_section(text, heading) for text in texts for heading in user_outcome_sections
    ).lower()
    if "user-outcome-journey" in triggered and "user-outcome-journey" not in user_outcome_authority:
        triggered.remove("user-outcome-journey")
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


def _user_outcome_journey_record_issues(
    record: dict[str, object], *, label: str, evidence_dir: Path
) -> list[str]:
    issues: list[str] = []
    for field in ("material_operations", "outcome_observations"):
        value = record.get(field)
        if (
            not isinstance(value, list)
            or not value
            or any(_evidence_value_missing(item) for item in value)
        ):
            issues.append(
                f"structured evidence: {label} `{field}` must be a non-empty list of "
                "performed or observed journey facts."
            )
    policy = record.get("invalid_substitute_policy")
    policy_values = (
        {str(value).strip().lower() for value in policy if str(value).strip()}
        if isinstance(policy, list)
        else set()
    )
    missing_policy = sorted(USER_OUTCOME_INVALID_SUBSTITUTE_POLICY - policy_values)
    if missing_policy:
        issues.append(
            f"structured evidence: {label} invalid_substitute_policy is missing: "
            + ", ".join(missing_policy)
            + "."
        )
    claim_scope = str(record.get("claim_scope", "")).strip()
    journey_scope = str(record.get("journey_scope", "")).strip()
    if claim_scope != journey_scope:
        issues.append(f"structured evidence: {label} journey_scope must exactly match claim_scope.")
    source_value = record.get("source_artifact")
    if (
        isinstance(source_value, str)
        and source_value.strip()
        and not re.match(r"^[a-z][a-z0-9+.-]*://", source_value.strip(), flags=re.IGNORECASE)
    ):
        source_path = Path(source_value.strip())
        candidates = [evidence_dir / source_path]
        repository_root = next(
            (parent for parent in evidence_dir.parents if (parent / ".project-workflow").is_dir()),
            None,
        )
        if repository_root is not None:
            candidates.append(repository_root / source_path)
        resolved_source = next((path for path in candidates if path.exists()), None)
        if resolved_source is None:
            issues.append(
                f"structured evidence: {label} source_artifact does not exist: {source_value}."
            )
        else:
            actual_source_hash = _sha256_file(resolved_source)
            evidence_source_hash = actual_source_hash
            source_member = str(record.get("source_artifact_member", "")).strip()
            if source_member:
                try:
                    with zipfile.ZipFile(resolved_source) as archive:
                        evidence_source_hash = (
                            "sha256:" + hashlib.sha256(archive.read(source_member)).hexdigest()
                        )
                except (KeyError, zipfile.BadZipFile):
                    issues.append(
                        f"structured evidence: {label} source_artifact_member does not exist "
                        f"in a readable ZIP artifact: {source_member}."
                    )
            recorded_commit = str(record.get("commit", "")).strip()
            if (
                not source_member
                and repository_root is not None
                and re.fullmatch(r"[a-fA-F0-9]{7,40}", recorded_commit)
            ):
                try:
                    current_commit = _run_git(["rev-parse", "HEAD"], cwd=repository_root)
                    evidence_commit = _run_git(
                        ["rev-parse", f"{recorded_commit}^{{commit}}"],
                        cwd=repository_root,
                    )
                    relative_source = resolved_source.resolve().relative_to(
                        repository_root.resolve()
                    )
                    ancestor = subprocess.run(
                        [
                            "git",
                            "merge-base",
                            "--is-ancestor",
                            evidence_commit,
                            current_commit,
                        ],
                        cwd=str(repository_root),
                        check=False,
                        capture_output=True,
                    )
                    if evidence_commit != current_commit and ancestor.returncode == 0:
                        historical = subprocess.run(
                            [
                                "git",
                                "show",
                                f"{evidence_commit}:{relative_source.as_posix()}",
                            ],
                            cwd=str(repository_root),
                            check=False,
                            capture_output=True,
                        )
                        if historical.returncode == 0:
                            evidence_source_hash = (
                                "sha256:" + hashlib.sha256(historical.stdout).hexdigest()
                            )
                except (subprocess.CalledProcessError, ValueError):
                    pass
            source_revision = _normalized_evidence_hash(record.get("source_revision"))
            if source_revision.startswith("sha256:") and source_revision != evidence_source_hash:
                issues.append(
                    f"structured evidence: {label} source_revision is stale "
                    f"(expected {evidence_source_hash})."
                )
            artifact_identity = str(record.get("artifact_identity", ""))
            if evidence_source_hash.removeprefix("sha256:") not in artifact_identity:
                issues.append(
                    f"structured evidence: {label} artifact_identity does not bind the recorded "
                    "source artifact."
                )
    entry_point = str(record.get("normal_entry_point", "")).lower()
    if any(term in entry_point for term in ("debug", "test-only", "internal-only")):
        issues.append(
            f"structured evidence: {label} normal_entry_point cannot be a debug, test-only, "
            "or internal-only path."
        )
    acceptance_required = record.get("owner_acceptance_required")
    acceptance_status = str(record.get("owner_acceptance_status", "")).strip().lower()
    if not isinstance(acceptance_required, bool):
        issues.append(f"structured evidence: {label} owner_acceptance_required must be boolean.")
    elif acceptance_required and acceptance_status not in {"pending", "accepted"}:
        issues.append(
            f"structured evidence: {label} owner_acceptance_status must be pending or accepted "
            "when owner acceptance is required."
        )
    elif not acceptance_required and acceptance_status != "not-required":
        issues.append(
            f"structured evidence: {label} owner_acceptance_status must be not-required when "
            "owner acceptance is not required."
        )
    return issues


def _owner_acceptance_completion_issues(evidence_path: Path) -> list[str]:
    records, load_issues = _load_structured_evidence(evidence_path)
    if load_issues:
        return []
    issues: list[str] = []
    for record in records:
        if record.get("recipe") != "user-outcome-journey":
            continue
        if (
            record.get("owner_acceptance_required") is True
            and str(record.get("owner_acceptance_status", "")).strip().lower() != "accepted"
        ):
            label = str(record.get("id", "")).strip() or "user-outcome claim"
            issues.append(
                f"structured evidence: {label} is outcome-proven and ready for owner acceptance, "
                "but owner acceptance is still pending."
            )
    return issues


def _structured_evidence_issues(
    *,
    requirements_path: Path,
    implementation_path: Path,
    parent_ac_ids: set[str] | None = None,
    include_explicit_nonpassing: bool = False,
) -> list[str]:
    requirements_text = (
        requirements_path.read_text(encoding="utf-8") if requirements_path.exists() else ""
    )
    implementation_text = (
        implementation_path.read_text(encoding="utf-8") if implementation_path.exists() else ""
    )
    triggered_recipes = _triggered_proof_recipes(requirements_text, implementation_text)
    evidence_path = implementation_path.parent / STRUCTURED_EVIDENCE_FILENAME
    if include_explicit_nonpassing and evidence_path.exists():
        explicit_records, explicit_load_issues = _load_structured_evidence(evidence_path)
        if explicit_load_issues:
            return [f"structured evidence: {issue}" for issue in explicit_load_issues]
        explicit_nonpassing = [
            record
            for record in explicit_records
            if str(record.get("status", "")).strip().lower() in {"fail", "blocked"}
        ]
        triggered_recipes.update(
            str(record.get("recipe", "")).strip()
            for record in explicit_nonpassing
            if str(record.get("recipe", "")).strip() in PROOF_RECIPE_REQUIRED_FIELDS
        )
        if explicit_nonpassing and not triggered_recipes:
            triggered_recipes.add("explicit-evidence")
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
            value_missing = _evidence_value_missing(record.get(field))
            if (
                recipe_id == "user-outcome-journey"
                and field == "owner_acceptance_status"
                and str(record.get(field, "")).strip().lower()
                in {"pending", "accepted", "not-required"}
            ):
                value_missing = False
            if value_missing:
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
        passing_claim = str(record.get("status", "")).strip().lower() == "pass"
        if invalid_values and passing_claim:
            issues.append(
                f"structured evidence: {label} records invalid substitute evidence: "
                + ", ".join(invalid_values)
            )
        text_blob = " ".join(
            str(value).lower()
            for key, value in record.items()
            if key != "invalid_substitute_policy"
        )
        for invalid_pattern in PROOF_RECIPE_INVALID_SUBSTITUTE_PATTERNS[recipe_id]:
            if not passing_claim:
                continue
            if invalid_pattern in text_blob:
                issues.append(
                    f"structured evidence: {label} uses invalid substitute for "
                    f"`{recipe_id}`: {invalid_pattern}."
                )
        if recipe_id == "user-outcome-journey":
            issues.extend(
                _user_outcome_journey_record_issues(
                    record, label=label, evidence_dir=implementation_path.parent
                )
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
        if passing_claim:
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
        proof_owner_map = _epic_contract_proof_owner_map(contract_path.read_text(encoding="utf-8"))
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
                include_explicit_nonpassing=True,
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


class ValidationImpactDecision(TypedDict, total=False):
    classification: str
    affected_proof_layers: tuple[str, ...]
    required_validation: str
    validation_verdict: str
    decision_identity: str


def _validation_impact_decision(
    *,
    classification: str,
    proof_layers: tuple[str, ...],
    validation_verdict: str,
) -> ValidationImpactDecision:
    if classification not in VALIDATION_IMPACT_CLASSIFICATIONS:
        raise ValueError(f"Unknown validation-impact classification: {classification}")
    if validation_verdict not in VALIDATION_IMPACT_VERDICTS:
        raise ValueError(f"Unknown validation-impact verdict: {validation_verdict}")
    invalid_layers = sorted(set(proof_layers) - set(OPERATIONAL_STATUS_PROOF_LAYER_NAMES))
    if invalid_layers:
        raise ValueError("Unknown proof layer(s): " + ", ".join(invalid_layers))
    if classification == "affected" and not proof_layers:
        raise ValueError("affected impact requires at least one invalidated proof layer")
    if classification == "unaffected":
        if proof_layers:
            raise ValueError("unaffected impact cannot name an invalidated proof layer")
        if validation_verdict != "not-required":
            raise ValueError("unaffected impact requires validation verdict not-required")
    elif classification == "ambiguous":
        if validation_verdict != "pending":
            raise ValueError("ambiguous impact must remain pending until clarified")
    elif validation_verdict == "not-required":
        raise ValueError(
            f"{classification} impact requires a pending, pass, or fail validation verdict"
        )
    affected_layers = tuple(dict.fromkeys(proof_layers))
    required_validation = VALIDATION_IMPACT_REQUIREMENTS[classification]
    return {
        "classification": classification,
        "affected_proof_layers": affected_layers,
        "required_validation": required_validation,
        "validation_verdict": validation_verdict,
    }


def _validation_impact_from_text(
    docs_text: str,
) -> tuple[ValidationImpactDecision | None, tuple[str, ...]]:
    section = _markdown_section(docs_text, "Validation Impact")
    if not section:
        return None, ()
    values = _parse_key_value_section(section)
    required_fields = (
        "baseline proof",
        "change summary",
        "impact",
        "invalidated proof layers",
        "required validation",
        "validation verdict",
        "decided by",
        "change identity",
    )
    missing = tuple(
        field
        for field in required_fields
        if not values.get(field, "").strip() or values.get(field, "").strip() == "____"
    )
    if missing:
        return None, tuple(f"record `{field}`" for field in missing)
    classification = values["impact"].strip().lower()
    validation_verdict = values["validation verdict"].strip().lower()
    layer_value = values["invalidated proof layers"].strip()
    proof_layers = (
        ()
        if layer_value.lower() == "none"
        else tuple(part.strip() for part in layer_value.split(",") if part.strip())
    )
    try:
        decision = _validation_impact_decision(
            classification=classification,
            proof_layers=proof_layers,
            validation_verdict=validation_verdict,
        )
    except ValueError as exc:
        return None, (str(exc),)
    issues: list[str] = []
    if values["required validation"].strip().lower() != decision["required_validation"]:
        issues.append("required validation contradicts the change classification")
    expected_identity = _validation_impact_identity(
        baseline=values["baseline proof"],
        change_summary=values["change summary"],
        decided_by=values["decided by"],
        decision=decision,
    )
    if values["change identity"].strip().lower() != expected_identity:
        issues.append("change identity does not match the recorded impact decision")
    decision["decision_identity"] = expected_identity
    return (decision if not issues else None), tuple(issues)


def _validation_impact_identity(
    *,
    baseline: str,
    change_summary: str,
    decided_by: str,
    decision: ValidationImpactDecision,
) -> str:
    payload = {
        "baseline_proof": baseline.strip(),
        "change_summary": change_summary.strip(),
        "decided_by": decided_by.strip(),
        "classification": decision["classification"],
        "affected_proof_layers": list(decision["affected_proof_layers"]),
        "required_validation": decision["required_validation"],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return VALIDATION_IMPACT_IDENTITY_PREFIX + hashlib.sha256(encoded).hexdigest()


def _validation_impact_section(
    *,
    baseline: str,
    change_summary: str,
    decided_by: str,
    decision: ValidationImpactDecision,
) -> str:
    layers = decision["affected_proof_layers"]
    rendered_layers = ", ".join(str(layer) for layer in layers) if layers else "None"
    decision_identity = _validation_impact_identity(
        baseline=baseline,
        change_summary=change_summary,
        decided_by=decided_by,
        decision=decision,
    )
    return (
        "## Validation Impact\n\n"
        f"- Baseline proof: {baseline.strip()}\n"
        f"- Change summary: {change_summary.strip()}\n"
        f"- Impact: {decision['classification']}\n"
        f"- Invalidated proof layers: {rendered_layers}\n"
        f"- Required validation: {decision['required_validation']}\n"
        f"- Validation verdict: {decision['validation_verdict']}\n"
        f"- Decided by: {decided_by.strip()}\n"
        f"- Change identity: {decision_identity}\n"
    )


def _upsert_markdown_section(
    text: str,
    *,
    heading: str,
    section: str,
    before_heading: str | None = None,
) -> str:
    lines = text.splitlines(keepends=True)
    target = f"## {heading}".lower()
    start: int | None = None
    end: int | None = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.lower() == target:
            start = index
            continue
        if start is not None and index > start and stripped.startswith("## "):
            end = index
            break
    replacement = section.rstrip() + "\n\n"
    if start is not None:
        section_end = len(lines) if end is None else end
        return "".join(lines[:start]) + replacement + "".join(lines[section_end:])
    if before_heading is not None:
        before_target = f"## {before_heading}".lower()
        for index, line in enumerate(lines):
            if line.strip().lower() == before_target:
                return "".join(lines[:index]) + replacement + "".join(lines[index:])
    return text.rstrip() + "\n\n" + replacement


def _approval_envelope_issues(
    requirements_text: str,
    *,
    require_decomposition: bool = False,
    require_implementation: bool = False,
) -> list[str]:
    section = _markdown_section(requirements_text, OWNER_APPROVAL_HEADING)
    if not section:
        return ["owner input required: add `## Owner Approval` with an approved scope envelope."]

    values = _parse_key_value_section(section)
    issues: list[str] = []

    if _intent_contract_mode(requirements_text) == "full" and not _approval_value_is_yes(
        values.get("intent reviewed and accurately reflected", "")
    ):
        issues.append(
            "owner input required: the plain-language Intent has not been confirmed as accurate."
        )
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
        issues.append(
            "owner input required: implementation is outside the approved scope envelope."
        )
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
    intent_reviewed: str,
) -> str:
    return (
        "## Owner Approval\n\n"
        f"- Intent reviewed and accurately reflected: {intent_reviewed}\n"
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
        intent_reviewed=(
            "Yes"
            if _intent_contract_mode(without_approval) == "full"
            else "Not required (legacy contract)"
        ),
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
        lines.append(
            "- Next action: resolve the listed gaps or record approved deferrals with follow-up work."
        )
    elif complete_requested:
        lines.append("- Next action: global epic row can be marked Complete.")
    else:
        lines.append(
            "- Next action: rerun closeout with --complete to mark the global epic row Complete."
        )
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
    task_id: str,
    title: str,
    parent_ac_coverage: str,
    child_charter: str = "",
    *,
    root: Path | None = None,
) -> str:
    parent_ac_value = parent_ac_coverage or "____"
    repository_id = _template_repository_id(root)
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
        f"## Repository Evidence\n\n"
        f"| Repository | Branch / PR | Validation | Delivery | Evidence |\n"
        f"| ---------- | ----------- | ---------- | -------- | -------- |\n"
        f"| {repository_id} | not recorded | not recorded | not recorded | not recorded |\n\n"
        f"## Task List\n\n"
        f"| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |\n"
        f"| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |\n"
        f"| 1 | ____ | ____ | AC1 / parent AC(s) {parent_ac_value}: ____ | ____ | To Do | | ____ | No | bounded-return |\n\n"
        f"## Parent AC Evidence\n\n"
        f"- {parent_ac_value}: Pending implementation evidence. Recipe-triggered claims must "
        f"also be backed by `{STRUCTURED_EVIDENCE_FILENAME}`.\n\n"
        f"## QA & Code Review\n\n"
        f"- Intent QA contract: adversarial\n"
        f"- Verdict: ____\n"
        f"- Intent adversarial verdict: ____\n"
        f"- Could every AC pass while the approved user job remains undone: ____\n"
        f"- Intent audit state: ____\n"
        f"- Outcome journey evidence: ____\n"
        f"- Reviewer independence: ____\n"
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
    return (
        json.dumps(
            {
                "task_id": task_id,
                "claims": [],
            },
            indent=2,
        )
        + "\n"
    )


def _epic_child_requirements_template(
    task_id: str,
    title: str,
    parent_ac_coverage: str,
    child_charter: str = "",
    *,
    root: Path | None = None,
) -> str:
    parent_ac_value = parent_ac_coverage or "____"
    repository_id = _template_repository_id(root)
    return (
        f"# Requirements\n\n"
        f"## Summary\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n"
        f"- Parent AC Coverage: {parent_ac_value}\n"
        f"- Last updated: {date.today().isoformat()}\n"
        f"- Intent contract: full\n\n"
        f"## Intent\n\n"
        f"State the child outcome in one or two plain-language sentences without narrowing the parent Intent.\n\n"
        f"## Intent Spine\n\n"
        f"- OC1 — Completion capability: ____\n"
        f"- OC2 — Material capabilities: ____\n"
        f"- OC3 — Success journey: ____\n"
        f"- OC4 — Successful-but-wrong result: ____\n"
        f"- OC5 — Exclusions: ____\n"
        f"- OC6 — Assumptions: ____\n"
        f"- OC7 — Authority source: Parent Epic Intent and approved decomposition row.\n\n"
        f"## Owner Approval\n\n"
        f"- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged\n"
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
        f"## Repository Scope\n\n"
        f"- Primary repository: {repository_id}\n"
        f"- Repositories touched: {repository_id}\n\n"
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
    table_columns: tuple[str, ...] | None = None
    for idx, line in enumerate(lines):
        cells = _parse_markdown_table_cells(line)
        if cells == list(DELEGATION_EXECUTION_NEEDS_TASK_COLUMNS):
            header_idx = idx
            table_columns = DELEGATION_EXECUTION_NEEDS_TASK_COLUMNS
            break
        if cells == list(DELEGATION_IMPLEMENTATION_TASK_COLUMNS):
            header_idx = idx
            table_columns = DELEGATION_IMPLEMENTATION_TASK_COLUMNS
            break
        if cells == list(IMPLEMENTATION_TASK_COLUMNS):
            header_idx = idx
            table_columns = IMPLEMENTATION_TASK_COLUMNS
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
        assert table_columns is not None
        if len(cells) != len(table_columns):
            malformed_rows.append(row_idx + 1)
            row_idx += 1
            continue
        row = dict(zip(table_columns, cells))
        row["_delegation_metadata"] = (
            "present"
            if table_columns
            in (
                DELEGATION_IMPLEMENTATION_TASK_COLUMNS,
                DELEGATION_EXECUTION_NEEDS_TASK_COLUMNS,
            )
            else "legacy"
        )
        row["_execution_needs_metadata"] = (
            "present" if table_columns == DELEGATION_EXECUTION_NEEDS_TASK_COLUMNS else "legacy"
        )
        row["_line_idx"] = str(row_idx + 1)
        rows.append(row)
        row_idx += 1

    return True, rows, malformed_rows


def _task_testing_integrity_issues(docs_text: str) -> tuple[str, ...]:
    """Return integrity issues that ordinary force is never allowed to bypass."""
    lines = docs_text.splitlines()
    task_list_headings = [idx for idx, line in enumerate(lines) if line.strip() == "## Task List"]
    if len(task_list_headings) != 1:
        return ("Task IMPLEMENTATION.md must contain exactly one canonical ## Task List section.",)

    section_start = task_list_headings[0] + 1
    section_end = len(lines)
    for idx in range(section_start, len(lines)):
        if lines[idx].startswith("## "):
            section_end = idx
            break
    section_lines = lines[section_start:section_end]
    supported_headers = [
        idx
        for idx, line in enumerate(section_lines)
        if _parse_markdown_table_cells(line)
        in (
            list(DELEGATION_EXECUTION_NEEDS_TASK_COLUMNS),
            list(DELEGATION_IMPLEMENTATION_TASK_COLUMNS),
            list(IMPLEMENTATION_TASK_COLUMNS),
        )
    ]
    if len(supported_headers) != 1:
        return ("Canonical Task List must contain exactly one supported implementation table.",)

    table_text = "\n".join(section_lines[supported_headers[0] :])
    table_found, rows, malformed_rows = _implementation_task_table_rows(table_text)
    if not table_found:
        return ("Task IMPLEMENTATION.md has no supported Task List table.",)
    if malformed_rows:
        return (
            "Task List has malformed rows at lines: "
            + ", ".join(str(line) for line in malformed_rows)
            + ".",
        )
    if not rows:
        return ("Task List must contain at least one required implementation row.",)

    first_non_table = supported_headers[0] + 2 + len(rows) + len(malformed_rows)
    trailing_table_lines = [
        section_start + idx + 1
        for idx, line in enumerate(section_lines[first_non_table:], start=first_non_table)
        if _parse_markdown_table_cells(line) is not None
    ]
    if trailing_table_lines:
        return (
            "Canonical Task List contains unexpected trailing or duplicate table rows at lines: "
            + ", ".join(str(line) for line in trailing_table_lines)
            + ".",
        )
    incomplete = tuple(
        row.get("ID", "row").strip() or "row"
        for row in rows
        if row.get("Status", "").strip() != "Done"
    )
    if incomplete:
        return (
            "Task cannot move to Testing until every required implementation row is Done; "
            "incomplete: " + ", ".join(incomplete) + ". Ordinary --force cannot bypass "
            "this integrity gate.",
        )
    return ()


def _has_qa_review_evidence(
    text: str,
    *,
    requirements_text: str | None = None,
) -> bool:
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


def _doctor_issue_metadata(path: Path | str, message: str) -> tuple[str, str, bool]:
    path_text = str(path).replace("\\", "/").lower()
    message_text = message.lower()

    if "local workflow cli differs" in message_text or (
        "source " in message_text
        and ("mirror differs" in message_text or "does not match" in message_text)
    ):
        return "PW_GENERATED_ASSET_DRIFT", "project-workflow", True
    if "generated project-workflow update is pending" in message_text:
        return "PW_GENERATED_UPDATE_PENDING", "owner", False
    if "approval" in message_text or "approved" in message_text:
        return "PW_APPROVAL_REQUIRED", "owner", False
    if "evidence" in message_text:
        return "PW_EVIDENCE_REQUIRED", "owner", False
    if "deferral" in message_text:
        return "PW_DEFERRAL_INVALID", "owner", False
    if "owner input" in message_text or "owner decision" in message_text:
        return "PW_OWNER_DECISION_REQUIRED", "owner", False
    if "duplicate" in message_text and "id" in message_text:
        return "PW_DUPLICATE_ID", "agent", False
    if "decomposition" in message_text:
        return "PW_DECOMPOSITION_INVALID", "agent", False
    if "epic-contract.md" in path_text or "epic contract" in message_text:
        return "PW_EPIC_CONTRACT_INVALID", "agent", False
    if path_text.endswith("/.project-workflow/config.json") or "namespace config" in message_text:
        return "PW_CONFIG_INVALID", "agent", False
    if "backlog.md" in path_text or "backlog" in message_text:
        return "PW_BACKLOG_INVALID", "agent", False
    if "/fix-" in path_text or message_text.startswith("fix-"):
        return "PW_FIX_INVALID", "agent", False
    if "tracker.md" in path_text or "tracker" in message_text:
        return "PW_TRACKER_INVALID", "agent", False
    if "/tasks/" in path_text:
        return "PW_TASK_DOCUMENT_INVALID", "agent", False
    return "PW_WORKFLOW_INVALID", "agent", False


def _add_issue(
    issues: list[DoctorIssue],
    severity: str,
    path: Path | str,
    message: str,
    *,
    code: str | None = None,
    remediation_owner: str | None = None,
    mechanically_upgradeable: bool | None = None,
) -> None:
    inferred_code, inferred_owner, inferred_mechanical = _doctor_issue_metadata(path, message)
    issues.append(
        DoctorIssue(
            code=code or inferred_code,
            severity=severity,
            path=str(path),
            message=message,
            remediation_owner=remediation_owner or inferred_owner,
            mechanically_upgradeable=(
                inferred_mechanical
                if mechanically_upgradeable is None
                else mechanically_upgradeable
            ),
        )
    )


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
            f"Global tracker schema mismatch. Expected header: '| {expected} |' in {tracker_path}."
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

INTENT_CONTRACT_MODES = {"full", "compact"}

INTENT_SPINE_FIELDS = {
    "OC1": "completion capability",
    "OC2": "material capabilities",
    "OC3": "success journey",
    "OC4": "successful-but-wrong result",
    "OC5": "exclusions",
    "OC6": "assumptions",
    "OC7": "authority source",
}

GENERIC_INTENTS = {
    "build the feature",
    "complete this task",
    "deliver the requested outcome",
    "do the work",
    "finish the epic",
    "fix the bug",
    "follow the workflow",
    "implement the requirements",
}


def _intent_contract_mode(requirements_text: str) -> str | None:
    summary = _parse_key_value_section(_markdown_section(requirements_text, "Summary"))
    mode = summary.get("intent contract", "").strip().lower()
    return mode or None


def _intent_plain_text(requirements_text: str) -> str:
    return " ".join(
        line.strip()
        for line in _markdown_section(requirements_text, "Intent").splitlines()
        if line.strip()
    )


def _normalized_intent_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _intent_sentence_count(value: str) -> int:
    return len(re.findall(r"[.!?](?=\s|$)", value.strip()))


def _intent_spine_records(requirements_text: str) -> list[tuple[str, str, str]]:
    records: list[tuple[str, str, str]] = []
    for logical_item, _first_line in _flat_markdown_bullet_records(
        _markdown_section(requirements_text, "Intent Spine")
    ):
        match = re.match(r"^(OC\d+)\s*[—-]\s*([^:]+):\s*(.+)$", logical_item)
        if not match:
            continue
        records.append((match.group(1), match.group(2).strip(), match.group(3).strip()))
    return records


def _intent_spine_values(requirements_text: str) -> dict[str, tuple[str, str]]:
    return {
        commitment_id: (label, value)
        for commitment_id, label, value in _intent_spine_records(requirements_text)
    }


def _intent_contract_issues(requirements_text: str) -> list[str]:
    mode = _intent_contract_mode(requirements_text)
    if mode is None:
        return []
    if mode not in INTENT_CONTRACT_MODES:
        return ["set `Intent contract` to `full` or `compact`"]

    issues: list[str] = []
    intent = _intent_plain_text(requirements_text)
    if not intent:
        issues.append("add `## Intent` with the owner's desired outcome")
    elif _section_has_placeholder(intent):
        issues.append("replace placeholder content under `## Intent`")
    else:
        normalized = _normalized_intent_text(intent)
        summary = _parse_key_value_section(_markdown_section(requirements_text, "Summary"))
        title = _normalized_intent_text(summary.get("title", ""))
        if normalized in GENERIC_INTENTS or normalized in {title, f"deliver {title}"}:
            issues.append(
                "replace procedural or circular `## Intent` text with the owner's actual outcome"
            )
        if len(re.findall(r"\b[\w'-]+\b", intent)) < 8:
            issues.append("make `## Intent` substantive enough to identify the desired outcome")
        sentence_count = _intent_sentence_count(intent)
        if sentence_count not in {1, 2}:
            issues.append("keep `## Intent` to one or two complete plain-language sentences")

    if mode == "compact":
        return issues

    spine_section = _markdown_section(requirements_text, "Intent Spine")
    if not spine_section:
        issues.append("add `## Intent Spine` with stable OC1-OC7 commitments")
        return issues
    spine_values = _intent_spine_values(requirements_text)
    spine_ids = [record[0] for record in _intent_spine_records(requirements_text)]
    duplicate_ids = sorted(
        commitment_id for commitment_id in set(spine_ids) if spine_ids.count(commitment_id) > 1
    )
    if duplicate_ids:
        issues.append("remove duplicate Intent Spine commitment IDs: " + ", ".join(duplicate_ids))
    for commitment_id, expected_label in INTENT_SPINE_FIELDS.items():
        parsed = spine_values.get(commitment_id)
        if parsed is None:
            issues.append(f"add `{commitment_id} — {expected_label.title()}` to `## Intent Spine`")
            continue
        label, value = parsed
        if _normalized_intent_text(label) != _normalized_intent_text(expected_label):
            issues.append(f"label {commitment_id} as `{expected_label}` in `## Intent Spine`")
        if not value or _section_has_placeholder(value):
            issues.append(f"replace placeholder content for {commitment_id} in `## Intent Spine`")
    return issues


def _format_intent_approval_summary(requirements_text: str) -> str:
    issues = _intent_contract_issues(requirements_text)
    if _intent_contract_mode(requirements_text) != "full":
        issues = [
            "add the current full Intent contract before requesting meaning-first approval",
            *issues,
        ]
    if issues:
        raise ValueError("; ".join(dict.fromkeys(issues)))

    intent = _intent_plain_text(requirements_text)
    spine = _intent_spine_values(requirements_text)

    def value(commitment_id: str) -> str:
        return spine[commitment_id][1]

    return (
        "Approval synopsis\n\n"
        "Intent\n"
        f"{intent}\n\n"
        "At completion\n"
        f"{value('OC1')}\n\n"
        "Material capabilities\n"
        f"{value('OC2')}\n\n"
        "Proof journey\n"
        f"{value('OC3')}\n\n"
        "A green result that would still be wrong\n"
        f"{value('OC4')}\n\n"
        "Still outside this work\n"
        f"{value('OC5')}\n\n"
        "Material assumptions\n"
        f"{value('OC6')}\n\n"
        "Approval question\n"
        "Does this Intent accurately capture what you want and what success means?\n\n"
        "Provenance note\n"
        "The workflow records artifact identity after approval, but IDs and hashes are not the "
        "meaning being approved.\n"
    )


INTENT_AUDIT_CLASSIFICATIONS = {
    "preserved",
    "narrowed",
    "proxy",
    "omitted",
    "broadened",
    "amended",
    "deferred",
    "unknown",
}

INTENT_AUDIT_DRIFT_CLASSIFICATIONS = {"narrowed", "proxy", "omitted", "broadened"}

INTENT_AUDIT_VERDICTS = {"pass", "changes-requested", "review-required"}


def _intent_audit_path(epic_dir: Path) -> Path:
    return epic_dir / INTENT_AUDIT_FILENAME


def _intent_audit_source_paths(epic_dir: Path) -> list[Path]:
    paths = [
        epic_dir / "REQUIREMENTS.md",
        epic_dir / EPIC_CONTRACT_FILENAME,
        epic_dir / DECOMPOSITION_PLAN_FILENAME,
        epic_dir / EPIC_AMENDMENTS_FILENAME,
    ]
    for child_dir in sorted(path for path in epic_dir.iterdir() if path.is_dir()):
        paths.extend((child_dir / "REQUIREMENTS.md", child_dir / "IMPLEMENTATION.md"))
    return sorted((path for path in paths if path.exists()), key=lambda path: path.as_posix())


def _intent_audit_source_identity(epic_dir: Path) -> str:
    records = []
    for path in _intent_audit_source_paths(epic_dir):
        records.append(
            {
                "path": path.relative_to(epic_dir).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return APPROVAL_IDENTITY_PREFIX + hashlib.sha256(encoded).hexdigest()


def _intent_audit_template(epic_dir: Path) -> str:
    requirements_path = epic_dir / "REQUIREMENTS.md"
    requirements_text = (
        requirements_path.read_text(encoding="utf-8") if requirements_path.exists() else ""
    )
    commitments = []
    for commitment_id, label, value in _intent_spine_records(requirements_text):
        commitments.append(
            {
                "id": commitment_id,
                "classification": "unknown",
                "disposition": "active",
                "material": commitment_id in {"OC1", "OC2", "OC3", "OC4"},
                "parent_acs": [],
                "child_owners": [],
                "required_outcome_proof": "",
                "source_locations": [f"REQUIREMENTS.md#intent-spine-{commitment_id.lower()}"],
                "target_locations": [],
                "user_visible_consequence": value,
                "lost_capability": "",
                "amendment": None,
            }
        )
    payload = {
        "schema_version": INTENT_AUDIT_SCHEMA_VERSION,
        "artifact_identity": _intent_audit_source_identity(epic_dir),
        "reviewed_by": "",
        "reviewed_at": "",
        "review_source": "",
        "verdict": "review-required",
        "commitments": commitments,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _load_intent_audit(epic_dir: Path) -> tuple[dict[str, object] | None, list[str]]:
    audit_path = _intent_audit_path(epic_dir)
    if not audit_path.exists():
        return None, [f"{INTENT_AUDIT_FILENAME} is missing"]
    try:
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"{INTENT_AUDIT_FILENAME} is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return None, [f"{INTENT_AUDIT_FILENAME} must contain a JSON object"]
    return payload, []


def _intent_audit_location_issues(
    epic_dir: Path, value: object, *, field: str, commitment_id: str
) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{commitment_id} must record non-empty `{field}`"]
    issues: list[str] = []
    for location in value:
        if not isinstance(location, str) or not location.strip():
            issues.append(f"{commitment_id} `{field}` contains an invalid location")
            continue
        path_part = location.split("#", 1)[0]
        location_path = Path(path_part)
        if location_path.is_absolute() or ".." in location_path.parts:
            issues.append(f"{commitment_id} `{field}` must use repository-relative locations")
        elif not (epic_dir / location_path).exists():
            issues.append(f"{commitment_id} `{field}` location does not exist: {location}")
    return issues


def _intent_audit_amendment_issues(
    amendment: object, *, commitment_id: str, lost_capability: str
) -> list[str]:
    if not isinstance(amendment, dict):
        capability_detail = (
            f"; lost or added capability: {lost_capability.strip()}"
            if lost_capability.strip()
            else ""
        )
        return [
            f"{commitment_id} material drift requires an owner-approved amendment identifying "
            "the lost or added capability" + capability_detail
        ]
    issues: list[str] = []
    required = ("approved_by", "decision_date", "source", "capability_change")
    for field in required:
        value = amendment.get(field)
        if not isinstance(value, str) or _approval_source_invalid(value):
            issues.append(f"{commitment_id} amendment must record substantive `{field}`")
    decision_date = amendment.get("decision_date")
    if isinstance(decision_date, str) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", decision_date):
        issues.append(f"{commitment_id} amendment `decision_date` must use YYYY-MM-DD")
    approved_by = amendment.get("approved_by")
    if isinstance(approved_by, str) and "agent" in approved_by.lower():
        issues.append(f"{commitment_id} amendment must name the approving owner, not an agent")
    if not lost_capability.strip() and amendment.get("capability_change", "").strip() == "":
        issues.append(f"{commitment_id} amendment must plainly identify the capability change")
    return issues


def _intent_audit_evaluation(epic_dir: Path) -> dict[str, object]:
    current_identity = _intent_audit_source_identity(epic_dir)
    payload, load_issues = _load_intent_audit(epic_dir)
    if payload is None:
        return {
            "schema_version": INTENT_AUDIT_SCHEMA_VERSION,
            "state": "unknown",
            "current_identity": current_identity,
            "audit_identity": None,
            "verdict": "review-required",
            "issues": load_issues,
            "commitments": [],
        }

    issues: list[str] = []
    if payload.get("schema_version") != INTENT_AUDIT_SCHEMA_VERSION:
        issues.append(f"schema_version must be {INTENT_AUDIT_SCHEMA_VERSION}")
    audit_identity = payload.get("artifact_identity")
    if not isinstance(audit_identity, str) or not audit_identity.startswith(
        APPROVAL_IDENTITY_PREFIX
    ):
        issues.append("artifact_identity must be a sha256 identity")
    for field in ("reviewed_by", "reviewed_at", "review_source"):
        value = payload.get(field)
        if not isinstance(value, str) or _approval_source_invalid(value):
            issues.append(f"record substantive `{field}`")
    reviewed_at = payload.get("reviewed_at")
    if (
        isinstance(reviewed_at, str)
        and reviewed_at
        and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", reviewed_at)
    ):
        issues.append("reviewed_at must use YYYY-MM-DD")
    verdict = payload.get("verdict")
    if verdict not in INTENT_AUDIT_VERDICTS:
        issues.append("verdict must be pass, changes-requested, or review-required")

    requirements_text = (epic_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    expected_ids = set(_intent_spine_values(requirements_text))
    parent_ac_ids = _extract_parent_ac_ids_from_requirements(requirements_text)
    tracker_path = epic_dir / "TRACKER.md"
    child_rows = {
        row.get("ID", ""): row
        for row in (_epic_tracker_rows(tracker_path)[2] if tracker_path.exists() else [])
    }
    child_ids = set(child_rows)
    commitments = payload.get("commitments")
    normalized_commitments: list[dict[str, object]] = []
    if not isinstance(commitments, list):
        issues.append("commitments must be a JSON array")
        commitments = []
    seen_ids: list[str] = []
    unresolved_drift: list[str] = []
    unknown_ids: list[str] = []
    for raw in commitments:
        if not isinstance(raw, dict):
            issues.append("each commitment audit record must be a JSON object")
            continue
        record = dict(raw)
        commitment_id = str(record.get("id", "")).strip()
        seen_ids.append(commitment_id)
        classification = record.get("classification")
        disposition = record.get("disposition")
        material = record.get("material")
        if classification not in INTENT_AUDIT_CLASSIFICATIONS:
            issues.append(f"{commitment_id or 'commitment'} has invalid classification")
        if disposition not in {"active", "amended", "deferred"}:
            issues.append(
                f"{commitment_id or 'commitment'} disposition must be active, amended, or deferred"
            )
        if not isinstance(material, bool):
            issues.append(f"{commitment_id or 'commitment'} must record boolean `material`")
        parent_acs = record.get("parent_acs")
        if not isinstance(parent_acs, list) or not parent_acs:
            issues.append(f"{commitment_id or 'commitment'} must map one or more parent ACs")
        else:
            invalid_acs = sorted(
                str(ac_id) for ac_id in parent_acs if str(ac_id) not in parent_ac_ids
            )
            if invalid_acs:
                issues.append(f"{commitment_id} maps unknown parent ACs: {', '.join(invalid_acs)}")
        child_owners = record.get("child_owners")
        if not isinstance(child_owners, list) or not child_owners:
            issues.append(f"{commitment_id or 'commitment'} must map one or more child owners")
        else:
            invalid_children = sorted(
                str(child_id) for child_id in child_owners if str(child_id) not in child_ids
            )
            if invalid_children:
                issues.append(
                    f"{commitment_id} maps unknown child owners: {', '.join(invalid_children)}"
                )
            if isinstance(parent_acs, list):
                uncovered_owners = sorted(
                    str(child_id)
                    for child_id in child_owners
                    if str(child_id) in child_rows
                    and not (
                        _extract_ac_ids(_extract_parent_ac_coverage(child_rows[str(child_id)]))
                        & {str(ac_id) for ac_id in parent_acs}
                    )
                )
                if uncovered_owners:
                    issues.append(
                        f"{commitment_id} child owners lack matching mapped parent ACs: "
                        + ", ".join(uncovered_owners)
                    )
        for field in ("required_outcome_proof", "user_visible_consequence"):
            value = record.get(field)
            if not isinstance(value, str) or not _section_has_substantive_text(value):
                issues.append(f"{commitment_id or 'commitment'} must record substantive `{field}`")
        issues.extend(
            _intent_audit_location_issues(
                epic_dir,
                record.get("source_locations"),
                field="source_locations",
                commitment_id=commitment_id or "commitment",
            )
        )
        issues.extend(
            _intent_audit_location_issues(
                epic_dir,
                record.get("target_locations"),
                field="target_locations",
                commitment_id=commitment_id or "commitment",
            )
        )
        lost_capability = record.get("lost_capability", "")
        if not isinstance(lost_capability, str):
            issues.append(f"{commitment_id or 'commitment'} `lost_capability` must be text")
            lost_capability = ""
        if classification == "unknown":
            unknown_ids.append(commitment_id)
        if material is True and classification in INTENT_AUDIT_DRIFT_CLASSIFICATIONS:
            amendment_issues = _intent_audit_amendment_issues(
                record.get("amendment"),
                commitment_id=commitment_id,
                lost_capability=lost_capability,
            )
            if amendment_issues:
                unresolved_drift.append(commitment_id)
                issues.extend(amendment_issues)
                if not lost_capability.strip():
                    issues.append(
                        f"{commitment_id} must name the lost or added user-visible capability"
                    )
            elif disposition not in {"amended", "deferred"}:
                unresolved_drift.append(commitment_id)
                issues.append(
                    f"{commitment_id} authorized material drift requires disposition "
                    "`amended` or `deferred`"
                )
        if classification in {"amended", "deferred"}:
            expected_disposition = classification
            if disposition != expected_disposition:
                issues.append(
                    f"{commitment_id} classification `{classification}` requires disposition "
                    f"`{expected_disposition}`"
                )
            issues.extend(
                _intent_audit_amendment_issues(
                    record.get("amendment"),
                    commitment_id=commitment_id,
                    lost_capability=lost_capability,
                )
            )
        normalized_commitments.append(record)

    duplicate_ids = sorted(
        commitment_id for commitment_id in set(seen_ids) if seen_ids.count(commitment_id) > 1
    )
    if duplicate_ids:
        issues.append("duplicate commitment records: " + ", ".join(duplicate_ids))
    missing_ids = sorted(expected_ids - set(seen_ids))
    extra_ids = sorted(set(seen_ids) - expected_ids)
    if missing_ids:
        issues.append("missing commitment coverage: " + ", ".join(missing_ids))
    if extra_ids:
        issues.append("unknown commitment coverage: " + ", ".join(extra_ids))

    if audit_identity != current_identity:
        state = "stale"
    elif unresolved_drift or verdict == "changes-requested":
        state = "changes-requested"
    elif issues or unknown_ids or verdict != "pass":
        state = "review-required"
    else:
        state = "current"
    return {
        "schema_version": INTENT_AUDIT_SCHEMA_VERSION,
        "state": state,
        "current_identity": current_identity,
        "audit_identity": audit_identity,
        "verdict": verdict,
        "reviewed_by": payload.get("reviewed_by"),
        "reviewed_at": payload.get("reviewed_at"),
        "review_source": payload.get("review_source"),
        "issues": list(dict.fromkeys(issues)),
        "unresolved_drift": unresolved_drift,
        "commitments": normalized_commitments,
    }


def _intent_audit_gate_issues(epic_dir: Path) -> list[str]:
    requirements_path = epic_dir / "REQUIREMENTS.md"
    if not requirements_path.exists():
        return [f"missing epic requirements file: {requirements_path}"]
    requirements_text = requirements_path.read_text(encoding="utf-8")
    if _intent_contract_mode(requirements_text) != "full":
        return []
    evaluation = _intent_audit_evaluation(epic_dir)
    if evaluation["state"] == "current":
        return []
    raw_details = evaluation.get("issues", [])
    details = raw_details if isinstance(raw_details, list) else []
    detail = f" ({'; '.join(str(issue) for issue in details[:3])})" if details else ""
    return [
        f"intent audit is {evaluation['state']}{detail}; review `{INTENT_AUDIT_FILENAME}` "
        "against the current requirements, decomposition and child plans"
    ]


def _format_intent_audit_human(epic_id: str, evaluation: dict[str, object]) -> str:
    lines = [
        "Intent audit",
        f"Epic: {epic_id}",
        f"State: {evaluation['state']}",
        f"Verdict: {evaluation.get('verdict') or 'review-required'}",
        f"Reviewed by: {evaluation.get('reviewed_by') or 'not recorded'}",
        f"Audit identity: {evaluation.get('audit_identity') or 'not recorded'}",
        f"Current identity: {evaluation['current_identity']}",
        "Commitments:",
    ]
    raw_commitments = evaluation.get("commitments", [])
    commitments = raw_commitments if isinstance(raw_commitments, list) else []
    for record in commitments:
        if not isinstance(record, dict):
            continue
        lines.append(
            f"- {record.get('id', 'unknown')}: {record.get('classification', 'unknown')}; "
            f"disposition={record.get('disposition', 'unknown')}; "
            f"material={'yes' if record.get('material') is True else 'no'}; "
            f"owners={','.join(str(value) for value in record.get('child_owners', [])) or 'none'}; "
            f"consequence={record.get('user_visible_consequence') or 'not recorded'}"
        )
    raw_issues = evaluation.get("issues", [])
    issues = raw_issues if isinstance(raw_issues, list) else []
    if issues:
        lines.append("Findings:")
        lines.extend(f"- {issue}" for issue in issues)
    next_actions = {
        "current": "Proceed inside the audited Intent envelope.",
        "stale": "Refresh the audit against the current source identity.",
        "unknown": f"Create and review `{INTENT_AUDIT_FILENAME}`.",
        "review-required": "Complete the sourced commitment coverage and semantic review.",
        "changes-requested": "Restore the capability or record a current owner-approved amendment.",
    }
    lines.append(f"Next action: {next_actions[str(evaluation['state'])]}")
    return "\n".join(lines)


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
    issues = [
        f"owner input required: {issue}." for issue in _intent_contract_issues(requirements_text)
    ]
    for heading in READINESS_REQUIRED_SECTIONS:
        section = _markdown_section(requirements_text, heading)
        if not section:
            issues.append(f"owner input required: add `## {heading}` to REQUIREMENTS.md.")
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

    if not _extract_ac_ids(
        _markdown_section(requirements_text, "Acceptance Criteria (Verifiable)")
    ):
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
        issues.append("owner input required: add stable parent AC IDs before epic decomposition.")
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
    issues = _task_readiness_issues(
        requirements_text=requirements_text,
        implementation_text=implementation_text,
        parent_ac_ids=parent_ac_ids,
    )
    root = next(
        (parent for parent in requirements_path.parents if (parent / ".project-workflow").is_dir()),
        None,
    )
    if root is not None:
        issues.extend(_repository_scope_issues(root, requirements_text))
    epic_dir = requirements_path.parent.parent
    if _epic_contract_path(epic_dir).exists():
        issues.extend(
            _legacy_truncated_child_charter_issues(
                epic_dir=epic_dir,
                requirements_text=requirements_text,
                implementation_text=implementation_text,
            )
        )
    return issues


def _repository_scope_values(requirements_text: str) -> tuple[str | None, tuple[str, ...]]:
    section = _markdown_section(requirements_text, "Repository Scope")
    primary_match = re.search(
        r"(?im)^\s*-\s*Primary repository:\s*(.+?)\s*$",
        section,
    )
    touched_match = re.search(
        r"(?im)^\s*-\s*Repositories touched:\s*(.+?)\s*$",
        section,
    )
    primary = primary_match.group(1).strip().strip("`") if primary_match else None
    touched = (
        tuple(
            value.strip().strip("`") for value in touched_match.group(1).split(",") if value.strip()
        )
        if touched_match
        else ()
    )
    if primary is None and not touched:
        fix_plan = _fix_values(requirements_text, "Fix Plan")
        fix_primary = fix_plan.get("primary repo")
        fix_touched = fix_plan.get("repos touched", "")
        primary = fix_primary.strip().strip("`") if fix_primary else None
        touched = tuple(
            value.strip().strip("`") for value in _split_fix_repos(fix_touched) if value.strip()
        )
    return primary, touched


def _repository_scope_issues(root: Path, requirements_text: str) -> list[str]:
    config = _load_workflow_config(root)
    if config.workspace is None:
        return []
    registered = {repository.repository_id for repository in config.workspace.repositories}
    primary, touched = _repository_scope_values(requirements_text)
    issues: list[str] = []
    if primary is None or primary in {"____", "not recorded"}:
        issues.append(
            "agent action required: record `Primary repository` in the Repository Scope section."
        )
    elif primary not in registered:
        issues.append(
            f"agent action required: primary repository `{primary}` is not registered in "
            ".project-workflow/config.json."
        )
    if not touched or any(value in {"____", "not recorded"} for value in touched):
        issues.append(
            "agent action required: record `Repositories touched` in the Repository Scope section."
        )
    else:
        duplicates = sorted(value for value in set(touched) if touched.count(value) > 1)
        if duplicates:
            issues.append(
                "agent action required: remove duplicate repository scope entries: "
                + ", ".join(duplicates)
                + "."
            )
        unknown = sorted(set(touched) - registered)
        if unknown:
            issues.append(
                "agent action required: repository scope contains unregistered repositories: "
                + ", ".join(unknown)
                + "."
            )
        if primary is not None and primary not in touched:
            issues.append(
                f"agent action required: primary repository `{primary}` must also appear in "
                "`Repositories touched`."
            )
    return issues


def _repository_evidence_rows(implementation_text: str) -> dict[str, dict[str, str]]:
    section = _markdown_section(implementation_text, "Repository Evidence")
    rows: dict[str, dict[str, str]] = {}
    for line in section.splitlines():
        cells = _parse_markdown_table_cells(line)
        if cells is None or len(cells) != 5:
            continue
        if cells[0] in {"Repository", "----------"} or set(cells[0]) <= {"-", ":"}:
            continue
        rows[cells[0].strip("`")] = {
            "branch_pr": cells[1],
            "validation": cells[2],
            "delivery": cells[3],
            "evidence": cells[4],
        }
    return rows


def _repository_evidence_duplicate_ids(implementation_text: str) -> set[str]:
    section = _markdown_section(implementation_text, "Repository Evidence")
    repository_ids: list[str] = []
    for line in section.splitlines():
        cells = _parse_markdown_table_cells(line)
        if cells is None or len(cells) != 5:
            continue
        if cells[0] in {"Repository", "----------"} or set(cells[0]) <= {"-", ":"}:
            continue
        repository_ids.append(cells[0].strip("`"))
    return {
        repository_id
        for repository_id in set(repository_ids)
        if repository_ids.count(repository_id) > 1
    }


def _repository_evidence_issues(
    root: Path,
    requirements_text: str,
    implementation_text: str,
) -> list[str]:
    config = _load_workflow_config(root)
    if config.workspace is None:
        return []
    _primary, touched = _repository_scope_values(requirements_text)
    rows = _repository_evidence_rows(implementation_text)
    issues: list[str] = []
    duplicates = sorted(_repository_evidence_duplicate_ids(implementation_text))
    if duplicates:
        issues.append(
            "agent action required: remove duplicate Repository Evidence rows for: "
            + ", ".join(duplicates)
            + "."
        )
    registered = {repository.repository_id for repository in config.workspace.repositories}
    unknown = sorted(set(rows) - registered)
    if unknown:
        issues.append(
            "agent action required: Repository Evidence contains unregistered repositories: "
            + ", ".join(unknown)
            + "."
        )
    out_of_scope = sorted(set(rows) - set(touched))
    if out_of_scope:
        issues.append(
            "agent action required: Repository Evidence contains repositories outside the "
            "recorded scope: " + ", ".join(out_of_scope) + "."
        )
    missing = sorted(set(touched) - set(rows))
    if missing:
        issues.append(
            "agent action required: add Repository Evidence rows for: " + ", ".join(missing) + "."
        )
    universal_placeholders = {"", "____"}
    proof_placeholders = {*universal_placeholders, "not recorded"}
    for repository_id in sorted(set(touched) & set(rows)):
        missing_fields = [
            field.replace("_", " / " if field == "branch_pr" else " ")
            for field, value in rows[repository_id].items()
            if value.strip().lower()
            in (
                proof_placeholders
                if field in {"validation", "evidence"}
                else universal_placeholders
            )
        ]
        if missing_fields:
            issues.append(
                f"agent action required: repository `{repository_id}` must record "
                + ", ".join(missing_fields)
                + " evidence."
            )
    return issues


def _resolve_fix_doc(*, root: Path, tracker_path: Path, fix_id: str) -> tuple[Path, dict[str, str]]:
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
    config = _load_workflow_config(root)
    if config.workspace is not None:
        targets: set[str] = set()
        for repository in config.workspace.repositories:
            targets.add(repository.repository_id)
            targets.add(repository.path)
        return targets

    # Compatibility only: older installations may still have the pre-registry
    # workspace.json metadata used by Fix triage.
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
    issues = _intent_contract_issues(fix_text)
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


def _fix_closeout_issues(root: Path, fix_text: str) -> list[str]:
    issues = _repository_evidence_issues(root, fix_text, fix_text)
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
    if _extract_workflow_ref_ids(
        originating_work, config=_load_workflow_config(root)
    ) and original_result.strip().lower() in {"not applicable", "n/a", "none"}:
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
    if outcome.get("disposition") == "Promoted" and _fix_value_missing(outcome.get("promoted to")):
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
        if new_status == "Review":
            repository_issues = _repository_evidence_issues(root, fix_text, fix_text)
            if repository_issues:
                raise SystemExit(_format_readiness_block(fix_id, repository_issues))
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


def _epic_tracker_header_columns(cells: list[str] | None) -> tuple[str, ...] | None:
    if cells == list(EPIC_TRACKER_COLUMNS):
        return EPIC_TRACKER_COLUMNS
    if cells == list(LEGACY_EPIC_TRACKER_COLUMNS):
        return LEGACY_EPIC_TRACKER_COLUMNS
    return None


def _epic_tracker_rows(epic_tracker_path: Path) -> tuple[list[str], int, list[dict[str, str]]]:
    lines = epic_tracker_path.read_text(encoding="utf-8").splitlines(keepends=True)
    header_idx: int | None = None
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
        tuple(format_columns_value.split("\x1f")) if format_columns_value else EPIC_TRACKER_COLUMNS
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
                f"Row {row_id} must be '{expected_from}' before this operation; found '{current}'."
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

        bullet: str | None = None
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
    match_re = re.compile(rf"^{re.escape(EPIC_ID_PREFIX)}-([A-Za-z0-9]+)-{re.escape(suffix)}$")

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
