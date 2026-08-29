#!/usr/bin/env python3
"""Capture a mechanically inspectable Project Workflow Epic dogfood packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def sha256_path(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return completed.stdout


def field(section: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", section, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"missing owner approval field: {label}")
    return match.group(1).strip()


def tracker_statuses(tracker: Path) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for line in tracker.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"TASK-\d+", cells[0]):
            statuses[cells[0]] = cells[2]
    return statuses


def verify_owner_approval_event(owner_observation: dict[str, Any]) -> dict[str, Any]:
    relative = Path(owner_observation["session_artifact"])
    if relative.is_absolute() or not relative.parts or relative.parts[0] != ".codex":
        raise RuntimeError("owner session artifact must be a home-relative .codex path")
    session_path = Path.home() / relative
    if not session_path.is_file():
        raise RuntimeError(f"owner session artifact is missing: {relative}")
    expected_turn = owner_observation["approval"]["turn_id"]
    expected_message = owner_observation["approval"]["message_id"]
    expected_text = owner_observation["approval"]["text"]
    with session_path.open(encoding="utf-8") as session:
        for line_number, raw_line in enumerate(session, start=1):
            event = json.loads(raw_line)
            payload = event.get("payload", {})
            metadata = payload.get("internal_chat_message_metadata_passthrough", {})
            if (
                event.get("type") != "response_item"
                or payload.get("type") != "message"
                or payload.get("role") != "user"
                or metadata.get("turn_id") != expected_turn
                or payload.get("id") != expected_message
            ):
                continue
            text = "".join(
                part.get("text", "")
                for part in payload.get("content", [])
                if part.get("type") in {"input_text", "text"}
            ).strip()
            if text == expected_text:
                raw_event = raw_line.rstrip("\n")
                return {
                    "artifact": relative.as_posix(),
                    "line": line_number,
                    "event_timestamp": event.get("timestamp"),
                    "message_id": payload.get("id"),
                    "turn_id": expected_turn,
                    "event_line_sha256": "sha256:"
                    + hashlib.sha256(raw_event.encode("utf-8")).hexdigest(),
                }
    raise RuntimeError(f"raw owner approval event was not found for {expected_turn}")


def relevant_artifacts(root: Path, epic_dir: Path, task_dir: Path) -> dict[str, str]:
    paths = [
        epic_dir / "REQUIREMENTS.md",
        epic_dir / "EPIC-CONTRACT.md",
        epic_dir / "DECOMPOSITION.md",
        epic_dir / "INTENT-AUDIT.json",
        epic_dir / "TRACKER.md",
        root / ".project-workflow/TRACKER.md",
        root / "scripts/capture_dogfood_journey.py",
        task_dir / "REQUIREMENTS.md",
        task_dir / "IMPLEMENTATION.md",
        task_dir / "evidence/package-journeys.json",
        task_dir / "evidence/independent-qa-initial.md",
        task_dir / "evidence/independent-qa-second.md",
    ]
    for child_dir in sorted(epic_dir.glob("TASK-*")):
        paths.extend(
            path
            for path in (child_dir / "REQUIREMENTS.md", child_dir / "IMPLEMENTATION.md")
            if path not in paths
        )
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"dogfood sources are missing: {missing}")
    return {path.relative_to(root).as_posix(): sha256_path(path) for path in sorted(paths)}


def capture(
    root: Path,
    epic_id: str,
    task_id: str,
    owner_observation_path: Path,
) -> dict[str, Any]:
    workflow = root / ".project-workflow/cli/workflow"
    epic_dir = next(iter(sorted((root / ".project-workflow/tasks").glob(f"{epic_id}-*"))), None)
    if epic_dir is None:
        raise RuntimeError(f"cannot find Epic directory for {epic_id}")
    task_dir = next(iter(sorted(epic_dir.glob(f"{task_id}-*"))), None)
    if task_dir is None:
        raise RuntimeError(f"cannot find child directory for {task_id}")

    owner_observation = json.loads(owner_observation_path.read_text(encoding="utf-8"))
    approval_text = owner_observation.get("approval", {}).get("text")
    if not approval_text or "happy with that" not in approval_text.lower():
        raise RuntimeError("owner observation does not contain the captured meaning approval")
    raw_owner_event = verify_owner_approval_event(owner_observation)

    synopsis = run([str(workflow), "epic", "approval-summary", "--epic-id", epic_id], root)
    if not synopsis.startswith("Approval synopsis\n\nIntent\n"):
        raise RuntimeError("approval synopsis is not meaning-first")
    if "Does this Intent accurately capture what you want and what success means?" not in synopsis:
        raise RuntimeError("approval synopsis omits the semantic approval question")
    if re.search(r"\b(?:AC|TASK|EPIC)-?\d+\b|sha256:[0-9a-f]{64}", synopsis):
        raise RuntimeError("approval synopsis substitutes workflow IDs or hashes for meaning")

    requirements = (epic_dir / "REQUIREMENTS.md").read_text(encoding="utf-8")
    approval_section = requirements.split("## Owner Approval", 1)[1].split("\n## ", 1)[0]
    approval_fields = {
        label: field(approval_section, label)
        for label in (
            "Intent reviewed and accurately reflected",
            "Requirements reviewed by owner",
            "Acceptance criteria reviewed by owner",
            "Approved scope envelope",
            "Approved by",
            "Approval date",
            "Approval note / source",
            "Approved artifact identity",
        )
    }
    for label in (
        "Intent reviewed and accurately reflected",
        "Requirements reviewed by owner",
        "Acceptance criteria reviewed by owner",
        "Approved scope envelope",
    ):
        if approval_fields[label] != "Yes":
            raise RuntimeError(f"owner approval is not current: {label}")

    intent_audit = json.loads(
        run(
            [
                str(workflow),
                "epic",
                "intent-audit",
                "--epic-id",
                epic_id,
                "--format",
                "json",
            ],
            root,
        )
    )
    if intent_audit.get("state") != "current" or intent_audit.get("verdict") != "pass":
        raise RuntimeError("live intent audit is not current and passing")

    status = json.loads(run([str(workflow), "status", "--id", epic_id, "--format", "json"], root))
    selected = next(
        (work for work in status.get("active_work", []) if work.get("id") == epic_id), None
    )
    if selected is None:
        raise RuntimeError("focused workflow status omitted the active Epic")
    task_status = tracker_statuses(epic_dir / "TRACKER.md")
    if task_status.get(task_id) != "Review":
        raise RuntimeError(f"{task_id} must remain in Review while QA is blocking")

    reviews: list[dict[str, str]] = []
    for name in ("independent-qa-initial.md", "independent-qa-second.md"):
        path = task_dir / "evidence" / name
        review_text = path.read_text(encoding="utf-8")
        if "Changes requested" not in review_text:
            raise RuntimeError(f"retained blocking review lacks its verdict: {name}")
        reviews.append(
            {
                "artifact": path.relative_to(root).as_posix(),
                "sha256": sha256_path(path),
                "verdict": "changes-requested",
            }
        )

    return {
        "schema_version": 1,
        "captured_at": owner_observation["captured_at"],
        "epic_id": epic_id,
        "task_id": task_id,
        "source_revision": "6bf7601f47bc1362347d1c067e5bd2db6b67fe4c+working-tree-candidate",
        "owner_observation": {
            "artifact": owner_observation_path.relative_to(root).as_posix(),
            "sha256": sha256_path(owner_observation_path),
            "thread_id": owner_observation["thread_id"],
            "approval_turn_id": owner_observation["approval"]["turn_id"],
            "approval_text": approval_text,
            "retrieval_surface": owner_observation["retrieval_surface"],
            "raw_session_event": raw_owner_event,
        },
        "approval_synopsis": {
            "output": synopsis,
            "sha256": "sha256:" + hashlib.sha256(synopsis.encode("utf-8")).hexdigest(),
            "meaning_first": True,
            "semantic_question_present": True,
            "workflow_identifier_substitute_present": False,
        },
        "approved_requirements": approval_fields,
        "intent_audit": {
            "state": intent_audit["state"],
            "verdict": intent_audit["verdict"],
            "audit_identity": intent_audit["audit_identity"],
            "issues": intent_audit["issues"],
            "unresolved_drift": intent_audit["unresolved_drift"],
        },
        "lifecycle_observation": {
            "epic_status": selected["lifecycle"],
            "child_statuses": task_status,
            "qa_blocking_child": task_id,
            "blocking_reviews": reviews,
        },
        "artifact_identities": relevant_artifacts(root, epic_dir, task_dir),
        "authority_boundary": (
            "Local dogfood evidence only; no publication, merge, release, rollout, "
            "consumer adoption, final owner acceptance or commercial validation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--epic-id", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--owner-observation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    payload = capture(root, args.epic_id, args.task_id, root / args.owner_observation)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
