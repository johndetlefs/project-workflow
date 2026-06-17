# Requirements

## Summary

- Task: TASK-005
- Title: AC-Aware Decomposition And Child Scaffold
- Parent Epic: EPIC-002 | Epic Acceptance Rigor
- Parent AC Coverage: EPIC-002 AC3, AC4, AC5
- Last updated: 2026-06-17

## Goal

Make epic decomposition and child scaffolding AC-aware enough that proposed child rows expose parent AC coverage, unmapped parent ACs are visible immediately, and approved child scaffolds preserve that coverage in child docs.

## Non-Goals

- Implementing epic audit or closeout commands; that belongs to TASK-006.
- Implementing owner deferral semantics; that belongs to TASK-007.
- Implementing general epic child status commands; that belongs to TASK-008.

## Users & Context

- Maintainers using `epic decompose` need coverage gaps shown before child rows are approved.
- Agents need a deterministic source for child parent AC coverage instead of relying on prose or scattered notes.
- Reviewers need child scaffolds to prove which parent ACs they own before implementation begins.

## Requirements (Outcome-Focused)

- `epic decompose` populates the `Parent ACs` field for child rows generated from numbered parent acceptance criteria.
- `epic decompose` warns when any parent epic AC remains unmapped after decomposition.
- `epic scaffold-child` preserves approved row parent AC coverage in child requirements and implementation docs.
- Legacy epic trackers using `Notes` coverage remain supported.
- Tests prove both canonical `Parent ACs` and legacy `Notes` flows.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-002 AC3 when `epic decompose` writes proposed child rows with parent AC coverage populated in `Parent ACs` for rows generated from numbered parent ACs.
- AC2: Covers EPIC-002 AC4 when `epic decompose` reports parent ACs from epic requirements that are not mapped into proposed child rows.
- AC3: Covers EPIC-002 AC5 when `epic scaffold-child` copies approved row parent AC coverage into child `REQUIREMENTS.md`, `IMPLEMENTATION.md`, and parent AC evidence sections.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Keep legacy `Notes` support while treating `Parent ACs` as canonical.
  - Context: Existing epics may already have coverage only in notes.
  - Chosen: New behavior writes `Parent ACs`; readers fall back to `Notes`.
  - Why: This improves validation without breaking existing workflow state.

## Validation Plan

- Add or update fixture tests for canonical decomposition coverage.
- Add fixture tests for unmapped parent AC warning output.
- Verify scaffold-child copies parent AC coverage into both child docs.
- Run `tests/test_doctor.py`, local workflow doctor, and packaged project doctor.
