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

Move a task through the lifecycle:

```bash
./.project-workflow/cli/workflow task status --id TASK-001 --to "In Progress"
./.project-workflow/cli/workflow task status --id TASK-001 --to Testing
./.project-workflow/cli/workflow task status --id TASK-001 --to Review
./.project-workflow/cli/workflow task status --id TASK-001 --to Complete
```

Illegal non-complete transitions require an audit reason:

```bash
./.project-workflow/cli/workflow task status --id TASK-001 --to Testing --force --reason "Recovering imported tracker state"
```

`Complete` is only allowed from `Review` and requires non-placeholder `## QA & Code Review` evidence.

Create and manage proposal-first epics:

```bash
./.project-workflow/cli/workflow epic init --title "Checkout Reliability"
./.project-workflow/cli/workflow epic decompose --epic-id EPIC-001 --limit 5 --type Task
./.project-workflow/cli/workflow epic approve --epic-id EPIC-001 --id TASK-014
./.project-workflow/cli/workflow epic scaffold-child --epic-id EPIC-001 --id TASK-014
```

Validate workflow state:

```bash
./.project-workflow/cli/workflow doctor
./.project-workflow/cli/workflow validate --strict
```

`doctor` and `validate` are equivalent. Use `--strict` when safety warnings should fail automation.

## Branch naming

Default branch format:

- `feature/<ID>-<kebab-case-title>`

Example:

- `feature/TASK-001-super-admin-access`

## Packaged CLI

This repo also exposes the packaged console script:

```bash
project task init --title "Super Admin Access" --update-tracker
project task status --id TASK-001 --to "In Progress"
project doctor
```

Re-run `project init` from the latest package to refresh marked generated workflow assets and managed host-file blocks. Unmarked existing files are preserved; project-workflow writes the new generated content beside them as `*.new` for review.

The in-repo script is intentionally dependency-free (stdlib only) so initialized projects can keep using the local workflow helper without installing the package.
