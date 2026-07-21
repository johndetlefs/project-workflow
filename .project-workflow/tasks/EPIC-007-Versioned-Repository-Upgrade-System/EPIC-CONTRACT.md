# Epic Contract

## Summary

- Epic: EPIC-007
- Title: Versioned Repository Upgrade System
- Last updated: 2026-07-21

## Sources of Truth

- `.project-workflow/tasks/EPIC-007-Versioned-Repository-Upgrade-System/REQUIREMENTS.md`
- `.project-workflow/CONSTITUTION.md`
- Current packaged CLI behavior in `src/project_workflow/cli.py`
- Generated helper behavior in `src/project_workflow/templates/workflow.py`
- Current prompts, Codex skills, Cursor rules, and managed Project Workflow instruction blocks
- Existing repository-owned workflow state in migration fixtures and selected sibling-repository scenarios
- The managed version metadata artifact introduced by the first child workstream
- The ordered migration registry and its fixture-backed compatibility policy

## Invalid Substitutes

- A successful `project init` run is not proof that durable repository state was upgraded.
- A clean old helper or old doctor result is not proof that the repository uses the current schema.
- Package version alone is not a substitute for separate asset and repository-schema versions.
- An agent-authored prose summary is not a substitute for a deterministic machine-readable upgrade plan.
- A passing plan is not proof that apply produced the predicted diff.
- Tests against only freshly initialized repositories are not historical upgrade evidence.
- Backups or Git availability do not permit overwriting user-owned content.
- Accepted warnings, inferred approvals, or stale evidence are not upgraded authority or proof.
- Best-effort partial changes are not an acceptable substitute for atomic application.

## Invariants

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

## Artifact Targets

- Managed repository metadata at `.project-workflow/manifest.json`
- Upgrade command, plan model, migration registry, and apply engine in `src/project_workflow/cli.py` with behavioral parity in `src/project_workflow/templates/workflow.py`
- Stable structured doctor and upgrade-plan output schemas
- Historical repository fixtures and focused regression coverage under `tests/`
- Generated agent guidance under `src/project_workflow/prompts/`, `src/project_workflow/codex/`, and `src/project_workflow/cursor/`
- README and changelog documentation for init, doctor, and upgrade responsibilities
- EPIC-007 child requirements, implementation plans, evidence, QA, acceptance map/audit, and closeout artifacts

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | Define Repository Version Manifest And Compatibility Policy, Add Historical Migration Registry And Fixtures | Fixture inspection showing explicit package/asset/schema versions and deterministic classification of pre-versioned state. |
| AC2 | Add Structured Doctor Findings, Align Documentation And Generated Agent Assets | Tests and captured output proving stable finding codes and equivalent human/machine-readable fields. |
| AC3 | Build Deterministic Upgrade Planner, Add Historical Migration Registry And Fixtures | Before/after fixture hashes proving zero plan mutation plus complete ordered plan records for every supported source schema. |
| AC4 | Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply | Dirty, stale, unsupported, and unrecognized failure tests plus a successful apply whose diff exactly matches the fresh plan. |
| AC5 | Define Repository Version Manifest And Compatibility Policy, Integrate Init Version Detection And Upgrade Direction | Legacy/current init fixtures proving managed refresh and honest schema/upgrade direction without repository-state mutation. |
| AC6 | Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures | Injected-failure evidence proving no partial writes and second-apply evidence proving no-op idempotency. |
| AC7 | Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures | Preservation-canary diffs across tracker, docs, backlog, guidance, config, approvals, deferrals, evidence, and unmarked content. |
| AC8 | Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply | Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply. |
| AC9 | Add Historical Migration Registry And Fixtures, Align Documentation And Generated Agent Assets | Passing targeted and full-suite output, strict doctor, backlog validation, and packaged/generated parity evidence. |
