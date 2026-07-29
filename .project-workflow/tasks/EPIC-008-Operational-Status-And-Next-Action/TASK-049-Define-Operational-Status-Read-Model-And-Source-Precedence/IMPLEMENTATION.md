## User Story

As a maintainer extending project-workflow status reporting, I want one immutable operational read model with explicit source ownership, so that collectors and renderers can explain repository state without inventing truth or conflating health, progress, proof, and delivery.

## Parent AC Coverage

- AC1, AC2, AC5, AC6, AC8

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
- AC2: owner `Read model; inspection; journey children`; required evidence: Tracker/Epic fixture matrix proving complete discovery plus stable contradiction findings without a second status store.
- AC5: owner `Read model; classification; journey children`; required evidence: Independently varied proof-layer fixtures showing no cross-layer inflation and exact source provenance.
- AC6: owner `Read model; classification; journey children`; required evidence: Repository-complete, integrated, receipt-backed released, and unknown-delivery fixtures with distinct non-inferred conclusions.
- AC8: owner `Read model; CLI children`; required evidence: Golden human/JSON outputs from one model with schema version, stable fields/codes, and semantic equivalence.

## Goal

Provide the validated internal contract that all later operational-status collection, action selection, human rendering, and JSON rendering must share.

## Approach

- Add stable vocabulary and immutable status dataclasses beside the existing Doctor and compatibility models.
- Encode source authority per status dimension instead of using one unsafe global precedence.
- Add one deterministic JSON-ready serializer as the sole renderer boundary.
- Prove separation, provenance, fail-closed validation, and stable ordering with focused tests before adding repository inspection or a public command.

## Phases

1. Define source, state, work-item, finding, action, and snapshot contracts.
2. Add fail-closed model validation and deterministic payload serialization.
3. Prove the contract with focused tests and repository-wide validation.

## Acceptance Criteria

- [x] AC1: The immutable snapshot contains every approved operational dimension and emits an explicit schema version.
- [x] AC2: Source records and dimension-specific precedence cover all approved repository truth families without becoming a state store.
- [x] AC3: Multiple active work items and contradiction findings preserve identity, lifecycle, meaning, and provenance.
- [x] AC4: Proof and delivery remain independently constructible and never infer later delivery stages.
- [x] AC5: Findings preserve stable codes, severity, message, and all relevant sources alongside readable facts.
- [x] AC6: Actions require valid responsibility and exactly one command or request, and are inert data.
- [x] AC7: Exact payload, invalid-model, parity, compilation, Doctor, and full-suite validation pass.

## Validation

- AC1, AC3, AC4, AC5, AC6: exact model-construction and payload tests.
- AC2: immutable precedence-map assertions covering each approved dimension/source family.
- AC7: focused pytest, Python compilation, packaged/template/local-helper parity, strict Doctor, and full pytest with Homebrew UVX available.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define operational vocabulary and immutable models | Add stable source kinds, dimensions, state values, responsibility values, source precedence, and immutable source/work/finding/action/snapshot records. | AC1, AC2, AC3, AC4, AC5, AC6 | Import the models and inspect a complete snapshot without invoking repository reads or mutation. | Done |
| 2 | Add fail-closed validation and deterministic payload | Validate every controlled value and action shape, then serialize one ordered schema-versioned payload for all future renderers. | AC1, AC3, AC4, AC5, AC6 | Compare a complete payload exactly and exercise invalid constructors. | Done |
| 3 | Prove separation, provenance, and parity | Add focused tests for source precedence, independent proof/delivery state, contradictions, action responsibility, stable ordering, and packaged/generated/local-launcher behavior. | AC2, AC3, AC4, AC5, AC6, AC7 | Run the focused tests, compilation, parity checks, strict Doctor, and full suite. | Done |

## Parent AC Evidence

- AC1: `OperationalStatusSnapshot` and its exact payload test contain installation, Git, health, proof, delivery, active work, findings, blockers, and actions behind schema version 1.
- AC2: `OPERATIONAL_STATUS_SOURCE_PRECEDENCE` assigns authority per dimension across compatibility/manifest, trackers, requirements, implementation, acceptance, evidence, Doctor, Git, receipts, and backlog; tuple immutability and full source-kind coverage are tested.
- AC5: `OperationalStatusValue` keeps proof separate from lifecycle and delivery, while `OperationalStatusFinding` preserves every contradiction source; invalid values and nested record shapes fail closed.
- AC6: Proof and delivery use independent controlled vocabularies; the focused test proves repository validation leaves delivery `not-recorded` rather than inferring integration or release.
- AC8: `operational_status_payload` is the one deterministic JSON-ready renderer boundary; the complete nested payload is asserted exactly and preserves prioritized tuple order.
- No recipe-triggered claim applies to this internal contract child; `EVIDENCE.json` correctly contains no claims.

## QA & Code Review

- Review date: 2026-07-22
- Reviewed areas: immutable model boundaries; controlled vocabularies; dimension-specific source authority; constructor validation; source and tuple ordering; proof/delivery separation; action responsibility and command/request exclusivity; deterministic payload shape; packaged/generated/local Python parity; task scope and proof-recipe applicability.
- Verdict: Pass.
- Evidence:
  - AC1: Exact payload coverage proves all required snapshot dimensions and schema version 1.
  - AC2: Source-precedence assertions cover every declared source kind and keep authority dimension-specific.
  - AC3: Multiple-source work-item and contradiction tests preserve identity, lifecycle, meaning, and ordered provenance.
  - AC4: Independent proof/delivery construction proves repository validation does not infer integration or later delivery.
  - AC5: Finding validation and exact payload assertions preserve stable code, severity, message, and sources.
  - AC6: Negative constructor tests reject invalid responsibility, empty actions, and command/request ambiguity.
  - AC7: 11 focused tests and Python compilation passed; packaged CLI, generated template, and local Python payload are byte-identical; full suite passed with 169 tests and the Homebrew UVX packaging path enabled; strict Doctor, backlog validation, readiness, and diff hygiene passed.
- Findings: None.
- Deferred by approved scope: Repository collection, action prioritization, public rendering, and complete operator journeys remain owned by TASK-050 through TASK-054; no later-child behavior is claimed here.

## Retro

- Retro date: 2026-07-22
- Reusable lessons: Status source authority must be dimension-specific; a global source ranking would let Git or Doctor overclaim approval, proof, or delivery. Proof-recipe keywords in a negated explanation can still trigger the current lexical detector, so task documents should state the applicable proof boundary directly rather than enumerate recipes that do not apply.
- Conventions or agent assets updated: Added a domain-focused operational-status test module while retaining packaged/generated Python parity and the launcher-based local helper contract.
- Follow-up tasks: Continue EPIC-008 in approved dependency order with TASK-050 repository inspection; no separate follow-up was created.
- Missed in-scope work: None.

## Notes

- Task: TASK-049
- Title: Define Operational Status Read Model And Source Precedence
- Created: 2026-07-22
- Scope is unchanged from the approved parent decomposition; implementation authority is inherited from the EPIC-008 approval envelope.
