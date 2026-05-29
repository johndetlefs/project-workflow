---
name: project-planner
description: Use when turning confirmed project-workflow requirements into a phased implementation plan and testable work-item table.
---

# Project Planner

Turn confirmed requirements into a safe, incremental implementation plan.

## Invocation Rules

- Use this skill whenever the user asks for an implementation plan, phases, or testable work items for a project-workflow task, even if they ask in natural language.
- Read `AGENTS.md` first and follow its Workflow Skill Map and CLI Requirements.
- If the task folder does not exist, use `project-scaffold` first so the CLI creates the required files and tracker row.
- If requirements are missing or unclear, use `project-requirements` or `project-clarify` before planning.
- Planning is a document workflow unless the CLI adds an explicit planner command.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/TRACKER.md`
- `.project-workflow/CONSTITUTION.md` if present
- `AGENTS.md` and other repo instructions if present

## Workflow

1. Read requirements first and treat them as the source of truth.
2. If requirements are missing, unclear, or internally inconsistent, stop and use `project-requirements` or `project-clarify`.
3. Produce or update `IMPLEMENTATION.md` with:
   - `## User Story` at the top
   - `## Goal`
   - `## Approach`
   - `## Phases`
   - `## Tasks`
4. Make every task independently testable and outcome-based.
5. Use this table shape for tasks:

```md
|  ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
|   1 | <Outcome> | <What changes for the user/system?> | - <observable pass/fail criteria> | - <steps or command> | To Do |
```

6. Keep each table row on one physical line. Use `<br>` for multiple items inside a cell and escape literal `|` characters.
7. Include validation steps for each phase.
8. Include QA/code review as the required gate after implementation validation and before completion.
9. Do not implement code during planning.
