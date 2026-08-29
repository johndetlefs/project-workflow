# Project Workflow Guidance

Use this file for repo-specific workflow guidance that should survive project-workflow upgrades.

Add local conventions, validation commands, safety constraints, handoff rules, and agent notes here.

## Local Tooling

- This machine has Homebrew `uvx` at `/opt/homebrew/bin/uvx`.
- The Codex app may omit `/opt/homebrew/bin` from `PATH`. Before skipping UVX validation or reporting `uvx` unavailable, check the explicit path and rerun with `PATH="/opt/homebrew/bin:$PATH"`.
- The complete validation command is `PATH="/opt/homebrew/bin:$PATH" uv run --locked pytest -q`; the UVX packaging test must pass rather than skip on this machine.

## Contributor Quality Gates

- Install the locked development environment with `uv sync --locked --extra dev`.
- Run `uv run --locked ruff check src/project_workflow/*.py scripts tests`.
- Run `uv run --locked ruff format --check src/project_workflow/*.py scripts tests`.
- Run `uv run --locked mypy src/project_workflow/*.py`.
- Run `uv run --locked python scripts/check_documentation.py`.
- Run `PATH="/opt/homebrew/bin:$PATH" uv run --locked pytest -q` for the complete regression gate.
- Regenerate bundled runtimes only with `uv run --locked python scripts/build_runtime_bundle.py --write`, then require the same command with `--check` before delivery.

## Delivery Proof

- Distinguish automated fixture coverage from a manual end-to-end product journey. For destructive, export, packaging, or handoff workflows, do not call the user-visible journey proven until a disposable realistic repository or artifact has been created, exercised, independently inspected, and retested.
- Record both proof levels explicitly: automated regression evidence protects breadth and edge cases; the manual journey proves the intended operator experience and resulting artifact.
- For Markdown parsers and generated scaffolds, assert complete logical content rather than only headings or first physical lines. Include wrapped-item, section-boundary, and delivered-legacy integrity coverage when silent truncation could remove workflow authority.
- For release candidates, retain the exact wheel and source distribution used by journey evidence, bind every shipped or manifest-covered source rather than sampling selected files, and keep publication or adoption as a separate proof gate.
- A dogfood narrative is context, not outcome proof. Bind the actual owner observation, meaning-first approval output, current workflow artifacts and independent blocking reviews in a mechanically regenerable packet; preserve each Changes-requested report instead of overwriting the evidence that caused remediation.

## Release Adoption

- For a multi-project Project Workflow rollout, inventory the current Codex project set first and retain a disposition for every entry. Apply the public exact-version package only to clean, unambiguous canonical authority roots using a reviewed plan fingerprint; keep dirty or active roots unchanged with their exact blocker.
- Validate adoption separately from repository health: a no-op second upgrade plan proves the installation is current, while Doctor findings prove workflow-state health. Preserve and report pre-existing owner-owned Doctor debt instead of attributing it to the managed upgrade or silently widening release scope.
