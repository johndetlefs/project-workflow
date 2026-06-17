## User Story

As a project-workflow maintainer, I want epic decomposition and child scaffolding to preserve parent AC coverage automatically, so every child task starts with visible responsibility for specific parent epic acceptance criteria.

## Goal

- Satisfy EPIC-002 AC3, AC4, and AC5 by making decomposition coverage visible, reporting unmapped parent ACs, and preserving parent ACs into child docs.

## Parent AC Coverage

- EPIC-002 AC3: `epic decompose` generates proposed child rows with parent AC coverage populated.
- EPIC-002 AC4: `epic decompose` reports parent ACs that remain unmapped.
- EPIC-002 AC5: `epic scaffold-child` copies approved row parent AC coverage into child task docs.

## Acceptance Criteria

- [x] AC1: Covers EPIC-002 AC3 by writing canonical `Parent ACs` values during decomposition for numbered parent AC-derived rows.
- [x] AC2: Covers EPIC-002 AC4 by printing a clear unmapped-parent-AC warning after decomposition when parent ACs from `REQUIREMENTS.md` are not covered by proposed rows.
- [x] AC3: Covers EPIC-002 AC5 by preserving parent AC coverage through scaffold-child into child `REQUIREMENTS.md`, child `IMPLEMENTATION.md`, and parent AC evidence sections.

## Approach

- Reuse the canonical `Parent ACs` field added in TASK-004.
- Add a helper that extracts parent AC IDs from epic requirements and compares them with coverage in the resulting tracker rows.
- Keep decompose output useful but non-blocking: unmapped ACs should be visible as warnings, not a hard error, because decomposition can be iterative.
- Extend fixture tests around `epic decompose` and `epic scaffold-child`.

## Phases

### Phase 1

- Implement unmapped parent AC reporting in package CLI and local workflow template/helper.
- Preserve current successful decompose behavior and legacy notes coverage.

### Phase 2

- Add fixture coverage for canonical parent ACs, unmapped warnings, and scaffold propagation.
- Run tests and doctor checks.

## Tasks

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Canonical Decompose Coverage | Ensure `epic decompose` writes `Parent ACs` for numbered parent AC-derived rows. | AC1 / EPIC-002 AC3: proposed rows include canonical parent AC coverage. | Run fixture test inspecting generated epic tracker rows. | Done |
| 2 | Unmapped AC Warning | Report parent ACs that are still unmapped after decompose. | AC2 / EPIC-002 AC4: command output lists unmapped parent AC IDs when limit or decomposition misses coverage. | Run fixture test with more parent ACs than generated rows. | Done |
| 3 | Child Scaffold Propagation | Verify scaffold-child carries parent AC coverage into child docs. | AC3 / EPIC-002 AC5: generated child docs include parent AC coverage and evidence sections. | Run fixture test for scaffold-child output. | Done |

## Validation

- AC1 / EPIC-002 AC3: targeted decompose fixture test.
- AC2 / EPIC-002 AC4: targeted unmapped warning fixture test.
- AC3 / EPIC-002 AC5: scaffold-child fixture test.

## Parent AC Evidence

- EPIC-002 AC3: Implemented canonical `Parent ACs` decompose output in `src/project_workflow/cli.py`, `src/project_workflow/templates/workflow.py`, and `.project-workflow/cli/workflow.py`. Evidence: `tests/test_doctor.py::test_epic_decompose_preserves_source_ac_ids_in_notes` passed.
- EPIC-002 AC4: Implemented unmapped parent AC reporting in decompose output. Evidence: `tests/test_doctor.py::test_epic_decompose_reports_unmapped_parent_ac_ids` passed.
- EPIC-002 AC5: Implemented parent AC propagation into epic child requirements, implementation, and evidence sections. Evidence: `tests/test_doctor.py::test_epic_child_scaffold_carries_parent_ac_sections` passed.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: `epic decompose` coverage output, unmapped parent AC warning behavior, scaffold-child parent coverage propagation, package/local helper parity, and fixture tests.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 19 tests.
- AC evidence: AC1 / EPIC-002 AC3 covered by canonical `Parent ACs` fixture; AC2 / EPIC-002 AC4 covered by unmapped warning fixture; AC3 / EPIC-002 AC5 covered by scaffold-child parent AC section fixture.
- Verdict: Pass.
- Findings: None.

## Retro

- Reusable lessons: Decompose can be iterative without blocking if unmapped parent ACs are reported loudly in command output.
- Conventions or agent assets updated: No additional guidance changes beyond TASK-004 were required.
- Follow-up tasks: TASK-006 should consume the same parent AC extraction helpers for audit/closeout.

## Notes

- Task: TASK-005
- Title: AC-Aware Decomposition And Child Scaffold
- Created: 2026-06-17
