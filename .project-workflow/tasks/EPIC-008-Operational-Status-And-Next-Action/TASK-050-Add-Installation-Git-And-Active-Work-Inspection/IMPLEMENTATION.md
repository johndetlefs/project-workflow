## User Story

As a repository owner or agent returning to project-workflow, I want one read-only inspection of installed contract identity, Git state, and active work, so that later status output can orient me using proven local facts rather than guesses.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC9

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
- AC3: owner `Inspection; journey children`; required evidence: Current, stale, legacy, unsupported, and helper-limited fixture outputs matching Doctor and canonical upgrade direction.
- AC4: owner `Inspection; next-action; journey children`; required evidence: Lifecycle-state matrix proving plain-language meaning and the next legal gate for tasks, Fixes, Epics, and children.
- AC9: owner `Inspection; CLI; journey children`; required evidence: Before/after repository hashes and Git-state captures across success, warning, malformed, and failure paths.

## Goal

Provide a deterministic read-only collector for installed contract identity, local Git state, and active workflow items that retains partial facts and provenance when repository sources are missing or contradictory.

## Approach

- Extend operational values with immutable ordered facts and define one repository-inspection result.
- Reuse the current compatibility classifier and a strict allowlist of read-only Git queries.
- Traverse global then active-Epic tracker rows in source order, mapping stored lifecycle values to plain operational meaning.
- Convert structural gaps into stable findings while retaining every safe fact already collected.
- Prove zero mutation with before/after repository and Git assertions.

## Phases

1. Extend the shared model and installation/Git collectors.
2. Add active-work traversal, lifecycle meaning, and contradiction handling.
3. Run focused safety/ordering coverage and repository-wide validation.

## Acceptance Criteria

- [x] AC1: Every compatibility state produces structured installation identity, reason, helper capability, provenance, and upgrade direction without mutation.
- [x] AC2: Every supported Git state produces structured local facts or stable findings using read-only commands only.
- [x] AC3: Global and active-Epic trackers yield every non-terminal work item in deterministic order with kind, lifecycle, meaning, and ownership sources.
- [x] AC4: Every supported lifecycle value has stable plain operational meaning without altering stored vocabulary.
- [x] AC5: Malformed, missing, duplicate, orphaned, and contradictory sources preserve partial facts and emit stable ordered findings.
- [x] AC6: File-tree and Git-state comparisons prove inspection is non-mutating across success and failure paths.
- [x] AC7: Focused/full validation, parity, backlog, and strict Doctor gates pass.

## Validation

- AC1: compatibility fixture matrix and exact structured fact assertions.
- AC2: Git-state matrix plus captured command allowlist.
- AC3, AC4, AC5: global/Epic lifecycle and structural-contradiction fixtures.
- AC6: before/after repository hashes and Git identity/status assertions.
- AC7: focused pytest, compilation, packaged/generated/local payload parity, backlog validation, strict Doctor, and full pytest with Homebrew UVX available.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add structured operational facts and inspection result | Extend the shared immutable model with ordered typed facts and a read-only inspection result for installation, Git, work, and findings. | AC1, AC2, AC3, AC5 | Construct and inspect one complete repository-inspection result and exact payload fragments. | Done |
| 2 | Inspect installation and Git state | Reuse compatibility authority and run only read-only Git queries, returning exact identity/capability facts and safe unavailable states. | AC1, AC2, AC6 | Run compatibility and Git fixture matrices and review captured commands plus before/after state. | Done |
| 3 | Discover active work and lifecycle meaning | Read global and active-Epic trackers in deterministic order, classify kinds, retain stored lifecycle, and attach plain operational meaning. | AC3, AC4, AC6 | Run the complete lifecycle matrix and inspect ordered active-work results. | Done |
| 4 | Preserve malformed and contradictory state | Emit stable findings for malformed, missing, duplicate, multi-owner, and completed-parent contradictions without discarding readable facts. | AC3, AC5, AC6 | Exercise malformed fixtures and verify partial work plus ordered findings and zero mutation. | Done |
| 5 | Prove parity and repository safety | Add focused regression coverage and run compilation, parity, backlog, strict Doctor, and full-suite validation. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Review focused/full test output, exact mirror comparisons, and strict workflow validation. | Done |

## Parent AC Evidence

- AC1: The actual worktree inspection reports current installation, dirty Git, EPIC-008 plus TASK-050 through TASK-054 in source order, and no inspection findings; exact model/payload tests preserve structured facts.
- AC2: Global/current and legacy Epic tracker fixtures discover every non-terminal task, namespaced task, Fix, Epic, and child while terminal rows remain excluded; malformed rows preserve partial work with stable findings.
- AC3: Current, schema-behind, legacy-unversioned, future-schema, invalid-JSON, and uninitialized fixtures retain compatibility reason, helper capability, manifest identity, migrations, provenance, and applicable canonical upgrade direction.
- AC4: Global and Epic-child meaning maps are asserted against every supported stored lifecycle value; Proposed and Approved children remain visible without false missing-doc findings.
- AC9: Captured Git commands are limited to read-only queries, and before/after repository hashes, HEAD, branch/status, and fixture bytes remain identical across successful and unavailable paths.
- No structured proof claim applies; `EVIDENCE.json` remains empty and repository fixtures/tests are the required evidence.

## QA & Code Review

- Review date: 2026-07-22
- Reviewed areas: compatibility-source reuse; fact typing and serialization; helper capability and upgrade direction; Git command allowlist and partial failures; branch/detached/dirty semantics; global and legacy/current Epic tracker traversal; terminal filtering; custom task prefixes; lifecycle meaning; duplicate/multi-owner provenance; missing/contradictory source handling; actual-worktree behavior; non-mutation; packaged/generated/local parity; child scope and proof boundary.
- Verdict: Pass.
- Evidence:
  - AC1: Six compatibility-state fixtures assert exact reason, manifest/helper facts, migrations, applicable upgrade command, provenance, and unchanged repository bytes.
  - AC2: Clean, dirty, detached, no-upstream, non-repository, and missing-Git paths return structured facts/findings; captured calls contain only five read-only Git queries and preserve HEAD/status.
  - AC3: Global plus current/legacy Epic trackers return non-terminal tasks, namespaced tasks, Fixes, Epics, and Proposed/Approved/In Progress children in deterministic order while excluding terminal rows.
  - AC4: Meaning maps exactly cover every global and Epic-child lifecycle constant without rewriting stored values.
  - AC5: Malformed rows, duplicate global IDs, shared child ownership, missing Epic trackers, missing scaffolded-child docs, and closed-parent contradictions emit stable ordered findings while preserving readable work.
  - AC6: Fixture tree hashes and Git HEAD/status comparisons remain identical; actual-worktree inspection performed no mutation.
  - AC7: 20 focused tests and Python compilation passed; full suite passed with 178 tests and Homebrew UVX enabled; source/template/local Python payloads match; readiness, backlog, strict Doctor, and diff hygiene passed.
- Findings: None.
- Deferred by approved scope: Approval/QA/proof/delivery classification, next-action selection, public rendering, and complete operator journeys remain owned by TASK-051 through TASK-054.

## Retro

- Retro date: 2026-07-22
- Reusable lessons: Operational inspection should preserve partial truth rather than fail the entire snapshot when one tracker or Git fact is unavailable. Tracker discovery order is a useful deterministic tie-breaker, and Proposed/Approved Epic children must remain visible without being treated as malformed for lacking pre-scaffold docs.
- Conventions or agent assets updated: Added domain-focused local-inspection fixtures covering compatibility, Git, global/current/legacy Epic trackers, lifecycle meaning, contradictions, and non-mutation; no broader guidance update was needed.
- Follow-up tasks: Continue EPIC-008 with TASK-051 proof, health, and delivery-state classification; no separate follow-up was created.
- Missed in-scope work: None.

## Notes

- Task: TASK-050
- Title: Add Installation, Git, And Active-Work Inspection
- Created: 2026-07-22
- Scope is unchanged from the approved parent decomposition; implementation authority is inherited from the EPIC-008 approval envelope.
