# Requirements

## Summary

- Task: TASK-009
- Title: Epic Rigor Docs Agent Guidance And Fixtures
- Parent AC Coverage: AC14, AC16, AC18
- Last updated: 2026-06-17

## Goal

Complete the final documentation, generated agent guidance, fixture coverage, and self-hosted parity sweep for EPIC-002 so the new epic rigor behavior is durable in both shipped project-workflow assets and this repository's installed helper.

## Non-Goals

- Adding new epic lifecycle behavior beyond the already implemented AC mapping, audit, closeout, deferral, and status gates.
- Retrofitting historical APP tasks that predate QA evidence requirements.
- Changing downstream Daily Checklist workflow artifacts.

## Users & Context

- Maintainers need tests and parity checks proving the epic rigor workflow behaves as documented.
- Agents using generated Codex/Copilot/Cursor assets need explicit instructions to validate directly when possible and to separate verified evidence from deferred setup.
- Users closing epics need confidence that the package source, generated templates, installed local helper, and generated prompts stay aligned.

## Requirements (Outcome-Focused)

- Documentation and generated agent assets tell agents to run validations they can perform directly before asking for manual user testing.
- QA guidance distinguishes verified evidence from deferred setup, owner-only actions, and unavailable connector/OAuth checks.
- Automated fixture coverage exercises complete epic coverage, missing mappings, missing evidence, approved deferrals, incomplete deferrals, unsafe closeout, child evidence gating, and generated guidance.
- Self-hosted parity validation compares package source, generated template assets, installed local helper, and generated prompt mirrors.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-002 AC14 by updating README and generated QA guidance so agents validate directly where possible and distinguish verified evidence from deferred setup.
- AC2: Covers EPIC-002 AC16 by ensuring automated tests cover complete coverage, missing mappings, evidence gaps, approved deferrals, incomplete/unapproved deferrals, unsafe closeout, child evidence gating, and generated guidance.
- AC3: Covers EPIC-002 AC18 by running parity checks across package source, generated workflow template, installed local helper, generated prompts, and installed prompt mirrors.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Treat TASK-009 as a closeout sweep, not a new behavior task.
  - Why: The CLI/template behavior already landed in TASK-004 through TASK-008; this task proves docs, generated guidance, fixtures, and self-hosted parity.

## Validation Plan

- Run `.venv/bin/pytest tests/test_doctor.py`.
- Run `./.project-workflow/cli/workflow doctor`.
- Run `.venv/bin/project doctor`.
- Run `git diff --check`.
- Compare `src/project_workflow/templates/workflow.py` with `.project-workflow/cli/workflow.py`.
- Compare generated prompt sources with `.github/prompts` mirrors for Epic, Retro, and QAReview.
