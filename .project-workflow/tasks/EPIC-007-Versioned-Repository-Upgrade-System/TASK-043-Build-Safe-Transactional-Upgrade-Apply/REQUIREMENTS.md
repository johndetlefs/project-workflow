# Requirements

## Summary

- Task: TASK-043
- Title: Build Safe Transactional Upgrade Apply
- Parent AC Coverage: AC4, AC6, AC7, AC8
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

- AC4: owner `Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Dirty, stale, unsupported, and unrecognized failure tests plus a successful apply whose diff exactly matches the fresh plan.
- AC6: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Injected-failure evidence proving no partial writes and second-apply evidence proving no-op idempotency.
- AC7: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Preservation-canary diffs across tracker, docs, backlog, guidance, config, approvals, deferrals, evidence, and unmarked content.
- AC8: owner `Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply.

## Goal

Apply one exact, fresh, fully validated mechanical upgrade plan as an all-or-restored transaction, with no partial file state and no authority to alter user-owned content outside declared migration targets.

## Non-Goals

- Registering production historical migrations; TASK-045 owns migration implementations and fixtures.
- Partial migration selection, best-effort application, interactive conflict resolution, or automatic commits.
- Applying owner decisions, approvals, evidence refreshes, deferrals, or accepted warnings.
- Defining generated asset content; canonical upgrade coordinates existing generators with schema migration.
- Providing cross-process distributed locking beyond clean-worktree and fresh hash/version checks.

## Users & Context

- Maintainers need explicit control over mutation and proof that apply matches the reviewed plan.
- Agents and CI need stale-plan rejection and deterministic machine output.
- Multi-file replacement can fail midway; the command must restore all touched files before returning failure.
- Migration code is privileged and must be constrained to the target files declared in immutable migration metadata.

## Requirements (Outcome-Focused)

- Add `project upgrade --apply --plan-fingerprint <SHA256>`; reject apply without both explicit inputs.
- Rebuild the plan immediately before apply and require the supplied fingerprint to match exactly.
- Require a Git worktree with no tracked, staged, or untracked changes before mutation.
- Revalidate repository compatibility state and every planned file hash/absent precondition immediately before mutation.
- Require one registered pure migration handler for every planned migration ID and reject undeclared, missing, duplicate, or non-bytes outputs.
- Compute all final target bytes in memory before writing any target.
- Validate the final manifest and target schema from computed bytes before writing.
- Write temporary files adjacent to targets, flush and fsync them, then replace targets atomically.
- Capture original bytes/absence for every target; on any replacement or validation failure, restore all touched targets and remove temporary files.
- Never mutate a path outside the plan's exact `target_files` list.
- Emit deterministic human/JSON apply results containing plan fingerprint, status, applied migrations, changed files, and failure code/message.
- A current plan with no steps must be a successful no-op; a second apply after successful migration must also no-op.
- Keep production handlers empty until TASK-045 registers fixture-proven migrations; test the engine with injected synthetic handlers and failure injection.
- Preserve packaged/template/local-helper parity.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC AC4: apply rejects missing/mismatched fingerprints, dirty or non-Git worktrees, stale compatibility state, changed input hashes, blocked plans, and missing handlers without mutation.
- AC2: Covers parent AC AC6: valid synthetic migrations compute all outputs first, atomically replace exactly declared targets, produce bytes matching the predicted plan, and no-op on a second current apply.
- AC3: Covers parent AC AC6: injected failure after any replacement restores every original target byte/absence and leaves no temporary files.
- AC4: Covers parent AC AC7: preservation canaries outside declared targets remain byte-identical through success, rejection, and rollback.
- AC5: Covers parent AC AC8: owner decisions remain unchanged plan metadata and are never passed to migration handlers or converted to passing state.
- AC6: Covers parent ACs AC4, AC6: human/JSON results report the exact fingerprint, applied migration IDs, changed files, no-op state, and stable failure details.
- AC7: Covers parent ACs AC4, AC6, AC7, AC8: targeted apply/failure/idempotency tests, full pytest, parity, compilation, and strict Doctor pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Require the caller to supply the reviewed plan fingerprint; do not accept an implicit latest plan for mutation.
- Reject all dirty worktrees, including untracked files.
- Use pure per-migration handlers that receive declared current bytes and return declared final bytes/absence.
- Validate every handler output before filesystem mutation and reject outputs outside declared targets.
- Use adjacent temporary files plus `os.replace`; restore captured originals if any replacement fails.
- Keep Git as the human audit/rollback layer but do not rely on Git to provide command-level rollback.
- Treat current/no-step apply as success with `noop: true`.
- Keep production handlers empty until TASK-045.

## Validation Plan

- Initialize temporary Git fixture repositories and test every apply precondition independently.
- Inject synthetic one-file and multi-file migration handlers and compare predicted targets with resulting bytes.
- Inject failure before and after each replacement and assert complete byte/absence restoration and no temporary files.
- Seed user-owned canaries, owner decisions, symlinks, undeclared outputs, and changed hashes; assert rejection/preservation.
- Apply a valid fixture then rebuild/apply the current plan and assert deterministic no-op.
- Run packaged/local CLI apply checks, full pytest, mirror parity, compilation, and strict Doctor.
