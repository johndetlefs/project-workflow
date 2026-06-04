---
name: project.retro
description: Run the post-completion retro to keep conventions, agent guidance, and workflow assets current.
argument-hint: taskId=TASK-330-Superuser focus="conventions, agents, follow-ups"
agent: agent
---

Use this prompt after a task has passed QA/code review and has been marked `Complete`.

Purpose:

- Capture reusable lessons from the finished task.
- Update durable repo conventions, agent instructions, prompts, skills, or workflow rules when the task exposed a repeatable gap.
- Keep future tasks internally consistent without adding one-off implementation details to global guidance.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- Repo-specific workflow guidance: [../../.project-workflow/guidance.md](../../.project-workflow/guidance.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical task tracker: `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`
- Requirements source of truth: `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
- Project outcomes: [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)
- Agent definitions: `/.github/prompts/`, `/AGENTS.md`, `/.agents/skills/`, and `/.cursor/rules/` when present

Inputs:

- Task: `${input:taskId:TASK-000-Example}`
- Focus: `${input:focus:What should the retro pay attention to?}`

Required workflow:

1. Read the completed task's `REQUIREMENTS.md`, `IMPLEMENTATION.md`, QA/code review notes, and tracker row.
2. Confirm the task is already `Complete`. If not, stop and direct the user to finish `project.qa-review` and explicit completion first.
3. Inspect the final diff and decisions for reusable lessons:
   - repo conventions or coding patterns that should be documented
   - recurring validation commands or QA checks
   - agent prompt/skill gaps that caused drift or rework
   - project-workflow lifecycle rules that need tightening
   - follow-up work that should become a separate task
4. Decide where each durable update belongs:
   - product outcomes: `.project-workflow/CONSTITUTION.md`
   - technical conventions: `.project-workflow/guidance.md`, `AGENTS.md`, `.github/copilot-instructions.md`, or equivalent repo guidance
   - Copilot workflow behavior: `.github/prompts/*.prompt.md`
   - Codex workflow behavior: `.agents/skills/project-*/SKILL.md`
   - Cursor workflow behavior: `.cursor/rules/project-workflow.mdc`
   - packaged project-workflow templates, when working in this repository: `src/project_workflow/**`
5. Make only durable, generally useful updates. Do not encode task-specific implementation details as global rules.
6. Record the retro in `IMPLEMENTATION.md` under `## Retro` with:
   - date
   - reusable lessons
   - conventions or agent assets updated
   - follow-up task suggestions, if any
   - "No durable updates needed" when nothing should change
7. If follow-up work is needed, propose a new task rather than reopening the completed task.

Output expectations:

- Summarize convention/agent changes made.
- List any files updated.
- List proposed follow-up tasks separately.
- Leave the completed task status as `Complete` unless the user explicitly asks to reopen it.

Guardrails:

- Retro is a maintenance step, not a new implementation phase.
- Do not change accepted requirements after completion; create a follow-up task for new scope.
- If a convention update would materially change project direction, ask before editing product-level guidance.
