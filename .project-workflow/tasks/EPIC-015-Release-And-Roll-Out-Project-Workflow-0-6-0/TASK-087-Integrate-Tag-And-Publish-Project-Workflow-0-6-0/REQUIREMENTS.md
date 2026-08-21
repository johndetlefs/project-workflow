# Requirements

## Summary

- Task: TASK-087
- Title: Integrate, tag and publish Project Workflow 0.6.0
- Parent AC Coverage: AC3
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Integrate the validated candidate through reviewed GitHub checks, tag the exact resulting main lineage, and let the trusted workflow publish that same 0.6.0 release without a divergent rebuild.

## Intent Spine

- OC1 — Completion capability: Version 0.6.0 is published from reviewed main lineage.
- OC2 — Material capabilities: Explicit commit, ready PR, CI, review, merge, annotated tag and trusted release workflow.
- OC3 — Success journey: Push candidate, pass checks, merge, identify main commit, tag it, and observe publication.
- OC4 — Successful-but-wrong result: A tag or release exists but does not identify the reviewed candidate lineage or artifacts diverge.
- OC5 — Exclusions: Do not bypass required checks, force-push main, rebuild different assets or start consumer upgrades.
- OC6 — Assumptions: TASK-086 has a current passing verdict and GitHub trusted publishing remains configured.
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
- Approval note / source: Owner explicitly authorized push, main integration and release.
- Approved artifact identity: Inherited from current parent requirements identity

## Goal

Publish 0.6.0 from the exact reviewed main commit.

## Non-Goals

- Public artifact acceptance or consumer upgrades, which remain later proof gates.

## Users & Context

Installers need a trusted public release whose provenance traces to reviewed main.

## Repository Scope

- Primary repository: .
- Repositories touched: Project Workflow GitHub repository and configured publishing services.

## Requirements (Outcome-Focused)

- Integrate only the validated candidate through a reviewed, green PR.
- Tag the exact merged main lineage with annotated tag v0.6.0.
- Verify the trusted workflow publishes the coherent wheel, sdist and GitHub Release assets.

## Acceptance Criteria (Verifiable)

- AC1: PR, checks, merge ancestry, annotated tag and release workflow evidence prove one coherent reviewed publication lineage.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use a ready PR and merge only after required checks pass; the owner has authorized this lifecycle.

## Validation Plan

- Inspect PR review/checks, merge commit ancestry, tag object and trusted release workflow outputs.
