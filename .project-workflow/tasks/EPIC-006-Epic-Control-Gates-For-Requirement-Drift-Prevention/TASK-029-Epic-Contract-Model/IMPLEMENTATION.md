## User Story

As a project owner, I want every new epic to declare its controlling contract before child work starts, so agents cannot substitute plausible but wrong sources of truth or proof owners.

## Parent AC Coverage

- AC2, AC4, AC11, AC12

## Acceptance Criteria

- [x] AC1: Covers parent AC2: new epics get `EPIC-CONTRACT.md`, and decomposition/child execution commands reject missing or placeholder contracts.
- [x] AC2: Covers parent AC4: the contract schema records parent AC proof ownership for every parent AC.
- [x] AC3: Covers parent AC11: README, CLI README, generated host guidance, and `project-epic` skill explain the contract gate.
- [x] AC4: Covers parent AC12: regression tests prove contract creation, contract-required decomposition blocking, and doctor failure for approved epics missing contracts.

## Validation

- AC1: `epic init` writes `EPIC-CONTRACT.md`; `epic ready`, `epic decompose`, `epic approve`, `epic scaffold-child`, and `epic status` validate the contract for new/adopted epics.
- AC2: Contract validation requires non-placeholder proof-owner rows covering all parent AC IDs declared in requirements.
- AC3: README, CLI README, generated host guidance, and `project-epic` skill were updated.
- AC4: `tests/test_doctor.py` includes contract creation, missing/placeholder contract, and approved-epic doctor failure coverage.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add contract template | Generate `EPIC-CONTRACT.md` from `epic init`. | AC1, AC2 | Focused tests. | Done |
| 2 | Add command gates | Require valid contracts before decomposition, child approval/scaffolding, status movement, and Ready/In Progress lifecycle. | AC1 | Focused tests. | Done |
| 3 | Add doctor state check | Fail approved/adopted epics with invalid contracts and warn legacy unapproved epics. | AC1, AC4 | Focused tests and doctor. | Done |
| 4 | Update guidance | Document the contract authority rule. | AC3 | File review and tests. | Done |

## Parent AC Evidence

- AC2: `EPIC-CONTRACT.md` is generated and required before high-risk epic transitions.
- AC4: Contract proof-owner table records parent AC proof owners and must cover every parent AC.
- AC11: README, CLI README, generated host guidance, and `project-epic` skill updated.
- AC12: Contract regression tests added and focused suite passed.

## QA & Code Review

- Verdict: Pass
- Evidence: `pytest tests/test_doctor.py` passed with 57 tests on 2026-07-09. Full suite `pytest` passed with 57 tests on 2026-07-09.
- Findings: No TASK-029 blocking findings in focused regression coverage.

## Retro

- Reusable lessons: Epic contracts should be checked at lifecycle gates; file presence alone is not enough.
- Conventions or agent assets updated: CLI/template mirrors, README, CLI README, project-epic skill, and tests updated.
- Follow-up tasks: TASK-031 should consume proof-owner data when generating child charters and enforcing proof ownership.

## Notes

- Task: TASK-029
- Title: Epic Contract Model
- Created: 2026-07-09
