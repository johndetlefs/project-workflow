# Epic Contract

## Summary

- Epic: EPIC-006
- Title: Epic Control Gates For Requirement Drift Prevention
- Last updated: 2026-07-09

## Sources of Truth

- Owner-approved EPIC-006 `REQUIREMENTS.md` and its Owner Approval envelope.
- EPIC-006 `DECOMPOSITION.md` for authorized child rows.
- Child `REQUIREMENTS.md` and `IMPLEMENTATION.md` files for assigned child evidence.
- Project workflow CLI tests in `tests/test_doctor.py` for enforced gate behavior.

## Invalid Substitutes

- Tracker rows without matching `DECOMPOSITION.md` authority.
- Prose summaries that are not backed by child implementation evidence.
- Legacy warnings from unadopted old epics as proof that new/adopted epics satisfy gates.
- Generic owner approval prompts when the work remains inside the approved authority envelope.

## Invariants

- Parent AC IDs remain stable.
- Approved child rows must match ID, title, and parent AC coverage in `DECOMPOSITION.md`.
- Missing or placeholder contract sections are not valid authority for new/adopted epics.
- Legacy epics without approval envelopes warn until adoption rather than blocking unrelated current work.

## Artifact Targets

- `.project-workflow/cli/workflow.py`
- `src/project_workflow/cli.py`
- `src/project_workflow/templates/workflow.py`
- `tests/test_doctor.py`
- `README.md`
- `.project-workflow/cli/README.md`
- `src/project_workflow/codex/skills/project-epic/SKILL.md`

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-028, TASK-035, TASK-036 | Approval-envelope commands, lifecycle gates, guidance updates, doctor warnings, and regression tests. |
| AC2 | TASK-029, TASK-035, TASK-036 | `EPIC-CONTRACT.md` template/schema, lifecycle gates, guidance updates, doctor checks, and regression tests. |
| AC3 | TASK-031, TASK-035, TASK-036 | Child charter generation, guidance updates, inheritance tests, and regression tests. |
| AC4 | TASK-029, TASK-031, TASK-036 | Contract proof-owner schema plus child proof-ownership gates and regression tests. |
| AC5 | TASK-030, TASK-032, TASK-035, TASK-036 | Structured evidence records, guidance updates, artifact identity fields, and regression tests. |
| AC6 | TASK-030, TASK-032, TASK-035, TASK-036 | Proof-recipe trigger rules, guidance updates, invalid-substitute rejection tests, and regression tests. |
| AC7 | TASK-030, TASK-032, TASK-036 | Stale, missing, substitute, contradiction evidence tests, and regression tests. |
| AC8 | TASK-033, TASK-035, TASK-036 | Amendment records, guidance updates, reactive-fix gate tests, and regression tests. |
| AC9 | TASK-033, TASK-036, TASK-037 | Decomposition or amendment provenance, active row gate tests, and regression tests. |
| AC10 | TASK-034, TASK-035, TASK-036 | Legacy adoption commands, guidance updates, untrusted inferred evidence handling, and regression tests. |
| AC11 | TASK-028, TASK-029, TASK-035, TASK-036, TASK-037 | Prompt, skill, template, README, CLI guidance updates, and regression tests. |
| AC12 | TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037 | Regression tests for generalized drift failures. |
| AC13 | TASK-028, TASK-032, TASK-035, TASK-036 | Approval/evidence freshness, guidance updates, stale artifact identity tests, and regression tests. |
| AC14 | TASK-031, TASK-033, TASK-035, TASK-036, TASK-037 | Decomposition plan authority, amendment provenance, guidance updates, child inheritance gates, and regression tests. |
| AC15 | TASK-030, TASK-032, TASK-035, TASK-036 | Visual calibration, guidance updates, delivered-artifact comparison recipe tests, and regression tests. |
| AC16 | TASK-028, TASK-032, TASK-036, TASK-037 | State-based doctor failures for invalid manual states and regression tests. |
| AC17 | TASK-030, TASK-032, TASK-035, TASK-036 | Structured claim-to-evidence ledger, guidance updates, contradictory prose checks, and regression tests. |
| AC18 | TASK-028, TASK-037 | Bounded approval prompts and in-envelope child progression evidence. |
