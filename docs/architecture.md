# Project Workflow Architecture

This document is the authority for source ownership, internal module boundaries, dependency
direction, and generated-runtime maintenance. The Constitution owns stable product outcomes;
AGENTS.md and .project-workflow/guidance.md own repository operating rules.

## Design Boundary

Project Workflow remains one Python package, one public project command, and one dependency-free
repository-local helper. Modular source is an implementation improvement, not a product split.

The target is twelve or fewer substantial runtime modules plus explicit host adapters. Add a module
only when it owns a distinct reason to change and reduces coupling more than it adds navigation.
Split a module when it mixes material responsibilities or exceeds 5,000 authored lines; do not
split cohesive code solely to satisfy a line count. cli.py is limited to parser/dispatch assembly
and compatibility access and must remain below 2,000 lines after extraction.

## Canonical Modules

| Module | Responsibility | May depend on |
| --- | --- | --- |
| contracts.py | Stable constants, errors, immutable records and operational-status value types | Python standard library |
| repository.py | Managed assets, configuration, manifests, Markdown contracts and low-level repository operations | contracts |
| architecture.py | Proportionate impact classification, source-bound authority and exact-candidate conformance | contracts, repository |
| lifecycle.py | Backlog, Fix, Task and Epic records, approvals, intent, evidence, readiness and proof-layer reads | contracts, repository |
| orchestration.py | Task/Epic work packets, delegation plans, runtime state and reconciliation primitives | contracts, repository, lifecycle |
| execution.py | Capability-aware Task and Epic orchestrators that execute an approved delegation plan | orchestration |
| coordination.py | Durable coordination, verification campaigns, execution control, lifecycle gates, QA/remediation and fixed candidates | contracts, repository, lifecycle, orchestration |
| execution_config.py | Public operator configuration, capability sealing, disable/successor history and model-free execution inspection | contracts, coordination, explicit host adapters |
| inspection.py | Doctor diagnostics plus read-only operational status classification, actions and rendering | contracts, repository, lifecycle, coordination |
| maintenance.py | Upgrade and smoke-bomb transactions that compose repository and inspection services | contracts, repository, inspection |
| commands.py | CLI command handlers that compose domain services without owning product policy | earlier domain modules |
| cli.py | Public entry point, parser assembly, dispatch and documented compatibility facade | contracts, commands, execution_config and parser callbacks |
| adapter_common.py | Pure dependency-free primitives whose semantics are identical on every host | Python standard library |
| codex_adapter.py and claude_adapter.py | Explicit host launch, hook, capability, limit and receipt behaviour | adapter_common |

The implementation may move a function to a neighbouring owner when dependency analysis proves
that responsibility more accurate. It may not introduce a cycle, a domain-to-cli import, wildcard
imports, or an undocumented mixed-responsibility exception.

## Dependency Direction

The table order is the dependency order: a module may import only a module above it, except that
the entry facade may import the command callbacks it assembles. Domain modules never import cli.py.
Commands may compose domains; domains do not import commands. Where code would otherwise need a
two-way policy call, the composing operation belongs to the higher owner instead of hiding the
cycle in a local import.

Architecture tests inspect top-level internal imports, strongly connected components, module line
budgets, generated provenance, and deterministic regeneration.

## Responsibilities

Project Workflow owns proportionate architecture classification, source-bound material decisions,
lifecycle conformance gates, and host-neutral semantic guidance. Each adopting repository owns its
actual structural responsibilities and topology in a repository-local architecture spine.

## Source Ownership

The architecture-control runtime is authored in `src/project_workflow/architecture.py`. Task and
Epic-child templates are composed by their existing repository and lifecycle owners. Host-neutral
Project Architect semantics are authored once under `src/project_workflow/prompts`; host-specific
entrypoints are generated derivatives and never competing truth.

## Shared State Boundaries

The Coordinator remains the only writer of shared workflow state. Project Architect returns a
bounded classification or architecture decision to the Coordinator; it does not update trackers,
approval envelopes, lifecycle, evidence indexes, Git state, or owner-facing decisions.

## Extension Points

Repositories select architecture authority paths and measurable constraints appropriate to their
stack. ADRs may record substantial individual trade-offs, but neither ADRs nor extension-specific
checks replace the architecture spine. New host formats transform the canonical semantic source
rather than introducing another authored architecture contract.

## Measurable Constraints

This repository selects acyclic runtime imports, manifest dependency direction, generated-runtime
parity, canonical source ownership, and existing module budgets as mechanical constraints. Other
repositories must choose constraints that protect their own boundaries; Project Workflow does not
impose universal file-size, module-count, layer, or folder-layout rules.

## Authored And Generated Sources

Canonical authored runtime source lives in the modules listed by scripts/runtime-modules.txt.
scripts/build_runtime_bundle.py concatenates those modules in dependency order, removes package-only
imports, and writes:

- src/project_workflow/templates/workflow.py
- .project-workflow/cli/workflow.py in this source repository

Both outputs carry a generated marker, source-manifest path, and manifest hash. They are never
edited directly. A clean generator run must be idempotent and --check must fail on either stale
copy.

Packaged prompts, skills, host rules and adapters are authored under src/project_workflow. Installed
copies are generated derivatives and must carry ownership markers where their host format permits.
Historical .project-workflow task records are audit state, not current product instructions.

## Compatibility

project_workflow.cli remains the console entry point. It provides parser/dispatch behaviour and a
bounded compatibility facade for names used by the maintained suite or known integrations while
new code imports each owning module directly.

The v0.9.0 command tree, flags, exit semantics, JSON schema versions, manifest/asset/repository
schema values, generated paths, and dependency-free helper behaviour are frozen in the TASK-104
compatibility baseline. Snapshot changes require a product decision; cleanup alone cannot approve
them.

## Validation Order

1. Focused domain tests.
2. Architecture and generated-runtime checks.
3. Ruff check, Ruff format check, and mypy on canonical authored production source.
4. Complete locked pytest.
5. One wheel/sdist build and inventory inspection.
6. Exact-package init/upgrade/no-op journeys and dependency-free local-helper journey.
7. Independent adversarial QA before completion.
