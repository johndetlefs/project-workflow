# Requirements

## Summary

- Task: TASK-008
- Title: Lifecycle Status Commands And Tracker Drift Guards
- Parent Epic: EPIC-002 | Epic Acceptance Rigor
- Parent AC Coverage: EPIC-002 AC11, AC15
- Last updated: 2026-06-17

## Goal

Add tracker-safe epic child status transitions so Testing, Review, and Complete no longer require manual epic tracker edits, and so Complete is blocked unless QA and parent AC evidence exist.

## Non-Goals

- Replacing task status commands for standalone tasks.
- Final epic closeout; implemented in TASK-006.

## Users & Context

- Agents need supported commands for normal epic child status transitions.
- Maintainers need drift guards around Complete so an epic child cannot be closed without parent AC evidence.

## Requirements (Outcome-Focused)

- `epic status` updates epic child rows through supported lifecycle states.
- Complete transitions require Review status, QA/code-review evidence, and parent AC evidence.
- Generated docs explain `epic status` and tracker ownership rules.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-002 AC11 when `epic status` supports Testing, Review, and Complete transitions without manual tracker edits.
- AC2: Covers EPIC-002 AC15 when generated docs and command behavior reinforce global tracker versus epic tracker ownership and drift guard rules.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Epic child Complete must pass the same evidence standards expected by epic closeout.
  - Context: The previous failure came from child completion being treated as enough without parent AC proof.
  - Chosen: `epic status --to Complete` requires QA evidence and parent AC evidence.
  - Why: This catches missing evidence before final epic closeout.

## Validation Plan

- Fixture test epic child status transitions through Testing and Review.
- Fixture test Complete blocks without parent AC evidence.
- Fixture test Complete passes after parent AC evidence is recorded.
- Run doctor and parity checks.
