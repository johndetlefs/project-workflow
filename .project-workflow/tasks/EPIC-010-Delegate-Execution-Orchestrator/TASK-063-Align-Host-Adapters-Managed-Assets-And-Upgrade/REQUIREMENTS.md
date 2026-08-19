# Requirements

## Summary

- Task: TASK-063
- Title: Align Host Adapters, Managed Assets, And Upgrade
- Parent AC Coverage: AC6, AC7, AC9, AC13, AC15, AC16, AC20
- Last updated: 2026-08-19

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

- One delegation run targets exactly one approved Epic or Task.
- Delegate executes existing authority; it does not create scope, approve requirements, or add unplanned children/work items.
- Coordinated standalone Tasks require an Epic; arbitrary Task batches are rejected.
- Epic child Tasks and Task implementation rows remain distinct execution units with distinct executor choices.
- Persistent Codex task creation requires explicit owner authority and verified host support.
- The coordinator is the single writer of shared workflow state and target lifecycle.
- Workers operate inside explicit write/repository scopes and never gain push, merge, release, deployment, external-contact, or cross-repository authority from delegation.
- Dependencies are satisfied by coordinator-verified results, not worker assertion alone.
- Concurrency never exceeds available host capacity and unsafe file overlap is never parallelized.
- A failed unit blocks its descendants; unrelated work continues only while the shared baseline remains valid.
- Canonical workflow artifacts remain the durable authority; machine-local execution handles remain ignored and contain no credentials or private transcripts.
- Task `Testing`, child completion, Epic closeout, and final completion remain gated by existing implementation, evidence, QA, audit, deferral, retro, and owner-authority rules.
- Unsupported host behavior fails closed or degrades explicitly; the system never fabricates support or parity.
- Existing non-delegated behavior remains backward compatible.

### Invalid Substitutes

- A prompt or skill that says work was delegated without observed worker launches, dependency behavior, monitoring, and returned evidence.
- Repository fixtures or mocked scheduler tests presented as proof of current Codex task, worktree, subagent, interruption, or resume behavior.
- A worker's completion claim without coordinator inspection of scope, changes, validation, and required evidence.
- A Task moved to `Testing` while required implementation rows remain incomplete.
- Multiple workers editing shared trackers, implementation-plan status, acceptance maps, evidence indexes, or lifecycle state.
- A fixed configured worker count presented as proof that host capacity was respected.
- Committed task IDs, agent IDs, cursors, leases, credentials, private transcripts, or other machine-local runtime state.
- Generated/source asset parity presented as proof that every supported host can perform persistent or parallel orchestration.
- Unit tests, builds, Doctor, QA prose, or related environments substituted for `external-contract-alignment` or `runtime-target-source` evidence.
- Delegate's own aggregate report substituted for independent QA, Epic acceptance audit, owner-only acceptance, integration, release, deployment, adoption, or effectiveness.

### Artifact Targets

- Host-neutral delegation graph, validation, state-transition, reconciliation, and reporting implementation under `src/project_workflow/` with mirrored helper behavior where required.
- A `project delegate` CLI family with read-only planning/status and controlled runtime-state operations, including schema-versioned JSON.
- Updated Task planning and Epic decomposition metadata for dependencies, Task-row write scope, and parallel safety with backward-compatible migration/upgrade behavior.
- Ignored machine-local delegation runtime state with no competing tracked lifecycle authority.
- Updated Codex `project-delegate` skill, other host Delegate prompts/agents, Planner, Implement, Epic, QA, AGENTS guidance, README, packaged resources, and generated/source mirrors.
- Focused deterministic tests, complete regression coverage, strict Doctor, build/package checks, and upgrade plan/apply/rollback evidence.
- Retained disposable Task-mode and Epic-mode runtime journey artifacts tied to the exact source revision, installed package, host, target repository/worktree, and observation method.

### Parent AC Proof Ownership

- AC6: owner `Epic Orchestration child`; required evidence: Current-host external-contract evidence and live task/worktree creation proving capability and explicit-authority gates.
- AC7: owner `Task and Epic Orchestration children`; required evidence: Captured work packets and enforcement tests for identity, ACs, dependencies, scope, validation, evidence, forbidden actions, and stop conditions.
- AC9: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Capacity-resolution tests and observed host run showing effective concurrency never exceeds available capacity.
- AC13: owner `Delegation Graph and Host Alignment children`; required evidence: Git/package privacy inspection proving host handles and private runtime data are ignored while canonical evidence remains reviewable.
- AC15: owner `Host Alignment child`; required evidence: Capability-matrix tests and unvalidated-host scenarios proving fail-closed or explicit sequential fallback with truthful claims.
- AC16: owner `Host Alignment child`; required evidence: Generated/source mirror checks, init/upgrade plan/apply/rollback tests, fresh install inspection, and package asset parity.
- AC20: owner `Host Alignment and End-To-End Proof children`; required evidence: README/AGENTS/skill/prompt/install inspection plus positive and negative invocation examples verified against implemented behavior.

## Goal

Ship one truthful Delegate contract across Codex, GitHub Copilot, Claude Code, and Cursor, with thin capability-aware adapters, aligned generated/install/upgrade assets, privacy protection, and no claims beyond capabilities observed on each host.

## Non-Goals

- Do not claim cross-host native orchestration parity from shared text or package delivery.
- Do not emulate unverified persistent tasks, worktrees, monitoring, or resume behavior.
- Do not bypass user-owned managed-asset collision handling or upgrade fingerprints/rollback.
- Do not place host IDs, leases, cursors, credentials, or transcripts in tracked/generated/package assets.

## Users & Context

Project Workflow consumers invoke Delegate through different host surfaces. Codex currently exposes observed bounded subagents and persistent task/worktree tools, while other hosts have not been live-verified; installed guidance must therefore discover capabilities, fall back safely, and tell the truth about what actually ran.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Define a tri-state capability contract (`verified`, `unsupported`, `unknown`) with provenance for subagents, persistent tasks, isolated worktrees, monitoring, resume reconciliation, and capacity.
- Authorise native launch only from runtime-observed verified capability; unknown never means supported.
- Report requested/effective executor, effective concurrency, provenance, and downgrade/block reason; provide explicit sequential/coordinator fallback only when contract invariants remain satisfiable.
- Replace Task-only, fixed-four, blanket-fail-fast Delegate guidance with the approved Epic/Task modes, capacity bounds, dependency authority, descendant-aware failure, single-writer, QA, and delivery boundaries.
- Remove Copilot-specific `${input:...}` syntax from generated Claude/Cursor agents and supply host-appropriate invocation contracts.
- Align Codex source/installed skill, common prompts, Planner/Epic/Implement/QA guidance, managed AGENTS/rules blocks, README, development mirrors, and packaged resources.
- Add `.project-workflow/.gitignore` runtime protection and upgrade/schema/asset-version handling with collision-safe plan/apply/no-op/rollback behavior.
- Make Doctor, release-contract checks, and exact-wheel journeys verify Delegate semantic assets and privacy without implying native support.

## Acceptance Criteria (Verifiable)

- AC1: Codex native intents require explicit authority plus dated runtime-observed verified capabilities; other verified/unsupported/unknown matrices launch or fall back exactly as specified and never overstate support. Covers parent AC6, AC9, AC15.
- AC2: Every host adapter delivers the same bounded packet, single-writer, dependency, failure, privacy, QA, and forbidden-delivery contract using host-valid syntax. Covers parent AC7 and AC20.
- AC3: Runtime handles are ignored and absent from tracked, generated, wheel/sdist, Smoke Bomb, and retained public evidence artifacts. Covers parent AC13.
- AC4: Init and canonical upgrade for all four hosts install/refresh the correct Delegate assets, remove literal cross-host Copilot placeholders, preserve user-owned collisions through `.new`, and retain fingerprint/no-op/rollback guarantees. Covers parent AC16.
- AC5: Codex source/installed skill, common/development prompts, managed guidance, standalone helper mirrors, templates, and packaged resources pass explicit semantic parity checks. Covers parent AC16 and AC20.
- AC6: README and installed guidance contain verified positive/negative examples distinguishing Epic, Task, row, Codex task, subagent, Implement, Delegate, QA, and closeout responsibilities. Covers parent AC20.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Capabilities are tri-state with provenance; only `runtime-observed` plus `verified` authorises native launch.
- Unknown Task-mode worker capability falls back to explicit sequential/coordinator execution when safe; unknown Epic persistent capability creates no task and otherwise coordinates sequentially or blocks.
- Codex guidance inspects callable current-session tools and available capacity instead of hard-coding support or four workers.
- GitHub Copilot, Claude Code, and Cursor ship truthful fail-closed/sequential defaults until native behavior is separately observed.
- Managed asset version is incremented with this contract; repository schema version changes only if TASK-060 metadata/runtime migration requires it.
- A user-owned active Delegate asset left beside a generated `.new` file is reported pending, not current.

## Validation Plan

- Add capability-matrix and exact adapter output tests, including absence of literal `${input:` in Claude/Cursor output.
- Parameterise init and exact-wheel journeys across all four host modes; inspect Delegate semantics but claim native execution only where live observed.
- Add Codex skill/prompt semantic parity, managed-block, Doctor, release-contract, package inventory, privacy, user-collision `.new`, upgrade plan/apply/no-op/rollback, and helper mirror tests.
- Verify README/installed positive and negative examples against implemented behavior, then run the full locked suite, strict Doctor, compilation, build/package, and independent QA.
