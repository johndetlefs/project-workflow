# Project Workflow CLI (local)

This folder contains a small helper CLI for the repo’s AI workflow.

Goals:

- Keep workflow scaffolding **out of** `package.json` scripts.
- Keep it **co-located** with the workflow artifacts (`.project-workflow/`), so it’s easy to use and later extract.

## Usage

From the repo root:

```bash
./.project-workflow/cli/workflow task init --title "Super Admin Access" --update-tracker
```

Create a git branch (requires a clean working tree):

```bash
./.project-workflow/cli/workflow task init --title "Super Admin Access" --update-tracker --create-branch --base-branch develop
```

Customize folder name suffix:

```bash
./.project-workflow/cli/workflow task init --title "Super Admin Access" --folder-suffix Superuser --update-tracker
```

Create and manage proposal-first epics:

```bash
./.project-workflow/cli/workflow epic init --title "Checkout Reliability"
./.project-workflow/cli/workflow epic decompose --epic-id EPIC-001 --limit 5 --type Task
./.project-workflow/cli/workflow epic approve --epic-id EPIC-001 --id TASK-014
./.project-workflow/cli/workflow epic scaffold-child --epic-id EPIC-001 --id TASK-014
```

## Branch naming

Default branch format:

- `feature/<ID>-<kebab-case-title>`

Example:

- `feature/TASK-001-super-admin-access`

## Packaged CLI

This repo also exposes the packaged console script:

```bash
project task init --title "Super Admin Access" --update-tracker
```

The in-repo script is intentionally dependency-free (stdlib only) so initialized projects can keep using the local workflow helper without installing the package.
