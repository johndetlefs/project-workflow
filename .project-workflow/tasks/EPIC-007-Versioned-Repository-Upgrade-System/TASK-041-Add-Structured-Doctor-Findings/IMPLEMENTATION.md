## User Story

As a human, agent, or CI system validating a repository, I want stable structured Doctor findings, so that I can act on the same diagnosis without parsing prose or guessing who owns remediation.

## Parent AC Coverage

- AC2, AC5, AC8

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

- AC2: owner `Add Structured Doctor Findings, Align Documentation And Generated Agent Assets`; required evidence: Tests and captured output proving stable finding codes and equivalent human/machine-readable fields.
- AC5: owner `Define Repository Version Manifest And Compatibility Policy, Integrate Init Version Detection And Upgrade Direction`; required evidence: New/existing init fixtures proving init-only creation and no-mutation upgrade direction, plus canonical upgrade asset refresh.
- AC8: owner `Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply.

## Acceptance Criteria

- [x] AC1: Every finding carries the complete stable structured contract.
- [x] AC2: Versioned JSON output matches human status, counts, accepted state, and exits across representative repository states.
- [x] AC3: Approval, evidence, deferral, and owner-decision gaps remain owner-owned and non-mechanical.
- [x] AC4: Generated-asset drift is project-workflow-owned without implying durable schema repair.
- [x] AC5: Existing human output, fingerprints, warning acceptance, strict behavior, and exits remain compatible.
- [x] AC6: Packaged, template, and local-helper parity plus targeted/full validation pass.

## Validation

- AC1 / parent AC2: structured issue unit tests assert every required field and stable code category.
- AC2 / parent AC2: exact JSON and cross-renderer fixture tests cover clean, warning, strict, error, legacy, and accepted findings.
- AC3 / parent AC8: owner-remediation classification tests for approvals, evidence, deferrals, and decisions.
- AC4 / parent AC5: generated-drift classification test distinguishes managed assets from repository schema state.
- AC5 / parent AC2, AC8: existing Doctor suite remains green without changing established human assertions.
- AC6 / parent AC2: generated helper invocation, full pytest, parity, compilation, and strict Doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define finding catalog and metadata | Extend Doctor issues with stable categories, remediation ownership, and mechanical eligibility while preserving fingerprints. | AC1, AC3, AC4, AC5 | Inspect representative structured issue objects and unchanged fingerprints. | Done |
| 2 | Share Doctor evaluation | Partition visible, accepted, blocking, current, and legacy findings once for both renderers. | AC2, AC5 | Compare evaluation counts and exit decisions across fixtures. | Done |
| 3 | Add versioned JSON renderer | Add `--format json` for doctor and validate with deterministic complete output. | AC1, AC2, AC3, AC4 | Parse exact JSON and compare it with human findings. | Done |
| 4 | Prove compatibility and parity | Add targeted tests, refresh generated mirrors, and run full validation. | AC2, AC5, AC6 | Run packaged and local helper checks, full pytest, and strict Doctor. | Done |

## Parent AC Evidence

- AC2: `DoctorIssue`, `DoctorEvaluation`, the finding-code catalog, and exact JSON/cross-renderer tests prove stable codes and equivalent human/machine fields and exits.
- AC5: Generated mirror drift is `PW_GENERATED_ASSET_DRIFT`, owned by `project-workflow`, and mechanically addressable; no repository-schema diagnosis or init completion claim was added.
- AC8: Approval, evidence, deferral, and owner-decision categories are owned by `owner`, are non-mechanical, remain in JSON even when accepted, and preserve existing accepted-warning fingerprints.

## QA & Code Review

- Verdict: Pass; completed under the owner's autonomous Epic continuation authority.
- Evidence: Five focused structured-Doctor tests passed; full suite passed with 94 tests and 1 existing skip; Python compilation, source/template parity, generated local-helper JSON invocation, and strict Doctor passed with 69 accepted historical warnings hidden.
- Findings: No blocking findings. Codes are stable categories while fingerprints remain issue-instance identities. Repository version findings remain correctly deferred to TASK-044.

## Retro

- Reusable lessons: Human and JSON output must share evaluation and effective-severity logic; accepted findings should remain machine-visible for audit even when hidden from default human output.
- Conventions or agent assets updated: Added the versioned Doctor JSON schema, finite finding catalog, remediation ownership, and mechanical eligibility to packaged, template, and local helpers.
- Follow-up tasks: TASK-044 will map repository compatibility states into this finding model and establish new-only init plus existing-repository upgrade direction.

## Notes

- Task: TASK-041
- Title: Add Structured Doctor Findings
- Created: 2026-07-21
- Scope is unchanged from the approved parent decomposition and owner continuation authority.
