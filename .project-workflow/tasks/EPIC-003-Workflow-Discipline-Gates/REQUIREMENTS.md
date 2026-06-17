# Requirements

## Summary

- Task: EPIC-003
- Title: Workflow Discipline Gates
- Last updated: 2026-06-17

## Goal

Create stronger workflow discipline gates so project-workflow can be handed to junior developers and coding agents without letting vague prompts turn into under-specified epics, under-specified child tasks, or premature implementation.

The workflow must require enough user context to justify creating a task or epic, enough parent-epic detail to justify decomposition into child tasks, and enough child-task readiness evidence to justify implementation. Agents should ask targeted clarification questions when required context is missing instead of inventing requirements or letting the model run ahead.

Project-workflow should be human-readable but agent-operated. The user is expected to act as product owner, product manager, or BA: they provide intent, constraints, priorities, examples, decisions, and approvals. The model is expected to operate the workflow: it runs commands, drafts and updates artifacts, asks focused questions, maps acceptance criteria, implements, validates, reviews, and records evidence. The CLI and doctor checks verify that the agent did not skip required gates.

## Non-Goals

- Replacing owner judgment about product priorities, scope tradeoffs, or final approval.
- Building a heavyweight external project management system outside repository-native Markdown and the existing CLI.
- Blocking exploratory discovery tasks when the user explicitly records that discovery is the intended outcome.
- Retrofitting every historical task or epic in this repository.
- Implementing this epic during the requirements pass.

## Users & Context

- Primary users are junior developers and agent operators using project-workflow to drive tasks and epics without deep prior context.
- Maintainers need the workflow to prevent avoidable ambiguity, ID collisions, missing clarification, and premature implementation.
- Product owners need confidence that vague requests result in clarifying questions, explicit assumptions, or accepted risks before work is decomposed or implemented.
- Agents need machine-checkable gates so they do not rely only on good judgment or conversational memory.
- The expected day-to-day flow is owner-directed and agent-operated: the owner explains goals conversationally, the agent turns that into workflow state, and the product verifies the workflow state before letting the agent proceed.

## Requirements (Outcome-Focused)

- Project-workflow defines a minimum context model for creating tasks and epics. At minimum, intake should establish the problem, desired outcome, affected user or actor, scope boundaries, acceptance signal, constraints, priority or risk, and relevant examples or failure modes.
- The workflow distinguishes missing context that blocks scaffolding from context that can be recorded as an assumption, accepted risk, or discovery objective.
- Epic-level requirements must be detailed enough to support child-task decisions. An epic cannot be decomposed only from vague intent; it needs parent acceptance criteria, scope boundaries, non-goals, decisions, and unresolved questions or accepted risks recorded explicitly.
- Child task implementation must be gated by an implementation-readiness check that proves requirements, acceptance criteria, planning, clarification, validation plan, and parent AC mapping are present before coding begins.
- Status transitions should encode the ceremony. Moving into implementation-oriented states should fail or warn when requirements intake, planning, clarification, or readiness evidence is missing.
- Task ID allocation must treat standalone tasks and epic child tasks as one global `TASK-###` namespace so scaffolded tasks never collide with existing epic children.
- CLI, doctor, templates, prompts, skills, and docs should explain blocked gates with actionable remediation rather than vague failure messages.
- The workflow must remain efficient: gates should ask only targeted questions, allow explicit discovery tasks, and avoid forcing ceremony that does not improve delivery quality.
- Automated fixtures must prove the gates block vague intake, unsafe decomposition, missing readiness, status skips, and ID collisions while allowing adequately specified tasks, adequately specified epics, and explicit discovery work.
- Generated agent guidance must assume the model is the primary workflow operator. Instructions should tell the agent how to extract requirements from conversation, draft artifacts, identify missing context, ask concise questions, record assumptions and owner decisions, and proceed only when gates pass.
- Generated user-facing docs must not imply the owner should manually fill templates as the normal path. They should explain what information the owner should provide conversationally and what decisions they must confirm.
- CLI gate failures should be shaped for agent remediation: each failure should state what is missing, whether the agent can infer it from existing artifacts, whether the owner must answer, and where the answer should be recorded.

## Acceptance Criteria (Verifiable)

- AC1: Task and epic intake guidance defines a required minimum context rubric covering problem, outcome, actor, scope, acceptance signal, constraints, priority/risk, and examples or failure modes.
- AC2: CLI or generated agent guidance prevents task or epic scaffolding from proceeding silently when blocking intake context is missing; it asks targeted questions or records explicit assumptions/accepted risks.
- AC3: Epic decomposition is gated on sufficient parent requirements: stable parent ACs, scope/non-goals, decisions, validation expectations, and no unresolved blocking questions.
- AC4: Epic child task scaffolding preserves the parent context needed for decisions at child level, including parent ACs, relevant parent decisions, open risks, and validation expectations.
- AC5: Implementation readiness validation exists for standalone tasks and epic child tasks, checking no placeholders, child ACs, AC-mapped implementation rows, validation plan, clarification state, and parent AC coverage where applicable.
- AC6: Status transitions into implementation/testing/review/complete states fail or warn when required readiness evidence is missing, with override or discovery paths only when explicitly recorded.
- AC7: `TASK-###` allocation scans standalone task folders, global tracker rows, all epic tracker rows, and epic child task folders so new standalone tasks and epic child tasks remain globally unique.
- AC8: Doctor or validation commands report discipline-gate problems with specific remediation, including missing context, unresolved blocking questions, missing readiness evidence, and ID collisions.
- AC9: Generated Codex/Copilot/Cursor assets and README explain the intended lifecycle for junior developers: intake sufficiency, requirements, clarification, planning, readiness, implementation, QA, retro, and epic closeout.
- AC10: Automated tests cover insufficient task intake, sufficient task intake, insufficient epic intake, unsafe epic decomposition, child scaffold context propagation, missing readiness blockers, explicit discovery exceptions, global ID allocation across epic children, and backward-compatible warnings for existing artifacts.
- AC11: Generated agent guidance defines the owner-directed, agent-operated role split: the owner supplies product judgment and approvals, while the agent runs commands, drafts artifacts, asks targeted questions, validates, and records evidence.
- AC12: User-facing documentation explains the conversational intake model for owners and avoids making manual template completion the default path.
- AC13: Gate failure messages are actionable for agents, distinguishing facts the agent can gather from the repo, assumptions it may record, and decisions that require owner input.

## Open Questions (Answer Needed)

- None blocking after owner decisions on 2026-06-17.

## Decisions (Resolved)

- Decision: Treat this as an epic, not a single task.
  - Context: The gap spans intake rules, requirements templates, epic decomposition, child scaffolding, status transitions, ID allocation, doctor validation, tests, generated agent assets, and docs.
  - Why: It has multiple independently testable workstreams and should dogfood the parent AC mapping discipline added in EPIC-002.

- Decision: Do not decompose EPIC-003 into tracker child rows during this requirements pass.
  - Context: While preparing this epic, `task init` exposed that standalone task ID allocation does not account for EPIC-002 child task IDs. The same risk exists for automated decomposition until global ID allocation is fixed.
  - Why: Creating proposed child rows before fixing or explicitly accounting for ID allocation could create confusing duplicate `TASK-###` rows.

- Decision: The product should optimize for junior-developer guardrails without turning every task into bureaucracy.
  - Context: The user's goal is to prevent agents from running wild while preserving efficacy and efficiency.
  - Why: Gates should block vague or unsafe work, but should still support explicitly scoped discovery and small well-understood tasks.

- Decision: Make the workflow owner-directed and agent-operated.
  - Context: The normal user is acting as product owner, PM, or BA, while the model operates project-workflow commands and artifacts.
  - Why: The product should not split responsibility ambiguously between human-filled templates and agent-filled templates. The owner supplies judgment and decisions; the agent maintains workflow state; CLI gates verify the agent's discipline.

- Decision: Allow scaffolding with incomplete intake, but block downstream execution until ready.
  - Context: Requirements artifacts are useful for gathering missing context, but vague scaffolds must not silently become implementation work.
  - Chosen: `task init` and `epic init` may create artifacts, but generated guidance and status/readiness gates must treat incomplete intake as `Analysing` or `Needs Clarification` work until requirements are sufficient.
  - Why: This preserves momentum without letting the agent run ahead.

- Decision: Add explicit readiness commands and reuse the same logic from doctor and status gates.
  - Context: Readiness should be directly checkable by agents, visible to owners, and enforceable by lifecycle transitions.
  - Chosen: Implement explicit commands such as `task ready`, `epic ready`, and `epic ready-child`; surface the same checks through `doctor --strict` and status transitions.
  - Why: A standalone command gives a clear preflight, while doctor/status integration prevents bypassing the gate.

- Decision: Represent discovery work explicitly and bound it.
  - Context: Some legitimate tasks start with incomplete requirements because the desired output is knowledge or a decision.
  - Chosen: Support an explicit discovery path using `--discovery` and/or `Type: Discovery`, with required question, decision enabled, scope/time boundary, output artifact, and validation signal.
  - Why: Discovery should be first-class, not a loophole for vague build work.

- Decision: Enforce both epic readiness and child task readiness.
  - Context: Sufficient parent epic requirements do not guarantee every child task is specific enough to implement.
  - Chosen: Gate epic decomposition on parent readiness and gate each standalone or epic child task before implementation.
  - Why: This prevents speculative child tasks and prevents shallow children from being implemented just because the parent epic is clear.

- Decision: Preserve backward compatibility with warnings by default and hard gates for new managed artifacts, strict mode, and status transitions.
  - Context: Existing repositories may contain historical tasks that predate readiness metadata.
  - Chosen: Default doctor warns for legacy gaps; `doctor --strict`, new readiness commands, and managed status transitions fail on missing readiness unless an explicit discovery/owner exception is recorded.
  - Why: This gives junior developers real guardrails without making older repos unusable.

- Decision: Owner confirmation must be explicit before inferred requirements are treated as accepted.
  - Context: The agent may draft requirements from conversation, but product judgment belongs to the owner.
  - Chosen: Generated guidance should require an explicit owner signal such as "approved", "proceed", or a direct instruction to begin implementation after the agent summarizes requirements and assumptions.
  - Why: Silence or lack of objection is too weak for guarded workflow state.

- Decision: Gate failures should include an agent-remediation checklist.
  - Context: The model is the workflow operator, so failures should tell it exactly what to gather, infer, record, or ask.
  - Chosen: Readiness and doctor failures should list missing fields with categories: repo-gatherable, assumption allowed with owner confirmation, or owner input required.
  - Why: This turns gate failures into efficient clarification prompts instead of dead ends.

## Validation Plan

- Add unit tests and fixture repositories for intake sufficiency, epic decomposition gating, child context propagation, readiness validation, status-transition enforcement, discovery exceptions, and global task ID allocation.
- Run `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor` against this repository.
- Run the full `tests/test_doctor.py` suite and any new targeted tests.
- Verify generated package templates, installed local helper, generated prompt mirrors, Codex skills, Cursor rules, and README remain aligned.
- Dogfood the new gates on EPIC-003 before closing it: every child task must map to parent ACs, pass readiness before implementation, and contribute evidence to the epic audit.
- Add fixture assertions that generated agent assets describe the owner-directed, agent-operated lifecycle and that user-facing docs ask owners for conversational context rather than manual template work.

## Initial Delivery Plan

Do not treat these as approved child task rows yet. They are proposed workstreams to refine after the ID allocation gate is addressed:

- Intake Sufficiency Model and Templates: define the minimum context rubric and update task/epic requirements templates plus owner-facing docs. Covers AC1, AC2, AC9, AC12.
- Epic Decomposition and Child Context Gates: block vague epic decomposition and propagate parent decisions, risks, validation expectations, and ACs into child docs. Covers AC3, AC4.
- Implementation Readiness and Status Gates: add readiness validation and wire it into status transitions for standalone and epic-managed tasks. Covers AC5, AC6, AC8.
- Global Task ID Allocation: make all task ID generation scan standalone tasks, global tracker rows, all epic trackers, and epic child folders. Covers AC7.
- Agent-Operated Guidance and Remediation: update generated skills/prompts and gate messages so the agent knows what to gather, what to ask, what to record, and when to stop for owner input. Covers AC11, AC13.
- Fixture Coverage and Dogfood Closeout: add tests, docs, generated asset parity checks, and prove EPIC-003 itself follows the gates. Covers AC8, AC9, AC10, AC11, AC12, AC13.
