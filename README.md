# project-workflow

Project Workflow is a repository-native delivery system for turning owner intent into planned,
implemented, evidenced, reviewed work. Its state is plain Markdown and JSON beside the code, so
people and coding agents can inspect the same requirements, status, decisions, and proof.

It supports GitHub Copilot, Claude Code, OpenAI Codex, and Cursor. It complements issue trackers,
Git hosts, CI, registries, and deployment platforms; it does not replace their authority.

## Quick Start

From the root of an existing Git repository:

```bash
uvx --from project-workflow==0.9.1 project init --agent codex
```

Choose `github-copilot`, `claude-code`, `codex`, or `cursor` to match the agent that will operate
the repository. For an existing installation, use upgrade—not init:

```bash
uvx --from project-workflow==0.9.1 project upgrade --agent codex
```

Then describe the outcome in ordinary language. The installed guidance routes it to the smallest
sufficient record:

| Route | Use it for | Durable record |
| --- | --- | --- |
| Backlog | Optional future intent not ready for execution | `BL-*` row in `BACKLOG.md` |
| Fix | One bounded correction to a delivered or accepted baseline | `FIX-*` folder and global tracker row |
| Task | One new independently reviewable outcome | `TASK-*` requirements and implementation |
| Epic | Coordinated workstreams with shared parent outcomes | `EPIC-*` contract, decomposition, children, audit, and retro |

An in-scope correction stays in its active work item. Completed history is not rewritten to make a
later defect look original.

## See What Is True

Start with the read-only status projection:

```bash
./.project-workflow/cli/workflow status
./.project-workflow/cli/workflow status --id TASK-001
./.project-workflow/cli/workflow status --strict
./.project-workflow/cli/workflow status --format json
```

Status reports sourced lifecycle, proof, blockers, delivery state, and the next safe action. It
does not execute that action. Use Doctor for workflow diagnosis:

```bash
./.project-workflow/cli/workflow doctor
./.project-workflow/cli/workflow doctor --strict
```

Tests, a passing Doctor, `Complete`, merge, release, deployment, adoption, and owner acceptance are
separate evidence layers. Project Workflow reports the strongest layer actually proved.

## How Work Moves

The owner confirms the plain-language Intent and outcome boundary once. The Coordinator then plans,
clarifies, implements, validates, and commissions QA autonomously inside that approved envelope.
Material drift, missing authority, or a changed proof obligation returns to the owner.

The normal Task path is:

```text
Analysing -> Ready -> In Progress -> Testing -> Review -> Complete
```

Epics use the same outcome discipline plus a contract, authoritative decomposition, child tracker,
intent audit, parent acceptance map, closeout audit, and retro. Fixes stay deliberately lighter.

For detailed commands and examples, read [Using Project Workflow](docs/using-project-workflow.md)
or run `./.project-workflow/cli/workflow --help`.

Approved material work can optionally use [Sealed Host Execution](docs/execution-control.md). Codex
uses repository-local skills plus an ephemeral per-run hook; a permanent marketplace-plugin entry
is neither required nor accepted as activation proof.

## What Is Installed

Initialization creates:

- `.project-workflow/` configuration, manifest, backlog, trackers, tasks, guidance, and a
  dependency-free local CLI;
- host-specific agent guidance for the selected mode;
- managed instruction blocks that point the agent at repository-local workflow truth.

Tracked requirements, plans, approvals, evidence, and local guidance remain repository-owned.
Managed helpers and installed host assets are generated derivatives; update their canonical source
or use the supported generator/upgrade path instead of editing copies.

See [Documentation and Source Authority](docs/authority.md) for the complete hierarchy and
[Compatibility](COMPATIBILITY.md) for versioned repository support.

## Contributing

Project Workflow is one Python package, one public `project` command, and one generated
dependency-free helper. Canonical runtime code is split by domain under `src/project_workflow/`;
`src/project_workflow/templates/workflow.py` and `.project-workflow/cli/workflow.py` are generated.

```bash
uv sync --locked --extra dev
uv run --locked ruff check src/project_workflow/*.py scripts tests
uv run --locked ruff format --check src/project_workflow/*.py scripts tests
uv run --locked mypy src/project_workflow/*.py
PATH="/opt/homebrew/bin:$PATH" uv run --locked pytest -q
```

Read [Contributing](docs/contributing.md) before changing source and
[Architecture](docs/architecture.md) before moving responsibilities. Maintainers should also read
[Maintenance](docs/maintenance.md); public release authority is isolated in
[RELEASING.md](RELEASING.md).

## Documentation Map

| Need | Authority |
| --- | --- |
| Product mission and stable outcomes | [Constitution](.project-workflow/CONSTITUTION.md) |
| Repository operating rules | [AGENTS.md](AGENTS.md) and [local guidance](.project-workflow/guidance.md) |
| Orientation and first commands | This README |
| Work-item operation | [Using Project Workflow](docs/using-project-workflow.md) |
| Bounded Codex and Claude Code execution | [Sealed Host Execution](docs/execution-control.md) |
| Source boundaries and generated ownership | [Architecture](docs/architecture.md) |
| Development and validation | [Contributing](docs/contributing.md) |
| Upgrade, hygiene, and generated assets | [Maintenance](docs/maintenance.md) |
| Compatibility policy | [COMPATIBILITY.md](COMPATIBILITY.md) |
| Public release procedure | [RELEASING.md](RELEASING.md) |
| Current command syntax | `project --help` and the [local CLI guide](.project-workflow/cli/README.md) |

Workflow task folders are durable state and audit history, not competing current product
instructions.

## License And Support

Project Workflow is available under the [MIT License](LICENSE). Report defects and proposals through
[GitHub Issues](https://github.com/johndetlefs/project-workflow/issues).
