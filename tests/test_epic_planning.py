from __future__ import annotations

import json
from pathlib import Path

from project_workflow import cli as workflow_cli
from tests.workflow_test_support import (
    ready_implementation,
    ready_requirements,
    run_project,
    write_decomposition_plan,
    write_epic_contract,
    write_namespace_config,
)


def test_epic_decompose_preserves_source_ac_ids_in_notes(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Mapped Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    initialized_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert (
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |" in initialized_tracker
    )
    assert (epic_dir / "EPIC-CONTRACT.md").exists()
    initialized_map = (epic_dir / "ACCEPTANCE-MAP.md").read_text(encoding="utf-8")
    assert "| AC1 | ____ | None | None | None | Unmapped |" in initialized_map
    initialized_retro = (epic_dir / "RETRO.md").read_text(encoding="utf-8")
    assert "## Lessons" in initialized_retro
    assert "## Missed In-Scope Work" in initialized_retro

    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Mapped Epic",
            [
                "- AC1: First epic outcome is delivered.",
                "- AC2: Second epic outcome is delivered.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Mapped Epic", ac_ids=["AC1", "AC2"])

    decompose = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-001", "--limit", "2"],
        cwd=tmp_path,
    )
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr
    assert "Parent AC coverage mapped: AC1, AC2" in decompose.stdout

    epic_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-001 | First epic outcome is delivered | Proposed | Task | AC1 |" in epic_tracker
    assert "| TASK-002 | Second epic outcome is delivered | Proposed | Task | AC2 |" in epic_tracker
    assert "Covers AC1; Prefix TASK:" in epic_tracker
    assert "Covers AC2; Prefix TASK:" in epic_tracker
    assert "Generated from REQUIREMENTS.md" in epic_tracker
    decomposition_plan = (epic_dir / "DECOMPOSITION.md").read_text(encoding="utf-8")
    assert (
        "| TASK-001 | First epic outcome is delivered | AC1 | Generated from REQUIREMENTS.md |"
        in decomposition_plan
    )
    assert (
        "| TASK-002 | Second epic outcome is delivered | AC2 | Generated from REQUIREMENTS.md |"
        in decomposition_plan
    )
    acceptance_map = (epic_dir / "ACCEPTANCE-MAP.md").read_text(encoding="utf-8")
    assert (
        "| AC1 | First epic outcome is delivered. | TASK-001 (Proposed) | None | None | Mapped - evidence pending |"
        in acceptance_map
    )
    assert (
        "| AC2 | Second epic outcome is delivered. | TASK-002 (Proposed) | None | None | Mapped - evidence pending |"
        in acceptance_map
    )


def test_epic_decompose_requires_ready_epic_contract(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Contract Required"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Contract Required",
            ["- AC1: Contract gate blocks decomposition."],
        ),
        encoding="utf-8",
    )

    decompose = run_project(["epic", "decompose", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert decompose.returncode != 0
    assert "EPIC-CONTRACT.md" in decompose.stderr
    assert "placeholder" in decompose.stderr


def test_doctor_fails_approved_epic_missing_contract(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Missing Contract"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Missing Contract",
            ["- AC1: Contract doctor failure is reported."],
        ),
        encoding="utf-8",
    )
    (epic_dir / "EPIC-CONTRACT.md").unlink()

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "epic contract: EPIC-CONTRACT.md is missing" in doctor.stdout


def test_epic_decompose_prefers_owner_proposed_child_work_plan(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Owner Plan"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))

    requirements_text = workflow_cli._remove_markdown_section(
        ready_requirements(
            "EPIC-001",
            "Owner Plan",
            ["- AC1: Owner-planned child work is authorized."],
        ),
        workflow_cli.OWNER_APPROVAL_HEADING,
    )
    requirements_text = (
        requirements_text + "\n## Proposed Child Work\n\n"
        "| Proposed Child | Parent ACs | Purpose |\n"
        "| --- | --- | --- |\n"
        "| Owner Named Child | AC1 | Use the owner-reviewed child title. |\n"
    )
    requirements_text = workflow_cli._requirements_with_approval_envelope(
        requirements_text,
        approved_by="Test Owner",
        source="Owner approved fixture requirements with decomposition plan.",
        decomposition=True,
        implementation=False,
    )
    (epic_dir / "REQUIREMENTS.md").write_text(requirements_text, encoding="utf-8")
    write_epic_contract(epic_dir, title="Owner Plan")

    decompose = run_project(["epic", "decompose", "--epic-id", "EPIC-001"], cwd=tmp_path)
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr

    epic_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    decomposition_plan = (epic_dir / "DECOMPOSITION.md").read_text(encoding="utf-8")
    assert "| TASK-001 | Owner Named Child | Proposed | Task | AC1 |" in epic_tracker
    assert "| TASK-001 | Owner Named Child | AC1 | Proposed Child Work |" in decomposition_plan


def test_epic_approve_blocks_child_outside_decomposition_plan(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Manual Drift"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Manual Drift",
            ["- AC1: Planned child work is enforced."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Manual Drift")
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Planned Child", "Parent ACs": "AC1"}],
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-002 | Invented Child | Proposed | Task | AC1 |  |  | Manually invented row |\n",
        encoding="utf-8",
    )

    approve = run_project(
        ["epic", "approve", "--epic-id", "EPIC-001", "--id", "TASK-002"],
        cwd=tmp_path,
    )
    assert approve.returncode != 0
    assert "outside the approved decomposition authority" in approve.stderr
    assert "TASK-002 is outside DECOMPOSITION.md" in approve.stderr


def test_epic_amend_authorizes_child_outside_decomposition_plan(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Approved Amendment"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    assert (epic_dir / workflow_cli.EPIC_AMENDMENTS_FILENAME).exists()
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Approved Amendment",
            ["- AC1: Planned child work is enforced."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Approved Amendment")
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Planned Child", "Parent ACs": "AC1"}],
    )

    amend = run_project(
        [
            "epic",
            "amend",
            "--epic-id",
            "EPIC-001",
            "--id",
            "TASK-002",
            "--title",
            "Reactive Fix",
            "--parent-acs",
            "AC1",
            "--approved-by",
            "Test Owner",
            "--reason",
            "Owner approved reactive fix after drift audit.",
            "--source",
            "Owner approval in test thread.",
        ],
        cwd=tmp_path,
    )
    assert amend.returncode == 0, amend.stdout + amend.stderr
    amendments_text = (epic_dir / workflow_cli.EPIC_AMENDMENTS_FILENAME).read_text(encoding="utf-8")
    assert "| TASK-002 | Reactive Fix | AC1 | Test Owner |" in amendments_text
    tracker_text = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert "| TASK-002 | Reactive Fix | Proposed | Task | AC1 |" in tracker_text

    approve = run_project(
        ["epic", "approve", "--epic-id", "EPIC-001", "--id", "TASK-002"],
        cwd=tmp_path,
    )
    assert approve.returncode == 0, approve.stdout + approve.stderr

    scaffold = run_project(
        ["epic", "scaffold-child", "--epic-id", "EPIC-001", "--id", "TASK-002"],
        cwd=tmp_path,
    )
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr


def test_doctor_fails_active_epic_child_without_decomposition_authority(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Manual Active Drift"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Manual Active Drift",
            ["- AC1: Active child rows are plan-authorized."],
        ),
        encoding="utf-8",
    )
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Manual Active Child | In Progress | Task | AC1 |  |  | Manual row |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "TASK-001 decomposition authority" in doctor.stdout
    assert "DECOMPOSITION.md is missing" in doctor.stdout


def test_epic_decompose_uses_configured_mixed_prefixes_and_prefix_override(
    tmp_path: Path,
) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    write_namespace_config(tmp_path)

    epic = run_project(["epic", "init", "--title", "Mixed App Work"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Mixed App Work",
            [
                "- AC1: MCP server payload contract is delivered.",
                "- AC2: Frontend UI route interaction is delivered.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Mixed App Work", ac_ids=["AC1", "AC2"])

    decompose = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-001", "--limit", "2"],
        cwd=tmp_path,
    )
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr

    epic_tracker = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert (
        "| MCP-001 | MCP server payload contract is delivered | Proposed | Task | AC1 |"
        in epic_tracker
    )
    assert (
        "| UI-001 | Frontend UI route interaction is delivered | Proposed | Task | AC2 |"
        in epic_tracker
    )
    assert "Prefix MCP: " in epic_tracker
    assert "Prefix UI: " in epic_tracker

    second_epic = run_project(["epic", "init", "--title", "Forced Mcp Work"], cwd=tmp_path)
    assert second_epic.returncode == 0, second_epic.stdout + second_epic.stderr
    second_epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-002-*"))
    (second_epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-002",
            "Forced Mcp Work",
            [
                "- AC1: Frontend UI fixture is delivered.",
                "- AC2: Workflow prompt fixture is delivered.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(
        second_epic_dir,
        epic_id="EPIC-002",
        title="Forced Mcp Work",
        ac_ids=["AC1", "AC2"],
    )

    forced = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-002", "--limit", "2", "--prefix", "MCP"],
        cwd=tmp_path,
    )
    assert forced.returncode == 0, forced.stdout + forced.stderr
    forced_tracker = (second_epic_dir / "TRACKER.md").read_text(encoding="utf-8")
    assert (
        "| MCP-002 | Frontend UI fixture is delivered | Proposed | Task | AC1 |" in forced_tracker
    )
    assert (
        "| MCP-003 | Workflow prompt fixture is delivered | Proposed | Task | AC2 |"
        in forced_tracker
    )
    assert "Prefix MCP: forced by --prefix" in forced_tracker


def test_epic_decompose_reports_unmapped_parent_ac_ids(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Coverage Gap"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Coverage Gap",
            [
                "- AC1: First epic outcome is delivered.",
                "- AC2: Second epic outcome is delivered.",
                "- AC3: Third epic outcome is delivered.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Coverage Gap", ac_ids=["AC1", "AC2", "AC3"])

    decompose = run_project(
        ["epic", "decompose", "--epic-id", "EPIC-001", "--limit", "2"],
        cwd=tmp_path,
    )
    assert decompose.returncode == 0, decompose.stdout + decompose.stderr
    assert "WARNING: Unmapped parent ACs after decomposition: AC3" in decompose.stdout


def test_epic_child_scaffold_carries_parent_ac_sections(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Parent Evidence"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Parent Evidence",
            [
                "- AC1: First parent evidence path is scaffolded.",
                "- AC3: Third parent evidence path is scaffolded.",
            ],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Parent Evidence", ac_ids=["AC1", "AC3"])
    contract_path = epic_dir / workflow_cli.EPIC_CONTRACT_FILENAME
    contract_text = contract_path.read_text(encoding="utf-8")
    contract_text = (
        contract_text.replace(
            "- Tracker rows without matching contract and decomposition authority.\n",
            "- Tracker rows without matching contract and decomposition authority or a passing build;\n"
            "  public package provenance must identify the exact source commit.\n",
        )
        .replace(
            "- Parent AC IDs remain stable across child work.\n",
            "- Parent AC IDs remain stable across child work in `REQUIREMENTS.md`\n"
            "  and `IMPLEMENTATION.md` child charters.\n",
        )
        .replace(
            "- Workflow markdown artifacts in this epic folder.\n",
            "- Workflow markdown artifacts in this epic folder, including exact-draft play\n"
            "  and ordinary public-source play.\n",
        )
    )
    contract_path.write_text(contract_text, encoding="utf-8")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Child Evidence | Approved | Task | AC1, AC3 |  |  | Covers AC1, AC3 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Child Evidence", "Parent ACs": "AC1, AC3"}],
    )

    scaffold = run_project(
        ["epic", "scaffold-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr

    child_dir = epic_dir / "TASK-001-Child-Evidence"
    requirements_text = (child_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    implementation_text = (child_dir / "IMPLEMENTATION.md").read_text(encoding="utf-8")

    assert "- Parent AC Coverage: AC1, AC3" in requirements_text
    assert "## Parent AC Coverage" in implementation_text
    assert "- AC1, AC3" in implementation_text
    assert "## Child Charter" in requirements_text
    assert "### Invalid Substitutes" in requirements_text
    assert "### Parent AC Proof Ownership" in requirements_text
    assert "## Child Charter" in implementation_text
    assert "## Parent AC Evidence" in implementation_text
    assert "AC1 / parent AC(s) AC1, AC3" in implementation_text
    for child_text in (requirements_text, implementation_text):
        assert (
            "- Parent AC IDs remain stable across child work in `REQUIREMENTS.md` "
            "and `IMPLEMENTATION.md` child charters."
        ) in child_text
        assert (
            "- Tracker rows without matching contract and decomposition authority or a passing build; "
            "public package provenance must identify the exact source commit."
        ) in child_text
        assert (
            "- Workflow markdown artifacts in this epic folder, including exact-draft play "
            "and ordinary public-source play."
        ) in child_text
        assert (
            "- Parent AC IDs remain stable across child work in `REQUIREMENTS.md`\n"
            not in child_text
        )
    evidence = json.loads(
        (child_dir / workflow_cli.STRUCTURED_EVIDENCE_FILENAME).read_text(encoding="utf-8")
    )
    assert evidence["claims"] == []

    standalone = run_project(
        ["task", "init", "--title", "Standalone Quiet", "--update-tracker"],
        cwd=tmp_path,
    )
    assert standalone.returncode == 0, standalone.stdout + standalone.stderr
    standalone_dir = next(
        p
        for p in (tmp_path / ".project-workflow" / "tasks").glob("TASK-*-Standalone-Quiet")
        if p.is_dir()
    )
    standalone_impl = (standalone_dir / "IMPLEMENTATION.md").read_text(encoding="utf-8")
    assert "## Parent AC Coverage" not in standalone_impl
    assert "## Parent AC Evidence" not in standalone_impl


def test_contract_bullet_parser_joins_flat_list_continuations() -> None:
    contract_text = (
        "# Epic Contract\n\n"
        "## Invariants\n\n"
        "- Indented continuation stays with\n"
        "  its logical bullet.\n"
        "* Lazy continuation also stays with\n"
        "its logical bullet.\n"
        "+ Plus markers remain supported.\n\n"
        "Introductory prose after a blank is not inherited.\n"
        "- ____\n\n"
        "## Artifact Targets\n\n"
        "- A later section is outside the invariant boundary.\n"
    )

    assert workflow_cli._contract_section_bullets(contract_text, "Invariants") == [
        "Indented continuation stays with its logical bullet.",
        "Lazy continuation also stays with its logical bullet.",
        "Plus markers remain supported.",
    ]


def test_active_epic_child_rejects_legacy_truncated_contract_charter(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Wrapped Contract"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr
    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Wrapped Contract",
            ["- AC1: Wrapped contract inheritance remains complete."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Wrapped Contract", ac_ids=["AC1"])
    contract_path = epic_dir / workflow_cli.EPIC_CONTRACT_FILENAME
    contract_text = contract_path.read_text(encoding="utf-8").replace(
        "- Parent AC IDs remain stable across child work.\n",
        "- Parent AC IDs remain stable across the parent contract\n"
        "  and every active child charter.\n",
    )
    contract_path.write_text(contract_text, encoding="utf-8")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Wrapped Child | Approved | Task | AC1 | tasks/EPIC-001-Wrapped-Contract/TASK-001-Wrapped-Child/IMPLEMENTATION.md |  | Covers AC1 |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "TASK-001", "Title": "Wrapped Child", "Parent ACs": "AC1"}],
    )
    scaffold = run_project(
        ["epic", "scaffold-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr
    tracker_path = epic_dir / "TRACKER.md"
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace("| Approved |", "| In Progress |"),
        encoding="utf-8",
    )

    child_dir = epic_dir / "TASK-001-Wrapped-Child"
    full_bullet = (
        "Parent AC IDs remain stable across the parent contract and every active child charter."
    )
    legacy_fragment = "Parent AC IDs remain stable across the parent contract"
    charter = workflow_cli._format_child_charter_from_contract(
        epic_dir=epic_dir,
        parent_ac_coverage="AC1",
    ).replace(full_bullet, legacy_fragment)
    child_requirements = ready_requirements(
        "TASK-001",
        "Wrapped Child",
        ["- AC1: The complete inherited contract is implemented."],
    )
    child_requirements = workflow_cli._remove_markdown_section(
        child_requirements,
        workflow_cli.OWNER_APPROVAL_HEADING,
    )
    child_requirements = child_requirements.replace("## Goal\n\n", charter + "## Goal\n\n")
    child_implementation = ready_implementation("AC1").replace(
        "## User Story\n\n",
        charter + "## User Story\n\n",
    )
    requirements_path = child_dir / "REQUIREMENTS.md"
    implementation_path = child_dir / "IMPLEMENTATION.md"
    requirements_path.write_text(child_requirements, encoding="utf-8")
    implementation_path.write_text(child_implementation, encoding="utf-8")

    ready_child = run_project(
        ["epic", "ready-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert ready_child.returncode != 0
    assert "legacy truncated `Inherited Invariants` bullet" in ready_child.stderr
    assert legacy_fragment in ready_child.stderr

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode != 0
    assert "legacy truncated `Inherited Invariants` bullet" in doctor.stdout

    requirements_path.write_text(
        requirements_path.read_text(encoding="utf-8").replace(legacy_fragment, full_bullet),
        encoding="utf-8",
    )
    implementation_path.write_text(
        implementation_path.read_text(encoding="utf-8").replace(legacy_fragment, full_bullet),
        encoding="utf-8",
    )
    ready_child = run_project(
        ["epic", "ready-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        cwd=tmp_path,
    )
    assert ready_child.returncode == 0, ready_child.stdout + ready_child.stderr
    doctor = run_project(["doctor"], cwd=tmp_path)
    assert "legacy truncated `Inherited Invariants` bullet" not in doctor.stdout

    requirements_path.write_text(
        requirements_path.read_text(encoding="utf-8").replace(full_bullet, legacy_fragment),
        encoding="utf-8",
    )
    implementation_path.write_text(
        implementation_path.read_text(encoding="utf-8").replace(full_bullet, legacy_fragment),
        encoding="utf-8",
    )
    tracker_path.write_text(
        tracker_path.read_text(encoding="utf-8").replace("| In Progress |", "| Complete |"),
        encoding="utf-8",
    )
    doctor = run_project(["doctor"], cwd=tmp_path)
    assert "legacy truncated `Inherited Invariants` bullet" not in doctor.stdout


def test_epic_child_scaffold_preserves_configured_task_prefix(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr
    write_namespace_config(tmp_path)

    epic = run_project(["epic", "init", "--title", "Custom Prefix Child"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "REQUIREMENTS.md").write_text(
        ready_requirements(
            "EPIC-001",
            "Custom Prefix Child",
            ["- AC1: Custom prefix child is scaffolded."],
        ),
        encoding="utf-8",
    )
    write_epic_contract(epic_dir, title="Custom Prefix Child")
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Parent ACs | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| UI-008 | Widget Interaction | Approved | Task | AC1 |  |  | Prefix UI: owner selected UI child |\n",
        encoding="utf-8",
    )
    write_decomposition_plan(
        epic_dir,
        rows=[{"ID": "UI-008", "Title": "Widget Interaction", "Parent ACs": "AC1"}],
    )

    scaffold = run_project(
        ["epic", "scaffold-child", "--epic-id", "EPIC-001", "--id", "UI-008"],
        cwd=tmp_path,
    )
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr

    child_dir = epic_dir / "UI-008-Widget-Interaction"
    assert child_dir.exists()
    requirements_text = (child_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    implementation_text = (child_dir / "IMPLEMENTATION.md").read_text(encoding="utf-8")
    tracker_text = (epic_dir / "TRACKER.md").read_text(encoding="utf-8")

    assert "- Task: UI-008" in requirements_text
    assert "- Task: UI-008" in implementation_text
    assert (
        "| UI-008 | Widget Interaction | In Progress | Task | AC1 | tasks/EPIC-001-Custom-Prefix-Child/UI-008-Widget-Interaction/IMPLEMENTATION.md |"
        in tracker_text
    )


def test_doctor_accepts_legacy_epic_tracker_schema(tmp_path: Path) -> None:
    init = run_project(["init"], cwd=tmp_path)
    assert init.returncode == 0, init.stderr

    epic = run_project(["epic", "init", "--title", "Legacy Epic"], cwd=tmp_path)
    assert epic.returncode == 0, epic.stdout + epic.stderr

    epic_dir = next((tmp_path / ".project-workflow" / "tasks").glob("EPIC-001-*"))
    (epic_dir / "TRACKER.md").write_text(
        "# Stories\n\n"
        "| ID | Title | Status | Type | Docs | Branch | Notes |\n"
        "|---|---|---|---|---|---|---|\n"
        "| TASK-001 | Legacy Child | Proposed | Task |  |  | Covers AC1 |\n",
        encoding="utf-8",
    )

    doctor = run_project(["doctor"], cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert "Epic tracker schema mismatch" not in doctor.stdout
