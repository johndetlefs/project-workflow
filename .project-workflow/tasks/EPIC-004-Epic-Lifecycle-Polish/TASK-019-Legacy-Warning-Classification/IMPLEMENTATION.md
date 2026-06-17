## User Story

As an agent reviewing workflow health, I want legacy warnings separated from current warnings, so that I can focus on actionable issues without losing historical cleanup signals.

## Parent AC Coverage

- EPIC-004 AC5: Doctor or validation output separates legacy/historical warnings from current actionable issues, with tests proving old APP/EPIC-002-style artifacts remain visible but do not obscure EPIC-003-or-newer gate failures.

## Acceptance Criteria

- [x] AC1: Covers EPIC-004 AC5 by classifying historical warnings separately.
- [x] AC2: Covers EPIC-004 AC5 by keeping current warnings actionable.
- [x] AC3: Covers EPIC-004 AC5 by preserving warning visibility and strict behavior.
- [x] AC4: Covers EPIC-004 AC5 by adding fixture tests.

## Validation

- AC1 / EPIC-004 AC5: Fixture asserts legacy warning label/output exists.
- AC2 / EPIC-004 AC5: Fixture asserts current active warnings remain normal warnings/errors.
- AC3 / EPIC-004 AC5: Doctor still exits successfully with warnings and strict mode still fails errors.
- AC4 / EPIC-004 AC5: `.venv/bin/pytest tests/test_doctor.py` passes.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Legacy Classifier | Add a small classifier for known historical workflow artifacts. | AC1, AC3 | Doctor fixture output. | Done |
| 2 | Doctor Output Split | Print legacy warnings separately from current warnings. | AC1, AC2, AC3 | Doctor fixture output. | Done |
| 3 | Fixture Coverage | Add tests for legacy versus current warning output. | AC4 | `.venv/bin/pytest tests/test_doctor.py`. | Done |

## Parent AC Evidence

- EPIC-004 AC5: Implemented legacy warning classification for historical APP rows and pre-EPIC-003 epic warnings, printed legacy warnings separately from current warnings, preserved strict-mode blocking behavior, and added fixture coverage for current versus legacy warning output.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 32 tests, including `test_doctor_separates_legacy_warnings_from_current_warnings`.
- Findings: None.

## Retro

- Reusable lessons: Warning noise is best reduced by classification before suppression; historical cleanup signals should remain visible.
- Conventions or agent assets updated: None.
- Follow-up tasks: None.

## Notes

- Task: TASK-019
- Title: Legacy Warning Classification
- Created: 2026-06-17
