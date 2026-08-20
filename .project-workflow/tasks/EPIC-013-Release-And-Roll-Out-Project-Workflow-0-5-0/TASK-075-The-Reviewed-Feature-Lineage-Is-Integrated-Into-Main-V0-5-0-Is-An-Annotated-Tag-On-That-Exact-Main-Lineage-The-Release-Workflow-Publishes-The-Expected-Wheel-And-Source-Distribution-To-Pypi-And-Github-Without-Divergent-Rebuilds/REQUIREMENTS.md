# Requirements

## Summary

- Task: TASK-075
- Title: The reviewed feature lineage is integrated into `main`; `v0.5.0` is an annotated tag on that exact main lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without divergent rebuilds
- Parent AC Coverage: AC3
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

- AC3: owner `TASK-075`; required evidence: Main integration, tag ancestry, release workflow, PyPI and GitHub records

## Goal

Integrate the reviewed release candidate into main and publish the exact main commit as v0.5.0.

## Non-Goals

- Consumer-project upgrades or claims about public installability before publication completes.

## Users & Context

Trusted Publishing is tag-triggered and must build once from reviewed main history.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Push the reviewed branch, integrate it to main, create one annotated v0.5.0 tag on that main lineage, and allow the release workflow to publish the exact artifacts.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC3 when branch/main ancestry, annotated tag identity, GitHub Actions, PyPI publication, and GitHub Release all agree on one commit and artifact set.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Do not tag before main integration and successful main CI.

## Validation Plan

- Verify remote ancestry, PR/main checks, tag object, release run, and published release metadata.
