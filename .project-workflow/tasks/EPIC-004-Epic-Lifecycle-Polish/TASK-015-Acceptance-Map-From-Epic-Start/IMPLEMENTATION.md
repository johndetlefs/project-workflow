## User Story

As an agent operating an epic, I want an acceptance map from the start, so that parent AC coverage remains visible before final closeout.

## Parent AC Coverage

- EPIC-004 AC1: New epics start with an `ACCEPTANCE-MAP.md` or equivalent maintained acceptance-map artifact that lists parent AC IDs, summaries, child coverage, evidence state, deferral state, and current status; generated templates/docs/tests prove the artifact exists from epic start.

## Acceptance Criteria

- [x] AC1: Covers EPIC-004 AC1 by making `epic init` create `ACCEPTANCE-MAP.md`.
- [x] AC2: Covers EPIC-004 AC1 by refreshing the map after decomposition and tracker changes.
- [x] AC3: Covers EPIC-004 AC1 by refreshing the map after audit/closeout with evidence and verdict state.
- [x] AC4: Covers EPIC-004 AC1 by updating README and generated epic guidance.
- [x] AC5: Covers EPIC-004 AC1 by adding fixture tests.

## Validation

- AC1 / EPIC-004 AC1: New epic fixture asserts `ACCEPTANCE-MAP.md` exists after `epic init`.
- AC2 / EPIC-004 AC1: Decomposition fixture asserts proposed child coverage appears in the map.
- AC3 / EPIC-004 AC1: Audit or closeout fixture asserts map evidence/verdict state refreshes.
- AC4 / EPIC-004 AC1: Documentation and generated epic guidance include map lifecycle language.
- AC5 / EPIC-004 AC1: `.venv/bin/pytest tests/test_doctor.py` passes.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Map Formatting Helper | Add helpers that derive and format acceptance map rows from requirements, tracker rows, deferrals, and child evidence. | AC1, AC2, AC3 | Fixture assertions inspect map content. | Done |
| 2 | Epic Command Integration | Write or refresh `ACCEPTANCE-MAP.md` from `epic init`, decompose, approve, scaffold-child, status, audit, and closeout. | AC1, AC2, AC3 | CLI fixtures pass. | Done |
| 3 | Documentation And Guidance | Update README and generated epic guidance with the map/audit distinction. | AC4 | Text checks or direct inspection. | Done |
| 4 | Fixture Coverage | Add tests for map creation, proposed coverage refresh, and evidence refresh. | AC5 | `.venv/bin/pytest tests/test_doctor.py`. | Done |

## Parent AC Evidence

- EPIC-004 AC1: Implemented acceptance map formatting and refresh behavior in `src/project_workflow/cli.py`, synced the packaged template and local helper, updated README and generated epic guidance, and added fixture assertions that `ACCEPTANCE-MAP.md` exists from epic init, updates after decomposition, and shows satisfied evidence after audit.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 30 tests, including acceptance map creation, decomposition refresh, and audit evidence refresh assertions.
- Findings: None.

## Retro

- Reusable lessons: Working epic-state views should be derived from existing workflow sources so they improve visibility without creating competing sources of truth.
- Conventions or agent assets updated: README, generated epic prompt, and generated Codex epic skill.
- Follow-up tasks: Continue EPIC-004 with closeout summary ergonomics.

## Notes

- Task: TASK-015
- Title: Acceptance Map From Epic Start
- Created: 2026-06-17
