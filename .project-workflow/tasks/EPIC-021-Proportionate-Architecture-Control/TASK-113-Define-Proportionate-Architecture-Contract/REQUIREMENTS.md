# Requirements

## Summary

- Task: TASK-113
- Title: Define Proportionate Architecture Contract
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC5, AC8
- Last updated: 2026-09-01
- Intent contract: full

## Intent

Define the repository-owned contract that distinguishes architecture-neutral, established-pattern,
and materially architecture-affecting work, and establishes the subordinate Project Architect and
architecture-spine boundaries before production enforcement is added.

## Intent Spine

- OC1 — Completion capability: Current-contract work has a precise proportionate classification
  and material work has source-bound repository architecture authority.
- OC2 — Material capabilities: Three-level classification, Project Architect/Coordinator contract,
  spine schema, optional ADR boundary and repository-selected measurable constraints.
- OC3 — Success journey: A planner can classify a local change by an established pattern, while a
  material plan names affected boundaries and the current architecture authority.
- OC4 — Successful-but-wrong result: The contract exists but imposes universal structure, creates a
  second owner-facing role, or cannot distinguish a stale authority from a current one.
- OC5 — Exclusions: Lifecycle enforcement, host generation, real-host canaries and final dogfood
  remain in TASK-114 through TASK-116.
- OC6 — Assumptions: `docs/architecture.md` is the current Project Workflow spine and a SHA-256
  identity is sufficient to bind a plan to its exact authority.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
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

- Coordinator remains the only owner-facing role and shared workflow-state writer.
- Architecture impact is exactly `no`, `local` or `material`; only material work requires the architecture decision/conformance gate.
- The repository owns its architecture spine and chooses its measurable constraints.
- Material authority is source-bound and fails closed when missing, placeholder, stale or inconsistent with the plan.
- ADRs supplement rather than replace the architecture spine and are used only for substantial individual trade-offs when useful.
- One canonical semantic Project Architect source generates both host entrypoints; derived copies are never edited as authored truth.
- Host generation parity and each real-host canary remain separate claims.
- No consumer repository or external delivery system is mutated under this Epic.

### Invalid Substitutes

- A universal architecture style, atomic-design rule, size/module/folder threshold, or ceremony for every change.
- A new owner-facing Architect role, second shared-state writer, or architecture truth duplicated across host-specific files.
- Requirements or QA prose without current architecture authority identity and exact-candidate conformance evidence for material work.
- Unit tests alone when the claim is real-host discovery/invocation.
- Generated Claude files, mocks, package membership or unauthenticated commands as proof of an authenticated supported Claude canary.
- Local implementation as proof of push, merge, release, deployment, consumer adoption, owner acceptance or commercial validation.

### Artifact Targets

- Extended `docs/architecture.md` plus a reusable architecture-spine contract/template.
- Architecture-impact, authority identity, plan-effect and conformance records in current-contract Task/Epic-child artifacts.
- Readiness, Review and Complete enforcement in the canonical runtime modules and generated helper.
- Project-selected mechanical constraint and dependency/source-ownership test support.
- One canonical Project Architect semantic source plus generated Codex and Claude entrypoints and a deterministic parity checker.
- Focused and integrated tests, Project Workflow dogfood evidence, separate host canary receipts, QA record, acceptance audit and local-only delivery record.

### Parent AC Proof Ownership

- AC1: owner `TASK-113, TASK-114`; required evidence: Schema/contract review and `no`/`local`/`material` fixture tests.
- AC2: owner `TASK-113, TASK-114, TASK-116`; required evidence: Cheap/local readiness journey with zero new architecture ceremony.
- AC3: owner `TASK-113, TASK-115`; required evidence: Coordinator/Architect contract tests and host entrypoint review.
- AC4: owner `TASK-113, TASK-115`; required evidence: Architecture-spine schema plus canonical semantic-source review.
- AC5: owner `TASK-113, TASK-114`; required evidence: Material child plan fixtures and readiness enforcement.
- AC8: owner `TASK-113, TASK-114, TASK-116`; required evidence: Repository-selected constraint mechanism and dogfood architecture tests.

## Goal

Make architecture decisions explicit and inspectable without adding ceremony to established-pattern
work or prescribing one architecture across repositories.

## Non-Goals

- Enforce readiness, Review or Complete gates.
- Generate host entrypoints or claim host support.
- Add universal file, module, layer or folder constraints.

## Users & Context

Project owners and Coordinator-led agents planning work whose structural impact ranges from none to
material across repositories with different architectures.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Define `no`, `local` and `material` semantics plus minimum evidence for each.
- Define Project Architect as a Coordinator-invoked, non-owner-facing, non-writer capability.
- Define the required architecture-spine concerns and the optional ADR boundary.
- Define exact authority identity and repository-selected constraint/conformance fields.

## Acceptance Criteria (Verifiable)

- AC1: The contract defines exactly `no`, `local` and `material`, and local work can cite an
  established pattern without new architecture artifacts.
- AC2: Project Architect is explicitly subordinate to Coordinator and cannot own shared workflow
  state or owner dialogue.
- AC3: The spine requires responsibilities, dependency direction, source ownership, shared-state
  boundaries, extension points and measurable constraints without universal topology.
- AC4: Material authority is path-and-digest bound, plans identify architectural effect and
  conformance proof, and ADRs remain optional for substantial individual trade-offs.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Add one `architecture.py` product module because classification, authority and conformance are a
  distinct reason to change.
- Put repository-specific architecture in its own spine; Project Workflow supplies fields and
  gates, not the structural answers.
- Record this child as material with a bootstrap decision against current `docs/architecture.md`.

## Validation Plan

- Unit-test classification values, current/stale authority identity and spine-section validation.
- Review `docs/architecture.md`, generated task templates and the Project Architect role boundary.
- Run focused architecture tests and generated runtime parity after the canonical module is added.
