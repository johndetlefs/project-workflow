# Requirements

## Summary

- Task: TASK-020
- Title: Backlog artifact, schema, and init support
- Parent AC Coverage: AC1, AC2, AC3
- Last updated: 2026-06-22

## Goal

Create the canonical backlog artifact and schema foundation so initialized repositories have a safe `.project-workflow/BACKLOG.md` that can hold future intent without becoming a second execution tracker.

## Non-Goals

- Adding the full backlog command lifecycle beyond init/schema helpers.
- Promoting backlog rows into tasks or epics.
- Creating generated agent prompts or documentation beyond schema text that belongs inside the backlog artifact.
- Importing or transforming existing roadmap/backlog documents.

## Users & Context

- Repo owners need a durable, versioned backlog file to capture future ideas before they are ready for task or epic workflow.
- Agents need a stable table schema and vocabulary so backlog rows can be parsed and validated consistently.
- Existing repositories need safe init behavior that creates the backlog only when missing and never overwrites user-owned backlog state.

## Requirements (Outcome-Focused)

- `project init` creates `.project-workflow/BACKLOG.md` when it is missing.
- Existing `.project-workflow/BACKLOG.md` files are treated as user-owned state and are not overwritten during init refresh.
- The default backlog file documents the canonical table columns: `ID`, `Title`, `Type`, `Priority`, `Status`, `Outcome`, `Promoted To`, and `Notes`.
- The default backlog file documents the allowed type values: `Idea`, `Task Candidate`, `Epic Candidate`, `Discovery`, and `Follow-Up`.
- The default backlog file documents the allowed priority values: `High`, `Medium`, `Low`, and `Unset`.
- The default backlog file documents the allowed status values: `Proposed`, `Accepted`, `Deferred`, `Rejected`, `Superseded`, and `Promoted`.
- The default backlog file states that active execution status belongs in `.project-workflow/TRACKER.md` or epic trackers after promotion.
- Shared parser/allocation helpers should support stable `BL-###` ID allocation without colliding with existing backlog rows.

## Acceptance Criteria (Verifiable)

- AC1: Running `project init` in a repository without `.project-workflow/BACKLOG.md` creates a backlog file with the required columns and documented vocabularies.
- AC2: Running `project init` in a repository with an existing `.project-workflow/BACKLOG.md` leaves that file unchanged.
- AC3: The backlog schema supports stable `BL-###` ID allocation from existing rows, and duplicate existing IDs are detectable by shared backlog parsing helpers or validation hooks.
- AC4: The generated backlog artifact clearly states that `Accepted` is not implementation-ready and that execution lifecycle status belongs in tracker/task/epic artifacts.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Treat `.project-workflow/BACKLOG.md` as user-owned workflow state, not a generated asset.
  - Why: Users and agents will update backlog rows over time, so init refresh must preserve it like `TRACKER.md`.

- Decision: Keep the initial schema as a Markdown table.
  - Why: This matches project-workflow's repository-native design and remains easy for all supported agents to read.

## Validation Plan

- Add tests for missing-backlog init creation and existing-backlog preservation.
- Add tests or helper coverage for `BL-###` ID allocation from existing rows.
- Run `project init` fixture checks for generated backlog content.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-005 --id TASK-020`.
