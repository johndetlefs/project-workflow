# Project Workflow

This repository uses project-workflow for spec-driven development. Keep workflow artifacts in `.project-workflow/` as the shared source of truth, and read `.project-workflow/guidance.md` for repo-specific workflow guidance when present.

## Workflow Order

1. Constitution: use `project-constitution` to establish or update `.project-workflow/CONSTITUTION.md` for product outcomes.
2. Task: use `project-task` to create one task folder under `.project-workflow/tasks/TASK-<NNN>-<Suffix>/`, with `REQUIREMENTS.md`, `IMPLEMENTATION.md`, and a tracker row.
3. Requirements: use `project-requirements` to capture the user story, scope, acceptance criteria, open questions, decisions, and validation plan in `REQUIREMENTS.md`.
4. Planner: use `project-planner` to turn confirmed requirements into testable work items in `IMPLEMENTATION.md`.
5. Clarify: use `project-clarify` to resolve inconsistencies between requirements, plan, repo constraints, and product outcomes before implementation.
6. Implement: use `project-implement` to make the smallest scoped code change for one work item, validate it, and move it to testing.
7. QA & Code Review: use `project-qa-review` to independently verify acceptance criteria and review the code before completion.
8. Retro: use `project-retro` after completion to update durable conventions, agent guidance, and follow-up tasks.

For multi-item orchestration, use `project-delegate` after planning. For large bodies of work, use `project-epic` to create proposal-first epic trackers and approved child tasks.

## Workflow Skill Map

- If the user asks to create, update, review, or align the product constitution, use `.agents/skills/project-constitution/SKILL.md`.
- If the user asks to create a task, story, feature folder, tracker row, or new project-workflow item, use `.agents/skills/project-task/SKILL.md`.
- If the user asks to create, decompose, approve, or scaffold epic-managed work, use `.agents/skills/project-epic/SKILL.md`.
- If the user asks to capture requirements, define scope, write acceptance criteria, record open questions, or prepare a validation plan, use `.agents/skills/project-requirements/SKILL.md`.
- If the user asks to plan implementation, break requirements into phases, or create testable work items, use `.agents/skills/project-planner/SKILL.md`.
- If the user asks to resolve ambiguity, reconcile conflicting requirements, or decide between unclear options, use `.agents/skills/project-clarify/SKILL.md`.
- If the user asks to implement a planned project-workflow item, use `.agents/skills/project-implement/SKILL.md`.
- If the user asks to coordinate or run multiple planned work items, use `.agents/skills/project-delegate/SKILL.md`.
- If the user asks for QA, code review, verification, release readiness, or completion approval, use `.agents/skills/project-qa-review/SKILL.md`.
- If the user asks for a retro, retrospective, lessons learned, convention updates, agent updates, prompt updates, or post-completion cleanup, use `.agents/skills/project-retro/SKILL.md`.
- If a task-specific workflow is requested but the task folder does not exist, run `project-task` first before requirements, planning, clarification, implementation, review, or retro.
- Do not skip directly to planning or implementation when requirements are missing, ambiguous, or not accepted as explicit risks.

## CLI Requirements

- Treat `.project-workflow/cli/workflow` as the authoritative way to perform operations it supports.
- Use the CLI for task scaffolding and tracker-safe task creation. Do not manually create task folders, starter `REQUIREMENTS.md`, starter `IMPLEMENTATION.md`, or tracker rows when the CLI can do it.
- Run project-workflow CLI commands from the repository root.
- If a selected project-workflow skill documents a CLI command, run that command instead of recreating its behavior manually.
- If the CLI does not support the selected workflow step, follow the selected skill and update the relevant Markdown files directly.
- If the CLI command fails, stop and report the failure before attempting a manual fallback.

## Codex Usage

- Use the repo-scoped skills in `.agents/skills/project-*` when the user asks for project workflow steps, even when the user asks in natural language rather than naming the skill.
- Read `.project-workflow/guidance.md` before changing workflow state when the file exists.
- If a task folder does not exist, run `./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker` from the repo root and let the CLI assign the next `TASK-###` ID.
- Read `.project-workflow/tasks/<ID>-*/REQUIREMENTS.md` before planning, implementing, reviewing, or running retro.
- Read `.project-workflow/tasks/<ID>-*/IMPLEMENTATION.md` before implementing, reviewing, or running retro for a work item.
- When planning, make every implementation task row map to one or more stable acceptance criteria IDs (`AC1`, `AC2`, etc.) from the task requirements or implementation acceptance criteria section.
- Keep `.project-workflow/TRACKER.md` status aligned with the current workflow state.
- Do not mark a task or work item `Complete` unless implementation validation and QA/code review have passed and the user explicitly asks for completion.

## Status Rules

- New scaffolded tasks start as `To Do`.
- Set the tracker row to `In Progress` before implementation work begins.
- Set the tracker row to `Testing` after implementation and validation have been run.
- Set the tracker row to `Review` while QA/code review is running.
- Set the tracker row to `Complete` only after QA/code review passes and the user explicitly requests it.
- Leave the tracker row as `Complete` during retro unless the user explicitly asks to reopen the task.

## Validation

- Run `.project-workflow/cli/workflow doctor` when workflow state is uncertain or before continuing after tracker/task doc edits.
- Use `.project-workflow/cli/workflow doctor --strict` when safety warnings should block autonomous work.
- Run the most relevant available tests, type checks, linters, or manual verification steps for the changed work.
- If broad validation fails for unrelated pre-existing reasons, run the narrowest meaningful checks and report the limitation.
