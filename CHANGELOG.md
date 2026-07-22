# Changelog

All notable changes to this project are documented in this file.

## Unreleased

## 0.2.0 - 2026-07-22

### Added

- Added explicit package, generated-asset, and repository-schema metadata in `.project-workflow/manifest.json`.
- Added stable structured Doctor finding codes, remediation ownership, mechanical eligibility, and `doctor --format json`.
- Added canonical UVX `project upgrade` as the single existing-repository entry point, combining managed-asset refresh, repository-schema migration, confirmation, apply, and post-upgrade validation.
- Added deterministic non-mutating `project upgrade --plan` human/JSON output plus explicit fingerprint-bound automation apply, clean-worktree and stale-plan rejection, rollback, and idempotent no-op behavior.
- Added immutable production migration `PW-0001-legacy-manifest` and checked-in historical preservation fixtures.
- Added configurable sequential or unique workflow ID generation for tasks, epics, and backlog rows.
- Added 5-character uppercase base36 unique IDs with local collision checks across trackers, backlog rows, and task folders.
- Added config-backed accepted doctor warning fingerprints and `doctor --show-accepted`.
- Added deterministic `project smoke-bomb` planning, fingerprint-bound transactional sanitization, explicit validation, client-agent handoff guidance, and safe deterministic ZIP export for agency-to-client delivery.
- Added a governed release contract with one authoritative version, locked validation, exact artifact receipts and digests, trusted PyPI publication, GitHub attestations, and immutable public install commands.

### Changed

- Restricted init to genuinely new repositories. Existing, legacy, invalid, and future repositories remain unchanged and receive the canonical upgrade command.
- Updated workflow validation, generated agent guidance, and README documentation to support configured unique IDs and accepted doctor warnings.

## 0.1.2 - 2026-06-04

### Added

- Added `project doctor` and `project validate` workflow-state validation commands.
- Added matching local workflow helper commands for initialized repositories.
- Added non-destructive `project init` refresh behavior for generated workflow and agent assets.
- Added `.project-workflow/guidance.md` as the user-owned repo-specific workflow guidance file.
- Added managed Project Workflow blocks for host-owned files such as `AGENTS.md` and `.github/copilot-instructions.md`.
- Added regression tests for doctor validation, agent-mode guidance installation, generated file refresh, managed blocks, and unmarked collision handling.

### Changed

- Updated README, local CLI docs, Codex guidance, Cursor rules, and generated prompt assets so agents know to run `doctor` after tracker/task-doc changes and read `.project-workflow/guidance.md` for repo-specific workflow guidance.

### Migration

- Existing users should run:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init
```

This refreshes marked generated files and managed host-file blocks so older local workflow helpers learn the new `doctor` and `validate` commands. Unmarked existing files are preserved; when a generated target collides with one, init writes the new content beside it as `*.new` for manual review.

## 0.1.1 - 2026-02-26

### Fixed

- Fixed `workflow task init` crash when `--update-tracker` is used without `--create-branch`.
- Hardened branch output handling so branch name is only referenced after successful branch creation.
- Updated packaged scaffold template so new installs receive the fix via `project init`.
