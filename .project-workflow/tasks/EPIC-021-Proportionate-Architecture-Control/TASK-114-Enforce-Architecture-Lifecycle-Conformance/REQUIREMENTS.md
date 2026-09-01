# Requirements

## Summary

- Task: TASK-114
- Title: Enforce Architecture Lifecycle Conformance
- Parent AC Coverage: AC1, AC2, AC5, AC6, AC7, AC8
- Last updated: 2026-09-01
- Intent contract: full

## Intent

Make current-contract Task and Epic-child lifecycle gates proportionate: cheap established-pattern
work proceeds without material ceremony, while material work cannot become Ready, Review, or
Complete without current repository architecture authority and exact-candidate conformance.

## Intent Spine

- OC1 — Completion capability: Lifecycle transitions enforce the selected architecture contract.
- OC2 — Material capabilities: Classification, authority freshness, plan effect and conformance.
- OC3 — Success journey: Local reaches Ready cheaply; stale material fails Ready; missing conformance fails Review.
- OC4 — Successful-but-wrong result: Helper tests pass but the real CLI transition remains bypassable.
- OC5 — Exclusions: No universal topology or ceremony, no consumer mutation, no external delivery.
- OC6 — Assumptions: Current-contract work contains generated Architecture Impact sections.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Yes, inherited unchanged from parent approval
- Requirements reviewed by owner: Yes, through the approved parent envelope
- Acceptance criteria reviewed by owner: Yes, through the approved parent envelope
- Approved for decomposition: Inherited
- Approved for implementation: Yes
- Approved scope envelope: EPIC-021 unchanged architecture lifecycle capability
- Approved by: John Detlefs
- Approval date: 2026-09-01
- Approval note / source: Originating task `01a05a3b-dea4-7330-a0ca-93f34c5e2cb9`
- Approved artifact identity: Inherited from current EPIC-021 intent audit

## Child Charter

- Coordinator remains the only owner-facing role and shared-state writer.
- Only material work requires source identity and conformance; local work cites an existing spine.
- Repository-selected constraints replace universal style, size, module or folder rules.
- Requirements or QA prose without mechanical lifecycle enforcement is an invalid substitute.

## Goal

Make architecture decisions operationally binding at the existing readiness and review gates.

## Non-Goals

- No host entrypoint generation or real-host canary work; TASK-115 owns those.
- No consumer adoption, release, push, merge or deployment.

## Users & Context

Coordinators planning and reviewing architecture-affecting work in configured repositories.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Parse exactly one `no`, `local`, or `material` classification.
- Require local authority to be a substantive repository architecture spine.
- Bind material readiness to the current spine digest and all plan-effect fields.
- Bind Task and Epic-child Review/Complete to exact-candidate conformance.
- Keep `no` and `local` paths free of material-only digest, ADR and campaign requirements.

## Acceptance Criteria (Verifiable)

- AC1: Real CLI fixtures prove local work reaches Ready without material ceremony.
- AC2: Missing, malformed, duplicate, incomplete, or stale material authority fails closed at readiness.
- AC3: Standalone and Epic-child material Review/Complete reject absent or mismatched conformance.
- AC4: Current authority plus passing conformance reaches the normal next lifecycle state.
- AC5: The dependency/ownership violation and selected Project Workflow module constraints fail mechanically.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Existing architecture spine is the minimum local authority; arbitrary repository files do not qualify.
- ADRs remain optional supplements and are never readiness prerequisites by default.

## Validation Plan

- Run unit adversarial probes, real packaged/local CLI lifecycle fixtures, architecture tests, runtime parity, and full regression gates.
