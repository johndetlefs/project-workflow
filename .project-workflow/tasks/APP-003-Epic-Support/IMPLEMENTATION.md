## User Story

As a product maintainer, I want each epic to have its own requirements and tracker where child tasks are proposed and reviewed before scaffolding, so that multi-step features can be tightened collaboratively and delivered coherently while still supporting standalone one-off tasks.

## Goal

- Deliver end-to-end epic workflow support (scaffold, decomposition proposal, approval-gated child scaffold, tracker/branch rules) with parity across repository development usage and installed package usage, while preserving existing standalone task behavior.

## Approach

- Extend current task-centric CLI with additive epic-aware commands/flags and explicit status/approval semantics.
- Keep global tracker high-level and epic-local tracker detailed.
- Enforce deterministic branch and ID allocation behaviors to reduce user error and state drift.
- Preserve backward compatibility by keeping existing standalone task flows unchanged.
- Validate parity across dev artifacts and packaged artifacts, including mirrored prompts/templates.

## Phases

### Phase 1

- Changes:
  - Add epic scaffold capability and epic folder/doc schema.
  - Define and enforce epic TRACKER.md schema and lifecycle states.
  - Add decomposition proposal flow that writes Proposed rows before scaffold.
  - Add approval-gated child scaffold with automatic global ID reservation.
- Validation:
  - Validate AC1-AC4, AC6, AC11, AC12 using local workflow command path.
  - Validate deterministic and idempotent behavior on re-runs.
- Tracker updates:
  - Keep APP-003 as Analysing until plan is approved.
  - Move to In Progress after user confirms this plan.

### Phase 2

- Changes:
  - Add branch lineage enforcement and fail-fast behavior.
  - Ensure prompt/template mirror parity and packaged parity.
  - Preserve standalone task behavior and update docs/help for epic flow.
  - Add failure-path handling and user remediation messaging.
- Validation:
  - Validate AC5, AC7-AC10, AC13, AC14 across both local and installed command paths.
  - Run parity checks for .github/prompts vs src/project_workflow/prompts and workflow templates.
- Tracker updates:
  - Move APP-003 to Testing once all planned outcomes are implemented.
  - Move to Complete only after validation is confirmed and user explicitly requests completion.

## Task List

|  ID | Title                                       | Description                                                                                                                                                                           | Acceptance Criteria                                                                                                                                                                                                                                                                                                                                                               | User Verification                                                                                                                                                                                                                                                                            | Status   |
| --: | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
|   1 | Epic Scaffold Baseline                      | Users can create an epic at tasks/<EPIC-ID>-<Suffix>/ with epic REQUIREMENTS.md and epic TRACKER.md using additive CLI behavior, and epic IDs are assigned sequentially by the CLI.   | - Epic scaffold command creates required epic folder and docs.<br>- Global tracker receives epic summary row behavior per requirements.<br>- Re-running epic scaffold does not duplicate tracker rows or overwrite user files unless explicit overwrite intent is provided.                                                                                                       | - Run epic scaffold for a title input and confirm the assigned ID and folder/docs exist.<br>- Re-run command and confirm no duplicate rows/files are created.                                                                                                                                | Complete |
|   2 | Epic Tracker Schema And Gating              | Epic TRACKER.md uses enforced schema and lifecycle Proposed -> Approved -> In Progress -> Testing -> Complete, and only Approved rows can be scaffolded into child tasks.             | - Epic tracker file includes documented required columns (ID, Title, Status, Type, Docs, Branch, Notes) and valid status transitions.<br>- Scaffold attempt for non-Approved row fails with clear message.<br>- Approved row can proceed to scaffold path.<br>- Approval works via both manual status edit and dedicated CLI approval command with equivalent markdown semantics. | - Create Proposed row and attempt scaffold; confirm rejection message.<br>- Mark row Approved manually and scaffold; confirm success.<br>- Reset another row to Proposed, approve via CLI command, and confirm resulting markdown status change and scaffold success.                        | Complete |
|   3 | Decomposition Proposal Agent Flow           | A dedicated epic decomposition flow reads epic REQUIREMENTS.md and writes candidate child task rows into epic TRACKER.md in Proposed state without creating child folders yet.        | - Decomposition operation writes Proposed rows only.<br>- No child task docs/folders are created during proposal-only pass.<br>- Proposal output is traceable in epic tracker.                                                                                                                                                                                                    | - Run decomposition pass and confirm Proposed rows appear in epic tracker.<br>- Confirm no child task folders were created yet.                                                                                                                                                              | Complete |
|   4 | Approval-Gated Child Scaffold With Auto IDs | Approved proposed rows can be scaffolded into child tasks under the epic, each with IMPLEMENTATION.md and REQUIREMENTS.md, and IDs are auto-reserved using next available global IDs. | - Child scaffold creates required docs under epic path for selected Approved rows.<br>- Auto ID allocation chooses next available global IDs deterministically.<br>- ID collisions are handled with deterministic resolution and clear messaging.<br>- Global tracker remains epic-summary only and does not receive epic child rows during/after child scaffold.                 | - Approve two proposals and scaffold them; confirm child docs exist and IDs are globally unique.<br>- Simulate ID collision and verify deterministic resolution message.<br>- Check global tracker and confirm no new child rows were added; child progression remains in epic tracker only. | Complete |
|   5 | Epic Branch Lineage Enforcement             | Child branch creation from epic-managed tasks enforces lineage to epic branch and fails fast if epic branch is missing, with actionable remediation guidance.                         | - Child branch creation succeeds when epic branch exists.<br>- Missing epic branch causes fail-fast with clear remediation steps.<br>- No implicit fallback to base branch for epic child branch creation.                                                                                                                                                                        | - Attempt child branch creation without epic branch and verify clear fail-fast error.<br>- Create epic branch and retry; verify child branch derives from epic branch.                                                                                                                       | To Do    |
|   6 | Standalone Task Backward Compatibility      | Existing standalone task workflow remains unchanged for non-epic usage, including current paths and command semantics.                                                                | - Existing task init commands still scaffold tasks/<ID>-<Suffix> as before.<br>- Existing examples and command usage remain valid.<br>- Epic features are additive and do not require adoption for one-off tasks.                                                                                                                                                                 | - Run existing standalone task init command examples and compare output behavior with current baseline.                                                                                                                                                                                      | To Do    |
|   7 | Dev-Packaged Parity And Mirrors             | Epic support behavior remains consistent between repository development flows and installed package flows, including prompt/template mirror requirements.                             | - Epic-related prompt changes are mirrored between .github/prompts and src/project_workflow/prompts.<br>- Workflow template behavior is mirrored for local generated workflow.py and packaged template outputs.<br>- Installed project command path exhibits same epic behavior as local repo flow.                                                                               | - Validate mirrored files exist with aligned behavior.<br>- Install package in clean environment and run epic flow; confirm parity with local flow.                                                                                                                                          | To Do    |
|   8 | Failure Recovery Determinism                | Epic and child scaffold failures leave state recoverable and deterministic across file system, tracker, and branch operations with explicit remediation messages.                     | - Partial failures do not leave ambiguous tracker/branch state.<br>- Error messages provide clear next action.<br>- Re-running after remediation succeeds without manual cleanup beyond documented steps.                                                                                                                                                                         | - Simulate failure cases for file write, tracker update, and branch operations; verify recoverable state and actionable error messaging.                                                                                                                                                     | To Do    |
|   9 | Documentation And Command Help              | README and CLI help document epic workflow end-to-end, including decomposition proposals, approval gating, ID allocation behavior, and branch-lineage rules.                          | - README includes accurate epic usage walkthrough and examples.<br>- CLI --help text reflects epic commands/options and constraints.<br>- Docs reflect both local workflow script and installed project command usage.                                                                                                                                                            | - Review README and run help commands; confirm instructions match actual observed behavior in both execution modes.                                                                                                                                                                          | To Do    |

## Notes

- Task: APP-003
- Title: Epic Support
- Created: 2026-03-20
