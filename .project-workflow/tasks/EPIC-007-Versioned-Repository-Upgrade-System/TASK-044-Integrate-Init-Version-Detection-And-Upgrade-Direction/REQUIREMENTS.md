# Requirements

## Summary

- Task: TASK-044
- Title: Integrate Init Version Detection And Upgrade Direction
- Parent AC Coverage: AC1, AC5
- Last updated: 2026-07-21

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

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

## Goal

Make canonical init mean initialization only: create a current new installation, leave every existing repository unchanged, and direct it to canonical UVX upgrade.

## Non-Goals

- Applying repository migrations or creating a current-schema manifest for legacy state.
- Registering historical migrations; TASK-045 owns them.
- Changing user-owned config, trackers, backlog, guidance, task/Epic history, approvals, or evidence.
- Adding automatic upgrade apply to init or Doctor.

## Users & Context

- New repositories need a current manifest at first initialization.
- Existing legacy repositories need one current-package upgrade command without first mutating through init.
- Versioned repositories may have current, behind, invalid, or future schema/asset state.
- Humans and agents need the same explicit next action from init and structured Doctor findings.

## Requirements (Outcome-Focused)

- Detect repository compatibility before init creates any managed asset.
- Fresh not-initialized repositories receive a deterministic current manifest after successful initialization.
- Current, legacy-unversioned, schema-behind, asset-behind, invalid, and unsupported-future repositories remain byte-identical when init is run.
- Existing-repository init output names the detected state and exact canonical UVX upgrade command without creating or refreshing assets.
- Doctor emits stable structured findings for not-initialized, legacy, schema-behind, asset-behind, invalid, and future state; current state emits none.
- Repository compatibility findings use explicit remediation ownership and mechanical eligibility.
- Preserve second-init no-op behavior and generated asset parity through upgrade.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC AC1: fresh init creates the exact current manifest and second init leaves it unchanged.
- AC2: Covers parent AC AC5: legacy init changes no file, creates no manifest, and directs canonical UVX `project upgrade`.
- AC3: Covers parent AC AC5: current and behind-schema init change no file or metadata and direct canonical upgrade.
- AC4: Covers parent ACs AC1, AC5: invalid/future manifests and all neighboring assets remain byte-identical while init reports upgrade direction.
- AC5: Covers parent AC AC5: Doctor human/JSON output provides stable version-state codes, owner, mechanical eligibility, artifact, and next-action message with unchanged strict exits.
- AC6: Covers parent ACs AC1, AC5: current init no-op, canonical upgrade refresh, Doctor behavior, full suite, generated parity, compilation, and strict Doctor pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Detect state before creating `.project-workflow/`; otherwise fresh and legacy state become indistinguishable.
- Create a manifest only for genuinely fresh initialization.
- Never create or normalize a legacy manifest during init; TASK-045 upgrade owns that transition.
- Never update an existing valid manifest or generated asset through init; canonical upgrade owns all existing-repository changes.
- Add explicit Doctor codes rather than deriving version findings from prose.
- Treat legacy/schema-behind as project-workflow-owned and mechanically upgradeable; invalid/future state blocks and requires owner/maintainer resolution.

## Validation Plan

- Fixture-test fresh, second-init, legacy, current, schema-behind, invalid, and future repositories.
- Snapshot preservation canaries and manifest bytes before/after each init state.
- Compare init output with Doctor human/JSON codes and remediation fields.
- Run packaged init, canonical upgrade, local Doctor, full pytest, parity, compilation, and strict Doctor.
