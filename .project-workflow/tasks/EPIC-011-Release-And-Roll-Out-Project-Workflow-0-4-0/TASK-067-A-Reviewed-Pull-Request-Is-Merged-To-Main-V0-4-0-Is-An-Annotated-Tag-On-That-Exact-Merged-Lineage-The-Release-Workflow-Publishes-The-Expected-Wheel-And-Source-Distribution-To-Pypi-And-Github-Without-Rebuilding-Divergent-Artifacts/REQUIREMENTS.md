# Requirements

## Summary

- Task: TASK-067
- Title: A reviewed pull request is merged to `main`; `v0.4.0` is an annotated tag on that exact merged lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without rebuilding divergent artifacts
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

- AC3: owner `TASK-066`; required evidence: PR checks/merge, tag ancestry, release workflow, PyPI and GitHub records

## Goal

Integrate the reviewed 0.4.0 candidate into `main` and publish its exact artifacts through the governed release workflow.

## Non-Goals

- Consumer upgrades and claims about public installability before independent verification.

## Users & Context

Maintainers and users need an immutable public release whose source, tag, artifacts, and provenance share one lineage.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Create one ready pull request, require green checks, merge it to `main`, annotate the exact main lineage with `v0.4.0`, and monitor Trusted Publishing plus GitHub Release completion.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC3 when the reviewed PR is merged, the annotated tag resolves to that lineage, and the release workflow publishes the expected wheel and source distribution to PyPI and GitHub.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use the existing protected-environment Trusted Publishing workflow; never rebuild artifacts after publication begins.

## Validation Plan

- Retain PR, check, merge, tag ancestry, GitHub Actions, PyPI metadata, GitHub Release, and asset hash evidence.
