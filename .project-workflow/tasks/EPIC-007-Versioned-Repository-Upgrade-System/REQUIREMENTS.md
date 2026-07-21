# Requirements

## Summary

- Task: EPIC-007
- Title: Versioned Repository Upgrade System
- Last updated: 2026-07-21
- Source discussion: Owner accepted the enterprise-grade upgrade-system recommendation on 2026-07-21 and asked that all displaced scope remain preserved in the backlog.

## Backlog Sources

- BL-003: Versioned Repository Upgrade System. Promoted to EPIC-007.
- BL-005: Generated Helper Version And Refresh Diagnostics. Promoted into EPIC-007 because explicit package, asset, schema, and capability metadata are prerequisites for deterministic upgrades.

## User Story

As an owner, maintainer, or agent returning to an older project-workflow repository, I want the latest project-workflow release to identify the repository's installed contract, plan an exact safe upgrade, and apply only deterministic mechanical transformations, so the repository can reach the current supported contract without losing user-owned content, rewriting history, or depending on agent improvisation.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-21
- Approval note / source: Owner approved the proposed correction on 2026-07-21: keep init new-project-only and make canonical UVX upgrade the one-command existing-repository flow; proceed with implementation.
- Approved artifact identity: sha256:db484c422b01a44adda39d567aa250a1acb103092bc06710b2b22acafa0ca103

## Goal

Make every supported project-workflow repository deterministically upgradeable to the current repository contract.

The owner-facing outcome is a trustworthy command model:

- `project init` creates project-workflow only in a new repository.
- `project doctor` diagnoses repository health without mutation.
- canonical UVX `project upgrade` is the single existing-repository entry point and plans managed-asset refresh plus versioned repository-state transformations together. The normal human command confirms and applies in one invocation; agents use `--yes`, while automation can separate `--plan` and fingerprinted `--apply`.

An upgrade must either apply the exact validated mechanical plan or make no changes. Product decisions, approvals, evidence refreshes, and unrecognized state remain visible and blocked for owner resolution.

## Non-Goals

- Building a dashboard, hosted control plane, database, or external migration service.
- Importing or transforming roadmap or backlog documents outside `.project-workflow/BACKLOG.md`.
- Silently approving historical requirements, evidence, warnings, deferrals, or product decisions.
- Replacing `project init` as the canonical new-repository acquisition path.
- Turning `project doctor` into a mutating repair command.
- Redesigning lifecycle status vocabulary.
- Fully modularizing the CLI; BL-009 owns that separate architectural Epic candidate.
- Adding batch accepted-warning ergonomics; BL-006 owns that work.
- Solving general atomic backlog/write concurrency; BL-007 owns that work.
- Fixing backlog-to-epic artifact parity; BL-016 owns that focused correction.
- Solving package/changelog release hygiene beyond metadata required by the upgrade contract; BL-010 remains separate.
- Redesigning local helper distribution; BL-014 remains separate.

## Users & Context

- Primary user: an owner or agent returning to a repository initialized by an older project-workflow release.
- Secondary user: a project-workflow maintainer upgrading a fleet of repositories with different historical workflow states.
- Enterprise context: repositories may have old generated helpers, unversioned Markdown schemas, legacy trackers, missing current artifacts, managed-file drift, `*.new` collisions, historical warnings, or newer approval and evidence gates.
- Proven evidence: sibling repositories exposed stale local helpers without current commands, missing configs and guidance, old Epic schemas, generated drift, and evidence/approval gaps that required manual interpretation.
- Product risk: without explicit versions and deterministic migrations, every new workflow gate increases the chance that older repositories become ambiguous or depend on an agent guessing how to repair them.

## Definitions

- Package version: the released project-workflow software version.
- Asset version: the version of generated helpers, prompts, skills, rules, templates, and managed instruction blocks installed in a repository.
- Repository schema version: the version of the durable `.project-workflow/` contract and artifact shapes.
- Migration ID: an immutable identifier for one ordered repository-schema transformation.
- Supported repository: a repository whose schema or recognized pre-versioned legacy profile has a tested migration path to the current schema.
- User-owned content: unmarked repository content and workflow files or fields that project-workflow does not own through an explicit generated marker or managed block.

## Requirements (Outcome-Focused)

- Add managed repository metadata that distinguishes package, generated-asset, and repository-schema versions and records applied migration IDs.
- Recognize pre-versioned project-workflow repositories as an explicit legacy baseline rather than guessing that they are current.
- Keep `project init` responsible only for new installation; existing repositories must remain unchanged and receive the exact canonical UVX upgrade command.
- Extend doctor findings with stable machine-readable codes, severity, affected artifact, remediation ownership, and whether a finding is mechanically upgradeable.
- Provide `project upgrade` as the repository-state upgrade command.
- Make canonical UVX `project upgrade` produce one ordered plan containing managed-asset refreshes, current and target versions, migration IDs, exact target files, expected transformations, preconditions, blockers, and owner decisions; the normal human path confirms and applies that plan in the same invocation.
- Provide machine-readable upgrade-plan output suitable for agents and CI alongside concise human-readable output.
- Support one-command non-interactive agent apply through `--yes`; retain non-mutating `--plan` and explicit fingerprint-bound `--apply` for automation and CI.
- In the first release, apply the complete validated mechanical plan as one transaction; do not support arbitrary partial migration selection.
- Reject apply when the worktree is dirty, the plan is stale, expected input hashes or versions changed, the target schema is unsupported, or repository state is unrecognized.
- Use atomic file replacement and pre-apply validation so a failed upgrade cannot leave a partially migrated repository.
- Preserve user-owned content, tracker history, task and Epic records, backlog rows, guidance, config values, approvals, deferrals, and evidence unless a versioned migration explicitly owns a generated field or managed block.
- Never convert missing approval, stale evidence, accepted warnings, or unresolved product decisions into passing state; report them as owner-owned follow-up.
- Make migrations ordered, immutable, idempotent, and independently testable. A second apply at the target version must be a no-op.
- Publish an explicit compatibility policy. The initial system must support the recognized pre-versioned legacy baseline plus every repository schema introduced by project-workflow until support is deliberately removed through a documented breaking-release decision.
- Integrate post-upgrade doctor validation and report whether the repository is current, current with named owner decisions, or blocked.
- Document the upgrade model and keep packaged CLI, generated helper, prompts, Codex skills, and Cursor rules behaviorally aligned.

## Acceptance Criteria (Verifiable)

- AC1: A managed repository metadata artifact records package, asset, and repository-schema versions plus applied migration IDs; recognized pre-versioned repositories receive a deterministic legacy classification rather than being treated as current.
- AC2: Doctor can emit stable machine-readable findings containing a code, severity, affected artifact, remediation ownership, and mechanical-upgrade eligibility, while preserving concise human-readable output.
- AC3: Running `project upgrade --plan` against each supported historical fixture produces an ordered, machine-readable and human-readable plan covering managed assets and schema with current/target versions, migration IDs, exact target files, preconditions, blockers, and owner decisions, and causes no repository file changes.
- AC4: `project upgrade --apply` applies exactly the validated mechanical plan only when worktree, version, and input-hash preconditions still match; dirty, stale, unsupported, or unrecognized state is rejected without mutation.
- AC5: Canonical `project init` creates a current new installation; on every existing repository state it makes no changes and directs the caller to canonical UVX `project upgrade`, which refreshes managed assets and migrates schema together.
- AC6: Migration application is atomic and idempotent: injected failure leaves no partial file changes, successful apply matches the predicted diff, and a second apply at the target version is a no-op.
- AC7: Upgrade fixtures prove that existing tracker rows, task/Epic docs, backlog rows, guidance, config values, approvals, deferrals, evidence, and unmarked content are preserved unless an explicit versioned migration owns the changed field.
- AC8: Missing approvals, stale evidence, accepted warnings, and unresolved product decisions remain visible as named owner-owned follow-up and are never automatically converted into passing evidence or authority.
- AC9: Targeted historical-fixture, stale-plan, dirty-worktree, unsupported-version, atomic-failure, preservation, idempotency, init-integration, doctor-output, and generated-helper parity tests pass together with the full project-workflow suite and strict doctor validation.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Rename the Epic from Repo Migration And Adoption Tooling to Versioned Repository Upgrade System.
- Use `project upgrade` for repository-state upgrades. Keep `task adopt` and `epic adopt` for record-level legacy adoption.
- Preserve clear command semantics: init creates, Doctor diagnoses, and canonical upgrade refreshes and transforms every existing installation.
- Store explicit package, asset, and repository-schema versions plus immutable applied migration IDs in a managed metadata artifact.
- Treat recognized pre-versioned repositories as a supported legacy baseline with tested migrations.
- Make canonical UVX `project upgrade` the only existing-repository update entry point. Default human operation plans, confirms, applies, and validates in one invocation; `--yes` supports authorized agents and `--plan` plus fingerprinted `--apply` supports separated automation.
- Apply the full validated mechanical plan transactionally in the first release; do not add partial-selection complexity.
- Require a clean worktree and fresh version/hash preconditions before apply. Git remains the human-visible rollback and audit mechanism.
- Use stable machine-readable finding codes and plan output for agents and CI.
- Block unknown or unsupported state rather than attempting best-effort repair.
- Keep collision-resistant IDs and accepted-warning suppression as completed TASK-026 and TASK-027 history.
- Preserve batch warning ergonomics (BL-006), atomic write safety (BL-007), backlog promotion parity (BL-016), CLI modularization (BL-009), release hygiene (BL-010), and helper distribution strategy (BL-014) outside this Epic.

## Validation Plan

- Build fixture repositories for the recognized pre-versioned baseline and every supported repository schema.
- Hash fixture trees before and after default upgrade planning to prove zero mutation.
- Assert plan ordering, migration IDs, target files, preconditions, blockers, owner decisions, and stable machine-readable fields.
- Compare the predicted plan diff with the actual apply diff.
- Inject stale plan inputs, dirty worktrees, unsupported versions, unrecognized files, and migration failures; assert no mutation or partial writes.
- Seed user-owned canary content in trackers, task/Epic docs, backlog, guidance, config, approvals, deferrals, evidence, managed-block neighbors, and unmarked files; assert preservation.
- Apply every fixture twice and assert the second apply is a no-op.
- Verify canonical init initializes only new repositories and leaves every existing state unchanged with exact upgrade direction.
- Verify canonical upgrade refreshes managed assets and applies required schema migrations in one transaction and one normal invocation.
- Run targeted migration tests, the full pytest suite, source/generated parity checks, backlog validation, and `project doctor --strict`.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Define Repository Version Manifest And Compatibility Policy | AC1, AC5, AC7 | Establish package, asset, schema, legacy-baseline, migration-ID, and compatibility contracts. |
| Add Structured Doctor Findings | AC2, AC5, AC8 | Provide stable human and machine-readable diagnostics with remediation ownership and upgrade eligibility. |
| Build Deterministic Upgrade Planner | AC3, AC4, AC8 | Add non-mutating ordered plans with exact targets, preconditions, blockers, and owner decisions. |
| Build Safe Transactional Upgrade Apply | AC4, AC6, AC7, AC8 | Apply the complete fresh mechanical plan atomically while preserving user-owned state. |
| Integrate Init Version Detection And Upgrade Direction | AC1, AC5 | Restrict canonical init to new repositories and direct every existing installation to canonical upgrade without mutation. |
| Add Historical Migration Registry And Fixtures | AC1, AC3, AC6, AC7, AC8, AC9 | Implement immutable migrations and prove legacy, preservation, failure, and idempotency behavior. |
| Align Documentation And Generated Agent Assets | AC2, AC3, AC5, AC9 | Document one-command canonical UVX upgrade and preserve packaged/generated behavioral parity. |
