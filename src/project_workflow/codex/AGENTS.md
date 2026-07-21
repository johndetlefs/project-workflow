# Project Workflow

This repository uses project-workflow for spec-driven development. Keep workflow artifacts in `.project-workflow/` as the shared source of truth, and read `.project-workflow/guidance.md` for repo-specific workflow guidance when present.

## Workflow Order

1. Constitution: use `project-constitution` to establish or update `.project-workflow/CONSTITUTION.md` for product outcomes.
2. Backlog: use `project-backlog` when future intent should be captured before it becomes committed task or epic workflow state.
3. Route: keep in-scope corrections in active work; use `project-fix` for one bounded correction
   against delivered/accepted behavior, `project-task` for a new outcome or multiple independent
   items, and `project-epic` for coordinated workstreams.
4. Requirements: use `project-requirements` to capture the user story, scope, acceptance criteria,
   open questions, decisions, and validation plan. The owner approves this envelope before planning.
5. Planner: after approval, use `project-planner` to turn requirements into testable work items.
6. Clarify: run `project-clarify` after planning to reconcile the plan with requirements, repo
   constraints, and product outcomes; return to the owner only for material drift.
7. Ready: run `task ready` and move new tasks to `Ready`. `Plan Confirmed` remains a legacy status,
   not the default human checkpoint.
8. Implement: use `project-implement` to make the smallest scoped code change for one work item,
   validate it, and move it to testing.
9. QA & Code Review: use `project-qa-review` to independently verify acceptance criteria and review
   the code before completion.
10. Retro: use `project-retro` after completion when there is a reusable lesson or follow-up.

For multi-item orchestration, use `project-delegate` after planning. For large bodies of work, use `project-epic` to create proposal-first epic trackers and approved child tasks.

Backlog is optional and sits between constitution and tracker state. Keep `.project-workflow/BACKLOG.md` for future intent, rough priority, options, and promotion history. Promoted rows remain in the backlog with `Promoted To` pointing at the created task or epic ID; active execution status belongs only in `.project-workflow/TRACKER.md`, epic trackers, and task/epic docs.

Project Workflow is owner-directed and agent-operated. The owner supplies intent, constraints, examples, decisions, and approvals; the agent runs commands, drafts artifacts, asks focused questions, validates readiness, implements, reviews, and records evidence. Do not make manual template completion the normal user path.

The user's work-item label is non-binding. The agent must make and state an evidence-based routing
recommendation. Clear authorized cases may proceed; genuinely ambiguous or materially different
cases require one focused question. Do not reopen or rewrite completed work by default.

For epic-managed work, preserve parent epic acceptance criteria coverage from the epic tracker through child requirements, child implementation, QA evidence, and closeout. New epic trackers use a `Parent ACs` field; legacy trackers may carry coverage in `Notes` as `Covers AC1, AC3`. The global tracker summarizes epic rows; epic `TRACKER.md` files own child rows, including Proposed rows.

When a user asks to initialize project-workflow in a new repository, run the canonical UVX init command from that repository root:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init
```

When a user asks to update, refresh, reinstall, align, or upgrade an existing repository, use canonical UVX upgrade instead; do not run init first:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project upgrade
```

Add `--agent codex`, `--agent cursor`, `--agent claude-code`, or `--agent github-copilot` for the target mode. Canonical UVX upgrade obtains current software and plans managed assets and repository schema together. Use `--yes` for an authorized non-interactive one-command apply, or `--plan --format json` followed by `--apply --plan-fingerprint <SHA256>` when automation requires separate review.

## Workflow Skill Map

- If the user asks to create, update, review, or align the product constitution, use `.agents/skills/project-constitution/SKILL.md`.
- If the user asks to capture, refine, validate, accept, defer, reject, supersede, or promote future project intent before task/epic execution, use `.agents/skills/project-backlog/SKILL.md`.
- If the user asks to create a task, story, feature folder, tracker row, or new project-workflow item, use `.agents/skills/project-task/SKILL.md`.
- If the user reports a bounded post-completion defect, regression, change request, incident, or
  hotfix, or asks whether work should be a Fix, use `.agents/skills/project-fix/SKILL.md`.
- If the user asks to create, decompose, approve, or scaffold epic-managed work, use `.agents/skills/project-epic/SKILL.md`.
- If the user asks to capture requirements, define scope, write acceptance criteria, record open questions, or prepare a validation plan, use `.agents/skills/project-requirements/SKILL.md`.
- If the user asks to plan implementation, break requirements into phases, or create testable work items, use `.agents/skills/project-planner/SKILL.md`.
- If the user asks to resolve ambiguity, reconcile conflicting requirements, or decide between unclear options, use `.agents/skills/project-clarify/SKILL.md`.
- If the user asks to implement a planned project-workflow item, use `.agents/skills/project-implement/SKILL.md`.
- If the user asks to coordinate or run multiple planned work items, use `.agents/skills/project-delegate/SKILL.md`.
- If the user asks for QA, code review, verification, release readiness, or completion approval, use `.agents/skills/project-qa-review/SKILL.md`.
- If the user asks for a retro, retrospective, lessons learned, convention updates, agent updates, prompt updates, or post-completion cleanup, use `.agents/skills/project-retro/SKILL.md`.
- If a task-specific workflow is requested but the task folder does not exist, run `project-task` first before requirements, planning, clarification, implementation, review, or retro.
- Do not skip directly to planning or implementation when requirements are missing, ambiguous, or not accepted as explicit risks.

## Drift Gate Requirements

- Before implementation-oriented work, record one owner-approved requirements/AC envelope with `task approve-requirements` or `epic approve-requirements`. Do not treat an agent draft, silence, or implementation request as approval.
- Do not ask for repeated generic approval when work remains inside the unchanged approved envelope. Fix concrete drift/evidence gaps directly, and ask the owner only for material scope changes, amendments, deviations, deferrals, artifact identity changes, or proof-obligation changes.
- For pre-existing work, use `task adopt` or `epic adopt`; pre-adoption inferred evidence remains untrusted until refreshed.
- New/adopted epics require non-placeholder `EPIC-CONTRACT.md` before decomposition, child approval/scaffolding, or movement into `Ready`/`In Progress`.
- Epic child rows must come from `DECOMPOSITION.md` or an approved `AMENDMENTS.md` record. Direct tracker edits outside that authority cannot advance through approval, scaffold, readiness, Review, or Complete gates.
- Scaffolded epic children inherit parent AC coverage, child charters, proof ownership, artifact targets, invalid substitutes, and child-local `EVIDENCE.json`.
- If requirements, acceptance criteria, child charters, epic contracts, or material claims trigger a proof recipe, structured evidence is required. QA prose, code review, tests, builds, surrogate surfaces, and wrong target/source pairs are invalid substitutes where the recipe requires stronger proof.
- Visual/reference fidelity requires calibration before implementation and rendered comparison against the delivered user-facing artifact before Review/Complete. Runtime target/source proof requires the exact execution target, source/artifact under test, observation method, and positive proof that the target used that source.

## CLI Requirements

- Treat `.project-workflow/cli/workflow` as the authoritative way to perform operations it supports.
- Use the CLI for backlog row creation, status changes, validation, and promotion. Do not hand-edit backlog lifecycle state when the CLI can do it.
- Use the CLI for task scaffolding and tracker-safe task creation. Do not manually create task folders, starter `REQUIREMENTS.md`, starter `IMPLEMENTATION.md`, or tracker rows when the CLI can do it.
- Use the CLI for Fix scaffolding, triage, lifecycle, promotion, and closeout. Keep Fix records under
  `.project-workflow/tasks/FIX-<ID>-<Suffix>/FIX.md` and in the one global tracker; do not create a
  separate Fix tracker or top-level fixes directory.
- Run project-workflow CLI commands from the repository root.
- If a selected project-workflow skill documents a CLI command, run that command instead of recreating its behavior manually.
- If the CLI does not support the selected workflow step, follow the selected skill and update the relevant Markdown files directly.
- If the CLI command fails, stop and report the failure before attempting a manual fallback.

## Codex Usage

- Use the repo-scoped skills in `.agents/skills/project-*` when the user asks for project workflow steps, even when the user asks in natural language rather than naming the skill.
- Read `.project-workflow/guidance.md` before changing workflow state when the file exists.
- For broad future objectives, use `project-backlog` to draft outcome-focused backlog candidates from project context. Do not create tracker rows, task folders, or epic folders until the owner accepts or promotes the row.
- Existing roadmap/backlog documents outside `.project-workflow/BACKLOG.md` are preserved. Do not import or transform them automatically; create a repo-local migration task if needed.
- Read `.project-workflow/config.json` for repo-owned task ID namespaces, ID generation, and accepted doctor warning fingerprints when it exists. Sequential IDs look like `TASK-001`; unique IDs keep the prefix and use a 5-character base36 suffix by default, such as `WF-K7F3Q`.
- Do not report accepted doctor warnings as active issues after `doctor` hides them. Use `doctor --show-accepted` only when auditing accepted workflow debt.
- If a task folder does not exist, run `./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker` from the repo root and let the CLI assign the next configured task ID. Add `--prefix <PREFIX>` only when the user or repo guidance calls for a configured non-default prefix.
- Read `.project-workflow/tasks/<ID>-*/REQUIREMENTS.md` before planning, implementing, reviewing, or running retro.
- Read `.project-workflow/tasks/<ID>-*/IMPLEMENTATION.md` before implementing, reviewing, or running retro for a work item.
- When planning, make every implementation task row map to one or more stable acceptance criteria IDs (`AC1`, `AC2`, etc.) from the task requirements or implementation acceptance criteria section.
- When planning epic-managed child tasks, keep both the child AC IDs and parent epic AC coverage visible in requirements, implementation rows, validation evidence, and QA notes.
- Before implementation-oriented status transitions, run readiness gates where available: `task ready`, `epic ready`, or `epic ready-child`. If a gate fails, remediate repo-gatherable gaps directly and ask the owner only for decisions, missing product context, or material authority changes listed above.
- Owner approval of requirements/ACs occurs before planning. After approval, run Planner,
  post-plan Clarify, `task ready`, and move to `Ready` autonomously unless setup-only scope,
  material drift, exceptional authority, or optional requested/high-risk plan review requires a pause.
- Keep `.project-workflow/TRACKER.md` status aligned with the current workflow state using `./.project-workflow/cli/workflow task status --id <TASK-ID> --to <STATUS>` when the command is available.
- Do not mark a task or work item `Complete` unless implementation validation and QA/code review have passed and the user explicitly asks for completion.

## Status Rules

- New scaffolded tasks start as `To Do`.
- Move a new task to `Analysing` only after its requirements/AC approval envelope is recorded.
- Move a planned and clarified new task to `Ready` after `task ready` passes. `Plan Confirmed` is
  supported for legacy tasks.
- Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to "In Progress"` before implementation work begins.
- Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to Testing` after implementation and validation have been run.
- Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to Review` while QA/code review is running.
- Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to Complete` only after QA/code review passes and the user explicitly requests it.
- Leave the tracker row as `Complete` during retro unless the user explicitly asks to reopen the task.

## Validation

- Run `.project-workflow/cli/workflow doctor` when workflow state is uncertain or before continuing after tracker/task doc edits.
- Use `.project-workflow/cli/workflow doctor --strict` when safety warnings should block autonomous work.
- Keep command ownership explicit: init creates a new installation, Doctor diagnoses without mutation, and canonical UVX upgrade plans and applies managed assets and repository schema together. Existing repositories must not run init first. Use `--yes` for authorized one-command agent operation or `--plan` plus `--apply --plan-fingerprint <SHA256>` for separate automation review.
- Run the most relevant available tests, type checks, linters, or manual verification steps for the changed work.
- If broad validation fails for unrelated pre-existing reasons, run the narrowest meaningful checks and report the limitation.
