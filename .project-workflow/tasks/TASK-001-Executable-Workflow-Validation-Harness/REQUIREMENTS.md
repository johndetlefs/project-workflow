# Requirements

## Summary

- Task: TASK-001
- Title: Executable Workflow Validation Harness
- Last updated: 2026-06-02

## Goal

Give maintainers and AI agents an executable way to verify that project-workflow state is safe enough to continue, instead of relying only on prompt instructions and manual inspection.

## Non-Goals

- Building a full project-management dashboard.
- Replacing the existing Markdown artifact format.
- Implementing full delegated execution scheduling.
- Enforcing every possible workflow convention in the first pass.

## Users & Context

- Maintainers changing project-workflow prompts, templates, and CLI behavior.
- AI agents working in initialized repositories that need a quick preflight before continuing autonomous work.
- Reviewers who need machine-checkable evidence that workflow assets and tracker state are structurally sound.

## Requirements (Outcome-Focused)

- A maintainer can run an executable workflow validation command from the packaged CLI.
- The local workflow CLI template exposes the same validation command in initialized repositories.
- The validation command catches structural workflow issues that directly affect safe AI autonomy.
- The source repository can detect drift between development prompt/template assets and packaged install assets.
- The command distinguishes blocking errors from strict-mode safety warnings so existing repositories can adopt it incrementally.
- Regression tests cover the validation command and the highest-risk failure cases.

## Acceptance Criteria (Verifiable)

- AC1: `project doctor` and `project validate` are available from the packaged CLI and return success for a freshly initialized repository with valid scaffold state.
- AC2: The generated local workflow CLI exposes equivalent `doctor` and `validate` commands.
- AC3: In this source repository, the command detects drift between `.github/prompts` and `src/project_workflow/prompts`, and between `.project-workflow/cli` and `src/project_workflow/templates`.
- AC4: The command validates global tracker structure, allowed statuses, linked docs paths, and epic tracker schemas.
- AC5: Completed tasks without QA/code-review evidence are reported, and `--strict` makes those safety findings fail the command.
- AC6: Pytest includes regression coverage for a clean initialized repo, prompt mirror drift, and strict completion evidence failure.
- AC7: Initialization and packaged agent guidance expose the doctor command where agents need to know about it.
- AC8: Existing initialized repositories have a deterministic non-destructive refresh path through `project init` that updates marked generated assets, updates managed host-file blocks, preserves user-owned guidance, and writes `*.new` on unmarked generated-file collisions.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Decision: Provide both `doctor` and `validate` command names.
  - Why: `doctor` is ergonomic for humans, while `validate` is natural for automation.
- Decision: Make completion evidence findings warnings by default and errors under `--strict`.
  - Why: Existing repositories may have historical complete tasks without QA sections, but AI autonomy should be able to opt into stricter gating.
- Decision: Only enforce prompt/template mirror parity when running in the project-workflow source repository.
  - Why: Initialized downstream repositories are allowed to customize their agent assets.

## Validation Plan

- AC1 -> Run `.venv/bin/python -m project_workflow.cli doctor` and `.venv/bin/python -m project_workflow.cli validate` in initialized temp repos.
- AC2 -> Run `.venv/bin/python .project-workflow/cli/workflow.py doctor --help`.
- AC3 -> Unit test a temporary source-repo-like fixture with prompt drift and assert non-zero output.
- AC4 -> Unit test tracker/doc validation paths and run doctor against this repo.
- AC5 -> Unit test a `Complete` task without QA evidence and assert `--strict` fails.
- AC6 -> Run `.venv/bin/python -m pytest`.
- AC7 -> Verify `project init` emits GitHub Copilot instructions and inspect packaged Codex, Cursor, and prompt assets for doctor guidance.
- AC8 -> Unit test `project init` after replacing marked generated files with stale content, updating managed blocks, and pre-creating an unmarked generated-file collision.
