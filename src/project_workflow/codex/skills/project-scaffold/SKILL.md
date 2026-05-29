---
name: project-scaffold
description: Use when creating a new project-workflow task folder, tracker row, and optional branch for a feature or bugfix.
---

# Project Scaffold

Create the minimal workflow artifacts for one new task.

## Invocation Rules

- Use this skill whenever the user asks to create a project-workflow task, story, feature folder, tracker row, or new tracked work item, even if they ask in natural language.
- Read `AGENTS.md` first and follow its Workflow Skill Map and CLI Requirements.
- The local workflow CLI is mandatory for supported scaffold operations. Do not manually create task folders, starter files, or tracker rows when the CLI command is available.
- If another project-workflow skill needs a task folder that does not exist, route through this skill first.

## Inputs

Determine these from the user prompt, current branch, or follow-up questions:

- Task ID, such as `APP-331`
- Task title, such as `Account Usage Export`
- Whether to create a branch
- If creating a branch: base branch, default `develop`, and branch prefix, default `feature/`

## Workflow

1. Confirm `.project-workflow/TRACKER.md` exists. If missing, tell the user to run `project init` first.
2. Check `.project-workflow/TRACKER.md` for an existing row with the same task ID. If present, stop and ask whether to use a different ID or update the existing task manually.
3. If creating a branch, ensure the working tree is clean before switching branches.
4. Run the local scaffolder from the repo root:

Without branch:

```bash
./.project-workflow/cli/workflow task init --id <ID> --title "<TITLE>" --update-tracker
```

With branch:

```bash
./.project-workflow/cli/workflow task init --id <ID> --title "<TITLE>" --update-tracker --create-branch --base-branch <BASE> --branch-prefix <PREFIX>
```

5. Report the created task folder, tracker update, and branch name if one was created.
6. Continue to requirements capture when the user is ready, then proceed through planning, clarification, implementation, QA/code review, and retro.
