# Requirements

## Summary

- Task: TASK-042
- Title: Build Deterministic Upgrade Planner
- Parent AC Coverage: AC3, AC4, AC8
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

- AC3: owner `Build Deterministic Upgrade Planner, Add Historical Migration Registry And Fixtures`; required evidence: Before/after fixture hashes proving zero plan mutation plus complete ordered plan records for every supported source schema.
- AC4: owner `Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Dirty, stale, unsupported, and unrecognized failure tests plus a successful apply whose diff exactly matches the fresh plan.
- AC8: owner `Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply.

## Goal

Provide a deterministic, non-mutating `project upgrade` planning command that turns proven repository state and an immutable migration registry into an exact, hash-bound plan suitable for human review, agents, CI, and later transactional application.

## Non-Goals

- Applying any file change or adding `--apply`; TASK-043 owns execution.
- Registering production historical migrations or claiming the legacy baseline is upgradeable before fixture proof; TASK-045 owns that registry.
- Refreshing managed assets or creating manifests through init; TASK-044 owns init integration.
- Automatically resolving owner-owned approvals, evidence, deferrals, or product decisions.
- Supporting partial migration selection or best-effort plans.

## Users & Context

- Maintainers need to know exactly what an upgrade would change before permitting mutation.
- Agents and CI need a stable JSON plan and fingerprint rather than interpreting prose.
- Apply must later reject stale plans, so planning must capture source versions and exact input-file hashes.
- Repositories may be current, recognized legacy, known-behind, invalid, future, or uninitialized; every state needs an honest plan or blocker.

## Requirements (Outcome-Focused)

- Add `project upgrade` as a non-mutating planning command with `--format human|json`.
- Define immutable migration metadata with ID, source and target schema versions, exact target files, and named transformations.
- Resolve one ordered contiguous migration path from source schema to current schema; reject duplicate IDs, ambiguous edges, cycles, gaps, downgrades, and unsupported sources.
- Emit a versioned plan containing plan fingerprint, repository compatibility state, package/asset/schema source and target versions, ordered migration steps, exact target files, expected transformations, file-hash and clean-worktree preconditions, blockers, and owner decisions.
- Use a deterministic absent-file sentinel and SHA-256 hashes for every planned target input.
- Include owner-owned Doctor findings as named owner decisions without altering or accepting them.
- Produce current/no-op plans without migrations and blocked plans for invalid, unsupported-future, not-initialized, or unregistered legacy state.
- Compute the plan fingerprint from canonical plan content excluding the fingerprint itself; repeated plans against unchanged state must be byte-identical.
- Planning must not write, normalize, create, or delete any repository file.
- Keep the production migration registry empty in this child; prove the engine with injected synthetic registries until TASK-045 adds historical fixture-backed entries.
- Preserve packaged, template, and local-helper parity.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC AC3: `project upgrade --format json` emits a deterministic versioned plan with source/target versions, ordered migration IDs, exact target files, transformations, preconditions, blockers, owner decisions, and a reproducible plan fingerprint.
- AC2: Covers parent AC AC3: a valid synthetic migration chain is ordered contiguously, while duplicate, ambiguous, cyclic, gapped, downgrade, and unsupported paths produce stable blockers rather than guessed steps.
- AC3: Covers parent AC AC4: every planned target has an expected SHA-256 or absent-file precondition and the plan records a clean-worktree precondition suitable for later stale-plan rejection.
- AC4: Covers parent AC AC8: owner-owned Doctor findings appear as unchanged named owner decisions and are never converted into migration steps or passing state.
- AC5: Covers parent AC AC3: current repositories produce deterministic no-op plans; invalid, future, uninitialized, and unregistered legacy repositories produce deterministic blocked plans.
- AC6: Covers parent AC AC3: before/after tree hashes prove human and JSON planning cause zero repository mutation.
- AC7: Covers parent ACs AC3, AC4, AC8: packaged/template/local parity, targeted tests, full pytest, compilation, and strict Doctor pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use `project upgrade` with planning as the default and no mutating flag in this child.
- Keep plan schema version independent from repository schema version.
- Use canonical compact JSON with sorted keys as the plan-fingerprint input and indented JSON for display.
- Treat a dirty worktree as an apply precondition, not a blocker to non-mutating planning.
- Treat owner decisions as visible plan data but not mechanical blockers unless a migration explicitly requires their resolution.
- Permit only one migration edge from each source schema in the first release; ambiguity blocks.
- Keep production migrations empty until TASK-045 supplies historical fixtures and preservation evidence.

## Validation Plan

- Test exact current, blocked, and synthetic multi-step JSON plans and fingerprints.
- Parameterize invalid registries for duplicate IDs, ambiguous edges, cycles, gaps, and downgrades.
- Seed changed, absent, owner-decision, and unmarked canary files; assert exact preconditions and zero mutation.
- Compare repeated human/JSON plans and packaged/local-helper behavior.
- Run targeted planner tests, full pytest, source/template parity, Python compilation, and strict Doctor.
