---
name: project.backlog
description: Capture, refine, validate, and promote optional project backlog items before they become task or epic workflow state.
argument-hint: action=add|list|status|update|validate|promote title="..." id=BL-001
agent: agent
---

Use this prompt to operate the optional project backlog in `.project-workflow/BACKLOG.md`.

Reference docs:

- Repo-specific workflow guidance: [../../.project-workflow/guidance.md](../../.project-workflow/guidance.md)
- Project outcomes: [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)
- Backlog: [../../.project-workflow/BACKLOG.md](../../.project-workflow/BACKLOG.md)
- Active tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)

Inputs:

- Action: `${input:action:add|list|status|update|validate|promote}`
- Backlog ID: `${input:id:BL-001}`
- Title: `${input:title:}`
- Outcome: `${input:outcome:}`
- Type: `${input:type:Idea|Task Candidate|Epic Candidate|Discovery|Follow-Up}`
- Priority: `${input:priority:High|Medium|Low|Unset}`
- Status: `${input:status:Proposed|Accepted|Deferred|Rejected|Superseded|Promoted}`
- Promotion target: `${input:promoteTo:task|epic}`

Backlog purpose:

- `CONSTITUTION.md` records durable product outcomes and principles.
- `BACKLOG.md` records future intent, rough priority, options, and promotion history.
- `TRACKER.md` and epic trackers record committed execution lifecycle state.
- Task/epic folders record executable requirements, plans, validation evidence, QA, and retros.

Rules:

- Backlog use is optional. If work is already clear and immediate, `project.task` or `project.epic` may be used directly.
- Do not use the backlog as a second active tracker.
- `Accepted` means worth keeping or preparing; it does not mean ready to implement.
- Promoted rows stay in the backlog with status `Promoted` and `Promoted To` set to the created `TASK-###` or `EPIC-###`.
- Existing roadmap/backlog documents outside `.project-workflow/BACKLOG.md` must be preserved. Do not import or transform them automatically; create a repo-local migration task if needed.
- Promotion requires owner confirmation. If the owner explicitly asks to accept and promote in one operation, pass `--accept`.

Broad-objective workflow:

1. Read project context first: `CONSTITUTION.md`, `BACKLOG.md` if present, `TRACKER.md`, active epic trackers, and `.project-workflow/guidance.md` if present.
2. Draft one or more outcome-focused candidate rows using the canonical schema: ID, Title, Type, Priority, Status, Outcome, Promoted To, Notes.
3. Recommend whether each candidate should remain an idea, become a task, become an epic, or require discovery.
4. Do not create tracker rows, task folders, or epic folders while only proposing candidates.
5. Ask for owner review before accepting rows or promoting them.
6. If context is insufficient, ask focused questions instead of inventing strategy.

CLI operations:

- Initialize backlog if missing:

`./.project-workflow/cli/workflow backlog init`

- Add a row:

`./.project-workflow/cli/workflow backlog add --title "<TITLE>" --outcome "<OUTCOME>" --type "Idea" --priority Unset`

- List rows:

`./.project-workflow/cli/workflow backlog list`

- Update status:

`./.project-workflow/cli/workflow backlog status --id BL-001 --to Accepted`

- Update fields:

`./.project-workflow/cli/workflow backlog update --id BL-001 --priority High --notes "<NOTES>"`

- Validate backlog:

`./.project-workflow/cli/workflow backlog validate`

- Promote an accepted row:

`./.project-workflow/cli/workflow backlog promote --id BL-001 --to task`

`./.project-workflow/cli/workflow backlog promote --id BL-001 --to epic`

Output:

- Report the exact command run.
- Summarize created or updated rows.
- For promotion, report the created `TASK-###` or `EPIC-###`, generated files, and backlog `Promoted To` reference.
- Run `./.project-workflow/cli/workflow doctor` after promotion or structural backlog edits and report warnings/errors.
