# Requirements

## Summary

- Task: TASK-076
- Title: Public verification proves `project-workflow==0.5.0` installs fresh, reports 0.5.0, exposes the capability-aware Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance
- Parent AC Coverage: AC4
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

- AC4: owner `TASK-076`; required evidence: Fresh public install, public artifact hashes, attestation/provenance

## Goal

Prove the public Project Workflow 0.5.0 package and release assets are complete, installable, and provenance-backed.

## Non-Goals

- Treating local candidate artifacts as public proof.

## Users & Context

Publication success is not the same as public usability or artifact identity.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Install exact public 0.5.0 into a fresh disposable repository, validate version and Delegate assets/commands, compare public artifact hashes, and verify GitHub attestation/provenance.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC4 when fresh public installation and public artifact/provenance checks pass against the released identities.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Public exact-version package availability is required before any consumer upgrade.

## Validation Plan

- Use public UVX/PyPI metadata, GitHub Release assets, hashes, attestations, and a fresh disposable init/Doctor journey.
