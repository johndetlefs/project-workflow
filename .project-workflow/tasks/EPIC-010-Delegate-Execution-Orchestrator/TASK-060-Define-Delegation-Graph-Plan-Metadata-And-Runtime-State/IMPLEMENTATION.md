## User Story

As a Project Workflow owner, I want an approved plan resolved into a deterministic safe execution graph so that Delegate can coordinate work without relying on prompt interpretation or hidden state.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC9, AC12, AC13

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

## Acceptance Criteria

- [ ] AC1: Exact-target resolution and approved-plan membership fail closed before launch. Parent AC1.
- [ ] AC2: Task and Epic dependency metadata validates cycles, missing references, parallel safety, and write collisions while preserving legacy plans. Parent AC2, AC3.
- [ ] AC3: Read-only planning/status surfaces provide deterministic human and schema-versioned JSON projections. Parent AC4.
- [ ] AC4: Capacity resolution is bounded by observed host availability and reports fallback reasons. Parent AC9.
- [ ] AC5: Machine-local run state reconciles completed, active, and orphaned units without duplicate eligibility. Parent AC12.
- [ ] AC6: Runtime handles remain ignored/private while canonical workflow evidence remains reviewable. Parent AC13.

## Validation

- AC1: Resolver fixtures for valid Task/Epic, mixed target, unknown unit, unrelated Tasks, and unapproved plan membership.
- AC2: Metadata round-trip, malformed/self/missing dependency, cycle, write-overlap, decomposition-authority, and legacy-plan fixtures.
- AC3: Human/JSON snapshots, schema assertions, deterministic ordering, and tracked-file non-mutation checks.
- AC4: Requested-versus-available capacity matrix including zero-child and sequential fallback cases.
- AC5: Initialize, interrupt, reconcile, orphan, canonical-completion, and no-duplicate eligibility fixtures.
- AC6: Git/package ignore inspection and hostile runtime-content privacy tests.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/TASK-060-delegation-graph`; no PR or push authorized | Focused 19/19; full locked suite 281/281; strict Doctor pass; compile/build/wheel/privacy/mirror checks pass | Implemented and QA-passed on the local task branch; local commit recorded in coordinator handoff; not pushed, merged, released, or deployed | `evidence/2026-08-19-validation.md` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- |
| 1 | Plan Metadata Contract | Extend Task implementation and Epic decomposition parsing/templates with dependencies, write scope, and parallel-safety data plus compatibility behavior. | AC2 | Review valid/invalid/legacy fixture matrix and generated artifacts. | Done | | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegation.py | No |
| 2 | Delegation Graph Resolver | Implement exact-target, authority, dependency, collision, executor, and capacity resolution in host-neutral code. Depends on row 1. | AC1, AC2, AC4 | Run focused graph and capacity tests including all rejection paths. | Done | 1 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegation.py | No |
| 3 | Read-Only CLI Projection | Add delegate plan/status human and JSON v1 output with stable ordering and provenance. Depends on row 2. | AC3 | Compare snapshots and confirm no tracked-file changes. | Done | 2 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegation.py | No |
| 4 | Runtime State Reconciliation | Add ignored local run-state initialization and reconciliation for active, completed, and orphaned units. Depends on row 2. | AC5, AC6 | Interrupt/reconcile a disposable run and inspect Git/package contents. | Done | 2 | .gitignore, src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegation.py | No |
| 5 | Child Validation Gate | Run focused/regression tests, strict Doctor, build/package, privacy inspection, and child QA handoff. Depends on rows 3 and 4. | AC1, AC2, AC3, AC4, AC5, AC6 | Review retained commands/results and proof boundaries. | Done | 3, 4 | .project-workflow/tasks/EPIC-010-Delegate-Execution-Orchestrator/TASK-060-Define-Delegation-Graph-Plan-Metadata-And-Runtime-State, tests/test_delegation.py | No |

## Parent AC Evidence

- AC1 / child AC1: exact-target, mixed/repeated-target, unknown-target, lifecycle-authority, unit-membership, and dependency-closure rejection are covered by `tests/test_delegation.py`; all failures occur during plan construction before any runtime mutation.
- AC2 and AC3 / child AC2: six- and nine-column Task tables plus four- and five-column decomposition tables are parsed compatibly; Delegate rejects legacy plans without explicit metadata; focused tests cover malformed/self/missing/cyclic dependencies, write-prefix validation, collisions, authority identity, and legacy behavior.
- AC4 / child AC3: `project delegate plan` and `status` share schema-v1 projections with stable topological ordering, deterministic JSON, concise human output, source hashes, capability provenance, and tracked-tree non-mutation checks.
- AC9 / child AC4: focused capacity tests prove child capacity excludes the coordinator, effective child concurrency is bounded by observed capacity, and zero-capacity/unobserved-host cases explain coordinator sequential fallback.
- AC12 / child AC5: ignored runtime-state tests cover idempotent initialization, canonical completion precedence, same-worktree active resume, missing-handle orphaning, cross-worktree orphaning, and removal of active/orphaned units from launch eligibility. This is host-neutral/disposable-repository proof, not a live Codex interruption or worker-launch claim.
- AC13 / child AC6: the runtime boundary is Git-ignored, atomic state uses an allowlisted schema, hostile transcript/credential fields are rejected, Smoke Bomb removes the ignore reference, and package/Git privacy inspection is part of row 5. This does not claim host-adapter parity.

## QA & Code Review

- Date: 2026-08-19
- Reviewed areas: requirements/AC mapping; exact-target and authority failure modes; legacy/new metadata compatibility; graph determinism; dependency and write-prefix validation; executor/capacity conservatism; CLI read-only behavior; runtime atomicity, reconciliation, privacy, and path containment; source/helper/package parity; Smoke Bomb compatibility; scope and prohibited shared-artifact boundaries.
- Validation evidence: focused delegation suite 19/19; complete locked suite 281/281; strict Doctor reported no issues with 69 accepted warnings hidden; Python compileall passed; sdist and wheel built; the installed wheel exposed all four delegate subcommands; source, template, local helper, and both packaged Python files shared SHA-256 `37f860398aeea7344fdcfb0ce8da830f905930e7c9749882c6f3418cfd05f926`; Git/package privacy checks found no runtime-state artifacts and confirmed the runtime path is ignored.
- Findings: No unresolved findings. QA found and resolved (1) a sanitized-ZIP regression where the managed runtime ignore entry remained as a Project Workflow reference, and (2) a runtime-directory symlink escape that could redirect state writes outside the repository. Regression coverage was added for both behaviors.
- Verdict: Pass. Every child AC has direct automated or artifact evidence. The coordinator-owned child lifecycle and shared trackers were intentionally not changed in this branch.
- Proof boundaries: Tests and disposable repositories prove the host-neutral contract, deterministic CLI projection, privacy schema, and reconciliation rules. They do not prove a live Codex worker launch, real interruption/resume, host adapter parity, parent Epic acceptance, integration, release, deployment, adoption, or owner acceptance.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-060
- Title: Define Delegation Graph, Plan Metadata, And Runtime State
- Created: 2026-08-19
