# Requirements

## Summary

- Task: TASK-112
- Title: Inventory and safely upgrade every Project Workflow installation
- Parent AC Coverage: AC5, AC6, AC7
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Inventory every current project, resolve every canonical Project Workflow authority root, and use
the public 0.9.1 package to upgrade each root that is clean and safe. Preserve every ineligible root
unchanged with a precise blocker and consolidate one complete rollout receipt.

## Intent Spine

- OC1 — Completion capability: Every current project has a disposition and every eligible
  canonical installation reports 0.9.1 with no-op-plan and Doctor evidence.
- OC2 — Material capabilities: Complete inventory, canonical-root resolution, Git/worktree/activity
  preflight, public upgrade plan/fingerprint/apply, preservation diff, no-op plan, manifest/helper,
  Doctor, blockers, and consolidated receipt.
- OC3 — Success journey: Discover all installations, classify immediate safety, plan and review
  each eligible root, apply the exact fingerprint, re-plan to no-op, inspect the diff and Doctor,
  and record both successes and unchanged blockers.
- OC4 — Successful-but-wrong result: Only familiar projects are counted, a nested or dirty root is
  upgraded, apply uses an unreviewed/stale plan, owner content changes, or installation is called
  physical-context refresh.
- OC5 — Exclusions: No installation into non-consumers, forced unsafe mutation, consumer commits,
  pushes, merges, releases, deployments, task resumption, or owner-acceptance claim.
- OC6 — Assumptions: TASK-111 proved the public exact package and each root's state is rechecked
  immediately before mutation.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
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

## Goal

Place the latest safe Project Workflow assets in every eligible current consumer while giving the
owner a complete truthful ledger for projects that cannot be changed.

## Non-Goals

- Installing new consumers, reconciling dirty application work, committing consumer diffs,
  deploying applications, or claiming loaded tasks refreshed their context.

## Users & Context

The owner has multiple local Codex projects at mixed workflow versions and worktree states. A broad
rollout must protect active work while eliminating silent version drift where safe.

## Repository Scope

- Primary repository: .
- Repositories touched: every discovered canonical Project Workflow root that passes the approved
  eligibility rule; Project Workflow source stores the consolidated receipt.

## Requirements (Outcome-Focused)

- Build a complete inventory from current project/task metadata and local canonical manifests,
  deduplicate roots, and retain a disposition for every entry.
- For each installation capture root, branch/detached state, HEAD/upstream relation, cleanliness,
  active-work evidence, installed version/asset/schema, and selected agent mode.
- Upgrade only clean, unambiguous canonical roots using public 0.9.1 plan JSON and its exact
  fingerprint; fail closed on changed input or plan blockers.
- Verify no-op plan, expected managed diff, preserved owner-owned bytes, 0.9.1 manifest/helper, and
  Doctor separately; do not attribute pre-existing Doctor findings to the upgrade.
- Retain every successful result and blocker in one machine-readable release/rollout receipt.

## Acceptance Criteria (Verifiable)

- AC1: Every current project inventory entry and every discovered canonical manifest root has one
  deduplicated disposition with exact eligibility evidence. Covers parent AC5.
- AC2: Every eligible root uses public 0.9.1 plan/fingerprint/apply and passes no-op, scoped-diff,
  version/helper, owner-content preservation, and applicable Doctor checks. Covers parent AC6.
- AC3: Every dirty, active, detached, ambiguous, nested, stale-plan, or failed root remains
  unchanged with its exact blocker; no consumer diff is committed or pushed. Covers parent AC5 and
  AC6.
- AC4: One consolidated receipt maps public release identity and all inventory/upgrade evidence to
  parent AC5-AC7 and remaining boundaries. Covers parent AC7.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- "All" requires complete inventory coverage; it does not authorize destructive conflict
  resolution or mutation of roots that fail safety checks.
- Repository upgrade changes managed assets and schema only; existing physical tasks must load the
  new contract explicitly before claiming refreshed instructions.

## Validation Plan

- Compare inventory sources and deduplicated roots; retain per-root preflight, public plan,
  fingerprint apply, no-op, diff, version/helper, preservation and Doctor receipts; validate the
  consolidated JSON and parent acceptance mapping.
