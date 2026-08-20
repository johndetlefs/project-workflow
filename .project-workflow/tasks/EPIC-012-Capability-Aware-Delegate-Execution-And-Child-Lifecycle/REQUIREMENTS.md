# Requirements

## Summary

- Task: EPIC-012
- Title: Capability-Aware Delegate Execution And Child Lifecycle
- Last updated: 2026-08-20

## User Story

As a Project Workflow owner, I want Delegate to choose the lightest execution surface that actually satisfies each approved unit's needs and to retire temporary visible child tasks after their results are safely reconciled, so that delegation remains effective without overrunning my project sidebar or weakening recovery and governance.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-20
- Approval note / source: Codex task owner message: Yeah, that's fine, go for it. (2026-08-20)
- Approved artifact identity: sha256:386b46efb54e618a1174d5a8f1c75f0cb5b5a288e95f2d38d67c2249440bf761

## Goal

Correct Delegate's coarse Task-versus-Epic executor mapping. Select coordinator work, in-session subagents, isolated/background tasks, or peer-capable teams from explicit execution needs and runtime-observed host capabilities; then apply a safe, reversible retention policy to any temporary user-visible tasks.

## Non-Goals

- Preferring one execution surface universally or replacing Project Workflow's existing Task, Epic, Implement, QA, or closeout semantics.
- Creating user-visible tasks without the explicit authority required by the current host.
- Archiving the coordinator, owner-promoted work, active work, failed work, orphaned work, unintegrated results, or anything awaiting owner attention.
- Deleting tasks or transcripts; archival is reversible sidebar cleanup, not evidence destruction.
- Claiming token savings, native multi-agent support, or equivalent orchestration on hosts not observed at runtime.
- Building a remote orchestration service, changing host UI behavior, or implementing provider-specific agents inside the Python core.
- Reopening the already-delivered EPIC-010 graph, lifecycle, QA, or evidence scope except where needed for this executor-selection and retention correction.
- Merging, releasing, or upgrading consumer repositories as part of implementation without separate delivery authority.

## Users & Context

- The owner runs multiple projects in Codex and needs the sidebar to remain a useful record of primary work rather than a residue of subordinate orchestration.
- A bounded implementation unit may need only an in-session subagent; a durable or isolated workstream may justify a visible background task; tightly coupled work may be safest with the coordinator; direct peer communication may justify a team surface when a host actually supports it.
- Codex, Claude Code, GitHub Copilot, and Cursor expose different and changing agent surfaces. Project Workflow must reason from observed capability and current authority, not from brand names or optimistic prompt text.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Each delegation unit must expose or conservatively derive the execution properties that matter to routing: isolation, durability/recovery, communication topology, owner-interaction/visibility, parallel safety, write scope, and repository scope.
- The host-neutral resolver must select the lightest sufficient surface from coordinator, in-session subagent, persistent/background task, and peer-capable team; target kind alone must never determine the executor.
- Native launch requires verified current-host capability, available capacity, and any host-required explicit authority. Capability evidence must distinguish surface-specific isolation and lifecycle support, including isolated subagents, isolated persistent tasks, task retirement, and retirement reconciliation. Unknown capability must not be treated as support.
- Safe sequential or coordinator fallback is permitted only when it still satisfies the unit's requirements. A binding unmet requirement must block with a precise reason rather than silently downgrade.
- Task rows and Epic children may use different surfaces within one run. In particular, an Epic child may use an in-session subagent when persistence and owner interaction are unnecessary, while a Task unit may use an isolated persistent task when its approved needs and authority require one.
- Direct worker-to-worker/team execution is justified only by an explicit peer-communication requirement and verified host support; ordinary dependency graphs remain coordinator-mediated.
- Planning and status output must explain the required properties, requested and effective executor, capacity, visibility, retention policy, capability provenance, and every fallback or block reason in human and versioned JSON forms.
- The coordinator remains the only writer of shared workflow state and the only authority that verifies identity, source, scope, validation, evidence, integration, and dependency satisfaction.
- A temporary user-visible subordinate task defaults to retirement-on-verified only after its result is coordinator-verified, terminal, and either durably integrated into the authoritative target or explicitly closed with a verified no-integration disposition and durable receipt, with no unresolved child-local or owner attention. The Codex adapter maps retirement to reversible task archival; hosts without verified retirement remain visible and reported.
- Active, returned-but-unverified, failed, rejected, orphaned, blocked, awaiting-owner, unintegrated, explicitly retained, and owner-promoted tasks must remain visible. The coordinator is never archived by Delegate.
- Retirement must be idempotent and resumable. Failed or unknown outcomes remain pending and retain their task handle; Delegate must never claim cleanup it has not observed.
- Host adapters must perform native launch, monitoring, reconciliation, and retirement. The host-neutral core may emit intents and record verified outcomes but must not pretend that a prompt or test double proves a host action.
- Managed Codex, Claude Code, GitHub Copilot, and Cursor guidance must express the same property-based policy using host-appropriate syntax, with truthful fallback on unverified surfaces.
- Existing repositories and legacy delegation plans must remain compatible through conservative defaults; non-Delegate lifecycle, QA, workspace, upgrade, package, and Doctor behavior must not regress.
- Current-Codex proof must use the fewest visible subordinate tasks needed to prove the behavior and leave no successful disposable proof task cluttering the sidebar when the run ends.

## Acceptance Criteria (Verifiable)

- AC1: Given any approved Task or Epic unit, the resolver deterministically evaluates isolation, durability/recovery, communication topology, owner interaction, parallel safety, write scope, and repository scope; changing only the Task-versus-Epic label does not change an otherwise identical executor decision.
- AC2: Given verified sufficient capability and capacity, bounded coordinator-mediated work selects an in-session subagent; persistence, cross-session recovery, owner interaction, or required isolated ownership may select a persistent/background task; an explicit peer-communication need may select a team surface; coupled or unsafe work remains coordinator-owned or sequential.
- AC3: Given unknown, unsupported, exhausted, or unauthorized capability, the plan either uses a reported safe fallback that still meets all binding properties or blocks before launch with the exact unmet property; it never fabricates parallelism, persistence, isolation, monitoring, reconciliation, peer messaging, or retirement support.
- AC4: Given current Codex policy, persistent child-task creation requires an explicit owner request applicable to that run in addition to verified create, isolate, monitor, reconcile, and task-retirement capabilities; an Epic approval by itself is not treated as task-creation authority.
- AC5: Human and schema-versioned JSON plan/status output identifies every unit's required properties, requested and effective executor, effective concurrency, visibility class (`ephemeral`, `visible-retirable`, or `visible-retained`), retention policy, capability status/source, and selection, fallback, or block reason, without launching or retiring work.
- AC6: Given a launched worker, existing single-writer, work-packet, scope, validation, evidence, dependency, failure, resume, orphan, QA, and closeout guarantees remain enforced regardless of executor surface.
- AC7: Given a temporary visible subordinate task whose result is terminal, coordinator-verified, durably integrated into the authoritative target or explicitly closed with a verified no-integration disposition and receipt, and free of unresolved attention, Delegate emits one stable retirement intent and records an observed successful host action idempotently; resume does not relaunch or re-retire it. In Codex, that host action is task archival.
- AC8: Given an active, unverified, failed, rejected, orphaned, blocked, awaiting-owner, unintegrated, explicitly retained, or owner-promoted task—or the coordinator itself—Delegate does not retire it and reports the retention reason.
- AC9: Given retirement failure, unknown completion, coordinator interruption, or stale runtime state, the task handle is retained, cleanup remains pending or orphaned, and reconciliation can resume without falsely claiming success or losing diagnostic access.
- AC10: Generated and installed Codex, Claude Code, GitHub Copilot, and Cursor Delegate assets express the property-based selection and retention contract in valid host-specific syntax; source/generated mirrors, upgrade behavior, collision handling, and package contents are tested. Unexercised hosts are described as expected/aligned, not runtime-validated.
- AC11: Legacy repositories and legacy delegation metadata continue to plan safely with documented conservative defaults, while the complete locked test suite, strict Doctor, build/package checks, and focused non-Delegate regressions pass.
- AC12: A minimal current-Codex journey proves at least one bounded unit uses an in-session subagent without creating a sidebar task, and uses no more than one explicitly authorized disposable persistent proof task; that task remains visible while unverified, is reconciled and archived only after verified durable disposition, the coordinator remains visible, and no duplicate launch or archive occurs after resume.
- AC13: Documentation gives decision-oriented positive and negative examples for coordinator, subagent, persistent task, and peer/team execution and explains that archive-on-verified is the default for temporary visible subordinates, not a blanket cleanup rule.
- AC14: Existing independent QA, owner acceptance, integration, release, deployment, and adoption gates remain separate; Delegate's executor or archive result cannot satisfy them.

## Open Questions (Answer Needed)

- None. The exact requirements and AC1-AC14 await the single owner approval envelope.

## Decisions (Resolved)

- Decision: Correct the model rather than simply switching all work to subagents or archiving every created task.
- Decision: Use property-based selection. Workflow target kind is context, not executor policy.
- Decision: Prefer the lightest sufficient executor, where sufficiency includes safety, durability, recovery, communication, authority, and owner visibility—not merely speed or token cost.
- Decision: Keep ordinary dependencies coordinator-mediated; require explicit peer-communication need before selecting a team surface.
- Decision: Treat current-host explicit task-creation authority as distinct from requirements or Epic approval.
- Decision: Default temporary visible subordinate tasks to archive-on-verified, preserve every attention-bearing state, and never delete task history.
- Decision: Keep the host-neutral policy and state machine in Project Workflow; use thin host adapters for native actions.
- Decision: Implement this as a compact corrective Epic because executor policy, runtime lifecycle, four host assets, and live cleanup proof cross one bounded Task boundary.
- Decision: Implement the Epic itself with in-thread agents/coordinator work. Do not create persistent sidebar tasks for its child implementation rows.

## Validation Plan

- Add deterministic matrix tests covering property combinations, capability tri-state/provenance, capacity, authority, safe fallback, blocking, mixed surfaces, and target-kind invariance.
- Add lifecycle tests covering archive eligibility, exclusion states, intent/outcome separation, idempotency, failure, resume, orphaning, retained handles, and coordinator protection.
- Add human/JSON schema and read-only non-mutation tests.
- Add generated/source asset, init/upgrade/collision/rollback, package-content, and host-specific syntax tests for Codex, Claude Code, GitHub Copilot, and Cursor.
- Run `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`, strict Doctor, build/package validation, helper-mirror checks, and `git diff --check`.
- Run a minimal dated current-Codex journey matching AC12. Treat other hosts as contract-aligned but runtime-unvalidated.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Define Property-Based Executor Selection | AC1, AC2, AC3, AC4, AC5, AC6, AC11 | Add the execution-needs model, deterministic capability/authority router, compatibility defaults, output contract, and focused matrix tests. |
| Implement Hybrid Runtime And Verified Child Retirement | AC5, AC6, AC7, AC8, AC9, AC12, AC14 | Let Epic units use the selected surface, preserve opaque handles through durable disposition, add retirement policy/intents/observed outcomes, and prove idempotent reconciliation and safe retention. Depends on executor selection. |
| Align Hosts And Prove Compatibility | AC3, AC4, AC5, AC7, AC8, AC10, AC11, AC12, AC13, AC14 | Align Codex, Claude Code, GitHub Copilot, and Cursor assets, valid syntax, packaging, upgrades, documentation, full regression, and the minimal current-Codex journey. Depends on executor selection and hybrid runtime. |
