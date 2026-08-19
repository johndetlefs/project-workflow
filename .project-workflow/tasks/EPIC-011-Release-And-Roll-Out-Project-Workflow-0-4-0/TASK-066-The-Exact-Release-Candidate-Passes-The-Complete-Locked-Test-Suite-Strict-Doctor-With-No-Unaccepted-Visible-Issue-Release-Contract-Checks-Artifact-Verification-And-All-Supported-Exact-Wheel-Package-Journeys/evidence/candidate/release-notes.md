# project-workflow 0.4.0

### Added

- Added capability-aware `delegate plan` and `delegate status` commands for coordinating exactly one approved Task or Epic through a deterministic dependency graph.
- Added Task implementation-row and Epic child-task delegation modes with bounded work packets, coordinator-only shared workflow mutation, scope and validation reconciliation, dependency release, failure isolation, terminal summaries, and resumable runtime state.
- Added native current-Codex Task-mode and Epic-mode journey evidence, plus deterministic four-host packaged-asset coverage and exact-wheel release validation.

### Changed

- Replaced the legacy fixed-capacity Delegate prompt with runtime-observed tri-state capability handling, safe sequential/coordinator fallback, explicit write-scope collision rules, and host-specific generated assets.
- Tightened the lifecycle gate so a Task cannot enter Testing until every required implementation row is Done; Delegate cannot bypass this integrity gate.
- Updated generated skills, prompts, instructions, status guidance, Doctor diagnostics, package journeys, and release validation for the Delegate execution contract.
