# Requirements

## Summary

- Task: TASK-050
- Title: Add Installation, Git, And Active-Work Inspection
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC9
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
- AC3: owner `Inspection; journey children`; required evidence: Current, stale, legacy, unsupported, and helper-limited fixture outputs matching Doctor and canonical upgrade direction.
- AC4: owner `Inspection; next-action; journey children`; required evidence: Lifecycle-state matrix proving plain-language meaning and the next legal gate for tasks, Fixes, Epics, and children.
- AC9: owner `Inspection; CLI; journey children`; required evidence: Before/after repository hashes and Git-state captures across success, warning, malformed, and failure paths.

## Goal

Populate the approved operational-status foundation with truthful, read-only installation identity, Git state, and active-work facts, preserving source provenance and structural contradictions for later classification and rendering.

## Non-Goals

- Classifying requirements approval, QA, parent acceptance coverage, structured proof, or delivery receipts; TASK-051 owns those dimensions.
- Selecting or ordering primary and secondary actions; TASK-052 owns next-action resolution.
- Adding the public command, human output, or final JSON CLI; TASK-053 owns presentation.
- Treating Git containment as proof of release, publication, or deployment.
- Mutating Git, trackers, manifests, task documents, or generated assets.
- Coordinating multiple repository roots or querying remote platforms.

## Users & Context

- A repository owner or agent needs exact installed package/asset/schema facts before deciding whether ordinary work can continue or canonical upgrade is required.
- A returning contributor needs branch, commit, upstream, detached/dirty state, and active workflow items without running several Git and tracker commands.
- Later EPIC-008 children need a deterministic collector that reports malformed, duplicate, orphaned, or contradictory sources instead of failing early or silently selecting one.
- Existing reusable primitives include `_repository_compatibility`, manifest parsing, global/Epic table parsers, and `_run_git`; this child must compose them without changing their command ownership.

## Requirements (Outcome-Focused)

- Extend operational values with ordered, typed facts so installation and Git identity remain structured in the shared payload rather than being embedded only in prose summaries.
- Add a read-only repository inspection result containing installation state, Git state, active work, and inspection findings.
- Reuse `_repository_compatibility` as the installation authority and report its state/reason plus every available manifest version and migration fact, current helper package/asset/schema capability, and canonical upgrade direction where applicable.
- Preserve `current`, `upgradeable`, `legacy-unversioned`, `unsupported-future`, `invalid`, and `not-initialized` compatibility meaning. Expose enough helper capability facts for the public command to distinguish when the inspecting helper cannot establish current contract state.
- Inspect Git without mutation and report repository top level, branch or detached state, HEAD commit, upstream when configured, and clean/dirty worktree state. A missing Git executable, non-repository, unborn HEAD, or missing upstream must produce an explicit available/unknown fact or finding rather than a traceback.
- Read global tracker rows in file order and include every non-terminal standalone task, Fix, and Epic. Preserve configured non-default task prefixes as task work.
- For every non-terminal global Epic, read its Epic tracker in file order and include every non-terminal child row with its owning Epic source. Proposed and Approved children remain visible as planned work; Complete children are terminal.
- Attach plain operational meaning to every supported global and Epic-child lifecycle value without renaming the stored lifecycle.
- Detect and report malformed tracker schemas/rows, missing active-Epic trackers, missing docs paths for scaffolded child statuses, duplicate workflow IDs, child IDs owned by multiple Epics, and completed Epics with non-terminal children. Proposed/Approved rows may legitimately lack docs before scaffold. Retain every safely readable fact alongside findings.
- Use stable inspection finding codes, severity, source paths, and deterministic ordering.
- Perform no repository or Git mutation in current, legacy, unsupported, malformed, detached, dirty, and failure paths.
- Keep packaged source, generated Python template, and local Python payload aligned; leave the shell launcher intact.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC1 and AC3: installation fixtures for current, upgradeable, legacy-unversioned, unsupported-future, invalid, and not-initialized repositories return the exact compatibility reason, available manifest versions/migrations, current helper capability, source provenance, and canonical upgrade direction without mutation.
- AC2: Covers parent AC1 and AC9: clean, dirty, detached, no-upstream, non-repository, and unavailable-Git fixtures return structured top-level/branch/HEAD/upstream/worktree facts or stable findings and never run a mutating Git command.
- AC3: Covers parent AC1 and AC2: global tracker plus active-Epic tracker fixtures return all non-terminal tasks, Fixes, Epics, and Epic children in deterministic source order with ID, title, kind, stored lifecycle, operational meaning, and owning sources; terminal rows are excluded.
- AC4: Covers parent AC4: table-driven tests cover every supported global and Epic-child lifecycle value and prove its stored value and plain operational meaning remain distinct and stable.
- AC5: Covers parent AC2: malformed schemas/rows, missing trackers or required scaffolded-child docs paths, duplicate IDs, multi-Epic child ownership, and completed-Epic/non-terminal-child contradictions produce stable ordered findings while retaining other readable work items; unscaffolded Proposed/Approved rows are not mislabeled malformed.
- AC6: Covers parent AC9: before/after repository bytes and Git-state captures are identical for successful, warning, malformed, and failure inspections.
- AC7: Covers parent AC1, AC2, AC3, AC4, and AC9: focused inspection tests, compilation, packaged/generated/local payload parity, backlog validation, strict Doctor, and the full suite pass with Homebrew UVX exercised.

## Open Questions (Answer Needed)

- None. The collector reports local repository and Git facts only; proof, delivery, action selection, remote verification, and rendering remain in their approved children.

## Decisions (Resolved)

- Represent structured identity as ordered immutable fact records attached to each operational value.
- Reuse compatibility state and reason verbatim; do not create a competing installation classifier.
- Treat global tracker order, then active Epic order and child row order, as deterministic discovery order.
- Treat `Complete` and `N/A` as terminal global statuses and `Complete` as the terminal Epic-child status.
- Include Proposed and Approved Epic children because they are authorised/planned work that affects the next operational action even though implementation has not begun.
- Keep Git inspection local and read-only. Remote containment, release, and deployment claims remain unknown until later sources prove them.
- Preserve partial results when one source is malformed; findings explain the gap.
- Keep `EVIDENCE.json` empty because repository fixtures and tests are the required proof for this inspection child.

## Validation Plan

- Build disposable repositories for every compatibility state and Git state; compare exact structured facts and findings.
- Build global/Epic tracker matrices covering every lifecycle, custom task prefixes, multiple active Epics, Proposed/Approved children, and terminal exclusion.
- Inject malformed headers/rows, missing trackers/docs, duplicate IDs, multi-owner children, and completed-parent contradictions; assert partial facts survive with stable findings.
- Capture every subprocess invocation in unit tests and assert only the approved read-only Git commands are used.
- Hash file trees and capture `git status --porcelain`, branch, and HEAD before and after inspection.
- Run focused tests, Python compilation, source/template/local payload comparisons, backlog validation, strict Doctor, and `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`.
