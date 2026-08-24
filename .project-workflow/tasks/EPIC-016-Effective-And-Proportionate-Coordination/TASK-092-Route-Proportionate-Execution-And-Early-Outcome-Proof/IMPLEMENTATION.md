## User Story

As a Coordinator, I want execution surfaces and early proof chosen proportionately, so that extra
contexts earn their cost and wrong product directions stop before expensive dependent work.

## Parent AC Coverage

- AC6, AC8, AC9, AC14

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

- AC6: owner `Execution Surface Decision`; required evidence: Coupled, independent, durable, owner-steered, unsupported, and overhead fixtures.
- AC8: owner `Early Real-Outcome Checkpoint`; required evidence: Wrong-product rejection before fan-out and bounded-task counter-fixture.
- AC9: owner `QA And Stop Integration`; required evidence: Existing and new stop-gate regressions proving no recursive QA.
- AC14: owner `Five-Boundary Drift Control`; required evidence: Water-style narrowing/proxy/broadening injections, branch blocking, and exact amendment refresh.

## Acceptance Criteria

- [x] AC1: Subagent availability alone never causes fan-out; named beneficial independent work may use it.
- [x] AC2: Binding persistent/peer/isolation needs remain capability- and authority-safe.
- [x] AC3: Fresh context requires a material boundary plus sufficient handoff, never age alone.
- [x] AC4: Water-style proxy work fails at the earliest normal user journey.
- [x] AC5: Bounded mechanical work avoids unnecessary checkpoints and owner questions.
- [x] AC6: Owner-only evidence routes one focused observation and contradiction to drift.
- [x] AC7: One QA and affected-proof stop behavior remain unchanged.

## Goal

Implement proportionate executor and early-outcome routing for parent AC6, AC8, AC9 and AC14 on top
of TASK-091 durable coordination controls.

## Approach

Make selection justification explicit, retain all existing safety gates, then integrate one
claim-triggered early outcome checkpoint with drift and continuation rather than another review.

## Phases

1. Require earned benefit for non-Coordinator execution.
2. Add proportionate early normal-journey checkpoints.
3. Prove QA/stop compatibility and counter-failures.

## Validation

- AC1-AC3 / parent AC6, AC14: executor and fresh-context decision matrix.
- AC4-AC6 / parent AC8, AC14: Water-style, bounded and owner-only checkpoint journeys.
- AC7 / parent AC9: focused QA and validation-impact regression evidence.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/effective-proportionate-coordination` | Earned-surface, checkpoint and stop regressions passed; prior full suite: 467 passed before affected QA corrections | Not integrated or released | `tests/test_coordination_controls.py`, existing delegation and continuation-sufficiency suites |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Require Earned Execution Benefit | Extend planning/decision inputs and selection so non-Coordinator surfaces require a named benefit/overhead basis. | AC1, AC2 | Run coupled, independent, durable, peer and unsupported selection fixtures. | Done | TASK-090, TASK-091 | planner/delegate assets, execution decision source and tests | No | bounded-return |
| 2 | Route Fresh Context Boundaries | Join phase/repository/reframe/context-pressure reasons to current TASK-091 handoff state and reject age-only splitting. | AC3 | Run bounded successor and insufficient-handoff fixtures. | Done | 1 | coordination/delegation source and tests | No | bounded-return |
| 3 | Add Early Outcome Checkpoint | Trigger existing user-outcome proof at the earliest material product boundary and route contradiction to drift. | AC4, AC5, AC6 | Run Water-style authoring, bounded mechanical and owner-only evidence journeys. | Done | 1, 2 | evidence/lifecycle/guidance source and tests | No | bounded-return |
| 4 | Preserve QA And Stop | Prove handoffs/checkpoints cannot create QA and reuse the one affected-validation stop decision. | AC7 | Run exact QA/validation-impact regression matrix. | Done | 3 | QA/Implement assets, stop-gate source and tests | No | bounded-return |
| 5 | Validate Proportionate Routing | Align managed surfaces and record focused proof without repeating unaffected full-package work. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Review focused receipts, strict Doctor and diff checks. | Done | 1, 2, 3, 4 | managed assets, tests and child evidence | No | bounded-return |

## Parent AC Evidence

- AC6, AC8, AC9, AC14: deterministic tests prove capacity alone defaults to Coordinator, an explicit benefit/overhead/tradeoff permits a verified surface, binding needs still fail closed, material outcome checkpoints block fan-out and owner-only self-certification, and existing one-QA/affected-proof stop regressions remain green. The one consolidated QA issued no TASK-092-specific blocker.

## Validation Impact

- Baseline proof: EPIC-016 independent QA Changes Requested 2026-08-24
- Change summary: Revalidated topology, drift and stopping, then corrected the literal-Pass completion gate so resolved findings close without second QA.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-016 Coordinator
- Change identity: sha256:a21c6934211bbea8d6536bddfc507cb57874c5f87ba9e0552d84edbcf63aeb45

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: Current
- Outcome journey evidence: Existing checkpoint, topology and stop evidence accepted by the reviewer
- Reviewer independence: Read-only local agent `/root/task093_eval_review`; not the implementation owner
- Evidence: `../INDEPENDENT-QA.md`; no TASK-092-specific blocking defect was issued
- Findings: No separate routing/checkpoint blocker; all consolidated QA findings are now resolved through affected validation.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Run 005 retains correct topology, early drift, owner-only judgment and no-recursive-QA decisions; the actual retained-Changes-Requested Review-to-Complete lifecycle passes without second QA; the final affected set passes 39/39.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-092
- Title: Route Proportionate Execution And Early Outcome Proof
- Created: 2026-08-24
