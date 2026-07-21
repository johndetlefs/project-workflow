## User Story

As a maintainer or agent, I want init to create only new installations and direct every existing repository to canonical upgrade without mutation, so command names match their user-facing behavior.

## Parent AC Coverage

- AC1, AC5

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

## Acceptance Criteria

- [x] AC1: Fresh and repeated init create then preserve the exact current manifest.
- [x] AC2: Legacy init changes nothing, creates no manifest, and directs canonical UVX upgrade.
- [x] AC3: Current and behind-schema init preserve every file and direct canonical upgrade.
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
| 1 | Integrate init state detection | Detect before mutation, create only fresh manifests, and leave every existing state unchanged. | AC1, AC2, AC3, AC4 | Run state matrix and inspect manifest/tree diffs. | Done |
| 2 | Add honest init direction | Report detected/resulting states and exact upgrade or recovery next actions. | AC2, AC3, AC4 | Compare init output across fixtures. | Done |
| 3 | Add repository Doctor findings | Map compatibility states to explicit structured finding codes and remediation metadata. | AC4, AC5 | Compare human/JSON findings and strict exits. | Done |
| 4 | Prove idempotency and parity | Refresh mirrors through upgrade and run complete validation. | AC1, AC6 | Run second init, canonical upgrade, local helper, pytest, parity, compilation, and strict Doctor. | Done |

## Parent AC Evidence

- AC1: Fresh/second init exact-manifest tests plus legacy, behind, invalid, and future state fixtures prove deterministic classification and no false current state.
- AC5: Init output and structured Doctor tests prove explicit state, remediation owner, mechanical eligibility, preservation, and correct upgrade direction.

## QA & Code Review

- Verdict: Pass; completed under autonomous Epic continuation authority.
- Evidence: Fresh/second/existing/legacy/invalid/future init tests prove new-only creation and byte-identical existing-state no-op behavior; canonical upgrade tests prove helper/agent refresh moved to the upgrade transaction; full suite, source/template/local parity, compilation, and strict Doctor passed.
- Findings: No blocking findings. Legacy repositories remain manifest-free after mistaken init and are migrated only by canonical upgrade.

## Retro

- Reusable lessons: Compatibility must be captured before init creates workflow markers; an existing-repository init should not mutate merely because older versions used init as refresh; canonical upgrade can preserve internal asset/schema boundaries without exposing them as separate user steps.
- Conventions or agent assets updated: Added new-only init behavior, exact canonical upgrade direction, combined upgrade asset refresh, and explicit repository-state Doctor findings across CLI mirrors.
- Follow-up tasks: TASK-045 will convert recognized legacy state through the immutable migration registry and preservation fixtures.

## Notes

- Task: TASK-044
- Title: Integrate Init Version Detection And Upgrade Direction
- Created: 2026-07-21
- Scope remains inside the approved parent decomposition and autonomous continuation authority.
