from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli


PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]


def target(kind: str = "task") -> workflow_cli.DelegationTarget:
    return workflow_cli.DelegationTarget(
        target_id="TASK-001" if kind == "task" else "EPIC-001",
        kind=kind,
        title="Delegated work",
        lifecycle="In Progress",
        source_path=".project-workflow/tasks/plan.md",
        source_hash="abc123",
    )


def unit(
    unit_id: str,
    *,
    dependencies: tuple[str, ...] = (),
    scope: tuple[str, ...] = ("src",),
    parallel_safe: bool = True,
    state: str = "pending",
    order: int = 0,
) -> workflow_cli.DelegationUnit:
    return workflow_cli.DelegationUnit(
        unit_id=unit_id,
        title=f"Unit {unit_id}",
        dependencies=dependencies,
        write_scope=scope,
        parallel_safe=parallel_safe,
        canonical_state=state,
        source_order=order,
        source_path=".project-workflow/tasks/plan.md",
    )


def plan(**overrides: object) -> workflow_cli.DelegationPlan:
    values: dict[str, object] = {
        "target": target(),
        "units": (
            unit("1", scope=("src/one",), order=0),
            unit("2", dependencies=("1",), scope=("src/two",), order=1),
        ),
    }
    values.update(overrides)
    return workflow_cli.build_delegation_plan(**values)  # type: ignore[arg-type]


def write_task_fixture(root: Path, *, legacy: bool = False, status: str = "In Progress") -> Path:
    workflow_dir = root / ".project-workflow"
    task_dir = workflow_dir / "tasks" / "TASK-001-Delegated-Work"
    task_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "TRACKER.md").write_text(
        "# Tracker\n\n"
        "| ID | Title | Status | Docs |\n"
        "|---|---|---|---|\n"
        f"| TASK-001 | Delegated Work | {status} | "
        "tasks/TASK-001-Delegated-Work/IMPLEMENTATION.md |\n",
        encoding="utf-8",
    )
    if legacy:
        table = (
            "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
            "|---|---|---|---|---|---|\n"
            "| 1 | First | Work | AC1 | Test | To Do |\n"
        )
    else:
        table = (
            "| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| 1 | First | Work | AC1 | Test | Done | | src/one | Yes |\n"
            "| 2 | Second | Work | AC1 | Test | To Do | 1 | src/two | Yes |\n"
        )
    implementation = task_dir / "IMPLEMENTATION.md"
    implementation.write_text("## Task List\n\n" + table, encoding="utf-8")
    (task_dir / "REQUIREMENTS.md").write_text("# Requirements\n", encoding="utf-8")
    return implementation


def init_git(root: Path) -> None:
    for command in (
        ["git", "init"],
        ["git", "config", "user.email", "tests@example.com"],
        ["git", "config", "user.name", "Project Workflow Tests"],
    ):
        result = subprocess.run(command, cwd=root, check=False, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr


def run_project(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*PROJECT_CMD, *args], cwd=root, check=False, capture_output=True, text=True
    )


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        if ".git" in path.relative_to(root).parts:
            continue
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def test_task_table_parser_preserves_legacy_and_round_trips_delegation_metadata() -> None:
    legacy = (
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "|---|---|---|---|---|---|\n"
        "| 1 | First | Work | AC1 | Test | To Do |\n"
    )
    modern = legacy.replace(
        " | Status |\n|---|---|---|---|---|---|\n| 1 | First | Work | AC1 | Test | To Do |",
        " | Status | Dependencies | Write Scope | Parallel Safe |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| 1 | First | Work | AC1 | Test | To Do | none | src/app | Yes |",
    )
    legacy_found, legacy_rows, legacy_bad = workflow_cli._implementation_task_table_rows(legacy)
    modern_found, modern_rows, modern_bad = workflow_cli._implementation_task_table_rows(modern)

    assert legacy_found and not legacy_bad
    assert legacy_rows[0]["_delegation_metadata"] == "legacy"
    assert modern_found and not modern_bad
    assert modern_rows[0]["Dependencies"] == "none"
    assert modern_rows[0]["Write Scope"] == "src/app"
    assert modern_rows[0]["Parallel Safe"] == "Yes"


def test_legacy_task_plan_is_readable_but_delegate_fails_closed(tmp_path: Path) -> None:
    implementation = write_task_fixture(tmp_path, legacy=True)
    found, rows, malformed = workflow_cli._implementation_task_table_rows(
        implementation.read_text(encoding="utf-8")
    )
    assert found and rows and not malformed
    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        workflow_cli._delegation_task_units(tmp_path, implementation)
    assert caught.value.code == "PW_DELEGATION_METADATA_MISSING"


def test_build_plan_orders_graph_and_reports_readiness_executor_capacity_and_provenance() -> None:
    built = plan(
        requested_concurrency=4,
        available_child_capacity=1,
        observed_capabilities=("subagent",),
        capability_source="codex adapter observation 42",
    )

    assert built.selected_units == ("1", "2")
    assert built.eligible_units == ("1",)
    assert built.blocked_units == ("2",)
    assert built.units[0].executor == "subagent"
    assert built.effective_concurrency == built.effective_child_concurrency == 1
    assert "Reduced from requested 4" in built.concurrency_reason
    assert built.provenance[-1] == "capability:codex adapter observation 42"
    assert workflow_cli.delegation_plan_payload(built)["schema_version"] == 1


def test_zero_child_capacity_excludes_coordinator_and_reports_sequential_fallback() -> None:
    built = plan(requested_concurrency=3, available_child_capacity=0)
    assert built.effective_child_concurrency == 0
    assert built.effective_concurrency == 1
    assert all(item.executor in {"coordinator", "none"} for item in built.units)
    assert "coordinator excluded" in built.concurrency_reason


@pytest.mark.parametrize(
    ("units", "code"),
    [
        ((unit("1", dependencies=("1",)),), "PW_DELEGATION_DEPENDENCY_SELF"),
        ((unit("1", dependencies=("9",)),), "PW_DELEGATION_DEPENDENCY_MISSING"),
        (
            (unit("1", dependencies=("2",)), unit("2", dependencies=("1",), order=1)),
            "PW_DELEGATION_DEPENDENCY_CYCLE",
        ),
    ],
)
def test_dependency_validation_has_stable_fail_closed_errors(
    units: tuple[workflow_cli.DelegationUnit, ...], code: str
) -> None:
    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        workflow_cli.build_delegation_plan(target=target(), units=units)
    assert caught.value.code == code


def test_unfinished_omitted_dependency_invalidates_selected_subset() -> None:
    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        plan(selected_unit_ids=("2",))
    assert caught.value.code == "PW_DELEGATION_SUBSET_DEPENDENCY_OMITTED"

    completed_dependency = plan(
        units=(
            unit("1", state="complete", scope=("src/one",)),
            unit("2", dependencies=("1",), scope=("src/two",), order=1),
        ),
        selected_unit_ids=("2",),
    )
    assert completed_dependency.eligible_units == ("2",)


def test_parallel_prefix_collision_uses_path_boundaries_and_dependencies() -> None:
    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        plan(
            units=(
                unit("1", scope=("src/app",)),
                unit("2", scope=("src/app/components",), order=1),
            )
        )
    assert caught.value.code == "PW_DELEGATION_WRITE_SCOPE_COLLISION"

    boundary_safe = plan(
        units=(
            unit("1", scope=("src/app",)),
            unit("2", scope=("src/application",), order=1),
        )
    )
    assert boundary_safe.selected_units == ("1", "2")

    dependency_safe = plan(
        units=(
            unit("1", scope=("src/app",)),
            unit("2", dependencies=("1",), scope=("src/app",), order=1),
        )
    )
    assert dependency_safe.selected_units == ("1", "2")


def test_write_scope_rejects_globs_absolute_and_parent_paths() -> None:
    for scope in ("src/**", "/src", "../src"):
        with pytest.raises(workflow_cli.DelegationPlanError) as caught:
            workflow_cli._delegation_write_scope(scope, unit_id="1")
        assert caught.value.code == "PW_DELEGATION_WRITE_SCOPE_INVALID"


def test_capability_requires_observed_adapter_provenance() -> None:
    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        plan(observed_capabilities=("subagent",), available_child_capacity=1)
    assert caught.value.code == "PW_DELEGATION_CAPABILITY_UNOBSERVED"


def test_persistent_task_executor_requires_separate_owner_authority() -> None:
    epic_units = (unit("TASK-001", scope=()),)
    without_authority = workflow_cli.build_delegation_plan(
        target=target("epic"),
        units=epic_units,
        observed_capabilities=("persistent-task",),
        capability_source="codex adapter",
        available_child_capacity=1,
    )
    assert without_authority.units[0].executor == "coordinator"

    authorized = workflow_cli.build_delegation_plan(
        target=target("epic"),
        units=epic_units,
        observed_capabilities=("persistent-task",),
        capability_source="codex adapter",
        persistent_task_authority="owner approval EPIC-001",
        available_child_capacity=1,
    )
    assert authorized.units[0].executor == "coordinator"
    assert authorized.persistent_task_authority == "owner approval EPIC-001"

    fully_supported = workflow_cli.build_delegation_plan(
        target=target("epic"),
        units=epic_units,
        observed_capabilities=("persistent-task", "isolated-worktree", "task-monitoring"),
        capability_source="current codex adapter observation",
        persistent_task_authority="owner approval EPIC-001",
        available_child_capacity=1,
    )
    assert fully_supported.units[0].executor == "persistent-task"


def test_exact_target_resolution_rejects_mixed_unknown_and_unapproved(tmp_path: Path) -> None:
    write_task_fixture(tmp_path)
    with pytest.raises(workflow_cli.DelegationPlanError) as mixed:
        workflow_cli._resolve_delegation_target(tmp_path, ("TASK-001", "EPIC-001"))
    assert mixed.value.code == "PW_DELEGATION_TARGET_COUNT"
    with pytest.raises(workflow_cli.DelegationPlanError) as repeated:
        workflow_cli._resolve_delegation_target(tmp_path, ("TASK-001", "TASK-001"))
    assert repeated.value.code == "PW_DELEGATION_TARGET_COUNT"
    with pytest.raises(workflow_cli.DelegationPlanError) as unknown:
        workflow_cli._resolve_delegation_target(tmp_path, ("TASK-999",))
    assert unknown.value.code == "PW_DELEGATION_TARGET_UNKNOWN"

    write_task_fixture(tmp_path, status="To Do")
    with pytest.raises(workflow_cli.DelegationPlanError) as unapproved:
        workflow_cli._resolve_delegation_target(tmp_path, ("TASK-001",))
    assert unapproved.value.code == "PW_DELEGATION_TARGET_UNAPPROVED"


def test_delegate_plan_and_status_human_json_are_deterministic_and_read_only(tmp_path: Path) -> None:
    write_task_fixture(tmp_path)
    before = tree_hash(tmp_path)
    arguments = (
        "delegate",
        "plan",
        "--id",
        "TASK-001",
        "--available-child-capacity",
        "1",
        "--observed-capability",
        "subagent",
        "--capability-source",
        "fixture adapter",
        "--format",
        "json",
    )
    first = run_project(tmp_path, *arguments)
    second = run_project(tmp_path, *arguments)
    human = run_project(tmp_path, "delegate", "status", "--id", "TASK-001")

    assert first.returncode == second.returncode == human.returncode == 0
    assert first.stdout == second.stdout
    payload = json.loads(first.stdout)
    assert payload["target"]["id"] == "TASK-001"
    assert payload["eligible_units"] == ["2"]
    assert payload["units"][1]["dependencies"] == ["1"]
    assert human.stdout.startswith("Delegation Status\nTarget: TASK-001")
    assert "Runtime: not initialized" in human.stdout
    assert tree_hash(tmp_path) == before


def test_epic_decomposition_dependencies_are_compatible_and_authoritative(tmp_path: Path) -> None:
    epic_dir = tmp_path / ".project-workflow" / "tasks" / "EPIC-001-Delegated-Epic"
    epic_dir.mkdir(parents=True)
    tracker = epic_dir / "TRACKER.md"
    tracker.write_text(
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | First | Complete | Task | AC1 | | | |\n"
        "| TASK-002 | Second | Approved | Task | AC2 | | | |\n",
        encoding="utf-8",
    )
    plan_path = epic_dir / "DECOMPOSITION.md"
    plan_path.write_text(
        "## Authorized Child Rows\n\n"
        "| ID | Title | Parent ACs | Source | Dependencies |\n"
        "|---|---|---|---|---|\n"
        "| TASK-001 | First | AC1 | Owner plan | |\n"
        "| TASK-002 | Second | AC2 | Owner plan | TASK-001 |\n",
        encoding="utf-8",
    )
    rows = workflow_cli._read_decomposition_plan_rows(plan_path)
    units = workflow_cli._delegation_epic_units(tmp_path, epic_dir, plan_path)
    built = workflow_cli.build_delegation_plan(target=target("epic"), units=units)
    assert rows[1]["Dependencies"] == "TASK-001"
    assert built.eligible_units == ("TASK-002",)

    legacy = plan_path.read_text(encoding="utf-8").replace(" | Dependencies", "").replace(
        "|---|---|---|---|---|", "|---|---|---|---|"
    ).replace(" | TASK-001 |\n", " |\n").replace(" |\n", " |\n")
    plan_path.write_text(
        "## Authorized Child Rows\n\n"
        "| ID | Title | Parent ACs | Source |\n"
        "|---|---|---|---|\n"
        "| TASK-001 | First | AC1 | Owner plan |\n",
        encoding="utf-8",
    )
    assert workflow_cli._read_decomposition_plan_rows(plan_path)[0]["ID"] == "TASK-001"
    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        workflow_cli._delegation_epic_units(tmp_path, epic_dir, plan_path)
    assert caught.value.code == "PW_DELEGATION_METADATA_MISSING"
    assert legacy  # exercise conversion input without relying on it for authority


def test_runtime_state_is_ignored_private_atomic_and_reconciles_without_duplicate_eligibility(
    tmp_path: Path,
) -> None:
    init_git(tmp_path)
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    built = plan()
    state = workflow_cli.initialize_delegation_runtime_state(tmp_path, built)
    runtime_path = workflow_cli._delegation_runtime_path(tmp_path, "TASK-001")
    assert runtime_path.exists()
    assert subprocess.run(
        ["git", "check-ignore", "-q", str(runtime_path)], cwd=tmp_path, check=False
    ).returncode == 0
    assert set(state) == {
        "schema_version",
        "target_id",
        "target_kind",
        "plan_fingerprint",
        "worktree",
        "units",
    }
    assert workflow_cli.initialize_delegation_runtime_state(tmp_path, built) == state

    same_worktree = {
        "1": {
            "kind": "subagent",
            "id": "agent-1",
            "worktree": str(tmp_path),
            "state": "active",
        }
    }
    resumed = workflow_cli.reconcile_delegation_runtime_state(
        tmp_path, built, state, same_worktree
    )
    assert resumed["units"]["1"]["state"] == "active"  # type: ignore[index]
    assert "1" not in workflow_cli._delegation_status_payload(built, resumed)["eligible_units"]

    cross_worktree = {
        "1": {
            "kind": "subagent",
            "id": "agent-1",
            "worktree": str(tmp_path / "other"),
            "state": "active",
        }
    }
    orphaned = workflow_cli.reconcile_delegation_runtime_state(
        tmp_path, built, resumed, cross_worktree
    )
    assert orphaned["units"]["1"]["state"] == "orphaned"  # type: ignore[index]
    missing = workflow_cli.reconcile_delegation_runtime_state(tmp_path, built, resumed, {})
    assert missing["units"]["1"]["state"] == "orphaned"  # type: ignore[index]

    completed_plan = replace(
        built,
        units=(replace(built.units[0], canonical_state="complete"), built.units[1]),
    )
    canonical_wins = workflow_cli.reconcile_delegation_runtime_state(
        tmp_path, completed_plan, resumed, same_worktree
    )
    assert canonical_wins["units"]["1"]["state"] == "complete"  # type: ignore[index]


def test_runtime_rejects_private_or_credential_like_handle_fields(tmp_path: Path) -> None:
    built = plan()
    state = {
        "target_id": "TASK-001",
        "units": {"1": {"state": "pending", "handle": None}},
    }
    hostile = {
        "1": {
            "kind": "subagent",
            "id": "agent-1",
            "worktree": str(tmp_path),
            "state": "active",
            "transcript": "private",
        }
    }
    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        workflow_cli.reconcile_delegation_runtime_state(tmp_path, built, state, hostile)
    assert caught.value.code == "PW_DELEGATION_RUNTIME_PRIVATE_FIELD"

    runtime_path = workflow_cli._delegation_runtime_path(tmp_path, "TASK-001")
    runtime_path.parent.mkdir(parents=True)
    runtime_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "target_id": "TASK-001",
                "target_kind": "task",
                "plan_fingerprint": "abc",
                "worktree": str(tmp_path),
                "units": {
                    "1": {
                        "state": "active",
                        "handle": None,
                        "credential": "secret",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(workflow_cli.DelegationPlanError) as stored:
        workflow_cli._load_delegation_runtime_state(tmp_path, "TASK-001")
    assert stored.value.code == "PW_DELEGATION_RUNTIME_PRIVATE_FIELD"


def test_runtime_cli_initializes_reconciles_and_status_suppresses_relaunch(tmp_path: Path) -> None:
    write_task_fixture(tmp_path)
    init_git(tmp_path)
    (tmp_path / ".gitignore").write_text(
        ".project-workflow/runtime/delegations/\n", encoding="utf-8"
    )
    initialized = run_project(
        tmp_path, "delegate", "state-init", "--id", "TASK-001", "--format", "json"
    )
    assert initialized.returncode == 0, initialized.stderr
    assert json.loads(initialized.stdout)["units"]["2"]["state"] == "pending"

    observations = tmp_path / "observations.json"
    observations.write_text(
        json.dumps(
            {
                "2": {
                    "kind": "subagent",
                    "id": "agent-2",
                    "worktree": str(tmp_path),
                    "state": "active",
                }
            }
        ),
        encoding="utf-8",
    )
    reconciled = run_project(
        tmp_path,
        "delegate",
        "state-reconcile",
        "--id",
        "TASK-001",
        "--observed-handles",
        str(observations),
        "--format",
        "json",
    )
    status = run_project(
        tmp_path, "delegate", "status", "--id", "TASK-001", "--format", "json"
    )
    assert reconciled.returncode == status.returncode == 0
    assert json.loads(reconciled.stdout)["units"]["2"]["state"] == "active"
    status_payload = json.loads(status.stdout)
    assert status_payload["eligible_units"] == []
    assert status_payload["runtime_summary"]["active"] == ["2"]


def test_runtime_path_rejects_symlink_escape(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    runtime_parent = tmp_path / ".project-workflow" / "runtime"
    runtime_parent.mkdir(parents=True)
    (runtime_parent / "delegations").symlink_to(outside, target_is_directory=True)

    with pytest.raises(workflow_cli.DelegationPlanError) as caught:
        workflow_cli._delegation_runtime_path(tmp_path, "TASK-001")
    assert caught.value.code == "PW_DELEGATION_RUNTIME_UNSAFE_PATH"
