# Constitution

## Mission

- Make repository-native, agent-assisted delivery a practical and trustworthy way for developers and teams to turn intent into shipped outcomes, while keeping the workflow open, low-overhead, and useful in real repositories.

## Target Users

- Primary users:
  - Individual developers and small teams using Cursor, OpenAI Codex, GitHub Copilot, or a mix of coding agents.
- Secondary users:
  - Engineering leads and collaborators who need visibility into scope, status, and delivery confidence through repository-native artifacts.
  - Independent adopters and contributors who choose to use, evaluate, improve, or adapt the open project.
  - Larger teams or organizations when their demonstrated delivery needs can be met without making hypothetical enterprise scale the default design target.

## Core Outcomes

- Every feature starts with a clearly stated user/business outcome before implementation begins.
- Teams maintain one unambiguous, auditable path from idea → requirements → plan → implementation → validated completion → integration or release receipt.
- Ambiguities are surfaced and resolved deliberately before coding proceeds, reducing rework and conflicting assumptions.
- Delivery status is transparent via a lightweight tracker that reflects real progress and validation state.
- Quality and maintainability are protected by an explicit QA/code review gate before completion.
- Completed tasks feed reusable lessons back into conventions and agent guidance so future work stays internally consistent.
- The workflow remains easy to adopt: repository-native, low-overhead, and compatible with existing git-based collaboration.
- The next meaningful action and the actual delivery state remain obvious to both people and agents.
- Proof remains proportionate to consequence, with stronger assurance added when real users and risks demonstrate the need.
- The public project remains understandable and usable without maintainer-specific context, private knowledge, or access to a particular organization.
- New capabilities are pulled by repeated real use, observed friction, or credible external demand rather than built in anticipation of hypothetical scale.

## Product Principles

- Enabler first: prioritize changes that improve delivery in active repositories or enable a decisive test of whether the workflow transfers to independent users.
- Outcome-first: define success in user/business terms before discussing implementation.
- Proportionate rigor: resolve material unknowns before execution while keeping ceremony proportional to risk and value.
- Repository-native truth: keep artifacts close to code so decisions are reviewable and versioned.
- Truth over artifact presence: distinguish declared, self-attested, independently verified, and externally authoritative evidence.
- Useful by default: make status, blockers, and the next action obvious without requiring workflow expertise.
- Incremental progress: favor small, verifiable steps with explicit validation.
- Human-in-the-loop: agents assist and accelerate, but users retain decision authority.
- Open and adoptable: preserve broad public access and a clear independent-use path without confusing availability with validated adoption.
- Evidence-pulled evolution: require repeated dogfooding friction, independent use, direct requests, or another credible outcome signal before investing in scale, governance, ecosystems, or integrations.
- Integrate rather than replace: use established delivery systems as authoritative sources when demonstrated use requires that integration.
- Coherent core: keep the default workflow simple and stable; add extension boundaries only when repeated real integration needs justify them.

## Non-Goals

- Replacing issue trackers, project management platforms, or sprint planning systems.
- Replacing git hosts, CI systems, package registries, deployment platforms, or organizational identity providers.
- Enforcing a single engineering stack, architecture, or coding style.
- Restricting usefulness to one maintainer, team, organization, or private operating context.
- Building enterprise governance, extension platforms, ecosystems, or multi-repository orchestration in anticipation of hypothetical demand.
- Creating a heavyweight governance process that slows feature delivery.
- Requiring enterprise ceremony for solo developers, prototypes, or low-risk changes.
- Maximizing the number of documents, prompts, commands, integrations, or public-adoption signals without a demonstrated user outcome.
- Producing deeply technical architecture standards in this document.

## Success Signals

- New work consistently has an outcome, an accountable approval boundary, and delivery evidence linked by task ID.
- Teams report fewer mid-implementation scope reversals caused by unclear requirements.
- Clarification and planning happen before implementation in the majority of completed tasks.
- Tracker status changes reflect real lifecycle movement (e.g., To Do → In Progress → Testing → Review → Complete).
- Completed tasks regularly produce useful retro notes or explicit "no durable updates needed" records.
- Active repositories continue receiving enough value to justify the workflow's setup and maintenance cost.
- Users can identify the true delivery state and next action in one interaction, including whether work is merely complete in-repo or has actually been integrated, released, or deployed.
- Independent users can install, understand, and apply the workflow without relying on maintainer intervention or undocumented operating knowledge.
- External value is demonstrated through verified outcomes, voluntary repeat use, substantive issues, requests, or contributions rather than stars, clone traffic, or generated artifacts alone.
- Safe upgrades and immutable releases keep continued use lower-risk than improvised local process.
- New capabilities trace back to repeated observed friction, independent evidence, or explicit user demand.
- Real repositories demonstrate reduced rework, faster handoff, and more reliable agent execution rather than adoption being measured by generated artifacts alone.

## Decision Filters

- Does this change improve outcome clarity for users and teams?
- Does it preserve traceability from requirement to implementation?
- Does it reduce ambiguity or hidden assumptions before coding?
- Does it keep workflow overhead low relative to value delivered?
- Does it maintain flexibility across project types without becoming vague?
- Does it improve an actual user outcome, unblock delivery, or materially reduce risk beyond what the current workflow already provides?
- Is the need demonstrated by active repository use, independent evidence, or a direct request rather than a plausible future scenario?
- Is there an adequate existing workaround that makes broader product investment premature?
- Does it preserve public accessibility without assuming broad adoption or enterprise scale?
- Is the proposed assurance level proportionate to the consequence of being wrong?
- Does it keep the core coherent and simple, introducing extension boundaries only when real integration pressure requires them?

## Assumptions & Risks

- Assumption: Teams are willing to maintain Markdown artifacts as part of normal development flow.
- Assumption: Users have access to at least one supported coding-agent workflow in their environment.
- Assumption: Continued maintainer and team use is sufficient reason to preserve the project even if broader product transferability remains unproven.
- Risk: Teams may skip clarification/planning steps under time pressure, reducing quality.
- Risk: Overly prescriptive prompts could reduce fit for diverse projects.
- Risk: If technical guidance is missing or weak, teams may confuse outcome guidance with implementation policy.
- Risk: Repository-local claims may be mistaken for externally verified delivery unless proof levels and authoritative systems remain explicit.
- Risk: Maintainer effectiveness and repeated dogfooding may be mistaken for evidence that independent users receive the same benefit.
- Risk: Public availability, downloads, stars, or clone traffic may be mistaken for meaningful adoption or realised value.
- Risk: Hypothetical scale work may displace higher-value outcomes in the projects this workflow exists to enable.
- Risk: A growing surface of copied helpers, prompts, and special cases could make upgrades and extensions less reliable than the problems they solve.

## Change Log

- 2026-02-13: Initial constitution created from repository context; defined mission, outcomes, principles, and governance boundaries.
- 2026-05-29: Updated outcomes for multi-agent support, QA/code review before completion, and post-completion retros.
- 2026-07-22: Reframed the product for trustworthy end-to-end delivery, proportionate assurance, clear operational state, immutable adoption foundations, and extension without core forks.
- 2026-07-25: Reframed Project Workflow as an open delivery enabler whose broader product, enterprise, ecosystem, and scale investment must be pulled by demonstrated use and independent evidence.
