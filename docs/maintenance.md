# Maintenance

This guide owns repository initialization, upgrades, generated assets, compatibility hygiene, and
local cleanup. Public publication belongs only in `RELEASING.md`.

## Initialize Or Upgrade

Initialize only a repository with no Project Workflow installation:

```bash
uvx --from project-workflow==0.10.0 project init --agent codex
```

Upgrade an existing installation directly; do not run init first:

```bash
uvx --from project-workflow==0.10.0 project upgrade --agent codex
```

Canonical UVX upgrade combines managed-asset refresh and declared repository-schema migrations in
one reviewed transaction. It preserves unmarked collisions, user configuration, guidance, workflow
records, evidence, and history. For automation, review a non-mutating plan and apply its exact
fingerprint with the same package version.

Run normal upgrade from a clean Git worktree. The human command asks for confirmation; an authorized
non-interactive agent adds `--yes`:

```bash
uvx --from project-workflow==0.10.0 project upgrade --agent codex --yes
```

For automation, separate the immutable plan from fingerprint-bound apply:

```bash
uvx --from project-workflow==0.10.0 \
  project upgrade --agent codex --plan --format json

uvx --from project-workflow==0.10.0 \
  project upgrade --agent codex \
  --apply --plan-fingerprint sha256:<REVIEWED_PLAN_FINGERPRINT>
```

The plan includes managed helper/agent-asset changes and every ordered repository migration. Apply
rechecks inputs and applies the confirmed plan as one transaction. Doctor is not a prerequisite.

| Detected state | Result |
| --- | --- |
| Not initialized | Block and direct the caller to init. |
| Current | Refresh changed assets or report a no-op. |
| Pre-versioned legacy | Apply `PW-0001-legacy-manifest` with the asset refresh. |
| Assets or schema behind | Apply every required ordered change together. |
| Invalid or unsupported future manifest | Block without mutation. |

The legacy migration recognizes a pre-versioned repository shape without rewriting repository-owned
history. See `COMPATIBILITY.md` for support and breaking-release policy.

Doctor diagnoses without mutation. Status projects truth and a next action. Neither substitutes for
upgrade, lifecycle gates, QA, Git integration, release, or service verification.

## Generated Assets

Canonical sources live under `src/project_workflow/`. The runtime generator reads
`scripts/runtime-modules.txt` and writes the packaged template plus source-repository local mirror.
Init and upgrade install host guidance, prompts, skills, rules, plugins, launchers, and adapter copies.

Rules:

- edit canonical source, never a generated runtime;
- regenerate deterministically and require `--check`;
- preserve user-owned or unmarked collisions and review generated `*.new` files;
- keep installed adapter files byte-identical to package source;
- bump asset or repository schema only for a real managed-contract change.

## Compatibility

Package, asset, and repository-schema versions are separate. The manifest records installed
contract identity; configuration and workflow history remain repository-owned. Read
`COMPATIBILITY.md` for supported states, migrations, and removal policy.

The release source gate checks version mirrors, generated runtime parity, manifest/changelog
identity, immutable installation guidance, required package files, and release semantics.

## Repository Hygiene

Before cleanup or worktree retirement, inspect:

- repository root, branch, base, remote relationship, and dirty state;
- untracked and ignored paths;
- unique commits, unpushed work, active tasks, pull requests, and evidence dependencies;
- whether a generated or binary artifact carries a claim not preserved elsewhere.

Ignored caches and build output are disposable only after no active process or retained candidate
needs them. Historical workflow records, accepted Doctor warnings, and blocked work are evidence, not
debris. A worktree may be removed only after its unique changes and ongoing task need are disproved.
Do not delete remote branches as part of local hygiene.

## Smoke Bomb Client Handoffs

Use canonical `project smoke-bomb` from a clean dedicated worktree. Review the exact plan,
validation commands, exclusions, client-agent guidance, inventory, and fingerprint before apply.
The resulting ZIP excludes Git and workflow internals while retaining useful client documentation.
Export proof does not authorize sending the archive.

## Routine Maintainer Checks

```bash
uv lock --check
uv run --locked python scripts/build_runtime_bundle.py --check
uv run --locked python scripts/check_documentation.py
./.project-workflow/cli/workflow doctor --strict
```

Then run the static and regression commands in `docs/contributing.md`. Use `RELEASING.md` only when
a specific reviewed candidate has separate merge and publication authority.
