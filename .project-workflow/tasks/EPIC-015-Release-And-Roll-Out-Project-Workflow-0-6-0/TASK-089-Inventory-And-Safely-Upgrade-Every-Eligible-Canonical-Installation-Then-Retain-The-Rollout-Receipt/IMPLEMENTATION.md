## User Story

As the owner of multiple active projects, I want every safe existing installation upgraded without disturbing my work so that 0.6.0 adoption is useful rather than destructive.

## Parent AC Coverage

- AC5
- AC6
- AC7

## Acceptance Criteria

- [x] AC1: Every canonical installation has an accurate disposition, safe roots are validated at 0.6.0, blocked roots are unchanged, and the complete receipt is retained.

## Validation

- AC1 / parent AC5-AC7: refreshed inventory, per-root preflight, public plan/apply/no-op plan, scoped diff, manifest/version/helper and Doctor evidence, unchanged blocked-root checks and receipt audit.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| Canonical installation estate | Per-project current branch | 10 dispositions; seven at 0.6.0 with strict Doctor pass; three dirty roots unchanged | Six public-package managed diffs remain uncommitted; Project Workflow main fast-forwarded | `evidence/rollout-receipt.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Roll out public 0.6.0 safely | Inventory, preflight, upgrade eligible roots, validate all results and retain the receipt. | AC1 | Inspect every disposition and consumer diff. | Done | TASK-088 | Managed workflow assets in eligible consumer roots plus parent evidence | No | coordinator |

## Parent AC Evidence

- AC5: Ten canonical installations recorded: seven upgraded and three dirty roots preserved.
- AC6: Six public-package consumers report 0.6.0, zero-target no-op plans and strict Doctor pass;
  Project Workflow is clean at released main `8f3f5c9` with strict Doctor pass.
- AC7: `evidence/rollout-receipt.json` binds release identity, public hashes, every plan fingerprint,
  per-root result and blocked-root unchanged evidence.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: Six clean consumers completed plan/fingerprint/apply/no-op-plan/Doctor;
  the clean Project Workflow root fast-forwarded to released main; three dirty roots retained their
  exact original head, dirty count and version.
- Reviewer independence: Public-package fingerprints and each installed helper independently
  enforce source identity, clean preconditions, no-op state and Doctor results.
- Evidence: `evidence/rollout-receipt.json` and the current consumer repositories.
- Findings: Three intentional blockers remain unchanged: The Moon Is Hollow, johndetlefs and Game
  Foundation are dirty and were not upgraded.

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: None planned
- Follow-up tasks: Any blocked consumer remains a separate future upgrade after its owner work is resolved

## Notes

- Task: TASK-089
- Created: 2026-08-21
