# Changelog

All notable changes to this project are documented in this file.

## Unreleased

## 0.6.0 - 2026-08-21

### Added

- Added one- or two-sentence plain-language Intent and stable outcome commitments to current Task and Epic requirements, with meaning-first approval summaries that ask the owner to confirm the requested outcome rather than approve IDs and hashes.
- Added sourced Epic intent audits, semantic narrowing classifications, current-identity lifecycle gates, child outcome-proof ownership, adversarial QA checks, deterministic behavioral fixtures, and inspectable end-to-end dogfood evidence.
- Added packaged four-host journeys and source/package parity checks for the intent-integrity contract, including current and legacy upgrade paths.

### Changed

- Changed readiness, status, QA and closeout evidence so green implementation proxies cannot substitute for the approved user outcome; Epic status now aggregates child-owned outcome evidence and preserves explicit validation boundaries.
- Added continuation sufficiency and materiality gates so post-pass work stops when the approved outcome is proven, while material contradictions still reopen the relevant validation layer.

### Fixed

- Fixed status projections that could obscure missing Epic-level outcome proof behind otherwise complete child lifecycle state.
- Fixed continuation guidance that could over-expand a bounded review into low-value deep dives after sufficient proof had already been obtained.
- Fixed historical structured-evidence checks so retained wheel members or recorded ancestor commits remain verifiable after later source revisions instead of forcing completed proof to track a moving file.

## 0.5.1 - 2026-08-20

### Fixed

- Preserved complete logical bullets, including indented and lazy continuation lines, when Epic contract invariants, invalid substitutes, and artifact targets are copied into child charters.
- Added fail-closed readiness and Doctor diagnostics for the exact legacy first-line truncation signature in active Epic child requirements and implementation documents.

## 0.5.0 - 2026-08-20

### Added

- Added per-unit execution-needs metadata and deterministic executor selection across coordinator, bounded subagent, persistent task, and peer-team surfaces, independent of whether the target is a Task or Epic.
- Added host-neutral visible-subordinate disposition and retirement lifecycle state, with stable idempotent retirement intents, resumable reconciliation, conservative legacy-state migration, and explicit retention reasons.
- Added current-Codex subordinate creation, monitoring, verification, and archive capability proof plus cross-host generated guidance for Claude Code, Cursor, GitHub Copilot, and Codex.

### Changed

- Changed Delegate routing from target-kind defaults to work-property and runtime-capability decisions, including truthful free-capacity accounting, fail-closed fallbacks, and explicit surface/schedule reporting.
- Kept ordinary bounded work inside the coordinator task by default, while persistent visible tasks are reserved for work that actually needs durable resume, direct owner steering, isolated worktrees, or peer communication.
- Retained verified visible handles until durable integration or no-integration disposition is recorded; successful eligible subordinates can then retire automatically, while failed, orphaned, owner-attention, unintegrated, or explicitly retained work remains visible.

## 0.4.0 - 2026-08-20

### Added

- Added capability-aware `delegate plan` and `delegate status` commands for coordinating exactly one approved Task or Epic through a deterministic dependency graph.
- Added Task implementation-row and Epic child-task delegation modes with bounded work packets, coordinator-only shared workflow mutation, scope and validation reconciliation, dependency release, failure isolation, terminal summaries, and resumable runtime state.
- Added native current-Codex Task-mode and Epic-mode journey evidence, plus deterministic four-host packaged-asset coverage and exact-wheel release validation.

### Changed

- Replaced the legacy fixed-capacity Delegate prompt with runtime-observed tri-state capability handling, safe sequential/coordinator fallback, explicit write-scope collision rules, and host-specific generated assets.
- Tightened the lifecycle gate so a Task cannot enter Testing until every required implementation row is Done; Delegate cannot bypass this integrity gate.
- Updated generated skills, prompts, instructions, status guidance, Doctor diagnostics, package journeys, and release validation for the Delegate execution contract.

## 0.3.0 - 2026-07-29

### Added

- Added read-only operational status in human and versioned JSON forms, with focused work-item inspection, strict health handling, explicit proof and delivery layers, and deterministic next actions.
- Added optional parent-workspace mode with one authoritative workflow repository and a registry of nested independent Git repositories.
- Added workspace-aware repository selectors and Git inspection so dirty, detached, unavailable, or wrong-branch child state cannot be hidden by the parent repository.
- Added registered primary/touched repository scope and repository-attributed validation, branch/PR, integration, release, and deployment evidence across task, Fix, and Epic-child lifecycle gates.
- Added retained generated-helper acceptance coverage for the complete disposable workspace lifecycle from initialization and approval through readiness, focused status, QA, completion, and handoff.

### Changed

- Reframed the product constitution around Project Workflow as an open, owner-usable delivery enabler driven by real adoption evidence rather than hypothetical scale.
- Updated README, managed agent instructions, prompts, skills, Doctor, upgrade behavior, and packaged/local CLI surfaces for workspace authority and evidence attribution.
- Updated the saved Codex worktree environment to use the locked Python 3.10 development setup with a writable UV cache.

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
