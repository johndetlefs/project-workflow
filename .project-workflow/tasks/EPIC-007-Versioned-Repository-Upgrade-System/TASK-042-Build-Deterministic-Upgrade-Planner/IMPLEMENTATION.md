## User Story

As a maintainer, agent, or CI system, I want an exact non-mutating upgrade plan, so that I can review and later apply only a fresh, supported, deterministic repository transformation.

## Parent AC Coverage

- AC3, AC4, AC8

## Child Charter

### Inherited Invariants

- `project init` creates new installations; `project doctor` owns diagnosis; canonical UVX `project upgrade` refreshes managed assets and transforms existing repository state in one transaction.
- Explicit `--plan` mode is non-mutating; normal human upgrade confirms before apply and authorized agents use `--yes`.
- Apply requires confirmation or an explicit automation flag, a clean worktree, a supported source version, and fresh version/hash preconditions.
- The first release applies the complete validated mechanical plan or no changes.
- Migration IDs are immutable and ordered.
- Successful migrations are idempotent; reapplying at the target schema is a no-op.
- Atomic failure cannot leave partial file changes.
- User-owned and unmarked content is preserved.
- Existing project history, approvals, deferrals, evidence, accepted warnings, and unresolved decisions are never silently rewritten into current passing state.
- Unsupported or unrecognized state blocks with a stable finding and concrete next action.
- Human output and machine-readable output describe the same findings and plan.
- Packaged and generated command behavior must remain aligned.

### Invalid Substitutes

- A successful `project init` run is not proof that durable repository state was upgraded.
- A clean old helper or old doctor result is not proof that the repository uses the current schema.
- Package version alone is not a substitute for separate asset and repository-schema versions.
- An agent-authored prose summary is not a substitute for a deterministic machine-readable upgrade plan.
- A passing plan is not proof that apply produced the predicted diff.
- Tests against only freshly initialized repositories are not historical upgrade evidence.
- Backups or Git availability do not permit overwriting user-owned content.
- Accepted warnings, inferred approvals, or stale evidence are not upgraded authority or proof.
- Best-effort partial changes are not an acceptable substitute for atomic application.

### Artifact Targets

- Managed repository metadata at `.project-workflow/manifest.json`
- Upgrade command, plan model, migration registry, and apply engine in `src/project_workflow/cli.py` with behavioral parity in `src/project_workflow/templates/workflow.py`
- Stable structured doctor and upgrade-plan output schemas
- Historical repository fixtures and focused regression coverage under `tests/`
- Generated agent guidance under `src/project_workflow/prompts/`, `src/project_workflow/codex/`, and `src/project_workflow/cursor/`
- README and changelog documentation for init, doctor, and upgrade responsibilities
- EPIC-007 child requirements, implementation plans, evidence, QA, acceptance map/audit, and closeout artifacts

### Parent AC Proof Ownership

- AC3: owner `Build Deterministic Upgrade Planner, Add Historical Migration Registry And Fixtures`; required evidence: Before/after fixture hashes proving zero plan mutation plus complete ordered plan records for every supported source schema.
- AC4: owner `Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Dirty, stale, unsupported, and unrecognized failure tests plus a successful apply whose diff exactly matches the fresh plan.
- AC8: owner `Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply.

## Acceptance Criteria

- [x] AC1: JSON plans contain the complete deterministic versioned contract and reproducible fingerprint.
- [x] AC2: Migration paths are contiguous and unambiguous; invalid registries and unsupported paths block stably.
- [x] AC3: Exact target hashes and clean-worktree requirements are recorded for later apply validation.
- [x] AC4: Owner-owned Doctor findings remain visible unchanged as non-mechanical decisions.
- [x] AC5: Current state no-ops and unsupported states block honestly.
- [x] AC6: Planning is proven non-mutating in human and JSON modes.
- [x] AC7: All CLI mirrors and validation gates pass.

## Validation

- AC1 / parent AC3: exact JSON and fingerprint stability tests.
- AC2 / parent AC3: synthetic valid-chain and invalid-registry matrix.
- AC3 / parent AC4: exact SHA-256, absent target, and clean-worktree precondition assertions.
- AC4 / parent AC8: owner-decision projection tests preserve codes, artifacts, and messages.
- AC5 / parent AC3: current, invalid, future, uninitialized, and legacy-without-registry tests.
- AC6 / parent AC3: before/after recursive tree hashes for both output modes.
- AC7 / parent AC3, AC4, AC8: packaged/local invocation, full pytest, parity, compilation, and strict Doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define plan and migration models | Add immutable migration, step, blocker, decision, precondition, and plan contracts with canonical serialization. | AC1, AC3, AC4 | Inspect exact serialized plan and fingerprint input. | Done |
| 2 | Resolve deterministic paths | Validate registries and resolve one contiguous ordered path without guessing. | AC2, AC5 | Run valid and invalid synthetic registry matrices. | Done |
| 3 | Build non-mutating planner command | Add `project upgrade` human/JSON planning with state, hashes, blockers, and owner decisions. | AC1, AC3, AC4, AC5, AC6 | Compare repeated plans and tree hashes. | Done |
| 4 | Prove parity and regression safety | Add targeted tests, refresh generated mirrors, and run complete validation. | AC6, AC7 | Run packaged/local commands, pytest, parity, compilation, and strict Doctor. | Done |

## Parent AC Evidence

- AC3: Exact current, blocked legacy, and synthetic migration plans prove ordering, stable blockers, human/JSON parity, reproducible fingerprints, and zero mutation; production historical fixtures remain TASK-045.
- AC4: Plans record clean-worktree, repository-state, and SHA-256/absent target preconditions; invalid non-file targets block. Apply enforcement remains TASK-043.
- AC8: Plans project every owner-owned Doctor finding with unchanged code, artifact, message, acceptance state, and fingerprint in both JSON and human output.

## QA & Code Review

- Verdict: Pass; completed under autonomous Epic continuation authority.
- Evidence: Thirteen focused planner tests passed; full suite passed with 107 tests and 1 existing skip; live current-repository planning, generated local-helper invocation, Python compilation, source/template/local parity, and strict Doctor passed.
- Pre-merge correction evidence: The repository plan now includes managed-asset targets and executable modes alongside schema steps; interactive, non-interactive, unsafe-target, historical-fixture, rollback, documentation, and real UVX packaging tests pass in the 132-test suite with no skips.
- Findings: No blocking findings. Production migration registry intentionally remains empty until TASK-045 provides fixture-backed migrations, so unversioned legacy planning blocks honestly rather than guessing.

## Retro

- Reusable lessons: Plan fingerprints must include owner decisions and exact input hashes; target paths must be safe regular files or absent; human output must name decisions rather than only count them.
- Conventions or agent assets updated: Added `project upgrade` planning, migration/plan models, stable blockers, canonical fingerprints, and human/JSON renderers to all CLI mirrors.
- Follow-up tasks: TASK-043 will validate and apply the exact fresh plan; TASK-045 will populate the production registry from historical fixtures.

## Notes

- Task: TASK-042
- Title: Build Deterministic Upgrade Planner
- Created: 2026-07-21
- Scope remains inside the approved parent decomposition and autonomous continuation authority.
