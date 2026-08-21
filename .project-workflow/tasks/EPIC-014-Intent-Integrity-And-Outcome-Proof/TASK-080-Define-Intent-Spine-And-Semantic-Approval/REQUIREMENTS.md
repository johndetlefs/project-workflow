# Requirements

## Summary

- Task: TASK-080
- Title: Define Intent Spine And Semantic Approval
- Parent AC Coverage: AC1, AC2, AC10
- Last updated: 2026-08-21
- Intent contract: full

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

- AC1, AC2, AC10: owner `TASK-080`; required evidence: Template/guidance diffs, readiness and approval fixtures, concise semantic envelope snapshots, and bounded-Fix proportionality proof.
- AC10, AC11, AC12: owner `TASK-083`; required evidence: Sanitized corpus inventory, held-out prompt/trial records, grader definitions, false-pass analysis, under-delivery and anti-gold-plating results.

## Intent

Make Project Workflow begin substantial work with a brief statement of what the owner actually
wants, and make that meaning—not IDs or document ceremony—the thing the owner confirms. Preserve
that intent as the authority for later requirements while keeping genuinely small work light.

## Intent Spine

- OC1 — Completion capability: Owners see and confirm a brief statement of the outcome they
  actually want before detailed requirements become implementation authority.
- OC2 — Material capabilities: Current work receives stable outcome commitments, meaning-first
  approval, bounded structural validation and a proportionate compact Fix path.
- OC3 — Success journey: An agent drafts substantive Intent, the workflow renders its approval
  synopsis, the owner confirms the meaning, and provenance is recorded behind that confirmation.
- OC4 — Successful-but-wrong result: The owner is asked to approve task, AC or hash identifiers
  while no concise statement of their actual intent is visible.
- OC5 — Exclusions: This child does not implement cross-artifact semantic audits, outcome-journey
  evidence, behavioural reliability claims, publication or rollout.
- OC6 — Assumptions: Deterministic checks can reject clearly unusable structure but cannot certify
  semantic fidelity without owner and reviewer judgment.
- OC7 — Authority source: Parent Epic Intent, AC1, AC2 and AC10 plus the owner's 2026-08-21
  confirmation that the revised plain-language Intent accurately captures the requested direction.

## Goal

Establish the source intent contract, proportional trigger and meaning-first approval experience
that every later intent audit, outcome proof and QA gate can rely on.

## Non-Goals

- Do not implement cross-artifact intent auditing or lifecycle narrowing gates; TASK-081 owns them.
- Do not implement outcome-journey evidence or independent QA state; TASK-082 owns them.
- Do not claim that deterministic parsing proves semantic fidelity.
- Do not require a full Intent Spine for every bounded Fix or mechanical change.

## Users & Context

- Owners who need to recognize their requested outcome without reading a legalistic requirements
  artifact or approving opaque IDs.
- Agents capturing requirements and generating task/Epic scaffolds across supported hosts.
- Maintainers who need deterministic validation without mistaking structural validity for meaning.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Add a one- or two-sentence `## Intent` to triggered Task and Epic requirements. It must
  describe the owner's desired outcome in plain language and precede detailed requirements and
  approval metadata.
- R2 — Add a compact Intent Spine with stable `OC<n>` commitments for completion capability,
  material capabilities, success journey, unacceptable successful-but-wrong result, exclusions,
  assumptions and authority source.
- R3 — Reject missing, placeholder, procedural and circular intent deterministically while
  keeping semantic interpretation reviewable rather than claiming parser certainty.
- R4 — Make approval guidance lead with the exact Intent and a concise capability/boundary/proof
  synopsis. IDs and hashes bind provenance behind the scenes but are not presented as the meaning
  the owner is approving.
- R5 — Apply the full contract to Epics and configured material work while retaining a compact
  intent path for bounded Fixes and mechanical tasks.
- R6 — Update package-source templates, requirements/Epic/Task/Fix guidance and installed
  self-hosted counterparts together so generated and current repository behavior stays aligned.

## Acceptance Criteria (Verifiable)

- AC1: Triggered Task and Epic scaffolds contain a substantive one- or two-sentence `## Intent`
  before approval detail plus a compact Intent Spine with stable `OC<n>` commitments; missing and
  placeholder content blocks readiness. Covers parent AC1.
- AC2: Readiness detects procedural or circular intent using bounded deterministic rules and
  reports that semantic fidelity still requires owner/reviewer judgment. Covers parent AC1.
- AC3: Requirements approval guidance leads with the exact Intent, what completion will and will
  not enable, material assumptions/exclusions and the proof journey; artifact identity remains
  provenance rather than the substance of the approval request. Covers parent AC2.
- AC4: A bounded-Fix fixture uses the smallest sufficient intent record and avoids the full
  Epic-level commitment/approval burden while remaining explicit about its outcome. Covers parent
  AC10.
- AC5: Source, generated host assets and installed self-hosted assets express equivalent
  meaning-first behavior and retain compatibility for pre-intent repositories. Covers parent AC1,
  AC2 and AC10.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Plain-language Intent is the approval meaning; requirements and ACs elaborate and bind it.
- Intent lives in `REQUIREMENTS.md`, not a separate owner-authored document.
- Structural checks may reject clearly unusable intent but may not certify meaning.
- Full and minimal paths are selected by work characteristics, not by an agent's desire to avoid
  rigor.

## Validation Plan

- Add template/scaffold and readiness tests for substantive, missing, placeholder, procedural and
  circular intent plus stable outcome commitments.
- Add approval snapshots proving Intent-first language and provenance separation.
- Add full-gate Epic/Task and lightweight bounded-Fix fixtures, including legacy compatibility.
- Compare package source, generated host assets and installed self-hosted assets byte-for-byte or
  through the repository's declared parity checks.
- Run focused tests, strict Doctor and `git diff --check`; do not claim behavioural reliability
  from these structural checks alone.
