# Requirements

## Summary

- Task: TASK-072
- Title: Align Hosts And Prove Compatibility
- Parent AC Coverage: AC3, AC4, AC5, AC7, AC8, AC10, AC11, AC12, AC13, AC14
- Last updated: 2026-08-20

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

- Delegate consumes existing approved scope and never creates execution authority.
- Target kind does not determine executor; the lightest surface that satisfies every binding property is selected.
- Unknown capability is not support, capacity is never hard-coded, and unmet binding properties block rather than silently downgrade.
- Native visible-task creation requires the explicit authority demanded by the current host.
- The coordinator is the only shared-state writer and the only verifier that may satisfy dependencies or issue retirement intent.
- Temporary visible tasks are retired only after verified terminal durable disposition and absence of unresolved attention; Codex uses reversible task archival.
- The coordinator and every active, uncertain, failed, orphaned, unintegrated, owner-promoted, explicitly retained, or attention-bearing task remain visible.
- Retirement is reversible where the host supports it, idempotent, observable, and resumable; task handles persist until success is verified.
- Host adapters perform native actions; the host-neutral core records requirements, decisions, intents, and verified outcomes.
- Worker scope, evidence, lifecycle, QA, closeout, privacy, and delivery boundaries from EPIC-010 remain intact.
- Unexercised hosts receive truthful expected behavior and safe fallback, never fabricated runtime validation.
- Existing non-Delegate behavior remains backward compatible.

### Invalid Substitutes

- Target kind, host brand, prompt prose, or an optimistic boolean substituted for per-unit execution needs and runtime-observed capability.
- A universal “always subagent,” “always persistent task,” “always team,” or “always archive” policy.
- Requirements/Epic approval substituted for current-host explicit task-creation authority.
- A worker completion claim substituted for coordinator verification and durable integration into the authoritative target or an explicit verified no-integration disposition with receipt.
- Marking a retirement intent as completed without observing the host result.
- Deleting tasks or transcripts presented as archival cleanup.
- Hiding active, failed, orphaned, unintegrated, or attention-bearing work to produce a clean sidebar.
- Unit tests or generated-asset parity presented as live proof of Claude Code, GitHub Copilot, Cursor, or unobserved Codex behavior.
- Delegate selection or cleanup presented as QA, owner acceptance, release, deployment, adoption, or effectiveness proof.

### Artifact Targets

- Host-neutral execution-needs and capability-aware selection model, human/JSON output, compatibility defaults, and tests under `src/project_workflow/` and required helper mirrors.
- Delegation runtime-state extensions for visibility class, retention policy, retirement intent/outcome, reconciliation, and retained-attention reasons.
- Updated Codex Delegate skill, common/host-specific prompts or agents, managed guidance, README, packaged resources, and init/upgrade/collision/rollback handling.
- Focused selection and retention suites, full locked regression, strict Doctor, build/package/mirror validation, and a sanitized current-Codex journey receipt.

### Parent AC Proof Ownership

- AC3: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Capability/authority/fallback matrix with exact block or downgrade reasons and adapter-alignment evidence.
- AC4: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Current Codex contract evidence and tests separating task-creation authority from Epic approval.
- AC5: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement`; required evidence: Human/JSON schema snapshots and read-only plan/status non-mutation evidence.
- AC7: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Retirement eligibility, intent/outcome, idempotency, integration/disposition receipt, and live successful-cleanup evidence.
- AC8: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Parameterized exclusion-state tests and live attention-bearing retention evidence.
- AC10: owner `Hosts And Compatibility`; required evidence: Host-specific syntax, generated/source parity, init/upgrade/collision/rollback, and package inspection results.
- AC11: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Compatibility fixtures, full locked suite, strict Doctor, build/package, and non-Delegate regression results.
- AC12: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Sanitized dated current-Codex journey receipt covering subagent, persistent task, archival, coordinator survival, and no duplicates.
- AC13: owner `Hosts And Compatibility`; required evidence: README/managed guidance examples checked against implemented routing and retention behavior.
- AC14: owner `Hosts And Compatibility`; required evidence: QA, owner acceptance, lifecycle, integration, release, deployment, and adoption boundary regressions.

## Goal

Ship truthful host guidance, managed assets, compatibility proof, and one minimal current-Codex journey for the new selection and retirement contract.

## Non-Goals

- Claiming live Claude Code, GitHub Copilot, or Cursor execution.
- Creating more than one visible Codex proof task or leaving successful proof clutter behind.
- Merge, release, deployment, or consumer upgrades.

## Users & Context

Project Workflow users installing or upgrading Codex, Claude Code, GitHub Copilot, or Cursor assets and relying on Delegate guidance to match implemented behavior.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Align all managed Delegate and surrounding Planner/Epic/Implement/QA guidance with property-based selection, current-host authority, and host-neutral retirement.
- Generate valid host-specific assets without leaking Copilot placeholders into Claude or Cursor.
- Bump and validate managed asset behavior, collision handling, upgrade fingerprints/rollback, release-contract contents, and exact-wheel journeys as required.
- Document positive and negative examples and the independent QA/delivery boundary.
- Prove current Codex with one in-thread subagent and no more than one explicitly authorized disposable persistent task, then archive that task after durable disposition.
- Run the complete locked suite, strict Doctor, builds, package/mirror/privacy checks, and record exact cross-host proof limits.

## Acceptance Criteria (Verifiable)

- AC1: Fresh init and upgrade for all four hosts install syntactically valid, semantically aligned Delegate assets with truthful unknown-capability fallback and tested collision/rollback/package behavior.
- AC2: Documentation and managed guidance explain the four surfaces, explicit Codex task authority, visibility/retirement classes, retained-attention states, and separate QA/delivery gates with usable examples.
- AC3: Full validation passes and a sanitized current-Codex journey proves subagent non-visibility, one persistent task's pre-disposition visibility and post-disposition archival, coordinator survival, and no duplicate actions; other hosts remain runtime-unvalidated.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Current Codex is the only live host claim for this Epic.
- Unknown retirement capability means visible-retained, never assumed cleanup.
- The proof task is disposable and must not remain in the active sidebar after successful verification.

## Validation Plan

- Run focused host-asset and packaging tests, four-host exact-wheel journeys, full pytest, strict Doctor, build/release contract, mirror/privacy checks, and the bounded Codex live receipt.
