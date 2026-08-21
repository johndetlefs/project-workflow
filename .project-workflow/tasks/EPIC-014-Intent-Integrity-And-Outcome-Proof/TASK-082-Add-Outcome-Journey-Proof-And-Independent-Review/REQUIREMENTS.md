# Requirements

## Summary

- Task: TASK-082
- Title: Add Outcome Journey Proof And Independent Review
- Parent AC Coverage: AC7, AC8, AC9
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Make completion evidence prove the actual user outcome through its normal journey, and make
independent QA reject work that satisfies derived criteria while failing the approved Intent.
Keep owner-only acceptance distinct wherever practical usability, feel or taste remains material.

## Intent Spine

- OC1 — Completion capability: A user-visible outcome cannot be certified without evidence from
  the exact normal journey and an independent intent-level verdict.
- OC2 — Material capabilities: Structured journey identity, invalid substitutes, QA adversarial
  review and distinct implementation/outcome/acceptance/delivery states are enforced.
- OC3 — Success journey: The exact actor enters through the normal path, performs material
  operations, observes the requested result, and independent QA confirms the Intent is fulfilled.
- OC4 — Successful-but-wrong result: Tests, builds, screenshots, internal data or a debug canary
  satisfy every derived AC while the normal user still cannot accomplish the requested job.
- OC5 — Exclusions: Automated evidence and QA do not manufacture owner acceptance, deployment,
  release, adoption or product feel.
- OC6 — Assumptions: Proof strength must match the claim and exact artifact/environment identity.
- OC7 — Authority source: Parent Epic Intent, OC2-OC5 and approved parent AC7-AC9.

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

Add a built-in outcome-journey proof recipe, intent-adversarial QA verdict and lifecycle state
separation that prevents lower evidence layers from laundering broader completion claims.

## Non-Goals

- Do not implement source Intent capture or narrowing classification.
- Do not claim automated proof replaces owner acceptance for judgment-dependent outcomes.
- Do not deploy, publish or validate live service adoption.

## Users & Context

- Owners evaluating whether delivered work actually performs the requested job.
- Implementers recording claim-matched evidence.
- Independent QA reviewers challenging green but outcome-wrong candidates.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Add `user-outcome-journey` with actor, normal entry point, starting state, material
  operations, result/artifact, observations, source/revision, environment and invalid substitutes.
- R2 — Validate claim/artifact freshness and reject tests, builds, screenshots, internal data,
  debug-only controls, related environments and canaries as sole proof of a broader user job.
- R3 — Require independent QA to review both AC evidence and preserved Intent and answer whether
  every AC could pass while the requested job remains undone.
- R4 — Require Changes requested whenever QA identifies that green-but-wrong possibility in the
  actual candidate.
- R5 — Distinguish implemented, outcome-proven, ready for owner acceptance, owner accepted,
  integrated, released and deployed states across status, audit and closeout.

## Acceptance Criteria (Verifiable)

- AC1: `user-outcome-journey` validates all required journey and artifact-identity fields and
  rejects declared invalid substitutes. Covers parent AC7.
- AC2: Normal-journey and proxy fixtures prove that lower evidence layers cannot satisfy a broader
  end-user outcome by themselves. Covers parent AC7.
- AC3: Independent QA guidance/artifacts contain an explicit intent-level adversarial verdict and
  block a candidate where all derived ACs pass but the job remains undone. Covers parent AC8.
- AC4: Lifecycle/status/audit/closeout expose outcome proof and owner acceptance separately from
  implementation and delivery states. Covers parent AC9.
- AC5: Existing built-in proof recipes and historical evidence retain compatibility.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- The normal user journey, not the cheapest observable proxy, owns user-outcome proof.
- QA is independent and adversarial; owner acceptance remains a separate authority boundary.
- Lifecycle labels state what has actually been proven rather than implying the next layer.

## Validation Plan

- Extend structured evidence schemas, fixtures and validation for the new recipe.
- Test exact artifact/source/environment freshness and every invalid substitute.
- Add QA pass/changes-requested fixtures where AC-level results are identical but Intent differs.
- Test lifecycle/status/audit/closeout state combinations and legacy recipes.
- Run focused/full suites, helper parity, strict Doctor and `git diff --check`.
