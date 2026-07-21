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

## Goal

Make canonical init and Doctor version-aware so managed asset refresh is honest about the repository schema it found and never masquerades as a durable repository upgrade.

## Non-Goals

- Applying repository migrations or creating a current-schema manifest for legacy state.
- Registering historical migrations; TASK-045 owns them.
- Changing user-owned config, trackers, backlog, guidance, task/Epic history, approvals, or evidence.
- Adding automatic upgrade apply to init or Doctor.

## Users & Context

- New repositories need a current manifest at first initialization.
- Existing legacy repositories need managed helper refresh without being mislabeled current.
- Versioned repositories may have current, behind, invalid, or future schema/asset state.
- Humans and agents need the same explicit next action from init and structured Doctor findings.

## Requirements (Outcome-Focused)

- Detect repository compatibility before init creates or refreshes any managed asset.
- Fresh not-initialized repositories receive a deterministic current manifest after successful initialization.
- Current repositories preserve schema and migration history while refreshing managed package/asset metadata when required.
- Legacy-unversioned repositories remain manifest-free, preserve all durable state, and are directed to non-mutating `project upgrade` planning.
- Schema-behind repositories preserve schema/applied migrations, refresh only managed assets, and are directed to upgrade.
- Invalid and unsupported-future manifests are never rewritten and produce blocking guidance.
- Init output names detected state, resulting asset/schema state, and the correct next command without claiming migration.
- Doctor emits stable structured findings for not-initialized, legacy, schema-behind, asset-behind, invalid, and future state; current state emits none.
- Repository compatibility findings use explicit remediation ownership and mechanical eligibility.
- Preserve second-init idempotency and generated asset parity.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC AC1: fresh init creates the exact current manifest and second init leaves it unchanged.
- AC2: Covers parent AC AC5: legacy init refreshes managed assets but creates no manifest, mutates no durable/user-owned canary, and directs `project upgrade`.
- AC3: Covers parent AC AC5: behind-schema init preserves schema/applied migrations, refreshes only package/asset metadata, and reports upgrade direction without claiming schema completion.
- AC4: Covers parent ACs AC1, AC5: invalid/future manifests remain byte-identical and init reports a stable blocking state.
- AC5: Covers parent AC AC5: Doctor human/JSON output provides stable version-state codes, owner, mechanical eligibility, artifact, and next-action message with unchanged strict exits.
- AC6: Covers parent ACs AC1, AC5: current init/Doctor no-op behavior, full suite, generated parity, compilation, and strict Doctor pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Detect state before creating `.project-workflow/`; otherwise fresh and legacy state become indistinguishable.
- Create a manifest only for genuinely fresh initialization.
- Never create or normalize a legacy manifest during init; TASK-045 upgrade owns that transition.
- Permit init to update only package/asset fields in an existing valid manifest while preserving schema and applied migrations.
- Add explicit Doctor codes rather than deriving version findings from prose.
- Treat legacy/schema-behind as project-workflow-owned and mechanically upgradeable; invalid/future state blocks and requires owner/maintainer resolution.

## Validation Plan

- Fixture-test fresh, second-init, legacy, current, schema-behind, invalid, and future repositories.
- Snapshot preservation canaries and manifest bytes before/after each init state.
- Compare init output with Doctor human/JSON codes and remediation fields.
- Run packaged/local init and Doctor, full pytest, parity, compilation, and strict Doctor.
