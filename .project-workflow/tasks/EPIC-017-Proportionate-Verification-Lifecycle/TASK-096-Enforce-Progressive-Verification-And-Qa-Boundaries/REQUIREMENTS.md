# Requirements

## Summary

- Task: TASK-096
- Title: Enforce Progressive Verification And QA Boundaries
- Parent AC Coverage: AC5, AC6, AC7, AC8, AC10, AC11
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Make materially expensive verification progress from cheap decisive proof to full certification,
stop/replan on blocking failure, reuse only current proof, and preserve one independent QA without
allowing a limit to waive assurance.

## Intent Spine

- OC1 — Completion capability: the Coordinator enforces ordered verification stages, typed failure
  transitions, bounded certification/diagnostic modes, current receipts, and one-QA closeout.
- OC2 — Material capabilities: stage prerequisites; fail-fast certification; bounded diagnostic
  mode; case/failure/call/time limits; typed product/evaluator/provider/harness outcomes;
  input-specific invalidation; resume/retry/regrade decisions; and QA routing.
- OC3 — Success journey: deterministic/canary failure blocks later stages; a corrected candidate
  passes affected then planned full certification; one QA closes; evaluator-only change regrades
  without target execution; unchanged proof advances to delivery.
- OC4 — Successful-but-wrong result: runner activity continues after a blocking failure, a limit
  produces pass, stale output is reused, infrastructure retry hides a product retry, or QA starts a
  new campaign.
- OC5 — Exclusions: no concrete verifier adapter, reference-consumer runner, second QA, release, or
  generic scheduling platform in this child.
- OC6 — Assumptions: the child consumes TASK-095's generic contract; stochastic repeated samples
  are predeclared inside one campaign; unknown impact expands proof.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

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

## Goal

Turn campaign intent into deterministic continuation authorization so expensive work cannot expand
or repeat without a current reason, boundary, and valid proof identity.

## Non-Goals

- No concrete consumer or test-framework dependency.
- No reduction of required proof after a limit or failure.
- No second lifecycle or QA verdict.
- No package publication or external rollout.

## Users & Context

- Coordinators deciding whether a verifier may start, continue, resume, regrade, or stop.
- Reviewers requiring current proof without becoming campaign schedulers.
- Owners protected from automatic diagnostic expansion after a certification failure.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Enforce ordered stages: deterministic, canary, affected, full certification, QA, delivery.
- R2 — In certification mode, the first blocking product/assertion failure terminates authorization
  for remaining target work and returns to implementation.
- R3 — Diagnostic mode requires a decision enabled, selected scope, and at least one finite
  observable limit; it remains non-certifying.
- R4 — Limit exhaustion produces paused/blocked state with required proof still missing. Resumption
  or expansion requires a current bounded campaign update.
- R5 — Type pass/product/evaluator/provider/harness outcomes and authorize only the matching
  retry/resume/regrade/invalidation path.
- R6 — Evaluate receipt currentness by applicable inputs and safely expand unknown material impact.
- R7 — QA may run only planned narrow validation; missing or broad expensive proof returns
  `verification-required`; findings close through one affected validation and never commission a
  second QA.
- R8 — Align CLI, templates, managed guidance, status/Doctor and deterministic tests.

## Acceptance Criteria (Verifiable)

- AC1: Failed deterministic/canary stages prevent affected/full authorization; certification
  records zero target invocations after its first blocking product failure. Covers parent AC5.
- AC2: Invalid diagnostic campaigns are rejected; valid diagnostic campaigns remain non-certifying
  and stop at selected scope/limits. Covers parent AC6.
- AC3: Every supported limit exhaustion remains non-passing and exposes missing proof plus the
  required bounded resumption/decision. Covers parent AC7.
- AC4: Product/evaluator/provider/harness fixtures invalidate, regrade, resume/retry, or block only
  the applicable inputs; unknown material impact expands to full required proof. Covers parent AC8.
- AC5: One retained independent QA closes through one affected validation; QA cannot broaden a
  campaign and unchanged green state cannot commission another QA. Covers parent AC10.
- AC6: Local/package/generated assets, status and Doctor remain aligned and preserve accepted
  historical states while failing current malformed/stale campaigns. Covers parent AC11.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Certification and diagnosis are different modes with different authority.
- A campaign limit pauses rather than passes.
- Retry is failure-type-specific.
- One QA verdict remains the only independent review authority.

## Validation Plan

- Focused stage/failure/limit/currentness/QA tests with actual fake invocation counters.
- Managed/package parity and current/historical Doctor/status counter-tests.
- Full locked Project Workflow suite only after this generic candidate is frozen.
