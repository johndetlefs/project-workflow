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

This is the **only** step that creates folders/files for a new story. Requirements/Clarify/Planner/Implement assume the task folder already exists.

## Inputs (ask the user)

Ask the user these questions and wait for answers:

1. Task title

- Example: `Account Usage Export`

2. Create a new git branch?

- `yes` / `no`

If branch = yes, also ask:

- Base branch (default: `develop`)
- Branch prefix (default: `feature/`)

## Safety checks

Before creating a branch, ensure the repo working tree is clean. If it’s not clean, stop and ask the user to commit/stash first.

Task IDs are assigned automatically in sequential `TASK-###` format by the scaffolder.

## Action (run the scaffolder)

From the repo root, run:

- Without branch:

`./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker`

- With branch:

`./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker --create-branch --base-branch <BASE> --branch-prefix <PREFIX>`

## Output (confirm back to the user)

After running:

- Confirm the created folder path under `.project-workflow/tasks/...`
- Confirm the assigned task ID (`TASK-###`)
- Confirm tracker updated
- If branch created, confirm the new branch name

## Next step

Immediately proceed to `.github/prompts/Requirements.prompt.md` (prompt name: `project.requirements`) for the new task (iteratively), then use `project.clarify` / `project.planner` / `project.implement` as needed.
