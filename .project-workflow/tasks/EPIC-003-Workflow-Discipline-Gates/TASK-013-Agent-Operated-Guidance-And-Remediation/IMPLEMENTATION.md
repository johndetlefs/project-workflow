## User Story

As an agent operating project-workflow for an owner, I want generated guidance and gate failures to tell me what to do next, so I stop for owner input only when product judgment is required.

## Parent AC Coverage

- EPIC-003 AC11: Generated agent guidance defines the owner-directed, agent-operated role split.
- EPIC-003 AC13: Gate failures distinguish repo-gatherable facts, assumptions, and owner-required decisions.

## Acceptance Criteria

- [x] AC1: Covers EPIC-003 AC11 by updating AGENTS, Codex skills, Cursor rules, and prompts with the owner/agent role split.
- [x] AC2: Covers EPIC-003 AC13 by shaping readiness failures as owner input required or agent action required.

## Validation

- AC1: `test_agent_mode_init_installs_doctor_guidance` asserts generated assets mention owner-directed/agent-operated and readiness commands.
- AC2: `test_task_ready_blocks_placeholders_and_allows_ready_docs` asserts readiness failures include owner input required and agent action required.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Agent Role Guidance | Update generated agent assets to define owner-directed, agent-operated workflow. | AC1: Generated assets carry the role split. | Run generated asset fixture. | Done |
| 2 | Remediation Messages | Categorize readiness failures by owner input and agent action. | AC2: Readiness failures are actionable. | Run readiness failure fixture. | Done |

## Parent AC Evidence

- EPIC-003 AC11: AGENTS, Task/Requirements/Planner/Implement/Epic prompts, Codex skills, and Cursor rules now define or reinforce the owner-directed, agent-operated workflow.
- EPIC-003 AC13: Readiness failures include owner input required and agent action required messages.
- EPIC-003 AC11 / AC13: Generated Codex guidance now tells agents to use the canonical `uvx --from git+https://github.com/johndetlefs/project-workflow.git project init` command when installing or refreshing project-workflow, and explicitly avoids bare `project init` unless the package is intentionally installed and current.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: generated skills, prompts, Cursor rules, readiness error messages.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 30 tests, including regression coverage for the canonical UVX install/update command in generated Codex guidance.
- Findings: None.
- Verdict: Pass.

## Retro

- Reusable lessons: Agent-facing errors should be written as next-action checklists.
- Conventions or agent assets updated: AGENTS, Codex skills, Cursor rules, prompts.
- Follow-up tasks: None.
- Missed in-scope work: None.
