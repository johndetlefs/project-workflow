from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli


def status_source(kind: str = "global-tracker") -> workflow_cli.OperationalStatusSource:
    artifact = (
        ".project-workflow/TRACKER.md"
        if kind == "global-tracker"
        else ".project-workflow/tasks/EPIC-001/TRACKER.md"
    )
    return workflow_cli.OperationalStatusSource(kind, artifact)


def installation(state: str = "current") -> workflow_cli.OperationalStatusValue:
    return workflow_cli.OperationalStatusValue(
        "installation",
        state,
        f"Installation is {state}.",
        (workflow_cli.OperationalStatusSource("repository-compatibility", ".project-workflow"),),
    )


def layers(**overrides: str) -> tuple[workflow_cli.OperationalStatusProofLayer, ...]:
    states = {
        "requirements-approval": "pass",
        "readiness": "pass",
        "implementation": "pass",
        "qa-review": "pass",
        "parent-acceptance": "not-required",
        "structured-evidence": "not-required",
    }
    states.update(overrides)
    return tuple(
        workflow_cli.OperationalStatusProofLayer(
            name,
            states[name],
            f"{name} is {states[name]}.",
            (status_source(),),
        )
        for name in workflow_cli.OPERATIONAL_STATUS_PROOF_LAYER_NAMES
    )


def item(
    item_id: str,
    *,
    kind: str = "task",
    lifecycle: str = "Ready",
    proof_layers: tuple[workflow_cli.OperationalStatusProofLayer, ...] | None = None,
    owner_epic: str | None = None,
    delivery: workflow_cli.OperationalStatusValue | None = None,
) -> workflow_cli.OperationalStatusWorkItem:
    source_kind = "epic-tracker" if kind == "epic-child" else "global-tracker"
    facts: tuple[workflow_cli.OperationalStatusFact, ...] = ()
    if owner_epic is not None:
        facts = (workflow_cli.OperationalStatusFact("owner_epic", owner_epic),)
    return workflow_cli.OperationalStatusWorkItem(
        item_id,
        f"Title for {item_id}",
        kind,
        lifecycle,
        f"{lifecycle} fixture.",
        (status_source(source_kind),),
        facts,
        layers() if proof_layers is None else proof_layers,
        delivery,
    )


def resolve(
    root: Path,
    work_items: tuple[workflow_cli.OperationalStatusWorkItem, ...] = (),
    *,
    installation_state: str = "current",
    findings: tuple[workflow_cli.OperationalStatusFinding, ...] = (),
    focus_id: str | None = None,
) -> tuple[workflow_cli.OperationalStatusAction, tuple[workflow_cli.OperationalStatusAction, ...]]:
    return workflow_cli.resolve_operational_actions(
        root,
        installation=installation(installation_state),
        work_items=work_items,
        findings=findings,
        focus_id=focus_id,
    )


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(path for path in root.rglob("*") if path.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def test_precedence_contract_is_explicit_and_installation_blocker_wins(
    tmp_path: Path,
) -> None:
    assert workflow_cli.OPERATIONAL_STATUS_ACTION_PRECEDENCE == (
        "installation-safety",
        "blocking-current-finding",
        "owner-decision",
        "missing-workflow-gate",
        "lifecycle-progress",
        "delivery-follow-up",
        "backlog-selection",
        "no-action",
    )
    blocker = workflow_cli.OperationalStatusFinding(
        "PW_STATUS_FIXTURE_BLOCKER",
        "error",
        "Fixture blocker.",
        (status_source(),),
    )

    primary, secondary = resolve(
        tmp_path,
        (item("TASK-001"),),
        installation_state="upgradeable",
        findings=(blocker,),
    )

    assert primary.code == "PW_STATUS_UPGRADE_REQUIRED"
    assert primary.command == workflow_cli.CANONICAL_UPGRADE_COMMAND
    assert [action.code for action in secondary] == [
        "PW_STATUS_REPAIR_BLOCKER",
        "PW_STATUS_START_TASK",
    ]


@pytest.mark.parametrize(
    ("state", "code", "party", "has_command"),
    [
        ("upgradeable", "PW_STATUS_UPGRADE_REQUIRED", "agent", True),
        ("legacy-unversioned", "PW_STATUS_UPGRADE_REQUIRED", "agent", True),
        ("not-initialized", "PW_STATUS_INIT_REQUIRED", "agent", True),
        ("helper-limited", "PW_STATUS_HELPER_UPGRADE_REQUIRED", "agent", True),
        ("unsupported-future", "PW_STATUS_UNSUPPORTED_FUTURE", "owner", False),
        ("invalid", "PW_STATUS_INSTALLATION_INVALID", "owner", False),
        ("unknown", "PW_STATUS_INSTALLATION_INVALID", "owner", False),
    ],
)
def test_installation_states_use_exact_commands_or_explicit_requests(
    tmp_path: Path,
    state: str,
    code: str,
    party: str,
    has_command: bool,
) -> None:
    primary, _ = resolve(tmp_path, installation_state=state)

    assert primary.code == code
    assert primary.responsible_party == party
    assert (primary.command is not None) is has_command
    assert (primary.request is not None) is (not has_command)


@pytest.mark.parametrize(
    ("work_item", "expected_code", "command_fragment"),
    [
        (item("TASK-001", lifecycle="To Do"), "PW_STATUS_ANALYSE_TASK", "--to 'Analysing'"),
        (item("TASK-001", lifecycle="Ready"), "PW_STATUS_START_TASK", "--to 'In Progress'"),
        (item("TASK-001", lifecycle="In Progress"), "PW_STATUS_TEST_TASK", "--to 'Testing'"),
        (item("TASK-001", lifecycle="Testing"), "PW_STATUS_REVIEW_TASK", "--to 'Review'"),
        (item("TASK-001", lifecycle="Review"), "PW_STATUS_COMPLETE_TASK", "--to 'Complete'"),
        (item("FIX-001", kind="fix", lifecycle="To Do"), "PW_STATUS_TRIAGE_FIX", "fix triage"),
        (
            item("FIX-001", kind="fix", lifecycle="Ready"),
            "PW_STATUS_START_FIX",
            "--to 'In Progress'",
        ),
        (
            item("FIX-001", kind="fix", lifecycle="In Progress"),
            "PW_STATUS_TEST_FIX",
            "--to 'Testing'",
        ),
        (item("FIX-001", kind="fix", lifecycle="Testing"), "PW_STATUS_REVIEW_FIX", "--to 'Review'"),
        (
            item("EPIC-001", kind="epic", lifecycle="Analysing"),
            "PW_STATUS_READY_EPIC",
            "--to 'Ready'",
        ),
        (
            item("EPIC-001", kind="epic", lifecycle="Ready"),
            "PW_STATUS_START_EPIC",
            "--to 'In Progress'",
        ),
        (
            item("EPIC-001", kind="epic", lifecycle="Closeout"),
            "PW_STATUS_COMPLETE_EPIC",
            "epic closeout",
        ),
        (
            item("TASK-002", kind="epic-child", lifecycle="Proposed", owner_epic="EPIC-001"),
            "PW_STATUS_APPROVE_EPIC_CHILD",
            "epic approve",
        ),
        (
            item("TASK-002", kind="epic-child", lifecycle="Approved", owner_epic="EPIC-001"),
            "PW_STATUS_SCAFFOLD_EPIC_CHILD",
            "epic scaffold-child",
        ),
        (
            item("TASK-002", kind="epic-child", lifecycle="In Progress", owner_epic="EPIC-001"),
            "PW_STATUS_TEST_EPIC_CHILD",
            "--to Testing",
        ),
        (
            item("TASK-002", kind="epic-child", lifecycle="Testing", owner_epic="EPIC-001"),
            "PW_STATUS_REVIEW_EPIC_CHILD",
            "--to Review",
        ),
        (
            item("TASK-002", kind="epic-child", lifecycle="Review", owner_epic="EPIC-001"),
            "PW_STATUS_COMPLETE_EPIC_CHILD",
            "--to Complete",
        ),
    ],
)
def test_each_supported_lifecycle_uses_existing_transition_command(
    tmp_path: Path,
    work_item: workflow_cli.OperationalStatusWorkItem,
    expected_code: str,
    command_fragment: str,
) -> None:
    primary, _ = resolve(tmp_path, (work_item,))

    assert primary.code == expected_code
    assert primary.responsible_party == "agent"
    assert primary.command is not None
    assert command_fragment in primary.command


@pytest.mark.parametrize(
    ("overrides", "expected_code", "expected_party"),
    [
        ({"requirements-approval": "pending"}, "PW_STATUS_REQUIREMENTS_APPROVAL_REQUIRED", "owner"),
        ({"readiness": "fail"}, "PW_STATUS_READINESS_REQUIRED", "agent"),
        ({"implementation": "pending"}, "PW_STATUS_IMPLEMENTATION_REQUIRED", "agent"),
        ({"qa-review": "not-recorded"}, "PW_STATUS_QA_REQUIRED", "agent"),
        ({"parent-acceptance": "pending"}, "PW_STATUS_PARENT_ACCEPTANCE_REQUIRED", "agent"),
        (
            {"structured-evidence": "pending"},
            "PW_STATUS_STRUCTURED_EVIDENCE_REQUIRED",
            "external-authority",
        ),
    ],
)
def test_earliest_unmet_proof_layer_wins_without_inflation(
    tmp_path: Path,
    overrides: dict[str, str],
    expected_code: str,
    expected_party: str,
) -> None:
    proof = layers(**overrides)
    primary, _ = resolve(
        tmp_path,
        (
            item(
                "TASK-002",
                kind="epic-child",
                lifecycle="Review",
                owner_epic="EPIC-001",
                proof_layers=proof,
            ),
        ),
    )

    assert primary.code == expected_code
    assert primary.responsible_party == expected_party
    assert primary.request is not None


def test_source_order_controls_ties_and_duplicate_actions_are_removed(
    tmp_path: Path,
) -> None:
    later_id_first = item("TASK-020")
    earlier_id_second = item("TASK-010")

    first = resolve(tmp_path, (later_id_first, earlier_id_second, later_id_first))
    second = resolve(tmp_path, (later_id_first, earlier_id_second, later_id_first))

    assert first == second
    assert first[0].title.endswith("TASK-020")
    assert [action.title for action in first[1]] == ["Start task: TASK-010"]


def test_distinct_items_with_same_delivery_request_are_not_deduplicated(
    tmp_path: Path,
) -> None:
    delivery = workflow_cli.OperationalStatusValue(
        "delivery",
        "repository-complete",
        "Repository work is complete.",
        (status_source(),),
    )
    work = (
        item("TASK-001", lifecycle="Complete", delivery=delivery),
        item("TASK-002", lifecycle="Complete", delivery=delivery),
    )

    primary, secondary = resolve(tmp_path, work)

    assert primary.title.endswith("TASK-001")
    assert [action.title for action in secondary] == ["Advance delivery for TASK-002"]


def write_backlog(root: Path, rows: list[str]) -> None:
    workflow_dir = root / ".project-workflow"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "BACKLOG.md").write_text(
        "# Backlog\n\n"
        "| ID | Title | Type | Priority | Status | Outcome | Promoted To | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n" + "".join(f"{row}\n" for row in rows),
        encoding="utf-8",
    )


def test_no_active_work_selects_backlog_by_priority_then_file_order_without_mutation(
    tmp_path: Path,
) -> None:
    write_backlog(
        tmp_path,
        [
            "| BL-001 | First medium | Task Candidate | Medium | Accepted | One |  |  |",
            "| BL-002 | First high | Epic Candidate | High | Proposed | Two |  |  |",
            "| BL-003 | Second high | Task Candidate | High | Accepted | Three |  |  |",
            "| BL-004 | Deferred | Task Candidate | High | Deferred | Four |  |  |",
        ],
    )
    before = tree_hash(tmp_path)

    primary, secondary = resolve(tmp_path)

    assert primary.code == "PW_STATUS_SELECT_BACKLOG_ITEM"
    assert "BL-002" in primary.title
    assert primary.responsible_party == "owner"
    assert secondary == ()
    assert tree_hash(tmp_path) == before


def test_focused_resolution_filters_work_and_reports_missing_focus(tmp_path: Path) -> None:
    work = (item("TASK-001"), item("TASK-002"))

    focused, _ = resolve(tmp_path, work, focus_id="TASK-002")
    missing, _ = resolve(tmp_path, work, focus_id="TASK-999")

    assert focused.title.endswith("TASK-002")
    assert missing.code == "PW_STATUS_FOCUS_NOT_FOUND"


@pytest.mark.parametrize("kind", ["task", "fix", "epic", "epic-child"])
def test_blocked_work_requires_owner_resolution_and_terminal_work_is_not_transitioned(
    tmp_path: Path,
    kind: str,
) -> None:
    item_id = "EPIC-001" if kind == "epic" else ("FIX-001" if kind == "fix" else "TASK-001")
    owner_epic = "EPIC-001" if kind == "epic-child" else None
    blocked, _ = resolve(
        tmp_path,
        (item(item_id, kind=kind, lifecycle="Blocked", owner_epic=owner_epic),),
    )
    terminal, _ = resolve(
        tmp_path,
        (item(item_id, kind=kind, lifecycle="Complete", owner_epic=owner_epic),),
    )

    assert blocked.code == "PW_STATUS_BLOCKER_DECISION_REQUIRED"
    assert blocked.responsible_party == "owner"
    assert blocked.command is None
    assert terminal.code == "PW_STATUS_NO_ACTION"


def test_malformed_backlog_returns_repair_action(tmp_path: Path) -> None:
    workflow_dir = tmp_path / ".project-workflow"
    workflow_dir.mkdir()
    (workflow_dir / "BACKLOG.md").write_text(
        "# Backlog\n\n| Wrong | Header |\n|---|---|\n| BL-001 | Broken |\n",
        encoding="utf-8",
    )

    primary, _ = resolve(tmp_path)

    assert primary.code == "PW_STATUS_BACKLOG_INVALID"
    assert primary.responsible_party == "agent"


def test_accepted_warning_absence_does_not_displace_work_but_visible_error_does(
    tmp_path: Path,
) -> None:
    current_error = workflow_cli.OperationalStatusFinding(
        "PW_TASK_DOCUMENT_INVALID",
        "error",
        "Current task document is invalid.",
        (
            workflow_cli.OperationalStatusSource(
                "doctor",
                ".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",
                "owner agent; mechanical false",
            ),
        ),
    )

    normal, _ = resolve(tmp_path, (item("TASK-001"),))
    blocked, _ = resolve(tmp_path, (item("TASK-001"),), findings=(current_error,))

    assert normal.code == "PW_STATUS_START_TASK"
    assert blocked.code == "PW_STATUS_REPAIR_BLOCKER"
    assert blocked.responsible_party == "agent"


def test_empty_repository_returns_explicit_no_action(tmp_path: Path) -> None:
    primary, secondary = resolve(tmp_path)

    assert primary.code == "PW_STATUS_NO_ACTION"
    assert primary.request is not None
    assert secondary == ()
