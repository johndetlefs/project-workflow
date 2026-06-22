# Requirements

## Summary

- Task: TASK-022
- Title: Backlog promotion to task and epic
- Parent AC Coverage: AC5, AC6
- Last updated: 2026-06-22

## Goal

Allow an owner-confirmed backlog row to become a normal project-workflow task or epic while preserving backlog traceability and all existing workflow gates.

## Non-Goals

- Implementing broad-objective candidate drafting.
- Importing legacy roadmap/backlog documents.
- Skipping requirements, planning, readiness, QA, or closeout gates after promotion.
- Creating branches during promotion unless an existing task/epic scaffold path explicitly supports and validates that behavior.

## Users & Context

- Owners need to choose when a backlog item becomes executable workflow state.
- Agents need a deterministic promotion command that updates the backlog row and creates the right task or epic artifact.
- Maintainers need promotion to reuse existing task/epic scaffolding semantics rather than creating a parallel workflow.

## Requirements (Outcome-Focused)

- Promotion to task creates a normal task folder, starter `REQUIREMENTS.md`, starter `IMPLEMENTATION.md`, and global tracker row using existing task scaffold semantics.
- Promotion to epic creates a normal epic folder, epic `REQUIREMENTS.md`, epic tracker, deferrals, retro, acceptance map, and global tracker row using existing epic scaffold semantics.
- Promotion requires the source row to be `Accepted`, unless the owner explicitly confirms accepting and promoting in the same operation.
- The promoted backlog row remains in `.project-workflow/BACKLOG.md`, changes to status `Promoted`, and records the created `TASK-###` or `EPIC-###` in `Promoted To`.
- Promoted task/epic requirements include a dedicated `## Backlog Source` section containing backlog ID, title, type, priority, outcome, notes, and original status context.
- Promotion should fail without partial writes when the backlog row is missing, already promoted, rejected, malformed, or has invalid required fields.
- Promotion should preserve the rule that active execution status after promotion lives in the tracker/task/epic artifacts, not in the backlog.

## Acceptance Criteria (Verifiable)

- AC1: Promoting an accepted backlog row to a task creates a normal task scaffold and global tracker row.
- AC2: Promoting an accepted backlog row to an epic creates a normal epic scaffold, epic tracker artifacts, acceptance map, and global tracker row.
- AC3: Successful promotion updates the backlog row to `Promoted` and writes the created task/epic ID into `Promoted To` while preserving the row.
- AC4: Promoted task and epic requirements include a populated `## Backlog Source` section.
- AC5: Promotion fails safely for missing, invalid, rejected, already-promoted, or non-accepted rows unless explicit one-step accept-and-promote confirmation is supplied.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Promotion should reuse existing task and epic scaffold logic.
  - Why: Promoted work should be indistinguishable from directly-created workflow work after the source context is recorded.

- Decision: Do not make branch creation part of initial backlog promotion.
  - Why: Existing branch creation has clean-tree and base-branch concerns that should not be hidden inside backlog promotion.

## Validation Plan

- Add promotion fixture tests for task and epic targets.
- Add failure-path tests for invalid row states and malformed backlog data.
- Inspect promoted requirements files for `## Backlog Source`.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-005 --id TASK-022`.
