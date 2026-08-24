# Requirements

## Summary

- Task: TASK-091
- Title: Build Durable Coordination Handoff And Drift Controls
- Parent AC Coverage: AC4, AC5, AC7, AC10, AC14
- Last updated: 2026-08-24
- Intent contract: full

## Intent

Give the logical Coordinator durable, inspectable state that survives physical task changes, and
make every material handoff, contract check, and drift decision fail closed against the approved
Intent through existing lifecycle and Delegate gates before affected work continues.

## Intent Spine

- OC1 — Completion capability: a successor Coordinator context can resume exact authorized work
  from durable state without receiving the complete prior conversation.
- OC2 — Material capabilities: compact logical coordination state, current-contract preflight,
  existing Delegate packets and verified returns, five source-bound drift decisions enforced by
  lifecycle gates, early-checkpoint blocking, and sourced status/Doctor projection.
- OC3 — Success journey: current work proceeds; stale loaded guidance requests one explicit load or
  handoff; the same context continues when fit or a fresh context resumes from bounded authority;
  Delegate verifies its return; Water-style drift blocks the affected transition; and status
  reports one next action.
- OC4 — Successful-but-wrong result: a repository upgrade is treated as a refreshed task context,
  a worker return self-certifies completion, or a drift record exists but descendants still start.
- OC5 — Exclusions: no executor optimization, early product proof policy, behavioural reliability
  claim, task creation, publication, rollout, or billing telemetry system.
- OC6 — Assumptions: the repository is durable authority; host task/context state may be unknown;
  semantic classification is reviewable while identity, coverage and lifecycle are deterministic.
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
- Fresh contexts receive bounded authority and sufficient relevant context; they do not receive full history by default and cannot invent scope.
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
- A coordination document that copies the canonical execution graph, Delegate packets/returns, or
  worker lifecycle instead of constraining existing lifecycle gates.
- A repository upgrade presented as proof that an already-loaded physical task refreshed its instructions and context.
- Static prompt text, template headings, unit tests, or status fields offered as sole proof that agent behavior improved.
- The Water task's 0.5.0 failure presented as proof that 0.6.0 intent or stop gates failed.
- Raw host internal-token accounting presented as a bill, credit balance, or portable efficiency measure.
- A green implementation that still requires the owner to remember the missing workflow prompts.

### Artifact Targets

- Updated Constitution, AGENTS guidance, README, and host-managed Coordinator assets.
- Coordinator role contract and a tested compatibility path from `project-delegate`.
- Current-contract preflight and stale-task adoption/handoff decision.
- Compact logical coordination state plus enriched existing Delegate packet and return contracts.
- Capability-aware execution-surface decision with explicit benefit and overhead basis.
- Proportionate early real-outcome checkpoint integrated with intent and proof rules.
- Five-boundary drift-decision contract using current intent and amendment authority.
- Evidence-backed Clarify fitness assessment and the smallest correction, if any.
- Status/Doctor projections for deterministic coordination and handoff state.
- Sanitized behavioural scenario corpus and repeated agent-evaluation report.
- Disposable end-to-end journey and EPIC-016 dogfood receipts.
- Exact package candidate, parity receipts, release evidence, and separate rollout disposition.

### Parent AC Proof Ownership

- AC4: owner `Contract Preflight And Handoff`; required evidence: Current/stale/loaded-context fixtures and one explicit adoption/handoff result.
- AC5: owner `Durable Coordination And Context Boundaries`; required evidence: Multi-phase, cross-repository, and material-reframe journeys proving justified continuation and justified fresh-context handoff.
- AC7: owner `Existing Delegate Packets And Returns`; required evidence: Schema and orchestration validation plus identity/source/scope/evidence reconciliation failures without a second packet ledger.
- AC10: owner `Operational Projection`; required evidence: Status/Doctor human and JSON checks over inspectable coordination state.
- AC14: owner `Five-Boundary Drift Control`; required evidence: Water-style narrowing/proxy/broadening injections, branch blocking, and exact amendment refresh.

## Goal

Make coordination continuity and drift control executable rather than dependent on a long-running
chat remembering what happened.

## Non-Goals

- No automatic task or subagent creation.
- No assumption that a file upgrade refreshes already-loaded instructions.
- No periodic drift review or duplicate intent ledger.
- No QA scheduling from handoff, return, reconciliation or drift state.
- No context split merely because a task is old or long.

## Users & Context

- Coordinators moving across phases, repositories, physical tasks or material reframes.
- Workers receiving bounded authority and returning evidence.
- Owners who need one next action and one focused question only when a material decision is unclear.
- Maintainers inspecting stale, returned-but-unverified or drift-blocked work.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Add one schema-versioned coordination state per Task/Epic recording only target, approved
  contract and intent identity, phase, repository/source identities, material decisions, context
  declaration, five boundary decisions, one outcome checkpoint, next action and host-observed
  facts. The canonical plan and Delegate remain the sole owners of units, dependencies, packets,
  returns, evidence, and worker lifecycle.
- R2 — Record the Project Workflow package/asset/contract identity loaded by a Coordinator. Current
  compatible state proceeds; a materially stale or unknown loaded contract produces a single
  adoption/handoff action. Repository upgrade alone cannot mark physical context refreshed.
- R3 — Enrich the existing Delegate work packets with exact authority source/hash, relevant OCs/ACs,
  allowed scope, dependencies, proof, invalid substitutes, stop conditions, and an explicit return
  contract. Prevent workers from mutating shared coordination/workflow state.
- R4 — Keep return verification in the existing Task/Epic Delegate orchestrators. Coordinator
  verification rejects missing, stale or mismatched identity, source, attempt, scope, diff,
  validation, evidence, or dependency state before dependencies are satisfied.
- R5 — Record exactly the five approved drift boundaries with `inside-envelope`, `drift-detected`
  or `approved-change`. Drift names relevant OCs, lost/broadened capability, user consequence and
  affected work; approved change requires amendment identity and refreshes the canonical plan and
  affected Delegate packets; an inside decision advances without owner interruption.
- R6 — Enforce the current boundary decision and early checkpoint at existing Task/Epic lifecycle
  transitions. Existing Delegate dependency/return rules continue to block descendants and allow
  unrelated branches only while shared premises remain valid.
- R7 — Project status and Doctor surface current/stale contract, phase, last boundary, checkpoint,
  host fact uncertainty and one sourced next action without executing it. Delegate status remains
  the execution/return projection.

## Acceptance Criteria (Verifiable)

- AC1: Current/compatible, stale, unknown and repository-upgraded-but-context-stale fixtures produce
  the correct proceed or single handoff action. Covers parent AC4.
- AC2: A multi-phase and cross-repository journey either continues in an explicitly current context
  or resumes in a fresh one from exact source, decisions, canonical-plan/Delegate references, next
  action and stop condition, without full history or a copied execution graph.
  Covers parent AC5.
- AC3: Existing Delegate packet and return validation rejects missing authority, relevant OCs/ACs,
  source, scope, dependencies, proof, stop condition, identity, diff or evidence. Covers parent AC7.
- AC4: Existing Delegate reconciliation alone satisfies dependencies and rejects stale, mismatched,
  duplicate, orphaned or self-certified returns; `coordinate` exposes no second packet or reconcile
  command. Covers parent AC7.
- AC5: Each of the five drift boundaries passes inside-envelope work, blocks Water-style
  narrowing/proxy/broadening before descendants, and refreshes exact affected packets after a valid
  amendment without creating QA. Covers parent AC14.
- AC6: Existing lifecycle transitions cannot bypass missing, stale or drifted decisions or a failed
  checkpoint; Delegate descendant blocking and unrelated-branch continuation remain green.
  Covers parent AC14.
- AC7: Human and JSON status plus Doctor report only sourced coordination facts and one next action;
  missing host context/telemetry remains unknown. Covers parent AC10.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use one compact logical coordination state and the existing Delegate packet/return graph, not a
  second execution state or document stack.
- Boundary decisions reuse approved Intent, intent audit and amendment authority.
- The Coordinator is the only writer; workers return evidence but never advance canonical state.
- Context currency is explicitly declared after loading, not inferred from repository version or
  falsely claimed as physically proven freshness.

## Validation Plan

- Add schema/parser/command tests for compact state, Delegate packet enrichment and drift decisions.
- Run current/stale/unknown and repository-upgrade context fixtures.
- Run same-context, fresh-context, multi-phase, cross-repository, material-reframe and Water-style
  lifecycle-blocking journeys.
- Verify human/JSON status and Doctor projections, managed CLI parity, strict Doctor and diff hygiene.
