# FIX-010 Disposition

## Source

- Prototype commit: `bd78627b47c90c492cbf844231c92e4843786f94`
- Prototype branch: `codex/enforced-execution-envelope`
- Authority: EPIC-018 approved Intent and TASK-101 inherited child charter
- Rule: useful mechanisms may be refactored into the subordinate Codex adapter; prototype product,
  lifecycle, release, public CLI, and constant-budget authority are retired or replaced.

## File Map

| Prototype file | Disposition | EPIC-018 destination or reason |
| --- | --- | --- |
| `.codex/config.toml` | Retire | The repository-wide 80,000-token backstop is not proportionate sealed authority and is not shipped. |
| `.project-workflow/TRACKER.md` | Replace | EPIC-018 and its child tracker rows own current lifecycle state; FIX-010 is not revived. |
| `.project-workflow/cli/workflow.py` | Replace | The managed CLI exposes host-neutral `project execute` and `project release`; it does not expose `project-enforce`. |
| `.project-workflow/guidance.md` | Replace | Current guidance describes host-neutral controlled execution and separates runtime, package, delivery, and adoption proof. |
| `.project-workflow/tasks/FIX-010-Enforce-Execution-Envelope/FIX.md` | Adopt as provenance only | The report and canary evidence explain the recurrence and prototype limits; they are not current workflow truth. |
| `AGENTS.md` | Replace | Current managed guidance routes through Coordinator-owned control without a Codex-only public command. |
| `CHANGELOG.md` | Replace | EPIC-018 changes are described as host-neutral core plus subordinate adapters, not as delivered FIX-010. |
| `README.md` | Replace | Public documentation uses Project Workflow execution control and proof boundaries. |
| `pyproject.toml` | Refactor | Package data retains only the subordinate adapter/plugin assets; the prototype console entry point is retired. |
| `scripts/release_contract.py` | Replace | TASK-100's fixed release controller owns release execution and terminal receipts. |
| `src/project_workflow/cli.py` | Replace | Host-neutral control, QA campaign, candidate promotion, fixed release, and adapter dispatch live in the core CLI. |
| `src/project_workflow/codex/AGENTS.md` | Replace | Codex guidance may describe supported routing but cannot create authority or claim universal enforcement. |
| `src/project_workflow/codex_plugin/project-workflow-enforcement/.codex-plugin/plugin.json` | Retire | The static universal-enforcement product claim is removed. |
| `src/project_workflow/codex_plugin/project-workflow-enforcement/hooks/hooks.json` | Refactor | Synchronous SessionStart/PreToolUse/PostToolUse configuration is injected for one supervised sealed App Server turn only. |
| `src/project_workflow/codex_plugin/project-workflow-enforcement/scripts/enforce-hook` | Refactor | The packaged subordinate handler calls `project_workflow.codex_adapter hook`; it is inert without sealed runtime state. |
| `src/project_workflow/enforcement.py` | Refactor and split | Atomic counters, path checks, App Server supervision, interruption, and receipts move to `codex_adapter.py`; core release and candidate authority stay in the host-neutral CLI. |
| `src/project_workflow/templates/workflow.py` | Replace | The managed template mirrors the host-neutral core CLI exactly. |
| `tests/test_execution_envelope.py` | Refactor | Deterministic adapter, hook, capability, dispatch, source/scope, and receipt tests retain the useful adversarial cases. |
| `tests/test_release_contract.py` | Replace | TASK-100 tests prove the fixed release contract; Codex adapter tests do not own release semantics. |

## Behavior Map

| Prototype behavior | Disposition | Current meaning |
| --- | --- | --- |
| Immutable execution input | Adopt | The host-neutral sealed control is the adapter's only authority input. |
| SQLite atomic counters and sticky denial | Refactor | Adapter-local state reserves aggregate tool, test, retry, worker, and path authority and cannot create workflow truth. |
| SessionStart, PreToolUse, and PostToolUse hooks | Refactor | Runtime-injected synchronous hooks must activate during the exact supervised turn or support fails closed. |
| App Server initialize/thread/turn lifecycle | Refactor | The Codex adapter supervises one ephemeral local turn and translates native events into a core receipt. |
| Token and elapsed interruption | Refactor | Finite values come from the sealed control; Codex token usage is never normalized into another host's unit. |
| Command, patch, traversal, move, and Git-scope checks | Adopt and harden | Pre-action inspection and post-action Git closeout jointly enforce repository-relative allowed paths. |
| Clean-source and fixed source identity | Adopt | Material execution starts from the exact sealed Git revision and fails on source drift. |
| Isolated Codex home and auth forwarding | Refactor | The supervised process receives only an ephemeral runtime home plus existing local authentication. |
| Public `project-enforce` command | Retire | `project execute --id` is the only public material adapter dispatch surface. |
| Codex-owned envelope schema and receipt | Replace | Core Project Workflow owns schemas, candidates, proof obligations, receipts, and persistence. |
| Standalone fixed-candidate release executor | Replace | TASK-100's host-neutral fixed release controller owns predeclared operations and terminal receipts. |
| Automatic QA, source repair, or replacement candidate | Retire | The adapter has no such authority; bounded QA remediation is core state owned by TASK-100. |
| Repository-wide native 80,000-token budget | Retire | Every material budget is explicit, finite, sealed, host-native, and work-specific. |
| Static plugin activation as support proof | Retire | Package presence is distinct from trusted runtime capability and a real hook-active canary. |
| Local Codex canary pattern | Adopt with new proof | TASK-101 runs one current supported App Server journey; TASK-103 owns dual-host conformance and delivery proof. |
| Hosted, untrusted, disabled-hook, or managed-policy coverage | Explicitly unsupported | Capability/status remains blocked and does not advertise support. |

## Forbidden Retentions

Source and built package scans must find none of these as active architecture:

- a `project-enforce` console entry point or public command;
- `limit_tokens = 80000` or another repository-wide constant presented as proportionate control;
- the `project-workflow-enforcement` plugin name;
- a Codex adapter that writes QA, candidate, lifecycle, or release state independently;
- a static hook configuration presented as proof of active supported control.

References in this disposition record are historical evidence and are not shipped runtime assets.
