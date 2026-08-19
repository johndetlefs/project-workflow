## User Story

As a Project Workflow consumer, I want Delegate guidance and installation to reflect my host's verified capabilities so that orchestration degrades safely and never pretends unsupported work occurred.

## Parent AC Coverage

- AC6, AC7, AC9, AC13, AC15, AC16, AC20

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

- AC6: owner `Epic Orchestration child`; required evidence: Current-host external-contract evidence and live task/worktree creation proving capability and explicit-authority gates.
- AC7: owner `Task and Epic Orchestration children`; required evidence: Captured work packets and enforcement tests for identity, ACs, dependencies, scope, validation, evidence, forbidden actions, and stop conditions.
- AC9: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Capacity-resolution tests and observed host run showing effective concurrency never exceeds available capacity.
- AC13: owner `Delegation Graph and Host Alignment children`; required evidence: Git/package privacy inspection proving host handles and private runtime data are ignored while canonical evidence remains reviewable.
- AC15: owner `Host Alignment child`; required evidence: Capability-matrix tests and unvalidated-host scenarios proving fail-closed or explicit sequential fallback with truthful claims.
- AC16: owner `Host Alignment child`; required evidence: Generated/source mirror checks, init/upgrade plan/apply/rollback tests, fresh install inspection, and package asset parity.
- AC20: owner `Host Alignment and End-To-End Proof children`; required evidence: README/AGENTS/skill/prompt/install inspection plus positive and negative invocation examples verified against implemented behavior.

## Acceptance Criteria

- [ ] AC1: Tri-state capability/provenance rules govern native launch, capacity, fallback, and truthful claims. Parent AC6, AC9, AC15.
- [ ] AC2: All host adapters carry the bounded packet and authority/lifecycle contract in host-valid syntax. Parent AC7, AC20.
- [ ] AC3: Runtime privacy exclusions hold across Git, generated assets, distributions, Smoke Bomb, and evidence. Parent AC13.
- [ ] AC4: Init/upgrade/collision/rollback and managed mirrors deliver semantically aligned Delegate assets for all hosts. Parent AC16.
- [ ] AC5: README and installed examples precisely distinguish orchestration units, tools, and QA/closeout boundaries. Parent AC20.

## Validation

- AC1: Verified/unsupported/unknown capability and capacity matrix with requested/effective executor and downgrade reasons.
- AC2: Exact Codex/GitHub/Claude/Cursor asset snapshots and no-literal-Copilot-placeholder assertions.
- AC3: `git check-ignore`, Git/package/Smoke Bomb inventories, and hostile private-runtime content tests.
- AC4: Parameterised init plus upgrade plan/apply/no-op/rollback and user-owned `.new` collision tests; helper/source/install parity.
- AC5: Positive/negative invocation examples checked against CLI/adapter behavior.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Capability Contract | Implement tri-state runtime capability/provenance evaluation, capacity bounds, and explicit fallback/block reporting. | AC1 | Run full capability matrix and inspect truthful requested/effective outputs. | To Do |
| 2 | Host Adapter Guidance | Rewrite Codex and common host Delegate contracts plus Planner/Epic/Implement/QA guidance using host-valid syntax. Depends on row 1. | AC2 | Inspect generated outputs for all four hosts and verify packet/authority/failure/QA invariants. | To Do |
| 3 | Managed Asset And Upgrade Alignment | Add runtime ignore, asset/schema migration as required, install/upgrade mirrors, collision handling, fingerprints, no-op, and rollback. Depends on row 2. | AC3, AC4 | Run parameterised install/upgrade/collision/rollback fixtures and inspect Git/package privacy. | To Do |
| 4 | Release And Doctor Coverage | Extend semantic parity, Doctor, release-contract, exact-wheel, package inventory, and Smoke Bomb checks. Depends on row 3. | AC3, AC4 | Run focused distribution and generated-helper parity gates. | To Do |
| 5 | Documentation Contract | Update README and installed managed guidance with positive/negative examples and precise unit/tool/gate boundaries. Depends on rows 2-4. | AC5 | Verify every example against actual CLI/adapter behavior. | To Do |
| 6 | Child QA Handoff | Run focused/full tests, strict Doctor, build/package/privacy checks, record evidence, and submit to independent QA. Depends on row 5. | AC1, AC2, AC3, AC4, AC5 | Review commands, results, cross-host proof limits, and unresolved `.new` behavior. | To Do |

## Parent AC Evidence

- AC6, AC7, AC9, AC13, AC15, AC16, AC20: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-063
- Title: Align Host Adapters, Managed Assets, And Upgrade
- Created: 2026-08-19
