## User Story

As a workflow maintainer, I want a delegate agent that runs work items in sequential or parallel mode via subagents while honoring task dependencies, so that complex implementation work can be completed faster without breaking logical execution order.

## Goal

- Deliver delegated work-item execution that is dependency-aware, defaults to `sequential`, and stops on first failure (fail-fast), while keeping workflow prompt behavior aligned across requirements, planning, and implementation.

## Approach

- Implement in vertical slices: first add delegation orchestration scaffolding and mode handling, then enforce dependency scheduling and fail-fast behavior, then harden validation and prompt workflow alignment.

## Phases

### Phase 1

- Changes: Introduce `project.delegate` agent entrypoint plus delegate workflow execution path with explicit work-item input, default `sequential` mode behavior, and per-item status reporting.
- Validation: Run targeted command or tests that exercise sequential execution and verify status output ordering.
- Tracker updates: Keep story status as `Analysing` during planning and move work items to implementation-ready states.

### Phase 2

- Changes: Add explicit dependency map handling, `parallel` execution for independent items, and fail-fast halt logic on first item failure.
- Validation: Run scenario checks covering dependency blocking, parallel execution of independent items, and fail-fast stop/report behavior.
- Tracker updates: Transition story to `Plan Confirmed` only after explicit user confirmation.

## Task List (for IMPLEMENTATION.md)

|  ID | Title                                            | Description                                                                                                                                                                      | Acceptance Criteria                                                                                                                                                                                                                                                                                                                                                                  | User Verification                                                                                                                                                                                                                                                                                                                                                                  | Status   |
| --: | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
|   1 | Create `project.delegate` agent entrypoint       | Add a new `project.delegate` agent command surface and wire it to delegated execution via `project.implement`.                                                                   | - `project.delegate` agent definition exists in `.github/prompts` and mirrored packaged prompts under `src/project_workflow/prompts`.<br>- Invoking `project.delegate` routes delegated work items through the implement command path.<br>- Existing agent names/flows remain unchanged.                                                                                             | - Run workflow help/listing and confirm `project.delegate` is available.<br>- Execute a minimal delegate scenario and confirm it dispatches via `project.implement`.                                                                                                                                                                                                               | Complete |
|   2 | Sequential delegate execution baseline           | Add delegate execution that accepts work items and runs them in deterministic order with `sequential` as the default mode when mode is omitted.                                  | - Delegate command accepts work-item input and executes one item at a time in order.<br>- Omitting mode results in `sequential` execution.<br>- Output includes per-item lifecycle states and final summary.                                                                                                                                                                         | - Run delegate flow with 3 independent items and no mode flag; confirm execution order is 1→2→3 and statuses are visible.                                                                                                                                                                                                                                                          | Complete |
|   3 | Dependency-aware parallel scheduling             | Enable `parallel` execution for independent items while enforcing explicit dependency-map prerequisites before starting dependent items.                                         | - Dependency map is required/consumed for ordering decisions.<br>- Unknown IDs, self-dependencies, and cycles are rejected before any execution starts.<br>- In `parallel` mode without an explicit limit, execution uses a default cap of 4 workers.<br>- Independent items can run concurrently in `parallel` mode and dependent items do not start before prerequisites complete. | - Run delegate flow with an invalid dependency map (unknown ID/cycle/self-dependency) and confirm run is rejected before execution.<br>- Run delegate flow in `parallel` mode without a limit and confirm at most 4 eligible items run concurrently.<br>- Run delegate flow with valid dependencies and confirm independents overlap while dependent items wait for prerequisites. | Complete |
|   4 | Fail-fast and completion reporting               | Enforce fail-fast behavior that stops launching new pending items after first failure while allowing already-running items to finish, and report halted/failed outcomes clearly. | - First failure halts launch of remaining pending items.<br>- Already-running items are allowed to finish and are reported with terminal state.<br>- Final summary clearly identifies failure cause and halted items.                                                                                                                                                                | - Run delegate flow where one item intentionally fails while another is in-flight; confirm no new pending items start, in-flight item completes, and final report lists failed + halted items.                                                                                                                                                                                     | To Do    |
|   5 | Prompt workflow alignment and validation mapping | Align workflow prompt behavior so requirements, planner, and implement flows remain consistent with delegate constraints and acceptance criteria verification.                   | - Planning and implementation docs remain consistent with requirements decisions.<br>- Each acceptance criterion has a mapped validation step.<br>- No unresolved story conflicts between requirements and implementation docs.                                                                                                                                                      | - Review requirements + implementation docs and confirm consistent user story, constraints, and validation mapping for all acceptance criteria.                                                                                                                                                                                                                                    | To Do    |

## Files / Areas Likely to Change

- `.github/prompts/Delegate.prompt.md`
- `.github/prompts/Requirements.prompt.md`
- `.github/prompts/Planner.prompt.md`
- `.github/prompts/Implement.prompt.md`
- `src/project_workflow/prompts/Delegate.prompt.md`
- `src/project_workflow/prompts/Requirements.prompt.md`
- `src/project_workflow/prompts/Planner.prompt.md`
- `src/project_workflow/prompts/Implement.prompt.md`
- `src/project_workflow/cli.py`
- `src/project_workflow/templates/workflow`
- `src/project_workflow/templates/workflow.py`

## Data / RLS / RPC / Migrations

- None expected.

## Risks & Mitigations

- Risk: Non-deterministic behavior in `parallel` mode when dependencies are incomplete.<br>Mitigation: require explicit dependency map validation before execution starts.
- Risk: Prompt drift between dev prompts and packaged prompts.<br>Mitigation: mirror any prompt edits in both `.github/prompts/` and `src/project_workflow/prompts/` within the same change.
- Risk: Fail-fast behavior ambiguity for in-flight work items.<br>Mitigation: define and test explicit terminal-state reporting for running, failed, and not-started items.

## Notes

- Task: APP-002
- Title: Delegate Agent
- Created: 2026-02-16
