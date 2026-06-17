# Requirements

## Summary

- Task: TASK-011
- Title: Intake Sufficiency Model And Templates
- Parent AC Coverage: AC1, AC2, AC9, AC12
- Last updated: 2026-06-17

## Goal

Define the intake model and update user-facing and generated guidance so agents gather enough conversational context before downstream planning or implementation.

## Non-Goals

- Implementing readiness command internals.
- Changing external package release metadata.
- Requiring owners to manually fill templates.

## Users & Context

- Owners act as PM/BA and provide product judgment conversationally.
- Agents operate the workflow and need a clear minimum context rubric.
- Junior developers need guardrails that prevent vague prompts becoming implementation work.

## Requirements (Outcome-Focused)

- Intake guidance names the minimum context needed for task and epic work.
- User-facing documentation explains conversational intake rather than manual template completion.
- Generated prompts and skills tell agents to ask targeted questions and keep work in clarification when context is missing.
- Discovery work is recorded explicitly with bounded output and validation.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-003 AC1 by documenting the minimum context rubric.
- AC2: Covers EPIC-003 AC2 by guiding agents to stop or clarify when blocking context is missing.
- AC3: Covers EPIC-003 AC9 by updating generated lifecycle guidance.
- AC4: Covers EPIC-003 AC12 by making conversational owner input the normal user path.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Owner context is conversational, not template-first.
  - Why: The agent should operate the workflow while the owner supplies product judgment.

## Validation Plan

- Run generated guidance tests.
- Inspect README, prompts, Codex skills, and Cursor rules for the intake model.
- Run full test suite and doctor before closeout.
