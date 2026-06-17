---
name: project.epic
description: Manage epic lifecycle (init, decompose, approve, scaffold child, status, audit, closeout).
argument-hint: action=setup|init|decompose|approve|scaffold-child|status|audit|closeout title="..." epicId=EPIC-001 id=TASK-001
agent: agent
---

Use this prompt to run epic workflow operations through the local workflow CLI.

Read `/.project-workflow/guidance.md` if present before changing workflow state.

Inputs:

- Action: `${input:action:setup|init|decompose|approve|scaffold-child|status|audit|closeout}`
- Epic title (required for `init`): `${input:title:}`
- Epic ID (required for all non-init actions): `${input:epicId:EPIC-001}`
- Row ID (required for `approve` and `scaffold-child`): `${input:id:TASK-014}`
- Status target (required for `status`): `${input:status:Testing|Review|Complete}`
- Decompose limit (optional, default 5): `${input:limit:5}`
- Decompose type (optional, default Task): `${input:type:Task}`
- Create branch for scaffold-child (optional): `${input:createBranch:no}`
- Epic branch for scaffold-child branch creation (optional, default epic/main): `${input:epicBranch:epic/main}`
- Branch prefix for scaffold-child branch creation (optional, default feature/): `${input:branchPrefix:feature/}`

Defaults and inference:

- If action is omitted, infer from provided inputs:
  - `title` only -> `setup`
  - `epicId` + no `id` -> `decompose`
  - `epicId` + `id` + intent to approve -> `approve`
  - `epicId` + `id` + intent to scaffold -> `scaffold-child`
  - `epicId` + `id` + lifecycle intent -> `status`
  - `epicId` + intent to audit -> `audit`
  - `epicId` + intent to close -> `closeout`
- If inference is unclear, ask one clarifying question and stop.

Required preflight for `init`:

- Never run `init` with an implicit/default title.
- If `title` is missing, empty, or still a placeholder/example value, ask exactly one clarifying question for the epic title and stop.
- If action is `init` and title is provided, echo the exact title back before executing.

Guided setup mode (`action=setup`):

- Use this as the default for new epics in chat.
- Drive the complete lifecycle so users do not miss gates:
  1. Initialize epic.
  2. Verify epic requirements are ready for decomposition.
  3. Decompose into Proposed rows.
  4. Ask user which rows to approve.
  5. Optionally scaffold approved children.
- Ask at most one clarifying question at a time.
- After each completed step, explicitly state the next required step and offer to run it.

Requirements readiness gate (before `decompose`):

- Do not run `decompose` until epic `REQUIREMENTS.md` contains concrete, non-placeholder bullets under `## Requirements` and/or `## Acceptance Criteria`.
- Acceptance criteria should use stable IDs (`AC1`, `AC2`, etc.). Preserve existing IDs; do not renumber them unless the user explicitly approves the requirements change.
- If requirements are missing/skeletal, lead the user through filling them:
  - Ask focused questions to capture intended outcomes and verifiable criteria.
  - Update epic `REQUIREMENTS.md` with the provided answers.
  - Re-check readiness, then continue.
- If the user declines to provide requirements details, stop and explain that decomposition cannot proceed yet.

Requirements interview flow (when requirements are missing/skeletal):

- Ask exactly one question at a time and wait for the answer before continuing.
- Offer two input modes: (a) step-by-step answers, or (b) one pasted requirements/PRD block.
- If the user provides a large pasted block, treat it as preferred epic input (do not force short answers first).
- Capture, then write answers into epic `REQUIREMENTS.md` using these prompts in order:
  1. Goal: "What user/business outcome should this epic deliver?"
  2. Scope boundaries: "What is explicitly out of scope for this epic?"
  3. Requirements bullets: "List 3-7 outcome-focused requirements as bullets."
  4. Acceptance bullets: "List 3-7 verifiable acceptance criteria as bullets."
  5. Open questions: "What unknowns still need decisions?"
- Normalize answers into concise bullet points and replace placeholder lines like `- ____` in matching sections.
- Prefix acceptance criteria with stable IDs when writing them, for example `- AC1: <verifiable outcome>`.
- For pasted blocks, extract and map content into sections:
  - Product outcome/business goal -> `## Goal`
  - Platform/UX behavior statements -> `## Requirements (Outcome-Focused)`
  - Testable "As a user..." or acceptance statements -> `## Acceptance Criteria (Verifiable)`
  - Unknowns/dependencies/API notes -> `## Open Questions (Answer Needed)`
- Keep source fidelity: preserve critical terms, links, and proper nouns from the pasted text.
- If the pasted block includes desktop/mobile/backend variants, keep those distinctions explicit in the normalized bullets.
- Read back the drafted `## Requirements` and `## Acceptance Criteria` bullets and ask for confirmation before decomposition.
- Only proceed to `decompose` after user confirms the drafted requirements content.

Readiness minimums for decomposition:

- `## Requirements` has at least 3 non-placeholder bullet items, or `## Acceptance Criteria` has at least 3 non-placeholder bullet items.
- At least one acceptance bullet is objectively testable (contains a measurable or observable outcome).

Execution:

- Run from repo root using the local workflow script:

`./.project-workflow/cli/workflow epic <subcommand> ...`

- Action mappings:
  - `setup` (orchestrated flow):

`./.project-workflow/cli/workflow epic init --title "<TITLE>"`

`./.project-workflow/cli/workflow epic decompose --epic-id <EPIC_ID> --limit <LIMIT> --type <TYPE>`

`./.project-workflow/cli/workflow epic approve --epic-id <EPIC_ID> --id <ROW_ID>` (one or more user-selected rows)

`./.project-workflow/cli/workflow epic scaffold-child --epic-id <EPIC_ID> --id <ROW_ID> [--create-branch --epic-branch <EPIC_BRANCH> --branch-prefix <PREFIX>]` (optional)

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

- `status`:

`./.project-workflow/cli/workflow epic status --epic-id <EPIC_ID> --id <ROW_ID> --to <STATUS>`

- `audit`:

`./.project-workflow/cli/workflow epic audit --epic-id <EPIC_ID>`

- `closeout`:

`./.project-workflow/cli/workflow epic closeout --epic-id <EPIC_ID> [--complete]`

Constraints to enforce in responses:

- Decomposition is proposal-first: it writes Proposed rows and does not scaffold child folders.
- Proposed child rows should preserve source AC IDs in the epic tracker `Parent ACs` field when they come from numbered acceptance criteria. Legacy trackers may still carry coverage in `Notes` as `Covers AC1, AC3`.
- Scaffolded epic child tasks must carry parent AC coverage and parent AC evidence sections forward into their docs. Their `IMPLEMENTATION.md` planning table must map each row to child AC IDs while keeping the parent AC mapping visible.
- The global tracker summarizes epic rows; the epic tracker owns child rows. Proposed child rows must stay in the epic tracker and must not be added to the global tracker.
- `epic audit` writes `ACCEPTANCE-AUDIT.md` with parent AC coverage, child evidence, deferrals, and verdicts.
- `epic closeout` must block if any parent AC is unmapped, lacks evidence, lacks a QA pass verdict, or lacks an approved deferral with follow-up.
- `epic status --to Complete` must block unless the child row is in `Review` and its docs contain QA/code-review evidence plus parent AC evidence for its assigned parent ACs.
- Approval gate: only Approved rows may be scaffolded.
- Child task IDs remain globally unique and are managed by workflow behavior.
- If branch creation is requested for `scaffold-child`, the epic branch must already exist; no fallback branch is allowed.
- In setup mode, do not skip required gates even if the user asks for later steps first; explain what is missing, satisfy the gate, then continue.

Output to user:

- Report the exact command run (for setup mode, report each command in order).
- Summarize resulting epic/task ID, files/folders created, tracker updates, and branch result (if any).
- Run `./.project-workflow/cli/workflow doctor` after epic tracker or child scaffold changes and report any warnings or errors.
- If command fails, return the error and the next remediation step from the error message.
- In setup mode, also include a short checklist of completed steps and the single next recommended action.
