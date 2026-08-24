# Requirements

## Summary

- Task: TASK-090
- Title: Define Coordinator Intent And Clarify Contract
- Parent AC Coverage: AC1, AC2, AC3, AC15
- Last updated: 2026-08-24
- Intent contract: full

## Intent

Make one owner-facing Coordinator the clear Project Workflow role from conversational intake through
delivery, with delegation as one action rather than a competing role. Make Clarify reliably resolve
only material uncertainty across Tasks, Epic parents, Epic children, and Coordinator-routed drift.

## Intent Spine

- OC1 — Completion capability: the owner interacts with one Coordinator that captures meaning,
  invokes the appropriate workflow capabilities, and remains the sole shared-state authority.
- OC2 — Material capabilities: constitutional proportionality; canonical Coordinator guidance;
  Delegate compatibility routing; meaning-first requirements dialogue; three-mode Clarify;
  Task/Epic target support; focused questions; and managed-asset parity.
- OC3 — Success journey: a material request is played back once, a clean plan proceeds without
  another owner prompt, an Epic-parent plan can be clarified without an implementation file, and
  ambiguous drift produces one focused decision rather than improvisation or review.
- OC4 — Successful-but-wrong result: assets are renamed while owners still face separate Delegate
  and Coordinator roles, Clarify stops on a valid Epic parent, or Clarify turns every uncertainty
  into owner-facing ceremony.
- OC5 — Exclusions: this child does not implement durable coordination state, work-packet schemas,
  drift decision storage, executor routing, behavioural reliability claims, publishing or rollout.
- OC6 — Assumptions: current Requirements, Planner, Intent audit, Implement, QA and stop-gate
  controls remain authoritative; prompt/skill behavior needs held-out proof beyond static parity.
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

- AC1: owner `Constitution And Operating Model`; required evidence: Constitution diff plus smallest-sufficient positive and counter-example checks.
- AC2: owner `Coordinator Contract And Compatibility`; required evidence: Managed asset parity, compatibility journeys, and single-writer role tests.
- AC3: owner `Requirements Dialogue`; required evidence: Held-out ambiguous and bounded request trials plus approval-burden evidence.
- AC15: owner `Clarify Fitness`; required evidence: Held-out Task/Epic/pre-plan/post-plan/mid-Epic scenarios and smallest evidence-backed disposition.

## Goal

Establish the stable role and decision contract that later coordination controls can implement
without duplicating authority, adding approval burden, or assuming Clarify is already sufficient.

## Non-Goals

- No durable coordination CLI/state or context-handoff engine; TASK-091 owns it.
- No executor-selection or early-outcome engine; TASK-092 owns it.
- No claim of behavioural effectiveness from prompt text or unit tests alone; TASK-093 owns it.
- No removal of `project-delegate` in the first Coordinator release.
- No new owner approval stage or periodic Clarify scheduler.

## Users & Context

- Owners who need one understandable workflow counterpart rather than a catalogue of agent roles.
- Agents operating Requirements, Planner, Clarify, implementation, QA and delivery capabilities.
- Existing consumers invoking Delegate assets that must not break during the migration.
- Epic coordinators that currently cannot apply Clarify directly to a valid parent without
  `IMPLEMENTATION.md`.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Add the smallest-sufficient coordination principle to the Constitution and decision filters:
  extra contexts, agents, documents, reviews or owner interruptions must address a named need and
  may never substitute reduced quality for efficiency.
- R2 — Define `Coordinator` as the single owner-facing role from intake through delivery. It invokes
  Requirements, Planner, Clarify, implementation, delegation, QA and delivery gates without
  becoming a second writer or self-certifying proof.
- R3 — Add canonical `project-coordinator` assets. Keep `project-delegate` as a compatibility entry
  in the first Coordinator release, routing to the same single-writer contract and warning that
  delegation is a Coordinator action. Removal is eligible only after one full minor release and
  observed migration evidence.
- R4 — Preserve the existing meaning-first Requirements approval and make Coordinator guidance use
  it automatically; the owner confirms meaning once and is not asked for generic plan approval.
- R5 — Make Clarify support `pre-approval`, `post-plan`, and `drift-ambiguity` modes. Anchor first to
  approved Intent/Intent Spine, then use an implementation User Story when present. Support
  standalone Tasks, Epic parents and Epic children without inventing missing files.
- R6 — In Clarify, ask the owner only when an unresolved answer materially changes scope, risk,
  proof, authority or user-visible behavior. Resolve in-envelope plan detail autonomously; route
  confirmed drift to restoration/amendment; never create implementation, QA or a review loop.
- R7 — Align README, AGENTS, Codex skills, GitHub prompts, Cursor rules, source templates, installed
  managed copies and generation manifests, with focused failure/counter-failure tests.

## Acceptance Criteria (Verifiable)

- AC1: Constitution and installed guidance state the smallest-sufficient principle and reject both
  avoidable coordination overhead and quality reduction. Covers parent AC1.
- AC2: Owners see one Coordinator role from intake through delivery; delegation is an action, and
  shared workflow state retains exactly one writer. Covers parent AC2.
- AC3: Canonical `project-coordinator` assets install across supported hosts. The retained
  `project-delegate` compatibility entry routes to the same contract, clearly signals migration,
  and does not create a second role or writer. Covers parent AC2.
- AC4: Held-out ambiguous and clean requests prove the Coordinator plays back meaning once, asks
  only material questions, and proceeds through planning without generic reapproval. Covers parent
  AC3.
- AC5: The six-scenario Clarify matrix passes for pre-approval ambiguity, clean bounded work,
  post-plan Intent proxy, Epic parent without `IMPLEMENTATION.md`, full-contract child, and
  ambiguous mid-Epic drift; failure and no-change counter-cases are retained. Covers parent AC15.
- AC6: Package source, generated host assets and installed self-hosted copies are semantically
  aligned and protected by focused parity/generation tests.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Coordinator is the public role; Delegate remains only as a compatibility entry and action name.
- Clarify resolves ambiguity; it does not monitor every boundary or own canonical drift state.
- The Coordinator detects a boundary and invokes Clarify only for genuinely ambiguous material
  decisions.
- Existing Clarify behavior that passes the baseline remains unchanged.

## Validation Plan

- Add focused Coordinator/Clarify asset, routing and compatibility tests.
- Run the retained six-scenario Clarify fitness matrix and bounded clean counter-case.
- Generate each supported host surface and compare canonical semantics and installed assets.
- Run focused tests, strict Doctor and diff hygiene; defer repeated behavioural effectiveness and
  exact-package journeys to TASK-093 and TASK-094.
