## Overview

- Goal (in user terms): Enable teams to group related stories under an epic and scaffold the full epic structure quickly while preserving the existing one-off task workflow.
- Primary user(s): Repository maintainers and developers using the project workflow CLI and prompts.
- Desired outcome: A user can create an epic with its own requirements and tracker, iteratively tighten epic scope with the agent, propose child tasks/stories into the epic tracker, and only scaffold approved child items; branch flows support epic parent branches and child branches derived from them.

## User Story

As a product maintainer, I want each epic to have its own requirements and tracker where child tasks are proposed and reviewed before scaffolding, so that multi-step features can be tightened collaboratively and delivered coherently while still supporting standalone one-off tasks.

## In Scope

- Add epic-level scaffolding support in the workflow tooling.
- Add epic-level REQUIREMENTS.md and TRACKER.md artifacts.
- Allow creation of task/story scaffolds as children of an epic after proposal review.
- Preserve support for one-off standalone task/story scaffolding.
- Define tracker behavior so epic and child task records remain visible and auditable in both global and epic-local trackers.
- Define branch workflow expectations for epic branch creation and child branch derivation.
- Add an agent/prompt flow that decomposes epic requirements into proposed child tasks/stories, updates epic tracker proposal rows, and scaffolds only approved items.

## Out of Scope

- Implementing task execution orchestration beyond scaffolding and tracking.
- Changing existing core prompt order outside additions needed for epic decomposition workflow.
- Enforcing a specific git hosting strategy beyond documented branch defaults and options.
- Migrating historical tasks into epics automatically.

## Requirements

List requirements as outcomes/expectations, not implementation details.

### Functional Requirements

- Users can scaffold an epic with an ID and title.
- Epic workflow support is delivered in both development artifacts in this repository and packaged install artifacts used by end users.
- Epic scaffolding creates a stable folder path at tasks/epics/<EPIC-ID>-<Suffix>/ and creates epic REQUIREMENTS.md and epic TRACKER.md suitable for downstream requirements, clarify, planner, and implement steps.
- Users can scaffold child tasks/stories under an epic folder, each with its own IMPLEMENTATION.md and REQUIREMENTS.md docs.
- Users can still scaffold standalone one-off tasks/stories at tasks/<ID>-<Suffix> without an epic parent.
- Child tasks/stories under epics use the same globally unique flat ID strategy as standalone tasks/stories.
- Global tracker entries represent epic summary rows for epic-managed work only, while epic TRACKER.md is the source of truth for epic child task/story rows at all stages (Proposed through Complete).
- Epic TRACKER.md uses status lifecycle Proposed -> Approved -> In Progress -> Testing -> Complete, and only Approved items are eligible for scaffold.
- Items can be moved from Proposed to Approved either by manual status edit or by dedicated CLI approval command; CLI writes the same markdown status change semantics as manual editing.
- The workflow includes a dedicated agent/prompt path that reads epic REQUIREMENTS.md, proposes a child task/story breakdown, writes proposed rows into epic TRACKER.md, and scaffolds only user-approved items.
- During scaffold confirmation for approved epic child tasks, workflow reserves the next available globally unique task IDs automatically.
- Epic branch creation is supported, and child task/story branch creation can derive from the epic branch.
- If child branch creation is requested for an epic child task and the epic branch is missing, workflow fails fast with a clear error and requires creating/selecting the epic branch first.
- Existing task-only scaffold behavior remains available for backward compatibility.
- Epic support changes that affect prompt behavior are mirrored between .github/prompts and src/project_workflow/prompts.
- Epic support changes that affect local workflow CLI template behavior are mirrored between .project-workflow/cli/workflow.py output and src/project_workflow/templates/workflow.py packaged template behavior.
- Epic scaffold and epic child scaffold operations are idempotent on safe re-run and do not duplicate tracker rows or corrupt existing files.
- Epic TRACKER.md schema is explicitly defined and enforced, including required columns and status semantics for Proposed and Approved stages.
- Epic TRACKER.md canonical required columns are ID, Title, Status, Type, Docs, Branch, and Notes.
- Scaffold operations use deterministic failure handling that avoids split state across folders, tracker entries, and branch operations.
- ID allocation collisions for auto-reserved child IDs are detected and resolved deterministically with clear user messaging.
- User-facing docs and command help are updated to include epic workflow, proposal approval gate, and branch-lineage rules.

### Non-Functional Requirements

- Performance / latency: Scaffolding operations should complete fast enough for interactive CLI usage and avoid unnecessary repeated prompts.
- Security / permissions: No privilege escalation or secret handling changes; operations respect local git permissions and current repo access.
- Accessibility: Prompt instructions and generated docs remain plain Markdown and readable in standard editors.
- Observability (logs/metrics/audit expectations): CLI output clearly reports created folders/files, tracker updates, and branch names for auditability.

## Acceptance Criteria

- AC1: A user can scaffold an epic with ID and title, and the command creates tasks/epics/<EPIC-ID>-<Suffix>/ with epic REQUIREMENTS.md and epic TRACKER.md.
- AC2: A user can run epic requirements iteration with the agent and keep epic REQUIREMENTS.md updated without creating child task/story scaffolds yet.
- AC3: A user can run epic decomposition to generate proposed child tasks/stories, and proposals are written into epic TRACKER.md before scaffold confirmation.
- AC4: A user can confirm selected proposals and scaffold one or more child tasks/stories under the epic, each with required docs.
- AC5: A user can scaffold a standalone one-off task/story at tasks/<ID>-<Suffix> outside any epic using the existing explicit workflow path.
- AC6: Tracker status and linkage clearly show epic records in global tracker and child records in epic tracker while requirements are captured as Analysing.
- AC7: Epic branch creation and child branch-from-epic behavior are supported and reported to the user.
- AC8: Existing task-only scaffold flow continues to work for repos not using epics.
- AC9: Epic capabilities are available both when developing in this repository and when using installed `project` CLI/package outputs.
- AC10: Prompt and template mirror rules are satisfied so epic behavior is consistent between repository development files and packaged install artifacts.
- AC11: Re-running epic init or child scaffold commands does not create duplicate tracker rows and does not overwrite user-modified files without explicit overwrite intent.
- AC12: Epic tracker schema (columns, statuses, and approval-gating semantics) is documented and validated by command behavior.
- AC13: Failure paths during epic or child scaffolding leave the workflow in a deterministic, recoverable state with clear remediation messages.
- AC14: README and command help include accurate epic usage, including decomposition proposal review, approval gating, and epic-to-child branch behavior.

## Assumptions

- Epic and child tasks/stories share the same task ID naming pattern style already used in this repo.
- Users may choose either develop or main as epic branch base depending on team workflow.
- Child branches should default to branching from the epic branch when one exists.
- Epic decomposition defaults to proposal-first workflow where scaffolding occurs only after explicit user confirmation.

## Open Questions

- None at this time.

## Decisions Log

- Decision:
  - Context: Need to preserve existing task support while introducing epic support.
  - Options considered: Replace task-only flow vs additive epic flow.
  - Chosen: Additive epic support while preserving task-only flow.
  - Why: Minimizes disruption and keeps backward compatibility.

- Decision:
  - Context: Standalone one-off task location.
  - Options considered: Keep tasks/<ID>-<Suffix> vs move to tasks/generic/<ID>-<Suffix> vs support both.
  - Chosen: Keep tasks/<ID>-<Suffix> as default location.
  - Why: Preserves existing workflow and avoids migration churn.

- Decision:
  - Context: Epic folder layout.
  - Options considered: tasks/epics/<EPIC-ID>-<Suffix> vs tasks/<EPIC-ID>-<Suffix> plus marker.
  - Chosen: tasks/epics/<EPIC-ID>-<Suffix>.
  - Why: Explicit folder typing improves discoverability and reduces ambiguity.

- Decision:
  - Context: Epic decomposition and scaffold timing.
  - Options considered: Auto-scaffold immediately vs confirm first vs configurable default.
  - Chosen: Proposal-first flow with confirmation before scaffolding.
  - Why: Supports iterative tightening and human validation before creating child artifacts.

- Decision:
  - Context: Global tracker representation for epic-managed child items.
  - Options considered: Global epic rows only vs global epic + all child rows vs global epic + in-progress child rows.
  - Chosen: Global tracker contains epic rows only; epic TRACKER.md is source of truth for child rows.
  - Why: Keeps top-level tracker readable and delegates detailed decomposition/progress to epic-local tracker.

- Decision:
  - Context: Child task ID strategy for epic-managed tasks.
  - Options considered: Global flat IDs vs epic-scoped IDs vs mixed mode.
  - Chosen: Keep globally unique flat IDs for child tasks (same pattern as standalone tasks).
  - Why: Simplifies CLI validation, branch naming, cross-epic movement, and audit traceability.

- Decision:
  - Context: Epic tracker lifecycle before scaffolding proposed child tasks.
  - Options considered: Proposed->Approved->In Progress->Testing->Complete vs existing statuses plus Approved column vs Proposed/Complete only.
  - Chosen: Proposed -> Approved -> In Progress -> Testing -> Complete, with scaffold allowed only from Approved.
  - Why: Gives explicit approval gating, clear progress semantics, and low risk of accidental scaffold.

- Decision:
  - Context: Child branch request when epic branch is missing.
  - Options considered: Fail fast vs auto-create epic branch vs fallback to base with warning.
  - Chosen: Fail fast with clear error; require creating/selecting epic branch first.
  - Why: Preserves deterministic branch lineage and avoids implicit branch topology changes.

- Decision:
  - Context: Child task ID allocation during epic decomposition scaffold.
  - Options considered: Agent-proposed IDs with conflict prompts vs auto-reserve next available IDs vs manual IDs per child.
  - Chosen: Auto-reserve next available globally unique IDs during scaffold confirmation.
  - Why: Reduces collision risk and user overhead while preserving global ID consistency.

- Decision:
  - Context: Canonical epic tracker schema for proposal and execution phases.
  - Options considered: Rich schema with Type/Branch/Notes vs minimal schema vs explicit Parent Epic/Approval By schema.
  - Chosen: Required columns are ID, Title, Status, Type, Docs, Branch, Notes.
  - Why: Provides sufficient structure for automation and auditability without over-constraining future evolution.

- Decision:
  - Context: Approval mechanism for moving items from Proposed to Approved in epic tracker.
  - Options considered: Manual status edits only vs CLI-only approval vs support both with identical markdown semantics.
  - Chosen: Support both manual status edits and CLI approval command, with CLI writing equivalent markdown status updates.
  - Why: Balances UX flexibility with deterministic and auditable tracker semantics.

- Decision:
  - Context: Whether epic child items should appear in global tracker.
  - Options considered: Add child rows after scaffold vs add proposed child rows immediately vs keep child rows only in epic tracker.
  - Chosen: Keep epic child rows only in epic tracker; do not add child rows to global tracker.
  - Why: Maintains global tracker readability and reinforces epic tracker as the canonical source for child execution details.

- Decision:
  - Context: Requirements capture phase status handling in tracker.
  - Options considered: Keep To Do during analysis vs set Analysing.
  - Chosen: Set APP-003 status to Analysing during requirements capture.
  - Why: Matches workflow prompt requirements and improves lifecycle visibility.

## Validation Plan (User-Facing)

- How the user will verify done:
  - AC1 -> Run epic scaffold command with ID/title and verify tasks/epics/<EPIC-ID>-<Suffix>/ exists with epic REQUIREMENTS.md and epic TRACKER.md.
  - AC2 -> Execute at least one epic requirements pass and confirm epic REQUIREMENTS.md updates without child scaffold side effects.
  - AC3 -> Run epic decomposition and verify proposed child rows are written to epic TRACKER.md in Proposed state before any child scaffold.
  - AC4 -> Confirm selected proposed rows and verify only selected child folders/docs are scaffolded under the epic.
  - AC5 -> Run standalone task/story scaffold command and verify tasks/<ID>-<Suffix> location and docs are created correctly.
  - AC6 -> Open global and epic trackers and verify global shows epic rows while epic tracker shows child rows, with Analysing status behavior during requirements capture.
  - AC7 -> Run epic branch creation then child branch creation; verify child branch starts from epic branch and names are reported.
  - AC8 -> Re-run existing task-only scaffold examples and verify no regression.
  - AC9 -> Validate epic workflow via local dev artifacts and via installed package command path to confirm parity.
  - AC10 -> Verify prompt and template behavior parity across .github/prompts, src/project_workflow/prompts, and packaged workflow template outputs.
  - AC11 -> Execute repeat runs of epic init and child scaffold commands and verify no duplicate tracker rows or unintended file overwrites.
  - AC12 -> Validate epic tracker file format and status transitions, including enforcement that only Approved entries can scaffold.
  - AC13 -> Simulate failures in folder creation/tracker update/branch creation paths and verify deterministic recoverable outcomes with actionable messages.
  - AC14 -> Verify README and command --help output match implemented epic flow and branch/approval semantics.
- Rollout notes (if any): Start with additive CLI options/flags so existing commands remain valid.
