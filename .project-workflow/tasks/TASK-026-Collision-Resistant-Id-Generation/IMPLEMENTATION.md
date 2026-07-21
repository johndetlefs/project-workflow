## User Story

As a maintainer working across multiple branches, I want optional collision-resistant
workflow IDs, so that team task and epic creation can merge cleanly without manual
renumbering.

## Acceptance Criteria

- [x] AC1: With no ID generation config, task, epic, and backlog creation continue to use existing sequential IDs.
- [x] AC2: With `id_generation` configured to `unique`, new task, epic, and backlog IDs use a 5-character uppercase base36 suffix and keep the appropriate prefix.
- [x] AC3: Unique ID generation scans existing tracker rows, epic trackers, backlog rows, and workflow task folders before accepting a candidate.
- [x] AC4: Doctor/backlog validation accepts configured unique promoted references and still detects duplicate or malformed workflow IDs.
- [x] AC5: README and generated agent guidance describe the unique ID mode clearly.

## Validation

- AC1: Full suite passed: `.venv/bin/python -m pytest`.
- AC2: `test_unique_id_generation_for_task_epic_backlog_and_promotion` asserts 5-character uppercase base36 task, epic, backlog, and promoted IDs.
- AC3: `test_unique_id_allocator_retries_local_collisions` forces an allocator collision and verifies regeneration.
- AC4: `test_unique_id_generation_for_task_epic_backlog_and_promotion` validates unique promoted references; `test_doctor_detects_duplicate_configured_unique_tracker_ids` verifies duplicate detection.
- AC5: README, changelog, generated Codex/Cursor guidance, prompts, and task/backlog/epic skills updated. `./.project-workflow/cli/workflow doctor` passed with only pre-existing legacy warnings.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add config model | Extend workflow config with `id_generation` and unique suffix length defaults. | AC1, AC2 | Config loader and default behavior tests pass. | Done |
| 2 | Implement ID allocator | Add shared sequential/unique ID helper with base36 `secrets` generation and collision checks. | AC2, AC3 | Unique generation and retry tests pass. | Done |
| 3 | Wire creation paths | Use the allocator for task init, epic init, backlog add/promote, and epic decomposition. | AC1, AC2, AC3 | CLI behavior tests pass. | Done |
| 4 | Update validation | Teach doctor/backlog validation and status normalization to accept configured unique IDs. | AC4 | Validation tests pass. | Done |
| 5 | Update docs and generated guidance | Document unique mode and update generated agent references from `TASK-###` assumptions. | AC5 | README/guidance review and doctor pass. | Done |

## QA & Code Review

- Review date: 2026-07-21
- Reviewed areas: Config compatibility, unique ID allocation, collision retry behavior, task/epic/backlog creation paths, doctor/backlog validation, generated guidance, and README coverage.
- AC1 evidence: `test_unique_id_generation_for_task_epic_backlog_and_promotion` and the full suite confirm sequential IDs remain the compatibility default.
- AC2 evidence: The unique-ID test confirms configured task, epic, backlog, and promoted IDs retain their prefixes and use five-character uppercase base36 suffixes.
- AC3 evidence: `test_unique_id_allocator_retries_local_collisions` and the unique-ID integration test cover collision detection across local workflow state and regeneration.
- AC4 evidence: Unique promoted references validate successfully, while duplicate configured unique tracker IDs remain detectable.
- AC5 evidence: Current README and generated agent guidance document unique ID mode and reserved workflow namespaces.
- Owner verification: John Detlefs confirmed on 2026-07-21 that TASK-026 is working and explicitly requested completion.
- Automated evidence: `.venv/bin/python -m pytest` passed 73 tests with one pre-existing UVX/network integration test skipped; `task adopt --evidence-refreshed` recorded the current approval envelope.
- Findings: None.
- Verdict: Pass

## Retro

- Retro date: 2026-07-21
- Reusable lessons: Collision-resistant IDs are most useful as an opt-in compatibility layer; preserving sequential defaults avoids unnecessary churn while unique mode protects concurrent branches and agents.
- Conventions or agent assets updated: The implementation, tests, README, and generated guidance already carry the durable unique-ID convention. No further asset change was required during closeout.
- Follow-up suggestions: Stronger atomic backlog/write safety remains separately tracked by BL-007 and EPIC-007 AC6.
- Missed in-scope work: None.

## Notes

- Task: TASK-026
- Title: Collision-Resistant ID Generation
- Created: 2026-06-25
