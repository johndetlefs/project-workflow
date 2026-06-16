# Requirements

## Summary

- Task: TASK-003
- Title: Configurable ID Namespaces
- Last updated: 2026-06-10

## Goal

Allow each repository to define useful task ID namespaces such as `UI`, `MCP`,
`DEV`, or `WF`, and let epic decomposition use that repo-owned namespace config
to propose mixed-prefix child work without forcing everything through
`TASK-###`.

## Non-Goals

- Replacing the Markdown tracker format.
- Silently guessing domain prefixes without repo-owned config guidance or a
  recorded classification reason.
- Migrating existing tracker rows automatically.
- Changing the default behavior for repositories that do not define ID
  namespaces.
- Implementing a full issue-management taxonomy beyond ID prefixes and
  lightweight classification guidance.

## Users & Context

- AI agents and maintainers need IDs that make work type clear in mixed projects.
- The `gpt-app` project already uses prefixes such as `UI`, `MCP`, `DEV`, and
  `WF` to distinguish frontend, MCP/tooling, development, and workflow work.
- Current epic decomposition generates `TASK-###` rows, which caused `gpt-app`
  child tasks to be manually reclassified from `TASK-*` to `MCP-*` or `UI-*`.
- A single `epic decompose --prefix MCP` flow is useful for homogeneous batches
  but does not match mixed epics where some children are MCP, some are UI, and
  some may be DEV or WF.
- The generated local helper currently has logic that can convert non-`TASK`
  epic child IDs back to `TASK-*`, which fights project-owned namespace choices.

## Requirements (Outcome-Focused)

- A repository can declare allowed task prefixes, default task prefix, and
  prefix guidance in a user-owned, non-destructive project-workflow config file.
- Missing config preserves the current default behavior: task IDs use `TASK` and
  epic IDs use `EPIC`.
- Config can describe how to classify work into prefixes, for example:
  - `UI`: frontend, widget, component, route, layout, visual, interaction, and
    UX work.
  - `MCP`: MCP server, app tool, payload contract, fixture, orchestration, and
    ChatGPT Apps SDK integration work.
  - `DEV`: local development, debug tooling, tunnels, build/dev scripts, and
    handoff utilities.
  - `WF`: project workflow conventions, process automation, prompts, and agent
    guidance.
- `project task init` and the generated local helper can create tasks with an
  explicit configured prefix, allocating the next number for that prefix.
- `project epic decompose` reads namespace config by default and can propose
  mixed-prefix child rows in one decomposition pass.
- `project epic decompose --prefix <PREFIX>` remains available as an explicit
  override for intentionally homogeneous batches.
- Epic child proposal rows include enough classification rationale in `Notes`
  for a maintainer or agent to review and correct the chosen prefix before
  approval/scaffolding.
- Epic child scaffolding preserves configured child IDs such as `UI-008` and
  `MCP-008` instead of reassigning them to `TASK-*`.
- `task status` accepts any configured task prefix and preserves its completion
  gate and transition validation.
- `doctor` validates configured namespace usage and reports unconfigured
  prefixes clearly without breaking legacy repositories by default.
- Generated prompts, Codex skills, Cursor rules, README, and local CLI docs
  explain that agents should read namespace config, classify child work against
  prefix guidance, and only use `--prefix` when forcing a homogeneous batch.
- Tests cover default compatibility, custom prefix allocation, config-driven
  mixed epic decomposition, prefix override behavior, epic child prefix
  preservation, status transitions for custom prefixes, and init refresh.

## Acceptance Criteria (Verifiable)

- AC1: A new initialized repo with no custom config still creates `TASK-001` and
  `EPIC-001` using existing commands.
- AC2: A repo can configure task prefixes such as `TASK`, `UI`, `MCP`, `DEV`,
  and `WF`, plus prefix guidance, without project-workflow overwriting that
  config on init refresh.
- AC3: `project task init --prefix UI --title "..." --update-tracker` creates
  the next `UI-###` row, task folder, docs, and branch name when branch creation
  is requested.
- AC4: `./.project-workflow/cli/workflow task init --prefix MCP ...` behaves the
  same as the packaged CLI.
- AC5: `project epic decompose --epic-id EPIC-001` reads namespace config and
  can create mixed proposed child rows such as `MCP-006`, `MCP-007`, and
  `UI-008` from one epic decomposition pass.
- AC6: `project epic decompose --epic-id EPIC-001 --prefix MCP` forces a
  homogeneous `MCP-###` decomposition batch and validates that `MCP` is
  configured.
- AC7: Decomposed epic rows include prefix classification rationale in `Notes`
  so agents and maintainers can review or correct IDs before approval.
- AC8: `project epic scaffold-child --id UI-###` preserves the `UI-###` ID when
  creating child docs and updating the epic tracker.
- AC9: `project task status --id UI-### --to Testing` accepts configured task
  prefixes and keeps the same transition, force, docs-path, and completion
  checks.
- AC10: `project doctor` warns about unconfigured prefixes and invalid namespace
  config, while preserving non-strict compatibility for existing legacy rows.
- AC11: Generated agent assets tell agents to classify work using namespace
  config guidance and to reserve `--prefix` for explicit homogeneous overrides.
- AC12: Tests cover packaged CLI behavior, local helper parity, generated asset
  refresh, config-driven mixed decomposition, and the `gpt-app` style `UI`/`MCP`
  epic child use case.

## Open Questions (Answer Needed)

- Q1: Should the config file be JSON or TOML?
  - Recommendation: use JSON for the first pass because the package supports
    Python 3.10+ and JSON is stdlib-only. TOML would require a dependency or a
    Python-version split.
- Q2: Should prefix numbers be global across all prefixes or per prefix?
  - Recommendation: allocate per prefix. `UI-008` and `MCP-008` should both be
    valid when each namespace has its own sequence.
- Q3: Should `epic decompose` require `--prefix`?
  - Recommendation: no. The normal mixed-epic path should read namespace config
    automatically and classify each child row. `--prefix` should be an override
    for homogeneous batches only.
- Q4: How should ambiguous prefix classification be handled?
  - Recommendation: Proposed rows should include classification rationale in
    `Notes`; low-confidence or fallback classifications should be obvious for
    review before approval/scaffolding. Do not silently select a non-default
    custom prefix without a recorded reason.
- Q5: Should unconfigured historical prefixes fail doctor?
  - Recommendation: warn in default doctor and fail only under `--strict`, so
    existing repos can adopt config incrementally.

## Decisions (Resolved)

- Decision: Namespace validity comes from config.
  - Why: Prefix taxonomy is project-specific and should not be hardcoded in the
    package.
- Decision: Epic decomposition should read namespace config by default.
  - Why: Mixed epics are normal in projects like `gpt-app`; requiring a single
    `--prefix` would push users back into manual reclassification.
- Decision: Prefix classification must be explainable.
  - Why: Agents can classify work, but maintainers need an audit trail before
    child rows are approved and scaffolded.
- Decision: Missing config must preserve current behavior.
  - Why: This keeps `project init` safe for existing users.
- Decision: Config must be user-owned and non-destructive.
  - Why: Prefix taxonomy is project-specific and should survive package upgrades.

## Validation Plan

- AC1/AC2: Run init in temporary repositories with and without config, then
  rerun init to confirm config preservation.
- AC3/AC4: Run packaged and local `task init --prefix` commands and inspect
  tracker rows, docs paths, and folder names.
- AC5/AC7: Run `epic decompose` against a configured mixed-prefix repo and
  verify proposed rows receive `MCP` and `UI` IDs with rationale in `Notes`.
- AC6: Run `epic decompose --prefix MCP` and verify all child rows use `MCP`.
- AC8: Approve and scaffold a custom-prefix epic child and verify the child ID
  remains unchanged.
- AC9: Move a custom-prefix task through lifecycle states with `task status`.
- AC10: Run doctor against valid config, invalid config, configured prefixes,
  and unconfigured legacy prefixes.
- AC11: Search generated prompts, skills, rules, and docs for namespace config
  and mixed-prefix decomposition guidance.
- AC12: Add regression coverage for a `gpt-app` style `MCP`/`UI` epic child
  scenario.
