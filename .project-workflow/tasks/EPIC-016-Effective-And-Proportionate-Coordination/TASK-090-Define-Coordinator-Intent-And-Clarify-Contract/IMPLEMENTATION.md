## User Story

As an owner, I want one Coordinator to understand my outcome and invoke Clarify only for material
uncertainty, so that long work remains coherent without forcing me to operate Project Workflow.

## Parent AC Coverage

- AC1, AC2, AC3, AC15

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

- AC1: owner `Constitution And Operating Model`; required evidence: Constitution diff plus smallest-sufficient positive and counter-example checks.
- AC2: owner `Coordinator Contract And Compatibility`; required evidence: Managed asset parity, compatibility journeys, and single-writer role tests.
- AC3: owner `Requirements Dialogue`; required evidence: Held-out ambiguous and bounded request trials plus approval-burden evidence.
- AC15: owner `Clarify Fitness`; required evidence: Held-out Task/Epic/pre-plan/post-plan/mid-Epic scenarios and smallest evidence-backed disposition.

## Acceptance Criteria

- [x] AC1: Constitution/guidance encode smallest-sufficient coordination without quality reduction.
- [x] AC2: Coordinator is the one owner-facing role and sole shared-state authority.
- [x] AC3: `project-coordinator` is canonical and `project-delegate` is a non-competing compatibility entry.
- [x] AC4: Requirements dialogue asks only material questions and confirms meaning once.
- [x] AC5: Clarify passes the six retained Task/Epic/pre-plan/post-plan/drift scenarios.
- [x] AC6: Source, generated and installed managed assets remain aligned.

## Goal

Ship the Coordinator and Clarify contract foundation required by parent AC1, AC2, AC3 and AC15,
without implementing later durable state, execution routing or release work.

## Approach

Lock failure/counter-failure tests around the current baseline, establish the public role and
compatibility contract, then make the smallest Clarify correction and regenerate managed surfaces.

## Phases

1. Encode the constitutional and canonical Coordinator role.
2. Correct only reproduced Clarify target/mode gaps.
3. Align compatibility assets and run focused proof.

## Validation

- AC1-AC3 / parent AC1-AC2: Constitution, routing, generated assets and single-writer tests.
- AC4 / parent AC3: ambiguous versus clean requirements-dialogue fixtures.
- AC5 / parent AC15: six-scenario Clarify matrix and counter-case results.
- AC6: package/source/generated/installed parity checks.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/effective-proportionate-coordination` | Affected coordination/Coordinator/evaluator set: 29 passed; prior full suite: 467 passed before affected QA corrections | Not integrated or released | `tests/test_coordinator_clarify_contract.py`; `CLARIFY-FITNESS-BASELINE.md`; `EPIC-016-run-005`; exact diff and Doctor |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Lock Coordinator And Clarify Baselines | Add focused tests for one-role semantics, compatibility routing and the retained Clarify failure/counter-failure matrix. | AC2, AC3, AC4, AC5 | Run focused tests against the current baseline and confirm reproduced failures. | Done |  | `tests/`, EPIC-016 child evidence | No | bounded-return |
| 2 | Define Smallest-Sufficient Coordination | Update Constitution, README and core managed guidance with the one-Coordinator role and earned-overhead rule. | AC1, AC2 | Inspect owner-facing docs and role routing. | Done | 1 | `.project-workflow/CONSTITUTION.md`, `README.md`, `AGENTS.md`, package guidance | No | bounded-return |
| 3 | Add Coordinator Compatibility Assets | Add canonical Coordinator skill/prompt assets and route retained Delegate assets to the same contract without a second writer. | AC2, AC3, AC6 | Generate all supported host outputs and inspect compatibility behavior. | Done | 1, 2 | `src/project_workflow/`, `.agents/`, `.github/`, managed templates, focused tests | No | bounded-return |
| 4 | Correct Clarify From Evidence | Support Intent-first Task/Epic targets and three modes while preserving one-question and autonomous in-envelope behavior. | AC4, AC5, AC6 | Run the six-scenario matrix and clean bounded counter-case. | Done | 1, 2 | Clarify skills/prompts, managed routing, focused tests | No | bounded-return |
| 5 | Validate Contract Foundation | Run focused tests, generation/parity, strict Doctor and diff checks; record exact parent evidence and proof boundaries. | AC1, AC2, AC3, AC4, AC5, AC6 | Review focused receipts and confirm later behavioral/package proof remains assigned. | Done | 3, 4 | tests and TASK-090 workflow evidence | No | bounded-return |

## Parent AC Evidence

- AC1, AC2, AC3: implemented in Constitution, managed guidance, canonical Coordinator assets and Delegate compatibility; focused generation/parity tests pass.
- AC15 / child AC4-AC5: the answer-key-free run exposed that the first candidate unnecessarily returned a clear post-plan proxy to the owner. The smallest Coordinator/Clarify correction now restores unchanged approved intent without another owner question and asks only when authority cannot classify a material choice. Both corrected candidate trials passed all six retained Clarify scenarios; static text and deterministic tests are not substituted for those outputs.

## Validation Impact

- Baseline proof: EPIC-016 independent QA Changes Requested 2026-08-24
- Change summary: Corrected the current Coordinator contract and reran preservation-aware current-contract trials.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-016 Coordinator
- Change identity: sha256:aa739d5e4c01c4e96fef20afdd9ff4d1448f4fe7b83ed89fc628c78d0a387d1e

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: Current
- Outcome journey evidence: Fresh-context journey verified; Run 005 evaluates the current contract twice with all 12 routing decisions correct
- Reviewer independence: Read-only local agent `/root/task093_eval_review`; not the implementation owner
- Evidence: `../INDEPENDENT-QA.md`; affected focused tests `21 passed`
- Findings: Run 003 predates the reviewed contract. Run 005 closes that gap; strict residual metadata variance remains recorded without another review.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Run 005 evaluates the corrected Coordinator contract twice; all 12 routing decisions are correct in both trials, and the final 39-test affected set passes.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-090
- Title: Define Coordinator Intent And Clarify Contract
- Created: 2026-08-24
