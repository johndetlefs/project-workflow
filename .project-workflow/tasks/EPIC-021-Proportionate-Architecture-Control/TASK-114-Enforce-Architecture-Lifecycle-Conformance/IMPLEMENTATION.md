## User Story

As a Coordinator, I want architecture decisions enforced by existing lifecycle gates, so that
material structural work cannot proceed on missing, stale, or unconformed authority.

## Parent AC Coverage

- AC1, AC2, AC5, AC6, AC7, AC8

## Architecture Impact

- Classification: material
- Reason: This task changes readiness, Review and Complete policy for Task and Epic-child lifecycle transitions.
- Architecture authority: docs/architecture.md
- Authority identity: sha256:f8327a14f96b2765b7e99eb744d218d0e0076cbec66ea3632761cb0a9cbe7737
- Architect invocation: project-architect:codex:01a05b1c-f694-7fc2-8346-0316d5564e83
- Architect decision identity: sha256:bb9fc09defa21edc2a2abb7b34081524c50b4f183df2a4c438ed3f1722ab3861
- Affected boundaries: architecture contract parsing; lifecycle readiness; standalone and Epic-child Review/Complete.
- Architecture decision: Compose one architecture module into existing lifecycle owners; keep Coordinator as sole shared-state writer.
- Measurable constraints: Exact-one classification, complete local spine, digest-bound material readiness and conformance-bound Review.
- Conformance plan: Run adversarial unit probes and real CLI transition journeys against the generated runtime.

## Acceptance Criteria

- [x] AC1: Local established-pattern work reaches Ready with no digest, ADR, or material campaign.
- [x] AC2: Duplicate/malformed/incomplete/stale material authority fails closed.
- [x] AC3: Standalone and Epic-child material Review/Complete require conformance.
- [x] AC4: Current authority and passing exact-candidate conformance proceed normally.
- [x] AC5: Repository-selected dependency and module constraints fail mechanically.

## Validation

- AC1: `test_local_established_pattern_reaches_ready_without_material_ceremony` passes through the real CLI.
- AC2: Architecture contract adversarial tests and stale real-CLI journey pass.
- AC3-AC4: Standalone Review journey and Epic-child gate call-site tests pass; generated runtime is current.
- AC5: Deliberate dependency-direction and manifest-to-spine constraint tests pass.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/architecture-control; no PR | 64 focused and 587 full-suite tests pass | Local working tree only | tests/test_architecture_lifecycle.py; tests/test_architecture_control.py; tests/test_architecture.py |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Enforce readiness | Bind no/local/material plans to proportionate authority. | AC1, AC2 | Run real CLI fixtures. | Done | | architecture.py; lifecycle.py | No | bounded-return |
| 2 | Enforce conformance | Block standalone and child Review/Complete without material conformance. | AC3, AC4 | Run lifecycle fixtures. | Done | 1 | coordination.py | No | bounded-return |
| 3 | Enforce selected constraints | Catch dependency and module-authority violations. | AC5 | Run architecture tests. | Done | 1 | tests/test_architecture.py | No | bounded-return |

## Parent AC Evidence

- AC1: Exactly-one classification and no/local/material semantics are mechanically tested.
- AC2: The local real-CLI journey reaches Ready without material fields or ADR.
- AC5: Material architecture effect, boundaries, decision, constraints and conformance are plan-bound.
- AC6: The actual readiness transition requires current material authority, as proven by adversarial lifecycle tests.
- AC7: Material Review requires matching authority, exact candidate, mechanical checks, resolved deviations and Pass.
- AC8: Project Workflow's own dependency direction, module table/budget and generated runtime checks are repository-specific.

## Validation Impact

- Baseline proof: integrated-qa:01a05b11-1112-7103-b9f5-f8e763952092
- Change summary: Made material readiness non-bypassable and conformance candidate-bound with Complete recheck; reran affected lifecycle and full proof.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: Coordinator
- Change identity: sha256:86f5035fd6fcb575a8fec095c8cade1271491913a64e34e301f6f64db601039a

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Changes Requested
- Could every AC pass while the approved user job remains undone: Yes
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Force-bypass, exact candidate/receipt and Review-then-mutate Complete regressions pass within 20 affected and 592 full-suite tests.
- Second QA commissioned: No
- Intent audit state: current
- Outcome journey evidence: Real CLI fixtures and mechanical violations are bound to `git:3e34317a847f24ff64581c78d246adff93e29e27`.
- Reviewer independence: Ephemeral read-only Codex reviewer `01a05b11-1112-7103-b9f5-f8e763952092` made no mutations.
- Evidence: Parent `QA-INTEGRATED.md`; exact-candidate `VERIFICATION-RECEIPT.md`.
- Findings: Original Changes Requested is preserved; all lifecycle findings are resolved by affected validation.

## Architecture Conformance

- Authority identity: sha256:f8327a14f96b2765b7e99eb744d218d0e0076cbec66ea3632761cb0a9cbe7737
- Candidate: git:3e34317a847f24ff64581c78d246adff93e29e27
- Mechanical checks: candidate=git:3e34317a847f24ff64581c78d246adff93e29e27; receipt=.project-workflow/tasks/EPIC-021-Proportionate-Architecture-Control/TASK-116-Dogfood-Architecture-Control-And-Closeout/VERIFICATION-RECEIPT.md
- Deviations: None.
- Verdict: Pass

## Retro

- Reusable lessons: Validate cardinality and authority semantics, not only happy-path field values.
- Conventions or agent assets updated: Generated task templates and lifecycle gates.
- Follow-up tasks: None inside the approved envelope.

## Notes

- Task: TASK-114
- Title: Enforce Architecture Lifecycle Conformance
- Created: 2026-09-01
