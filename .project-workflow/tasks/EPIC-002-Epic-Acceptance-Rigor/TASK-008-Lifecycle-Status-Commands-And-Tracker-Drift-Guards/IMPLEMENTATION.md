## User Story

As a project-workflow maintainer, I want supported epic child status commands, so agents do not manually edit epic trackers and cannot complete child rows without QA and parent AC evidence.

## Goal

- Satisfy EPIC-002 AC11 and AC15 with `epic status` and documented tracker ownership/drift guard behavior.

## Parent AC Coverage

- EPIC-002 AC11: CLI status handling covers Testing, Review, and Complete transitions without manual tracker edits.
- EPIC-002 AC15: Root tracker versus epic tracker rules are explicit.

## Acceptance Criteria

- [x] AC1: Covers EPIC-002 AC11 by adding `epic status --to Testing|Review|Complete` with lifecycle validation.
- [x] AC2: Covers EPIC-002 AC15 by documenting `epic status` and enforcing epic-child updates in epic trackers instead of the global tracker.

## Approach

- Add `EPIC_STATUS_TRANSITIONS` and `epic status` command.
- Reuse existing task status force semantics for audited non-Complete exceptions.
- Require QA/code-review evidence and parent AC evidence before Complete.
- Update README and generated epic guidance.

## Phases

### Phase 1

- Add command behavior to package CLI and generated local workflow helper.
- Add fixture tests for status transitions and Complete blockers.

### Phase 2

- Update generated docs/prompts and mirror installed prompt.
- Run tests and doctor checks.

## Tasks

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Epic Status Command | Add tracker-safe `epic status` transitions for epic child rows. | AC1 / EPIC-002 AC11: Testing, Review, Complete transitions are CLI-supported. | Run epic status fixture test. | Done |
| 2 | Complete Evidence Guard | Block Complete unless QA and parent AC evidence are present. | AC1 / EPIC-002 AC11: Complete cannot bypass evidence gates. | Run missing-parent-evidence fixture. | Done |
| 3 | Tracker Ownership Docs | Update docs/guidance for epic child lifecycle ownership. | AC2 / EPIC-002 AC15: README and generated epic prompt/skill mention `epic status`. | Inspect docs and prompt mirror. | Done |

## Validation

- AC1 / EPIC-002 AC11: `tests/test_doctor.py::test_epic_status_requires_parent_ac_evidence_before_complete`.
- AC2 / EPIC-002 AC15: generated README, skill, prompt, and mirror updates plus doctor checks.

## Parent AC Evidence

- EPIC-002 AC11: Implemented `epic status` in package CLI, generated template, and installed local helper. Evidence: status fixture passed.
- EPIC-002 AC15: Updated README and generated epic guidance to use epic tracker-owned status transitions. Evidence: prompt mirror comparison returned 0 and doctor passed with only historical APP warnings.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: status transition graph, Complete gate, parent AC evidence enforcement, parser entry, README/guidance updates, package/local helper parity.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 24 tests; doctor checks passed with only pre-existing APP warnings.
- AC evidence: AC1 / EPIC-002 AC11 covered by epic status fixture; AC2 / EPIC-002 AC15 covered by docs/guidance and epic tracker-owned command behavior.
- Verdict: Pass.
- Findings: None.

## Retro

- Reusable lessons: Epic child status is distinct from global task status; supporting it directly removes manual tracker drift.
- Conventions or agent assets updated: README, project-epic skill, Epic prompt, and installed prompt mirror.
- Follow-up tasks: TASK-009 should run final fixture/doc parity sweep.
- Missed in-scope work: None.

## Notes

- Task: TASK-008
- Title: Lifecycle Status Commands And Tracker Drift Guards
- Created: 2026-06-17
