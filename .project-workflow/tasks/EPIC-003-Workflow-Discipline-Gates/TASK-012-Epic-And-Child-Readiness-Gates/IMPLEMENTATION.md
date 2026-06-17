## User Story

As an agent operating project-workflow, I want explicit readiness gates before decomposition and implementation, so I cannot run ahead with incomplete requirements or planning.

## Parent AC Coverage

- EPIC-003 AC3: Epic decomposition requires sufficient parent requirements.
- EPIC-003 AC4: Epic child scaffolds inherit parent context needed for decisions.
- EPIC-003 AC5: Implementation readiness validation exists for standalone and epic child tasks.
- EPIC-003 AC6: Status transitions enforce readiness or explicit exceptions.
- EPIC-003 AC8: Doctor/validation gives actionable discipline-gate remediation.

## Acceptance Criteria

- [x] AC1: Covers EPIC-003 AC3 with `epic ready` and a decomposition readiness gate.
- [x] AC2: Covers EPIC-003 AC4 with `epic ready-child` parent AC coverage validation.
- [x] AC3: Covers EPIC-003 AC5 with reusable task readiness checks and `task ready`.
- [x] AC4: Covers EPIC-003 AC6 by blocking normal implementation/testing/review transitions when readiness is missing.
- [x] AC5: Covers EPIC-003 AC8 with owner-input and agent-action remediation messages.

## Validation

- AC1: `test_epic_ready_blocks_vague_epic_and_decomposition`.
- AC2: `test_epic_ready_child_blocks_shallow_child_status`.
- AC3: `test_task_ready_blocks_placeholders_and_allows_ready_docs`.
- AC4: status fixtures pass only after ready docs are written.
- AC5: readiness failures include owner input required and agent action required categories.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Readiness Helpers | Add reusable readiness checks for requirements, implementation plans, parent ACs, and discovery. | AC1, AC2, AC3, AC5: Gates produce actionable failures. | Run readiness tests. | Done |
| 2 | Ready Commands | Add `task ready`, `epic ready`, and `epic ready-child`. | AC1, AC2, AC3: Commands pass/fail appropriately. | Run command fixtures. | Done |
| 3 | Status Integration | Block implementation-oriented transitions when readiness is missing. | AC4: Status gates enforce readiness without breaking audited force recovery. | Run lifecycle tests. | Done |
| 4 | Doctor Integration | Report readiness warnings through doctor and strict mode. | AC5: Doctor reports actionable readiness gaps. | Run doctor tests. | Done |

## Parent AC Evidence

- EPIC-003 AC3: `epic decompose` now runs epic readiness and fails on vague parent requirements.
- EPIC-003 AC4: `epic ready-child` validates parent AC coverage in child implementation docs.
- EPIC-003 AC5: `task ready` and `epic ready-child` validate task-specific requirements and implementation plans.
- EPIC-003 AC6: Task and epic child status transitions check readiness before implementation/testing/review/complete paths, with existing audited force behavior for non-complete recovery.
- EPIC-003 AC8: Gate failures list owner-input and agent-action remediation steps.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: readiness helpers, command parser, task/epic status gates, doctor integration, discovery exception path.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 30 tests.
- Findings: None.
- Verdict: Pass.

## Retro

- Reusable lessons: Readiness must be a reusable validator, not only status-command logic.
- Conventions or agent assets updated: Prompt and skill guidance now names readiness commands.
- Follow-up tasks: None.
- Missed in-scope work: None.
