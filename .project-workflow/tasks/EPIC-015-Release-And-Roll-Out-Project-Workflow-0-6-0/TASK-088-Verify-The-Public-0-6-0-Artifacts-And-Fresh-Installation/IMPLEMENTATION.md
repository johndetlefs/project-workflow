## User Story

As a downstream project owner, I want the public exact package verified so that upgrades do not rely on an unproven local artifact.

## Parent AC Coverage

- AC4

## Acceptance Criteria

- [x] AC1: Public PyPI/GitHub identities, attestations and a fresh 0.6.0 installation prove the intended package and capabilities.

## Validation

- AC1 / parent AC4: public metadata and hashes, GitHub assets/provenance, disposable exact-version install, version/assets/command checks.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| Public release | `v0.6.0` / PyPI 0.6.0 | GitHub and PyPI hashes match; disposable public install reports 0.6.0 and Doctor passes | Public | [GitHub Release](https://github.com/johndetlefs/project-workflow/releases/tag/v0.6.0); [PyPI](https://pypi.org/project/project-workflow/0.6.0/) |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Verify public 0.6.0 | Compare public identities and attestations, then run fresh exact-version installation checks. | AC1 | Inspect hashes, URLs and fresh-install output. | Done | TASK-087 | Disposable validation artifacts and task evidence | No | bounded-return |

## Parent AC Evidence

- AC4: Public wheel SHA-256 `e459af77a75f6b21ee5361e0c2019b38bc3a007c93bf787e09cb6ae7a27020b1`
  and sdist SHA-256 `fcc9a70bae464f93c1038a5470878acdea424f8101125259eab09d799606986f`
  match on GitHub and PyPI. A disposable `uvx --from project-workflow==0.6.0 project init
  --agent codex` reports `project 0.6.0` and passes Doctor.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: Fresh temporary repository initialized through the public exact-version
  package, then verified with installed helper Doctor and version command.
- Reviewer independence: GitHub Release and PyPI independently expose matching public artifact
  hashes; the disposable installation did not use the local checkout.
- Evidence: Public metadata, matching hashes, GitHub attestations and fresh exact-version install.
- Findings: None blocking.

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: None planned
- Follow-up tasks: None currently identified

## Notes

- Task: TASK-088
- Created: 2026-08-21
