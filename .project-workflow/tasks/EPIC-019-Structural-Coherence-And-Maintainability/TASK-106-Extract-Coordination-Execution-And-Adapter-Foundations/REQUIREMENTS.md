# Requirements

## Summary

- Task: TASK-106
- Title: Extract Coordination Execution And Adapter Foundations
- Parent AC Coverage: AC2, AC3, AC4, AC5, AC10, AC11
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Extract orchestration, delegation, coordination, verification, and execution control into cohesive
modules and remove genuinely duplicated adapter foundations. Preserve host-specific behaviour,
bounded execution semantics, receipt meanings, and the explicit uncertified Claude runtime state.

## Intent Spine

- OC1 — Completion capability: Maintainers can change coordination or execution policy in its owner
  module without touching repository lifecycle code or obscuring adapter capability differences.
- OC2 — Material capabilities: Orchestration, delegation, coordination/verification,
  execution-control modules, shared adapter primitives, explicit host adapters, and bundle parity.
- OC3 — Success journey: Extract one policy boundary, run its focused adversarial tests, regenerate
  the standalone helper/adapters, and compare receipts and projections with v0.9.0.
- OC4 — Successful-but-wrong result: Shared code hides different host semantics, a generic base
  class adds indirection without reducing duplication, receipt/control behaviour changes, or Claude
  support is described as runtime-certified.
- OC5 — Exclusions: No host capability expansion, Claude canary, execution-policy redesign, release,
  consumer rollout, or repository/delivery-domain extraction.
- OC6 — Assumptions: TASK-104 supplies the generation/baseline rails and TASK-105 supplies the
  lower-level core contracts on which these domains may depend.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
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

## Goal

Remove the coordination/execution half of the monolithic hotspot and make shared versus host-specific
enforcement behaviour obvious in source and generated installations.

## Non-Goals

- Claiming new runtime coverage or completing EPIC-018.
- Replacing current orchestration, verification, QA/remediation, or release-control semantics.
- Forcing unlike adapters behind one inheritance framework.

## Users & Context

Maintainers currently navigate several thousand lines of orchestration, delegation, coordination,
verification, and execution code inside the CLI plus 14 duplicated top-level adapter helpers.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Extract Task/Epic orchestration and graph/delegation planning/runtime state behind explicit
  interfaces and one-way dependencies.
- Extract durable coordination, verification campaign, execution control, QA/remediation, fixed
  candidate, and release projection/commands without changing schemas or receipt meanings.
- Identify adapter code that is semantically identical, move only that code into a shared
  dependency-free adapter module, and retain explicit Codex/Claude policy and lifecycle code.
- Preserve local copied adapter paths and standalone import fallbacks.
- Keep the Claude adapter fail-closed and documentation/tests explicit that no authenticated real
  Claude Code canary has passed.
- Update the ordered standalone bundle and compatibility facade with no manual mirror editing.

## Acceptance Criteria (Verifiable)

- AC1: Orchestration, delegation, coordination/verification, and execution-control modules satisfy
  the architecture dependency/size rules and contain no duplicated authored definitions.
- AC2: Shared adapter code has one canonical dependency-free implementation only where Codex and
  Claude semantics are identical; host-specific capability, hook, launch, limits, and receipt code
  remains explicit and independently tested.
- AC3: Execution-control schemas, denial/continuation decisions, fixed-candidate semantics,
  verification projections, and typed receipts match v0.9.0 focused baselines.
- AC4: The package and generated local helper/adapters import and execute in both package and copied
  standalone layouts without circular imports or an installed-package requirement.
- AC5: Tests and documentation retain the exact Claude boundary: packaged and fail-closed, but no
  authenticated runtime canary and no certification claim.
- AC6: Focused adversarial suites and the complete locked regression suite pass after regeneration.

## Open Questions (Answer Needed)

- None. Any discovered host-semantic difference stays duplicated explicitly rather than being
  abstracted on appearance alone.

## Decisions (Resolved)

- Prefer shared pure helpers and small data contracts over an adapter inheritance hierarchy.
- Keep orchestration and delegation separate from coordination/execution because graph execution and
  durable owner-facing phase/proof state have different ownership and change reasons.
- Preserve existing JSON schema versions and command names.

## Validation Plan

- Run orchestration, delegation, coordination, verification, execution-control, QA/release-control,
  Codex adapter, and Claude adapter focused suites.
- Compare schema/projection/receipt snapshots with TASK-104 baseline.
- Exercise package and copied standalone import modes with package imports blocked where applicable.
- Regenerate runtime/adapters and run the complete locked suite.
