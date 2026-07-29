# Requirements

## Summary

- Task: TASK-056
- Title: Enforce Workflow Authority And Repository Scope
- Parent AC Coverage: AC3, AC4, AC5
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

- AC3: owner `TASK-055, TASK-056`; required evidence: Invalid registry and competing-authority fixture matrix with stable findings and repair paths.
- AC4: owner `TASK-056`; required evidence: Task, Fix, and Epic-child scaffold/readiness fixtures for valid and invalid repository scope.
- AC5: owner `TASK-056, TASK-058`; required evidence: Cross-repository readiness fixtures proving explicit scope, separate authority visibility, and no child tracker.

## Goal

Make repository ownership an enforceable work-item contract and prevent registered child repositories from becoming competing workflow authorities.

## Non-Goals

- Do not implement repository Git/status rendering or delivery evidence classification.
- Do not create child workflow state.
- Do not retroactively block legacy single-repository tasks that predate workspace metadata.

## Users & Context

Workspace tasks currently express primary and touched repositories through inconsistent prose. Agents need generated structure and readiness checks that resolve repository IDs through the authoritative registry while keeping old single-repository work usable.

## Requirements (Outcome-Focused)

- Add a consistent `Repository Scope` section to new task, Fix, and Epic-child requirements.
- Record primary repository and repositories touched as registered IDs.
- Validate workspace-mode scope during task and Epic-child readiness.
- Report live child `.project-workflow/` state as competing authority while ignoring authority-owned historical archives.
- Keep authority identity visible even when a child repository is the primary implementation owner.

## Acceptance Criteria (Verifiable)

- AC1: New task, Fix, and Epic-child scaffolds contain the same parseable repository-scope fields.
- AC2: Workspace readiness accepts valid scope and rejects missing, unknown, duplicate, or primary-not-touched repository IDs with stable findings.
- AC3: Doctor reports live workflow state in a registered non-authority Git root as competing authority without misclassifying authority-owned archives.
- AC4: Single-repository/legacy work remains compatible, while workspace-mode output names the authority separately from the primary implementation repository.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Repository scope is Markdown-native and parseable; no second task-state file is introduced.
- The authority repository is included in repositories touched when its tracked workflow artifacts are part of delivery.
- Legacy tasks are not rewritten automatically.

## Validation Plan

- Scaffold task, Fix, and Epic children in disposable single- and multi-repository roots.
- Exercise readiness against every valid/invalid scope combination.
- Exercise Doctor with live child state, archived parent state, and no child state.
