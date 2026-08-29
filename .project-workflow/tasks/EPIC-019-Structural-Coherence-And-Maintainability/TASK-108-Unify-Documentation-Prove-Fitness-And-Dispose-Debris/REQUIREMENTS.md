# Requirements

## Summary

- Task: TASK-108
- Title: Unify Documentation Prove Fitness And Dispose Debris
- Parent AC Coverage: AC8, AC9, AC10, AC11, AC12, AC13
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Give people and coding agents one current documentation hierarchy, remove only repository material
proved unnecessary, and demonstrate through exact-candidate journeys plus independent QA that the
result is structurally coherent and still functionally fit for purpose.

## Intent Spine

- OC1 — Completion capability: A new maintainer can identify product intent, operating rules,
  architecture, contribution/validation, release, generated assets, and historical records without
  encountering competing current instructions.
- OC2 — Material capabilities: Concise README, small docs hierarchy, authority map, version/link
  checks, cleanup disposition ledger, exact wheel/local-helper proof, independent QA, and local-only
  delivery record.
- OC3 — Success journey: Follow current docs to change one module, regenerate, validate, build,
  install into a disposable repo, use the dependency-free helper, and reach truthful status/Doctor
  results from the exact candidate.
- OC4 — Successful-but-wrong result: Documentation is merely rearranged, stale guidance remains,
  historical proof or unique work is deleted, retained debris lacks rationale, unit tests substitute
  for exact runtime journeys, or local validation is called released/adopted.
- OC5 — Exclusions: No public merge/release/rollout, historical approval reconstruction, Claude
  runtime certification, Constitution rewrite without conflict, or deletion based on appearance.
- OC6 — Assumptions: TASK-107 supplies a frozen candidate and real quality gates; external GitHub
  or PyPI mutation is not required to prove local package and standalone behaviour.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
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

- `project = project_workflow.cli:main` remains the public package entry point.
- Initialized repositories retain `.project-workflow/cli/workflow` plus a dependency-free Python runtime and current copied adapter paths.
- Public commands, flags, exit semantics, JSON schemas, manifest/asset/repository schema versions, generated paths, and supported agent modes remain compatible with v0.9.0 unless separately approved as a product change.
- Canonical authored modules have one-way dependencies and no circular imports; the CLI imports domain interfaces and domains do not import the CLI.
- The standalone workflow runtime is deterministic generated output with provenance and is never a second authored implementation.
- User-owned workflow records, accepted historical debt, active EPIC-016/EPIC-018 state, and the TASK-102 Claude canary blocker are preserved truthfully.
- One cleanup programme does not become a product redesign, multi-package architecture, arbitrary coverage campaign, public release, or consumer rollout.

### Invalid Substitutes

- Smaller files without cohesive ownership, acyclic dependency direction, or a thin entry facade.
- Moving the current monolith unchanged behind one import or distributing it across arbitrary helper files while preserving global coupling.
- Editing `templates/workflow.py`, `.project-workflow/cli/workflow.py`, generated prompts, or installed skills as if they were canonical authored sources.
- Passing unit tests without exact built-package, generated-bundle, dependency-free local-helper, current/legacy upgrade, and command/schema compatibility evidence.
- Treating configured but unlocked/unexecuted lint or type tools as quality gates.
- Rewriting historical approvals/evidence, deleting unique work, or deleting retained candidate artifacts without preserving the claims that depend on them.
- Rewriting the Constitution with implementation detail instead of fixing code/document structure.
- Calling local validation merged, released, adopted, owner-accepted, or authenticated Claude Code runtime certification.

### Artifact Targets

- `docs/architecture.md`: module/dependency map, source/generated ownership, bundle design, and module-splitting rules.
- A small canonical module set under `src/project_workflow/` with `cli.py` as entry and compatibility facade.
- Deterministic bundle-generation tooling plus generated `src/project_workflow/templates/workflow.py` and source-repository installed mirror parity.
- Shared adapter foundation where host semantics are identical, with explicit Codex/Claude modules.
- Product-boundary tests, shared fixtures, command/schema snapshots, architecture checks, and exact candidate journeys.
- Locked Ruff/mypy development dependencies and enforced CI checks.
- Concise README and a small contributor/maintenance/release documentation hierarchy with tested current identity and generated-surface ownership.
- A cleanup disposition ledger for empty directories, ignored output, worktrees/branches, prototypes, binary evidence, generated copies, and historical workflow records.

### Parent AC Proof Ownership

- AC8: owner `Unify Documentation Prove Fitness And Dispose Debris`; required evidence: Documentation authority map, link/version checks, and semantic review.
- AC9: owner `Unify Documentation Prove Fitness And Dispose Debris`; required evidence: Evidence-led disposition ledger and Git/worktree/artifact uniqueness checks.
- AC10: owner `Rebuild Test And Quality Infrastructure; final proof child`; required evidence: Complete locked suite, strict Doctor, build inspection, and package journeys.
- AC11: owner `Architecture; both extraction children; final proof child`; required evidence: v0.9.0 versus candidate command/schema/path snapshots and representative journey comparison.
- AC12: owner `Unify Documentation Prove Fitness And Dispose Debris`; required evidence: Independent structural and functional QA verdict with findings disposition.
- AC13: owner `Unify Documentation Prove Fitness And Dispose Debris`; required evidence: Delivery-state record explicitly stopping at local validated source.

## Goal

Finish the cleanup as an understandable maintained repository, not just a refactored codebase, and
answer fit-for-purpose from exact post-change evidence.

## Non-Goals

- Publishing or rolling out the candidate.
- Deleting audit history or evidence to reduce file count.
- Rewriting stable product principles with implementation detail.
- Claiming owner acceptance on the owner's behalf.

## Users & Context

Users and coding agents currently face an 896-line README, a release runbook frozen at 0.6.0,
inconsistent authored/generated markers, historical records mixed with current guidance, and local
worktree/prototype/build debris that requires evidence-led disposition.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Define a tested documentation authority hierarchy: Constitution for stable outcomes, AGENTS and
  local guidance for operating rules, README for orientation/quick start, focused docs for
  architecture/maintenance/release, packaged prompts/skills as authored assets, installed host
  surfaces as generated derivatives, and workflow task folders as history/state rather than
  instruction.
- Make release guidance version-neutral or derived from the authoritative package version and remove
  every contradictory current version, role, lifecycle, proof, and generated-ownership instruction.
- Inventory empty directories, ignored caches/build output, worktrees, branches, prototype commits,
  tracked candidate binaries, generated mirrors, workflow history, accepted Doctor debt, and active
  blocked work with remove/retain/disposition evidence.
- Remove local ignored debris and fully superseded worktrees/branches only after exact cleanliness,
  merge, uniqueness, active-task, and evidence checks. Preserve unique work or evidence until its
  durable disposition is proved.
- Run exact frozen wheel/sdist inspection and disposable fresh-init, current-upgrade, legacy-upgrade,
  no-op, status, Doctor, representative lifecycle, and no-installed-package helper journeys.
- Conduct one independent adversarial QA review focused on cohesion, source authority,
  compatibility, necessity, and fit for purpose; resolve findings with affected validation only.

## Acceptance Criteria (Verifiable)

- AC1: README and focused docs expose one linked authority hierarchy; automated checks find no stale
  current version, broken local link, conflicting role/lifecycle/proof rule, or ambiguous
  authored/generated instruction.
- AC2: The Constitution is unchanged unless a documented product-level conflict requires an approved
  amendment; implementation architecture stays in contributor documentation.
- AC3: Every cleanup candidate has a remove/retain/disposition row with evidence. Deleted worktrees,
  branches, directories, or artifacts have no unique work or required evidence; retained history,
  binaries, accepted warnings, and blockers have a concrete reason.
- AC4: One exact candidate wheel/sdist passes full inventory inspection and disposable init/upgrade/
  no-op/status/Doctor/lifecycle/package journeys; the installed local helper also works with package
  imports blocked and records runtime target/source.
- AC5: Command/schema/path snapshots match v0.9.0 and all locked quality/tests/build gates pass from
  the same source identity.
- AC6: Independent QA passes cohesion, model clarity, compatibility, cleanup necessity, and
  functional fit-for-purpose with every finding resolved or explicitly blocking.
- AC7: Delivery evidence states local validated source only and explicitly excludes merge, release,
  publication, rollout, owner acceptance, and authenticated Claude certification.

## Open Questions (Answer Needed)

- None. Destructive cleanup blocks on missing uniqueness evidence rather than asking the owner to
  guess whether an artifact is safe to delete.

## Decisions (Resolved)

- Keep the Constitution unchanged unless review proves a stable product conflict; current principles
  already require a coherent core and warn about copied-helper sprawl.
- Retain historical workflow records and accepted warnings as auditable history; distinguish them
  from current instruction in the authority map.
- Retain tracked binary evidence unless each dependent claim has an equally durable replacement.
- Remove fully merged/superseded local worktrees and local ignored build/cache output only after
  read-only proof. Do not push or delete remote branches.

## Validation Plan

- Run documentation version/link/authority/semantic checks.
- Produce and independently inspect the cleanup disposition ledger before removal.
- Run locked static/tests/build/package gates and exact wheel/local-helper journeys.
- Run intent audit, strict Doctor, acceptance audit, diff hygiene, and one independent adversarial QA
  pass; rerun affected checks after any QA remediation.
