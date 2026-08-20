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

- [x] AC1: Covers parent AC3 when branch/main ancestry, annotated tag identity, GitHub Actions, PyPI publication, and GitHub Release all agree on one commit and artifact set.

## Validation

- AC1 / parent AC3: Verify remote ancestry, PR/main checks, tag object, release run, and published release metadata.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | PR #15 merged to `main` at `fdd4e15c621cb6805e1455d0658c60ee24b92b0c`; annotated `v0.5.0` | Main CI `32336376836` and release run `32336460480` passed; PyPI and GitHub Release hashes agree | Public release complete | `evidence/release-rollout-receipt.json`; GitHub Release `v0.5.0` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Integrate and publish | Push and integrate the reviewed candidate, wait for main CI, create the annotated tag, and verify the release workflow. | AC1: branch/main ancestry, annotated tag identity, GitHub Actions, PyPI publication, and GitHub Release all agree on one commit and artifact set. | Compare main, tag, workflow, PyPI, and GitHub Release identities. | Done | | Git refs; GitHub pull request and Actions; PyPI and GitHub Release | No | bounded-return |

## Parent AC Evidence

- AC3: PR #15 integrated the reviewed lineage at `fdd4e15c621cb6805e1455d0658c60ee24b92b0c`; annotated `v0.5.0`, successful Trusted Publishing run `32336460480`, PyPI 0.5.0, and the GitHub Release identify the same wheel (`b970773...`) and sdist (`7d0ef1...`). Structured deployed-artifact evidence passes in `EVIDENCE.json`.

## QA & Code Review

- Verdict: Pass (2026-08-20)
- Evidence: Independently compared remote main/tag ancestry, CI and release jobs, public PyPI metadata, GitHub Release metadata, downloaded hashes, and release receipt `6caaafbc...`.
- Findings: None. Publication is complete; consumer application deployment was outside scope and was not inferred.

## Retro

- Reusable lessons: Approve protected Trusted Publishing only after the exact tag run has passed build, package-journey, receipt, and attestation jobs.
- Conventions or agent assets updated: None; the release runbook already owns this sequence.
- Follow-up tasks: None.

## Notes

- Task: TASK-075
- Title: The reviewed feature lineage is integrated into `main`; `v0.5.0` is an annotated tag on that exact main lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without divergent rebuilds
- Created: 2026-08-20
