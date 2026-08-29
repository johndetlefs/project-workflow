from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli

PROJECT = [sys.executable, "-m", "project_workflow.cli"]


def run_project(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*PROJECT, *args], cwd=root, check=False, capture_output=True, text=True)


def fixture_repo(tmp_path: Path, *, task_id: str = "TASK-001") -> Path:
    initialized = run_project(tmp_path, "init", "--agent", "codex")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    scaffolded = run_project(
        tmp_path,
        "task",
        "init",
        "--title",
        "Coordination Canary",
        "--update-tracker",
        "--status",
        "In Progress",
    )
    assert scaffolded.returncode == 0, scaffolded.stdout + scaffolded.stderr
    assert f"Assigned ID: {task_id}" in scaffolded.stdout
    task_dir = tmp_path / ".project-workflow/tasks" / f"{task_id}-Coordination-Canary"
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nDeliver the approved canary without proxy substitution.\n"
    )
    (task_dir / "IMPLEMENTATION.md").write_text(
        "## User Story\n\nAs an owner, I want the canary delivered.\n"
    )
    return task_dir


def coordinate_init(
    root: Path,
    task_id: str = "TASK-001",
    *,
    package_version: str | None = None,
    asset_version: str | None = None,
    contract_version: str | None = None,
    claim_class: str = "mechanical",
    material: str = "no",
    checkpoint_unit: str | None = None,
) -> subprocess.CompletedProcess[str]:
    args = [
        "coordinate",
        "init",
        "--id",
        task_id,
        "--phase",
        "implementation",
        "--source-revision",
        "abc123",
        "--loaded-package-version",
        package_version or workflow_cli.CURRENT_PACKAGE_VERSION,
        "--loaded-asset-version",
        asset_version or str(workflow_cli.CURRENT_ASSET_VERSION),
        "--loaded-contract-version",
        contract_version or str(workflow_cli.COORDINATION_CONTRACT_VERSION),
        "--context-id",
        "context-1",
        "--next-action",
        "Run the existing lifecycle gate.",
        "--claim-class",
        claim_class,
        "--material-user-facing",
        material,
        "--material-verification",
        "no",
    ]
    if checkpoint_unit:
        args.extend(("--checkpoint-unit", checkpoint_unit))
    return run_project(root, *args)


def record_boundary(
    root: Path,
    boundary: str,
    classification: str,
    *,
    affected: str = "water-canary",
    amendment: str | None = None,
) -> subprocess.CompletedProcess[str]:
    args = [
        "coordinate",
        "boundary",
        "--id",
        "TASK-001",
        "--boundary",
        boundary,
        "--classification",
        classification,
        "--ocs",
        "OC1",
        "--capability-change",
        "editable authored water became a truthful read-only preview",
        "--consequence",
        "the owner still cannot author the requested level",
        "--affected-units",
        affected,
        "--shared-premises-valid",
        "no" if classification == "drift-detected" else "yes",
        "--decided-by",
        "coordinator",
    ]
    if amendment:
        args.extend(("--amendment-identity", amendment))
    return run_project(root, *args)


def test_current_stale_unknown_and_explicit_contract_load_preflight(tmp_path: Path) -> None:
    fixture_repo(tmp_path)
    assert coordinate_init(tmp_path).returncode == 0
    current = run_project(
        tmp_path, "coordinate", "preflight", "--id", "TASK-001", "--format", "json"
    )
    current_payload = json.loads(current.stdout)
    assert current_payload["contract_state"] == "current"
    assert current_payload["repository_contract"]["contract_version"] == str(
        workflow_cli.COORDINATION_CONTRACT_VERSION
    )

    state_path = next((tmp_path / ".project-workflow/tasks").rglob("COORDINATION.json"))
    state = json.loads(state_path.read_text())
    state["loaded_contract"]["package_version"] = "unknown"
    state_path.write_text(json.dumps(state))
    unknown = run_project(
        tmp_path, "coordinate", "preflight", "--id", "TASK-001", "--format", "json"
    )
    assert json.loads(unknown.stdout)["contract_state"] == "unknown"

    state["loaded_contract"]["package_version"] = "0.5.0"
    state["loaded_contract"]["asset_version"] = "4"
    state["loaded_contract"]["contract_version"] = "0"
    state_path.write_text(json.dumps(state))
    stale = run_project(tmp_path, "coordinate", "preflight", "--id", "TASK-001", "--format", "json")
    stale_payload = json.loads(stale.stdout)
    assert stale_payload["contract_state"] == "stale"
    assert stale_payload["next_action"] == "contract-load-required"
    assert "context-id-after-explicit-load" in stale_payload["command"]


def test_existing_task_lifecycle_enforces_source_bound_decisions_automatically(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture_repo(tmp_path)
    assert coordinate_init(tmp_path).returncode == 0
    monkeypatch.setattr(workflow_cli, "_task_testing_integrity_issues", lambda _text: ())
    monkeypatch.setattr(
        workflow_cli,
        "_approval_envelope_issues",
        lambda _text, *, require_implementation: [],
    )
    monkeypatch.setattr(
        workflow_cli,
        "_task_ready_issues_for_paths",
        lambda *, requirements_path, implementation_path: [],
    )

    def update():
        return workflow_cli._update_global_tracker_row_status(
            root=tmp_path,
            tracker_path=tmp_path / ".project-workflow/TRACKER.md",
            row_id="TASK-001",
            new_status="Testing",
            force=False,
            reason=None,
        )

    with pytest.raises(SystemExit) as missing_return:
        update()
    assert "unit-return-or-dependency-join" in str(missing_return.value)

    assert (
        record_boundary(
            tmp_path,
            "unit-return-or-dependency-join",
            "inside-envelope",
            affected="TASK-001",
        ).returncode
        == 0
    )
    advanced = run_project(
        tmp_path,
        "coordinate",
        "phase",
        "--id",
        "TASK-001",
        "--phase",
        "testing",
        "--source-revision",
        "def456",
        "--next-action",
        "Require a current source-bound return decision.",
    )
    assert advanced.returncode == 0, advanced.stdout + advanced.stderr
    with pytest.raises(SystemExit) as stale_source:
        update()
    assert "stale source-bound" in str(stale_source.value)
    assert (
        record_boundary(
            tmp_path,
            "unit-return-or-dependency-join",
            "inside-envelope",
            affected="TASK-001",
        ).returncode
        == 0
    )
    assert update() == ("In Progress", "Testing")


def test_epic_child_lifecycle_rejects_stale_source_bound_decision(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    initialized = run_project(tmp_path, "init", "--agent", "codex")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    epic_dir = tmp_path / ".project-workflow/tasks/EPIC-001-Source-Gate"
    child_dir = epic_dir / "TASK-901-Child"
    child_dir.mkdir(parents=True)
    (epic_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nKeep child lifecycle bound to exact source.\n"
    )
    (child_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nDeliver the exact child source.\n"
    )
    (child_dir / "IMPLEMENTATION.md").write_text("## User Story\n\nDeliver the child.\n")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-901 | Child | In Progress | Task | AC1 | "
        "tasks/EPIC-001-Source-Gate/TASK-901-Child/IMPLEMENTATION.md |  |  |\n"
    )
    coordinated = run_project(
        tmp_path,
        "coordinate",
        "init",
        "--id",
        "EPIC-001",
        "--phase",
        "implementation",
        "--source-revision",
        "rev-a",
        "--loaded-package-version",
        workflow_cli.CURRENT_PACKAGE_VERSION,
        "--loaded-asset-version",
        str(workflow_cli.CURRENT_ASSET_VERSION),
        "--loaded-contract-version",
        str(workflow_cli.COORDINATION_CONTRACT_VERSION),
        "--context-id",
        "context-1",
        "--next-action",
        "Verify the child return.",
        "--material-verification",
        "no",
    )
    assert coordinated.returncode == 0, coordinated.stdout + coordinated.stderr

    def epic_boundary() -> subprocess.CompletedProcess[str]:
        return run_project(
            tmp_path,
            "coordinate",
            "boundary",
            "--id",
            "EPIC-001",
            "--boundary",
            "unit-return-or-dependency-join",
            "--classification",
            "inside-envelope",
            "--ocs",
            "OC1",
            "--capability-change",
            "none",
            "--consequence",
            "the exact child source remains authorized",
            "--affected-units",
            "TASK-901",
            "--shared-premises-valid",
            "yes",
            "--decided-by",
            "coordinator",
            "--next-action",
            "Move the child to Testing.",
        )

    assert epic_boundary().returncode == 0
    advanced = run_project(
        tmp_path,
        "coordinate",
        "phase",
        "--id",
        "EPIC-001",
        "--phase",
        "testing",
        "--source-revision",
        "rev-b",
        "--next-action",
        "Require a current child-return decision.",
    )
    assert advanced.returncode == 0, advanced.stdout + advanced.stderr
    monkeypatch.setattr(workflow_cli, "_task_testing_integrity_issues", lambda _text: ())
    monkeypatch.setattr(
        workflow_cli,
        "_task_ready_issues_for_paths",
        lambda *, requirements_path, implementation_path, parent_ac_ids: [],
    )

    def update():
        return workflow_cli._update_epic_child_status(
            root=tmp_path,
            epic_tracker_path=epic_dir / "TRACKER.md",
            row_id="TASK-901",
            new_status="Testing",
            force=False,
            reason=None,
        )

    with pytest.raises(SystemExit) as stale:
        update()
    assert "stale source-bound" in str(stale.value)
    assert epic_boundary().returncode == 0
    assert update() == ("In Progress", "Testing")


@pytest.mark.parametrize("boundary", workflow_cli.COORDINATION_BOUNDARIES)
def test_water_style_drift_blocks_at_each_source_bound_gate(tmp_path: Path, boundary: str) -> None:
    fixture_repo(tmp_path)
    assert coordinate_init(tmp_path).returncode == 0
    drift = record_boundary(tmp_path, boundary, "drift-detected")
    assert drift.returncode == 0, drift.stdout + drift.stderr

    issues = workflow_cli._coordination_boundary_gate_issues(
        tmp_path,
        "TASK-001",
        boundary=boundary,
        subject_id="water-canary",
    )
    assert issues and "blocked by recorded drift" in issues[0]
    status = run_project(tmp_path, "coordinate", "status", "--id", "TASK-001", "--format", "json")
    payload = json.loads(status.stdout)
    assert payload["last_boundary"]["classification"] == "drift-detected"
    assert payload["last_boundary"]["intent_identity"].startswith("sha256:")
    assert "units" not in payload


def test_early_outcome_checkpoint_gates_existing_lifecycle_and_owner_judgment(
    tmp_path: Path,
) -> None:
    fixture_repo(tmp_path)
    initialized = coordinate_init(
        tmp_path,
        claim_class="authoring",
        material="yes",
        checkpoint_unit="water-canary",
    )
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    assert workflow_cli._coordination_checkpoint_gate_issues(
        tmp_path, "TASK-001", subject_id="polish"
    ) == ["early outcome checkpoint water-canary must pass before starting polish"]
    assert (
        workflow_cli._coordination_checkpoint_gate_issues(
            tmp_path, "TASK-001", subject_id="water-canary"
        )
        == []
    )

    checkpoint_args = (
        "coordinate",
        "checkpoint",
        "--id",
        "TASK-001",
        "--unit",
        "water-canary",
        "--actor",
        "owner",
        "--entry-point",
        "level editor",
        "--starting-state",
        "blank ocean level",
        "--operations",
        "author water and shoreline",
        "--resulting-state",
        "playable authored level",
        "--source-environment",
        "rendered editor canary",
        "--observations",
        "water is editable",
        "--owner-judgment",
        "required",
        "--verdict",
        "pass",
        "--recorded-by",
        "coordinator",
    )
    self_pass = run_project(tmp_path, *checkpoint_args)
    assert self_pass.returncode != 0
    assert "cannot self-pass" in self_pass.stderr.lower()


def test_phase_handoff_preserves_decisions_and_approved_change_refreshes_authority(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path)
    initialized = run_project(
        tmp_path,
        "coordinate",
        "init",
        "--id",
        "TASK-001",
        "--phase",
        "planning",
        "--source-revision",
        "repo-a-1",
        "--repository-source",
        "app=repo-a-1",
        "--repository-source",
        "foundation=repo-b-3",
        "--decision",
        "Ocean art remains consumer-owned",
        "--loaded-package-version",
        workflow_cli.CURRENT_PACKAGE_VERSION,
        "--loaded-asset-version",
        str(workflow_cli.CURRENT_ASSET_VERSION),
        "--loaded-contract-version",
        str(workflow_cli.COORDINATION_CONTRACT_VERSION),
        "--context-id",
        "context-1",
        "--next-action",
        "Run existing planning gates",
        "--material-verification",
        "no",
    )
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr

    requirements = task_dir / "REQUIREMENTS.md"
    requirements.write_text(
        requirements.read_text() + "\n## Decision\n\nUse consumer source two.\n"
    )
    amended = record_boundary(
        tmp_path,
        "new-evidence-or-owner-reframe",
        "approved-change",
        affected="consumer",
        amendment="AMEND-001",
    )
    assert amended.returncode == 0, amended.stdout + amended.stderr
    loaded = run_project(
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
        "same-context-after-load",
        "--next-action",
        "Refresh the canonical plan and Delegate packet.",
    )
    assert loaded.returncode == 0, loaded.stdout + loaded.stderr

    state = json.loads((task_dir / "COORDINATION.json").read_text())
    assert state["decisions"] == ["Ocean art remains consumer-owned"]
    assert state["repositories"]["foundation"]["source_revision"] == "repo-b-3"
    assert state["last_boundary"]["amendment_identity"] == "AMEND-001"
    assert "packet_refs" not in state


def test_inside_envelope_evidence_refresh_advances_authority_without_circular_preflight(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path)
    assert coordinate_init(tmp_path).returncode == 0
    requirements = task_dir / "REQUIREMENTS.md"
    requirements.write_text(
        requirements.read_text()
        + "\n## Evidence Update\n\nFocused validation completed without changing Intent.\n"
    )

    stale = run_project(tmp_path, "coordinate", "preflight", "--id", "TASK-001", "--format", "json")
    assert json.loads(stale.stdout)["contract_state"] == "stale"

    refreshed = record_boundary(
        tmp_path,
        "new-evidence-or-owner-reframe",
        "inside-envelope",
        affected="TASK-001",
    )
    assert refreshed.returncode == 0, refreshed.stdout + refreshed.stderr

    current = run_project(
        tmp_path, "coordinate", "preflight", "--id", "TASK-001", "--format", "json"
    )
    payload = json.loads(current.stdout)
    assert payload["contract_state"] == "current"
    assert payload["recorded_intent_identity"] == payload["current_intent_identity"]


def test_project_status_prioritizes_pending_outcome_checkpoint(tmp_path: Path) -> None:
    fixture_repo(tmp_path)
    assert (
        coordinate_init(
            tmp_path,
            claim_class="authoring",
            material="yes",
            checkpoint_unit="water-canary",
        ).returncode
        == 0
    )
    status = run_project(tmp_path, "status", "--id", "TASK-001", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    payload = json.loads(status.stdout)
    assert payload["primary_action"]["code"] == "PW_STATUS_COORDINATION_CHECKPOINT"


def test_earned_execution_surface_defaults_to_coordinator_without_basis() -> None:
    target = workflow_cli.DelegationTarget(
        target_id="TASK-001",
        kind="task",
        title="Task",
        lifecycle="In Progress",
        source_path="IMPLEMENTATION.md",
        source_hash="abc",
    )
    unit = workflow_cli.DelegationUnit(
        unit_id="1",
        title="Coupled work",
        dependencies=(),
        write_scope=("src",),
        parallel_safe=True,
        canonical_state="pending",
        source_order=0,
        source_path="IMPLEMENTATION.md",
        execution_needs=workflow_cli.DelegationExecutionNeeds(earned_surface_required=True),
    )
    plan = workflow_cli.build_delegation_plan(
        target=target,
        units=(unit,),
        requested_concurrency=2,
        available_child_capacity=2,
        observed_capabilities=("subagent",),
        capability_source="2026-08-24 current runtime",
    )
    assert plan.units[0].executor == "coordinator"

    earned = workflow_cli.DelegationUnit(
        **{
            **unit.__dict__,
            "execution_needs": workflow_cli.DelegationExecutionNeeds(
                tokens=(
                    "benefit:independent-context",
                    "overhead:low-packet-synthesis",
                    "tradeoff:isolation-outweighs-handoff",
                ),
                execution_benefit="independent-context",
                expected_overhead="low-packet-synthesis",
                benefit_overhead_basis="isolation-outweighs-handoff",
                earned_surface_required=True,
            ),
        }
    )
    earned_plan = workflow_cli.build_delegation_plan(
        target=target,
        units=(earned,),
        requested_concurrency=2,
        available_child_capacity=2,
        observed_capabilities=("subagent",),
        capability_source="2026-08-24 current runtime",
    )
    assert earned_plan.units[0].executor == "subagent"
