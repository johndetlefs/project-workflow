# Requirements

## Summary

- Task: EPIC-005
- Title: Project Backlog Support
- Last updated: 2026-06-22

## Goal

Add first-class project backlog support to project-workflow so a user can give a broad future objective, have the agent capture and refine it into durable backlog items, and later promote selected items into executable tasks or epics without losing product-intent history.

The backlog should sit between the project constitution and the active tracker:

- `CONSTITUTION.md` records durable project outcomes and principles.
- `BACKLOG.md` records future intent, options, rough priority, and promotion history.
- `TRACKER.md` records committed execution state for scaffolded tasks and epics.
- `tasks/*` records executable requirements, plans, implementation evidence, QA, and retros.

The outcome is a lightweight, Markdown-first backlog that works consistently across GitHub Copilot, Claude Code, OpenAI Codex, and Cursor, while preserving the existing gated workflow for requirements, planning, implementation, QA, and closeout.

## Non-Goals

- Replacing external issue trackers, sprint boards, or roadmap tools.
- Turning backlog rows into implementation work without owner confirmation.
- Mirroring active execution status in two places.
- Building a configurable project-management workflow engine.
- Requiring teams to use backlog support before creating a small, well-understood task directly.
- Migrating every historical task or epic into the backlog as part of this epic.
- Automatically importing or transforming arbitrary existing roadmap/backlog documents into canonical backlog rows.
- Adding networked sync with GitHub Issues, Linear, Jira, Notion, or other planning systems.

## Users & Context

- Owners, PMs, BAs, and technical leads need a place to capture broad objectives and future intent before they are ready for task or epic scaffolding.
- Developers and agent operators need a clear distinction between "future idea" and "committed workflow item" so agents do not treat vague backlog entries as ready-to-build work.
- Maintainers need backlog support to remain repository-native, low overhead, and compatible with all existing agent modes.
- Agents need explicit instructions for reading project context, drafting backlog rows from conversation, asking focused questions when needed, and promoting only after owner approval.

## Requirements (Outcome-Focused)

- Project-workflow should create or maintain `.project-workflow/BACKLOG.md` as the canonical backlog artifact, without overwriting user-owned backlog content on refresh.
- Backlog rows should use stable `BL-###` IDs and preserve rows after promotion, rejection, deferral, or supersession.
- Backlog row fields should capture enough intent for later requirements work without becoming a full task spec. At minimum: ID, title, type, priority, status, outcome, promoted-to reference, and notes.
- Backlog type values should be deliberately small and documented: `Idea`, `Task Candidate`, `Epic Candidate`, `Discovery`, and `Follow-Up`.
- Backlog priority values should be deliberately small and documented: `High`, `Medium`, `Low`, and `Unset`.
- Backlog statuses should distinguish proposal and execution boundaries. The backlog may describe `Proposed`, `Accepted`, `Deferred`, `Rejected`, `Superseded`, and `Promoted` states, but active implementation status must live only in `TRACKER.md` or an epic tracker.
- A promoted backlog item should remain in the backlog with status `Promoted` and a `Promoted To` reference to the created `TASK-###` or `EPIC-###`.
- Created task or epic requirements should include a `## Backlog Source` section that references the originating backlog ID and carries forward the backlog item's outcome and relevant notes.
- The workflow should support both direct backlog entry creation and broad-objective decomposition, where the agent can read project context and propose multiple backlog candidates for owner review.
- Promotion should be owner-confirmed. An agent may draft candidates and recommend task-vs-epic treatment, but should not silently create executable tasks or epics from backlog rows.
- Promotion should require the source backlog row to be `Accepted`, unless the owner explicitly confirms accepting and promoting the same row in one operation.
- CLI support should cover the core lifecycle where it adds real safety: initialize backlog, add/list/update rows, validate backlog structure, and promote accepted rows into task or epic scaffolds.
- Validation should detect malformed backlog rows, duplicate backlog IDs, invalid statuses, and promoted references that do not point to existing task or epic artifacts.
- Deterministic CLI commands should own file creation, row mutation, validation, and promotion mechanics. Agent guidance should own broad-objective interpretation, candidate drafting, and recommendation of task-vs-epic treatment.
- Generated prompts, Claude agents, Codex skills, Cursor agents/rules, README docs, and local/package CLI templates should stay aligned so all supported models operate the backlog consistently.
- Existing repositories should gain backlog support through `project init` safely and idempotently, with missing backlog files created and existing unmarked backlog files preserved; existing roadmap/backlog documents should remain untouched unless a repo-local migration task explicitly changes them.
- Backlog support should remain optional in day-to-day use. Users can still create a task or epic directly when scope is already clear.

## Acceptance Criteria (Verifiable)

- AC1: `project init` installs backlog support idempotently: `.project-workflow/BACKLOG.md` is created when missing, existing user-owned backlog content is not overwritten, and generated agent assets include backlog workflow instructions for every supported agent mode.
- AC2: Backlog rows use globally stable `BL-###` IDs and a documented table schema containing ID, title, type, priority, status, outcome, promoted-to reference, and notes; type values are limited to `Idea`, `Task Candidate`, `Epic Candidate`, `Discovery`, and `Follow-Up`; priority values are limited to `High`, `Medium`, `Low`, and `Unset`; tests cover ID allocation and duplicate-ID detection.
- AC3: The backlog lifecycle supports `Proposed`, `Accepted`, `Deferred`, `Rejected`, `Superseded`, and `Promoted` without duplicating active task/epic execution status; docs and generated guidance explicitly say `Accepted` is not implementation-ready, and execution status belongs in `TRACKER.md` or epic trackers after promotion.
- AC4: A broad objective can be turned into one or more proposed backlog rows that are context-aware, outcome-focused, and not automatically added to `TRACKER.md`; generated agent guidance requires owner review before rows are accepted or promoted.
- AC5: Promoting an accepted backlog row to a task creates a normal task folder and global tracker row, sets the backlog row to `Promoted`, records the new `TASK-###` in `Promoted To`, and copies backlog source context into a `## Backlog Source` section in the task requirements.
- AC6: Promoting an accepted backlog row to an epic creates a normal epic folder and global tracker row, sets the backlog row to `Promoted`, records the new `EPIC-###` in `Promoted To`, and copies backlog source context into a `## Backlog Source` section in the epic requirements.
- AC7: Backlog validation reports malformed tables, missing required fields, duplicate `BL-###` IDs, invalid type/priority/status values, and promoted references that do not resolve to existing task or epic artifacts, with remediation messages an agent can act on.
- AC8: `project.backlog` or equivalent generated agent assets exist for GitHub Copilot prompts, Claude Code agents, OpenAI Codex skills, and Cursor agents/rules, and each asset explains creation, refinement, validation, and promotion behavior consistently.
- AC9: README and installed workflow guidance explain where backlog sits relative to constitution, tracker, tasks, and epics; they include examples for capturing an idea, accepting it, promoting it, and preserving traceability.
- AC10: Automated tests cover backlog init, add/update/list behavior, validation failures, task promotion, epic promotion, idempotent refresh, generated asset inclusion, and the rule that promoted backlog rows remain in the backlog.

## Open Questions (Answer Needed)

- None blocking for requirements. UI wording and exact CLI flag names can be finalized during planning, as long as the accepted behavior above remains intact.

## Decisions (Resolved)

- Decision: Treat backlog support as an epic, not a single task.
  - Why: The change spans a new workflow artifact, CLI behavior, promotion semantics, validation, generated assets for four agent modes, README updates, and tests.

- Decision: Keep promoted rows in the backlog instead of deleting them.
  - Why: The backlog should preserve product-intent history and traceability, while execution state lives in the tracker/task/epic artifacts.

- Decision: Make `.project-workflow/BACKLOG.md` the canonical artifact.
  - Why: It keeps the feature repository-native, reviewable, versioned, and consistent with project-workflow's Markdown-first design.

- Decision: Do not let backlog become a second active tracker.
  - Why: Duplicating execution status would make the workflow ambiguous and weaken the existing lifecycle gates.

- Decision: Require owner confirmation before promotion.
  - Why: A broad objective can be model-decomposed, but committing work to tasks or epics requires human product judgment.

- Decision: Support direct task/epic creation without requiring backlog first.
  - Why: The backlog is for future intent and broad objectives; it should not add ceremony to clear, immediate work.

- Decision: Use a fixed lightweight vocabulary for backlog type and priority.
  - Chosen: Type values are `Idea`, `Task Candidate`, `Epic Candidate`, `Discovery`, and `Follow-Up`; priority values are `High`, `Medium`, `Low`, and `Unset`.
  - Why: Agents and CLI validation need a small shared vocabulary, but the backlog should not become a customizable workflow engine.

- Decision: Treat `Accepted` as "worth keeping or preparing", not "ready to implement".
  - Why: Requirements, planning, readiness, implementation, QA, and closeout gates still belong to the task/epic workflow after promotion.

- Decision: Promotion normally requires `Accepted`, with one-step accept-and-promote allowed only when the owner explicitly confirms both.
  - Why: This preserves the owner approval boundary without adding pointless ceremony when the owner is already giving a direct promotion instruction.

- Decision: Put backlog provenance in a dedicated `## Backlog Source` section in promoted task/epic requirements.
  - Why: A stable section name gives agents an easy place to preserve product intent without mixing backlog notes into acceptance criteria.

- Decision: Split responsibilities between deterministic CLI behavior and agent-authored interpretation.
  - Chosen: The CLI owns file creation, row mutation, validation, and promotion mechanics. Agents own broad-objective interpretation, candidate drafting, and task-vs-epic recommendations.
  - Why: The CLI cannot infer product strategy, and agents should not hand-edit lifecycle state when a deterministic command can preserve consistency.

- Decision: Do not build a generic legacy backlog importer in this epic.
  - Chosen: Existing-repository support means safe, idempotent installation and preservation of existing backlog/roadmap files. Migration from known existing docs, such as Daily Checklist or johndetlefs roadmaps, should be handled later by repo-local project-workflow tasks when needed.
  - Why: The current user base and project set are known, so a broad importer would add complexity before it proves value. Manual/repo-local migration preserves judgment and avoids damaging strategic roadmap documents.

## Validation Plan

- Run `./.project-workflow/cli/workflow epic ready --epic-id EPIC-005` after requirements are reviewed.
- Decompose EPIC-005 into proposed child rows that map every parent AC to at least one child workstream.
- Add or update unit tests for backlog parsing, ID allocation, validation, promotion, and init refresh behavior.
- Run `.venv/bin/pytest tests/test_doctor.py` and any new targeted tests.
- Run `./.project-workflow/cli/workflow doctor` and `.venv/bin/project doctor`.
- Verify generated assets across GitHub Copilot, Claude Code, Codex, and Cursor include consistent backlog workflow guidance.
- Dogfood the feature by adding a real backlog item for a future project-workflow improvement and promoting it only through the confirmed workflow.
