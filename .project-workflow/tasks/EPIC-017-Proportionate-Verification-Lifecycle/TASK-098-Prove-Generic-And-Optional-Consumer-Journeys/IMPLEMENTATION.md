## User Story

As the owner, I want the exact expensive-loop journey and countercases exercised with real
invocation receipts, so that Project Workflow cannot call the feature fixed through prose, mocks,
undercooked proof, or consumer coupling.

## Parent AC Coverage

- AC4, AC5, AC8, AC10, AC11, AC12, AC13, AC15

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

- AC4: owner `TASK-095, TASK-098`; required evidence: Incomplete-candidate release fixture with zero verifier invocations.
- AC5: owner `TASK-096, TASK-098`; required evidence: Deterministic and real fake-verifier invocation counts proving fail-fast stage blocking.
- AC8: owner `TASK-096, TASK-097, TASK-098`; required evidence: Product/evaluator/provider/harness currentness, retry, resume, regrade, and fallback receipts.
- AC10: owner `TASK-096, TASK-098`; required evidence: One retained QA verdict, affected-validation closure, and no campaign expansion or second QA.
- AC11: owner `TASK-096, TASK-098`; required evidence: Managed/package parity, Doctor/status, fresh/upgrade journey, and historical-state counter-tests.
- AC12: owner `TASK-098`; required evidence: Complete sanitized failure/counter-failure behavioural matrix.
- AC13: owner `TASK-098`; required evidence: Disposable fake-verifier journey with exact target/full/QA/regrade/delivery counts.
- AC15: owner `TASK-097, TASK-098`; required evidence: Sanitized optional-combination journey and package/source no-coupling proof.

## Acceptance Criteria

- [x] AC1: Incomplete preflight invokes zero verifier calls. Covers parent AC4.
- [x] AC2: Canary/full/regrade/unchanged invocation counts match the approved journey. Covers parent AC5, AC8, AC13.
- [x] AC3: One QA closes without second review or campaign expansion. Covers parent AC10.
- [x] AC4: Focused/full/package/parity/status/Doctor proof is exact and current. Covers parent AC11.
- [x] AC5: Complete sanitized failure/counter-failure matrix passes. Covers parent AC12.
- [x] AC6: Generic source is consumer-free and optional consumer is standalone. Covers parent AC15.
- [x] AC7: Intent/acceptance audits and delivery boundaries are complete. Covers parent AC4, AC11, AC12, AC13, AC15.

## Validation

- AC1-AC7 / parent AC4, AC5, AC8, AC10, AC11, AC12, AC13, AC15: deterministic
  invocation journey, failure/counter-failure matrix, focused/frozen full/package/parity/status/
  Doctor proof, optional-consumer evidence, one QA and Epic audits.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/epic-017-proportionate-verification` from `e1f68633` | 63 affected focused and 492 full tests pass; generated CLI SHA parity; Doctor pass | Local implementation/QA/closeout only; no push/merge/release authorized | Complete fake-adapter sequence and `evidence/optional-consumer-dogfood.json` |
| `/Users/johndetlefs/repos/strategic-advisor` | `codex/proportionate-verification-runner` at `82b44a0aabe81662917c44b8e99d3a2a6fd021c4`, from `6d65830f` | 17 focused runner tests, 188 full tests and seven validation scopes pass | Local commit only; no push/merge/release/install authorized | Standalone/request-bound receipt; pre-existing TASK-030 Doctor boundary retained |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Build Fake-Verifier Journey | Exercise the complete preflight/fail/correct/certify/QA/regrade/deliver sequence with exact counters. | AC1, AC2 | Inspect retained invocation and receipt identities. | Done | TASK-095, TASK-096 | generic journey scripts/tests/evidence | No | bounded-return |
| 2 | Run Failure Countercases | Exercise diagnostics, limits, interruption, stale/unknown impact, cheap work, no-adapter and high-assurance cases. | AC2, AC5 | Run the complete sanitized matrix. | Done | TASK-095, TASK-096 | behavioral scenarios and tests | No | bounded-return |
| 3 | Prove Decoupling | Scan generic product/package source and reconcile standalone optional-consumer capability/receipt evidence. | AC6 | Run prohibited-identity scan and standalone/conformance checks. | Done | TASK-097 | source scan and sanitized receipts | No | bounded-return |
| 4 | Freeze And Validate Candidate | Run affected focused checks, one frozen full suite, package/parity/status/Doctor evidence and record exact source. | AC4 | Inspect validation and package receipts. | Done | 1, 2, 3 | Project Workflow validation/evidence | No | bounded-return |
| 5 | Prepare QA And Epic Audit Packet | Freeze current child evidence, exact validation receipts and delivery boundaries for the one independent review and final audits. | AC3, AC7 | Inspect the bounded reviewer packet and current Intent audit. | Done | 1, 2, 3, 4 | child docs, evidence, Epic audits | No | bounded-return |

## Parent AC Evidence

- AC4, AC5, AC8, AC10, AC11, AC12, AC13, AC15: Sanitized fake-verifier fixtures prove zero calls before completion, no full after canary failure, one corrected canary/full campaign, zero-target evaluator regrade, one QA and unchanged delivery reuse. The optional real-process join retains that complete ordered sequence and binds exact request/candidate/stage/scope in schema-2 `evidence/optional-consumer-dogfood.json`; product source scans remain consumer-free. The current Intent audit passes, and the pre-completion acceptance audit reported only TASK-098's own Review/evidence disposition as the remaining gap.

## Validation Impact

- Baseline proof: Independent QA Changes Requested for TASK-098 on 2026-08-27
- Change summary: Added the missing omission, hard-cap, rehashed-ledger and repeated-malformed-output countercases, and replaced the final-only optional-consumer receipt with a tested seven-event bounded sequence.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-017 Coordinator
- Change identity: sha256:e96e24a3928492c94868468ebe85f658ac49933dea3d829884bdee8ffe757ef1

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: current
- Outcome journey evidence: The reviewer accepted current focused/full/parity/Doctor evidence and source decoupling, but found that the optional receipt retained only its final event and the matrix omitted reproduced fail-closed counterexamples.
- Reviewer independence: Isolated read-only `codex exec` reviewer session `96524`; it did not author or modify the candidate.
- Evidence: Independent QA transcript `/private/tmp/pw-epic017-qa.txt`; review-time Intent audit identity `sha256:189ad5aeaaba52429ab1adceecac63d56beeb837f824181f7939ff8fe2a4745a` with parent acceptance pending; schema-2 `evidence/optional-consumer-dogfood.json`; affected regressions in `tests/test_verification_campaign.py`.
- Findings: High - optional-consumer dogfood retained only one final full-stage result rather than the required sequence. High - matrix missed omitted campaign, completed-stage cap, rehashed-ledger and repeated malformed-output counterexamples. Medium - AC3/AC7 and acceptance audit were still pending at the intentionally pre-closeout review point.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: The tested schema-2 artifact retains incomplete preflight, failed canary, correction, canary/full pass, zero-target regrade, one QA and unchanged delivery; all new countercases, 63 affected focused tests and 492 full tests pass. AC3 and AC7 are complete; the acceptance audit was run before TASK-098 completion and isolated only its self-referential Review/evidence gap.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-098
- Title: Prove Generic And Optional-Consumer Journeys
- Created: 2026-08-27
