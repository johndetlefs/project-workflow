# Epic Contract

## Summary

- Epic: EPIC-016
- Title: Effective And Proportionate Coordination
- Last updated: 2026-08-24

## Sources of Truth

- Owner meaning and acceptance envelope: `REQUIREMENTS.md`.
- Stable product outcomes and proportionality: `.project-workflow/CONSTITUTION.md`.
- Current intent-integrity baseline: `../EPIC-014-Intent-Integrity-And-Outcome-Proof/`.
- Current post-proof stop baseline: `../FIX-009-Enforce-Proportionate-Post-Proof-Validation/FIX.md`.
- Current execution baseline: `../EPIC-010-Delegate-Execution-Orchestrator/` and
  `../EPIC-012-Capability-Aware-Delegate-Execution-And-Child-Lifecycle/`.
- Current managed execution guidance: `.agents/skills/project-delegate/SKILL.md`,
  `src/project_workflow/prompts/Delegate.prompt.md`, `AGENTS.md`, and `README.md`.
- Sanitized triggering evidence: the owner-observed long-running cross-repository Water Authoring
  Programme and its inspected Project Workflow 0.5.0 installation boundary.

## Invalid Substitutes

- An arbitrary token ceiling, shorter answer, smaller model, fewer tests, or reduced proof offered
  as efficiency.
- More subagents, persistent tasks, or parallel calls offered as efficiency without a named benefit
  and capability-aware overhead decision.
- Renaming Delegate to Coordinator without changing the intake-to-delivery operating model.
- A durable coordination file that copies the canonical execution graph, Delegate packets/returns,
  or worker lifecycle instead of constraining existing lifecycle gates.
- A repository upgrade presented as proof that an already-loaded physical task refreshed its
  instructions and context.
- Static prompt text, template headings, unit tests, or status fields offered as sole proof that
  agent behavior improved.
- The Water task's 0.5.0 failure presented as proof that 0.6.0 intent or stop gates failed.
- Raw host internal-token accounting presented as a bill, credit balance, or portable efficiency
  measure.
- A green implementation that still requires the owner to remember the missing workflow prompts.

## Invariants

- The approved owner outcome and material boundaries remain authoritative across every handoff.
- Exactly one logical Coordinator owns shared workflow state and lifecycle decisions.
- A physical task, subagent, persistent task, peer, or worktree is an execution surface, not a
  second workflow authority.
- Fresh contexts receive bounded authority and sufficient relevant context; they do not receive
  full history by default and cannot invent scope. A fresh context is optional and must earn its
  transfer cost; explicit loading of current authority can make the same context fit for purpose.
- Context rotation never discards unresolved decisions, evidence, blockers, owner attention, or
  source identity.
- Multi-agent execution is optional and must not be selected when coupling or coordination overhead
  makes one-context execution more effective.
- One independent QA gate remains separate from implementation and Coordinator verification.
- Later changes invalidate only named proof layers through the existing stop gate.
- Requirements rigor, security, source control, evidence, and delivery boundaries are never traded
  away to improve an efficiency metric.
- Unsupported or unobserved host capability remains `unknown` or `unsupported` and fails closed
  where it is binding.

## Artifact Targets

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

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | Constitution And Operating Model | Constitution diff plus smallest-sufficient positive and counter-example checks. |
| AC2 | Coordinator Contract And Compatibility | Managed asset parity, compatibility journeys, and single-writer role tests. |
| AC3 | Requirements Dialogue | Held-out ambiguous and bounded request trials plus approval-burden evidence. |
| AC4 | Contract Preflight And Handoff | Current/stale/loaded-context fixtures and one explicit adoption/handoff result. |
| AC5 | Durable Coordination And Context Boundaries | Multi-phase, cross-repository, and material-reframe journeys proving both justified continuation and justified fresh-context handoff. |
| AC6 | Execution Surface Decision | Coupled, independent, durable, owner-steered, unsupported, and overhead fixtures. |
| AC7 | Existing Delegate Packets And Returns | Schema and orchestration validation plus identity/source/scope/evidence reconciliation failures without a second packet ledger. |
| AC8 | Early Real-Outcome Checkpoint | Wrong-product rejection before fan-out and bounded-task counter-fixture. |
| AC9 | QA And Stop Integration | Existing and new stop-gate regressions proving no recursive QA. |
| AC10 | Operational Projection | Status/Doctor human and JSON checks over inspectable coordination state. |
| AC11 | Behavioural Scenario Coverage | Sanitized nine-scenario corpus with under- and over-processing verdicts. |
| AC12 | Effectiveness Proof | Repeated eval and disposable journey comparison with scoped effort telemetry. |
| AC13 | Packaging And Delivery | Full suite, parity, exact artifacts, fresh/upgrade journeys, and delivery receipt. |
| AC14 | Five-Boundary Drift Control | Water-style narrowing/proxy/broadening injections, branch blocking, and exact amendment refresh. |
| AC15 | Clarify Fitness | Held-out Task/Epic/pre-plan/post-plan/mid-Epic scenarios and smallest evidence-backed disposition. |
