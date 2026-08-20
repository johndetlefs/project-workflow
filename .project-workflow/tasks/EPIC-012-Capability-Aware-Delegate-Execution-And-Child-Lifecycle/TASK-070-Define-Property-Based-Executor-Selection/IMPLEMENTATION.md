## User Story

As a Delegate coordinator, I want one property-based selector, so that Task and Epic work use the lightest sufficient executor without invented capability.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC5, AC6, AC11

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

- AC1: owner `Property-Based Executor Selection`; required evidence: Target-kind-invariance and execution-property parsing/derivation tests.
- AC2: owner `Property-Based Executor Selection`; required evidence: Deterministic routing matrix covering coordinator, subagent, persistent task, and peer/team eligibility.
- AC3: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Capability/authority/fallback matrix with exact block or downgrade reasons and adapter-alignment evidence.
- AC4: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Current Codex contract evidence and tests separating task-creation authority from Epic approval.
- AC5: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement`; required evidence: Human/JSON schema snapshots and read-only plan/status non-mutation evidence.
- AC6: owner `Property-Based Executor Selection, Hybrid Runtime And Verified Child Retirement, Hosts And Compatibility`; required evidence: Existing work-packet, single-writer, reconciliation, failure, resume, QA, and closeout regression evidence.
- AC11: owner `Property-Based Executor Selection, Hosts And Compatibility`; required evidence: Compatibility fixtures, full locked suite, strict Doctor, build/package, and non-Delegate regression results.

## Acceptance Criteria

- [x] AC1: Execution-needs metadata is backward-compatible, distinct from capability evidence, and validated deterministically.
- [x] AC2: One selector covers coordinator, subagent, persistent-task, and peer-team with target-kind invariance and exact fallback/block reasons.
- [x] AC3: Human/JSON projections and existing scheduling, scope, lifecycle, and compatibility contracts remain truthful and stable.

## Validation

- AC1 / parent AC1, AC2: parser and legacy/default matrix.
- AC2 / parent AC1-AC4: selector/capability/authority/capacity matrix.
- AC3 / parent AC5, AC6, AC11: CLI snapshots, non-mutation, focused regressions, and mirrors.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/EPIC-012-delegate-executor-lifecycle | 131 focused and 395 full checks pass; strict Doctor and mirror checks pass | Local candidate only; not merged or released | `tests/test_delegation.py`, `tests/test_delegate_task_mode.py`, `tests/test_delegate_epic_mode.py` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- |
| 1 | Execution Needs Contract | Add compatible needs metadata and surface-specific capability vocabulary. | AC1 | Run parser/default/invalid-token tests. | Done | | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegation.py | No |
| 2 | Shared Executor Selector | Implement surface/schedule selection and replace target-kind branches. | AC2 | Run the full routing and target-kind-invariance matrix. | Done | 1 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegation.py, tests/test_delegate_task_mode.py, tests/test_delegate_epic_mode.py | No |
| 3 | Decision Projection | Extend human/JSON output with needs, visibility, executor, concurrency, and provenance. | AC3 | Compare stable snapshots and tracked-tree hashes. | Done | 2 | src/project_workflow/cli.py, src/project_workflow/templates/workflow.py, .project-workflow/cli/workflow.py, tests/test_delegate_cli.py | No |
| 4 | Selector Validation | Run focused compatibility, mirror, and Doctor checks and record proof boundaries. | AC1, AC2, AC3 | Review focused results and unchanged lifecycle gates. | Done | 3 | tests/test_delegation.py, tests/test_delegate_task_mode.py, tests/test_delegate_epic_mode.py, tests/test_delegate_cli.py | No |

## Parent AC Evidence

- AC1, AC2: execution-needs parsing, legacy defaults, target-kind invariance, four-surface routing, binding-need blocks, repository-scope collision, and child-slot accounting are covered in `tests/test_delegation.py`.
- AC3, AC4: current-host tri-state capability, explicit authority, generic retained-visible fallback, and stricter Codex creation requirements are covered in selector and host-asset matrices.
- AC5, AC6, AC11: schema-v2 projections, Task/shared-surface runtime consistency, resume/free-capacity regressions, byte-identical helpers, full regression, and strict Doctor pass.

## QA & Code Review

- Verdict: Pass
- Evidence: Independent read-only QA reported 131 focused checks, 395 full locked checks, strict Doctor, clean diff, and byte-identical helpers at CLI SHA-256 `164972ce90039feacce999c37792748d50a4d28bbbc883a721f0587fddff569d`.
- Findings: Initial runtime downgrades and free-capacity accounting defects were corrected and regression-tested; no remaining code blocker.

## Retro

- Reusable lessons: Select a surface from immutable work properties, keep schedule separate, and treat runtime free capacity as already excluding active workers.
- Conventions or agent assets updated: Delegate and Planner now use Execution Needs, four surfaces, tri-state capability provenance, and target-kind neutrality.
- Follow-up tasks: None required for this child.

## Notes

- Task: TASK-070
- Title: Define Property-Based Executor Selection
- Created: 2026-08-20
