# Epic Contract

## Summary

- Epic: EPIC-020
- Title: Release Structural Cleanup And Upgrade All Projects
- Last updated: 2026-08-29

## Sources of Truth

- Owner authority: the current Codex instruction to push the release and update all projects.
- Accepted implementation: EPIC-019 source, evidence, QA review, acceptance audit, and exact
  candidate receipts based on released 0.9.0 commit `86ca8859eb5e331db2505c2ae7230e2bc0030242`.
- Release identity: `src/project_workflow/_version.py`, `CURRENT_PACKAGE_VERSION`,
  `.project-workflow/manifest.json`, `CHANGELOG.md`, current installation guidance, CI/release
  workflows, generated runtime, and the release-source contract.
- Integrated/public identity: reviewed PR, canonical `origin/main`, annotated `v0.9.1` tag, trusted
  release workflow, PyPI, GitHub Release assets, hashes, receipts, and attestations.
- Adoption identity: the refreshed local project inventory plus each canonical root's manifest,
  branch/worktree status, reviewed upgrade plan, no-op plan, scoped diff, and Doctor result.

## Invalid Substitutes

- EPIC-019's local wheel offered as a public 0.9.1 release.
- A branch push, PR, tag, GitHub run, or PyPI page offered alone as complete release proof.
- Rebuilding or changing the candidate between reviewed source, tag, trusted publication, and
  public verification without a new immutable version.
- A project label, nested helper copy, or stale saved path offered as a canonical installation.
- A successful upgrade command without clean-root preflight, reviewed fingerprint, no-op re-plan,
  scoped diff, exact version, and Doctor evidence.
- Forced mutation of dirty, active, detached, ambiguous, nested, or unreconciled consumer state.
- Package or fixture proof offered as authenticated Claude Code runtime certification.

## Invariants

- Public commands, schemas, lifecycle semantics, asset version 8, and repository schema remain
  compatible with 0.9.0; only package version/current pins and approved maintenance content change.
- Reviewed source, merge lineage, tag, public wheel/sdist, GitHub release, and provenance identify
  one immutable 0.9.1 release.
- EPIC-019 evidence and historical workflow records are preserved; release evidence is additive.
- Publication passes before consumer mutation, and every upgrade uses public
  `project-workflow==0.9.1` rather than the source checkout.
- Only clean, unambiguous canonical authority roots are eligible; user-owned content and unrelated
  work remain untouched.
- Consumer diffs are not committed, pushed, merged, released, or deployed by this Epic.
- No project is reported upgraded when blocked, partially applied, stale, or unvalidated.
- TASK-102 remains blocked until the exact authenticated Claude canary exists.

## Artifact Targets

- One clean reviewed 0.9.1 source commit and retained candidate receipt.
- PyPI `project-workflow==0.9.1` and GitHub Release `v0.9.1` with verified wheel, sdist, hashes,
  receipt, package journeys, and attestations.
- Independent public-install and upgrade journey receipt.
- Complete local project inventory with one disposition per entry.
- Validated 0.9.1 managed assets at every eligible canonical consumer root.
- Consolidated machine-readable release/rollout receipt plus parent acceptance audit.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-109 | Coherent version scan, generated parity, source contract, package inventory, and diff hygiene |
| AC2 | TASK-109 | Locked gates, complete suite, strict Doctor, exact build/journeys, retained EPIC-019 QA, and candidate receipt |
| AC3 | TASK-110 | Reviewed PR/checks, main ancestry, annotated tag, trusted publish workflow, and GitHub Release evidence |
| AC4 | TASK-111 | Public PyPI/GitHub hashes, attestations, version/assets, and disposable exact-version journeys |
| AC5 | TASK-112 | Refreshed project inventory with canonical-root eligibility and disposition for every entry |
| AC6 | TASK-112 | Per-root fingerprint plan/apply/no-op/diff/version/helper/Doctor validation |
| AC7 | TASK-112 | Consolidated release and rollout receipt plus unresolved boundary record |
