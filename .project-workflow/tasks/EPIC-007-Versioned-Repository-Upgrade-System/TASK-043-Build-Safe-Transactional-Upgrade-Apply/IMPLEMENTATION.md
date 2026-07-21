## User Story

As a maintainer or automation system, I want to apply only the exact fresh upgrade plan I reviewed, so that deterministic mechanical migrations cannot leave partial state or overwrite undeclared content.

## Parent AC Coverage

- AC4, AC6, AC7, AC8

## Child Charter

### Inherited Invariants

- `project init` owns managed installation and refresh; `project doctor` owns diagnosis; `project upgrade` owns versioned repository-state transformation.
- Upgrade planning is non-mutating by default.
- Apply requires an explicit flag, a clean worktree, a supported source version, and fresh version/hash preconditions.
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

- AC4: owner `Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Dirty, stale, unsupported, and unrecognized failure tests plus a successful apply whose diff exactly matches the fresh plan.
- AC6: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Injected-failure evidence proving no partial writes and second-apply evidence proving no-op idempotency.
- AC7: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Preservation-canary diffs across tracker, docs, backlog, guidance, config, approvals, deferrals, evidence, and unmarked content.
- AC8: owner `Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply.

## Acceptance Criteria

- [x] AC1: Every missing, dirty, stale, blocked, or unhandled apply precondition rejects without mutation.
- [x] AC2: Valid migrations replace exactly declared targets and a repeated current apply no-ops.
- [x] AC3: Failure injection restores every original byte/absence and removes temporary files.
- [x] AC4: All undeclared preservation canaries remain byte-identical.
- [x] AC5: Owner decisions are never migration inputs or transformed authority.
- [x] AC6: Human/JSON apply results are deterministic and complete.
- [x] AC7: All focused, full-suite, parity, compilation, and Doctor gates pass.

## Validation

- AC1 / parent AC4: independent rejection matrix with before/after tree hashes.
- AC2 / parent AC6: synthetic one/multi-file success and second-apply no-op tests.
- AC3 / parent AC6: replacement-index failure matrix with byte/absence restoration assertions.
- AC4 / parent AC7: config, tracker, docs, evidence, guidance, and unmarked canaries outside targets.
- AC5 / parent AC8: handler-input assertions exclude owner decisions and preserve Doctor state.
- AC6 / parent AC4, AC6: exact human/JSON success, failure, and no-op outputs.
- AC7 / parent AC4, AC6, AC7, AC8: packaged/local invocation, full pytest, parity, compilation, and strict Doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define apply contracts and gates | Add explicit apply/fingerprint CLI, result schema, Git/state/hash validation, and handler registration checks. | AC1, AC5, AC6 | Run rejection matrix and inspect stable results. | Done |
| 2 | Compute and validate transformations | Execute pure handlers in memory, constrain outputs to declared targets, and validate final manifest/schema. | AC1, AC2, AC4, AC5 | Compare computed outputs with declared plan targets. | Done |
| 3 | Apply transaction with rollback | Atomically replace targets and restore all originals on any injected or real failure. | AC2, AC3, AC4 | Run replacement-index failure matrix and success/no-op checks. | Done |
| 4 | Prove parity and regression safety | Add focused fixtures, refresh mirrors, and run complete validation. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Run packaged/local apply, pytest, parity, compilation, and strict Doctor. | Done |

## Parent AC Evidence

- AC4: Rejection tests prove explicit fingerprint, clean Git, current plan, state/hash, plan blocker, and registered-handler gates; predicted output hashes are fingerprint-bound and revalidated immediately before replacement.
- AC6: Synthetic success, current no-op, changed-handler, and failure-after-each-replacement tests prove exact apply, idempotency, and restoration.
- AC7: Undeclared output rejection and unmarked canaries prove handlers and filesystem writes remain confined to exact plan targets; historical fixture breadth remains TASK-045.
- AC8: Handlers receive only declared target bytes; owner decisions remain plan metadata and are never handler input or transformed state.

## QA & Code Review

- Verdict: Pass; completed under autonomous Epic continuation authority.
- Evidence: Eight focused apply tests and 21 combined planner/apply tests passed; full suite passed with 115 tests and 1 existing skip; compilation, source/template/local parity, generated helper refresh, and strict Doctor passed.
- Findings: No blocking findings. Production handlers intentionally remain empty until TASK-045 supplies fixture-proven migrations. Rollback failures are surfaced explicitly rather than concealed.

## Retro

- Reusable lessons: A reviewed plan must bind predicted output hashes as well as input hashes; state, hashes, and Git cleanliness need a second check immediately before mutation; rollback must preserve absent-file state as well as bytes.
- Conventions or agent assets updated: Added explicit apply CLI, result schema, pure-handler confinement, predicted-output binding, adjacent atomic replacement, and rollback across all CLI mirrors.
- Follow-up tasks: TASK-045 will register the first immutable production handler and run the same apply engine across historical preservation fixtures.

## Notes

- Task: TASK-043
- Title: Build Safe Transactional Upgrade Apply
- Created: 2026-07-21
- Scope remains inside the approved parent decomposition and autonomous continuation authority.
