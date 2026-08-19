# Requirements

## Summary

- Task: EPIC-010
- Title: Delegate Execution Orchestrator
- Last updated: 2026-08-19

## User Story

As a Project Workflow owner, I want Project Delegate to execute an approved Epic or Task plan through the appropriate Codex tasks, subagents, or coordinating agent while preserving dependencies, authority, workflow state, evidence, recovery, and QA boundaries, so that multi-unit delivery is faster and more reliable than ad hoc task creation without weakening Project Workflow governance.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-19
- Approval note / source: Codex task owner message: Approved. Go for it. (2026-08-19)
- Approved artifact identity: sha256:5e4b09452b861ac5b13fd700c4320fd2702dc4f51eab3808f200f6e3ceb83038

## Goal

Turn `project-delegate` from a prompt-only description into a host-aware execution orchestrator that consumes existing approved Project Workflow plans, selects the correct execution surface, supervises dependency-aware delivery, and returns trustworthy evidence to the canonical Epic or Task lifecycle.

## Non-Goals

- Inventing, approving, decomposing, or materially changing requirements on behalf of the owner.
- Treating unrelated standalone Tasks as one execution graph; coordinated Tasks require an Epic authority boundary.
- Replacing `project-epic`, `project-task`, `project-implement`, `project-qa-review`, or Epic closeout.
- Creating a permanent Codex task for every implementation row.
- Allowing worker agents to own shared tracker, implementation-plan, evidence-index, or lifecycle mutations.
- Granting implicit authority to create branches, commit, push, merge, release, deploy, contact third parties, or mutate registered repositories.
- Building a remote orchestration service, queueing platform, or provider-specific daemon.
- Committing host task IDs, agent IDs, credentials, private task transcripts, or other machine-local execution handles.
- Claiming equivalent parallel or persistent-task support on hosts whose current capabilities have not been verified.

## Users & Context

- Primary user: a Project Workflow owner asking one Codex task to manage approved multi-unit delivery.
- Task-mode context: one Ready Task contains two or more planned implementation rows; some may be safely isolated and delegated to subagents while the coordinating task retains shared-state ownership.
- Epic-mode context: one approved and decomposed Epic contains two or more child Tasks; eligible children may run as separate persistent Codex tasks and worktrees when the owner explicitly authorises task creation.
- Portability context: Project Workflow supports Codex, GitHub Copilot, Claude Code, and Cursor, but host adapters must use verified capabilities and degrade safely rather than pretending unsupported orchestration.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Delegate must accept exactly one approved Project Workflow target per run: an Epic or a Task. It must reject mixed targets and arbitrary collections of unrelated Tasks.
- Epic mode must treat approved child Tasks as execution units, preserve the Epic contract and parent AC mappings, and use persistent Codex tasks/worktrees only when the host supports them and the owner has explicitly authorised their creation.
- Task mode must treat planned implementation rows as execution units, use subagents only for bounded parallel-safe work, keep coupled work with the coordinating agent or run it sequentially, and avoid creating permanent Codex tasks per row.
- Planner and Epic decomposition artifacts must record durable dependency information. Task rows must additionally record write scope and whether parallel execution is safe.
- A deterministic, host-neutral delegation core and CLI surface must resolve the execution graph, validate readiness and dependencies, expose human and versioned JSON status, and reject invalid execution before any worker launch.
- Delegate must validate target identity, approval, readiness, selected unit identity, dependency closure, cycles, executor capability, repository/worktree boundaries, proof obligations, parallel write-scope overlap, and required authority before launch.
- The coordinating Delegate must be the single writer for shared workflow state. Workers must not mutate global or Epic trackers, shared implementation-plan statuses, acceptance maps, delegation runtime state, or target lifecycle.
- Every worker must receive a bounded work packet containing target and unit identity, AC coverage, satisfied dependencies, permitted write/repository scope, required validation and evidence, prohibited actions, and stop conditions.
- Effective concurrency must be derived from the requested or planned limit and currently available host capacity; a universal fixed worker count must not overrun the coordinating host.
- Task lifecycle must move to `In Progress` once before worker execution and to `Testing` only after every required implementation row is integrated and Done. Partial delegated completion must leave the Task `In Progress`.
- Epic child lifecycle and QA must remain child-owned; Delegate may monitor and coordinate children but must not mark a child Complete or begin Epic closeout without the existing evidence, QA, audit, deferral, and retro gates.
- Failure handling must block descendants of a failed unit, preserve unaffected independent work when the shared baseline remains valid, halt new launches globally only when a shared premise is invalidated, and report failed, blocked, halted, in-flight, and unaffected units separately.
- Delegation must be resumable after coordinator interruption without duplicate launches. Canonical workflow documents remain the durable authority; machine-local host handles and leases must live in ignored runtime state and be safely reconcilable or orphanable.
- Delegate must aggregate worker outputs, inspect returned changes and evidence before satisfying dependencies, detect collisions or out-of-scope changes, and expose a sourced final run summary.
- Host adapters must map the host-neutral contract to verified native capabilities. Unsupported persistent-task or subagent behavior must fail closed or degrade to explicit sequential coordination without weakening the contract.
- Generated skills, prompts, AGENTS guidance, README documentation, packaged resources, upgrade planning/apply behavior, source helpers, and installed consumer assets must remain aligned.
- Existing non-delegated Task, Epic, Implement, QA, Retro, status, Doctor, upgrade, workspace, and evidence behavior must remain backward compatible.
- Project Workflow must explain when Delegate should and should not be invoked, including the distinction between Epic child Tasks, Task implementation rows, persistent Codex tasks, and subagents.

## Acceptance Criteria (Verifiable)

- AC1: Given a delegation request, the host-neutral resolver accepts exactly one existing Epic or Task target and rejects mixed targets, unknown units, unrelated Task batches, and work outside the approved plan before execution begins.
- AC2: Given Task-mode planning, every implementation row can record stable dependencies, write scope, and parallel-safety metadata; malformed references, self-dependencies, cycles, missing units, and parallel write-scope overlap are rejected deterministically.
- AC3: Given Epic-mode planning, approved child dependencies are durably recorded and validated against the decomposition plan without changing parent AC authority or allowing unapproved children into the graph.
- AC4: Given a valid target, the delegate planning/status surface returns a deterministic execution graph, readiness results, eligible and blocked units, executor decision, effective concurrency, and provenance in concise human output and schema-versioned JSON without launching work.
- AC5: Given Task mode, independent parallel-safe rows may be assigned to bounded subagents, while coupled, overlapping, or non-parallel-safe rows remain sequential or coordinator-owned; no permanent Codex task is created for an implementation row.
- AC6: Given Epic mode and explicit owner authority, eligible approved child Tasks may be created as persistent Codex tasks with isolated worktrees and monitored by the coordinator; without that authority or host capability, no persistent task is created.
- AC7: Given any worker launch, the work packet names the exact target/unit, ACs, satisfied dependencies, allowed write or repository scope, required validation/evidence, forbidden shared-state and delivery actions, and stop conditions.
- AC8: Given multiple Task-mode workers, only the coordinator mutates shared workflow artifacts and Task lifecycle; the Task moves to `In Progress` once and cannot move to `Testing` while any required implementation row is not Done.
- AC9: Given configured or requested concurrency, effective parallelism never exceeds currently available host child capacity and the output explains any reduction or sequential fallback.
- AC10: Given a unit failure, descendants are blocked, unrelated ready siblings may continue only when the shared baseline remains valid, shared-premise failures stop new launches globally, in-flight work reaches a safe checkpoint, and the final state distinguishes failed, blocked, halted, completed, and unaffected units.
- AC11: Given returned worker output, the coordinator verifies scope, changes, validation, and evidence before marking a unit Done or releasing its dependants; out-of-scope or colliding results remain unsatisfied and are reported.
- AC12: Given coordinator interruption and restart, a delegation run reconciles canonical workflow state with ignored machine-local leases/host handles and resumes without relaunching a unit already running or completed; missing handles are surfaced as orphaned rather than guessed.
- AC13: Given runtime delegation state, host task IDs, agent IDs, cursors, leases, credentials, and private transcripts are excluded from tracked/package artifacts, while canonical plan, lifecycle, validation, and final evidence remain reviewable in existing Project Workflow sources of truth.
- AC14: Given child or Task implementation completion, Delegate hands the result to the existing QA/Review gate and cannot self-certify completion; Epic closeout still requires child completion, QA evidence, parent AC coverage, accepted deferrals, acceptance audit, and retro.
- AC15: Given a host without verified subagent or persistent-task support, the adapter fails closed or performs an explicitly reported sequential fallback without claiming parallel, persistent, monitored, or resumed execution.
- AC16: Given project initialization or canonical upgrade for Codex, GitHub Copilot, Claude Code, or Cursor, all relevant managed Delegate assets, planning guidance, packaged resources, schemas, and generated/source mirrors are aligned; plan/apply fingerprinting and rollback remain intact.
- AC17: Given existing repositories that do not use Delegate, initialization, upgrade, Task/Epic lifecycle, workspace mode, status, Doctor, QA, evidence, smoke-bomb, and packaging behavior remain backward compatible and the complete locked test suite passes.
- AC18: A disposable Task-mode journey proves two disjoint work items execute safely with bounded subagents, an overlapping write scope is rejected before launch, one dependency waits, a failure is reconciled correctly, shared state has one writer, and the Task reaches `Testing` only after every required row is Done.
- AC19: A disposable Epic-mode journey proves approved child Codex tasks/worktrees are created only with explicit authority, independent children can progress concurrently, dependent children wait for verified predecessors, interruption resumes without duplicate task creation, and parent closeout remains blocked until existing gates pass.
- AC20: Documentation and installed guidance give unambiguous positive and negative invocation examples and correctly distinguish Epic, Task, implementation row, Codex task, subagent, Implement, Delegate, QA, and closeout responsibilities.

## Open Questions (Answer Needed)

- None. The exact requirements and AC1-AC20 remain pending the one required owner approval envelope.

## Decisions (Resolved)

- Decision: Keep the public capability name `project-delegate` for compatibility and describe it as the Delegate Execution Orchestrator.
- Decision: Implement two explicit target modes—Epic child-Task orchestration and Task work-item orchestration—under one host-neutral execution contract.
- Decision: Require exactly one Epic or Task target per delegation run; coordinated standalone Tasks must first gain an Epic authority boundary.
- Decision: Use persistent Codex tasks/worktrees for eligible Epic children and bounded subagents for eligible Task rows; keep coupled Task work coordinator-owned or sequential.
- Decision: Make the coordinating Delegate the only shared workflow-state and lifecycle writer.
- Decision: Replace blanket fail-fast with descendant-aware failure propagation plus global halt only for invalidated shared premises.
- Decision: Use capacity-aware concurrency rather than a universal default of four workers.
- Decision: Keep host handles, leases, cursors, and other resumption state machine-local and ignored; do not create a second tracked lifecycle authority.
- Decision: Build deterministic host-neutral graph/state behavior in Project Workflow and keep host-specific spawning/monitoring in thin adapters.
- Decision: Preserve existing QA and Epic closeout as independent proof gates; Delegate coordinates but does not certify completion.
- Decision: Treat this as a new Epic rather than a bounded APP-002 Fix because it introduces new execution modes, durable plan metadata, state/recovery behavior, host adapters, and live journeys.
- Decision: The 2026-08-19 requirements Clarify pass found no unresolved scope, authority, lifecycle, privacy, host-boundary, or validation decision. Current Codex exposes persistent project-task/worktree creation plus task monitoring, and the current agent runtime exposes bounded subagents; those observed capabilities justify the proposed adapters but do not substitute for AC18/AC19 live proof.

## Validation Plan

- Map every parent AC to child-local ACs, automated checks, and retained evidence before child completion and Epic closeout.
- Add deterministic tests for target resolution, dependency parsing, invalid graphs, write-scope collision, executor selection, capacity limiting, work-packet construction, state transitions, failure propagation, reconciliation, orphan handling, privacy boundaries, JSON schema, and non-mutation of read-only planning.
- Add CLI and packaged/generated-helper parity tests across init, upgrade plan/apply, rollback, Doctor, source assets, and installed consumer assets.
- Run the complete locked repository suite with `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`; the UVX packaging test must pass rather than skip.
- Run strict Doctor, compilation, packaging/build checks, `git diff --check`, and focused backward-compatibility tests.
- Execute and retain a disposable realistic Task-mode journey matching AC18; fixture tests alone are an invalid substitute for host/subagent behavior.
- Execute and retain a disposable realistic Epic-mode journey matching AC19 in the current Codex runtime; synthetic prompt assertions or repository-only fixtures are invalid substitutes for task creation, worktree isolation, monitoring, interruption/resume, and closeout behavior.
- For host adapters not exercised live, report support as unvalidated and prove only safe failure/sequential fallback; do not claim cross-host parity from aligned text assets.
- Apply `external-contract-alignment` to current host capability/tool contracts and `runtime-target-source` to fresh installed-consumer journeys. Required evidence must identify the exact host/runtime, package/source revision, target repository, observation method, and positive proof that the target used the intended installed source.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Define Delegation Graph, Plan Metadata, And Runtime State | AC1, AC2, AC3, AC4, AC9, AC12, AC13 | Add durable dependencies/write-scope metadata, a deterministic host-neutral graph and JSON contract, ignored resumable runtime state, and safe validation/status surfaces. |
| Build Task Work-Item Subagent Orchestration | AC5, AC7, AC8, AC9, AC10, AC11, AC12, AC14, AC18 | Implement Task-mode executor selection, bounded work packets, single-writer lifecycle, integration, failure propagation, reconciliation, and the Task-mode journey. Depends on the graph/state child. |
| Build Epic Child-Task Orchestration | AC3, AC6, AC7, AC9, AC10, AC11, AC12, AC14, AC19 | Implement Epic-mode persistent Codex task/worktree creation, monitoring, dependency release, recovery, evidence aggregation, and the Epic-mode journey. Depends on the graph/state child. |
| Align Host Adapters, Managed Assets, And Upgrade | AC6, AC7, AC9, AC13, AC15, AC16, AC20 | Align Codex and other host adapters, safe capability fallback, generated/source mirrors, packaging, schema migration, upgrade plan/apply/rollback, and installed guidance. Depends on both execution-mode children. |
| Prove End-To-End Delegation And Backward Compatibility | AC4, AC10, AC11, AC12, AC14, AC15, AC16, AC17, AC18, AC19, AC20 | Run deterministic and live disposable journeys, full locked regression, strict Doctor, packaging parity, privacy checks, documentation verification, and final proof-boundary review. Depends on all preceding children. |
