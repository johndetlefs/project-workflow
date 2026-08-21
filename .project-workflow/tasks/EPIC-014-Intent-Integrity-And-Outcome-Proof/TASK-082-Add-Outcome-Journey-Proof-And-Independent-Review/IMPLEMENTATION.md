## User Story

As an owner, I want proof and independent QA to exercise the exact user outcome I requested, so
that related tests or a narrow canary cannot be certified as completion.

## Parent AC Coverage

- AC7, AC8, AC9

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

- AC7, AC8, AC9: owner `TASK-082`; required evidence: Structured recipe validation, normal-journey and invalid-substitute fixtures, intent-aware independent QA verdicts, and lifecycle-state proof.

## Goal

Implement claim-matched user-outcome evidence, intent-adversarial independent review and honest
lifecycle-state separation after the Intent audit foundation exists.

## Approach

Extend the structured evidence model with a normal-journey recipe, integrate its validation into
gated states, then update QA and status/closeout projections to preserve each proof boundary.

## Phases

1. Outcome-journey schema and invalid substitutes.
2. Lifecycle recipe enforcement and freshness.
3. Intent-aware independent QA verdict.
4. State projection and compatibility validation.

## Acceptance Criteria

- [x] AC1: The outcome-journey recipe validates exact claim-matched fields.
- [x] AC2: Proxy evidence cannot satisfy the normal user job.
- [x] AC3: Independent QA issues an intent-level adversarial verdict.
- [x] AC4: Outcome proof, owner acceptance and delivery states remain separate.
- [x] AC5: Existing proof recipes and historical evidence remain compatible.

## Validation

- AC1-AC2 / parent AC7: recipe schema, freshness, normal-journey and invalid-substitute matrix.
- AC3 / parent AC8: QA pass/fail fixtures with identical AC evidence and divergent Intent outcomes.
- AC4 / parent AC9: lifecycle/status/audit/closeout state matrix.
- AC5: existing recipe and historical compatibility suite.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof` | Focused journey/intent tests and the full regression suite pass; strict Doctor, parity, py_compile and diff checks pass | Local implementation candidate only; no release authority or manufactured owner acceptance | `EVIDENCE.json`, `evidence/outcome-journey-receipt.md`, `tests/test_user_outcome_journey.py` and status/lifecycle receipts |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define Outcome Journey Recipe | Add actor, entry, state, operations, result, observation, source and environment fields. | AC1 | Run valid/missing/stale schema fixtures. | Done | TASK-080, TASK-081 | evidence schema, CLI mirrors and tests | No | bounded-return |
| 2 | Reject Proxy Evidence | Encode invalid substitutes and claim/artifact identity checks. | AC2 | Run build/screenshot/internal/debug/canary/related-target failures. | Done | 1 | evidence validation and tests | No | bounded-return |
| 3 | Make QA Intent-Adversarial | Require QA to compare AC evidence with preserved Intent and issue the green-but-wrong verdict. | AC3 | Run paired QA fixtures with identical AC results. | Done | 2 | QA skills/prompts, CLI gates and tests | No | bounded-return |
| 4 | Separate Proof States | Project implementation, outcome proof, owner acceptance and delivery as distinct states. | AC4 | Run status/audit/closeout state matrix. | Done | 2, 3 | lifecycle/status/audit code and tests | No | bounded-return |
| 5 | Validate Recipe Compatibility | Run existing recipe, focused/full, parity, strict Doctor and diff checks. | AC1, AC2, AC3, AC4, AC5 | Review receipts and remaining owner-acceptance boundary. | Done | 4 | tests and child evidence | No | bounded-return |

## Parent AC Evidence

- AC7: `user-outcome-journey` requires claim/journey scope identity, actor, normal entry point,
  starting state, material operations, result, observations, source/revision, artifact identity,
  environment, explicit invalid-substitute policy and fresh evidence artifact. `CLM-082-AC7`
  records the current self-hosted journey; proxy fixtures reject scope mismatch, debug entry and
  substitute-only evidence.
- AC8: Current implementation templates, QA skill/prompt and completion gates require an
  adversarial Intent verdict. A reviewer must answer whether every AC could pass while the approved
  job remains undone; Yes or unknown requires Changes requested. `CLM-082-AC8` and paired tests
  exercise the divergent verdict with otherwise green evidence.
- AC9: Operational status projects `outcome_proof_state` and `owner_acceptance_state` separately
  from implementation proof and delivery. Required but not-yet-given acceptance projects
  `ready-for-owner-acceptance` and blocks Complete until an actual accepted record exists;
  `CLM-082-AC9` preserves that boundary.

## QA & Code Review

- Intent QA contract: adversarial
- Date: 2026-08-21
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: `CLM-082-AC7`, `CLM-082-AC8`, `CLM-082-AC9` and
  `evidence/outcome-journey-receipt.md` exercise the normal self-hosted CLI journey, proxy
  rejection, adversarial verdict and owner-acceptance boundary.
- Reviewer independence: Fresh QA phase re-read requirements, source, tests, structured evidence
  and generated assets after implementation; it did not treat implementation assertions or green
  AC checks as sufficient and does not claim owner acceptance.
- Evidence: Focused recipe/adversarial/state tests and the full suite pass; existing recipe tests
  remain green; strict Doctor, CLI byte parity, py_compile and diff validation pass.
- Findings: Review caught that the generic missing-value helper treated the legitimate
  `owner_acceptance_status: pending` state as absent. The recipe-specific validation now preserves
  pending as an explicit state without allowing it to satisfy owner acceptance. No unresolved
  blocking findings remain.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-082
- Title: Add Outcome Journey Proof And Independent Review
- Created: 2026-08-21
