---
name: project.qa-review
description: Run the QA and code review gate after implementation validation, before completion.
argument-hint: taskId=APP-330-Superuser scope="review changed work"
agent: agent
---

Use this prompt after `project.implement` has made changes and moved the task or work item to `Testing`.

Purpose:

- Independently verify the implemented work against requirements and acceptance criteria.
- Review the changed code for correctness, maintainability, security, data safety, and scope control.
- Record review results before any task is marked `Complete`.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical task tracker: `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`
- Requirements source of truth: `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
- Project outcomes: [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)

Inputs:

- Task: `${input:taskId:APP-000-Example}`
- Scope: `${input:scope:What changed or what should be reviewed?}`

Defaults and inference:

- If `taskId` is omitted, infer it from the current branch name when possible.
- If `scope` is omitted, review the current uncommitted diff plus the task docs.
- Ask only when the task cannot be inferred safely.

Required workflow:

1. Read `REQUIREMENTS.md`, `IMPLEMENTATION.md`, and the tracker row for the task.
2. Confirm implementation has reached `Testing`. If it has not, stop and direct the user to run `project.implement` first.
3. Set the tracker row to `Review` before starting QA/code review.
4. Inspect the changed files and map each acceptance criterion to evidence:
   - automated test, typecheck, lint, build, or script result
   - manual verification result
   - code inspection finding
5. Run any missing narrow validation that is necessary to support the review. Do not rerun broad checks unless they are the most meaningful available check.
6. Review code for:
   - correctness against requirements and decisions
   - unintended scope expansion
   - error handling and edge cases
   - security, permissions, privacy, and data integrity
   - migrations, rollback, observability, and operational risk where relevant
   - tests and documentation appropriate to the change
7. Record results in `IMPLEMENTATION.md` under `## QA & Code Review` with:
   - date
   - reviewer/agent context
   - files or areas reviewed
   - validation evidence
   - findings, if any
   - verdict: `Pass`, `Pass with follow-ups`, or `Changes requested`
8. If issues are found:
   - keep tracker status as `Review` or set it to `Blocked` if the issue prevents safe release
   - list findings first, ordered by severity, with file references where possible
   - do not mark anything `Complete`
9. If review passes:
   - say that QA/code review passed
   - only set the tracker row to `Complete` if the user explicitly asked you to complete the task after review
   - otherwise leave status as `Review` and ask for explicit completion approval

Output expectations:

- Findings first when any exist.
- Validation evidence with exact commands or manual checks.
- A concise verdict.
- The next step is `project.retro` only after the task is marked `Complete`.

Guardrails:

- Do not mark `Complete` based on implementation validation alone. QA/code review must pass first.
- Do not use this prompt to implement new scope. Small review fixes are allowed only when they directly address review findings and remain within the accepted requirements.
- If review reveals a requirements conflict, route back to `project.clarify` and record the decision before continuing.
