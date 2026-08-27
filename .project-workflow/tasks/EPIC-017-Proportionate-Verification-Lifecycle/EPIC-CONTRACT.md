# Epic Contract

## Summary

- Epic: EPIC-017
- Title: Proportionate Verification Lifecycle
- Last updated: 2026-08-27

## Sources of Truth

- Owner meaning and decoupling boundary: `REQUIREMENTS.md` and the current Codex task.
- Current coordination/lifecycle foundation: `../EPIC-016-Effective-And-Proportionate-Coordination/`.
- Current post-proof stop foundation: `../FIX-009-Enforce-Proportionate-Post-Proof-Validation/`.
- Stable product outcomes: `.project-workflow/CONSTITUTION.md`.
- Generic implementation authority: current Project Workflow source at
  `e1f68633b71f729d199208c850d3b0de2f737505` plus this Epic's approved decomposition.
- Triggering evidence class: the sanitized incomplete-candidate, expensive-certification,
  product-failure, evaluator-regrade, and release journey defined by AC4, AC5, AC8, AC10, AC13,
  and AC15; no private transcript is a package dependency.

## Invalid Substitutes

- Another instruction saying to avoid unnecessary QA without executable stage/failure controls.
- Installing Project Workflow 0.7.0 without adding the missing pre-proof campaign capability.
- Adding only reference-consumer runner flags while Project Workflow still cannot govern costly
  verification.
- Adding a second lifecycle, tracker, review scheduler, execution graph, or generalized platform.
- Treating a release request as authority to silently implement or launch unbounded certification.
- Treating a canary, subset, diagnostic run, stale receipt, or QA prose as complete certification.
- Treating a cost/time limit as evidence that missing or failed proof passed.
- Rerunning target execution after an evaluator-only change when retained outputs are current.
- Static schemas, prompts, status text, or mocked decisions without actual invocation-count proof.
- Any Project Workflow runtime branch, import, schema field, prompt, fixture identifier, or package
  dependency that names or requires Strategic Advisor.
- Any reference-consumer change that makes its standalone runner depend on Project Workflow.

## Invariants

- One 0.7.0 Coordinator and the existing lifecycle remain authoritative.
- Operational verification state is derived from inspectable evidence and never performs work.
- Every materially expensive campaign is bound to one exact candidate, proof contract, mode,
  ordered stages, limits, and current receipts.
- Required assurance is never traded away for lower usage, elapsed time, or ceremony.
- Certification stops at a blocking product failure; extended investigation is a separate bounded
  diagnostic decision.
- Later stages never run after an earlier blocking stage.
- Proof reuse is input-specific; unknown material impact fails safely toward broader proof.
- One independent QA verdict remains separate from implementation and Coordinator verification.
- Neither Project Workflow nor a verifier requires the other. Optional compatibility is expressed
  only through a generic command/JSON boundary.
- Product-specific dogfood evidence is sanitized before it becomes generic package behavior.
- Merge, release, installation, adoption, owner acceptance, and effectiveness remain separate proof
  gates and authorities.

## Artifact Targets

- Generic campaign schema/state and deterministic operational projection integrated with existing
  Coordinator/status/Doctor surfaces.
- Progressive stage, failure-mode, campaign-limit, currentness, resume, and one-QA enforcement.
- Framework-neutral optional verifier capability and receipt contract plus manual/no-adapter path.
- Aligned local CLI, package source, templates, Codex/Claude/Copilot/Cursor guidance, README, and
  validation assets.
- Sanitized behavioural corpus and disposable fake-verifier journey with invocation-count receipts.
- Independent reference-consumer branch with standalone runner controls and optional generic output.
- Sanitized optional-combination dogfood receipt and explicit package/repository/delivery boundary.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-095, TASK-096 | Architecture/source inspection and regressions proving one Coordinator/lifecycle and no copied graph. |
| AC2 | TASK-095, TASK-096 | Campaign schema/currentness tests plus malformed/stale/source-mismatch failures. |
| AC3 | TASK-095 | Human/JSON status fixtures deriving each operational result without mutation. |
| AC4 | TASK-095, TASK-098 | Incomplete-candidate release fixture with zero verifier invocations. |
| AC5 | TASK-096, TASK-098 | Deterministic and real fake-verifier invocation counts proving fail-fast stage blocking. |
| AC6 | TASK-096, TASK-098 | Invalid/valid diagnostic campaign fixtures and bounded non-certifying receipts. |
| AC7 | TASK-096, TASK-098 | Limit-hit fixtures showing pause/block with required proof still missing. |
| AC8 | TASK-096, TASK-097, TASK-098 | Product/evaluator/provider/harness currentness, retry, resume, regrade, and fallback receipts. |
| AC9 | TASK-095, TASK-097, TASK-098 | Generic source scan, no-adapter/manual path, fake adapter, standalone consumer, and optional conformance proof. |
| AC10 | TASK-096, TASK-098 | One retained QA verdict, affected-validation closure, and no campaign expansion or second QA. |
| AC11 | TASK-096, TASK-098 | Managed/package parity, Doctor/status, fresh/upgrade journey, and historical-state counter-tests. |
| AC12 | TASK-098 | Complete sanitized failure/counter-failure behavioural matrix. |
| AC13 | TASK-098 | Disposable fake-verifier journey with exact target/full/QA/regrade/delivery counts. |
| AC14 | TASK-097 | Standalone reference-consumer runner tests, validation, checkpoints, telemetry, and generic optional output. |
| AC15 | TASK-097, TASK-098 | Sanitized optional-combination journey and package/source no-coupling proof. |
