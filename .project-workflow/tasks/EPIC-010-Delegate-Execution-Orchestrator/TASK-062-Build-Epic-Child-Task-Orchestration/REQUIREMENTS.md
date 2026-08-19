# Requirements

## Summary

- Task: TASK-062
- Title: Build Epic Child-Task Orchestration
- Parent AC Coverage: AC3, AC6, AC7, AC9, AC10, AC11, AC12, AC14, AC19
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

- AC3: owner `Delegation Graph and Epic Orchestration children`; required evidence: Decomposition dependency persistence, authority matching, unapproved-child rejection, and parent AC preservation evidence.
- AC6: owner `Epic Orchestration child`; required evidence: Current-host external-contract evidence and live task/worktree creation proving capability and explicit-authority gates.
- AC7: owner `Task and Epic Orchestration children`; required evidence: Captured work packets and enforcement tests for identity, ACs, dependencies, scope, validation, evidence, forbidden actions, and stop conditions.
- AC9: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Capacity-resolution tests and observed host run showing effective concurrency never exceeds available capacity.
- AC10: owner `Task and Epic Orchestration children`; required evidence: Failure-injection tests and live run evidence for descendant blocking, independent continuation, shared-premise halt, safe in-flight completion, and terminal classifications.
- AC11: owner `Task and Epic Orchestration children`; required evidence: Integration/reconciliation tests and retained examples where verified results release dependencies while collision/out-of-scope results do not.
- AC12: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Interruption/resume and orphan tests plus live proof of no duplicate worker or Codex task launch.
- AC14: owner `Task and Epic Orchestration children`; required evidence: Lifecycle/QA/closeout regression tests and live evidence that Delegate cannot self-complete Task or Epic delivery.
- AC19: owner `Epic Orchestration and End-To-End Proof children`; required evidence: Retained disposable current-Codex Epic-mode journey matching every AC19 condition and tied to exact runtime/source identity.

## Goal

Coordinate approved Epic child Tasks as persistent Codex tasks/worktrees when explicitly authorised and currently supported, while preserving decomposition authority, verified dependency release, safe recovery, child-owned QA, and parent closeout gates.

## Non-Goals

- Do not create or approve new Epic children, amend decomposition authority, or batch unrelated standalone Tasks.
- Do not use persistent tasks without explicit owner authority and verified current-host capability.
- Do not let child tasks mutate the parent tracker, acceptance map, delegation runtime state, or parent lifecycle.
- Do not merge, push, release, deploy, mark a child Complete, or self-certify Epic closeout.

## Users & Context

A coordinating Codex task owns one approved/decomposed Epic. Eligible independent children can use isolated persistent tasks/worktrees; dependent children must wait for coordinator verification, and interruption must reconcile the same host tasks without duplicate creation.
Who is affected and in what situation?

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Consume the TASK-060 graph and permit only approved child rows matching the canonical decomposition identity and parent AC coverage.
- Emit a persistent-task creation intent only when explicit owner authority and verified host capability are both present; otherwise fail closed or return an explicit sequential fallback.
- Construct child work packets with exact child/parent identity, ACs, verified predecessors, repository/worktree scope, validation/evidence duties, forbidden parent/delivery actions, and stop conditions.
- Record only sanitised local handles/leases necessary for reconciliation and keep them ignored and subordinate to canonical tracker state.
- Monitor child results and require coordinator inspection of branch/diff, scope, validation, evidence, and collisions before releasing dependants.
- Distinguish child failure, blocked descendants, unaffected siblings, shared-premise halt, safe in-flight work, completion, and orphaned handles.
- Preserve child implementation/QA lifecycle and parent audit/deferral/retro/closeout gates; orchestration cannot certify delivery.
- Retain a dated current-Codex journey showing authorised persistent task/worktree creation, safe concurrent progress where write scopes permit, dependency delay, resume without duplicate creation, and blocked premature closeout.

## Acceptance Criteria (Verifiable)

- AC1: Only approved children matching decomposition identity and parent AC coverage enter the Epic graph; unapproved or drifted rows are rejected. Covers parent AC3.
- AC2: Persistent creation intent requires explicit owner authority plus verified current-host support and never occurs under absent/unknown authority or capability. Covers parent AC6.
- AC3: Each child packet names exact authority, dependencies, repository/worktree scope, validation/evidence, forbidden parent/delivery actions, and stop conditions. Covers parent AC7.
- AC4: Launch eligibility respects dependency verification and available persistent-task capacity, with explicit reduction/fallback reporting. Covers parent AC9.
- AC5: Coordinator verification is required before dependency release, while child failure and shared-premise invalidation produce correct blocked/unaffected/halted/in-flight classifications. Covers parent AC10 and AC11.
- AC6: Reconciliation reuses active/completed task handles, marks missing handles orphaned, and never emits duplicate creation for the same child. Covers parent AC12.
- AC7: Child QA/completion and parent closeout continue to reject missing existing gates regardless of Delegate state. Covers parent AC14.
- AC8: A retained disposable current-Codex journey proves authorised isolated tasks/worktrees, permitted concurrency, dependency waiting, interruption/resume with no duplicate creation, and blocked parent closeout. Covers parent AC19.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Native task creation and monitoring remain host-adapter actions; the host-neutral core validates and emits/records intents and outcomes but cannot call Codex app tools itself.
- Owner approval of this Epic explicitly authorises creation of its planned persistent Codex child tasks/worktrees, but grants no push, merge, release, deployment, external-contact, or cross-repository mutation authority.
- Host identifiers are stored only in ignored local runtime state and are sanitised out of committed receipts.
- Persistent-task capacity is a host input distinct from current-session subagent capacity.
- A monitoring pause is claimed only as reconciliation/resume unless an actual coordinator restart is observed and retained.
- TASK-062 uses the existing standalone/mirrored CLI architecture. Because TASK-061 touches the same helper mirrors, their implementation is serialized unless a later validated write-scope plan proves non-overlap; live safe-concurrency proof uses disjoint disposable child scopes rather than pretending these production children are disjoint.

## Validation Plan

- Add approved-child, authority/capability, work-packet, capacity, verification, failure, resume, orphan, and lifecycle-gate tests in `tests/test_delegate_epic_mode.py`.
- Use the real EPIC-010 dependency chain from an exact committed base for current-Codex task/worktree creation and monitoring; do not invent proof-only children outside decomposition authority.
- Retain `evidence/epic-mode-live-run.json`, runtime-target-source evidence, and dated external-contract-alignment evidence for the exact task tools observed in this session without committing task IDs/cursors/transcripts.
- Run focused tests, full locked regression, strict Doctor, compilation, package build, privacy inspection, and independent child QA.
