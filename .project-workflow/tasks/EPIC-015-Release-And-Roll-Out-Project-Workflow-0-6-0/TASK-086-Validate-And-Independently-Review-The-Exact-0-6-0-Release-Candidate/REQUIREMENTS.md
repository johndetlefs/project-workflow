# Requirements

## Summary

- Task: TASK-086
- Title: Validate and independently review the exact 0.6.0 release candidate
- Parent AC Coverage: AC2
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Prove that the exact 0.6.0 source candidate and the wheel and sdist built from it satisfy the complete release contract before anything is integrated or published.

## Intent Spine

- OC1 — Completion capability: The exact candidate is safe to submit for reviewed integration.
- OC2 — Material capabilities: Full suite, strict Doctor, release contract, deterministic build inspection, four-host journeys, behavioral fixtures and independent QA.
- OC3 — Success journey: Freeze the candidate, build once, validate source and artifacts, then obtain an independent adversarial verdict.
- OC4 — Successful-but-wrong result: Source tests pass while packaged assets, host journeys or intent behavior fail.
- OC5 — Exclusions: Do not merge, tag, publish, or silently repair findings outside the accepted envelope.
- OC6 — Assumptions: TASK-085 supplies the final candidate identity.
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

Produce an evidence-backed go or no-go verdict for the exact final 0.6.0 candidate.

## Non-Goals

- GitHub integration, trusted publication, public-package verification or consumer rollout.

## Users & Context

The owner needs release confidence tied to the built distribution, not a lower-level proxy.

## Repository Scope

- Primary repository: .
- Repositories touched: Project Workflow source repository and disposable validation environments only.

## Requirements (Outcome-Focused)

- Validate the complete source tree and exact built distributions.
- Exercise all declared host installation journeys and current intent/continuation fixtures.
- Obtain independent adversarial QA against the approved parent intent.

## Acceptance Criteria (Verifiable)

- AC1: The exact candidate passes every parent AC2 validation layer and independent QA reports no blocking finding.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- One final candidate validation pass is sufficient unless a material failure requires a correction.

## Validation Plan

- Run the locked suite, strict Doctor, release contract, build and distribution inspection, four-host exact-wheel journeys, behavioral fixtures and independent QA.
