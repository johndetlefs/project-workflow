# Requirements

## Summary

- Task: TASK-104
- Title: Establish Canonical Architecture And Bundle Contract
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC11
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Define the one canonical source architecture and deterministic standalone-runtime contract before
production extraction begins. Freeze the released v0.9.0 command, schema, path, and dependency-free
runtime baseline so later modularization cannot pass by silently changing the product.

## Intent Spine

- OC1 — Completion capability: Maintainers know which modules own which behaviour and can regenerate
  every derived runtime from canonical source with one deterministic command.
- OC2 — Material capabilities: Architecture/dependency map, authored/generated ownership rules,
  bundle manifest and generator, v0.9.0 command/schema/path snapshot, and architecture checks.
- OC3 — Success journey: Capture the released baseline, regenerate the current standalone runtime
  without a semantic diff, and prove the snapshot and dependency-free journey are reproducible.
- OC4 — Successful-but-wrong result: A diagram exists but source ownership is still ambiguous, the
  bundle is hand-edited, regeneration is nondeterministic, or compatibility is asserted from tests
  without comparing the released CLI and standalone runtime.
- OC5 — Exclusions: No domain extraction, public command change, package release, consumer rollout,
  product redesign, or claim that the modular candidate is complete.
- OC6 — Assumptions: Released commit 86ca885 and package 0.9.0 are the comparison baseline; the
  current monolith may be the generator's initial single input before later children replace it.
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

- AC1: owner `Establish Canonical Architecture And Bundle Contract`; required evidence: Reviewed architecture map and automated ownership/dependency checks.
- AC2: owner `Both extraction children; Rebuild Test And Quality Infrastructure`; required evidence: Module metrics, import graph, thin CLI, and architecture gate.
- AC3: owner `Establish Canonical Architecture And Bundle Contract`; required evidence: Deterministic regeneration receipt, provenance marker, and byte parity.
- AC4: owner `Architecture; both extraction children; final proof child`; required evidence: Disposable dependency-free local-helper and compatibility journeys.
- AC11: owner `Architecture; both extraction children; final proof child`; required evidence: v0.9.0 versus candidate command/schema/path snapshots and representative journey comparison.

## Goal

Create the architecture and compatibility rails that make subsequent extraction measurable and
reversible rather than a large unbounded rewrite.

## Non-Goals

- Extracting repository, lifecycle, coordination, execution, or adapter domains.
- Declaring the final module layout successful before later children exercise it.
- Changing public behaviour or deleting repository material.

## Users & Context

Maintainers and coding agents need a precise destination and an exact released baseline before
moving definitions out of the 25,583-line CLI.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Document the bounded module map, dependency direction, compatibility facade, source ownership,
  generated-runtime design, and objective split/add rules.
- Capture machine-readable v0.9.0 command help, version/schema constants, generated path inventory,
  and representative JSON/status behaviour from the released source and public package.
- Add a deterministic generator driven by an explicit ordered module manifest. It may initially
  consume the existing canonical CLI as one input, but its contract must support later modular
  inputs without manual output editing.
- Mark generated runtime artifacts with provenance while preserving executable behaviour.
- Add checks for deterministic regeneration, source-repository mirror parity, dependency-free local
  execution, module size limits, CLI direction, and circular internal imports.

## Acceptance Criteria (Verifiable)

- AC1: docs/architecture.md names responsibilities, allowed dependencies, compatibility exports,
  authored/generated assets, bundle ordering, and rules for adding or splitting a module.
- AC2: A checked-in generator and ordered manifest reproduce the standalone runtime byte-for-byte
  after one clean generation and reject stale or manually changed outputs.
- AC3: Retained v0.9.0 baseline artifacts capture the command tree, contract versions, generated
  paths, and representative status/Doctor output with source and package identity.
- AC4: An automated dependency-free journey runs the repository-local helper with package imports
  blocked and records the exact runtime target/source used.
- AC5: Architecture tests fail on a CLI over 2,000 lines after extraction, authored modules over
  5,000 lines without an allowlisted rationale, circular imports, domain-to-CLI imports, stale
  generated output, or missing provenance.

## Open Questions (Answer Needed)

- None. The parent approval establishes the compatibility and modularity boundaries.

## Decisions (Resolved)

- Use one explicit ordered manifest and a simple repository-owned bundler; do not add a framework,
  template engine, second package, or runtime dependency.
- Treat the existing monolith as a temporary first generator input only. Later extraction children
  must replace it in the manifest before the Epic can pass.
- Store baseline receipts as evidence, not as a second behavioural specification.

## Validation Plan

- Run architecture tests and deterministic generation twice from a clean source.
- Compare source-repository mirrors and run the local helper with package imports blocked.
- Capture and checksum released-source/public-package command and contract snapshots.
- Run focused package, init, status, Doctor, and source-parity tests.
