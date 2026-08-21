# Decomposition Plan

## Summary

- Epic: EPIC-015
- Status: Approved by parent requirements envelope
- Authority source: Parent REQUIREMENTS.md Owner Approval
- Source requirements identity: sha256:71fa64f9c5449cc6c641a48c3fb93cf4ef5e6ebc11419d830017ed43cd64df96
- Last updated: 2026-08-21

## Authorized Child Rows

| ID | Title | Parent ACs | Source | Dependencies | Execution Needs |
|---|---|---|---|---|---|
| TASK-085 | Prepare the coherent Project Workflow 0.6.0 release identity | AC1 | Proposed Child Work |  | bounded-return |
| TASK-086 | Validate the exact 0.6.0 release candidate | AC2 | Proposed Child Work | TASK-085 | bounded-return |
| TASK-087 | Integrate, tag and publish Project Workflow 0.6.0 | AC3 | Proposed Child Work | TASK-086 | bounded-return |
| TASK-088 | Verify the public 0.6.0 artifacts and fresh installation | AC4 | Proposed Child Work | TASK-087 | bounded-return |
| TASK-089 | Inventory and safely upgrade every eligible canonical installation, then retain the rollout receipt | AC5, AC6, AC7 | Proposed Child Work | TASK-088 | bounded-return |

## Authority Rules

- Matching rows inside this plan may be approved and scaffolded without separate per-row owner approval.
- Rows outside this plan require an approved amendment before gated lifecycle movement.
- Matching is by ID, title, and parent AC coverage.
