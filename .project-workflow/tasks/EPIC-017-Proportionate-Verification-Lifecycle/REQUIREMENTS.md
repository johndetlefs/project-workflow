# Requirements

## Summary

- Task: EPIC-017
- Title: Proportionate Verification Lifecycle
- Last updated: 2026-08-27
- Proposal state: Owner-approved direction; artifact approval pending
- Intent contract: full

## Intent

Make Project Workflow obtain sufficient truthful proof without allowing verification to become an
unbounded implementation, diagnostic, QA, or release loop. Extend the existing 0.7.0 Coordinator
with progressive, cost-bounded verification while keeping every verifier and consumer optional and
independently usable.

## Intent Spine

- OC1 — Completion capability: one Coordinator can take an exact candidate from implementation
  through proportionate verification, one independent QA gate, and delivery; blocking failures stop
  and replan, current proof is reused, and an unchanged proven candidate is delivered without
  reopening validation or review.
- OC2 — Material capabilities: exact candidate identity; a compact verification campaign;
  claim-to-proof stages; deterministic operational projection; certification versus diagnostic
  modes; campaign limits that pause rather than waive proof; input-bound receipts; affected proof
  reuse; typed product/evaluator/provider/harness outcomes; optional verifier adapters; one-QA
  integration; and sanitized behavioural evidence.
- OC3 — Success journey: a release request for an incomplete candidate reports
  `implementation-required` and visible verification scope; after completion, deterministic checks
  and canaries precede affected and full certification; a blocking canary prevents the full
  campaign; a corrected candidate reaches one planned full certification and one QA; an
  evaluator-only change regrades retained outputs; the unchanged green candidate then delivers.
- OC4 — Successful-but-wrong result: Project Workflow adds persuasive guidance or status fields
  while an expensive verifier can still start without a current candidate/plan, continue after a
  blocking failure, restart completed work, rerun targets after evaluator-only change, commission a
  second QA, skip required proof because a limit was reached, or require one named consumer at
  runtime.
- OC5 — Exclusions: no arbitrary universal token target; no reduction of required proof; no second
  workflow lifecycle, tracker, QA scheduler, or generalized verification platform; no mandatory
  adapter; no Project Workflow dependency in a verifier; no verifier/product dependency inside
  Project Workflow; and no Strategic Advisor-specific product source, schema, prompt, or runtime
  branch in Project Workflow.
- OC6 — Assumptions: verifier cost and resumability vary; missing cost history can be estimated by a
  bounded canary; unknown material impact safely expands proof; stochastic proof may contain a
  predeclared repeated sample; and campaign limits stop or escalate work but never manufacture a
  passing verdict.
- OC7 — Authority source: owner direction in the current Codex task on 2026-08-27, the inspected
  Strategic Advisor alpha.6 release incident, and current Project Workflow 0.7.0 source at
  `e1f68633b71f729d199208c850d3b0de2f737505`.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-27
- Approval note / source: Codex owner direction 2026-08-27: approved the complete proportionate-verification implementation provided Project Workflow and Strategic Advisor remain optional and uncoupled.
- Approved artifact identity: sha256:14011fe714b8e9e1575c1fb3011fe2949d35b7c8189bd1e8e45495c6c42dd4f8

## Goal

Close the pre-proof verification gap left by Project Workflow 0.7.0 without rebuilding its
Coordinator, weakening QA, or coupling the framework to any one verifier. Required assurance must
remain effective; avoidable duplicate work, uncontrolled diagnosis, and repeated target execution
must become mechanically blocked rather than discouraged only by prose.

## Non-Goals

- Do not replace the 0.7.0 Coordinator, coordination state, lifecycle, intent audit, evidence
  recipes, validation-impact decision, or independent QA gate.
- Do not optimize only for low token count, elapsed time, or test count.
- Do not let a cost or time limit turn failed, missing, stale, or unknown proof into a pass.
- Do not require every cheap deterministic test command to create a campaign artifact.
- Do not build adapters for every test framework or consumer in this Epic.
- Do not make Project Workflow import, invoke, identify, or require Strategic Advisor.
- Do not make Strategic Advisor or another verifier require Project Workflow for standalone use.
- Do not claim merge, publication, installation, consumer adoption, or outcome effectiveness from
  repository tests alone.

## Users & Context

- Owners need a release request to reveal the true delivery state and material verification cost
  before expensive work begins.
- Coordinators need deterministic rules for progressing, stopping, diagnosing, reusing proof, and
  escalating a campaign without asking the owner to remember a special prompt.
- Implementers need immediate blocking feedback from the cheapest decisive proof rather than a full
  certification used as late defect discovery.
- Independent reviewers need current proof and a bounded right to request only planned narrow
  validation; QA must not become another campaign scheduler.
- Verifier maintainers need an optional, generic capability/receipt contract that can be satisfied
  without importing Project Workflow.
- Projects that use BMAD, another methodology, or no workflow framework must remain unaffected.

## Repository Scope

- Primary repository: `.` (generic Project Workflow contract, CLI, managed assets, tests, and
  sanitized evidence).
- Optional reference consumer: `/Users/johndetlefs/repos/strategic-advisor` (independent runner
  controls and conformance dogfood on its own branch and repository authority).
- Runtime dependency direction: none. Integration occurs only through optional command-line and
  JSON capability/receipt boundaries.

## Requirements (Outcome-Focused)

- R1 — Extend, rather than duplicate, Project Workflow 0.7.0. The existing Coordinator remains the
  only owner-facing role and shared-state writer; existing lifecycle and QA states remain
  authoritative.
- R2 — Add one compact current verification-campaign record for materially expensive proof. It
  records candidate identity, approved claims/proof obligations, campaign mode, ordered stages,
  selected/affected scope, declared limits, current outcome, next action, and references to
  evidence receipts. It must not copy full runner output or create another execution graph.
- R3 — Derive one operational projection from existing lifecycle plus current campaign evidence:
  `implementation-required`, `verification-required`, `qa-required`, `delivery-ready`, or
  `blocked`. Projection is read-only truth, not another mutable status.
- R4 — Stage material verification from the cheapest decisive evidence to the most expensive:
  deterministic/unit checks; new, changed, high-risk, and previously failing canaries; affected
  cases; one planned full certification campaign; one independent QA gate; and delivery/artifact
  verification. A later stage cannot start after an earlier blocking failure.
- R5 — Separate `certification` from `diagnostic` mode. Certification stops at the first blocking
  product failure. Diagnostic continuation requires a named information need, bounded selected
  scope, and declared limits; diagnostic output cannot satisfy release certification by itself.
- R6 — Campaign limits cover relevant observable units such as case/failure count, target calls, or
  elapsed time using known suite size/history or a bounded estimate. Reaching a limit pauses or
  blocks with the missing proof and next decision; it never waives required assurance or silently
  expands work.
- R7 — Bind every proof receipt to only the inputs that determine its validity: candidate/source,
  proof/case contract, runtime/model/host configuration, target output, evaluator, and artifact as
  applicable. Source changes create a new candidate; evaluator-only changes regrade retained
  outputs; provider/harness interruptions resume or retry within the plan; unknown impact safely
  expands proof.
- R8 — Classify outcomes as product/assertion failure, evaluator failure, provider failure, harness
  failure, or pass. Failure class controls retry, reuse, return-to-implementation, and escalation;
  infrastructure recovery must not disguise a product retry.
- R9 — Define a framework-neutral optional verifier-adapter contract for capabilities, invocation,
  checkpoint/resume, selection, limits, and receipt output. Project Workflow must operate safely
  when no adapter exists by using declared manual commands or blocking an unsupported required
  control; it must contain no consumer-specific runtime branch.
- R10 — Preserve one independent QA verdict. QA may run planned narrow validation but cannot start,
  broaden, or restart a materially expensive campaign. Missing expensive proof returns to the
  Coordinator as `verification-required`; findings close through the existing affected-validation
  disposition without a second QA.
- R11 — Keep local CLI, packaged source, managed host guidance, templates, README, Doctor/status,
  schemas, and tests aligned. Static guidance alone is invalid proof of changed behavior.
- R12 — Add sanitized behavioural scenarios for release-request preflight, canary-first blocking,
  certification/diagnostic separation, budget pause, candidate invalidation, evaluator-only
  regrade, infrastructure resume, one-QA closure, unchanged-green delivery, unknown-impact fallback,
  and cheap-task countercases.
- R13 — Prove the complete generic journey in a disposable repository using a fake controllable
  verifier. Assert actual invocation counts and receipt identities so prose or status-only
  implementations cannot pass.
- R14 — Independently add the required selection, fail-fast, limits, typed outcome, checkpoint,
  telemetry, and regrade controls to the Strategic Advisor live evaluation runner. The runner must
  remain usable without Project Workflow and expose only the generic optional adapter boundary when
  the two are combined.
- R15 — Dogfood the optional combination against a sanitized form of the alpha.6 incident. Keep
  implemented, validated, QA-passed, merged, released, installed, adopted, and effective claims
  separate; do not roll out to other consumers without separate current evidence and authority.

## Acceptance Criteria (Verifiable)

- AC1: Current 0.7.0 Coordinator/lifecycle/QA authority remains singular; no second mutable
  lifecycle, tracker, QA scheduler, or copied execution graph is introduced.
- AC2: A valid compact campaign records exact candidate, mode, claims, ordered stages, affected
  scope, limits, receipt references, current outcome, and next action; malformed, stale, or
  source-mismatched campaigns fail closed.
- AC3: Status deterministically reports exactly one of `implementation-required`,
  `verification-required`, `qa-required`, `delivery-ready`, or `blocked` from inspectable evidence
  and never initiates work.
- AC4: A fixture with incomplete implementation and a release request reports
  `implementation-required`, including the required campaign scope, without invoking the verifier.
- AC5: A blocking deterministic or canary result prevents affected/full certification. In
  certification mode, target invocations after the first blocking product failure are zero.
- AC6: Diagnostic continuation is rejected unless it names the decision enabled, selected scope,
  and limits. A valid diagnostic campaign remains non-certifying and stops at its declared boundary.
- AC7: Limits pause/block rather than pass. Required proof remains visibly missing, and resumption
  or scope expansion requires a current campaign decision rather than an automatic loop.
- AC8: Receipt currentness is input-specific: product changes invalidate affected target proof;
  evaluator-only change causes zero new target calls; provider/harness interruption resumes; and
  unknown material impact falls back to full required proof.
- AC9: The generic adapter schema and tests contain no Strategic Advisor identifier, repository
  path, import, prompt, case name, or runtime dependency. A no-adapter/manual verifier fixture and a
  fake adapter fixture both operate safely.
- AC10: Exactly one independent QA verdict is retained. QA cannot broaden an expensive campaign;
  one affected validation resolves findings, and an unchanged passing candidate cannot commission
  another QA.
- AC11: Generated/project-local host assets and packaged source remain byte/behavior aligned, and
  Doctor/status identify missing or stale campaign evidence without turning accepted historical
  work into false current failures.
- AC12: Sanitized behavioural and deterministic coverage exercises every R12 failure and
  counter-failure, including a cheap bounded task that incurs no campaign ceremony.
- AC13: A disposable fake-verifier journey proves invocation counts: zero full calls after canary
  failure, one planned full campaign for the corrected candidate, zero target calls for evaluator
  regrade, one QA, and no new verification for unchanged delivery.
- AC14: The Strategic Advisor runner supports case/metadata selection, previously failing/affected
  scope, fail-fast/max-failures, target-call and elapsed limits, content-addressed resume,
  per-case/call telemetry, typed outcomes, bounded infrastructure retry, and transcript-only
  regrade while remaining standalone.
- AC15: The sanitized reference-consumer dogfood follows the AC4/AC5/AC8/AC10/AC13 sequence and
  records the optional integration boundary. Project Workflow package/source tests prove no
  consumer-specific product coupling.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose | Dependencies |
| --- | --- | --- | --- |
| Define Generic Verification Campaign Contract | AC1, AC2, AC3, AC4, AC9 | Extend the Coordinator with the compact generic campaign, derived operational projection, optional adapter boundary, and decoupling invariants. |  |
| Enforce Progressive Verification And QA Boundaries | AC5, AC6, AC7, AC8, AC10, AC11 | Implement progressive stage gates, certification/diagnostic separation, limits, receipt currentness, typed outcomes, QA routing, managed assets, and deterministic tests. | TASK-095 |
| Add Standalone Reference-Consumer Runner Controls | AC9, AC14 | Upgrade the reference consumer to current Project Workflow guidance on its own branch and add standalone runner controls plus optional generic capability/receipt output without either product importing the other. | TASK-095, TASK-096 |
| Prove Generic And Optional-Consumer Journeys | AC4, AC5, AC8, AC10, AC11, AC12, AC13, AC15 | Run sanitized behavioural fixtures, a disposable fake-verifier journey, optional consumer dogfood, one independent QA per child, and exact package/repository validation; retain delivery and rollout boundaries. | TASK-095, TASK-096, TASK-097 |

## Outcome Commitment Coverage

| Commitment | Child Owners | Parent ACs | Required Disposition |
| --- | --- | --- | --- |
| OC1 — Bounded path from candidate to delivery | TASK-095, TASK-096, TASK-098 | AC1-AC8, AC10-AC13 | Generic campaign, gates, proof reuse, one QA, and delivery journey implemented and proven. |
| OC2 — Material verification capabilities | TASK-095, TASK-096, TASK-097, TASK-098 | AC1-AC15 | Every capability implemented generically, supplied by the optional consumer, or proven through a counter-fixture. |
| OC3 — Complete successful journey | TASK-095, TASK-096, TASK-098 | AC3-AC13, AC15 | Disposable and dogfood journeys prove preflight, failure stop, correction, certification, QA, regrade, and delivery. |
| OC4 — Reject persuasive but unbounded verification | TASK-096, TASK-098 | AC4-AC13, AC15 | Invocation-count and lifecycle evidence rejects prose-only, status-only, repeated-run, second-QA, and proof-waiver candidates. |
| OC5 — Preserve quality and decoupling | TASK-095, TASK-096, TASK-097, TASK-098 | AC1, AC5-AC15 | Counter-fixtures retain full proof when required and both products operate independently. |
| OC6 — Honest unknowns and campaign limits | TASK-095, TASK-096, TASK-097 | AC2, AC3, AC6-AC9, AC14 | Missing cost/impact/capability remains visible, bounds pause rather than pass, and unknown material impact expands safely. |
| OC7 — Current owner and source authority | TASK-095, TASK-098 | AC1-AC4, AC11-AC15 | Approval, candidate, proof, QA, package, and optional-consumer evidence remain source-bound and inspectable. |

## Delivery Sequence

1. Define the generic campaign and derived state on current 0.7.0 without changing its lifecycle.
2. Enforce progressive stages, failure modes, limits, proof reuse, and one-QA routing in Project
   Workflow with fake/manual verifier coverage.
3. Independently upgrade and change the reference-consumer runner; preserve standalone operation
   and expose only the optional generic boundary.
4. Run the exact sanitized journeys, package/repository validation, and independent QA. Stop before
   merge, publication, installation, or wider rollout unless separately authorized by current
   delivery evidence.

## Open Questions (Answer Needed)

- None. The owner confirmed the architecture, required a strict no-coupling boundary, and approved
  the complete implementation envelope in the current Codex task on 2026-08-27.

## Decisions (Resolved)

- The feature is a proportionate verification lifecycle, not a narrower anti-QA-loop patch.
- Project Workflow owns only a generic optional campaign/adapter contract.
- Strategic Advisor is an independent reference consumer and remains standalone.
- BMAD-only, other-methodology, and no-Project-Workflow projects are unaffected.
- The 0.7.0 Coordinator, one-QA verdict, validation-impact decision, and lifecycle are extended, not
  replaced.
- Operational projection is derived evidence, not a second mutable status.
- Campaign limits stop/escalate work and never reduce required assurance.
- Certification fails fast; extended failure collection is an explicitly bounded diagnostic mode.
- Input-specific receipts replace a generalized global proof-dependency graph.
- Unknown material impact safely requires broader proof.
- Delivery authority in this approval covers requirements, planning, implementation, validation,
  independent QA, and local closeout evidence; push, merge, package publication, installation, and
  rollout remain separate external actions.

## Validation Plan

- Run focused campaign/schema/status/Doctor tests and the exact fail/counter-fail matrix.
- Run the disposable fake-verifier journey and assert real invocation/receipt counts.
- Run the full locked Project Workflow suite once after the generic candidate is frozen.
- Validate packaged managed-asset parity and fresh/upgrade journeys when source changes require it.
- In the reference consumer, run focused runner-unit tests, checkpoint/resume and transcript-regrade
  fixtures, its repository validation, and the sanitized optional-integration dogfood.
- Run one independent adversarial QA verdict per child, close findings through affected validation,
  generate the Epic intent/acceptance audits, and retain explicit delivery boundaries.
