## User Story

As an agent managing an epic, I want safe global epic lifecycle transitions, so that tracker progress is visible without bypassing closeout gates.

## Parent AC Coverage

- EPIC-004 AC4: A minimal epic status lifecycle exists for global epic rows where useful, with CLI-supported transitions or validation for `Analysing`, `Ready`, `In Progress`, `Closeout`, and `Complete`; transitions must not bypass readiness, audit, retro, or closeout gates.

## Acceptance Criteria

- [x] AC1: Covers EPIC-004 AC4 by adding `epic lifecycle`.
- [x] AC2: Covers EPIC-004 AC4 by gating `Ready`, `In Progress`, and `Closeout`.
- [x] AC3: Covers EPIC-004 AC4 by refusing `Complete` outside closeout.
- [x] AC4: Covers EPIC-004 AC4 by adding tests and docs/guidance.

## Validation

- AC1 / EPIC-004 AC4: Help and fixture coverage show the command exists.
- AC2 / EPIC-004 AC4: Fixtures prove blocked and passing gated transitions.
- AC3 / EPIC-004 AC4: Fixture proves `Complete` is refused with guidance to use closeout.
- AC4 / EPIC-004 AC4: `.venv/bin/pytest tests/test_doctor.py` passes.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Lifecycle Command | Add `epic lifecycle --epic-id <ID> --to <STATUS>` for global epic row transitions. | AC1, AC3 | Fixture and help output pass. | Done |
| 2 | Transition Gates | Gate Ready, In Progress, and Closeout using readiness, AC mapping/audit, and retro checks. | AC2, AC3 | Blocked/pass fixtures. | Done |
| 3 | Docs And Tests | Update README/generated epic guidance and add fixture coverage. | AC4 | Test suite passes. | Done |

## Parent AC Evidence

- EPIC-004 AC4: Implemented `epic lifecycle --epic-id <ID> --to <STATUS>`, added gated transitions for `Ready`, `In Progress`, and `Closeout`, refused `Complete` outside `epic closeout --complete`, updated README/generated epic guidance, and added fixture coverage.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 31 tests, including `test_epic_lifecycle_gates_global_epic_status`.
- Findings: None.

## Retro

- Reusable lessons: Global epic status commands should be separate from child row status commands to avoid ambiguous tracker ownership.
- Conventions or agent assets updated: README, generated epic prompt, and generated Codex epic skill.
- Follow-up tasks: Continue EPIC-004 with legacy warning classification.

## Notes

- Task: TASK-018
- Title: Minimal Epic Status Lifecycle
- Created: 2026-06-17
