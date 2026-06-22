# Requirements

## Summary

- Task: TASK-023
- Title: Broad-objective backlog proposal workflow
- Parent AC Coverage: AC4, AC8
- Last updated: 2026-06-22

## Goal

Define the agent-operated workflow for turning a broad user objective into proposed backlog rows without automatically creating tracker work or bypassing owner review.

## Non-Goals

- Implementing deterministic CLI row mutation beyond calling the backlog commands created by other tasks.
- Creating all cross-agent packaging and README updates.
- Promoting rows into task or epic scaffolds.
- Asking owners to manually fill backlog templates as the normal path.

## Users & Context

- Owners often describe future work conversationally rather than as clean task specs.
- Agents need instructions for reading project context, drafting candidate rows, and recommending whether items look like ideas, task candidates, epic candidates, discovery work, or follow-ups.
- Maintainers need the proposal workflow to avoid accidental tracker mutation from broad prompts.

## Requirements (Outcome-Focused)

- The backlog workflow should support a broad objective input such as "capture future project backlog support" or "add post-launch planning improvements."
- The agent should read relevant project context before drafting candidates: constitution, existing backlog if present, global tracker, active epics, and repo guidance.
- The agent should propose one or more backlog rows with title, type, priority, status, outcome, notes, and source context.
- Proposed candidates should be outcome-focused and should avoid implementation-step titles unless the user asked for a narrow technical task.
- The agent should recommend whether each candidate is likely to remain an idea, become a task, become an epic, or require discovery.
- The agent should not add rows to `TRACKER.md` while creating or proposing backlog candidates.
- The agent should ask for owner confirmation before accepting or promoting candidate rows.
- If the broad objective lacks enough context to produce useful candidates, the agent should ask focused questions rather than inventing strategy.

## Acceptance Criteria (Verifiable)

- AC1: Generated backlog workflow guidance tells agents to read project context before drafting backlog candidates.
- AC2: Generated backlog workflow guidance tells agents to produce outcome-focused candidate rows with the canonical schema.
- AC3: Generated backlog workflow guidance forbids automatic tracker/task/epic creation during candidate proposal.
- AC4: Generated backlog workflow guidance requires owner review before candidate acceptance or promotion.
- AC5: Guidance includes a fallback for insufficient context: ask focused questions rather than inventing backlog strategy.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Broad-objective decomposition is an agent workflow, not a deterministic CLI algorithm.
  - Why: Product strategy and candidate grouping require judgment from context and owner intent.

- Decision: Candidate proposal may be conversational before rows are written.
  - Why: The owner should be able to reject or reshape candidates before canonical backlog state changes.

## Validation Plan

- Add generated-asset assertions for context-reading, owner-review, and no-tracker-mutation guidance.
- Dogfood the workflow with one broad objective after backlog commands exist.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-005 --id TASK-023`.
