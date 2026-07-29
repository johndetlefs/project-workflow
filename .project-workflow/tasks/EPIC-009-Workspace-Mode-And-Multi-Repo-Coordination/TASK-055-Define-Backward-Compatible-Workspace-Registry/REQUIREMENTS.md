# Requirements

## Summary

- Task: TASK-055
- Title: Define Backward-Compatible Workspace Registry
- Parent AC Coverage: AC1, AC2, AC3, AC13
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

- AC1: owner `TASK-055`; required evidence: Parsed valid JohnDetlefs-shaped config showing stable IDs, paths, roles, and exactly one authority.
- AC2: owner `TASK-055`; required evidence: No-workspace regression matrix covering Doctor, task, Epic, status, and upgrade behavior.
- AC3: owner `TASK-055, TASK-056`; required evidence: Invalid registry and competing-authority fixture matrix with stable findings and repair paths.
- AC13: owner `TASK-055, TASK-059`; required evidence: Current, legacy, and workspace-declared upgrade fixtures plus preservation and packaged/helper parity evidence.

## Goal

Give Project Workflow one safe, backward-compatible config model for declaring a workspace authority and its independent Git repositories.

## Non-Goals

- Do not inspect work-item scope, render multi-repository status, or classify repository evidence in this child.
- Do not add an automatic config editor or repository discovery engine.
- Do not require workspace configuration for ordinary single-repository installations.

## Users & Context

Repository owners currently use `.project-workflow/config.json` for namespaces and warning policy. Workspace owners need to extend that established contract without a second config file, while invalid or unsafe paths must fail before later commands trust them.

## Requirements (Outcome-Focused)

- Add immutable workspace/repository models to the loaded workflow config.
- Parse an optional `workspace` object with one authority repository and an ordered repository list.
- Preserve the current implicit single-repository behavior when `workspace` is absent.
- Reject malformed IDs, roles, authority references, duplicate IDs/paths, absolute/outside/symlink-escaped paths, missing paths, non-Git roots, and multiple entries resolving to one Git root.
- Preserve user-owned workspace declarations through current and legacy upgrade flows.

## Acceptance Criteria (Verifiable)

- AC1: A JohnDetlefs-shaped config parses into stable `workspace`, `next`, and `email` repository records with exactly one authority.
- AC2: A config without `workspace` produces the existing implicit `.` repository model and does not change current Doctor/status/task behavior.
- AC3: Every invalid registry case in the parent envelope produces a deterministic config error or Doctor finding that identifies `.project-workflow/config.json` and the rejected field/path.
- AC4: Upgrade planning/apply preserves an existing workspace declaration byte-for-byte unless a reviewed schema migration explicitly targets it.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- The registry lives in existing `.project-workflow/config.json`.
- Repository IDs are stable lower-case slugs; paths are workspace-relative.
- `control` and `implementation` are the first roles; the authority may still own implementation files.
- No-workspace config remains implicit single-repository mode.

## Validation Plan

- Add focused config/model tests for valid, absent, malformed, duplicate, escaped, symlinked, missing, non-Git, and aliased-root declarations.
- Re-run existing namespace/config, Doctor, status, init, and upgrade regression tests.
- Prove upgrade preservation using before/after config bytes and plan/apply fixtures.
