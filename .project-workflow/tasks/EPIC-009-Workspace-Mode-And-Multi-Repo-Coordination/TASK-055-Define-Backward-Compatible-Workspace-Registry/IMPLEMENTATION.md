## User Story

As a workspace owner, I want repository boundaries and workflow authority declared in the existing config so that later workflow commands use one validated topology instead of prose assumptions.

## Goal

Implement the workspace registry model, parser, safety validation, implicit single-repository fallback, and upgrade preservation.

## Approach

- Extend `WorkflowConfig` with immutable workspace/repository records.
- Resolve declared paths from the authoritative root and validate filesystem/Git boundaries without mutation.
- Keep absence of the new config object behaviorally identical to the current product.
- Centralize stable config failures so Doctor and direct config consumers agree.

## Phases

- Phase 1: Add models and valid/implicit parsing.
- Phase 2: Add fail-closed path/Git/authority validation.
- Phase 3: Preserve declarations through config templates and upgrades.
- Phase 4: Run focused and regression validation.

## Parent AC Coverage

- AC1, AC2, AC3, AC13

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

## Acceptance Criteria

- [x] AC1: Valid workspace config returns ordered repository records and one authority.
- [x] AC2: Missing workspace config retains implicit single-repository behavior.
- [x] AC3: Invalid declarations fail deterministically with source-specific repair direction.
- [x] AC4: Upgrade fixtures preserve user-owned workspace declarations.

## Validation

- AC1 / parent AC1: Parse a disposable parent/next/email registry and assert IDs, roles, paths, and authority.
- AC2 / parent AC2: Run existing no-workspace config, Doctor, and status fixtures unchanged.
- AC3 / parent AC3: Run the full invalid-registry matrix including symlink and duplicate Git-root aliases.
- AC4 / parent AC13: Compare config bytes before/after current and legacy upgrade fixtures.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/BL-017-workspace-mode`; PR not created | 262-test suite passed; workspace registry matrix passed | Local implementation complete; push, merge, release, and deployment not authorized | `tests/test_workspace_mode.py`; `evidence/final-validation.json` under TASK-059 |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Workspace Registry Model | Extend loaded config with repository and authority records plus implicit single-repository fallback. | AC1, AC2 | Run focused valid/absent config tests. | Done |
| 2 | Registry Safety Validation | Reject malformed, duplicate, escaped, missing, non-Git, and aliased-root declarations deterministically. | AC3 | Run invalid-registry table tests. | Done |
| 3 | Upgrade Preservation | Keep workspace declarations user-owned through config templates and upgrade planning/apply. | AC4 | Compare config bytes across upgrade fixtures. | Done |
| 4 | Regression Gate | Re-run config, Doctor, status, init, and upgrade tests. | AC1, AC2, AC3, AC4 | Review focused and regression results. | Done |

## Parent AC Evidence

- AC1: `test_workspace_status_reports_each_independent_repository_and_selector` proves ordered registered records and one authority.
- AC2: Existing operational-status and Doctor suites remained unchanged and passed; workspace output is additive only when declared.
- AC3: `tests/test_workspace_mode.py` covers duplicate IDs, traversal, missing directories, non-Git nested paths, aliased Git roots, symlink escape, invalid control roles, and competing authority state.
- AC13: `test_workspace_registry_remains_user_owned_during_managed_upgrade` proves the config is excluded from managed outputs and remains byte-identical.

## QA & Code Review

- Verdict: Pass
- Evidence: 262 tests passed; Python compilation passed; package build passed; Doctor has zero visible/blocking findings.
- Findings: None in TASK-055 scope.

## Retro

- Reusable lessons: Validate configured paths as resolved, unique Git roots rather than treating path existence as repository identity.
- Conventions or agent assets updated: Shared config model and README/managed guidance now define the optional parent-workspace registry.
- Follow-up tasks: None.

## Notes

- Task: TASK-055
- Title: Define Backward-Compatible Workspace Registry
- Created: 2026-07-29
