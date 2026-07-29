## User Story

As a workspace owner, I want every new work item to name valid repository owners so that readiness and handoff cannot depend on free-form conventions.

## Goal

Generate and validate repository scope across tasks, Fixes, and Epic children while enforcing one live workflow authority.

## Approach

- Add one canonical Markdown section and parser.
- Apply workspace-mode gates to readiness without retroactive legacy churn.
- Reuse registry records from TASK-055 for ID resolution.
- Add Doctor authority checks that distinguish live child state from parent-owned archives.

## Phases

- Phase 1: Add shared scope template/parser.
- Phase 2: Integrate readiness validation.
- Phase 3: Add competing-authority Doctor checks.
- Phase 4: Prove scaffolding and compatibility.

## Parent AC Coverage

- AC3, AC4, AC5

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

- AC3: owner `TASK-055, TASK-056`; required evidence: Invalid registry and competing-authority fixture matrix with stable findings and repair paths.
- AC4: owner `TASK-056`; required evidence: Task, Fix, and Epic-child scaffold/readiness fixtures for valid and invalid repository scope.
- AC5: owner `TASK-056, TASK-058`; required evidence: Cross-repository readiness fixtures proving explicit scope, separate authority visibility, and no child tracker.

## Acceptance Criteria

- [x] AC1: All new work-item types emit one parseable repository-scope contract.
- [x] AC2: Readiness accepts only complete registered workspace scope.
- [x] AC3: Doctor rejects competing live child workflow state and permits authority-owned archives.
- [x] AC4: Authority and primary implementation ownership remain distinct and legacy work stays compatible.

## Validation

- AC1 / parent AC4: Compare task, Fix, and Epic-child scaffold output.
- AC2 / parent AC4-AC5: Run readiness across valid and invalid scope matrices.
- AC3 / parent AC3: Run Doctor against competing-child and archive fixtures.
- AC4 / parent AC5: Run no-workspace and child-primary workspace fixtures.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/BL-017-workspace-mode`; PR not created | Workspace scaffold/scope and Doctor authority tests passed within 262-test suite | Local implementation complete; push, merge, release, and deployment not authorized | `tests/test_workspace_mode.py`; TASK-059 final validation receipt |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Repository Scope Contract | Add one shared requirements structure and parser for primary/touched repository IDs. | AC1 | Scaffold and inspect all work-item types. | Done |
| 2 | Readiness Gates | Resolve scope through the registry and fail incomplete or contradictory workspace scope. | AC2, AC4 | Run readiness matrix. | Done |
| 3 | Authority Enforcement | Detect competing live child workflow state without flagging authority-owned archives. | AC3 | Run Doctor authority fixtures. | Done |
| 4 | Compatibility Tests | Preserve legacy and implicit single-repository behavior. | AC4 | Run existing task/Fix/Epic readiness tests. | Done |

## Parent AC Evidence

- AC3: `test_doctor_rejects_competing_child_workflow_state` produces `PW_WORKSPACE_AUTHORITY_CONFLICT`; authority-owned workflow archives are outside every child root and remain valid.
- AC4: Task, Fix, and Epic-child templates derive their default repository ID from the authority registry; readiness rejects missing, unknown, duplicate, and primary-not-touched scope.
- AC5: Focused child-primary status retains `workspace_authority` separately and filters repository records through the work-item scope without creating child state.

## QA & Code Review

- Verdict: Pass
- Evidence: 262 tests passed, including all existing task/Fix/Epic readiness regressions and new workspace authority/scope fixtures.
- Findings: None in TASK-056 scope.

## Retro

- Reusable lessons: Authority identity and primary implementation ownership must be separate fields even when they point to the same repository.
- Conventions or agent assets updated: Task, Fix, Epic-child, Doctor, readiness, prompts, and skills use one repository-scope contract.
- Follow-up tasks: None.

## Notes

- Task: TASK-056
- Title: Enforce Workflow Authority And Repository Scope
- Created: 2026-07-29
