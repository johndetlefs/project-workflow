## User Story

As a Coordinator, I want one generic current verification campaign and derived next state, so that
I can expose the true release boundary before any expensive verifier runs.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC9

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

- AC1: owner `TASK-095, TASK-096`; required evidence: Architecture/source inspection and regressions proving one Coordinator/lifecycle and no copied graph.
- AC2: owner `TASK-095, TASK-096`; required evidence: Campaign schema/currentness tests plus malformed/stale/source-mismatch failures.
- AC3: owner `TASK-095`; required evidence: Human/JSON status fixtures deriving each operational result without mutation.
- AC4: owner `TASK-095, TASK-098`; required evidence: Incomplete-candidate release fixture with zero verifier invocations.
- AC9: owner `TASK-095, TASK-097, TASK-098`; required evidence: Generic source scan, no-adapter/manual path, fake adapter, standalone consumer, and optional conformance proof.

## Acceptance Criteria

- [x] AC1: Existing Coordinator/lifecycle remains singular; campaign state is compact. Covers parent AC1.
- [x] AC2: Campaign schema/currentness fails closed with stable diagnostics. Covers parent AC2.
- [x] AC3: All five operational projections are deterministic and non-mutating. Covers parent AC3.
- [x] AC4: Incomplete release preflight invokes no verifier. Covers parent AC4.
- [x] AC5: Generic/manual/fake-adapter paths prove no consumer coupling. Covers parent AC9.

## Validation

- AC1-AC5 / parent AC1, AC2, AC3, AC4, AC9: focused campaign, projection, Doctor/status,
  non-mutation, adapter-boundary, and source-scan tests.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/epic-017-proportionate-verification` from `e1f68633` | 63 affected focused tests and 492-test full suite pass; three CLI copies SHA-256 `ba8c038a...` | Local implementation only; no push/merge/release authorized | `tests/test_verification_campaign.py`; full-suite receipt from 2026-08-27 |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define Campaign Schema | Add the compact current-campaign and optional adapter capability/receipt contracts without another graph or lifecycle. | AC1, AC2, AC5 | Run valid/invalid schema and no-coupling fixtures. | Done |  | CLI/source schemas, coordination state | No | bounded-return |
| 2 | Add Campaign CLI | Initialize, update, and inspect fingerprint-bound campaign state through supported CLI operations. | AC1, AC2 | Exercise CLI round-trip and stale-source rejection. | Done | 1 | CLI/parser/template parity | No | bounded-return |
| 3 | Project Operational State | Derive the five read-only operational outcomes in human/JSON status and Doctor. | AC2, AC3, AC4 | Run all projection fixtures twice and compare repository bytes. | Done | 1, 2 | status/Doctor source and tests | No | bounded-return |
| 4 | Align Generic Guidance | Update Coordinator/Implement guidance and packaged host copies for the generic preflight only. | AC1, AC4, AC5 | Run managed-asset parity and product-source identifier scan. | Done | 1, 2, 3 | managed assets, README, tests | No | bounded-return |

## Parent AC Evidence

- AC1, AC2, AC3, AC4, AC9: Generic campaign/state, durable required/not-required classification, exact requirement-to-campaign binding, request-bound adapter, manual path, read-only projection, ledger-bound malformed/stale countercases, generated-host parity, and zero-call incomplete preflight pass in `tests/test_verification_campaign.py`; 492-test regression suite passes.

## Validation Impact

- Baseline proof: Independent QA Changes Requested for TASK-095 on 2026-08-27
- Change summary: Durably bound material-verification authority and exact scope, and added an ordered receipt-ledger identity so a rehashed receipt edit cannot pass unchanged campaign state.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-017 Coordinator
- Change identity: sha256:223981d419d4a104de8fb2f55c9e9dc81eb160a9fd6c832ee6f2f23b521e1ebb

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: current
- Outcome journey evidence: The reviewer accepted deterministic projection, zero-call incomplete preflight, generic adapters, CLI parity and decoupling, but reproduced omission/redefinition and rehashed-receipt counterexamples.
- Reviewer independence: Isolated read-only `codex exec` reviewer session `96524`; it did not author or modify the candidate.
- Evidence: Independent QA transcript `/private/tmp/pw-epic017-qa.txt`; review-time Intent audit identity `sha256:189ad5aeaaba52429ab1adceecac63d56beeb837f824181f7939ff8fe2a4745a`; exact source at `e1f68633`; affected regressions in `tests/test_verification_campaign.py`.
- Findings: High - transient preflight materiality/scope allowed a required campaign to be omitted or redefined. High - receipt integrity was only a recomputable per-receipt self-hash.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: New durable-requirement omission/redefinition and rehashed-ledger countertests pass; 63 affected focused tests and the 492-test full suite pass; all three CLI copies share SHA-256 `ba8c038a...`.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-095
- Title: Define Generic Verification Campaign Contract
- Created: 2026-08-27
