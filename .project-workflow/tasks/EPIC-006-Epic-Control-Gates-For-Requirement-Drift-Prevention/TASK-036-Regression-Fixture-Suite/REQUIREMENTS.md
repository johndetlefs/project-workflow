# Requirements

## Summary

- Task: TASK-036
- Title: Regression Fixture Suite
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC17
- Last updated: 2026-07-09

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

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

## Goal

Add regression coverage for the generalized EPIC-006 drift failures so future workflow changes cannot reintroduce requirement drift, wrong-proof substitution, stale/contradictory evidence, unapproved child work, or legacy adoption bypasses.

## Non-Goals

- Do not exhaustively test every CLI branch; focus on high-risk drift gates and fixture classes.
- Do not add domain-specific ChatGPT/MCP/widget behavior to core tests except as generalized proof-pattern fixtures.
- Do not replace existing unit tests that already cover an AC; extend coverage where a failure class remains uncovered.

## Users & Context

- Workflow maintainers need regression tests that pin the enforcement behavior introduced by EPIC-006.
- Agents need generated artifacts that are usable by gates without hidden shape mismatches.
- Owners need confidence that future changes cannot silently weaken approval, decomposition, evidence, amendment, adoption, or visual/runtime proof gates.

## Requirements (Outcome-Focused)

- Cover generalized drift failures listed in EPIC-006 validation, including owner approval, contract, child charter, proof ownership, structured evidence, invalid substitutes, stale evidence, runtime target/source contradiction, decomposition/amendment provenance, legacy adoption, and state-based doctor failures.
- Add a regression for the multi-parent-AC structured evidence shape exposed during TASK-035: generated `EVIDENCE.json` must create one claim record per inherited parent AC, not a comma-separated value that later gates cannot credit.
- Keep fixtures domain-general; Knowledge Graph-derived failures should appear only as visual/reference or runtime target/source proof classes.
- Verify both generation behavior and validator behavior for the new multi-parent-AC evidence fixture.

## Acceptance Criteria (Verifiable)

- AC1: Tests cover the existing generalized EPIC-006 drift gates and the new multi-parent-AC structured evidence fixture.
- AC2: Scaffolded child evidence for multi-parent coverage generates separate records for each parent AC.
- AC3: Structured evidence validation rejects comma-separated parent AC claims and accepts separate per-AC claims.
- AC4: Focused and full test suites pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- TASK-036 adds targeted regression coverage rather than a broad rewrite of the existing tests.
- The scaffold evidence template defect found while completing TASK-035 is in scope because it would cause future epic children to drift at Review even when agents followed generated artifacts.

## Validation Plan

- Run focused pytest for child scaffold and structured evidence recipe tests.
- Run the full pytest suite.
- Run workflow doctor and EPIC-006 audit.
