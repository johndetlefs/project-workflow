# Epic Contract

## Summary

- Epic: EPIC-019
- Title: Structural Coherence And Maintainability
- Last updated: 2026-08-29

## Sources of Truth

- Owner meaning: the current Codex task requesting a post-v0.9.0 Strategic Advisor review and a
  full, proportionate structural/documentation cleanup.
- Behavioural baseline: released commit `86ca8859eb5e331db2505c2ae7230e2bc0030242`, package
  `project-workflow==0.9.0`, asset version 8, repository schema version 1, and public command/schema
  surfaces captured before extraction.
- Product outcomes and constraints: `.project-workflow/CONSTITUTION.md`.
- Repository operating rules: `AGENTS.md` and `.project-workflow/guidance.md`.
- Canonical implementation after migration: authored modules under `src/project_workflow/` named by
  `docs/architecture.md`; generated standalone and installed helpers are derived artifacts.
- Compatibility proof: locked tests, command/schema snapshots, deterministic bundle parity, exact
  wheel/sdist inspection, disposable package/local-helper journeys, and strict Doctor.

## Invalid Substitutes

- Smaller files without cohesive ownership, acyclic dependency direction, or a thin entry facade.
- Moving the current monolith unchanged behind one import or distributing it across arbitrary
  helper files while preserving global coupling.
- Editing `templates/workflow.py`, `.project-workflow/cli/workflow.py`, generated prompts, or
  installed skills as if they were canonical authored sources.
- Passing unit tests without exact built-package, generated-bundle, dependency-free local-helper,
  current/legacy upgrade, and command/schema compatibility evidence.
- Treating configured but unlocked/unexecuted lint or type tools as quality gates.
- Rewriting historical approvals/evidence, deleting unique work, or deleting retained candidate
  artifacts without preserving the claims that depend on them.
- Rewriting the Constitution with implementation detail instead of fixing code/document structure.
- Calling local validation merged, released, adopted, owner-accepted, or authenticated Claude Code
  runtime certification.

## Invariants

- `project = project_workflow.cli:main` remains the public package entry point.
- Initialized repositories retain `.project-workflow/cli/workflow` plus a dependency-free Python
  runtime and current copied adapter paths.
- Public commands, flags, exit semantics, JSON schemas, manifest/asset/repository schema versions,
  generated paths, and supported agent modes remain compatible with v0.9.0 unless separately
  approved as a product change.
- Canonical authored modules have one-way dependencies and no circular imports; the CLI imports
  domain interfaces and domains do not import the CLI.
- The standalone workflow runtime is deterministic generated output with provenance and is never a
  second authored implementation.
- User-owned workflow records, accepted historical debt, active EPIC-016/EPIC-018 state, and the
  TASK-102 Claude canary blocker are preserved truthfully.
- One cleanup programme does not become a product redesign, multi-package architecture, arbitrary
  coverage campaign, public release, or consumer rollout.

## Artifact Targets

- `docs/architecture.md`: module/dependency map, source/generated ownership, bundle design, and
  module-splitting rules.
- A small canonical module set under `src/project_workflow/` with `cli.py` as entry and compatibility
  facade.
- Deterministic bundle-generation tooling plus generated
  `src/project_workflow/templates/workflow.py` and source-repository installed mirror parity.
- Shared adapter foundation where host semantics are identical, with explicit Codex/Claude modules.
- Product-boundary tests, shared fixtures, command/schema snapshots, architecture checks, and exact
  candidate journeys.
- Locked Ruff/mypy development dependencies and enforced CI checks.
- Concise README and a small contributor/maintenance/release documentation hierarchy with tested
  current identity and generated-surface ownership.
- A cleanup disposition ledger for empty directories, ignored output, worktrees/branches,
  prototypes, binary evidence, generated copies, and historical workflow records.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-104 | Reviewed architecture map and automated ownership/dependency checks. |
| AC2 | TASK-104, TASK-105, TASK-106, TASK-107 | Module metrics, import graph, thin CLI, and architecture gate. |
| AC3 | TASK-104, TASK-105, TASK-106 | Deterministic regeneration receipt, provenance marker, and byte parity. |
| AC4 | TASK-104, TASK-105, TASK-106 | Disposable dependency-free local-helper and compatibility journeys. |
| AC5 | TASK-106 | Shared-foundation diff, host-specific contract tests, and explicit Claude boundary. |
| AC6 | TASK-107 | Test inventory before/after, shared fixtures, split suites, and full regression result. |
| AC7 | TASK-107 | Locked dependency diff and passing local/CI Ruff, format, mypy, pytest, and build gates. |
| AC8 | TASK-108 | Documentation authority map, link/version checks, and semantic review. |
| AC9 | TASK-108 | Evidence-led disposition ledger and Git/worktree/artifact uniqueness checks. |
| AC10 | TASK-105, TASK-106, TASK-107, TASK-108 | Complete locked suite, strict Doctor, build inspection, and package journeys. |
| AC11 | TASK-104, TASK-105, TASK-106, TASK-107, TASK-108 | v0.9.0 versus candidate command/schema/path snapshots and representative journey comparison. |
| AC12 | TASK-108 | Independent structural and functional QA verdict with findings disposition. |
| AC13 | TASK-108 | Delivery-state record explicitly stopping at local validated source. |
