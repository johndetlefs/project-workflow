---
name: project.implement
description: Implement a change with tracker status updates and an explicit validation plan.
argument-hint: taskId=APP-330-Superuser workItem="#2" scope="..."
agent: agent
---

Use this prompt to make code changes.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical tracker: `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`
- Requirements source of truth: `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
- E2E exception rules (only if editing `front-end/apps/e2e/**`): [../instructions/e2e.instructions.md](../instructions/e2e.instructions.md)

Inputs:

- Task: `${input:taskId:APP-000-Example}`
- Work item: `${input:workItem:#}`
- Scope: `${input:scope:What are we changing?}`

Defaults and inference:

- If `taskId` is omitted, infer it from the current branch name when possible (e.g., `feature/APP-482-...` -> `APP-482`).
- If `workItem` is omitted, infer the next work item with status `To do` in `/.project-workflow/TRACKER.md`; if none exist, default to `1`.
- If `scope` is omitted, default to: `Implement work item ${input:workItem} per REQUIREMENTS.md`.
- Only ask the user for missing inputs when inference is not possible.
- After inference, restate the inferred work item and scope as a hard boundary and proceed without extra confirmation.
- Do not implement, update, or mark status for any acceptance criteria outside the inferred `workItem`.
- If any change would touch a different work item, stop and ask for explicit user instruction.

Required workflow:

- Before coding, set the specific tracker row to `In Progress`.
- After implementation, set it to `Testing`.
- Only set it to `Complete` after validation is confirmed AND the user explicitly instructs you to mark it `Complete`.

Sequence enforcement:

- Do NOT ask whether to “move on” or start the next work item until you have completed the Validation step for the current work item.
- The next step after implementation is always Validation: run the most relevant automated checks (tests/typecheck/lint) and perform any required manual verification steps.
- Only after you have (1) executed validation, (2) summarized results, and (3) set the work item/story to `Testing`, may you ask for next-step instructions.

Requirements guardrails:

- Before coding, read `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` and treat it as the source of truth for outcomes and expectations.
- If `REQUIREMENTS.md` does not exist yet, stop and instruct the user to run the `project.requirements` prompt to create it.
- If you discover a conflict between the current codebase constraints and `REQUIREMENTS.md` (or the `## User Story` in `IMPLEMENTATION.md`), stop and route to the `project.clarify` prompt; after the user chooses an option, ensure the decision is recorded in `REQUIREMENTS.md` before continuing.
- Before coding, list the acceptance criteria in the inferred `workItem` and map each planned change to them. If any change does not map, do not proceed.
- Before coding, cross-check the inferred work-item acceptance criteria against `REQUIREMENTS.md` and `IMPLEMENTATION.md`; if they conflict, stop and route to `project.clarify` and record the decision in `REQUIREMENTS.md`.

User story tracker workflow:

- `/.project-workflow/TRACKER.md` is part of the process and must be kept up-to-date.
- Before coding, ensure there is a story row for `${input:taskId}` and set story `Status` to `In Progress`.
- After implementation (when the work item is set to `Testing`), set story `Status` to `Testing`.
- Only set story `Status` to `Complete` after validation is confirmed AND the user explicitly instructs you to mark it `Complete`.

Implementation doc structure:

- Ensure `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md` begins with a `## User Story` section at the very top (with acceptance criteria). If it’s missing, add it.

Output expectations:

- Make the smallest safe change that satisfies the requirement.
- Add or update tests when appropriate.
- Provide a short validation checklist (commands + manual steps) and call out any risks.

Validation execution requirement:

- Do not merely propose validation commands—run them using available repo tools (e.g. `run_task`, `runTests`, terminal) and report the results.
- If a broad check (e.g. whole-app typecheck) fails due to pre-existing issues unrelated to your change, do not stop early: still validate what you changed with the narrowest meaningful checks available (package-level typecheck, targeted tests, file-level checks) and clearly state the limitation.

Validation alignment guardrail:

- Use `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` as the validation checklist source of truth.
- Explicitly map each `## Acceptance Criteria` item (and any must-have `## Requirements`) to at least one validation step (automated test, manual verification, or query).
- After running validation, report results in AC-by-AC form (`AC -> validation evidence/result`) for the current work item.
- If a requirement is not verifiable, stop and route to Clarify to make it testable and record the decision/update in `REQUIREMENTS.md`.

E2E exception:

- If you are working under `front-end/apps/e2e/**`, maintain the suite-local `implementation.md` per the E2E instructions.
