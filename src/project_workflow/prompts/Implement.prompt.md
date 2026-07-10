---
name: project.implement
description: Implement a change with tracker status updates and an explicit validation plan.
argument-hint: taskId=TASK-330-Superuser workItem="#2" scope="..."
agent: agent
---

Use this prompt to make code changes.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- Repo-specific workflow guidance: [../../.project-workflow/guidance.md](../../.project-workflow/guidance.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical tracker: `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`
- Requirements source of truth: `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
- E2E exception rules (only if editing `front-end/apps/e2e/**`): [../instructions/e2e.instructions.md](../instructions/e2e.instructions.md)

Inputs:

- Task: `${input:taskId:TASK-000-Example}`
- Work item: `${input:workItem:#}`
- Scope: `${input:scope:What are we changing?}`

Defaults and inference:

- If `taskId` is omitted, infer it from the current branch name when possible (e.g., `feature/TASK-482-...` -> `TASK-482`).
- If `workItem` is omitted, infer the next work item with status `To do` in `/.project-workflow/TRACKER.md`; if none exist, default to `1`.
- If `scope` is omitted, default to: `Implement work item ${input:workItem} per REQUIREMENTS.md`.
- Only ask the user for missing inputs when inference is not possible.
- After inference, restate the inferred work item and scope as a hard boundary and proceed without extra confirmation.
- Do not implement, update, or mark status for any acceptance criteria outside the inferred `workItem`.
- If any change would touch a different work item, stop and ask for explicit user instruction.

Required workflow:

- Before coding, run the relevant ready gate:
  - standalone task: `./.project-workflow/cli/workflow task ready --id ${input:taskId}`
  - epic child: `./.project-workflow/cli/workflow epic ready-child --epic-id <EPIC_ID> --id ${input:taskId}`
- If the ready gate fails, remediate the listed requirements/planning/clarification/approval/evidence gaps or ask the owner only for the specific material decision required. Do not code from an unapproved or stale requirements/AC envelope.
- If approval is missing or stale after requirements and ACs are ready, record the one owner-approved envelope with `task approve-requirements` or `epic approve-requirements` as applicable; do not treat the implementation request itself as approval.
- Before coding, move the relevant row to `In Progress` with the workflow CLI. For unchanged work inside an approved envelope, do not ask for repeated owner approval.
- After implementation, run the relevant status command to move the row to `Testing`.
- Do not set it to `Complete`; completion is owned by `project.qa-review` after QA/code review passes and the user explicitly approves completion.

Sequence enforcement:

- Do NOT ask whether to “move on” or start the next work item until you have completed the Validation step for the current work item.
- The next step after implementation is always Validation: run the most relevant automated checks (tests/typecheck/lint) and perform any required manual verification steps.
- Only after you have (1) executed validation, (2) summarized results, and (3) set the work item/story to `Testing`, may you ask for next-step instructions.
- The next lifecycle step after `Testing` is `project.qa-review`.

Requirements guardrails:

- Before coding, read `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` and treat it as the source of truth for outcomes and expectations.
- If the task is an epic child, also read the parent epic `EPIC-CONTRACT.md`, `DECOMPOSITION.md`, `AMENDMENTS.md`, and the child `Child Charter`; those define inherited invariants, invalid substitutes, artifact targets, and proof ownership.
- If `REQUIREMENTS.md` does not exist yet, stop and instruct the user to run the `project.requirements` prompt to create it.
- If you discover a conflict between the current codebase constraints and `REQUIREMENTS.md` (or the `## User Story` in `IMPLEMENTATION.md`), stop and route to the `project.clarify` prompt; after the user chooses an option, ensure the decision is recorded in `REQUIREMENTS.md` before continuing.
- Before coding, list the AC IDs in the inferred `workItem` and map each planned change to them. If any change does not map to an AC ID, do not proceed.
- Before coding, cross-check the inferred work-item acceptance criteria against `REQUIREMENTS.md` and `IMPLEMENTATION.md`; if they conflict, stop and route to `project.clarify` and record the decision in `REQUIREMENTS.md`.
- Before coding, identify any triggered proof recipes. Visual/reference-fidelity work must have calibration before implementation; runtime/deployment/source work must identify the exact target/source pair to prove. If the required recipe or artifact identity is missing, stop and fix the workflow artifacts before coding.

User story tracker workflow:

- `/.project-workflow/TRACKER.md` is part of the process and must be kept up-to-date.
- Before coding, ensure there is a story row for `${input:taskId}` and move story `Status` to `In Progress` with the lifecycle command.
- After implementation (when the work item is set to `Testing`), move story `Status` to `Testing` with the lifecycle command.
- Do not set story `Status` to `Complete` from this prompt. Route to `project.qa-review` for completion approval.

Implementation doc structure:

- Ensure `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md` begins with a `## User Story` section at the very top (with acceptance criteria). If it’s missing, add it.

Output expectations:

- Make the smallest safe change that satisfies the requirement.
- Add or update tests when appropriate.
- If requirements or material claims trigger a proof recipe, create or update child-local `EVIDENCE.json` with the structured claim record and evidence artifact path. Do not rely on implementation prose, tests, builds, or a surrogate artifact for recipe-specific proof.
- Provide a short validation checklist (commands + manual steps) and call out any risks.
- Tell the user that QA/code review is the next required step before completion.

Validation execution requirement:

- Do not merely propose validation commands—run them using available repo tools (e.g. `run_task`, `runTests`, terminal) and report the results.
- If a broad check (e.g. whole-app typecheck) fails due to pre-existing issues unrelated to your change, do not stop early: still validate what you changed with the narrowest meaningful checks available (package-level typecheck, targeted tests, file-level checks) and clearly state the limitation.
- After tracker or task-doc updates, run `./.project-workflow/cli/workflow doctor` when available and report any workflow-state warnings or errors.

Validation alignment guardrail:

- Use `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md` as the validation checklist source of truth.
- Explicitly map each `## Acceptance Criteria` item by AC ID (and any must-have `## Requirements`) to at least one validation step (automated test, manual verification, or query).
- After running validation, report results in AC-by-AC form (`AC1 -> validation evidence/result`, `AC2 -> ...`) for the current work item.
- If a requirement is not verifiable, stop and route to Clarify to make it testable and record the decision/update in `REQUIREMENTS.md`.

E2E exception:

- If you are working under `front-end/apps/e2e/**`, maintain the suite-local `implementation.md` per the E2E instructions.
