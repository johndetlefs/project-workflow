## User Story

As the Project Workflow maintainer, I want one consistent 0.5.0 release candidate so that the accepted Delegate lifecycle can be published without version or artifact ambiguity.

## Parent AC Coverage

- AC1

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

- AC1: owner `TASK-073`; required evidence: Version scan, mirror parity, changelog/docs/workflow diff

## Acceptance Criteria

- [x] AC1: Covers parent AC1 when source version, managed manifest, CLI mirrors, CI/release workflow, changelog, and current-use docs agree on 0.5.0 and historical evidence is unchanged.

## Validation

- AC1 / parent AC1: Scan current version authorities, compare required mirror hashes, inspect the scoped diff, and run source release-contract checks.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/EPIC-012-delegate-executor-lifecycle` | `check-source --version 0.5.0 --tag v0.5.0`, three-way mirror hash, current-scope version scan, `git diff --check` | Release candidate identity prepared; not yet published | Coordinator command output on 2026-08-20 |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Prepare 0.5.0 identity | Update canonical version authorities, release workflows, changelog, and current-use documentation while preserving history. | AC1 / parent AC1: Covers parent AC1 when source version, managed manifest, CLI mirrors, CI/release workflow, changelog, and current-use docs agree on 0.5.0 and historical evidence is unchanged. | Run the version scan and source contract check. | Done | | src/project_workflow/_version.py; src/project_workflow/cli.py; src/project_workflow/templates/workflow.py; .project-workflow/cli/workflow.py; .project-workflow/manifest.json; CHANGELOG.md; README.md; AGENTS.md; .github/workflows | No | bounded-return |

## Parent AC Evidence

- AC1: Source version, local manifest, three byte-identical CLI mirrors, CI/release workflow, runbook, current-use docs, tests, and changelog agree on 0.5.0; historical completed-task evidence was not rewritten.

## QA & Code Review

- Verdict: Pass
- Evidence: Source contract reported `0.5.0`; public availability confirmed the version is unused; all three helpers have SHA-256 `ae1db5179b621f17d6ef3a6dbb349e3bdd965e697fc9f9461f1e388cb5b7df63`; current-scope scan and `git diff --check` passed.
- Findings: None.

## Retro

- Reusable lessons: Rebuild exact artifacts after version identity changes; a pre-bump green wheel is not release evidence.
- Conventions or agent assets updated: Release pins and immutable runbook examples now identify 0.5.0.
- Follow-up tasks: None.

## Notes

- Task: TASK-073
- Title: All current release identity authorities and current-use documentation consistently identify version 0.5.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged
- Created: 2026-08-20
