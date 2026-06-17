# Requirements

## Summary

- Task: TASK-004
- Title: Epic AC Schema And Templates
- Parent Epic: EPIC-002 | Epic Acceptance Rigor
- Parent AC Coverage: EPIC-002 AC1, AC2, AC6, AC15
- Last updated: 2026-06-17

## Goal

Make parent epic acceptance-criteria coverage a first-class part of the epic and child-task artifact shape, so future epic work starts with visible AC IDs, proposed child rows expose parent AC coverage, and generated child docs include parent AC sections before implementation begins.

## Non-Goals

- Implementing `epic decompose` coverage generation logic; that belongs to `TASK-005`.
- Implementing `epic audit` or `epic closeout`; that belongs to `TASK-006`.
- Implementing full status transition behavior; that belongs to `TASK-008`.
- Migrating historical epic trackers beyond backward-compatible documentation and validation expectations.

## Users & Context

- Developers and agents creating epics need templates that force stable parent AC IDs from the beginning.
- Reviewers need child-task docs to show exactly which parent epic ACs the child is responsible for.
- Maintainers need clear root tracker versus epic tracker rules so proposed child rows do not drift into the wrong tracker.

## Requirements (Outcome-Focused)

- Epic requirements templates and generated guidance must default to stable numbered parent ACs and instruct agents to preserve those IDs.
- New epic tracker schema guidance must make parent AC coverage visible as a dedicated field while preserving backward-compatible reading of legacy `Notes` coverage.
- Epic-managed child task templates must include parent AC coverage and parent AC evidence sections.
- Documentation and generated agent assets must explain global tracker versus epic tracker ownership rules.
- Template changes must be mirrored across package source and the installed local workflow helper where this repo self-hosts project-workflow.

## Acceptance Criteria (Verifiable)

- AC1: Parent epic AC `EPIC-002 AC1` is satisfied when epic requirements templates and generated agent guidance create numbered parent AC IDs by default and instruct agents not to renumber existing IDs without explicit approval.
- AC2: Parent epic AC `EPIC-002 AC2` is satisfied when new epic tracker schema guidance includes a dedicated parent AC coverage field and documents backward-compatible parsing of `Notes` values such as `Covers AC1, AC3`.
- AC3: Parent epic AC `EPIC-002 AC6` is satisfied when epic-managed child docs include `Parent AC Coverage` and `Parent AC Evidence` sections, while standalone task docs remain low-noise.
- AC4: Parent epic AC `EPIC-002 AC15` is satisfied when docs and generated agent guidance clearly state that the global tracker summarizes epics, epic trackers own child rows, and proposed child rows must stay inside the epic tracker until approved/scaffolded.

## Open Questions (Answer Needed)

- None. The parent epic clarification pass resolved the relevant schema and lifecycle decisions.

## Decisions (Resolved)

- Decision: Use a dedicated parent AC coverage field for new epic trackers.
  - Context: A `Notes` convention is too easy to miss and too hard to validate reliably.
  - Chosen: Introduce a first-class field for new epic tracker rows while documenting backward-compatible `Notes` support.
  - Why: The field makes parent AC coverage scan-friendly and automation-friendly without abandoning existing epics.

- Decision: Keep child task AC IDs local while explicitly naming parent ACs.
  - Context: project-workflow task plans already expect stable `AC1`, `AC2`, etc. in each task.
  - Chosen: Child task ACs remain `AC1` through `AC4`, and each criterion names the parent epic AC it proves.
  - Why: This preserves existing doctor behavior while making parent coverage visible.

## Validation Plan

- Verify generated requirement and implementation templates include stable AC IDs and parent AC sections where appropriate.
- Verify generated Codex/Copilot/Cursor guidance describes parent AC coverage, child evidence, and tracker ownership rules.
- Verify package source and `.project-workflow/cli/workflow.py` remain aligned after template changes.
- Run targeted tests for scaffold/template output once implementation is complete.
