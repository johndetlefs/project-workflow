from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli


def source() -> workflow_cli.OperationalStatusSource:
    return workflow_cli.OperationalStatusSource(
        "global-tracker", ".project-workflow/TRACKER.md"
    )


def fact(key: str, value: object) -> workflow_cli.OperationalStatusFact:
    return workflow_cli.OperationalStatusFact(key, value)  # type: ignore[arg-type]


def work_item(
    *,
    lifecycle: str = "Complete",
    kind: str = "task",
    item_facts: tuple[workflow_cli.OperationalStatusFact, ...] = (),
) -> workflow_cli.OperationalStatusWorkItem:
    return workflow_cli.OperationalStatusWorkItem(
        "TASK-001",
        "Classified work",
        kind,
        lifecycle,
        "Fixture lifecycle meaning.",
        (source(),),
        item_facts,
    )


def proof_layers(
    **states: str,
) -> tuple[workflow_cli.OperationalStatusProofLayer, ...]:
    defaults = {
        "requirements-approval": "pass",
        "readiness": "pass",
        "implementation": "pass",
        "qa-review": "pass",
        "parent-acceptance": "not-required",
        "structured-evidence": "pass",
    }
    defaults.update(states)
    return tuple(
        workflow_cli.OperationalStatusProofLayer(
            name,
            defaults[name],
            f"{name} fixture.",
            (source(),),
        )
        for name in workflow_cli.OPERATIONAL_STATUS_PROOF_LAYER_NAMES
    )


def run_git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def init_git(root: Path) -> None:
    run_git(root, "init", "-b", "main")
    run_git(root, "config", "user.email", "classification@example.com")
    run_git(root, "config", "user.name", "Classification Tests")
    (root / "README.md").write_text("fixture\n", encoding="utf-8")
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "fixture")


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(path for path in root.rglob("*") if path.is_file()):
        if ".git" in path.relative_to(root).parts:
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


@pytest.mark.parametrize("kind", ["task", "fix", "epic", "epic-child"])
def test_every_work_item_kind_exposes_six_ordered_sourced_proof_layers(
    tmp_path: Path,
    kind: str,
) -> None:
    layers = workflow_cli._operational_item_proof_layers(
        tmp_path,
        work_item(kind=kind, lifecycle="In Progress"),
    )

    assert tuple(layer.name for layer in layers) == (
        workflow_cli.OPERATIONAL_STATUS_PROOF_LAYER_NAMES
    )
    assert all(layer.sources for layer in layers)


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"requirements-approval": "pending"}, "declared"),
        ({"readiness": "pending"}, "approved"),
        ({"implementation": "pending"}, "ready"),
        ({"qa-review": "pending"}, "implementation-recorded"),
        ({"parent-acceptance": "pending"}, "implementation-recorded"),
        ({"structured-evidence": "pending"}, "repository-validated"),
        ({"structured-evidence": "not-required"}, "repository-validated"),
        ({}, "recorded-evidence"),
    ],
)
def test_aggregate_proof_stops_at_each_missing_prerequisite(
    overrides: dict[str, str],
    expected: str,
) -> None:
    assert workflow_cli._operational_aggregate_proof_state(
        proof_layers(**overrides)
    ) == expected


def test_proof_classification_is_stable_and_idempotent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    layers = proof_layers(**{"structured-evidence": "not-required"})
    monkeypatch.setattr(
        workflow_cli,
        "_operational_item_proof_layers",
        lambda _root, _item: layers,
    )

    first_proof, first_items = workflow_cli.classify_operational_proof(
        tmp_path, (work_item(lifecycle="In Progress"),)
    )
    second_proof, second_items = workflow_cli.classify_operational_proof(
        tmp_path, first_items
    )

    assert first_proof == second_proof
    assert first_items == second_items
    assert [entry.key for entry in first_items[0].facts].count(
        "aggregate_proof_state"
    ) == 1
    assert first_proof.state == "repository-validated"


def test_health_matches_doctor_evaluation_including_accepted_and_legacy_counts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    accepted_issue = workflow_cli.DoctorIssue(
        "PW_TASK_DOCUMENT_INVALID",
        "warning",
        ".project-workflow/tasks/TASK-001/IMPLEMENTATION.md",
        "Accepted fixture warning.",
        "agent",
        False,
    )
    legacy_issue = workflow_cli.DoctorIssue(
        "PW_TRACKER_INVALID",
        "warning",
        ".project-workflow/tasks/EPIC-001-Legacy/TRACKER.md",
        "Legacy fixture warning.",
        "owner",
        False,
    )
    accepted_fingerprint = workflow_cli._doctor_issue_fingerprint(
        accepted_issue, tmp_path
    )
    issues = [accepted_issue, legacy_issue]
    accepted = {accepted_fingerprint: "Historical fixture."}
    monkeypatch.setattr(workflow_cli, "run_doctor", lambda _root: issues)
    monkeypatch.setattr(
        workflow_cli,
        "_accepted_doctor_warning_fingerprints",
        lambda _root: accepted,
    )

    health, findings = workflow_cli.classify_operational_health(tmp_path)
    strict_health, strict_findings = workflow_cli.classify_operational_health(
        tmp_path, strict=True
    )
    expected = workflow_cli._evaluate_doctor(
        issues,
        root=tmp_path,
        strict=False,
        accepted_fingerprints=accepted,
    )
    health_facts = {entry.key: entry.value for entry in health.facts}

    assert health.state == expected.status == "warning"
    assert health_facts == {
        "strict": False,
        "total_count": 2,
        "visible_count": 1,
        "accepted_count": 1,
        "current_count": 0,
        "legacy_count": 1,
        "blocking_count": 0,
    }
    assert [finding.code for finding in findings] == ["PW_TRACKER_INVALID"]
    assert strict_health.state == "fail"
    assert strict_findings[0].severity == "error"


def write_receipt(root: Path, name: str, payload: object) -> Path:
    path = root / name
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"release": {"version": "1.2.3"}}, "released"),
        (
            {
                "release": {
                    "version": "1.2.3",
                    "public_url": "https://example.invalid/package",
                }
            },
            "released",
        ),
        (
            {
                "release": {
                    "version": "1.2.3",
                    "publication": {
                        "status": "verified",
                        "target": "registry/package",
                        "source": "registry response",
                        "observed_at": "2026-07-22T00:00:00Z",
                        "result": "version 1.2.3 is public",
                    },
                }
            },
            "published",
        ),
        (
            {
                "deployment": {
                    "status": "verified",
                    "target": "production",
                    "source": "deployment receipt",
                    "observed_at": "2026-07-22T00:00:00Z",
                    "result": "healthy",
                }
            },
            "deployed",
        ),
    ],
)
def test_delivery_requires_exact_local_receipt_evidence_for_later_states(
    tmp_path: Path,
    payload: object,
    expected: str,
) -> None:
    receipt_path = write_receipt(tmp_path, "delivery.json", payload)
    item = work_item(
        item_facts=(fact("delivery_receipt", receipt_path.name),)
    )
    before = tree_hash(tmp_path)

    delivery, findings = workflow_cli.classify_operational_delivery(tmp_path, item)

    assert delivery.state == expected
    assert findings == ()
    assert tree_hash(tmp_path) == before


def test_delivery_separates_nonterminal_completion_and_git_integration(
    tmp_path: Path,
) -> None:
    tmp_path.mkdir(exist_ok=True)
    init_git(tmp_path)
    head_before = run_git(tmp_path, "rev-parse", "HEAD")
    status_before = run_git(tmp_path, "status", "--porcelain")

    nonterminal, _ = workflow_cli.classify_operational_delivery(
        tmp_path, work_item(lifecycle="Review")
    )
    completed, _ = workflow_cli.classify_operational_delivery(tmp_path, work_item())
    integrated, _ = workflow_cli.classify_operational_delivery(
        tmp_path,
        work_item(item_facts=(fact("tracker_branch", "main"),)),
    )

    assert nonterminal.state == "not-recorded"
    assert completed.state == "repository-complete"
    assert integrated.state == "integrated"
    assert run_git(tmp_path, "rev-parse", "HEAD") == head_before
    assert run_git(tmp_path, "status", "--porcelain") == status_before


def test_delivery_reports_missing_and_malformed_receipts_without_inflation(
    tmp_path: Path,
) -> None:
    malformed_path = tmp_path / "malformed.json"
    malformed_path.write_text("{bad", encoding="utf-8")

    missing, missing_findings = workflow_cli.classify_operational_delivery(
        tmp_path,
        work_item(item_facts=(fact("delivery_receipt", "missing.json"),)),
    )
    malformed, malformed_findings = workflow_cli.classify_operational_delivery(
        tmp_path,
        work_item(item_facts=(fact("delivery_receipt", malformed_path.name),)),
    )

    assert missing.state == malformed.state == "repository-complete"
    assert [finding.code for finding in missing_findings] == [
        "PW_STATUS_DELIVERY_RECEIPT_MISSING"
    ]
    assert [finding.code for finding in malformed_findings] == [
        "PW_STATUS_DELIVERY_RECEIPT_INVALID"
    ]
