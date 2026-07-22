# Project Workflow Guidance

Use this file for repo-specific workflow guidance that should survive project-workflow upgrades.

Add local conventions, validation commands, safety constraints, handoff rules, and agent notes here.

## Local Tooling

- This machine has Homebrew `uvx` at `/opt/homebrew/bin/uvx`.
- The Codex app may omit `/opt/homebrew/bin` from `PATH`. Before skipping UVX validation or reporting `uvx` unavailable, check the explicit path and rerun with `PATH="/opt/homebrew/bin:$PATH"`.
- The complete validation command is `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`; the UVX packaging test must pass rather than skip on this machine.

## Delivery Proof

- Distinguish automated fixture coverage from a manual end-to-end product journey. For destructive, export, packaging, or handoff workflows, do not call the user-visible journey proven until a disposable realistic repository or artifact has been created, exercised, independently inspected, and retested.
- Record both proof levels explicitly: automated regression evidence protects breadth and edge cases; the manual journey proves the intended operator experience and resulting artifact.
