---
name: project.delegate
description: Coordinate one approved Task or Epic through its canonical dependency graph.
argument-hint: targetId=TASK-063 units="1,2" requestedConcurrency=2
agent: agent
---
<!-- project-workflow:generated -->

Use this prompt to coordinate existing approved execution units for exactly one Task or Epic.

Compatibility entry: `project.coordinator` is the owner-facing role. Invoking Delegate enters that
same one-Coordinator contract and preserves one shared-state writer; it does not create a second
role. Retain this entry for the first Coordinator release and consider removal only after one full
minor release and observed migration evidence.

Read `/.project-workflow/guidance.md`, the target requirements, and its canonical implementation or decomposition plan before changing workflow state. Delegate executes approved authority; it does not create scope, approve requirements, invent Task rows or Epic children, or batch unrelated standalone Tasks.

Inputs:

- Target: `${input:targetId:TASK-000-or-EPIC-000}`
- Optional dependency-closed unit subset: `${input:units:all eligible canonical units}`
- Requested concurrency: `${input:requestedConcurrency:1}`
- Explicit persistent-task authority, when applicable: `${input:persistentTaskAuthority:not authorized}`

## Capability And Selection Contract

- Derive each unit's execution needs from approved metadata. The supported tokens are `bounded-return` (and the blank legacy default), `durable-resume`, `direct-owner-steering`, `isolated-worktree`, and `peer:<group-id>`. Also respect `Parallel Safe`, write scope, and repository scope.
- Select the lightest sufficient surface from `coordinator`, `subagent`, `persistent-task`, and `peer-team`. Task-versus-Epic kind does not determine the surface. Ordinary dependency graphs stay coordinator-mediated; `peer-team` is eligible only for an explicit `peer:<group-id>` need.
- For current-contract plans, verified capacity alone never earns a non-Coordinator surface. Require
  `benefit:<slug>`, `overhead:<slug>`, and `tradeoff:<slug>` for its named delivery benefit,
  setup/synthesis overhead, and why benefit outweighs overhead. Missing basis defaults non-binding
  work to Coordinator/sequential and blocks a binding surface need.
- Resolve every relevant capability as `verified`, `unsupported`, or `unknown`, with dated current-runtime observation provenance (`YYYY-MM-DD`). Distinguish `subagent`, `subagent-isolated-worktree`, `persistent-task`, persistent `isolated-worktree`, `persistent-task-owner-steering`, `task-monitoring`, `task-reconciliation`, `peer-team`, `peer-messaging`, `task-retirement`, `task-retirement-reconciliation`, and available child capacity.
- Only capability observed as `verified` in the current runtime authorises its native execution path. Installed text, generated parity, repository tests, fixtures, or another session do not prove general or cross-host support.
- Native persistent-task creation also requires explicit authority applicable to the current request. Task or Epic approval alone is not creation authority.
- If native execution is not verified or authorised, use explicit sequential/coordinator execution only when every binding need, authority, dependency, write-scope, validation, and evidence invariant remains satisfiable. Otherwise block with the exact unmet property.
- Never hard-code a worker count. Effective child concurrency is bounded by requested concurrency, observed available capacity excluding the coordinator, eligible units, dependency readiness, and non-overlapping parallel-safe scopes.
- Report each unit's required properties, requested and effective executor, `sequential` or `parallel` schedule, requested and effective concurrency, capability state/provenance, visibility (`ephemeral`, `visible-retirable`, or `visible-retained`), retention policy, and every selection, fallback, or block reason.

## Execution And Retirement Contract

1. Run `./.project-workflow/cli/workflow delegate plan --id <TARGET> ...` or `delegate status` to derive the canonical graph without launching or retiring work.
2. Validate exactly one target, approved lifecycle/requirements, canonical units, dependency closure, unknown/self/cyclic dependencies, execution needs, scope overlap, and `Parallel Safe` metadata before launch.
3. Preserve one coordinator as the only writer of shared trackers, implementation-row status, acceptance maps, evidence indexes, delegation runtime state, and target lifecycle.
4. Give every worker a bounded packet containing target/unit identity, acceptance criteria, dependencies, repository and write scope, required validation/evidence, forbidden actions, stop conditions, exact source revision, and return format.
5. Workers may not push, merge, release, deploy, contact third parties, create unapproved persistent tasks/worktrees, mutate shared workflow state, or write outside their packet.
6. A dependency is satisfied only after the coordinator inspects returned identity, source/worktree, scope/diff, validation, and evidence and records a verified result. A worker completion assertion alone is insufficient.
7. Launch only eligible units. A failed unit blocks its descendants. Unrelated branches may continue only while shared premises remain valid; do not blanket-stop independent work.
8. Allow in-flight work to return, then reconcile missing, duplicate, stale, orphaned, or mismatched handles before integration or canonical status changes.
9. Treat temporary user-visible subordinate work as `archive-on-verified` on Codex, and as host-neutral retirement elsewhere. Retire only after a terminal coordinator-verified result is durably integrated or has a verified no-integration disposition and durable receipt, with no unresolved child or owner attention.
10. Never retire the coordinator, active, returned-but-unverified, failed, rejected, orphaned, blocked, awaiting-owner, unintegrated, explicitly retained, or owner-promoted work. Keep it visible with the exact retention reason.
11. Retirement is an idempotent host action, not deletion. Emit one stable intent, observe and record the host outcome, retain the handle until success, and leave failed or unknown retirement pending for resume. On Codex, map retirement to reversible task archival only when `task-retirement` and `task-retirement-reconciliation` are verified.
12. Keep machine-local handles, leases, cursors, credentials, and private transcripts under ignored runtime state. Canonical evidence remains reviewable and contains no private runtime data.
13. Move a Task to `Testing` only after all required implementation rows are complete. Epic child completion, Epic closeout, and final completion retain their existing QA, evidence, audit, deferral, retro, and owner-authority gates.
14. Route implementation through Implement and independent QA/code review through QA Review. Delegate's aggregate or retirement report is not independent QA, owner acceptance, integration, release, deployment, adoption, or effectiveness proof.

## Host Boundary

- Codex may use current-session subagents for bounded work and isolated persistent tasks for approved durable/owner-steered work when the corresponding current-runtime capability and authority gates pass; archive successful disposable visible children only after verified reconciliation.
- Claude Code may use subagents, isolated subagents, or teams only when the current runtime verifies the needed surfaces; teams require explicit peer communication. GitHub Copilot and Cursor follow the same property policy using their native surfaces only when observed.
- For every host not exercised in the current run, report the asset as contract-aligned or expected to work, never runtime-validated.

## Required Report

Return the target and exact source, selected graph, per-unit canonical and execution state, dependencies and execution needs, requested/effective executor and schedule, requested/effective concurrency, visibility and retention, capability matrix with provenance, launched/returned/coordinator-verified results, retirement intents and observed outcomes, retained attention reasons, blocked descendants, unrelated continuation decisions, validation/evidence, privacy boundary, cross-host proof boundary, and remaining QA/delivery gates.
