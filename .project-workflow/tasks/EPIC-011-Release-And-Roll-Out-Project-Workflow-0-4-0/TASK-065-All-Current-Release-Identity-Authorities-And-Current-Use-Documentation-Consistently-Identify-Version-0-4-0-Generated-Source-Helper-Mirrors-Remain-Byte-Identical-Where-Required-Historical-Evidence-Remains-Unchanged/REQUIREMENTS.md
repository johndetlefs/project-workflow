# Requirements

## Summary

- Task: TASK-065
- Title: All current release identity authorities and current-use documentation consistently identify version 0.4.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged
- Parent AC Coverage: AC1
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

- AC1: owner `TASK-065`; required evidence: Version scan, mirror parity, changelog/docs/workflow diff

## Goal

Prepare one internally consistent Project Workflow 0.4.0 release identity without altering historical evidence.

## Non-Goals

- Publishing, tagging, or consumer upgrades.

## Users & Context

Maintainers and release automation need one unambiguous candidate version before validation and publication.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Update every current release authority and current-use pin to 0.4.0, add accurate Delegate release notes, and preserve required mirror parity.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC1 when source version, managed manifest, CLI mirrors, CI/release workflow, changelog, and current-use docs agree on 0.4.0 and historical evidence is unchanged.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use semantic version 0.4.0 because Delegate is backward-compatible new functionality.

## Validation Plan

- Scan current version authorities, compare required mirror hashes, inspect the scoped diff, and run source release-contract checks.
