from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from project_workflow import cli as workflow_cli


def source(kind: str, artifact: str, detail: str = "") -> workflow_cli.OperationalStatusSource:
    return workflow_cli.OperationalStatusSource(kind, artifact, detail)


def value(
    dimension: str,
    state: str,
    summary: str,
    *sources: workflow_cli.OperationalStatusSource,
) -> workflow_cli.OperationalStatusValue:
    return workflow_cli.OperationalStatusValue(dimension, state, summary, tuple(sources))


def test_operational_status_source_precedence_is_dimension_specific_and_immutable() -> None:
    precedence = dict(workflow_cli.OPERATIONAL_STATUS_SOURCE_PRECEDENCE)

    assert precedence["installation"] == (
        "repository-compatibility",
        "manifest",
        "local-helper",
    )
    assert precedence["work"] == ("epic-tracker", "global-tracker")
    assert precedence["approval"] == ("requirements",)
    assert precedence["integration"] == ("git",)
    assert precedence["delivery"] == (
        "delivery-receipt",
        "structured-evidence",
        "git",
    )
    assert set(workflow_cli.OPERATIONAL_STATUS_SOURCE_KINDS) == {
        source_kind
        for _dimension, source_kinds in workflow_cli.OPERATIONAL_STATUS_SOURCE_PRECEDENCE
        for source_kind in source_kinds
    }

    with pytest.raises(TypeError):
        workflow_cli.OPERATIONAL_STATUS_SOURCE_PRECEDENCE[0] = ("health", ("doctor",))  # type: ignore[index]


def test_operational_status_snapshot_serializes_exact_payload_without_inference() -> None:
    manifest_source = source("manifest", ".project-workflow/manifest.json")
    tracker_source = source("global-tracker", ".project-workflow/TRACKER.md", "EPIC-008")
    requirements_source = source(
        "requirements",
        ".project-workflow/tasks/EPIC-008/REQUIREMENTS.md",
        "owner approval",
    )
    git_source = source("git", ".git", "branch codex/EPIC-008")
    doctor_source = source("doctor", ".project-workflow", "current evaluation")
    work_item = workflow_cli.OperationalStatusWorkItem(
        "EPIC-008",
        "Operational Status And Next Action",
        "epic",
        "Analysing",
        "Requirements are approved and decomposition is active.",
        (tracker_source, requirements_source),
    )
    blocker = workflow_cli.OperationalStatusFinding(
        "PW_STATUS_OWNER_DECISION_REQUIRED",
        "warning",
        "The next child requires an owner decision.",
        (requirements_source,),
    )
    primary_action = workflow_cli.OperationalStatusAction(
        "PW_STATUS_REQUEST_OWNER_DECISION",
        "Confirm the child boundary",
        "owner",
        "Implementation cannot select between two product outcomes.",
        (requirements_source,),
        request="Choose the intended child outcome.",
    )
    secondary_action = workflow_cli.OperationalStatusAction(
        "PW_STATUS_RUN_DOCTOR",
        "Validate workflow state",
        "agent",
        "Workflow artifacts changed.",
        (doctor_source,),
        command="./.project-workflow/cli/workflow doctor",
    )
    snapshot = workflow_cli.OperationalStatusSnapshot(
        "/repo",
        value("installation", "current", "Installed contract is current.", manifest_source),
        value("git", "clean", "Branch is clean.", git_source),
        value("health", "warning", "One current warning is visible.", doctor_source),
        value("proof", "repository-validated", "Repository validation passed.", doctor_source),
        value(
            "delivery",
            "not-recorded",
            "No integration or release receipt is recorded.",
            tracker_source,
        ),
        active_work=(work_item,),
        findings=(blocker,),
        blockers=(blocker,),
        primary_action=primary_action,
        secondary_actions=(secondary_action,),
    )

    assert workflow_cli.operational_status_payload(snapshot) == {
        "schema_version": 1,
        "root": "/repo",
        "installation": {
            "state": "current",
            "summary": "Installed contract is current.",
            "sources": [
                {
                    "kind": "manifest",
                    "artifact": ".project-workflow/manifest.json",
                    "detail": "",
                }
            ],
            "facts": [],
        },
        "git": {
            "state": "clean",
            "summary": "Branch is clean.",
            "sources": [{"kind": "git", "artifact": ".git", "detail": "branch codex/EPIC-008"}],
            "facts": [],
        },
        "health": {
            "state": "warning",
            "summary": "One current warning is visible.",
            "sources": [
                {
                    "kind": "doctor",
                    "artifact": ".project-workflow",
                    "detail": "current evaluation",
                }
            ],
            "facts": [],
        },
        "proof": {
            "state": "repository-validated",
            "summary": "Repository validation passed.",
            "sources": [
                {
                    "kind": "doctor",
                    "artifact": ".project-workflow",
                    "detail": "current evaluation",
                }
            ],
            "facts": [],
        },
        "delivery": {
            "state": "not-recorded",
            "summary": "No integration or release receipt is recorded.",
            "sources": [
                {
                    "kind": "global-tracker",
                    "artifact": ".project-workflow/TRACKER.md",
                    "detail": "EPIC-008",
                }
            ],
            "facts": [],
        },
        "active_work": [
            {
                "id": "EPIC-008",
                "title": "Operational Status And Next Action",
                "kind": "epic",
                "lifecycle": "Analysing",
                "operational_meaning": "Requirements are approved and decomposition is active.",
                "sources": [
                    {
                        "kind": "global-tracker",
                        "artifact": ".project-workflow/TRACKER.md",
                        "detail": "EPIC-008",
                    },
                    {
                        "kind": "requirements",
                        "artifact": ".project-workflow/tasks/EPIC-008/REQUIREMENTS.md",
                        "detail": "owner approval",
                    },
                ],
                "facts": [],
                "proof_layers": [],
                "delivery": None,
            }
        ],
        "findings": [
            {
                "code": "PW_STATUS_OWNER_DECISION_REQUIRED",
                "severity": "warning",
                "message": "The next child requires an owner decision.",
                "sources": [
                    {
                        "kind": "requirements",
                        "artifact": ".project-workflow/tasks/EPIC-008/REQUIREMENTS.md",
                        "detail": "owner approval",
                    }
                ],
            }
        ],
        "blockers": [
            {
                "code": "PW_STATUS_OWNER_DECISION_REQUIRED",
                "severity": "warning",
                "message": "The next child requires an owner decision.",
                "sources": [
                    {
                        "kind": "requirements",
                        "artifact": ".project-workflow/tasks/EPIC-008/REQUIREMENTS.md",
                        "detail": "owner approval",
                    }
                ],
            }
        ],
        "primary_action": {
            "code": "PW_STATUS_REQUEST_OWNER_DECISION",
            "title": "Confirm the child boundary",
            "responsible_party": "owner",
            "reason": "Implementation cannot select between two product outcomes.",
            "command": None,
            "request": "Choose the intended child outcome.",
            "sources": [
                {
                    "kind": "requirements",
                    "artifact": ".project-workflow/tasks/EPIC-008/REQUIREMENTS.md",
                    "detail": "owner approval",
                }
            ],
        },
        "secondary_actions": [
            {
                "code": "PW_STATUS_RUN_DOCTOR",
                "title": "Validate workflow state",
                "responsible_party": "agent",
                "reason": "Workflow artifacts changed.",
                "command": "./.project-workflow/cli/workflow doctor",
                "request": None,
                "sources": [
                    {
                        "kind": "doctor",
                        "artifact": ".project-workflow",
                        "detail": "current evaluation",
                    }
                ],
            }
        ],
    }


def test_operational_status_keeps_proof_and_delivery_independent() -> None:
    tracker_source = source("global-tracker", ".project-workflow/TRACKER.md")
    proof = value(
        "proof",
        "repository-validated",
        "Implementation and repository validation are recorded.",
        tracker_source,
    )
    delivery = value(
        "delivery",
        "not-recorded",
        "No integration or later delivery source is recorded.",
        tracker_source,
    )

    assert proof.state == "repository-validated"
    assert delivery.state == "not-recorded"
    assert delivery.state not in {"integrated", "released", "published", "deployed"}


@pytest.mark.parametrize(
    "factory, message",
    [
        (
            lambda: workflow_cli.OperationalStatusSource("unknown-source", "artifact"),
            "Unknown operational status source kind",
        ),
        (
            lambda: workflow_cli.OperationalStatusFact("Invalid Key", "value"),
            "Invalid operational status fact key",
        ),
        (
            lambda: workflow_cli.OperationalStatusFact("valid_key", 1.5),
            "fact values must be text, integer, boolean",
        ),
        (
            lambda: value("proof", "published", "Invalid cross-dimension state."),
            "Unknown operational status proof state",
        ),
        (
            lambda: workflow_cli.OperationalStatusWorkItem(
                "TASK-001", "Task", "unknown-kind", "Ready", "Ready to begin.", (source("global-tracker", "tracker"),)
            ),
            "Unknown operational status work item kind",
        ),
        (
            lambda: workflow_cli.OperationalStatusFinding(
                "bad-code", "warning", "Contradiction.", (source("doctor", "doctor"),)
            ),
            "Invalid operational status finding code",
        ),
        (
            lambda: workflow_cli.OperationalStatusAction(
                "PW_STATUS_INVALID",
                "Invalid",
                "agent",
                "Both fields are set.",
                (source("doctor", "doctor"),),
                command="project doctor",
                request="Run Doctor.",
            ),
            "exactly one non-empty command or request",
        ),
        (
            lambda: workflow_cli.OperationalStatusAction(
                "PW_STATUS_INVALID",
                "Invalid",
                "project-workflow",
                "Responsibility is invalid.",
                (source("doctor", "doctor"),),
                command="project doctor",
            ),
            "Unknown operational status responsible party",
        ),
        (
            lambda: workflow_cli.OperationalStatusAction(
                "PW_STATUS_INVALID",
                "Invalid",
                "agent",
                "An empty command is not an action.",
                (source("doctor", "doctor"),),
                command="  ",
            ),
            "command must be non-empty text or None",
        ),
    ],
)
def test_operational_status_model_rejects_invalid_values(factory: object, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        factory()  # type: ignore[operator]


def test_operational_status_records_are_frozen_and_preserve_source_order() -> None:
    tracker_source = source("epic-tracker", ".project-workflow/tasks/EPIC-008/TRACKER.md")
    global_source = source("global-tracker", ".project-workflow/TRACKER.md")
    work_item = workflow_cli.OperationalStatusWorkItem(
        "TASK-049",
        "Define Operational Status Read Model And Source Precedence",
        "epic-child",
        "In Progress",
        "The foundational contract is being implemented.",
        (tracker_source, global_source),
    )
    finding = workflow_cli.OperationalStatusFinding(
        "PW_STATUS_CONTRADICTORY_WORK_ITEM",
        "error",
        "The Epic and global trackers disagree about work-item ownership.",
        (tracker_source, global_source),
    )

    assert [entry["kind"] for entry in workflow_cli._operational_status_work_item_payload(work_item)["sources"]] == [
        "epic-tracker",
        "global-tracker",
    ]
    assert [entry["kind"] for entry in workflow_cli._operational_status_finding_payload(finding)["sources"]] == [
        "epic-tracker",
        "global-tracker",
    ]
    with pytest.raises(FrozenInstanceError):
        work_item.lifecycle = "Complete"  # type: ignore[misc]
