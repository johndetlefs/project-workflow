# Changelog

All notable changes to this project are documented in this file.

## Unreleased

## 0.9.2 - 2026-08-31

### Added

- Added public `project execution configure`, `status`, and `disable` commands so operators can
  create and inspect exact host-neutral sealed authority without fabricating internal coordination
  JSON or hashes. Successor envelopes retain previous controls and receipts.

### Changed

- Documented Codex installation as repository-local skills plus a package-owned ephemeral per-run
  hook. A persistent marketplace-plugin listing is neither required nor treated as activation or
  runtime proof.

### Known proof boundary

- Sealed runtime execution is certified for Codex only in this release. The Claude Code adapter and
  managed assets remain packaged and fail closed, but no real authenticated Claude Code canary has
  passed; this release makes no Claude runtime or dual-host certification claim.

## 0.9.1 - 2026-08-29

### Changed

- Replaced the authored 25,583-line CLI monolith with cohesive, acyclic runtime domains, a bounded
  compatibility facade, and one deterministic manifest-driven standalone runtime without changing
  the public v0.9 command or schema contract.
- Split the catch-all Doctor tests into product-boundary suites, centralized only shared fixtures,
  and made locked Ruff, Ruff format, mypy, architecture, documentation, full-suite, and package
  journey checks part of both CI and release validation.
- Replaced the oversized README and stale release guidance with a small authority-led documentation
  hierarchy covering architecture, use, contribution, maintenance, and release ownership.

### Fixed

- Kept a completed Task or Epic's retained verification campaign inspectable from terminal global
  tracker state so Doctor and delivery projection do not lose exact-candidate proof after closeout.
- Removed dead distribution globs and stale current-version guidance while retaining historical
  workflow records, exact release artifacts, blocked proof obligations, and unique work.

## 0.9.0 - 2026-08-29

### Added

- Added the host-neutral sealed execution, progress, candidate, capability, typed-limit, and
  input-bound receipt contract on the existing Coordinator state, with different host-native units
  preserved rather than normalized.
- Added model-free `project execute --id` and `project release --id` preflight plus matching
  coordination status and Doctor projection; material work fails closed until current sealed
  authority and every binding host control are verified.
- Added one source-bound QA findings campaign with sealed-scope remediation, changed-input progress,
  affected-proof closure, and exact one-broad-QA accounting.
- Added authoritative single-candidate promotion and a terminal fixed-release executor with clean
  source/artifact checks, argv-only operations, exact invocation receipts, and one unchanged-input
  infrastructure retry.
- Added the subordinate Codex App Server adapter with exact executable/configuration negotiation,
  isolated synchronous hooks, atomic native limit reservation, required-change and source/scope
  closeout, package-owned plugin assets, and core-owned typed receipts.
- Added the subordinate Claude Code print-mode adapter with exact executable/version/authentication
  negotiation, model-free hook activation preflight, fail-closed native `dontAsk` permissions,
  streamed initialization/result supervision, process-tree termination, exact output/validator
  obligations, native USD-micro/turn/elapsed limits, self-contained managed assets, and core-owned
  typed terminal receipts for both successful and failed dispatches.

### Changed

- Kept working revisions, verification candidates, and release candidates distinct so ordinary
  implementation failures do not create rejected release-candidate churn and promotion requires
  implementation, verification, QA, and affected-proof obligations to pass.
- Kept fixed release free of source repair, QA, product-failure retry, and replacement-candidate
  authority; external push, merge, publication, installation, and rollout remain separate gates.
- Refactored the useful FIX-010 state, hook, App Server, and adversarial-test mechanisms behind
  `project execute`; retired its public enforcement command, repository-static activation, fixed
  token budget, and independent release truth.
- Made Status and Doctor treat explicit failing structured evidence and blocked parent-AC evidence
  as non-passing instead of allowing prose references or absent trigger heuristics to conceal them.

### Known proof boundary

- The Claude Code adapter and its managed assets are included and fail closed when their exact
  runtime, authentication, hook activation, native permission, or required-output contract is not
  verified. v0.9.0 has deterministic, package, and affected-remediation evidence for that adapter,
  but it has not yet completed the required real authenticated Claude Code canary; the release does
  not claim current Claude runtime certification or completed cross-host conformance.

## 0.8.0 - 2026-08-27

### Added

- Added an optional, durable verification campaign inside the existing Coordinator lifecycle,
  binding exact candidate, source, proof contract, claims, scope, ordered stages, limits, and
  input-current typed receipts before materially expensive verification begins.
- Added generic manual and command/JSON verifier adapters with capability negotiation, exact
  request/receipt identity binding, evaluator-only zero-target regrade, and consumer-independent
  operation.
- Added deterministic operational states for implementation, verification, QA, delivery readiness,
  and blocked work, plus sanitized end-to-end invocation-count dogfood and adversarial countercases.

### Changed

- Changed material verification to progress from cheap canary/affected proof to full certification,
  while unknown material impact fails safely toward broader proof and cheap work retains the normal
  lifecycle without extra ceremony.
- Changed verification continuation so certification stops on the first product failure, diagnostics
  require a separately named bounded decision, and only one infrastructure retry can be retained.
- Changed resolved independent QA handling so the original verdict is preserved and one named
  affected validation disposition closes the finding without another QA invocation.

### Fixed

- Fixed expensive first-green release campaigns being able to continue into full verification after
  an earlier blocking stage failed or declared limits were exhausted.
- Fixed omitted, stale, redefined, rehashed, malformed, and over-limit campaign evidence appearing
  current enough to advance Review or Complete.
- Fixed evaluator-only changes rerunning target work, and fixed verifier/adaptor failures escaping
  retained bounded attempt accounting.

## 0.7.0 - 2026-08-24

### Added

- Added one owner-facing Coordinator that carries approved intent through requirements, planning,
  proportionate execution, independent QA, and delivery while keeping Delegate as the compatible
  execution graph.
- Added compact contract-version-2 coordination state with explicit context loading, source-bound
  drift decisions at five lifecycle boundaries, and an earliest sufficient outcome checkpoint.
- Added sanitized behavioural evaluations for drift prevention, Clarify routing, context choice,
  fan-out, stopping behaviour, and preservation of required quality controls.

### Changed

- Changed Clarify to resolve material ambiguity at intake, after planning, or at a detected drift
  boundary without becoming a periodic reviewer or creating another QA loop.
- Changed execution-surface selection so every added context, agent, task, or handoff must earn its
  overhead through a named dependency, risk, authority, or evidence need.
- Changed QA completion so one preserved `Changes Requested` verdict can close through named
  affected validation and an explicit resolved disposition without commissioning a second review.

### Fixed

- Fixed stale coordination decisions remaining usable after source or repository authority changed.
- Fixed long-running work drifting through narrowing, omission, proxy substitution, stale context,
  or unverified worker returns without a deterministic lifecycle block.
- Fixed post-proof continuation that could repeat broad validation or review after sufficient proof
  had already passed.

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
