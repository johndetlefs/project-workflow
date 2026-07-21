## User Story

As a maintainer or agent inspecting an initialized repository, I want an explicit version manifest and deterministic compatibility classification, so that later upgrade, Doctor, and init behavior can act on proven repository state without guessing or rewriting user-owned content.

## Parent AC Coverage

- AC1, AC5, AC7

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
- AC5: owner `Define Repository Version Manifest And Compatibility Policy, Integrate Init Version Detection And Upgrade Direction`; required evidence: New/existing init fixtures proving init-only creation and no-mutation upgrade direction, plus canonical upgrade asset refresh.
- AC7: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Preservation-canary diffs across tracker, docs, backlog, guidance, config, approvals, deferrals, evidence, and unmarked content.

## Acceptance Criteria

- [x] AC1: The deterministic current manifest records independent manifest, package, asset, and schema versions plus ordered applied migration IDs.
- [x] AC2: Recognizable pre-versioned and unrelated uninitialized repositories receive distinct classifications.
- [x] AC3: Current, known-behind, unsupported-future, and malformed manifests receive deterministic compatibility states and stable reasons.
- [x] AC4: The compatibility policy retains the legacy baseline and introduced schema versions until an explicit breaking-release decision.
- [x] AC5: Inspection is read-only and manifest writing preserves every non-target file byte-for-byte.
- [x] AC6: Reusable internal primitives expose distinct package, asset, and schema state for init, Doctor, and canonical upgrade integration.
- [x] AC7: Targeted and full validation, strict Doctor, and source/generated parity checks pass.

## Validation

- AC1 / parent AC1: exact manifest payload and deterministic serialization tests.
- AC2 / parent AC1: legacy-unversioned and not-initialized fixture tests.
- AC3 / parent AC1: table-driven compatibility and invalid-manifest tests.
- AC4 / parent AC1: explicit supported-schema policy assertions and compatibility documentation inspection.
- AC5 / parent AC7: tree-hash read-only inspection and preservation-canary write tests.
- AC6 / parent AC5: unit tests consume reusable contract primitives without invoking or mutating init behavior.
- AC7 / parent AC1, AC5, AC7: targeted tests, full pytest, byte parity, and strict Doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define manifest contract | Add version constants, typed manifest data, strict validation, deterministic serialization, and managed write behavior. | AC1, AC5, AC6 | Inspect an exact serialized manifest and preservation-canary result. | Done |
| 2 | Classify repository compatibility | Add read-only recognition for current, known-behind, legacy-unversioned, unsupported-future, invalid, and not-initialized state. | AC2, AC3, AC6 | Run the compatibility fixture matrix and inspect stable states/reasons. | Done |
| 3 | Publish compatibility policy | Document support for the legacy baseline and introduced schemas, with explicit breaking-release removal rules and ownership boundaries. | AC4, AC6 | Inspect policy text against the implementation constants and task boundaries. | Done |
| 4 | Prove contract and parity | Add focused tests, preserve source/template behavior parity, run the full suite, and run strict Doctor. | AC1, AC2, AC3, AC5, AC7 | Review targeted/full test and Doctor outputs. | Done |

## Parent AC Evidence

- AC1: `.project-workflow/manifest.json`, exact serialization assertions, six-state compatibility coverage, and future-contract tests prove the explicit version and legacy-baseline contract.
- AC5: `WorkflowManifest` and `RepositoryCompatibility` provide reusable init-facing state primitives; no init behavior or repository upgrade claim was added. TASK-044 retains integration ownership.
- AC7: `test_manifest_inspection_and_writing_preserve_non_target_files` proves inspection is non-mutating and all config, tracker, backlog, guidance, task, evidence, and unmarked canaries remain byte-identical when the manifest is written.

## QA & Code Review

- Verdict: Pass; ready for owner review.
- Evidence: 16 targeted contract tests passed; full suite passed with 89 tests and 1 existing skip; Python compilation passed; packaged/template/local-helper parity passed strict Doctor with 69 accepted historical warnings hidden.
- Findings: No blocking findings. Public init, Doctor, planner, and apply behavior remains intentionally deferred to TASK-041 through TASK-045.

## Retro

- Reusable lessons: Version provenance, generated-asset state, and durable repository schema must remain independent; future manifest formats must be recognized before current-format field validation so older clients fail closed rather than mislabeling them invalid.
- Conventions or agent assets updated: Added `COMPATIBILITY.md`, the managed repository manifest, and matching packaged/generated/local contract primitives.
- Follow-up tasks: Continue EPIC-007 with TASK-041 structured Doctor findings, then planner, apply, init integration, and historical migration fixtures in dependency order.

## Notes

- Task: TASK-040
- Title: Define Repository Version Manifest And Compatibility Policy
- Created: 2026-07-21
- Scope is unchanged from the approved parent decomposition; implementation authority is inherited from the EPIC-007 approval envelope.
