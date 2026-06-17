# Requirements

## Summary

- Task: TASK-018
- Title: Minimal Epic Status Lifecycle
- Parent AC Coverage: AC4
- Last updated: 2026-06-17

## Goal

Add a minimal CLI-supported lifecycle for global epic rows so agents can communicate epic progress without bypassing readiness, audit, retro, or closeout gates.

## Non-Goals

- Replacing child task lifecycle statuses.
- Allowing a generic status override for `Complete`.
- Building a configurable workflow engine.
- Rewriting historical tracker rows.

## Users & Context

- Owners need the global tracker to show whether an epic is being analysed, ready, in progress, or in closeout.
- Agents need a safe command for global epic row progress instead of manual tracker edits.
- Maintainers need `Complete` to remain guarded by `epic closeout --complete`.

## Requirements (Outcome-Focused)

- Add a minimal global epic lifecycle command for `Analysing`, `Ready`, `In Progress`, and `Closeout`.
- `Ready` requires the epic requirements readiness gate to pass.
- `In Progress` requires readiness and parent AC coverage mapping.
- `Closeout` requires the current acceptance audit to have no parent AC gaps and the epic retro gate to be satisfied.
- `Complete` is not set by the lifecycle command; users must run `epic closeout --complete`.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-004 AC4 by adding a CLI-supported global epic lifecycle command.
- AC2: Covers EPIC-004 AC4 by gating `Ready`, `In Progress`, and `Closeout` transitions.
- AC3: Covers EPIC-004 AC4 by refusing `Complete` transitions outside `epic closeout --complete`.
- AC4: Covers EPIC-004 AC4 by adding fixture tests and docs/guidance.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Add `epic lifecycle` rather than overloading child-row `epic status`.
  - Why: `epic status` already manages child rows; a separate command avoids ambiguous IDs and accidental child/global row edits.

## Validation Plan

- Add tests for allowed and blocked lifecycle transitions.
- Run `.venv/bin/pytest tests/test_doctor.py`.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-004 --id TASK-018`.
- Run `./.project-workflow/cli/workflow doctor`.
