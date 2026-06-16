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
- `project init` must never overwrite unmarked existing files. Project-workflow generated files must carry a `project-workflow:generated` marker before init may refresh them in place.
- Host-owned files such as `AGENTS.md` and `.github/copilot-instructions.md` must be created or updated only through the `<!-- project-workflow:start -->` / `<!-- project-workflow:end -->` managed block.
- If a generated target path exists without the generated marker, init must leave it untouched and write the new generated content beside it as `*.new`.
- `project init` must scaffold:
  - `.project-workflow/TRACKER.md`
  - `.project-workflow/guidance.md`
  - `.project-workflow/cli/workflow`
  - `.project-workflow/cli/workflow.py`
  - `.github/prompts/*.prompt.md`
  - a managed block in `AGENTS.md` and generated `.agents/skills/project-*` when Codex mode is selected
  - `.claude/agents/*.md` when Claude Code mode is selected
  - `.cursor/agents/*.md` and `.cursor/rules/project-workflow.mdc` when Cursor mode is selected
- `project task init` must continue scaffolding task docs and optional tracker updates/branch creation.
- Prefer extending behavior with additive flags/options; avoid changing defaults without explicit task scope.

## Prompt/Agent Sync Rules

- If you change any file in `.github/prompts/`, mirror the same change in `src/project_workflow/prompts/`.
- If you add, remove, or rename a workflow step, update all matching assets: packaged prompts, generated Claude/Cursor agent output, Cursor rules, Codex skills, Codex AGENTS template, README, and the `project init` install lists.
- If you add a workflow CLI command, update both the packaged CLI and generated local helper template, document the command in user-facing docs, refresh managed host guidance if agents need to know about it, and add init-refresh coverage that proves older generated helpers receive the new command.
- For agent-facing CLI commands, add or update help smoke coverage so `--help` shows a clear command description and options.
- Keep agent names stable (`name: project.*`) unless explicitly requested.
- README should describe usage via `/project.*` agent commands, not copy/paste prompt workflows.
- Repo-specific workflow customization belongs in `.project-workflow/guidance.md`; generated prompts/skills should reference it rather than asking users to edit generated files by default.

## Constitution Boundary

- `CONSTITUTION.md` is outcome-focused and non-technical.
- Technical constraints, coding conventions, validation rules, and architecture notes for this source repo belong here in `copilot-instructions.md`. Installed repositories should put repo-specific workflow guidance in `.project-workflow/guidance.md`.

## Python Implementation Standards

- Prefer Python stdlib; add third-party dependencies only when clearly justified.
- Preserve existing public function names and argument behavior unless scope requires change.
- Keep code compatible with `requires-python >=3.10`.
- Avoid adding one-off scripts; put reusable behavior in `src/project_workflow/`.

## Validation Expectations

Run the narrowest checks first, then broader checks if needed.

Validation preflight (required for Python/CLI checks in this repo):

- Always run validation commands from the repository virtual environment (`.venv`).
- Prefer explicit binary paths to avoid interpreter drift:
  - `.venv/bin/python`
  - `.venv/bin/pip`
  - `.venv/bin/project`
- Do not rely on system-managed Python/pip for local validation in this repo.
- If `.venv` is missing, create it first, then continue with the sequence below.

Terminal robustness (required for validation/failure-path tests):

- Prefer explicit venv binaries in every command invocation (`.venv/bin/python`, `.venv/bin/project`) rather than relying on shell activation state.
- In initialized repos, run generated workflow commands through Python for consistency:
  - `.venv/bin/python .project-workflow/cli/workflow.py ...`
- Avoid very long chained shell commands for failure-path simulation; use stepwise commands or a short script file.
- When intentionally testing failing scenarios, capture and assert non-zero exit codes explicitly instead of allowing strict shell mode to terminate the terminal process.

Validation command protocol (mandatory):

- Treat these rules as hard constraints, not preferences.
- Run one logical action per terminal command.
- Do not use inline heredocs in long chained commands.
- If multi-line input is required, either:
  - write a short temporary script/file first, then run it in a separate command, or
  - use separate stepwise commands to build the file content.
- Do not combine setup + content-writing + execution + assertions in one command.
- If terminal output appears malformed, interactive, or truncated unexpectedly, stop and re-run using smaller stepwise commands.

Pre-execution checklist for validation commands:

- Confirm command uses explicit repo venv binaries (`.venv/bin/project` or `.venv/bin/python`).
- Confirm command performs exactly one logical step.
- Confirm no chained heredoc pattern is used.
- If any check fails, rewrite the command before execution.

Recommended local validation sequence:

1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -e .`
3. `project --help`
4. `project init` in a temp directory and verify scaffolded files
5. `project doctor` in the initialized temp directory
6. `./.project-workflow/cli/workflow task init --help` (inside initialized temp repo)
7. `./.project-workflow/cli/workflow doctor --help` (inside initialized temp repo)

When behavior changes:

- Validate idempotency by running `project init` twice.
- Validate unmarked existing files are preserved and generated updates are written as `*.new`.

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
2. `/project.task`
3. `/project.requirements`
4. `/project.planner`
5. `/project.clarify`
6. `/project.implement`
7. `/project.qa-review`
8. `/project.retro`

Do not mark work `Complete` from implementation alone. Use `./.project-workflow/cli/workflow task status ...` for tracker lifecycle moves: implementation moves work to `Testing`; QA/code review moves it to `Review` and may complete only after passing review and explicit user approval. Retro runs after completion and updates durable conventions or agent guidance only when there is a reusable lesson.
