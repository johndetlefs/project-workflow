## User Story

As a consumer, I want independently verified public 0.9.1 artifacts, so that upgrades use the same
authentic package that was actually released.

## Parent AC Coverage

- AC4

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

- AC4: owner `TASK-111`; required evidence: Public PyPI/GitHub hashes, attestations, version/assets, and disposable exact-version journeys

## Acceptance Criteria

- [ ] AC1: PyPI/GitHub public artifacts, hashes, metadata, tag source, and attestations agree.
- [ ] AC2: Public exact-version fresh and upgrade journeys pass across supported hosts.
- [ ] AC3: A source-bound public checkpoint authorizes rollout without claiming adoption.

## Validation

- AC1 / parent AC4: independent downloads, receipt/hash comparison, and GitHub attestation verify.
- AC2 / parent AC4: public uvx version and full exact-package journeys.
- AC3 / parent AC4: retained public receipt and coordination outcome checkpoint.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Verify public bytes and provenance | Download from PyPI and GitHub, compare identities, and verify attestations. | AC1, AC3 | Inspect public receipt, hashes, tag source, and attestation result. | To Do | TASK-110 | disposable downloads; task evidence | No | bounded-return |
| 2 | Exercise public exact package | Run version plus fresh/current/legacy/no-op/Doctor/lifecycle/helper journeys from public 0.9.1. | AC2, AC3 | Inspect disposable journey output and package source proof. | To Do | 1 | disposable repositories; task evidence | No | bounded-return |
| 3 | Record rollout checkpoint | Bind the passing public journey to EPIC-020 before consumer mutation. | AC3 | Inspect current coordination checkpoint. | To Do | 1, 2 | coordination state; task evidence | No | bounded-return |

## Parent AC Evidence

- AC4: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

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

- Task: TASK-111
- Title: Verify the public Project Workflow 0.9.1 release
- Created: 2026-08-29
