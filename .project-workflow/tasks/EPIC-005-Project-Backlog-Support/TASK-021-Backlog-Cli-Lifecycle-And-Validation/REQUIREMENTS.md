# Requirements

## Summary

- Task: TASK-021
- Title: Backlog CLI lifecycle and validation
- Parent AC Coverage: AC2, AC3, AC7
- Last updated: 2026-06-22

## Goal

Provide deterministic CLI commands for normal backlog row operations and validation so agents do not hand-edit lifecycle state or silently accept malformed backlog data.

## Non-Goals

- Creating task or epic promotion behavior.
- Interpreting broad product objectives into candidate backlog rows.
- Importing existing roadmap/backlog documents.
- Building custom status workflows or user-configurable vocabularies.

## Users & Context

- Agents need safe commands for adding, listing, updating, accepting, deferring, rejecting, superseding, and validating backlog rows.
- Owners need readable CLI output that explains the current backlog state and any remediation needed.
- Maintainers need validation coverage for malformed rows, invalid vocabulary, duplicates, and stale promotion references.

## Requirements (Outcome-Focused)

- Add a backlog CLI namespace for deterministic row operations.
- Support adding a row with required title/outcome and optional type, priority, status, and notes.
- Support listing backlog rows in a terminal-readable format.
- Support safe status updates using the accepted backlog status vocabulary.
- Support safe metadata updates for title, type, priority, outcome, promoted-to reference, and notes where appropriate.
- Validate required fields, duplicate `BL-###` IDs, invalid type values, invalid priority values, invalid status values, and promoted references that do not resolve to existing task or epic artifacts.
- Validation output should distinguish agent-actionable fixes from owner-input decisions where possible.
- CLI behavior should preserve the rule that backlog statuses are not implementation lifecycle statuses.

## Acceptance Criteria (Verifiable)

- AC1: `backlog add` or equivalent creates a new row with the next stable `BL-###` ID and valid default values.
- AC2: `backlog list` or equivalent prints existing rows without mutating the file.
- AC3: `backlog status` or equivalent enforces allowed status transitions/values and rejects invalid tracker-style statuses such as `In Progress` or `Complete`.
- AC4: `backlog update` or equivalent validates type and priority vocabulary before writing changes.
- AC5: `backlog validate` reports malformed tables, missing required fields, duplicate IDs, invalid type/priority/status values, and unresolved promoted references with actionable messages.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Keep backlog lifecycle commands simple and deterministic.
  - Why: The backlog should be easy for agents to operate without turning into a workflow engine.

- Decision: Allow exact CLI command names and flags to settle during implementation.
  - Why: The required behavior matters more than final ergonomics at requirements time.

## Validation Plan

- Add CLI fixture tests for add, list, status/update, validation failures, and promoted-reference resolution.
- Run invalid-value tests for type, priority, and status vocabulary.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-005 --id TASK-021`.
