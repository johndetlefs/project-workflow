## User Story

As a project-workflow agent/operator, I want the prompt, skill, template, README, and rule guidance to route me through the EPIC-006 drift gates, so that long-running epics stay inside approved requirements and prove the right artifact/target without creating approval fatigue.

## Parent AC Coverage

- AC1, AC2, AC3, AC5, AC6, AC8, AC10, AC11, AC13, AC14, AC15, AC17

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
- AC5: owner `TASK-030, TASK-032`; required evidence: Structured evidence records and artifact identity fields.
- AC6: owner `TASK-030, TASK-032`; required evidence: Proof-recipe trigger rules and invalid-substitute rejection tests.
- AC8: owner `TASK-033`; required evidence: Amendment records and reactive-fix gate tests.
- AC10: owner `TASK-034`; required evidence: Legacy adoption commands and untrusted inferred evidence handling.
- AC11: owner `TASK-028, TASK-029, TASK-035, TASK-037`; required evidence: Prompt, skill, template, README, and CLI guidance updates.
- AC13: owner `TASK-028, TASK-032`; required evidence: Approval/evidence freshness and stale artifact identity tests.
- AC14: owner `TASK-031, TASK-033, TASK-037`; required evidence: Decomposition plan authority, amendment provenance, and child inheritance gates.
- AC15: owner `TASK-030, TASK-032`; required evidence: Visual calibration and delivered-artifact comparison recipe tests.
- AC17: owner `TASK-030, TASK-032`; required evidence: Structured claim-to-evidence ledger and contradictory prose checks.

## Acceptance Criteria

- [x] AC1: Prompt templates mention one-time owner requirements/AC approval, stale approval handling, and no repeated approval for unchanged in-envelope work.
- [x] AC2: Epic prompt/skill/README guidance route new/adopted epics through `EPIC-CONTRACT.md`, `DECOMPOSITION.md`, child charters, `AMENDMENTS.md`, adoption, proof recipes, and closeout gates.
- [x] AC3: Task/requirements/planner/implement/QA guidance routes work through readiness checks before implementation and recipe-specific structured evidence before Review/Complete.
- [x] AC4: Guidance explicitly rejects invalid substitutes for visual/reference fidelity and runtime target/source proof.
- [x] AC5: Guidance updates are verified by a repo search artifact and structured evidence record.

## Validation

- AC1: `src/project_workflow/prompts/Task.prompt.md`, `Requirements.prompt.md`, `Planner.prompt.md`, `Implement.prompt.md`, `Epic.prompt.md`, `project-task`, `project-requirements`, and `project-planner` now describe one-time owner approval and bounded re-approval.
- AC2: `src/project_workflow/prompts/Epic.prompt.md`, `src/project_workflow/codex/skills/project-epic/SKILL.md`, `README.md`, and `.project-workflow/cli/README.md` describe contracts, decomposition authority, amendments, adoption, child charters, proof recipes, and closeout.
- AC3: `src/project_workflow/prompts/Implement.prompt.md`, `QAReview.prompt.md`, and the matching skills now require ready gates, explicit owner approval commands when approval is missing/stale, and recipe evidence before QA/complete claims.
- AC4: Guidance rejects invalid substitutes for visual/reference fidelity and runtime target/source proof.
- AC5: Evidence artifact: `evidence/guidance-surface-review.txt`; structured record: `EVIDENCE.json`.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Align prompt templates | Update task, requirements, planner, implement, QA, and epic prompts so the gates are active during agent workflow use. | AC1, AC2, AC3, AC4: prompts route through approval envelopes, readiness gates, proof recipes, and invalid-substitute checks. | Search prompt templates for approval, proof recipe, evidence, contract, decomposition, amendment, and adoption guidance. | Done |
| 2 | Align skills and rules | Update Codex skills and Cursor rules so non-prompt entry points carry the same behavior. | AC1, AC2, AC3, AC4: skills/rules describe bounded owner approval and recipe evidence. | Search skills/rules for the same gate terminology and compare against prompt behavior. | Done |
| 3 | Record guidance evidence | Add a child-local evidence artifact and structured claim record for the guidance-surface review. | AC5: evidence artifact and hash exist in `EVIDENCE.json`. | Run artifact hash check and workflow doctor/status gates. | Done |

## Parent AC Evidence

- AC1, AC11, AC13: Prompt/skill guidance records one-time owner requirements/AC approval and stale approval handling.
- AC2, AC3, AC14: Epic guidance records contracts, child charters, decomposition plan authority, and child provenance.
- AC5, AC6, AC15, AC17: Requirements/planner/implement/QA guidance records proof-recipe triggers, structured evidence, invalid substitutes, and claim-to-evidence expectations.
- AC8, AC10: Epic guidance records amendments and legacy adoption.
- Evidence artifact: `evidence/guidance-surface-review.txt`.

## QA & Code Review

- Verdict: Pass.
- Evidence: `.venv/bin/python -m pytest` passed with 67 tests. `epic status --to Testing` and `epic status --to Review` passed for TASK-035. `EVIDENCE.json` validates as JSON and contains passing child-local records for each covered parent AC, backed by `evidence/guidance-surface-review.txt`.
- Findings: None.

## Retro

- Reusable lessons: Guidance must exist where agents act, not only in long-form docs.
- Conventions or agent assets updated: Prompt templates, generated Codex/Cursor/Claude/Copilot guidance surfaces, Codex skills, Cursor rule, README/CLI guidance.
- Follow-up tasks: TASK-036 regression fixtures.

## Notes

- Task: TASK-035
- Title: Prompt Skill Template And README Updates
- Created: 2026-07-09
