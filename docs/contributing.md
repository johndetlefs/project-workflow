# Contributing

Project Workflow is maintained as one package with explicit domain owners and one generated
dependency-free runtime. Read `docs/architecture.md` before moving functions or adding modules.

## Environment

Use Python 3.10 and the locked development extra:

```bash
uv sync --locked --extra dev --python 3.10
```

On this repository's macOS environment, Homebrew `uvx` is at `/opt/homebrew/bin/uvx`; include
`/opt/homebrew/bin` in `PATH` before diagnosing UVX tests as unavailable.

## Normal Change Path

1. Identify the owning module and focused test suite.
2. Change canonical authored source only.
3. Run the focused tests.
4. If a runtime module changed, regenerate the standalone bundle.
5. Run locked static gates and the complete suite.
6. Build one wheel/sdist candidate and exercise that exact wheel when package behaviour is affected.
7. Run adversarial QA and preserve the actual delivery boundary.

Generated runtime command:

```bash
uv run --locked python scripts/build_runtime_bundle.py --write
uv run --locked python scripts/build_runtime_bundle.py --check
```

Never edit `src/project_workflow/templates/workflow.py` or
`.project-workflow/cli/workflow.py` directly. Adapter copies under `.project-workflow/cli/` must
remain byte-identical to their package sources.

## Required Quality Gates

Local guidance and CI use the same commands:

```bash
uv run --locked ruff check src/project_workflow/*.py scripts tests
uv run --locked ruff format --check src/project_workflow/*.py scripts tests
uv run --locked mypy src/project_workflow/*.py
PATH="/opt/homebrew/bin:$PATH" uv run --locked pytest -q
```

Ruff covers authored source, scripts, and tests. Mypy covers canonical production modules. Generated
runtime copies are checked through deterministic parity rather than counted as a second authored
codebase.

## Structural Rules

- Domain modules never import `cli.py` or `commands.py`.
- Dependencies follow `scripts/runtime-modules.txt`; cycles fail the architecture gate.
- Add a module only for a distinct reason to change, not to reduce a number.
- Keep cohesive domain modules below 5,000 authored lines and `cli.py` below 2,000.
- Keep maintained test files below 2,000 lines and shared test support narrow and explicit.
- Keep host-specific adapter semantics in their host modules; share only identical primitives.
- Treat public command, schema, path, and exit changes as product compatibility decisions.

## Documentation

Use `docs/authority.md` to choose the owning document. Keep README as orientation, not a second
manual. Keep release instructions in `RELEASING.md`, compatibility policy in `COMPATIBILITY.md`, and
implementation architecture here or in `docs/architecture.md`. Historical task evidence is not
current guidance.

Run the documentation check after changing current docs:

```bash
uv run --locked python scripts/check_documentation.py
```

## Proof And Delivery

Match proof to the claim. Unit tests do not prove a built package, package proof does not prove a
hosted service, and local source does not prove merge or release. Do not push, merge, tag, publish,
deploy, or adopt merely because repository validation passes.
