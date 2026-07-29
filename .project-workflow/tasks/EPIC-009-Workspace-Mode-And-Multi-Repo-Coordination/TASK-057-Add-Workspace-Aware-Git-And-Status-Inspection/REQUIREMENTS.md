# Requirements

## Summary

- Task: TASK-057
- Title: Add Workspace-Aware Git And Status Inspection
- Parent AC Coverage: AC6, AC7, AC8, AC10
- Last updated: 2026-07-29

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

- Exactly one registered repository owns live Project Workflow state for a declared workspace.
- Registered repository paths remain inside the workspace, resolve safely, and identify distinct Git roots.
- Parent-owned non-repository folders remain owned by the authority repository and are not invented as repositories.
- Workspace inspection, Doctor, and status remain read-only across success, warning, malformed, and failure paths.
- No command introduced by this Epic creates, switches, commits, pushes, merges, releases, deploys, or otherwise mutates Git across registered repositories.
- Work-item repository scope is explicit, registered, and consistent before readiness.
- Workflow authority, implementation ownership, live Git state, recorded validation, integration, and later delivery remain separate dimensions.
- Missing or contradictory repository facts remain visible as missing, unknown, not recorded, or blocked; they are never guessed.
- Evidence stays attributed to the repository that produced it.
- Single-repository installations remain compatible and low-overhead when no workspace declaration exists.
- Parent-root invocation is the first-version operating contract; transparent discovery from child repositories is not implied.
- Packaged CLI, generated helpers, templates, prompts, skills, upgrade behavior, and documentation remain aligned.
- The real JohnDetlefs repositories remain read-only unless the owner separately authorizes a specific mutation lifecycle.

### Invalid Substitutes

- `AGENTS.md` or guidance prose is not a first-class repository registry and cannot substitute for config validation.
- A path that exists is not proof that it is a registered, safe, distinct Git root.
- A parent repository's clean/dirty or branch state is not the state of a nested independent repository.
- A task mentioning repository names in free prose is not valid repository scope unless the names resolve through the declared registry and required structure.
- A child `.project-workflow/` tracker is not a valid substitute for parent authority; it is competing live state.
- A validation command written in a document is not evidence that it ran or passed.
- One repository's tests, branch, pull request, merge, release, or deployment evidence cannot prove another repository's state.
- Repository implementation completion is not proof of pull request, merge, release, publication, or deployment.
- Fixture tests do not prove that the real JohnDetlefs workspace has the observed topology, and read-only real-workspace inspection does not prove mutation, upgrade, delivery, or adoption.
- Automatic Git actions or arbitrary validation execution are not acceptable substitutes for explicit authority and recorded evidence.
- A separate workspace tracker, database, or status file is not an acceptable substitute for the parent repository's existing workflow state.

### Artifact Targets

- Workspace registry and authority models, config parsing, validation, and stable findings in `src/project_workflow/cli.py`.
- Backward-compatible config template and repository-schema/upgrade handling.
- Doctor checks for registry safety, distinct Git roots, authority ownership, and competing child workflow state.
- Consistent repository-scope and repository-evidence structures in task, Fix, and Epic-child templates plus readiness/lifecycle validation.
- Workspace-aware operational projection, repository-focused selection, human output, and versioned JSON output built on the existing `project status` model.
- Table-driven workspace, Git-state, evidence-attribution, non-mutation, and compatibility tests under `tests/`.
- Disposable three-repository manual journey evidence and bounded read-only JohnDetlefs topology/status evidence.
- README and managed Codex, Cursor, Claude Code, and GitHub Copilot guidance describing the workspace contract and authority boundaries.
- EPIC-009 decomposition, child artifacts, structured evidence where triggered, acceptance map/audit, QA, retro, and closeout records.

### Parent AC Proof Ownership

- AC6: owner `TASK-057`; required evidence: Three-Git-root human/JSON status output with repository-scoped Git facts.
- AC7: owner `TASK-057`; required evidence: Independently varied dirty, detached, missing, unavailable, and wrong-branch child fixtures plus non-mutation captures.
- AC8: owner `TASK-057`; required evidence: Golden human/JSON outputs proving one model, focused selectors, deterministic ordering, provenance, and compatibility.
- AC10: owner `TASK-057, TASK-058`; required evidence: Before/after filesystem hashes and Git captures across success, warning, malformed, and failure paths.

## Goal

Make one read-only status interaction reveal the authoritative workspace and the actual Git state of repositories relevant to active or selected work.

## Non-Goals

- Do not mutate Git or execute recommended actions.
- Do not add live Git-host, CI, registry, or deployment APIs.
- Do not collapse repository validation or delivery evidence into Git state.

## Users & Context

The current status model inspects one root Git repository. In the JohnDetlefs topology that can report the parent while omitting `next` and `email`, so a child repository can be dirty, detached, absent, or on the wrong branch without appearing in the operational answer.

## Requirements (Outcome-Focused)

- Extend the operational projection with workspace authority and ordered repository inspections.
- Inspect each relevant registered Git root independently with the existing read-only Git command boundary.
- Select relevant repositories from work-item scope, always retaining authority identity.
- Add a stable `--repository <id>` focus compatible with `--id`.
- Preserve existing single-repository fields and human/JSON behavior.
- Emit repository-attributed findings and next actions without Git mutation.

## Acceptance Criteria (Verifiable)

- AC1: A three-repository fixture returns authority plus per-repository path, Git root, branch/detached, HEAD, upstream, and clean/dirty facts.
- AC2: `--id` limits repositories to the work item's declared scope plus authority and `--repository` focuses one registered repository; unknown IDs fail deterministically.
- AC3: Dirty, detached, missing, unavailable, and expected-branch mismatch fixtures identify the exact repository and never inherit the parent state.
- AC4: Human/JSON outputs share one model, remain deterministically ordered and source-attributed, preserve compatible single-repository output, and make no filesystem or Git changes.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Extend `project status`; do not create a parallel workspace status command or store.
- Use registered repository IDs as selector and output identities.
- Keep authority visible even when not the primary implementation repository.

## Validation Plan

- Create disposable parent/next/email Git roots with independently varied state.
- Compare human and JSON projections across selectors and failures.
- Capture every repository's HEAD/status and non-Git tree hash before and after status.
- Re-run the complete existing operational-status suite.
