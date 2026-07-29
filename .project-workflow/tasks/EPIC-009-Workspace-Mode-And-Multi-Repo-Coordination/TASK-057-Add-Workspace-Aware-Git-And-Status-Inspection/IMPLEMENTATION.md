## User Story

As a workspace owner, I want status to show each relevant Git root independently so that a healthy parent cannot conceal unsafe child-repository state.

## Goal

Extend the shared operational model, inspection, selection, rendering, and action logic with non-mutating repository-scoped Git facts.

## Approach

- Add repository status records alongside the compatible top-level authority Git value.
- Reuse the existing `_inspect_operational_git` boundary per registered root.
- Resolve work-item scope through TASK-056 metadata.
- Render human and JSON from the same inspection model.

## Phases

- Phase 1: Extend operational models/schema.
- Phase 2: Inspect relevant registered repositories.
- Phase 3: Add repository selector, rendering, findings, and actions.
- Phase 4: Prove compatibility and non-mutation.

## Parent AC Coverage

- AC6, AC7, AC8, AC10

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

## Acceptance Criteria

- [x] AC1: Three-root status contains complete repository-scoped Git facts and authority identity.
- [x] AC2: Work-item and repository selectors resolve deterministically through the registry.
- [x] AC3: Unsafe or unavailable child state remains repository-attributed and visible.
- [x] AC4: Human/JSON equivalence, single-repository compatibility, and non-mutation are proven.

## Validation

- AC1 / parent AC6: Snapshot a disposable parent/next/email status.
- AC2 / parent AC8: Exercise combined and invalid selectors.
- AC3 / parent AC7: Independently vary each unsafe child Git state.
- AC4 / parent AC8-AC10: Compare projections and before/after hashes/Git facts.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/BL-017-workspace-mode`; PR not created | Operational status suites plus 11 workspace-mode tests passed | Local implementation complete; push, merge, release, and deployment not authorized | `tests/test_workspace_mode.py`; exact-target receipt under TASK-059 |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Repository Status Model | Extend the operational schema with authority and ordered repository records. | AC1, AC4 | Inspect JSON schema fixture output. | Done |
| 2 | Multi-Root Git Inspection | Inspect each relevant registered Git root independently and read-only. | AC1, AC3, AC4 | Run three-root state matrix. | Done |
| 3 | Selection And Rendering | Add repository focus and render repository-attributed human/JSON findings/actions. | AC2, AC3, AC4 | Exercise selectors and golden outputs. | Done |
| 4 | Regression And Non-Mutation | Preserve existing status behavior and prove no repository changes. | AC4 | Run existing status suite and hash checks. | Done |

## Parent AC Evidence

- AC6: JSON repository records expose registered ID/path/role/authority plus Git root, branch or detached state, HEAD, upstream, and cleanliness for each independent root.
- AC7: Workspace dirty, detached, and unavailable states produce repository-named blocking findings/actions; invalid and missing roots fail config validation without mutation.
- AC8: Human output and additive JSON use the same snapshot; `--repository` and `--id` compose through registered scope while legacy payload tests remain unchanged.
- AC10: Disposable tests and the exact JohnDetlefs receipt compare repository facts before and after; all observations were identical.

## QA & Code Review

- Verdict: Pass
- Evidence: Status model/action/classification/CLI/inspection suites and workspace tests all passed; exact target returned three distinct roots unchanged.
- Findings: None in TASK-057 scope.

## Retro

- Reusable lessons: Keep the existing top-level Git field authoritative while adding repository records conditionally, so legacy consumers do not need a schema migration.
- Conventions or agent assets updated: Status help, human output, JSON output, README, and agent guidance now expose `--repository`.
- Follow-up tasks: Expected-branch policy remains intentionally out of scope; status reports the actual branch without inventing governance.

## Notes

- Task: TASK-057
- Title: Add Workspace-Aware Git And Status Inspection
- Created: 2026-07-29
