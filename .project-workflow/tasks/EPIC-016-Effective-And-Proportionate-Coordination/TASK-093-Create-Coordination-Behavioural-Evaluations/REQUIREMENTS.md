# Requirements

## Summary

- Task: TASK-093
- Title: Create Coordination Behavioural Evaluations
- Parent AC Coverage: AC11, AC12, AC14, AC15
- Last updated: 2026-08-24
- Intent contract: full

## Intent

Prove through sanitized repeated behaviour—not prompt presence—that the Coordinator, Clarify,
handoff, drift, executor, early-outcome and stop controls improve real delivery while avoiding both
undercooking and unnecessary process.

## Intent Spine

- OC1 — Completion capability: maintainers can compare the candidate with the retained baseline on
  outcome fidelity, drift timing, rework, duplicate actions, owner interruptions and scoped effort.
- OC2 — Material capabilities: sanitized corpus, held-out trials, objective graders, Clarify matrix,
  Water drift sequence, topology counter-cases, stop behavior, false-pass analysis and provenance.
- OC3 — Success journey: repeated trials preserve intent, choose proportionate context topology,
  reject proxy drift early, ask only material questions, stop after sufficient proof and expose
  honest limitations.
- OC4 — Successful-but-wrong result: static tests pass or one curated run succeeds while held-out
  trials still over-fan-out, miss drift, repeat review or reduce necessary proof.
- OC5 — Exclusions: no claim of universal model reliability, billing savings, commercial value,
  publication, consumer rollout, or privacy-sensitive task reproduction.
- OC6 — Assumptions: supported agent harness behavior is variable; evaluation identity and failures
  must be retained; host internal tokens are scoped telemetry rather than billing truth.
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

- The approved owner outcome and material boundaries remain authoritative across every handoff.
- Exactly one logical Coordinator owns shared workflow state and lifecycle decisions.
- A physical task, subagent, persistent task, peer, or worktree is an execution surface, not a second workflow authority.
- Fresh contexts receive bounded authority and sufficient relevant context; they do not receive full history by default and cannot invent scope. A fresh context is optional and must earn its transfer cost; explicit loading of current authority can make the same context fit for purpose.
- Context rotation never discards unresolved decisions, evidence, blockers, owner attention, or source identity.
- Multi-agent execution is optional and must not be selected when coupling or coordination overhead makes one-context execution more effective.
- One independent QA gate remains separate from implementation and Coordinator verification.
- Later changes invalidate only named proof layers through the existing stop gate.
- Requirements rigor, security, source control, evidence, and delivery boundaries are never traded away to improve an efficiency metric.
- Unsupported or unobserved host capability remains `unknown` or `unsupported` and fails closed where it is binding.

### Invalid Substitutes

- An arbitrary token ceiling, shorter answer, smaller model, fewer tests, or reduced proof offered as efficiency.
- More subagents, persistent tasks, or parallel calls offered as efficiency without a named benefit and capability-aware overhead decision.
- Renaming Delegate to Coordinator without changing the intake-to-delivery operating model.
- A coordination document that copies the canonical execution graph, Delegate packets/returns, or worker lifecycle instead of constraining existing lifecycle gates.
- A repository upgrade presented as proof that an already-loaded physical task refreshed its instructions and context.
- Static prompt text, template headings, unit tests, or status fields offered as sole proof that agent behavior improved.
- The Water task's 0.5.0 failure presented as proof that 0.6.0 intent or stop gates failed.
- Raw host internal-token accounting presented as a bill, credit balance, or portable efficiency measure.
- A green implementation that still requires the owner to remember the missing workflow prompts.

### Artifact Targets

- Updated Constitution, AGENTS guidance, README, and host-managed Coordinator assets.
- Coordinator role contract and a tested compatibility path from `project-delegate`.
- Current-contract preflight and stale-task adoption/handoff decision.
- Compact logical coordination state plus enriched existing Delegate packet and verified-return contracts.
- Capability-aware execution-surface decision with explicit benefit and overhead basis.
- Proportionate early real-outcome checkpoint integrated with intent and proof rules.
- Five-boundary drift-decision contract using current intent and amendment authority.
- Evidence-backed Clarify fitness assessment and the smallest correction, if any.
- Status/Doctor projections for deterministic coordination and handoff state.
- Sanitized behavioural scenario corpus and repeated agent-evaluation report.
- Disposable end-to-end journey and EPIC-016 dogfood receipts.
- Exact package candidate, parity receipts, release evidence, and separate rollout disposition.

### Parent AC Proof Ownership

- AC11: owner `Behavioural Scenario Coverage`; required evidence: Sanitized nine-scenario corpus with under- and over-processing verdicts.
- AC12: owner `Effectiveness Proof`; required evidence: Repeated eval and disposable journey comparison with scoped effort telemetry.
- AC14: owner `Five-Boundary Drift Control`; required evidence: Water-style narrowing/proxy/broadening injections, branch blocking, and exact amendment refresh.
- AC15: owner `Clarify Fitness`; required evidence: Held-out Task/Epic/pre-plan/post-plan/mid-Epic scenarios and smallest evidence-backed disposition.

## Goal

Demonstrate that the complete candidate changes agent decisions in the intended direction and does
not merely add more repository ceremony.

## Non-Goals

- No private transcript, absolute personal path or proprietary project fixture.
- No single-run or prompt-snapshot reliability claim.
- No optimization grader that rewards lower effort when the approved outcome or proof is missing.
- No weakening graders after candidate failures without a requirements-level justification.
- No package publication or rollout.

## Users & Context

- Maintainers deciding whether the candidate is effective enough to release.
- Owners exposed to requirement questions, drift correction, handoffs and QA continuation.
- Agents operating across supported managed guidance surfaces.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Create sanitized scenarios for bounded one-context work, independent beneficial fan-out,
  tightly coupled work, stale loaded contract, phase/repository handoff, material owner reframe,
  Water-style proxy drift, unjustified subagent fan-out, passed-proof stopping and all six Clarify
  fitness cases.
- R2 — Include counter-failures proving the workflow does not force context churn, owner questions,
  product checkpoints, maximal scope or skipped proof onto bounded correct work.
- R3 — Run multiple held-out trials or an equivalent behaviorally meaningful harness for supported
  agent guidance. Retain prompt, model, harness, candidate, randomization/trial and grader identity.
- R4 — Grade approved intent preservation, capability coverage, drift boundary/timing, executor
  justification, packet sufficiency, reconciliation, early outcome validity, owner interruptions,
  duplicate work/review, sufficient stopping and unsupported claims.
- R5 — Compare against a retained baseline using useful outcome, late rework, repeated actions and
  available scoped effort telemetry. Do not set or infer a universal token target and do not convert
  internal accounting into credits or billing.
- R6 — Coordinator analysis records false-pass/failure dispositions and corrects the earliest
  owning contract or code without weakening a grader. The one independent QA gate then challenges
  a sample and the retained verdict; this requirement must not create a pre-QA reviewer or a second
  review loop.
- R7 — Publish only sanitized aggregate evidence sufficient to reproduce the evaluation boundary;
  preserve private source observations outside public package artifacts.

## Acceptance Criteria (Verifiable)

- AC1: The corpus contains every R1 failure class and paired counter-cases with no private task
  content or maintainer-only paths. Covers parent AC11.
- AC2: Repeated held-out trials retain exact prompt/model/harness/candidate/trial/grader identity and
  report result variance rather than one chosen run. Covers parent AC12.
- AC3: The Water sequence is blocked at decomposition, child start, return/join, material reframe and
  pre-review/complete injections with the exact user-visible capability consequence. Covers parent
  AC14.
- AC4: Clarify passes pre-approval, clean bounded, post-plan proxy, Epic parent, Epic child and
  mid-Epic ambiguity scenarios without redundant questions or approval/review loops. Covers parent
  AC15.
- AC5: Executor/context cases reject availability-only fan-out and age-only splitting while
  permitting evidenced independent benefit and required durable/isolation needs. Covers parent AC11.
- AC6: Passed-proof trials stop after sufficient proof or one affected validation and never create
  recursive QA. Covers parent AC11 and AC12.
- AC7: Candidate comparison preserves or improves outcome/proof while reducing at least one observed
  source of context replay, duplicate action, late rework or unnecessary owner interruption; scoped
  effort telemetry carries explicit accounting limitations. Covers parent AC12.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Behavioural evidence must test both under-processing and over-processing.
- The Water case is generalized and sanitized; it is not copied into the public package.
- Agent variability is reported, not hidden behind a binary suite result.
- A failing candidate changes the earliest owning implementation or contract, not the approved Intent.

## Validation Plan

- Extend the existing evaluation harness with a schema-validated coordination suite and grader.
- Run repeated baseline and candidate trials over the complete scenario/counter-scenario matrix.
- Retain sanitized inputs/outputs, aggregate report, false-pass analysis and telemetry boundaries.
- Route one sample challenge through the existing independent QA gate; run strict Doctor and diff hygiene.
