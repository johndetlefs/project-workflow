## User Story

As a Project Workflow user, I want public 0.5.0 independently verified so that consumer upgrades use the released package rather than a local surrogate.

## Parent AC Coverage

- AC4

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

- AC4: owner `TASK-076`; required evidence: Fresh public install, public artifact hashes, attestation/provenance

## Acceptance Criteria

- [x] AC1: Covers parent AC4 when fresh public installation and public artifact/provenance checks pass against the released identities.

## Validation

- AC1 / parent AC4: Use public UVX/PyPI metadata, GitHub Release assets, hashes, attestations, and a fresh disposable init/Doctor journey.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | Public `project-workflow==0.5.0` from source commit `fdd4e15c621cb6805e1455d0658c60ee24b92b0c` | Public UVX reports `project 0.5.0`; all four public package journeys and SLSA attestation verification pass | Public artifacts verified | `evidence/release-rollout-receipt.json`; child `EVIDENCE.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Verify public release | Exercise the public exact-version package and match PyPI/GitHub artifacts and provenance. | AC1: fresh public installation and public artifact/provenance checks pass against the released identities. | Run the fresh public install and compare all recorded identities. | Done | | Disposable temporary repository; public PyPI and GitHub release metadata | No | bounded-return |

## Parent AC Evidence

- AC4: Public `uvx --from project-workflow==0.5.0 project --version` returned `project 0.5.0`; public exact-version Codex, Claude Code, Cursor, and GitHub Copilot journeys passed; downloaded hashes matched the release; GitHub SLSA provenance verified source commit, tag ref, release workflow, and runner. Structured runtime/source evidence passes in `EVIDENCE.json`.

## QA & Code Review

- Verdict: Pass (2026-08-20)
- Evidence: Public wheel `b970773...`, sdist `7d0ef1...`, public-package journey receipt `872c21d4...`, and verified GitHub attestation provenance.
- Findings: None. Non-Codex host proof is package-install guidance parity, not native runtime activation.

## Retro

- Reusable lessons: GitHub attestation verification may need a task-local `XDG_CACHE_HOME` when the normal TUF cache is sandbox-inaccessible.
- Conventions or agent assets updated: None; this is environment setup evidence rather than a source defect.
- Follow-up tasks: None.

## Notes

- Task: TASK-076
- Title: Public verification proves `project-workflow==0.5.0` installs fresh, reports 0.5.0, exposes the capability-aware Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance
- Created: 2026-08-20
