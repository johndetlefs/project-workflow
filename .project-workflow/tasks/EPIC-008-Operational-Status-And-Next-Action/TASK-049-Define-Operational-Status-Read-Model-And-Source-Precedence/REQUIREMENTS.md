# Requirements

## Summary

- Task: TASK-049
- Title: Define Operational Status Read Model And Source Precedence
- Parent AC Coverage: AC1, AC2, AC5, AC6, AC8
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
- AC2: owner `Read model; inspection; journey children`; required evidence: Tracker/Epic fixture matrix proving complete discovery plus stable contradiction findings without a second status store.
- AC5: owner `Read model; classification; journey children`; required evidence: Independently varied proof-layer fixtures showing no cross-layer inflation and exact source provenance.
- AC6: owner `Read model; classification; journey children`; required evidence: Repository-complete, integrated, receipt-backed released, and unknown-delivery fixtures with distinct non-inferred conclusions.
- AC8: owner `Read model; CLI children`; required evidence: Golden human/JSON outputs from one model with schema version, stable fields/codes, and semantic equivalence.

## Goal

Define one immutable, versioned operational-status model and dimension-specific source-precedence contract that later EPIC-008 children can populate, prioritize, and render without creating competing truth or collapsing health, lifecycle, proof, and delivery into one status.

## Non-Goals

- Inspecting the manifest, Git repository, trackers, work-item documents, evidence artifacts, or receipts; TASK-050 and TASK-051 own collection and classification.
- Selecting the primary next action; TASK-052 owns precedence execution and tie-breaking.
- Adding the public `project status` parser, human renderer, or final JSON CLI; TASK-053 owns the command surface.
- Documenting or proving complete end-to-end operator journeys; TASK-054 owns that proof.
- Adding live external verification, assurance profiles, extension adapters, or multi-repository behavior.

## Users & Context

- Later status collectors need a shared contract so manifest, Doctor, tracker, evidence, Git, and receipt data cannot silently overwrite one another.
- Renderers need one canonical payload model so human and JSON output cannot diverge in meaning.
- Maintainers need stable state values, finding codes, responsibility values, and source provenance that can be fixture-tested before the public command exists.
- The existing CLI already uses immutable dataclasses for Doctor, compatibility, upgrade, and Smoke Bomb models; the status foundation should follow that architecture without coupling itself to rendering.

## Requirements (Outcome-Focused)

- Define a schema-versioned immutable snapshot containing distinct installation, Git, health, proof, and delivery dimensions plus active work, findings/blockers, primary action, and secondary actions.
- Define typed source records with stable source kinds, repository-relative artifact identity where applicable, and optional detail sufficient to explain material conclusions.
- Publish dimension-specific authoritative source precedence. A higher-ranked source may resolve conflict within its dimension but may not substitute across dimensions.
- Preserve work-item ID, title, kind, lifecycle value, operational meaning, and source provenance without interpreting lifecycle completion as integration or release.
- Define explicit proof and delivery values that support `unknown` and `not-recorded` states and do not imply later stages from earlier ones.
- Define stable finding records for malformed, duplicate, orphaned, contradictory, or unavailable-source state without discarding the facts that remain readable.
- Define action records with a stable code, responsible party (`agent`, `owner`, or `external-authority`), reason, sources, and exactly one of an executable command or a concrete request.
- Validate model invariants at construction so invalid state, source kinds, severities, responsibility, or action shapes fail closed.
- Serialize the model deterministically to a versioned JSON-ready payload. Preserve tuple order for already-prioritized items and use stable field names for future human and JSON renderers.
- Keep these primitives independent of file reads, Git subprocesses, CLI parsing, rendering, and mutation.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC1 and AC8: an immutable `OperationalStatusSnapshot` represents installation, Git, health, proof, delivery, active work, findings, blockers, primary action, and secondary actions and serializes with an explicit schema version.
- AC2: Covers parent AC1 and AC2: typed source records and a dimension-specific precedence contract cover manifest/compatibility, global and Epic trackers, requirements/implementation, acceptance/evidence, Git, Doctor, and explicit delivery receipts without creating a new state store.
- AC3: Covers parent AC2: work-item records preserve ID, title, kind, lifecycle, operational meaning, and sources; the model can represent multiple active items and contradictory-source findings without silently selecting one.
- AC4: Covers parent AC5 and AC6: proof and delivery are separate states, both support `unknown` and `not-recorded`, and constructing repository-complete work does not infer integrated, released, published, or deployed state.
- AC5: Covers parent AC2 and AC5: findings retain stable code, severity, message, and all relevant sources so malformed or contradictory inputs can coexist with discoverable facts.
- AC6: Covers parent AC1: action records require a valid responsible party and exactly one command or concrete request, retaining reason and source provenance without executing anything.
- AC7: Covers parent AC8: focused tests prove invariant rejection and exact deterministic payloads; source/template/local-helper parity, compilation, strict Doctor, and the full suite remain green.

## Open Questions (Answer Needed)

- None. This child defines the approved shared contract and leaves collection, prioritization, and presentation to their named child tasks.

## Decisions (Resolved)

- Use immutable dataclasses and tuple collections, matching existing CLI model conventions.
- Use a schema-versioned JSON-ready dictionary as the renderer boundary rather than letting each renderer inspect repository artifacts independently.
- Use dimension-specific source precedence, not one global ranking: Git can own integration facts but cannot overrule requirements approval, and Doctor can own health findings but cannot prove delivery.
- Keep `unknown` distinct from `not-recorded`: unknown means available sources cannot establish the answer; not-recorded means the workflow has no source claiming the state.
- Model action responsibility as `agent`, `owner`, or `external-authority` and require exactly one of `command` or `request`.
- Add no structured proof claim to `EVIDENCE.json`; this internal contract task is fully proven by repository artifacts and tests.

## Validation Plan

- Construct a complete snapshot and compare its JSON-ready payload with an exact expected dictionary.
- Independently construct proof and delivery states to show no automatic escalation between dimensions.
- Exercise every invalid enum/value and invalid action command/request combination and assert fail-closed errors.
- Represent multiple work items plus a contradiction finding and prove all facts/sources survive serialization in stable order.
- Assert the source-precedence contract contains every approved source family in the correct dimension and cannot be mutated.
- Run focused operational-model tests, Python compilation, packaged/template/local-helper parity, `./.project-workflow/cli/workflow doctor --strict`, and the full test suite with Homebrew UVX available.
