# Epic Contract

## Summary

- Epic: EPIC-015
- Title: Release And Roll Out Project Workflow 0.6.0
- Last updated: 2026-08-21

## Sources of Truth

- EPIC-014, FIX-007 and FIX-008 accepted local implementation and evidence.
- `src/project_workflow/_version.py`, `CHANGELOG.md`, `README.md`, the three required CLI mirrors,
  package/host assets, `.project-workflow/manifest.json`, CI and release workflows.
- The reviewed PR, integrated commit on current `origin/main`, annotated `v0.6.0` tag, PyPI package,
  GitHub Release assets and GitHub attestations for public identity.
- The live Codex saved-project inventory and each local root's own manifest, branch and worktree
  state for rollout scope and eligibility.

## Invalid Substitutes

- A green source suite without final built and public artifact checks.
- A local branch, tag or GitHub Release without reviewed main ancestry, PyPI publication and fresh
  public installation proof.
- A saved project label, nested copy or source-checkout file copy in place of a canonical root
  manifest and public-package upgrade.
- A successful upgrade command without preflight cleanliness, scoped diff, no-op re-plan and Doctor.
- Installing into non-consumers or overwriting dirty work to increase adoption counts.

## Invariants

- Reviewed source, main commit, tag, wheel, sdist, GitHub release bundle and public package trace to
  one 0.6.0 identity.
- Historical completed evidence is preserved; current release evidence is additive.
- Consumer user-owned files and unrelated Git changes remain untouched.
- Only clean, unambiguous canonical roots are eligible for mutation; workspace children do not gain
  duplicate workflow authority.
- No project is reported upgraded if it is blocked, partially mutated or not validated.
- Publication precedes consumer mutation, and the public exact-version package is used for adoption.

## Artifact Targets

- PyPI `project-workflow==0.6.0`.
- GitHub Release `v0.6.0` with wheel, sdist, receipt, hashes, package journeys and provenance.
- Reviewed and validated Project Workflow `main` lineage.
- Validated installed 0.6.0 managed assets in every eligible canonical saved-project root.
- A retained parent release/rollout receipt and acceptance audit.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-085 | Version scan, mirror parity, changelog/docs/workflow and clean release-identity diff |
| AC2 | TASK-086 | Complete tests, strict Doctor, release contract, distributions, four-host exact-wheel journeys and independent QA |
| AC3 | TASK-087 | Reviewed PR/checks, main merge ancestry, annotated tag and release workflow evidence |
| AC4 | TASK-088 | Public package/release hashes, provenance and fresh exact-version installation |
| AC5 | TASK-089 | Refreshed saved-project inventory with per-entry disposition |
| AC6 | TASK-089 | Per-root plan/apply/no-op/diff/manifest/helper/Doctor validation |
| AC7 | TASK-089 | Consolidated machine-readable release and rollout receipt plus parent acceptance audit |
