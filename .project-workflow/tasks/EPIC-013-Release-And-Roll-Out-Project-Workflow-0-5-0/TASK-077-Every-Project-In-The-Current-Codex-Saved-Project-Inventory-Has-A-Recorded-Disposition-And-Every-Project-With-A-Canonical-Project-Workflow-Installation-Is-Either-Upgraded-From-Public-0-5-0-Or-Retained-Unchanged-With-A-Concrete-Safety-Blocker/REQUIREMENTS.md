# Requirements

## Summary

- Task: TASK-077
- Title: Every project in the current Codex saved-project inventory has a recorded disposition, and every project with a canonical Project Workflow installation is either upgraded from public 0.5.0 or retained unchanged with a concrete safety blocker
- Parent AC Coverage: AC5
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

- AC5: owner `TASK-077`; required evidence: Codex project inventory and per-project disposition

## Goal

Inventory every current Codex project and record an exact upgrade, already-current, absent, or blocked disposition.

## Non-Goals

- Installing Project Workflow where no canonical installation exists.

## Users & Context

Saved Codex projects are not automatically Project Workflow authority roots and may contain active owner work.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Discover current Codex project roots, deduplicate repositories/worktrees, inspect manifests and Git safety, and upgrade every eligible canonical installation from public 0.5.0.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC5 when every inventoried project has an evidence-backed disposition and every eligible installed root is upgraded.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Dirty, detached, ambiguous, nested, or failed-plan roots remain unchanged with an exact blocker.

## Validation Plan

- Record inventory roots, manifests, Git state, upgrade plans/results, and post-upgrade version/Doctor status.
