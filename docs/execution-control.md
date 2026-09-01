# Sealed Host Execution

Use sealed host execution only for approved material work that needs mechanical scope, limit, and
receipt enforcement. Ordinary planning, status, Doctor, requirements, and cheap deterministic work
stay in the current Coordinator context and launch no subordinate model.

## What Codex Installation Means

A Codex repository installation has two distinct parts:

- repository-local Project Workflow guidance and skills, installed by `project init` or `project
  upgrade`; and
- package-owned execution assets, activated ephemerally only for one sealed `project execute` run.

Project Workflow is deliberately not a permanently active Codex marketplace plugin. `codex plugin
list` is therefore not an installation or health check for this integration. There is no static
Project Workflow hook in the user's global Codex configuration, and repository-local skills are not
duplicated globally. The supervised adapter creates an isolated temporary Codex home, injects its
synchronous hook for the exact run, and removes that temporary runtime afterward.

Package presence, repository skill discovery, successful configuration, hook discovery, one runtime
receipt, release, adoption, and owner acceptance are separate proof layers.

## Operator Journey

Install a new repository or upgrade an existing one through the canonical package:

```bash
uvx --from project-workflow==0.10.0 project init --agent codex
uvx --from project-workflow==0.10.0 project upgrade --agent codex
```

Create current Coordinator state for the approved work item before configuring execution. The
coordinate command records the exact Git source, loaded package/assets/contract, phase, and proof
requirements. `coordinate preflight --id <WORK-ID>` must report a current or compatible contract.

Create an operator configuration such as `execution-config.json`:

```json
{
  "schema_version": 1,
  "host": "codex",
  "executable": "/absolute/path/to/codex",
  "trust": "trusted-local",
  "model": "gpt-5.6-luna",
  "prompt": "Create src/canary.txt with the exact approved content.\n",
  "allowed_write_paths": ["src/canary.txt"],
  "permitted_operations": ["material-execution"],
  "proof_obligations": ["exact-canary-content", "sealed-write-scope"],
  "limits": {
    "elapsed-seconds": {"maximum": 180, "native_unit": "seconds"},
    "agent-budget": {"maximum": 10000, "native_unit": "tokens"},
    "turns": {"maximum": 1, "native_unit": "turns"},
    "tool-calls": {"maximum": 4, "native_unit": "tool-calls"},
    "test-invocations": {"maximum": 1, "native_unit": "test-invocations"},
    "identical-retries": {"maximum": 1, "native_unit": "identical-retries"},
    "worker-launches": {"maximum": 1, "native_unit": "worker-launches"},
    "changed-paths": {"maximum": 1, "native_unit": "changed-paths"},
    "write-scope": {"maximum": 1, "native_unit": "write-scope"}
  },
  "allowed_tools": ["apply_patch"],
  "allowed_command_patterns": [],
  "test_command_patterns": [],
  "required_changed_paths": ["src/canary.txt"]
}
```

Every limit is explicit and host-native. Project Workflow does not supply a universal budget. The
configuration file contains operator policy, not an internal `COORDINATION.json` payload: the CLI
observes and hashes the exact executable/version, probes the supported non-model host contract,
constructs the generic capability mapping, computes the sealed identity, and writes state through
the Coordinator-owned writer. When coordination declares material verification, the core—not the
operator—prepends the current proof-contract identity and every durable verification claim to the
sealed proof obligations. Reserved `verification-contract:` and `verification-claim:` entries are
therefore rejected in operator configuration. The active control cannot validate if those derived
obligations are missing.

Configure, inspect, and execute:

```bash
./.project-workflow/cli/workflow execution configure \
  --id <WORK-ID> --config execution-config.json
./.project-workflow/cli/workflow execution status --id <WORK-ID>
./.project-workflow/cli/workflow execute --id <WORK-ID>
```

`execution configure` and `execution status` make zero model calls. Configuration rerun against the
same sealed inputs is a byte-preserving no-op. An unsupported capability is retained truthfully and
returns a non-zero exit; it is not promoted to verified. `project execute` re-probes the exact
runtime contract and then dispatches only when every binding control is verified.

Disable receipt-free or completed authority with:

```bash
./.project-workflow/cli/workflow execution disable --id <WORK-ID>
```

Disable and reconfiguration create successor envelopes. Previous controls and receipts remain in
`execution_control_history`; the active control never rewrites its own authority or erases completed
evidence. Re-enable by running `execution configure` again with the reviewed configuration.

Coordinator-owned `COORDINATION.json` changes are excluded from the adapter's product-source Git
diff because configuration and receipt persistence necessarily update that state around a run. The
operator configuration may never grant the worker write authority over any such file; all other
tracked and untracked product paths remain subject to the clean-source and sealed-scope checks.

## Claude Code Adapter Status

Project Workflow 0.10.0 does not claim Claude Code runtime certification. The adapter and managed
assets are packaged so the host-neutral boundary stays inspectable, but the current release has no
real authenticated Claude Code canary. Material execution must therefore fail closed unless a later
candidate proves the exact executable, authentication, hook activation, permissions, native limits,
required outputs, interruption, and core receipt. Passing Codex evidence is not Claude evidence.

For future Claude certification, use the following distinct native configuration rather than
translating Codex units:

Use `"host": "claude-code"`, an absolute executable ending in `claude`, and
`"agent-budget"` native unit `"usd-micros"`. Claude configuration may also contain:

- `disallowed_tools`;
- `required_output_identities`, mapping repository-relative paths to SHA-256 identities; and
- `required_validation_commands`, each also present as an exact literal
  `allowed_command_patterns` entry.

Configuration probes exact version and authentication without making a model request. Actual hook
activation, native permission containment, streaming, cost/turn accounting, required outputs, and
interruption remain unproved until a real dispatch returns its input-bound receipt.

## Failure And Proof Boundaries

- Missing coordination, stale source, a changed executable, invalid native units, unsupported host
  controls, exhausted limits, scope drift, absent hooks, and malformed runtime events fail closed.
- A blocked or interrupted receipt preserves unmet proof; it never manufactures completion.
- A successful host run proves only the exact source, configuration, executable, prompt, limits,
  paths, and observations named by that receipt.
- Merge, package publication, repository upgrade, portfolio adoption, and owner acceptance still
  require their own evidence and authority.

Use `project status --id <WORK-ID>` for the combined workflow projection and `project doctor
--strict` for structural diagnosis. Neither command launches the configured host.
