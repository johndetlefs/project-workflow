## User Story

As a Project Workflow maintainer, I want coordination, execution, and adapter behaviour in explicit
owner modules, so that enforcement changes remain comprehensible without hiding host differences.

## Parent AC Coverage

- AC2, AC3, AC4, AC5, AC10, AC11

## Child Charter

### Inherited Invariants

- `project = project_workflow.cli:main` remains the public package entry point.
- Initialized repositories retain `.project-workflow/cli/workflow` plus a dependency-free Python runtime and current copied adapter paths.
- Public commands, flags, exit semantics, JSON schemas, manifest/asset/repository schema versions, generated paths, and supported agent modes remain compatible with v0.9.0 unless separately approved as a product change.
- Canonical authored modules have one-way dependencies and no circular imports; the CLI imports domain interfaces and domains do not import the CLI.
- The standalone workflow runtime is deterministic generated output with provenance and is never a second authored implementation.
- User-owned workflow records, accepted historical debt, active EPIC-016/EPIC-018 state, and the TASK-102 Claude canary blocker are preserved truthfully.
- One cleanup programme does not become a product redesign, multi-package architecture, arbitrary coverage campaign, public release, or consumer rollout.

### Invalid Substitutes

- Smaller files without cohesive ownership, acyclic dependency direction, or a thin entry facade.
- Moving the current monolith unchanged behind one import or distributing it across arbitrary helper files while preserving global coupling.
- Editing `templates/workflow.py`, `.project-workflow/cli/workflow.py`, generated prompts, or installed skills as if they were canonical authored sources.
- Passing unit tests without exact built-package, generated-bundle, dependency-free local-helper, current/legacy upgrade, and command/schema compatibility evidence.
- Treating configured but unlocked/unexecuted lint or type tools as quality gates.
- Rewriting historical approvals/evidence, deleting unique work, or deleting retained candidate artifacts without preserving the claims that depend on them.
- Rewriting the Constitution with implementation detail instead of fixing code/document structure.
- Calling local validation merged, released, adopted, owner-accepted, or authenticated Claude Code runtime certification.

### Artifact Targets

- `docs/architecture.md`: module/dependency map, source/generated ownership, bundle design, and module-splitting rules.
- A small canonical module set under `src/project_workflow/` with `cli.py` as entry and compatibility facade.
- Deterministic bundle-generation tooling plus generated `src/project_workflow/templates/workflow.py` and source-repository installed mirror parity.
- Shared adapter foundation where host semantics are identical, with explicit Codex/Claude modules.
- Product-boundary tests, shared fixtures, command/schema snapshots, architecture checks, and exact candidate journeys.
- Locked Ruff/mypy development dependencies and enforced CI checks.
- Concise README and a small contributor/maintenance/release documentation hierarchy with tested current identity and generated-surface ownership.
- A cleanup disposition ledger for empty directories, ignored output, worktrees/branches, prototypes, binary evidence, generated copies, and historical workflow records.

### Parent AC Proof Ownership

- AC2: owner `Both extraction children; Rebuild Test And Quality Infrastructure`; required evidence: Module metrics, import graph, thin CLI, and architecture gate.
- AC3: owner `Establish Canonical Architecture And Bundle Contract`; required evidence: Deterministic regeneration receipt, provenance marker, and byte parity.
- AC4: owner `Architecture; both extraction children; final proof child`; required evidence: Disposable dependency-free local-helper and compatibility journeys.
- AC5: owner `Extract Coordination Execution And Adapter Foundations`; required evidence: Shared-foundation diff, host-specific contract tests, and explicit Claude boundary.
- AC10: owner `Rebuild Test And Quality Infrastructure; final proof child`; required evidence: Complete locked suite, strict Doctor, build inspection, and package journeys.
- AC11: owner `Architecture; both extraction children; final proof child`; required evidence: v0.9.0 versus candidate command/schema/path snapshots and representative journey comparison.

## Acceptance Criteria

- [x] AC1: Orchestration, delegation, coordination, verification, and execution modules satisfy
  documented boundaries and contain unique authored definitions.
- [x] AC2: Only semantically identical adapter primitives are shared; host-specific behaviour stays
  explicit and independently covered.
- [x] AC3: Execution schemas, projections, decisions, candidate semantics, and receipts match v0.9.0.
- [x] AC4: Package and copied standalone runtime/adapter layouts both execute successfully.
- [x] AC5: Claude remains truthfully packaged fail-closed and uncertified by real runtime canary.
- [x] AC6: Focused adversarial and complete locked regression suites pass.

## Validation

- AC1 / parent AC2: run module metrics, import graph, and source-definition checks.
- AC2, AC5 / parent AC5: run adapter parity/difference tests and inspect retained Claude wording.
- AC3 / parent AC11: compare execution/coordination schema and receipt projections.
- AC4 / parent AC3, AC4: regenerate and exercise package and copied local layouts.
- AC6 / parent AC10, AC11: run focused adversarial suites and full locked pytest.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/structural-coherence-cleanup` at `86ca8859eb5e331db2505c2ae7230e2bc0030242` plus working-tree candidate; no PR | 557 pytest tests, adapter package/copy checks, architecture snapshot, compatibility comparison | Local only; push/merge/release and authenticated Claude canary not authorized/proven | `evidence/architecture-snapshot.json`; `evidence/candidate-compatibility.json`; retained TASK-102 blocked state |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Extract orchestration and delegation | Move Task/Epic orchestration, graph planning, executor selection, and runtime reconciliation behind explicit interfaces. | AC1 | Run orchestration/delegation focused and architecture tests. | Done | TASK-104, TASK-105 core | src/project_workflow; tests | No | bounded-return |
| 2 | Extract coordination and verification | Move durable coordination, boundary/checkpoint, and verification-campaign contracts and commands. | AC1, AC3 | Run coordination and verification focused suites and compare projections. | Done | 1 | src/project_workflow; tests | No | bounded-return |
| 3 | Extract execution and fixed-candidate control | Move sealed execution, QA/remediation, promotion, fixed release, and status projections. | AC1, AC3 | Run execution-control and QA/release adversarial suites. | Done | 2 | src/project_workflow; tests | No | bounded-return |
| 4 | Deduplicate adapter foundations | Extract only proven-identical pure adapter helpers and preserve explicit Codex/Claude behaviour and standalone fallbacks. | AC2, AC4, AC5 | Run both adapter suites in package and copied layouts and inspect Claude boundary. | Done | 3 | src/project_workflow; generated adapter copies; tests | No | bounded-return |
| 5 | Restore bundle facade and validate | Regenerate runtime/adapters, compare execution surfaces, and run focused plus complete regression. | AC3, AC4, AC6 | Verify hashes, schemas, receipts, package/copy imports, and full suite. | Done | 1, 2, 3, 4 | scripts; generated helpers; task evidence | No | bounded-return |

## Parent AC Evidence

- AC2: `evidence/architecture-snapshot.json` records the explicit orchestration, execution, and
  coordination owners in a one-way graph with unique definitions.
- AC3, AC4, AC5: the 169-line `adapter_common.py` owns only the SQLite ledger, identity, scoped-path
  and snapshot primitives already used identically by both hosts. Codex and Claude keep separate
  validation, launch, hook, limit and receipt logic; all three copied files match package source
  and execute in isolated mode.
- AC10: 52 focused adapter/execution tests passed and the complete locked suite passed 557 tests.
- AC11: command and contract/schema snapshots exactly match v0.9.0 and the retained cross-host
  truth boundary is unchanged. TASK-102 remains Blocked, and its package receipt explicitly says
  package/install proof is not authenticated Claude activation or runtime support.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: The package and copied local layouts execute through the exact
  workflow and adapter entry paths; orchestration, coordination, verification and fixed-candidate
  journeys preserve v0.9.0 semantics while TASK-102 remains truthfully blocked on a real Claude
  runtime canary.
- Reviewer independence: Distinct adversarial read-only pass by the same Coordinator context;
  system policy did not authorize a separate subagent. The review inspected the exact adapter
  common/import boundary, host-specific source, blocked TASK-102 evidence, module graph, diff and
  executable tests rather than implementation assertions.
- Evidence: 216 focused architecture, adapter, delegation, coordination, verification, execution
  and QA/release tests passed in 23.94 seconds; the earlier complete run passed 557 tests;
  `git diff --check`, live TASK-102 status and strict Doctor passed.
- Findings: None.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-106
- Title: Extract Coordination Execution And Adapter Foundations
- Created: 2026-08-29
