# Decomposition Plan

## Summary

- Epic: EPIC-020
- Status: Approved by parent requirements envelope
- Authority source: Parent REQUIREMENTS.md Owner Approval
- Source requirements identity: sha256:4dfaab081e570fa32d700d9db1a92c7b6686239f08c026af8f61591922a1b608
- Last updated: 2026-08-29

## Authorized Child Rows

| ID | Title | Parent ACs | Source | Dependencies | Execution Needs |
|---|---|---|---|---|---|
| TASK-109 | Prepare and prove the exact Project Workflow 0.9.1 candidate | AC1, AC2 | Proposed Child Work |  | bounded-return |
| TASK-110 | Integrate, tag, and publish Project Workflow 0.9.1 | AC3 | Proposed Child Work | TASK-109 | bounded-return |
| TASK-111 | Verify the public Project Workflow 0.9.1 release | AC4 | Proposed Child Work | TASK-110 | bounded-return |
| TASK-112 | Inventory and safely upgrade every Project Workflow installation | AC5, AC6, AC7 | Proposed Child Work | TASK-111 | bounded-return |

## Authority Rules

- Matching rows inside this plan may be approved and scaffolded without separate per-row owner approval.
- Rows outside this plan require an approved amendment before gated lifecycle movement.
- Matching is by ID, title, and parent AC coverage.
