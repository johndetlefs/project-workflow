# Requirements

## Summary

- Task: TASK-052
- Title: Build Deterministic Next-Action Resolver
- Parent AC Coverage: AC4, AC7, AC10
- Last updated: 2026-07-22

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Child Charter

### Inherited Invariants

- `project status` is read-only in every success, warning, and failure path.
- Existing workflow artifacts remain the only lifecycle and evidence stores; status is a derived projection.
- Current workflow health, work lifecycle, proof state, and delivery state remain separate dimensions.
- Later delivery stages are never inferred from earlier stages.
- Every material conclusion and recommended action retains source provenance.
- One unchanged input state produces the same primary action and stable secondary ordering.
- A mechanical action names an exact supported command; an owner or external action names the required decision or evidence and is never mislabeled as agent-remediable.
- Safety and compatibility blockers outrank ordinary progress, but accepted historical noise does not hide the next meaningful current action.
- Malformed or contradictory state remains visible and cannot be collapsed into a clean summary.
- Status does not approve, accept, repair, mutate, transition, merge, publish, deploy, or run the action it recommends.
- Packaged CLI and generated local helper use the same operational model and remain behaviorally aligned.
- The first version is single-repository and repository-native; live platform verification and assurance policy remain explicit extension points for later Epics.

### Invalid Substitutes

- A passing Doctor result is not proof that work is implemented, reviewed, integrated, released, or deployed.
- A `Complete` tracker row is not proof that its branch was merged or that an artifact was released or deployed.
- Requirements approval, a completed implementation checklist, a QA paragraph, and a structured runtime claim are distinct proof layers and cannot substitute for one another.
- An accepted warning is not a repaired condition, and its suppression from normal Doctor output is not evidence that it disappeared.
- A clean worktree, current branch, tag name, URL, or prose statement is not by itself a verified integration, publication, deployment, or runtime claim.
- A local package version or manifest is not proof that the same version is currently public in a registry.
- A recorded external URL or receipt is not a fresh live verification unless the evidence explicitly records the target, source, observation, and result required for that claim.
- Agent inference is not a substitute for a missing source artifact; the status must report `unknown`, `not recorded`, or a contradiction.
- Human and JSON renderers may not implement separate status or next-action rules.

### Artifact Targets

- Shared operational-status projection, source records, state enums/codes, contradiction handling, and next-action resolver in `src/project_workflow/cli.py`
- Equivalent generated helper behavior in `src/project_workflow/templates/workflow.py` and checked-in local helper parity
- `project status` human renderer, optional focused work-item selection, and versioned JSON schema
- Table-driven lifecycle, proof, delivery, compatibility, malformed-state, ordering, and non-mutation fixtures under `tests/`
- README command guidance plus managed Codex, Cursor, Claude Code, and GitHub Copilot assets explaining status boundaries and next-action use
- EPIC-008 child requirements, implementation plans, evidence, QA, acceptance map/audit, and closeout artifacts

### Parent AC Proof Ownership

- AC4: owner `Inspection; next-action; journey children`; required evidence: Lifecycle-state matrix proving plain-language meaning and the next legal gate for tasks, Fixes, Epics, and children.
- AC7: owner `Next-action; journey children`; required evidence: Published precedence table plus regression matrix proving responsibility, exact commands, stable tie-breaking, and blocker priority.
- AC10: owner `Classification; next-action; journey children`; required evidence: Accepted/current/strict finding fixtures proving historical noise remains inspectable without displacing a real blocker or action.

## Goal

Resolve one deterministic, truthful primary next action plus ordered secondary actions from the operational inspection and classification model, without executing or inventing authority for any action.

## Non-Goals

- Adding the public `project status` parser or renderer; TASK-053 owns the command surface.
- Mutating tracker, document, Git, warning-acceptance, release, or deployment state.
- Repairing malformed workflow artifacts from the status path.
- Choosing product priority among equally ranked backlog outcomes beyond the repository's recorded priority and source order.
- Performing live service verification or authenticated owner decisions.
- Replacing existing workflow transition checks with resolver-specific lifecycle rules.

## Users & Context

- An agent returning to a repository needs the exact supported command it can safely run next.
- An owner needs a concrete decision request when the repository cannot authorize the next transition.
- A reviewer needs to see why one action outranked another and which sources justified both primary and secondary actions.
- Status already has typed installation, Git, health, proof, delivery, work-item, and finding records. The resolver should be a pure ordered projection over those records plus read-only backlog discovery.

## Requirements (Outcome-Focused)

- R1. Define one published precedence table, from highest to lowest: incompatible or unsafe repository state; blocking current findings; required owner decisions; missing workflow gates or proof; next legal lifecycle action for active work; delivery follow-up for completed work; backlog selection when no work is active; and an explicit no-action state.
- R2. Resolve candidates without mutation, then select one primary action by precedence, active-work source order, stable item ID, and stable action code. Return remaining candidates in the same order as secondary actions without duplicates.
- R3. Every action must have a stable `PW_STATUS_*` code, concise title, reason, source records, responsible party, and exactly one executable command or concrete request.
- R4. Mechanical commands must be existing supported project-workflow or Git commands with exact item IDs. Resolver output must never fabricate a command or bypass an existing gate.
- R5. Owner decisions and evidence requests must use `owner` or `external-authority`, never `agent`; accepted historical Doctor warnings must remain inspectable but must not become action candidates unless their underlying issue is visible/current and blocking.
- R6. Installation states that require upgrade, initialization, or a newer helper must produce exact canonical commands. Unsupported future or invalid state must produce a named owner/maintainer request rather than a speculative mutation.
- R7. Lifecycle candidates must preserve stored vocabulary and point to the next legal existing gate for tasks, Fixes, Epics, and Epic children. Blocked items require the recorded blocker to be resolved; Review requires QA; Complete work must not be re-opened or re-completed.
- R8. Proof-layer gaps must name the first unmet ordered layer and source. A failed gate outranks a merely pending later gate; structured evidence requests must not be represented as ordinary checklist completion.
- R9. When there is no active work, select the highest recorded non-terminal backlog item using priority then file order and recommend promotion/selection as an owner request. When no candidate exists, return an explicit no-action owner request rather than an empty or invented command.
- R10. Focused resolution for one work item must use the same precedence and candidate rules as repository-wide resolution, only filtering the eligible work scope.

## Acceptance Criteria (Verifiable)

- AC1: A documented precedence constant and table-driven matrix prove compatibility/safety blockers outrank current findings, owner decisions, missing gates, lifecycle progress, delivery follow-up, backlog selection, and no-action fallback.
- AC2: Every supported task, Fix, Epic, and Epic-child lifecycle produces the exact next valid command or concrete request with stable code, responsibility, reason, and sources; terminal work is not assigned an invalid lifecycle transition.
- AC3: Multiple equally ranked candidates resolve identically across repeated runs using source order, item ID, and code; the complete ordered remainder is returned as duplicate-free secondary actions.
- AC4: Proof-layer fixtures independently vary approval, readiness, implementation, QA, parent acceptance, and structured evidence; the resolver selects the earliest blocking layer without allowing later passing evidence to hide it.
- AC5: Accepted hidden warnings never displace a current action, while visible strict/current blockers do; owner and service-authority requests are never labeled as agent commands.
- AC6: Current, upgradeable, legacy, invalid, unsupported-future, not-initialized, and helper-limited installation fixtures produce exact supported commands or explicit requests without mutation.
- AC7: No-active-work fixtures select backlog intent deterministically by recorded priority and order, and an empty/non-actionable repository returns an explicit no-action result.
- AC8: Focused and repository-wide resolution share one implementation; exact payload, before/after repository and Git state, mirror parity, strict Doctor, backlog validation, and the full suite pass.

## Open Questions (Answer Needed)

- None. The parent envelope already fixes precedence categories, responsibility boundaries, supported-command requirement, stable ordering, and read-only behavior. Implementation details may be resolved without changing that authority.

## Decisions (Resolved)

- Use candidate generation followed by one stable sort and primary/secondary projection; do not encode precedence separately in renderers.
- Treat visible error findings as blocking. Non-strict warnings remain findings unless a specific candidate rule identifies a required current gate.
- Use work discovery order before item ID so the resolver respects repository source order while remaining deterministic for duplicate-rank candidates.
- Recommend workflow commands only when they already exist. Represent owner approval, blocker resolution, missing evidence, integration, publication, and deployment as concrete requests when status cannot safely perform them.
- Backlog fallback is an owner selection request, not automatic promotion.

## Validation Plan

- AC1, AC3: Assert the exact precedence table and permute candidate inputs across repeated calls.
- AC2, AC4: Run a complete lifecycle/action matrix plus independent proof-layer gap fixtures for every work kind.
- AC5, AC6: Combine accepted/current/strict Doctor evaluation with every installation compatibility state and assert responsibility plus command/request exclusivity.
- AC7: Exercise priority, file-order, terminal, malformed, and empty backlog fixtures.
- AC8: Compare focused/full resolution outputs, hash repository files, capture Git identity/status, compare all maintained Python payloads, and run focused/full workflow gates with Homebrew UVX available.
- No specialized proof recipe applies to this repository-native deterministic resolver; local structured fixtures and exact regression assertions are the acceptance evidence.
