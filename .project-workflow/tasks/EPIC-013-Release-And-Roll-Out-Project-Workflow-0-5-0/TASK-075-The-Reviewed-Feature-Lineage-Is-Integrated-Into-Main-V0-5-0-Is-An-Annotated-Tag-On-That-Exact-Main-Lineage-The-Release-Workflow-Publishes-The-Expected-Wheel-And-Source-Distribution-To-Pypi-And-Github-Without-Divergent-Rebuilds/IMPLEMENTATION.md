## User Story

As the Project Workflow maintainer, I want one reviewed main commit tagged and published so that public 0.5.0 has a single traceable origin.

## Parent AC Coverage

- AC3

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

- AC3: owner `TASK-075`; required evidence: Main integration, tag ancestry, release workflow, PyPI and GitHub records

## Acceptance Criteria

- [ ] AC1: Covers parent AC3 when branch/main ancestry, annotated tag identity, GitHub Actions, PyPI publication, and GitHub Release all agree on one commit and artifact set.

## Validation

- AC1 / parent AC3: Verify remote ancestry, PR/main checks, tag object, release run, and published release metadata.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/EPIC-012-delegate-executor-lifecycle | Planned validation recorded in this task | Pending release/adoption stage | Coordinator command output and retained evidence |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Integrate and publish | Push and integrate the reviewed candidate, wait for main CI, create the annotated tag, and verify the release workflow. | AC1: branch/main ancestry, annotated tag identity, GitHub Actions, PyPI publication, and GitHub Release all agree on one commit and artifact set. | Compare main, tag, workflow, PyPI, and GitHub Release identities. | To Do | | Git refs; GitHub pull request and Actions; PyPI and GitHub Release | No | bounded-return |

## Parent AC Evidence

- AC3: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-075
- Title: The reviewed feature lineage is integrated into `main`; `v0.5.0` is an annotated tag on that exact main lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without divergent rebuilds
- Created: 2026-08-20
