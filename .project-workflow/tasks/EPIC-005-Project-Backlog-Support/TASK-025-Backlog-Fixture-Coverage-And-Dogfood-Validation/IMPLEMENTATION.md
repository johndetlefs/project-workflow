## User Story

As a maintainer, I want focused tests and dogfood evidence for backlog support, so that the feature can close with confidence across CLI behavior and generated agent assets.

## Parent AC Coverage

- AC7, AC10

## Acceptance Criteria

- [x] AC1: Tests cover init creation and existing backlog preservation.
- [x] AC2: Tests cover valid add/list/update/status behavior.
- [x] AC3: Tests cover validation failures for malformed rows, missing fields, duplicates, invalid vocabulary, and bad promoted references.
- [x] AC4: Tests cover task and epic promotion with backlog provenance.
- [x] AC5: Tests or assertions cover generated backlog assets across supported agent modes.
- [x] AC6: Tests prove promoted rows remain in the backlog.
- [x] AC7: A dogfood backlog scenario is executed or documented with validation evidence.

## Validation

- AC1 / parent AC AC10: Passed in `test_doctor_passes_for_clean_initialized_repo` and `test_project_init_preserves_existing_backlog`.
- AC2 / parent AC AC10: Passed in `test_backlog_cli_add_list_update_status_and_validate`, including list immutability, valid update/status behavior, and invalid status/priority rejection.
- AC3 / parent ACs AC7, AC10: Passed in `test_backlog_validate_reports_invalid_rows_and_bad_promoted_refs` and `test_doctor_reports_existing_backlog_validation_errors`.
- AC4 / parent AC AC10: Passed in `test_backlog_promote_to_task_preserves_source_and_row` and `test_backlog_promote_to_epic_preserves_source_and_row`.
- AC5 / parent AC AC10: Passed in `test_doctor_passes_for_clean_initialized_repo`, `test_generated_local_workflow_exposes_doctor`, and `test_agent_mode_init_installs_doctor_guidance`.
- AC6 / parent AC AC10: Passed in task and epic promotion tests; both assert source rows remain in `BACKLOG.md` with status `Promoted` and `Promoted To` populated.
- AC7 / parent AC AC10: Dogfood row `BL-001` was created in this repo for "Legacy Backlog Adoption Helper"; `./.project-workflow/cli/workflow backlog validate` passed and `backlog list` reported the row as not promoted.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add backlog behavior fixtures | Add tests covering init, row lifecycle, validation failures, and promoted-row preservation. | AC1: Init tests pass.<br>AC2: Lifecycle tests pass.<br>AC3: Validation failure tests pass.<br>AC6: Promoted rows remain in backlog. | Passed via backlog init, lifecycle, validation, and promotion tests. | Done |
| 2 | Add promotion and provenance fixtures | Add tests for task and epic promotion, including `## Backlog Source` requirements sections. | AC4: Task and epic promotion tests pass with provenance assertions. | Passed via task and epic promotion tests. | Done |
| 3 | Add generated asset and dogfood checks | Verify backlog assets are generated for supported modes and run one small dogfood scenario. | AC5: Generated asset checks pass.<br>AC7: Dogfood evidence is recorded. | Passed via generated asset tests and dogfood `BL-001` validation. | Done |

## Parent AC Evidence

- AC7: Validation fixtures cover malformed rows, missing fields, duplicate IDs, invalid vocabulary, bad promoted references, and doctor integration with actionable messages.
- AC10: Automated tests now cover backlog init, add/list/update/status behavior, validation failures, task promotion, epic promotion, generated asset inclusion, idempotent refresh, and promoted-row preservation.

## QA & Code Review

- Verdict: Pass.
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py` passed with 40 tests; dogfood `BL-001` validated with `./.project-workflow/cli/workflow backlog validate`; `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor` passed with only pre-existing legacy warnings.
- Findings: No blocking findings in fixture coverage or dogfood validation.

## Retro

- Reusable lessons: Dogfood rows are useful for proving the feature works in the host repo without promoting artificial work.
- Conventions or agent assets updated: Test fixtures now guard backlog lifecycle, promotion, generated assets, and doctor validation behavior.
- Follow-up tasks: None.

## Notes

- Task: TASK-025
- Title: Backlog fixture coverage and dogfood validation
- Created: 2026-06-22
