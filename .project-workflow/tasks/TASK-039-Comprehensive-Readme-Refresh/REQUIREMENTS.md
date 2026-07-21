# Requirements

## Summary

- Task: TASK-039
- Title: Comprehensive README Refresh
- Last updated: 2026-07-21
- Source discussion: Owner request on 2026-07-21 to comprehensively review and rewrite the README because current usage guidance and time estimates are stale.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: No
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-21
- Approval note / source: Owner message on 2026-07-21: All looks good, go get it.
- Approved artifact identity: sha256:6f375afcec324a9e9e2717138d8fbd2cc5c5e8f9d3253cc041c8c01191dfb5c1

## Goal

Rewrite the project-workflow README so it accurately explains the current product, feels useful and human-friendly to new readers, and gives agents enough precise operational guidance to use the workflow correctly without relying on stale timing, outdated lifecycle assumptions, or buried implementation details.

## Non-Goals

- Changing workflow behavior, CLI commands, generated prompts, skills, tests, package metadata, or project-workflow templates.
- Replacing the full CLI reference or every generated agent instruction with README content.
- Creating marketing copy that obscures workflow constraints, evidence requirements, owner approval gates, or supported command behavior.
- Removing technical depth entirely; the README must still help maintainers, adopters, and agents operate the project.
- Rewriting unrelated docs unless the README needs links to them.

## Users & Context

- New human readers need to quickly understand what project-workflow is, why it exists, who it helps, and how it changes agentic software delivery.
- Project owners and product leads need to understand their role: provide intent, decisions, requirements approval, and completion authority while agents operate the workflow.
- Coding agents need a precise, up-to-date operational guide covering backlog, Fix, task, epic, requirements approval, planning, clarify, ready, implementation, QA, and retro.
- Maintainers need the README to reflect current source-of-truth behavior after the Fix workflow and authority-flow updates landed.
- Current README evidence shows stale or misleading guidance, including stopwatch-style section labels such as `Create a Task (5 min)`, `Write Requirements (15-30 min)`, `Create a Plan (15 min)`, `Clarify ... (10-20 min)`, `QA & Code Review (10-30 min)`, and `Retro ... (5-15 min)`.

## User Story

As a prospective adopter or agent working in a project-workflow repository, I want the README to explain the value, concepts, routes, commands, and human/agent responsibilities clearly and accurately, so I can adopt or operate the workflow without stale assumptions or unnecessary ceremony.

## Requirements (Outcome-Focused)

- Open with a human-friendly product explanation that is clear enough for maintainers, consultants, technical leads, and clients. The top of the README should communicate the value proposition with a modest sales tone: project-workflow helps humans keep intent, decisions, evidence, and delivery state coherent while agents do the mechanical workflow work.
- Replace the current stale stopwatch framing with lifecycle guidance that reflects present behavior. The README must not promise fixed timings for creating tasks, writing requirements, planning, clarification, QA, or retro.
- Explain the human/agent split early:
  - humans own goals, constraints, product decisions, requirements/AC approval, exceptional risk decisions, and final completion authority;
  - agents gather context, scaffold workflow artifacts, draft requirements, plan after approval, clarify internally, validate readiness, implement, record evidence, and keep trackers current.
- Present the current routing model clearly: backlog for future intent, Fix for one bounded post-completion correction, Task for one new outcome or multiple related implementation steps, and Epic for coordinated workstreams.
- Explain the new Fix workflow accurately:
  - Fixes are first-class lightweight records under `.project-workflow/tasks/`;
  - Fixes use one `FIX.md`, the global tracker, and reserved `FIX-###` IDs;
  - completed tasks remain historically accurate and are linked rather than rewritten by default;
  - defects, regressions, bounded change requests, and incidents/hotfixes are classified during triage.
- Explain the current task authority model accurately:
  - task requirements and acceptance criteria require one explicit owner approval before planning;
  - after approval, the agent normally runs Planner, post-plan Clarify, `task ready`, and moves the task to `Ready` autonomously;
  - generic repeated plan approvals are not required unless the user requested review, risk is exceptional, or scope/proof/source-of-truth drift occurs.
- Explain current epic behavior at the right level for README readers, including proposal-first epics, `EPIC-CONTRACT.md`, decomposition authority, child rows, parent AC coverage, evidence requirements, amendments, audit, closeout, and when an epic is appropriate.
- Keep installation and refresh guidance current and explicit:
  - canonical command is `uvx --from git+https://github.com/johndetlefs/project-workflow.git project init`;
  - supported agent modes are GitHub Copilot, Claude Code, OpenAI Codex, and Cursor;
  - initialized repos should use `./.project-workflow/cli/workflow` for local commands;
  - re-running init refreshes generated assets while preserving unmarked host-owned files via managed blocks or `*.new` behavior.
- Provide a quick-start path that is useful to a human reader and to an agent. It should show the minimum route from install to first meaningful work without implying the owner manually fills templates.
- Preserve and improve agent-useful details:
  - command examples for backlog, fix, task, epic, doctor/validate, and status transitions where relevant;
  - file structure after init, including generated agent assets by mode;
  - validation and doctor guidance;
  - task ID namespace and unique ID guidance;
  - evidence/proof caveats where README-level explanation is appropriate.
- Reduce duplication and wall-of-text where it harms comprehension. Detailed mechanics should remain, but the README should guide readers from overview to operation, with deeper technical sections lower down.
- Remove or rewrite outdated examples that conflict with current behavior, especially examples implying manual owner operation of every workflow phase or obsolete `Plan Confirmed`-first flow.
- Keep the README truthful about limits: project-workflow is Markdown/git based, not a hosted dashboard, external ticketing system, or substitute for product ownership.
- Keep tone professional and human. Avoid hype, jokes, or excessive sales language in operational sections.

## Acceptance Criteria (Verifiable)

- AC1: The README top section explains project-workflow in human-friendly language, including the value proposition and the human/agent collaboration model, before deep installation or command detail.
- AC2: No README heading or guidance uses fixed duration estimates for workflow phases such as task creation, requirements, planning, clarify, QA, or retro.
- AC3: The README accurately describes backlog, Fix, Task, and Epic routing and distinguishes when each route should be used.
- AC4: The README describes the Fix workflow with `FIX-###` IDs, one `FIX.md`, global tracker use, post-completion historical accuracy, triage classification, and promotion/escalation boundary.
- AC5: The README describes the current requirements approval model: one explicit owner approval before planning, followed by agent-owned Planner, Clarify, `task ready`, and `Ready` movement inside the unchanged approved envelope.
- AC6: The README documents owner responsibilities and agent responsibilities clearly enough that a new user knows what they provide versus what the agent operates.
- AC7: Installation and refresh instructions use the canonical UVX command and identify all supported agent modes.
- AC8: Local command examples use the initialized repo helper path where appropriate: `./.project-workflow/cli/workflow`.
- AC9: The README includes current validation guidance for `doctor`, `validate`, strict mode, and accepted warning review at a concise README-appropriate level.
- AC10: The README keeps current task ID namespace and unique ID guidance, including reserved Fix IDs.
- AC11: The README gives a useful file-structure overview for GitHub Copilot, Claude Code, Codex, and Cursor modes without becoming the only source of truth for generated assets.
- AC12: Epic coverage includes proposal-first epics, contracts, decomposition authority, child rows, evidence, amendments, audit, and closeout at README depth.
- AC13: The README removes or rewrites outdated examples that imply `Plan Confirmed` is the normal current target for new work, while noting legacy compatibility only if needed.
- AC14: The README remains usable by agents: it contains enough concrete command names, file paths, route rules, and lifecycle constraints for an agent to operate correctly.
- AC15: The README remains usable by humans: it is easier to scan than the current version, with clearer section order, less duplicated command prose, and a more approachable top.
- AC16: The README update is limited to documentation unless the task is explicitly expanded.

## Open Questions (Answer Needed)

- None for initial requirements draft. Owner review is required before implementation.

## Decisions (Resolved)

- The README is out of date enough to justify a comprehensive rewrite rather than small copy edits.
- The top of the README should be human-friendly and modestly sales-oriented.
- The README must serve both human readers and agents.
- Stale time estimates should be removed.
- This work is a Task, not a Fix, because it is a new documentation outcome rather than a bounded post-completion correction against one delivered behavior.

## Validation Plan

- Inspect README before and after the rewrite to confirm stale time-estimate headings are gone.
- Use `rg` to verify outdated duration text is removed and current terms such as Fix, owner approval, `task ready`, and canonical UVX init are present.
- Run `./.project-workflow/cli/workflow doctor` after task-doc and tracker changes.
- Run relevant repository tests only if implementation touches generated docs or code; README-only changes should not require unit tests.
- Review the final README manually against AC1-AC16 for clarity, accuracy, human readability, and agent utility.
