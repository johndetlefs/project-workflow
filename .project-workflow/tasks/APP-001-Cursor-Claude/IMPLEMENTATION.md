## User Story

As a repository maintainer running project initialization, I want to choose GitHub Copilot (default), Claude Code, or Cursor during `project init`, so that the scaffolded files are created in the folder and filename structure required by the selected agent.

## Goal

- Add agent-aware initialization so users can choose GitHub Copilot (default), Claude Code, or Cursor and receive the correct scaffold layout for the selected ecosystem, while preserving idempotent init behavior and keeping existing layouts when switching modes.

## Approach

- Extend initialization inputs with explicit agent selection and default-to-Copilot behavior.
- Centralize scaffold path/filename mapping per agent to avoid branching logic spread across command handlers.
- Preserve current conflict-handling and idempotency guarantees for every mode.
- Treat re-initialization with a different agent as additive, keeping both layouts.

## Phases

### Phase 1

- Changes: Add agent selection contract to init command and wire default mode to GitHub Copilot; introduce deterministic layout resolver for Copilot, Claude Code, and Cursor scaffold targets.
- Validation: Run init in fresh repos for each mode and verify expected top-level scaffold paths/files are created for that mode.
- Tracker updates: Keep story status `Analysing` while plan is reviewed.

### Phase 2

- Changes: Implement additive re-init behavior so switching modes keeps existing artifacts and adds missing layout for newly selected mode; ensure duplicate creation is avoided and conflict prompts still protect modified files.
- Validation: Re-run init in same repo across multiple modes, validate both layouts coexist, no duplicate artifacts appear, and modified files trigger existing conflict behavior.
- Tracker updates: Move to `Plan Confirmed` only after explicit user confirmation.

## Task List (for IMPLEMENTATION.md)

|  ID | Title                                   | Description                                                                                                                      | Acceptance Criteria                                                                                                                                                                                                                                                              | User Verification                                                                                                                                                                                                                                                                                                                                                                     | Status  |
| --: | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
|   1 | Agent-aware init selection              | Users can run init with an explicit agent mode and default to GitHub Copilot when no mode is provided.                           | - `project init` accepts supported agent choices: GitHub Copilot, Claude Code, Cursor.<br>- Running init without agent selection behaves as Copilot mode.<br>- CLI output states which agent mode was applied.                                                                   | - Run `project init` with no agent option and confirm output indicates Copilot mode.<br>- Run init with Claude and Cursor selections and confirm output shows selected mode.                                                                                                                                                                                                          | Testing |
|   2 | Canonical Claude Code scaffold          | Selecting Claude Code creates files in the canonical sub-agent structure expected by Claude Code.                                | - Claude mode scaffold matches https://code.claude.com/docs/en/sub-agents structure requirements.<br>- Existing Copilot scaffold contract remains unchanged in default mode.                                                                                                     | - In a fresh repo, run init in Claude mode and compare created folders/files to the Claude docs expectations.<br>- Run default init and confirm Copilot scaffold is unchanged from baseline.                                                                                                                                                                                          | To Do   |
|   3 | Canonical Cursor scaffold               | Selecting Cursor creates files in the canonical sub-agent structure expected by Cursor.                                          | - Cursor mode scaffold matches https://cursor.com/docs/context/subagents structure requirements.<br>- Existing Copilot scaffold contract remains unchanged in default mode.                                                                                                      | - In a fresh repo, run init in Cursor mode and compare created folders/files to the Cursor docs expectations.<br>- Run default init and confirm Copilot scaffold is unchanged from baseline.                                                                                                                                                                                          | To Do   |
|   4 | Additive re-initialization across modes | Re-running init with a different selected agent keeps existing layout and adds only required missing artifacts for the new mode. | - If repo is initialized in one mode, running init in another mode preserves existing mode layout.<br>- Newly selected mode artifacts are added without deleting prior artifacts.<br>- Re-running same mode remains idempotent and does not duplicate files.                     | - Initialize repo in Copilot mode, then run Claude mode; confirm both layouts exist and Copilot artifacts remain.<br>- In a separate fresh repo, initialize in Copilot mode, then run Cursor mode; confirm both layouts exist and Copilot artifacts remain.<br>- Re-run Claude mode in the first repo and Cursor mode in the second repo; confirm no duplicate artifacts are created. | To Do   |
|   5 | Preserve conflict and safety behavior   | File update safety and conflict prompts continue to protect user-modified files across all agent modes.                          | - Modified local scaffold files still trigger existing conflict flow when init would update them.<br>- Unmodified files update or remain unchanged per current behavior.<br>- No destructive overwrite occurs without explicit user choice where conflict prompting is expected. | - Modify a scaffold file, run init in same and different modes, and confirm conflict prompt behavior is preserved.<br>- Keep local version and verify file content remains user-modified.                                                                                                                                                                                             | To Do   |

## Files / Areas Likely to Change

- `src/project_workflow/cli.py` (init command arguments, agent selection flow, scaffold resolution)
- `src/project_workflow/prompts/*` (if agent-specific prompt packaging rules require variations)
- `src/project_workflow/templates/*` (agent-specific scaffold templates/paths)
- `README.md` (document new init option and mode behavior)

## Data / RLS / RPC / Migrations

- No database, RLS, RPC, or migration changes expected.

## Risks & Mitigations

- Risk: Ambiguity in external agent layout expectations can cause drift from official docs.<br>Mitigation: Encode layout mappings directly from official docs and validate in isolated fresh repos.
- Risk: Switching modes could unintentionally overwrite user-customized files.<br>Mitigation: Reuse existing conflict detection/prompting and avoid destructive migration logic.
- Risk: Added CLI options could reduce usability if unclear.<br>Mitigation: Provide explicit help text and init output showing selected agent mode.

## Notes

- Task: APP-001
- Title: Cursor & Claude
- Created: 2026-02-13
