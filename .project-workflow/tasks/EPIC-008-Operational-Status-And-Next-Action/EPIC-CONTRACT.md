# Epic Contract

## Summary

- Epic: EPIC-008
- Title: Operational Status And Next Action
- Last updated: 2026-07-22

## Sources of Truth

- `.project-workflow/tasks/EPIC-008-Operational-Status-And-Next-Action/REQUIREMENTS.md`
- `.project-workflow/CONSTITUTION.md` and `.project-workflow/BACKLOG.md`
- `.project-workflow/manifest.json` and repository compatibility evaluation for installed package, asset, and schema identity
- `.project-workflow/config.json` for namespaces, ID generation, and accepted-warning records
- `.project-workflow/TRACKER.md` for global execution lifecycle state
- Active Epic `TRACKER.md`, `DECOMPOSITION.md`, `ACCEPTANCE-MAP.md`, `ACCEPTANCE-AUDIT.md`, `DEFERRALS.md`, and `AMENDMENTS.md` files for Epic-owned state and parent coverage
- Work-item `REQUIREMENTS.md`, `IMPLEMENTATION.md`, `FIX.md`, `EVIDENCE.json`, and referenced evidence artifacts for approval, readiness, implementation, QA, and proof claims
- Existing Doctor finding/evaluation logic in `src/project_workflow/cli.py` and its generated-helper mirror
- Read-only Git branch, HEAD, upstream, merge-containment, and worktree state for repository integration facts Git can actually establish
- Explicit repository-recorded release, publication, deployment, or handoff receipts for later delivery claims; absence of a receipt is an unknown/not-recorded state

## Invalid Substitutes

- A passing Doctor result is not proof that work is implemented, reviewed, integrated, released, or deployed.
- A `Complete` tracker row is not proof that its branch was merged or that an artifact was released or deployed.
- Requirements approval, a completed implementation checklist, a QA paragraph, and a structured runtime claim are distinct proof layers and cannot substitute for one another.
- An accepted warning is not a repaired condition, and its suppression from normal Doctor output is not evidence that it disappeared.
- A clean worktree, current branch, tag name, URL, or prose statement is not by itself a verified integration, publication, deployment, or runtime claim.
- A local package version or manifest is not proof that the same version is currently public in a registry.
- A recorded external URL or receipt is not a fresh live verification unless the evidence explicitly records the target, source, observation, and result required for that claim.
- Agent inference is not a substitute for a missing source artifact; the status must report `unknown`, `not recorded`, or a contradiction.
- Human and JSON renderers may not implement separate status or next-action rules.

## Invariants

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

## Artifact Targets

- Shared operational-status projection, source records, state enums/codes, contradiction handling, and next-action resolver in `src/project_workflow/cli.py`
- Equivalent generated helper behavior in `src/project_workflow/templates/workflow.py` and checked-in local helper parity
- `project status` human renderer, optional focused work-item selection, and versioned JSON schema
- Table-driven lifecycle, proof, delivery, compatibility, malformed-state, ordering, and non-mutation fixtures under `tests/`
- README command guidance plus managed Codex, Cursor, Claude Code, and GitHub Copilot assets explaining status boundaries and next-action use
- EPIC-008 child requirements, implementation plans, evidence, QA, acceptance map/audit, and closeout artifacts

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-049, TASK-050, TASK-051, TASK-053 | Realistic initialized-repository output showing every required status dimension, source, and primary action in one invocation. |
| AC2 | TASK-049, TASK-050, TASK-054 | Tracker/Epic fixture matrix proving complete discovery plus stable contradiction findings without a second status store. |
| AC3 | TASK-050, TASK-054 | Current, stale, legacy, unsupported, and helper-limited fixture outputs matching Doctor and canonical upgrade direction. |
| AC4 | TASK-050, TASK-052, TASK-054 | Lifecycle-state matrix proving plain-language meaning and the next legal gate for tasks, Fixes, Epics, and children. |
| AC5 | TASK-049, TASK-051, TASK-054 | Independently varied proof-layer fixtures showing no cross-layer inflation and exact source provenance. |
| AC6 | TASK-049, TASK-051, TASK-054 | Repository-complete, integrated, receipt-backed released, and unknown-delivery fixtures with distinct non-inferred conclusions. |
| AC7 | TASK-052, TASK-054 | Published precedence table plus regression matrix proving responsibility, exact commands, stable tie-breaking, and blocker priority. |
| AC8 | TASK-049, TASK-053 | Golden human/JSON outputs from one model with schema version, stable fields/codes, and semantic equivalence. |
| AC9 | TASK-050, TASK-053, TASK-054 | Before/after repository hashes and Git-state captures across success, warning, malformed, and failure paths. |
| AC10 | TASK-051, TASK-052, TASK-054 | Accepted/current/strict finding fixtures proving historical noise remains inspectable without displacing a real blocker or action. |
| AC11 | TASK-053, TASK-054 | README and generated-agent guidance review, packaged/helper parity, focused/full tests, backlog validation, strict Doctor, and executed UVX packaging proof. |
