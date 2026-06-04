## User Story

As a project-workflow maintainer, I want an executable validation harness for workflow state and packaged assets, so that AI agents can verify safety-critical workflow assumptions before continuing autonomous work.

## Acceptance Criteria

- [x] `project doctor` and `project validate` run from the packaged CLI and pass on a freshly initialized repository.
- [x] The local workflow CLI template exposes equivalent `doctor` and `validate` commands.
- [x] Source-repo prompt/template mirror drift is detected.
- [x] Global tracker rows, linked docs, statuses, and epic tracker schemas are validated.
- [x] Completed tasks without QA/code-review evidence are warnings by default and failures with `--strict`.
- [x] Pytest regression coverage exercises clean state, drift detection, and strict completion evidence failure.
- [x] Initialization and packaged agent guidance expose the doctor command where agents need to know about it.
- [x] Existing initialized repositories have a deterministic non-destructive refresh path through `project init` that updates marked generated assets, updates managed host-file blocks, preserves user-owned guidance, and writes `*.new` on unmarked generated-file collisions.

## Validation

- `.venv/bin/python -m pytest` -> 8 passed.
- `.venv/bin/python -m project_workflow.cli doctor` -> passed with warnings for historical completed tasks missing QA evidence.
- `.venv/bin/python -m project_workflow.cli doctor --strict` -> expected failure with 3 blocking issues for historical completed tasks missing QA evidence.
- `.venv/bin/python .project-workflow/cli/workflow.py doctor` -> passed with the same warnings.
- `.venv/bin/python -m project_workflow.cli init --help` -> no `--upgrade` flag exposed.
- `.venv/bin/python .project-workflow/cli/workflow.py doctor --help` -> local doctor help works.
- `.venv/bin/python -c 'from importlib.resources import files; ...'` -> package resources ok.
- Prompt mirror parity check -> no differences.
- Workflow template parity check -> no differences.
- `rg -n "doctor|validate"` over packaged Codex, Cursor, prompts, README, and local CLI docs -> doctor guidance present in the expected assets.
- `project init` regression tests -> marked generated files refresh in place, host managed blocks update in place, user guidance is created/preserved, and unmarked generated collisions write `*.new`.

## Task List

|  ID | Title                          | Description                                                                                 | Acceptance Criteria                                                                                                 | User Verification                                                               | Status      |
| --: | ------------------------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------- |
|   1 | CLI Doctor Command             | Add `doctor` and `validate` commands to the packaged CLI and generated local workflow CLI.   | - Both command names exist.<br>- Commands return zero for valid scaffold state.<br>- `--strict` is available.        | - Run `project doctor --help` and local `workflow.py doctor --help`.             | Complete    |
|   2 | Workflow State Checks          | Validate tracker schemas, statuses, linked docs, source-repo asset mirrors, and QA evidence. | - Invalid tracker/doc state is reported.<br>- Mirror drift is reported in source repo.<br>- Strict mode fails QA gaps. | - Run doctor against this repo and targeted temp fixtures.                       | Complete    |
|   3 | Regression Test Harness        | Add pytest coverage for the validation harness and high-risk failure cases.                  | - Tests cover clean initialized state, prompt mirror drift, and strict completion evidence failure.<br>- Pytest collects and passes. | - Run `.venv/bin/python -m pytest` and confirm tests pass.                       | Complete    |
|   4 | Agent And Init Readiness       | Ensure initialization and packaged agent guidance expose the doctor command where agents need it. | - GitHub Copilot mode installs `copilot-instructions.md`.<br>- Codex AGENTS and key skills mention doctor.<br>- Cursor rule and generated prompt bodies mention doctor. | - Run init regression tests.<br>- Inspect packaged assets with `rg -n "doctor\|validate"`. | Complete    |
|   5 | Non-Destructive Refresh Path   | Make plain `project init` refresh owned workflow assets without taking over user-owned repo files. | - Marked generated files refresh in place.<br>- Host files receive only a managed block.<br>- User guidance is created/preserved.<br>- Unmarked generated collisions write `*.new`. | - Replace marked generated files with stale content, rerun `project init`, then run local `workflow.py doctor --help`.<br>- Pre-create an unmarked prompt and confirm `*.new` is written. | Complete    |

## QA & Code Review

- Date: 2026-06-04
- Reviewed areas: non-destructive `project init` ownership rules, retired project-workflow asset cleanup, generated marker handling, managed host-file blocks, `.new` collision behavior, doctor/validate checks, local workflow template parity, generated prompt/skill guidance, package resources, and regression coverage.
- Verdict: Pass.
- Evidence:
  - `.venv/bin/python -m pytest` -> 8 passed.
  - `.venv/bin/python -m project_workflow.cli doctor` -> passed with known historical warnings for APP-001, APP-002, and APP-003 missing QA/code-review evidence.
  - `.venv/bin/python -m project_workflow.cli validate` -> passed with the same known historical warnings.
  - `.venv/bin/python .project-workflow/cli/workflow.py doctor` -> passed with the same known historical warnings.
  - `.venv/bin/python .project-workflow/cli/workflow.py validate` -> passed with the same known historical warnings.
  - `.venv/bin/python -m project_workflow.cli init --help` -> no `--upgrade` flag exposed.
  - Package resource smoke check -> templates, prompts, and Codex skill resources load.
  - Prompt/template mirror parity check -> no differences for sampled prompt mirrors and workflow template mirror.
  - `git diff --check` -> clean.
- Findings:
  - Found during QA: retired `Scaffold` / `project-scaffold` assets were still handled like potentially reusable customization, and the packaged Codex `project-scaffold` alias still existed. Fixed by removing the packaged alias and making `project init` delete known retired project-workflow paths with regression coverage in `test_init_removes_retired_scaffold_assets`.
  - No remaining blocking findings after the QA fix and validation rerun.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-001
- Title: Executable Workflow Validation Harness
- Created: 2026-06-02
