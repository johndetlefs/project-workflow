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

- [x] AC1: Only approved children matching decomposition identity and parent AC coverage enter the Epic graph; unapproved or drifted rows are rejected. Covers parent AC3.
- [x] AC2: Persistent creation intent requires explicit owner authority plus verified current-host support and never occurs under absent/unknown authority or capability. Covers parent AC6.
- [x] AC3: Each child packet names exact authority, dependencies, repository/worktree scope, validation/evidence, forbidden parent/delivery actions, and stop conditions. Covers parent AC7.
- [x] AC4: Launch eligibility respects dependency verification and available persistent-task capacity, with explicit reduction/fallback reporting. Covers parent AC9.
- [x] AC5: Coordinator verification is required before dependency release, while child failure and shared-premise invalidation produce correct blocked/unaffected/halted/in-flight classifications. Covers parent AC10 and AC11.
- [x] AC6: Reconciliation reuses active/completed task handles, marks missing handles orphaned, and never emits duplicate creation for the same child. Covers parent AC12.
- [x] AC7: Child QA/completion and parent closeout continue to reject missing existing gates regardless of Delegate state. Covers parent AC14.
- [x] AC8: A retained disposable current-Codex journey proves authorised isolated tasks/worktrees, permitted concurrency, dependency waiting, interruption/resume with no duplicate creation, and blocked parent closeout. Covers parent AC19.

## Validation

- AC1: Approved/decomposition membership, parent-AC drift, and omitted-Complete-dependency matrix.
- AC2: Authority plus plan/runtime capability, source, reconciliation, and capacity matrix with zero-intent counts.
- AC3: Complete serialized packet assertions and bounded live work packets.
- AC4: Capacity shrink/no-expand, dependency wait, repository-scoped collision, and explicit eligibility-reason tests plus live concurrency.
- AC5: Exact identity/scope/diff/evidence/collision verification, failure classifications, and live coordinator-gated release.
- AC6: Persistent resume, orphan, retry, duplicate-state, canonical-precedence, privacy, and stable CLI error regressions plus live same-handle/cursor resume.
- AC7: Existing child Complete and parent closeout negative-gate regressions plus read-only closeout gaps.
- AC8: Sanitised `evidence/epic-mode-live-run.json` plus external-contract-alignment and runtime-target-source claims from this dated session.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/TASK-062-epic-child-orchestration`; no PR or push authorized | Focused 103/103; full locked 365/365; strict Doctor, compile, mirror, build, fresh wheel install, package/privacy, live current-Codex, independent QA, and diff checks pass | Implemented and evidence-complete on the local child branch; not pushed, merged, released, or deployed | `evidence/2026-08-19-validation.md`; `evidence/epic-mode-live-run.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- |
| 1 | Epic Authority And Creation Intent | Implement approved-child/decomposition validation and explicit owner-authority plus host-capability gates for persistent task creation. | AC1, AC2 | Run the authority/capability matrix and inspect zero-create negative paths. | Done | | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_epic_mode.py | No |
| 2 | Child Packet And Verification | Implement bounded child packets, persistent capacity, monitored result inspection, collision handling, and verified dependency release. Depends on row 1. | AC3, AC4, AC5 | Exercise accepted/rejected child results and dependency eligibility. | Done | 1 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_epic_mode.py | No |
| 3 | Failure And Reconciliation | Implement descendant blocking, unrelated continuation, shared-premise halt, safe in-flight state, handle reuse, duplicate prevention, and orphan classification. Depends on row 2. | AC5, AC6 | Run state-transition and interrupted-monitoring fixtures. | Done | 2 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_epic_mode.py | No |
| 4 | Lifecycle Boundary Regression | Prove Delegate state cannot bypass child QA/Complete or parent audit/deferral/retro/closeout gates. | AC7 | Run existing lifecycle gates with otherwise-complete Delegate state. | Done | 3 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_epic_mode.py | No |
| 5 | Live Epic-Mode Journey | Coordinate planned EPIC-010 persistent tasks/worktrees from a committed base, retain safe concurrency/dependency/resume evidence, and sanitise host IDs. Depends on rows 1-4. | AC8 | Inspect dated host contract, creation count, worktree isolation, monitoring events, no-duplicate resume, and closeout rejection. | Done | 4 | .project-workflow/tasks/EPIC-010-Delegate-Execution-Orchestrator/TASK-062-Build-Epic-Child-Task-Orchestration | No |
| 6 | Child QA Handoff | Run focused/full tests, Doctor/build/privacy checks, record evidence, and submit to independent QA. Depends on row 5. | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8 | Review commands, results, evidence recipes, and claims limited to the observed host/session. | Done | 5 | .project-workflow/tasks/EPIC-010-Delegate-Execution-Orchestrator/TASK-062-Build-Epic-Child-Task-Orchestration, tests/test_delegate_epic_mode.py | No |

## Parent AC Evidence

- AC3: Real EPIC-010 resolution and authority-drift tests bind units to decomposition identity, title, dependencies, and parent AC coverage before launch.
- AC6: Current-host negative projections emitted zero persistent executors without authority or the full observed capability set; the authorized final run created isolated persistent tasks only after both gates passed.
- AC7: Packet regressions and final proof prompts carry exact authority, dependencies, repositories/write scope, validation/evidence, forbidden actions, stop conditions, base, fingerprint, and attempt.
- AC9: The coordinator selected a cap of two from requested concurrency three, and both independent tasks were concurrently active; this proves current-host capacity of at least two, not a host maximum.
- AC10: Deterministic tests cover descendant failure, unaffected continuation, shared-premise halt, safe in-flight checkpoint, and terminal classifications; the live run separately proves safe concurrent in-flight work.
- AC11: Coordinator Git inspection—not worker summaries—verified exact base, checkout, worktree, path, bytes/hash, scope, and boundaries before TASK-063 creation.
- AC12: Monitoring resumed with the same two task/cursor aliases and create count unchanged; persistence tests cover exact-handle reuse, missing-handle orphaning, retry, and canonical completion precedence.
- AC14: Child QA/Complete and parent audit/deferral/retro/closeout remained independent; read-only closeout inspection returned 70 audit and 4 retro gaps with no parent mutation.
- AC19: `evidence/epic-mode-live-run.json` retains the sanitized dated authoritative current-Codex journey at exact commit `62e56d68732b354c269bec9be928a81c63379e69`, with all seven earlier diagnostic and three authoritative tasks disclosed.

## QA & Code Review

- Verdict: Pass — independent read-only code and final evidence review on 2026-08-19 found no remaining findings.
- Evidence: Focused 103/103 and full locked 365/365 independently repeated; strict Doctor, compileall, mirror identity, diff integrity, exact scope, JSON/claim schema, package hashes, receipt/validation hashes, live worktree/path/hash facts, and privacy scans passed.
- Findings fixed: immutable plan/runtime capability split-brain; generic Epic reconciliation ambiguity; coordinator-root drift; omitted Complete dependencies; exact Git identities; repository-scoped collisions and eligibility reporting; retry/coordinator-token coverage; runtime privacy/duplicate identity; stable CLI errors; exact AC1–AC8 crosswalk; honest capacity wording.
- Review boundary: QA independently inspected all three authoritative worktrees and ordering, but its separate task-list/monitor request hung; same-handle/cursor resume is supported by the sanitized coordinator receipt plus deterministic regressions rather than a second live monitor observation.

## Retro

- Reusable lessons: Bind current host observations to the immutable plan rather than accepting a richer side channel; treat detached worktrees with uncommitted diffs as a native checkout contract; scope collisions by repository; persist only bounded opaque identities and stable issue codes; describe host capacity as an observed lower bound unless a numeric maximum is exposed; initialize the locked dev extra in fresh proof worktrees before running pytest.
- Conventions or agent assets updated: The shared CLI and both generated/local helper mirrors now enforce these rules; focused Epic tests and child-local evidence capture the durable convention. No global guidance, parent Epic artifact, or unrelated agent asset was changed under TASK-062 authority.
- Follow-up tasks: None created by this child. Parent integration, acceptance-map/audit updates, lifecycle transitions, and any broader host-adapter adoption remain with the parent coordinator.

## Notes

- Task: TASK-062
- Title: Build Epic Child-Task Orchestration
- Created: 2026-08-19
