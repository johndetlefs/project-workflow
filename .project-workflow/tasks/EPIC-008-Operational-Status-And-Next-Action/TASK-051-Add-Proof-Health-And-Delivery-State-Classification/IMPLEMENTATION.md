## User Story

As an owner, agent, or reviewer, I want health, proof layers, and delivery stages classified independently from repository evidence, so that a passing check or optimistic status cannot make unfinished or undelivered work look complete.

## Parent AC Coverage

- AC1, AC5, AC6, AC10

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

Turn inspected repository facts into truthful Doctor health, per-item proof layers, aggregate proof, and source-backed delivery states without mutation or cross-layer inference.

## Approach

- Extend the shared model with proof-layer and work-fact records.
- Reuse approval, readiness, QA, parent-evidence, structured-evidence, and Doctor helpers.
- Resolve later delivery only through read-only Git ancestry or validated local receipt content.
- Preserve partial classifications and failures as sourced facts for TASK-052 rather than selecting actions here.

## Phases

1. Add proof-layer/work-fact models and health classification.
2. Classify every work-item proof layer and aggregate progression.
3. Add focused delivery progression and receipt validation.
4. Prove separation, accepted-warning semantics, non-mutation, and parity.

## Acceptance Criteria

- [x] AC1: Every work-item kind exposes six ordered, sourced proof layers.
- [x] AC2: Independent proof variation and aggregate progression never inflate a missing or failing prerequisite.
- [x] AC3: Health matches Doctor pass/warning/fail, visible, accepted, legacy, and blocking evaluation.
- [x] AC4: Completion, integration, release, public publication, deployment, missing, and malformed receipt states remain distinct.
- [x] AC5: Later delivery never follows from tracker, branch/tag, cleanliness, tests, or URLs alone.
- [x] AC6: Accepted/failing/malformed sources remain explicit beside partial facts.
- [x] AC7: Classification and payload order are deterministic and non-mutating.
- [x] AC8: Focused/full validation, parity, backlog, and strict Doctor pass.

## Validation

- AC1, AC2: work-kind and independently varied proof-layer fixture matrices.
- AC3, AC6: direct equivalence assertions against Doctor evaluation including accepted history.
- AC4, AC5: disposable Git histories and local receipt/substitute fixtures.
- AC7: exact payload plus before/after repository and Git comparisons.
- AC8: focused pytest, compilation, source/template/local parity, backlog validation, strict Doctor, and full pytest with Homebrew UVX available.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add proof-layer and work-fact contracts | Extend immutable work items and payloads with ordered structured facts and six sourced proof layers. | AC1, AC2, AC6, AC7 | Construct exact task/Epic/child/Fix layer payloads and reject invalid records. | Done |
| 2 | Classify work-item proof | Reuse approval, readiness, task rows, QA, parent evidence, and structured evidence to derive separate layers and monotonic aggregate proof. | AC1, AC2, AC6, AC7 | Independently vary every layer and inspect exact aggregate progression. | Done |
| 3 | Classify Doctor health | Reuse Doctor evaluation and accepted fingerprints to report equivalent state, counts, codes, owners, and hidden accepted history. | AC3, AC6, AC7 | Compare status health directly with Doctor evaluation fixtures. | Done |
| 4 | Classify recorded delivery | Distinguish repository completion, Git integration, and valid local receipt stages while rejecting weaker substitutes. | AC4, AC5, AC6, AC7 | Exercise disposable histories and valid/missing/malformed/unreferenced receipt fixtures. | Done |
| 5 | Prove parity and safety | Run focused matrices, non-mutation checks, compilation, mirror comparisons, backlog, strict Doctor, and full suite. | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8 | Review exact focused/full outputs and before/after state. | Done |

## Parent AC Evidence

- AC1: Every task, Fix, Epic, and Epic-child fixture exposes the same six ordered proof-layer records with non-empty sources; the actual worktree classification returns separate active-work proof without inspection findings.
- AC5: The proof progression matrix independently stalls at approval, readiness, implementation, QA, parent acceptance, and structured evidence; repeated classification is idempotent and does not duplicate aggregate facts.
- AC6: Disposable Git and receipt fixtures distinguish non-terminal, repository-complete, integrated, released, published, and deployed states. A URL alone remains only released; missing and malformed receipts retain repository completion plus distinct findings.
- AC10: Direct Doctor-evaluation comparison preserves total, visible, accepted, current, legacy, and blocking counts; the actual strict worktree result is Pass with 69 accepted warnings retained and zero visible findings.
- No structured proof claim applies; `EVIDENCE.json` remains empty and repository fixtures/tests are the required evidence.

## QA & Code Review

- Review date: 2026-07-22
- Reviewed areas: immutable proof/fact contracts; exact payload ordering; task/Fix/Epic/child classification; inherited approval; readiness, implementation, QA, parent acceptance, and structured-evidence separation; aggregate proof monotonicity; Doctor evaluation parity; accepted and legacy warning semantics; read-only Git ancestry; delivery receipt validation; weak URL rejection; malformed-source preservation; idempotency; non-mutation; maintained payload parity; child-scope boundaries.
- Verdict: Pass.
- Evidence:
  - AC1: Four work-kind fixtures expose the exact six-layer order and non-empty sources; invalid/duplicate model records remain rejected by the shared immutable contracts.
  - AC2: Eight aggregate cases independently vary approval, readiness, implementation, QA, parent acceptance, and structured evidence. Each missing prerequisite stops progression at the exact earlier state; repeated classification returns the same objects with one aggregate fact.
  - AC3: Status health is compared directly with `_evaluate_doctor`; pass/warning/fail and total, visible, accepted, current, legacy, and blocking counts agree, including strict escalation.
  - AC4: Disposable fixtures distinguish `not-recorded`, `repository-complete`, `integrated`, `released`, `published`, and `deployed`; missing and malformed receipts stay at repository completion with different stable findings.
  - AC5: Git integration requires ancestry. Release publication/deployment require repository-local records containing verified status, target, source, observation time, and result; an external URL alone does not advance beyond release.
  - AC6: Accepted warnings remain counted but hidden from visible findings; visible Doctor issues keep stable codes and strict severity; missing/malformed receipt sources remain attached to partial delivery facts.
  - AC7: Exact payload tests, classifier idempotency, repository hashes, Git HEAD/status captures, and captured read-only commands prove stable order and non-mutation.
  - AC8: 40 focused operational-status tests and Python compilation passed; 198 full-suite tests passed with Homebrew UVX enabled; source/template/local Python payloads are byte-identical; diff hygiene passed.
  - Actual-worktree evidence: EPIC-008 and TASK-051 classify at their current proof stage, Proposed TASK-052 through TASK-054 stop at approved, aggregate proof is approved, strict health is Pass with 69 accepted and zero visible/blocking findings, and inspection has no contradiction findings.
- Findings: None.
- Deferred by approved scope: Primary/secondary action resolution, public human/JSON rendering, CLI wiring, documentation, and complete operator journeys remain owned by TASK-052 through TASK-054.

## Retro

- Retro date: 2026-07-22
- Reusable lessons: Keep proof as ordered independent gates rather than a confidence score; use the weakest active item for aggregate proof; reuse Doctor evaluation wholesale so accepted and strict semantics cannot drift; require Git ancestry for integration and explicit observed receipt fields for publication/deployment; keep partial repository completion visible when a later receipt is missing or malformed.
- Conventions or agent assets updated: The classifier and its focused regression matrix now encode these product rules. No broader guidance or managed-agent update was warranted because the approved Epic already owns the status-specific contract and later documentation work remains TASK-053/TASK-054 scope.
- Follow-up tasks: Continue EPIC-008 with approved TASK-052 deterministic next-action resolution. No separate backlog or Fix item was needed.
- Missed in-scope work: None.

## Notes

- Task: TASK-051
- Title: Add Proof, Health, And Delivery-State Classification
- Created: 2026-07-22
- Scope is unchanged from the approved parent decomposition; implementation authority is inherited from the EPIC-008 approval envelope.
