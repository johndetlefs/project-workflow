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
- If `mode` is `parallel` and `workers` is omitted, use `4`.

Execution contract:

- For each delegated work item, invoke `project.implement` as the execution path.
- Accept the provided work-item list and selected mode as the execution plan input.
- In `sequential` mode, execute exactly one work item at a time, in listed order.
- In `sequential` mode, initialize each item as `not started`, set current item to `in progress`, then mark it `completed` or `failed` before starting the next item.
- Emit a completion status line for each item before moving to the next item.
- Use the explicit dependency map provided in `dependencies` as the only prerequisite source.
- Before starting any item in `parallel` mode, validate dependency input strictly: reject unknown item IDs, self-dependencies, and cyclic dependencies.
- On dependency-validation failure, reject immediately and start no work items.
- In `parallel` mode, launch only eligible items whose prerequisites are completed.
- In `parallel` mode, allow independent eligible items to run concurrently up to the worker limit.
- Keep dependent items in `not started` until all prerequisites complete.
- On first work-item failure, enter fail-fast mode and stop launching any new pending items.
- Allow already `in progress` items to finish and report their terminal states.
- Mark any items that never started because of fail-fast as `halted` in run output.
- Final summary must clearly include overall result, failed item(s), failure cause, and halted item(s).
- End with a final aggregate summary that includes overall result and per-item terminal status.
- Preserve existing `project.*` agent behavior; do not rename or replace existing commands.

Scope note:

- This prompt defines the delegate entrypoint and routing contract only.
