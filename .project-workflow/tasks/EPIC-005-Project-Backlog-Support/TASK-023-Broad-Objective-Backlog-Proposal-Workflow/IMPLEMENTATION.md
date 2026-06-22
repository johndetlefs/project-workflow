## User Story

As an owner, I want to describe a broad future objective and receive well-formed backlog candidates, so that product intent is captured before any work is committed to the tracker.

## Parent AC Coverage

- AC4, AC8

## Acceptance Criteria

- [x] AC1: Backlog workflow guidance instructs agents to read project context before drafting candidates.
- [x] AC2: Backlog workflow guidance defines outcome-focused candidate rows using the canonical schema.
- [x] AC3: Backlog workflow guidance prevents automatic tracker/task/epic creation during proposal.
- [x] AC4: Backlog workflow guidance requires owner review before acceptance or promotion.
- [x] AC5: Backlog workflow guidance tells agents to ask focused questions when context is insufficient.

## Validation

- AC1 / parent ACs AC4, AC8: Passed by inspection and generated-asset tests; `Backlog.prompt.md` and `project-backlog/SKILL.md` require reading guidance, constitution, backlog, tracker, and active epic trackers first.
- AC2 / parent ACs AC4, AC8: Passed by inspection of `Backlog.prompt.md`; broad-objective instructions require outcome-focused candidate rows using ID, title, type, priority, status, outcome, promoted-to, and notes.
- AC3 / parent AC AC4: Passed by inspection of prompt and Codex skill; both state not to create tracker rows, task folders, or epic folders while only proposing candidates.
- AC4 / parent AC AC4: Passed by inspection of prompt and Codex skill; both require owner review before accepting or promoting rows.
- AC5 / parent AC AC4: Passed by inspection of prompt and Codex skill; insufficient context routes to focused questions instead of invented strategy.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define broad-objective intake flow | Write backlog workflow guidance for reading project context, extracting candidate rows, and asking focused questions when context is weak. | AC1: Context sources are required.<br>AC2: Candidate rows use the canonical schema.<br>AC5: Insufficient context routes to focused questions. | Passed by source prompt and Codex skill inspection plus generated asset assertions. | Done |
| 2 | Enforce proposal-before-commit behavior | Add guidance that candidate proposal does not create tracker rows, task folders, or epic folders. | AC3: Proposal guidance forbids automatic tracker/task/epic creation. | Passed by prompt/skill inspection; proposal guidance forbids tracker/task/epic mutation. | Done |
| 3 | Require owner review for acceptance and promotion | Add guidance that the owner must confirm candidate acceptance or promotion before canonical state changes. | AC4: Guidance requires owner review before row acceptance or promotion. | Passed by prompt/skill inspection; acceptance and promotion require owner review. | Done |

## Parent AC Evidence

- AC4: Broad-objective guidance now drafts proposed backlog rows from project context, avoids automatic tracker/task/epic creation, requires owner review, and asks focused questions when context is insufficient.
- AC8: The generated `project.backlog` prompt and Codex `project-backlog` skill describe creation, refinement, validation, and promotion behavior consistently.

## QA & Code Review

- Verdict: Pass.
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py` passed with 40 tests; generated asset assertions verify backlog prompt and skill installation; `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor` passed with only pre-existing legacy warnings.
- Findings: No blocking findings in broad-objective backlog guidance.

## Retro

- Reusable lessons: Broad-objective guidance should separate candidate drafting from committed workflow mutation.
- Conventions or agent assets updated: Added `project.backlog` prompt and `project-backlog` Codex skill guidance.
- Follow-up tasks: None.

## Notes

- Task: TASK-023
- Title: Broad-objective backlog proposal workflow
- Created: 2026-06-22
