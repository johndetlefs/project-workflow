# Requirements

## Summary

- Task: EPIC-004
- Title: Epic Lifecycle Polish
- Last updated: 2026-06-17

## Goal

Polish project-workflow's epic lifecycle now that the core acceptance-criteria gates are in place. The outcome should make epics easier to start, easier to close, easier to audit, and less noisy to operate without turning project-workflow into a heavyweight project-management system.

This epic should include all five candidate improvements discussed after EPIC-003:

- Create or maintain an `ACCEPTANCE-MAP.md` from the start of an epic.
- Improve `epic closeout` ergonomics so humans and agents get a clear summary.
- Add lightweight epic-level retro enforcement.
- Add a minimal epic status lifecycle where it creates real guardrails.
- Reduce legacy warning noise without hiding real workflow problems.

## Non-Goals

- Building a general workflow engine or configurable status graph.
- Requiring ceremony that does not improve delivery quality or auditability.
- Retrofitting every historical task by hand as part of the main product change.
- Removing warnings that identify real quality gaps in current or future work.
- Replacing child task QA, parent AC mapping, or closeout gates added in EPIC-002 and EPIC-003.

## Users & Context

- Owners and PM/BA users need epics to be understandable and auditable without reading every child task file.
- Agents need clearer generated artifacts and CLI output so they know exactly what to do next.
- Junior developers need visible guardrails for epic progress, closeout, retros, and legacy warnings.
- Maintainers need to preserve the lightweight Markdown-first design and avoid expanding the product beyond its useful workflow boundary.

## Requirements (Outcome-Focused)

- Epic initialization should make parent AC mapping visible immediately, not only at final audit time.
- Epic closeout output should summarize what passed, what failed, where evidence lives, and what the agent or owner should do next.
- Epic closeout should require a lightweight epic-level retro or explicit "no lessons/follow-ups" record before completion.
- Epic status lifecycle should be minimal and practical: enough to show `Analysing`, `Ready`, `In Progress`, `Closeout`, and `Complete` style progress where the CLI can enforce useful gates, without duplicating child task lifecycle machinery.
- Doctor and validation output should distinguish legacy/historical warnings from current actionable blockers so old artifacts do not drown out new workflow problems.
- Generated docs, prompts, skills, local helper, package source, tests, and this repository's installed workflow state should remain aligned.

## Acceptance Criteria (Verifiable)

- AC1: New epics start with an `ACCEPTANCE-MAP.md` or equivalent maintained acceptance-map artifact that lists parent AC IDs, summaries, child coverage, evidence state, deferral state, and current status; generated templates/docs/tests prove the artifact exists from epic start.
- AC2: `epic closeout` prints a concise human/agent-friendly summary covering total parent ACs, pass/fail/deferred counts, missing mappings, missing evidence, missing QA, deferrals, follow-ups, and next actions, while still writing the detailed audit file.
- AC3: Epic closeout blocks completion unless a lightweight epic retro is recorded, with sections for lessons, follow-up tasks, deferrals, missed in-scope work, and a permitted explicit "none" entry; generated guidance and tests cover the required retro behavior.
- AC4: A minimal epic status lifecycle exists for global epic rows where useful, with CLI-supported transitions or validation for `Analysing`, `Ready`, `In Progress`, `Closeout`, and `Complete`; transitions must not bypass readiness, audit, retro, or closeout gates.
- AC5: Doctor or validation output separates legacy/historical warnings from current actionable issues, with tests proving old APP/EPIC-002-style artifacts remain visible but do not obscure EPIC-003-or-newer gate failures.

## Open Questions (Answer Needed)

- None blocking. Depth decisions are intentionally bounded in the decisions section.

## Decisions (Resolved)

- Decision: Treat all five follow-ups as one epic with five focused child workstreams.
  - Why: They all affect epic lifecycle ergonomics and should be designed together so commands, docs, and tests stay coherent.

- Decision: Keep the status lifecycle minimal.
  - Why: Status should communicate and enforce gates, not become a separate project-management system.

- Decision: Make legacy cleanup primarily a warning-classification/product-noise problem.
  - Why: This gives value to every repository with historical artifacts without spending the epic manually rewriting old docs.

- Decision: Require an epic retro record at closeout, but allow explicit "none" entries.
  - Why: The point is to prevent hidden follow-ups or missed scope, not to force fake retros.

- Decision: Use generated artifacts and tests as the quality bar for each improvement.
  - Why: The product is installed into other repos, so source behavior, packaged templates, generated guidance, and this repo's local helper must stay in sync.

## Validation Plan

- Run `./.project-workflow/cli/workflow epic ready --epic-id EPIC-004` after requirements are drafted.
- Decompose EPIC-004 into proposed child rows with parent AC coverage and leave them unscaffolded until approved.
- Add fixture tests for each accepted child task during implementation.
- Run `.venv/bin/pytest tests/test_doctor.py`.
- Run `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor`.
- Run parity checks for source CLI, packaged template, local helper, generated prompts, generated skills, Cursor rules, and README.
- Before closeout, run `./.project-workflow/cli/workflow epic audit --epic-id EPIC-004` and `./.project-workflow/cli/workflow epic closeout --epic-id EPIC-004`.
