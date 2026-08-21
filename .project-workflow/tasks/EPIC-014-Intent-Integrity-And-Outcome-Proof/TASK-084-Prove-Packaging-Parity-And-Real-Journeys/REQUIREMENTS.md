# Requirements

## Summary

- Task: TASK-084
- Title: Prove Packaging Parity And Real Journeys
- Parent AC Coverage: AC13, AC14, AC15
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Prove that the exact packaged Project Workflow preserves owner Intent from intake through
closeout in realistic use, including rejection of a deliberately green-but-wrong result. Keep
implementation proof separate from publication, rollout and adoption authority.

## Intent Spine

- OC1 — Completion capability: Maintainers can install the exact candidate and demonstrate a
  complete meaning-first journey that rejects proxy completion.
- OC2 — Material capabilities: Package/generated/self-hosted parity, safe legacy upgrade,
  disposable journey, current dogfood receipt and independent Epic QA are verified.
- OC3 — Success journey: A realistic request produces brief approved Intent, traced children,
  audited execution, exact outcome proof and correct rejection/closeout decisions.
- OC4 — Successful-but-wrong result: Local source tests pass while the packaged artifact or actual
  owner journey omits intent controls, accepts a proxy or breaks historical repositories.
- OC5 — Exclusions: Do not publish, tag, release, roll out, upgrade consumers or claim the problem
  is universally solved without separate authority and exact release evidence.
- OC6 — Assumptions: Package identity and fresh disposable/current dogfood evidence own candidate
  claims; source/self-hosted success alone is insufficient.
- OC7 — Authority source: Parent Epic Intent, OC1-OC7 and approved parent AC13-AC15.

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

- AC13, AC14, AC15: owner `TASK-084`; required evidence: Generated/self-hosted/package parity, safe upgrade results, disposable exact-package journey, current dogfood receipt, strict Doctor/full suite, and independent Epic QA.

## Goal

Align all shipped/managed surfaces and prove the exact candidate through compatibility,
disposable end-to-end and current owner-facing dogfood journeys before independent Epic review.

## Non-Goals

- Do not publish a package, create a release/tag, merge, deploy or roll out consumer upgrades.
- Do not present source-only or self-hosted-only checks as packaged evidence.
- Do not replace independent QA or owner acceptance with automated tests.

## Users & Context

- Maintainers deciding whether the candidate is genuinely releasable.
- Existing repositories that must remain safe through adoption/upgrade.
- Owners using Project Workflow on current consequential work.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Keep CLI source, packaged templates/prompts/skills, generated host assets, installed
  self-hosted helper, documentation and fixtures in verified parity.
- R2 — Provide reviewable safe upgrade behavior for pre-intent repositories without invalidating
  completed historical work or silently applying new gates retroactively.
- R3 — Build/install the exact candidate into a disposable realistic repository and exercise
  intake, Intent approval, planning, decomposition, audit, implementation proof, QA and closeout.
- R4 — Include a deliberately internally green but Intent-wrong candidate and prove the workflow
  rejects it with the lost capability named.
- R5 — Run one current owner-facing dogfood journey and record practical burden, false friction and
  proof boundaries.
- R6 — Obtain independent QA/code review over code, behavioural evidence, parity and journeys.

## Acceptance Criteria (Verifiable)

- AC1: Package source, generated host assets, installed self-hosted helpers and documentation pass
  parity checks; a reviewable upgrade plan preserves existing completed work. Covers parent AC13.
- AC2: A fresh exact-package disposable repository completes the normal journey and rejects the
  deliberate green-but-wrong candidate with a sourced Intent consequence. Covers parent AC14.
- AC3: A current dogfood journey demonstrates concise approval, practical execution and
  intent-aware closeout without private data entering public fixtures. Covers parent AC14.
- AC4: Independent QA verifies code, deterministic tests, behavioural trials, package identity and
  both journeys, with findings resolved or explicitly blocking. Covers parent AC15.
- AC5: All reports state that publication, release, rollout and consumer adoption remain
  unauthorized and unproven. Covers parent AC15.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- The exact built/installed candidate owns final proof, not the source checkout alone.
- Historical work remains valid; new controls apply through safe current-contract adoption.
- The current EPIC-014 journey is the primary dogfood case, with sanitized public evidence only.

## Validation Plan

- Run mirror/parity checks, build artifacts and inspect package contents.
- Exercise canonical init and safe upgrade/no-op paths in disposable repositories.
- Run the complete exact-package journey including deliberate proxy rejection.
- Inspect EPIC-014 itself as the current dogfood journey and record burden/limitations.
- Run the full locked suite, canonical UVX packaging test, strict Doctor and diff checks.
- Perform independent QA separately; stop at publication/release/rollout boundaries.
