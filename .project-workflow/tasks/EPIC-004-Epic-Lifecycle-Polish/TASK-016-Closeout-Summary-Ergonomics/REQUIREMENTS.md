# Requirements

## Summary

- Task: TASK-016
- Title: Closeout Summary Ergonomics
- Parent AC Coverage: AC2
- Last updated: 2026-06-17

## Goal

Make `epic closeout` output easier for humans and agents to act on by printing a concise summary before detailed gap lines.

## Non-Goals

- Replacing `ACCEPTANCE-AUDIT.md`.
- Changing the closeout gate rules in this task.
- Building a rich report renderer or external dashboard.

## Users & Context

- Owners need to know whether an epic is ready to close without reading the audit file first.
- Agents need categorized next actions so they can remediate missing mappings, evidence, QA, or deferral metadata.
- Maintainers need the CLI output to remain concise and script-friendly.

## Requirements (Outcome-Focused)

- `epic closeout` prints total parent AC count and pass/deferred/gap counts.
- When gaps exist, output categorizes missing mappings, incomplete child rows, missing evidence, missing QA, and deferral metadata/follow-up gaps.
- When closeout passes without `--complete`, output clearly says the next action is rerun with `--complete`.
- When closeout passes with `--complete`, output clearly says the epic row was updated.
- The detailed audit file remains the source of full evidence detail.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-004 AC2 by printing closeout counts for total/pass/deferred/gap parent ACs.
- AC2: Covers EPIC-004 AC2 by categorizing common closeout blockers in CLI output.
- AC3: Covers EPIC-004 AC2 by printing clear next actions for blocked, validate-only pass, and complete pass paths.
- AC4: Covers EPIC-004 AC2 by adding fixture coverage for closeout summary output.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Keep the summary text simple and line-oriented.
  - Why: Agents can parse it, humans can scan it, and the audit file remains available for detail.

## Validation Plan

- Add or update closeout fixture tests in `tests/test_doctor.py`.
- Run `.venv/bin/pytest tests/test_doctor.py`.
- Run `./.project-workflow/cli/workflow epic ready-child --epic-id EPIC-004 --id TASK-016`.
- Run `./.project-workflow/cli/workflow doctor`.
