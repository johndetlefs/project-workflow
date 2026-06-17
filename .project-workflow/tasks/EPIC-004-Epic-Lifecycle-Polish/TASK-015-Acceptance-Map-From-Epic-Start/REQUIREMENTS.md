# Requirements

## Summary

- Task: TASK-015
- Title: Acceptance Map From Epic Start
- Parent AC Coverage: AC1
- Last updated: 2026-06-17

## Goal

Make parent acceptance coverage visible from the moment an epic is created by having project-workflow generate and maintain an `ACCEPTANCE-MAP.md` artifact for epics.

## Non-Goals

- Replacing `ACCEPTANCE-AUDIT.md`; the audit remains the closeout evidence artifact.
- Building a continuously running synchronization service.
- Requiring owners to manually maintain the map as the normal workflow.
- Retrofitting every historical epic map by hand.

## Users & Context

- Owners need to see which parent ACs are covered before final closeout.
- Agents need an obvious artifact to update and inspect during decomposition, scaffolding, status changes, and audit.
- Junior developers need the epic folder itself to show AC coverage state without searching child task docs.

## Requirements (Outcome-Focused)

- `epic init` creates an `ACCEPTANCE-MAP.md` artifact alongside `REQUIREMENTS.md`, `TRACKER.md`, and `DEFERRALS.md`.
- The acceptance map includes parent AC ID, parent AC summary, child coverage, evidence state, deferral state, and status.
- Epic commands that change coverage state refresh the acceptance map when practical: decomposition, approval, child scaffold, child status, audit, and closeout.
- The acceptance map stays lightweight and derived from existing requirements, tracker, deferral, and child evidence sources.
- User-facing and agent-facing docs explain that `ACCEPTANCE-MAP.md` is an in-progress coverage view while `ACCEPTANCE-AUDIT.md` is the closeout gate artifact.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-004 AC1 by making `epic init` create `ACCEPTANCE-MAP.md` for new epics.
- AC2: Covers EPIC-004 AC1 by refreshing `ACCEPTANCE-MAP.md` after decomposition so proposed child coverage appears by parent AC.
- AC3: Covers EPIC-004 AC1 by refreshing `ACCEPTANCE-MAP.md` after audit/closeout so evidence and verdict state are visible.
- AC4: Covers EPIC-004 AC1 by updating README and generated epic guidance to describe the acceptance map lifecycle.
- AC5: Covers EPIC-004 AC1 by adding fixture tests for map creation and coverage refresh.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Treat `ACCEPTANCE-MAP.md` as a derived, lightweight working view.
  - Why: It should improve visibility without creating a new source of truth that can contradict requirements, tracker, deferrals, or child QA evidence.

- Decision: Keep `ACCEPTANCE-AUDIT.md` as the closeout artifact.
  - Why: Audit and closeout need a stable evidence record; the map is for in-progress coverage tracking.

## Validation Plan

- Add or update tests in `tests/test_doctor.py`.
- Run `.venv/bin/pytest tests/test_doctor.py`.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-004 --id TASK-015`.
- Run `./.project-workflow/cli/workflow doctor`.
- Verify source CLI, packaged template, and installed local helper stay aligned.
