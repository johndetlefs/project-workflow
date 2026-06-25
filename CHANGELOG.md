# Changelog

All notable changes to this project are documented in this file.

## Unreleased

### Added

- Added configurable sequential or unique workflow ID generation for tasks, epics, and backlog rows.
- Added 5-character uppercase base36 unique IDs with local collision checks across trackers, backlog rows, and task folders.

### Changed

- Updated workflow validation, generated agent guidance, and README documentation to support configured unique IDs.

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
