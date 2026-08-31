# Using Project Workflow

Use this guide for the normal owner-to-delivery journey. Current option syntax remains authoritative
in `./.project-workflow/cli/workflow --help`. Initialization, upgrade, and generated-asset ownership
belong in [Maintenance](maintenance.md).

## Start With Status

```bash
./.project-workflow/cli/workflow status
./.project-workflow/cli/workflow status --id <WORK-ID>
./.project-workflow/cli/workflow status --strict
./.project-workflow/cli/workflow status --format json
./.project-workflow/cli/workflow doctor --format json
```

Status is read-only. It combines manifest, Git, workflow records, proof, Doctor, and delivery
receipts into one sourced next action. It neither fixes state nor authorizes mutation.

## Choose The Smallest Sufficient Route

- Backlog preserves optional future intent.
- Fix corrects one bounded delivered or accepted baseline.
- Task delivers one independently reviewable new outcome.
- Epic coordinates several workstreams against shared parent outcomes.

The label in a request is evidence, not authority to force the wrong route. Keep a correction inside
active approved work when it remains in scope; preserve completed history and link later work.

## Backlog

```bash
./.project-workflow/cli/workflow backlog add \
  --title "Account export" --type Feature --priority Medium
./.project-workflow/cli/workflow backlog list
./.project-workflow/cli/workflow backlog validate
```

Promoted rows remain in the backlog as provenance. Active status belongs in trackers and work-item
documents.

## Task

```bash
./.project-workflow/cli/workflow task init --title "Account export"
./.project-workflow/cli/workflow task approval-summary --id TASK-001
./.project-workflow/cli/workflow task approve-requirements \
  --id TASK-001 --approved-by "Product Owner" --source "Owner confirmed the Intent"
./.project-workflow/cli/workflow task ready --id TASK-001
```

The Coordinator drafts a brief Intent, outcome commitments, requirements, plan, implementation rows,
and proof obligations. The owner confirms meaning before planning. Inside that unchanged envelope,
the Coordinator advances through Ready, implementation, Testing, Review, and Complete without
repeated approval prompts.

Use `task adopt` for pre-existing work. Inferred pre-adoption evidence remains untrusted until it is
refreshed.

## Fix

```bash
./.project-workflow/cli/workflow fix init --title "Export fails for large accounts"
./.project-workflow/cli/workflow fix triage --id FIX-001
./.project-workflow/cli/workflow fix status --id FIX-001 --to "In Progress"
```

A Fix uses one `FIX.md`, the shared tasks directory, and the global tracker. Triage chooses Defect,
Regression, Change Request, or Incident and records the baseline, impact, risk, and validation. If
investigation reveals a new outcome or several independent changes, promote it rather than stretching
the bounded record.

## Epic

```bash
./.project-workflow/cli/workflow epic init --title "Checkout reliability"
./.project-workflow/cli/workflow epic lifecycle --epic-id EPIC-001 --to Analysing
./.project-workflow/cli/workflow epic approval-summary --epic-id EPIC-001
./.project-workflow/cli/workflow epic approve-requirements \
  --epic-id EPIC-001 --approved-by "Product Owner" \
  --source "Owner confirmed the Epic Intent and boundary"
./.project-workflow/cli/workflow epic decompose --epic-id EPIC-001 --limit 5 --type Task
```

`EPIC-CONTRACT.md` owns sources, invariants, artifact targets, invalid substitutes, and proof owners.
`DECOMPOSITION.md` authorizes child IDs, titles, and parent-AC coverage. Matching children may be
approved and scaffolded inside the approved envelope:

```bash
./.project-workflow/cli/workflow epic approve --epic-id EPIC-001 --id TASK-014
./.project-workflow/cli/workflow epic scaffold-child --epic-id EPIC-001 --id TASK-014
./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-001 --id TASK-014
./.project-workflow/cli/workflow epic intent-audit --epic-id EPIC-001
```

The intent audit fails closed on omitted, narrowed, substituted, or broadened commitments. Use
`epic amend` only for a current owner-approved capability change outside decomposition authority.
Closeout requires parent acceptance evidence, deferral decisions, QA, and retro.

## Evidence And QA

Acceptance criteria state what must be true. Validation names how it will be checked. Evidence records
what actually happened against the relevant source and target.

Structured proof is required for triggered visual/reference, external-contract, deployed-artifact,
runtime-target/source, and responsive/multi-context claims. Tests, builds, prose, and surrogate
artifacts cannot replace the exact required target.

Implementation validation precedes QA. QA is one adversarial gate, not a recursive review loop. A
later source change invalidates only affected proof; ambiguous impact expands before completion.

For material work that requires mechanically sealed host scope, limits, interruption, and receipts,
use the separate [Sealed Host Execution](execution-control.md) operator journey. Repository-local
skills remain the normal Codex integration; execution hooks are activated only for the exact sealed
dispatch.

## Delegate Approved Work By Need

Delegate coordinates existing approved rows; it does not create another owner-facing role. A Task
delegates implementation rows and an Epic delegates approved child Tasks. Task-versus-Epic kind
does not choose the executor surface. Choose the lightest current-host surface whose verified
capabilities satisfy the row's execution needs:

- `bounded-return` can return through the current Coordinator session;
- `durable-resume` requires cross-session recovery;
- `direct-owner-steering` requires a visible child the owner can steer;
- `isolated-worktree` requires real filesystem isolation;
- `peer:<group-id>` requires workers in that group to communicate directly.

The available surfaces are `coordinator`, `subagent`, `persistent-task`, and `peer-team`. Capability
is runtime-observed `verified`, `unsupported`, or `unknown`; only verified current-host capability
authorizes native launch. A non-Coordinator surface also needs an explicit benefit, overhead, and
tradeoff rationale. Capacity alone is not a benefit.

Positive examples:

- Independent bounded rows with disjoint scopes may use a `subagent` when current capacity is
  verified.
- A row that must survive interruption and needs direct owner steering may use an authorized
  `persistent-task`.
- Workers that genuinely need to negotiate may use `peer-team` with a matching `peer:<group-id>`.
- Coupled changes to the same files remain Coordinator-owned and sequential.

Negative examples:

- Parallel-safe work alone does not justify a peer team.
- Epic approval does not authorize a visible task without current owner authority.
- Shared-filesystem execution cannot substitute when isolation is binding.
- A tidy sidebar does not authorize retiring active or unresolved work.

The Coordinator alone writes shared workflow state and verifies every bounded return. Temporary
visible children use retirement-on-verified; Codex maps this to reversible `archive-on-verified`.
Never retire the Coordinator. Active, failed, blocked, unintegrated, owner-promoted, or otherwise
attention-bearing work stays visible. Generated asset parity proves contract alignment, not
runtime-validated host support.

## Workspaces

Workspace mode keeps the only live workflow state in a parent authority repository while registered
independent repositories retain their own Git and delivery evidence. Run workflow commands from the
authority root and use repository IDs in scope and evidence. Status may inspect registered Git state
read-only; it never authorizes cross-repository mutation.

## Completion And Delivery

`Complete` means the work item's repository-level implementation and QA gates passed. It does not
mean merged, released, deployed, adopted, owner-accepted, or commercially validated. Record each
later state from its authoritative system and stop at the strongest proved claim.
