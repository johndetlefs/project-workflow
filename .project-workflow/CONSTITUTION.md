# Constitution

## Mission

- Make repository-native, agent-assisted delivery the obvious default for turning intent into trustworthy shipped outcomes, from a solo developer to a governed engineering organization.

## Target Users

- Primary users:
  - Individual developers and small teams using Cursor, OpenAI Codex, GitHub Copilot, or a mix of coding agents.
- Secondary users:
  - Engineering leads and collaborators who need visibility into scope, status, and delivery confidence through repository-native artifacts.
  - Organizations that need stronger approval, policy, evidence, integration, and audit controls without imposing those controls on every project.

## Core Outcomes

- Every feature starts with a clearly stated user/business outcome before implementation begins.
- Teams maintain one unambiguous, auditable path from idea → requirements → plan → implementation → validated completion → integration or release receipt.
- Ambiguities are surfaced and resolved deliberately before coding proceeds, reducing rework and conflicting assumptions.
- Delivery status is transparent via a lightweight tracker that reflects real progress and validation state.
- Quality and maintainability are protected by an explicit QA/code review gate before completion.
- Completed tasks feed reusable lessons back into conventions and agent guidance so future work stays internally consistent.
- The workflow remains easy to adopt: repository-native, low-overhead, and compatible with existing git-based collaboration.
- The next meaningful action and the actual delivery state remain obvious to both people and agents.
- Assurance scales with consequence: lightweight local proof for low-risk work, stronger independent or platform-backed proof where risk and governance require it.
- Teams can integrate their existing source control, CI, release, deployment, identity, and policy systems without forking the core workflow.

## Non-Goals

- Replacing issue trackers, project management platforms, or sprint planning systems.
- Replacing git hosts, CI systems, package registries, deployment platforms, or organizational identity providers.
- Enforcing a single engineering stack, architecture, or coding style.
- Creating a heavyweight governance process that slows feature delivery.
- Requiring enterprise ceremony for solo developers, prototypes, or low-risk changes.
- Maximizing the number of documents, prompts, commands, or integrations without a demonstrated user outcome.
- Producing deeply technical architecture standards in this document.

## Product Principles

- Outcome-first: define success in user/business terms before discussing implementation.
- Proportionate rigor: resolve material unknowns before execution while keeping ceremony proportional to risk and value.
- Repository-native truth: keep artifacts close to code so decisions are reviewable and versioned.
- Truth over artifact presence: distinguish declared, self-attested, independently verified, and externally authoritative evidence.
- Useful by default: make status, blockers, and the next action obvious without requiring workflow expertise.
- Incremental progress: favor small, verifiable steps with explicit validation.
- Human-in-the-loop: agents assist and accelerate, but users retain decision authority.
- Integrate rather than replace: use established delivery systems as authoritative sources where they already own the truth.
- Extensible without forking: keep the core coherent while allowing policy, evidence, and platform adapters at stable boundaries.

## Success Signals

- New work consistently has an outcome, an accountable approval boundary, and delivery evidence linked by task ID.
- Teams report fewer mid-implementation scope reversals caused by unclear requirements.
- Clarification and planning happen before implementation in the majority of completed tasks.
- Tracker status changes reflect real lifecycle movement (e.g., To Do → In Progress → Testing → Review → Complete).
- Completed tasks regularly produce useful retro notes or explicit "no durable updates needed" records.
- Adoption remains strong because setup and day-to-day usage stay simple and fast.
- Users can identify the true delivery state and next action in one interaction, including whether work is merely complete in-repo or has actually been integrated, released, or deployed.
- The same core workflow succeeds across individual, team, and governed-enterprise assurance profiles without separate forks.
- Safe upgrades, immutable releases, and stable extension boundaries make long-lived adoption lower-risk than improvised local process.
- Real repositories demonstrate reduced rework, faster handoff, and more reliable agent execution rather than adoption being measured by generated artifacts alone.

## Decision Filters

- Does this change improve outcome clarity for users and teams?
- Does it preserve traceability from requirement to implementation?
- Does it reduce ambiguity or hidden assumptions before coding?
- Does it keep workflow overhead low relative to value delivered?
- Does it maintain flexibility across project types without becoming vague?
- Does it improve an actual user outcome, unblock delivery, or materially reduce risk beyond what the current workflow already provides?
- Is the proposed assurance level proportionate to the consequence of being wrong?
- Does it strengthen a stable core or extension boundary instead of adding another special case?

## Assumptions & Risks

- Assumption: Teams are willing to maintain Markdown artifacts as part of normal development flow.
- Assumption: Users have access to at least one supported coding-agent workflow in their environment.
- Risk: Teams may skip clarification/planning steps under time pressure, reducing quality.
- Risk: Overly prescriptive prompts could reduce fit for diverse projects.
- Risk: If technical guidance is missing or weak, teams may confuse outcome guidance with implementation policy.
- Risk: Repository-local claims may be mistaken for externally verified delivery unless proof levels and authoritative systems remain explicit.
- Risk: A growing surface of copied helpers, prompts, and special cases could make upgrades and extensions less reliable than the problems they solve.

## Change Log

- 2026-02-13: Initial constitution created from repository context; defined mission, outcomes, principles, and governance boundaries.
- 2026-05-29: Updated outcomes for multi-agent support, QA/code review before completion, and post-completion retros.
- 2026-07-22: Reframed the product for trustworthy end-to-end delivery, proportionate assurance, clear operational state, immutable adoption foundations, and extension without core forks.
