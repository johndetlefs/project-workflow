# Epic Contract

## Summary

- Epic: EPIC-011
- Title: Release And Roll Out Project Workflow 0.4.0
- Last updated: 2026-08-20

## Sources of Truth

- EPIC-010 accepted implementation and evidence for Delegate behavior.
- `src/project_workflow/_version.py`, the three required CLI mirrors, `.project-workflow/manifest.json`, `CHANGELOG.md`, and release workflows for release identity.
- The reviewed merge commit on `origin/main`, annotated `v0.4.0` tag, PyPI project metadata, GitHub Release assets, and GitHub attestations for public artifact identity.
- The live Codex saved-project inventory and each root's own `.project-workflow/manifest.json` for rollout scope.

## Invalid Substitutes

- A green source test suite without exact built/public artifact checks.
- A tag or GitHub Release without PyPI publication and fresh installation proof.
- A saved Codex project name without a canonical root manifest.
- A source-checkout upgrade, copied managed files, or an unreviewed nested workflow copy in place of public-package upgrade.
- A successful upgrade command without scoped diff and Doctor validation.

## Invariants

- The reviewed source, tag, wheel, source distribution, release assets, and public package are traceable to one 0.4.0 release identity.
- Historical completed-task evidence is not rewritten to simulate current version alignment.
- Consumer user-owned files and unrelated Git changes are preserved.
- Only canonical project authority roots are upgraded; workspace child repositories do not gain duplicate workflow state.
- No consumer project is called upgraded if it is blocked, partially mutated, or not validated.

## Artifact Targets

- PyPI `project-workflow==0.4.0`.
- GitHub Release `v0.4.0` with wheel, source distribution, hashes/provenance, and release notes.
- A clean, validated Project Workflow `main` lineage.
- Per-project installed 0.4.0 managed assets for every eligible Codex project.
- Parent release/rollout receipt and acceptance audit.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-065 | Version scan, mirror parity, changelog/docs/workflow diff |
| AC2 | TASK-066 | Complete tests, strict Doctor, release contract, exact-artifact journeys |
| AC3 | TASK-067 | PR checks/merge, tag ancestry, release workflow, PyPI and GitHub records |
| AC4 | TASK-068 | Fresh public install, public artifact hashes, attestation/provenance |
| AC5 | TASK-069 | Codex project inventory and per-project disposition |
| AC6 | TASK-069 | Per-project plan/apply/diff/manifest/helper/Doctor validation |
| AC7 | TASK-069 | Consolidated receipt and parent acceptance audit |
