# Requirements

## Summary

- Task: TASK-078
- Title: Validate every successful consumer upgrade and preserve user-owned content
- Parent AC Coverage: AC6
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

- AC6: owner `TASK-077`; required evidence: Per-project plan/apply/diff/manifest/helper/Doctor validation

## Goal

Validate every successful consumer upgrade and prove that user-owned content and unrelated work were preserved.

## Non-Goals

- Bypassing clean-worktree protections or publishing consumer repositories.

## Users & Context

A successful command alone cannot prove a safe, scoped consumer upgrade.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- For each upgraded root, inspect the exact before/after diff, manifest, helper version/parity, managed files, and Doctor result.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC6 when every successful upgrade has scoped diffs, version 0.5.0, managed/helper validation, and applicable Doctor success without user-owned-content loss.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Consumer remote pushes are outside the local-adoption authority unless separately authorized.

## Validation Plan

- Compare Git state and manifests before/after, hash generated helpers, run Doctor, and retain per-project evidence.
