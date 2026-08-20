# project-workflow 0.5.0

### Added

- Added per-unit execution-needs metadata and deterministic executor selection across coordinator, bounded subagent, persistent task, and peer-team surfaces, independent of whether the target is a Task or Epic.
- Added host-neutral visible-subordinate disposition and retirement lifecycle state, with stable idempotent retirement intents, resumable reconciliation, conservative legacy-state migration, and explicit retention reasons.
- Added current-Codex subordinate creation, monitoring, verification, and archive capability proof plus cross-host generated guidance for Claude Code, Cursor, GitHub Copilot, and Codex.

### Changed

- Changed Delegate routing from target-kind defaults to work-property and runtime-capability decisions, including truthful free-capacity accounting, fail-closed fallbacks, and explicit surface/schedule reporting.
- Kept ordinary bounded work inside the coordinator task by default, while persistent visible tasks are reserved for work that actually needs durable resume, direct owner steering, isolated worktrees, or peer communication.
- Retained verified visible handles until durable integration or no-integration disposition is recorded; successful eligible subordinates can then retire automatically, while failed, orphaned, owner-attention, unintegrated, or explicitly retained work remains visible.
