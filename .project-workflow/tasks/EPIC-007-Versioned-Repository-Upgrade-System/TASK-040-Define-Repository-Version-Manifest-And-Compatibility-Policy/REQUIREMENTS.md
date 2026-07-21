# Requirements

## Summary

- Task: TASK-040
- Title: Define Repository Version Manifest And Compatibility Policy
- Parent AC Coverage: AC1, AC5, AC7
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
- AC7: owner `Build Safe Transactional Upgrade Apply, Add Historical Migration Registry And Fixtures`; required evidence: Preservation-canary diffs across tracker, docs, backlog, guidance, config, approvals, deferrals, evidence, and unmarked content.

## Goal

Define one explicit, machine-readable repository version contract so project-workflow can identify current, recognized legacy, upgradeable, invalid, and unsupported-future repositories without inferring state from whichever files happen to exist.

## Non-Goals

- Implementing `project upgrade` planning or application.
- Adding structured Doctor findings or changing Doctor's public output.
- Integrating version reporting or upgrade direction into `project init`.
- Implementing historical migrations or claiming that a pre-versioned repository has been upgraded.
- Changing package release/versioning policy, generated-helper distribution, or user-owned workflow content.

## Users & Context

- Maintainers and agents need a stable contract before they can safely plan or execute upgrades across repositories created by different project-workflow releases.
- Existing repositories predate explicit version metadata. Their missing manifest is meaningful legacy state, not evidence that they are current or invalid.
- Future repositories may contain a schema newer than the installed CLI understands. They must be blocked rather than interpreted using older assumptions.
- `.project-workflow/config.json`, trackers, backlog rows, task/Epic documents, approvals, evidence, guidance, and unmarked files remain user or workflow-history content; the new manifest does not transfer ownership of them.

## Requirements (Outcome-Focused)

- Add a managed `.project-workflow/manifest.json` contract with independent package, generated-asset, and repository-schema versions plus ordered applied migration IDs.
- Keep the manifest's format version explicit so its own shape can evolve independently of the repository schema it describes.
- Define one current asset version and one current repository-schema version in code, separate from the package release version.
- Parse and validate manifests strictly enough that malformed or ambiguous state is never treated as current.
- Classify repository state deterministically as current, upgradeable, recognized legacy-unversioned, unsupported-future, invalid, or not-initialized.
- Treat an absent manifest as legacy only when the repository contains a recognizable `.project-workflow/` installation; an unrelated repository is not initialized.
- Make compatibility inspection read-only. Reading or classifying repository state must not create, rewrite, or normalize any repository file.
- Provide deterministic serialization for the current managed manifest without modifying user-owned config, history, documentation, evidence, or unmarked content.
- Publish a compatibility policy that supports the recognized pre-versioned baseline and every repository-schema version introduced by project-workflow until a documented breaking release removes support.
- Expose the state model as reusable internal primitives for later Doctor, upgrade, and init children without adding their public behavior in this task.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC AC1: the current manifest schema records `manifest_version`, `package_version`, `asset_version`, `schema_version`, and an ordered `applied_migrations` list using stable types and deterministic serialization.
- AC2: Covers parent AC AC1: a recognizable pre-versioned `.project-workflow/` repository is classified as `legacy-unversioned`, while an unrelated repository without a manifest is classified as `not-initialized`.
- AC3: Covers parent AC AC1: valid manifests are deterministically classified as `current`, `upgradeable`, or `unsupported-future`; malformed manifests are `invalid` with a stable reason and are never treated as current.
- AC4: Covers parent AC AC1: the compatibility policy explicitly retains the legacy baseline and all introduced schema versions unless support is removed by a documented breaking-release decision.
- AC5: Covers parent AC AC7: compatibility inspection performs no writes, and current-manifest serialization changes only the caller-selected manifest target while preservation canaries for config, trackers, docs, approvals, evidence, and unmarked files remain byte-identical.
- AC6: Covers parent AC AC5: reusable state and version primitives expose package, asset, and schema state without collapsing the distinct version dimensions used by canonical upgrade.
- AC7: Covers parent ACs AC1, AC5, AC7: focused tests cover every compatibility state, strict manifest validation, deterministic output, read-only inspection, and preservation boundaries, and the full suite plus strict Doctor validation pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use `.project-workflow/manifest.json` as generated, project-workflow-owned metadata; keep user configuration in `.project-workflow/config.json`.
- Start `manifest_version`, `asset_version`, and `schema_version` at integer version `1`; source `package_version` from the installed package version.
- Use six compatibility states: `current`, `upgradeable`, `legacy-unversioned`, `unsupported-future`, `invalid`, and `not-initialized`.
- A manifest is upgradeable only when its schema is known and below current. Unknown older versions are invalid until a supported migration is registered; newer manifest, asset, or schema versions are unsupported-future.
- Preserve migration order in `applied_migrations`; reject duplicates and malformed migration IDs rather than silently normalizing them.
- This task creates reusable contract primitives only. TASK-041 owns Doctor presentation, TASK-042/TASK-043 own upgrade planning/application, TASK-044 owns init integration, and TASK-045 owns historical migration registration and fixtures.

## Validation Plan

- Unit-test manifest parsing and serialization with exact expected payloads.
- Exercise current, known-behind, recognized legacy, malformed, unsupported-future, and not-initialized repositories.
- Hash repository trees before and after compatibility inspection to prove zero mutation.
- Write a current manifest into a canary fixture and prove every non-target file remains byte-identical.
- Run targeted tests, the complete pytest suite, source/template parity checks, and `./.project-workflow/cli/workflow doctor --strict`.
