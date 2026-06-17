# Requirements

## Summary

- Task: TASK-013
- Title: Agent Operated Guidance And Remediation
- Parent AC Coverage: AC11, AC13
- Last updated: 2026-06-17

## Goal

Make generated agent guidance and gate failures support the owner-directed, agent-operated workflow model.

## Non-Goals

- Building an interactive UI for question asking.
- Replacing owner approval with model inference.
- Changing every historical prompt unrelated to workflow operation.

## Users & Context

- Owners provide judgment and decisions.
- Agents run commands and maintain artifacts.
- Gate failures should help the agent decide what to gather, what to infer, and when to stop for owner input.

## Requirements (Outcome-Focused)

- Agent assets define the role split clearly.
- Implementation guidance requires readiness checks before coding.
- Epic guidance requires readiness checks before decomposition and child implementation/testing.
- Gate failures distinguish owner input from agent action.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-003 AC11 by updating generated agent guidance with the owner-directed, agent-operated role split.
- AC2: Covers EPIC-003 AC13 by producing actionable remediation categories in readiness failures.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Gate failures should be useful prompts for the agent.
  - Why: The model is the workflow operator and needs actionable next steps.

## Validation Plan

- Run guidance fixture assertions.
- Run readiness failure tests.
- Inspect generated assets and installed mirrors.
