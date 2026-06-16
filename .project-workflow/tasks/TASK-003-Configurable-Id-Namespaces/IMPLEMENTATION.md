## User Story

As a project-workflow maintainer, I want repositories to configure meaningful
task ID prefixes and prefix guidance, so agents can decompose mixed epics into
domain-specific child tasks such as `MCP-006` and `UI-008` without manual
tracker reclassification.

## Acceptance Criteria

- [ ] AC1: Default repos without config keep `TASK-###` and `EPIC-###`
  behavior.
- [ ] AC2: Repos can configure allowed task prefixes and prefix guidance without
  init overwriting project-owned config.
- [ ] AC3: Packaged `task init --prefix <PREFIX>` creates the next ID for that
  namespace.
- [ ] AC4: Local helper `task init --prefix <PREFIX>` matches packaged behavior.
- [ ] AC5: `epic decompose` reads namespace config by default and can propose
  mixed-prefix child rows in one pass.
- [ ] AC6: `epic decompose --prefix <PREFIX>` remains available as a validated
  homogeneous-batch override.
- [ ] AC7: Decomposed rows record prefix classification rationale for review.
- [ ] AC8: `epic scaffold-child` preserves configured child IDs.
- [ ] AC9: `task status` accepts configured task prefixes and keeps lifecycle
  gates.
- [ ] AC10: Doctor validates namespace config and reports unconfigured prefixes
  clearly.
- [ ] AC11: Generated agent assets document config-driven prefix classification
  and homogeneous `--prefix` overrides.
- [ ] AC12: Tests cover packaged/local parity, config-driven mixed
  decomposition, and `gpt-app` style `UI`/`MCP` epic children.

## Validation

- AC1/AC2: Init and re-init temporary repos with and without namespace config.
- AC3/AC4: Run packaged and local `task init --prefix` smoke tests.
- AC5/AC7: Run mixed-prefix epic decomposition using namespace config and
  inspect proposed row IDs plus `Notes` rationale.
- AC6: Run `epic decompose --prefix MCP` and confirm all proposed rows use
  `MCP`.
- AC8: Run epic approve and scaffold for custom-prefix child rows.
- AC9: Run `task status` transitions against a custom-prefix task.
- AC10: Run doctor against valid, invalid, and legacy-prefix tracker states.
- AC11: Inspect generated prompts, skills, rules, README, and CLI docs.
- AC12: Run `.venv/bin/python -m pytest` and packaged/local doctor checks.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Namespace Config & Guidance | Add a user-owned config shape for task/epic prefixes, default prefix, and prefix guidance with safe defaults when config is missing. | AC1, AC2, AC10: Defaults preserve current behavior; config is preserved; invalid or unconfigured prefixes are reported clearly. | Re-run init with custom config and confirm it is not overwritten. | To Do |
| 2 | Prefix-Aware Task Creation | Add `--prefix` support to packaged and local `task init`, including per-prefix next-ID allocation and branch naming. | AC3, AC4: Packaged/local task init create matching custom-prefix task docs and tracker rows. | Create `UI-001` and `MCP-001` in temp repos and inspect rows/folders. | To Do |
| 3 | Config-Driven Epic Decomposition | Make `epic decompose` read namespace config by default, classify each proposed child against prefix guidance, and write mixed-prefix Proposed rows with rationale. | AC5, AC7, AC12: A gpt-app style epic can produce `MCP-*` and `UI-*` children in one pass with reviewable notes. | Decompose a mixed epic fixture and inspect proposed row IDs and `Notes`. | To Do |
| 4 | Homogeneous Prefix Override | Keep `epic decompose --prefix <PREFIX>` as an explicit override for one-domain batches and validate that the prefix is configured. | AC6, AC12: Forced homogeneous decomposition creates only the selected prefix and rejects unconfigured prefixes. | Run `--prefix MCP` and an invalid prefix against temp epics. | To Do |
| 5 | Epic Child Scaffolding Preservation | Remove hardcoded reassignment of non-`TASK` child IDs and preserve configured IDs during approve/scaffold. | AC8, AC12: `UI-*` and `MCP-*` epic rows scaffold without being converted to `TASK-*`. | Approve and scaffold `UI-008` and verify folder/docs/tracker paths. | To Do |
| 6 | Lifecycle & Doctor Updates | Make `task status` and doctor use configured task prefixes instead of hardcoded `TASK`. | AC9, AC10: Custom-prefix tasks can move through statuses and doctor catches namespace issues. | Move a custom-prefix task through `Analysing`, `In Progress`, and `Testing`. | To Do |
| 7 | Agent Guidance & Docs | Update generated prompts, Codex skills, Cursor rules, README, and CLI docs so agents use config guidance for mixed decomposition and `--prefix` only for homogeneous overrides. | AC11, AC12: Agents are told how to classify prefixes and tests prove generated assets refresh. | Search generated assets for namespace guidance and stale hardcoded `TASK` assumptions. | To Do |

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-003
- Title: Configurable ID Namespaces
- Created: 2026-06-10
- 2026-06-10: Created after reviewing the `gpt-app` EPIC-001 flow, where CLI-generated `TASK-*` child rows were manually reclassified to domain prefixes such as `MCP-*` and `UI-*`.
- 2026-06-10: Revised the plan so namespace config drives mixed-prefix epic decomposition by default; `--prefix` is now documented as a homogeneous-batch override rather than the primary flow.
