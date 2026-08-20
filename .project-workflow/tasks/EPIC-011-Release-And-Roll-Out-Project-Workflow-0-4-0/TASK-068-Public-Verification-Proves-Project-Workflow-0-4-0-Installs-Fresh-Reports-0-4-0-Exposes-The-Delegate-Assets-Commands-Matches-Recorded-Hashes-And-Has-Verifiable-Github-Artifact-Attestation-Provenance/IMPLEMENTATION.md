## User Story

As a Codex user, I want the public 0.4.0 package independently verified so that project upgrades use the actual released Delegate-capable artifact.

## Parent AC Coverage

- AC4

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

- AC4: owner `TASK-068`; required evidence: Fresh public install, public artifact hashes, attestation/provenance

## Acceptance Criteria

- [x] AC1: Fresh public installation, version/Delegate inspection, public hashes, and attestation verification all pass.

## Validation

- AC1 / parent AC4: fresh public UVX journey, downloaded asset digests, and GitHub attestation output.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | Public package and release for `e9fe9d17a0968ee3fc078d7bb1eb5548029839d2` | Fresh isolated UVX install, public four-host journeys, receipt/checksum comparison, PyPI metadata, and GitHub attestation verification passed | Public 0.4.0 independently verified | `evidence/public-release/` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Verify public 0.4.0 | Exercise public installation and independently verify artifact identity and provenance. | AC1: all public checks pass | Repeat fresh exact-version journey | Done |

## Parent AC Evidence

- AC4: Fresh public UVX reported `project 0.4.0` and exposed all four Delegate commands; public package journeys passed for every packaged host; PyPI and GitHub hashes match; receipt and checksums verify; SLSA provenance binds the artifacts to `e9fe9d17a0968ee3fc078d7bb1eb5548029839d2` and `refs/tags/v0.4.0`.

## QA & Code Review

- Verdict: Pass
- Evidence: `evidence/public-release/release-receipt.json`, `SHA256SUMS`, `public-package-journeys.json`, and `public-verification.json`.
- Findings: None. Other hosts are proven at packaged asset/journey level; only Codex has the separately retained native runtime proof from EPIC-010.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-068
- Title: Public verification proves `project-workflow==0.4.0` installs fresh, reports 0.4.0, exposes the Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance
- Created: 2026-08-20
