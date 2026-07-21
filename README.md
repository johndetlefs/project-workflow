# project-workflow

Project-workflow turns a conversation about what should change into a reviewable delivery record that lives beside the code.

It gives project owners clear decision points and gives coding agents a dependable way to move from intent to requirements, implementation, evidence, QA, and closeout. The workflow stays in Markdown and Git, so there is no separate dashboard to maintain and no hidden agent state to trust.

Use it with GitHub Copilot, Claude Code, OpenAI Codex, or Cursor.

## Quick Start

From the root of an existing Git repository:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init --agent codex
```

Choose the mode that matches your agent:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init --agent github-copilot
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init --agent claude-code
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init --agent codex
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init --agent cursor
```

Then tell the agent what you want in ordinary language:

> Add a backlog item for account export.

> Create a task for the approved account export feature. I want to review the requirements before implementation.

> The completed export flow now fails for large accounts. Treat this as a bounded fix.

The initialized agent instructions and skills tell the agent how to create the right artifacts, use the local workflow CLI, preserve approval history, and validate state.

## What You Get

- A repository-native backlog for ideas worth preserving but not yet active.
- Lightweight Fix records for bounded corrections after work has been delivered.
- Requirements and implementation records with stable acceptance-criteria IDs.
- One visible global tracker for active standalone work and epics, with child trackers inside epics.
- Explicit owner authority without repeated approval prompts inside an unchanged scope.
- Evidence and QA gates that make completion mean more than "the code was written."
- Proposal-first epics for coordinated work that needs decomposition and closeout.
- Agent guidance that can be refreshed without replacing your repository-owned instructions.
- Versioned repository upgrades with one-command confirmation, optional non-mutating plans, stale-plan rejection, and rollback.

Project-workflow is not a replacement for Jira, Linear, or another planning system. It is the execution layer beside the code: the place where agents can reliably read the agreed outcome, current status, proof obligations, and next action.

## How Collaboration Works

Project-workflow is human-directed and agent-operated.

The owner provides:

- the problem or opportunity;
- the desired outcome and affected user or system;
- boundaries, non-goals, constraints, priority, and relevant examples;
- the signal that would make the work acceptable;
- decisions where product authority is required;
- one explicit approval of the requirements and acceptance-criteria envelope before planning.

The agent:

- inspects the repository and existing workflow state;
- recommends Backlog, Fix, Task, or Epic from the actual scope;
- drafts and maintains the Markdown artifacts;
- surfaces unresolved product decisions instead of guessing;
- runs Planner and the post-plan Clarify pass after approval;
- validates readiness and advances work inside the approved envelope;
- implements, validates, records evidence, and runs QA/code review;
- returns to the owner when scope, proof obligations, or artifact identity materially changes.

The important boundary is the approved requirements envelope. Approval is recorded once before planning. Work that remains inside that envelope proceeds without approval fatigue. Material drift requires the requirements to be corrected or amended and approved again.

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

When those requirements are correct, the owner approves the envelope:

```bash
./.project-workflow/cli/workflow task approve-requirements \
  --id TASK-001 \
  --approved-by "Product Owner" \
  --source "Owner approved requirements and acceptance criteria in the project task"
```

After approval, the agent:

1. runs Planner and maps every implementation row to acceptance criteria;
2. runs Clarify as a post-plan consistency pass;
3. resolves implementation details that remain inside the approved envelope;
4. runs the readiness gate and moves the task to `Ready`;
5. implements and validates the work;
6. moves the task through `Testing` and `Review`;
7. records QA evidence by acceptance-criteria ID;
8. marks the task `Complete` only after QA passes and the owner explicitly asks for completion;
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

- `REQUIREMENTS.md` with stable parent acceptance criteria and any proposed child work;
- `EPIC-CONTRACT.md` with sources of truth, invariants, artifact targets, invalid substitutes, proof owners, and evidence expectations.

Then record the owner's single requirements approval and create the authoritative decomposition:

```bash
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

Run the canonical init command from the repository root:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init
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
uvx --from git+https://github.com/johndetlefs/project-workflow.git \
  project upgrade --agent codex
```

The command builds one deterministic plan containing managed helper/agent-asset changes and
ordered repository-schema migrations. It displays the exact targets, hashes, blockers, owner
decisions, and fingerprint, asks for confirmation, applies the confirmed plan as one transaction,
and reports post-upgrade validation. A cancellation makes no changes.

Agents and other non-interactive callers use the same canonical command with `--yes` after the
owner has authorized the upgrade:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git \
  project upgrade --agent codex --yes
```

Doctor is not a prerequisite. Run it separately when detailed diagnosis is useful; upgrade itself
reports the resulting repository state and finding counts.

### Automation And CI

Automation can retain an explicitly separated, non-mutating plan and fingerprinted apply. Both
commands must use the same package source and version:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git \
  project upgrade --agent codex --plan --format json

uvx --from git+https://github.com/johndetlefs/project-workflow.git \
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

## Existing Work And Repository History

Use `task adopt` or `epic adopt` when bringing pre-existing work under current gates. Adoption records the current authority envelope and marks inferred pre-adoption evidence as untrusted until it is refreshed.

Project-workflow should preserve history:

- promoted backlog rows remain visible;
- completed Tasks and Epics remain complete;
- later corrections link back through a Fix;
- deferrals and Epic amendments record owner, date, reason, and follow-up;
- tracker status changes use the CLI rather than silent Markdown edits.

This history is useful to humans and agents for the same reason: it distinguishes what was originally agreed from what was discovered later.

## Day-To-Day Guidance

- Start with the outcome, not a preselected workflow type.
- Keep one independently reviewable outcome per Task.
- Use the smallest route that still captures the required decisions and proof.
- Let the agent gather repository evidence before asking the owner questions it can answer locally.
- Keep acceptance-criteria IDs stable from requirements through planning, validation, and QA.
- Treat `Ready` as a passed gate, not a label applied by optimism.
- Use Delegate when one Task has several planned work items with explicit dependencies; delegated work still passes through implementation, QA, and retro.
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
