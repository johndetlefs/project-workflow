# Epic Contract

## Summary

- Epic: EPIC-009
- Title: Workspace Mode And Multi-Repo Coordination
- Last updated: 2026-07-29

## Sources of Truth

- `.project-workflow/tasks/EPIC-009-Workspace-Mode-And-Multi-Repo-Coordination/REQUIREMENTS.md` for the owner-approved outcome, boundaries, acceptance criteria, and proposed child work.
- `.project-workflow/config.json` for the optional workspace declaration, authority repository, repository registry, task namespaces, ID generation, and accepted warnings.
- `.project-workflow/CONSTITUTION.md` and `.project-workflow/BACKLOG.md` for the enabler-first, evidence-pulled product boundary.
- The authority repository's `.project-workflow/TRACKER.md`, Epic trackers, and work-item artifacts for the only live workflow lifecycle state.
- Work-item repository-scope and repository-evidence sections for primary repository, repositories touched, validation, branch/PR, integration, and delivery attribution.
- Read-only local Git observation from each registered repository root for branch/detached state, HEAD, upstream, and clean/dirty facts.
- Existing Doctor, operational-status, readiness, evidence, upgrade, and managed-asset parity logic in `src/project_workflow/cli.py` and its generated helper mirror.
- `/Users/johndetlefs/repos/johndetlefs`, `next/`, and `email/` as a read-only real topology and current-gap acceptance target; their contents are not EPIC-009 workflow state and are not authorized mutation targets.
- Disposable three-repository fixtures and a manual JohnDetlefs-shaped journey for mutation-based validation.

## Invalid Substitutes

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

## Invariants

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

## Artifact Targets

- Workspace registry and authority models, config parsing, validation, and stable findings in `src/project_workflow/cli.py`.
- Backward-compatible config template and repository-schema/upgrade handling.
- Doctor checks for registry safety, distinct Git roots, authority ownership, and competing child workflow state.
- Consistent repository-scope and repository-evidence structures in task, Fix, and Epic-child templates plus readiness/lifecycle validation.
- Workspace-aware operational projection, repository-focused selection, human output, and versioned JSON output built on the existing `project status` model.
- Table-driven workspace, Git-state, evidence-attribution, non-mutation, and compatibility tests under `tests/`.
- Disposable three-repository manual journey evidence and bounded read-only JohnDetlefs topology/status evidence.
- README and managed Codex, Cursor, Claude Code, and GitHub Copilot guidance describing the workspace contract and authority boundaries.
- EPIC-009 decomposition, child artifacts, structured evidence where triggered, acceptance map/audit, QA, retro, and closeout records.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-055 | Parsed valid JohnDetlefs-shaped config showing stable IDs, paths, roles, and exactly one authority. |
| AC2 | TASK-055 | No-workspace regression matrix covering Doctor, task, Epic, status, and upgrade behavior. |
| AC3 | TASK-055, TASK-056 | Invalid registry and competing-authority fixture matrix with stable findings and repair paths. |
| AC4 | TASK-056 | Task, Fix, and Epic-child scaffold/readiness fixtures for valid and invalid repository scope. |
| AC5 | TASK-056, TASK-058 | Cross-repository readiness fixtures proving explicit scope, separate authority visibility, and no child tracker. |
| AC6 | TASK-057 | Three-Git-root human/JSON status output with repository-scoped Git facts. |
| AC7 | TASK-057 | Independently varied dirty, detached, missing, unavailable, and wrong-branch child fixtures plus non-mutation captures. |
| AC8 | TASK-057 | Golden human/JSON outputs proving one model, focused selectors, deterministic ordering, provenance, and compatibility. |
| AC9 | TASK-058 | Per-repository evidence matrix proving isolation of validation, PR, integration, release, and deployment claims. |
| AC10 | TASK-057, TASK-058 | Before/after filesystem hashes and Git captures across success, warning, malformed, and failure paths. |
| AC11 | TASK-059 | Independently inspected disposable parent/next/email journey from declaration through handoff without child trackers or unauthorized delivery. |
| AC12 | TASK-059 | Recorded read-only topology/current-gap inspection of the exact JohnDetlefs parent, next, and email Git roots with no file or Git mutation. |
| AC13 | TASK-055, TASK-059 | Current, legacy, and workspace-declared upgrade fixtures plus preservation and packaged/helper parity evidence. |
| AC14 | TASK-059 | README and all managed agent guidance reviewed against the approved authority, invocation, evidence, and Git-action boundaries. |
| AC15 | TASK-059 | Focused/full test results, strict Doctor, backlog validation, parity, compilation, diff checks, and executed UVX packaging proof. |
