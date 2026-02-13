---
name: project.clarify
description: Ask the minimum set of questions needed to remove ambiguity before planning/implementing.
argument-hint: topic="..." taskId=APP-330-Superuser
agent: agent
---

Use this prompt when requirements or constraints are unclear.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- Project outcomes: [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical task docs:
  - `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md` (must include `## User Story` at the top)
  - `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` (source of truth for agreed outcomes/expectations)

Inputs:

- Task (optional): `${input:taskId:APP-000-Example}`
- Topic: `${input:topic:What needs clarifying?}`

Output (Markdown):

Workflow (must follow):

1. Read context first

- Read the `## User Story` section from `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`.
- Read `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` (if it exists) and treat it as the source of truth for what’s already been agreed.
- Cross-check against repo constraints in `../copilot-instructions.md` and project outcomes in `../../.project-workflow/CONSTITUTION.md`.

Guardrail:

- If `IMPLEMENTATION.md` does not have a usable `## User Story` yet, STOP and instruct the user to run the `project.requirements` prompt first. Do not invent clarifying questions without a user story anchor.

2. Proactively log questions BEFORE asking the user

- Identify every ambiguity/conflict that would change scope, safety, security, billing attribution, data correctness, or user-visible behavior.
- For each ambiguity, write it into `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` as a numbered open question (e.g. `Q1`, `Q2`, …) with 2–4 options labeled `A/B/C/...`.
- Each question must be explicitly anchored to the current user story and include a short “why it matters”.

3. Work through questions item-by-item until resolved

- Ask the user ONE unresolved question per response (default) so decisions are made sequentially.
  - If there are many low-risk questions and the user explicitly asks for batching, you may ask up to 2–3 at a time.
- After the user answers:
  - Update `REQUIREMENTS.md` immediately: record the decision in a decisions log, mark the question resolved, and remove/strike it from open questions.
  - Keep `IMPLEMENTATION.md` in sync with the confirmed decisions.
  - Keep the `IMPLEMENTATION.md` task list in sync:
    - If `IMPLEMENTATION.md` has a `## Tasks` section, update it to reflect the confirmed decisions (add/update/remove tasks as needed; mark “clarification-only” tasks complete as questions are resolved).
    - If `IMPLEMENTATION.md` does NOT yet have a `## Tasks` section, you MAY add a minimal `## Tasks` section limited to tracking clarification work (e.g., “Resolve Q1…Qn”). Do NOT invent a full implementation plan here — the `project.planner` prompt owns full task planning.
- Repeat until `REQUIREMENTS.md` has no unresolved open questions (or the user explicitly accepts remaining items as risks and that acceptance is recorded).

## User Story (from IMPLEMENTATION.md)

-

## Conflicts / Ambiguities Found

For each conflict/issue:

- Explain what is conflicting and why it matters.
- Propose 2–4 reasonable options (labeled A/B/C/…); each option should be actionable, realistic for this repo, and include tradeoffs.
- Ask the user to choose an option (or provide a different preference).

Example format:

### Issue 1: <short title>

- Conflict: <what conflicts with what>
- Why it matters: <risk / impact>
- Options:
  - A: <option> (pros/cons)
  - B: <option> (pros/cons)
  - C: <option> (pros/cons)
- Question: Which option should we take?

## Clarifying Questions

### Product / UX

-

### Permissions / Security

-

### Data / DB / RLS

-

### Migration / Rollout

-

### Observability

-

## Decisions to Record in REQUIREMENTS.md

Always ensure the questions exist in `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` BEFORE you ask them.

If the user’s answers are present in the conversation context, document the decisions and chosen options immediately in `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` (including rationale/tradeoffs where relevant), and do not ask again.

If the user’s answers are not present yet:

- First, write/update `REQUIREMENTS.md` with the open questions (Q1/Q2/…) and their A/B/C options.
- Then ask the user the next single unanswered question.

Also keep the implementation tracker up to date:

- After recording each decision in `REQUIREMENTS.md`, update `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md` to keep BOTH:
  - `## User Story` (and any decision-dependent notes) consistent with `REQUIREMENTS.md`, and
  - `## Tasks` consistent with the confirmed decisions.
- Clarify may update an existing task list (or add a minimal “clarification tracking” task list), but must not generate a full multi-phase implementation plan — Planner owns full task planning.

-

## Suggested Defaults (if the user doesn’t care)

-

Guardrail: don’t start implementation until unresolved questions are cleared (or explicitly accepted as risks) and decisions are recorded in `REQUIREMENTS.md`.
