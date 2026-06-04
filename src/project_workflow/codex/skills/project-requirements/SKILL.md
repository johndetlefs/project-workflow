---
name: project-requirements
description: Use when drafting or updating project-workflow REQUIREMENTS.md with user story, scope, acceptance criteria, decisions, and open questions.
---

# Project Requirements

Capture what is being built before planning or coding.

## Invocation Rules

- Use this skill whenever the user asks for requirements, scope, acceptance criteria, open questions, decisions, or a validation plan, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If the task folder does not exist, use `project-task` first so the CLI creates the required files and tracker row.
- After the task exists, requirements capture is a document workflow unless the CLI adds an explicit requirements command.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/CONSTITUTION.md` if present
- `.github/copilot-instructions.md` or `AGENTS.md` if present

## Workflow

1. Identify the task folder. If it does not exist, use `project-task` first.
2. Read existing `REQUIREMENTS.md` and the `## User Story` section of `IMPLEMENTATION.md`.
3. If the feature or bugfix is not clear, ask only for discovery context: what change, where in the product, who is affected, and what success looks like.
4. Draft or update `REQUIREMENTS.md` with:
   - Overview
   - User Story
   - Goal
   - Non-Goals
   - Users & Context
   - Outcome-focused requirements
   - Verifiable acceptance criteria
   - Open questions
   - Resolved decisions
   - Validation plan
5. Keep only the `## User Story` section in `IMPLEMENTATION.md` synced with `REQUIREMENTS.md`. Do not add implementation tasks here.
6. If critical requirements are ambiguous, record them as open questions in `REQUIREMENTS.md`, then ask the user the minimum questions needed.
7. Do not proceed to planning or implementation until open questions are resolved or explicitly accepted as risks and recorded.
