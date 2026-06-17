# Requirements

## Summary

- Task: TASK-019
- Title: Legacy Warning Classification
- Parent AC Coverage: AC5
- Last updated: 2026-06-17

## Goal

Separate legacy/historical workflow warnings from current actionable issues in doctor output so old artifacts remain visible without obscuring problems in new work.

## Non-Goals

- Deleting or suppressing legacy warnings entirely.
- Manually rewriting every historical task or epic.
- Weakening strict-mode failures for current workflow artifacts.
- Adding a complex migration subsystem.

## Users & Context

- Agents need to distinguish warnings they should fix now from historical warnings outside the active task/epic.
- Owners need confidence that legacy noise is visible but not confused with current epic health.
- Maintainers need doctor output that remains backward compatible and script-friendly.

## Requirements (Outcome-Focused)

- Doctor output labels historical warnings separately from current warnings.
- Current EPIC-003-or-newer/newly active workflow issues remain normal warnings or errors.
- Legacy warnings remain printed and count toward doctor visibility.
- Tests prove historical APP/EPIC-002-style warnings are classified as legacy while new/current gate failures remain actionable.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-004 AC5 by classifying historical warnings separately in doctor output.
- AC2: Covers EPIC-004 AC5 by keeping current active/new task and epic warnings actionable.
- AC3: Covers EPIC-004 AC5 by preserving warning visibility and strict behavior.
- AC4: Covers EPIC-004 AC5 by adding fixture tests for legacy and current warnings.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Classify legacy warnings by historical artifact age/ID in this repo's current workflow history rather than hiding them.
  - Why: This directly reduces noise while keeping the cleanup signal available.

## Validation Plan

- Add doctor fixture assertions.
- Run `.venv/bin/pytest tests/test_doctor.py`.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-004 --id TASK-019`.
- Run `./.project-workflow/cli/workflow doctor`.
