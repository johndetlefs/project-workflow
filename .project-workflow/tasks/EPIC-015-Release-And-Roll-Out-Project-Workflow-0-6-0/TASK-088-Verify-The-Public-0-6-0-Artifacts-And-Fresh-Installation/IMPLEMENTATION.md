## User Story

As a downstream project owner, I want the public exact package verified so that upgrades do not rely on an unproven local artifact.

## Parent AC Coverage

- AC4

## Acceptance Criteria

- [ ] AC1: Public PyPI/GitHub identities, attestations and a fresh 0.6.0 installation prove the intended package and capabilities.

## Validation

- AC1 / parent AC4: public metadata and hashes, GitHub assets/provenance, disposable exact-version install, version/assets/command checks.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| Public release | v0.6.0 | Pending public verification | Pending | Public URLs and hashes pending |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Verify public 0.6.0 | Compare public identities and attestations, then run fresh exact-version installation checks. | AC1 | Inspect hashes, URLs and fresh-install output. | To Do | TASK-087 | Disposable validation artifacts and task evidence | No | bounded-return |

## Parent AC Evidence

- AC4: Pending TASK-088 public verification evidence.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pending public proof
- Intent adversarial verdict: Pending public proof
- Could every AC pass while the approved user job remains undone: Yes if cached or local artifacts substitute for public retrieval; downloads must be fresh.
- Intent audit state: Parent audit refresh pending after child scaffolding
- Outcome journey evidence: Pending fresh public installation
- Reviewer independence: Public service identities provide an external boundary after TASK-086 review
- Evidence: Pending execution
- Findings: None recorded before execution

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: None planned
- Follow-up tasks: None currently identified

## Notes

- Task: TASK-088
- Created: 2026-08-21
