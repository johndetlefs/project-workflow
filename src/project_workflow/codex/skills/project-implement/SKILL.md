---
name: project-implement
description: Use when implementing one project-workflow work item with requirements alignment, tracker updates, validation, and concise reporting.
---

# Project Implement

Implement one scoped work item from a project-workflow task and move it to testing.

## Invocation Rules

- Use this skill whenever the user asks to implement a project-workflow task or planned work item, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If the task folder does not exist, use `project-task` first so the CLI creates the required files and tracker row.
- If requirements or implementation tasks are missing, use `project-requirements` and `project-planner` before coding.
- Use the CLI for any supported tracker-safe operation before editing Markdown manually.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/TRACKER.md`
- Repo instruction files such as `AGENTS.md`

## Workflow

1. Infer the task ID from the user prompt or current branch if possible. Ask only if it cannot be inferred.
2. Infer the work item from the user prompt or the next `To Do` task in `IMPLEMENTATION.md`. Ask only if ambiguous.
3. Read `REQUIREMENTS.md` and `IMPLEMENTATION.md` before editing code.
4. Restate the selected work item and scope boundary.
5. Map each planned change to the relevant AC IDs. If a change does not map,
   stop and ask for direction.
6. Set the tracker row for the task to `In Progress` before coding.
7. Make the smallest safe code change that satisfies the selected work item.
8. Add or update tests when appropriate.
9. Run relevant automated checks and any required manual verification steps.
10. Set the tracker row to `Testing` after implementation and validation have run.
11. Run `./.project-workflow/cli/workflow doctor` and report workflow-state warnings or errors.
12. Do not set status to `Complete`; completion is owned by `project-qa-review` after QA/code review passes and the user explicitly asks.
13. Report changed files, validation results, remaining risks, and that `project-qa-review` is the next required lifecycle step.

If requirements conflict with repo constraints or validation is not testable, stop and use `project-clarify`.
