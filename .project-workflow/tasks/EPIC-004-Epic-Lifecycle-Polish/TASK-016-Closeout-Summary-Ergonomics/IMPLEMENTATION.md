## User Story

As an agent closing an epic, I want a concise closeout summary, so that I can see what passed, what failed, and what to do next without reading the full audit first.

## Parent AC Coverage

- EPIC-004 AC2: `epic closeout` prints a concise human/agent-friendly summary covering total parent ACs, pass/fail/deferred counts, missing mappings, missing evidence, missing QA, deferrals, follow-ups, and next actions, while still writing the detailed audit file.

## Acceptance Criteria

- [x] AC1: Covers EPIC-004 AC2 by printing closeout counts for total/pass/deferred/gap parent ACs.
- [x] AC2: Covers EPIC-004 AC2 by categorizing common closeout blockers.
- [x] AC3: Covers EPIC-004 AC2 by printing clear next actions for blocked, validate-only pass, and complete pass paths.
- [x] AC4: Covers EPIC-004 AC2 by adding fixture coverage.

## Validation

- AC1 / EPIC-004 AC2: Closeout fixture asserts count summary output.
- AC2 / EPIC-004 AC2: Blocked closeout fixture asserts categorized blocker output.
- AC3 / EPIC-004 AC2: Passing closeout fixture asserts validate-only and complete next-action output.
- AC4 / EPIC-004 AC2: `.venv/bin/pytest tests/test_doctor.py` passes.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Summary Formatter | Add a helper that summarizes audit rows and gaps into closeout counts and categories. | AC1, AC2 | Fixture output assertions pass. | Done |
| 2 | Closeout Integration | Print the summary from `epic closeout` on blocked and passing paths. | AC1, AC2, AC3 | Closeout fixtures pass. | Done |
| 3 | Fixture Coverage | Extend closeout tests for summary and next-action output. | AC4 | `.venv/bin/pytest tests/test_doctor.py`. | Done |

## Parent AC Evidence

- EPIC-004 AC2: Implemented `_epic_closeout_summary` in the CLI, printed it from blocked and passing `epic closeout` paths, synced generated workflow helpers, and added fixture assertions for count summaries, categorized missing evidence, and next-action output.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 30 tests, including closeout summary output assertions for blocked, validate-only, and complete paths.
- Findings: None.

## Retro

- Reusable lessons: Closeout output should lead with a compact action summary while preserving detailed audit output for traceability.
- Conventions or agent assets updated: None.
- Follow-up tasks: Continue EPIC-004 with the lightweight epic retro gate.

## Notes

- Task: TASK-016
- Title: Closeout Summary Ergonomics
- Created: 2026-06-17
