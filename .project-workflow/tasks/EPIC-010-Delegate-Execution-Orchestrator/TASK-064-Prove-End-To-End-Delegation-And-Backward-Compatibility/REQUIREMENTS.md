# Requirements

## Summary

- Task: TASK-064
- Title: Prove End-To-End Delegation And Backward Compatibility
- Parent AC Coverage: AC4, AC10, AC11, AC12, AC14, AC15, AC16, AC17, AC18, AC19, AC20
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

- AC4: owner `Delegation Graph child`; required evidence: Human/JSON snapshots and schema tests proving deterministic graph, readiness, eligibility, blocking, executor, concurrency, provenance, and read-only behavior.
- AC10: owner `Task and Epic Orchestration children`; required evidence: Failure-injection tests and live run evidence for descendant blocking, independent continuation, shared-premise halt, safe in-flight completion, and terminal classifications.
- AC11: owner `Task and Epic Orchestration children`; required evidence: Integration/reconciliation tests and retained examples where verified results release dependencies while collision/out-of-scope results do not.
- AC12: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Interruption/resume and orphan tests plus live proof of no duplicate worker or Codex task launch.
- AC14: owner `Task and Epic Orchestration children`; required evidence: Lifecycle/QA/closeout regression tests and live evidence that Delegate cannot self-complete Task or Epic delivery.
- AC15: owner `Host Alignment child`; required evidence: Capability-matrix tests and unvalidated-host scenarios proving fail-closed or explicit sequential fallback with truthful claims.
- AC16: owner `Host Alignment child`; required evidence: Generated/source mirror checks, init/upgrade plan/apply/rollback tests, fresh install inspection, and package asset parity.
- AC17: owner `End-To-End Proof child`; required evidence: Complete locked regression, strict Doctor, compilation/build/package results, and non-delegated journey checks.
- AC18: owner `Task Orchestration and End-To-End Proof children`; required evidence: Retained disposable current-Codex Task-mode journey matching every AC18 condition and tied to exact runtime/source identity.
- AC19: owner `Epic Orchestration and End-To-End Proof children`; required evidence: Retained disposable current-Codex Epic-mode journey matching every AC19 condition and tied to exact runtime/source identity.
- AC20: owner `Host Alignment and End-To-End Proof children`; required evidence: README/AGENTS/skill/prompt/install inspection plus positive and negative invocation examples verified against implemented behavior.

## Goal

Establish that the integrated Delegate is safe, truthful, distributable, backward compatible, and genuinely useful through deterministic regression plus retained current-Codex Task/Epic journeys tied to the exact shipped source.

## Non-Goals

- Do not use synthetic tests as proof of native task, worktree, subagent, monitoring, or resume behavior.
- Do not generalise dated Codex observations to untested hosts or provider versions.
- Do not mark children/Epic Complete, push, merge, release, deploy, or claim adoption/effectiveness from validation alone.
- Do not retain private task/agent IDs, cursors, credentials, transcripts, or user data in evidence.

## Users & Context

The owner needs a release-grade answer to whether Delegate works better than ad hoc orchestration without weakening Project Workflow. Automated behavior, packaged consumer behavior, actual current-Codex execution, and lifecycle/QA closeout are separate proof layers and must all remain explicit.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Audit every parent AC against child evidence, exact source/runtime identity, and the parent contract's invalid substitutes.
- Run focused graph/Task/Epic/adapter/runtime/CLI suites plus the complete locked repository regression, strict Doctor, compilation, build/package, release-contract, and helper parity gates.
- Prove untouched non-Delegate init, upgrade, Task/Epic lifecycle, workspace, status, Doctor, QA, evidence, Smoke Bomb, and packaging journeys remain compatible.
- Re-run or independently inspect the retained current-Codex Task-mode and Epic-mode journeys, including overlap rejection, dependency timing, failure/recovery, bounded capacity, single writer, persistent task/worktree authority, no-duplicate resume, and blocked premature gates.
- Verify all committed evidence is sanitised, no local handles leak into Git/distributions, and claims identify their observation method and limits.
- Verify documentation and installed assets give accurate positive/negative invocation guidance and that unverified hosts fail closed or report sequential fallback.
- Produce child QA/retro and parent-ready acceptance evidence without substituting Delegate's aggregate report for independent Epic audit/closeout.

## Acceptance Criteria (Verifiable)

- AC1: Human/JSON plan/status, failure/reconciliation, verification, QA-boundary, host-fallback, upgrade/privacy, and documentation checks map to complete retained evidence with no invalid substitute. Covers parent AC4, AC10-AC16, AC20.
- AC2: The complete locked suite passes, strict Doctor has no visible/blocking finding, helper mirrors are byte-identical, compilation/build/package/release-contract succeed, and representative non-Delegate journeys remain unchanged. Covers parent AC17.
- AC3: The Task-mode receipt is tied to exact source/runtime/target identity and proves every AC18 event through real current-Codex subagents, coordinator-observed hashes, and lifecycle results. Covers parent AC18.
- AC4: The Epic-mode receipt is tied to exact source/runtime/target identity and proves every AC19 event through real authorised current-Codex tasks/worktrees and monitoring/reconciliation observations. Covers parent AC19.
- AC5: Git, sdist/wheel, generated assets, Smoke Bomb, and committed evidence contain no private runtime handles/transcripts, and cross-host claims remain limited to tested semantics/capability matrices. Covers parent AC12, AC15, AC16.
- AC6: Independent child QA passes, documentation examples match implemented behavior, and parent acceptance audit/deferral/retro/closeout remain separate pending gates. Covers parent AC14 and AC20.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- TASK-064 verifies and consolidates evidence; it does not add scheduler behavior except for defects discovered through an authorised Fix or explicit child-scope correction.
- Full-suite success is necessary but not sufficient for AC18/AC19 native-host claims.
- A monitoring pause proves resume/reconciliation only; a restart claim requires evidence from a genuine distinct coordinator runtime boundary.
- Receipts record sanitised unit events, counts, hashes, commands/results, capability provenance, and proof limitations, never native private identifiers.
- Final status language distinguishes implemented, validated, packaged, current-host observed, released, adopted, and effective.

## Validation Plan

- Re-run focused Delegate suites and representative legacy journeys, then the exact locked full suite with UVX packaging enabled.
- Run strict Doctor, Python compilation, package build, release-contract/package journeys, helper/prompt/skill parity, `git diff --check`, and Git/package/privacy inventories.
- Independently inspect and, where required, repeat Task/Epic live events against the exact integrated commit and built artifact; retain `evidence/delegation-validation-receipt.json` referencing the child receipts.
- Complete child QA/retro, refresh Epic acceptance map/audit, resolve deferrals, and only then attempt governed parent closeout.
