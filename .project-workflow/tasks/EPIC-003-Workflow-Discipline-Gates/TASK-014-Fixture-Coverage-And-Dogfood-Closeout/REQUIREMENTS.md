# Requirements

## Summary

- Task: TASK-014
- Title: Fixture Coverage And Dogfood Closeout
- Parent AC Coverage: AC8, AC9, AC10, AC11, AC12, AC13
- Last updated: 2026-06-17

## Goal

Prove EPIC-003 is covered by tests, generated asset parity, doctor checks, and its own acceptance audit.

## Non-Goals

- Adding new product behavior beyond the implemented gates and guidance.
- Releasing a package version.
- Hiding known historical APP warnings.

## Users & Context

- Maintainers need confidence the new gates work and stay synced across shipped assets.
- Owners need closeout evidence summarized at the epic level.
- Agents need tests that prove both blocking and passing paths.

## Requirements (Outcome-Focused)

- Automated tests cover intake, readiness, discovery exceptions, ID allocation, decomposition gating, child readiness, status gates, and generated guidance.
- Package source, generated workflow template, local helper, source prompts, and prompt mirrors stay aligned.
- EPIC-003 acceptance audit passes before closeout.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-003 AC8 by validating doctor/readiness remediation behavior.
- AC2: Covers EPIC-003 AC9 by verifying generated docs/assets explain lifecycle gates.
- AC3: Covers EPIC-003 AC10 by adding passing and failing fixtures for discipline gates.
- AC4: Covers EPIC-003 AC11 by asserting generated agent assets include the role split.
- AC5: Covers EPIC-003 AC12 by verifying owner-facing docs describe conversational intake.
- AC6: Covers EPIC-003 AC13 by testing actionable remediation categories.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Keep historical APP warnings visible.
  - Why: They are unrelated pre-existing workflow-state warnings and should not be silently suppressed.

## Validation Plan

- Run full `tests/test_doctor.py`.
- Run local helper doctor and package doctor.
- Run exact parity comparisons for workflow helper and prompt mirrors.
- Run `epic audit` and `epic closeout` for EPIC-003.
