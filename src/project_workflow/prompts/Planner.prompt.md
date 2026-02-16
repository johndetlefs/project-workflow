---
name: project.planner
description: Turn confirmed requirements into a phased implementation plan with validation steps.
argument-hint: taskId=APP-330-Superuser planFocus="..."
agent: agent
---

Use this prompt to propose a safe, incremental plan.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical task tracker location: `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`
- Requirements source of truth: `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
- Project outcomes: [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)

Inputs:

- Task: `${input:taskId:APP-000-Example}`
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

- Each task must be independently _testable_ and have a clear "done" outcome.
- Tasks must be **outcome-based** (deliverable behavior or user-visible capability), not a checklist of implementation steps.
- Each task must include explicit **Acceptance Criteria (AC)**.
- Each task must include a **User Verification** step that a non-developer user can perform (or a precise dev command if it's inherently technical).
- Avoid vague tasks like "ensure X works" or "verify Y" without stating what to check and how.
- Prefer vertical slices when possible (deliver value incrementally), but don't mix unrelated concerns in one task.

If the repo uses a task table, include at least: `Title`, `Description`, `Acceptance Criteria`, `User Verification`, `Status`.

Use this exact table format in `IMPLEMENTATION.md` (copy/paste):

```md
|  ID | Title     | Description                         | Acceptance Criteria               | User Verification            | Status |
| --: | --------- | ----------------------------------- | --------------------------------- | ---------------------------- | ------ |
|   1 | <Outcome> | <What changes for the user/system?> | - <observable pass/fail criteria> | - <steps a user can perform> | To Do  |
```

### Table formatting rules (critical)

Markdown tables break if you put literal newlines inside a cell.

- Every task row **must be a single physical line** (one `| ... | ... |` line per task).
- For multiple bullets/steps inside a cell, use HTML line breaks: `<br>`.
- Do not include raw `|` characters inside cell text. If you need them, escape as `\|`.
- Do not wrap table rows across multiple lines.

Good example (multi-line content in a cell, but still one row):

```md
| 1 | Example | Short description | - AC 1<br>- AC 2<br>- AC 3 | - Step 1<br>- Step 2 | To Do |
```

Example (good outcome-based tasks; replace with your task's domain):

```md
|  ID | Title                                    | Description                                                                                                                     | Acceptance Criteria                                                       | User Verification | Status |
| --: | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ----------------- | ------ |
|   1 | Enforce server-side allocation on create | When creating an entity, server assigns allocation based on trusted server context, ignoring client-supplied allocation fields. | - Create succeeds and persisted `team_id` equals the server-derived team. |

- Passing a different `team_id` in the request body has no effect.<br>- Unauthorized users cannot create entities for other teams. | - In the app UI, create an entity under Team A; confirm it appears under Team A only.<br>- (Dev) Attempt to POST with a mismatched `team_id`; confirm response still allocates to Team A. | To Do |
  | 2 | Fail fast on required config missing | If a required env/config value is missing, the request fails with a stable error contract. | - API responds with HTTP 500.
```

Anti-examples (do NOT write tasks like this):

- "Find where call creation happens"
- "Add helper function to compute team id"
- "Refactor X" (without a user-visible or measurable outcome)
- "Verify billing works" (without specifying the scenario and what to check)

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
- If you detect conflicts between `REQUIREMENTS.md`, the `## User Story` in `IMPLEMENTATION.md`, and repo constraints, stop and instruct the user to run the `project.clarify` prompt to resolve them and record decisions back into `REQUIREMENTS.md`.

Task list guardrails:

- The `project.planner` prompt owns the implementation task list in `IMPLEMENTATION.md`.
- Do not treat AC as optional; missing AC means the task is not ready.
- The user should be able to verify each task without reading code (unless explicitly unavoidable).
- Ensure every acceptance criterion in `REQUIREMENTS.md` is mapped to at least one concrete validation step in the task list (`User Verification` or explicit validation notes).
- If any requirement/acceptance criterion is not covered by the plan, stop and route to `project.clarify` to resolve and record the decision in `REQUIREMENTS.md` before planning continues.
- For delegate-execution stories (`project.delegate`), explicitly cover mode defaults, dependency-map validation, worker-limit behavior, and fail-fast/halted reporting in planned outcomes and validation steps.

Tracker rules:

- Use statuses: `To Do`, `Analysing`, `Plan Confirmed`, `In Progress`, `Blocked`, `Testing`, `Complete`, `N/A`.
- Only mark `Complete` after validation is confirmed AND the user explicitly instructs you to mark it `Complete`.

User story tracker rules:

- `/.project-workflow/TRACKER.md` is part of the process. When moving into planning for a story/task, ensure there is a row for `${input:taskId}` and update its `Status`.
- Use the same status vocabulary as above.
- During planning, set story `Status` to `Analysing`.
- Only set story `Status` to `Plan Confirmed` after the user explicitly confirms the plan.
- Do not set story `Status` to `Complete` unless validation is confirmed AND the user explicitly instructs you to mark it `Complete`.
