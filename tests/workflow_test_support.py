from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from project_workflow import cli as workflow_cli

REPO_ROOT = Path(__file__).resolve().parents[1]

PROJECT_CMD = [sys.executable, "-m", "project_workflow.cli"]


def find_uvx_executable() -> str | None:
    candidates = (
        shutil.which("uvx"),
        "/opt/homebrew/bin/uvx",
        "/usr/local/bin/uvx",
        str(Path.home() / ".local" / "bin" / "uvx"),
    )
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def run_project(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*PROJECT_CMD, *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _run_git_for_test(root: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def init_git_fixture(root: Path) -> None:
    commands = (
        ["git", "init"],
        ["git", "config", "user.email", "tests@example.com"],
        ["git", "config", "user.name", "Project Workflow Tests"],
        ["git", "add", "."],
        ["git", "commit", "-m", "fixture"],
    )
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr


def commit_git_fixture(root: Path, message: str) -> None:
    for command in (["git", "add", "."], ["git", "commit", "-m", message]):
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr


def write_namespace_config(root: Path) -> None:
    (root / ".project-workflow" / "config.json").write_text(
        "{\n"
        '  "task_id_prefixes": ["TASK", "UI", "MCP", "DEV", "WF"],\n'
        '  "default_task_id_prefix": "WF",\n'
        '  "prefix_guidance": {\n'
        '    "TASK": "General task work.",\n'
        '    "UI": "Frontend, widget, component, route, layout, visual, interaction, UX.",\n'
        '    "MCP": "MCP server, app tool, payload contract, fixture, orchestration.",\n'
        '    "DEV": "Local development, debug tooling, tunnels, build scripts.",\n'
        '    "WF": "Project workflow conventions, process automation, prompts, agent guidance."\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )


def write_unique_id_config(root: Path) -> None:
    (root / ".project-workflow" / "config.json").write_text(
        "{\n"
        '  "task_id_prefixes": ["TASK", "UI", "MCP", "DEV", "WF"],\n'
        '  "default_task_id_prefix": "WF",\n'
        '  "id_generation": {\n'
        '    "tasks": "unique",\n'
        '    "epics": "unique",\n'
        '    "fixes": "unique",\n'
        '    "backlog": "unique"\n'
        "  },\n"
        '  "unique_id_length": 5,\n'
        '  "prefix_guidance": {\n'
        '    "TASK": "General task work.",\n'
        '    "UI": "Frontend, widget, component, route, layout, visual, interaction, UX.",\n'
        '    "MCP": "MCP server, app tool, payload contract, fixture, orchestration.",\n'
        '    "DEV": "Local development, debug tooling, tunnels, build scripts.",\n'
        '    "WF": "Project workflow conventions, process automation, prompts, agent guidance."\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )


def add_accepted_doctor_warnings(root: Path, entries: list[object]) -> None:
    config_path = root / ".project-workflow" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["accepted_doctor_warnings"] = entries
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def assert_unique_id(value: str, prefix: str) -> None:
    match = re.fullmatch(rf"{re.escape(prefix)}-([0-9A-Z]{{5}})", value)
    assert match, value
    assert not match.group(1).isdigit()


def ready_requirements(task_id: str, title: str, ac_lines: list[str] | None = None) -> str:
    criteria = "\n".join(ac_lines or ["- AC1: Ready outcome is delivered."])
    requirements_text = (
        "# Requirements\n\n"
        "## Summary\n\n"
        f"- Task: {task_id}\n"
        f"- Title: {title}\n\n"
        "## Goal\n\n"
        "- Deliver the requested ready outcome.\n\n"
        "## Non-Goals\n\n"
        "- Do not expand scope beyond this fixture.\n\n"
        "## Users & Context\n\n"
        "- Maintainers need a ready workflow artifact.\n\n"
        "## Requirements (Outcome-Focused)\n\n"
        "- The workflow artifact is specific enough to proceed.\n\n"
        "## Acceptance Criteria (Verifiable)\n\n"
        f"{criteria}\n\n"
        "## Open Questions (Answer Needed)\n\n"
        "- None.\n\n"
        "## Decisions (Resolved)\n\n"
        "- Proceed with the ready fixture.\n\n"
        "## Validation Plan\n\n"
        "- Run targeted workflow validation.\n"
    )
    return workflow_cli._requirements_with_approval_envelope(
        requirements_text,
        approved_by="Test Owner",
        source="Owner approved fixture requirements.",
        decomposition=task_id.startswith("EPIC-"),
        implementation=not task_id.startswith("EPIC-"),
    )


def ready_fix_text(fix_path: Path, *, hotfix: bool = False) -> str:
    text = fix_path.read_text(encoding="utf-8")
    text = text.replace(
        "State the bounded correction and restored outcome in one or two plain-language sentences.",
        "Restore successful export for supported accounts without adding a new export capability.",
    )
    values = (
        ("Report", "Observed or requested", "Export fails after the delivered release."),
        ("Report", "Expected", "Export completes for supported accounts."),
        ("Report", "Affected users or systems", "Users of account export."),
        ("Report", "Delivered baseline", "The accepted export release."),
        ("Report", "Report evidence", "Reproduction log in the report."),
        ("Routing", "Rationale", "One bounded correction to delivered behavior."),
        ("Routing", "Bounded correction", "Yes; no new product outcome."),
        ("Classification", "Type", "Regression"),
        ("Classification", "Mode", "Hotfix" if hotfix else "Normal"),
        ("Classification", "Severity", "High"),
        ("Classification", "Impact", "Affected users cannot export."),
        ("Classification", "Urgency", "Resolve before the next release."),
        ("Classification", "Owner", "Workflow maintainer"),
        ("Risk", "Risk level", "Medium"),
        ("Risk", "Risks", "Export behavior could regress for adjacent account shapes."),
        ("Risk", "Rollback or containment", "Revert the bounded patch."),
        ("Fix Plan", "Scope", "Restore the delivered export behavior."),
        ("Fix Plan", "Non-goals", "No new export formats."),
        ("Fix Plan", "Affected target", "Packaged and local workflow CLI."),
        ("Fix Plan", "Branch, PR, and evidence links", "Branch plus targeted test evidence."),
        ("Fix Plan", "Verification plan", "Run targeted regression and doctor checks."),
    )
    for heading, key, value in values:
        text = workflow_cli._replace_fix_field(text, heading, key, value)
    return text


def verified_fix_text(fix_path: Path) -> str:
    text = fix_path.read_text(encoding="utf-8")
    values = (
        ("Verification", "Delivered scope", "Bounded export correction only."),
        ("Verification", "Verification result", "Targeted checks passed."),
        ("Verification", "Adjacent behavior checked", "Small and large accounts passed."),
        ("Verification", "Regression evidence", "Automated regression test passed."),
        ("Verification", "Residual risk", "Low; rollback remains available."),
    )
    for heading, key, value in values:
        text = workflow_cli._replace_fix_field(text, heading, key, value)
    return text


def write_decomposition_plan(
    epic_dir: Path,
    *,
    epic_id: str = "EPIC-001",
    rows: list[dict[str, str]],
) -> None:
    requirements_text = (epic_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    (epic_dir / workflow_cli.DECOMPOSITION_PLAN_FILENAME).write_text(
        workflow_cli._format_decomposition_plan(
            epic_id=epic_id,
            requirements_text=requirements_text,
            rows=[
                {
                    "ID": row["ID"],
                    "Title": row["Title"],
                    "Parent ACs": row.get("Parent ACs", ""),
                    "Source": row.get("Source", "Test decomposition plan"),
                }
                for row in rows
            ],
        ),
        encoding="utf-8",
    )


def write_epic_contract(
    epic_dir: Path,
    *,
    epic_id: str = "EPIC-001",
    title: str = "Ready Epic",
    ac_ids: list[str] | None = None,
) -> None:
    ac_ids = ac_ids or ["AC1"]
    rows = "\n".join(
        f"| {ac_id} | TASK-001 | Parent AC evidence plus QA pass |" for ac_id in ac_ids
    )
    (epic_dir / workflow_cli.EPIC_CONTRACT_FILENAME).write_text(
        "# Epic Contract\n\n"
        "## Summary\n\n"
        f"- Epic: {epic_id}\n"
        f"- Title: {title}\n"
        "- Last updated: 2026-07-09\n\n"
        "## Sources of Truth\n\n"
        "- Owner-approved requirements and acceptance criteria.\n\n"
        "## Invalid Substitutes\n\n"
        "- Tracker rows without matching contract and decomposition authority.\n\n"
        "## Invariants\n\n"
        "- Parent AC IDs remain stable across child work.\n\n"
        "## Artifact Targets\n\n"
        "- Workflow markdown artifacts in this epic folder.\n\n"
        "## Parent AC Proof Ownership\n\n"
        "| Parent AC | Proof Owner | Required Evidence |\n"
        "| --- | --- | --- |\n"
        f"{rows}\n",
        encoding="utf-8",
    )


def write_structured_evidence(
    child_dir: Path,
    *,
    recipe: str = "visual-reference-fidelity",
    parent_ac: str = "AC1",
    invalid_substitutes: list[str] | None = None,
    evidence_artifact_hash: str | None = None,
) -> None:
    evidence_dir = child_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    artifact = evidence_dir / "visual-comparison.txt"
    artifact.write_text("rendered comparison evidence", encoding="utf-8")
    artifact_hash = evidence_artifact_hash or workflow_cli._sha256_file(artifact)
    child_dir.joinpath(workflow_cli.STRUCTURED_EVIDENCE_FILENAME).write_text(
        json.dumps(
            {
                "task_id": "TASK-001",
                "claims": [
                    {
                        "id": "CLM-001",
                        "parent_ac": parent_ac,
                        "claim": "Delivered surface matches the reference visual.",
                        "recipe": recipe,
                        "status": "pass",
                        "commit": "abc123",
                        "timestamp": "2026-07-09T00:00:00Z",
                        "reference_artifact": "reference/playground.png",
                        "delivered_artifact": "http://localhost:3000/widget",
                        "comparison_method": "browser screenshot comparison",
                        "evidence_artifact": "evidence/visual-comparison.txt",
                        "evidence_artifact_hash": artifact_hash,
                        "invalid_substitutes": invalid_substitutes or [],
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def write_runtime_structured_evidence(
    child_dir: Path,
    *,
    execution_target: str = "working/local",
    source_artifact: str = "local checkout",
) -> None:
    evidence_dir = child_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    artifact = evidence_dir / "runtime-target-source.txt"
    artifact.write_text("runtime target used local checkout", encoding="utf-8")
    child_dir.joinpath(workflow_cli.STRUCTURED_EVIDENCE_FILENAME).write_text(
        json.dumps(
            {
                "task_id": "TASK-001",
                "claims": [
                    {
                        "id": "CLM-001",
                        "parent_ac": "AC1",
                        "claim": "Runtime target used the expected source.",
                        "recipe": "runtime-target-source",
                        "status": "pass",
                        "commit": "abc123",
                        "timestamp": "2026-07-09T00:00:00Z",
                        "execution_target": execution_target,
                        "source_artifact": source_artifact,
                        "observation_method": "browser proof plus process inspection",
                        "target_used_source_proof": "runtime response included local checkout marker",
                        "evidence_artifact": "evidence/runtime-target-source.txt",
                        "evidence_artifact_hash": workflow_cli._sha256_file(artifact),
                        "invalid_substitutes": [],
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def ready_implementation(parent_ac: str | None = None, *, qa: bool = False) -> str:
    parent_sections = ""
    if parent_ac:
        parent_sections = (
            "## Parent AC Coverage\n\n"
            f"- {parent_ac}\n\n"
            "## Parent AC Evidence\n\n"
            f"- {parent_ac}: Targeted parent evidence recorded.\n\n"
        )
    qa_section = (
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n"
        "- Evidence: Targeted validation passed.\n"
        "- Findings: None.\n\n"
        if qa
        else "## QA & Code Review\n\n- Verdict: ____\n- Evidence: ____\n- Findings: ____\n\n"
    )
    return (
        "## User Story\n\n"
        "As a maintainer, I want a ready implementation plan, so that status gates pass.\n\n"
        f"{parent_sections}"
        "## Acceptance Criteria\n\n"
        "- [x] AC1: Ready outcome is delivered.\n\n"
        "## Validation\n\n"
        "- AC1: Targeted validation passed.\n\n"
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "| --: | ----- | ----------- | ------------------- | ----------------- | ------ |\n"
        "| 1 | Ready Work | Complete the ready fixture work. | AC1: Ready outcome is delivered. | Targeted validation. | Done |\n\n"
        f"{qa_section}"
        "## Retro\n\n"
        "- Reusable lessons: None.\n"
        "- Conventions or agent assets updated: None.\n"
        "- Follow-up tasks: None.\n"
    )


def ready_epic_retro(epic_id: str = "EPIC-001", title: str = "Ready Epic") -> str:
    return (
        "# Epic Retro\n\n"
        f"- Epic: {epic_id}\n"
        f"- Title: {title}\n"
        "- Last updated: 2026-06-17\n\n"
        "## Lessons\n\n"
        "- None.\n\n"
        "## Follow-up Tasks\n\n"
        "- None.\n\n"
        "## Deferrals\n\n"
        "- None.\n\n"
        "## Missed In-Scope Work\n\n"
        "- None.\n"
    )
