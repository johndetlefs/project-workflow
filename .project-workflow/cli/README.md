# AI Workflow CLI (local)

This folder contains a small helper CLI for the repo’s AI workflow.

Goals:

- Keep workflow scaffolding **out of** `package.json` scripts.
- Keep it **co-located** with the workflow artifacts (`.project-workflow/`), so it’s easy to use and later extract.

## Usage

From the repo root:

```bash
./.project-workflow/cli/workflow task init --id APP-331 --title "Super Admin Access" --update-tracker
```

Create a git branch (requires a clean working tree):

```bash
./.project-workflow/cli/workflow task init --id APP-331 --title "Super Admin Access" --update-tracker --create-branch
```

Customize folder name suffix:

```bash
./.project-workflow/cli/workflow task init --id APP-331 --title "Super Admin Access" --folder-suffix Superuser --update-tracker
```

## Branch naming

Default branch format:

- `feature/<ID>-<kebab-case-title>`

Example:

- `feature/APP-331-super-admin-access`

## uvx (future)

When you move this workflow into its own repo and publish it as a Python package, you can expose the same CLI as a console script entrypoint so teams can run it via `uvx`.

Until then, this in-repo script is intentionally dependency-free (stdlib only).
