# Requirements

## Summary

- Task: TASK-061
- Title: Build Task Work-Item Subagent Orchestration
- Parent AC Coverage: AC5, AC7, AC8, AC9, AC10, AC11, AC12, AC14, AC18
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

- AC5: owner `Task Orchestration child`; required evidence: Executor-selection tests and Task-mode runtime evidence distinguishing subagent, sequential, and coordinator-owned work without per-row Codex tasks.
- AC7: owner `Task and Epic Orchestration children`; required evidence: Captured work packets and enforcement tests for identity, ACs, dependencies, scope, validation, evidence, forbidden actions, and stop conditions.
- AC8: owner `Task Orchestration child`; required evidence: Single-writer tests, shared-artifact diff evidence, lifecycle transition proof, and live rejection of premature `Testing`.
- AC9: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Capacity-resolution tests and observed host run showing effective concurrency never exceeds available capacity.
- AC10: owner `Task and Epic Orchestration children`; required evidence: Failure-injection tests and live run evidence for descendant blocking, independent continuation, shared-premise halt, safe in-flight completion, and terminal classifications.
- AC11: owner `Task and Epic Orchestration children`; required evidence: Integration/reconciliation tests and retained examples where verified results release dependencies while collision/out-of-scope results do not.
- AC12: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Interruption/resume and orphan tests plus live proof of no duplicate worker or Codex task launch.
- AC14: owner `Task and Epic Orchestration children`; required evidence: Lifecycle/QA/closeout regression tests and live evidence that Delegate cannot self-complete Task or Epic delivery.
- AC18: owner `Task Orchestration and End-To-End Proof children`; required evidence: Retained disposable current-Codex Task-mode journey matching every AC18 condition and tied to exact runtime/source identity.

## Goal

Coordinate one approved Task's implementation rows through bounded current-session workers while preserving dependency order, write isolation, coordinator-only workflow state, verifiable integration, recovery, and the independent QA gate.

## Non-Goals

- Do not create persistent Codex tasks or worktrees for implementation rows.
- Do not implement Epic child orchestration or cross-Epic Task batching.
- Do not let workers mutate trackers, implementation status, acceptance maps, evidence indexes, runtime leases, or Task lifecycle.
- Do not mark Review or Complete, self-certify QA, push, merge, release, deploy, or contact third parties.

## Users & Context

A coordinating Codex task has one approved, Ready Project Workflow Task with multiple implementation rows. Some rows are disjoint and safe for bounded subagents; coupled or overlapping rows must remain coordinator-owned or sequential, and returned work is not trusted until inspected.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Consume only a valid TASK-060 graph and select subagent, sequential-worker, or coordinator execution per row from dependencies, parallel safety, write scope, and observed capacity.
- Construct a bounded packet containing target/unit identity, ACs, verified dependencies, allowed paths/repositories, validation/evidence duties, forbidden actions, and stop conditions.
- Make the coordinator the sole writer of shared workflow artifacts, local delegation state, and Task lifecycle.
- Transition the Task to `In Progress` once before worker execution and reject `Testing` while any required implementation row is not Done, including through ordinary force semantics.
- Verify returned diffs, scope, collisions, validations, and evidence before satisfying a row or releasing dependants.
- Propagate unit failure to descendants, allow unaffected siblings only while the shared premise remains valid, halt new launches on shared-premise failure, and classify all terminal/in-flight outcomes.
- Reconcile interruption, retry, active, completed, and orphaned worker state without duplicate launches.
- Retain a sanitised current-Codex Task-mode journey proving real bounded subagent execution without committing agent IDs or transcripts.

## Acceptance Criteria (Verifiable)

- AC1: Disjoint parallel-safe rows may select bounded subagents; overlapping, unsafe, coupled, or excess-capacity rows select sequential/coordinator execution, and no row creates a persistent Codex task. Covers parent AC5 and AC9.
- AC2: Every launch packet includes exact identity, ACs, verified dependencies, write/repository scope, validation and evidence obligations, forbidden shared/delivery actions, and stop conditions. Covers parent AC7.
- AC3: Only the coordinator changes shared workflow state; Task lifecycle enters `In Progress` once and `Testing` is rejected until every required row is integrated and Done. Covers parent AC8 and AC14.
- AC4: Verification of scope, diff, collisions, validation, and evidence is required before a row is Done or its dependants become eligible. Covers parent AC11.
- AC5: Failure and shared-premise handling produce distinct completed, failed, blocked, halted, in-flight, and unaffected sets with safe continuation rules. Covers parent AC10.
- AC6: Resume/retry reconciles active, completed, failed, and orphaned rows without duplicate worker launch. Covers parent AC12.
- AC7: A retained disposable current-Codex journey proves two disjoint bounded subagents, overlap rejection, dependency waiting, failed-result reconciliation and correction, coordinator-only state changes, bounded capacity, and the Testing gate. Covers parent AC18.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- TASK-061 owns Task-mode functions and focused tests inside the existing standalone/mirrored CLI architecture. Because TASK-062 touches the same helper mirrors, the coordinator must serialize or otherwise prove non-overlapping integration rather than assume the two children are parallel-safe.
- Persistent task/worktree creation is forbidden in Task mode even when the host supports it.
- `--force` does not bypass the incomplete-row Testing gate; exceptional recovery requires a separately explicit audited path outside Delegate.
- Worker assertions are inputs only; coordinator inspection is the dependency-release authority.
- Live receipts are sanitised and commit source/runtime identity and observed events, not private agent identifiers or transcripts.

## Validation Plan

- Add executor-selection, packet, capacity, single-writer, Testing-gate, reconciliation, failure-propagation, and resume tests in `tests/test_delegate_task_mode.py` plus focused lifecycle regression tests.
- Run a disposable Task from the exact committed/built source with disjoint, overlapping, dependent, and initially failed rows using real bounded subagents in the current Codex session.
- Retain `evidence/task-mode-live-run.json` and a runtime-target-source claim tied to source commit, installed artifact, target repo/worktree, host/date, observation, hashes, and proof limitations.
- Run focused tests, full locked regression, strict Doctor, compilation, package build, privacy inspection, and child QA.
