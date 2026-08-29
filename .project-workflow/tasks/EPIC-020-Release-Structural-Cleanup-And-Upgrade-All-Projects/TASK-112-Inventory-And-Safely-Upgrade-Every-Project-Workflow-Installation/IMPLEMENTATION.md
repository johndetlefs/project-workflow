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

- [ ] AC1: The complete current project and canonical-installation inventory has one disposition per entry.
- [ ] AC2: Every eligible root passes public fingerprinted upgrade, no-op, diff, preservation, version/helper, and Doctor proof.
- [ ] AC3: Every ineligible or failed root remains unchanged with an exact blocker and no consumer delivery action.
- [ ] AC4: One consolidated receipt maps release and every project result to parent AC5-AC7.

## Validation

- AC1 / parent AC5: inventory-source reconciliation, manifest-root deduplication, and eligibility evidence.
- AC2 / parent AC6: per-root public plan/fingerprint/apply/no-op/diff/version/helper/preservation/Doctor receipt.
- AC3 / parent AC5-AC6: before/after status equality and exact blocker for unchanged roots.
- AC4 / parent AC7: schema-valid consolidated release/rollout receipt and parent evidence map.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Reconcile complete project inventory | Discover current project entries and canonical manifests, deduplicate roots, and classify eligibility. | AC1, AC3 | Inspect one disposition for every entry/root. | To Do | TASK-111 | read-only project estate; task evidence | No | bounded-return |
| 2 | Upgrade eligible canonical roots | Recheck safety, plan public 0.9.1, review/apply exact fingerprints, and stop on any changed input. | AC2, AC3 | Inspect per-root command and before/after state. | To Do | 1 | eligible consumer managed assets only | No | bounded-return |
| 3 | Validate adoption separately from health | Prove no-op, managed diff, owner-content preservation, exact version/helper, and Doctor state for each applied root. | AC2, AC3 | Review scoped diffs and Doctor classification. | To Do | 2 | eligible consumer roots; task evidence | No | bounded-return |
| 4 | Consolidate release and rollout receipt | Record every disposition, public identity, validation result, and residual boundary in one machine-readable artifact. | AC4 | Validate JSON and parent AC map. | To Do | 1, 2, 3 | task evidence; parent acceptance artifacts | No | bounded-return |

## Parent AC Evidence

- AC5, AC6, AC7: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: ____
- Intent adversarial verdict: ____
- Could every AC pass while the approved user job remains undone: ____
- Intent audit state: ____
- Outcome journey evidence: ____
- Reviewer independence: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-112
- Title: Inventory and safely upgrade every Project Workflow installation
- Created: 2026-08-29
