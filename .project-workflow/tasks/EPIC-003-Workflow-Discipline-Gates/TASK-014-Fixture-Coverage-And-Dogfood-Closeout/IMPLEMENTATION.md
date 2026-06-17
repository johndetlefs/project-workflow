## User Story

As a project-workflow maintainer, I want EPIC-003 validated by fixtures, parity checks, doctor checks, and an acceptance audit, so the new discipline gates are proven before closeout.

## Parent AC Coverage

- EPIC-003 AC8: Doctor/validation gives actionable discipline-gate remediation.
- EPIC-003 AC9: Generated docs and agent assets explain the intended lifecycle.
- EPIC-003 AC10: Automated tests cover insufficient intake, readiness, discovery, ID allocation, and compatibility.
- EPIC-003 AC11: Generated agent guidance defines the owner-directed, agent-operated role split.
- EPIC-003 AC12: User-facing docs explain conversational intake.
- EPIC-003 AC13: Gate failures distinguish repo-gatherable facts, assumptions, and owner-required decisions.

## Acceptance Criteria

- [x] AC1: Covers EPIC-003 AC8 with readiness command, status, and doctor fixtures.
- [x] AC2: Covers EPIC-003 AC9 with generated guidance assertions and prompt mirror parity.
- [x] AC3: Covers EPIC-003 AC10 with 30 automated tests including new discipline-gate cases.
- [x] AC4: Covers EPIC-003 AC11 with generated agent asset assertions.
- [x] AC5: Covers EPIC-003 AC12 with README and prompt guidance.
- [x] AC6: Covers EPIC-003 AC13 with remediation category assertions.

## Validation

- AC1: Doctor and readiness tests cover actionable failures.
- AC2: Generated asset tests and parity checks cover docs/guidance.
- AC3: `tests/test_doctor.py` has 30 passing tests.
- AC4: Generated Codex/Cursor assets assert role split and readiness commands.
- AC5: README and prompts state conversational intake.
- AC6: Readiness failure tests assert owner input required and agent action required.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Fixture Coverage | Add targeted tests for ID allocation, readiness, decomposition, child gates, and discovery. | AC1, AC3, AC6: Passing and failing gate paths covered. | Run full test suite. | Done |
| 2 | Generated Asset Coverage | Assert generated agent assets include role split, readiness commands, and conversational owner guidance. | AC2, AC4, AC5: Generated guidance coverage exists. | Run generated asset fixture. | Done |
| 3 | Dogfood Closeout | Use EPIC-003 acceptance audit and closeout gates. | AC1-AC6: Epic audit passes. | Run `epic audit` and `epic closeout`. | Done |

## Parent AC Evidence

- EPIC-003 AC8: Readiness failures are surfaced by commands/status/doctor with actionable remediation.
- EPIC-003 AC9: README, prompts, skills, and Cursor rules explain lifecycle and readiness gates.
- EPIC-003 AC10: Full `tests/test_doctor.py` suite passes with 30 tests covering the new gates.
- EPIC-003 AC11: Generated assets assert owner-directed, agent-operated language.
- EPIC-003 AC12: Owner-facing docs describe conversational intake instead of manual template completion.
- EPIC-003 AC13: Readiness failure tests assert owner input required and agent action required categories.
- EPIC-003 AC9 / AC12 / AC13: README, generated Codex guidance, local CLI README, and CLI bootstrap errors now make the canonical UVX install/update command explicit for agents refreshing project-workflow in another repository.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: test coverage, generated asset assertions, source/helper parity, epic audit readiness.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 30 tests; final doctor/parity/audit checks are refreshed during epic closeout. The suite includes regression coverage that generated Codex guidance and missing-tracker CLI failures surface the canonical UVX init command.
- Findings: None.
- Verdict: Pass.

## Retro

- Reusable lessons: A workflow-gate epic should prove the gate with both failing and passing fixtures.
- Conventions or agent assets updated: Tests, README, prompts, skills, Cursor rules.
- Follow-up tasks: None.
- Missed in-scope work: None.
