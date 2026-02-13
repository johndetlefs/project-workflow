# Copilot Instructions

This file defines **technical implementation guidance** for agents working in this repository.
Product outcomes and mission belong in `.project-workflow/CONSTITUTION.md`.

## Scope

- Apply these instructions to all code and documentation changes in this repo.
- Keep changes minimal and task-focused; avoid unrelated refactors.

## Repository Architecture

- Python package source lives in `src/project_workflow/`.
- Main CLI entrypoint is `src/project_workflow/cli.py`.
- Packaged templates are in `src/project_workflow/templates/`.
- Packaged agent definitions are in `src/project_workflow/prompts/`.
- Dev copies of agent definitions used in this repo are in `.github/prompts/`.

## CLI Contract (Do Not Break)

- Console command is `project` (configured in `pyproject.toml`).
- `project init` must remain idempotent and safe on re-run.
- `project init` must scaffold:
  - `.project-workflow/TRACKER.md`
  - `.project-workflow/cli/workflow`
  - `.project-workflow/cli/workflow.py`
  - `.github/prompts/*.prompt.md`
- `project task init` must continue scaffolding task docs and optional tracker updates/branch creation.
- Prefer extending behavior with additive flags/options; avoid changing defaults without explicit task scope.

## Prompt/Agent Sync Rules

- If you change any file in `.github/prompts/`, mirror the same change in `src/project_workflow/prompts/`.
- Keep agent names stable (`name: project.*`) unless explicitly requested.
- README should describe usage via `/project.*` agent commands, not copy/paste prompt workflows.

## Constitution Boundary

- `CONSTITUTION.md` is outcome-focused and non-technical.
- Technical constraints, coding conventions, validation rules, and architecture notes belong here in `copilot-instructions.md`.

## Python Implementation Standards

- Prefer Python stdlib; add third-party dependencies only when clearly justified.
- Preserve existing public function names and argument behavior unless scope requires change.
- Keep code compatible with `requires-python >=3.10`.
- Avoid adding one-off scripts; put reusable behavior in `src/project_workflow/`.

## Validation Expectations

Run the narrowest checks first, then broader checks if needed.

Recommended local validation sequence:

1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -e .`
3. `project --help`
4. `project init` in a temp directory and verify scaffolded files
5. `./.project-workflow/cli/workflow task init --help` (inside initialized temp repo)

When behavior changes:

- Validate idempotency by running `project init` twice.
- Validate conflict prompts are preserved for user-modified files.

## Git Hygiene

- Never commit runtime artifacts or caches.
- Ensure `.gitignore` excludes: `.venv/`, `__pycache__/`, `*.pyc`, `*.egg-info/`, `build/`, `dist/`.
- If cache artifacts were previously tracked, remove them from git index.

## Documentation Requirements

- Keep `README.md` aligned with actual CLI behavior and agent order.
- Keep examples executable and consistent with current command names.
- Do not document speculative or unimplemented commands.

## Workflow Order (Default)

Use this sequence unless user direction overrides it:

1. `/project.constitution` (once per repo, or when outcomes change)
2. `/project.scaffold`
3. `/project.requirements`
4. `/project.planner`
5. `/project.clarify`
6. `/project.implement`
