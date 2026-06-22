## User Story

As a product owner, I want to promote an accepted backlog item into a normal task or epic, so that future intent can become executable work without losing its origin.

## Parent AC Coverage

- AC5, AC6

## Acceptance Criteria

- [x] AC1: Task promotion creates the same scaffold and global tracker state as normal task creation.
- [x] AC2: Epic promotion creates the same scaffold, tracker, and acceptance-map state as normal epic creation.
- [x] AC3: Successful promotion leaves the backlog row in place with status `Promoted` and a `Promoted To` reference.
- [x] AC4: Promoted requirements include a populated `## Backlog Source` section.
- [x] AC5: Invalid or unaccepted rows fail promotion without partial workflow writes.

## Validation

- AC1 / parent AC AC5: Passed in `test_backlog_promote_to_task_preserves_source_and_row`; promotion creates the task folder, requirements, implementation, and global tracker row.
- AC2 / parent AC AC6: Passed in `test_backlog_promote_to_epic_preserves_source_and_row`; promotion creates epic requirements, tracker, deferral/retro artifacts, acceptance map, and global tracker row.
- AC3 / parent ACs AC5, AC6: Passed in task and epic promotion tests; the source `BL-001` rows remain with status `Promoted` and `Promoted To` set to the created ID.
- AC4 / parent ACs AC5, AC6: Passed in task and epic promotion tests; promoted requirements contain a populated `## Backlog Source` section with ID, type, outcome, and notes.
- AC5 / parent ACs AC5, AC6: Passed in `test_backlog_promote_requires_accepted_or_explicit_accept`; unaccepted promotion fails without creating a task folder, while explicit `--accept` succeeds.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Promote backlog rows to tasks | Implement task promotion by reusing task scaffold behavior and writing backlog provenance. | AC1: Task scaffold and global tracker row are created.<br>AC3: Backlog row becomes `Promoted` with `Promoted To` set.<br>AC4: Task requirements include `## Backlog Source`. | Passed via `test_backlog_promote_to_task_preserves_source_and_row`. | Done |
| 2 | Promote backlog rows to epics | Implement epic promotion by reusing epic scaffold behavior and writing backlog provenance. | AC2: Epic scaffold, epic tracker artifacts, acceptance map, and global tracker row are created.<br>AC3: Backlog row becomes `Promoted` with `Promoted To` set.<br>AC4: Epic requirements include `## Backlog Source`. | Passed via `test_backlog_promote_to_epic_preserves_source_and_row`. | Done |
| 3 | Block unsafe promotion states | Add validation so missing, malformed, rejected, already-promoted, or non-accepted rows fail safely unless explicit accept-and-promote confirmation is supplied. | AC5: Invalid promotion attempts fail without partial writes. | Passed via `test_backlog_promote_requires_accepted_or_explicit_accept`. | Done |

## Parent AC Evidence

- AC5: Task promotion creates normal task scaffolding, updates the global tracker, leaves the backlog row as `Promoted`, records `Promoted To`, and writes `## Backlog Source`; validated by task promotion fixture coverage.
- AC6: Epic promotion creates normal epic scaffolding, updates the global tracker, leaves the backlog row as `Promoted`, records `Promoted To`, and writes `## Backlog Source`; validated by epic promotion fixture coverage.

## QA & Code Review

- Verdict: Pass.
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py` passed with 40 tests; `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor` passed with only pre-existing legacy warnings; source, template, and local workflow CLI copies matched by `cmp`.
- Findings: No blocking findings in backlog promotion behavior.

## Retro

- Reusable lessons: Promotion tests need to inspect both sides of traceability: generated task/epic artifacts and the preserved backlog row.
- Conventions or agent assets updated: Promotion provenance uses a stable `## Backlog Source` section for task and epic requirements.
- Follow-up tasks: None.

## Notes

- Task: TASK-022
- Title: Backlog promotion to task and epic
- Created: 2026-06-22
