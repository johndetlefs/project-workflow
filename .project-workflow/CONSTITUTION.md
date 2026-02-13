# Constitution

## Mission

- Help teams ship software predictably by using a spec-driven, agent-assisted workflow centered on clear outcomes, traceable decisions, and iterative validation.

## Target Users

- Primary users:
  - Individual developers and small teams using GitHub Copilot in VSCode.
- Secondary users:
  - Engineering leads and collaborators who need visibility into scope, status, and delivery confidence through repository-native artifacts.

## Core Outcomes

- Every feature starts with a clearly stated user/business outcome before implementation begins.
- Teams maintain a shared, auditable path from idea → requirements → plan → implementation using standardized task artifacts.
- Ambiguities are surfaced and resolved deliberately before coding proceeds, reducing rework and conflicting assumptions.
- Delivery status is transparent via a lightweight tracker that reflects real progress and validation state.
- The workflow remains easy to adopt: repository-native, low-overhead, and compatible with existing git-based collaboration.

## Non-Goals

- Replacing issue trackers, project management platforms, or sprint planning systems.
- Enforcing a single engineering stack, architecture, or coding style.
- Creating a heavyweight governance process that slows feature delivery.
- Producing deeply technical architecture standards in this document.

## Product Principles

- Outcome-first: define success in user/business terms before discussing implementation.
- Clarity over speed: resolve unknowns and conflicts explicitly before execution.
- Repository-native truth: keep artifacts close to code so decisions are reviewable and versioned.
- Incremental progress: favor small, verifiable steps with explicit validation.
- Human-in-the-loop: agents assist and accelerate, but users retain decision authority.

## Success Signals

- New work consistently includes task scaffolding, requirements, and implementation artifacts linked by task ID.
- Teams report fewer mid-implementation scope reversals caused by unclear requirements.
- Clarification and planning happen before implementation in the majority of completed tasks.
- Tracker status changes reflect real lifecycle movement (e.g., To Do → In Progress → Testing → Complete).
- Adoption remains strong because setup and day-to-day usage stay simple and fast.

## Decision Filters

- Does this change improve outcome clarity for users and teams?
- Does it preserve traceability from requirement to implementation?
- Does it reduce ambiguity or hidden assumptions before coding?
- Does it keep workflow overhead low relative to value delivered?
- Does it maintain flexibility across project types without becoming vague?

## Assumptions & Risks

- Assumption: Teams are willing to maintain Markdown artifacts as part of normal development flow.
- Assumption: Users have access to GitHub Copilot chat workflows in their environment.
- Risk: Teams may skip clarification/planning steps under time pressure, reducing quality.
- Risk: Overly prescriptive prompts could reduce fit for diverse projects.
- Risk: If technical guidance is missing or weak, teams may confuse outcome guidance with implementation policy.

## Change Log

- 2026-02-13: Initial constitution created from repository context; defined mission, outcomes, principles, and governance boundaries.
