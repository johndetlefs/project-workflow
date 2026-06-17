## User Story

As a project-workflow maintainer, I want epic audit and closeout commands to validate every parent acceptance criterion, so epics cannot close just because their child tasks appear complete.

## Goal

- Satisfy EPIC-002 AC7, AC8, AC9, AC13, and AC17 with executable epic audit and closeout gates.

## Parent AC Coverage

- EPIC-002 AC7: Epic audit artifact summarizes parent ACs, child tasks, evidence, verdicts, and deferrals.
- EPIC-002 AC8: CLI audit/closeout validates unmapped ACs, missing evidence, missing verdicts, and unapproved deferrals.
- EPIC-002 AC9: Epic closeout cannot mark the global epic row Complete without passing audit or approved deferrals.
- EPIC-002 AC13: Epic-level validation evidence is summarized.
- EPIC-002 AC17: Epic-managed child completion checks assigned parent AC evidence or approved deferral.

## Acceptance Criteria

- [x] AC1: Covers EPIC-002 AC7 by generating `ACCEPTANCE-AUDIT.md` with parent AC, mapped child, evidence, deferral, and verdict fields.
- [x] AC2: Covers EPIC-002 AC8 by blocking closeout when any parent AC is unmapped, lacks evidence, lacks QA pass, or has only pending child status.
- [x] AC3: Covers EPIC-002 AC9 by requiring explicit `--complete` before closeout mutates the global tracker and allowing mutation only when gates pass.
- [x] AC4: Covers EPIC-002 AC13 by summarizing child evidence into the audit artifact.
- [x] AC5: Covers EPIC-002 AC17 by treating completed child rows without parent AC evidence as blocking in closeout.

## Approach

- Build reusable audit helpers from parent requirements ACs, epic tracker rows, and child implementation docs.
- Keep audit generation deterministic and Markdown-native.
- Make closeout strict by default and mutating only with an explicit flag.
- Defer structured owner deferral approval fields to TASK-007 while keeping an audit column ready.

## Phases

### Phase 1

- Add `epic audit` command and `ACCEPTANCE-AUDIT.md` generation.
- Add evidence extraction from child `Parent AC Evidence` and QA verdict sections.

### Phase 2

- Add `epic closeout` validation and optional global tracker completion.
- Add passing and failing fixture tests.

## Tasks

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Audit Artifact | Generate epic-level `ACCEPTANCE-AUDIT.md` from parent requirements, tracker rows, and child docs. | AC1 / EPIC-002 AC7 and AC4 / EPIC-002 AC13: audit summarizes parent AC evidence. | Run audit fixture and inspect generated audit table. | Done |
| 2 | Closeout Gate | Block closeout on unmapped ACs, non-complete children, missing evidence, or missing QA pass verdicts. | AC2 / EPIC-002 AC8 and AC5 / EPIC-002 AC17: unsafe closeout exits non-zero with gaps. | Run failing closeout fixture. | Done |
| 3 | Explicit Completion | Allow global epic status mutation only with explicit `--complete` and passing gates. | AC3 / EPIC-002 AC9: closeout without flag validates only; closeout with flag completes only when safe. | Run passing closeout fixture with and without `--complete`. | Done |

## Validation

- AC1 / EPIC-002 AC7: audit generation fixture.
- AC2 / EPIC-002 AC8: failing closeout fixture.
- AC3 / EPIC-002 AC9: passing closeout mutation fixture.
- AC4 / EPIC-002 AC13: audit evidence summary fixture.
- AC5 / EPIC-002 AC17: completed-child-without-parent-evidence fixture.

## Parent AC Evidence

- EPIC-002 AC7: Implemented `epic audit` and `ACCEPTANCE-AUDIT.md` generation. Evidence: `tests/test_doctor.py::test_epic_audit_and_closeout_complete_only_when_gates_pass` passed; live `./.project-workflow/cli/workflow epic audit --epic-id EPIC-002` wrote the audit artifact.
- EPIC-002 AC8: Implemented strict closeout gap detection for unmapped, incomplete, missing-docs, missing-parent-evidence, and missing-QA cases. Evidence: `tests/test_doctor.py::test_epic_closeout_blocks_missing_parent_ac_evidence` passed.
- EPIC-002 AC9: Implemented explicit `--complete` status mutation only after gates pass. Evidence: `tests/test_doctor.py::test_epic_audit_and_closeout_complete_only_when_gates_pass` verified validate-only and completing paths.
- EPIC-002 AC13: Implemented epic-level evidence summary in `ACCEPTANCE-AUDIT.md`. Evidence: audit fixture asserted child evidence and QA pass summary in the generated artifact.
- EPIC-002 AC17: Implemented closeout blocking for completed children that lack parent AC evidence. Evidence: missing-parent-evidence fixture exits non-zero.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: audit row construction, parent AC summary parsing, child evidence extraction, QA verdict detection, closeout blocking, optional global completion, local helper parity, and fixtures.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 21 tests; live `./.project-workflow/cli/workflow epic audit --epic-id EPIC-002` generated `ACCEPTANCE-AUDIT.md` and correctly reported remaining epic gaps.
- AC evidence: AC1 / EPIC-002 AC7 covered by audit generation; AC2 / EPIC-002 AC8 covered by closeout blocker fixture; AC3 / EPIC-002 AC9 covered by explicit completion fixture; AC4 / EPIC-002 AC13 covered by audit evidence summary fixture; AC5 / EPIC-002 AC17 covered by missing-parent-evidence blocker fixture.
- Verdict: Pass.
- Findings: None.

## Retro

- Reusable lessons: Audit generation can safely run before an epic is complete and should produce actionable gap output rather than blocking iteration.
- Conventions or agent assets updated: None in this task.
- Follow-up tasks: TASK-007 should replace the placeholder deferral column with structured owner-approved deferrals.

## Notes

- Task: TASK-006
- Title: Epic Acceptance Audit And Closeout Gates
- Created: 2026-06-17
