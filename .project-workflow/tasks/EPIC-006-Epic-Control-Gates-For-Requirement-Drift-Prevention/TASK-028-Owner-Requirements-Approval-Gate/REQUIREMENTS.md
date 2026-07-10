# Requirements

## Summary

- Task: TASK-028
- Title: Approved Scope Authority Gate
- Parent AC Coverage: AC1, AC11, AC12, AC13, AC16, AC18
- Last updated: 2026-07-09
- Status: Approved for implementation under EPIC-006 authority envelope

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for implementation: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-09
- Approval note / source: Approved under EPIC-006 authority envelope after owner clarified that matching child work should proceed without separate per-child approval: "it shouldn't be... approve absolutely everything... there should be some intelligence here".

## Goal

Add a small, enforceable approved-scope authority gate so agents cannot advance new tasks or epics from unreviewed, stale, or drifted requirements, while still allowing ordinary child work to proceed inside an already approved epic/decomposition boundary without repeated owner approval.

This child should make drift detection an active lifecycle precondition at the right boundary. Approval establishes authority; mechanical gates decide whether the current work is still inside that authority.

## Non-Goals

- Do not implement the full epic contract model; that belongs to TASK-029.
- Do not implement proof recipes, visual calibration, evidence ledgers, or invalid-substitute logic; those belong to TASK-030 and TASK-032.
- Do not implement full decomposition-plan authority checks beyond checking that epic child work cannot bypass owner-approved parent requirements; that belongs to TASK-037.
- Do not implement legacy adoption commands beyond preserving the existing manual approval block path for current artifacts; full adoption belongs to TASK-034.
- Do not require approval gates for pure read-only discovery work.
- Do not require repeated owner approval for unchanged work inside an approved authority envelope.
- Do not use generic approval prompts where a specific drift reason, evidence gap, stale artifact, or missing amendment can be reported instead.

## Users & Context

- Project owners need an explicit stop before implementation starts outside an approved scope boundary.
- Project owners need approval prompts to stay rare and meaningful so they do not approve blindly from fatigue.
- Agents need a machine-checkable way to know whether requirements and ACs are approved and whether current work is inside the approved authority envelope.
- Existing projects may already have manual approval blocks, so the first implementation must support both command-written and manual approval metadata.
- Workflow maintainers need doctor failures that catch invalid current states even when a file was edited by hand.

## Requirements (Outcome-Focused)

- Add parseable owner approval metadata for task and epic `REQUIREMENTS.md` files.
- Add supported CLI command paths to record owner approval envelopes for task and epic requirements/ACs, including approval source text and approved artifact identity.
- Preserve manual approval block support for current and legacy artifacts, but reject placeholders, agent-only approval notes, missing approval source, and incomplete approval metadata.
- Compute and store an approval freshness identity for the approved requirements artifact. The identity must be stable enough for doctor/status gates to detect material edits after approval.
- Block supported task lifecycle commands from moving unapproved, stale-approved, or outside-envelope tasks into implementation or completion states.
- Block supported epic lifecycle commands from decomposition, child approval, child scaffolding, In Progress, Review, or Complete when the epic requirements/AC approval envelope is missing, stale, or not applicable to the requested movement.
- Allow child tasks generated from an approved epic/decomposition envelope to proceed without separate owner approval, provided they do not change parent AC coverage, source-of-truth interpretation, artifact identity, proof obligations, or approved scope.
- Fail gates with specific drift/evidence reasons rather than generic approval-needed prompts when the work is unchanged but evidence is missing or invalid.
- Require fresh owner input only for material scope boundaries: initial approval, stale material edits, deviations, changed source-of-truth interpretation, changed artifact identity, changed proof obligations, new child work outside the decomposition plan, or explicit deferrals.
- Preserve a bounded discovery exception for read-only inspection and explicitly allowed findings-only artifacts, without allowing product source changes under that exception.
- Add doctor/validate checks that fail invalid current states caused by manual tracker or docs edits, not only invalid CLI transitions.
- Update generated task/epic templates and README/agent guidance so new work asks for owner approval at the scope boundary and proceeds autonomously inside that boundary.
- Add regression tests for missing approval, stale approval after requirements edits, placeholder approval, agent-only approval, manual invalid status edits, and discovery exception boundaries.

## Acceptance Criteria (Verifiable)

- AC1: Task and epic requirements templates include a parseable owner approval envelope block with reviewed flags, approval state, approver/source, approval date, approved artifact identity, and scope covered by the approval.
- AC2: CLI approval commands can record approval envelopes for standalone tasks and epics with non-placeholder owner approval source text.
- AC3: Approval validation rejects missing approval, placeholder approval, agent-only approval, missing source, missing artifact identity, stale approval after material requirements/AC edits, and work outside the approved envelope.
- AC4: `task ready`, `task status`, `epic ready`, `epic decompose`, `epic approve`, `epic scaffold-child`, `epic lifecycle`, `epic status`, and `epic closeout` enforce the relevant approval envelope before gated movement while allowing ordinary matching child work inside the envelope.
- AC5: Doctor/validate fails current invalid states even if they were created by manual edits rather than CLI commands.
- AC6: The bounded discovery exception allows read-only inspection and explicitly allowed findings-only artifacts while still blocking product source changes and gated lifecycle movement.
- AC7: Templates, CLI README, and generated agent guidance explain the approval envelope without adding proof-recipe or visual-fidelity concepts to ordinary tasks.
- AC8: Automated tests cover the parent drift failures assigned to this child: work starts without owner approval, approval becomes stale after requirements edits, outside-envelope work proceeds, and manual tracker/doc edits bypass CLI commands.
- AC9: Gated commands and doctor checks do not require fresh owner approval for unchanged work inside the approved authority envelope; they either pass or fail with a specific drift/evidence/staleness reason.

## Open Questions (Answer Needed)

- None blocking. Command names may be adjusted during implementation if the CLI structure suggests a clearer naming pattern, but the supported command path must be documented and tested.

## Decisions (Resolved)

- Approval must be machine-checkable, freshness-bound, and scoped to an authority envelope.
- The goal is to remove drift, not transfer verification labor to the owner.
- Approval prompts must be reserved for owner decisions; all other failures should be actionable drift/evidence findings for the agent.
- Manual approval blocks remain supported, but command-written approval is the preferred path for new work.
- Approval freshness and envelope membership belong in this child because stale or outside-scope work is a direct owner-approval failure, not a proof-recipe failure.
- State-based doctor enforcement belongs in this child for the basic approval gate; later children can extend the same pattern for contracts, evidence, decomposition plans, and proof recipes.

## Validation Plan

- Run targeted unit tests for approval block parsing, approval command writes, artifact identity/freshness, authority envelope membership, lifecycle blockers, bounded approval prompts, discovery exception handling, and doctor state checks.
- Run existing task, epic, audit, closeout, and doctor tests to check backwards compatibility.
- Run `./.project-workflow/cli/workflow doctor`.
