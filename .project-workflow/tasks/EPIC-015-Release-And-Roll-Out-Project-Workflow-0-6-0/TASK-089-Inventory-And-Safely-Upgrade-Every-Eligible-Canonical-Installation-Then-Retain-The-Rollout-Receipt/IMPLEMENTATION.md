## User Story

As the owner of multiple active projects, I want every safe existing installation upgraded without disturbing my work so that 0.6.0 adoption is useful rather than destructive.

## Parent AC Coverage

- AC5
- AC6
- AC7

## Acceptance Criteria

- [ ] AC1: Every saved project has an accurate disposition, safe canonical roots are validated at 0.6.0, blocked roots are unchanged, and the complete receipt is retained.

## Validation

- AC1 / parent AC5-AC7: refreshed inventory, per-root preflight, public plan/apply/no-op plan, scoped diff, manifest/version/helper and Doctor evidence, unchanged blocked-root checks and receipt audit.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| Saved-project estate | Per-project current branch | Pending refreshed inventory | No consumer integration authorized | Machine-readable receipt pending |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Roll out public 0.6.0 safely | Inventory, preflight, upgrade eligible roots, validate all results and retain the receipt. | AC1 | Inspect every disposition and consumer diff. | To Do | TASK-088 | Managed workflow assets in eligible consumer roots plus parent evidence | No | coordinator |

## Parent AC Evidence

- AC5: Pending refreshed estate inventory and dispositions.
- AC6: Pending per-consumer upgrade validation.
- AC7: Pending retained release/rollout receipt and parent audit.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pending rollout proof
- Intent adversarial verdict: Pending rollout proof
- Could every AC pass while the approved user job remains undone: Yes if unsafe roots are silently skipped or clean roots are called upgraded without diff/Doctor proof; every disposition must be explicit.
- Intent audit state: Parent audit refresh pending after child scaffolding
- Outcome journey evidence: Pending public-package consumer upgrades
- Reviewer independence: Parent closeout will independently inspect the receipt and boundaries
- Evidence: Pending execution
- Findings: None recorded before execution

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: None planned
- Follow-up tasks: Any blocked consumer remains a separate future upgrade after its owner work is resolved

## Notes

- Task: TASK-089
- Created: 2026-08-21
