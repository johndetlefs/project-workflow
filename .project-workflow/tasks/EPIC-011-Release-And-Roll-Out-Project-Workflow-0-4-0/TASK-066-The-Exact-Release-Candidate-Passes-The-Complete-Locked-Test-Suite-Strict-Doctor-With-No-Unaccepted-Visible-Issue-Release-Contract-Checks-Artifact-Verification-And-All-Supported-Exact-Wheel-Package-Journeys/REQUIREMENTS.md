# Requirements

## Summary

- Task: TASK-066
- Title: The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys
- Parent AC Coverage: AC2
- Last updated: 2026-08-20

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

- The reviewed source, tag, wheel, source distribution, release assets, and public package are traceable to one 0.4.0 release identity.
- Historical completed-task evidence is not rewritten to simulate current version alignment.
- Consumer user-owned files and unrelated Git changes are preserved.
- Only canonical project authority roots are upgraded; workspace child repositories do not gain duplicate workflow state.
- No consumer project is called upgraded if it is blocked, partially mutated, or not validated.

### Invalid Substitutes

- A green source test suite without exact built/public artifact checks.
- A tag or GitHub Release without PyPI publication and fresh installation proof.
- A saved Codex project name without a canonical root manifest.
- A source-checkout upgrade, copied managed files, or an unreviewed nested workflow copy in place of public-package upgrade.
- A successful upgrade command without scoped diff and Doctor validation.

### Artifact Targets

- PyPI `project-workflow==0.4.0`.
- GitHub Release `v0.4.0` with wheel, source distribution, hashes/provenance, and release notes.
- A clean, validated Project Workflow `main` lineage.
- Per-project installed 0.4.0 managed assets for every eligible Codex project.
- Parent release/rollout receipt and acceptance audit.

### Parent AC Proof Ownership

- AC2: owner `TASK-065`; required evidence: Complete tests, strict Doctor, release contract, exact-artifact journeys

## Goal

Prove the exact 0.4.0 candidate is release-safe before merge.

## Non-Goals

- Merging, tagging, public publication, or consumer rollout.

## Users & Context

Maintainers need evidence that both source behavior and the exact built artifacts satisfy the release contract.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Run the full locked suite, strict Doctor, source and artifact contract checks, and exact-wheel journeys for every packaged host mode.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC2 when the exact candidate passes all required source, workflow, build, artifact, and package-journey gates with retained logs.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Existing EPIC-010 native-runtime evidence remains valid for the feature; this child separately proves the final release candidate and package.

## Validation Plan

- Run the locked complete suite, strict Doctor, release-contract source/build/receipt checks, and exact-wheel Codex, Claude, Cursor, and Copilot journeys.
