# Requirements

## Summary

- Task: TASK-069
- Title: Inventory and upgrade every eligible Codex Project Workflow installation, then retain the consolidated rollout receipt
- Parent AC Coverage: AC5, AC6, AC7
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

- AC5: owner `TASK-067`; required evidence: Codex project inventory and per-project disposition
- AC6: owner `TASK-067`; required evidence: Per-project plan/apply/diff/manifest/helper/Doctor validation
- AC7: owner `TASK-068`; required evidence: Consolidated receipt and parent acceptance audit

## Goal

Upgrade every eligible current Codex project that already has Project Workflow to the verified public 0.4.0 package, without damaging unrelated work, and retain a complete adoption receipt.

## Non-Goals

- Installing into projects without an existing root manifest, mutating non-authority nested repositories, deploying consumer products, or silently publishing consumer Git changes.

## Users & Context

The owner needs Delegate available consistently across saved Codex projects while active or ambiguous repositories remain safe.

## Repository Scope

- Primary repository: .
- Repositories touched: every eligible root discovered from the live Codex saved-project inventory; exact paths and dispositions are captured in the receipt before mutation.

## Requirements (Outcome-Focused)

- Inventory each saved project, classify root/install/Git state, plan upgrades with the public 0.4.0 package, apply only eligible plans, verify scoped diffs and Doctor, and record every success or blocker.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC5 when every saved Codex project has an exact disposition and each installed authority root is upgraded or safely blocked.
- AC2: Covers parent AC6 when every successful upgrade preserves user-owned content, changes only expected managed/schema assets, reports 0.4.0, and passes Doctor.
- AC3: Covers parent AC7 when a machine-readable receipt maps release identity, inventory, per-project before/after proof, validation, and blockers.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use `project-workflow==0.4.0` as the only upgrade authority; fail closed on dirty, detached, ambiguous, or failed-plan repositories; do not infer installation targets from project names alone.

## Validation Plan

- Capture live Codex inventory, read-only Git/manifest state, public-package upgrade plans, before/after hashes and diffs, version/helper checks, Doctor output, and a consolidated JSON receipt.
