# Requirements

## Summary

- Task: EPIC-002
- Title: Epic Acceptance Rigor
- Last updated: 2026-06-16

## Goal

Tighten project-workflow's epic lifecycle so an epic cannot appear complete merely because child tasks are complete. Parent acceptance criteria must be visible from requirements through decomposition, child implementation, child QA, epic-level acceptance audit, explicit deferrals, and closeout.

This epic is based on the Daily Checklist `EPIC-001 | Daily Checklist MCP Access` failure mode, where child tasks were complete but the original parent acceptance criteria had not been systematically audited end-to-end until late closeout.

## Non-Goals

- Retrofitting every historical project-workflow task or epic in this repository.
- Building integrations for a specific downstream project such as Daily Checklist.
- Replacing human approval for scope deferrals, QA verdicts, or final epic completion.
- Creating a heavyweight project management system outside repository-native Markdown and the existing CLI.
- Changing standalone task behavior except where shared lifecycle safety helpers need to remain compatible.

## Users & Context

- Primary users are developers and maintainers using project-workflow to manage multi-task epics with coding agents.
- Secondary users are reviewers and product owners who need confidence that an epic's original acceptance criteria were proven, explicitly deferred, or escalated before closeout.
- Agents are also users of the workflow contract: they need generated prompts, skills, templates, and CLI safeguards that make the disciplined path the default.

## Requirements (Outcome-Focused)

- Epic requirements define stable parent acceptance criteria IDs by default and make those IDs the durable unit of decomposition, evidence, deferral, and closeout.
- Epic decomposition produces proposed child rows that show which parent ACs each child is expected to cover, so coverage gaps are visible before scaffolding.
- Scaffolded epic child tasks carry parent AC coverage into child `REQUIREMENTS.md`, child `IMPLEMENTATION.md`, and child QA/review expectations.
- Child QA can pass only when it records evidence for the parent ACs assigned to that child or records an explicit owner-approved deferral/follow-up.
- Epic closeout includes a mandatory acceptance audit that maps every parent AC to child tasks, validation evidence, owner-approved deferrals, or open blockers.
- CLI workflow operations reduce manual tracker drift by supporting status transitions and epic lifecycle gates for Testing, Review, Complete, audit, and closeout.
- Epic retro guidance separates follow-up tasks from work that should already have been completed in the current task, avoiding ambiguous retro language.
- Documentation and agent skills explain the intended epic lifecycle: requirements, AC IDs, decomposition with AC mapping, child task QA mapped to parent ACs, epic acceptance audit, explicit deferrals, and closeout.
- Validation fixtures prove the CLI, templates, and generated agent assets preserve parent AC coverage and reject or warn on unsafe epic closeout.
- project-workflow's self-hosted installation stays aligned with packaged source and generated templates so this repository can validate the workflow it ships.

## Acceptance Criteria (Verifiable)

- AC1: New epic requirements templates and agent guidance create numbered parent acceptance criteria (`AC1`, `AC2`, etc.) by default and instruct agents to preserve IDs across revisions.
- AC2: Epic tracker rows support a clear parent AC coverage convention, either as a dedicated `Parent ACs` column or a validated `Notes` format, and docs define the canonical schema.
- AC3: `epic decompose` generates proposed child rows with parent AC coverage populated for every row that originates from parent requirements or acceptance criteria.
- AC4: `epic decompose` reports parent ACs that remain unmapped after proposal generation so users see coverage gaps before approving children.
- AC5: `epic scaffold-child` copies the approved row's parent AC coverage into the child task requirements and implementation plan in a way that child QA can read directly.
- AC6: Child implementation and QA templates include explicit `Parent AC Coverage` and `Parent AC Evidence` sections for epic-managed children without adding noise to standalone tasks.
- AC7: The workflow provides an epic-level `ACCEPTANCE-AUDIT.md` or equivalent generated audit artifact that summarizes every parent AC, mapped children, evidence, verdict, and deferral status.
- AC8: A CLI command such as `epic audit` or `epic closeout` generates or validates the epic acceptance audit and fails or warns when any parent AC is unmapped, lacks evidence, lacks a verdict, or is hidden behind an unapproved deferral.
- AC9: Epic closeout cannot mark the global epic tracker row `Complete` unless the acceptance audit passes or every gap has an explicit owner-approved deferral with a follow-up task or epic reference.
- AC10: Owner-approved deferrals have a structured representation that records the deferred scope, owner decision, date, reason, and follow-up task or epic ID.
- AC11: CLI status handling covers Testing, Review, and Complete transitions needed by normal task and epic flows without requiring manual tracker edits for supported operations.
- AC12: Retro templates and agent guidance distinguish completed work, follow-up tasks, and missed in-scope work that should block completion until resolved or explicitly deferred.
- AC13: Epic-level validation evidence is summarized in the epic audit or closeout artifact rather than only scattered across child task docs.
- AC14: Documentation and generated Codex/Copilot/Cursor assets tell agents to run validation they can perform directly before asking the user for manual testing, and to distinguish verified connector evidence from deferred setup.
- AC15: The root tracker versus epic tracker rules are explicit: global tracker rows summarize epics, epic trackers own child rows, and proposed child rows do not live outside the epic folder.
- AC16: Automated tests cover fixture epics with complete coverage, missing mappings, missing evidence, approved deferrals, unapproved deferrals, and unsafe closeout attempts.
- AC17: Completing an epic-managed child task is blocked or warned when the child has assigned parent ACs but lacks parent AC evidence or an approved deferral for those ACs.
- AC18: Changes to workflow behavior are verified across package source, generated templates, generated agent assets, and this repository's installed `.project-workflow/` helper so self-hosted usage does not drift from shipped behavior.

## Open Questions (Answer Needed)

- None blocking after clarification on 2026-06-16.

## Decisions (Resolved)

- Decision: Treat this effort as an epic rather than a single task.
  - Context: The requested improvements span CLI behavior, Markdown templates, generated agent skills/prompts, documentation, and fixture tests.
  - Options considered: one broad task, several standalone tasks, or an epic with child proposals.
  - Chosen: Create `EPIC-002` and use proposal-first child tasks.
  - Why: It matches project-workflow's own guidance for multi-item work and lets parent AC coverage be modeled in the artifact this product is meant to improve.

- Decision: Do not implement product code during this setup pass.
  - Context: The delegated request explicitly asked to inspect capabilities, create the tracked effort, and draft requirements/plan before implementation.
  - Chosen: Limit this pass to workflow-state artifacts and validation of the scaffold.
  - Why: Preserves the requirements and planning gate the product is designed to enforce.

- Decision: ChatGPT/Codex connector evidence from downstream projects is a motivating example, not product-specific scope.
  - Context: Daily Checklist exposed the failure mode, but project-workflow must stay generally useful across repositories.
  - Chosen: Encode the general rule: verified evidence and deferred setup must be distinguishable in child QA and epic audit records.
  - Why: Fixes the underlying process gap without coupling project-workflow to one downstream MCP epic.

- Decision: Add a dedicated parent AC coverage field for new epic tracker rows.
  - Context: The existing `Notes` convention can carry `Covers AC1`, but the Daily Checklist failure showed coverage must be first-class enough to validate.
  - Options considered: keep using `Notes`; add a dedicated `Parent ACs` column; support both indefinitely with no canonical preference.
  - Chosen: New epic trackers should use a dedicated `Parent ACs` column, while validators read legacy `Notes` coverage for backward compatibility.
  - Why: A column is easier for agents, CLI validation, and human review to scan; backward-compatible reading avoids breaking existing epics.

- Decision: Provide both `epic audit` and `epic closeout` concepts.
  - Context: Users need to generate/check coverage before closeout, and they also need a final gate that prevents unsafe completion.
  - Options considered: one `epic audit` command only; one `epic closeout` command only; both, with separate responsibilities.
  - Chosen: `epic audit` generates or refreshes the acceptance audit without changing completion status; `epic closeout` validates the audit and enforces the completion gate.
  - Why: Separating audit from closeout supports early QA and reduces accidental completion.

- Decision: Epic closeout should not silently mark the epic complete.
  - Context: Project-workflow already requires explicit user approval for `Complete` transitions, and epic closeout should preserve that control.
  - Options considered: closeout always updates global tracker to `Complete`; closeout only validates; closeout validates and completes only with an explicit completion flag or explicit user request.
  - Chosen: Closeout validates by default and only updates the global tracker to `Complete` when completion is explicitly requested and all gates pass.
  - Why: This keeps the owner in control while still making the safe path automatable.

- Decision: Parent AC evidence should be structured but not limited to one validation type.
  - Context: Evidence may come from automated tests, command output, manual verification, code inspection, connector/OAuth setup, or approved deferral.
  - Options considered: free-form notes only; command output only; structured audit rows that can reference multiple evidence types.
  - Chosen: Use structured audit rows with AC ID, child task IDs, evidence summary, evidence source, verdict, and deferral/follow-up fields.
  - Why: This is strict enough to validate and flexible enough for different project types.

- Decision: Child-task QA must be an enforcement point, not only the final epic audit.
  - Context: In Daily Checklist, local child completion could look acceptable without proving the parent epic AC it was supposed to satisfy.
  - Chosen: Epic-managed child completion should check parent AC evidence or explicit deferral for that child before it can safely complete.
  - Why: Catching missing evidence at child QA reduces late epic closeout surprises.

- Decision: Self-hosted parity is part of this epic's definition of done.
  - Context: project-workflow is both the product and a repository using the product; drift between `src/project_workflow`, generated templates, generated agent assets, and `.project-workflow/` would hide failures.
  - Chosen: Include parity validation in the epic acceptance criteria and fixture coverage.
  - Why: This repo should prove the workflow it ships.

## Clarification Review

- Reviewed against the Daily Checklist failure mode on 2026-06-16.
- The original problem list is covered by AC1 through AC18 after adding child completion evidence gating and self-hosted parity validation.
- No blocking ambiguity remains before planning, but implementation should preserve backward compatibility for existing epic trackers that only have coverage in `Notes`.
- The riskiest implementation area is closeout enforcement: it must block unsafe completion without making normal audit iteration cumbersome.

## Initial Delivery Plan

Use the epic tracker as the source of truth for child work. Proposed rows should cover:

- Requirements, schema, and template updates for parent AC IDs and coverage.
- CLI decomposition and scaffold-child support for parent AC propagation.
- CLI audit/closeout gates for AC coverage, evidence, and deferrals.
- QA, retro, and generated agent guidance updates.
- Documentation and fixture tests covering both passing and failing epic closeout scenarios.
- Self-hosted parity checks that compare package source, generated templates, generated agent assets, and this repository's installed workflow helper.

## Validation Plan

- Run existing unit tests to establish no regression in standalone task and current epic commands.
- Add fixture tests for epic decomposition AC coverage, child scaffold AC propagation, audit generation, closeout blocking, and deferral handling.
- Run local generated workflow CLI tests and packaged `project_workflow.cli` tests to verify parity.
- Run `./.project-workflow/cli/workflow doctor` and strict validation on fixture repositories that intentionally pass and fail the new gates.
- Review generated Codex, Copilot, and Cursor assets to confirm the durable agent instructions match the implemented lifecycle.
