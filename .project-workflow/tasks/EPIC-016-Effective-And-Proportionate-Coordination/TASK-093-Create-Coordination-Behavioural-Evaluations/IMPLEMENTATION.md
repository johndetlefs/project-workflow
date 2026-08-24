## User Story

As a maintainer, I want repeated behavioral evidence for coordination decisions, so that Project
Workflow is released because it improves real delivery rather than because its prompts look right.

## Parent AC Coverage

- AC11, AC12, AC14, AC15

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

- AC11: owner `Behavioural Scenario Coverage`; required evidence: Sanitized nine-scenario corpus with under- and over-processing verdicts.
- AC12: owner `Effectiveness Proof`; required evidence: Repeated eval and disposable journey comparison with scoped effort telemetry.
- AC14: owner `Five-Boundary Drift Control`; required evidence: Water-style narrowing/proxy/broadening injections, branch blocking, and exact amendment refresh.
- AC15: owner `Clarify Fitness`; required evidence: Held-out Task/Epic/pre-plan/post-plan/mid-Epic scenarios and smallest evidence-backed disposition.

## Acceptance Criteria

- [x] AC1: Sanitized corpus covers all failure and counter-failure classes.
- [x] AC2: Repeated held-out trials retain complete model/harness/candidate/grader provenance.
- [x] AC3: Water drift is blocked at all five boundaries with named capability consequences.
- [x] AC4: Clarify passes six modes without redundant owner or review loops.
- [x] AC5: Executor/context topology accepts only evidenced sufficient surfaces.
- [x] AC6: Passed-proof behavior stops without recursive QA.
- [x] AC7: Candidate comparison preserves outcome/proof and reports scoped effectiveness honestly.

## Goal

Provide the behavioural and effectiveness proof required by parent AC11, AC12, AC14 and AC15 before
the exact package is built or released.

## Approach

Generalize retained real failures into sanitized scenarios, run paired baseline/candidate trials,
grade outcome and process together, and investigate false verdicts without moving the goalposts.

## Phases

1. Build sanitized coordination and Clarify corpus plus counter-cases.
2. Run repeated baseline/candidate trials and objective grading.
3. Independently inspect failures and publish scoped findings.

## Validation

- AC1 / parent AC11: corpus inventory and privacy scan.
- AC2, AC7 / parent AC12: repeated trial records, comparison and telemetry boundary.
- AC3 / parent AC14: five-boundary Water-style results.
- AC4 / parent AC15: six-scenario Clarify results.
- AC5-AC6 / parent AC11-AC12: topology and stop counter-failure results.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/effective-proportionate-coordination` | Affected coordination/Coordinator/evaluator set: 29 passed; prior full suite: 467 passed before affected QA corrections; current-contract `gpt-5.4` Run 005 retained | Not integrated or released | `EPIC-016-run-001` invalid-run evidence; `EPIC-016-run-002` answer-key-free baseline; `EPIC-016-run-004` strict pre-correction; `EPIC-016-run-005` current candidate; `EPIC-016-ANALYSIS.md`; `PROVENANCE-REDACTION.md`; `DOGFOOD-RECEIPT.md` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Build Sanitized Scenario Corpus | Add coordination, drift, Clarify, topology, checkpoint and stop cases plus bounded counter-cases. | AC1, AC3, AC4, AC5, AC6 | Inspect corpus inventory and privacy scan. | Done | TASK-090, TASK-091, TASK-092 | `evaluations/`, sanitized fixtures and schema tests | No | bounded-return |
| 2 | Define Outcome And Process Graders | Grade intent, capability, drift timing, topology, packet/return, owner burden, duplicate actions, proof and stopping with provenance. | AC2, AC7 | Review grader schema and anti-gaming counter-cases. | Done | 1 | evaluation graders/schemas/tests | No | bounded-return |
| 3 | Run Baseline And Candidate Trials | Execute repeated held-out trials with exact model/harness/candidate/trial identity. | AC2, AC3, AC4, AC5, AC6, AC7 | Inspect aggregate and per-trial retained outputs. | Done | 1, 2 | evaluation outputs and child evidence | No | bounded-return |
| 4 | Record False-Verdict Dispositions | Analyze failures at the Coordinator layer, correct the earliest owner, and reserve independent sample challenge for the one QA gate. | AC2, AC7 | Review false-pass/failure dispositions and validation-impact decisions. | Done | 3 | evaluation report, affected source/tests | No | bounded-return |
| 5 | Record Effectiveness Boundary | Publish sanitized report and scoped telemetry limits, then run strict Doctor and diff hygiene. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Confirm no universal reliability, billing or token-savings claim. | Done | 3, 4 | evaluation report and child workflow evidence | No | bounded-return |

## Parent AC Evidence

- AC11/AC14 deterministic structure: the sanitized corpus covers 12 under- and over-processing scenarios; all five Water-style boundaries, topology counter-cases and no-recursive-QA stop behavior pass locally.
- AC12/AC15 behavioural evidence: run 001 is retained but invalid because the prompt leaked the grader answer key. The corrected answer-key-free baseline scored 10/12 and 11/12. Its failures exposed the Epic-parent Clarify and stale-loaded-context gaps. The pre-correction candidate also scored 10/12 and 11/12 and exposed a real unnecessary-owner-question defect for clear post-plan proxy drift. After the smallest owning contract correction, affected candidate trials scored 12/12 and 11/12, both passed all six Clarify scenarios, and the only residual variance kept owner-only gameplay feel blocked but counted zero literal owner questions. `EPIC-016-ANALYSIS.md` retains exact hashes, baseline-reuse checks, raw scoped usage and the non-universal claim boundary. `PROVENANCE-REDACTION.md` retains the before/after collection identities for the bounded absolute-path removal; a regression prevents future personal or ephemeral path retention.
- Post-QA evidence: Run 005 evaluates the current corrected contract twice with the strict preservation-aware grader. All 12 routing decisions pass in both trials; strict metadata/process scores are 10/12 and 9/12, with every deduction retained and dispositioned rather than tuned away. The stale physical context now blocks as `contract-load-required` without forcing an unearned new context.
- Independent sample challenge is assigned to this child’s single QA gate. The earlier attempts to create a pre-QA reviewer were excluded because they duplicated that gate; no reviewer verdict is inferred from them.
- EPIC-016 dogfood and `FRESH-CONTEXT-JOURNEY.md` prove current contract loading, architectural subtraction, automatic lifecycle gating and one bounded physical-context transfer. They do not substitute for consolidated independent QA.

## Validation Impact

- Baseline proof: EPIC-016 independent QA Changes Requested 2026-08-24
- Change summary: Added non-leaking preservation grading and completed two current-contract candidate trials.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-016 Coordinator
- Change identity: sha256:c35468bb5c7bb13091a2f3e534bb7f10d44da8db7cac73be878b0c44736903e4

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: Current
- Outcome journey evidence: Run 005 evaluates the current contract twice; all 12 routing decisions pass in both trials
- Reviewer independence: Read-only local agent `/root/task093_eval_review`; not the implementation owner
- Evidence: `../INDEPENDENT-QA.md`; stricter grader and counter-failure tests in `tests/test_coordination_evaluations.py`
- Findings: The old grader ignored `must_preserve`, and Run 003 used an older contract. Both are corrected and affected validation is retained; strict Run 005 deductions remain explicit non-universal variance.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Preservation counter-failures pass and Run 005 evaluates the corrected behavioral contract twice with every routing decision correct; the later deterministic completion-gate delta passes its targeted lifecycle regression.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-093
- Title: Create Coordination Behavioural Evaluations
- Created: 2026-08-24
