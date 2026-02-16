## Overview

- Goal (in user terms): Add a delegate agent that can execute work items through subagents in either sequential or parallel mode, with dependency-aware ordering.
- Primary user(s): Workflow maintainers using project agents to implement complex tasks.
- Desired outcome: Maintainers can invoke a single delegate workflow that reliably dispatches and coordinates subagent work according to selected execution mode.

## User Story

As a workflow maintainer, I want a delegate agent that runs work items in sequential or parallel mode via subagents while honoring task dependencies, so that complex implementation work can be completed faster without breaking logical execution order.

## In Scope

- Define expected behavior for sequential and parallel delegation modes.
- Define dependency handling rules that preserve logical order when tasks depend on prior outputs.
- Define completion behavior and user-visible confirmation for delegated work items.
- Define failure handling expectations for one or more subagent work item failures.
- Create a new `project.delegate` agent entrypoint and keep dev and packaged agent definitions in sync.
- Update prompt behavior in `project.requirements`, `project.planner`, and `project.implement` so delegated execution expectations are consistent across workflow stages.

## Out of Scope

- Replacing existing `project.implement` behavior outside delegated execution paths.
- Introducing unrelated workflow prompts or new planning frameworks.
- Building non-agent UI surfaces.

## Requirements

List requirements as outcomes/expectations, not implementation details.

### Functional Requirements

- The workflow provides a `project.delegate` agent command that users invoke for delegated work-item execution.
- The delegate workflow accepts a set of work items and an execution mode (`sequential` or `parallel`).
- If no mode is provided, the delegate workflow defaults to `sequential`.
- In `sequential` mode, work items execute one at a time in defined order.
- In `parallel` mode, independent work items may execute concurrently, while declared dependencies are respected.
- In `parallel` mode, if no worker limit is provided, the workflow uses a default limit of 4 concurrent workers.
- Dependencies are supplied as an explicit dependency map in command input.
- If a work item depends on another, the dependent item does not start until its prerequisite item is complete.
- If any work item fails, the workflow uses fail-fast behavior and does not start additional pending items.
- Each delegated work item uses the `project.implement` command path for subagent execution.
- The workflow reports per-item status (not started, in progress, completed, failed) and final aggregate result.

### Non-Functional Requirements

- Performance / latency: Delegation overhead should be minimal relative to subagent execution time; parallel mode should reduce total wall-clock time for independent items.
- Security / permissions: Delegated execution uses existing repository and agent permission boundaries; no privilege escalation is introduced.
- Accessibility: User-facing outputs remain clear, concise, and readable in terminal/CLI contexts.
- Observability (logs/metrics/audit expectations): Execution mode, dependency decisions, and per-item outcomes are captured in user-visible run output.

## Acceptance Criteria

- Given workflow setup is complete, when the user invokes `project.delegate`, then the delegate agent entrypoint is available and routes delegated items through `project.implement`.
- Given a list of work items without an explicit mode, when execution starts, then the workflow uses `sequential` mode by default.
- Given a list of work items in `sequential` mode, when execution starts, then items run one-by-one in order and each item emits completion status before the next starts.
- Given a list with independent and dependent items in `parallel` mode, when execution starts, then independent items can run concurrently and dependent items wait for prerequisites.
- Given `parallel` mode without an explicit worker limit, when execution starts, then no more than 4 eligible work items run concurrently.
- Given any failed work item, when failure occurs, then the workflow stops launching new pending items (fail-fast) and final output identifies failed item(s) and overall result clearly.
- Given task input, when dependencies are evaluated, then an explicit dependency map is used to determine prerequisites.
- Given dependency-map input, when validation runs before execution, then unknown IDs, self-dependencies, and cycles cause immediate rejection with no work items started.
- Given delegated execution, when each item is processed, then the delegated command path used is `project.implement`.

## Assumptions

- Work items can be uniquely identified and mapped to dependency relationships.
- Existing agent infrastructure supports launching multiple subagent runs when needed.
- Dependency metadata is provided explicitly in command input at delegation time.

## Open Questions

- None.

## Decisions Log

- Decision:
  - Context: Default execution mode for the delegate workflow.
  - Options considered: `sequential`, `parallel`, explicit required each run.
  - Chosen: `sequential`.
  - Why: Predictable ordering is safer as the default behavior.
- Decision:
  - Context: Failure handling strategy for delegated work.
  - Options considered: fail-fast, best-effort, user-selectable per run.
  - Chosen: Fail-fast.
  - Why: Reduces cascading errors and keeps execution state easier to reason about.
- Decision:
  - Context: Fail-fast handling for already-running work items when first failure occurs.
  - Options considered: finish in-flight items, cancel in-flight items, configurable per run.
  - Chosen: Finish in-flight items and block any new pending starts.
  - Why: Preserves deterministic reporting without adding cancellation complexity.
- Decision:
  - Context: Dependency specification format.
  - Options considered: explicit dependency map, ordered list only, tracker/task-doc inference.
  - Chosen: Explicit dependency map in command input.
  - Why: Makes ordering deterministic and avoids hidden inference.
- Decision:
  - Context: Validation policy for explicit dependency-map input.
  - Options considered: strict reject-on-invalid, permissive warn-and-skip, mixed strict/permissive.
  - Chosen: Strict validation (reject unknown IDs, self-dependencies, and cycles before execution).
  - Why: Maximizes correctness and predictability, and avoids partial execution on invalid inputs.
- Decision:
  - Context: Default worker limit for `parallel` mode when no explicit limit is provided.
  - Options considered: unlimited concurrency, fixed safe default, environment-based auto scaling.
  - Chosen: Fixed safe default of 4 workers.
  - Why: Provides predictable performance and resource usage across environments.
- Decision:
  - Context: Prompt coverage needed to deliver delegate behavior consistently.
  - Options considered: update only implement flow, update all workflow stages involved in requirement/plan/execute handoff.
  - Chosen: Update `project.requirements`, `project.planner`, and `project.implement`.
  - Why: Keeps requirements capture, planning, and execution aligned around explicit dependency-driven delegation.

## Validation Plan (User-Facing)

- How the user will verify “done”: Run the delegate workflow with a sample set of independent + dependent work items in both execution modes and verify ordering, concurrency, and per-item status reporting.
- Rollout notes (if any): Start with internal usage on small task sets, then expand to broader workflow usage once behavior is stable.
