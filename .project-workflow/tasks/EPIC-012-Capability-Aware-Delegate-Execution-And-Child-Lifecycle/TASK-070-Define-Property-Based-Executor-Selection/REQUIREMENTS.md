# Requirements

## Summary

- Task: TASK-070
- Title: Define Property-Based Executor Selection
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC5, AC6, AC11
- Last updated: 2026-08-20

## Owner Approval

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

- Delegate consumes existing approved scope and never creates execution authority.
- Target kind does not determine executor; the lightest surface that satisfies every binding property is selected.
- Unknown capability is not support, capacity is never hard-coded, and unmet binding properties block rather than silently downgrade.
- Native visible-task creation requires the explicit authority demanded by the current host.
- The coordinator is the only shared-state writer and the only verifier that may satisfy dependencies or issue retirement intent.
- Temporary visible tasks are retired only after verified terminal durable disposition and absence of unresolved attention; Codex uses reversible task archival.
- The coordinator and every active, uncertain, failed, orphaned, unintegrated, owner-promoted, explicitly retained, or attention-bearing task remain visible.
- Retirement is reversible where the host supports it, idempotent, observable, and resumable; task handles persist until success is verified.
- Host adapters perform native actions; the host-neutral core records requirements, decisions, intents, and verified outcomes.
- Worker scope, evidence, lifecycle, QA, closeout, privacy, and delivery boundaries from EPIC-010 remain intact.
- Unexercised hosts receive truthful expected behavior and safe fallback, never fabricated runtime validation.
- Existing non-Delegate behavior remains backward compatible.

### Invalid Substitutes

- Target kind, host brand, prompt prose, or an optimistic boolean substituted for per-unit execution needs and runtime-observed capability.
- A universal “always subagent,” “always persistent task,” “always team,” or “always archive” policy.
- Requirements/Epic approval substituted for current-host explicit task-creation authority.
- A worker completion claim substituted for coordinator verification and durable integration into the authoritative target or an explicit verified no-integration disposition with receipt.
- Marking a retirement intent as completed without observing the host result.
- Deleting tasks or transcripts presented as archival cleanup.
- Hiding active, failed, orphaned, unintegrated, or attention-bearing work to produce a clean sidebar.
- Unit tests or generated-asset parity presented as live proof of Claude Code, GitHub Copilot, Cursor, or unobserved Codex behavior.
- Delegate selection or cleanup presented as QA, owner acceptance, release, deployment, adoption, or effectiveness proof.

### Artifact Targets

- Host-neutral execution-needs and capability-aware selection model, human/JSON output, compatibility defaults, and tests under `src/project_workflow/` and required helper mirrors.
- Delegation runtime-state extensions for visibility class, retention policy, retirement intent/outcome, reconciliation, and retained-attention reasons.
- Updated Codex Delegate skill, common/host-specific prompts or agents, managed guidance, README, packaged resources, and init/upgrade/collision/rollback handling.
- Focused selection and retention suites, full locked regression, strict Doctor, build/package/mirror validation, and a sanitized current-Codex journey receipt.

### Parent AC Proof Ownership

- AC1: owner `Property-Based Executor Selection`; required evidence: Target-kind-invariance and execution-property parsing/derivation tests.
- AC2: owner `Property-Based Executor Selection`; required evidence: Deterministic routing matrix covering coordinator, subagent, persistent task, and peer/team eligibility.
- AC3: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Capability/authority/fallback matrix with exact block or downgrade reasons and adapter-alignment evidence.
- AC4: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Current Codex contract evidence and tests separating task-creation authority from Epic approval.
- AC5: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement`; required evidence: Human/JSON schema snapshots and read-only plan/status non-mutation evidence.
- AC6: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Existing work-packet, single-writer, reconciliation, failure, resume, QA, and closeout regression evidence.
- AC11: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Compatibility fixtures, full locked suite, strict Doctor, build/package, and non-Delegate regression results.

## Goal

Replace target-kind routing with one deterministic property-based executor selector shared by planning and runtime coordination.

## Non-Goals

- Native host launch or retirement actions.
- Changing EPIC-010 evidence, QA, or closeout rules.
- Assuming capability from host name or target kind.

## Users & Context

Delegate users planning Task rows or Epic children whose safest execution surface depends on the work, not its workflow container.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Add optional, backward-compatible per-unit execution-needs metadata with conservative bounded-return defaults.
- Keep work needs separate from observed host capabilities and explicit authority.
- Select surface (`coordinator`, `subagent`, `persistent-task`, `peer-team`) separately from schedule (`sequential`, `parallel`).
- Make identical Task and Epic units select identically; preserve dependency, capacity, scope, and single-writer safeguards.
- Project required properties, visibility class, requested/effective executor, concurrency, provenance, and exact fallback/block reasons in human and JSON output.

## Acceptance Criteria (Verifiable)

- AC1: Legacy blank execution needs resolve as bounded return-to-coordinator work, while supported tokens for durable resume, direct owner steering, isolated worktree, and peer communication parse and validate deterministically.
- AC2: A routing matrix covers all four surfaces, target-kind invariance, surface-specific isolation, capability/authority/capacity failures, and safe fallback versus blocking.
- AC3: Plan/status human and JSON output expose the decision inputs and outcome without mutation, while existing legacy CLI and non-Delegate behavior remain compatible.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Execution needs are plan facts; capabilities are dated runtime observations.
- Peer-team is selected only for explicit lateral communication, never ordinary dependency parallelism.
- Current-request authority remains distinct from parent requirements approval.

## Validation Plan

- Extend focused delegation, Task-mode, Epic-mode, CLI, and compatibility tests; run strict Doctor and helper mirror checks.
