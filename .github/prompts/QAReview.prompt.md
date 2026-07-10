---
name: project.qa-review
description: Run the QA and code review gate after implementation validation, before completion.
argument-hint: taskId=TASK-330-Superuser scope="review changed work"
agent: agent
---

Use this prompt after `project.implement` has made changes and moved the task or work item to `Testing`.

Purpose:

- Independently verify the implemented work against requirements and acceptance criteria.
- Review the changed code for correctness, maintainability, security, data safety, and scope control.
- Record review results before any task is marked `Complete`.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- Repo-specific workflow guidance: [../../.project-workflow/guidance.md](../../.project-workflow/guidance.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical task tracker: `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`
- Requirements source of truth: `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
- Project outcomes: [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)

Inputs:

- Task: `${input:taskId:TASK-000-Example}`
- Scope: `${input:scope:What changed or what should be reviewed?}`

Defaults and inference:

- If `taskId` is omitted, infer it from the current branch name when possible.
- If `scope` is omitted, review the current uncommitted diff plus the task docs.
- Ask only when the task cannot be inferred safely.

Required workflow:

1. Read `REQUIREMENTS.md`, `IMPLEMENTATION.md`, and the tracker row for the task.
2. Confirm implementation has reached `Testing`. If it has not, stop and direct the user to run `project.implement` first.
3. Run the relevant workflow status command to move the row to `Review` before starting QA/code review:
   - standalone task: `./.project-workflow/cli/workflow task status --id ${input:taskId} --to Review`
   - epic child: `./.project-workflow/cli/workflow epic status --epic-id <EPIC_ID> --id ${input:taskId} --to Review`
4. Inspect the changed files and map each acceptance criterion ID to evidence:
   - automated test, typecheck, lint, build, or script result
   - manual verification result
   - code inspection finding
5. If a requirement, acceptance criterion, child charter, epic contract, or material claim triggers a proof recipe, inspect child-local `EVIDENCE.json` and the referenced evidence artifact before accepting the claim. Visual/reference fidelity requires rendered comparison against the delivered user-facing artifact, not code review, tests, build output, or a surrogate surface. Runtime target/source proof requires the exact target/source pair and positive proof that target used that source.
6. Run any missing narrow validation that is necessary to support the review. Do not ask the user to manually test behavior that the agent can validate directly with available commands, tests, scripts, browser tools, screenshots, or local tools. Do not rerun broad checks unless they are the most meaningful available check.
7. Review code for:
   - correctness against requirements and decisions
   - unintended scope expansion
   - error handling and edge cases
   - security, permissions, privacy, and data integrity
   - migrations, rollback, observability, and operational risk where relevant
   - tests and documentation appropriate to the change
8. Record results in `IMPLEMENTATION.md` under `## QA & Code Review` with:
   - date
   - reviewer/agent context
   - files or areas reviewed
   - validation evidence
   - a clear distinction between verified evidence and deferred setup, owner-only actions, or unavailable connector/OAuth checks
   - findings, if any
   - verdict: `Pass`, `Pass with follow-ups`, or `Changes requested`
9. Run `./.project-workflow/cli/workflow doctor` when available and include any workflow-state warnings or errors in the review output.
10. If issues are found:
   - keep tracker status as `Review` or set it to `Blocked` if the issue prevents safe release
   - list findings first, ordered by severity, with file references where possible
   - do not mark anything `Complete`
11. If review passes:
   - say that QA/code review passed
   - only run the relevant workflow command to mark `Complete` if the user explicitly asked you to complete the task after review
   - otherwise leave status as `Review` and ask for explicit completion approval

Output expectations:

- Findings first when any exist.
- Validation evidence with exact commands or manual checks, reported by AC ID.
- A concise verdict.
- The next step is `project.retro` only after the task is marked `Complete`.

Guardrails:

- Do not mark `Complete` based on implementation validation alone. QA/code review must pass first.
- Do not use this prompt to implement new scope. Small review fixes are allowed only when they directly address review findings and remain within the accepted requirements.
- If review reveals a requirements conflict, route back to `project.clarify` and record the decision before continuing.
- Do not accept unsupported prose claims as closeout evidence. If prose claims contradict structured evidence, report the contradiction as a blocking finding.
