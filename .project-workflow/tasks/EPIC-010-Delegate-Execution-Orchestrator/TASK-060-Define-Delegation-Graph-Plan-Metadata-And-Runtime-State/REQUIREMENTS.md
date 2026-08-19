# Requirements

## Summary

- Task: TASK-060
- Title: Define Delegation Graph, Plan Metadata, And Runtime State
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC9, AC12, AC13
- Last updated: 2026-08-19

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

- One delegation run targets exactly one approved Epic or Task.
- Delegate executes existing authority; it does not create scope, approve requirements, or add unplanned children/work items.
- Coordinated standalone Tasks require an Epic; arbitrary Task batches are rejected.
- Epic child Tasks and Task implementation rows remain distinct execution units with distinct executor choices.
- Persistent Codex task creation requires explicit owner authority and verified host support.
- The coordinator is the single writer of shared workflow state and target lifecycle.
- Workers operate inside explicit write/repository scopes and never gain push, merge, release, deployment, external-contact, or cross-repository authority from delegation.
- Dependencies are satisfied by coordinator-verified results, not worker assertion alone.
- Concurrency never exceeds available host capacity and unsafe file overlap is never parallelized.
- A failed unit blocks its descendants; unrelated work continues only while the shared baseline remains valid.
- Canonical workflow artifacts remain the durable authority; machine-local execution handles remain ignored and contain no credentials or private transcripts.
- Task `Testing`, child completion, Epic closeout, and final completion remain gated by existing implementation, evidence, QA, audit, deferral, retro, and owner-authority rules.
- Unsupported host behavior fails closed or degrades explicitly; the system never fabricates support or parity.
- Existing non-delegated behavior remains backward compatible.

### Invalid Substitutes

- A prompt or skill that says work was delegated without observed worker launches, dependency behavior, monitoring, and returned evidence.
- Repository fixtures or mocked scheduler tests presented as proof of current Codex task, worktree, subagent, interruption, or resume behavior.
- A worker's completion claim without coordinator inspection of scope, changes, validation, and required evidence.
- A Task moved to `Testing` while required implementation rows remain incomplete.
- Multiple workers editing shared trackers, implementation-plan status, acceptance maps, evidence indexes, or lifecycle state.
- A fixed configured worker count presented as proof that host capacity was respected.
- Committed task IDs, agent IDs, cursors, leases, credentials, private transcripts, or other machine-local runtime state.
- Generated/source asset parity presented as proof that every supported host can perform persistent or parallel orchestration.
- Unit tests, builds, Doctor, QA prose, or related environments substituted for `external-contract-alignment` or `runtime-target-source` evidence.
- Delegate's own aggregate report substituted for independent QA, Epic acceptance audit, owner-only acceptance, integration, release, deployment, adoption, or effectiveness.

### Artifact Targets

- Host-neutral delegation graph, validation, state-transition, reconciliation, and reporting implementation under `src/project_workflow/` with mirrored helper behavior where required.
- A `project delegate` CLI family with read-only planning/status and controlled runtime-state operations, including schema-versioned JSON.
- Updated Task planning and Epic decomposition metadata for dependencies, Task-row write scope, and parallel safety with backward-compatible migration/upgrade behavior.
- Ignored machine-local delegation runtime state with no competing tracked lifecycle authority.
- Updated Codex `project-delegate` skill, other host Delegate prompts/agents, Planner, Implement, Epic, QA, AGENTS guidance, README, packaged resources, and generated/source mirrors.
- Focused deterministic tests, complete regression coverage, strict Doctor, build/package checks, and upgrade plan/apply/rollback evidence.
- Retained disposable Task-mode and Epic-mode runtime journey artifacts tied to the exact source revision, installed package, host, target repository/worktree, and observation method.

### Parent AC Proof Ownership

- AC1: owner `Delegation Graph child`; required evidence: Resolver tests for exact target identity, approved-plan membership, mixed/unknown/unrelated rejection, and non-launch on failure.
- AC2: owner `Delegation Graph child`; required evidence: Plan-schema, dependency, cycle, malformed-reference, write-scope, and collision validation tests plus migration evidence.
- AC3: owner `Delegation Graph and Epic Orchestration children`; required evidence: Decomposition dependency persistence, authority matching, unapproved-child rejection, and parent AC preservation evidence.
- AC4: owner `Delegation Graph child`; required evidence: Human/JSON snapshots and schema tests proving deterministic graph, readiness, eligibility, blocking, executor, concurrency, provenance, and read-only behavior.
- AC9: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Capacity-resolution tests and observed host run showing effective concurrency never exceeds available capacity.
- AC12: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Interruption/resume and orphan tests plus live proof of no duplicate worker or Codex task launch.
- AC13: owner `Delegation Graph and Host Alignment children`; required evidence: Git/package privacy inspection proving host handles and private runtime data are ignored while canonical evidence remains reviewable.

## Goal

Give every approved Epic or Task a deterministic, inspectable delegation graph and resumable host-neutral state model before any adapter is allowed to launch work.

## Non-Goals

- Do not launch Codex tasks, worktrees, subagents, or other host workers.
- Do not implement Task-mode or Epic-mode result integration, QA, or closeout.
- Do not create a second tracked lifecycle store or commit host execution handles.
- Do not require new metadata on untouched legacy plans unless Delegate is invoked for them.

## Users & Context

Project Workflow owners and host adapters need one stable plan contract that can reject unsafe delegation before launch, explain the exact graph in human and JSON forms, and reconcile an interrupted run without guessing about host state.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Extend implementation-row planning with optional stable dependency, write-scope, and parallel-safety metadata while preserving existing six-column plans.
- Extend Epic decomposition with durable child dependencies that remain matched to approved decomposition authority and parent AC coverage.
- Model one delegation target, ordered execution units, dependency closure, executor decision, readiness/blocking reasons, requested and available capacity, and provenance in host-neutral code.
- Reject unknown or mixed targets, arbitrary Task batches, malformed/self/missing dependencies, cycles, and unsafe parallel write overlap before launch.
- Add `project delegate plan` and `project delegate status` read-only surfaces with deterministic human output and schema-versioned JSON.
- Add controlled run-state initialization/reconciliation primitives whose machine-local files are ignored, contain no credentials or transcripts, and cannot override canonical workflow documents.
- Compute effective concurrency as the minimum safe value derived from plan/request and host capacity, with an explicit reason for reduction or sequential fallback.

## Acceptance Criteria (Verifiable)

- AC1: The resolver accepts exactly one existing approved Epic or Task and rejects mixed, unknown, unrelated, or unplanned unit requests before any launch operation is possible. Covers parent AC1.
- AC2: Task-row metadata round-trips dependencies, write scopes, and parallel safety; malformed references, self-dependencies, cycles, missing units, and unsafe parallel overlap return stable errors while legacy six-column plans remain readable. Covers parent AC2.
- AC3: Epic child dependencies persist in decomposition artifacts, match approved row identity and parent AC coverage, and exclude unapproved children. Covers parent AC3.
- AC4: `delegate plan` and `delegate status` return deterministic graph, readiness, eligible/blocked units, executor decision, effective concurrency, and provenance in human and versioned JSON output without mutating tracked files or launching work. Covers parent AC4.
- AC5: Effective concurrency never exceeds supplied available host capacity and reports why it was reduced or forced sequential. Covers parent AC9.
- AC6: Interrupted state reconciliation distinguishes canonical completed work, active handles, and orphaned/missing handles without duplicate-launch eligibility or invented state. Covers parent AC12.
- AC7: Host handles and leases remain under an ignored machine-local runtime path, are absent from Git/package artifacts, and never contain credentials or private transcripts. Covers parent AC13.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- The durable plan is Markdown metadata in existing Task implementation and Epic decomposition artifacts; no separate tracked graph database is introduced.
- The host-neutral core owns validation, graph/state transitions, work-packet data, and reporting; host adapters own native launch and monitoring calls.
- JSON begins at schema version 1 and uses stable unit ordering for reproducible automation and tests.
- Legacy plans remain valid for ordinary workflow use; Delegate requires sufficient metadata or reports a precise remediation rather than guessing.
- Runtime handles live beneath an ignored `.project-workflow/runtime/delegate/` boundary and canonical workflow documents win every reconciliation conflict.

## Validation Plan

- Add table-driven parser/resolver tests for target identity, authority, dependency closure, cycles, collisions, legacy compatibility, and concurrency.
- Snapshot human and JSON planning/status output and assert read-only Git state.
- Exercise run-state initialize/reconcile/orphan cases in disposable repositories and inspect Git/package contents for private runtime exclusion.
- Run focused tests, the complete locked suite, strict Doctor, compilation, package build, and `git diff --check` before child QA.
