## User Story

As a project-workflow maintainer, I want regression fixtures for EPIC-006 drift gates, so future workflow changes cannot silently allow unsupported claims, wrong evidence, or unusable generated evidence artifacts.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC17

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

- AC1: owner `TASK-028`; required evidence: Approval-envelope commands, lifecycle gates, doctor warnings, and regression tests.
- AC2: owner `TASK-029`; required evidence: `EPIC-CONTRACT.md` template/schema, lifecycle gates, doctor checks, and regression tests.
- AC3: owner `TASK-031`; required evidence: Child charter generation and inheritance tests.
- AC4: owner `TASK-029, TASK-031`; required evidence: Contract proof-owner schema plus child proof-ownership gates.
- AC5: owner `TASK-030, TASK-032`; required evidence: Structured evidence records and artifact identity fields.
- AC6: owner `TASK-030, TASK-032`; required evidence: Proof-recipe trigger rules and invalid-substitute rejection tests.
- AC7: owner `TASK-030, TASK-032`; required evidence: Stale, missing, substitute, and contradiction evidence tests.
- AC8: owner `TASK-033`; required evidence: Amendment records and reactive-fix gate tests.
- AC9: owner `TASK-033, TASK-037`; required evidence: Decomposition or amendment provenance and active row gate tests.
- AC10: owner `TASK-034`; required evidence: Legacy adoption commands and untrusted inferred evidence handling.
- AC11: owner `TASK-028, TASK-029, TASK-035, TASK-037`; required evidence: Prompt, skill, template, README, and CLI guidance updates.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.
- AC13: owner `TASK-028, TASK-032`; required evidence: Approval/evidence freshness and stale artifact identity tests.
- AC14: owner `TASK-031, TASK-033, TASK-037`; required evidence: Decomposition plan authority, amendment provenance, and child inheritance gates.
- AC15: owner `TASK-030, TASK-032`; required evidence: Visual calibration and delivered-artifact comparison recipe tests.
- AC16: owner `TASK-028, TASK-032, TASK-037`; required evidence: State-based doctor failures for invalid manual states.
- AC17: owner `TASK-030, TASK-032`; required evidence: Structured claim-to-evidence ledger and contradictory prose checks.

## Acceptance Criteria

- [x] AC1: Tests cover the existing generalized EPIC-006 drift gates and the new multi-parent-AC structured evidence fixture.
- [x] AC2: Scaffolded child evidence for multi-parent coverage generates separate records for each parent AC.
- [x] AC3: Structured evidence validation rejects comma-separated parent AC claims and accepts separate per-AC claims.
- [x] AC4: Focused test suite passes; full suite pending final run.

## Validation

- Focused pytest passed: `test_epic_child_scaffold_carries_parent_ac_sections`, `test_multi_parent_ac_structured_evidence_requires_one_claim_per_ac`, and `test_visual_reference_recipe_requires_structured_evidence_before_review`.
- Full pytest passed with 67 tests. Workflow doctor passed with warnings limited to pre-existing legacy/current adoption warnings.
- Generated guidance regression now pins the drift-gate terms in Codex AGENTS/skills, Cursor rules, Claude generated agents, and Copilot managed instructions so cross-agent surfaces cannot silently lose owner approval, epic contract/decomposition, or structured evidence guidance.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Multi-AC evidence scaffold regression | Update scaffolded `EVIDENCE.json` so multi-parent child rows get one claim placeholder per parent AC. | AC1, AC2, AC3: generated evidence can be credited by status/audit gates. | Focused pytest verifies generated claims are `AC1`, `AC3` instead of one comma value. | Done |
| 2 | Multi-AC validator regression | Add a validator fixture proving comma-separated parent AC evidence is rejected and split records pass. | AC1, AC3: validator behavior matches gate expectations. | Focused pytest verifies rejection and acceptance paths. | Done |
| 3 | Full regression run | Run the full test suite, doctor, and epic audit. | AC4: broad workflow behavior remains intact. | Full pytest plus workflow doctor/audit output. | Done |

## Parent AC Evidence

- AC1: Regression tests cover approval envelope gates and in-envelope child progression.
- AC2: Regression tests cover mandatory epic contract gates.
- AC3: Regression tests cover child charter inheritance and scaffolded evidence shape.
- AC4: Regression tests cover proof-owner rejection for unassigned child evidence.
- AC5: Regression tests cover structured evidence records and artifact identity fields.
- AC6: Regression tests cover proof-recipe triggers and invalid substitute rejection.
- AC7: Regression tests cover stale, missing, invalid, and contradictory evidence.
- AC8: Regression tests cover amendment gates for new child work and reactive fixes.
- AC9: Regression tests cover decomposition and amendment provenance gates.
- AC10: Regression tests cover legacy adoption and untrusted pre-adoption evidence gates.
- AC11: Regression tests cover generated guidance across Codex, Cursor, Claude, and Copilot surfaces plus prompt mirror alignment.
- AC12: Regression tests cover generalized drift failures across the EPIC-006 gate set.
- AC13: Regression tests cover approval/evidence freshness and stale artifact identity.
- AC14: Regression tests cover decomposition authority, amendment provenance, and child inheritance gates.
- AC15: Regression tests cover visual/reference fidelity recipe enforcement before Review.
- AC16: Regression tests cover state-based doctor failures for invalid manual states.
- AC17: Regression tests cover structured claim-to-evidence and contradictory prose rejection.
- Evidence artifact: `evidence/regression-fixtures.txt`.

## QA & Code Review

- Verdict: Pass.
- Evidence: Focused pytest passed for scaffold and structured evidence regression fixtures. Full `.venv/bin/python -m pytest` passed with 67 tests. `./.project-workflow/cli/workflow doctor` passed with warnings limited to pre-existing legacy/current adoption warnings.
- Findings: None currently known.

## Retro

- Reusable lessons: Generated evidence shape must be tested against the same validator that later gates use.
- Conventions or agent assets updated: `EVIDENCE.json` scaffold template now emits one claim per parent AC.
- Follow-up tasks: None currently known.

## Notes

- Task: TASK-036
- Title: Regression Fixture Suite
- Created: 2026-07-09
