# Requirements

## Summary

- Task: TASK-085
- Title: Prepare the coherent Project Workflow 0.6.0 release identity
- Parent AC Coverage: AC1
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Prepare one internally coherent Project Workflow 0.6.0 candidate so every current release authority and packaged managed asset describes the same release without rewriting historical evidence.

## Intent Spine

- OC1 — Completion capability: The repository can build one unambiguous 0.6.0 candidate.
- OC2 — Material capabilities: Align version authorities, managed mirrors, changelog, README, CI and release workflow.
- OC3 — Success journey: Inspect current authorities, update only current-use references, prove parity, and retain the candidate diff.
- OC4 — Successful-but-wrong result: Tests pass while one current authority still reports 0.5.1 or generated assets diverge.
- OC5 — Exclusions: Do not publish, merge, tag, rewrite completed evidence or change accepted feature behavior.
- OC6 — Assumptions: 0.6.0 remains the approved backward-compatible feature release identity.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
- Requirements reviewed by owner: Inherited from parent epic envelope when unchanged
- Acceptance criteria reviewed by owner: Inherited from parent epic envelope when unchanged
- Approved for decomposition: Not applicable
- Approved for implementation: Yes, inherited from parent epic envelope
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-21
- Approval note / source: EPIC-015 owner-approved release and rollout envelope.
- Approved artifact identity: Inherited from current parent requirements identity

## Goal

Make the final source tree a coherent 0.6.0 release candidate.

## Non-Goals

- Integration, publication, public verification or consumer upgrades.
- Feature changes outside the already accepted EPIC-014, FIX-007 and FIX-008 work.

## Users & Context

The release coordinator needs a single candidate identity before expensive validation and publication.

## Repository Scope

- Primary repository: .
- Repositories touched: Project Workflow source repository only.

## Requirements (Outcome-Focused)

- Align every current version authority and release instruction on 0.6.0.
- Preserve byte-identical CLI mirrors and matching managed skills/prompts.
- Add an accurate 0.6.0 changelog entry without altering historical release records.

## Acceptance Criteria (Verifiable)

- AC1: Version scans, mirror hashes, managed-asset comparisons and release-file inspection prove one coherent 0.6.0 identity with no historical evidence rewrite.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use semantic version 0.6.0 and update current-use release authorities only.

## Validation Plan

- Run version-reference scans, CLI mirror comparisons, managed asset parity checks and inspect the release-identity diff.
