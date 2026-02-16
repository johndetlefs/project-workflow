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

Defaults:

- If `mode` is omitted, use `sequential`.

Execution contract:

- For each delegated work item, invoke `project.implement` as the execution path.
- Accept the provided work-item list and selected mode as the execution plan input.
- In `sequential` mode, execute exactly one work item at a time, in listed order.
- In `sequential` mode, initialize each item as `not started`, set current item to `in progress`, then mark it `completed` or `failed` before starting the next item.
- Emit a completion status line for each item before moving to the next item.
- End with a final aggregate summary that includes overall result and per-item terminal status.
- Preserve existing `project.*` agent behavior; do not rename or replace existing commands.

Scope note:

- This prompt defines the delegate entrypoint and routing contract only.
