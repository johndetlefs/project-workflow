## User Story

As a coordinating Codex task, I want to delegate only safe implementation rows to bounded subagents so that one Task can progress faster without losing dependency, scope, lifecycle, or QA control.

## Parent AC Coverage

- AC5, AC7, AC8, AC9, AC10, AC11, AC12, AC14, AC18

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

## Acceptance Criteria

- [ ] AC1: Executor selection uses parallel safety, write scope, dependencies, and observed capacity and never creates per-row persistent tasks. Parent AC5, AC9.
- [ ] AC2: Launch packets are complete, bounded, and prohibit shared-state and delivery mutations. Parent AC7.
- [ ] AC3: Coordinator-only lifecycle and shared-state enforcement blocks premature Testing. Parent AC8, AC14.
- [ ] AC4: Returned work is verified before completion or dependency release. Parent AC11.
- [ ] AC5: Failure and interruption reconciliation preserve descendant and unaffected-work semantics without duplicates. Parent AC10, AC12.
- [ ] AC6: A retained current-Codex Task-mode journey proves the required real worker behavior and proof boundaries. Parent AC18.

## Validation

- AC1: Executor matrix for disjoint, overlap, unsafe, coupled, dependency-blocked, and capacity-limited rows; assert zero persistent task intents.
- AC2: Work-packet schema/content tests and forbidden-action enforcement.
- AC3: Shared-artifact hash/diff tests and lifecycle regression showing To Do rows reject Testing while all Done permits it.
- AC4: Scope, diff, collision, validation, and evidence reconciliation fixtures with dependency release only after acceptance.
- AC5: Descendant failure, unrelated continuation, shared-premise halt, safe in-flight completion, retry, resume, and orphan fixtures.
- AC6: Sanitised `evidence/task-mode-live-run.json` from exact current source/runtime and real bounded subagents.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- |
| 1 | Task Executor And Packet | Implement Task-mode executor selection and bounded packet construction in the standalone/mirrored CLI architecture; TASK-060 graph/state APIs are read-only dependencies. | AC1, AC2 | Run selector/packet matrix and inspect exact payload fields. | To Do | | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_task_mode.py | No |
| 2 | Coordinator Integration Gate | Implement result verification, collision/scope checks, dependency release, and coordinator-only shared-state transitions in the Task-mode module. | AC3, AC4 | Exercise accepted and rejected worker results and compare shared-artifact hashes. | To Do | 1 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_task_mode.py | No |
| 3 | Failure And Resume Semantics | Implement descendant blocking, shared-premise halt, in-flight checkpoints, retry, resume, and orphan classification. | AC5 | Run failure/interruption state-transition matrix. | To Do | 2 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_task_mode.py | No |
| 4 | Testing Lifecycle Gate | Harden Task status so Testing requires every required implementation row Done and cannot be bypassed by ordinary force. | AC3 | Demonstrate rejected incomplete transition with unchanged state, then successful all-Done transition. | To Do | 3 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_task_mode.py | No |
| 5 | Live Task-Mode Journey | Execute the exact AC18 current-Codex journey and retain sanitised runtime-target-source evidence. | AC6 | Inspect source/runtime identity, worker events, scopes, hashes, dependency timing, failure correction, and lifecycle results. | To Do | 1, 2, 3, 4 | .project-workflow/tasks/EPIC-010-Delegate-Execution-Orchestrator/TASK-061-Build-Task-Work-Item-Subagent-Orchestration | No |
| 6 | Child QA Handoff | Run focused/full tests, Doctor/build/privacy checks, record evidence, and submit to independent QA. | AC1, AC2, AC3, AC4, AC5, AC6 | Review commands, results, evidence recipe, and proof limitations. | To Do | 5 | .project-workflow/tasks/EPIC-010-Delegate-Execution-Orchestrator/TASK-061-Build-Task-Work-Item-Subagent-Orchestration, tests/test_delegate_task_mode.py | No |

## Parent AC Evidence

- AC5, AC7, AC8, AC9, AC10, AC11, AC12, AC14, AC18: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-061
- Title: Build Task Work-Item Subagent Orchestration
- Created: 2026-08-19
