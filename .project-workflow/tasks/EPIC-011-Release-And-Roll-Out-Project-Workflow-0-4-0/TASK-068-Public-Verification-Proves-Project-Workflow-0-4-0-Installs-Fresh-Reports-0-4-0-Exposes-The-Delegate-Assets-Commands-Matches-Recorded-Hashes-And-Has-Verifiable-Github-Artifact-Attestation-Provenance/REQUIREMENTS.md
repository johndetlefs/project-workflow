# Requirements

## Summary

- Task: TASK-068
- Title: Public verification proves `project-workflow==0.4.0` installs fresh, reports 0.4.0, exposes the Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance
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

- AC4: owner `TASK-066`; required evidence: Fresh public install, public artifact hashes, attestation/provenance

## Goal

Independently verify that public Project Workflow 0.4.0 is the intended Delegate-capable artifact and installs successfully from public infrastructure.

## Non-Goals

- Consumer repository upgrades.

## Users & Context

Codex users need proof that the public package—not merely the source checkout or CI artifact—is usable.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Install the exact public version in a fresh disposable repository, verify version and Delegate assets/commands, compare public artifact hashes, and verify GitHub attestation/provenance.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC4 when a fresh public exact-version journey succeeds and public artifacts match recorded hashes with verifiable attestation/provenance.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Treat PyPI, GitHub Release, and attestation checks as independent public gates after publication.

## Validation Plan

- Run fresh UVX init/upgrade/version/Delegate checks, download public artifacts, compare hashes, and run GitHub attestation verification with a writable cache.
