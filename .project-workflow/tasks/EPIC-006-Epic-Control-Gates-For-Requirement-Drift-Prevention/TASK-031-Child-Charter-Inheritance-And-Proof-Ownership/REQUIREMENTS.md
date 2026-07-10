# Requirements

## Summary

- Task: TASK-031
- Title: Child Charter Inheritance And Proof Ownership
- Parent AC Coverage: AC3, AC4, AC12, AC14
- Last updated: 2026-07-09
- Status: Approved for implementation under EPIC-006 authority envelope.

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

- AC3: owner `TASK-031`; required evidence: Child charter generation and inheritance tests.
- AC4: owner `TASK-029, TASK-031`; required evidence: Contract proof-owner schema plus child proof-ownership gates.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.
- AC14: owner `TASK-031, TASK-033, TASK-037`; required evidence: Decomposition plan authority, amendment provenance, and child inheritance gates.

## Goal

Make epic child tasks inherit the controlling contract context they need, and make epic audit reject parent AC evidence from children that are not assigned proof owners.

## Non-Goals

- Do not implement full recipe-specific proof validation; TASK-030 owns recipe evidence.
- Do not implement amendment provenance; TASK-033 owns amendments.
- Do not force every legacy child to have a retroactive charter before adoption.

## Users & Context

- Agents need child-local constraints so they do not reinterpret long-epic requirements from memory.
- Reviewers need parent AC evidence to come from assigned proof owners, not any child that happens to mention an AC.
- Project owners need in-envelope child work to proceed without repeated approval prompts.

## Requirements (Outcome-Focused)

- `epic scaffold-child` must inject a `Child Charter` into child `REQUIREMENTS.md` and `IMPLEMENTATION.md`.
- The charter must inherit contract invariants, invalid substitutes, artifact targets, and proof-owner rows relevant to the child parent AC coverage.
- Epic audit must only count parent AC evidence from children assigned as proof owners for that AC when the contract is valid.
- Placeholder or invalid legacy contracts must not accidentally block legacy closeout through proof-owner enforcement; contract validity is handled separately.
- Tests must prove child charter injection and proof-owner rejection.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC3: scaffolded child docs contain inherited `Child Charter` sections from the epic contract.
- AC2: Covers parent AC4: epic audit rejects parent AC evidence from a child not assigned as proof owner for that parent AC.
- AC3: Covers parent AC12: tests cover charter inheritance and proof-owner rejection.
- AC4: Covers parent AC14: in-plan child rows inherit authority context without separate per-row owner approval.

## Open Questions (Answer Needed)

- None blocking.

## Decisions (Resolved)

- Child charter content is copied into both requirements and implementation docs for visibility during planning and QA.
- Proof-owner enforcement only runs when the epic contract is valid; placeholder legacy contracts remain separate warnings/gaps.

## Validation Plan

- Run `pytest tests/test_doctor.py`.
- Run the full test suite.
- Run project doctor and EPIC-006 audit.

