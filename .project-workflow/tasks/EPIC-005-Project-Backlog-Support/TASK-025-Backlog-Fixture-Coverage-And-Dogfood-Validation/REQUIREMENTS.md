# Requirements

## Summary

- Task: TASK-025
- Title: Backlog fixture coverage and dogfood validation
- Parent AC Coverage: AC7, AC10
- Last updated: 2026-06-22

## Goal

Prove backlog support works end-to-end through focused fixtures, generated asset checks, and a small dogfood scenario before epic closeout.

## Non-Goals

- Re-implementing backlog commands covered by earlier child tasks.
- Migrating Daily Checklist or johndetlefs backlog documents.
- Running external services or networked planning integrations.
- Closing the parent epic without QA/code-review evidence from all child tasks.

## Users & Context

- Maintainers need confidence that backlog support works across init, lifecycle commands, validation, promotion, and generated assets.
- Agents need tests that fail clearly when backlog state becomes malformed or generated guidance drifts.
- The parent epic needs final evidence that promoted rows remain in the backlog and dogfood use is viable.

## Requirements (Outcome-Focused)

- Add automated tests for backlog init creation and existing-file preservation.
- Add automated tests for add/list/update/status behavior.
- Add automated tests for validation failures: malformed table, missing required fields, duplicate IDs, invalid vocabulary, and unresolved promoted references.
- Add automated tests for task promotion and epic promotion.
- Add automated checks that generated assets include backlog workflow support.
- Add automated tests or assertions proving promoted backlog rows remain in `.project-workflow/BACKLOG.md`.
- Run the relevant full or targeted test suite and record validation evidence.
- Dogfood the new backlog workflow with a small future project-workflow idea after the core commands exist.

## Acceptance Criteria (Verifiable)

- AC1: Tests cover backlog init creation and existing backlog preservation.
- AC2: Tests cover add/list/update/status behavior for valid backlog rows.
- AC3: Tests cover validation failures for malformed rows, missing fields, duplicate IDs, invalid type/priority/status values, and bad promoted references.
- AC4: Tests cover task promotion and epic promotion, including `## Backlog Source` provenance.
- AC5: Tests or assertions cover generated backlog assets across supported agent modes.
- AC6: Tests prove promoted rows remain in the backlog after promotion.
- AC7: A dogfood backlog row is created or proposed for a future project-workflow improvement and validation evidence is recorded.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Treat dogfood as evidence, not a migration exercise.
  - Why: The first dogfood scenario should prove the new workflow, not move unrelated roadmap documents.

- Decision: Prefer targeted fixtures plus existing doctor tests.
  - Why: Backlog behavior is mostly file/CLI behavior and should be testable without external services.

## Validation Plan

- Run new targeted backlog tests.
- Run `.venv/bin/pytest tests/test_doctor.py` or the updated relevant test suite.
- Run `./.project-workflow/cli/workflow doctor`.
- Record validation evidence in `IMPLEMENTATION.md`.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-005 --id TASK-025`.
