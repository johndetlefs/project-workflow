# Requirements

## Summary

- Task: TASK-046
- Title: Align Documentation And Generated Agent Assets
- Parent AC Coverage: AC2, AC3, AC5, AC9
- Last updated: 2026-07-21

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

- `project init` owns managed installation and refresh; `project doctor` owns diagnosis; `project upgrade` owns versioned repository-state transformation.
- Upgrade planning is non-mutating by default.
- Apply requires an explicit flag, a clean worktree, a supported source version, and fresh version/hash preconditions.
- The first release applies the complete validated mechanical plan or no changes.
- Migration IDs are immutable and ordered.
- Successful migrations are idempotent; reapplying at the target schema is a no-op.
- Atomic failure cannot leave partial file changes.
- User-owned and unmarked content is preserved.
- Existing project history, approvals, deferrals, evidence, accepted warnings, and unresolved decisions are never silently rewritten into current passing state.
- Unsupported or unrecognized state blocks with a stable finding and concrete next action.
- Human output and machine-readable output describe the same findings and plan.
- Packaged and generated command behavior must remain aligned.

### Invalid Substitutes

- A successful `project init` run is not proof that durable repository state was upgraded.
- A clean old helper or old doctor result is not proof that the repository uses the current schema.
- Package version alone is not a substitute for separate asset and repository-schema versions.
- An agent-authored prose summary is not a substitute for a deterministic machine-readable upgrade plan.
- A passing plan is not proof that apply produced the predicted diff.
- Tests against only freshly initialized repositories are not historical upgrade evidence.
- Backups or Git availability do not permit overwriting user-owned content.
- Accepted warnings, inferred approvals, or stale evidence are not upgraded authority or proof.
- Best-effort partial changes are not an acceptable substitute for atomic application.

### Artifact Targets

- Managed repository metadata at `.project-workflow/manifest.json`
- Upgrade command, plan model, migration registry, and apply engine in `src/project_workflow/cli.py` with behavioral parity in `src/project_workflow/templates/workflow.py`
- Stable structured doctor and upgrade-plan output schemas
- Historical repository fixtures and focused regression coverage under `tests/`
- Generated agent guidance under `src/project_workflow/prompts/`, `src/project_workflow/codex/`, and `src/project_workflow/cursor/`
- README and changelog documentation for init, doctor, and upgrade responsibilities
- EPIC-007 child requirements, implementation plans, evidence, QA, acceptance map/audit, and closeout artifacts

### Parent AC Proof Ownership

- AC2: owner `Add Structured Doctor Findings, Align Documentation And Generated Agent Assets`; required evidence: Tests and captured output proving stable finding codes and equivalent human/machine-readable fields.
- AC3: owner `Build Deterministic Upgrade Planner, Add Historical Migration Registry And Fixtures`; required evidence: Before/after fixture hashes proving zero plan mutation plus complete ordered plan records for every supported source schema.
- AC5: owner `Define Repository Version Manifest And Compatibility Policy, Integrate Init Version Detection And Upgrade Direction`; required evidence: Legacy/current init fixtures proving managed refresh and honest schema/upgrade direction without repository-state mutation.
- AC9: owner `Add Historical Migration Registry And Fixtures, Align Documentation And Generated Agent Assets`; required evidence: Passing targeted and full-suite output, strict doctor, backlog validation, and packaged/generated parity evidence.

## Goal

Document one accurate human and agent operating model for version-aware init, structured Doctor diagnostics, non-mutating upgrade planning, and explicit transactional apply.

## Non-Goals

- Changing upgrade behavior or adding new migration scope.
- Duplicating every CLI implementation detail in every agent asset.
- Publishing a release or changing package versions.

## Users & Context

- Owners need a concise safe path for new, current, and legacy repositories.
- Agents need explicit command ownership and mutation boundaries.
- CI needs discoverable JSON output and exit semantics.

## Requirements (Outcome-Focused)

- Update README structure, init behavior, Doctor JSON/finding fields, and complete plan/review/apply commands.
- Link and align the compatibility policy with the implemented support window and migration ID.
- Update changelog with the complete unreleased upgrade system.
- Update managed instructions, Codex/Cursor guidance, and relevant prompts/skills to preserve init/doctor/upgrade separation and explicit apply fingerprinting.
- Refresh generated local assets and prove source/generated parity.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent ACs AC2, AC3, AC5: README gives runnable fresh/legacy init, Doctor human/JSON, upgrade plan, and explicit apply instructions with safety boundaries.
- AC2: Covers parent AC AC9: compatibility/changelog accurately name schema 1, legacy migration, support policy, rollback/idempotency, and limitations.
- AC3: Covers parent ACs AC2, AC3, AC5, AC9: generated agent assets consistently direct install/refresh to init, diagnosis to Doctor, and transformation to upgrade with fingerprinted apply.
- AC4: Covers parent AC AC9: documentation assertions, full pytest, parity, compilation, and strict Doctor pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Keep README task-oriented and link to `COMPATIBILITY.md` for support policy detail.
- Show JSON commands for automation and human commands for review.
- State that accepted/owner findings survive migration and apply requires a clean worktree.

## Validation Plan

- Search every generated agent surface for the command ownership and apply safety language.
- Run documentation contract assertions, full pytest, init refresh, parity, compilation, and strict Doctor.
