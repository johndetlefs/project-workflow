---
name: project.epic
description: Manage epic lifecycle (init, decompose, approve, scaffold child).
argument-hint: action=init|decompose|approve|scaffold-child title="..." epicId=EPIC-001 id=TASK-001
agent: agent
---

Use this prompt to run epic workflow operations through the local workflow CLI.

Inputs:

- Action: `${input:action:init|decompose|approve|scaffold-child}`
- Epic title (required for `init`): `${input:title:}`
- Epic ID (required for all non-init actions): `${input:epicId:EPIC-001}`
- Row ID (required for `approve` and `scaffold-child`): `${input:id:TASK-014}`
- Decompose limit (optional, default 5): `${input:limit:5}`
- Decompose type (optional, default Task): `${input:type:Task}`
- Create branch for scaffold-child (optional): `${input:createBranch:no}`
- Epic branch for scaffold-child branch creation (optional, default epic/main): `${input:epicBranch:epic/main}`
- Branch prefix for scaffold-child branch creation (optional, default feature/): `${input:branchPrefix:feature/}`

Defaults and inference:

- If action is omitted, infer from provided inputs:
  - `title` only -> `init`
  - `epicId` + no `id` -> `decompose`
  - `epicId` + `id` + intent to approve -> `approve`
  - `epicId` + `id` + intent to scaffold -> `scaffold-child`
- If inference is unclear, ask one clarifying question and stop.

Required preflight for `init`:

- Never run `init` with an implicit/default title.
- If `title` is missing, empty, or still a placeholder/example value, ask exactly one clarifying question for the epic title and stop.
- If action is `init` and title is provided, echo the exact title back before executing.

Execution:

- Run from repo root using the local workflow script:

`./.project-workflow/cli/workflow epic <subcommand> ...`

- Action mappings:
  - `init`:

`./.project-workflow/cli/workflow epic init --title "<TITLE>"`

- `decompose`:

`./.project-workflow/cli/workflow epic decompose --epic-id <EPIC_ID> --limit <LIMIT> --type <TYPE>`

- `approve`:

`./.project-workflow/cli/workflow epic approve --epic-id <EPIC_ID> --id <ROW_ID>`

- `scaffold-child` without branch:

`./.project-workflow/cli/workflow epic scaffold-child --epic-id <EPIC_ID> --id <ROW_ID>`

- `scaffold-child` with branch:

`./.project-workflow/cli/workflow epic scaffold-child --epic-id <EPIC_ID> --id <ROW_ID> --create-branch --epic-branch <EPIC_BRANCH> --branch-prefix <PREFIX>`

Constraints to enforce in responses:

- Decomposition is proposal-first: it writes Proposed rows and does not scaffold child folders.
- Approval gate: only Approved rows may be scaffolded.
- Child task IDs remain globally unique and are managed by workflow behavior.
- If branch creation is requested for `scaffold-child`, the epic branch must already exist; no fallback branch is allowed.

Output to user:

- Report the exact command run.
- Summarize resulting epic/task ID, files/folders created, tracker updates, and branch result (if any).
- If command fails, return the error and the next remediation step from the error message.
