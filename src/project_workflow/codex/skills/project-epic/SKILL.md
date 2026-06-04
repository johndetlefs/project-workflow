---
name: project-epic
description: Use when creating, decomposing, approving, or scaffolding proposal-first project-workflow epics.
---

# Project Epic

Manage proposal-first epic work under `.project-workflow/tasks/`.

## Invocation Rules

- Use this skill whenever the user asks for an epic, epic decomposition, proposed child work, approval of epic rows, or scaffolding an approved epic child task.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- Use the local workflow CLI for every supported epic operation.
- Do not scaffold child task folders until the relevant epic tracker row is `Approved`.

## Workflows

Create a new epic:

```bash
./.project-workflow/cli/workflow epic init --title "<TITLE>"
```

Decompose an epic into proposed child rows only:

```bash
./.project-workflow/cli/workflow epic decompose --epic-id <EPIC-ID> --limit 5 --type Task
```

Approve one proposed child row:

```bash
./.project-workflow/cli/workflow epic approve --epic-id <EPIC-ID> --id <TASK-ID>
```

Scaffold one approved child row:

```bash
./.project-workflow/cli/workflow epic scaffold-child --epic-id <EPIC-ID> --id <TASK-ID>
```

Scaffold one approved child row with a branch from an existing epic branch:

```bash
./.project-workflow/cli/workflow epic scaffold-child --epic-id <EPIC-ID> --id <TASK-ID> --create-branch --epic-branch <EPIC-BRANCH>
```

## Rules

- `epic init` creates an epic `REQUIREMENTS.md` and epic `TRACKER.md`.
- `epic decompose` writes Proposed child rows only and does not create child task folders.
- `epic approve` moves a child row from `Proposed` to `Approved`.
- `epic scaffold-child` only accepts `Approved` child rows and moves them to `In Progress` after scaffold.
- Child IDs remain globally unique `TASK-###` IDs across standalone and epic-managed work.
- When `--create-branch` is used, the epic branch must already exist; do not fall back to a base branch.
- After any epic tracker or child scaffold change, run `./.project-workflow/cli/workflow doctor` and report workflow-state warnings or errors.
