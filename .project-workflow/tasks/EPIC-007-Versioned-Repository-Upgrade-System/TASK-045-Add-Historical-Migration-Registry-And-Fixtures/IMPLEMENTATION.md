## User Story

As a maintainer of a pre-versioned repository, I want a tested production migration that adopts explicit schema metadata without rewriting history, so that future upgrades have a trustworthy baseline.

## Parent AC Coverage

- AC1, AC3, AC6, AC7, AC8, AC9

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

- AC1: owner `Define Repository Version Manifest And Compatibility Policy, Add Historical Migration Registry And Fixtures`; required evidence: Fixture inspection showing explicit package/asset/schema versions and deterministic classification of pre-versioned state.
- AC3: owner `Build Deterministic Upgrade Planner, Add Historical Migration Registry And Fixtures`; required evidence: Before/after fixture hashes proving zero plan mutation plus complete ordered plan records for every supported source schema.
- AC6: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Injected-failure evidence proving no partial writes and second-apply evidence proving no-op idempotency.
- AC7: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Preservation-canary diffs across tracker, docs, backlog, guidance, config, approvals, deferrals, evidence, and unmarked content.
- AC8: owner `Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply.
- AC9: owner `Add Historical Migration Registry And Fixtures, Align Documentation And Generated Agent Assets`; required evidence: Passing targeted and full-suite output, strict doctor, backlog validation, and packaged/generated parity evidence.

## Acceptance Criteria

- [x] AC1: Immutable production 0-to-1 migration and handler produce the applied manifest ID.
- [x] AC2: Checked-in fixture planning is deterministic, exact, and non-mutating.
- [x] AC3: Apply matches prediction, rollback restores absence, and second apply no-ops.
- [x] AC4: Every non-manifest historical/user canary remains byte-identical.
- [x] AC5: Historical owner findings remain visible and unchanged.
- [x] AC6: Packaged/local end-to-end and all validation gates pass.

## Validation

- AC1 / parent AC1: registry and exact manifest assertions.
- AC2 / parent AC3: fixture tree hashes and exact plan JSON.
- AC3 / parent AC6: success/failure/no-op production tests.
- AC4 / parent AC7: recursive non-target byte comparison.
- AC5 / parent AC8: before/after owner finding comparison.
- AC6 / parent AC9: packaged/local E2E, full pytest, parity, compilation, strict Doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Register legacy migration | Add immutable metadata and pure manifest handler to production registries. | AC1 | Inspect registry and output manifest. | Done |
| 2 | Add checked-in historical fixture | Capture representative durable/history/user-owned artifacts and expected preservation boundary. | AC2, AC4, AC5 | Inspect fixture and hashes. | Done |
| 3 | Prove production end-to-end | Prove mistaken init is a no-op, then run canonical plan, one-command apply, rollback, post-Doctor, and no-op against the fixture. | AC2, AC3, AC4, AC5 | Compare exact plans, diffs, findings, and bytes. | Done |
| 4 | Prove all mirrors and gates | Refresh generated helpers and run complete regression validation. | AC6 | Run packaged/local E2E, pytest, parity, compilation, strict Doctor. | Done |

## Parent AC Evidence

- AC1, AC3, AC6, AC7, AC8, AC9: Checked-in legacy fixture and production tests prove exact manifest-only planning/application, immutable migration recording, rollback to absence, second-apply no-op, non-target byte preservation, and unchanged owner findings.

## QA & Code Review

- Verdict: Pass; completed under autonomous Epic continuation authority.
- Evidence: Production legacy planning/apply tests prove mistaken init no-op, combined one-command upgrade, preservation, rollback, and current no-op behavior; final suite passed with 131 tests and 1 environment-gated UVX skip, plus local-helper parity, compilation, and strict Doctor.
- Findings: No blocking findings. Schema 1 adopts the explicit version contract without falsifying historical document compliance.

## Retro

- Reusable lessons: The baseline migration should establish version authority only; historical validation debt must remain visible rather than being rewritten into compliance.
- Conventions or agent assets updated: Added immutable production migration `PW-0001-legacy-manifest`, pure handler, and checked-in legacy fixture.
- Follow-up tasks: TASK-046 will document the complete init/doctor/upgrade operating model and generated agent guidance.

## Notes

- Task: TASK-045
- Title: Add Historical Migration Registry And Fixtures
- Created: 2026-07-21
- Scope remains inside the approved parent decomposition and autonomous continuation authority.
