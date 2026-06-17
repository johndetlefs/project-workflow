## User Story

As a project-workflow maintainer, I want task ID allocation to scan standalone tasks and all epic child tasks, so agents cannot create duplicate `TASK-###` IDs when using task or epic commands.

## Parent AC Coverage

- EPIC-003 AC7: `TASK-###` allocation scans standalone task folders, global tracker rows, all epic tracker rows, and epic child task folders so new standalone tasks and epic child tasks remain globally unique.

## Acceptance Criteria

- [x] AC1: Covers EPIC-003 AC7 by making standalone `task init` allocate after existing epic child folder and tracker IDs.
- [x] AC2: Covers EPIC-003 AC7 by making `epic decompose` allocate after existing child IDs in other epic trackers.
- [x] AC3: Covers EPIC-003 AC7 by syncing the package source workflow and installed local helper.

## Validation

- AC1 / EPIC-003 AC7: `tests/test_doctor.py::test_task_init_allocates_after_epic_child_ids`.
- AC2 / EPIC-003 AC7: `tests/test_doctor.py::test_epic_decompose_allocates_after_all_epic_child_ids`.
- AC3 / EPIC-003 AC7: `src/project_workflow/templates/workflow.py` copied to `.project-workflow/cli/workflow.py`.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Shared ID Scan | Add a reusable scan for IDs in nested task folders and all tracker files. | AC1, AC2 | Targeted allocation tests pass. | Done |
| 2 | Standalone Allocation | Use the shared scan for `task init`. | AC1 | Standalone task test assigns after epic child IDs. | Done |
| 3 | Epic Decomposition Allocation | Use the shared scan for `epic decompose`. | AC2 | Epic decompose test assigns after other epic child IDs. | Done |
| 4 | Helper Sync | Sync generated local workflow helper from package template. | AC3 | File comparison passes in final validation. | Done |

## Parent AC Evidence

- EPIC-003 AC7: Implemented `_used_ids_for_prefix` in package CLI and generated workflow template, updated standalone task allocation and epic decomposition allocation to use it, and added targeted tests for both collision paths.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: recursive task ID scan, tracker ID scan, standalone task allocation, epic decomposition allocation, template/helper parity.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py::test_task_init_allocates_after_epic_child_ids tests/test_doctor.py::test_epic_decompose_allocates_after_all_epic_child_ids` passed.
- Findings: None.
- Verdict: Pass.

## Retro

- Reusable lessons: Any code that allocates global task IDs must scan nested epic state, not only root task folders or the global tracker.
- Conventions or agent assets updated: None yet.
- Follow-up tasks: Continue with intake/readiness gates now that child IDs can be allocated safely.
- Missed in-scope work: None.

## Notes

- Task: TASK-010
- Title: Global Task ID Allocation
- Created: 2026-06-17
