from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from project_workflow import cli as workflow_cli

PROJECT = [sys.executable, "-m", "project_workflow.cli"]


def run_project(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*PROJECT, *args], cwd=root, check=False, capture_output=True, text=True)


def fixture_repo(tmp_path: Path) -> Path:
    initialized = run_project(tmp_path, "init", "--agent", "codex")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    scaffolded = run_project(
        tmp_path,
        "task",
        "init",
        "--title",
        "Coordination Subtraction",
        "--update-tracker",
        "--status",
        "In Progress",
    )
    assert scaffolded.returncode == 0, scaffolded.stdout + scaffolded.stderr
    task_dir = tmp_path / ".project-workflow/tasks/TASK-001-Coordination-Subtraction"
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nPreserve intent without a second execution graph.\n"
    )
    return task_dir


def coordinate_init(root: Path) -> subprocess.CompletedProcess[str]:
    return run_project(
        root,
        "coordinate",
        "init",
        "--id",
        "TASK-001",
        "--phase",
        "implementation",
        "--source-revision",
        "abc123",
        "--loaded-package-version",
        workflow_cli.CURRENT_PACKAGE_VERSION,
        "--loaded-asset-version",
        str(workflow_cli.CURRENT_ASSET_VERSION),
        "--loaded-contract-version",
        str(workflow_cli.COORDINATION_CONTRACT_VERSION),
        "--context-id",
        "context-1",
        "--next-action",
        "Run the existing lifecycle gate.",
        "--material-verification",
        "no",
    )


def test_durable_coordination_does_not_duplicate_delegate_execution_state(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    initialized = coordinate_init(tmp_path)
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr

    state = json.loads((task_dir / "COORDINATION.json").read_text())
    assert state["schema_version"] == workflow_cli.COORDINATION_SCHEMA_VERSION
    assert state["host_facts"]["context_contract"] == "declared"
    assert "units" not in state
    assert "packet_refs" not in state
    assert "receipt_refs" not in state

    removed = run_project(tmp_path, "coordinate", "packet", "--id", "TASK-001")
    assert removed.returncode != 0
    assert "invalid choice" in removed.stderr.lower()


def test_required_boundary_is_fail_closed_and_source_bound(tmp_path: Path) -> None:
    fixture_repo(tmp_path)
    assert coordinate_init(tmp_path).returncode == 0

    missing = workflow_cli._coordination_boundary_gate_issues(
        tmp_path,
        "TASK-001",
        boundary="before-unit-start",
        subject_id="unit-a",
    )
    assert missing == [
        "missing current before-unit-start intent decision for unit-a; record the bounded "
        "decision before continuing"
    ]

    recorded = run_project(
        tmp_path,
        "coordinate",
        "boundary",
        "--id",
        "TASK-001",
        "--boundary",
        "before-unit-start",
        "--classification",
        "inside-envelope",
        "--ocs",
        "OC1",
        "--capability-change",
        "none",
        "--consequence",
        "the approved capability remains intact",
        "--affected-units",
        "unit-a",
        "--shared-premises-valid",
        "yes",
        "--decided-by",
        "coordinator",
        "--next-action",
        "Start unit-a through Delegate.",
    )
    assert recorded.returncode == 0, recorded.stdout + recorded.stderr
    assert (
        workflow_cli._coordination_boundary_gate_issues(
            tmp_path,
            "TASK-001",
            boundary="before-unit-start",
            subject_id="unit-a",
        )
        == []
    )

    advanced = run_project(
        tmp_path,
        "coordinate",
        "phase",
        "--id",
        "TASK-001",
        "--phase",
        "implementation",
        "--source-revision",
        "def456",
        "--next-action",
        "Continue only after a current source-bound decision.",
    )
    assert advanced.returncode == 0, advanced.stdout + advanced.stderr
    stale_source = workflow_cli._coordination_boundary_gate_issues(
        tmp_path,
        "TASK-001",
        boundary="before-unit-start",
        subject_id="unit-a",
    )
    assert stale_source and "stale source-bound" in stale_source[0]

    refreshed = run_project(
        tmp_path,
        "coordinate",
        "boundary",
        "--id",
        "TASK-001",
        "--boundary",
        "before-unit-start",
        "--classification",
        "inside-envelope",
        "--ocs",
        "OC1",
        "--capability-change",
        "none",
        "--consequence",
        "the approved capability remains intact on the current source",
        "--affected-units",
        "unit-a",
        "--shared-premises-valid",
        "yes",
        "--decided-by",
        "coordinator",
        "--next-action",
        "Start unit-a through Delegate.",
    )
    assert refreshed.returncode == 0, refreshed.stdout + refreshed.stderr

    requirements = next((tmp_path / ".project-workflow/tasks").rglob("REQUIREMENTS.md"))
    requirements.write_text(requirements.read_text() + "\n## Decision\n\nChanged authority.\n")
    stale = workflow_cli._coordination_boundary_gate_issues(
        tmp_path,
        "TASK-001",
        boundary="before-unit-start",
        subject_id="unit-a",
    )
    assert stale and "stale" in stale[0]


def test_context_record_is_a_declaration_not_freshness_proof(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    assert coordinate_init(tmp_path).returncode == 0
    result = run_project(
        tmp_path,
        "coordinate",
        "context-record",
        "--id",
        "TASK-001",
        "--loaded-package-version",
        workflow_cli.CURRENT_PACKAGE_VERSION,
        "--loaded-asset-version",
        str(workflow_cli.CURRENT_ASSET_VERSION),
        "--loaded-contract-version",
        str(workflow_cli.COORDINATION_CONTRACT_VERSION),
        "--context-id",
        "same-context-after-explicit-reload",
        "--next-action",
        "Continue because the current contract was explicitly loaded.",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "declared loaded physical-context contract" in result.stdout.lower()
    state = json.loads((task_dir / "COORDINATION.json").read_text())
    assert state["host_facts"] == {
        "context_contract": "declared",
        "telemetry": "unknown",
    }
