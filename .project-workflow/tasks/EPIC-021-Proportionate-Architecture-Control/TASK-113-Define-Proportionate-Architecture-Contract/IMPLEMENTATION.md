## User Story

As a repository owner, I want proportionate architecture impact and authority recorded before
material work, so that structural decisions are explicit without burdening ordinary changes.

## Architecture Impact

- Classification: material
- Reason: Adds a new architecture-control product domain, artifact contract and generated task fields.
- Architecture authority: docs/architecture.md
- Authority identity: sha256:f8327a14f96b2765b7e99eb744d218d0e0076cbec66ea3632761cb0a9cbe7737
- Architect invocation: project-architect:codex:01a05b1c-f694-7fc2-8346-0316d5564e83
- Architect decision identity: sha256:8d96f86e92b06159db520568543202ccf5b5b98b236ef027922ebe877da6a395
- Affected boundaries: contracts, repository task artifacts, lifecycle consumers, host adapters
- Architecture decision: TASK-113 establishes the source-bound contract before production gating.
- Measurable constraints: architecture module follows manifest dependency direction and remains covered by architecture tests.
- Conformance plan: extend the spine first, then add the canonical module and focused tests.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC5, AC8

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

## Acceptance Criteria

- [x] AC1: Define the three impact values and evidence required for each.
- [x] AC2: Define subordinate Project Architect and architecture-spine/ADR boundaries.
- [x] AC3: Add path-and-digest authority validation plus plan/conformance records.
- [x] AC4: Extend Project Workflow's own spine and mechanical architecture checks.

## Validation

- AC1-AC4: 64 focused architecture/lifecycle/host/work-item/Epic tests passed; generated runtime parity passed;
  document review confirms all six required spine concerns and the subordinate Architect boundary.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/architecture-control; no PR | 64 focused tests and generated runtime parity pass | Local working tree only; not pushed, merged, released or adopted | tests/test_architecture_control.py; tests/test_architecture.py; docs/architecture.md |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Extend the architecture spine | Record architecture-control responsibility, source ownership, state boundaries and extension rules. | AC2, AC4 | Inspect `docs/architecture.md`. | Done | | docs/architecture.md | No | bounded-return |
| 2 | Add architecture contract primitives | Implement classification, authority identity and spine/conformance validation in one canonical module. | AC1, AC3 | Run focused unit tests. | Done | 1 | src/project_workflow/architecture.py; scripts/runtime-modules.txt | No | bounded-return |
| 3 | Add reusable artifact fields | Extend current task/child templates with proportionate architecture impact and conformance sections. | AC1, AC3 | Scaffold fixtures and inspect fields. | Done | 2 | src/project_workflow/lifecycle.py | No | bounded-return |
| 4 | Prove the contract boundary | Add focused tests for local, material-current, material-stale and spine completeness. | AC1, AC2, AC3, AC4 | Run focused pytest and runtime parity. | Done | 2, 3 | tests/test_architecture_control.py; tests/test_architecture.py | No | bounded-return |

## Parent AC Evidence

- AC1: `ArchitectureImpact` and readiness tests cover exactly no/local/material.
- AC2: the local fixture passes with an existing spine and no new ADR, Architect invocation or campaign.
- AC3: `docs/architecture.md` and the child charter keep Architect subordinate to Coordinator.
- AC4: all six required spine sections are machine-validated.
- AC5: material fields bind effect, boundaries, path/digest authority, constraints and conformance.
- AC8: Project Workflow selects its own import/parity/module constraints; no universal values are encoded.

## Validation Impact

- Baseline proof: integrated-qa:01a05b11-1112-7103-b9f5-f8e763952092
- Change summary: Resolved duplicate-section and source-bound Architect decision findings; reran affected contract and full proof.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: Coordinator
- Change identity: sha256:ac3cc30f9a55a1d11c71636be4837f8f2a1df4490c9098959a6099e8a2444974

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Changes Requested
- Could every AC pass while the approved user job remains undone: Yes
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Duplicate-line, duplicate-section, arbitrary-authority, stale-authority and source-bound decision tests pass within 20 affected and 592 full-suite tests.
- Second QA commissioned: No
- Intent audit state: current
- Outcome journey evidence: Direct adversarial probes plus focused contract and repository-constraint tests bound to the exact candidate.
- Reviewer independence: An ephemeral read-only Codex reviewer inspected the candidate and made no mutations.
- Evidence: Parent `QA-INTEGRATED.md`; exact-candidate `VERIFICATION-RECEIPT.md`; generated-runtime check; mypy; package journeys.
- Findings: Original Changes Requested is preserved; all contract-scope findings are resolved by affected validation.

## Architecture Conformance

- Authority identity: sha256:f8327a14f96b2765b7e99eb744d218d0e0076cbec66ea3632761cb0a9cbe7737
- Candidate: git:3e34317a847f24ff64581c78d246adff93e29e27
- Mechanical checks: candidate=git:3e34317a847f24ff64581c78d246adff93e29e27; receipt=.project-workflow/tasks/EPIC-021-Proportionate-Architecture-Control/TASK-116-Dogfood-Architecture-Control-And-Closeout/VERIFICATION-RECEIPT.md
- Deviations: None.
- Verdict: Pass

## Retro

- Reusable lessons: Local impact can remain cheap while material authority uses a digest.
- Conventions or agent assets updated: Project architecture spine and task/child templates.
- Follow-up tasks: TASK-114 enforces lifecycle conformance; TASK-115 owns generated host entrypoints.

## Notes

- Task: TASK-113
- Title: Define Proportionate Architecture Contract
- Created: 2026-09-01
