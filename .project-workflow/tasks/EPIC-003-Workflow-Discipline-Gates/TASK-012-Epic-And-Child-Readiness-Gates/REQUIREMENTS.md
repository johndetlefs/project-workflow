# Requirements

## Summary

- Task: TASK-012
- Title: Epic And Child Readiness Gates
- Parent AC Coverage: AC3, AC4, AC5, AC6, AC8
- Last updated: 2026-06-17

## Goal

Add explicit readiness gates for epics, standalone tasks, and epic child tasks so implementation and decomposition cannot proceed from incomplete requirements or planning.

## Non-Goals

- Replacing QA/code review or epic closeout evidence gates.
- Eliminating audited force transitions for non-complete recovery.
- Requiring full implementation ACs for bounded discovery work.

## Users & Context

- Agents need a command-level preflight before coding.
- Owners need missing context surfaced as targeted remediation.
- Maintainers need readiness logic reused by commands, status gates, and doctor.

## Requirements (Outcome-Focused)

- `task ready` validates standalone task requirements and implementation plan.
- `epic ready` validates parent epic requirements before decomposition.
- `epic ready-child` validates child requirements, implementation plan, and parent AC coverage before implementation/testing.
- Status transitions enforce readiness for implementation-oriented states while preserving audited exceptions.
- Doctor reports readiness gaps with actionable remediation.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-003 AC3 by blocking epic decomposition when parent requirements are not ready.
- AC2: Covers EPIC-003 AC4 by requiring parent AC context for epic child readiness.
- AC3: Covers EPIC-003 AC5 by adding standalone and child task readiness validation.
- AC4: Covers EPIC-003 AC6 by wiring readiness into status transitions.
- AC5: Covers EPIC-003 AC8 by reporting actionable readiness failures.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Use explicit ready commands plus status and doctor integration.
  - Why: Agents need direct preflight commands, and lifecycle gates must prevent bypasses.

## Validation Plan

- Run readiness command fixtures.
- Run status transition fixtures.
- Run full workflow doctor and package/local helper parity checks.
