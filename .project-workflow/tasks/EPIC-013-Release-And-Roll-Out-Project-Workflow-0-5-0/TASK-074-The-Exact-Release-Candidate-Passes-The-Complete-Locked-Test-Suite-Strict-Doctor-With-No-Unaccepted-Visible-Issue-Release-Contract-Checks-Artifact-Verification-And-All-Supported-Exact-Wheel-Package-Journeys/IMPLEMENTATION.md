## User Story

As the release owner, I want the exact 0.5.0 candidate proven end to end so that publication cannot drift from the reviewed source.

## Parent AC Coverage

- AC2

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

- AC2: owner `TASK-074`; required evidence: Complete tests, strict Doctor, release contract, exact-artifact journeys

## Acceptance Criteria

- [x] AC1: Covers parent AC2 when every declared candidate validation passes and the recorded wheel/source hashes bind to the exact source commit.

## Validation

- AC1 / parent AC2: Run locked pytest, strict Doctor, `check-source`, build distributions, verify the receipt, and run exact-wheel package journeys.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/EPIC-012-delegate-executor-lifecycle`; candidate `94934cfd2995885216c15447852de4c72c3e36d9` | 395/395 tests, strict Doctor, lock/source contract, wheel/sdist receipt, and exact-wheel journeys for Codex, Claude Code, Cursor, and GitHub Copilot passed | Validated local release candidate; not yet merged or published | `evidence/candidate/` plus coordinator command output on 2026-08-20 |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Validate exact candidate | Exercise the complete locked suite, strict Doctor, release contract, built distributions, and exact-wheel journeys. | AC1: every declared candidate validation passes and the recorded wheel/source hashes bind to the exact source commit. | Inspect the final receipt, hashes, and passing command results. | Done | | tests; scripts; dist; release; .project-workflow/tasks/EPIC-013-Release-And-Roll-Out-Project-Workflow-0-5-0/evidence | No | bounded-return |

## Parent AC Evidence

- AC2: Candidate `94934cfd2995885216c15447852de4c72c3e36d9` passed 395 tests in 70.64s, strict Doctor with 69 accepted historical warnings hidden and no issue, `uv lock --check`, clean source contract, receipt verification, and exact-wheel journeys for all four packaged host modes. Wheel SHA-256 is `2cce584f7d6a498d3824d15bf5085d0e1bb9e874f23cec35be81a71c724c8a8d`; sdist SHA-256 is `52160e32af065dcb0a3b7b4244bbc4c7ea0c97a8c7f9f1e4a0b63408f74e38a2`.

## QA & Code Review

- Verdict: Pass
- Evidence: `evidence/candidate/release-receipt.json`, `SHA256SUMS`, `package-journeys.json`, full-suite output, strict Doctor output, and clean source-contract output.
- Findings: None. GitHub CI will independently rebuild and bind the final integrated lineage before tagging.

## Retro

- Reusable lessons: Keep a writable task-specific UV cache in Codex release commands; the default user cache may be sandbox-inaccessible.
- Conventions or agent assets updated: None.
- Follow-up tasks: None.

## Notes

- Task: TASK-074
- Title: The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys
- Created: 2026-08-20
