## User Story

As a repo owner, I want project-workflow to create a safe canonical backlog file during init, so that future ideas can be captured without corrupting active tracker state.

## Parent AC Coverage

- AC1, AC2, AC3

## Acceptance Criteria

- [x] AC1: `project init` creates `.project-workflow/BACKLOG.md` with the canonical schema when the file is missing.
- [x] AC2: `project init` preserves an existing `.project-workflow/BACKLOG.md` without overwriting user-owned rows.
- [x] AC3: Backlog schema helpers support stable `BL-###` ID allocation and duplicate ID detection.
- [x] AC4: The backlog artifact documents that execution lifecycle state remains in tracker/task/epic artifacts.

## Validation

- AC1 / parent ACs AC1, AC2: Passed in `test_doctor_passes_for_clean_initialized_repo`; created backlog table includes required columns and vocabulary.
- AC2 / parent AC AC1: Passed in `test_project_init_preserves_existing_backlog`; existing backlog content remains unchanged after init.
- AC3 / parent AC AC2: Passed in `test_backlog_helpers_allocate_ids_and_detect_duplicates`; helper allocates `BL-011` after sparse existing IDs and detects duplicate `BL-010`.
- AC4 / parent AC AC3: Passed in generated backlog artifact assertions; artifact states `Accepted` is not implementation-ready and execution status lives in tracker artifacts.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Create backlog artifact on init | Add `.project-workflow/BACKLOG.md` creation for missing files with canonical columns and vocabulary. | AC1: Missing backlog file is created with required schema and vocabulary. | Passed via `test_doctor_passes_for_clean_initialized_repo`. | Done |
| 2 | Preserve existing backlog state | Ensure init refresh leaves existing `.project-workflow/BACKLOG.md` content unchanged. | AC2: Existing backlog file content survives init refresh byte-for-byte or with only explicitly accepted safe changes. | Passed via `test_project_init_preserves_existing_backlog`. | Done |
| 3 | Add schema and ID helpers | Add shared parsing/allocation support for `BL-###` rows and duplicate detection hooks. | AC3: Next backlog ID allocation skips existing IDs and duplicate IDs can be reported. | Passed via `test_backlog_helpers_allocate_ids_and_detect_duplicates`. | Done |
| 4 | Document tracker boundary in artifact | Include clear in-file guidance that backlog status is not active execution status. | AC4: Backlog artifact says `Accepted` is not implementation-ready and promoted execution state belongs in trackers. | Passed via generated backlog artifact assertions in `test_doctor_passes_for_clean_initialized_repo`. | Done |

## Parent AC Evidence

- AC1: `project init` now creates `.project-workflow/BACKLOG.md` when missing and preserves existing backlog files; validated by targeted init tests.
- AC2: Backlog schema/vocabulary constants and helper coverage support stable `BL-###` IDs and duplicate detection; validated by helper tests.
- AC3: Generated backlog artifact states that backlog status is not implementation status and execution state lives in tracker/task/epic artifacts; validated by generated artifact assertions.

## QA & Code Review

- Verdict: Pass.
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py` passed with 40 tests; `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor` passed with only pre-existing legacy warnings; source, template, and local workflow CLI copies matched by `cmp`.
- Findings: No blocking findings in the backlog artifact/init changes.

## Retro

- Reusable lessons: Keep canonical artifact creation idempotent and treat existing workflow state as user-owned.
- Conventions or agent assets updated: Added backlog as a generated workflow artifact and preserved the tracker boundary language in the artifact template.
- Follow-up tasks: None.

## Notes

- Task: TASK-020
- Title: Backlog artifact, schema, and init support
- Created: 2026-06-22
