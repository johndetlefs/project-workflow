# Requirements

## Summary

- Task: TASK-054
- Title: Document And Prove End-To-End Operational Journeys
- Parent AC Coverage: AC2, AC3, AC4, AC5, AC6, AC7, AC9, AC10, AC11
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

- AC2: owner `Read model; inspection; journey children`; required evidence: Tracker/Epic fixture matrix proving complete discovery plus stable contradiction findings without a second status store.
- AC3: owner `Inspection; journey children`; required evidence: Current, stale, legacy, unsupported, and helper-limited fixture outputs matching Doctor and canonical upgrade direction.
- AC4: owner `Inspection; next-action; journey children`; required evidence: Lifecycle-state matrix proving plain-language meaning and the next legal gate for tasks, Fixes, Epics, and children.
- AC5: owner `Read model; classification; journey children`; required evidence: Independently varied proof-layer fixtures showing no cross-layer inflation and exact source provenance.
- AC6: owner `Read model; classification; journey children`; required evidence: Repository-complete, integrated, receipt-backed released, and unknown-delivery fixtures with distinct non-inferred conclusions.
- AC7: owner `Next-action; journey children`; required evidence: Published precedence table plus regression matrix proving responsibility, exact commands, stable tie-breaking, and blocker priority.
- AC9: owner `Inspection; CLI; journey children`; required evidence: Before/after repository hashes and Git-state captures across success, warning, malformed, and failure paths.
- AC10: owner `Classification; next-action; journey children`; required evidence: Accepted/current/strict finding fixtures proving historical noise remains inspectable without displacing a real blocker or action.
- AC11: owner `CLI; journey children`; required evidence: README and generated-agent guidance review, packaged/helper parity, focused/full tests, backlog validation, strict Doctor, and executed UVX packaging proof.

## Goal

Make `project status` understandable and independently believable by documenting its boundaries, exercising realistic disposable repository journeys, and refreshing Epic acceptance evidence for closeout.

## Non-Goals

- Adding new status policy or product scope unless a journey exposes a blocking defect.
- Claiming current hosted/registry/deployment state without a suitable recorded source.
- Publishing a new package release; this Epic delivers repository implementation and release readiness, not 0.2.1 publication.

## Users & Context

- Owners and agents need guidance on status versus Doctor, upgrade, lifecycle, QA, and service verification.
- Reviewers need realistic journey artifacts beyond unit fixtures.
- Maintainers need generated instructions and README examples aligned with the packaged/local CLI.

## Requirements (Outcome-Focused)

- Document status usage, formats, focus/strict options, source boundaries, and non-mutating behavior in README and generated agent instructions.
- Add durable journey coverage for initialized/active work, strict warning, malformed/uninitialized, stable action ordering, proof separation, delivery separation, and before/after safety.
- Exercise the checked-in local helper in a disposable initialized Git repository and inspect both human and JSON results.
- Refresh the Epic acceptance map/audit and run every closeout gate; record any residual limitation without overclaiming release or deployment.

## Acceptance Criteria (Verifiable)

- AC1: README and every generated agent instruction explain when to use status versus Doctor/upgrade/lifecycle/QA/service verification and show human, JSON, focus, and strict commands.
- AC2: A disposable initialized Git journey uses the checked-in helper, creates active work, captures human/JSON status, proves stable action/source semantics, and preserves repository/Git state across status calls.
- AC3: Automated journey coverage retains contradiction, compatibility, lifecycle, proof, delivery, ordering, strict/accepted-warning, and non-mutation evidence across parent AC2-AC10.
- AC4: Source/template/local parity, generation tests, strict Doctor, backlog validation, diff hygiene, full suite with Homebrew UVX, Epic audit, and closeout gates pass.
- AC5: Handoff states repository completion separately from merge, release, publication, deployment, and external adoption; unresolved later delivery remains explicit.

## Open Questions (Answer Needed)

- None. Documentation and journey scope is fixed by the parent contract and completed implementation.

## Decisions (Resolved)

- Keep the main README concise and use one status section near the working model plus command-boundary guidance near lifecycle/versioning material.
- Add status guidance to the generated managed block so all supported agent ecosystems receive the same contract on init/upgrade.
- Use disposable local evidence for the operator journey; do not label it public release or deployment proof.

## Validation Plan

- Review generated asset diffs and run generation/parity tests.
- Run one disposable initialized Git journey with before/after tree hash, HEAD, branch, and porcelain status.
- Run focused operational tests, full pytest with Homebrew UVX, backlog validation, strict Doctor, Epic acceptance audit, and closeout.
- No specialized proof recipe applies; repository-local command artifacts and exact journey assertions are the required evidence.
