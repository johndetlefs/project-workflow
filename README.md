# project-workflow

Project-workflow turns a conversation about what should change into a reviewable delivery record that lives beside the code.

It gives project owners clear decision points and gives coding agents a dependable way to move from intent to requirements, implementation, evidence, QA, and closeout. The workflow stays in Markdown and Git, so there is no separate dashboard to maintain and no hidden agent state to trust.

Use it with GitHub Copilot, Claude Code, OpenAI Codex, or Cursor.

## Quick Start

From the root of an existing Git repository:

```bash
uvx --from project-workflow==0.8.0 project init --agent codex
```

Choose the mode that matches your agent:

```bash
uvx --from project-workflow==0.8.0 project init --agent github-copilot
uvx --from project-workflow==0.8.0 project init --agent claude-code
uvx --from project-workflow==0.8.0 project init --agent codex
uvx --from project-workflow==0.8.0 project init --agent cursor
```

Then tell the agent what you want in ordinary language:

> Add a backlog item for account export.

> Create a task for the approved account export feature. I want to review the requirements before implementation.

> The completed export flow now fails for large accounts. Treat this as a bounded fix.

The initialized agent instructions and skills tell the agent how to create the right artifacts, use the local workflow CLI, preserve approval history, and validate state.

## What You Get

- A repository-native backlog for ideas worth preserving but not yet active.
- Lightweight Fix records for bounded corrections after work has been delivered.
- Brief plain-language Intent, stable outcome commitments, and detailed requirements/implementation
  records that remain subordinate to what the owner actually wants.
- One visible global tracker for active standalone work and epics, with child trackers inside epics.
- Explicit owner authority without repeated approval prompts inside an unchanged scope.
- Evidence and QA gates that make completion mean more than "the code was written."
- Proposal-first epics for coordinated work that needs decomposition and closeout.
- Agent guidance that can be refreshed without replacing your repository-owned instructions.
- Versioned repository upgrades with one-command confirmation, optional non-mutating plans, stale-plan rejection, and rollback.

Project-workflow is not a replacement for Jira, Linear, or another planning system. It is the execution layer beside the code: the place where agents can reliably read the agreed outcome, current status, proof obligations, and next action.

## See Operational Status And The Next Action

Run status when arriving at a repository or deciding what to do next:

```bash
./.project-workflow/cli/workflow status
./.project-workflow/cli/workflow status --id TASK-001
./.project-workflow/cli/workflow status --repository next
./.project-workflow/cli/workflow status --strict
./.project-workflow/cli/workflow status --format json
```

Status is a read-only projection over the manifest, Git, trackers, requirements, implementation and QA records, Epic acceptance, structured evidence, Doctor findings, and repository-local delivery receipts. It reports one sourced primary action plus stable secondary actions. `--id <WORK-ID>` focuses active work; `--repository <ID>` focuses one registered workspace repository; `--strict` makes visible Doctor warnings blocking; `--format json` emits schema version 1 with the same conclusions as the human report.

Use the related commands for their narrower jobs:

- `project status` explains current operational truth and the next safe action; it never runs that action.
- `project doctor` diagnoses workflow structure and compatibility. Use `--show-accepted` to audit hidden historical warnings.
- `project upgrade` applies managed-asset and repository-schema changes after review; status only recommends it when appropriate.
- task, Fix, and Epic lifecycle commands perform transitions and enforce their existing gates.
- QA/review records acceptance evidence; a passing Doctor result does not prove implementation or delivery.
- Git, release, publication, and deployment remain separate stages. A `Complete` row, clean branch, tag, URL, test, or prose statement cannot substitute for the source required by a later stage.

When the repository cannot prove a claim, status says `unknown` or `not-recorded`. It does not make live service calls, accept warnings, approve requirements, repair files, merge branches, publish releases, or verify deployments.

## How Collaboration Works

Project-workflow is human-directed and agent-operated.

The owner provides:

- the problem or opportunity;
- the desired outcome and affected user or system;
- boundaries, non-goals, constraints, priority, and relevant examples;
- the signal that would make the work acceptable;
- decisions where product authority is required;
- one explicit confirmation that the plain-language Intent and success meaning are accurate before
  planning; identifiers and hashes remain internal provenance.

The agent:

- inspects the repository and existing workflow state;
- remains the single owner-facing Coordinator from intake through delivery, while treating
  delegation as an internal execution choice;
- recommends Backlog, Fix, Task, or Epic from the actual scope;
- drafts and maintains the Markdown artifacts;
- surfaces unresolved product decisions instead of guessing;
- runs Planner and the bounded post-plan Clarify pass after approval;
- validates readiness and advances work inside the approved envelope;
- implements, validates, records evidence, and runs QA/code review;
- returns to the owner when scope, proof obligations, or artifact identity materially changes.

The important boundary is the approved Intent: a one- or two-sentence statement of what the owner
actually wants, supported by completion capability, exclusions and the proof journey. The agent
runs `task approval-summary` or `epic approval-summary` and asks whether that meaning is accurate;
it does not ask the owner to approve IDs or hashes. Approval is recorded once before planning.
Work that remains inside that meaning and its detailed envelope proceeds without approval fatigue.
Material drift requires correction or amendment and renewed confirmation.

## Choose The Right Route

| Route | Use it when | Result |
| --- | --- | --- |
| Backlog | The idea is useful future intent but is not ready for execution. | A `BL-*` row in `.project-workflow/BACKLOG.md`. |
| Fix | One bounded defect, regression, change request, or incident corrects a delivered or accepted baseline. | A lightweight `FIX-*` folder with one `FIX.md` and a row in the global tracker. |
| Task | The work creates a new outcome, needs a material product decision, or contains more than one independent change. | A `TASK-*` folder with `REQUIREMENTS.md` and `IMPLEMENTATION.md`. |
| Epic | Several coordinated outcomes or workstreams share parent acceptance criteria and closeout obligations. | An `EPIC-*` proposal, contract, decomposition, child tracker, evidence map, audit, and retro. |

An in-scope correction stays in its active task or epic child. Do not rewrite completed requirements to make later defects look as though they were part of the original ticket. Link the new Fix to the originating work and preserve the historical record.

The user's label is useful evidence, but the agent should recommend the route that matches the actual work.

## The Working Model

### Set Stable Project Outcomes

For a new repository, use the project constitution skill once to create or refine:

```text
.project-workflow/CONSTITUTION.md
```

The constitution records durable product outcomes, users, principles, and decision filters. Technical conventions belong in repository instructions or `.project-workflow/guidance.md`, not in the constitution.

### Keep Future Intent In The Backlog

Backlog rows are optional future intent, not active delivery state:

```bash
./.project-workflow/cli/workflow backlog add --title "Account export" --type "Task Candidate" --priority Medium --status Proposed --outcome "Customers can retain a portable copy of their account data."
./.project-workflow/cli/workflow backlog status --id BL-001 --to Accepted
./.project-workflow/cli/workflow backlog promote --id BL-001 --to task
./.project-workflow/cli/workflow backlog validate
```

Promotion keeps the backlog row for history, marks it `Promoted`, and links it to the new Task or Epic. Execution status then belongs in the trackers and work-item documents.

### Run A Task

A Task is the standard route for a new, bounded outcome:

```bash
./.project-workflow/cli/workflow task init --title "Account Export" --update-tracker
./.project-workflow/cli/workflow task status --id TASK-001 --to Analysing
```

The agent captures `REQUIREMENTS.md` with a user story, scope, non-goals, stable `AC1`, `AC2`, and later acceptance criteria, open questions, decisions, and a validation plan.

The file begins with a one- or two-sentence Intent and stable outcome commitments. When that meaning
and its supporting detail are correct, the agent renders the owner-facing synopsis and records the
owner's confirmation:

```bash
./.project-workflow/cli/workflow task approval-summary --id TASK-001
./.project-workflow/cli/workflow task approve-requirements \
  --id TASK-001 \
  --approved-by "Product Owner" \
  --source "Owner approved requirements and acceptance criteria in the project task"
```

After approval, the agent:

1. runs Planner and maps every implementation row to acceptance criteria;
2. runs Clarify as a bounded post-plan consistency pass that supports Tasks, Epic parents, and Epic
   children without creating another review loop;
3. resolves implementation details that remain inside the approved envelope;
4. runs the readiness gate and moves the task to `Ready`;
5. implements and validates the work;
6. moves the task through `Testing` and `Review`;
7. records QA evidence by acceptance-criteria ID;
8. marks the task `Complete` only after QA has a passing final disposition and the owner explicitly
   asks for completion. A retained `Changes Requested` verdict can reach that disposition through
   one exact passing affected-validation record; it is never rewritten or sent through automatic
   repeat QA;
9. runs a retro when the work produced reusable lessons or follow-up intent.

```bash
./.project-workflow/cli/workflow task ready --id TASK-001
./.project-workflow/cli/workflow task status --id TASK-001 --to Ready
./.project-workflow/cli/workflow task status --id TASK-001 --to "In Progress"
./.project-workflow/cli/workflow task status --id TASK-001 --to Testing
./.project-workflow/cli/workflow task status --id TASK-001 --to Review
./.project-workflow/cli/workflow task status --id TASK-001 --to Complete
```

`Plan Confirmed` remains available for legacy records. New work normally uses the owner-approved requirements envelope followed by agent-run planning, clarification, readiness, and `Ready`.

### Run A Fix

A Fix is deliberately lighter than a Task. It uses:

- a reserved `FIX-*` ID;
- one `FIX.md` containing report, triage, plan, evidence, and closeout;
- the shared `.project-workflow/tasks/` directory;
- the global `.project-workflow/TRACKER.md`;
- one triage classification: Defect, Regression, Change Request, or Incident;
- an optional Hotfix mode when urgency changes execution order, not the evidence requirement.

```bash
./.project-workflow/cli/workflow fix init --title "Export fails for large accounts"
./.project-workflow/cli/workflow fix triage --id FIX-001
./.project-workflow/cli/workflow fix status --id FIX-001 --to "In Progress"
./.project-workflow/cli/workflow fix status --id FIX-001 --to Testing
./.project-workflow/cli/workflow fix status --id FIX-001 --to Review
./.project-workflow/cli/workflow fix close \
  --id FIX-001 \
  --disposition Fixed \
  --decision "Verified bounded correction" \
  --closed-by "Product Owner"
```

Triage confirms the baseline, impact, likely affected area, regression risk, validation, and originating work. If investigation reveals a new outcome, several independent items, or coordinated workstreams, promote the Fix instead of stretching the lightweight record:

```bash
./.project-workflow/cli/workflow fix promote \
  --id FIX-001 \
  --to task \
  --reason "Investigation found several independent outcomes" \
  --promoted-by "Delivery Agent"
```

### Run An Epic

Epics are proposal-first. They add authority and evidence controls because several child workstreams must add up to one parent outcome.

```bash
./.project-workflow/cli/workflow epic init --title "Checkout Reliability"
./.project-workflow/cli/workflow epic lifecycle --epic-id EPIC-001 --to Analysing
```

Before decomposition, complete:

- `REQUIREMENTS.md` with a brief Intent, stable outcome commitments, parent acceptance criteria
  and any proposed child work;
- `EPIC-CONTRACT.md` with sources of truth, invariants, artifact targets, invalid substitutes, proof owners, and evidence expectations.

Then show the meaning-first synopsis, record the owner's confirmation, and create the authoritative
decomposition:

```bash
./.project-workflow/cli/workflow epic approval-summary --epic-id EPIC-001
./.project-workflow/cli/workflow epic approve-requirements \
  --epic-id EPIC-001 \
  --approved-by "Product Owner" \
  --source "Owner approved the epic requirements and decomposition boundary"
./.project-workflow/cli/workflow epic decompose --epic-id EPIC-001 --limit 5 --type Task
```

`DECOMPOSITION.md` is the authority for planned child IDs, titles, and parent-AC coverage. The agent can approve and scaffold matching rows inside the approved envelope without another owner checkpoint:

```bash
./.project-workflow/cli/workflow epic approve --epic-id EPIC-001 --id TASK-014
./.project-workflow/cli/workflow epic scaffold-child --epic-id EPIC-001 --id TASK-014
./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-001 --id TASK-014
```

For a full-contract Epic, complete `INTENT-AUDIT.json` after decomposition and child planning, then
inspect it read-only:

```bash
./.project-workflow/cli/workflow epic intent-audit --epic-id EPIC-001
```

The audit maps each OC commitment to parent ACs, child owners, disposition, required outcome proof,
source/target locations and user-visible consequences. Child readiness, Review and Complete fail
closed unless the audit is current; material narrowing, proxy substitution, omission or broadening
must be restored or covered by a current owner-approved capability amendment.

During delivery:

- the epic tracker owns child status and `Parent ACs` coverage;
- the global tracker summarizes the parent Epic;
- `ACCEPTANCE-MAP.md` is the live parent-coverage view;
- each child proves only the parent criteria assigned to it;
- proof-recipe claims use child-local `EVIDENCE.json`;
- `epic amend` records owner-approved work outside the decomposition authority;
- `epic audit` creates the closeout evidence record;
- `epic closeout --complete` completes the Epic only after parent criteria are evidenced or explicitly deferred and the retro is complete.

```bash
./.project-workflow/cli/workflow epic amend --help
./.project-workflow/cli/workflow epic audit --epic-id EPIC-001
./.project-workflow/cli/workflow epic closeout --epic-id EPIC-001 --complete
```

Direct child-row edits outside the decomposition or amendment authority are blocked. This prevents an Epic from quietly changing shape while work is underway.

### Evidence Is Part Of The Work

Tests, builds, prose review, and code inspection are useful evidence, but they are not interchangeable with every claim.

Project-workflow has structured proof recipes for:

- visual or reference fidelity;
- external contract alignment;
- deployed artifact alignment;
- runtime target and source identity;
- responsive or multi-context visual behavior.

When a requirement or material claim triggers one of these recipes, the relevant `EVIDENCE.json` must contain a passing structured claim and the required artifacts. A surrogate environment, unrendered inspection, or unrelated build cannot stand in for proof of the exact target.

## Installation And Refresh

### Prerequisites

- A Git repository
- Python 3.10 or newer
- `uvx`, or an intentional current package installation
- GitHub Copilot, Claude Code, OpenAI Codex, or Cursor

On Apple Silicon macOS, Homebrew installs `uvx` at `/opt/homebrew/bin/uvx`. Sandboxed agent
processes may omit Homebrew from `PATH` even when `uvx` is installed. Before treating it as
unavailable, check that path and expose it for the command or test run:

```bash
test -x /opt/homebrew/bin/uvx
PATH="/opt/homebrew/bin:$PATH" uvx --version
```

Run the canonical init command from the repository root:

```bash
uvx --from project-workflow==0.8.0 project init
```

Without `--agent`, the default mode is `github-copilot`. Pass an explicit mode when the repository uses another agent.

Use init only for a repository that does not yet contain project-workflow. If the repository is
already initialized, init makes no changes and directs the caller to canonical `project upgrade`.

For a new repository, init:

- installs the packaged CLI, templates, prompts, skills, rules, and managed guidance;
- creates marked project-workflow blocks in host-owned files;
- user-owned workflow files and unmarked host content are preserved;
- when generated content cannot safely replace an unmarked existing file, init writes a `*.new` file for review.

Init detects repository state before writing. A genuinely new installation receives a current
`.project-workflow/manifest.json`; every existing, legacy, invalid, or future installation is left
unchanged and receives the exact canonical upgrade command instead.

### Generated Structure

Every mode creates the shared workflow core:

```text
.project-workflow/
|-- BACKLOG.md
|-- TRACKER.md
|-- CONSTITUTION.md
|-- config.json
|-- manifest.json
|-- guidance.md
|-- cli/
|   |-- workflow
|   `-- workflow.py
`-- tasks/
    |-- TASK-*/REQUIREMENTS.md
    |-- TASK-*/IMPLEMENTATION.md
    |-- FIX-*/FIX.md
    `-- EPIC-*/
```

The selected mode adds agent-facing assets:

| Mode | Agent assets |
| --- | --- |
| GitHub Copilot | `.github/prompts/` and a managed block in `.github/copilot-instructions.md` |
| Claude Code | `.claude/agents/` |
| OpenAI Codex | `.agents/skills/` and a managed block in `AGENTS.md` |
| Cursor | `.cursor/agents/` and `.cursor/rules/project-workflow.mdc` |

`.project-workflow/guidance.md` is the repository-owned place for local validation commands, safety constraints, handoff rules, and conventions that should survive upgrades.

## Validation And Health

Use the initialized, dependency-free helper for day-to-day commands:

```bash
./.project-workflow/cli/workflow doctor
./.project-workflow/cli/workflow validate
./.project-workflow/cli/workflow backlog validate
```

Use canonical UVX, not the local helper, for repository upgrades. The local helper cannot prove it
has the latest managed asset resources; when those package resources are unavailable, its upgrade
command blocks and prints the exact canonical UVX command.

Strict mode makes safety warnings fail automation:

```bash
./.project-workflow/cli/workflow doctor --strict
./.project-workflow/cli/workflow validate --strict
```

Doctor checks tracker structure, linked task documents, readiness and completion evidence, epic schemas and coverage, and source-repository asset parity where applicable.

For agents and CI, use the versioned JSON envelope:

```bash
./.project-workflow/cli/workflow doctor --format json
./.project-workflow/cli/workflow doctor --strict --format json
```

Each finding includes a stable code, original and effective severity, affected artifact,
remediation owner, mechanical-upgrade eligibility, acceptance state, legacy state, message, and
fingerprint. Human and JSON output share the same finding evaluation and exit behavior.

Warnings have stable fingerprints. A known historical warning can be accepted in `.project-workflow/config.json` with a reason:

```json
{
  "accepted_doctor_warnings": [
    {
      "fingerprint": "22715ece2effa18a",
      "reason": "Accepted historical workflow artifact."
    }
  ]
}
```

Accepted warnings are hidden from normal output and do not fail strict mode. They reappear if their severity, path, or message changes. Review them explicitly:

```bash
./.project-workflow/cli/workflow doctor --show-accepted
```

Run `doctor` after tracker or task-document changes and before handing work over.

## Repository Upgrades

The commands have separate responsibilities:

- `project init` creates project-workflow in a new repository.
- `project doctor` diagnoses repository and workflow state without mutation.
- canonical UVX `project upgrade` refreshes managed assets and transforms durable repository state
  together.

### Normal Upgrade

Run one canonical command from a clean Git worktree. Do not run init first. UVX obtains the current
project-workflow package, so this works even when the repository's local helper is old or does not
yet contain the upgrade command:

```bash
uvx --from project-workflow==0.8.0 \
  project upgrade --agent codex
```

The command builds one deterministic plan containing managed helper/agent-asset changes and
ordered repository-schema migrations. It displays the exact targets, hashes, blockers, owner
decisions, and fingerprint, asks for confirmation, applies the confirmed plan as one transaction,
and reports post-upgrade validation. A cancellation makes no changes.

Agents and other non-interactive callers use the same canonical command with `--yes` after the
owner has authorized the upgrade:

```bash
uvx --from project-workflow==0.8.0 \
  project upgrade --agent codex --yes
```

Doctor is not a prerequisite. Run it separately when detailed diagnosis is useful; upgrade itself
reports the resulting repository state and finding counts.

### Automation And CI

Automation can retain an explicitly separated, non-mutating plan and fingerprinted apply. Both
commands must use the same package source and version:

```bash
uvx --from project-workflow==0.8.0 \
  project upgrade --agent codex --plan --format json

uvx --from project-workflow==0.8.0 \
  project upgrade --agent codex \
  --apply \
  --plan-fingerprint sha256:<REVIEWED_PLAN_FINGERPRINT>
```

Upgrade behavior by detected repository state:

| State before upgrade | Upgrade result |
| --- | --- |
| Not initialized | Blocks without mutation and directs the caller to `project init`. |
| Current | Refreshes changed managed assets, or reports a no-op when assets and schema are current. |
| Pre-versioned legacy | Refreshes managed assets and applies `PW-0001-legacy-manifest` in the same transaction. |
| Assets or schema behind | Refreshes assets and applies every required ordered migration together. |
| Invalid or unsupported future manifest | Blocks without mutation; the state must be resolved rather than forced. |

Apply requires a clean Git worktree including no untracked files. It rechecks repository state and
input hashes immediately before writing, computes every output first, and replaces only declared
targets. A failed multi-file replacement restores touched targets. Unmarked collisions are
preserved and receive a generated `*.new` file for review. Missing approvals, stale evidence,
accepted warnings, deferrals, and owner decisions remain visible and are never upgraded into
authority.

The first production migration, `PW-0001-legacy-manifest`, adopts the schema-1 manifest for a
recognized pre-versioned repository without rewriting its tracker, backlog, config, guidance,
task/Epic history, evidence, or unmarked content. See [COMPATIBILITY.md](COMPATIBILITY.md) for the
support policy.

## Sanitized Client Handoffs With Smoke Bomb

Smoke Bomb prepares a client ZIP from an agency- or freelancer-owned repository without handing
over Git history or internal project-workflow state. The recommended operating pattern is to create
a disposable branch, prepare useful client-facing context, review a deterministic cleanup plan,
apply that exact plan, and hand over the validated ZIP and its SHA-256. Smoke Bomb warns on a
detected default branch but leaves branch creation, commits, pushes, merges, and deletion to normal
Git operations.

The handoff is intentionally not a bare source dump. `README.md` and a canonical `AGENTS.md` must
remain substantive, and selected client targets receive their conventional instruction entry point
for Codex, Claude Code, Cursor, or GitHub Copilot. Missing guidance, unmarked ownership conflicts,
dirty state, unsafe file types, secret-like paths, residual project-workflow references, or failed
reviewed validation commands block export.

Plan without mutation from a clean dedicated worktree. Repeat `--client-agent` and
`--validation-command` when needed; the ZIP path must be outside the repository:

```bash
project smoke-bomb \
  --client-agent codex \
  --validation-command "npm test" \
  --output ../client-handoff.zip \
  --plan --format json
```

After reviewing every action, ownership decision, client artifact, exclusion, validation command,
warning, blocker, and the fingerprint, apply that exact plan. Authorized non-interactive agents add
`--yes`; human invocation otherwise confirms in a TTY:

```bash
project smoke-bomb \
  --client-agent codex \
  --validation-command "npm test" \
  --output ../client-handoff.zip \
  --apply --plan-fingerprint <REVIEWED_FINGERPRINT> --yes --format json
```

The archive inventory comes from Git-tracked and non-ignored existing worktree files after apply.
It excludes `.git`, `.project-workflow`, ignored build/transient files, and unsafe or secret-like
paths. Smoke Bomb is not a legal, licensing, security, or data-loss-prevention audit; those handoff
responsibilities remain separate.

## IDs And Parallel Work

`.project-workflow/config.json` controls prefixes and ID generation.

The compatibility defaults are:

- `TASK-###` for standalone tasks;
- reserved `FIX-###` IDs for lightweight fixes;
- `EPIC-###` for epics;
- `BL-###` for backlog rows.

Repositories can configure domain prefixes such as `UI`, `MCP`, or `DEV` for tasks. Fix, Epic, and Backlog IDs retain their own namespaces.

Sequential IDs are easy to read but can collide when several branches or agents allocate `max + 1` independently. Set the relevant `id_generation` value to `unique` for concurrent work:

```json
{
  "task_id_prefixes": ["TASK", "UI", "MCP", "DEV"],
  "default_task_id_prefix": "TASK",
  "id_generation": {
    "tasks": "unique",
    "epics": "unique",
    "fixes": "unique",
    "backlog": "unique"
  },
  "unique_id_length": 5
}
```

Unique IDs keep the namespace and use a short uppercase base36 suffix, such as `UI-K7F3Q`, `FIX-H4T2P`, `EPIC-R5M8T`, or `BL-Q6P4V`. The CLI checks workflow folders, the global tracker, epic trackers, and backlog rows before accepting a generated ID.

For one task, force a configured namespace with:

```bash
./.project-workflow/cli/workflow task init --title "Responsive account view" --prefix UI --update-tracker
```

## Parent Workspaces With Independent Repositories

A parent repository can own the only live Project Workflow state while work spans nested,
independently versioned Git repositories. Declare the registry in the existing
`.project-workflow/config.json`; do not create child trackers or a second workspace config:

```json
{
  "workspace": {
    "authority_repository": "workspace",
    "repositories": [
      {"id": "workspace", "path": ".", "role": "control"},
      {"id": "next", "path": "next", "role": "implementation"},
      {"id": "email", "path": "email", "role": "implementation"}
    ]
  }
}
```

Run workflow commands from the parent authority root. Every path must be relative, remain inside
that root, exist, and resolve to a unique independent Git worktree. The authority repository must
be the parent path `.` and the only repository with role `control`. Doctor reports a blocking
authority conflict if a registered non-authority repository contains a competing
`.project-workflow` directory.

Workspace tasks record `Primary repository` and `Repositories touched` in `REQUIREMENTS.md`.
Before Review or Complete, `IMPLEMENTATION.md` must contain one `Repository Evidence` row per
touched repository, attributing branch or PR state, validation, delivery state, and evidence.
Explicit `not applicable` or `not authorized` boundaries are valid records; placeholders and
`not recorded` may remain explicit for a branch/PR or later delivery stage that is outside scope.
Validation and its evidence source must be recorded before Review. Status inspects Git read-only
and never creates branches, commits, pushes, pull requests, releases, or deployments in any
repository.

## Existing Work And Repository History

Use `task adopt` or `epic adopt` when bringing pre-existing work under current gates. Adoption records the current authority envelope and marks inferred pre-adoption evidence as untrusted until it is refreshed.

Project-workflow should preserve history:

- promoted backlog rows remain visible;
- completed Tasks and Epics remain complete;
- later corrections link back through a Fix;
- deferrals and Epic amendments record owner, date, reason, and follow-up;
- tracker status changes use the CLI rather than silent Markdown edits.

This history is useful to humans and agents for the same reason: it distinguishes what was originally agreed from what was discovered later.

## Coordinator: One Owner-Facing Delivery Role

Coordinator carries a Project Workflow outcome from conversational intake through requirements,
planning, execution, proof, and authorised delivery. The owner confirms the plain-language meaning
once; the Coordinator carries the approved envelope and does not require a memorised workflow
prompt. It remains the sole writer of shared workflow state across physical tasks, compactions, and
executor returns.

Coordinator uses the smallest sufficient context and execution surface. An added agent, visible
task, document, review, owner interruption, or context transfer must address a named dependency,
risk, authority, or evidence need. Executor packets contain the relevant outcome, ACs, source,
scope, validation, evidence, prohibitions, and return contract—not full task history by default.

Clarify is available before approval, after planning/decomposition, and for a concrete ambiguity at
a Coordinator-owned execution boundary. It supports Task, Epic-parent, and Epic-child authority,
reuses answers already given, and returns `inside-envelope`, `drift-detected`, or
`approved-change` for a routed drift ambiguity. Clarify does not monitor work or create QA/review
loops. Coordinator stops after sufficient proof and authorised delivery unless later change or
evidence materially invalidates a named approved outcome or proof obligation.

## Delegate Compatibility: Graph Execution, Not A Second Role

`project-delegate` is retained as a compatibility entry for the first Coordinator release. It
enters the same one-Coordinator contract for an already-approved graph and becomes removal-eligible
only after one full minor release and observed migration evidence.

For work that crosses a material phase, repository, reframe, or physical context, `project
coordinate` maintains one work-item-local `COORDINATION.json`. Its preflight distinguishes the
package, asset, and coordination-contract version actually loaded by the context from repository
upgrade state; contract version `2` identifies this Coordinator contract. The file is a compact
logical handoff: current Intent and source identity, material decisions, context declaration, five
named boundary decisions, one earliest checkpoint, and one sourced next action. It does not copy
execution units, dependencies, packets, receipts, or worker lifecycle from the canonical plan and
Delegate. Missing, stale, or drifted decisions fail closed at existing lifecycle transitions.
Material product claims can name one earliest normal-user-journey checkpoint before dependent
fan-out. The same physical context may continue after explicitly loading the current contract when
there is no conflicting authority or isolation need; before that explicit load, preflight blocks
continuation as `contract-load-required`. A fresh context must earn its transfer cost.

Materially expensive verification is an optional campaign inside that same coordination state,
not another lifecycle or review scheduler. `coordinate init` durably classifies verification as
required or not required; required work also binds exact claims, stages, and scope so omission or
redefinition cannot bypass Review/Complete. `coordinate verification-preflight` reads that durable
classification and projects
`implementation-required`, `verification-required`, `qa-required`, `delivery-ready`, or `blocked`
without executing anything. A required campaign binds an exact candidate to claims, canonical
cheap-to-expensive stages, affected scope, finite limits, and input-bound typed receipts. Use a
declared manual command or a framework-neutral command/JSON adapter; every command receipt must
echo the exact request/candidate/source/proof/stage identity before it is retained. Project
Workflow does not require or identify a verifier. Certification fails fast on a product/assertion failure, while
diagnostic continuation requires a named selected decision and finite boundary. Limits pause or
block missing proof rather than waiving it. Candidate changes refresh affected proof,
evaluator-only changes regrade retained output with zero target calls, infrastructure gets one
bounded retry, and unknown material impact requires full proof. A current passing campaign proceeds
to the one existing independent QA gate and unchanged green proof is reused for delivery. Cheap
bounded work explicitly requiring no material campaign keeps the ordinary lifecycle unchanged.

Delegate coordinates existing approved execution units for exactly one target:

- for a Task, the units are implementation-plan rows and Implement performs each bounded unit;
- for an Epic, the units are approved child Tasks from the decomposition/amendment authority;
- a coordinator, current-session subagent, persistent/background task, and peer-capable team are
  executor surfaces, not interchangeable workflow units;
- independent QA reviews coordinator-verified results after implementation; Delegate's aggregate
  or retirement report cannot complete QA, Epic closeout, owner acceptance, integration, release,
  deployment, or adoption.

### Choose By Execution Need

Delegate selects the lightest surface that satisfies the unit's approved properties.
Task-versus-Epic kind does not decide the executor. Units use these execution-needs tokens:

- `bounded-return`, or blank metadata in a legacy plan, means the result can return through the
  current coordinator session;
- `durable-resume` requires cross-session recovery;
- `direct-owner-steering` requires a child the owner can interact with directly;
- `isolated-worktree` makes filesystem isolation binding;
- `peer:<group-id>` requires workers in that group to communicate directly.
- `benefit:<slug>`, `overhead:<slug>`, and `tradeoff:<slug>` are all required before a
  current-contract row may use a non-Coordinator surface. They state the delivery benefit, expected
  packet/setup/synthesis cost, and why the benefit outweighs it. Verified capacity alone is not a
  benefit; without this basis, non-binding work remains Coordinator/sequential.

The router still enforces parallel safety, write scope, repository scope, dependencies, validation,
and evidence. It chooses between a `sequential` and `parallel` schedule separately from the surface.

Positive examples:

- Two independent, bounded Epic children with disjoint scopes may use in-session `subagent`
  executors when current capacity is verified. Being Epic children does not force visible tasks.
- One Task implementation row that must survive coordinator interruption and needs direct owner
  steering may use an authorised `persistent-task`, even though it belongs to a Task.
- Two workers that genuinely need to negotiate a shared protocol may use `peer-team` when both the
  explicit `peer:<group-id>` need and current peer-team/peer-messaging capability are verified.
- A coupled migration whose steps mutate the same files remains `coordinator`-owned and sequential.

Negative examples:

- Parallel-safe work alone is not a reason to create a peer team; ordinary dependencies remain
  coordinator-mediated.
- An Epic approval is not authority to create a persistent Codex task. The current request must
  explicitly authorise visible task creation, and all required runtime capabilities must be
  verified.
- An unavailable isolated subagent cannot be replaced with a shared-filesystem subagent when
  isolation is binding. Use another verified isolated surface or block with the unmet property.
- A clean sidebar is not authority to archive active, failed, unresolved, or owner-promoted work.

Inspect a canonical graph without launching work:

```bash
./.project-workflow/cli/workflow delegate plan --id TASK-063 --format json
```

When the current host actually observes bounded subagents and two free child slots, report that
specific runtime observation rather than assuming host support or a fixed worker count:

```bash
./.project-workflow/cli/workflow delegate plan \
  --id TASK-063 \
  --requested-concurrency 3 \
  --available-child-capacity 2 \
  --observed-capability subagent \
  --unsupported-capability persistent-task \
  --capability-source "2026-08-19 current session tool and capacity inspection" \
  --format json
```

Capability provenance must contain the runtime observation date in `YYYY-MM-DD` form. The resulting
capability matrix is tri-state: runtime-observed `verified`, runtime-observed
`unsupported`, or `unknown`. Only verified current-host capability authorises native launch or
retirement. Distinguish ordinary subagents from isolated subagents; persistent creation from
persistent isolation, monitoring, and reconciliation; peer-team from peer messaging; and task
retirement from retirement reconciliation. Unknown or unsupported capability may use safe
sequential/coordinator execution only when every binding property remains satisfiable. Otherwise
the unit blocks before launch with the exact unmet property. Native persistent-task creation also
requires explicit owner authority applicable to the current request.

Plans and status are read-only. Human and versioned JSON output explain each unit's required
properties, requested/effective executor, schedule, concurrency, visibility
(`ephemeral`, `visible-retirable`, or `visible-retained`), retention policy, capability provenance,
and selection, fallback, or block reason.

The coordinator is the only writer of shared trackers, row status, acceptance maps, evidence
indexes, delegation runtime state, and lifecycle. Every worker receives a bounded packet and returns
identity, exact source/worktree, allowed diff, validation, and evidence for coordinator inspection.
A failure blocks its descendants, while unrelated graph branches continue only if the shared
baseline and premises remain valid.

### Retire Temporary Visible Children Safely

Temporary user-visible subordinate tasks default to host-neutral retirement-on-verified. In Codex,
the adapter maps that policy to reversible `archive-on-verified`. The coordinator emits one stable
retirement intent only after the child is terminal, coordinator-verified, durably integrated into
the authoritative target—or closed with a verified no-integration disposition and durable
receipt—and has no unresolved child-local or owner attention. It then observes the host action and
records the outcome. A confirmed archive is not repeated after resume.

The coordinator is never retired. Active, returned-but-unverified, failed, rejected, orphaned,
blocked, awaiting-owner, unintegrated, explicitly retained, and owner-promoted work stays visible
with its retention reason. Failed or unknown retirement remains pending and keeps the task handle;
Delegate never reports cleanup it did not observe. Retirement is sidebar lifecycle management, not
deletion of the task or its transcript.

Codex, Claude Code, GitHub Copilot, and Cursor use the same property policy through host-native
adapters. Installed syntax, generated parity, tests, and package inspection prove contract
alignment only. A host that was not exercised in the current run must be reported as expected or
aligned, not runtime-validated.

Invalid uses include delegating an arbitrary batch of standalone Tasks, treating a generated host
asset as proof of native support, asking a worker to mutate shared workflow state, treating a worker
completion assertion as dependency proof, blanket-archiving subordinate work, or treating Delegate
output as independent QA or closeout. Use an Epic to coordinate standalone Tasks, Planner to add
approved graph metadata, Implement for bounded changes, QA Review for independent verification,
and Epic closeout for final parent acceptance gates.

## Day-To-Day Guidance

- Start with the outcome, not a preselected workflow type.
- Keep one independently reviewable outcome per Task.
- Use the smallest route that still captures the required decisions and proof.
- Let the agent gather repository evidence before asking the owner questions it can answer locally.
- Keep acceptance-criteria IDs stable from requirements through planning, validation, and QA.
- Treat `Ready` as a passed gate, not a label applied by optimism.
- Use Coordinator for the owner-facing delivery journey. Its Delegate compatibility entry may run
  one approved Task or Epic graph with explicit scope metadata; delegated work still passes through
  implementation, independent QA, and retro.
- Commit workflow artifacts with the code they govern so branches and reviews carry their own context.
- Put durable local conventions in `.project-workflow/guidance.md`.
- Run `doctor` whenever workflow state feels uncertain.

Everything project-workflow creates is plain text. Owners can read it, agents can operate it, and teams can review it with the same Git history as the software it describes.

## Reference And Support

- Run `./.project-workflow/cli/workflow --help` for the current command surface.
- Read the [local CLI guide](.project-workflow/cli/README.md) for command-level detail.
- Report defects or propose improvements through [GitHub Issues](https://github.com/johndetlefs/project-workflow/issues).

## License

Project-workflow is available under the [MIT License](LICENSE).
