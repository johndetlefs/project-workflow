## User Story

As a project owner, I want task and epic work blocked when it drifts outside approved requirements, so that agents cannot start from unreviewed, stale, or out-of-scope requirements while still working autonomously inside the approved boundary.

## Parent AC Coverage

- AC1, AC11, AC12, AC13, AC16, AC18

## Acceptance Criteria

- [x] AC1: Task and epic requirements templates include a parseable owner approval envelope block with reviewed flags, approval state, approver/source, approval date, approved artifact identity, and scope covered by the approval.
- [x] AC2: CLI approval commands can record approval envelopes for standalone tasks and epics with non-placeholder owner approval source text.
- [x] AC3: Approval validation rejects missing approval, placeholder approval, agent-only approval, missing source, missing artifact identity, stale approval after material requirements/AC edits, and work outside the approved envelope.
- [x] AC4: `task ready`, `task status`, `epic ready`, `epic decompose`, `epic approve`, `epic scaffold-child`, `epic lifecycle`, `epic status`, and `epic closeout` enforce the relevant approval envelope before gated movement while allowing ordinary matching child work inside the envelope.
- [x] AC5: Doctor/validate fails current invalid states even if they were created by manual edits rather than CLI commands.
- [x] AC6: The bounded discovery exception allows read-only inspection and explicitly allowed findings-only artifacts while still blocking product source changes and gated lifecycle movement.
- [x] AC7: Templates, CLI README, and generated agent guidance explain the approval envelope without adding proof-recipe or visual-fidelity concepts to ordinary tasks.
- [x] AC8: Automated tests cover the parent drift failures assigned to this child: work starts without owner approval, approval becomes stale after requirements edits, outside-envelope work proceeds, and manual tracker/doc edits bypass CLI commands.
- [x] AC9: Gated commands and doctor checks do not require fresh owner approval for unchanged work inside the approved authority envelope; they either pass or fail with a specific drift/evidence/staleness reason.

## Validation

- AC1: Verified by template changes in `.project-workflow/cli/workflow.py`, `src/project_workflow/cli.py`, and `src/project_workflow/templates/workflow.py`; covered by `test_task_scaffold_uses_ac_mapped_implementation_shape`.
- AC2: Verified by `test_task_approval_envelope_command_and_stale_detection`.
- AC3: Verified by stale approval checks in `test_task_approval_envelope_command_and_stale_detection` and invalid approval source validation in command implementation.
- AC4: Verified by existing task/epic lifecycle tests plus `test_epic_child_ready_uses_parent_approval_envelope_without_child_approval`.
- AC5: Verified by `test_doctor_flags_manual_active_task_without_approval_envelope`.
- AC6: Verified by `test_discovery_task_ready_allows_bounded_discovery`.
- AC7: Verified by README, CLI README, generated managed block, and Codex skill updates; suite includes init/generated asset coverage.
- AC8: Verified by approval-envelope regression tests added in `tests/test_doctor.py`.
- AC9: Verified by `test_epic_child_ready_uses_parent_approval_envelope_without_child_approval`.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Approval envelope model | Define parser/serializer, approved artifact identity, and scope membership for owner approval envelopes. | AC1, AC3 | Tests show valid, invalid, stale, and outside-envelope approval states are classified correctly. | Done |
| 2 | Approval CLI commands | Add supported task and epic command paths for recording owner approval source, freshness identity, and scope covered. | AC2, AC3 | CLI tests prove command-written approval passes and placeholder/agent-only/outside-envelope source fails. | Done |
| 3 | Lifecycle gate integration | Wire approval envelope checks into task and epic ready/status/decompose/approve/scaffold/lifecycle/closeout commands. | AC4, AC6 | Lifecycle tests prove unapproved/stale/outside-envelope work is blocked, ordinary in-envelope work proceeds, and discovery remains bounded. | Done |
| 4 | Doctor state validation | Add doctor checks for invalid current states created outside supported CLI transitions. | AC5 | Doctor fixture tests fail manual bypass states. | Done |
| 5 | Templates and guidance | Update generated templates, CLI README, and managed agent guidance for the approval gate. | AC1, AC7 | Generated assets contain the approval block and concise usage guidance. | Done |
| 6 | Bounded prompt behavior | Ensure approval gates distinguish owner decisions from agent-fixable drift/evidence failures. | AC4, AC9 | Tests show unchanged in-envelope work proceeds and invalid work fails with concrete reasons rather than generic approval prompts. | Done |
| 7 | Regression tests | Add targeted regression fixtures for missing approval, stale approval, outside-envelope work, in-envelope autonomy, and manual bypass drift. | AC8, AC9 | Test suite fails before fix and passes after fix. | Done |

## Parent AC Evidence

- AC1: Approval envelope block added to task, epic, and epic-child requirements templates; lifecycle commands enforce the envelope.
- AC11: README, CLI README, generated managed block, and Codex task/epic skills explain approval envelopes and bounded approval prompts.
- AC12: `.venv/bin/python -m pytest` passed with 52 tests on 2026-07-09.
- AC13: Approval artifact identity uses a hash of requirements content excluding the approval block; stale approval is rejected after material requirements edits.
- AC16: Doctor flags manual active-state bypasses without approval envelopes.
- AC18: Epic children inside an approved parent envelope proceed without separate child approval; failures report concrete stale/missing/out-of-envelope reasons.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/python -m pytest` passed with 52 tests on 2026-07-09; `./.project-workflow/cli/workflow doctor` passed with expected pre-existing approval-envelope warnings for legacy/open work outside TASK-028.
- Findings: No TASK-028 blocking findings. Remaining approval-envelope warnings are pre-existing work that belongs to the legacy adoption path, not this child.

## Retro

- Reusable lessons: Approval gates must operate as scope envelopes and drift checks, not repeated user approval prompts.
- Conventions or agent assets updated: README, CLI README, generated managed block, and Codex task/epic skills.
- Follow-up tasks: Legacy adoption remains covered by TASK-034; decomposition-plan authority remains covered by TASK-037.

## Notes

- Task: TASK-028
- Title: Approved Scope Authority Gate
- Created: 2026-07-09
- Implementation code changes are approved only inside the EPIC-006 authority envelope; material scope changes require renewed owner review.
