# Epic Contract

## Summary

- Epic: EPIC-021
- Title: Proportionate Architecture Control
- Last updated: 2026-09-01

## Sources of Truth

- Owner meaning and authority: EPIC-021 `REQUIREMENTS.md`, sourced to originating task
  `01a05a3b-dea4-7330-a0ca-93f34c5e2cb9` and its exact approval response.
- Stable product outcomes: `.project-workflow/CONSTITUTION.md`.
- Repository operating rules: `AGENTS.md` and `.project-workflow/guidance.md`.
- Project Workflow implementation architecture: `docs/architecture.md`.
- Architecture-control product contract: canonical authored modules and semantic host source under
  `src/project_workflow/`, named by the child plans after TASK-113 establishes exact ownership.
- Workflow state and proof: this Epic tracker, child requirements/implementation/evidence, intent
  audit, acceptance audit and coordination state.

## Invalid Substitutes

- A universal architecture style, atomic-design rule, size/module/folder threshold, or ceremony for
  every change.
- A new owner-facing Architect role, second shared-state writer, or architecture truth duplicated
  across host-specific files.
- Requirements or QA prose without current architecture authority identity and exact-candidate
  conformance evidence for material work.
- Unit tests alone when the claim is real-host discovery/invocation.
- Generated Claude files, mocks, package membership or unauthenticated commands as proof of an
  authenticated supported Claude canary.
- Local implementation as proof of push, merge, release, deployment, consumer adoption, owner
  acceptance or commercial validation.

## Invariants

- Coordinator remains the only owner-facing role and shared workflow-state writer.
- Architecture impact is exactly `no`, `local` or `material`; only material work requires the
  architecture decision/conformance gate.
- The repository owns its architecture spine and chooses its measurable constraints.
- Material authority is source-bound and fails closed when missing, placeholder, stale or
  inconsistent with the plan.
- ADRs supplement rather than replace the architecture spine and are used only for substantial
  individual trade-offs when useful.
- One canonical semantic Project Architect source generates both host entrypoints; derived copies
  are never edited as authored truth.
- Host generation parity and each real-host canary remain separate claims.
- No consumer repository or external delivery system is mutated under this Epic.

## Artifact Targets

- Extended `docs/architecture.md` plus a reusable architecture-spine contract/template.
- Architecture-impact, authority identity, plan-effect and conformance records in current-contract
  Task/Epic-child artifacts.
- Readiness, Review and Complete enforcement in the canonical runtime modules and generated helper.
- Project-selected mechanical constraint and dependency/source-ownership test support.
- One canonical Project Architect semantic source plus generated Codex and Claude entrypoints and a
  deterministic parity checker.
- Focused and integrated tests, Project Workflow dogfood evidence, separate host canary receipts,
  QA record, acceptance audit and local-only delivery record.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-113, TASK-114 | Schema/contract review and `no`/`local`/`material` fixture tests. |
| AC2 | TASK-113, TASK-114, TASK-116 | Cheap/local readiness journey with zero new architecture ceremony. |
| AC3 | TASK-113, TASK-115 | Coordinator/Architect contract tests and host entrypoint review. |
| AC4 | TASK-113, TASK-115 | Architecture-spine schema plus canonical semantic-source review. |
| AC5 | TASK-113, TASK-114 | Material child plan fixtures and readiness enforcement. |
| AC6 | TASK-114, TASK-116 | Missing, placeholder, stale, mismatched and current authority tests. |
| AC7 | TASK-114, TASK-116 | Implementation/QA conformance fixtures and lifecycle rejection tests. |
| AC8 | TASK-113, TASK-114, TASK-116 | Repository-selected constraint mechanism and dogfood architecture tests. |
| AC9 | TASK-115, TASK-116 | Deterministic generation, byte/semantic parity and one-copy drift failure. |
| AC10 | TASK-115, TASK-116 | Real Codex discovery and invocation receipt for the current candidate. |
| AC11 | TASK-115, TASK-116 | Authenticated Claude receipt or exact retained blocker with no parity claim. |
| AC12 | TASK-116 | Integrated dogfood receipt covering local, fail-closed and violation cases. |
| AC13 | TASK-116 | Git/delivery boundary evidence and no consumer-repository mutation. |
