## User Story

As a reviewer, I want child tasks to carry inherited epic constraints and proof ownership, so parent acceptance evidence cannot be claimed by the wrong child.

## Parent AC Coverage

- AC3, AC4, AC12, AC14

## Child Charter

### Inherited Invariants

- Parent AC IDs remain stable.
- Approved child rows must match ID, title, and parent AC coverage in `DECOMPOSITION.md`.
- Missing or placeholder contract sections are not valid authority for new/adopted epics.
- Legacy epics without approval envelopes warn until adoption rather than blocking unrelated current work.

### Invalid Substitutes

- Tracker rows without matching `DECOMPOSITION.md` authority.
- Prose summaries that are not backed by child implementation evidence.
- Legacy warnings from unadopted old epics as proof that new/adopted epics satisfy gates.
- Generic owner approval prompts when the work remains inside the approved authority envelope.

### Artifact Targets

- `.project-workflow/cli/workflow.py`
- `src/project_workflow/cli.py`
- `src/project_workflow/templates/workflow.py`
- `tests/test_doctor.py`
- `README.md`
- `.project-workflow/cli/README.md`
- `src/project_workflow/codex/skills/project-epic/SKILL.md`

### Parent AC Proof Ownership

- AC3: owner `TASK-031`; required evidence: Child charter generation and inheritance tests.
- AC4: owner `TASK-029, TASK-031`; required evidence: Contract proof-owner schema plus child proof-ownership gates.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.
- AC14: owner `TASK-031, TASK-033, TASK-037`; required evidence: Decomposition plan authority, amendment provenance, and child inheritance gates.

## Acceptance Criteria

- [x] AC1: Covers parent AC3: scaffolded child docs contain inherited `Child Charter` sections from the epic contract.
- [x] AC2: Covers parent AC4: epic audit rejects parent AC evidence from a child not assigned as proof owner for that parent AC.
- [x] AC3: Covers parent AC12: tests cover charter inheritance and proof-owner rejection.
- [x] AC4: Covers parent AC14: in-plan child rows inherit authority context without separate per-row owner approval.

## Validation

- AC1: `_format_child_charter_from_contract` copies inherited invariants, invalid substitutes, artifact targets, and proof-owner rows into child docs during `epic scaffold-child`.
- AC2: `_epic_audit_rows` builds a proof-owner map from valid contracts and rejects evidence from unassigned child rows.
- AC3: `tests/test_doctor.py` covers charter injection and proof-owner rejection.
- AC4: Charter inheritance runs after decomposition-plan authority and parent approval checks; no extra owner approval is required for matching planned rows.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Inject child charter | Add contract-derived child charter to scaffolded child requirements and implementation docs. | AC1, AC4 | Focused tests. | Done |
| 2 | Enforce proof ownership | Reject parent AC evidence from unassigned proof-owner children during epic audit. | AC2 | Focused tests. | Done |
| 3 | Update guidance | Document child charter behavior in README and project-epic skill. | AC3 | File review. | Done |

## Parent AC Evidence

- AC3: Scaffolded child docs now include inherited `Child Charter` sections.
- AC4: Epic audit rejects evidence from child rows not assigned as proof owners.
- AC12: Focused tests cover charter inheritance and proof-owner rejection.
- AC14: Matching planned child rows inherit contract context without separate owner approval.

## QA & Code Review

- Verdict: Pass
- Evidence: `pytest tests/test_doctor.py` passed with 58 tests on 2026-07-09. Full suite `pytest` passed with 58 tests on 2026-07-09.
- Findings: No TASK-031 blocking findings in focused regression coverage.

## Retro

- Reusable lessons: Proof-owner enforcement should only run against valid contracts; placeholder legacy contracts remain a separate adoption concern.
- Conventions or agent assets updated: CLI/template mirrors, README, project-epic skill, and tests updated.
- Follow-up tasks: TASK-030 should add recipe-specific evidence payloads consumed by these ownership gates.

## Notes

- Task: TASK-031
- Title: Child Charter Inheritance And Proof Ownership
- Created: 2026-07-09
