# Requirements

## Overview

- Goal (in user terms): Let a user pick the target coding agent ecosystem during initialization so project scaffolding matches that ecosystem’s expected file layout.
- Primary user(s): Repository maintainers initializing workflow in a repo.
- Desired outcome: `project init` creates the correct folder/file structure for the selected agent, with GitHub Copilot as the default when no option is provided.

## User Story

As a repository maintainer running project initialization, I want to choose GitHub Copilot (default), Claude Code, or Cursor during `project init`, so that the scaffolded files are created in the folder and filename structure required by the selected agent.

## In Scope

- Add an agent selection input to initialization with supported values: GitHub Copilot, Claude Code, Cursor.
- Keep GitHub Copilot as the default behavior when no agent is provided.
- Scaffold prompts/workflow artifacts into the correct location and naming pattern for the selected agent.
- Keep `project init` idempotent and safe on re-run.

## Out of Scope

- Changing task lifecycle commands (`project task init`) beyond compatibility with selected scaffold layout.
- Adding support for agents beyond the three named in this story.
- Redesigning prompt content quality; this story is about placement/structure compatibility.

## Requirements

List requirements as outcomes/expectations, not implementation details.

### Functional Requirements

- `project init` allows selecting one agent target: GitHub Copilot, Claude Code, or Cursor.
- When agent is not specified, initialization behaves as GitHub Copilot mode.
- For each agent mode, generated scaffold files are created at the file paths and filenames expected by that agent tooling.
- Claude Code mode follows the custom agent structure defined by https://code.claude.com/docs/en/sub-agents.
- Cursor mode follows the custom agent structure defined by https://cursor.com/docs/context/subagents.
- Initialization output clearly confirms which agent mode was applied.
- If initialization is run again with a different agent mode, the CLI keeps both layouts.
- Re-running initialization does not duplicate files and preserves existing conflict-handling behavior.

### Non-Functional Requirements

- Performance / latency: Initialization time stays within the same practical range as current behavior for default mode.
- Security / permissions: No additional credentials, network access, or elevated permissions are required.
- Accessibility: CLI prompts/help text are clear and unambiguous for agent selection.
- Observability (logs/metrics/audit expectations): CLI output states selected agent and key scaffolded locations.

## Acceptance Criteria

- Running `project init` with no agent option scaffolds the existing GitHub Copilot layout and content contract.
- Running `project init` for each supported agent results in that agent’s expected folder and filename structure.
- Running `project init` for Claude Code mode creates artifacts matching the structure from https://code.claude.com/docs/en/sub-agents.
- Running `project init` for Cursor mode creates artifacts matching the structure from https://cursor.com/docs/context/subagents.
- Running `project init` with a different agent mode in an already-initialized repo keeps both layouts.
- Re-running `project init` for the same agent mode remains idempotent and does not create duplicate artifacts.
- If local files differ from packaged files, existing conflict resolution behavior is preserved.

## Assumptions

- Existing Copilot layout is the current baseline and must remain backward-compatible.
- Agent-specific layouts can be represented as deterministic path/file rules.

## Open Questions

- None.

## Decisions Log

- Decision:
  - Context: Agent choices required for initialization.
  - Options considered: GitHub Copilot only vs Copilot + Claude Code + Cursor.
  - Chosen: Support all three, with GitHub Copilot as default.
  - Why: Matches requested user outcome while preserving existing default behavior.

- Decision:
  - Context: Canonical structure definitions for non-Copilot agents.
  - Options considered: Define custom internal structure vs align to official agent docs.
  - Chosen: Use official structures from https://code.claude.com/docs/en/sub-agents and https://cursor.com/docs/context/subagents.
  - Why: Reduces ambiguity and ensures compatibility with each agent ecosystem.

- Decision:
  - Context: Behavior when a repo already initialized for one agent is initialized again for another.
  - Options considered: Keep both layouts vs migrate/replace vs fail with instructions.
  - Chosen: Keep both layouts.
  - Why: Matches requested behavior and avoids destructive migration.

## Validation Plan (User-Facing)

- How the user will verify “done”:
  - Run `project init` without agent selection and confirm Copilot-compatible scaffold is created.
  - Run initialization in fresh test repos for Claude Code and Cursor modes and confirm expected paths/filenames exist.
  - In an already-initialized repo, run initialization with a second agent mode and confirm existing layout is preserved while new layout is added.
  - Re-run initialization for each mode and confirm no duplicate artifacts are produced.
  - Modify a scaffolded file and re-run initialization to confirm conflict behavior still protects local edits.
- Rollout notes (if any): Start with Copilot-default parity checks, then validate Claude/Cursor layouts in isolated temp repos before release.
