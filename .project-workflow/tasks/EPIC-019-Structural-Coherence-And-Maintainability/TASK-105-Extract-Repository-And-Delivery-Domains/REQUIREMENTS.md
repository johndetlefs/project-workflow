# Requirements

## Summary

- Task: TASK-105
- Title: Extract Repository And Delivery Domains
- Parent AC Coverage: AC2, AC3, AC4, AC10, AC11
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Extract repository installation, compatibility, operational status, work-item lifecycle, evidence,
upgrade, smoke-bomb, and Doctor behaviour into cohesive modules behind the stable CLI facade.
Preserve every v0.9.0 command, schema, generated path, and repository-local runtime behaviour.

## Intent Spine

- OC1 — Completion capability: A maintainer can change one repository or lifecycle concern in its
  owning module without navigating or editing unrelated coordination/execution code.
- OC2 — Material capabilities: Shared contracts/core utilities, repository/install/upgrade,
  work-item/evidence lifecycle, Doctor, and operational-status modules with explicit imports.
- OC3 — Success journey: Extract one boundary at a time, regenerate the standalone helper, and pass
  focused plus compatibility tests before the next boundary moves.
- OC4 — Successful-but-wrong result: Files are smaller but private cross-domain imports, cycles,
  duplicate definitions, compatibility drift, or hand-maintained bundle edits preserve the old
  coupling.
- OC5 — Exclusions: No coordination/execution/adapter extraction, product redesign, schema/version
  bump, cleanup deletion, or broad final verification campaign.
- OC6 — Assumptions: TASK-104 supplies the architecture, baseline, generator, and compatibility
  rails; temporary compatibility re-exports are allowed only at the CLI facade.
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
- AC10: owner `Rebuild Test And Quality Infrastructure; final proof child`; required evidence: Complete locked suite, strict Doctor, build inspection, and package journeys.
- AC11: owner `Architecture; both extraction children; final proof child`; required evidence: v0.9.0 versus candidate command/schema/path snapshots and representative journey comparison.

## Goal

Remove the repository and delivery half of the monolithic hotspot while making its boundaries,
dependencies, and generated-runtime parity explicit.

## Non-Goals

- Moving coordination, orchestration, delegation, execution-control, or host-adapter behaviour.
- Renaming public APIs or changing workflow semantics.
- Splitting cohesive functions merely to meet a line count.

## Users & Context

Maintainers currently change configuration, upgrades, status, lifecycle, evidence, and Doctor in
one global module where unrelated symbols are visible and tests import private details directly.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Establish a dependency-light core/contracts module for constants, value types, basic file/Markdown
  helpers, configuration, manifests, and templates that are genuinely shared.
- Extract repository installation/assets, compatibility/migrations, upgrades, and smoke-bomb into a
  cohesive repository module.
- Extract backlog, Fix, Task, Epic, approval, intent, evidence, and lifecycle behaviour into a
  cohesive work-items module.
- Extract Doctor diagnostics and operational-status inspection/rendering into explicit modules with
  one-way dependencies and no domain-to-CLI import.
- Preserve old import access through the CLI compatibility facade while new tests import owning
  modules directly.
- Update the ordered standalone bundle and prove byte parity after every completed extraction.

## Acceptance Criteria (Verifiable)

- AC1: Core/contracts, repository, work-items, Doctor, and operational-status modules each have one
  documented responsibility and pass the architecture dependency/size rules.
- AC2: No extracted definition remains duplicated in authored source, and domain modules do not
  import project_workflow.cli or depend on later layers.
- AC3: project_workflow.cli continues exposing the v0.9.0 compatibility names used by tests and
  integrations while command help, flags, JSON schemas, exit semantics, and paths match baseline.
- AC4: The regenerated standalone runtime is byte-current and passes focused init, upgrade,
  smoke-bomb, backlog/Fix/Task/Epic, status, Doctor, and legacy compatibility tests.
- AC5: Focused and full regression results attribute failures to extraction or pre-existing state;
  no acceptance criterion is satisfied by simply updating a snapshot to new behaviour.

## Open Questions (Answer Needed)

- None. Exact internal module names may follow the architecture map without changing responsibility.

## Decisions (Resolved)

- Keep status separate from Doctor because status is a read-only projection while Doctor owns
  diagnosis, but allow status to call the Doctor interface in the documented dependency direction.
- Keep shared utilities small and policy-free; domain-specific parsing stays with its owner.
- Use explicit imports and facade re-exports rather than wildcard imports.

## Validation Plan

- Run focused repository, upgrade, smoke-bomb, status, lifecycle, evidence, intent, and Doctor tests
  after each extraction group.
- Run architecture/import-cycle and generated-bundle parity checks.
- Compare command/schema/path snapshots with TASK-104 baseline.
- Run the complete locked suite before handing the source to TASK-107.
