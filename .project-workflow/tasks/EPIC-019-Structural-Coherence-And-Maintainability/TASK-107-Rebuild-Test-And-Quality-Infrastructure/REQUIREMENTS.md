# Requirements

## Summary

- Task: TASK-107
- Title: Rebuild Test And Quality Infrastructure
- Parent AC Coverage: AC2, AC6, AC7, AC10, AC11
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Make the modular architecture maintainable in practice by aligning tests with product boundaries,
centralizing repeated fixtures, and turning Ruff and mypy from decorative configuration into locked
local and CI gates without weakening the released behavioural suite.

## Intent Spine

- OC1 — Completion capability: Contributors receive fast, domain-specific failures and one complete
  locked validation path before a candidate is considered ready for QA.
- OC2 — Material capabilities: Product-boundary test files, shared fixtures, architecture/parity
  tests, locked Ruff/mypy dependencies, clean source, and enforced CI commands.
- OC3 — Success journey: Change a domain, run its focused suite, regenerate, run Ruff/format/mypy,
  then run the full 548-or-greater behavioural suite and build/package checks.
- OC4 — Successful-but-wrong result: Tests are merely renamed, private coupling grows, test count or
  compatibility coverage drops, lint rules are weakened to green, generated duplicates are checked
  as authored code, or CI differs from documented local commands.
- OC5 — Exclusions: No arbitrary coverage percentage, testing framework replacement, product
  behaviour change, public release, or second broad QA campaign.
- OC6 — Assumptions: TASK-105 and TASK-106 have established final module boundaries; mechanical
  formatting is allowed only with regression proof and no semantic change.
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
- AC6: owner `Rebuild Test And Quality Infrastructure`; required evidence: Test inventory before/after, shared fixtures, split suites, and full regression result.
- AC7: owner `Rebuild Test And Quality Infrastructure`; required evidence: Locked dependency diff and passing local/CI Ruff, format, mypy, pytest, and build gates.
- AC10: owner `Rebuild Test And Quality Infrastructure; final proof child`; required evidence: Complete locked suite, strict Doctor, build inspection, and package journeys.
- AC11: owner `Architecture; both extraction children; final proof child`; required evidence: v0.9.0 versus candidate command/schema/path snapshots and representative journey comparison.

## Goal

Create a test and static-analysis structure that reinforces the new module boundaries and catches
the exact regressions that made the original monolith and manual mirrors risky.

## Non-Goals

- Chasing an arbitrary coverage score or rewriting stable tests for style.
- Running mypy over generated duplicate runtime artifacts.
- Suppressing real findings broadly instead of fixing or narrowly justifying them.

## Users & Context

Maintainers currently rely on a strong 548-test suite, but one Doctor file holds 146 tests across
unrelated products, repeated subprocess helpers exist across many files, and configured static
tools are neither locked nor run.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Split the Doctor catch-all into domain suites while preserving test intent, names where useful,
  legacy fixtures, and total behavioural coverage.
- Centralize repeated command/repository builders in explicit test support without creating a large
  universal fixture abstraction.
- Add architecture, source/generated ownership, deterministic regeneration, documentation identity,
  and v0.9.0 compatibility snapshot tests.
- Lock Ruff and mypy in the development extra and uv lock; use Ruff as formatter/linter and remove
  unused Black configuration unless Black is actually retained and run.
- Fix current Ruff and mypy findings in canonical authored code; scope static checks explicitly and
  narrowly justify any exclusion.
- Run identical locked checks locally and in CI before pytest/build/package journeys.

## Acceptance Criteria (Verifiable)

- AC1: No maintained test file exceeds 2,000 lines; the former Doctor tests are split by product
  boundary and all released legacy fixtures and behavioural cases still collect.
- AC2: Repeated subprocess/repository builders have one small shared implementation where semantics
  match, with domain-specific setup retained locally.
- AC3: Ruff check and format check pass on the declared maintained scope from the locked environment;
  mypy passes on canonical authored production modules; generated duplicate runtime is parity-tested
  rather than statically counted twice.
- AC4: pyproject, uv.lock, local guidance, and CI name the same commands and dependencies; unused
  Black or other aspirational configuration is absent.
- AC5: Architecture and compatibility tests reject cycles, wrong dependency direction, oversized
  mixed-responsibility modules, stale generation, stale release identity, command/schema/path drift,
  and package/local-helper mismatch.
- AC6: The complete locked pytest suite collects at least 548 tests and passes, then build and
  package journeys pass from the same source candidate.

## Open Questions (Answer Needed)

- None. Rule selection may be narrowed only for an evidenced false positive, not to avoid cleanup.

## Decisions (Resolved)

- Use Ruff for both formatting and linting; remove the unused Black block rather than lock two
  overlapping formatters.
- Run mypy on canonical production modules first. Test typing is improved by Ruff and shared helper
  annotations but is not made a blocking mypy scope without a separate demonstrated need.
- Preserve test assertions and compatibility fixtures; file movement is not permission to update
  expected product behaviour.

## Validation Plan

- Compare pytest collection node IDs and count before/after splitting.
- Run locked Ruff check, Ruff format check, and mypy from the new worktree environment.
- Run architecture and deliberately invalid fixture tests.
- Run complete locked pytest, build, package inspection, and package journeys.
