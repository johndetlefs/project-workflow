## User Story

As the release coordinator, I want one coherent 0.6.0 candidate so that later validation and publication refer to the same artifact identity.

## Parent AC Coverage

- AC1

## Acceptance Criteria

- [x] AC1: All current release authorities identify 0.6.0 and managed mirrors are aligned without historical evidence changes.

## Validation

- AC1 / parent AC1: version scan, mirror hashes, managed asset parity, changelog and release-workflow diff inspection.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | PR [#19](https://github.com/johndetlefs/project-workflow/pull/19) | Release contract, version scans, mirror hashes and focused manifest/guidance tests pass | Merged as `8f3f5c9`; published as `v0.6.0` | CLI SHA-256 `57fc045258bb32c5899ae86b6de007d1da7f913c3b683a08523d5d8992ff9257`; focused tests 2/2 |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Align 0.6.0 release identity | Update current version authorities, managed mirrors, changelog and release instructions. | AC1 | Inspect version and parity evidence. | Done | | Source and managed release files | No | bounded-return |

## Parent AC Evidence

- AC1: Source, three CLI mirrors, manifest, managed asset version, current docs, CI, release workflow and runbook identify 0.6.0; release-contract check and focused tests pass; historical 0.5.1 records remain unchanged.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: Version 0.6.0 source contract and manifest/guidance generation checks pass.
- Reviewer independence: Independent review is owned by TASK-086
- Evidence: `check-source --version 0.6.0 --tag v0.6.0`, locked dependency check, two focused tests, mirror SHA-256 and clean diff check.
- Findings: None blocking; TASK-086 regenerated and validated the exact candidate artifacts before publication.

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: Release authorities only
- Follow-up tasks: None currently identified

## Notes

- Task: TASK-085
- Created: 2026-08-21
