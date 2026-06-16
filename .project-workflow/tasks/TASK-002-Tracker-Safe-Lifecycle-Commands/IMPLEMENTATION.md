## User Story

As a project-workflow maintainer, I want tracker lifecycle changes to run
through validated CLI commands, so agents can move work between statuses without
manually editing Markdown rows or bypassing workflow gates.

## Acceptance Criteria

- [x] AC1: Packaged CLI exposes `project task status --id TASK-### --to
  <STATUS>`.
- [x] AC2: Local workflow helper exposes the equivalent command.
- [x] AC3: Command validates task ID, current tracker row, docs path, allowed
  statuses, and legal transitions.
- [x] AC4: Illegal lifecycle transitions require an explicit force path with a
  reason.
- [x] AC5: `Complete` transition is blocked unless QA/code-review evidence
  exists.
- [x] AC6: Generated prompts, skills, and rules instruct agents to use the
  lifecycle command for tracker status changes.
- [x] AC7: Tests cover valid transition, invalid transition, missing task/docs,
  and the completion gate.
- [x] AC8: Doctor passes after changes, with only known historical warnings in
  this repository.
- [x] AC9: Every implementation task row maps to one or more acceptance criteria
  IDs.
- [x] AC10: Generated task, planner, and epic workflow assets require AC-to-task
  mapping for future tasks and epic-managed child tasks.
- [x] AC11: Doctor reports active implementation plans whose task rows do not
  map to AC IDs.

## Validation

- `.venv/bin/python -m pytest` -> 16 passed.
- `.venv/bin/python -m project_workflow.cli doctor` -> passed with known historical APP-001/002/003 QA-evidence warnings.
- `.venv/bin/python .project-workflow/cli/workflow.py doctor` -> passed with the same known historical APP warnings.
- `.venv/bin/python -m project_workflow.cli task status --help` -> packaged command help works.
- `.venv/bin/python .project-workflow/cli/workflow.py task status --help` -> local helper command help works.
- Temporary repository smoke coverage verifies packaged and local `task status` commands.
- Init-refresh regression verifies old generated local helpers are refreshed to expose `task status`, and managed agent guidance includes the lifecycle command.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | CLI Transition Command | Add a `task status` lifecycle command to the packaged CLI. | AC1, AC3, AC4: Supports `--id`, `--to`, optional force controls, and updates only the matching global tracker row. | Run command in a temp initialized repo and inspect tracker row. | Complete |
| 2 | Transition Validation & Gates | Implement status validation, transition validation, docs existence checks, and completion QA gate. | AC3, AC4, AC5: Invalid or unsafe transitions fail with clear non-zero errors. | Attempt invalid transitions and complete-without-QA in tests. | Complete |
| 3 | Local Helper Parity | Mirror the lifecycle command in the generated local workflow helper template. | AC2, AC8: `./.project-workflow/cli/workflow task status ...` behaves like the packaged CLI. | Run local helper in this repo and in a temp initialized repo. | Complete |
| 4 | Agent Guidance Updates | Update generated prompts, Codex skill guidance, Cursor rules, and related agent files to use the lifecycle command. | AC6: Agent assets no longer rely on manual tracker status edits where the command can be used. | Search generated assets for lifecycle command references and stale manual instructions. | Complete |
| 5 | Regression Tests & QA | Add focused tests and run workflow validation. | AC7, AC8, AC9: Pytest and doctor cover the new lifecycle behavior, installation parity, and AC mapping. | Review test output and doctor warnings. | Complete |
| 6 | AC Mapping Workflow Enforcement | Update future task, planner, and epic workflows so implementation task rows must reference stable AC IDs, and doctor warns when active plans miss those references. | AC9, AC10, AC11: Generated assets instruct agents to map task rows to AC IDs, and doctor detects active unmapped implementation task rows. | Create or inspect generated workflow assets, run targeted doctor tests, and run doctor on this repo. | Complete |

## QA & Code Review

- Date: 2026-06-10
- Reviewed areas: packaged CLI status command, generated local helper parity, transition validation, forced-transition guardrails, completion gate, init refresh behavior, generated prompt/skill/rule guidance, README/CLI docs, and regression coverage.
- Verdict: Pass.
- Evidence:
  - `.venv/bin/python -m pytest` -> 16 passed.
  - `git diff --check` -> passed.
  - `.venv/bin/python -m project_workflow.cli doctor` -> passed with known historical APP-001/002/003 QA-evidence warnings.
  - `.venv/bin/python .project-workflow/cli/workflow.py doctor` -> passed with the same known historical APP warnings.
  - Packaged and local `task status --help` smoke checks both show the lifecycle command and options.
  - Self-hosted lifecycle smoke moved `TASK-002` from `In Progress` to `Testing`, then `Review` with the local lifecycle command.
- Findings: None blocking.

## Retro

- Date: 2026-06-10
- Reusable lessons:
  - Agent-safe workflow commands need a full install-surface pass: packaged CLI, generated local helper, generated prompts/skills/rules, README/CLI docs, managed host guidance, and init-refresh tests.
  - New agent-facing subcommands should have help smoke coverage so agents and users can discover the command contract without reading source.
  - Completion gating is stronger when the workflow mutator enforces QA evidence before `Complete`, not only when `doctor` warns after the fact.
- Conventions or agent assets updated:
  - `.github/copilot-instructions.md` now documents the expected update surface and help coverage for future workflow CLI commands.
  - Generated prompt, Codex, Cursor, and README assets were updated during implementation to route tracker changes through `task status`.
- Follow-up tasks:
  - Consider durable audit logging for forced non-`Complete` transitions if force usage becomes common.
  - Consider extending lifecycle commands to epic child rows after the global task command has been used in practice.

## Notes

- Task: TASK-002
- Title: Tracker-Safe Lifecycle Commands
- Created: 2026-06-05
- 2026-06-05: Added AC-mapping workflow enforcement before the lifecycle-command implementation because it is a prerequisite for safe agent execution and QA traceability.
- 2026-06-10: Implemented `task status` in packaged and local CLIs, updated generated guidance to use it, and added regression tests for transitions, force reasons, missing docs, and completion gating.
