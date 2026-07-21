# Requirements

## Summary

- Task: TASK-045
- Title: Add Historical Migration Registry And Fixtures
- Parent AC Coverage: AC1, AC3, AC6, AC7, AC8, AC9
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
- AC3: owner `Build Deterministic Upgrade Planner, Add Historical Migration Registry And Fixtures`; required evidence: Before/after fixture hashes proving zero plan mutation plus complete ordered plan records for every supported source schema.
- AC6: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Injected-failure evidence proving no partial writes and second-apply evidence proving no-op idempotency.
- AC7: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Preservation-canary diffs across tracker, docs, backlog, guidance, config, approvals, deferrals, evidence, and unmarked content.
- AC8: owner `Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply.
- AC9: owner `Add Historical Migration Registry And Fixtures, Align Documentation And Generated Agent Assets`; required evidence: Passing targeted and full-suite output, strict doctor, backlog validation, and packaged/generated parity evidence.

## Goal

Register and prove the first immutable production migration from recognized pre-versioned state to schema 1 without rewriting any historical or user-owned content.

## Non-Goals

- Normalizing old trackers, task/Epic documents, approvals, evidence, warnings, or decisions into current passing shapes.
- Refreshing generated assets; init owns that operation.
- Supporting unknown legacy profiles that do not meet the recognized project-workflow markers.
- Adding schema versions beyond 1.

## Users & Context

- Existing repositories predate manifests but contain valuable workflow history and local guidance.
- The first migration must adopt explicit version metadata while preserving that history byte-for-byte.
- Post-upgrade Doctor findings remain truthful owner/agent follow-up rather than migration-created authority.

## Requirements (Outcome-Focused)

- Register immutable migration `PW-0001-legacy-manifest` from schema 0 to schema 1.
- Target only `.project-workflow/manifest.json` and create the current manifest with that migration ID recorded.
- Register one pure production handler whose output is bound into the plan fingerprint.
- Add a checked-in representative legacy fixture containing tracker, backlog, config, guidance, task requirements/implementation/evidence, approvals/placeholder history, and unmarked user content.
- Prove canonical init refresh leaves the fixture legacy and preserves durable content before upgrade.
- Prove production plan/apply succeeds on the clean initialized fixture, changes only the manifest, and records the exact migration.
- Prove plan diff equals apply diff, failure restores manifest absence, and second apply at current schema is a no-op.
- Prove post-upgrade compatibility is current while historical Doctor findings remain visible and unchanged.
- Preserve all fixture canaries byte-for-byte and run full regression/parity gates.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC AC1: production registry contains the immutable ordered 0-to-1 migration and applied manifest records its ID.
- AC2: Covers parent AC AC3: the checked-in legacy fixture produces one deterministic exact-target plan with predicted manifest hash and zero planning mutation.
- AC3: Covers parent AC AC6: apply creates exactly the predicted manifest, failure restores absence, and second apply no-ops.
- AC4: Covers parent AC AC7: every tracker/backlog/config/guidance/task/evidence/unmarked fixture canary remains byte-identical through init, plan, apply, and rollback.
- AC5: Covers parent AC AC8: historical approval/evidence/decision gaps remain Doctor findings and are never transformed by migration.
- AC6: Covers parent AC AC9: production CLI and local helper run the fixture end-to-end with full pytest, parity, compilation, and strict Doctor passing.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Schema 1 represents adoption of the explicit versioned repository contract, not retroactive proof that every historical document satisfies current gates.
- The first migration writes only the managed manifest; all other content is outside its ownership.
- Historical validation findings remain visible after migration.
- Keep fixture content checked in and human-inspectable rather than synthesizing the only historical case entirely in test code.

## Validation Plan

- Copy the checked-in fixture, run init, commit it, then run production plan/apply through packaged and local helpers.
- Hash every non-manifest file across init, plan, success, rollback, and no-op phases.
- Assert exact migration ID, target, predicted output hash, manifest payload, plan/apply diff, and post-upgrade findings.
- Run full pytest, mirror parity, compilation, and strict Doctor.
