## User Story

As a Coordinator, I want executable progressive-verification and failure rules, so that required
proof remains effective without an unbounded certification, diagnostic, or QA loop.

## Parent AC Coverage

- AC5, AC6, AC7, AC8, AC10, AC11

## Child Charter

### Inherited Invariants

- One 0.7.0 Coordinator and the existing lifecycle remain authoritative.
- Operational verification state is derived from inspectable evidence and never performs work.
- Every materially expensive campaign is bound to one exact candidate, proof contract, mode, ordered stages, limits, and current receipts.
- Required assurance is never traded away for lower usage, elapsed time, or ceremony.
- Certification stops at a blocking product failure; extended investigation is a separate bounded diagnostic decision.
- Later stages never run after an earlier blocking stage.
- Proof reuse is input-specific; unknown material impact fails safely toward broader proof.
- One independent QA verdict remains separate from implementation and Coordinator verification.
- Neither Project Workflow nor a verifier requires the other. Optional compatibility is expressed only through a generic command/JSON boundary.
- Product-specific dogfood evidence is sanitized before it becomes generic package behavior.
- Merge, release, installation, adoption, owner acceptance, and effectiveness remain separate proof gates and authorities.

### Invalid Substitutes

- Another instruction saying to avoid unnecessary QA without executable stage/failure controls.
- Installing Project Workflow 0.7.0 without adding the missing pre-proof campaign capability.
- Adding only reference-consumer runner flags while Project Workflow still cannot govern costly verification.
- Adding a second lifecycle, tracker, review scheduler, execution graph, or generalized platform.
- Treating a release request as authority to silently implement or launch unbounded certification.
- Treating a canary, subset, diagnostic run, stale receipt, or QA prose as complete certification.
- Treating a cost/time limit as evidence that missing or failed proof passed.
- Rerunning target execution after an evaluator-only change when retained outputs are current.
- Static schemas, prompts, status text, or mocked decisions without actual invocation-count proof.
- Any Project Workflow runtime branch, import, schema field, prompt, fixture identifier, or package dependency that names or requires Strategic Advisor.
- Any reference-consumer change that makes its standalone runner depend on Project Workflow.

### Artifact Targets

- Generic campaign schema/state and deterministic operational projection integrated with existing Coordinator/status/Doctor surfaces.
- Progressive stage, failure-mode, campaign-limit, currentness, resume, and one-QA enforcement.
- Framework-neutral optional verifier capability and receipt contract plus manual/no-adapter path.
- Aligned local CLI, package source, templates, Codex/Claude/Copilot/Cursor guidance, README, and validation assets.
- Sanitized behavioural corpus and disposable fake-verifier journey with invocation-count receipts.
- Independent reference-consumer branch with standalone runner controls and optional generic output.
- Sanitized optional-combination dogfood receipt and explicit package/repository/delivery boundary.

### Parent AC Proof Ownership

- AC5: owner `TASK-096, TASK-098`; required evidence: Deterministic and real fake-verifier invocation counts proving fail-fast stage blocking.
- AC6: owner `TASK-096, TASK-098`; required evidence: Invalid/valid diagnostic campaign fixtures and bounded non-certifying receipts.
- AC7: owner `TASK-096, TASK-098`; required evidence: Limit-hit fixtures showing pause/block with required proof still missing.
- AC8: owner `TASK-096, TASK-097, TASK-098`; required evidence: Product/evaluator/provider/harness currentness, retry, resume, regrade, and fallback receipts.
- AC10: owner `TASK-096, TASK-098`; required evidence: One retained QA verdict, affected-validation closure, and no campaign expansion or second QA.
- AC11: owner `TASK-096, TASK-098`; required evidence: Managed/package parity, Doctor/status, fresh/upgrade journey, and historical-state counter-tests.

## Acceptance Criteria

- [x] AC1: Earlier blocking stages prevent later/full work and certification fails fast. Covers parent AC5.
- [x] AC2: Diagnostic mode is explicit, bounded and non-certifying. Covers parent AC6.
- [x] AC3: Limits pause/block without waiving proof. Covers parent AC7.
- [x] AC4: Typed outcomes control currentness, retry, resume and regrade. Covers parent AC8.
- [x] AC5: One QA closes through affected validation without campaign expansion. Covers parent AC10.
- [x] AC6: CLI/package/guidance/status/Doctor parity and historical countercases pass. Covers parent AC11.

## Validation

- AC1-AC6 / parent AC5, AC6, AC7, AC8, AC10, AC11: focused invocation-count,
  stage/failure/limit/currentness/QA tests, managed parity, Doctor/status, then one frozen full suite.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/epic-017-proportionate-verification` from `e1f68633` | 63 affected focused tests and 492-test full suite pass; Doctor passes | Local implementation only; no push/merge/release authorized | Typed failure/limit/regrade/retry, durable omission gate, malformed-output retry and one-QA countercases in `tests/test_verification_campaign.py` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Enforce Stage Order | Gate deterministic, canary, affected, full, QA and delivery transitions from current campaign evidence. | AC1 | Run stage matrix and invocation counter fixtures. | Done | TASK-095 | CLI campaign transitions and tests | No | bounded-return |
| 2 | Separate Certification And Diagnosis | Add fail-fast certification and decision/scope/limit-gated non-certifying diagnosis. | AC1, AC2, AC3 | Prove failure stop, invalid diagnostics and limit exhaustion. | Done | 1 | CLI transition rules and tests | No | bounded-return |
| 3 | Bind Typed Receipts | Add product/evaluator/provider/harness outcome and input-specific reuse, resume, retry, regrade and fallback rules. | AC3, AC4 | Run currentness and typed-outcome matrix. | Done | 1, 2 | receipt validation and tests | No | bounded-return |
| 4 | Constrain QA | Route missing expensive proof back to Coordinator and retain one QA plus affected-validation closure. | AC5 | Run exact QA expansion and second-review countercases. | Done | 1, 2, 3 | QA/Implement/Coordinator guidance and lifecycle tests | No | bounded-return |
| 5 | Align Delivered Surfaces | Update packaged/local/generated assets, README, status/Doctor and historical countercases. | AC5, AC6 | Run parity, package journey, Doctor/status and focused suites. | Done | 1, 2, 3, 4 | managed assets, docs, tests | No | bounded-return |

## Parent AC Evidence

- AC5, AC6, AC7, AC8, AC10, AC11: Invocation-count tests prove fail-fast ordering; diagnostics and limits remain non-certifying; typed request/receipt tampering fails closed; evaluator regrade records zero target calls; infrastructure retry is bounded; QA cannot broaden/repeat the campaign; managed/package/status/Doctor regression coverage passes.

## Validation Impact

- Baseline proof: Independent QA Changes Requested for TASK-096 on 2026-08-27
- Change summary: Made durable required-campaign omission block Review/Complete, made hard-limit overshoot block even after stage completion, and retained malformed/mismatched adapter output as one typed harness attempt before blocking after the single retry.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-017 Coordinator
- Change identity: sha256:c4f696771545aa14f6db9c8e489da1d51e9173def3707cfa45f68766ec8f37fd

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: current
- Outcome journey evidence: The reviewer confirmed tested stage ordering, fail-fast, diagnostics, regrade and one infrastructure retry, then reproduced omitted-campaign, completed-stage limit-overrun and unrecorded malformed-adapter loops.
- Reviewer independence: Isolated read-only `codex exec` reviewer session `96524`; it did not author or modify the candidate.
- Evidence: Independent QA transcript `/private/tmp/pw-epic017-qa.txt`; review-time Intent audit identity `sha256:189ad5aeaaba52429ab1adceecac63d56beeb837f824181f7939ff8fe2a4745a`; affected invocation-count regressions in `tests/test_verification_campaign.py`.
- Findings: High - required campaign enforcement disappeared when state was absent. High - a completed stage could exceed a declared target-call cap and still pass. High - request mismatch exited without retaining an infrastructure attempt and could repeat indefinitely.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Durable omission blocks Review, completed-stage overshoot projects `limit-reached`, and two malformed adapter attempts are retained before the third invocation is forbidden; 63 affected focused and 492 full tests pass.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-096
- Title: Enforce Progressive Verification And QA Boundaries
- Created: 2026-08-27
