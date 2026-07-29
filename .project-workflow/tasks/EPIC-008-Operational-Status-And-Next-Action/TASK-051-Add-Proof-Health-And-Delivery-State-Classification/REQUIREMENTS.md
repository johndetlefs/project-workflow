# Requirements

## Summary

- Task: TASK-051
- Title: Add Proof, Health, And Delivery-State Classification
- Parent AC Coverage: AC1, AC5, AC6, AC10
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

- AC1: owner `Operational read model; inspection; CLI children`; required evidence: Realistic initialized-repository output showing every required status dimension, source, and primary action in one invocation.
- AC5: owner `Read model; classification; journey children`; required evidence: Independently varied proof-layer fixtures showing no cross-layer inflation and exact source provenance.
- AC6: owner `Read model; classification; journey children`; required evidence: Repository-complete, integrated, receipt-backed released, and unknown-delivery fixtures with distinct non-inferred conclusions.
- AC10: owner `Classification; next-action; journey children`; required evidence: Accepted/current/strict finding fixtures proving historical noise remains inspectable without displacing a real blocker or action.

## Goal

Classify workflow health, per-work-item proof layers, aggregate repository proof, and recorded delivery state without allowing one passing layer or an unverified claim to inflate another.

## Non-Goals

- Selecting the primary next action or precedence among blockers; TASK-052 owns action resolution.
- Adding the public command or rendering; TASK-053 owns the CLI surface.
- Performing live calls to Git hosts, CI systems, registries, deployment platforms, or identity providers.
- Introducing configurable assurance profiles or authenticated authority levels; BL-019 owns that product outcome.
- Treating accepted warnings as repaired, tests as owner approval, tracker completion as integration, or a recorded URL as fresh external verification.
- Rewriting approval, QA, evidence, tracker, Git, or receipt state.

## Users & Context

- Owners and agents need to know whether requirements, readiness, implementation, QA, parent acceptance, and structured proof are separately missing, pending, passing, or failing.
- Reviewers need Doctor health represented using the same finding evaluation and accepted-warning semantics as `project doctor`.
- Delivery claims need an explicit progression: repository-complete, Git-proven integrated, release-recorded, publicly recorded, or deployment-recorded. A later state requires a source appropriate to that exact claim.
- Existing helpers already own approval identity, readiness, QA verdict, parent AC evidence, structured evidence validation, Doctor evaluation, and Git queries. This child should compose them rather than create parallel rules.

## Requirements (Outcome-Focused)

- Add immutable proof-layer records with stable layer names, controlled states, summary, and source provenance; attach ordered proof layers and structured work facts to operational work items.
- Preserve six independent work-item layers: requirements approval, readiness, implementation, QA/review, parent acceptance, and structured evidence.
- For Epic children, inherit approval authority from the approved parent envelope and decomposition; do not misclassify placeholder child approval fields as missing approval.
- Treat Proposed/Approved unscaffolded children as approved planned work with readiness/implementation/QA pending or not recorded, not malformed.
- Reuse existing readiness, task-table, QA verdict, parent AC evidence, and structured evidence helpers for scaffolded tasks and children. Use Epic contract/readiness/audit sources for parent Epics and the Fix authority packet for Fixes.
- Derive one aggregate proof value from explicit layers using a documented monotonic progression: unknown/not-recorded, declared, approved, ready, implementation-recorded, repository-validated, or recorded-evidence. Any failing required layer must remain visible and prevent a stronger aggregate claim.
- Reuse `run_doctor`, accepted fingerprints, and `_evaluate_doctor` for health. Report pass/warning/fail, current/legacy/accepted/blocking counts, and visible findings with their original stable codes and remediation metadata.
- Accepted historical findings must remain counted and reviewable but must not become visible current blockers solely because status was requested.
- Add focused delivery classification for an inspected work item. Non-terminal work is `not-recorded`; terminal repository work is `repository-complete`; Git containment may advance it to `integrated`; an explicit validated local receipt may advance it to `released`, `published`, or `deployed` according to fields in that receipt.
- Resolve delivery receipts only from a work item's structured evidence references or explicit repository-local receipt path. A URL or prose-only statement is not a receipt.
- Never infer publication or deployment from a tag, branch, tracker state, clean worktree, test result, or successful Git query.
- Return `unknown` when sources exist but cannot establish the claim and `not-recorded` when the workflow records no source for it.
- Preserve deterministic ordering and perform no repository, Git, warning-acceptance, evidence, or lifecycle mutation.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC1 and AC5: active standalone task, Fix, Epic, scaffolded child, and unscaffolded child fixtures expose ordered approval, readiness, implementation, QA, parent-acceptance, and structured-evidence layers with stable states, summaries, and sources.
- AC2: Covers parent AC5: independently varying each proof layer changes only that layer and the justified aggregate progression; a passing test/QA/evidence layer never repairs missing approval, readiness, implementation, or parent acceptance.
- AC3: Covers parent AC1 and AC10: Doctor pass, visible-warning, strict-blocking, accepted-warning, and legacy-warning fixtures produce equivalent health state/counts/codes to Doctor evaluation while accepted history remains counted but hidden from visible blockers.
- AC4: Covers parent AC6: non-terminal, repository-complete, Git-integrated, release-receipted, public-receipted, deployment-receipted, missing-receipt, malformed-receipt, and prose/URL-only fixtures produce distinct delivery states and exact source provenance.
- AC5: Covers parent AC6: no fixture advances beyond repository-complete without Git containment or a valid local receipt for that exact later stage; a tag, branch name, clean worktree, test pass, or URL alone is rejected as a substitute.
- AC6: Covers parent AC5 and AC10: accepted findings, failing required proof layers, malformed evidence, and malformed receipts remain explicit without hiding readable health/proof/delivery facts.
- AC7: Covers parent AC1, AC5, AC6, and AC10: classification and payload ordering are deterministic and all inspection paths are non-mutating.
- AC8: Focused classification tests, compilation, packaged/generated/local Python parity, backlog validation, strict Doctor, and the full suite pass with Homebrew UVX exercised.

## Open Questions (Answer Needed)

- None. The first version reports only local repository, Git, and receipt evidence; live authority and policy profiles remain later work.

## Decisions (Resolved)

- Use six explicit proof layers rather than one confidence score.
- Treat parent Epic approval plus decomposition as the approval source for unchanged children.
- Keep aggregate proof monotonic but fail closed: the strongest reported state is the strongest consecutively justified layer, not the maximum isolated passing layer.
- Reuse Doctor's existing evaluation and fingerprints exactly.
- Treat `Complete` as repository completion only. Integration needs a successful read-only Git ancestry check against the recorded target branch.
- Treat a valid local receipt as recorded evidence, not a fresh live check. Receipt content determines whether the recorded state is release, public publication, or deployment.
- Prefer `unknown` or `not-recorded` to inference.
- Keep `EVIDENCE.json` empty for TASK-051 itself because fixture matrices and local validation are the proof required for this classifier.

## Validation Plan

- Build work-item fixtures for every kind and lifecycle, independently varying approval, readiness, task rows, QA verdict, parent evidence, and structured evidence.
- Assert exact layer and aggregate payloads for valid, pending, missing, contradictory, and failing combinations.
- Compare health state, counts, visible codes, accepted counts, and blocking counts directly with `_evaluate_doctor` results.
- Build disposable Git histories proving unintegrated and integrated completed branches without mutation.
- Build valid release/public/deployment receipt fixtures plus missing, malformed, unreferenced, URL-only, and prose-only substitutes.
- Hash repositories and capture Git state before/after classification.
- Run focused tests, Python compilation, source/template/local payload comparisons, backlog validation, strict Doctor, and `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`.
