# Requirements

## Summary

- Task: TASK-058
- Title: Attribute Validation And Delivery Evidence By Repository
- Parent AC Coverage: AC5, AC9, AC10
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

- AC5: owner `TASK-056, TASK-058`; required evidence: Cross-repository readiness fixtures proving explicit scope, separate authority visibility, and no child tracker.
- AC9: owner `TASK-058`; required evidence: Per-repository evidence matrix proving isolation of validation, PR, integration, release, and deployment claims.
- AC10: owner `TASK-057, TASK-058`; required evidence: Before/after filesystem hashes and Git captures across success, warning, malformed, and failure paths.

## Goal

Make validation, branch/PR, integration, and later delivery claims explicit and isolated for each touched repository.

## Non-Goals

- Do not automatically execute validation, Git, PR, release, or deployment actions.
- Do not require later delivery stages for repository implementation completion.
- Do not add authenticated external authority or assurance levels.

## Users & Context

Cross-repository handoffs currently rely on prose that can omit one repository or let one repository's successful checks imply another's state. Owners need one parseable evidence table with bounded states and repository identity.

## Requirements (Outcome-Focused)

- Add a canonical `Repository Evidence` table to implementation artifacts.
- Require one row per touched repository before Review/Complete evidence credit.
- Record branch, PR/integration state, validation command/method and result, delivery state, and evidence source.
- Accept explicit bounded states such as not applicable, not authorized, and not recorded without treating them as successful delivery.
- Extend status proof/delivery classification to preserve repository isolation and the weakest relevant state.

## Acceptance Criteria (Verifiable)

- AC1: New task, Fix, and Epic-child implementation artifacts expose the same parseable repository-evidence table.
- AC2: Review/Complete gates reject missing/unknown/duplicate repository rows or unattributed validation evidence and accept complete bounded records without requiring unauthorized later delivery.
- AC3: Status independently reports each repository's validation, branch/PR, integration, release, and deployment evidence and never promotes one repository from another's record.
- AC4: Evidence parsing/classification and all failure paths are deterministic, source-attributed, backward compatible outside workspace mode, and non-mutating.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Evidence remains Markdown-native and repository-attributed.
- `not authorized`, `not applicable`, and `not recorded` are truthful states, not pass verdicts.
- The workflow validates evidence records but does not execute their commands.

## Validation Plan

- Scaffold and parse repository-evidence tables for all work-item types.
- Independently vary repository rows and later delivery stages.
- Exercise Review/Complete gates with missing, bounded, passing, and contradictory records.
- Capture before/after hashes and re-run existing proof/delivery regression tests.
