# Requirements

## Summary

- Task: TASK-024
- Title: Cross-agent docs and generated asset alignment
- Parent AC Coverage: AC1, AC3, AC8, AC9
- Last updated: 2026-06-22

## Goal

Expose backlog support consistently through every generated agent mode and user-facing documentation so all supported models operate the same backlog lifecycle.

## Non-Goals

- Implementing core backlog CLI mechanics.
- Writing every task/epic promotion test.
- Adding integrations with external planning tools.
- Changing unrelated project-workflow prompts or skills beyond references needed for backlog placement.

## Users & Context

- Users may initialize project-workflow for GitHub Copilot, Claude Code, OpenAI Codex, or Cursor.
- Agents in each environment need consistent instructions for backlog creation, refinement, validation, and promotion.
- Maintainers need generated assets, README examples, and installed helper guidance to stay aligned.

## Requirements (Outcome-Focused)

- Add a backlog prompt/agent/skill asset to every supported agent mode.
- Update shared agent guidance so `project.backlog` is discoverable alongside constitution, task, epic, requirements, planner, clarify, implement, QA review, delegate, and retro.
- Update Codex `AGENTS.md` managed block guidance and local skill map to include backlog behavior.
- Update Cursor rules to explain where backlog sits in workflow order and how agents should use it.
- Update README file-structure, typical workflow, and examples to explain backlog placement and lifecycle.
- Generated assets should consistently state that backlog is optional and sits between constitution and tracker.
- Generated assets should consistently state that backlog rows remain after promotion and execution status moves to task/epic trackers.
- Generated assets should mention existing roadmap/backlog docs are preserved and migration should be repo-local, not automatic.

## Acceptance Criteria (Verifiable)

- AC1: GitHub Copilot prompt generation includes a `project.backlog` prompt or equivalent asset.
- AC2: Claude Code agent generation includes a `project-backlog` agent or equivalent asset.
- AC3: OpenAI Codex generation includes a `project-backlog` skill and managed block guidance.
- AC4: Cursor generation includes a `project-backlog` agent or equivalent asset and updated project-workflow rule guidance.
- AC5: README explains backlog placement relative to constitution, tracker, tasks, and epics, including creation, acceptance, promotion, and traceability examples.
- AC6: Generated guidance consistently states that promoted rows remain in the backlog and active execution status belongs in tracker/task/epic artifacts.
- AC7: Generated guidance consistently states that existing roadmap/backlog docs are preserved and not automatically imported.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Add backlog as a peer workflow command/skill, not as part of `project.task`.
  - Why: Backlog is a distinct pre-commitment layer, while task and epic are executable workflow state.

- Decision: Keep README examples concise and operational.
  - Why: The feature should be easy to adopt without turning docs into a planning manual.

## Validation Plan

- Add generated asset presence checks where current tests cover prompt/skill generation.
- Inspect README and generated mode-specific assets after init refresh.
- Run `project init --agent` checks for each supported mode when feasible.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-005 --id TASK-024`.
