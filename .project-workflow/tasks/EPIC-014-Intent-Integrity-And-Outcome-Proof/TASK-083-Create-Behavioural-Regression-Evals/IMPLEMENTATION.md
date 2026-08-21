## User Story

As a maintainer, I want repeated realistic agent evaluations, so that green parser tests cannot be
presented as proof that agents now preserve owner intent.

## Parent AC Coverage

- AC10, AC11, AC12

## Child Charter

### Inherited Invariants

- Approval asks whether the brief Intent accurately reflects what the owner means; IDs, hashes, requirements and ACs bind and elaborate that approval but never substitute for it.
- The owner outcome and material capability commitments remain visible and traceable through every derived artifact; downstream AC precision cannot supersede a contradicted source intent.
- Material capability reduction is a scope change requiring a plain-language amendment or refreshed approval; implementation detail inside the approved intent envelope remains autonomous.
- Semantic judgments are inspectable and independently reviewable; deterministic gates enforce presence, identity, coverage, freshness and provenance without claiming mathematical proof of meaning.
- Requirements approval stays concise and bounded; the workflow must not solve approval failure by transferring artifact-reading labor back to the owner.
- User-outcome proof matches the claim and normal journey. Lower evidence layers remain useful but cannot satisfy higher user-visible claims.
- Owner acceptance remains separate from automated validation and independent QA where practical usability, feel or taste is material.
- Full intent gates are proportional; low-risk bounded fixes retain a lightweight path and over-delivery outside owner intent is a defect, not a virtue.
- Structured workflow state remains repository-native, agent-operated and compatible with existing repositories through explicit warning/adoption/upgrade behavior.
- Public package, documentation and fixtures remain sanitized and independently usable.
- Implementation, integration, publication, release, rollout, adoption and commercial validation remain distinct proof and authority boundaries.

### Invalid Substitutes

- New headings, longer prompts, parser branches or green unit tests presented as proof that agents preserve owner intent in realistic work.
- An approval hash presented as proof that the approved artifact faithfully represents the owner's requested outcome.
- AC coverage that begins only after the original capability has already been narrowed, proxied or omitted.
- The same implementation agent self-certifying that its interpretation preserved intent without an independently reviewable audit and QA verdict.
- A canary, preview, internal data model, debug-only path, related environment, screenshot, build or test suite presented as completion of a broader user-operable outcome.
- One hand-authored regression prompt or one successful model run presented as behavioural reliability across agents, tasks or releases.
- A maximal implementation or speculative completeness presented as fidelity to a bounded owner request.
- Public documentation or fixture text that reproduces private transcripts, absolute personal paths, proprietary project content or maintainer-only context.
- Local source/self-hosted proof presented as packaged release, consumer upgrade, adoption or commercial validation.

### Artifact Targets

- `REQUIREMENTS.md` Intent Spine and concise semantic approval envelope contract.
- Intent commitment coverage and read-only audit artifacts with freshness/provenance.
- CLI readiness, lifecycle, audit, closeout, Doctor and status enforcement.
- `user-outcome-journey` structured evidence recipe and invalid-substitute validation.
- Intent-aware requirements, planner, clarify, implement, QA, Epic and retro skills/prompts across supported generated agent surfaces.
- Sanitized deterministic fixtures plus held-out multi-trial behavioural evaluations and graders.
- Package/self-hosted parity checks, compatibility/upgrade coverage and exact packaged-artifact disposable journey evidence.
- Current owner-facing dogfood receipt and independent Epic QA/acceptance audit.

### Parent AC Proof Ownership

- AC1, AC2, AC10: owner `TASK-080`; required evidence: Template/guidance diffs, readiness and approval fixtures, concise semantic envelope snapshots, and bounded-Fix proportionality proof.
- AC10, AC11, AC12: owner `TASK-083`; required evidence: Sanitized corpus inventory, held-out prompt/trial records, grader definitions, false-pass analysis, under-delivery and anti-gold-plating results.

## Goal

Deliver a sanitized multi-trial behavioural corpus, harness and report that measures both
under-delivery rejection and proportionality.

## Approach

Define cases and graders independently of candidate outputs, validate deterministic scoring,
execute held-out trials with exact identity, then review disagreements before reporting bounded
claims.

## Phases

1. Sanitized corpus and anti-gold-plating counter-case.
2. Harness identity and six-axis grading contract.
3. Multi-trial execution and disagreement analysis.
4. Proportionality and claim-boundary report.

## Acceptance Criteria

- [x] AC1: Bounded work remains proportionate while material work triggers full controls.
- [x] AC2: The sanitized corpus covers all required failure classes without private content.
- [x] AC3: Multiple held-out trials grade all six axes with exact run identity.
- [x] AC4: False-pass/failure analysis and tested-surface limits are explicit.
- [x] AC5: Behavioural and deterministic evidence remain distinct.

## Validation

- AC1 / parent AC10: full-gate and compact-Fix paired trials.
- AC2 / parent AC11: corpus inventory, sanitization audit and expected-verdict tests.
- AC3-AC4 / parent AC12: multi-trial receipts, grader results and disagreement review.
- AC5: report explicitly separates structural tests from agent behaviour.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof` | 416 repository tests pass; strict Doctor and `git diff --check` pass; three CLI copies share SHA-256 `aa7fa487...`; two repeated release trials pass 6/6 cases and all six axes | Local evaluation candidate only; no release authority | `evaluations/intent_integrity/REPORT.md`, exact prompts, corpus/schema/grader, and three raw trial artifacts |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Build Sanitized Corpus | Create five required scenarios plus proportional counter-cases with expected verdicts. | AC2 | Audit fixtures for private/proprietary identifiers and run expected-verdict tests. | Done | TASK-080, TASK-081, TASK-082 | evaluation fixtures and tests | No | bounded-return |
| 2 | Define Behavioural Graders | Grade intent, de-scoping, capability coverage, proof, unnecessary scope and approval burden. | AC3, AC5 | Run deterministic grader contract and adversarial-output tests. | Done | 1 | evaluation harness/graders and tests | No | bounded-return |
| 3 | Execute Held-Out Trials | Run multiple trials with exact prompt/model/harness/evaluator identity and preserve artifacts. | AC3 | Inspect run receipts and rerun determinism boundaries. | Done | 2 | evaluation results and harness | No | bounded-return |
| 4 | Analyze Errors And Proportionality | Review false passes/failures, disagreements, compact-Fix burden and gold-plating. | AC1, AC4 | Independently inspect sampled results and bounded counter-case. | Done | 3 | evaluation report and receipts | No | bounded-return |
| 5 | Validate Behavioural Claim | Run deterministic/full suites and write the tested-surface-limited result. | AC1, AC2, AC3, AC4, AC5 | Compare behavioural receipts with structural checks without conflation. | Done | 4 | tests and child evidence | No | bounded-return |

## Parent AC Evidence

- AC10: Trial 2 and trial 3 route five material cases through full controls and the bounded label
  correction through compact controls with zero additional approval requests.
- AC11: `evaluations/intent_integrity/cases.json` contains six sanitized, distinct cases and the
  deterministic sanitization test rejects private identifiers and paths.
- AC12: `evaluations/intent_integrity/REPORT.md` records exact model, CLI, prompt, harness,
  evaluator and raw-result identities, all six grading axes, calibration disagreements and claim
  boundaries. Behavioural receipts remain separate from deterministic tests.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: Behavioural evidence is `evaluations/intent_integrity/REPORT.md` and
  its raw trial artifacts; this child makes no broader user-runtime or release claim.
- Reviewer independence: The deterministic evaluator is separate from model outputs, and raw
  outputs were manually sampled for grader disagreements. Independent Epic QA remains pending.
- Evidence: 416 repository tests, strict Doctor, `git diff --check`, exact CLI mirror parity, and
  three preserved trials, with trial 1 retained as calibration disagreement and trials 2-3 passing
  every case and axis.
- Findings: The first prompt left `unnecessary_scope` semantically ambiguous and the first lexical
  expectations produced two false failures. Both are documented; no final false passes were found.
  The adversarial corpus intentionally contains candidates whose internal checklists can pass while
  their user jobs remain undone; TASK-083 itself does not pass unless the corpus, repeated trials,
  raw evidence, disagreement analysis and tested-surface limits are all present.

## Retro

- Reusable lessons: Preserve calibration failures. A grader that rewards only a preferred output
  vocabulary can manufacture confidence just as easily as a shallow implementation can.
- Conventions or agent assets updated: Behavioural corpus, exact prompts, structured output schema,
  six-axis evaluator, deterministic evaluator tests and bounded claim report are repository-owned.
- Follow-up tasks: TASK-084 must prove packaged parity and real disposable journeys; these local
  model trials do not satisfy that boundary.

## Notes

- Task: TASK-083
- Title: Create Behavioural Regression Evals
- Created: 2026-08-21
