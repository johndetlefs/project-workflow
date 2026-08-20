# Epic Contract

## Summary

- Epic: EPIC-012
- Title: Capability-Aware Delegate Execution And Child Lifecycle
- Last updated: 2026-08-20

## Sources of Truth

- Product and authority envelope: this Epic's approved `REQUIREMENTS.md` identity.
- Approved child authority: this Epic's `DECOMPOSITION.md`, tracker, and any owner-approved amendments.
- Existing Delegate guarantees: EPIC-010 artifacts, current delegation graph/runtime schemas, lifecycle gates, QA evidence, and focused tests.
- Executor policy: the versioned host-neutral execution-needs, capability, selection, visibility, and retention contracts in source and tests.
- Host capability and authority: current callable host contracts plus runtime observations and the current owner's explicit request; packaged prose alone is not proof.
- Native child lifecycle: host-observed creation, monitoring, reconciliation, retirement, and resume results recorded in ignored runtime state without private transcripts or credentials; Codex retirement maps to task archival.
- Packaged delivery: source/generated mirrors, managed upgrade plans, built artifacts, and fresh installed-consumer inspections.

## Invalid Substitutes

- Target kind, host brand, prompt prose, or an optimistic boolean substituted for per-unit execution needs and runtime-observed capability.
- A universal “always subagent,” “always persistent task,” “always team,” or “always archive” policy.
- Requirements/Epic approval substituted for current-host explicit task-creation authority.
- A worker completion claim substituted for coordinator verification and durable integration into the authoritative target or an explicit verified no-integration disposition with receipt.
- Marking a retirement intent as completed without observing the host result.
- Deleting tasks or transcripts presented as archival cleanup.
- Hiding active, failed, orphaned, unintegrated, or attention-bearing work to produce a clean sidebar.
- Unit tests or generated-asset parity presented as live proof of Claude Code, GitHub Copilot, Cursor, or unobserved Codex behavior.
- Delegate selection or cleanup presented as QA, owner acceptance, release, deployment, adoption, or effectiveness proof.

## Invariants

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

## Artifact Targets

- Host-neutral execution-needs and capability-aware selection model, human/JSON output, compatibility defaults, and tests under `src/project_workflow/` and required helper mirrors.
- Delegation runtime-state extensions for visibility class, retention policy, retirement intent/outcome, reconciliation, and retained-attention reasons.
- Updated Codex Delegate skill, common/host-specific prompts or agents, managed guidance, README, packaged resources, and init/upgrade/collision/rollback handling.
- Focused selection and retention suites, full locked regression, strict Doctor, build/package/mirror validation, and a sanitized current-Codex journey receipt.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-070 | Target-kind-invariance and execution-property parsing/derivation tests. |
| AC2 | TASK-070 | Deterministic routing matrix covering coordinator, subagent, persistent task, and peer/team eligibility. |
| AC3 | TASK-070, TASK-072 | Capability/authority/fallback matrix with exact block or downgrade reasons and adapter-alignment evidence. |
| AC4 | TASK-070, TASK-072 | Current Codex contract evidence and tests separating task-creation authority from Epic approval. |
| AC5 | TASK-070, TASK-071, TASK-072 | Human/JSON schema snapshots and read-only plan/status non-mutation evidence. |
| AC6 | TASK-070, TASK-071 | Existing work-packet, single-writer, reconciliation, failure, resume, QA, and closeout regression evidence. |
| AC7 | TASK-071, TASK-072 | Retirement eligibility, intent/outcome, idempotency, integration/disposition receipt, and live successful-cleanup evidence. |
| AC8 | TASK-071, TASK-072 | Parameterized exclusion-state tests and live attention-bearing retention evidence. |
| AC9 | TASK-071 | Retirement failure/unknown/resume/orphan tests proving retained handles and truthful state. |
| AC10 | TASK-072 | Host-specific syntax, generated/source parity, init/upgrade/collision/rollback, and package inspection results. |
| AC11 | TASK-070, TASK-072 | Compatibility fixtures, full locked suite, strict Doctor, build/package, and non-Delegate regression results. |
| AC12 | TASK-071, TASK-072 | Sanitized dated current-Codex journey receipt covering subagent, persistent task, archival, coordinator survival, and no duplicates. |
| AC13 | TASK-072 | README/managed guidance examples checked against implemented routing and retention behavior. |
| AC14 | TASK-071, TASK-072 | QA, owner acceptance, lifecycle, integration, release, deployment, and adoption boundary regressions. |
