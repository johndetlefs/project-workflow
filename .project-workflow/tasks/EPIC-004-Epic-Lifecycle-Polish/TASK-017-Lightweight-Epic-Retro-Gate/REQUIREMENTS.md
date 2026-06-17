# Requirements

## Summary

- Task: TASK-017
- Title: Lightweight Epic Retro Gate
- Parent AC Coverage: AC3
- Last updated: 2026-06-17

## Goal

Require a lightweight epic-level retro record before an epic can be closed, so follow-ups, deferrals, lessons, and missed scope are not hidden by child task completion.

## Non-Goals

- Forcing a long retrospective ceremony.
- Replacing child task retros.
- Blocking closeout when a section legitimately has no content and records `None.` explicitly.
- Building follow-up task creation automation in this task.

## Users & Context

- Owners need confidence that missed in-scope work, follow-ups, and deferrals have been surfaced before closure.
- Agents need a clear artifact to inspect and update during closeout.
- Maintainers need closeout gates that prevent ambiguous "we should do X" retro notes from being buried in child task docs.

## Requirements (Outcome-Focused)

- New epics include a lightweight `RETRO.md` template.
- The retro records lessons, follow-up tasks, deferrals, and missed in-scope work.
- `epic closeout` blocks completion if the retro is missing, has missing required sections, or still contains placeholders.
- Explicit `None.` entries are accepted for sections where there is nothing to report.
- README and generated epic guidance explain the retro requirement.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-004 AC3 by making `epic init` create an epic `RETRO.md` template.
- AC2: Covers EPIC-004 AC3 by making `epic closeout` block when the epic retro is missing or incomplete.
- AC3: Covers EPIC-004 AC3 by allowing explicit `None.` entries for required retro sections.
- AC4: Covers EPIC-004 AC3 by updating README and generated epic guidance.
- AC5: Covers EPIC-004 AC3 by adding fixture tests for blocked and passing retro closeout paths.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Use `RETRO.md` in the epic folder.
  - Why: It is simple, visible, and consistent with repository-native Markdown workflow state.

- Decision: Accept explicit `None.` entries.
  - Why: The gate should prove the topic was considered, not force fake content.

## Validation Plan

- Add or update closeout fixture tests in `tests/test_doctor.py`.
- Run `.venv/bin/pytest tests/test_doctor.py`.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-004 --id TASK-017`.
- Run `./.project-workflow/cli/workflow doctor`.
