## User Story

As the release coordinator, I want the exact candidate validated once and then stopped, so a later
change can invalidate and rerun only named proof without manufacturing another review cycle.

## Parent AC Coverage

- AC2

## Acceptance Criteria

- [x] AC1: The complete final-candidate validation matrix passes, and repeated status evaluation
  proves that the same passed change identity cannot generate another validation or review action.

## Validation

- AC1 / parent AC2: locked suite, strict Doctor, release contract, wheel/sdist inspection,
  four-host journeys, behavioral fixtures and deterministic pass-to-stop dogfood.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof` at `d06eb8b` | 79/79 focused stop-gate/status tests; one 442-test process completed without a recorded failure but lost its detached final summary; strict Doctor; source contract; wheel/sdist receipt and all package journeys pass | Not integrated | `evidence/candidate/` exact artifacts, receipt, hashes and package journeys |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Validate exact candidate | Build and exercise every approved validation layer once, then prove the post-proof stop gate. | AC1 | Inspect final candidate evidence and repeated pass-to-stop status. | Done | TASK-085 | Validation artifacts and task evidence | No | bounded-return |

## Parent AC Evidence

- AC2: Final candidate `d06eb8b` produced wheel SHA-256
  `944b201ff15c3b9b2ecfd8bb8055830a5b9bc9c6c984efb4ebdda93f90715c99` and sdist SHA-256
  `734bda96c54b74f7fe215910c9bef4dd61f6294dd2d8ef9e6a70409c36a2dae5`;
  receipt verification, fresh Codex/Claude Code/Cursor/GitHub Copilot journeys and legacy upgrade
  pass. Repeated affected-pass evaluation returns no continuation action.

## Validation Impact

- Baseline proof: 32b1aeb candidate matrix and package evidence
- Change summary: FIX-009 changes packaged CLI behavior and managed agent guidance
- Impact: affected
- Invalidated proof layers: implementation, structured-evidence
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: Codex
- Change identity: sha256:4a54e8c95e5849bcb33bec76d5f36290a26799d933d453f32dfe16e262f6e904

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: `evidence/candidate/package-journeys.json` exercises the exact final
  wheel across all four supported fresh hosts and the legacy upgrade journey; focused tests execute
  affected-pending, affected-pass twice, unaffected and ambiguous stop-gate paths.
- Reviewer independence: The owner independently identified the recursive-review failure, rejected
  the overbuilt design and approved the three-outcome replacement; GitHub PR review remains the
  separate integration gate.
- Evidence: 79/79 focused tests, strict Doctor, exact final receipt and package journeys; the one
  442-test process completed without a recorded failure, although its detached final summary was
  not recoverable and CI must provide the authoritative full-suite receipt.
- Findings: No blocking finding within AC1. No additional model review is authorized.

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: None planned
- Follow-up tasks: None currently identified

## Notes

- Task: TASK-086
- Created: 2026-08-21
