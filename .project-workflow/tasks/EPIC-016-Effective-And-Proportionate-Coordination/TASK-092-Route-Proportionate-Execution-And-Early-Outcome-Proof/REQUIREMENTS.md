# Requirements

## Summary

- Task: TASK-092
- Title: Route Proportionate Execution And Early Outcome Proof
- Parent AC Coverage: AC6, AC8, AC9, AC14
- Last updated: 2026-08-24
- Intent contract: full

## Intent

Make the Coordinator choose a fresh context, subagent, persistent task, peer team, or direct
execution only when that surface is the lightest sufficient way to deliver the approved outcome,
and catch wrong user-facing directions through an early real-outcome checkpoint before fan-out.

## Intent Spine

- OC1 — Completion capability: execution topology and early proof are chosen from work needs and
  named benefit/overhead, not from available agent capacity alone.
- OC2 — Material capabilities: earned surface selection, coordinator default for coupled work,
  explicit fresh-context benefit, collision/dependency safety, early normal-journey checkpoints,
  owner-only judgment routing, and existing QA/stop integration.
- OC3 — Success journey: coupled work stays with one Coordinator; independent work uses a bounded
  fresh context when beneficial; a user-facing proxy fails before dependent polish; one QA runs;
  and post-proof continuation stops.
- OC4 — Successful-but-wrong result: verified capacity automatically launches subagents, or an
  accurate code/test proxy postpones product contradiction until the Epic is nearly complete.
- OC5 — Exclusions: no fixed worker count, universal token score, automatic task creation, durable
  state schema, behavioural reliability claim, publication or rollout.
- OC6 — Assumptions: work metadata and current host capabilities are distinguishable; normal user
  journeys can be named for triggered product classes; taste/feel remains owner-only evidence.
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

- AC6: owner `Execution Surface Decision`; required evidence: Coupled, independent, durable, owner-steered, unsupported, and overhead fixtures.
- AC8: owner `Early Real-Outcome Checkpoint`; required evidence: Wrong-product rejection before fan-out and bounded-task counter-fixture.
- AC9: owner `QA And Stop Integration`; required evidence: Existing and new stop-gate regressions proving no recursive QA.
- AC14: owner `Five-Boundary Drift Control`; required evidence: Water-style narrowing/proxy/broadening injections, branch blocking, and exact amendment refresh.

## Goal

Route effort where it improves delivery and expose outcome mistakes before they create large
downstream rework, while preserving the one-QA and affected-proof stopping rules.

## Non-Goals

- No assumption that parallel execution is efficient merely because it is possible.
- No early product checkpoint for bounded mechanical work without a material user-facing claim.
- No replacement for independent QA or owner acceptance.
- No repeated real-outcome check after an unchanged checkpoint passes.
- No modification of TASK-091 durable state ownership.

## Users & Context

- Coordinators selecting execution surfaces for approved Task rows or Epic children.
- Owners of authoring, visual, migration, replacement and gameplay-feel work where proxies are risky.
- Workers whose bounded packets require either fresh isolation or direct coupled context.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Change bounded-return selection so verified subagent capacity alone never forces fan-out.
  Every non-Coordinator surface records the named benefit, expected setup/synthesis overhead and why
  the benefit outweighs it; absence of that basis uses Coordinator/sequential execution.
- R2 — Preserve binding durable-resume, direct-owner-steering, isolation and peer needs, current
  capability truth, dependency readiness and write-scope collision rules. Named benefit never
  overrides an unmet capability or unsafe shared premise.
- R3 — Support explicit fresh-context benefit for phase, repository, material-reframe or observed
  context-pressure handoffs only when TASK-091 state plus the canonical plan and Delegate packet
  can preserve continuity without copying the execution graph or full history.
- R4 — Trigger the earliest sufficient normal-user-journey checkpoint for material user-facing,
  authoring, visual, gameplay-feel, migration or replacement claims before dependent fan-out or
  expensive polish. Bounded mechanical work remains exempt.
- R5 — A checkpoint records actor, normal entry point, starting state, material operations,
  resulting state/artifact, source/environment, observations and invalid substitutes using the
  existing user-outcome proof contract. Code, tests, builds, hidden data, debug paths and a canary
  cannot satisfy a broader job.
- R6 — Inside-envelope objective checkpoints proceed autonomously. Taste, feel, practical usability
  or material product choices request one owner observation/decision; a contradiction routes to
  TASK-091 drift handling before descendants proceed.
- R7 — One independent QA remains after implementation. Handoffs/checkpoints never create QA;
  unaffected changes stop, affected changes run one named validation, and ambiguity asks one
  focused question under the existing validation-impact gate.

## Acceptance Criteria (Verifiable)

- AC1: Coupled work and bounded work without a named benefit remain Coordinator/sequential even
  when subagent capacity is verified; sufficiently independent work with an evidenced benefit may
  use a bounded subagent. Covers parent AC6.
- AC2: Persistent and peer selections still fail closed on unmet authority, capability, isolation,
  monitoring, reconciliation, retirement, capacity, dependency or write-scope needs. Covers parent
  AC6.
- AC3: Phase/repository/reframe/context-pressure fixtures use a fresh context only with a current
  bounded handoff; length or age alone never triggers a split. Covers parent AC6 and AC14.
- AC4: A Water-style practical-authoring fixture rejects preview/canary or renderer-control proxies
  at the earliest normal authoring journey before descendants/polish. Covers parent AC8 and AC14.
- AC5: A bounded mechanical counter-fixture proceeds without an unnecessary checkpoint or owner
  question; objective product checks proceed without owner interruption. Covers parent AC8.
- AC6: Taste/feel/usability checkpoints request exactly the owner-only observation needed and route
  contradiction to drift without treating it as QA. Covers parent AC8 and AC14.
- AC7: Existing QA and validation-impact regressions prove one QA, no handoff/checkpoint-created
  review, one affected validation and stop after pass. Covers parent AC9.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Coordinator/sequential is the default when no non-Coordinator benefit is recorded.
- Capability availability authorizes a surface but does not justify using it.
- Early checkpoints are claim-triggered and occur once at the earliest useful product boundary.
- Owner involvement is reserved for owner-only evidence or genuine material decisions.

## Validation Plan

- Extend executor-decision fixtures with benefit/overhead and counter-failure cases.
- Run phase/repository/reframe/context-pressure handoff scenarios against TASK-091 state.
- Run Water-style early-authoring and bounded mechanical counter-journeys.
- Re-run focused QA/validation-impact tests and assert no new review action.
- Align managed planning/delegation/implementation/QA guidance, strict Doctor and diff hygiene.
