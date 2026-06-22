## User Story

As an agent operator, I want deterministic backlog CLI commands, so that backlog rows can be changed and validated without fragile manual table edits.

## Parent AC Coverage

- AC2, AC3, AC7

## Acceptance Criteria

- [x] AC1: A backlog add command creates a valid row with the next `BL-###` ID.
- [x] AC2: A backlog list command displays rows without mutating `.project-workflow/BACKLOG.md`.
- [x] AC3: Backlog status/update commands reject invalid lifecycle values and tracker-style execution statuses.
- [x] AC4: Backlog update behavior validates type and priority values before writing.
- [x] AC5: Backlog validation reports malformed rows, missing fields, duplicates, invalid vocabulary, and bad promoted references.

## Validation

- AC1 / parent AC AC2: Passed in `test_backlog_cli_add_list_update_status_and_validate`; `backlog add` created `BL-001` with the expected type, priority, status, outcome, and notes.
- AC2 / parent AC AC2: Passed in `test_backlog_cli_add_list_update_status_and_validate`; the test captures the backlog before `backlog list` and asserts the file is unchanged afterward.
- AC3 / parent AC AC3: Passed in `test_backlog_cli_add_list_update_status_and_validate`; `backlog status --to "In Progress"` fails and leaves the backlog unchanged.
- AC4 / parent AC AC2: Passed in `test_backlog_cli_add_list_update_status_and_validate`; invalid priority `Urgent` fails without mutation, while a valid update changes the intended fields.
- AC5 / parent AC AC7: Passed in `test_backlog_validate_reports_invalid_rows_and_bad_promoted_refs` and `test_doctor_reports_existing_backlog_validation_errors`; validation reports malformed vocabulary, duplicate IDs, missing promoted references, and invalid tracker-style statuses.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add backlog row lifecycle commands | Implement deterministic add/list/status/update operations for `.project-workflow/BACKLOG.md`. | AC1: Add creates the next `BL-###` row.<br>AC2: List displays rows without mutation.<br>AC3: Status rejects invalid execution statuses.<br>AC4: Update validates type and priority. | Passed via `test_backlog_cli_add_list_update_status_and_validate`. | Done |
| 2 | Add backlog validation command | Implement validation for schema, required fields, duplicate IDs, invalid vocabulary, and promoted references. | AC5: Validation reports every supported malformed state with actionable messages. | Passed via invalid backlog validation fixtures and doctor validation coverage. | Done |
| 3 | Preserve tracker boundary in commands | Ensure commands do not treat backlog statuses as task/epic lifecycle statuses. | AC3: Tracker-style statuses such as `Testing`, `Review`, and `Complete` are rejected for backlog rows. | Passed via invalid status command coverage and existing-backlog doctor validation. | Done |

## Parent AC Evidence

- AC2: Backlog CLI row lifecycle uses canonical `BL-###` IDs and validated type/priority values; tested through add/update/list coverage.
- AC3: Backlog commands reject tracker-style execution statuses and keep backlog lifecycle values separate from task/epic statuses; tested with invalid status command and doctor validation fixtures.
- AC7: Backlog validation reports duplicate IDs, invalid vocabulary, missing promoted references, and unresolved references with actionable messages; tested by invalid fixture coverage.

## QA & Code Review

- Verdict: Pass.
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py` passed with 40 tests; `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor` passed with only pre-existing legacy warnings; source, template, and local workflow CLI copies matched by `cmp`.
- Findings: No blocking findings in backlog lifecycle or validation command behavior.

## Retro

- Reusable lessons: Lifecycle command tests should assert both successful output and absence of unintended file mutation.
- Conventions or agent assets updated: Backlog CLI command vocabulary now defines the canonical mutation path for agents.
- Follow-up tasks: None.

## Notes

- Task: TASK-021
- Title: Backlog CLI lifecycle and validation
- Created: 2026-06-22
