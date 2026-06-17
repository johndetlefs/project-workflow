## User Story

As a project-workflow maintainer, I want repositories to configure meaningful
task ID prefixes and prefix guidance, so agents can decompose mixed epics into
domain-specific child tasks such as `MCP-006` and `UI-008` without manual
tracker reclassification.

## Acceptance Criteria

- [x] AC1: Default repos without config keep `TASK-###` and `EPIC-###`
  behavior.
- [x] AC2: Repos can configure allowed task prefixes and prefix guidance without
  init overwriting project-owned config.
- [x] AC3: Packaged `task init --prefix <PREFIX>` creates the next ID for that
  namespace.
- [x] AC4: Local helper `task init --prefix <PREFIX>` matches packaged behavior.
- [x] AC5: `epic decompose` reads namespace config by default and can propose
  mixed-prefix child rows in one pass.
- [x] AC6: `epic decompose --prefix <PREFIX>` remains available as a validated
  homogeneous-batch override.
- [x] AC7: Decomposed rows record prefix classification rationale for review.
- [x] AC8: `epic scaffold-child` preserves configured child IDs.
- [x] AC9: `task status` accepts configured task prefixes and keeps lifecycle
  gates.
- [x] AC10: Doctor validates namespace config and reports unconfigured prefixes
  clearly.
- [x] AC11: Generated agent assets document config-driven prefix classification
  and homogeneous `--prefix` overrides.
- [x] AC12: Tests cover packaged/local parity, config-driven mixed
  decomposition, and `gpt-app` style `UI`/`MCP` epic children.

## Validation

- AC1/AC2: `uv run --extra dev pytest tests/test_doctor.py` covered default
  init plus non-destructive custom config preservation across init refresh.
- AC3/AC4: `test_configured_task_prefixes_work_for_packaged_and_local_workflow`
  covered packaged `WF` task creation and local helper `MCP` task creation.
- AC5/AC7: `test_epic_decompose_uses_configured_mixed_prefixes_and_prefix_override`
  covered mixed `MCP` and `UI` child rows with classification notes.
- AC6: The same decomposition regression covered `--prefix MCP` homogeneous
  override allocation.
- AC8: `test_epic_child_scaffold_preserves_configured_task_prefix` scaffolded
  `UI-008` and verified child folder, docs, and tracker path preserved `UI-008`.
- AC9: `test_configured_task_prefixes_work_for_packaged_and_local_workflow`
  moved `WF-001-Workflow-Status` to `Analysing`.
- AC10: `test_doctor_warns_for_unconfigured_task_prefixes` covered non-strict
  warnings and strict failures for unconfigured `WF`.
- AC11: Updated README, generated prompts, Codex guidance, Codex skills, and
  Cursor rules to describe namespace config and mixed-prefix decomposition.
- AC12: `uv run --extra dev pytest tests/test_doctor.py` passed with 35 tests.
  `./.project-workflow/cli/workflow doctor` passed with existing legacy
  warnings. `python -m py_compile src/project_workflow/cli.py` and
  `git diff --check` passed.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Namespace Config & Guidance | Add a user-owned config shape for task/epic prefixes, default prefix, and prefix guidance with safe defaults when config is missing. | AC1, AC2, AC10: Defaults preserve current behavior; config is preserved; invalid or unconfigured prefixes are reported clearly. | Re-run init with custom config and confirm it is not overwritten. | Done |
| 2 | Prefix-Aware Task Creation | Add `--prefix` support to packaged and local `task init`, including per-prefix next-ID allocation and branch naming. | AC3, AC4: Packaged/local task init create matching custom-prefix task docs and tracker rows. | Create `UI-001` and `MCP-001` in temp repos and inspect rows/folders. | Done |
| 3 | Config-Driven Epic Decomposition | Make `epic decompose` read namespace config by default, classify each proposed child against prefix guidance, and write mixed-prefix Proposed rows with rationale. | AC5, AC7, AC12: A gpt-app style epic can produce `MCP-*` and `UI-*` children in one pass with reviewable notes. | Decompose a mixed epic fixture and inspect proposed row IDs and `Notes`. | Done |
| 4 | Homogeneous Prefix Override | Keep `epic decompose --prefix <PREFIX>` as an explicit override for one-domain batches and validate that the prefix is configured. | AC6, AC12: Forced homogeneous decomposition creates only the selected prefix and rejects unconfigured prefixes. | Run `--prefix MCP` and an invalid prefix against temp epics. | Done |
| 5 | Epic Child Scaffolding Preservation | Remove hardcoded reassignment of non-`TASK` child IDs and preserve configured IDs during approve/scaffold. | AC8, AC12: `UI-*` and `MCP-*` epic rows scaffold without being converted to `TASK-*`. | Approve and scaffold `UI-008` and verify folder/docs/tracker paths. | Done |
| 6 | Lifecycle & Doctor Updates | Make `task status` and doctor use configured task prefixes instead of hardcoded `TASK`. | AC9, AC10: Custom-prefix tasks can move through statuses and doctor catches namespace issues. | Move a custom-prefix task through `Analysing`, `In Progress`, and `Testing`. | Done |
| 7 | Agent Guidance & Docs | Update generated prompts, Codex skills, Cursor rules, README, and CLI docs so agents use config guidance for mixed decomposition and `--prefix` only for homogeneous overrides. | AC11, AC12: Agents are told how to classify prefixes and tests prove generated assets refresh. | Search generated assets for namespace guidance and stale hardcoded `TASK` assumptions. | Done |

## QA & Code Review

- Verdict: Pass
- Evidence: `uv run --extra dev pytest tests/test_doctor.py` passed with 35 tests; `./.project-workflow/cli/workflow doctor` passed with existing legacy warnings; `python -m py_compile src/project_workflow/cli.py` passed; `git diff --check` passed.
- Findings: None.

## Retro

- Reusable lessons: Do not treat a scoped workflow task document as implemented until its tracker row, implementation checklist, source, generated template, generated local helper, docs, and tests all agree.
- Conventions or agent assets updated: README, generated prompts, Codex guidance, Codex skills, Cursor rules, packaged CLI, generated workflow template, and repo-local workflow helper now document and support configured task ID namespaces.
- Follow-up tasks: None.

## Notes

- Task: TASK-003
- Title: Configurable ID Namespaces
- Created: 2026-06-10
- 2026-06-10: Created after reviewing the `gpt-app` EPIC-001 flow, where CLI-generated `TASK-*` child rows were manually reclassified to domain prefixes such as `MCP-*` and `UI-*`.
- 2026-06-10: Revised the plan so namespace config drives mixed-prefix epic decomposition by default; `--prefix` is now documented as a homogeneous-batch override rather than the primary flow.
