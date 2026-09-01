## User Story

As the Project Workflow owner, I want the capability dogfooded and independently challenged, so
that local completion reflects a real fixed candidate rather than green-but-incomplete artifacts.

## Parent AC Coverage

- AC2, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13

## Architecture Impact

- Classification: material
- Reason: This closeout binds the integrated exact candidate to Project Workflow's architecture and proof boundaries.
- Architecture authority: docs/architecture.md
- Authority identity: sha256:f8327a14f96b2765b7e99eb744d218d0e0076cbec66ea3632761cb0a9cbe7737
- Architect invocation: project-architect:codex:01a05b1c-f694-7fc2-8346-0316d5564e83
- Architect decision identity: sha256:5feccb39a86e66697aab7b0638745318ac01c64eb83383acb8837366c0a087e5
- Affected boundaries: whole local EPIC-021 candidate, validation receipts, QA and acceptance claims.
- Architecture decision: Dogfood the same material contract and preserve host/delivery proof layers separately.
- Measurable constraints: Full contributor gates, local/material/violation journeys, generated parity, host receipts and independent QA.
- Conformance plan: Run fixed-candidate full validation and one read-only integrated adversarial review.

## Acceptance Criteria

- [x] AC1: Dogfood covers cheap/local, stale material, conformance and deliberate dependency violations.
- [x] AC2: Generated parity and real Codex invocation pass; Claude blocker remains explicit.
- [x] AC3: Full fixed-candidate contributor/package gates pass.
- [x] AC4: Independent integrated QA passes or all findings are remediated with affected validation.
- [x] AC5: Exact closeout inputs are current and parent acceptance audit/lifecycle remain explicit post-child gates.

## Validation

- AC1: 64 focused tests pass, including real CLI lifecycle journeys and deliberate violations.
- AC2: Generator and init tests plus real Codex receipt pass; Claude executable is unavailable.
- AC3: Documentation, generator, runtime, Ruff, formatting, mypy, 587 tests, build and exact-package journeys pass.
- AC4: Original integrated Changes Requested is preserved; all five findings are resolved by affected validation and the complete campaign.
- AC5: All closeout inputs are current; parent acceptance audit and lifecycle remain the next explicit gates after child completion.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/architecture-control; no PR | 64 focused and 587 full-suite tests, static gates, build and exact-package journeys pass | Local only; no push/merge/release/deploy/adoption | `/tmp/pw-architecture-package-journeys.json`; child canary receipts |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Run integrated dogfood | Exercise cheap, fail-closed, conformance and violation paths. | AC1 | Run focused suite. | Done | | tests | No | bounded-return |
| 2 | Bind host evidence | Preserve generator, Codex and Claude-specific receipts. | AC2 | Inspect receipts. | Done | 1 | child evidence | No | bounded-return |
| 3 | Validate fixed candidate | Run all locked contributor and package gates. | AC3 | Inspect final receipt. | Done | 1, 2 | whole candidate | No | fixed-candidate |
| 4 | Prepare governed closeout | Bind the exact QA, campaign, acceptance and delivery boundaries for the existing closeout gates. | AC4, AC5 | Inspect the bounded closeout contract. | Done | 3 | workflow artifacts | No | independent-review |

## Parent AC Evidence

- AC2/AC6/AC7: Real CLI journeys distinguish cheap local, stale material and conformance Review.
- AC8: Project Workflow dogfoods its module, dependency, ownership and generation constraints.
- AC9: One canonical source and three generated derivatives are parity-checked.
- AC10: Authenticated Codex invocation receipt is retained.
- AC11: Claude has an exact unavailable-executable blocker and no support claim.
- AC12: Integrated proof covers every required dogfood branch.
- AC13: Git evidence is one local branch/worktree only; no consumer was touched.

## Validation Impact

- Baseline proof: integrated-qa:01a05b11-1112-7103-b9f5-f8e763952092
- Change summary: Attached and completed the exact-candidate campaign and resolved every integrated QA finding.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: Coordinator
- Change identity: sha256:47424822835183794b35d21f9a111e0798f4b617b2559d2fa5925e1742022dc7

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Changes Requested
- Could every AC pass while the approved user job remains undone: Yes
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: All four campaign stages pass against `git:3e34317a847f24ff64581c78d246adff93e29e27`; 20 affected and 592 full-suite tests plus exact-package journeys pass.
- Second QA commissioned: No
- Intent audit state: current
- Outcome journey evidence: Exact-candidate campaign, governed Codex receipt, honest Claude blocker, mechanical violations and package journeys.
- Reviewer independence: Ephemeral read-only Codex reviewer `01a05b11-1112-7103-b9f5-f8e763952092` made no mutations.
- Evidence: Parent `QA-INTEGRATED.md`; `VERIFICATION-RECEIPT.md`; parent `COORDINATION.json` receipts.
- Findings: Original Changes Requested is preserved; all five findings are resolved by affected validation without a second QA commission.

## Architecture Conformance

- Authority identity: sha256:f8327a14f96b2765b7e99eb744d218d0e0076cbec66ea3632761cb0a9cbe7737
- Candidate: git:3e34317a847f24ff64581c78d246adff93e29e27
- Mechanical checks: candidate=git:3e34317a847f24ff64581c78d246adff93e29e27; receipt=.project-workflow/tasks/EPIC-021-Proportionate-Architecture-Control/TASK-116-Dogfood-Architecture-Control-And-Closeout/VERIFICATION-RECEIPT.md
- Deviations: Resolved as the approved honest-blocker branch: Claude runtime is unavailable and no parity claim is made.
- Verdict: Pass

## Retro

- Reusable lessons: Pending final QA.
- Conventions or agent assets updated: Pending final QA.
- Follow-up tasks: Claude canary and consumer adoption remain separate future decisions.

## Notes

- Task: TASK-116
- Title: Dogfood Architecture Control And Closeout
- Created: 2026-09-01
