---
name: project.task
description: Create minimal task scaffolding (task folder, tracker row, optional branch).
argument-hint: title="..." branch=yes|no base=develop prefix=feature/
agent: agent
---

# task (Task + Optional Branch)

Purpose: create the minimal workflow scaffolding for a new feature/task inside this repo:

- A new task folder under `.project-workflow/tasks/<ID>-<Suffix>/`
- `IMPLEMENTATION.md` (must start with `## User Story`)
- `REQUIREMENTS.md`
- A new row in `.project-workflow/TRACKER.md`
- Optionally: create and checkout a git branch named from the assigned task id + title

This is the **only** step that creates folders/files for a new story. Requirements/Clarify/Planner/Implement/QA Review/Retro assume the task folder already exists.

Project Workflow is owner-directed and agent-operated. The user supplies product judgment, constraints, examples, decisions, and approvals conversationally. The agent runs commands, drafts artifacts, asks targeted questions, and records workflow state.

Read `/.project-workflow/guidance.md` if present before changing workflow state.

## Inputs (ask the user)

Ask the user these questions and wait for answers:

1. Task title

- Example: `Account Usage Export`

2. Create a new git branch?

- `yes` / `no`

If branch = yes, also ask:

- Base branch (default: `develop`)
- Branch prefix (default: `feature/`)

Minimum intake context before downstream work:

- Problem or opportunity
- Desired outcome
- Affected user, actor, or system
- Scope boundaries and non-goals
- Acceptance signal for done
- Constraints, priority/risk, and examples or failure modes

If the user has not provided this context, create the scaffold only as a requirements/clarification artifact. Do not proceed to planning or implementation until `task ready` passes or the owner explicitly records discovery/accepted risk.

Owner approval is required for the requirements/AC envelope before planning, but it is not a
repeated per-step ceremony. After that approval, the agent normally runs Planner, post-plan
Clarify, `task ready`, and moves to `Ready` autonomously. Pause only for material drift,
exceptional authority, requested/high-risk plan review, or an explicit setup-only boundary.

## Safety checks

Before creating a branch, ensure the repo working tree is clean. If it’s not clean, stop and ask the user to commit/stash first.

Task IDs are assigned automatically by the scaffolder. The default prefix is `TASK`,
but repositories can choose task ID namespaces and generation in
`.project-workflow/config.json` with `task_id_prefixes`,
`default_task_id_prefix`, `id_generation`, `unique_id_length`, and
`prefix_guidance`. Sequential IDs look like `TASK-001`; unique IDs keep the
prefix and use a 5-character base36 suffix by default, such as `WF-K7F3Q`.

## Action (run the scaffolder)

From the repo root, run:

- Without branch:

`./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker`

To use a configured namespace, add `--prefix <PREFIX>`:

`./.project-workflow/cli/workflow task init --prefix <PREFIX> --title "<TITLE>" --update-tracker`

- With branch:

`./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker --create-branch --base-branch <BASE> --branch-prefix <PREFIX>`

## Output (confirm back to the user)

After running:

- Confirm the created folder path under `.project-workflow/tasks/...`
- Confirm the assigned task ID (for example `TASK-001`, `UI-K7F3Q`, or another configured prefix)
- Confirm tracker updated
- If branch created, confirm the new branch name
- Run `./.project-workflow/cli/workflow doctor` and report any warnings or errors.

## Next step

Immediately proceed to `.github/prompts/Requirements.prompt.md` (prompt name:
`project.requirements`) for the new task (iteratively). Once requirements/ACs are confirmed and
approval is recorded, run `project.planner`, a post-plan `project.clarify` pass, `task ready`, and
move to `Ready`; then implement within the approved envelope when authorized.
