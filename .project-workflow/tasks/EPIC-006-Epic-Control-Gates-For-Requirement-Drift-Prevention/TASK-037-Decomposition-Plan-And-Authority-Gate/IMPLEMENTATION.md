## User Story

As a project owner, I want epic child rows checked against an approved decomposition plan, so that long-running epics cannot silently accumulate invented task scope.

## Parent AC Coverage

- AC9, AC11, AC12, AC14, AC16, AC18

## Acceptance Criteria

- [x] AC1: Covers parent AC9 and AC14: child rows for new/adopted epics cannot be approved, scaffolded, readied, or advanced through gated status transitions unless they match `DECOMPOSITION.md` by ID, title, and parent AC coverage.
- [x] AC2: Covers parent AC11 and AC18: README/CLI guidance describes the decomposition plan as the owner-approved boundary and clarifies that matching planned rows do not need per-row approval.
- [x] AC3: Covers parent AC12 and AC16: automated tests prove `epic decompose` writes `DECOMPOSITION.md`, owner `Proposed Child Work` is preferred, unplanned rows are blocked, and doctor fails active manual rows without authority.

## Validation

- AC1: `epic approve`, `epic scaffold-child`, `epic ready-child`, and `epic status` call decomposition authority checks before advancing rows. Matching is ID, title, and parent AC coverage.
- AC2: CLI/README guidance now names `DECOMPOSITION.md` as the approved child-row boundary and says matching rows do not need per-row owner approval.
- AC3: `tests/test_doctor.py` covers plan creation, owner-proposed child work, command blocking for invented rows, and doctor failure for active manual rows.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add decomposition plan artifact | Generate and parse `DECOMPOSITION.md` from approved epic decomposition. | AC1, AC3 | Focused tests. | Done |
| 2 | Gate child lifecycle commands | Reject rows outside the plan before approval, scaffolding, readiness, and status movement. | AC1 | Focused tests. | Done |
| 3 | Add doctor state check | Fail active manually-created child rows without authority. | AC3 | Focused tests and doctor. | Done |
| 4 | Update guidance and EPIC-006 plan | Document the plan boundary and record current EPIC-006 child authority. | AC2 | Doctor and file review. | Done |

## Parent AC Evidence

- AC9: New epic child rows now require decomposition-plan authority before approval/scaffold/readiness/status movement.
- AC11: README and CLI README guidance updated for decomposition-plan authority.
- AC12: Regression tests added for plan generation, proposed-child preference, command blocking, and doctor failure.
- AC14: Matching rows inside `DECOMPOSITION.md` proceed without separate per-row approval; rows outside the plan are blocked.
- AC16: Doctor fails active child rows missing decomposition authority, including manual tracker edits.
- AC18: Gates fail with concrete authority gaps instead of asking for generic owner approval for in-plan rows.

## QA & Code Review

- Verdict: Pass
- Evidence: `pytest tests/test_doctor.py` passed with 55 tests on 2026-07-09. Full suite `pytest` passed with 55 tests on 2026-07-09.
- Findings: No TASK-037 blocking findings in focused regression coverage.

## Retro

- Reusable lessons: The tracker should be treated as execution state, not approval authority.
- Conventions or agent assets updated: CLI/template mirrors and tests updated; guidance docs updated.
- Follow-up tasks: TASK-033 should add the amendment path that authorizes new rows outside `DECOMPOSITION.md`.

## Notes

- Task: TASK-037
- Title: Decomposition Plan And Authority Gate
- Created: 2026-07-09
