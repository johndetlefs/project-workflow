from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli

PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def git_state(root: Path) -> dict[str, object]:
    def optional(*args: str) -> str | None:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip() if completed.returncode == 0 else None

    porcelain = optional("status", "--porcelain")
    return {
        "root": str(root.resolve()),
        "branch": optional("symbolic-ref", "--quiet", "--short", "HEAD"),
        "head": optional("rev-parse", "HEAD"),
        "porcelain": porcelain,
        "porcelain_sha256": hashlib.sha256((porcelain or "").encode()).hexdigest(),
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_project(
    root: Path,
    *args: str,
    command_log: list[dict[str, object]] | None = None,
) -> subprocess.CompletedProcess[str]:
    local_helper = root / ".project-workflow" / "cli" / "workflow"
    using_local_helper = local_helper.exists()
    project_cmd = [str(local_helper)] if using_local_helper else PROJECT_CMD
    completed = subprocess.run(
        [*project_cmd, *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if command_log is not None:
        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        record: dict[str, object] = {
            "entrypoint": (
                ".project-workflow/cli/workflow"
                if using_local_helper
                else "python -m project_workflow.cli"
            ),
            "args": list(args),
            "returncode": completed.returncode,
        }
        if len(stdout) <= 1000:
            record["stdout"] = stdout
        else:
            record["stdout_bytes"] = len(completed.stdout.encode())
            record["stdout_sha256"] = hashlib.sha256(completed.stdout.encode()).hexdigest()
        if stderr:
            record["stderr"] = stderr
        command_log.append(record)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return completed


def init_git(root: Path, marker: str) -> None:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-b", "main")
    git(root, "config", "user.email", "workspace-tests@example.com")
    git(root, "config", "user.name", "Workspace Tests")
    (root / "README.md").write_text(f"{marker}\n", encoding="utf-8")
    git(root, "add", "README.md")
    git(root, "commit", "-m", f"initialize {marker}")


def write_workspace_config(root: Path) -> Path:
    workflow_dir = root / ".project-workflow"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    config_path = workflow_dir / "config.json"
    payload = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    payload["workspace"] = {
        "authority_repository": "workspace",
        "repositories": [
            {"id": "workspace", "path": ".", "role": "control"},
            {"id": "next", "path": "next", "role": "implementation"},
            {"id": "email", "path": "email", "role": "implementation"},
        ],
    }
    config_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return config_path


def workspace_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "workspace"
    init_git(root, "workspace")
    init_git(root / "next", "next")
    init_git(root / "email", "email")
    write_workspace_config(root)
    return root


def disposable_workspace_requirements() -> str:
    return """\
# Requirements

## Summary

- Task: TASK-001
- Title: Coordinate Site Delivery

## Goal

- Coordinate one delivery spanning the parent authority, next, and email repositories.

## Non-Goals

- Do not commit, push, merge, release, or deploy any repository.

## Users & Context

- The workspace owner needs one authoritative workflow with repository-specific state.

## Repository Scope

- Primary repository: next
- Repositories touched: workspace, next, email

## Requirements (Outcome-Focused)

- Keep workflow authority in the parent while attributing implementation and proof by repository.

## Acceptance Criteria (Verifiable)

- AC1: The task reaches Complete with explicit scope, status, and evidence for all touched repositories.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use the parent workflow and perform no cross-repository delivery actions.

## Validation Plan

- Inspect focused workspace status and record one validation result per touched repository.
"""


def disposable_workspace_implementation(*, completed: bool) -> str:
    if completed:
        repository_evidence = """\
| workspace | `main`; PR not created | Workflow Doctor passed | No delivery authorized | `evidence/workspace-validation.txt` |
| next | `main`; PR not created | Next validation passed | No delivery authorized | `evidence/next-validation.txt` |
| email | Detached fixture; PR not created | Email validation passed | No delivery authorized | `evidence/email-validation.txt` |"""
        checkbox = "x"
        task_status = "Done"
        qa = """\
- Date: 2026-07-29
- Verdict: Pass
- Evidence: Focused CLI status and repository-specific validation receipts passed.
- Findings: None."""
    else:
        repository_evidence = """\
| workspace | not recorded | not recorded | not recorded | not recorded |
| next | not recorded | not recorded | not recorded | not recorded |
| email | not recorded | not recorded | not recorded | not recorded |"""
        checkbox = " "
        task_status = "To Do"
        qa = """\
- Verdict: Pending
- Evidence: Pending implementation.
- Findings: Pending review."""
    return f"""\
## User Story

As the workspace owner, I want one parent task to coordinate three repositories without creating child workflow state.

## Architecture Impact

- Classification: no
- Reason: The fixture exercises existing workspace lifecycle and evidence behavior without changing architecture.
- Architecture authority: Not applicable
- Authority identity: Not applicable
- Affected boundaries: None
- Architecture decision: Not required
- Measurable constraints: Not required
- Conformance plan: Not required

## Acceptance Criteria

- [{checkbox}] AC1: The parent task records valid repository scope, status, and evidence through handoff.

## Validation

- AC1: Run the actual Project Workflow CLI lifecycle and inspect the generated task and tracker artifacts.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
{repository_evidence}

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Coordinate repositories | Exercise the parent-owned workspace lifecycle. | AC1 | Inspect CLI output and generated artifacts. | {task_status} |

## QA & Code Review

{qa}

## Retro

- Reusable lessons: Workspace handoff proof must remain repository-attributed.
- Conventions or agent assets updated: None.
- Follow-up tasks: None.
"""


def run_disposable_workspace_cli_journey(root: Path) -> dict[str, object]:
    if root.exists() and any(root.iterdir()):
        raise AssertionError(f"Journey root must be empty: {root}")
    root.mkdir(parents=True, exist_ok=True)
    commands: list[dict[str, object]] = []

    init_git(root, "workspace")
    run_project(root, "init", "--agent", "codex", command_log=commands)
    init_git(root / "next", "next")
    init_git(root / "email", "email")
    write_workspace_config(root)
    run_project(root, "doctor", command_log=commands)
    run_project(
        root,
        "task",
        "init",
        "--title",
        "Coordinate Site Delivery",
        "--update-tracker",
        command_log=commands,
    )

    task_dir = next((root / ".project-workflow" / "tasks").glob("TASK-001-*"))
    requirements_path = task_dir / "REQUIREMENTS.md"
    implementation_path = task_dir / "IMPLEMENTATION.md"
    requirements_path.write_text(disposable_workspace_requirements(), encoding="utf-8")
    implementation_path.write_text(
        disposable_workspace_implementation(completed=False),
        encoding="utf-8",
    )
    run_project(
        root,
        "task",
        "approve-requirements",
        "--id",
        "TASK-001",
        "--approved-by",
        "Disposable Workspace Owner",
        "--source",
        "FIX-005 disposable CLI journey approval.",
        command_log=commands,
    )
    run_project(
        root,
        "task",
        "status",
        "--id",
        "TASK-001",
        "--to",
        "Analysing",
        command_log=commands,
    )
    run_project(root, "task", "ready", "--id", "TASK-001", command_log=commands)
    run_project(
        root,
        "task",
        "status",
        "--id",
        "TASK-001",
        "--to",
        "Ready",
        command_log=commands,
    )
    run_project(
        root,
        "task",
        "status",
        "--id",
        "TASK-001",
        "--to",
        "In Progress",
        command_log=commands,
    )

    (root / "next" / "uncommitted.txt").write_text("next is intentionally dirty\n")
    git(root / "email", "checkout", "--detach")
    before_read_only_status = {
        repository_id: git_state(repository_root)
        for repository_id, repository_root in (
            ("workspace", root),
            ("next", root / "next"),
            ("email", root / "email"),
        )
    }
    focused_status = run_project(
        root,
        "status",
        "--id",
        "TASK-001",
        "--format",
        "json",
        command_log=commands,
    )
    focused_payload = json.loads(focused_status.stdout)
    selected_status = run_project(
        root,
        "status",
        "--id",
        "TASK-001",
        "--repository",
        "email",
        "--format",
        "json",
        command_log=commands,
    )
    selected_payload = json.loads(selected_status.stdout)
    after_read_only_status = {
        repository_id: git_state(repository_root)
        for repository_id, repository_root in (
            ("workspace", root),
            ("next", root / "next"),
            ("email", root / "email"),
        )
    }
    assert before_read_only_status == after_read_only_status

    evidence_dir = task_dir / "evidence"
    evidence_dir.mkdir()
    focused_status_path = evidence_dir / "focused-status.json"
    focused_status_path.write_text(focused_status.stdout, encoding="utf-8")
    selected_status_path = evidence_dir / "email-status.json"
    selected_status_path.write_text(selected_status.stdout, encoding="utf-8")
    for repository_id in ("workspace", "next", "email"):
        (evidence_dir / f"{repository_id}-validation.txt").write_text(
            f"{repository_id} validation: pass\n",
            encoding="utf-8",
        )
    implementation_path.write_text(
        disposable_workspace_implementation(completed=True),
        encoding="utf-8",
    )
    before_lifecycle_close = {
        repository_id: git_state(repository_root)
        for repository_id, repository_root in (
            ("workspace", root),
            ("next", root / "next"),
            ("email", root / "email"),
        )
    }
    for status in ("Testing", "Review", "Complete"):
        run_project(
            root,
            "task",
            "status",
            "--id",
            "TASK-001",
            "--to",
            status,
            command_log=commands,
        )
    after_lifecycle_close = {
        repository_id: git_state(repository_root)
        for repository_id, repository_root in (
            ("workspace", root),
            ("next", root / "next"),
            ("email", root / "email"),
        )
    }
    for repository_id in ("workspace", "next", "email"):
        assert (
            before_lifecycle_close[repository_id]["head"]
            == after_lifecycle_close[repository_id]["head"]
        )
        assert (
            before_lifecycle_close[repository_id]["branch"]
            == after_lifecycle_close[repository_id]["branch"]
        )
    assert before_lifecycle_close["next"] == after_lifecycle_close["next"]
    assert before_lifecycle_close["email"] == after_lifecycle_close["email"]

    tracker_path = root / ".project-workflow" / "TRACKER.md"
    tracker_text = tracker_path.read_text(encoding="utf-8")
    assert "| TASK-001 | Coordinate Site Delivery | Complete |" in tracker_text
    assert not (root / "next" / ".project-workflow").exists()
    assert not (root / "email" / ".project-workflow").exists()

    repositories = {entry["id"]: entry for entry in focused_payload["repositories"]}
    assert set(repositories) == {"workspace", "next", "email"}
    assert repositories["next"]["git"]["state"] == "dirty"
    assert repositories["email"]["git"]["state"] == "detached"
    assert [entry["id"] for entry in selected_payload["repositories"]] == ["email"]

    return {
        "schema_version": 1,
        "executed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "execution_target": str(root.resolve()),
        "source": {
            "bootstrap_entrypoint": "python -m project_workflow.cli",
            "journey_entrypoint": ".project-workflow/cli/workflow",
            "source_cli_sha256": file_sha256(Path(workflow_cli.__file__).resolve()),
            "canonical_generated_runtime_sha256": file_sha256(
                Path(workflow_cli.__file__).resolve().parent / "templates" / "workflow.py"
            ),
            "generated_helper_sha256": file_sha256(
                root / ".project-workflow" / "cli" / "workflow.py"
            ),
        },
        "workspace": {
            "authority_repository": "workspace",
            "repositories": ["workspace", "next", "email"],
            "child_workflow_state_created": False,
        },
        "lifecycle": {
            "task": "TASK-001",
            "final_status": "Complete",
            "commands": commands,
        },
        "status_observation": {
            "next": "dirty",
            "email": "detached",
            "repository_selector": "email",
            "before_after_read_only_git_state_equal": True,
        },
        "git_mutation_boundary": {
            "heads_and_branches_unchanged_by_workflow_lifecycle": True,
            "next_and_email_git_state_unchanged_by_workflow_lifecycle": True,
            "commit_push_merge_release_deploy_performed": False,
        },
        "handoff_artifacts": {
            "requirements": {
                "path": str(requirements_path.relative_to(root)),
                "sha256": file_sha256(requirements_path),
            },
            "implementation": {
                "path": str(implementation_path.relative_to(root)),
                "sha256": file_sha256(implementation_path),
            },
            "tracker": {
                "path": str(tracker_path.relative_to(root)),
                "sha256": file_sha256(tracker_path),
            },
            "focused_status": {
                "path": str(focused_status_path.relative_to(root)),
                "sha256": file_sha256(focused_status_path),
            },
            "selected_status": {
                "path": str(selected_status_path.relative_to(root)),
                "sha256": file_sha256(selected_status_path),
            },
            "repository_evidence": [
                {
                    "path": str(path.relative_to(root)),
                    "sha256": file_sha256(path),
                }
                for path in sorted(evidence_dir.glob("*-validation.txt"))
            ],
            "all_task_artifacts": sorted(
                str(path.relative_to(root)) for path in task_dir.rglob("*") if path.is_file()
            ),
        },
    }


def test_workspace_status_reports_each_independent_repository_and_selector(
    tmp_path: Path,
) -> None:
    root = workspace_fixture(tmp_path)
    (root / "next" / "dirty.txt").write_text("dirty\n", encoding="utf-8")

    snapshot = workflow_cli.build_operational_status_snapshot(root)
    payload = workflow_cli.operational_status_payload(snapshot)

    assert payload["workspace"] == {
        "enabled": True,
        "authority_repository": "workspace",
    }
    repositories = {entry["id"]: entry for entry in payload["repositories"]}
    assert set(repositories) == {"workspace", "next", "email"}
    assert repositories["workspace"]["authority"] is True
    assert repositories["workspace"]["git"]["facts"][1]["value"] == str(root.resolve())
    assert repositories["next"]["git"]["state"] == "dirty"
    assert repositories["email"]["git"]["state"] == "clean"
    assert payload["git"] == repositories["workspace"]["git"]
    human = workflow_cli.render_operational_status_human(snapshot)
    assert "Workspace repositories" in human
    assert "- next [implementation] next — Git dirty" in human
    next_dirty = next(
        finding
        for finding in snapshot.findings
        if finding.code == "PW_STATUS_WORKSPACE_REPOSITORY_DIRTY" and "'next'" in finding.message
    )
    next_action = workflow_cli._operational_finding_candidates((next_dirty,))[0].action
    assert "'next'" in next_action.reason

    selected = workflow_cli.build_operational_status_snapshot(
        root,
        repository_id="next",
    )
    assert [repository.repository_id for repository in selected.repositories] == ["next"]
    assert selected.repositories[0].git.state == "dirty"
    assert next(fact.value for fact in selected.git.facts if fact.key == "top_level") == str(
        root.resolve()
    )


def test_workspace_status_rejects_unknown_repository_selector(tmp_path: Path) -> None:
    root = workspace_fixture(tmp_path)

    with pytest.raises(SystemExit, match="Unknown workspace repository 'missing'"):
        workflow_cli.build_operational_status_snapshot(
            root,
            repository_id="missing",
        )


def test_workspace_status_names_detached_repository_and_safe_action(
    tmp_path: Path,
) -> None:
    root = workspace_fixture(tmp_path)
    git(root / "email", "checkout", "--detach")

    snapshot = workflow_cli.build_operational_status_snapshot(
        root,
        repository_id="email",
    )

    assert snapshot.repositories[0].git.state == "detached"
    detached = next(
        finding
        for finding in snapshot.findings
        if finding.code == "PW_STATUS_WORKSPACE_REPOSITORY_DETACHED"
    )
    assert "'email'" in detached.message
    action = workflow_cli._operational_finding_candidates((detached,))[0].action
    assert "'email'" in action.reason


def test_workspace_status_names_unavailable_repository_and_safe_action(
    tmp_path: Path,
) -> None:
    root = workspace_fixture(tmp_path)
    git(root / "email", "update-ref", "-d", "refs/heads/main")

    snapshot = workflow_cli.build_operational_status_snapshot(
        root,
        repository_id="email",
    )

    assert snapshot.repositories[0].git.state == "unavailable"
    unavailable = next(
        finding
        for finding in snapshot.findings
        if finding.code == "PW_STATUS_WORKSPACE_REPOSITORY_UNAVAILABLE"
    )
    assert "'email'" in unavailable.message
    action = workflow_cli._operational_finding_candidates((unavailable,))[0].action
    assert "'email'" in action.reason


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda payload: payload["workspace"]["repositories"].append(
                {"id": "next", "path": "email", "role": "implementation"}
            ),
            "repository ID 'next' is duplicated",
        ),
        (
            lambda payload: payload["workspace"]["repositories"][1].update({"path": "../outside"}),
            "cannot contain '..'",
        ),
        (
            lambda payload: payload["workspace"]["repositories"][1].update(
                {"path": "nested-not-a-root"}
            ),
            "does not exist as a directory",
        ),
        (
            lambda payload: payload["workspace"]["repositories"][0].update(
                {"role": "implementation"}
            ),
            "exactly one control repository",
        ),
    ],
)
def test_workspace_config_rejects_ambiguous_or_unsafe_registry(
    tmp_path: Path,
    mutate: object,
    message: str,
) -> None:
    root = workspace_fixture(tmp_path)
    config_path = root / ".project-workflow" / "config.json"
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    mutate(payload)
    config_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match=message):
        workflow_cli._load_workflow_config(root)


def test_workspace_config_rejects_non_root_alias_and_symlink_escape(
    tmp_path: Path,
) -> None:
    root = workspace_fixture(tmp_path)
    config_path = root / ".project-workflow" / "config.json"
    original = json.loads(config_path.read_text(encoding="utf-8"))

    (root / "nested-not-a-root").mkdir()
    non_root = json.loads(json.dumps(original))
    non_root["workspace"]["repositories"].append(
        {
            "id": "nested",
            "path": "nested-not-a-root",
            "role": "implementation",
        }
    )
    config_path.write_text(json.dumps(non_root), encoding="utf-8")
    with pytest.raises(SystemExit, match="is not an independent Git root"):
        workflow_cli._load_workflow_config(root)

    (root / "next-alias").symlink_to(root / "next", target_is_directory=True)
    aliased = json.loads(json.dumps(original))
    aliased["workspace"]["repositories"].append(
        {"id": "next-alias", "path": "next-alias", "role": "implementation"}
    )
    config_path.write_text(json.dumps(aliased), encoding="utf-8")
    with pytest.raises(SystemExit, match="aliases an existing repository"):
        workflow_cli._load_workflow_config(root)

    outside = tmp_path / "outside"
    init_git(outside, "outside")
    (root / "outside-alias").symlink_to(outside, target_is_directory=True)
    escaped = json.loads(json.dumps(original))
    escaped["workspace"]["repositories"].append(
        {"id": "outside", "path": "outside-alias", "role": "implementation"}
    )
    config_path.write_text(json.dumps(escaped), encoding="utf-8")
    with pytest.raises(SystemExit, match="escapes the authority root"):
        workflow_cli._load_workflow_config(root)


def test_workspace_registry_remains_user_owned_during_managed_upgrade(
    tmp_path: Path,
) -> None:
    root = workspace_fixture(tmp_path)
    config_path = root / ".project-workflow" / "config.json"
    before = config_path.read_bytes()

    outputs, _executables = workflow_cli._managed_asset_upgrade_outputs(
        root,
        "codex",
    )

    assert ".project-workflow/config.json" not in outputs
    assert config_path.read_bytes() == before


def test_doctor_rejects_competing_child_workflow_state(tmp_path: Path) -> None:
    root = workspace_fixture(tmp_path)
    (root / "next" / ".project-workflow").mkdir()

    issues = workflow_cli.run_doctor(root)

    conflict = [issue for issue in issues if issue.code == "PW_WORKSPACE_AUTHORITY_CONFLICT"]
    assert len(conflict) == 1
    assert "non-authority repository 'next'" in conflict[0].message


def test_workspace_scope_and_repository_evidence_are_lifecycle_gates(
    tmp_path: Path,
) -> None:
    root = workspace_fixture(tmp_path)
    assert "- Primary repository: workspace" in workflow_cli._requirements_template(
        "TASK-001",
        "Workspace Task",
        root=root,
    )
    assert (
        "| workspace | not recorded | not recorded | not recorded | not recorded |"
        in workflow_cli._implementation_template(
            "TASK-001",
            "Workspace Task",
            root=root,
        )
    )
    fix_template = workflow_cli._fix_template(
        "FIX-001",
        "Workspace Fix",
        root=root,
    )
    assert "- Primary repo: workspace" in fix_template
    assert (
        "| workspace | not recorded | not recorded | not recorded | not recorded |" in fix_template
    )
    assert workflow_cli._repository_scope_values(fix_template) == (
        "workspace",
        ("workspace",),
    )
    assert "- Primary repository: workspace" in workflow_cli._epic_child_requirements_template(
        "TASK-002",
        "Workspace Child",
        "AC1",
        root=root,
    )
    requirements = """\
# Requirements

## Repository Scope

- Primary repository: next
- Repositories touched: next, email
"""
    incomplete_implementation = """\
## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| next | codex/work | not recorded | not recorded | evidence/next.txt |
"""

    assert workflow_cli._repository_scope_issues(root, requirements) == []
    issues = workflow_cli._repository_evidence_issues(
        root,
        requirements,
        incomplete_implementation,
    )
    assert any("add Repository Evidence rows for: email" in issue for issue in issues)
    assert any("repository `next` must record validation evidence" in issue for issue in issues)

    complete_implementation = incomplete_implementation.replace(
        "| next | codex/work | not recorded | not recorded | evidence/next.txt |",
        "| next | codex/work | pytest | parent PR pending | evidence/next.txt |\n"
        "| email | not applicable | lint | no delivery authorized | evidence/email.txt |",
    )
    assert (
        workflow_cli._repository_evidence_issues(
            root,
            requirements,
            complete_implementation,
        )
        == []
    )


def test_focused_workspace_status_attributes_evidence_to_touched_repositories(
    tmp_path: Path,
) -> None:
    root = workspace_fixture(tmp_path)
    task_dir = root / ".project-workflow" / "tasks" / "TASK-001-Cross-Repo"
    task_dir.mkdir(parents=True)
    (root / ".project-workflow" / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Docs |\n"
        "|---|---|---|---|\n"
        "| TASK-001 | Cross Repo | In Progress | "
        "tasks/TASK-001-Cross-Repo/IMPLEMENTATION.md |\n",
        encoding="utf-8",
    )
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n"
        "## Repository Scope\n\n"
        "- Primary repository: next\n"
        "- Repositories touched: next, email\n",
        encoding="utf-8",
    )
    (task_dir / "IMPLEMENTATION.md").write_text(
        "## Repository Evidence\n\n"
        "| Repository | Branch / PR | Validation | Delivery | Evidence |\n"
        "| ---------- | ----------- | ---------- | -------- | -------- |\n"
        "| next | codex/work | pytest | parent integration pending | evidence/next.txt |\n"
        "| email | not applicable | lint | no delivery authorized | evidence/email.txt |\n",
        encoding="utf-8",
    )

    snapshot = workflow_cli.build_operational_status_snapshot(
        root,
        focus_id="TASK-001",
    )

    assert [repository.repository_id for repository in snapshot.repositories] == [
        "next",
        "email",
    ]
    next_evidence = {fact.key: fact.value for fact in snapshot.repositories[0].evidence}
    assert next_evidence["primary_work"] == ("TASK-001",)
    assert next_evidence["validation"] == ("TASK-001: pytest",)
    assert next_evidence["delivery"] == ("TASK-001: parent integration pending",)
    assert any(source.kind == "repository-evidence" for source in snapshot.repositories[0].sources)
    mismatch = next(
        finding
        for finding in snapshot.findings
        if finding.code == "PW_STATUS_WORKSPACE_REPOSITORY_BRANCH_MISMATCH"
        and "'next'" in finding.message
    )
    assert "'main'" in mismatch.message
    assert "'codex/work'" in mismatch.message


def test_disposable_workspace_cli_journey_reaches_complete_with_retained_proof(
    tmp_path: Path,
) -> None:
    receipt = run_disposable_workspace_cli_journey(tmp_path / "cli-journey")

    assert receipt["lifecycle"]["final_status"] == "Complete"
    assert (
        receipt["source"]["canonical_generated_runtime_sha256"]
        == receipt["source"]["generated_helper_sha256"]
    )
    assert receipt["workspace"]["child_workflow_state_created"] is False
    assert receipt["status_observation"]["before_after_read_only_git_state_equal"] is True
    assert (
        receipt["git_mutation_boundary"]["heads_and_branches_unchanged_by_workflow_lifecycle"]
        is True
    )
    assert receipt["git_mutation_boundary"]["commit_push_merge_release_deploy_performed"] is False
    assert set(receipt["handoff_artifacts"]) == {
        "requirements",
        "implementation",
        "tracker",
        "focused_status",
        "selected_status",
        "repository_evidence",
        "all_task_artifacts",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run and retain the disposable Project Workflow workspace CLI journey."
    )
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = run_disposable_workspace_cli_journey(args.output_root)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(args.receipt)


if __name__ == "__main__":
    main()
