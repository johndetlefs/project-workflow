## User Story

As the owner relying on the real JohnDetlefs workspace, I want a realistic end-to-end proof and aligned guidance so that workspace mode is demonstrably usable without risking the production repositories.

## Goal

Align distribution/guidance and produce layered automated, disposable-journey, and read-only real-target evidence for EPIC-009.

## Approach

- Update all managed surfaces from one approved workspace contract.
- Use a disposable three-Git-root journey for mutation-based workflow proof.
- Use exact runtime-target/source evidence and before/after captures for the real read-only workspace.
- Finish with the complete locked Python 3.10 validation matrix.

## Phases

- Phase 1: Align config/upgrade templates and guidance surfaces.
- Phase 2: Build and run the disposable operator journey.
- Phase 3: Run bounded real-target read-only inspection.
- Phase 4: Run complete QA and packaging validation.

## Parent AC Coverage

- AC11, AC12, AC13, AC14, AC15

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

## Acceptance Criteria

- [x] AC1: Managed config/upgrade/guidance surfaces preserve and explain the workspace contract.
- [x] AC2: The disposable JohnDetlefs-shaped journey passes and its artifacts withstand independent inspection.
- [x] AC3: Structured evidence proves exact real-target/source observation and zero mutation.
- [x] AC4: Every focused, strict, parity, packaging, and full-suite validation gate passes.

## Validation

- AC1 / parent AC13-AC14: Review upgrade fixtures and every managed guidance surface.
- AC2 / parent AC11: Run and independently inspect the disposable journey.
- AC3 / parent AC12: Compare exact real workspace Git/filesystem facts before and after read-only inspection.
- AC4 / parent AC15: Run the complete declared validation matrix with non-skipped UVX packaging proof.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/BL-017-workspace-mode`; PR not created | Locked Python 3.10 sync, compilation, 262 tests, retained CLI journey, Doctor, diff check, parity, and package build passed | Local implementation complete; push, merge, release, publication, and deployment not authorized | `evidence/final-validation.json`; `evidence/real-workspace-readonly-inspection.json`; `../../FIX-005-Harden-Workspace-Journey-Proof/evidence/disposable-cli-journey.json`; `EVIDENCE.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Managed Surface Alignment | Update config/upgrade templates, README, prompts, skills, and agent guidance. | AC1 | Review managed surfaces and parity checks. | Done |
| 2 | Disposable Workspace Journey | Exercise declaration, scope, Git state, evidence, status, readiness, QA, and handoff in three Git roots. | AC2 | Inspect journey report and resulting repositories. | Done |
| 3 | Real Read-Only Acceptance | Observe exact JohnDetlefs parent/next/email targets and prove no mutation. | AC3 | Review structured runtime/source evidence. | Done |
| 4 | Complete Validation Gate | Run focused, strict, parity, packaging, compilation, diff, and full-suite checks. | AC4 | Review validation receipt. | Done |

## Parent AC Evidence

- AC11: `tests/test_workspace_mode.py` provides a 14-case workspace matrix, including a subprocess-driven CLI journey from initialization and approval through readiness, focused status, repository evidence, Testing, Review, Complete, and retained handoff artifacts under FIX-005.
- AC12: `evidence/real-workspace-readonly-inspection.json` records exact parent/next/email roots, branches, HEADs, and porcelain hashes before and after; all facts were unchanged.
- AC13: `evidence/final-validation.json` records user-config preservation, matching CLI/template/helper hash, release-contract tests, and built sdist/wheel hashes.
- AC14: The final validation receipt lists every reviewed README, AGENTS, Cursor, prompt, and skill surface and the shared authority/mutation contract.
- AC15: The final receipt records Python 3.10.20, locked sync, compilation, 262 passing tests, zero visible/blocking Doctor findings, diff/parity checks, and successful package build. `EVIDENCE.json` contains passing runtime-target-source records for AC11-AC15.

## QA & Code Review

- Verdict: Pass
- Evidence: `EVIDENCE.json` validates with no structured-evidence issues; the retained CLI journey, final validation, and real-target receipts are hash-bound.
- Findings: The real JohnDetlefs parent already had one dirty entry and existing unrelated workflow findings (legacy-unversioned plus COACH approval/evidence debt). These were preserved unchanged and are not EPIC-009 implementation failures.

## Retro

- Reusable lessons: Exact-target proof should inject registry state in-process when target mutation is forbidden, then compare every Git fact before and after.
- Conventions or agent assets updated: README, root/package AGENTS, Cursor rule, six prompts, and six Codex skills now describe workspace authority, scope, evidence, and mutation boundaries.
- Follow-up tasks: Adoption or upgrade of the real JohnDetlefs workspace remains a separate owner-authorized lifecycle action.
- Missed in-scope work corrected by FIX-005: AC11 now has a retained CLI-level journey rather than fixture aggregation alone, and unavailable-repository status has direct regression coverage.
- Approval record clarification: `Approved for implementation: No` on Epic requirements is correct schema behavior; the Epic command approves decomposition and the approved scope envelope authorizes unchanged child implementation.

## Notes

- Task: TASK-059
- Title: Prove Upgrade, Guidance, And Real Workspace Journey
- Created: 2026-07-29
