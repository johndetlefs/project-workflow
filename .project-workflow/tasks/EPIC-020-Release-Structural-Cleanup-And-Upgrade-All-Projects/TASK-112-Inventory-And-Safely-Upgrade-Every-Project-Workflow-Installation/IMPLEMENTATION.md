## User Story

As the owner, I want every current Project Workflow consumer safely on 0.9.1 or explicitly blocked,
so that version drift is visible without damaging active work.

## Parent AC Coverage

- AC5, AC6, AC7

## Child Charter

### Inherited Invariants

- Public commands, schemas, lifecycle semantics, asset version 8, and repository schema remain compatible with 0.9.0; only package version/current pins and approved maintenance content change.
- Reviewed source, merge lineage, tag, public wheel/sdist, GitHub release, and provenance identify one immutable 0.9.1 release.
- EPIC-019 evidence and historical workflow records are preserved; release evidence is additive.
- Publication passes before consumer mutation, and every upgrade uses public `project-workflow==0.9.1` rather than the source checkout.
- Only clean, unambiguous canonical authority roots are eligible; user-owned content and unrelated work remain untouched.
- Consumer diffs are not committed, pushed, merged, released, or deployed by this Epic.
- No project is reported upgraded when blocked, partially applied, stale, or unvalidated.
- TASK-102 remains blocked until the exact authenticated Claude canary exists.

### Invalid Substitutes

- EPIC-019's local wheel offered as a public 0.9.1 release.
- A branch push, PR, tag, GitHub run, or PyPI page offered alone as complete release proof.
- Rebuilding or changing the candidate between reviewed source, tag, trusted publication, and public verification without a new immutable version.
- A project label, nested helper copy, or stale saved path offered as a canonical installation.
- A successful upgrade command without clean-root preflight, reviewed fingerprint, no-op re-plan, scoped diff, exact version, and Doctor evidence.
- Forced mutation of dirty, active, detached, ambiguous, nested, or unreconciled consumer state.
- Package or fixture proof offered as authenticated Claude Code runtime certification.

### Artifact Targets

- One clean reviewed 0.9.1 source commit and retained candidate receipt.
- PyPI `project-workflow==0.9.1` and GitHub Release `v0.9.1` with verified wheel, sdist, hashes, receipt, package journeys, and attestations.
- Independent public-install and upgrade journey receipt.
- Complete local project inventory with one disposition per entry.
- Validated 0.9.1 managed assets at every eligible canonical consumer root.
- Consolidated machine-readable release/rollout receipt plus parent acceptance audit.

### Parent AC Proof Ownership

- AC5: owner `TASK-112`; required evidence: Refreshed project inventory with canonical-root eligibility and disposition for every entry
- AC6: owner `TASK-112`; required evidence: Per-root fingerprint plan/apply/no-op/diff/version/helper/Doctor validation
- AC7: owner `TASK-112`; required evidence: Consolidated release and rollout receipt plus unresolved boundary record

## Acceptance Criteria

- [x] AC1: The complete current project and canonical-installation inventory has one disposition per entry.
- [x] AC2: Every eligible root passes public fingerprinted upgrade, no-op, diff, preservation, version/helper, and Doctor proof.
- [x] AC3: Every ineligible or failed root remains unchanged with an exact blocker and no consumer delivery action.
- [x] AC4: One consolidated receipt maps release and every project result to parent AC5-AC7.

## Validation

- AC1 / parent AC5: inventory-source reconciliation, manifest-root deduplication, and eligibility evidence.
- AC2 / parent AC6: per-root public plan/fingerprint/apply/no-op/diff/version/helper/preservation/Doctor receipt.
- AC3 / parent AC5-AC6: before/after status equality and exact blocker for unchanged roots.
- AC4 / parent AC7: schema-valid consolidated release/rollout receipt and parent evidence map.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | Release merge `cdd98f4`; rollout evidence branch `codex/structural-coherence-cleanup` | 20 project entries and 15 manifest roots reconciled; one clean root current on 0.9.1; 14 dirty/ambiguous roots rechecked unchanged | Project Workflow clean `main` fast-forwarded to the released merge; no consumer commit, push, merge, release, or deployment | `evidence/rollout/rollout-receipt.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Reconcile complete project inventory | Discover current project entries and canonical manifests, deduplicate roots, and classify eligibility. | AC1, AC3 | Inspect one disposition for every entry/root. | Done | TASK-111 | read-only project estate; task evidence | No | bounded-return |
| 2 | Upgrade eligible canonical roots | Recheck safety, plan public 0.9.1, review/apply exact fingerprints, and stop on any changed input. | AC2, AC3 | Inspect per-root command and before/after state. | Done | 1 | eligible consumer managed assets only | No | bounded-return |
| 3 | Validate adoption separately from health | Prove no-op, managed diff, owner-content preservation, exact version/helper, and Doctor state for each applied root. | AC2, AC3 | Review scoped diffs and Doctor classification. | Done | 2 | eligible consumer roots; task evidence | No | bounded-return |
| 4 | Consolidate release and rollout receipt | Record every disposition, public identity, validation result, and residual boundary in one machine-readable artifact. | AC4 | Validate JSON and parent AC map. | Done | 1, 2, 3 | task evidence; parent acceptance artifacts | No | bounded-return |

## Parent AC Evidence

- AC5: Codex project metadata contained 20 entries: 18 local and two cloud-only. The local estate
  contained 12 saved installations and six saved non-consumers. A filesystem scan found 15 unique
  manifest roots, including three additional roots not registered as saved projects. Every entry
  and root has a disposition in the rollout receipt.
- AC6: Project Workflow was the only clean, unambiguous root. Its clean `main` fast-forwarded from
  `86ca885` to released merge `cdd98f4`; the public 0.9.1 plan fingerprint
  `sha256:c58551f1e7b5f20803d47eb3593896b6e28a309b6d0839a65c8ab70afe6e6c5b`
  reported `versions-current` with zero steps, helper version 0.9.1, strict Doctor passed, and the
  worktree remained clean. The other 14 roots remained byte-for-byte unchanged because every one
  was dirty; several also had stale, active-branch, duplicate-authority, or unregistered-root
  blockers.
- AC7: `evidence/rollout/rollout-receipt.json` binds release identity, all 20 projects, all 15
  manifests, the one validated-current result, 14 exact blockers, unchanged status digests, and
  zero consumer delivery actions.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: The normal owner journey starts with every Codex project plus every
  local manifest root, applies the verified public version only to a clean canonical root, and ends
  with one exact disposition for every entry. It does not turn unsafe non-mutation into a false
  upgrade claim.
- Reviewer independence: A distinct adversarial review reconciled Codex metadata against a fresh
  filesystem manifest scan and repeated every blocked status digest after the sole eligible action.
  System policy prohibited a separate subagent.
- Evidence: `evidence/rollout/rollout-receipt.json`; live Codex project inventory; manifest scan;
  per-root Git/manifest/agent/upstream/worktree/status checks; public 0.9.1 plan; helper; strict
  Doctor.
- Findings: No implementation defect. Fourteen installations remain on 0.9.0 by design because
  their current repository state fails the approved safe-mutation precondition. That residual is a
  visible operational boundary, not a hidden success claim.

## Retro

- Reusable lessons: A rollout cannot remain continuously upgradable when prior managed-asset diffs
  are left uncommitted in canonical roots; each repository needs its existing workflow change
  reconciled before the next release can apply safely.
- Conventions or agent assets updated: None in consumers; the release itself supplies the new
  managed assets.
- Follow-up tasks: Reconcile the 14 blocked repositories under their own authority, then rerun the
  public fingerprinted 0.9.1 upgrade in each now-clean canonical root.

## Notes

- Task: TASK-112
- Title: Inventory and safely upgrade every Project Workflow installation
- Created: 2026-08-29
