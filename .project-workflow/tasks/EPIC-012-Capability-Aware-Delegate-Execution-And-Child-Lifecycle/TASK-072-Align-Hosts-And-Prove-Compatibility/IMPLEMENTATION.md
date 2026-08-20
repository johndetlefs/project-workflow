## User Story

As a Project Workflow user, I want installed Delegate guidance and packaging to match the implemented hybrid policy, so that every host degrades truthfully and Codex leaves no successful proof clutter.

## Parent AC Coverage

- AC3, AC4, AC5, AC7, AC8, AC10, AC11, AC12, AC13, AC14

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

## Acceptance Criteria

- [x] AC1: Four-host managed assets, upgrade/collision/rollback behavior, and packages carry the truthful property/retirement contract.
- [x] AC2: Documentation provides tested surface-selection, retention, and QA-boundary examples.
- [x] AC3: Full deterministic/package validation and the minimal current-Codex proof pass with exact proof boundaries.

## Validation

- AC1 / parent AC3, AC4, AC5, AC10, AC11: host asset/init/upgrade/collision/rollback/release tests.
- AC2 / parent AC8, AC13, AC14: semantic guidance and documentation inspection.
- AC3 / parent AC7, AC11, AC12: focused/full suite, strict Doctor, builds/packages/mirrors/privacy, and sanitized Codex receipt.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/EPIC-012-delegate-executor-lifecycle | 131 focused and 395 full checks; strict Doctor; source contract; build; exact-wheel four-host journey | Local candidate only; not merged or released | `EVIDENCE.json`, `evidence/final-validation.json`, `evidence/package-journey.json`, `evidence/current-codex-lifecycle-receipt.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- |
| 1 | Host Contract Alignment | Rewrite Codex and common/generated host guidance around property selection, authority, visibility, and retirement. | AC1, AC2 | Inspect all four generated host outputs and syntax invariants. | Done | | src/project_workflow/prompts, src/project_workflow/codex, src/project_workflow/cursor, .github/prompts, .agents/skills, README.md | Yes |
| 2 | Managed Asset And Package Alignment | Update asset version, managed blocks, upgrade/collision/rollback, Doctor, release contract, and package journeys. | AC1 | Run four-host init/upgrade and exact-wheel package tests. | Done | 1 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, scripts, tests/test_delegate_host_assets.py, tests/test_doctor.py, tests/test_release_contract.py | No |
| 3 | Current Codex Proof | Run one in-thread subagent and at most one persistent proof task through verified durable disposition and archival, recording sanitized evidence. | AC3 | Confirm no sidebar increase for subagent, proof-task archival, coordinator survival, and no duplicates. | Done | 2 | .project-workflow/tasks/EPIC-012-Capability-Aware-Delegate-Execution-And-Child-Lifecycle/TASK-072-Align-Hosts-And-Prove-Compatibility | No |
| 4 | Full Validation And QA Handoff | Run focused/full tests, strict Doctor, build/package/mirror/privacy checks, and record cross-host boundaries. | AC1, AC2, AC3 | Review final receipts and independent QA findings. | Done | 3 | tests, scripts, .project-workflow/tasks/EPIC-012-Capability-Aware-Delegate-Execution-And-Child-Lifecycle | No |

## Parent AC Evidence

- AC3, AC4, AC5, AC7, AC8, AC10, AC11, AC12, AC13, AC14: passing structured claims in `EVIDENCE.json` bind the final CLI identity to the build/package receipt and the separately bounded current-Codex lifecycle receipt.
- Current Codex: one visible canary was created from committed base, reconciled clean, archived only after verified no-integration disposition, confirmed absent from the active list, and recorded without native IDs or transcripts.
- Cross-host boundary: Codex current-session host actions were observed; Claude Code, GitHub Copilot, and Cursor were syntax-, package-, init-, Doctor-, and upgrade-validated but not runtime-validated.

## QA & Code Review

- Verdict: Pass
- Evidence: Independent QA found no remaining code blocker after 131 focused and 395 full checks, strict Doctor, clean diff, byte-identical helpers, and the resume/capacity corrections. Exact-wheel four-host journey and sanitized Codex receipt are retained child-locally.
- Findings: Codex needed an explicit every-persistent-child isolation rule; generic hosts without retirement correctly remain visible-retained. Live canary proves host actions from committed base, not candidate execution.

## Retro

- Reusable lessons: Host guidance must distinguish generic core capability from stricter host policy, and live receipts must state which source actually executed.
- Conventions or agent assets updated: Delegate/Planner prompts, Codex skills, managed AGENTS/Cursor guidance, README examples, manifest asset version 3, and host-asset tests were updated.
- Follow-up tasks: Runtime validation for Claude Code, GitHub Copilot, and Cursor remains future work only when those hosts are available; it is not required for this child.

## Notes

- Task: TASK-072
- Title: Align Hosts And Prove Compatibility
- Created: 2026-08-20
