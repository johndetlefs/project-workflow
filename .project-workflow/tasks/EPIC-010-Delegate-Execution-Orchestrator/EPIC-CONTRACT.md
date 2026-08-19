# Epic Contract

## Summary

- Epic: EPIC-010
- Title: Delegate Execution Orchestrator
- Last updated: 2026-08-19

## Sources of Truth

- Product and authority envelope: this Epic's `REQUIREMENTS.md` and recorded owner approval identity.
- Approved child authority: `DECOMPOSITION.md`, this Epic's `TRACKER.md`, and any owner-approved `AMENDMENTS.md` rows.
- Task-mode plan: the target Task's approved `REQUIREMENTS.md` and AC-mapped `IMPLEMENTATION.md` rows, including dependencies, write scope, parallel safety, and validation.
- Epic-mode plan: the target Epic's approved requirements, contract, decomposition, child tracker, child charters, repository scopes, and parent AC mappings.
- Canonical lifecycle: the existing global tracker, Epic trackers, Task implementation rows, CLI transition rules, QA evidence, acceptance map/audit, deferrals, and retro.
- Host-neutral execution behavior: versioned Project Workflow delegation graph, state-transition, human-output, and JSON contracts in source plus their focused tests.
- Host capability: the current host's callable task/subagent/monitoring contracts observed at validation time; packaged prompt or skill prose alone is not capability proof.
- Packaged delivery: `src/project_workflow/**`, generated/source mirrors, build artifacts, fresh installed-consumer assets, canonical upgrade plan/apply fingerprint, and rollback evidence.

## Invalid Substitutes

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

## Invariants

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

## Artifact Targets

- Host-neutral delegation graph, validation, state-transition, reconciliation, and reporting implementation under `src/project_workflow/` with mirrored helper behavior where required.
- A `project delegate` CLI family with read-only planning/status and controlled runtime-state operations, including schema-versioned JSON.
- Updated Task planning and Epic decomposition metadata for dependencies, Task-row write scope, and parallel safety with backward-compatible migration/upgrade behavior.
- Ignored machine-local delegation runtime state with no competing tracked lifecycle authority.
- Updated Codex `project-delegate` skill, other host Delegate prompts/agents, Planner, Implement, Epic, QA, AGENTS guidance, README, packaged resources, and generated/source mirrors.
- Focused deterministic tests, complete regression coverage, strict Doctor, build/package checks, and upgrade plan/apply/rollback evidence.
- Retained disposable Task-mode and Epic-mode runtime journey artifacts tied to the exact source revision, installed package, host, target repository/worktree, and observation method.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-060 | Resolver tests for exact target identity, approved-plan membership, mixed/unknown/unrelated rejection, and non-launch on failure. |
| AC2 | TASK-060 | Plan-schema, dependency, cycle, malformed-reference, write-scope, and collision validation tests plus migration evidence. |
| AC3 | TASK-060, TASK-062 | Decomposition dependency persistence, authority matching, unapproved-child rejection, and parent AC preservation evidence. |
| AC4 | TASK-060, TASK-064 | Human/JSON snapshots and schema tests proving deterministic graph, readiness, eligibility, blocking, executor, concurrency, provenance, and read-only behavior. |
| AC5 | TASK-061 | Executor-selection tests and Task-mode runtime evidence distinguishing subagent, sequential, and coordinator-owned work without per-row Codex tasks. |
| AC6 | TASK-062, TASK-063 | Current-host external-contract evidence and live task/worktree creation proving capability and explicit-authority gates. |
| AC7 | TASK-061, TASK-062, TASK-063 | Captured work packets and enforcement tests for identity, ACs, dependencies, scope, validation, evidence, forbidden actions, and stop conditions. |
| AC8 | TASK-061 | Single-writer tests, shared-artifact diff evidence, lifecycle transition proof, and live rejection of premature `Testing`. |
| AC9 | TASK-060, TASK-061, TASK-062, TASK-063 | Capacity-resolution tests and observed host run showing effective concurrency never exceeds available capacity. |
| AC10 | TASK-061, TASK-062, TASK-064 | Failure-injection tests and live run evidence for descendant blocking, independent continuation, shared-premise halt, safe in-flight completion, and terminal classifications. |
| AC11 | TASK-061, TASK-062, TASK-064 | Integration/reconciliation tests and retained examples where verified results release dependencies while collision/out-of-scope results do not. |
| AC12 | TASK-060, TASK-061, TASK-062, TASK-064 | Interruption/resume and orphan tests plus live proof of no duplicate worker or Codex task launch. |
| AC13 | TASK-060, TASK-063 | Git/package privacy inspection proving host handles and private runtime data are ignored while canonical evidence remains reviewable. |
| AC14 | TASK-061, TASK-062, TASK-064 | Lifecycle/QA/closeout regression tests and live evidence that Delegate cannot self-complete Task or Epic delivery. |
| AC15 | TASK-063, TASK-064 | Capability-matrix tests and unvalidated-host scenarios proving fail-closed or explicit sequential fallback with truthful claims. |
| AC16 | TASK-063, TASK-064 | Generated/source mirror checks, init/upgrade plan/apply/rollback tests, fresh install inspection, and package asset parity. |
| AC17 | TASK-064 | Complete locked regression, strict Doctor, compilation/build/package results, and non-delegated journey checks. |
| AC18 | TASK-061, TASK-064 | Retained disposable current-Codex Task-mode journey matching every AC18 condition and tied to exact runtime/source identity. |
| AC19 | TASK-062, TASK-064 | Retained disposable current-Codex Epic-mode journey matching every AC19 condition and tied to exact runtime/source identity. |
| AC20 | TASK-063, TASK-064 | README/AGENTS/skill/prompt/install inspection plus positive and negative invocation examples verified against implemented behavior. |
