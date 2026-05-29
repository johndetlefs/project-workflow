---
name: project-scaffold
description: Legacy alias for project-task when creating a new project-workflow task folder, tracker row, and optional branch.
---

# Project Scaffold

Legacy alias for `project-task`.

## Invocation Rules

- Prefer `.agents/skills/project-task/SKILL.md` for new work.
- Use this skill only when the user or local environment still refers to `project-scaffold`.
- Read `AGENTS.md` first and follow its Workflow Skill Map and CLI Requirements.
- The local workflow CLI is mandatory for supported scaffold operations. Do not manually create task folders, starter files, or tracker rows when the CLI command is available.
- If another project-workflow skill needs a task folder that does not exist, route through this skill first.

## Inputs

Determine these from the user prompt, current branch, or follow-up questions:

- Task title, such as `Account Usage Export`
- Whether to create a branch
- If creating a branch: base branch, default `develop`, and branch prefix, default `feature/`

## Workflow

1. Confirm `.project-workflow/TRACKER.md` exists. If missing, tell the user to run `project init` first.
2. If creating a branch, ensure the working tree is clean before switching branches.
3. Run the local scaffolder from the repo root and let it assign the next `TASK-###` ID:

Without branch:

```bash
./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker
```

With branch:

```bash
./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker --create-branch --base-branch <BASE> --branch-prefix <PREFIX>
```

4. Report the created task folder, assigned task ID, tracker update, and branch name if one was created.
5. Continue to requirements capture when the user is ready, then proceed through planning, clarification, implementation, QA/code review, and retro.
