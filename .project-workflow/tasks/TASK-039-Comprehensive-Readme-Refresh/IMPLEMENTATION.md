## User Story

As a prospective adopter or agent working in a project-workflow repository, I want the README to explain the value, concepts, routes, commands, and human/agent responsibilities clearly and accurately, so I can adopt or operate the workflow without stale assumptions or unnecessary ceremony.

## Acceptance Criteria

- [x] AC1: The README top section explains project-workflow in human-friendly language, including the value proposition and the human/agent collaboration model, before deep installation or command detail.
- [x] AC2: No README heading or guidance uses fixed duration estimates for workflow phases such as task creation, requirements, planning, clarify, QA, or retro.
- [x] AC3: The README accurately describes backlog, Fix, Task, and Epic routing and distinguishes when each route should be used.
- [x] AC4: The README describes the Fix workflow with `FIX-###` IDs, one `FIX.md`, global tracker use, post-completion historical accuracy, triage classification, and promotion/escalation boundary.
- [x] AC5: The README describes the current requirements approval model: one explicit owner approval before planning, followed by agent-owned Planner, Clarify, `task ready`, and `Ready` movement inside the unchanged approved envelope.
- [x] AC6: The README documents owner responsibilities and agent responsibilities clearly enough that a new user knows what they provide versus what the agent operates.
- [x] AC7: Installation and refresh instructions use the canonical UVX command and identify all supported agent modes.
- [x] AC8: Local command examples use the initialized repo helper path where appropriate: `./.project-workflow/cli/workflow`.
- [x] AC9: The README includes current validation guidance for `doctor`, `validate`, strict mode, and accepted warning review at a concise README-appropriate level.
- [x] AC10: The README keeps current task ID namespace and unique ID guidance, including reserved Fix IDs.
- [x] AC11: The README gives a useful file-structure overview for GitHub Copilot, Claude Code, Codex, and Cursor modes without becoming the only source of truth for generated assets.
- [x] AC12: Epic coverage includes proposal-first epics, contracts, decomposition authority, child rows, evidence, amendments, audit, and closeout at README depth.
- [x] AC13: The README removes or rewrites outdated examples that imply `Plan Confirmed` is the normal current target for new work, while noting legacy compatibility only if needed.
- [x] AC14: The README remains usable by agents: it contains enough concrete command names, file paths, route rules, and lifecycle constraints for an agent to operate correctly.
- [x] AC15: The README remains usable by humans: it is easier to scan than the current version, with clearer section order, less duplicated command prose, and a more approachable top.
- [x] AC16: The README update is limited to documentation unless the task is explicitly expanded.

## Goal

Replace the stale README with a concise, accurate guide that introduces project-workflow to humans, gives owners a clear mental model, and gives coding agents enough concrete routing, command, lifecycle, and validation detail to operate the current workflow safely.

## Approach

- Lead with the product outcome and human/agent collaboration model, then provide a short quick start.
- Organize daily use around choosing Backlog, Fix, Task, or Epic rather than a timed sequence of ceremonies.
- Explain the single requirements approval envelope and the autonomous agent lifecycle inside that boundary.
- Keep detailed command and file references available after the conceptual guide, using the initialized local helper consistently.
- Retain advanced epic, evidence, validation, ID, and agent-mode guidance at README depth while removing duplicated and legacy examples.

## Phases

### Phase 1: Human Orientation And Routing

Rewrite the opening, quick start, collaboration model, and work-routing guidance. Validate that a new owner can understand the value and choose Backlog, Fix, Task, or Epic without reading implementation detail.

### Phase 2: Current Operating Workflow

Document Task, Fix, and Epic lifecycles, including approval authority, readiness, evidence, QA, completion, and retro. Validate commands and status names against the local CLI and repository guidance.

### Phase 3: Agent And Maintainer Reference

Consolidate installation, refresh, validation, namespace, file-structure, and agent-mode guidance. Remove stale timings, legacy-normal-flow implications, duplicated examples, and unsupported command paths.

### Phase 4: Documentation QA

Run targeted text checks, workflow doctor, and a criterion-by-criterion manual review. Record evidence and findings before completion.

## Validation

- AC1-AC16: Manual README review against accepted criteria.
- AC2: `rg -n -i "[0-9]+[[:space:]]*(min|mins|minute|minutes)|how to use \\(the typical workflow\\)|create a task.*5|write requirements.*15|create a plan.*15|clarify.*10|qa.*10|retro.*5" README.md`
- AC3-AC15: targeted `rg` checks for current workflow terms and commands.
- Workflow state: `./.project-workflow/cli/workflow doctor`

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Reframe the product for humans | Rewrite the opening and collaboration model so owners understand the value, their decision authority, and what agents operate. | AC1, AC6, AC15: Human-friendly positioning and clear owner/agent responsibilities are visible before technical detail. | Read the opening and "How collaboration works" without prior project-workflow knowledge; confirm the value and responsibility split are clear. | Complete |
| 2 | Replace the timed flow with current routing and lifecycle guidance | Document Backlog, Fix, Task, and Epic selection plus the current approval, readiness, implementation, QA, completion, and retro lifecycle. | AC2, AC3, AC4, AC5, AC12, AC13: No fixed timings remain; all routes and current lifecycle authority are accurate. | Compare the route table and lifecycle sections with `./.project-workflow/cli/workflow --help`, task/fix/epic help, and repository guidance. | Complete |
| 3 | Consolidate installation and agent reference | Keep canonical UVX setup/refresh, local helper commands, validation behavior, ID configuration, supported modes, and generated file locations in a compact reference. | AC7, AC8, AC9, AC10, AC11, AC14: Commands, namespaces, validation, modes, and paths are concrete and current. | Run targeted `rg` checks for canonical commands, modes, validation terms, namespaces, and local helper usage. | Complete |
| 4 | Verify documentation scope and acceptance coverage | Review the final README against every requirement, run workflow health checks, and record QA evidence without changing product behavior. | AC1-AC16: Every criterion has evidence and the diff remains documentation-only. | Inspect `git diff`, run targeted stale-text checks and `./.project-workflow/cli/workflow doctor`, then record the QA verdict. | Complete |

## QA & Code Review

- Review date: 2026-07-21
- Reviewed areas: README positioning and navigation; Backlog, Fix, Task, and Epic routing; owner/agent authority; CLI examples; installation and refresh; validation; ID generation; generated assets; repository history; documentation-only scope.
- AC1, AC6, AC15 evidence: The opening, `What You Get`, and `How Collaboration Works` explain the value and responsibility boundary before operational detail. The README was reduced from the previous duplicated walkthrough to a route-first 429-line guide.
- AC2 evidence: The targeted stale-duration and obsolete-heading search returned no matches.
- AC3-AC5, AC12-AC14 evidence: Route and lifecycle content was manually compared with repository guidance and the local `backlog`, `fix`, `task`, and `epic` CLI help. The first draft's invalid backlog type and incomplete Fix promotion command were found and corrected before the verdict.
- AC7-AC11 evidence: The canonical UVX command, four agent modes, local helper path, strict and accepted-warning validation, sequential and unique namespaces, and mode-specific generated paths are present and were compared with current CLI help and repository files.
- AC16 evidence: The implementation changes only `README.md` plus TASK-039 workflow records and the global tracker row. No source, template, generated agent asset, package metadata, or test file was changed for TASK-039.
- Automated evidence: `task ready`, `backlog validate`, `doctor`, `doctor --strict`, `validate --strict`, and `git diff --check` passed. Doctor reported no active issues and 71 configured accepted warnings hidden.
- Tests: Unit tests were not run because the accepted scope and diff are documentation-only; the requirements explicitly route README-only work to documentation and workflow validation.
- Findings: None remaining. The draft support/license omission and two invalid command examples were corrected during review.
- Verdict: Pass

## Retro

- Retro date: 2026-07-21
- Reusable lessons: A route-first README is easier for owners to navigate than a timed ceremony walkthrough. Executable documentation examples must be checked against the current local CLI help; plausible command syntax is not sufficient proof.
- Conventions or agent assets updated: `README.md` is now the durable human and agent entry point. No prompt, skill, generated asset, template, or repository guidance change was needed because this task corrected documentation rather than workflow behavior.
- Follow-up suggestions: None from this task. Broader migration and adoption work remains separately tracked under EPIC-007.
- Missed in-scope work: None.

## Notes

- Task: TASK-039
- Title: Comprehensive README Refresh
- Created: 2026-07-21
