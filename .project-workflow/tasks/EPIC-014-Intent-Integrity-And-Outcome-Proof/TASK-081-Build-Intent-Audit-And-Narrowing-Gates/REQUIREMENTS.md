# Requirements

## Summary

- Task: TASK-081
- Title: Build Intent Audit And Narrowing Gates
- Parent AC Coverage: AC3, AC4, AC5, AC6
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Make Project Workflow expose and block when derived work narrows, omits or replaces the approved
Intent with an easier proxy. Let ordinary technical refinement proceed, but require a plain
amendment when a material capability is lost.

## Intent Spine

- OC1 — Completion capability: A reviewer can see how every approved outcome commitment survives
  into child scope and can block a material reduction before implementation or completion.
- OC2 — Material capabilities: Commitment coverage, audit classifications, source locations,
  user-visible consequences, freshness, amendments and lifecycle enforcement are reviewable.
- OC3 — Success journey: The narrowed-authoring fixture turns full authoring into preview plus one
  control and is rejected with the exact lost capability despite internally green artifacts.
- OC4 — Successful-but-wrong result: Requirements, AC mappings, tests and evidence all pass after
  the original outcome was silently reduced upstream.
- OC5 — Exclusions: Do not claim deterministic semantic certainty or require approval for routine
  implementation detail that preserves all material capabilities.
- OC6 — Assumptions: Semantic classification remains reviewable while identity, coverage,
  freshness, provenance and lifecycle state are deterministic.
- OC7 — Authority source: Parent Epic Intent, OC1, OC3-OC5 and approved parent AC3-AC6.

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

- AC3, AC4, AC5, AC6: owner `TASK-081`; required evidence: Cross-artifact coverage/audit fixtures, narrowed-authoring failure, amendment/freshness lifecycle results, Doctor/status output, and independent review.

## Goal

Add traceability, reviewable intent-audit results and fail-closed material-narrowing gates across
requirements, decomposition, child plans and lifecycle transitions.

## Non-Goals

- Do not implement the initial Intent/approval contract owned by TASK-080.
- Do not implement the outcome evidence recipe or independent QA verdict owned by TASK-082.
- Do not treat every wording change or implementation choice as material scope drift.

## Users & Context

- Owners whose intended outcome can otherwise disappear before implementation begins.
- Planners/coordinators translating parent outcomes into child work.
- Reviewers who need sourced explanations rather than a confidence score.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Add a validated commitment coverage map linking each triggered `OC<n>` to parent ACs,
  child owners, disposition and required outcome proof.
- R2 — Add a read-only audit with `preserved`, `narrowed`, `proxy`, `omitted`, `broadened`,
  `amended` and `deferred` classifications plus source locations and user-visible consequences.
- R3 — Define material reductions by capability consequence, including full-to-canary,
  authoring-to-preview, operable-to-hidden, all-to-subset and normal-to-debug-only changes.
- R4 — Block readiness, Review and Complete for material reduction without a current approved
  amendment or refreshed approval identifying the lost capability.
- R5 — Surface audit state and next action through Doctor/status while retaining explicit
  `unknown` or `review-required` semantics.
- R6 — Preserve compatibility for historical work that predates the Intent contract.

## Acceptance Criteria (Verifiable)

- AC1: A coverage map links every triggered outcome commitment to parent AC, child owner,
  disposition and proof; unmapped material commitments block readiness. Covers parent AC3.
- AC2: A read-only audit emits all required classifications with source locations and user-visible
  consequences without mutating requirements or presenting confidence as truth. Covers parent AC4.
- AC3: The sanitized narrowed-authoring fixture is classified as narrowed/proxy and blocked even
  when downstream ACs, tests, evidence and hashes are internally consistent. Covers parent AC5.
- AC4: Readiness, Review and Complete block unapproved material reductions while routine
  in-envelope implementation changes proceed without owner approval fatigue. Covers parent AC6.
- AC5: Doctor/status report current, stale, unknown and review-required audit states with a sourced
  next action and retain legacy compatibility. Covers parent AC3-AC6.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- The audit is read-only and judgment-bearing; deterministic gates enforce traceability and state.
- Capability consequence, not word-diff size, determines whether a change is material.
- Unknown semantic state cannot authorize lifecycle movement that requires intent fidelity.

## Validation Plan

- Unit-test commitment parsing, logical wrapped bullets, mapping, freshness and classifications.
- Exercise each material-reduction archetype plus preserved and broadened counter-cases.
- Reproduce the sanitized narrowed-authoring failure with internally green downstream artifacts.
- Test readiness/Review/Complete, amendment, deferral, Doctor/status and legacy paths.
- Run focused and full suites, helper parity, strict Doctor and `git diff --check`.
