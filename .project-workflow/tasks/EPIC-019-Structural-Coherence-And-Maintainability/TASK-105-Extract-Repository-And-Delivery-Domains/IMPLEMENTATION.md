## User Story

As a Project Workflow maintainer, I want repository and delivery behaviour owned by cohesive
modules, so that ordinary changes do not require understanding the entire CLI implementation.

## Parent AC Coverage

- AC2, AC3, AC4, AC10, AC11

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
- AC10: owner `Rebuild Test And Quality Infrastructure; final proof child`; required evidence: Complete locked suite, strict Doctor, build inspection, and package journeys.
- AC11: owner `Architecture; both extraction children; final proof child`; required evidence: v0.9.0 versus candidate command/schema/path snapshots and representative journey comparison.

## Acceptance Criteria

- [x] AC1: Core, repository, work-items, Doctor, and status modules satisfy documented boundaries.
- [x] AC2: Extracted authored definitions are unique, imports are explicit and acyclic, and no
  domain imports the CLI.
- [x] AC3: CLI compatibility names and the complete public command/schema/path surface match v0.9.0.
- [x] AC4: Generated standalone and installed helpers are current and pass focused domain journeys.
- [x] AC5: Focused and complete regression suites pass without snapshot-based acceptance drift.

## Validation

- AC1, AC2 / parent AC2: run module metrics, import graph, and source-definition checks.
- AC3 / parent AC11: compare command, schema, path, and compatibility-name snapshots.
- AC4 / parent AC3, AC4: regenerate and run dependency-free focused local-helper journeys.
- AC5 / parent AC10, AC11: run focused suites then the complete locked suite.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/structural-coherence-cleanup` at `86ca8859eb5e331db2505c2ae7230e2bc0030242` plus working-tree candidate; no PR | 557 pytest tests, architecture snapshot, compatibility comparison, deterministic generation, isolated helper | Local only; push/merge/release not authorized | `evidence/architecture-snapshot.json`; `evidence/candidate-compatibility.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Extract shared core and repository lifecycle | Move shared contracts/config/templates plus install, compatibility, upgrade, and smoke-bomb behaviour with explicit imports. | AC1, AC2 | Run repository and upgrade focused tests and architecture checks. | Done | TASK-104 | src/project_workflow; tests | No | bounded-return |
| 2 | Extract work-item and evidence lifecycle | Move backlog, Fix, Task, Epic, approvals, intent, evidence, and lifecycle behaviour into its owner module. | AC1, AC2 | Run lifecycle, intent, evidence, workspace, and legacy tests. | Done | 1 | src/project_workflow; tests | No | bounded-return |
| 3 | Extract Doctor and operational status | Move diagnostics and read-only status projection into explicit one-way modules. | AC1, AC2 | Run Doctor and operational-status suites including accepted historical findings. | Done | 1, 2 | src/project_workflow; tests | No | bounded-return |
| 4 | Restore facade bundle and compatibility | Re-export known compatibility names, regenerate the standalone helper, and compare public/baseline surfaces. | AC3, AC4 | Run command snapshots, mirror parity, and dependency-free domain journeys. | Done | 1, 2, 3 | src/project_workflow; scripts; generated helpers | No | bounded-return |
| 5 | Validate extracted delivery domains | Run focused and complete locked regression and record exact source identity. | AC5 | Inspect the full result and reject any unapproved snapshot change. | Done | 4 | task evidence | No | bounded-return |

## Parent AC Evidence

- AC2: `evidence/architecture-snapshot.json` records ten uniquely owned runtime modules, valid
  one-way dependencies, no duplicate top-level definitions, a 1,235-line entry module, and no
  domain module above 4,483 lines.
- AC3, AC4: deterministic regeneration is current and both generated helpers are byte-identical;
  the isolated repository-local helper reports `project 0.9.0` without package imports.
- AC10: complete locked pytest passed: 557 tests in 89.31 seconds.
- AC11: `evidence/candidate-compatibility.json` matches the v0.9.0 contracts and recursive command
  surface exactly. All existing generated paths remain; the only additive internal path is the
  owner-approved shared adapter foundation `.project-workflow/cli/adapter_common.py`.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: The package facade and isolated generated helper preserve the exact
  recursive command/schema contract; repository, workspace, Doctor and status journeys pass using
  the extracted owners rather than a hidden monolith.
- Reviewer independence: Distinct adversarial read-only pass by the same Coordinator context;
  system policy did not authorize a separate subagent. The review inspected the actual module
  graph, compatibility artifacts, complete diff and executable journeys rather than relying on the
  implementation summary.
- Evidence: 202 focused architecture, Doctor, operational-status, package and workspace tests
  passed in 57.91 seconds; the earlier complete run passed 557 tests in 89.31 seconds;
  `git diff --check`, deterministic generation and strict Doctor passed.
- Findings: None.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-105
- Title: Extract Repository And Delivery Domains
- Created: 2026-08-29
