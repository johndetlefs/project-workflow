## User Story

As a Delegate coordinator, I want selected executors and verified subordinate retirement to survive interruption, so that successful temporary tasks disappear without hiding unresolved work.

## Parent AC Coverage

- AC5, AC6, AC7, AC8, AC9, AC12, AC14

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

- AC5: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement`; required evidence: Human/JSON schema snapshots and read-only plan/status non-mutation evidence.
- AC6: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Existing work-packet, single-writer, reconciliation, failure, resume, QA, and closeout regression evidence.
- AC7: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Retirement eligibility, intent/outcome, idempotency, integration/disposition receipt, and live successful-cleanup evidence.
- AC8: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Parameterized exclusion-state tests and live attention-bearing retention evidence.
- AC9: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Retirement failure/unknown/resume/orphan tests proving retained handles and truthful state.
- AC12: owner `Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Sanitized dated current-Codex journey receipt covering subagent, persistent task, archival, coordinator survival, and no duplicates.
- AC14: owner `Hosts And Compatibility`; required evidence: QA, owner acceptance, lifecycle, integration, release, deployment, and adoption boundary regressions.

## Acceptance Criteria

- [x] AC1: Epic runtime honors the shared surface decision without weakening existing orchestration guarantees.
- [x] AC2: Durable disposition gates one stable retirement intent and an exact observed host acknowledgement.
- [x] AC3: Exclusion, failure, interruption, resume, legacy-state, and owner-retain paths preserve visibility and handles truthfully.

## Validation

- AC1 / parent AC5, AC6: hybrid executor and invariant regression tests.
- AC2 / parent AC7, AC12: disposition, retirement intent/ack, idempotency, and live Codex archival proof.
- AC3 / parent AC8, AC9, AC14: retention-state, failure/resume/migration, and lifecycle-boundary tests.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/EPIC-012-delegate-executor-lifecycle | Hybrid Task/Epic surface runtime and retirement matrices pass inside 131 focused and 395 full checks | Local candidate only; not merged or released | `tests/test_delegate_epic_mode.py`, `tests/test_delegate_task_mode.py` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- |
| 1 | Hybrid Epic Runtime | Consume shared executor decisions and add surface/visibility state without weakening orchestration. | AC1 | Run hybrid route, packet, dependency, failure, and capacity tests. | Done | | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_epic_mode.py | No |
| 2 | Durable Disposition Gate | Separate result verification from authoritative integration or verified no-integration disposition. | AC2 | Prove verified-but-unintegrated work remains visible and blocks retirement. | Done | 1 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_epic_mode.py | No |
| 3 | Retirement Reconciliation | Preserve handles and add stable retirement intent/requested/confirmed/failed/retained states with resume compatibility. | AC2, AC3 | Run exact-handle, idempotency, crash-window, legacy, and exclusion matrices. | Done | 2 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_epic_mode.py, tests/test_delegate_cli.py | No |
| 4 | Runtime Validation | Run focused Task/Epic/CLI compatibility and lifecycle-boundary tests. | AC1, AC2, AC3 | Review results and proof boundaries before host proof. | Done | 3 | tests/test_delegate_epic_mode.py, tests/test_delegate_task_mode.py, tests/test_delegate_cli.py | No |

## Parent AC Evidence

- AC5, AC6: `DelegationSurfaceOrchestrator` consumes immutable Task or Epic surface decisions while retaining single-writer, packet, scope, dependency, failure, and reconciliation gates.
- AC7, AC8, AC9: verified result and durable disposition are separate; stable retirement intent/outcome, exclusion states, retained handles, v1 migration, interruption, zero-free-capacity resume, and idempotency are covered by focused runtime tests.
- AC12: the runtime state supports the live Codex canary receipt owned by TASK-072; candidate execution remains automation-backed rather than claimed as live.
- AC14: runtime completion and retirement do not bypass independent QA, owner acceptance, closeout, or delivery gates.

## QA & Code Review

- Verdict: Pass
- Evidence: Independent read-only QA reported the hybrid, retirement, handle-preservation, peer-slot, and zero-free-capacity resume matrices passing within 131 focused and 395 full checks.
- Findings: Verification had initially been conflated with integration, and resume with creation eligibility; both were separated before acceptance.

## Retro

- Reusable lessons: A worker result, durable disposition, and visible-task retirement are three distinct coordinator-observed states; creation authority and free capacity must never gate reconciliation of an existing handle.
- Conventions or agent assets updated: Host-neutral retirement intent vocabulary and `DelegationSurfaceOrchestrator` now cover Task and Epic targets; `EpicOrchestrator` remains a compatibility alias.
- Follow-up tasks: None required for this child.

## Notes

- Task: TASK-071
- Title: Implement Hybrid Runtime And Verified Child Retirement
- Created: 2026-08-20
