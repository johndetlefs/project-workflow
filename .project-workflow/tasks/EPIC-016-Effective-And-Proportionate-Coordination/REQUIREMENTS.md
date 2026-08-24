# Requirements

## Summary

- Task: EPIC-016
- Title: Effective And Proportionate Coordination
- Last updated: 2026-08-24
- Proposal state: Owner-approved; implementation in progress
- Intent contract: full

## Intent

Make Project Workflow reliably deliver the owner's intended outcome with the smallest sufficient
coordination, context, execution, and proof structure. The owner should be able to explain what
they want conversationally; Project Workflow must carry the requirements, task boundaries,
handoffs, validation, and stopping rules without requiring the owner to remember a long prompt.

## Intent Spine

- OC1 — Completion capability: one owner-facing Coordinator can take a consequential request from
  requirements conversation through delivery while preserving intent in durable repository state,
  moving bounded work through the smallest sufficient same-context or fresh-context surface, and
  stopping after sufficient proof.
- OC2 — Material capabilities: one Coordinator role; meaning-first requirements dialogue; current-
  contract preflight; logical-coordinator versus physical-task separation; context-boundary
  decisions enforced by existing lifecycle gates; existing Delegate work packets and verified
  returns; proportionate executor selection; early
  real-outcome checkpoints; an explicit five-boundary drift decision; fit-for-purpose Clarify;
  existing QA/validation stop-gate integration; and inspectable effectiveness evidence.
- OC3 — Success journey: an owner describes a material user-facing programme once; the Coordinator
  plays back the outcome and material boundaries, records one approval, checks the current Project
  Workflow contract, decomposes the work, uses fresh bounded execution contexts only where they
  earn their transfer cost, checks intent at every material coordination boundary, detects a successful-but-wrong
  product direction before broad implementation, independently validates the affected result once,
  and returns a concise delivery state without recursive review or repeated owner prompting.
- OC4 — Successful-but-wrong result: Project Workflow creates correct documents, launches several
  agents, passes tests, and reports activity, while one physical task accumulates unrelated phases
  and repository history, an active programme continues under a stale workflow contract, a wrong
  product interpretation is discovered only after broad implementation, or proof is repeated
  without a named invalidated layer.
- OC5 — Exclusions: no arbitrary usage cap, no instruction to reduce effort regardless of outcome,
  no assumption that subagents or new tasks are inherently efficient, no forced task split based
  only on length, no second QA system, and no weakening of requirements, implementation, evidence,
  security, or delivery standards.
- OC6 — Assumptions: repository artifacts are the durable coordination authority; host context and
  usage telemetry may be incomplete or non-portable; fresh contexts help only when their packets
  are bounded and their work is sufficiently independent; and semantic fidelity still requires
  reviewable judgment.
- OC7 — Authority source: owner direction in the current Codex task on 2026-08-23 and 2026-08-24,
  supported by direct inspection of the Water Authoring Programme task and Project Workflow 0.6.0.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-24
- Approval note / source: Codex owner direction 2026-08-24: approved evidence-backed Coordinator Core correction with Fine, let us go.
- Approved artifact identity: sha256:ce8b00b647d1d5dcd8d6bbf7c4a8fbc6a0c72ca4fe15266b4bd34c53ed47fc32

## Goal

Turn Project Workflow's existing intent, execution, and proof controls into one coherent operating
model that is effective and proportionate in long-running real projects. The change must preserve
quality where consequence demands it while preventing avoidable context replay, duplicate work,
unjustified multi-agent fan-out, stale-contract continuation, late semantic correction, and
recursive validation.

## Non-Goals

- Do not impose an arbitrary task, context, agent, tool-call, or token ceiling.
- Do not reduce requirements fidelity, implementation quality, validation, independent QA,
  security, privacy, data integrity, or delivery proof to improve an efficiency measure.
- Do not split work automatically because a physical task is old, long, or has compacted.
- Do not make subagents, persistent tasks, parallel execution, or a fresh task the default for work
  that remains more effective in one context.
- Do not add a second intent ledger, approval system, QA scheduler, or generalized review loop.
- Do not build a billing, credit-accounting, or cross-host token-normalization product.
- Do not change the product scope of Mechanics Playground, Game Foundation, or another consumer;
  those repositories are rollout targets only when clean, eligible, and separately verified.

## User Story

As the owner, I want to describe the outcome and material decisions conversationally, then rely on
one Coordinator to preserve that meaning across requirements, planning, execution, fresh-context
handoffs, QA, and delivery so substantial work remains effective without avoidable process or
context wastage.

## Problem Statement And Current Evidence

Project Workflow 0.6.0 already fixes two important failure classes: it adds meaning-first Intent
and outcome proof, and it enforces a three-outcome validation-impact stop gate after proof. The
current repository is clean at `c215b4379c4b38a4efee672c64c2b4b599385d04`, matches fetched
`origin/main`, reports package 0.6.0 and asset version 5 as current, and has no visible Doctor
finding. Those controls must be reused, not rebuilt.

The Water Authoring Programme exposes the remaining failure. Its physical Codex task spans
requirements, two repositories, multiple Epics, implementation, QA, owner correction, and later
product reframing. The inspected consumer worktree still runs Project Workflow 0.5.0 and asset
version 3. It therefore proves a long-lived-coordinator, stale-contract, context-boundary, and
adoption problem; it does not prove that the later 0.6.0 intent and stop gates failed.

The same case also shows why neither one enormous task nor automatic multi-agent fan-out is a safe
default. Separate contexts can isolate bounded work, but they add startup, coordination, and
synthesis cost. The workflow needs an explicit decision about when a fresh context earns that cost,
what minimal authority it receives, what it returns, and when the logical Coordinator moves to a
new physical task while durable repository state preserves continuity.

## Users & Context

- The owner wants to state outcomes and make material decisions conversationally, without having
  to remember workflow mechanics or repeatedly restate approved requirements.
- Coordinators need to retain authoritative state across phases without dragging a complete task
  history into every implementation or review action.
- Implementers and reviewers need only the approved scope, exact source, dependencies, evidence
  contract, and relevant local context for their bounded assignment.
- Maintainers need proof that a candidate improves the ratio of useful delivery to coordination
  effort without disguising lower quality as efficiency.
- Supported hosts differ in task creation, subagent isolation, persistence, monitoring, context
  telemetry, and retirement capabilities; the contract must report those differences truthfully.

## Repository Scope

- Primary repository: .
- Repositories touched: .
- Real consumer history may inform sanitized fixtures and dogfood evidence, but this Epic does not
  mutate Mechanics Playground, Game Foundation, or another consumer without explicit rollout
  authority.

## Requirements (Outcome-Focused)

- R1 — Add a stable constitutional outcome and decision filter: Project Workflow uses the smallest
  sufficient coordination and proof structure that can reliably deliver the approved outcome.
  Additional contexts, agents, documents, reviews, and owner interruptions must address a named
  dependency, risk, authority boundary, or evidence gap.
- R2 — Establish one public owner-facing `Coordinator` role from intake through delivery.
  Delegation is one action available to the Coordinator, not a second role. Preserve a documented,
  time-bounded compatibility path for existing `Delegate` skills and host assets rather than
  silently breaking installed consumers.
- R3 — Make the Coordinator conduct a proportionate requirements dialogue. It extracts requirements
  from the conversation, asks focused questions only for material unknowns, and plays back the
  intended completion capability, material inclusions, exclusions, assumptions, successful-but-
  wrong result, and outcome journey for one meaning confirmation. It must not treat internally
  consistent inferred requirements as owner understanding.
- R4 — Before a material programme starts or resumes, inspect the installed Project Workflow
  contract and the contract under which its current plan was approved. A current compatible
  contract proceeds. A materially stale contract produces a bounded adoption or handoff decision;
  it may not continue silently under obsolete operating guidance or imply that a repository
  upgrade has refreshed an already-loaded task context.
- R5 — Separate the durable logical Coordinator from any physical chat, task, agent, or worktree.
  Record only phase, current Intent/source identity, material decisions, context declaration, the
  named boundary decisions, one earliest outcome checkpoint, next action, and handoff reason in
  repository-native coordination state. Reference rather than copy execution units, dependencies,
  packets, returns, evidence, and worker lifecycle owned by the canonical plan and Delegate. Select
  a fresh physical task or bounded subagent
  at material phase changes, repository boundaries, owner-approved reframes, or observed context
  pressure only when its named benefit outweighs transfer cost and continuity can be preserved by
  a compact handoff; the same physical context may continue after explicitly loading the current
  contract when there is no conflict or isolation need. Do not split merely because a task is old
  or long.
- R6 — Select the lightest sufficient execution surface using approved needs, dependency coupling,
  write-scope collision, repository isolation, direct owner steering, durability, capability, and
  expected coordination overhead. Parallel or multi-agent execution must have a named benefit that
  outweighs its setup and synthesis cost; independent work may proceed in parallel, while coupled
  work remains sequential or Coordinator-owned.
- R7 — Extend the existing Delegate work packet and verified-return contracts rather than creating
  a second coordination packet/receipt system. A packet contains only the
  owner-approved outcome commitments relevant to the unit, exact source/worktree, allowed scope,
  dependencies, required proof, invalid substitutes, authority, and stopping condition. A receipt
  returns identity, source, actual diff/scope, validation/evidence, decisions, residual risks, and
  next dependency state. Full conversation history is referenced when needed, not copied by
  default.
- R8 — For material user-facing, authoring, visual, gameplay-feel, migration, or replacement work,
  require the earliest proportionate real-outcome checkpoint before broad fan-out or expensive
  polish. The checkpoint must exercise the normal user journey or owner-visible product surface,
  not a code/test proxy. Owner interruption is required only where taste, usability, feel, or a
  material product choice genuinely belongs to the owner.
- R9 — Integrate, rather than duplicate, 0.6.0 intent integrity and post-proof validation. One
  independent QA gate remains required after implementation. Later changes reopen only named
  proof layers through the existing validation-impact decision; Coordinator handoffs, receipts,
  context changes, and QA findings cannot recursively create more QA.
- R10 — Surface the current coordination state and one sourced next action through workflow status
  and Doctor where deterministic evidence exists. Host-observed context or usage telemetry may be
  retained as evidence, but unavailable telemetry remains unknown and raw internal token counts
  must not be represented as invoice, credit, or cross-host efficiency truth.
- R11 — Add sanitized behavioural scenarios covering: a bounded one-context task; an independent
  parallel programme; a tightly coupled programme; a stale consumer task; a phase/repository
  handoff; a material owner reframe; an early successful-but-wrong product; a subagent fan-out that
  costs more than it helps; and a passed-proof change that must stop after one affected validation.
- R12 — Prove the candidate through repeated agent trials or equivalent behavioural evaluation,
  a disposable end-to-end repository journey, and current Project Workflow dogfood. Compare useful
  outcome, rework, duplicate actions, owner interruptions, handoff sufficiency, and host-observed
  effort against the retained baseline without adopting an arbitrary universal token target.
- R13 — Keep package source, managed skills/prompts, generated assets, documentation, compatibility
  aliases, installation/upgrade behavior, and repository-local copies aligned. Release,
  publication, merge, and consumer rollout remain explicit delivery gates.
- R14 — At five material coordination boundaries—after planning/decomposition, before a child
  starts, when a child returns or dependencies join, when new evidence or owner direction changes a
  premise, and before Review/Complete—the Coordinator compares the proposed next state with the
  approved Intent Spine and records one bounded decision: `inside-envelope`, `drift-detected`, or
  `approved-change`. Inside-envelope work continues without owner interruption. Drift blocks the
  affected branch and names the narrowed, proxy, omitted, or broadened capability plus its user-
  visible consequence. An approved change uses the existing amendment/reapproval path, refreshes
  only affected descendants and existing Delegate work packets, and then resumes. Existing
  lifecycle transitions fail closed when the required current decision or checkpoint is missing,
  stale, or drifted, so the owner need not remember a special coordination command. The decision
  is boundary-triggered, not periodic, and cannot commission QA or a general review.
- R15 — Evaluate Clarify as a distinct decision capability rather than assuming its current prompt
  is sufficient. It must support pre-approval product ambiguity, autonomous post-plan consistency,
  and ambiguous mid-Epic drift routed by the Coordinator; use the Intent Spine rather than only an
  `IMPLEMENTATION.md` User Story; work for Epic parents and children as well as standalone Tasks;
  ask only questions whose answers materially change scope, risk, proof, authority, or user-visible
  behavior; and stay unchanged where held-out evidence shows the current contract already works.

## Acceptance Criteria (Verifiable)

- AC1: The Constitution states the smallest-sufficient coordination principle and rejects both
  avoidable overhead and quality reduction; every new execution or proof layer must be traceable to
  a named dependency, risk, authority boundary, or evidence gap.
- AC2: Installed guidance presents one owner-facing Coordinator from intake through delivery and
  describes delegation as its action. Existing `project-delegate` invocations have a tested
  compatibility/deprecation path and cannot create a competing shared-state writer.
- AC3: In a held-out ambiguous request, the Coordinator asks only the material requirements
  questions and produces an approval synopsis that accurately states capability, inclusions,
  exclusions, assumptions, successful-but-wrong result, and proof journey. It proceeds after one
  meaning confirmation and does not ask for generic reapproval inside the unchanged envelope.
- AC4: A material programme on the current installed contract proceeds without ceremony. A fixture
  approved under a materially older contract blocks silent continuation and produces one explicit
  adoption/handoff action; upgrading files alone does not falsely certify that an already-loaded
  task is operating under the new contract.
- AC5: A logical Coordinator can move from requirements to implementation, across a repository
  boundary, and through a material reframe using the same context or a fresh physical context only
  when justified. A successor resumes from a compact durable handoff with exact source, decisions,
  canonical plan/Delegate references, next action, and stopping condition, without receiving the
  complete conversation or a copied execution graph.
- AC6: Executor-selection fixtures choose one context for coupled work, bounded subagents for
  sufficiently independent work, and persistent tasks only for verified durability or owner-
  steering needs. The decision records the benefit and overhead basis and fails closed when a
  binding capability is unknown or unsupported.
- AC7: Existing Delegate work-packet and verified-return schemas reject missing authority, source, relevant outcome
  commitments, scope, dependency, proof, or stopping information. Coordinator reconciliation
  rejects mismatched identity, source, scope, evidence, or stale return state.
- AC8: In the successful-but-wrong user-facing fixture, an early normal-journey checkpoint rejects
  the proxy implementation before dependent implementation/polish begins. A bounded mechanical
  task does not acquire an unnecessary product checkpoint or owner interruption.
- AC9: The existing independent QA and validation-impact regressions still pass. A Coordinator
  handoff never creates QA; passed QA plus an unaffected change stops; an affected change runs the
  one named validation; ambiguous impact asks one focused question and does not schedule review.
- AC10: Status and Doctor report current/stale contract state, logical coordination phase, recorded
  handoff state, boundary/checkpoint state, Delegate executor/return state, and the single next action only
  from inspectable evidence. Missing host telemetry is reported as unknown rather than estimated.
- AC11: Sanitized behavioural coverage includes all nine R11 scenarios and demonstrates both
  failure avoidance and counter-failure avoidance: no undercooking, no gold-plating, no automatic
  fan-out, no arbitrary context churn, no stale-contract continuation, and no recursive review.
- AC12: Repeated evaluation and a disposable real journey show that the candidate preserves or
  improves outcome fidelity and required proof while reducing avoidable context replay, duplicate
  work, late rework, or unnecessary owner interruptions relative to the baseline. Available host
  usage telemetry is reported with its accounting boundary, not converted into unsupported credit
  or billing claims.
- AC13: Source, packaged assets, generated host guidance, compatibility behavior, exact candidate
  artifacts, and supported fresh/legacy installation journeys pass together. Delivery state keeps
  implemented, validated, merged, published, released, and consumer-adopted claims separate.
- AC14: A Water-style fixture begins with an approved practical-authoring capability and then tries
  to substitute preview plus one canary during decomposition, renderer-internal controls during
  implementation, and a green proxy at child return. The five-boundary drift decision blocks each
  injected failure before affected descendants continue, names the user-visible lost capability,
  preserves unrelated branches only while their shared premises remain valid, and refreshes exact
  descendants after an owner-approved reframe without triggering a new QA cycle.
- AC15: Held-out Clarify scenarios cover pre-approval material ambiguity, a clean bounded request,
  an internally consistent post-plan proxy that violates Intent, an Epic parent without
  `IMPLEMENTATION.md`, a full-contract child, and an ambiguous mid-Epic drift decision. Clarify asks
  one focused owner question only when a material decision is unresolved, resolves in-envelope
  implementation detail autonomously, routes confirmed drift to restore/amend rather than
  re-planning it, and introduces no redundant approval or review loop. Any Clarify change is limited
  to reproduced failures from this matrix.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose | Dependencies |
| --- | --- | --- | --- |
| Define Coordinator Intent And Clarify Contract | AC1, AC2, AC3, AC15 | Establish the constitutional and owner-facing Coordinator model, evaluate Clarify against held-out Task/Epic scenarios, and make only the smallest reproduced Clarify correction. |  |
| Build Durable Coordination Handoff And Drift Controls | AC4, AC5, AC7, AC10, AC14 | Add current-contract preflight, compact logical coordination state, lifecycle-enforced drift decisions, enrich existing Delegate packets/returns, and provide sourced status/Doctor projection. | TASK-090 |
| Route Proportionate Execution And Early Outcome Proof | AC6, AC8, AC9, AC14 | Make executor selection earn its overhead, add proportionate early real-outcome checkpoints, and integrate them with the existing one-QA and post-proof stop gates. | TASK-090, TASK-091 |
| Create Coordination Behavioural Evaluations | AC11, AC12, AC14, AC15 | Build sanitized failure/counter-failure fixtures, repeated trials, and effectiveness grading for drift, Clarify, context topology, fan-out, rework, owner interruption, and stopping behavior. | TASK-090, TASK-091, TASK-092 |
| Prove Package Publish And Eligible Rollout | AC12, AC13 | Run the exact candidate suite and real journeys, verify each child already has its one required QA and evidence without reopening review, merge and publish the approved release, verify the public artifact, and upgrade only eligible clean consumer repositories with per-root dispositions. | TASK-090, TASK-091, TASK-092, TASK-093 |

## Outcome Commitment Coverage

| Commitment | Child Owners | Parent ACs | Required Disposition |
| --- | --- | --- | --- |
| OC1 — One effective owner-facing Coordinator | TASK-090, TASK-091, TASK-094 | AC1-AC5, AC13, AC15 | Defined, implemented, packaged, and proven from intake through eligible rollout. |
| OC2 — Material coordination capabilities | TASK-090, TASK-091, TASK-092, TASK-093, TASK-094 | AC1-AC15 | Every capability is implemented, behaviorally evaluated, or explicitly retained unchanged through passing evidence. |
| OC3 — Complete effective journey | TASK-091, TASK-092, TASK-093, TASK-094 | AC4-AC14 | Disposable and dogfood journeys prove bounded handoffs, drift blocking, one QA, stop, publication, and adoption. |
| OC4 — Reject successful-but-wrong coordination | TASK-091, TASK-092, TASK-093 | AC4-AC12, AC14-AC15 | Stale-contract, long-task, proxy-product, over-fan-out, and recursive-review candidates are rejected before propagation. |
| OC5 — Preserve quality and avoid arbitrary limits | TASK-090, TASK-092, TASK-093 | AC1, AC3, AC6, AC8, AC9, AC11, AC12, AC15 | Counter-fixtures prove bounded work remains light and required rigor is not removed. |
| OC6 — Honest capability and telemetry boundaries | TASK-091, TASK-093, TASK-094 | AC4-AC7, AC10, AC12, AC13 | Unknown host facts stay unknown; package and rollout claims remain evidence-scoped. |
| OC7 — Owner authority and evidence provenance | TASK-090, TASK-091, TASK-094 | AC2-AC5, AC7, AC10, AC13-AC15 | Approval, amendment, work-packet, return, release, and rollout authority remain inspectable. |

## Delivery Sequence

1. Define the single Coordinator role and prove Clarify's current failures before changing its
   contract or managed copies.
2. Build compact logical coordination state, version-aware context loading/handoff, enrich the
   existing Delegate packet/return contract, and enforce five-boundary drift decisions through
   existing lifecycle gates.
3. Route execution surfaces and early real-outcome checkpoints through those controls while
   retaining the existing independent-QA and validation-impact stop behavior.
4. Run sanitized behavioural evaluations and revise the earliest owning contract when a trial
   exposes real under-processing or over-processing.
5. Build and independently review the exact candidate once, merge and publish the authorized
   release, verify the public artifact, and upgrade only eligible clean consumers.

## Open Questions (Answer Needed)

- None. The owner confirmed the Intent, explicit drift gate, Clarify assessment, implementation,
  independent QA, merge, package publication, and rollout to eligible clean consumer repositories
  in the current Codex task on 2026-08-24.

## Decisions (Resolved)

- The objective is effective and proportionate delivery without wastage, not token minimization.
- v0.6.0 intent-integrity and post-proof stop controls remain and will not be redesigned without a
  reproduced current-version failure.
- The Water task is valid evidence of v0.5.0 coordination/adoption failure, not evidence that v0.6.0
  failed controls it did not provide to that task.
- Coordinator is the role; delegation, implementation, review, and handoff are actions or gates.
- Durable repository state preserves continuity; a single physical task is not the programme.
- Fresh contexts and multi-agent work are selected only when they improve the expected outcome
  enough to justify their coordination cost.
- Drift prevention is a five-boundary Coordinator decision using the existing Intent Spine,
  intent-audit, amendment, readiness, reconciliation, and lifecycle gates; it does not add a
  periodic review scheduler or a second source of truth.
- Clarify owns unresolved decisions and post-plan consistency. The Coordinator owns boundary
  detection and routing; Clarify is invoked only when that decision is genuinely ambiguous.
- Cross-host behavior remains capability-aware and fail-closed.
- Delivery authority extends through implementation, independent QA, merge, package publication,
  and rollout to eligible clean consumer repositories. Dirty, active, ambiguous, or otherwise
  blocked consumers remain unchanged with an exact recorded disposition.

## Validation Plan

- Run focused schema, parser, readiness, Coordinator, capability, status, Doctor, compatibility,
  stop-gate, and managed-asset parity tests during implementation.
- Run repeated held-out behavioural evaluations over the R11 scenario matrix.
- Exercise the five-boundary Water-style drift fixture and the six-scenario Clarify fitness matrix,
  retaining both failure and no-change counterexamples.
- Exercise a disposable repository from conversational intake through requirements confirmation,
  decomposition, bounded execution, phase/repository handoff, early product rejection, independent
  QA, affected-layer validation, and stop/delivery.
- Dogfood EPIC-016 itself, retaining compact task/agent lineage, work packets, receipts, handoff
  decisions, owner interruptions, rework, duplicate-action findings, and accurately scoped host
  usage telemetry where available.
- Run the complete locked suite once on the exact release candidate, strict Doctor, build/package
  verification, and all supported exact-package fresh/upgrade journeys. Do not repeat unaffected
  proof after a passing validation-impact decision.
