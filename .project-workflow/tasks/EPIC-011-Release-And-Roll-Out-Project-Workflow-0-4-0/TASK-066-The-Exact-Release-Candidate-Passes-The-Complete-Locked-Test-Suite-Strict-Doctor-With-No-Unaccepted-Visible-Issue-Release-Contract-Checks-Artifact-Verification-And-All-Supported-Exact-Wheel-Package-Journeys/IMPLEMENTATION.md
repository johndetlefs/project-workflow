## User Story

As the release maintainer, I want the exact 0.4.0 candidate proven at source and package layers so that merge does not rely on lower-fidelity evidence.

## Parent AC Coverage

- AC2

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

- AC2: owner `TASK-066`; required evidence: Complete tests, strict Doctor, release contract, exact-artifact journeys

## Acceptance Criteria

- [x] AC1: The candidate passes the full locked suite, strict Doctor, release contract, artifact verification, and every exact-wheel host journey.

## Validation

- AC1 / parent AC2: retained full-test, Doctor, build, receipt, and four-host package-journey logs.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/EPIC-010-delegate-execution-orchestrator`; candidate commit `977c3eb1aa0a74b27c9d1d59bb34fd46ae14e20c` | 377/377 tests, strict Doctor, lock/source contract, wheel/sdist receipt verification, and exact-wheel journeys for Codex, Claude Code, Cursor, and GitHub Copilot passed | Validated release candidate; not yet merged or published | `evidence/candidate/` plus 2026-08-20 command outputs |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Validate exact candidate | Exercise all source and built-artifact gates against the same 0.4.0 candidate. | AC1: every required command passes | Re-run logged release validation | Done |

## Parent AC Evidence

- AC2: Candidate commit `977c3eb1aa0a74b27c9d1d59bb34fd46ae14e20c` passed 377 tests in 61.85s, strict Doctor with 69 accepted historical warnings hidden and no issue, `uv lock --check`, source contract, clean artifact receipt verification, and exact-wheel journeys for all four packaged host modes. The retained wheel SHA-256 is `f6094f1025542d9edd3bc2f2cc9bf1ee3486b49c80f5351d43af96afdf25e1df`.

## QA & Code Review

- Verdict: Pass
- Evidence: `evidence/candidate/release-receipt.json`, `SHA256SUMS`, `package-journeys.json`, full-suite output, strict Doctor output, and source-contract output.
- Findings: None. The local receipt proves the pre-merge candidate commit; GitHub CI will independently build and bind the reviewed merge lineage before tagging.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-066
- Title: The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys
- Created: 2026-08-20
