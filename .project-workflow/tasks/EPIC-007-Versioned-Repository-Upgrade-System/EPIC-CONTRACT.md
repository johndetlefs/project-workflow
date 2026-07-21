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

- `project init` creates new installations; `project doctor` owns diagnosis; canonical UVX `project upgrade` refreshes managed assets and transforms existing repository state in one transaction.
- Explicit `--plan` mode is non-mutating; the normal human command confirms before apply and authorized non-interactive agents use `--yes`.
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

## Artifact Targets

- Managed repository metadata at `.project-workflow/manifest.json`
- Combined managed-asset/schema upgrade command, plan model, migration registry, and apply engine in `src/project_workflow/cli.py` with behavioral parity in `src/project_workflow/templates/workflow.py`
- Stable structured doctor and upgrade-plan output schemas
- Historical repository fixtures and focused regression coverage under `tests/`
- Generated agent guidance under `src/project_workflow/prompts/`, `src/project_workflow/codex/`, and `src/project_workflow/cursor/`
- README and changelog documentation for init, doctor, and upgrade responsibilities
- EPIC-007 child requirements, implementation plans, evidence, QA, acceptance map/audit, and closeout artifacts

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-040, TASK-044, TASK-045 | Fixture inspection showing explicit package/asset/schema versions and deterministic classification of pre-versioned state. |
| AC2 | TASK-041, TASK-046 | Tests and captured output proving stable finding codes and equivalent human/machine-readable fields. |
| AC3 | TASK-042, TASK-045, TASK-046 | Before/after fixture hashes proving zero `--plan` mutation plus complete managed-asset and ordered migration records for every supported source schema. |
| AC4 | TASK-042, TASK-043 | Dirty, stale, unsupported, and unrecognized failure tests plus a successful apply whose diff exactly matches the fresh plan. |
| AC5 | TASK-040, TASK-041, TASK-044, TASK-046 | New/existing init fixtures proving init-only creation and no-mutation upgrade direction, plus canonical upgrade asset refresh. |
| AC6 | TASK-043, TASK-045 | Injected-failure evidence proving no partial writes and second-apply evidence proving no-op idempotency. |
| AC7 | TASK-040, TASK-043, TASK-045 | Preservation-canary diffs across tracker, docs, backlog, guidance, config, approvals, deferrals, evidence, and unmarked content. |
| AC8 | TASK-041, TASK-042, TASK-043, TASK-045 | Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply. |
| AC9 | TASK-045, TASK-046 | Passing targeted and full-suite output, strict doctor, backlog validation, and packaged/generated parity evidence. |
