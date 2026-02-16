---
name: project.delegate
description: Coordinate delegated work items by routing each item through project.implement.
argument-hint: taskId=APP-330-Superuser workItems="1,2,3" mode=sequential dependencies="{}"
agent: agent
---

Use this prompt to coordinate delegated execution for task work items.

Inputs:

- Task: `${input:taskId:APP-000-Example}`
- Work items: `${input:workItems:1,2,3}`
- Mode: `${input:mode:sequential|parallel}`
- Dependencies: `${input:dependencies:{"2":["1"]}}`
- Worker limit: `${input:workers:4}`

Execution contract:

- For each delegated work item, invoke `project.implement` as the execution path.
- Keep delegation output concise and include per-item status updates.
- Preserve existing `project.*` agent behavior; do not rename or replace existing commands.

Scope note:

- This prompt defines the delegate entrypoint and routing contract only.
