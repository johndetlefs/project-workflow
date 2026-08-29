## User Story

As a Project Workflow maintainer, I want one explicit source architecture and frozen compatibility
baseline, so that modular extraction is safe, reviewable, and unable to hide product drift.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC11

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

## Acceptance Criteria

- [x] AC1: The architecture map and dependency/source-ownership rules are complete and testable.
- [x] AC2: The ordered generator reproduces the standalone runtime deterministically with
  provenance and mirror parity.
- [x] AC3: v0.9.0 command/schema/path and representative journey baselines are retained with source
  identity.
- [x] AC4: The repository-local helper passes with installed-package imports blocked and records
  runtime target/source evidence.
- [x] AC5: Automated architecture gates reject circularity, wrong dependency direction, size-budget
  regression, and stale generated output.

## Validation

- AC1 / parent AC1, AC2: inspect docs/architecture.md and run architecture tests.
- AC2 / parent AC3: run clean generation twice and compare template and installed helper hashes.
- AC3 / parent AC11: regenerate and compare baseline command/schema/path snapshots.
- AC4 / parent AC4: run the disposable no-installed-package helper journey.
- AC5 / parent AC2, AC11: run negative architecture/parity fixtures.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Capture released compatibility baseline | Record command, schema, generated-path, source, public-package, and dependency-free runtime evidence before extraction. | AC3, AC4 | Re-run baseline capture and verify stable checksums and runtime identity. | Done | | tests/baselines; task evidence | No | bounded-return |
| 2 | Define canonical architecture | Write the cohesive module/dependency/source-ownership map and compatibility facade rules. | AC1 | Inspect the module table and dependency direction against current symbol clusters. | Done | 1 | docs/architecture.md | No | bounded-return |
| 3 | Build deterministic runtime generator | Add the ordered manifest, generator, provenance, clean-regeneration command, and mirror update path. | AC2 | Generate twice and compare exact output hashes. | Done | 2 | scripts; src/project_workflow/templates; .project-workflow/cli | No | bounded-return |
| 4 | Enforce architecture and standalone contracts | Add negative architecture, parity, size, import-cycle, and dependency-free helper tests. | AC4, AC5 | Run focused checks including deliberately invalid fixtures. | Done | 2, 3 | tests; task evidence | No | bounded-return |

## Parent AC Evidence

- AC1, AC2, AC3: `docs/architecture.md`, `scripts/runtime-modules.txt`, and
  `scripts/build_runtime_bundle.py`; `tests/test_architecture.py` passed all eight architecture,
  provenance, deterministic generation, negative graph, size-budget, and isolated-helper checks.
- AC4: the generated source template and repository-local helper are byte-identical at
  `sha256:6e1e4a5a9ff1029b818f150eb44ae8364a0f60ae945e18eca7254a96b3a676db`; the helper returned
  `project 0.9.0` under Python isolated mode (`-I`). See `EVIDENCE.json`.
- AC11: `evidence/v0.9.0-compatibility-baseline.json` retains the released command/schema/path
  surface and source identities at `sha256:ae3d3b14a2567d20efa3bb2974a26a7c3b258feaee0075773a0bb9e0b5cb1c27`.

## Validation Impact

- Baseline proof: TASK-104 initial adversarial QA finding recorded in this implementation
- Change summary: Normalized generator terminal newline and regenerated both managed runtimes.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: Coordinator
- Change identity: sha256:172599c6da7d10a2470d134e21f57336701fed36c826ecc2f1fd5c6b602ef59f

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: `tests/test_architecture.py` exercises deterministic generation,
  forbidden graph fixtures, and an isolated dependency-free helper; the retained v0.9.0 baseline
  binds the pre-extraction compatibility surface.
- Reviewer independence: Distinct read-only adversarial pass by the same Coordinator context;
  system policy did not authorize a separate subagent. The pass did not rely on implementation
  assertions and began from the task requirements, exact diff, generated artifacts, and tests.
- Evidence: Focused architecture/release tests passed before review; `git diff --check` then failed
  on both generated runtime files at line 25589.
- Findings: [P1] `scripts/build_runtime_bundle.py` emitted an extra terminal blank line into both
  managed outputs, making the candidate fail the repository whitespace/release gate. Fix the
  generator, regenerate both outputs, and run affected architecture, release-contract, package,
  mirror, diff-check, and Doctor validation.
- Workflow validation impact: affected (`qa-review`) because the correction changes generated
  runtime bytes and the generator contract.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: `git diff --check` passed; 23 architecture, release-contract,
  package-journey and mirror-contract tests passed; deterministic `--check` passed; Doctor's only
  failure was the mechanically stale Intent audit created by recording this review, which was
  refreshed before completion.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-104
- Title: Establish Canonical Architecture And Bundle Contract
- Created: 2026-08-29
