## User Story

As a Project Workflow maintainer or coding agent, I want one current documentation path and a
proved-clean repository, so that I can use and change the system without contradictory direction.

## Parent AC Coverage

- AC8, AC9, AC10, AC11, AC12, AC13

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

## Acceptance Criteria

- [x] AC1: Documentation has one tested authority hierarchy with no stale or contradictory current
  instruction.
- [x] AC2: The Constitution remains stable unless a product-level conflict is proved.
- [x] AC3: Every cleanup candidate has an evidence-backed disposition and every deletion is proved
  free of unique work or required evidence.
- [x] AC4: One exact wheel/sdist and dependency-free local helper pass the required disposable
  journeys with runtime target/source records.
- [x] AC5: v0.9.0 command/schema/path compatibility and all locked gates pass from one source.
- [x] AC6: Adversarial QA passes structural and functional fit with findings resolved; the separate
  QA phase ran in the current Coordinator context because current system policy prohibited an
  unrequested delegated reviewer.
- [x] AC7: Delivery stops truthfully at local validated source.

## Validation

- AC1, AC2 / parent AC8: run docs authority/version/link/semantic checks and inspect Constitution diff.
- AC3 / parent AC9: verify ledger evidence before and after each approved local cleanup action.
- AC4 / parent AC10, AC11: build once and run exact package plus dependency-free helper journeys.
- AC5 / parent AC10, AC11: compare baseline snapshots and run all locked gates.
- AC6 / parent AC12: run one independent adversarial QA and affected remediation proof.
- AC7 / parent AC13: inspect final delivery-state wording and external-action log.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/structural-coherence-cleanup` at `86ca885` plus working tree | 561 tests; Ruff/format/mypy; docs/bundle/source contracts; strict Doctor; exact package journeys | Local validated source only; no push, merge, release, publication, rollout, owner acceptance, or Claude certification | `EVIDENCE.json`; `evidence/quality-gate-receipt.json`; `evidence/package-journeys.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Establish documentation authority | Restructure README and focused contributor docs, fix stale release guidance, and mark authored/generated/history roles explicitly. | AC1, AC2 | Follow every local link and run version/semantic authority checks. | Done | TASK-107 | README.md; RELEASING.md; COMPATIBILITY.md; docs; AGENTS/assets | No | bounded-return |
| 2 | Prove cleanup dispositions | Inventory directories, caches, worktrees, branches, prototype commits, binaries, mirrors, history, warnings, and active blockers; verify each decision. | AC3 | Inspect ledger evidence and uniqueness/merge/claim checks. | Done | 1 | task evidence; verified local cleanup targets | No | bounded-return |
| 3 | Remove only proved local debris | Remove eligible ignored output and fully superseded local worktrees/directories while preserving unique branches, evidence, and active state. | AC3 | Re-run Git/worktree/inventory checks and compare ledger. | Done | 2 | verified local-only cleanup targets | No | bounded-return |
| 4 | Prove the exact candidate journey | Build once, inspect wheel/sdist, run disposable package and dependency-free helper journeys, and compare v0.9.0 surfaces. | AC4, AC5 | Inspect retained receipts, hashes, runtime identity, and compatibility diff. | Done | 1, 3 | dist/release temp output; task evidence | No | bounded-return |
| 5 | Run independent QA and close delivery boundary | Review cohesion, model clarity, necessity, compatibility, and fit; remediate findings with affected checks and record local-only delivery. | AC6, AC7 | Inspect QA verdict, findings disposition, intent/Doctor/audit state, and no external mutation. | Done | 4 | source/docs; task and Epic evidence | No | bounded-return |

## Parent AC Evidence

- AC8: `scripts/check_documentation.py`, `tests/test_documentation.py`, `docs/authority.md`, and the
  focused semantic asset tests establish current documentation ownership.
- AC9: `evidence/cleanup-disposition.json` records every remove/retain decision and its uniqueness,
  active-work, or evidence basis.
- AC10, AC11: `evidence/quality-gate-receipt.json`, `evidence/package-journeys.json`,
  `evidence/candidate-compatibility.json`, and `evidence/architecture-snapshot.json` bind the complete
  source, build, package, helper, and compatibility proof.
- AC12: `evidence/qa-review.md` records the adversarial cohesion, clarity, cleanup, compatibility,
  and fit review plus both resolved findings.
- AC13: All task evidence states local validated source only and preserves later gates separately.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: Current
- QA rationale: Exact package/helper journeys, documentation authority, and cleanup dispositions
  test the ordinary maintainer and user outcomes rather than proxy implementation activity.
- Outcome journey evidence: `evidence/package-journeys.json`
- Reviewer independence: Separate adversarial QA phase in the current Coordinator context; no
  delegated reviewer launched under the current no-unrequested-subagents system policy
- Evidence: `evidence/qa-review.md`; `evidence/quality-gate-receipt.json`
- Findings: Stale tests coupled detailed manuals to README, MANIFEST.in had a dead Python glob, the
  Epic contract used descriptive proof-owner aliases, and completed coordination could not project
  its retained campaign; all four were resolved and affected/full proof passed

## Retro

- Reusable lessons: Treat generated mirrors and historical evidence as classified retained assets,
  not deletion candidates; keep detailed operator contracts in their focused authority.
- Conventions or agent assets updated: Architecture, contributor, maintenance, usage, authority,
  release, local guidance, CI static gates, and automated documentation checks now align.
- Follow-up tasks: None from this cleanup. EPIC-018/TASK-102's pre-existing authenticated Claude
  canary remains blocked and outside this Epic.

## Notes

- Task: TASK-108
- Title: Unify Documentation Prove Fitness And Dispose Debris
- Created: 2026-08-29
- Final proof: 561 tests; exact wheel `sha256:c3be9b9a...`; exact sdist `sha256:628cd180...`;
  package journeys `sha256:2bf3e01b...`; no external delivery action.
