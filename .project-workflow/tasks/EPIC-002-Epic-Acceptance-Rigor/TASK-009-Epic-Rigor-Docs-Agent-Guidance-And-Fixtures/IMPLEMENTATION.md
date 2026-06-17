## User Story

As a project-workflow maintainer, I want the epic rigor behavior backed by docs, generated guidance, fixture tests, and parity checks, so shipped workflow assets enforce the same discipline validated in this repository.

## Parent AC Coverage

- EPIC-002 AC14: Documentation and generated Codex/Copilot/Cursor assets tell agents to run direct validation where possible and distinguish verified connector evidence from deferred setup.
- EPIC-002 AC16: Automated tests cover complete coverage, missing mappings, evidence gaps, deferrals, and unsafe closeout attempts.
- EPIC-002 AC18: Package source, generated templates, generated agent assets, and installed local helper stay aligned.

## Acceptance Criteria

- [x] AC1: Covers EPIC-002 AC14 by updating README and generated QA guidance for direct validation and verified-vs-deferred evidence.
- [x] AC2: Covers EPIC-002 AC16 by adding/confirming fixture coverage for the epic rigor gates and generated guidance.
- [x] AC3: Covers EPIC-002 AC18 by verifying source/template/helper and generated prompt parity.

## Validation

- AC1 / EPIC-002 AC14: README, generated QA skill, source QA prompt, and installed QA prompt mirror include direct-validation and verified-vs-deferred evidence guidance.
- AC2 / EPIC-002 AC16: `tests/test_doctor.py` covers AC-aware decomposition, unmapped AC reporting, child scaffold propagation, legacy tracker support, audit/closeout success, missing evidence blockers, approved deferral acceptance, incomplete deferral blocking, child Complete evidence gating, completed-epic audit evidence recognition by strict doctor, and generated QA guidance.
- AC3 / EPIC-002 AC18: Final validation compares generated workflow and prompt mirrors, then runs local helper doctor and installed package doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | QA Guidance Sweep | Update README and generated QA assets for direct validation and verified-vs-deferred evidence. | AC1 / EPIC-002 AC14 | Inspect docs and generated prompt mirrors. | Done |
| 2 | Fixture Coverage Sweep | Confirm tests cover passing and failing epic rigor scenarios. | AC2 / EPIC-002 AC16 | Run `.venv/bin/pytest tests/test_doctor.py`. | Done |
| 3 | Self-Hosted Parity Sweep | Verify package source, generated templates, installed helper, source prompts, and installed prompt mirrors align. | AC3 / EPIC-002 AC18 | Run cmp checks, doctor checks, and diff whitespace check. | Done |

## Parent AC Evidence

- EPIC-002 AC14: README QA workflow, generated QA skill, source QA prompt, installed QA prompt mirror, and generated guidance fixture assertions now require direct validation when available and separate verified evidence from deferred setup or unavailable connector/OAuth checks.
- EPIC-002 AC16: Automated fixtures in `tests/test_doctor.py` cover complete audit/closeout, unmapped parent AC reporting, missing parent AC evidence blockers, approved deferral acceptance, incomplete deferral blocking, unsafe closeout blocking, epic child Complete evidence gating, completed-epic audit evidence recognition by strict doctor, and generated QA guidance assertions.
- EPIC-002 AC18: Source and installed workflow helper parity plus source and installed prompt parity are validated by exact file comparisons; local helper doctor and installed package doctor both run against this repository.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: README QA workflow guidance, generated QA skill, generated QA prompt, installed prompt mirror, fixture coverage, workflow helper parity, prompt mirror parity.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 24 tests after adding the completed-epic audit evidence regression; `./.project-workflow/cli/workflow doctor` passed with only pre-existing APP-001/002/003 QA-evidence warnings; `.venv/bin/project doctor` passed with the same pre-existing warnings; `git diff --check` passed; exact `cmp` checks passed for `src/project_workflow/templates/workflow.py` versus `.project-workflow/cli/workflow.py`, and for Epic, Retro, and QAReview prompt mirrors.
- AC evidence: AC1 / EPIC-002 AC14 covered by docs/generated guidance; AC2 / EPIC-002 AC16 covered by fixture tests; AC3 / EPIC-002 AC18 covered by parity checks.
- Verdict: Pass.
- Findings: None.

## Retro

- Reusable lessons: The final epic task should prove the workflow assets users install, not only the package source.
- Conventions or agent assets updated: README, generated QA skill, QAReview prompt, and installed prompt mirror.
- Follow-up tasks: None.
- Missed in-scope work: None.

## Notes

- Task: TASK-009
- Title: Epic Rigor Docs Agent Guidance And Fixtures
- Created: 2026-06-17
