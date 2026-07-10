# Requirements

## Summary

- Task: TASK-033
- Title: Epic Amendment Child Provenance And Drift Audit Flow
- Parent AC Coverage: AC8, AC9, AC12, AC14
- Last updated: 2026-07-09

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

- AC8: owner `TASK-033`; required evidence: Amendment records and reactive-fix gate tests.
- AC9: owner `TASK-033, TASK-037`; required evidence: Decomposition or amendment provenance and active row gate tests.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.
- AC14: owner `TASK-031, TASK-033, TASK-037`; required evidence: Decomposition plan authority, amendment provenance, and child inheritance gates.

## Goal

Add a supported amendment path so mid-epic child rows, reactive fixes, and material scope changes cannot enter the epic tracker without recorded provenance.

The workflow must make the valid exception path explicit: rows from the approved decomposition plan can proceed without repeated approval, while rows outside that plan require an owner-approved amendment recorded in `AMENDMENTS.md`.

## Non-Goals

- Do not build a full multi-step change-request workflow.
- Do not require amendments for unchanged rows already inside the approved decomposition plan.
- Do not make amendments satisfy parent AC evidence by themselves; amended children still need normal implementation, QA, and evidence gates.
- Do not implement legacy adoption in this child; TASK-034 owns pre-existing work adoption.

## Users & Context

- Agents need a supported command for legitimate mid-epic changes instead of hand-editing tracker rows.
- Owners need material scope/provenance decisions recorded once, with concrete reason and source metadata.
- Doctor/status gates need to distinguish approved amendment work from invented child rows.

## Requirements (Outcome-Focused)

- Add `AMENDMENTS.md` for epics with owner/source metadata for child-row amendments.
- Create `AMENDMENTS.md` during new epic initialization and backlog promotion to epic.
- Add `epic amend` to record an owner-approved amendment and append the matching Proposed child row.
- Require amendment metadata: child ID, title, parent ACs, owner approver, decision date, reason, and source.
- Extend decomposition authority gates so `epic approve`, `epic scaffold-child`, `epic ready-child`, `epic status`, and doctor accept rows outside `DECOMPOSITION.md` only when a matching valid amendment exists.
- Continue rejecting direct tracker edits outside both decomposition and amendment authority.
- Update README, CLI README, generated guidance, and project-epic skill guidance to route agents through `epic amend`.
- Add regression tests proving an amended row can approve/scaffold and an unamended row remains blocked.

## Acceptance Criteria (Verifiable)

- AC1: New epics include `AMENDMENTS.md` with an approved child-row amendment table. Covers parent AC8 and AC9.
- AC2: `epic amend` records owner-approved amendment metadata and appends the matching Proposed child row. Covers parent AC8 and AC14.
- AC3: Child rows outside `DECOMPOSITION.md` can advance only when a matching valid amendment exists. Covers parent AC9 and AC14.
- AC4: Direct tracker edits outside decomposition/amendment authority remain blocked by approval/status/doctor gates. Covers parent AC9 and AC14.
- AC5: Regression tests cover amendment authority and existing decomposition authority. Covers parent AC12.

## Open Questions (Answer Needed)

- None blocking. Amendment approval remains a material owner decision; ordinary in-envelope child work remains approval-free.

## Decisions (Resolved)

- `AMENDMENTS.md` is the amendment authority artifact.
- `epic amend` appends Proposed rows only; normal `epic approve` and `epic scaffold-child` gates still apply afterward.
- Amendment matching uses ID, title, and normalized parent AC coverage, matching the decomposition authority model.
- Missing/placeholder amendment approver, reason, source, or decision date invalidates amendment authority.

## Validation Plan

- Run focused amendment/decomposition regression tests.
- Run full pytest suite.
- Move TASK-033 through epic status gates.
- Run EPIC-006 audit and doctor.
