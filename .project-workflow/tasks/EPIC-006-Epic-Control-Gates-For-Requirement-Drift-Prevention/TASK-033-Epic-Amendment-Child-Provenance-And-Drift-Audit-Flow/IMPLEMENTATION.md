## User Story

As a workflow owner, I want mid-epic child rows to require amendment provenance, so that reactive fixes and newly discovered work cannot silently expand or reinterpret the epic.

## Parent AC Coverage

- AC8, AC9, AC12, AC14

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

- AC8: owner `TASK-033`; required evidence: Amendment records and reactive-fix gate tests.
- AC9: owner `TASK-033, TASK-037`; required evidence: Decomposition or amendment provenance and active row gate tests.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.
- AC14: owner `TASK-031, TASK-033, TASK-037`; required evidence: Decomposition plan authority, amendment provenance, and child inheritance gates.

## Acceptance Criteria

- [x] AC1: New epics include `AMENDMENTS.md` with an approved child-row amendment table. Covers parent AC8 and AC9.
- [x] AC2: `epic amend` records owner-approved amendment metadata and appends the matching Proposed child row. Covers parent AC8 and AC14.
- [x] AC3: Child rows outside `DECOMPOSITION.md` can advance only when a matching valid amendment exists. Covers parent AC9 and AC14.
- [x] AC4: Direct tracker edits outside decomposition/amendment authority remain blocked by approval/status/doctor gates. Covers parent AC9 and AC14.
- [x] AC5: Regression tests cover amendment authority and existing decomposition authority. Covers parent AC12.

## Validation

- AC1 / AC8 / AC9: `cmd_epic_init` and backlog epic promotion now create `AMENDMENTS.md` using `_epic_amendments_template`.
- AC2 / AC8 / AC14: `cmd_epic_amend` records owner-approved amendment metadata and appends the matching Proposed child row.
- AC3 / AC9 / AC14: `_decomposition_plan_authority_issues` now accepts valid amendment rows when a child is outside `DECOMPOSITION.md`.
- AC4 / AC9 / AC14: Existing outside-plan rejection remains enforced; missing/placeholder amendment metadata remains invalid authority.
- AC5 / AC12: Focused regression run passed: `9 passed, 55 deselected`; full suite passed: `64 passed`.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Amendment artifact | Add `AMENDMENTS.md` template and create it for new epics. | AC1 | Focused and full pytest suite. | Done |
| 2 | Amendment command | Add `epic amend` to record approved amendment metadata and append a Proposed child row. | AC2 | `test_epic_amend_authorizes_child_outside_decomposition_plan`. | Done |
| 3 | Authority gate integration | Let valid amendment rows satisfy child-row authority while preserving decomposition enforcement. | AC3, AC4 | Focused decomposition/amendment tests. | Done |
| 4 | Guidance updates | Update README, CLI README, generated guidance, and project-epic skill. | AC5 | Full pytest suite. | Done |

## Parent AC Evidence

- AC8: `epic amend` records owner-approved amendment metadata for mid-epic child work and reactive fixes.
- AC9: Child rows still require decomposition or amendment provenance before approval/scaffold/status advancement.
- AC12: Added `test_epic_amend_authorizes_child_outside_decomposition_plan`; focused and full suites pass.
- AC14: Amendment authority is matched by child ID, title, and parent AC coverage, preserving owner-controlled decomposition without per-row approval fatigue for unchanged plan rows.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py -k "amend or decomposition_plan or decompose or decomposition_authority"` passed with 9 selected tests; `.venv/bin/python -m pytest` passed with 64 tests.
- Findings: No blocking findings.

## Retro

- Reusable lessons: Amendment support belongs in the same authority gate as decomposition; a separate note would not prevent direct tracker drift.
- Conventions or agent assets updated: README, CLI README, generated guidance block, and project-epic skill now route mid-epic work through `epic amend`.
- Follow-up tasks: TASK-034 still needs legacy adoption so old rows can be safely brought under these gates.

## Notes

- Task: TASK-033
- Title: Epic Amendment Child Provenance And Drift Audit Flow
- Created: 2026-07-09
