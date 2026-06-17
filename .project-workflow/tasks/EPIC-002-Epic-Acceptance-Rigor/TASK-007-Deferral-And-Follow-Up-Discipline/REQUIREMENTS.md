# Requirements

## Summary

- Task: TASK-007
- Title: Deferral And Follow-Up Discipline
- Parent Epic: EPIC-002 | Epic Acceptance Rigor
- Parent AC Coverage: EPIC-002 AC10, AC12
- Last updated: 2026-06-17

## Goal

Make owner-approved deferrals structured and auditable, and make retro guidance separate future follow-ups from missed in-scope work that should have blocked completion.

## Non-Goals

- Full closeout command implementation; completed in TASK-006.
- General lifecycle status commands; reserved for TASK-008.

## Users & Context

- Product owners need deferral decisions recorded with accountable metadata and a follow-up reference.
- Agents need retro guidance that does not hide unfinished in-scope work as a vague follow-up.

## Requirements (Outcome-Focused)

- New epics include `DEFERRALS.md` with structured owner decision fields.
- Closeout accepts a deferral only when status, owner, date, reason, and follow-up are present.
- Closeout blocks incomplete or unapproved deferrals.
- Retro guidance separates follow-up tasks from missed in-scope work.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-002 AC10 when `DEFERRALS.md` exists for new epics and closeout accepts only approved deferrals with owner, date, reason, and follow-up reference.
- AC2: Covers EPIC-002 AC12 when generated retro guidance requires follow-up suggestions to be listed separately from missed in-scope work.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Store deferrals as an epic-local Markdown table.
  - Context: Deferrals are parent-AC decisions and belong beside epic tracker/audit artifacts.
  - Chosen: `DEFERRALS.md` under the epic folder.
  - Why: Keeps deferrals repository-native and closeout-readable.

## Validation Plan

- Fixture test approved deferral with follow-up passes closeout.
- Fixture test incomplete deferral metadata blocks closeout.
- Verify retro prompt/skill guidance includes separated missed in-scope work.
