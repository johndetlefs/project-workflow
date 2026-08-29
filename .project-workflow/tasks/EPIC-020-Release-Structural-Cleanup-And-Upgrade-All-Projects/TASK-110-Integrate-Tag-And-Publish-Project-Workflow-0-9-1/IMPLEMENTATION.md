## User Story

As a Project Workflow maintainer, I want the certified source merged, tagged, and published through
the protected release path, so that the public version traces to reviewed code.

## Parent AC Coverage

- AC3

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

- AC3: owner `TASK-110`; required evidence: Reviewed PR/checks, main ancestry, annotated tag, trusted publish workflow, and GitHub Release evidence

## Acceptance Criteria

- [ ] AC1: The certified branch passes review/checks and merges into current main.
- [ ] AC2: Annotated v0.9.1 peels to that reviewed main lineage.
- [ ] AC3: The protected workflow publishes the coherent trusted release bundle.

## Validation

- AC1 / parent AC3: PR metadata, required checks, merge identity, and ancestry.
- AC2 / parent AC3: tag object/peeled commit and one remote tag creation.
- AC3 / parent AC3: release workflow/job conclusion, PyPI job, GitHub Release and bundle receipt.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Push and review certified branch | Push TASK-109's clean commit, create the release PR, and wait for required checks. | AC1 | Compare PR head to certified source and inspect checks. | To Do | TASK-109 | GitHub branch and PR | No | bounded-return |
| 2 | Merge and prove main lineage | Merge the passing PR, fetch canonical main, and prove candidate ancestry. | AC1 | Inspect merge commit and ancestry. | To Do | 1 | GitHub PR; local Git refs | No | bounded-return |
| 3 | Tag and publish once | Create annotated v0.9.1 on reviewed main, push it once, and monitor trusted publication. | AC2, AC3 | Inspect tag peel and all release jobs/assets. | To Do | 2 | Git tag; GitHub Actions; PyPI; GitHub Release | No | bounded-return |

## Parent AC Evidence

- AC3: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

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

- Task: TASK-110
- Title: Integrate, tag, and publish Project Workflow 0.9.1
- Created: 2026-08-29
