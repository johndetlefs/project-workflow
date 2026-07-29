## User Story

As a workspace owner, I want every repository's validation and delivery state recorded separately so that a handoff cannot borrow proof from another Git root or imply an unauthorized later action.

## Goal

Add the repository-evidence contract, lifecycle gates, and operational classification needed for truthful multi-repository handoff.

## Approach

- Use one Markdown table keyed by registered repository ID.
- Validate complete repository coverage at Review/Complete in workspace mode.
- Preserve explicit bounded non-delivery states.
- Extend the existing proof/delivery projection without a second store.

## Phases

- Phase 1: Add shared evidence template/parser.
- Phase 2: Add Review/Complete validation.
- Phase 3: Add repository evidence to status classification/rendering.
- Phase 4: Prove isolation, compatibility, and non-mutation.

## Parent AC Coverage

- AC5, AC9, AC10

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

- AC5: owner `TASK-056, TASK-058`; required evidence: Cross-repository readiness fixtures proving explicit scope, separate authority visibility, and no child tracker.
- AC9: owner `TASK-058`; required evidence: Per-repository evidence matrix proving isolation of validation, PR, integration, release, and deployment claims.
- AC10: owner `TASK-057, TASK-058`; required evidence: Before/after filesystem hashes and Git captures across success, warning, malformed, and failure paths.

## Acceptance Criteria

- [x] AC1: All work-item types emit one parseable repository-evidence contract.
- [x] AC2: Lifecycle evidence gates require truthful coverage without forcing unauthorized delivery.
- [x] AC3: Status keeps validation and delivery claims isolated per repository.
- [x] AC4: Parsing, classification, compatibility, provenance, and non-mutation are proven.

## Validation

- AC1 / parent AC5: Scaffold and parse task, Fix, and Epic-child evidence.
- AC2 / parent AC9: Exercise lifecycle gates with missing, bounded, and passing evidence.
- AC3 / parent AC9: Independently vary every repository evidence dimension.
- AC4 / parent AC10: Run compatibility and before/after hash fixtures.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/BL-017-workspace-mode`; PR not created | Repository-evidence and lifecycle matrix passed within 262-test suite | Local implementation complete; push, merge, release, and deployment not authorized | `tests/test_workspace_mode.py`; TASK-059 final validation receipt |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Repository Evidence Contract | Add one shared implementation table and parser keyed by registered repository ID. | AC1 | Scaffold and inspect all work-item types. | Done |
| 2 | Lifecycle Evidence Gates | Require complete, truthful per-repository records at Review/Complete. | AC2 | Run lifecycle evidence matrix. | Done |
| 3 | Operational Classification | Report repository validation and delivery layers without cross-repository inflation. | AC3 | Inspect human/JSON varied evidence fixtures. | Done |
| 4 | Compatibility And Safety | Preserve legacy mode and prove deterministic non-mutation. | AC4 | Run proof/delivery regression and hash checks. | Done |

## Parent AC Evidence

- AC5: Task, Fix, and Epic-child scaffolds emit repository evidence keyed by registered repository ID; focused status keeps the parent authority separate.
- AC9: Review/Complete gates reject missing, duplicate, unregistered, out-of-scope, or unvalidated rows while preserving explicit not-recorded/not-authorized later delivery boundaries.
- AC10: Status evidence is attached only to the matching repository record with source provenance; disposable and exact-target inspections are read-only.

## QA & Code Review

- Verdict: Pass
- Evidence: Repository scope/evidence helpers, Fix/Task/Epic lifecycle gates, Doctor, focused status attribution, and all 262 regressions passed.
- Findings: None in TASK-058 scope.

## Retro

- Reusable lessons: Validation proof must be present before Review, while later branch/PR or delivery actions may truthfully remain not recorded or not authorized.
- Conventions or agent assets updated: Shared Repository Evidence table added to Task, Fix, and Epic-child templates plus implementation, QA, epic, Fix, and requirements guidance.
- Follow-up tasks: None.

## Notes

- Task: TASK-058
- Title: Attribute Validation And Delivery Evidence By Repository
- Created: 2026-07-29
