## User Story

As a maintainer, I want a safe adoption path for pre-existing work, so that legacy tasks and epics can enter the new gates without trusting stale inferred evidence.

## Parent AC Coverage

- AC10, AC12

## Child Charter

### Inherited Invariants

- Parent AC IDs remain stable.
- Approved child rows must match ID, title, and parent AC coverage in `DECOMPOSITION.md`.
- Missing or placeholder contract sections are not valid authority for new/adopted epics.
- Legacy epics without approval envelopes warn until adoption rather than blocking unrelated current work.

### Invalid Substitutes

- Tracker rows without matching `DECOMPOSITION.md` authority.
- Prose summaries that are not backed by child implementation evidence.
- Legacy warnings from unadopted old epics as proof that new/adopted epics satisfy gates.
- Generic owner approval prompts when the work remains inside the approved authority envelope.

### Artifact Targets

- `.project-workflow/cli/workflow.py`
- `src/project_workflow/cli.py`
- `src/project_workflow/templates/workflow.py`
- `tests/test_doctor.py`
- `README.md`
- `.project-workflow/cli/README.md`
- `src/project_workflow/codex/skills/project-epic/SKILL.md`

### Parent AC Proof Ownership

- AC10: owner `TASK-034`; required evidence: Legacy adoption commands and untrusted inferred evidence handling.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.

## Acceptance Criteria

- [x] AC1: `task adopt` records owner approval and `Legacy Adoption` metadata for pre-existing standalone tasks. Covers parent AC10.
- [x] AC2: `epic adopt` records owner approval and `Legacy Adoption` metadata for pre-existing epics and ensures `AMENDMENTS.md` exists. Covers parent AC10.
- [x] AC3: Adopted work defaults pre-adoption inferred evidence to untrusted until refreshed. Covers parent AC10.
- [x] AC4: Completion gates block unrefreshed adopted task evidence, and refreshed adoption allows completion. Covers parent AC10.
- [x] AC5: Regression tests cover adoption behavior. Covers parent AC12.

## Validation

- AC1 / AC10: `cmd_task_adopt` writes approval and `Legacy Adoption` metadata for standalone tasks.
- AC2 / AC10: `cmd_epic_adopt` writes approval and `Legacy Adoption` metadata for epics and creates `AMENDMENTS.md` if missing.
- AC3 / AC10: Adoption defaults `Evidence refreshed after adoption: No`.
- AC4 / AC10: `task status --to Complete` rejects unrefreshed adopted evidence and accepts refreshed adoption.
- AC5 / AC12: Focused adoption tests passed: `4 passed, 62 deselected`; full suite passed: `66 passed`.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Standalone adoption | Add `task adopt` and legacy adoption metadata. | AC1, AC3 | Focused adoption tests. | Done |
| 2 | Epic adoption | Add `epic adopt` and amendment-log creation for legacy epics. | AC2, AC3 | Focused adoption tests. | Done |
| 3 | Untrusted evidence gate | Block completion when adopted evidence is not refreshed and warn in doctor. | AC3, AC4 | Focused adoption tests. | Done |
| 4 | Guidance and regression | Update guidance and add adoption regression tests. | AC5 | Full pytest suite. | Done |

## Parent AC Evidence

- AC10: Legacy adoption commands and untrusted evidence handling implemented in CLI, status gates, and doctor.
- AC12: Added regression tests for task adoption, epic adoption, untrusted evidence blocking, refreshed evidence completion, and amendment-log creation.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py -k "adopt or legacy"` passed with 4 selected tests; `.venv/bin/python -m pytest` passed with 66 tests.
- Findings: No blocking findings.

## Retro

- Reusable lessons: Adoption metadata must be excluded from approval identity; otherwise adoption itself stales the approval envelope.
- Conventions or agent assets updated: README, CLI README, generated guidance, project-epic skill, and project-implement skill now route old work through adoption commands.
- Follow-up tasks: None for adoption; remaining EPIC-006 slices cover guidance consolidation and broader regression fixtures.

## Notes

- Task: TASK-034
- Title: Legacy Adoption Path
- Created: 2026-07-09
