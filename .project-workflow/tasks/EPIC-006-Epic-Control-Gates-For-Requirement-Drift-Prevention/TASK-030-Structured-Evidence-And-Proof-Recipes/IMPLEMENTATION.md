## User Story

As a workflow user, I want proof-recipe-triggered claims to require structured evidence, so that long epic closeout cannot substitute generic QA prose for visual, runtime, deployment, or contract proof.

## Parent AC Coverage

- AC5, AC6, AC7, AC12, AC15, AC17

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

- AC5: owner `TASK-030, TASK-032`; required evidence: Structured evidence records and artifact identity fields.
- AC6: owner `TASK-030, TASK-032`; required evidence: Proof-recipe trigger rules and invalid-substitute rejection tests.
- AC7: owner `TASK-030, TASK-032`; required evidence: Stale, missing, substitute, and contradiction evidence tests.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.
- AC15: owner `TASK-030, TASK-032`; required evidence: Visual calibration and delivered-artifact comparison recipe tests.
- AC17: owner `TASK-030, TASK-032`; required evidence: Structured claim-to-evidence ledger and contradictory prose checks.

## Acceptance Criteria

- [x] AC1: `EVIDENCE.json` exists as the structured evidence ledger for recipe-triggered child work and supports recipe-specific required fields. Covers parent AC5.
- [x] AC2: Proof-recipe trigger rules require structured evidence before Review/Complete for visual/reference-fidelity claims. Covers parent AC6 and AC15.
- [x] AC3: Invalid substitutes are rejected by status/audit/doctor gates. Covers parent AC6 and AC7.
- [x] AC4: Epic audit only gives parent AC credit when recipe-triggered claims have valid structured evidence from the assigned child. Covers parent AC5 and AC17.
- [x] AC5: Doctor fails invalid Review/Complete states created outside supported lifecycle commands. Covers parent AC7 and AC17.
- [x] AC6: Regression tests cover missing structured evidence, invalid substitute evidence, and valid structured evidence for generalized visual/reference proof drift. Covers parent AC12.
- [x] AC7: Non-triggered ordinary work remains lightweight and is not forced to complete scaffolded evidence records. Covers parent AC6.

## Validation

- AC1 / AC5: `STRUCTURED_EVIDENCE_FILENAME`, recipe field definitions, JSON loader, and required-field validator added in `.project-workflow/cli/workflow.py`, synced to `src/project_workflow/cli.py` and `src/project_workflow/templates/workflow.py`.
- AC2 / AC6 / AC15: `test_visual_reference_recipe_requires_structured_evidence_before_review` proves a visual/reference claim cannot move from Testing to Review without `EVIDENCE.json`.
- AC3 / AC6 / AC7: `test_invalid_substitute_structured_evidence_blocks_doctor_and_audit` proves invalid substitute evidence fails doctor and prevents epic audit credit.
- AC4 / AC5 / AC17: `test_valid_structured_visual_evidence_satisfies_epic_audit` proves valid structured evidence is accepted by epic audit.
- AC5 / AC7 / AC17: Doctor now emits blocking errors for invalid Review/Complete states when triggered structured evidence is missing or invalid.
- AC6 / AC12: Focused regression run passed: `3 passed, 58 deselected`.
- AC6 / AC12: Full suite passed: `61 passed`.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Structured evidence schema | Add child-local `EVIDENCE.json`, recipe-specific required fields, evidence artifact checks, and invalid-substitute detection. | AC1, AC3 | Focused and full pytest suite. | Done |
| 2 | Recipe trigger gates | Trigger built-in proof recipes from requirements/material claims and block Review/Complete when evidence is missing or invalid. | AC2, AC5, AC7 | Focused lifecycle regression tests. | Done |
| 3 | Epic audit integration | Make epic audit refuse parent AC credit when triggered structured evidence is invalid. | AC4 | Audit regression tests. | Done |
| 4 | Guidance updates | Update README, CLI README, project-epic skill, project-qa-review skill, and generated managed block guidance. | AC6, AC7 | Full pytest suite plus file review. | Done |

## Parent AC Evidence

- AC5: Structured evidence records and artifact fields implemented through `EVIDENCE.json`, recipe field definitions, evidence artifact validation, and scaffold support.
- AC6: Recipe trigger rules and invalid-substitute rejection implemented; non-triggered work remains lightweight.
- AC7: Status, doctor, and audit gates reject missing/invalid/substitute structured evidence for triggered claims.
- AC12: Added generalized regression tests for missing visual proof, invalid substitute proof, and valid structured proof.
- AC15: Visual/reference-fidelity claims now require structured evidence before Review/Complete and cannot be satisfied by QA prose alone.
- AC17: Material parent AC credit in epic audit now depends on structured claim records when recipes are triggered.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py -k "structured or recipe or visual_reference or invalid_substitute or valid_structured"` passed with 3 selected tests; `.venv/bin/python -m pytest` passed with 61 tests.
- Findings: No blocking findings. TASK-032 still owns deeper artifact identity freshness and contradiction checks.

## Retro

- Reusable lessons: Evidence gates need to live in status, doctor, and audit paths; a template-only evidence file would be passive documentation.
- Conventions or agent assets updated: README, CLI README, generated managed block, project-epic skill, and project-qa-review skill now describe recipe-triggered structured evidence.
- Follow-up tasks: TASK-032 should add artifact identity freshness and generated-summary contradiction checks on top of these structured records.

## Notes

- Task: TASK-030
- Title: Structured Evidence And Proof Recipes
- Created: 2026-07-09
