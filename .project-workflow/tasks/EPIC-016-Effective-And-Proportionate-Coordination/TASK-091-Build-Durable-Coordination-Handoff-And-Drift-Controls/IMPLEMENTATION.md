## User Story

As a Coordinator, I want durable coordination, handoff and drift state, so that fresh physical
contexts can continue exact work without silently losing intent or trusting worker assertions.

## Parent AC Coverage

- AC4, AC5, AC7, AC10, AC14

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

## Acceptance Criteria

- [x] AC1: Contract preflight distinguishes current, stale, unknown and file-upgraded/context-stale state.
- [x] AC2: Compact handoff state supports justified same-context continuation or fresh-context resume without full history or a copied execution graph.
- [x] AC3: Existing Delegate packet and return schemas fail closed on missing or mismatched authority/evidence.
- [x] AC4: Existing Delegate reconciliation alone satisfies dependencies; `coordinate` has no second packet/reconcile path.
- [x] AC5: Five boundary decisions block Water-style drift or refresh exact amended descendants.
- [x] AC6: Descendant blocking preserves only demonstrably unrelated branches.
- [x] AC7: Status/Doctor expose sourced state and one next action.

## Goal

Implement the durable state and enforcement substrate required by parent AC4, AC5, AC7, AC10 and
AC14 without selecting execution surfaces or claiming behavioural effectiveness.

## Approach

Define the smallest logical-state schema and pure validation first, enrich the existing Delegate
packet/return contract, then enforce deterministic boundary/checkpoint facts through lifecycle,
status and Doctor.

## Phases

1. Define compact coordination and boundary-decision contracts; subtract duplicate execution state.
2. Enforce contract currency through lifecycle while retaining Delegate reconciliation/blocking.
3. Surface state and prove the exact Water-style failure path.

## Validation

- AC1 / parent AC4: version/loaded-context preflight matrix.
- AC2-AC4 / parent AC5, AC7: compact handoff and existing Delegate packet/return journeys.
- AC5-AC6 / parent AC14: five-boundary Water-style drift and dependency graph fixtures.
- AC7 / parent AC10: human/JSON status and Doctor evidence.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/effective-proportionate-coordination` | 113 focused coordination/Clarify/Task+Epic Delegate tests pass after Coordinator Core subtraction and Delegate packet enrichment | Not integrated or released | Compact coordination/lifecycle fixtures, existing Delegate packet/return tests, `DOGFOOD-RECEIPT.md`, and status/Doctor checks |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define Compact Logical State | Keep only phase, authority/source, decisions, context declaration, boundary/checkpoint and next action; remove copied units, packet refs and receipt refs. | AC1, AC2, AC3, AC5 | Run valid/invalid schema and subtraction fixtures. | Done | TASK-090 | CLI/model source and focused tests | No | bounded-return |
| 2 | Enforce Contract Loading And Handoff | Add loaded-contract preflight and allow explicit same-context loading or a justified fresh-context handoff without claiming freshness telemetry. | AC1, AC2 | Exercise current/stale/unknown, same-context and successor-resume journeys. | Done | 1 | CLI, templates, status fixtures | No | bounded-return |
| 3 | Reuse Delegate Packets And Returns | Enrich existing Task/Epic Delegate packets and retain its sole reconciliation/dependency graph; remove `coordinate packet` and `coordinate reconcile`. | AC3, AC4, AC6 | Inject missing/mismatched/stale returns through Delegate tests and reject duplicate coordination commands. | Done | 1, 2 | Delegate orchestration and focused tests | No | bounded-return |
| 4 | Enforce Five Drift Boundaries | Record source-bound inside/drift/amended decisions and make existing lifecycle transitions fail closed before affected continuation. | AC5, AC6 | Run Water-style planning, child-start, return, reframe and closeout injections plus checkpoint blocking. | Done | 1, 2, 3 | intent/lifecycle/coordination CLI and tests | No | bounded-return |
| 5 | Project And Validate State | Add sourced status/Doctor human+JSON output, align CLI mirrors and retain focused evidence. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Inspect projections, run focused tests, strict Doctor and diff checks. | Done | 2, 3, 4 | status/Doctor, mirrors, tests and child evidence | No | bounded-return |

## Parent AC Evidence

- AC4, AC5, AC7, AC10, AC14: deterministic tests cover current/stale/unknown loaded contracts, explicit context declaration, compact state without copied execution data, existing Task/Epic Delegate packet and return authority, all five Water-style source-bound drift decisions, lifecycle/checkpoint blocking, Doctor, and sourced `project status` routing. EPIC-016 dogfood exposed that the first design duplicated Delegate and relied on remembered commands; the Coordinator Core correction removed that layer. `FRESH-CONTEXT-JOURNEY.md` proves one exact bounded successor handoff and records its non-trivial host context counters. The one consolidated QA and affected disposition are retained in `../INDEPENDENT-QA.md`.

## Validation Impact

- Baseline proof: EPIC-016 independent QA Changes Requested 2026-08-24
- Change summary: Bound lifecycle decisions to exact current source identity and added Task and Epic counter-failures.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-016 Coordinator
- Change identity: sha256:d625a62f48053bf1bf0ca25d16fdbb6ea4695e93de2502587054b9570316b607

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: Current
- Outcome journey evidence: Source-bound Task and Epic lifecycle counter-failures now pass
- Reviewer independence: Read-only local agent `/root/task093_eval_review`; not the implementation owner
- Evidence: `../INDEPENDENT-QA.md`; `tests/test_coordination_controls.py`; `tests/test_coordination_subtraction.py`
- Findings: QA found that a decision survived source revision. Fixed by binding every new decision to a hash of current revision and repository authority; affected regressions pass.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Task and Epic lifecycle counter-failures reject stale source-bound decisions; the final combined affected set passes 39/39.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-091
- Title: Build Durable Coordination Handoff And Drift Controls
- Created: 2026-08-24
