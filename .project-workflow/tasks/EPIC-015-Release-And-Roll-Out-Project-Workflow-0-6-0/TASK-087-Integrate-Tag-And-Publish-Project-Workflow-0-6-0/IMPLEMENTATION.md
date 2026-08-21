## User Story

As an installer, I want 0.6.0 published from reviewed main so that the package has a trustworthy integration lineage.

## Parent AC Coverage

- AC3

## Acceptance Criteria

- [x] AC1: A green reviewed PR, exact main ancestry, annotated v0.6.0 tag and successful trusted publication are proven.

## Validation

- AC1 / parent AC3: GitHub PR/check/review evidence, merge ancestry, tag inspection and release workflow evidence.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | PR [#19](https://github.com/johndetlefs/project-workflow/pull/19) | Required `validate` check passed; merge ancestry and release workflow passed | Merged as `8f3f5c9`; `v0.6.0` published | [Release run 32458912205](https://github.com/johndetlefs/project-workflow/actions/runs/32458912205) |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Integrate and publish 0.6.0 | Commit, open ready PR, pass checks, merge, tag exact main and monitor trusted release. | AC1 | Inspect PR, commit, tag and workflow identities. | Done | TASK-086 | Git branch, PR, main tag and release workflow | No | coordinator |

## Parent AC Evidence

- AC3: PR #19 merged at `8f3f5c95973f36e010e7639a5a95909369813ac4`; annotated tag
  `v0.6.0` identifies that commit; release run 32458912205 passed build, full validation, exact
  package journeys, attestation, trusted PyPI publication and GitHub Release creation.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: PR #19, merge commit `8f3f5c9`, tag `v0.6.0` and release run
  32458912205 form one inspectable lineage.
- Reviewer independence: GitHub required checks and protected PyPI-environment approval are
  external integration gates separate from local implementation.
- Evidence: PR #19; release run 32458912205; GitHub Release `v0.6.0`; PyPI 0.6.0.
- Findings: None blocking.

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: None planned
- Follow-up tasks: None currently identified

## Notes

- Task: TASK-087
- Created: 2026-08-21
