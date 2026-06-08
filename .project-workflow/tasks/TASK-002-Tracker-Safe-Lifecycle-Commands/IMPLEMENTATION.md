## User Story

As a project-workflow maintainer, I want tracker lifecycle changes to run
through validated CLI commands, so agents can move work between statuses without
manually editing Markdown rows or bypassing workflow gates.

## Acceptance Criteria

- [ ] AC1: Packaged CLI exposes `project task status --id TASK-### --to
  <STATUS>`.
- [ ] AC2: Local workflow helper exposes the equivalent command.
- [ ] AC3: Command validates task ID, current tracker row, docs path, allowed
  statuses, and legal transitions.
- [ ] AC4: Illegal lifecycle transitions require an explicit force path with a
  reason.
- [ ] AC5: `Complete` transition is blocked unless QA/code-review evidence
  exists.
- [ ] AC6: Generated prompts, skills, and rules instruct agents to use the
  lifecycle command for tracker status changes.
- [ ] AC7: Tests cover valid transition, invalid transition, missing task/docs,
  and the completion gate.
- [ ] AC8: Doctor passes after changes, with only known historical warnings in
  this repository.
- [ ] AC9: Every implementation task row maps to one or more acceptance criteria
  IDs.
- [ ] AC10: Generated task, planner, and epic workflow assets require AC-to-task
  mapping for future tasks and epic-managed child tasks.
- [ ] AC11: Doctor reports active implementation plans whose task rows do not
  map to AC IDs.

## Validation

- `.venv/bin/python -m pytest`
- `.venv/bin/python -m project_workflow.cli doctor`
- `.venv/bin/python .project-workflow/cli/workflow.py doctor`
- Temporary repository smoke test for packaged and local `task status` commands

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | CLI Transition Command | Add a `task status` lifecycle command to the packaged CLI. | AC1, AC3, AC4: Supports `--id`, `--to`, optional force controls, and updates only the matching global tracker row. | Run command in a temp initialized repo and inspect tracker row. | To Do |
| 2 | Transition Validation & Gates | Implement status validation, transition validation, docs existence checks, and completion QA gate. | AC3, AC4, AC5: Invalid or unsafe transitions fail with clear non-zero errors. | Attempt invalid transitions and complete-without-QA in tests. | To Do |
| 3 | Local Helper Parity | Mirror the lifecycle command in the generated local workflow helper template. | AC2, AC8: `./.project-workflow/cli/workflow task status ...` behaves like the packaged CLI. | Run local helper in this repo and in a temp initialized repo. | To Do |
| 4 | Agent Guidance Updates | Update generated prompts, Codex skill guidance, Cursor rules, and related agent files to use the lifecycle command. | AC6: Agent assets no longer rely on manual tracker status edits where the command can be used. | Search generated assets for lifecycle command references and stale manual instructions. | To Do |
| 5 | Regression Tests & QA | Add focused tests and run workflow validation. | AC7, AC8, AC9: Pytest and doctor cover the new lifecycle behavior, installation parity, and AC mapping. | Review test output and doctor warnings. | To Do |
| 6 | AC Mapping Workflow Enforcement | Update future task, planner, and epic workflows so implementation task rows must reference stable AC IDs, and doctor warns when active plans miss those references. | AC9, AC10, AC11: Generated assets instruct agents to map task rows to AC IDs, and doctor detects active unmapped implementation task rows. | Create or inspect generated workflow assets, run targeted doctor tests, and run doctor on this repo. | Complete |

## QA & Code Review

- Verdict: Not started.
- Evidence: QA will be completed after implementation.
- Findings: None yet.

## Retro

- Reusable lessons: Pending.
- Conventions or agent assets updated: Pending.
- Follow-up tasks: Pending.

## Notes

- Task: TASK-002
- Title: Tracker-Safe Lifecycle Commands
- Created: 2026-06-05
- 2026-06-05: Added AC-mapping workflow enforcement before the lifecycle-command implementation because it is a prerequisite for safe agent execution and QA traceability.
