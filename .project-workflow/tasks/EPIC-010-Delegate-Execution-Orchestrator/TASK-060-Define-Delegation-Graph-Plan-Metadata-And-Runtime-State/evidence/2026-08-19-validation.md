# TASK-060 Validation Evidence

- Date: 2026-08-19
- Source base: `53769e89c3c2b8fd1df4e960c745ad9a75291255`
- Branch: `codex/TASK-060-delegation-graph`
- Delivery boundary: local implementation and QA only; no push, PR, merge, release, deployment, external contact, or other repository mutation.

## Automated validation

- `.venv/bin/pytest -q tests/test_delegation.py` — 19 passed.
- `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q` — 281 passed in 45.86 seconds.
- `PATH="/opt/homebrew/bin:$PATH" ./.project-workflow/cli/workflow doctor --strict` — no issues; 69 accepted warnings hidden.
- `.venv/bin/python -m compileall -q src/project_workflow .project-workflow/cli/workflow.py` — passed.
- `PATH="/opt/homebrew/bin:$PATH" .venv/bin/python -m build` — sdist and wheel built successfully.
- `PATH="/opt/homebrew/bin:$PATH" uvx --from ./dist/project_workflow-0.3.0-py3-none-any.whl project delegate --help` — installed wheel exposed `plan`, `status`, `state-init`, and `state-reconcile`.
- `git diff --check` — passed.

## Contract and privacy inspection

- `src/project_workflow/cli.py`, `src/project_workflow/templates/workflow.py`, and `.project-workflow/cli/workflow.py` were byte-identical at SHA-256 `37f860398aeea7344fdcfb0ce8da830f905930e7c9749882c6f3418cfd05f926`.
- The wheel copies of `project_workflow/cli.py` and `project_workflow/templates/workflow.py` matched the same SHA-256.
- Wheel and sdist listings contained no `.project-workflow` or `runtime/delegations` state artifacts.
- `git ls-files .project-workflow/runtime/delegations` returned no tracked files.
- `git check-ignore -v .project-workflow/runtime/delegations/probe.json` resolved to the managed `.gitignore` entry.
- Runtime payload loading and host observations are allowlisted; transcript/credential-like fields and unsafe symlinked runtime directories are rejected by focused tests.

## Read-only current-task projection

- `./.project-workflow/cli/workflow delegate plan --id TASK-060 --requested-concurrency 3 --available-child-capacity 0 --format json` resolved the exact approved child target, ordered rows 1-5, reported only row 5 eligible during validation, bounded child concurrency at 0, and explained coordinator sequential fallback.
- `./.project-workflow/cli/workflow delegate status --id TASK-060` reported runtime state as not initialized and did not mutate tracked files.

## Proof boundaries

- This evidence proves code-level behavior, artifact parity, package contents, host-neutral reconciliation, and read-only projection.
- It does not claim a live Codex task/subagent launch, host interruption/resume, cross-worktree host recovery, host adapter parity, parent acceptance, integration, release, deployment, adoption, effectiveness, or owner acceptance.
