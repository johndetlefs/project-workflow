## User Story

As an Epic coordinator, I want approved children launched and monitored as isolated persistent Codex tasks only when authorised and supported so that parallel delivery remains governed, resumable, and evidence-based.

## Parent AC Coverage

- AC3, AC6, AC7, AC9, AC10, AC11, AC12, AC14, AC19

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

- AC3: owner `Delegation Graph and Epic Orchestration children`; required evidence: Decomposition dependency persistence, authority matching, unapproved-child rejection, and parent AC preservation evidence.
- AC6: owner `Epic Orchestration child`; required evidence: Current-host external-contract evidence and live task/worktree creation proving capability and explicit-authority gates.
- AC7: owner `Task and Epic Orchestration children`; required evidence: Captured work packets and enforcement tests for identity, ACs, dependencies, scope, validation, evidence, forbidden actions, and stop conditions.
- AC9: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Capacity-resolution tests and observed host run showing effective concurrency never exceeds available capacity.
- AC10: owner `Task and Epic Orchestration children`; required evidence: Failure-injection tests and live run evidence for descendant blocking, independent continuation, shared-premise halt, safe in-flight completion, and terminal classifications.
- AC11: owner `Task and Epic Orchestration children`; required evidence: Integration/reconciliation tests and retained examples where verified results release dependencies while collision/out-of-scope results do not.
- AC12: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Interruption/resume and orphan tests plus live proof of no duplicate worker or Codex task launch.
- AC14: owner `Task and Epic Orchestration children`; required evidence: Lifecycle/QA/closeout regression tests and live evidence that Delegate cannot self-complete Task or Epic delivery.
- AC19: owner `Epic Orchestration and End-To-End Proof children`; required evidence: Retained disposable current-Codex Epic-mode journey matching every AC19 condition and tied to exact runtime/source identity.

## Acceptance Criteria

- [ ] AC1: Epic units remain bound to approved decomposition identity and parent AC authority. Parent AC3.
- [ ] AC2: Persistent creation requires explicit authority and verified capability; absent/unknown inputs produce no creation. Parent AC6.
- [ ] AC3: Child packets, capacity, and coordinator verification enforce scope and dependency release. Parent AC7, AC9, AC11.
- [ ] AC4: Failure, halt, resume, duplicate prevention, and orphan handling preserve deterministic state. Parent AC10, AC12.
- [ ] AC5: Child QA/completion and parent closeout remain independent blocked gates until existing proof is present. Parent AC14.
- [ ] AC6: A retained dated current-Codex journey proves real tasks/worktrees, safe concurrency, dependency delay, and no-duplicate reconciliation. Parent AC19.

## Validation

- AC1: Approved/decomposition membership and drift rejection matrix.
- AC2: Authority and verified/unknown/unsupported capability matrix with creation-intent counts.
- AC3: Packet field, persistent-capacity, scope/diff/evidence verification, and dependency release tests.
- AC4: Descendant failure, unaffected sibling, shared halt, in-flight checkpoint, resume, duplicate, and orphan tests.
- AC5: Existing child Complete and parent closeout negative-gate regressions.
- AC6: Sanitised `evidence/epic-mode-live-run.json` plus external-contract-alignment and runtime-target-source claims from this dated session.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Epic Authority And Creation Intent | Implement approved-child/decomposition validation and explicit owner-authority plus host-capability gates for persistent task creation. | AC1, AC2 | Run the authority/capability matrix and inspect zero-create negative paths. | To Do |
| 2 | Child Packet And Verification | Implement bounded child packets, persistent capacity, monitored result inspection, collision handling, and verified dependency release. Depends on row 1. | AC3 | Exercise accepted/rejected child results and dependency eligibility. | To Do |
| 3 | Failure And Reconciliation | Implement descendant blocking, unrelated continuation, shared-premise halt, safe in-flight state, handle reuse, duplicate prevention, and orphan classification. Depends on row 2. | AC4 | Run state-transition and interrupted-monitoring fixtures. | To Do |
| 4 | Lifecycle Boundary Regression | Prove Delegate state cannot bypass child QA/Complete or parent audit/deferral/retro/closeout gates. | AC5 | Run existing lifecycle gates with otherwise-complete Delegate state. | To Do |
| 5 | Live Epic-Mode Journey | Coordinate planned EPIC-010 persistent tasks/worktrees from a committed base, retain safe concurrency/dependency/resume evidence, and sanitise host IDs. Depends on rows 1-4. | AC6 | Inspect dated host contract, creation count, worktree isolation, monitoring events, no-duplicate resume, and closeout rejection. | To Do |
| 6 | Child QA Handoff | Run focused/full tests, Doctor/build/privacy checks, record evidence, and submit to independent QA. Depends on row 5. | AC1, AC2, AC3, AC4, AC5, AC6 | Review commands, results, evidence recipes, and claims limited to the observed host/session. | To Do |

## Parent AC Evidence

- AC3, AC6, AC7, AC9, AC10, AC11, AC12, AC14, AC19: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-062
- Title: Build Epic Child-Task Orchestration
- Created: 2026-08-19
