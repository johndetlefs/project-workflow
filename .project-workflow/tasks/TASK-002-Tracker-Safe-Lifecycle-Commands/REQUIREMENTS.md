# Requirements

## Summary

- Task: TASK-002
- Title: Tracker-Safe Lifecycle Commands
- Last updated: 2026-06-10

## Goal

Give maintainers and agents executable commands for changing project-workflow
task lifecycle state, so tracker updates are validated instead of manually edited.

## Non-Goals

- Replacing the Markdown tracker format.
- Implementing a full issue or project management system.
- Adding epic child lifecycle transitions in the first pass.
- Auto-completing tasks without explicit workflow evidence.
- Enforcing every workflow convention beyond status, document, and QA gates.

## Users & Context

- AI agents currently update `.project-workflow/TRACKER.md` manually when moving
  tasks through lifecycle states such as `In Progress`, `Testing`, `Review`, and
  `Complete`.
- Maintainers need status changes to be repeatable, reviewable, and safe.
- `project doctor` validates workflow state after the fact. This task adds safe
  mutation commands before the state changes.

## Requirements (Outcome-Focused)

- A maintainer or agent can move an existing global tracker task through the
  supported lifecycle with a CLI command.
- The command validates that the task exists, linked docs exist, the current
  status is known, the requested status is allowed, and the transition is legal.
- Completion is blocked unless QA/code-review evidence exists in the task
  implementation document.
- The packaged CLI and local workflow helper expose equivalent lifecycle
  commands.
- Generated prompts, skills, and rules use the lifecycle command instead of
  instructing agents to manually edit tracker rows.
- Regression tests cover successful transitions, invalid transitions, missing
  task/docs, and blocked completion without QA evidence.
- Implementation plans map each task row to the acceptance criteria it satisfies,
  so scope, execution, and QA stay aligned.
- Future task and epic workflows require stable AC IDs (`AC1`, `AC2`, etc.) and
  preserve those IDs through planning, epic decomposition, implementation, and
  validation.

## Acceptance Criteria (Verifiable)

- AC1: `project task status --id TASK-### --to <STATUS>` updates the global
  tracker row for an existing task.
- AC2: The same command is available through
  `./.project-workflow/cli/workflow task status ...`.
- AC3: Invalid statuses, missing IDs, missing docs, and unknown current statuses
  fail with clear non-zero errors.
- AC4: Illegal lifecycle transitions are refused unless an explicit force path
  is provided with a reason.
- AC5: `Complete` is refused unless the task doc contains non-placeholder
  `## QA & Code Review` evidence.
- AC6: Agent guidance is updated so implementation and review flows call the
  lifecycle command for tracker status changes.
- AC7: Pytest covers valid transition, invalid transition,
  complete-without-QA refusal, and local helper parity.
- AC8: `project doctor` and local `workflow doctor` pass after lifecycle command
  changes, subject only to known historical warnings.
- AC9: The implementation document maps every task row to one or more acceptance
  criteria IDs.
- AC10: Generated task, planner, and epic workflow assets require AC-to-task
  mapping for future tasks and epic-managed child tasks.
- AC11: Doctor reports active implementation plans whose task rows do not map to
  AC IDs.

## Open Questions (Answer Needed)

- Q1: Should the first pass include a separate `task complete` convenience
  command, or only `task status --to Complete`?
  - Recommendation: implement only `task status --to Complete` first. Add
    aliases later if repeated use proves worthwhile.
- Q2: Should force transitions be supported in the first pass?
  - Recommendation: include `--force --reason` only for non-`Complete`
    transitions, and continue blocking `Complete` without QA evidence.
- Q3: Should epic child rows be included?
  - Recommendation: no. Keep the first pass focused on global tracker rows.

## Decisions (Resolved)

- Decision: The first pass targets global tracker task rows only.
  - Why: This is the path every workflow step currently touches manually, and it
    limits blast radius.
- Decision: Completion must require QA/code-review evidence.
  - Why: This directly improves safe autonomy and reinforces the QA gate added
    in TASK-001.
- Decision: Generated agents should use the CLI status command once it exists.
  - Why: Each agent should not reimplement Markdown row edits.

## Validation Plan

- AC1/AC2: Run packaged and local lifecycle commands against temporary
  initialized repositories.
- AC3/AC4: Unit test invalid status, missing task, missing docs, and illegal
  transition cases.
- AC5: Unit test `Complete` transition with placeholder QA and with real QA
  evidence.
- AC6: Search generated prompts, skills, and rules for manual tracker edit
  instructions and lifecycle command references.
- AC7: Run `.venv/bin/python -m pytest`.
- AC8: Run `.venv/bin/python -m project_workflow.cli doctor` and
  `.venv/bin/python .project-workflow/cli/workflow.py doctor`.
- AC9: Review the implementation task table and confirm each row references at
  least one AC ID.
- AC10: Inspect generated task/planner/epic assets and initialized mirrors for
  AC-mapping instructions.
- AC11: Add regression coverage for doctor warnings on unmapped active task rows.
