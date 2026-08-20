# Requirements

## Summary

- Task: TASK-071
- Title: Implement Hybrid Runtime And Verified Child Retirement
- Parent AC Coverage: AC5, AC6, AC7, AC8, AC9, AC12, AC14
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

- AC5: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement`; required evidence: Human/JSON schema snapshots and read-only plan/status non-mutation evidence.
- AC6: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Existing work-packet, single-writer, reconciliation, failure, resume, QA, and closeout regression evidence.
- AC7: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Retirement eligibility, intent/outcome, idempotency, integration/disposition receipt, and live successful-cleanup evidence.
- AC8: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Parameterized exclusion-state tests and live attention-bearing retention evidence.
- AC9: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Retirement failure/unknown/resume/orphan tests proving retained handles and truthful state.
- AC12: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Sanitized dated current-Codex journey receipt covering subagent, persistent task, archival, coordinator survival, and no duplicates.
- AC14: owner `Hosts And Compatibility`; required evidence: QA, owner acceptance, lifecycle, integration, release, deployment, and adoption boundary regressions.

## Goal

Make Epic coordination honor the selected executor and safely retire temporary visible child tasks only after verified durable disposition.

## Non-Goals

- Deleting tasks, branches, worktrees, or transcripts.
- Retiring the coordinator or attention-bearing work.
- Replacing integration, QA, closeout, or owner acceptance.

## Users & Context

Owners who want effective persistent-task use without leaving successful subordinate work permanently visible in the sidebar.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Let Epic units execute through coordinator, subagent, persistent task, or peer/team intents from the shared selector.
- Preserve opaque visible-task handles through result verification and explicit durable disposition.
- Model visibility and retirement independently from executor success, using stable intent and observed-result states.
- Issue retirement only after verified integration or explicit verified no-integration disposition and no unresolved attention.
- Retain active, unverified, failed, rejected, orphaned, blocked, awaiting-owner, unintegrated, promoted, explicitly retained, and retirement-failed tasks with reasons.
- Reconcile create, result, disposition, and retirement state across resume without duplicate actions or false claims.

## Acceptance Criteria (Verifiable)

- AC1: Epic runtime consumes the shared executor decision and preserves existing work-packet, dependency, capacity, scope, failure, and single-writer rules across surfaces.
- AC2: A visible subordinate becomes retirement-eligible only after exact result verification and durable disposition; Codex archival is requested and confirmed as separate idempotent states.
- AC3: Every excluded, failed, unknown, stale, interrupted, or owner-retained state preserves the handle and reports why it remains visible; legacy runtime state loads without fabricated cleanup.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Retirement is orthogonal to executor selection and never justifies creating a persistent task.
- Verification alone does not prove integration; durable disposition is a separate gate.
- Archive intent and observed archive acknowledgement are separate events.

## Validation Plan

- Add deterministic runtime, migration, resume, exclusion, idempotency, and summary tests plus the current-Codex proof owned jointly with TASK-072.
