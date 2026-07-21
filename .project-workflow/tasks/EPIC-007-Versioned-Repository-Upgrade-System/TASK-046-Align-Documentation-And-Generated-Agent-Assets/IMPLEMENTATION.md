## User Story

As an owner or agent, I want one accurate upgrade operating guide, so that I can diagnose, plan, and apply safely without inferring command responsibilities.

## Parent AC Coverage

- AC2, AC3, AC5, AC9

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
- AC3: owner `Build Deterministic Upgrade Planner, Add Historical Migration Registry And Fixtures`; required evidence: Before/after fixture hashes proving zero plan mutation plus complete ordered plan records for every supported source schema.
- AC5: owner `Define Repository Version Manifest And Compatibility Policy, Integrate Init Version Detection And Upgrade Direction`; required evidence: New/existing init fixtures proving init-only creation and no-mutation upgrade direction, plus canonical upgrade asset refresh.
- AC9: owner `Add Historical Migration Registry And Fixtures, Align Documentation And Generated Agent Assets`; required evidence: Passing targeted and full-suite output, strict doctor, backlog validation, and packaged/generated parity evidence.

## Acceptance Criteria

- [x] AC1: README contains complete runnable new-init, one-command upgrade, and advanced automation workflows and boundaries.
- [x] AC2: Compatibility policy and changelog match the delivered contract.
- [x] AC3: Generated agent guidance consistently encodes new-only init, optional Doctor, canonical UVX upgrade, `--yes`, and advanced fingerprinted apply.
- [x] AC4: Documentation and complete validation gates pass.

## Validation

- AC1 / parent AC2, AC3, AC5: README command and boundary assertions.
- AC2 / parent AC9: policy/changelog comparison with constants, migration registry, and tested behavior.
- AC3 / parent AC2, AC3, AC5, AC9: generated guidance search and refresh parity.
- AC4 / parent AC9: full pytest, compilation, backlog validation, and strict Doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Update owner documentation | Align README, structure, health, and upgrade operating sequence. | AC1 | Follow every documented command path. | Done |
| 2 | Align policy and changelog | Record support window, migration, safety, and limitations. | AC2 | Compare docs with constants and tests. | Done |
| 3 | Align generated agent assets | Add command ownership and one-command upgrade safety to managed guidance surfaces. | AC3 | Search packaged and generated assets. | Done |
| 4 | Validate documentation contract | Add assertions, refresh mirrors, and run complete gates. | AC4 | Run pytest, parity, compilation, strict Doctor. | Done |

## Parent AC Evidence

- AC2, AC3, AC5, AC9: README, compatibility policy, changelog, managed instructions, Codex/Cursor guidance, and documentation contract tests align with new-only init and one-command canonical UVX managed-asset/schema upgrade behavior.

## QA & Code Review

- Verdict: Pass; completed under autonomous Epic continuation authority.
- Evidence: Documentation contract test passed; the checked-in legacy fixture now proves mistaken init is a byte-identical no-op and canonical package upgrade with `--yes` installs managed Codex assets, migrates schema, validates, preserves owner findings, and becomes a current no-op in one invocation; final suite passed with 131 tests and 1 environment-gated UVX skip, plus generated refresh, source/template/local parity, backlog validation, compilation, and strict Doctor.
- Findings: A pre-merge review found that splitting managed-asset refresh into init made the public upgrade journey needlessly complex and allowed direct UVX schema upgrade to overstate asset currency. Canonical upgrade now owns both output sets in one deterministic transaction. Release publishing/version increment remains outside EPIC-007 under BL-010.

## Retro

- Reusable lessons: Internal ownership boundaries must not become mandatory user choreography; command names should match intent, while human and machine workflows can expose different review ergonomics over the same deterministic plan.
- Conventions or agent assets updated: README, compatibility policy, changelog, managed AGENTS block, packaged Codex guidance, Cursor rule, CLI mirrors, and documentation assertions.
- Follow-up tasks: BL-010 retains release/version hygiene; no additional EPIC-007 implementation follow-up identified.

## Notes

- Task: TASK-046
- Title: Align Documentation And Generated Agent Assets
- Created: 2026-07-21
- Scope remains inside the approved parent decomposition and autonomous continuation authority.
- Pre-merge documentation correction on 2026-07-21 stayed within AC1 and did not change upgrade behavior or rewrite completed task history.
