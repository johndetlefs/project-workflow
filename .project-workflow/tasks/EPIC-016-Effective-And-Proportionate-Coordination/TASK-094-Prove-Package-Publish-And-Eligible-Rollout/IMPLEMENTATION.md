## User Story

As the owner, I want the independently proven coordination feature released and safely adopted, so
that paused projects can use it without confusing local source, publication or context freshness.

## Parent AC Coverage

- AC12, AC13

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

## Acceptance Criteria

- [x] AC1: Exact 0.7.0 candidate passes one complete suite, strict Doctor and package journeys.
- [x] AC2: Dependencies retain one QA each and are not re-reviewed.
- [ ] AC3: PR, merge, tag, release and publication share exact identities.
- [ ] AC4: Public package retrieval and fresh Coordinator journey pass.
- [ ] AC5: Only eligible clean consumer roots upgrade with no-op and preservation proof.
- [ ] AC6: Blocked/stale-context consumers remain unchanged with exact dispositions.
- [ ] AC7: Consolidated release/rollout receipt maps every claim to evidence.

## Goal

Deliver the exact publicly verified 0.7.0 release and safe eligible adoption required by parent
AC12 and AC13 without reopening unchanged QA or overclaiming context refresh.

## Approach

Freeze one candidate after dependencies pass, validate and retain it, integrate/publish the same
identity, verify it publicly, then apply fingerprinted upgrades only after per-root rechecks.

## Phases

1. Freeze and prove the exact candidate from completed child evidence.
2. Integrate, tag, publish and publicly verify the same artifacts.
3. Inventory, safely upgrade and record every consumer disposition.

## Validation

- AC1-AC2 / parent AC12-AC13: dependency, QA, suite, Doctor and exact-package receipts.
- AC3 / parent AC13: PR/checks/main/tag/release/publication identities.
- AC4 / parent AC13: public hash, provenance and fresh-install journey.
- AC5-AC6 / parent AC13: complete inventory and per-root plan/apply/no-op/preservation evidence.
- AC7: consolidated release and rollout receipt.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/effective-proportionate-coordination` at candidate source `80ca56757442984db2fe4e8a6360cea56523bc0b`; PR not yet created | 474/474 complete suite; strict validation; source/release contract; exact wheel/sdist receipt; Codex, Copilot, Claude Code and Cursor fresh/upgrade journeys; legacy preservation/no-op journey | Exact local candidate proven; not yet pushed, merged, tagged or published | `evidence/candidate/`; `../INDEPENDENT-QA.md`; `../../../../evaluations/coordination/results/EPIC-016-ANALYSIS.md` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Freeze Exact 0.7.0 Candidate | Align version/metadata/changelog, verify dependency QA, run focused/full checks once, build and retain exact artifacts. | AC1, AC2 | Inspect candidate receipt, hashes and package journeys. | Done | TASK-090, TASK-091, TASK-092, TASK-093 | release metadata, package source, tests and candidate evidence | No | bounded-return |
| 2 | Integrate Tag And Publish | Commit/push, create and merge reviewed PR, tag exact main commit and publish retained wheel/sdist through trusted infrastructure. | AC3 | Compare PR, merge, tag, release and artifact identities. | To Do | 1 | Git/release metadata and release evidence | No | direct-owner-steering |
| 3 | Verify Public Release | Retrieve public artifacts, verify hashes/provenance/version/assets and run a fresh Coordinator journey. | AC4 | Install exact public 0.7.0 into a disposable repository. | To Do | 2 | disposable verification artifacts and task evidence | No | bounded-return |
| 4 | Inventory And Upgrade Eligible Consumers | Refresh inventory, recheck authority/Git/activity, fingerprint plans, upgrade eligible clean roots and prove no-op/preservation. | AC5, AC6 | Inspect every inventory disposition and consumer diff. | To Do | 3 | eligible consumer managed assets plus rollout evidence | No | coordinator |
| 5 | Consolidate Delivery Receipt | Map every claim to exact code, QA, PR, package, public and per-consumer evidence; run final strict Doctor/diff checks. | AC7 | Review machine-readable and human delivery receipts. | To Do | 1, 2, 3, 4 | release/rollout receipts and Epic evidence | No | bounded-return |

## Parent AC Evidence

- AC12: TASK-090 through TASK-093 remain Complete with the single retained independent QA in
  `../INDEPENDENT-QA.md`; no review was reopened. The candidate keeps the repeated behavioural and
  disposable journey evidence in `../../../../evaluations/coordination/results/EPIC-016-ANALYSIS.md`.
- AC13: Candidate source `80ca56757442984db2fe4e8a6360cea56523bc0b` passed the 474-test
  suite and strict validation. `evidence/candidate/release-receipt.json` binds wheel SHA-256
  `d9c168b53990b6b04f3a2657c52584614be9900dd783e0a539afe3f6f892a961` and sdist SHA-256
  `d9b7a2ded251d4cf76efe0160dd7120b52fa725fc64ad0c4ab66e3ea9074b768`;
  `evidence/candidate/package-journeys.json` proves all four generated-host surfaces, exact source
  parity for 33 wheel resources and 71 sdist sources, the fresh Coordinator outcome journey, and
  the legacy preservation/no-op upgrade journey.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: ____
- Intent adversarial verdict: ____
- Could every AC pass while the approved user job remains undone: ____
- Intent audit state: ____
- Outcome journey evidence: ____
- Reviewer independence: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-094
- Title: Prove Package Publish And Eligible Rollout
- Created: 2026-08-24
- Current owner delivery boundary: publish and publicly verify 0.7.0, then stop. Do not install it
  in any consumer project until the owner separately requests rollout. Rows 4-5 and AC5-AC7 remain
  pending rather than being misreported as complete.
