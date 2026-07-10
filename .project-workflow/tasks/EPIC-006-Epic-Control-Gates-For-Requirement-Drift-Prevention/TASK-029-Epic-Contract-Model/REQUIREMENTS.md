# Requirements

## Summary

- Task: TASK-029
- Title: Epic Contract Model
- Parent AC Coverage: AC2, AC4, AC11, AC12
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

## Goal

Add a small epic contract artifact and gate so new/adopted epics must declare their sources of truth, invalid substitutes, invariants, artifact targets, and parent AC proof owners before decomposition or child execution.

## Non-Goals

- Do not implement full proof-recipe validation; TASK-030 owns structured proof recipes.
- Do not implement full child charter inheritance; TASK-031 owns child charter propagation.
- Do not force legacy unadopted epics to fail immediately; TASK-034 owns adoption.

## Users & Context

- Project owners need a compact place to state what controls an epic before child tasks start.
- Agents need source-of-truth and invalid-substitute constraints available at lifecycle gates.
- Reviewers need doctor to distinguish missing contract authority in new/adopted work from legacy warnings.

## Requirements (Outcome-Focused)

- `epic init` must create `EPIC-CONTRACT.md`.
- The contract must include sections for sources of truth, invalid substitutes, invariants, artifact targets, and parent AC proof ownership.
- New/adopted epics must replace placeholder contract content before `epic ready`, `epic decompose`, `epic approve`, `epic scaffold-child`, child status movement, or global movement into `Ready`/`In Progress`.
- Contract proof-owner rows must cover every parent AC declared in epic requirements.
- Doctor must fail approved/adopted epics with missing or placeholder contracts and warn for legacy unapproved epics.
- Guidance must explain the contract as an authority artifact, not passive documentation.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC2: new epics get `EPIC-CONTRACT.md`, and decomposition/child execution commands reject missing or placeholder contracts.
- AC2: Covers parent AC4: the contract schema records parent AC proof ownership for every parent AC.
- AC3: Covers parent AC11: README, CLI README, generated host guidance, and `project-epic` skill explain the contract gate.
- AC4: Covers parent AC12: regression tests prove contract creation, contract-required decomposition blocking, and doctor failure for approved epics missing contracts.

## Open Questions (Answer Needed)

- None blocking.

## Decisions (Resolved)

- The contract remains Markdown with a structured proof-owner table.
- Legacy unapproved epics warn rather than fail until the adoption task lands.
- Full proof-owner enforcement at audit/closeout remains shared with TASK-031 because it depends on child charter/proof ownership behavior.

## Validation Plan

- Run `pytest tests/test_doctor.py`.
- Run the full test suite.
- Run project doctor after EPIC-006 gets a valid contract.

