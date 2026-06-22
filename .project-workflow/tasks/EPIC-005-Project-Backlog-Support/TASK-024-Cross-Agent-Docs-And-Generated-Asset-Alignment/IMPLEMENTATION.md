## User Story

As a project-workflow user, I want backlog support to appear consistently in every supported agent mode, so that the same repo workflow works with Copilot, Claude, Codex, and Cursor.

## Parent AC Coverage

- AC1, AC3, AC8, AC9

## Acceptance Criteria

- [x] AC1: Copilot generated assets include backlog workflow support.
- [x] AC2: Claude generated assets include backlog workflow support.
- [x] AC3: Codex generated assets include backlog workflow support.
- [x] AC4: Cursor generated assets include backlog workflow support.
- [x] AC5: README documents backlog placement, examples, and traceability.
- [x] AC6: Generated guidance says promoted rows remain in backlog and execution state lives in trackers.
- [x] AC7: Generated guidance says existing roadmap/backlog docs are preserved and not automatically imported.

## Validation

- AC1 / parent ACs AC1, AC8: Passed in `test_doctor_passes_for_clean_initialized_repo`; `.github/prompts/Backlog.prompt.md` is generated and contains `project.backlog` plus promoted-row guidance.
- AC2 / parent AC AC8: Passed in `test_agent_mode_init_installs_doctor_guidance`; Claude mode generates `.claude/agents/project-backlog.md`.
- AC3 / parent AC AC8: Passed in `test_agent_mode_init_installs_doctor_guidance`; Codex mode installs `.agents/skills/project-backlog/SKILL.md` and `AGENTS.md` backlog guidance.
- AC4 / parent AC AC8: Passed in `test_agent_mode_init_installs_doctor_guidance`; Cursor mode generates `.cursor/agents/project-backlog.md` and backlog-aware rules.
- AC5 / parent AC AC9: README now documents backlog placement, example add/status/promote commands, promoted-row traceability, and existing-doc preservation.
- AC6 / parent AC AC3: Generated prompt, Codex skill, AGENTS guidance, Cursor rules, and README state that promoted rows stay in backlog and execution state belongs in trackers/task/epic docs.
- AC7 / parent AC AC9: Generated prompt, Codex skill, AGENTS guidance, Cursor rules, and README state existing roadmap/backlog docs are preserved and not automatically imported.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add generated backlog assets | Add backlog prompt/agent/skill source files and include them in generation lists for Copilot, Claude, Codex, and Cursor. | AC1: Copilot asset exists.<br>AC2: Claude asset exists.<br>AC3: Codex asset exists.<br>AC4: Cursor asset exists. | Passed via generated asset tests for Copilot, Claude, Codex, and Cursor modes. | Done |
| 2 | Update shared agent guidance | Update AGENTS managed block, Cursor rules, and skill maps so agents know when and how to use backlog workflow. | AC3: Codex guidance includes backlog.<br>AC4: Cursor rule includes backlog.<br>AC6: Guidance preserves promoted-row and tracker-boundary language.<br>AC7: Existing-doc preservation is stated. | Passed via generated guidance assertions and source inspection. | Done |
| 3 | Update README workflow docs | Document backlog placement, optional use, lifecycle examples, promotion traceability, and legacy-doc preservation. | AC5: README explains backlog placement and examples.<br>AC6: README states promoted rows remain in backlog.<br>AC7: README states existing roadmap/backlog docs are not automatically imported. | Passed by README review and test coverage for generated guidance. | Done |

## Parent AC Evidence

- AC1: `project init` now installs backlog artifact and backlog workflow guidance for every supported agent mode; verified by generated asset tests.
- AC3: README and generated guidance preserve the boundary that backlog status is not active implementation status and promoted execution state lives in trackers/task/epic docs.
- AC8: Copilot, Claude, Codex, and Cursor generated assets all include backlog creation, refinement, validation, and promotion guidance.
- AC9: README and installed workflow guidance explain backlog placement relative to constitution, tracker, tasks, and epics, with examples for capture, acceptance, promotion, and traceability.

## QA & Code Review

- Verdict: Pass.
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py` passed with 40 tests; generated asset assertions cover Copilot, Claude, Codex, and Cursor; `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor` passed with only pre-existing legacy warnings.
- Findings: No blocking findings in generated assets or README guidance.

## Retro

- Reusable lessons: Cross-agent workflow changes should be validated through init-generation tests, not source-file inspection alone.
- Conventions or agent assets updated: Added backlog prompt, Codex skill, Claude/Cursor generated agents, AGENTS guidance, Cursor rule guidance, Copilot instructions, and README docs.
- Follow-up tasks: None.

## Notes

- Task: TASK-024
- Title: Cross-agent docs and generated asset alignment
- Created: 2026-06-22
