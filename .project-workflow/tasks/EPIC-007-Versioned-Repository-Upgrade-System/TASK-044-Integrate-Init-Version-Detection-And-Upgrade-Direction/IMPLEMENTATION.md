## User Story

As a maintainer or agent initializing an existing repository, I want init to distinguish managed asset refresh from schema migration, so that it never reports old durable state as current.

## Parent AC Coverage

- AC1, AC5

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

- AC1: owner `Define Repository Version Manifest And Compatibility Policy, Add Historical Migration Registry And Fixtures`; required evidence: Fixture inspection showing explicit package/asset/schema versions and deterministic classification of pre-versioned state.
- AC5: owner `Define Repository Version Manifest And Compatibility Policy, Integrate Init Version Detection And Upgrade Direction`; required evidence: Legacy/current init fixtures proving managed refresh and honest schema/upgrade direction without repository-state mutation.

## Acceptance Criteria

- [x] AC1: Fresh and repeated init create then preserve the exact current manifest.
- [x] AC2: Legacy init refreshes assets without manifest creation or durable-state mutation and directs upgrade.
- [x] AC3: Behind-schema init preserves schema/history while refreshing only managed metadata and directing upgrade.
- [x] AC4: Invalid/future manifests remain byte-identical and block honestly.
- [x] AC5: Doctor emits equivalent stable human/JSON version findings and exits.
- [x] AC6: Current behavior, all mirrors, and validation gates pass.

## Validation

- AC1 / parent AC1: exact fresh/second-init manifest assertions.
- AC2 / parent AC5: legacy tree snapshot, no-manifest, and output assertions.
- AC3 / parent AC5: behind manifest field-preservation and direction assertions.
- AC4 / parent AC1, AC5: invalid/future byte-preservation and blocking output tests.
- AC5 / parent AC5: Doctor human/JSON finding matrix.
- AC6 / parent AC1, AC5: packaged/local runs, full pytest, parity, compilation, and strict Doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Integrate init state detection | Detect before mutation, create only fresh manifests, and safely refresh valid managed metadata. | AC1, AC2, AC3, AC4 | Run state matrix and inspect manifest/tree diffs. | Done |
| 2 | Add honest init direction | Report detected/resulting states and exact upgrade or recovery next actions. | AC2, AC3, AC4 | Compare init output across fixtures. | Done |
| 3 | Add repository Doctor findings | Map compatibility states to explicit structured finding codes and remediation metadata. | AC4, AC5 | Compare human/JSON findings and strict exits. | Done |
| 4 | Prove idempotency and parity | Refresh mirrors and run complete validation. | AC1, AC6 | Run second init, local helper, pytest, parity, compilation, and strict Doctor. | Done |

## Parent AC Evidence

- AC1: Fresh/second init exact-manifest tests plus legacy, behind, invalid, and future state fixtures prove deterministic classification and no false current state.
- AC5: Init output and structured Doctor tests prove explicit state, remediation owner, mechanical eligibility, preservation, and correct upgrade direction.

## QA & Code Review

- Verdict: Pass; completed under autonomous Epic continuation authority.
- Evidence: Ten focused init/version tests passed; full suite passed with 124 tests and 1 existing skip; live current init, local helper refresh, source/template/local parity, compilation, and strict Doctor passed.
- Findings: No blocking findings. Legacy repositories intentionally remain manifest-free until TASK-045 performs the fixture-backed migration.

## Retro

- Reusable lessons: Compatibility must be captured before init creates workflow markers; managed asset refresh may update package/asset provenance but must preserve schema and migration history; invalid/future metadata must never be normalized.
- Conventions or agent assets updated: Added version-aware init output, fresh-manifest creation, safe metadata refresh, and explicit repository-state Doctor findings across CLI mirrors.
- Follow-up tasks: TASK-045 will convert recognized legacy state through the immutable migration registry and preservation fixtures.

## Notes

- Task: TASK-044
- Title: Integrate Init Version Detection And Upgrade Direction
- Created: 2026-07-21
- Scope remains inside the approved parent decomposition and autonomous continuation authority.
