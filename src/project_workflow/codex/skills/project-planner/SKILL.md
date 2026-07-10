---
name: project-planner
description: Use when turning confirmed project-workflow requirements into a phased implementation plan and testable work-item table.
---

# Project Planner

Turn confirmed requirements into a safe, incremental implementation plan.

## Invocation Rules

- Use this skill whenever the user asks for an implementation plan, phases, or testable work items for a project-workflow task, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If the task folder does not exist, use `project-task` first so the CLI creates the required files and tracker row.
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
4. Assign or preserve stable acceptance criteria IDs (`AC1`, `AC2`, etc.) from
   `REQUIREMENTS.md` and the `## Acceptance Criteria` section in
   `IMPLEMENTATION.md`.
5. Make every task independently testable and outcome-based.
6. Map every task row to one or more AC IDs, and ensure every AC ID is covered
   by at least one task row.
   If a row claims visual/reference fidelity, external contract alignment,
   deployed/published artifact alignment, runtime target/source verification,
   or responsive/multi-context behavior, include the matching proof recipe and
   evidence artifact expectation in the row. Do not use code review, tests,
   builds, surrogate surfaces, or related environments as recipe substitutes.
7. Use this table shape for tasks:

```md
|  ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
|   1 | <Outcome> | <What changes for the user/system?> | AC1: <observable pass/fail criteria> | <steps or command> | To Do |
```

8. Keep each table row on one physical line. Use `<br>` for multiple items
   inside a cell and escape literal `|` characters.
9. Include validation steps for each phase.
10. Run `./.project-workflow/cli/workflow task ready --id <TASK-ID>` after planning and before moving to `Plan Confirmed`; if it fails, fix the listed gaps or route to `project-clarify`. If requirements/AC approval is missing or stale after requirements are ready, record the one owner-approved envelope with `task approve-requirements`.
11. Include QA/code review as the required gate after implementation validation
    and before completion.
12. Do not implement code during planning.
