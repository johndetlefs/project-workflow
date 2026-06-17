# Requirements

## Summary

- Task: TASK-010
- Title: Global Task ID Allocation
- Parent AC Coverage: AC7
- Last updated: 2026-06-17

## Goal

Ensure every new standalone task and epic child task receives a globally unique `TASK-###` ID, even when existing task IDs appear inside epic trackers or nested epic child folders.

## Non-Goals

- Changing existing IDs or rewriting historical task folders.
- Changing EPIC ID allocation behavior beyond preserving current compatibility.
- Implementing intake or readiness gates outside ID allocation.

## Users & Context

- Agents need safe task creation and epic decomposition without colliding with existing child task IDs.
- Maintainers need the documented global `TASK-###` uniqueness rule to be enforced by code.
- EPIC-003 setup exposed this bug when standalone `task init` tried to assign `TASK-004` even though EPIC-002 already had child tasks `TASK-004` through `TASK-009`.

## Requirements (Outcome-Focused)

- Standalone task ID allocation scans standalone task folders, nested epic child task folders, global tracker rows, and all epic tracker rows.
- Epic decomposition ID allocation scans the same global set before proposing child rows.
- Generated local workflow helper stays aligned with package source.
- Fixture tests prove both standalone task creation and epic decomposition allocate after existing epic child IDs.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-003 AC7 by ensuring `task init` allocates the next task ID after existing epic child folder and tracker IDs.
- AC2: Covers EPIC-003 AC7 by ensuring `epic decompose` allocates proposed child IDs after existing child IDs in other epic trackers.
- AC3: Covers EPIC-003 AC7 by keeping package source and installed local helper behavior aligned.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Scan all task folders recursively and all `TRACKER.md` files under `.project-workflow/tasks`.
  - Why: Epic child rows and folders are nested under epic folders, so top-level scans are insufficient.

## Validation Plan

- Run targeted ID allocation tests in `tests/test_doctor.py`.
- Run the full `tests/test_doctor.py` suite before epic closeout.
- Compare `src/project_workflow/templates/workflow.py` with `.project-workflow/cli/workflow.py`.
