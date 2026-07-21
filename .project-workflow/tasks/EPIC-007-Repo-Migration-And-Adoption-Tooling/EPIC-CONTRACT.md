# Epic Contract

## Summary

- Epic: EPIC-007
- Title: Repo Migration And Adoption Tooling
- Last updated: 2026-07-10

## Sources of Truth

- `.project-workflow/tasks/EPIC-007-Repo-Migration-And-Adoption-Tooling/REQUIREMENTS.md`
- Current project-workflow CLI behavior in `src/project_workflow/cli.py`
- Packaged generated helper template in `src/project_workflow/templates/workflow.py`
- Current generated prompts, Codex skills, Cursor rules, and managed Project Workflow block assets
- Doctor output from the project-workflow repo and sibling repository review evidence recorded in the epic requirements
- Existing user-owned workflow state in target repositories

## Invalid Substitutes

- A successful `project init` run alone is not proof that a repository is migrated.
- A clean old local helper is not proof that the helper exposes current commands.
- Accepted warnings are not active blockers, but they are also not proof that underlying historical evidence was refreshed.
- Manual tracker edits are not a substitute for migration/adoption commands when a CLI command exists.
- Generated `*.new` files are not migrated until reviewed, merged, or otherwise resolved.
- Tests against only a freshly initialized repository are not enough; migration fixtures must cover stale installs and historical workflow state.

## Invariants

- Migration starts with a dry run that does not mutate repository files.
- User-owned files and unmarked content are preserved unless the user explicitly chooses a fix.
- Generated files may be refreshed only when they carry the project-workflow generated marker or live inside a managed block.
- Accepted-warning fingerprints remain exact matches over severity, repo-relative path, and message.
- Stale or missing approval and evidence remain visible until explicitly approved, adopted, refreshed, or accepted with a reason.
- Commands must be safe to run from a repository root and must explain concrete next actions.
- Current tests must continue to pass while migration support is added.

## Artifact Targets

- CLI commands and helpers in `src/project_workflow/cli.py` and `src/project_workflow/templates/workflow.py`
- Tests under `tests/`, preferably split or grouped by migration/adoption behavior when practical
- Generated agent guidance in `src/project_workflow/prompts/`, `src/project_workflow/codex/`, and `src/project_workflow/cursor/` when command behavior changes
- README and changelog updates that explain the migration/adoption workflow
- Workflow artifacts under `.project-workflow/tasks/EPIC-007-Repo-Migration-And-Adoption-Tooling/`

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | Define Migration Command Shape And Dry-Run Report, Add Helper Version And Capability Detection | Fixture output showing stale helper/capability detection with no file mutation. |
| AC2 | Define Migration Command Shape And Dry-Run Report, Add Migration Fixtures And Regression Tests | Fixture output showing grouped blockers, current warnings, legacy warnings, accepted warnings, stale generated assets, and safe mechanical fixes. |
| AC3 | Define Migration Command Shape And Dry-Run Report, Implement Safe Mechanical Repair Apply Path | Migration plan output listing exact actions and categories for automatic versus owner-confirmed decisions. |
| AC4 | Implement Safe Mechanical Repair Apply Path | Before/after fixture evidence showing low-risk repairs applied without overwriting user-owned unmarked content. |
| AC5 | Add Batch Accepted-Warning Review Support | Tests and fixture output showing selected warning fingerprints added with reasons and changed/unselected warnings still visible. |
| AC6 | Harden Sequential ID And Backlog Write Safety | Regression test proving duplicate sequential IDs are prevented or detected/retried; documentation of unique-ID mitigation if applicable. |
| AC7 | Implement Safe Mechanical Repair Apply Path, Add Migration Fixtures And Regression Tests | Test proving backlog promotion to epic creates current required epic artifacts and doctor has no immediate missing-artifact warning. |
| AC8 | Implement Safe Mechanical Repair Apply Path, Add Batch Accepted-Warning Review Support | Before/after fixture evidence showing existing tracker rows, docs, backlog rows, guidance, and config values are preserved. |
| AC9 | Add Migration Fixtures And Regression Tests | Passing targeted tests plus full suite output. |
