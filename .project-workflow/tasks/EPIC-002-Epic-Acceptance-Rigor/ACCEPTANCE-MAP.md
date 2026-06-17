# Acceptance Map

## Summary

- Epic: EPIC-002
- Title: Epic Acceptance Rigor
- Last updated: 2026-06-17
- Purpose: Track parent acceptance criteria coverage from the start of the epic so child completion cannot be mistaken for epic completion.

## Coverage Matrix

| Parent AC | Requirement Summary | Proposed Child Coverage | Evidence Status | Closeout Status |
| --- | --- | --- | --- | --- |
| AC1 | Epic requirements templates and guidance create stable numbered parent AC IDs. | TASK-004 | TASK-004 QA passed | Satisfied |
| AC2 | Epic tracker rows support canonical parent AC coverage. | TASK-004 | TASK-004 QA passed | Satisfied |
| AC3 | `epic decompose` generates proposed child rows with parent AC coverage. | TASK-005 | TASK-005 QA passed | Satisfied |
| AC4 | `epic decompose` reports unmapped parent ACs. | TASK-005 | TASK-005 QA passed | Satisfied |
| AC5 | `epic scaffold-child` copies parent AC coverage into child docs. | TASK-005 | TASK-005 QA passed | Satisfied |
| AC6 | Child implementation and QA templates include parent AC sections for epic children. | TASK-004 | TASK-004 QA passed | Satisfied |
| AC7 | Epic audit artifact summarizes parent ACs, children, evidence, verdicts, and deferrals. | TASK-006 | TASK-006 QA passed | Satisfied |
| AC8 | CLI audit or closeout validates unmapped ACs, missing evidence, missing verdicts, and unapproved deferrals. | TASK-006 | TASK-006 and TASK-007 QA passed | Satisfied |
| AC9 | Epic closeout cannot mark the global epic row Complete without passing audit or approved deferrals. | TASK-006 | TASK-006 QA passed | Satisfied |
| AC10 | Owner-approved deferrals are structured with decision, date, reason, and follow-up reference. | TASK-007 | TASK-007 QA passed | Satisfied |
| AC11 | CLI status handling covers Testing, Review, and Complete transitions without manual tracker edits. | TASK-008 | TASK-008 QA passed | Satisfied |
| AC12 | Retro guidance distinguishes follow-ups from missed in-scope work. | TASK-007 | TASK-007 QA passed | Satisfied |
| AC13 | Epic-level validation evidence is summarized instead of scattered only across child docs. | TASK-006 | TASK-006 QA passed | Satisfied |
| AC14 | Agent docs require direct validation when possible and distinguish verified evidence from deferred setup. | TASK-009 | TASK-009 QA passed | Satisfied |
| AC15 | Root tracker versus epic tracker rules are explicit. | TASK-004, TASK-008 | TASK-004 and TASK-008 QA passed | Satisfied |
| AC16 | Automated tests cover complete coverage, missing mappings, evidence gaps, deferrals, and unsafe closeout. | TASK-009 | TASK-009 QA passed | Satisfied |
| AC17 | Epic-managed child completion checks assigned parent AC evidence or approved deferral. | TASK-006 | TASK-006 QA passed | Satisfied |
| AC18 | Package source, generated templates, generated agent assets, and installed local helper stay aligned. | TASK-009 | TASK-009 QA passed | Satisfied |

## Deferrals

No deferrals approved.

## Closeout Gate

EPIC-002 must not be marked `Complete` until every parent AC above has one of:

- Passing implementation and QA evidence linked from a child task.
- A documented owner-approved deferral with a follow-up task or epic ID.
- An explicit owner decision that the criterion is no longer required, recorded in `REQUIREMENTS.md`.
