# Requirements

## Summary

- Task: TASK-035
- Title: Prompt Skill Template And README Updates
- Parent AC Coverage: AC1, AC2, AC3, AC5, AC6, AC8, AC10, AC11, AC13, AC14, AC15, AC17
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
- AC5: owner `TASK-030, TASK-032`; required evidence: Structured evidence records and artifact identity fields.
- AC6: owner `TASK-030, TASK-032`; required evidence: Proof-recipe trigger rules and invalid-substitute rejection tests.
- AC8: owner `TASK-033`; required evidence: Amendment records and reactive-fix gate tests.
- AC10: owner `TASK-034`; required evidence: Legacy adoption commands and untrusted inferred evidence handling.
- AC11: owner `TASK-028, TASK-029, TASK-035, TASK-037`; required evidence: Prompt, skill, template, README, and CLI guidance updates.
- AC13: owner `TASK-028, TASK-032`; required evidence: Approval/evidence freshness and stale artifact identity tests.
- AC14: owner `TASK-031, TASK-033, TASK-037`; required evidence: Decomposition plan authority, amendment provenance, and child inheritance gates.
- AC15: owner `TASK-030, TASK-032`; required evidence: Visual calibration and delivered-artifact comparison recipe tests.
- AC17: owner `TASK-030, TASK-032`; required evidence: Structured claim-to-evidence ledger and contradictory prose checks.

## Goal

Agents using project-workflow prompts, Codex skills, README guidance, CLI README guidance, generated workflow blocks, or Cursor rules should naturally follow the new EPIC-006 drift gates without treating them as passive documentation or repeatedly asking the owner for approval inside an already-approved envelope.

## Non-Goals

- Do not add new workflow gate mechanics in this child; those belong to TASK-028 through TASK-034 and TASK-037.
- Do not make ordinary standalone tasks carry epic-only ceremony unless a gate or proof recipe is actually triggered.
- Do not introduce domain-specific ChatGPT/MCP/widget requirements into generic guidance.

## Users & Context

- Agents using prompt templates need active instructions at the point they plan, implement, verify, and close work.
- Owners need one explicit requirements/AC approval moment, followed by mechanical drift checks rather than repeated approval prompts.
- QA/review agents need to verify recipe-specific proof against the delivered artifact or exact target/source pair, not substitute code review, tests, builds, or related environments.
- Existing users may operate through Codex skills, prompt templates, README/CLI docs, or Cursor rules, so guidance must be aligned across those surfaces.

## Requirements (Outcome-Focused)

- Update prompt templates so task, requirements, planner, implement, QA, and epic flows route through owner approval, readiness gates, epic contracts, decomposition authority, amendments/adoption, structured evidence, and proof recipes.
- Update Codex skills so natural-language task, epic, requirements, planning, implementation, and QA requests follow the same gates without asking for generic repeated approval.
- Update README/CLI/generated guidance so the installed workflow explains the authority envelope, legacy adoption, child charter, proof recipes, invalid substitutes, and evidence freshness.
- Keep guidance bounded: ask owners for material decisions only, and tell agents to remediate concrete drift/evidence gaps directly when work remains inside the approved envelope.
- Include general visual/reference and runtime target/source examples only as proof-recipe classes, not as ChatGPT/MCP-specific requirements.

## Acceptance Criteria (Verifiable)

- AC1: Prompt templates mention one-time owner requirements/AC approval, stale approval handling, and no repeated approval for unchanged in-envelope work.
- AC2: Epic prompt/skill/README guidance route new/adopted epics through `EPIC-CONTRACT.md`, `DECOMPOSITION.md`, child charters, `AMENDMENTS.md`, adoption, proof recipes, and closeout gates.
- AC3: Task/requirements/planner/implement/QA guidance routes work through readiness checks before implementation and recipe-specific structured evidence before Review/Complete.
- AC4: Guidance explicitly rejects invalid substitutes for visual/reference fidelity and runtime target/source proof.
- AC5: Guidance updates are verified by a repo search artifact and structured evidence record.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- TASK-035 is a guidance-surface child only. It should not create new enforcement code beyond updating prompts, skills, README-style docs, generated blocks, and rules.
- Approval fatigue is a failure mode. Guidance must tell agents to ask owners only for initial approval or material changes, not for ordinary child steps inside the approved authority envelope.

## Validation Plan

- Review prompt, skill, README/CLI, generated guidance, and Cursor rule changes for the required terms and behavior.
- Run `rg` over guidance surfaces for approval, contract, decomposition, amendment/adoption, evidence, and proof-recipe terms.
- Run the repository test suite and workflow doctor after updates.
