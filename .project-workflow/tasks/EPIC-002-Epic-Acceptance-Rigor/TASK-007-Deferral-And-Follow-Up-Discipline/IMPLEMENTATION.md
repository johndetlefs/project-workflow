## User Story

As a project-workflow maintainer, I want deferrals and retro follow-ups to be recorded distinctly, so incomplete parent AC work cannot be hidden as "done".

## Goal

- Satisfy EPIC-002 AC10 and AC12 with structured deferral artifacts, closeout validation, and retro guidance.

## Parent AC Coverage

- EPIC-002 AC10: Owner-approved deferrals are structured with decision, date, reason, and follow-up reference.
- EPIC-002 AC12: Retro guidance distinguishes follow-ups from missed in-scope work.

## Acceptance Criteria

- [x] AC1: Covers EPIC-002 AC10 by creating `DEFERRALS.md` for new epics and validating approved deferral metadata during closeout.
- [x] AC2: Covers EPIC-002 AC12 by updating generated retro guidance to separate follow-up tasks from missed in-scope work.

## Approach

- Add a deferrals table template and create it during `epic init`.
- Parse deferrals during audit/closeout and accept only approved rows with owner, decision date, reason, and follow-up.
- Update generated retro skill and prompt guidance, then mirror the installed prompt.

## Phases

### Phase 1

- Add `DEFERRALS.md` template and closeout parsing.
- Add fixture tests for approved and incomplete deferrals.

### Phase 2

- Update retro guidance and prompt mirror.
- Run tests and doctor checks.

## Tasks

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Structured Deferrals | Add `DEFERRALS.md` and closeout validation for approved owner deferrals with follow-up references. | AC1 / EPIC-002 AC10: approved deferral passes, incomplete deferral blocks. | Run deferral closeout fixtures. | Done |
| 2 | Retro Separation | Update retro guidance to distinguish follow-ups from missed in-scope work. | AC2 / EPIC-002 AC12: generated retro assets contain separate guidance. | Inspect generated retro skill/prompt and prompt mirror. | Done |

## Validation

- AC1 / EPIC-002 AC10: `tests/test_doctor.py::test_epic_closeout_accepts_approved_deferral_with_follow_up` and `tests/test_doctor.py::test_epic_closeout_blocks_incomplete_deferral_metadata`.
- AC2 / EPIC-002 AC12: generated retro skill and prompt updates, with `.github/prompts/Retro.prompt.md` mirrored from source.

## Parent AC Evidence

- EPIC-002 AC10: Implemented `DEFERRALS.md`, deferral parsing, approved-deferral closeout pass, and incomplete-deferral closeout block. Evidence: deferral fixture tests passed.
- EPIC-002 AC12: Implemented retro guidance separation in `src/project_workflow/codex/skills/project-retro/SKILL.md`, `src/project_workflow/prompts/Retro.prompt.md`, and `.github/prompts/Retro.prompt.md`. Evidence: prompt mirror comparison returned 0 and tests passed.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: deferral table schema, approved deferral gate, incomplete deferral blocker, `DEFERRALS.md` generation, retro guidance, and prompt mirror.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 23 tests; prompt mirror comparison returned 0.
- AC evidence: AC1 / EPIC-002 AC10 covered by approved and incomplete deferral fixtures; AC2 / EPIC-002 AC12 covered by retro skill/prompt updates.
- Verdict: Pass.
- Findings: None.

## Retro

- Reusable lessons: Deferrals are closeout inputs, not comments; requiring follow-up IDs prevents hidden "done" scope.
- Conventions or agent assets updated: Retro skill and prompt now separate follow-up tasks from missed in-scope work.
- Follow-up tasks: TASK-008 should add tracker-safe lifecycle commands so epic child status changes stop requiring manual edits.
- Missed in-scope work: None.

## Notes

- Task: TASK-007
- Title: Deferral And Follow-Up Discipline
- Created: 2026-06-17
