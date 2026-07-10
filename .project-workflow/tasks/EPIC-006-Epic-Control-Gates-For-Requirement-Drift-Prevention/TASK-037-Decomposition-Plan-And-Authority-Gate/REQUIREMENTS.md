# Requirements

## Summary

- Task: TASK-037
- Title: Decomposition Plan And Authority Gate
- Parent AC Coverage: AC9, AC11, AC12, AC14, AC16, AC18
- Last updated: 2026-07-09
- Status: Approved for implementation under EPIC-006 authority envelope.

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Goal

Make epic decomposition an enforceable authority boundary so agents cannot create, approve, scaffold, or advance invented child rows outside the owner-approved decomposition without an amendment.

## Non-Goals

- Do not implement the full amendment workflow; rows outside the plan should point to the future amendment path.
- Do not require separate owner approval for every unchanged row that already appears in the approved decomposition plan.
- Do not replace epic trackers. Trackers remain execution state; the decomposition plan is the authority artifact.

## Users & Context

- Project owners need one approved decomposition boundary to stop child tasks being created on the fly during long epics.
- Agents need a mechanical check that distinguishes authorized child work from plausible but invented tracker rows.
- Reviewers need doctor/status failures when manual edits create active child rows without provenance.

## Requirements (Outcome-Focused)

- Add a first-class `DECOMPOSITION.md` artifact for epics. It must list authorized child rows by ID, title, parent AC coverage, and source.
- `epic decompose` must write the decomposition plan when it creates proposed child rows.
- If the epic requirements include a `Proposed Child Work` table, `epic decompose` must prefer that owner-reviewed table over generic prose-derived decomposition.
- `epic approve`, `epic scaffold-child`, `epic ready-child`, and `epic status` must reject child rows that are missing from the decomposition plan or whose ID/title/parent ACs differ from the plan.
- Doctor must fail active child rows that are outside the decomposition plan, even if they were created by manual tracker edits.
- Existing approved EPIC-006 rows must be recorded in a decomposition plan without requiring per-row owner reapproval.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC9 and AC14: child rows for new/adopted epics cannot be approved, scaffolded, readied, or advanced through gated status transitions unless they match `DECOMPOSITION.md` by ID, title, and parent AC coverage.
- AC2: Covers parent AC11 and AC18: README/CLI guidance describes the decomposition plan as the owner-approved boundary and clarifies that matching planned rows do not need per-row approval.
- AC3: Covers parent AC12 and AC16: automated tests prove `epic decompose` writes `DECOMPOSITION.md`, owner `Proposed Child Work` is preferred, unplanned rows are blocked, and doctor fails active manual rows without authority.

## Open Questions (Answer Needed)

- None blocking. The amendment workflow is intentionally left to TASK-033.

## Decisions (Resolved)

- The plan is a small Markdown table, not a new heavy database.
- Plan authority is inherited from the parent requirements approval envelope for rows already approved in the parent decomposition scope.
- The tracker is no longer sufficient authority for active child rows.

## Validation Plan

- Run `pytest tests/test_doctor.py` to cover decomposition-plan gates and existing lifecycle behavior.
- Run the full test suite.
- Run project doctor to confirm current EPIC-006 rows have valid decomposition authority.

