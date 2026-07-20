---
name: project.planner
description: Turn confirmed requirements into a phased implementation plan with validation steps.
argument-hint: taskId=TASK-330-Superuser planFocus="..."
agent: agent
---

Use this prompt to produce a safe, incremental plan after the owner has approved the
requirements/acceptance-criteria envelope. The plan is agent-owned execution detail inside that
authority; a second generic human plan-approval ceremony is not required by default.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- Repo-specific workflow guidance: [../../.project-workflow/guidance.md](../../.project-workflow/guidance.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical task tracker location: `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`
- Requirements source of truth: `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
- Project outcomes: [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)

Inputs:

- Task: `${input:taskId:TASK-000-Example}`
- Plan focus: `${input:planFocus:What are we planning (feature/bug/area)?}`

Output (Markdown, use headings exactly):

## Goal

-

## Approach

-

## Phases

### Phase 1

- Changes:
- Validation:
- Tracker updates:

### Phase 2

- Changes:
- Validation:
- Tracker updates:

## Task List (for IMPLEMENTATION.md)

Produce (or update) an agile task list in `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`.

Task quality rules (must follow):

- Each task must be independently _testable_ and have a clear “done” outcome.
- Tasks must be **outcome-based** (deliverable behavior or user-visible capability), not a checklist of implementation steps.
- Each task must map to explicit **Acceptance Criteria IDs** from `REQUIREMENTS.md` or the `## Acceptance Criteria` section in `IMPLEMENTATION.md` (`AC1`, `AC2`, etc.).
- Each task must include a **User Verification** step that a non-developer user can perform (or a precise dev command if it’s inherently technical).
- Every acceptance criterion must be covered by at least one task row.
- If a row claims visual/reference fidelity, external contract alignment, deployed/published artifact alignment, runtime target/source verification, or responsive/multi-context behavior, include the matching proof recipe and expected evidence artifact. Do not plan to satisfy those claims with code review, tests, build output, surrogate surfaces, or a related environment.
- A task row may map to multiple ACs, for example `AC1, AC3: <criteria summary>`.
- Avoid vague tasks like “ensure X works” or “verify Y” without stating what to check and how.
- Prefer vertical slices when possible (deliver value incrementally), but don’t mix unrelated concerns in one task.

If the repo uses a task table, include at least: `Title`, `Description`, `Acceptance Criteria`, `User Verification`, `Status`.

Use this exact table format in `IMPLEMENTATION.md` (copy/paste):

```md
|  ID | Title     | Description                         | Acceptance Criteria               | User Verification            | Status |
| --: | --------- | ----------------------------------- | --------------------------------- | ---------------------------- | ------ |
|   1 | <Outcome> | <What changes for the user/system?> | AC1: <observable pass/fail criteria> | <steps a user can perform> | To Do  |
```

### Table formatting rules (critical)

Markdown tables break if you put literal newlines inside a cell.

- Every task row **must be a single physical line** (one `| ... | ... |` line per task).
- For multiple bullets/steps inside a cell, use HTML line breaks: `<br>`.
- Do not include raw `|` characters inside cell text. If you need them, escape as `\|`.
- Do not wrap table rows across multiple lines.

Good example (multi-line content in a cell, but still one row):

```md
| 1 | Example | Short description | AC1, AC2: First observable criterion.<br>AC3: Second observable criterion. | Step 1<br>Step 2 | To Do |
```

Example (good outcome-based tasks; replace with your task’s domain):

```md
|  ID | Title                                    | Description                                                                                                                     | Acceptance Criteria                                                                                                                    | User Verification                                                                                                                                                                            | Status |
| --: | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
|   1 | Enforce server-side allocation on create | When creating an entity, server assigns allocation based on trusted server context, ignoring client-supplied allocation fields. | AC1: Create succeeds and persisted `team_id` equals the server-derived team.<br>AC2: Passing a different `team_id` has no effect. | In the app UI, create an entity under Team A and confirm it appears under Team A only.<br>(Dev) POST with a mismatched `team_id`; confirm response still allocates to Team A. | To Do |
|   2 | Fail fast on required config missing | If a required env/config value is missing, the request fails with a stable error contract. | AC3: API responds with HTTP 500 and a stable error body when config is missing. | Temporarily remove the config in a test environment and confirm the API returns the documented error contract. | To Do |
```

Anti-examples (do NOT write tasks like this):

- “Find where call creation happens”
- “Add helper function to compute team id”
- “Refactor X” (without a user-visible or measurable outcome)
- “Verify billing works” (without specifying the scenario and what to check)

## Files / Areas Likely to Change

-

## Data / RLS / RPC / Migrations

-

## Risks & Mitigations

-

Planning guardrails:

- Base the plan on `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` (outcomes/expectations), not assumptions.
- If `REQUIREMENTS.md` is missing, stop and instruct the user to run the `project.requirements` prompt first.
- If `REQUIREMENTS.md` has any unresolved `## Open Questions`, stop and instruct the user to run the `project.clarify` prompt (or answer directly) and ensure the outcomes/decisions are recorded back into `REQUIREMENTS.md` before planning.
- Exception: you may proceed with a plan only if the user explicitly accepts the unresolved items as risks AND that acceptance is recorded in `REQUIREMENTS.md` (e.g., in `## Decisions Log`).
- Before planning, verify the requirements approval envelope. If approval is missing or stale,
  stop and return to owner review; do not ask an agent to self-approve it.
- After approval, move the task to `Analysing`, write the plan, run a post-plan clarification pass
  against requirements and repo constraints, then run `task ready`. Remediate repo-gatherable plan
  gaps autonomously. Return to the owner only for material scope drift, new product decisions,
  exceptional authority, or a deliberately requested/high-risk plan review.
- If you detect conflicts between `REQUIREMENTS.md`, the `## User Story` in `IMPLEMENTATION.md`, and repo constraints, stop and instruct the user to run the `project.clarify` prompt to resolve them and record decisions back into `REQUIREMENTS.md`.

Task list guardrails:

- The `project.planner` prompt owns the implementation task list in `IMPLEMENTATION.md`.
- Do not treat AC mapping as optional; a task row without an `AC#` reference is not ready for implementation.
- The user should be able to verify each task without reading code (unless explicitly unavoidable).
- Ensure every acceptance criterion in `REQUIREMENTS.md` is mapped to at least one concrete task row and validation step in the task list (`Acceptance Criteria`, `User Verification`, or explicit validation notes).
- Keep AC IDs stable. Do not renumber existing ACs unless the user explicitly approves the requirements change.
- If any requirement/acceptance criterion is not covered by the plan, stop and route to `project.clarify` to resolve and record the decision in `REQUIREMENTS.md` before planning continues.
- For delegate-execution stories (`project.delegate`), explicitly cover mode defaults, dependency-map validation, worker-limit behavior, and fail-fast/halted reporting in planned outcomes and validation steps.

Tracker rules:

- Use statuses: `To Do`, `Analysing`, `Ready`, `Plan Confirmed` (legacy-compatible), `In Progress`, `Blocked`, `Testing`, `Review`, `Complete`, `N/A`.
- Only mark `Complete` after implementation validation and QA/code review have passed AND the user explicitly instructs you to mark it `Complete`.

User story tracker rules:

- `/.project-workflow/TRACKER.md` is part of the process. When moving into planning for a story/task, ensure there is a row for `${input:taskId}` and use the lifecycle command to update its `Status`.
- Use the same status vocabulary as above.
- During planning, run `./.project-workflow/cli/workflow task status --id ${input:taskId} --to Analysing`.
- When the post-plan clarification pass and `task ready` succeed, run
  `./.project-workflow/cli/workflow task status --id ${input:taskId} --to Ready` and continue inside
  the approved envelope. `Plan Confirmed` remains valid for legacy tasks but is not the default
  human checkpoint for new work.
- Do not set story `Status` to `Complete` unless QA/code review has passed AND the user explicitly instructs you to mark it `Complete`.
