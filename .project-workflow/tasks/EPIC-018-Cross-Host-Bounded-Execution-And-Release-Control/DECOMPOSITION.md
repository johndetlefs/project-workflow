# Decomposition Plan

## Summary

- Epic: EPIC-018
- Status: Approved by parent requirements envelope
- Authority source: Parent REQUIREMENTS.md Owner Approval
- Source requirements identity: sha256:4fb20ac510298374315f6e6988d1b25c68ad65a206f19c910c31e6ecf2e6e57d
- Last updated: 2026-08-31

## Authorized Child Rows

| ID | Title | Parent ACs | Source | Dependencies | Execution Needs |
|---|---|---|---|---|---|
| TASK-099 | Define Host-Neutral Execution And Candidate Contract | AC1, AC2, AC3, AC4, AC5, AC7, AC11, AC12 | Proposed Child Work |  | bounded-return |
| TASK-100 | Enforce Proportionate QA Remediation And Fixed Release | AC4, AC5, AC6, AC7, AC8, AC15 | Proposed Child Work | Define Host-Neutral Execution And Candidate Contract | bounded-return |
| TASK-101 | Refactor FIX-010 Into The Codex Adapter | AC3, AC4, AC8, AC9, AC12, AC13, AC14 | Proposed Child Work | Define Host-Neutral Execution And Candidate Contract; Enforce Proportionate QA Remediation And Fixed Release | bounded-return |
| TASK-102 | Build The Claude Code Adapter | AC3, AC4, AC8, AC10, AC11, AC12, AC13 | Proposed Child Work | Define Host-Neutral Execution And Candidate Contract; Enforce Proportionate QA Remediation And Fixed Release | bounded-return |
| TASK-103 | Prove Cross-Host Conformance And Delivery Boundary | AC5, AC6, AC8, AC9, AC11, AC12, AC13, AC14, AC15, AC16 | AMD-002 Codex-only release boundary | Refactor FIX-010 Into The Codex Adapter; Build The Claude Code Adapter | bounded-return |

## Authority Rules

- Matching rows inside this plan may be approved and scaffolded without separate per-row owner approval.
- Rows outside this plan require an approved amendment before gated lifecycle movement.
- Matching is by ID, title, and parent AC coverage.
