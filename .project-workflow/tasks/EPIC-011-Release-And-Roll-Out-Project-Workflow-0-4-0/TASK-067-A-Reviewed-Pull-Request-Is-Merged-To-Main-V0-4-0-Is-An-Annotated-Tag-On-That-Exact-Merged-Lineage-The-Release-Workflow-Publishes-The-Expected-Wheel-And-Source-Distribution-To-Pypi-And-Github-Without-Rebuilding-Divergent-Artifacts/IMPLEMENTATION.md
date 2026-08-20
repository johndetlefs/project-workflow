## User Story

As the Project Workflow owner, I want the reviewed candidate merged and published from one immutable lineage so that 0.4.0 is trustworthy and reproducible.

## Parent AC Coverage

- AC3

## Child Charter

### Inherited Invariants

- The reviewed source, tag, wheel, source distribution, release assets, and public package are traceable to one 0.4.0 release identity.
- Historical completed-task evidence is not rewritten to simulate current version alignment.
- Consumer user-owned files and unrelated Git changes are preserved.
- Only canonical project authority roots are upgraded; workspace child repositories do not gain duplicate workflow state.
- No consumer project is called upgraded if it is blocked, partially mutated, or not validated.

### Invalid Substitutes

- A green source test suite without exact built/public artifact checks.
- A tag or GitHub Release without PyPI publication and fresh installation proof.
- A saved Codex project name without a canonical root manifest.
- A source-checkout upgrade, copied managed files, or an unreviewed nested workflow copy in place of public-package upgrade.
- A successful upgrade command without scoped diff and Doctor validation.

### Artifact Targets

- PyPI `project-workflow==0.4.0`.
- GitHub Release `v0.4.0` with wheel, source distribution, hashes/provenance, and release notes.
- A clean, validated Project Workflow `main` lineage.
- Per-project installed 0.4.0 managed assets for every eligible Codex project.
- Parent release/rollout receipt and acceptance audit.

### Parent AC Proof Ownership

- AC3: owner `TASK-067`; required evidence: PR checks/merge, tag ancestry, release workflow, PyPI and GitHub records

## Acceptance Criteria

- [x] AC1: Green PR checks, merge ancestry, annotated tag, Trusted Publishing, GitHub Release, and expected assets are all verified.

## Validation

- AC1 / parent AC3: PR and Actions records, tag ancestry, PyPI release metadata, GitHub Release assets, and hashes.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | PR #13 merged to `main` as `e9fe9d17a0968ee3fc078d7bb1eb5548029839d2` | PR CI `32315178030`, main CI `32315301955`, and release run `32315431852` passed | `v0.4.0`, PyPI 0.4.0, and GitHub Release published | `evidence/release-publication.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Merge and publish 0.4.0 | Push the candidate, merge the green PR, tag the exact main lineage, and monitor publication. | AC1: one reviewed and published lineage | Inspect GitHub and PyPI records | Done |

## Parent AC Evidence

- AC3: PR #13 merged after green validation; the independent main run passed; annotated `v0.4.0` targets the exact merge commit; protected-environment Trusted Publishing and the same-bundle GitHub Release completed successfully with the recorded hashes.

## QA & Code Review

- Verdict: Pass
- Evidence: `evidence/release-publication.json`, GitHub PR #13, main CI run `32315301955`, release run `32315431852`, PyPI 0.4.0, and GitHub Release v0.4.0.
- Findings: None.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-067
- Title: A reviewed pull request is merged to `main`; `v0.4.0` is an annotated tag on that exact merged lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without rebuilding divergent artifacts
- Created: 2026-08-20
