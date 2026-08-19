---
name: project.delegate
description: Coordinate one approved Task or Epic through its canonical dependency graph.
argument-hint: targetId=TASK-063 units="1,2" requestedConcurrency=2
agent: agent
---
<!-- project-workflow:generated -->

Use this prompt to coordinate existing approved execution units for exactly one Task or Epic.

Read `/.project-workflow/guidance.md`, the target requirements, and its canonical implementation or decomposition plan before changing workflow state. Delegate executes approved authority; it does not create scope, approve requirements, invent Task rows or Epic children, or batch unrelated standalone Tasks.

Inputs:

- Target: `${input:targetId:TASK-000-or-EPIC-000}`
- Optional dependency-closed unit subset: `${input:units:all eligible canonical units}`
- Requested concurrency: `${input:requestedConcurrency:1}`
- Explicit persistent-task authority, when applicable: `${input:persistentTaskAuthority:not authorized}`

## Capability Contract

- Resolve every relevant capability as `verified`, `unsupported`, or `unknown`, with dated current-runtime observation provenance (`YYYY-MM-DD`). Relevant capabilities include subagents, persistent tasks, isolated worktrees, monitoring, resume/reconciliation, and available child capacity.
- Only a capability observed as `verified` in the current runtime authorises its native execution path. `unsupported` and `unknown` never mean supported.
- Do not infer general Codex or cross-host support from installed text, generated parity, repository tests, fixtures, or another session.
- If native execution is not verified, use explicit sequential/coordinator execution only when every authority, dependency, write-scope, validation, and evidence invariant remains satisfiable. Otherwise block with the exact reason.
- Never hard-code a worker count. Effective child concurrency is bounded by requested concurrency, currently observed available child capacity excluding the coordinator, eligible units, dependency readiness, and non-overlapping write scopes.
- Report requested and effective executor, requested and effective concurrency, capability state/provenance, and every downgrade or block reason.

## Execution Contract

1. Run `./.project-workflow/cli/workflow delegate plan --id <TARGET> ...` or `delegate status` to derive the canonical graph. Treat Task implementation rows and Epic child Tasks as distinct execution-unit types.
2. Validate exactly one target, approved lifecycle/requirements, canonical units, dependency closure, unknown/self/cyclic dependencies, write-scope overlap, and `Parallel Safe` metadata before launch.
3. Preserve one coordinator as the only writer of shared trackers, implementation-row status, acceptance maps, evidence indexes, delegation runtime state, and target lifecycle.
4. Give every worker a bounded packet containing target/unit identity, acceptance criteria, dependencies, repository and write scope, required validation, required evidence, forbidden actions, stop conditions, exact source revision, and return format.
5. Workers may not push, merge, release, deploy, contact third parties, create unapproved persistent tasks/worktrees, mutate shared workflow state, or write outside their packet.
6. A dependency is satisfied only after the coordinator inspects the returned scope/diff, validation, and evidence and records a verified result. A worker completion assertion alone is insufficient.
7. Launch only eligible units. A failed unit blocks its descendants. Unrelated branches may continue only while the shared baseline and premises remain valid; do not blanket-stop independent in-flight or future work.
8. Allow in-flight work to return, then verify scope, identity, source/worktree, validation, and evidence before integration or canonical status changes. Treat missing, duplicate, stale, orphaned, or mismatched handles as blocked until reconciled.
9. Keep machine-local handles, leases, cursors, credentials, and private transcripts under ignored runtime state. Canonical repository evidence must remain reviewable and contain no private runtime data.
10. Move a Task to `Testing` only after all required implementation rows are complete. Epic child completion, Epic closeout, and final completion retain their existing QA, evidence, audit, deferral, retro, and owner-authority gates.
11. Route implementation through Implement and independent QA/code review through QA Review. Delegate's aggregate report is not independent QA, owner acceptance, integration, release, deployment, adoption, or effectiveness proof.

## Required Report

Return the target and exact source, selected graph, per-unit canonical and execution state, dependencies, requested/effective executor, requested/effective concurrency, capability matrix with provenance, launched/returned/coordinator-verified results, blocked descendants, unrelated continuation decisions, validation/evidence, privacy boundary, and remaining QA/delivery gates.
