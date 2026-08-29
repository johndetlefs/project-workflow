# Requirements

## Summary

- Task: TASK-110
- Title: Integrate, tag, and publish Project Workflow 0.9.1
- Parent AC Coverage: AC3
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Integrate the exact TASK-109 candidate through a reviewed passing PR, tag its resulting `main`
lineage as v0.9.1, and publish the trusted release bundle without changing or rebuilding its public
identity outside the protected workflow.

## Intent Spine

- OC1 — Completion capability: Project Workflow 0.9.1 exists on reviewed `main`, PyPI, and GitHub
  Release with one traceable immutable tag and trusted workflow.
- OC2 — Material capabilities: Branch push, reviewed PR/checks, merge ancestry, annotated tag,
  protected release workflow, PyPI publication, GitHub Release, and retained identities.
- OC3 — Success journey: Push the certified commit, merge only after required checks pass, fetch and
  verify `main`, tag that lineage, push the new tag once, and observe the trusted workflow publish.
- OC4 — Successful-but-wrong result: A tag is created before reviewed merge, a different commit is
  tagged, required checks are skipped, or public publication is inferred from a successful build.
- OC5 — Exclusions: No source repair after candidate freeze, no tag movement/reuse, no consumer
  upgrade, no public-verification substitution, and no owner-acceptance claim.
- OC6 — Assumptions: GitHub branch/release protections and PyPI trusted publishing remain available.
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

- AC3: owner `TASK-110`; required evidence: Reviewed PR/checks, main ancestry, annotated tag, trusted publish workflow, and GitHub Release evidence

## Goal

Make the exact structural maintenance candidate publicly available through the project's normal
reviewed and trusted release path.

## Non-Goals

- Candidate source changes, public artifact verification, consumer upgrades, and deployments.

## Users & Context

Maintainers need the frozen TASK-109 candidate integrated and published without bypassing review or
confusing workflow completion with public availability.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Push the certified branch, create a PR, and require current CI to pass before merge.
- Fetch and prove the merge commit contains the certified source before creating annotated v0.9.1.
- Push the tag once and monitor the protected build, attest, PyPI, and GitHub publication jobs.
- Retain PR, check, merge, tag, workflow, and release identities with exact failure state if blocked.

## Acceptance Criteria (Verifiable)

- AC1: The certified source is reviewed in one PR, all required checks pass, and the merge commit on
  current `origin/main` contains the candidate. Covers parent AC3.
- AC2: Annotated v0.9.1 peels to that reviewed `main` lineage and is pushed exactly once without
  movement or reuse. Covers parent AC3.
- AC3: The trusted workflow completes build, attest, PyPI publish, and GitHub Release jobs for that
  tag, retaining one coherent release bundle. Covers parent AC3.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Publication evidence is recorded here; independent retrieval remains TASK-111.

## Validation Plan

- Inspect branch/PR/head/check/merge ancestry, annotated tag peel, workflow jobs, PyPI publication
  job, GitHub Release creation, and retained release bundle identities.
