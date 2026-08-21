## User Story

As the release coordinator, I want the exact candidate independently validated so that integration is based on artifact-level proof.

## Parent AC Coverage

- AC2

## Acceptance Criteria

- [ ] AC1: The complete candidate validation matrix passes with no blocking independent QA finding.

## Validation

- AC1 / parent AC2: locked suite, strict Doctor, release contract, wheel/sdist inspection, four-host journeys, behavioral fixtures and independent QA.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/intent-integrity-outcome-proof | Pending exact candidate run | Not integrated | Retained validation outputs |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Validate exact candidate | Build and exercise every approved validation layer, then run independent QA. | AC1 | Inspect command results and QA verdict. | To Do | TASK-085 | Validation artifacts and task evidence | No | bounded-return |

## Parent AC Evidence

- AC2: Pending TASK-086 validation evidence.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pending independent QA
- Intent adversarial verdict: Pending independent QA
- Could every AC pass while the approved user job remains undone: Yes if only source checks run; distribution and journey proof are mandatory.
- Intent audit state: Parent audit refresh pending after child scaffolding
- Outcome journey evidence: Pending exact-wheel journeys
- Reviewer independence: Required and pending
- Evidence: Pending execution
- Findings: None recorded before execution

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: None planned
- Follow-up tasks: None currently identified

## Notes

- Task: TASK-086
- Created: 2026-08-21
