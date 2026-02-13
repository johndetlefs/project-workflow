---
name: project.scaffold
description: Create minimal task scaffolding (task folder, tracker row, optional branch).
argument-hint: taskId=APP-331 title="..." branch=yes|no base=develop prefix=feature/
agent: agent
---

# scaffold (Task + Optional Branch)

Purpose: create the minimal workflow scaffolding for a new feature/task inside this repo:

- A new task folder under `.project-workflow/tasks/<ID>-<Suffix>/`
- `IMPLEMENTATION.md` (must start with `## User Story`)
- `REQUIREMENTS.md`
- A new row in `.project-workflow/TRACKER.md`
- Optionally: create and checkout a git branch named from the task id + title

This is the **only** step that creates folders/files for a new story. Requirements/Clarify/Planner/Implement assume the task folder already exists.

## Inputs (ask the user)

Ask the user these questions and wait for answers:

1. Task ID

- Example: `APP-331`

2. Task title

- Example: `Account Usage Export`

3. Create a new git branch?

- `yes` / `no`

If branch = yes, also ask:

- Base branch (default: `develop`)
- Branch prefix (default: `feature/`)

## Safety checks

Before creating a branch, ensure the repo working tree is clean. If it's not clean, stop and ask the user to commit/stash first.

If `.project-workflow/TRACKER.md` already contains the task ID, stop and ask the user whether to:

- use a different ID, or
- manually update the existing entry.

## Action (run the scaffolder)

From the repo root, run:

- Without branch:

`./.project-workflow/cli/workflow task init --id <ID> --title "<TITLE>" --update-tracker`

- With branch:

`./.project-workflow/cli/workflow task init --id <ID> --title "<TITLE>" --update-tracker --create-branch --base-branch <BASE> --branch-prefix <PREFIX>`

## Output (confirm back to the user)

After running:

- Confirm the created folder path under `.project-workflow/tasks/…`
- Confirm tracker updated
- If branch created, confirm the new branch name

## Next step

Immediately proceed to `.github/prompts/Requirements.prompt.md` (prompt name: `project.requirements`) for the new task (iteratively), then use `project.clarify` / `project.planner` / `project.implement` as needed.
