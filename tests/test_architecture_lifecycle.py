from __future__ import annotations

from pathlib import Path

import pytest

from project_workflow import coordination as workflow_cli
from project_workflow.architecture import architecture_authority_identity
from tests.test_architecture_control import SPINE, impact
from tests.workflow_test_support import ready_implementation, ready_requirements, run_project


def replace_impact(implementation: str, replacement: str) -> str:
    start = implementation.index("## Architecture Impact")
    end = implementation.index("\n## ", start + 3)
    return implementation[:start] + replacement.rstrip() + "\n" + implementation[end:]


def initialized_task(root: Path, title: str) -> Path:
    assert run_project(["init"], cwd=root).returncode == 0
    created = run_project(["task", "init", "--title", title, "--update-tracker"], cwd=root)
    assert created.returncode == 0, created.stdout + created.stderr
    task_dir = next((root / ".project-workflow/tasks").glob("TASK-001-*"))
    (task_dir / "REQUIREMENTS.md").write_text(
        ready_requirements("TASK-001", title), encoding="utf-8"
    )
    return task_dir


def write_spine(root: Path) -> Path:
    authority = root / "docs/architecture.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text(SPINE, encoding="utf-8")
    return authority


def move_to_analysing(root: Path) -> None:
    result = run_project(["task", "status", "--id", "TASK-001", "--to", "Analysing"], cwd=root)
    assert result.returncode == 0, result.stdout + result.stderr


def test_local_established_pattern_reaches_ready_without_material_ceremony(
    tmp_path: Path,
) -> None:
    task_dir = initialized_task(tmp_path, "Local Pattern")
    write_spine(tmp_path)
    implementation = replace_impact(ready_implementation(), impact("local"))
    (task_dir / "IMPLEMENTATION.md").write_text(implementation, encoding="utf-8")
    move_to_analysing(tmp_path)

    ready = run_project(["task", "status", "--id", "TASK-001", "--to", "Ready"], cwd=tmp_path)

    assert ready.returncode == 0, ready.stdout + ready.stderr
    assert "Analysing -> Ready" in ready.stdout
    assert "sha256:" not in implementation
    assert "ADR" not in implementation


def test_material_stale_authority_fails_closed_at_ready(tmp_path: Path) -> None:
    task_dir = initialized_task(tmp_path, "Material Boundary")
    write_spine(tmp_path)
    implementation = replace_impact(
        ready_implementation(), impact("material", identity="sha256:" + "0" * 64)
    )
    (task_dir / "IMPLEMENTATION.md").write_text(implementation, encoding="utf-8")
    move_to_analysing(tmp_path)

    ready = run_project(["task", "status", "--id", "TASK-001", "--to", "Ready"], cwd=tmp_path)

    assert ready.returncode != 0
    assert "architecture authority is stale or missing" in ready.stderr


def test_force_cannot_bypass_material_architecture_readiness(tmp_path: Path) -> None:
    task_dir = initialized_task(tmp_path, "Forced Material Boundary")
    write_spine(tmp_path)
    implementation = replace_impact(
        ready_implementation(), impact("material", identity="sha256:" + "0" * 64)
    )
    (task_dir / "IMPLEMENTATION.md").write_text(implementation, encoding="utf-8")
    move_to_analysing(tmp_path)

    forced = run_project(
        [
            "task",
            "status",
            "--id",
            "TASK-001",
            "--to",
            "Ready",
            "--force",
            "--reason",
            "attempted architecture bypass",
        ],
        cwd=tmp_path,
    )

    assert forced.returncode != 0
    assert "architecture authority is stale or missing" in forced.stderr


def test_material_review_requires_exact_candidate_conformance(tmp_path: Path) -> None:
    task_dir = initialized_task(tmp_path, "Material Review")
    authority = write_spine(tmp_path)
    identity = architecture_authority_identity(authority)
    implementation = replace_impact(ready_implementation(), impact("material", identity=identity))
    implementation += """
## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | fixture | targeted checks pass | local only | fixture evidence |
"""
    implementation_path = task_dir / "IMPLEMENTATION.md"
    implementation_path.write_text(implementation, encoding="utf-8")
    move_to_analysing(tmp_path)
    for status in ("Ready", "In Progress", "Testing"):
        result = run_project(["task", "status", "--id", "TASK-001", "--to", status], cwd=tmp_path)
        assert result.returncode == 0, result.stdout + result.stderr

    blocked = run_project(["task", "status", "--id", "TASK-001", "--to", "Review"], cwd=tmp_path)
    assert blocked.returncode != 0
    assert "Architecture Conformance Verdict: Pass" in blocked.stderr

    candidate = "git:" + "b" * 40
    receipt = task_dir / "architecture-conformance-receipt.md"
    receipt.write_text(
        f"# Receipt\n\n- Candidate: {candidate}\n- Verdict: Pass\n", encoding="utf-8"
    )
    implementation_path.write_text(
        implementation
        + f"""
## Architecture Conformance

- Authority identity: {identity}
- Candidate: {candidate}
- Mechanical checks: candidate={candidate}; receipt=.project-workflow/tasks/TASK-001-Material-Review/architecture-conformance-receipt.md
- Deviations: None
- Verdict: Pass
""",
        encoding="utf-8",
    )
    review = run_project(["task", "status", "--id", "TASK-001", "--to", "Review"], cwd=tmp_path)
    assert review.returncode == 0, review.stdout + review.stderr


def test_epic_child_complete_rechecks_material_conformance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    epic_dir = tmp_path / ".project-workflow/tasks/EPIC-001-Architecture"
    child_dir = epic_dir / "TASK-001-Material-Child"
    child_dir.mkdir(parents=True)
    authority = write_spine(tmp_path)
    identity = architecture_authority_identity(authority)
    implementation = impact("material", identity=identity)
    implementation += "\n## Parent AC Evidence\n\n- AC1: Exact candidate evidence.\n"
    implementation += """
## Architecture Conformance

- Authority identity: PLACEHOLDER
- Candidate: x
- Mechanical checks: trust me
- Deviations: None
- Verdict: Pass
"""
    (child_dir / "IMPLEMENTATION.md").write_text(
        implementation.replace("PLACEHOLDER", identity), encoding="utf-8"
    )
    (child_dir / "REQUIREMENTS.md").write_text("# Requirements\n", encoding="utf-8")
    tracker = epic_dir / "TRACKER.md"
    tracker.write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Material Child | Review | Task | AC1 | tasks/EPIC-001-Architecture/TASK-001-Material-Child/IMPLEMENTATION.md | | Covers AC1 |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(workflow_cli, "_task_ready_issues_for_paths", lambda **_kwargs: [])
    monkeypatch.setattr(workflow_cli, "_structured_evidence_issues", lambda **_kwargs: [])
    monkeypatch.setattr(workflow_cli, "_owner_acceptance_completion_issues", lambda _path: [])
    monkeypatch.setattr(workflow_cli, "_repository_evidence_issues", lambda *_args: [])

    with pytest.raises(SystemExit) as blocked:
        workflow_cli._update_epic_child_status(
            root=tmp_path,
            epic_tracker_path=tracker,
            row_id="TASK-001",
            new_status="Complete",
            force=False,
            reason=None,
        )

    assert "Candidate must be an exact" in str(blocked.value)
