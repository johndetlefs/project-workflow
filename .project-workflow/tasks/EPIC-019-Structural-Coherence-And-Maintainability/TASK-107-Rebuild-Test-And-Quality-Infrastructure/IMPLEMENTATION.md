## User Story

As a Project Workflow contributor, I want focused test suites and real static-quality gates, so
that regressions fail at the owning boundary before a full candidate is assembled.

## Parent AC Coverage

- AC2, AC6, AC7, AC10, AC11

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

## Acceptance Criteria

- [x] AC1: Test files follow product boundaries, remain below 2,000 lines, and preserve at least 548
  collected behavioural tests.
- [x] AC2: Repeated command/repository fixtures are centralized without hiding domain setup.
- [x] AC3: Locked Ruff check/format and canonical-production mypy pass.
- [x] AC4: pyproject, uv.lock, local guidance, and CI use the same real quality commands.
- [x] AC5: Architecture/parity/version/compatibility negative checks enforce the new structure.
- [x] AC6: Full pytest, build, inspection, and package journeys pass from one source candidate.

## Validation

- AC1, AC2 / parent AC6: compare test inventory/node IDs and run split focused suites.
- AC3, AC4 / parent AC7: run locked Ruff check, format check, and mypy locally; inspect CI commands.
- AC5 / parent AC2, AC11: run architecture and invalid-fixture checks.
- AC6 / parent AC10, AC11: run full locked suite, build, inspection, and package journeys.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/structural-coherence-cleanup` at `86ca8859eb5e331db2505c2ae7230e2bc0030242` plus working-tree candidate; no PR | Locked Ruff/format/mypy, 557 pytest tests, deterministic generation, source contract, build and exact-wheel journeys passed | Local only; push, merge, release and adoption not authorized | `evidence/test-inventory.json`; `evidence/quality-gate-receipt.json`; `evidence/package-journeys.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Capture test inventory and extract shared support | Record collected node IDs/count and centralize only repeated command/repository helpers. | AC1, AC2 | Compare baseline and candidate collection and inspect helper responsibilities. | Done | TASK-105, TASK-106 | tests; task evidence | No | bounded-return |
| 2 | Split catch-all suites by product boundary | Move Doctor catch-all cases into cohesive files below 2,000 lines without changing assertions. | AC1 | Run every split suite and compare collected test coverage. | Done | 1 | tests | No | bounded-return |
| 3 | Make Ruff and mypy real | Lock tools, remove unused formatter configuration, fix findings, and define canonical maintained scopes. | AC3, AC4 | Run locked checks and inspect pyproject/uv.lock consistency. | Done | TASK-105, TASK-106 | pyproject.toml; uv.lock; src; tests; scripts | No | bounded-return |
| 4 | Enforce architecture compatibility and docs identity | Add negative gates for imports, sizes, generation, versions, command/schema paths, and package/local parity. | AC5 | Run valid and deliberately invalid fixtures. | Done | 2, 3 | tests; scripts; baselines | No | bounded-return |
| 5 | Validate one complete candidate | Run identical local/CI gates, full pytest, build, inspection, and package journeys. | AC6 | Inspect retained command receipts and artifact identity. | Done | 1, 2, 3, 4 | task evidence; release candidate output | No | bounded-return |

## Parent AC Evidence

- AC2: the architecture suite enforces the manifest-ordered acyclic graph, thin CLI, deterministic
  generation, unique definition ownership and module budgets; all 18 architecture/release-contract
  tests pass.
- AC6: `evidence/test-inventory.json` records 557 collected tests versus the released 548 baseline,
  a 1,417-line largest test file, and a stable sorted node-ID identity. The focused split suites pass
  all 154 cases.
- AC7: Ruff and mypy are locked in `uv.lock`; pyproject, guidance, CI and release workflows run the
  same commands. Ruff check/format and mypy pass with zero production issues and no broad excludes.
- AC10: the final Task 107 source passes all 557 tests, generated bundle currentness, source
  contract, wheel/sdist build, and exact-wheel journeys. See `evidence/quality-gate-receipt.json`.
- AC11: `evidence/package-journeys.json` proves the built package retains the command, path, schema,
  four-agent install, current/legacy upgrade, generated parity and intent journey contracts.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: A contributor can change one domain, run its focused suite, regenerate
  the runtime, execute the documented locked static gates, then pass all 557 tests and exercise the
  exact built wheel across fresh, current and legacy repositories.
- Reviewer independence: Distinct adversarial read-only pass by the same Coordinator context;
  system policy did not authorize a separate subagent. The pass inspected the source/test split,
  rule configuration, CI command identity, negative architecture fixtures, package contents and
  executable journey receipts rather than accepting implementation claims.
- Evidence: `evidence/test-inventory.json`, `evidence/quality-gate-receipt.json` and
  `evidence/package-journeys.json`; locked Ruff/format/mypy passed; 557 tests passed in 85.46
  seconds; exact wheel and sdist built; built-wheel journeys passed.
- Findings: Two issues were found and resolved. The release-source gate still assigned version
  ownership to the retired CLI monolith, so it now points at the canonical contracts module. Ruff
  formatting also occurred after the managed adapters were last synchronized, so all three local
  adapter files were refreshed byte-for-byte. Strict Doctor, all static gates and 172 focused QA
  tests then passed. No open findings remain.

## Retro

- Reusable lessons: Static gates become useful only when they run the canonical authored surface;
  generated mirrors should be parity-tested, and heterogeneous mutation plans need explicit typed
  schemas at their JSON boundary.
- Conventions or agent assets updated: Repository guidance, locked dependency declarations and both
  CI workflows now use one named quality command set. Architecture tests own size/dependency rules.
- Follow-up tasks: None. Documentation hierarchy and final cleanup disposition remain in TASK-108.

## Notes

- Task: TASK-107
- Title: Rebuild Test And Quality Infrastructure
- Created: 2026-08-29
