# Requirements

## Summary

- Task: TASK-079
- Title: Retain the consolidated release and rollout receipt
- Parent AC Coverage: AC7
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

- The reviewed source, tag, wheel, source distribution, release assets, and public package are traceable to one 0.5.0 release identity.
- Historical completed-task evidence is not rewritten to simulate current version alignment.
- Consumer user-owned files and unrelated Git changes are preserved.
- Only canonical project authority roots are upgraded; workspace children do not gain duplicate workflow state.
- No consumer project is called upgraded if it is blocked, partially mutated, or not validated.

### Invalid Substitutes

- A green source test suite without exact built/public artifact checks.
- A tag or GitHub Release without PyPI publication and fresh installation proof.
- A saved Codex project name without a canonical root manifest.
- A source-checkout upgrade, copied managed files, or an unreviewed nested workflow copy in place of public-package upgrade.
- A successful upgrade command without scoped diff and Doctor validation.

### Artifact Targets

- PyPI `project-workflow==0.5.0`.
- GitHub Release `v0.5.0` with wheel, source distribution, hashes/provenance, and release notes.
- A clean, validated Project Workflow `main` lineage.
- Per-project installed 0.5.0 managed assets for every eligible Codex project.
- Parent release/rollout receipt and acceptance audit.

### Parent AC Proof Ownership

- AC7: owner `TASK-077`; required evidence: Consolidated receipt and parent acceptance audit

## Goal

Retain one complete release-and-rollout receipt that maps every EPIC-013 acceptance criterion to durable evidence.

## Non-Goals

- Replacing external release/adoption proof with prose.

## Users & Context

The feature, release, public package, and consumer adoption are separate evidence layers.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Produce a sanitized machine-readable receipt containing source/tag/artifact identities, public URLs, inventory, per-project results, blockers, and proof mappings.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC7 when the receipt is complete, identity-bound, sanitized, and accepted by the parent audit.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Exact blockers remain visible; the receipt must not convert retained projects into successful upgrades.

## Validation Plan

- Validate receipt schema/content, evidence paths, AC mapping, and parent acceptance audit.
