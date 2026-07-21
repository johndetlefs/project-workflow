# Project Workflow Guidance

Use this file for repo-specific workflow guidance that should survive project-workflow upgrades.

Add local conventions, validation commands, safety constraints, handoff rules, and agent notes here.

## Local Tooling

- This machine has Homebrew `uvx` at `/opt/homebrew/bin/uvx`.
- The Codex app may omit `/opt/homebrew/bin` from `PATH`. Before skipping UVX validation or reporting `uvx` unavailable, check the explicit path and rerun with `PATH="/opt/homebrew/bin:$PATH"`.
- The complete validation command is `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`; the UVX packaging test must pass rather than skip on this machine.
