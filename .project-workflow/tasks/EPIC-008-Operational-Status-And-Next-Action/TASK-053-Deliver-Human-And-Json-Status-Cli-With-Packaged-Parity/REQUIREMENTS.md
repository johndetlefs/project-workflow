# Requirements

## Summary

- Task: TASK-053
- Title: Deliver Human And JSON Status CLI With Packaged Parity
- Parent AC Coverage: AC1, AC8, AC9, AC11
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
- AC8: owner `Read model; CLI children`; required evidence: Golden human/JSON outputs from one model with schema version, stable fields/codes, and semantic equivalence.
- AC9: owner `Inspection; CLI; journey children`; required evidence: Before/after repository hashes and Git-state captures across success, warning, malformed, and failure paths.
- AC11: owner `CLI; journey children`; required evidence: README and generated-agent guidance review, packaged/helper parity, focused/full tests, backlog validation, strict Doctor, and executed UVX packaging proof.

## Goal

Deliver the canonical read-only `project status` command by composing the existing operational collectors, classifiers, and resolver into one snapshot with concise human output and a versioned JSON projection.

## Non-Goals

- Changing classifier or resolver policy except where composition exposes a correctness defect.
- Live service verification, mutation, automatic remediation, or action execution.
- Full operator-journey documentation and release proof; TASK-054 owns those outcomes.
- Persisting a status cache or second lifecycle store.

## Users & Context

- Owners and agents need one command that states installation, Git, health, active work, proof, delivery, blockers, sources, and next action.
- Automation needs stable JSON generated from the identical snapshot used by human output.
- Maintainers need packaged, template, and checked-in helper parity and safe behavior on partial or malformed repositories.

## Requirements (Outcome-Focused)

- R1. Register `project status` with `--format human|json`, optional `--id`, and `--strict` Doctor evaluation.
- R2. Build one immutable snapshot by composing repository inspection, proof classification, Doctor health, per-item delivery classification, aggregate dimensions, findings/blockers, and action resolution exactly once.
- R3. Human output must lead with the primary next action, then concise installation/Git/health/proof/delivery/work/findings/source context. It must name accepted-warning counts without expanding hidden history by default.
- R4. JSON must use `OPERATIONAL_STATUS_SCHEMA_VERSION`, serialize the same snapshot, preserve stable field/source/action order, and contain no renderer-specific conclusions.
- R5. `--id` must focus work and actions consistently; a missing/non-active ID must return a stable sourced action rather than silently falling back to unrelated work.
- R6. Status must retain partial facts and stable findings when inspection/classification inputs are malformed or unavailable and must never mutate repository or Git state.
- R7. Per-item delivery and aggregate delivery must remain separate from work lifecycle. Non-terminal active work remains `not-recorded`; later stages require the TASK-051 sources.
- R8. Source, template, and local Python payloads must be byte-identical; the shell launcher remains a launcher, not a copied Python payload.

## Acceptance Criteria (Verifiable)

- AC1: Human and JSON invocations from one initialized fixture agree on every snapshot dimension, selected work, finding/blocker, and primary/secondary action.
- AC2: `--format json` emits the exact versioned schema and deterministic ordering; repeated unchanged invocations are identical.
- AC3: Human output leads with one executable command or concrete request and includes installation, Git, health, proof, delivery, work, findings, sources, and accepted-warning count in concise sections.
- AC4: Focused active, missing-ID, no-active-work, malformed-state, strict-warning, non-Git, and uninitialized fixtures return stable truthful results without traceback or mutation.
- AC5: Repository/file hashes plus Git HEAD/status prove status is read-only for human, JSON, focused, warning, and failure-shaped paths.
- AC6: CLI parser/help, source/template/local parity, compilation, focused tests, backlog validation, strict Doctor, diff hygiene, and full pytest with Homebrew UVX pass.

## Open Questions (Answer Needed)

- None. The parent and completed children already define model, source, classification, precedence, responsibility, and action policy.

## Decisions (Resolved)

- Human and JSON output are renderers over one snapshot builder.
- Default human mode is concise; JSON is selected explicitly with `--format json`.
- Strict mode changes Doctor warning blocking semantics but does not change accepted-warning suppression.
- Focus applies after discovery/classification and before aggregate work/action rendering; missing focus remains explicit.
- Status returns a report rather than mutating or auto-running the selected action.

## Validation Plan

- AC1, AC2: exact snapshot and renderer-equivalence fixtures plus repeat-run JSON comparisons.
- AC3: human golden assertions for section order, action content, counts, and source paths.
- AC4, AC5: subprocess fixtures with before/after tree hashes and Git identity/status.
- AC6: parser/help tests, payload comparisons, compilation, workflow gates, and full suite with Homebrew UVX.
- No specialized proof recipe applies; command/output contract fixtures are the required evidence.
