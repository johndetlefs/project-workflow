# Requirements

## Summary

- Task: TASK-094
- Title: Prove Package Publish And Eligible Rollout
- Parent AC Coverage: AC12, AC13
- Last updated: 2026-08-24
- Intent contract: full

## Intent

Prove the exact Project Workflow 0.7.0 candidate, confirm every implementation child already passed
its one required QA without reopening review, merge and publish that reviewed artifact, verify the
public package, and upgrade only eligible clean consumer repositories with truthful dispositions.

## Intent Spine

- OC1 — Completion capability: owners can use the released Coordinator/Clarify/coordination controls
  in eligible consumers from one publicly verifiable exact package.
- OC2 — Material capabilities: coherent 0.7.0 identity, exact suite and package journeys, existing
  child-QA verification, reviewed merge, trusted publication, public verification, complete consumer
  inventory, safe upgrades, no-op confirmation and consolidated receipt.
- OC3 — Success journey: build once, validate once, confirm child proof, merge/tag/publish the same
  artifacts, install publicly in a fresh repository, inventory consumers, upgrade eligible clean
  roots, and leave blocked roots unchanged with reasons.
- OC4 — Successful-but-wrong result: local source passes but a different artifact is published,
  review is recursively reopened, or active/dirty consumers are upgraded to claim adoption.
- OC5 — Exclusions: no forced upgrade, private repository mutation outside inventory authority,
  deployment, commercial-adoption claim, or re-review of completed child implementations.
- OC6 — Assumptions: 0.7.0 is the next approved feature release; trusted publishing and consumer
  access remain available; eligibility is rechecked immediately before each mutation.
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

- The approved owner outcome and material boundaries remain authoritative across every handoff.
- Exactly one logical Coordinator owns shared workflow state and lifecycle decisions.
- A physical task, subagent, persistent task, peer, or worktree is an execution surface, not a second workflow authority.
- Fresh contexts receive bounded authority and sufficient relevant context; they do not receive full history by default and cannot invent scope. A fresh context is optional and must earn its transfer cost; explicit loading of current authority can make the same context fit for purpose.
- Context rotation never discards unresolved decisions, evidence, blockers, owner attention, or source identity.
- Multi-agent execution is optional and must not be selected when coupling or coordination overhead makes one-context execution more effective.
- One independent QA gate remains separate from implementation and Coordinator verification.
- Later changes invalidate only named proof layers through the existing stop gate.
- Requirements rigor, security, source control, evidence, and delivery boundaries are never traded away to improve an efficiency metric.
- Unsupported or unobserved host capability remains `unknown` or `unsupported` and fails closed where it is binding.

### Invalid Substitutes

- An arbitrary token ceiling, shorter answer, smaller model, fewer tests, or reduced proof offered as efficiency.
- More subagents, persistent tasks, or parallel calls offered as efficiency without a named benefit and capability-aware overhead decision.
- Renaming Delegate to Coordinator without changing the intake-to-delivery operating model.
- A coordination document that copies the canonical execution graph, Delegate packets/returns, or worker lifecycle instead of constraining existing lifecycle gates.
- A repository upgrade presented as proof that an already-loaded physical task refreshed its instructions and context.
- Static prompt text, template headings, unit tests, or status fields offered as sole proof that agent behavior improved.
- The Water task's 0.5.0 failure presented as proof that 0.6.0 intent or stop gates failed.
- Raw host internal-token accounting presented as a bill, credit balance, or portable efficiency measure.
- A green implementation that still requires the owner to remember the missing workflow prompts.

### Artifact Targets

- Updated Constitution, AGENTS guidance, README, and host-managed Coordinator assets.
- Coordinator role contract and a tested compatibility path from `project-delegate`.
- Current-contract preflight and stale-task adoption/handoff decision.
- Compact logical coordination state plus enriched existing Delegate packet and verified-return contracts.
- Capability-aware execution-surface decision with explicit benefit and overhead basis.
- Proportionate early real-outcome checkpoint integrated with intent and proof rules.
- Five-boundary drift-decision contract using current intent and amendment authority.
- Evidence-backed Clarify fitness assessment and the smallest correction, if any.
- Status/Doctor projections for deterministic coordination and handoff state.
- Sanitized behavioural scenario corpus and repeated agent-evaluation report.
- Disposable end-to-end journey and EPIC-016 dogfood receipts.
- Exact package candidate, parity receipts, release evidence, and separate rollout disposition.

### Parent AC Proof Ownership

- AC12: owner `Effectiveness Proof`; required evidence: Repeated eval and disposable journey comparison with scoped effort telemetry.
- AC13: owner `Packaging And Delivery`; required evidence: Full suite, parity, exact artifacts, fresh/upgrade journeys, and delivery receipt.

## Goal

Convert the locally proven feature into one exact publicly usable release and safe consumer adoption
without confusing implementation, QA, merge, publication or upgrade evidence.

## Non-Goals

- No publication before every dependency and its one QA verdict pass.
- No new independent QA invocation for unchanged completed children.
- No consumer upgrade when the authority root is dirty, active, ambiguous or lacks a reviewed plan.
- No claim that public availability or installation proves commercial value.
- No deployment of consumer applications.

## Users & Context

- Project Workflow maintainers publishing the next feature release.
- Existing consumers requiring exact safe upgrade and preserved user-owned content.
- Owners resuming paused programmes, including the stale Water task, after verified adoption.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Prepare one coherent 0.7.0 version, changelog, manifest, package metadata and immutable release
  identity covering Coordinator, Clarify, coordination, drift, execution and evaluation assets.
- R2 — Confirm TASK-090 through TASK-093 are Complete with their one required QA and current intent
  audit. Run focused release checks, the complete locked suite once, strict Doctor, build, artifact
  verification and supported exact-wheel fresh/legacy journeys against the exact candidate.
- R3 — Use validation impact for any later release-only correction; rerun only affected layers and
  never commission another broad review without a new authorized material change.
- R4 — Commit and push the reviewed branch, create/review/merge the PR, tag the exact main commit and
  publish the retained wheel/sdist through trusted release infrastructure.
- R5 — Verify public hashes, provenance, package metadata, version output, installed assets and a
  fresh current-contract Coordinator journey from the publicly obtainable package.
- R6 — Refresh the saved-project/consumer inventory, resolve canonical authority roots, recheck Git
  and active-work state, generate fingerprinted upgrade plans and mutate only eligible clean roots.
- R7 — For every inventory entry retain disposition, before/after version and identity, plan/apply/
  no-op result, diff, preserved user-owned content, Doctor state and exact blocker where unchanged.
- R8 — Resume long-running stale tasks only through a compact handoff recommendation; repository
  upgrade does not claim that their already-loaded physical context refreshed.

## Acceptance Criteria (Verifiable)

- AC1: One exact 0.7.0 wheel/sdist and source commit pass focused checks, the complete locked suite
  once, strict Doctor, build verification and all supported exact-package journeys. Covers parent
  AC12 and AC13.
- AC2: Every dependency is Complete with one QA verdict and current parent intent audit; release
  work verifies rather than reopens those reviews. Covers parent AC12.
- AC3: Reviewed PR/checks merge the candidate; the annotated tag, GitHub release and trusted package
  publication identify the same commit and retained artifact hashes. Covers parent AC13.
- AC4: Public retrieval independently matches hashes/provenance and a fresh installation reports
  0.7.0 with the canonical Coordinator and compatibility assets. Covers parent AC13.
- AC5: Every saved-project inventory entry has a disposition; only clean eligible authority roots
  receive fingerprinted plan/apply/no-op upgrades, and user-owned content is preserved. Covers
  parent AC13.
- AC6: Active/dirty/ambiguous/stale-context consumers remain unchanged with exact blockers or
  handoff recommendations; no repository upgrade is called physical-context refresh. Covers parent
  AC13.
- AC7: A consolidated receipt maps parent AC12-AC13 to exact code, tests, QA, PR, commit, tag,
  publication, public verification and per-consumer adoption evidence.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Release version is 0.7.0 because this adds a new canonical Coordinator and coordination contract.
- Existing Delegate entry points remain compatibility assets in this release.
- Owner authority in the parent envelope covers merge, publication and eligible clean rollout.
- Existing child QA is verified, not recursively repeated.

## Validation Plan

- Verify dependency states, intent audit and exact child QA/evidence before candidate construction.
- Run the declared complete test command once, strict Doctor, build and artifact verification.
- Exercise exact wheel/sdist fresh and legacy upgrade journeys across supported hosts.
- Verify PR/checks/main/tag/release/PyPI identities and public fresh installation.
- Inventory and safely upgrade eligible clean consumers with fingerprint/no-op/diff/Doctor receipts.
