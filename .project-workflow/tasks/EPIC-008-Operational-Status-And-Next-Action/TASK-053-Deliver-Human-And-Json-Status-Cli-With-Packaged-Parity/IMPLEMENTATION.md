## User Story

As an owner or agent returning to a repository, I want one `project status` command with readable and machine output, so that I can understand current truth and act next without reconstructing several sources.

## Parent AC Coverage

- AC1, AC8, AC9, AC11

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

## Acceptance Criteria

- [x] AC1: One snapshot builder composes every operational dimension and action once.
- [x] AC2: Human and JSON renderers agree and remain deterministic.
- [x] AC3: Human output is concise, action-first, sourced, and includes accepted-warning counts.
- [x] AC4: Focused, missing, malformed, strict, non-Git, and uninitialized paths fail safely.
- [x] AC5: Human/JSON/focused/warning paths are repository- and Git-read-only.
- [x] AC6: Parser, payload parity, focused/full tests, and workflow gates pass.

## Validation

- AC1, AC2, AC3: exact snapshot, JSON, and human projection fixtures.
- AC4, AC5: subprocess and before/after fixture matrices.
- AC6: help/parser, compilation, source/template/local parity, backlog, strict Doctor, diff hygiene, and full pytest with Homebrew UVX.

## Goal

Expose the completed operational model through one safe `project status` CLI interaction.

## Approach

- Compose inspection, classification, delivery, findings, and resolution into one immutable snapshot.
- Render JSON directly from the shared payload serializer and human text directly from the same snapshot.
- Register a narrow parser surface and keep every path read-only.
- Prove maintained-payload parity and command behavior through direct and subprocess fixtures.

## Phases

1. Build snapshot composition and focused filtering.
2. Add concise human and exact JSON renderers.
3. Register parser/command behavior and safe partial-state handling.
4. Prove non-mutation, parity, and repository-wide gates.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Compose operational snapshot | Combine collectors, classifiers, delivery, findings, blockers, and resolver without duplicating policy. | AC1, AC4 | Inspect exact full/focused snapshots. | Done |
| 2 | Render human and JSON output | Produce action-first human text and versioned JSON from one snapshot. | AC2, AC3 | Compare semantic fields and repeated output. | Done |
| 3 | Register safe status CLI | Add parser, strict/focus/format options, stable partial-state handling, and no mutations. | AC3, AC4, AC5 | Run subprocess success/warning/malformed/non-Git fixtures and compare before/after state. | Done |
| 4 | Prove maintained parity | Mirror the Python payload, test help and exact behavior, and run all workflow gates. | AC1, AC2, AC3, AC4, AC5, AC6 | Review compilation, byte comparisons, focused/full tests, backlog, Doctor, and diff hygiene. | Done |

## Parent AC Evidence

- AC1: `build_operational_status_snapshot` composes inspection, proof, health, per-item/aggregate delivery, findings, blockers, and resolver into one immutable record used by both formats.
- AC8: Repeated JSON subprocess output is byte-identical and equals `operational_status_payload` from the direct snapshot builder; human output contains the same primary code and dimensions.
- AC9: Before/after hashes prove uninitialized, initialized, focused, missing-focus, human, JSON, strict, and `--root` paths do not alter target or caller files; inspection uses only prior read-only Git queries.
- AC11: Parser/help exposes `status`, `--root`, `--id`, `--strict`, and `--format`; source/template/local Python payloads match and the checked-in shell launcher runs the local payload successfully.
- Actual-worktree evidence: Human output leads with TASK-053 implementation, reports current installation, dirty branch, strict-compatible Pass health with 69 accepted warnings, ready proof, unrecorded delivery, the selected active child, no findings, and exact source artifacts.
- No specialized proof recipe applies; `EVIDENCE.json` is empty and CLI/non-mutation fixtures are the required evidence.

## QA & Code Review

- Review date: 2026-07-22
- Reviewed areas: parser/help; root resolution; snapshot composition; focused filtering; proof/delivery aggregation; Doctor strict/accepted semantics; finding/blocker preservation; resolver reuse; human action-first ordering; JSON schema/order; source visibility; missing/no-active/uninitialized/non-Git behavior; subprocess stability; target/caller non-mutation; local shell launcher; source/template/local parity; scope boundaries.
- Verdict: Pass.
- Evidence:
  - AC1: Direct snapshot and subprocess JSON equality proves one composition path owns installation, Git, health, proof, delivery, work, findings, blockers, and primary/secondary actions.
  - AC2: Two unchanged JSON invocations are byte-identical and use schema version 1; human output includes the same primary action code and state dimensions from the shared snapshot.
  - AC3: Actual and fixture human reports start with `Next action`, responsibility, reason, command/request, then status, work, findings, secondary actions, and deduplicated sources; accepted-warning count remains visible without expanding 69 historical warnings.
  - AC4: Initialized/non-Git, uninitialized, active focus, missing focus, empty work, and strict-warning fixtures return stable reports with no traceback. Completing a draft fixture creates non-strict warning versus strict fail/blockers and changes the primary action only under strict evaluation.
  - AC5: File hashes before/after human, JSON, repeated, focused, missing-focus, strict, uninitialized, and cross-root calls remain equal; caller and target roots both remain unchanged.
  - AC6: Help exposes the complete narrow surface; local launcher successfully runs status JSON; 88 focused status tests and three-file compilation passed; 246 full-suite tests passed with Homebrew UVX enabled; Python payloads are byte-identical; diff hygiene passed.
  - Actual-worktree evidence: `project status --id TASK-053` reports current installation, dirty Git, Pass health with 69 accepted warnings, ready proof, unrecorded delivery, no findings, implementation as the primary action, and exact repository sources.
- Findings: None.
- Deferred by approved scope: README/managed-agent teaching, disposable operator journeys, acceptance audit, and Epic closeout remain TASK-054 scope; this task provides the command they will document and exercise.

## Retro

- Retro date: 2026-07-22
- Reusable lessons: Build the status snapshot once and keep renderers policy-free; action-first human output makes the command useful without hiding proof/source context; strictness belongs in Doctor evaluation before action resolution; focused selection must never fall through to unrelated work; subprocess equality and file hashes are stronger CLI evidence than direct-unit assertions alone.
- Conventions or agent assets updated: Added the canonical parser, snapshot builder, human renderer, JSON command, local payload parity, and six subprocess-focused CLI tests. Public README and managed-agent guidance intentionally remain TASK-054 deliverables so this child does not duplicate documentation ownership.
- Follow-up tasks: Continue EPIC-008 with approved TASK-054 end-to-end journeys, documentation, acceptance audit, and closeout. No separate backlog or Fix item was needed.
- Missed in-scope work: None.

## Notes

- Task: TASK-053
- Title: Deliver Human And JSON Status CLI With Packaged Parity
- Created: 2026-07-22
- Scope is unchanged from the approved parent decomposition; implementation authority is inherited from the EPIC-008 approval envelope.
