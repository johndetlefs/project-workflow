## User Story

As the owner, I want each local adoption proven safe so that a nominal upgrade cannot hide overwritten work or partial mutation.

## Parent AC Coverage

- AC6

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

- AC6: owner `TASK-078`; required evidence: Per-project plan/apply/diff/manifest/helper/Doctor validation

## Acceptance Criteria

- [x] AC1: Covers parent AC6 when every successful upgrade has scoped diffs, version 0.5.0, managed/helper validation, and applicable Doctor success without user-owned-content loss.

## Validation

- AC1 / parent AC6: Compare Git state and manifests before/after, hash generated helpers, run Doctor, and retain per-project evidence.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| Six upgraded consumer roots | Local upgrade commits `e52bfe8`, `8cf371f`, `71402de`, `0f53668`, `d69795c`, `f91fa52` | Exact five-file managed diff, manifest 0.5.0/asset 3/schema 1, helper hash `ae1db517...`, second public plan current, Doctor results retained | Local commits only; no consumer push or deployment | `evidence/release-rollout-receipt.json`; child `EVIDENCE.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Validate consumer upgrades | Verify each upgraded root's scoped diff, manifest, generated helper, managed assets, and Doctor result. | AC1: every successful upgrade has scoped diffs, version 0.5.0, managed/helper validation, and applicable Doctor success without user-owned-content loss. | Inspect the retained before/after evidence for every successful upgrade. | Done | | Only consumer roots upgraded by TASK-077 | No | bounded-return |

## Parent AC Evidence

- AC6: Every successful upgrade changed only the five planned managed paths, reports `project 0.5.0`, has manifest asset 3/schema 1 and helper SHA-256 `ae1db517...`, and returns current/versions-current on a second public plan. Game Foundation, Toby's Games, and Strategic Advisor are Doctor-clean; pre-existing owner-owned Doctor findings remain visible in Mechanics Playground, Daily Checklist, and Client Management without being rewritten. Structured runtime/source evidence passes in `EVIDENCE.json`.

## QA & Code Review

- Verdict: Pass (2026-08-20)
- Evidence: Before/after commits, exact plan fingerprints, five-file diff lists, manifest/version/hash checks, Doctor JSON, no-op second plans, and clean post-commit worktrees.
- Findings: Existing workflow debt remains in three consumers. It is not caused by the upgrade and was not silently treated as resolved.

## Retro

- Reusable lessons: Retain both the canonical no-op post-plan and the Doctor summary; they prove different things—upgrade currency versus repository workflow health.
- Conventions or agent assets updated: None.
- Follow-up tasks: Address the recorded owner-owned Doctor debt in each affected product's own workflow, not in this release epic.

## Notes

- Task: TASK-078
- Title: Validate every successful consumer upgrade and preserve user-owned content
- Created: 2026-08-20
