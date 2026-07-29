# Requirements

## Summary

- Task: TASK-059
- Title: Prove Upgrade, Guidance, And Real Workspace Journey
- Parent AC Coverage: AC11, AC12, AC13, AC14, AC15
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

- AC11: owner `TASK-059`; required evidence: Independently inspected disposable parent/next/email journey from declaration through handoff without child trackers or unauthorized delivery.
- AC12: owner `TASK-059`; required evidence: Recorded read-only topology/current-gap inspection of the exact JohnDetlefs parent, next, and email Git roots with no file or Git mutation.
- AC13: owner `TASK-055, TASK-059`; required evidence: Current, legacy, and workspace-declared upgrade fixtures plus preservation and packaged/helper parity evidence.
- AC14: owner `TASK-059`; required evidence: README and all managed agent guidance reviewed against the approved authority, invocation, evidence, and Git-action boundaries.
- AC15: owner `TASK-059`; required evidence: Focused/full test results, strict Doctor, backlog validation, parity, compilation, diff checks, and executed UVX packaging proof.

## Goal

Deliver the managed surfaces and decisive end-to-end proof that workspace mode works in a realistic parent/next/email topology and truthfully describes the real JohnDetlefs workspace without modifying it.

## Non-Goals

- Do not modify, upgrade, branch, commit, push, merge, release, or deploy any JohnDetlefs repository.
- Do not call fixture coverage a real-workspace journey or call read-only inspection adoption/deployment proof.
- Do not publish or release Project Workflow in this child.

## Users & Context

The owner needs this feature for active JohnDetlefs.com work. Automated fixtures protect breadth, but the operator experience must also be exercised in a disposable three-repository workspace and checked against the actual parent/next/email topology read-only.

## Requirements (Outcome-Focused)

- Align config templates, upgrade behavior, README, prompts, skills, agent guidance, and local/packaged helper parity.
- Build and independently inspect a disposable JohnDetlefs-shaped workspace journey covering declaration, work-item scope, varied Git state, validation/delivery evidence, status, readiness, QA, and handoff.
- Record exact runtime target/source proof for the disposable journey and real read-only topology/status inspection.
- Capture before/after Git/filesystem evidence proving no real JohnDetlefs mutation.
- Run focused, strict, parity, packaging, and full-suite validation under the declared Python 3.10 locked environment.

## Acceptance Criteria (Verifiable)

- AC1: Managed templates, upgrades, README, and all supported agent surfaces explain and preserve the approved workspace contract.
- AC2: A disposable parent/next/email journey completes declaration through handoff while surfacing independently varied repository state and creating no child tracker or unauthorized Git delivery.
- AC3: A structured runtime-target/source record identifies the exact real JohnDetlefs parent, `next`, and `email` Git roots, observes current status read-only, and proves before/after state is unchanged.
- AC4: Focused tests, legacy/current/workspace upgrade fixtures, strict Doctor, backlog validation, parity, compilation, diff checks, the Homebrew UVX packaging test, and the full Python 3.10 suite pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Mutation-based acceptance uses a disposable topology; the real target remains read-only.
- Parent-root invocation is documented as the first-version contract.
- This Epic ends at repository implementation/validation/closeout; release and deployment require separate authority.

## Validation Plan

- Review every managed surface against the approved invariants and invalid substitutes.
- Run an explicit disposable journey script and independently inspect its repositories and workflow artifacts.
- Capture real target repository roots, HEADs, branches, and porcelain status before/after read-only Project Workflow inspection.
- Run the complete repository validation command with UVX available at `/opt/homebrew/bin/uvx`.
