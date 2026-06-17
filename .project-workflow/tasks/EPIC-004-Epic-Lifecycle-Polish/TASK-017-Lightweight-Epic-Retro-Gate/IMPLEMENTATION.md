## User Story

As an owner closing an epic, I want a lightweight epic retro gate, so that lessons, follow-ups, deferrals, and missed in-scope work are explicitly reviewed before completion.

## Parent AC Coverage

- EPIC-004 AC3: Epic closeout blocks completion unless a lightweight epic retro is recorded, with sections for lessons, follow-up tasks, deferrals, missed in-scope work, and a permitted explicit "none" entry; generated guidance and tests cover the required retro behavior.

## Acceptance Criteria

- [x] AC1: Covers EPIC-004 AC3 by making `epic init` create `RETRO.md`.
- [x] AC2: Covers EPIC-004 AC3 by making `epic closeout` block missing or incomplete retro records.
- [x] AC3: Covers EPIC-004 AC3 by accepting explicit `None.` entries.
- [x] AC4: Covers EPIC-004 AC3 by updating README and generated epic guidance.
- [x] AC5: Covers EPIC-004 AC3 by adding fixture tests.

## Validation

- AC1 / EPIC-004 AC3: Epic init fixture asserts `RETRO.md` exists.
- AC2 / EPIC-004 AC3: Closeout fixture asserts missing/incomplete retro blocks completion.
- AC3 / EPIC-004 AC3: Closeout pass fixture records explicit `None.` entries.
- AC4 / EPIC-004 AC3: README and generated epic guidance mention the retro gate.
- AC5 / EPIC-004 AC3: `.venv/bin/pytest tests/test_doctor.py` passes.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Retro Template | Add an epic `RETRO.md` template created by `epic init`. | AC1 | Init fixture passes. | Done |
| 2 | Closeout Gate | Validate required retro sections during `epic closeout`. | AC2, AC3 | Closeout fixtures pass. | Done |
| 3 | Guidance Updates | Document the epic retro gate in README and generated epic guidance. | AC4 | Text checks or inspection. | Done |
| 4 | Fixture Coverage | Add blocked and passing retro gate assertions. | AC5 | `.venv/bin/pytest tests/test_doctor.py`. | Done |

## Parent AC Evidence

- EPIC-004 AC3: Implemented epic `RETRO.md` creation in `epic init`, added closeout validation for required retro sections, allowed explicit `None.` entries as substantive retro content, updated README and generated epic guidance, and added fixture coverage for init and closeout paths.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 30 tests, including epic retro template creation and closeout retro gate assertions.
- Findings: None.

## Retro

- Reusable lessons: A retro gate should prove topics were considered, while allowing explicit `None.` entries to avoid fake ceremony.
- Conventions or agent assets updated: README, generated epic prompt, and generated Codex epic skill.
- Follow-up tasks: Continue EPIC-004 with the minimal epic status lifecycle.

## Notes

- Task: TASK-017
- Title: Lightweight Epic Retro Gate
- Created: 2026-06-17
