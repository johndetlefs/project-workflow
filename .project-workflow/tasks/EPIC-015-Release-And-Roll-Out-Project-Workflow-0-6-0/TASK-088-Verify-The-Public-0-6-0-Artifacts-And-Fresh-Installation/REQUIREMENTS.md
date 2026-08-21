# Requirements

## Summary

- Task: TASK-088
- Title: Verify the public 0.6.0 artifacts and fresh installation
- Parent AC Coverage: AC4
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Prove that users can obtain the exact intended 0.6.0 release from public services and that a fresh installation contains and runs the accepted intent-integrity and sufficiency capabilities.

## Intent Spine

- OC1 — Completion capability: Public project-workflow==0.6.0 is independently installable and attributable.
- OC2 — Material capabilities: Public metadata/downloads, hashes, attestations, GitHub assets and disposable fresh installation.
- OC3 — Success journey: Fetch public records, compare identities, install exact version fresh, inspect assets and execute core commands.
- OC4 — Successful-but-wrong result: The workflow is green while PyPI is unavailable, hashes differ or the package lacks managed assets.
- OC5 — Exclusions: Do not use the local checkout or cached pre-release artifact as public proof and do not upgrade consumers yet.
- OC6 — Assumptions: TASK-087 completed trusted publication.
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

Establish the public package as the proven upgrade authority.

## Non-Goals

- Consumer mutation or claims about unpublished/local artifacts.

## Users & Context

Every downstream upgrade depends on the actual public package, not the source checkout.

## Repository Scope

- Primary repository: .
- Repositories touched: Public PyPI/GitHub services and disposable installation directories only.

## Requirements (Outcome-Focused)

- Compare public wheel/sdist and GitHub Release identities with recorded candidate artifacts.
- Verify provenance or attestation evidence.
- Install exact 0.6.0 fresh and inspect version, managed assets and representative behavior.

## Acceptance Criteria (Verifiable)

- AC1: Public metadata, hashes, attestations and fresh exact-version installation prove the expected 0.6.0 package and accepted assets.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Public exact-version installation must pass before any consumer mutation.

## Validation Plan

- Query PyPI and GitHub, download public assets, hash them, verify attestation/provenance and run a disposable exact-version installation journey.
