## User Story

As the release coordinator, I want the exact candidate validated once and then stopped, so a later
change can invalidate and rerun only named proof without manufacturing another review cycle.

## Parent AC Coverage

- AC2

## Acceptance Criteria

- [ ] AC1: The complete final-candidate validation matrix passes, and repeated status evaluation
  proves that the same passed change identity cannot generate another validation or review action.

## Validation

- AC1 / parent AC2: locked suite, strict Doctor, release contract, wheel/sdist inspection,
  four-host journeys, behavioral fixtures and deterministic pass-to-stop dogfood.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/intent-integrity-outcome-proof at `32b1aeb` | 428/428 tests, strict Doctor, source contract, wheel/sdist receipt and four-host exact-wheel journeys pass | Not integrated | Retained `evidence/candidate/` artifacts and hashes |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Validate exact candidate | Build and exercise every approved validation layer once, then prove the post-proof stop gate. | AC1 | Inspect final candidate evidence and repeated pass-to-stop status. | Done | TASK-085 | Validation artifacts and task evidence | No | bounded-return |

## Parent AC Evidence

- AC2: Commit `32b1aeb` is the superseded baseline. FIX-009 changes packaged CLI and managed
  guidance, so the final commit requires one fresh locked suite, package build, distribution
  inspection and four-host exact-wheel journey before integration.

## Validation Impact

- Baseline proof: 32b1aeb candidate matrix and package evidence
- Change summary: FIX-009 changes packaged CLI behavior and managed agent guidance
- Impact: affected
- Invalidated proof layers: implementation, structured-evidence
- Required validation: affected-proof-layer
- Validation verdict: pending
- Decided by: Codex
- Change identity: sha256:4a54e8c95e5849bcb33bec76d5f36290a26799d933d453f32dfe16e262f6e904

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pending final candidate validation
- Intent adversarial verdict: Pending final candidate validation
- Could every AC pass while the approved user job remains undone: Yes if the final package and
  repeated stop sequence are not exercised; both remain mandatory.
- Intent audit state: Parent audit refresh pending after final child update
- Outcome journey evidence: Superseded `32b1aeb` package evidence is retained; final candidate
  evidence will replace it after the code is frozen.
- Reviewer independence: No additional model reviewer is authorized by the owner-approved stop
  gate; reviewed GitHub integration remains a separate delivery gate.
- Evidence: Focused stop-gate regression is passing; final locked suite and package evidence pending.
- Findings: No blocking focused-test finding; final candidate validation remains.

## Retro

- Reusable lessons: Pending completion
- Conventions or agent assets updated: None planned
- Follow-up tasks: None currently identified

## Notes

- Task: TASK-086
- Created: 2026-08-21
