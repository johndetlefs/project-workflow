---
name: project.requirements
description: Capture and confirm what we are building (problem, scope, acceptance criteria).
argument-hint: taskId=APP-330-Superuser goal="..." context="..."
agent: agent
---

Use this prompt to produce a crisp, testable set of requirements.

This is an iterative prompt. Expect to run it multiple times:

- Pass 1: ask what the feature/bugfix is, draft an initial user story, produce a best-effort `REQUIREMENTS.md`, and ask the minimum questions needed to remove ambiguity.
- Pass N: incorporate the user's answers, resolve open questions, tighten acceptance criteria, and strengthen the validation plan.

Context sources (reference, don't duplicate):

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- Project outcomes (north stars): [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- E2E exception rules (only if editing `front-end/apps/e2e/**`): [../instructions/e2e.instructions.md](../instructions/e2e.instructions.md)

Canonical task docs:

- `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` (this prompt produces/updates this file)
- `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md` (must include `## User Story` at the top; keep it in sync with `REQUIREMENTS.md`)

Inputs:

- Task: `${input:taskId:APP-000-Example}`
- Goal: `${input:goal:Describe the user outcome}`
- Optional context: `${input:context:Links, routes, screenshots, logs, constraints}`

Output (Markdown, use headings exactly):

Primary output artifact:

- Write/update `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` with the contents of this prompt output.

This is not a technical design doc. Focus on outcomes, expectations, and "what done means".

Process:

- Step 0 (always first): Discovery — identify what we are building.
  - If the feature/bugfix is not explicitly described in the conversation context and inputs, ask the user:
    - "What is the new feature or bugfix?"
    - And only the minimal freeform context needed to draft a user story (where in the product, who is affected, and what success looks like).
  - IMPORTANT: In Discovery, do NOT ask A/B/C-style questions yet. You do not have a user story to anchor them to.
  - If Discovery information is missing, STOP after asking the Discovery questions. Do not draft a user story, do not write/update files, and do not ask additional questions.

- Step 1: Draft the user story (only after Discovery is answered).
  - Based on the user's Discovery answer (or the provided inputs), write a first-draft user story (may be imperfect) and put it in BOTH:
    - `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md` under `## User Story`
    - `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` under `## User Story`
  - IMPORTANT: This prompt may only create/update the `## User Story` section in `IMPLEMENTATION.md`.
    - Do NOT add or modify `## Tasks`, task lists, phases, checklists, or implementation steps in `IMPLEMENTATION.md`.
    - Task planning belongs to the `project.planner` prompt.

- Step 2: Clarify only after the user story exists.
  - If any critical requirement is ambiguous, untestable, or missing, write it as an open question.
  - Ask the user the minimum set of questions to resolve it.
  - A/B/C-style multiple-choice questions are allowed ONLY here (after the user story exists), and must be explicitly anchored to the current user story.
  - Stop after asking questions. Do not proceed to planning/implementation until open questions are resolved or explicitly accepted as risks and recorded.

- Read `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` if it exists. Treat it as the current draft.
- Read `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md` and treat its user story as canonical for implementation, but keep it synced with `REQUIREMENTS.md` as discovery evolves.
- Cross-check for conflicts across: Goal input, the user's described feature/bugfix, the user story, existing REQUIREMENTS, and repo constraints.
- Update `REQUIREMENTS.md` to be internally consistent.
- If any critical requirement is ambiguous, untestable, or missing, write it as an open question and then ask the user the minimum set of questions to resolve it.
- Stop after asking questions. Do not proceed to planning/implementation until open questions are resolved or explicitly accepted as risks and recorded.

## Overview

- Goal (in user terms):
- Primary user(s):
- Desired outcome:

## User Story

Derive the user story from the user's described feature/bugfix via the discovery back-and-forth.

- In Pass 1, it is acceptable for the user story to be a first draft.
- In Pass N, refine the user story as ambiguities are resolved.
- Always keep the user story consistent across:
  - `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
  - `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`

-

## In Scope

-

## Out of Scope

-

## Requirements

List requirements as outcomes/expectations, not implementation details.

### Functional Requirements

-

### Non-Functional Requirements

- Performance / latency:
- Security / permissions:
- Accessibility:
- Observability (logs/metrics/audit expectations):

## Acceptance Criteria

-

## Assumptions

-

## Open Questions

-

If this section is non-empty, also ask the user these questions at the end of your response.

Rules for asking questions:

- Do not ask A/B/C questions until `## User Story` is drafted.
- When you do ask A/B/C questions, explicitly reference the user story they relate to.

## Decisions Log

Capture resolved questions and selected options from the Clarify step.

- Decision:
  - Context:
  - Options considered:
  - Chosen:
  - Why:

## Validation Plan (User-Facing)

- How the user will verify "done":
- Rollout notes (if any):

## Review Questions (Answer Needed)

Include this section only when `## Open Questions` is non-empty.

Rules:

- Ask the minimum set of questions required to make the requirements complete and testable.
- Prefer multiple choice with 2–4 options (A/B/C/…) when it helps remove ambiguity; include tradeoffs.
- Do not use A/B/C until `## User Story` exists (in both docs) and your question is explicitly anchored to that story.
- If the user already answered in the conversation context, do not ask again; instead record the decision in `## Decisions Log` and remove it from `## Open Questions`.

-

Also:

- Ensure `/.project-workflow/TRACKER.md` has a row for `${input:taskId}` and set story `Status` to `Analysing` while requirements are being captured.
- Ensure `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md` exists and begins with a `## User Story` section at the very top.
  - If you need to create the file, keep it minimal (user story only, plus placeholders if required by repo convention).
  - Do not generate or populate any task list here.
- Create or update `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` with the contents of this output.

Guardrails:

- The requirements must be internally consistent (no contradictions across sections).
- Every item in `## Acceptance Criteria` must be verifiable in `## Validation Plan (User-Facing)`.
- Do not create or update implementation task lists in `IMPLEMENTATION.md` from this prompt; the `project.planner` prompt owns tasks.
- Do not move the story status past `Analysing` from this prompt.
