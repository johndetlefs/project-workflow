---
name: project-delegate
description: Use when coordinating approved Task implementation rows or Epic child Tasks through a capability-aware dependency graph.
---

# Project Delegate

Coordinate existing execution units for exactly one approved Task or Epic. Delegate executes authority already recorded in requirements and the canonical plan; it never creates scope, approves requirements, invents rows/children, or batches unrelated standalone Tasks.

## Invocation Rules

- Use this skill whenever the user asks to delegate, coordinate, batch, parallelize, monitor, resume, or run multiple planned work items.
- Read `AGENTS.md`, `.project-workflow/guidance.md`, target requirements, and the canonical implementation or decomposition plan first.
- Requirements, clarification, approval, and planning must already be complete. Use an Epic for coordinated standalone Tasks.
- Delegation does not bypass Implement, independent QA/code review, evidence, audit, retro, owner acceptance, or delivery gates.

## Capability Gate

Before choosing an executor, inspect tools callable in this current Codex session and resolve each relevant capability as `verified`, `unsupported`, or `unknown`, with dated observation provenance (`YYYY-MM-DD`):

- bounded current-session subagents and available child slots;
- persistent Codex tasks, isolated worktrees, monitoring/waiting, and resume/reconciliation.

Only `verified` capability observed in this runtime authorises native launch. Installed guidance, repository tests, fixtures, another session, or one available tool do not prove a complete capability set or general Codex support. `unsupported` and `unknown` fail closed for that native path.

Codex may use current-session subagents only when the subagent tools and available capacity are actually observed. Codex may create persistent tasks/worktrees only with explicit owner authority and current-runtime verification of persistent creation, isolation, monitoring, and required reconciliation. Otherwise use safe sequential/coordinator execution when all invariants remain satisfiable, or block with the exact reason.

Never hard-code four workers or any other fixed capacity. Effective child concurrency is the minimum of requested concurrency, observed available child slots excluding the coordinator, currently eligible units, dependency readiness, and collision-free `Parallel Safe` scopes.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`, or the target Epic's `DECOMPOSITION.md` and tracker
- `.project-workflow/TRACKER.md`
- child-local `EVIDENCE.json` when a proof recipe applies
- repo instructions such as `AGENTS.md`

## Workflow

1. Identify exactly one target and optional dependency-closed unit subset. Reject mixed targets and arbitrary Task batches.
2. Run `./.project-workflow/cli/workflow delegate plan --id <TARGET>` or `delegate status`, passing only runtime-observed verified/unsupported capabilities, their provenance, observed child capacity, and explicit persistent-task authority where applicable.
3. Validate approved lifecycle, canonical graph, unknown/self/cyclic dependencies, subset closure, `Write Scope`, `Parallel Safe`, and current shared baseline before launch.
4. Keep one coordinator as the only writer of shared trackers, implementation-row status, acceptance maps, evidence indexes, delegation runtime state, and target lifecycle.
5. Give each executor a bounded packet containing target/unit identity, acceptance criteria, dependencies, repository/write scope, required validation/evidence, forbidden actions, stop conditions, exact source revision, and return format.
6. Workers may not push, merge, release, deploy, contact others, create unapproved persistent tasks/worktrees, mutate shared workflow state, or write outside the packet.
7. Launch only eligible units. Task rows use bounded subagents or sequential/coordinator execution; Epic children may use persistent tasks only after the stronger authority/capability gate. Keep these unit types and executor choices distinct.
8. Treat dependencies as satisfied only after coordinator inspection verifies returned identity, source/worktree, allowed diff, validation, and evidence. A worker completion claim is not proof.
9. A failed unit blocks its descendants. Continue unrelated work only while the shared baseline and premises remain valid; do not blanket fail-fast independent branches. Allow in-flight work to return and verify it before integration.
10. Persist only machine-local handles/leases/cursors under ignored runtime state and never store credentials or private transcripts. Canonical evidence remains reviewable and contains no runtime secrets.
11. Move a Task to `Testing` only when every required implementation row is complete. Route implementation through `project-implement`, then independent review through `project-qa-review`; after authorized completion, run `project-retro`.

## Required Report

Report target/source, graph and dependencies, requested/effective executor per unit, requested/effective concurrency, the tri-state capability matrix and provenance, launches/returns/coordinator verification, failures and blocked descendants, unrelated continuation decisions, validation/evidence, privacy boundaries, and all remaining QA/closeout/delivery gates. Never present Delegate's aggregate report as independent QA, owner acceptance, integration, release, deployment, adoption, or effectiveness proof.
