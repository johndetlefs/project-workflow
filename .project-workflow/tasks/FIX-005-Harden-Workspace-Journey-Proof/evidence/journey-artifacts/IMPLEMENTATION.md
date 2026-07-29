## User Story

As the workspace owner, I want one parent task to coordinate three repositories without creating child workflow state.

## Acceptance Criteria

- [x] AC1: The parent task records valid repository scope, status, and evidence through handoff.

## Validation

- AC1: Run the actual Project Workflow CLI lifecycle and inspect the generated task and tracker artifacts.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| workspace | `main`; PR not created | Workflow Doctor passed | No delivery authorized | `evidence/workspace-validation.txt` |
| next | `main`; PR not created | Next validation passed | No delivery authorized | `evidence/next-validation.txt` |
| email | Detached fixture; PR not created | Email validation passed | No delivery authorized | `evidence/email-validation.txt` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Coordinate repositories | Exercise the parent-owned workspace lifecycle. | AC1 | Inspect CLI output and generated artifacts. | Done |

## QA & Code Review

- Date: 2026-07-29
- Verdict: Pass
- Evidence: Focused CLI status and repository-specific validation receipts passed.
- Findings: None.

## Retro

- Reusable lessons: Workspace handoff proof must remain repository-attributed.
- Conventions or agent assets updated: None.
- Follow-up tasks: None.
