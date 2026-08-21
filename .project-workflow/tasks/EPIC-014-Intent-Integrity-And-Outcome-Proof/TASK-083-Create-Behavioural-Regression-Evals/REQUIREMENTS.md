# Requirements

## Summary

- Task: TASK-083
- Title: Create Behavioural Regression Evals
- Parent AC Coverage: AC10, AC11, AC12
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Prove that the new controls change agent behaviour across realistic work rather than merely adding
documents and parser branches. Reject under-delivery and proxy completion without encouraging
gold-plating or approval fatigue for genuinely bounded requests.

## Intent Spine

- OC1 — Completion capability: Maintainers can compare repeated held-out agent trials and see
  whether agents preserve intent, expose de-scoping and choose claim-matched proof.
- OC2 — Material capabilities: Sanitized cases, repeatable harness identity, multi-axis grading,
  false-pass analysis, proportionality and tested-surface limits are recorded.
- OC3 — Success journey: Multiple agents/trials handle five distinct failure classes and the
  bounded counter-case, with graders catching proxy completion and unnecessary scope.
- OC4 — Successful-but-wrong result: Template tests pass and one cherry-picked model response looks
  good while realistic agents still narrow outcomes or bury approval meaning.
- OC5 — Exclusions: Do not claim universal model reliability, expose private transcripts, tune only
  to public fixtures or treat maximal output as intent fidelity.
- OC6 — Assumptions: Behavioural results are conditional on recorded model, prompt, harness and
  evaluator identities and require false-positive/false-negative review.
- OC7 — Authority source: Parent Epic Intent, OC5-OC7 and approved parent AC10-AC12.

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

## Goal

Create a sanitized, repeatable behavioural evaluation that tests intent preservation and
proportionality on realistic held-out prompts across supported agent guidance.

## Non-Goals

- Do not publish private task transcripts or proprietary downstream project content.
- Do not claim evaluation success proves every model, host or future version.
- Do not weaken graders to make a preferred implementation pass.

## Users & Context

- Maintainers deciding whether a workflow release genuinely improves agent behaviour.
- Owners harmed by under-delivery, proxy completion, over-scoping or approval burden.
- Reviewers diagnosing false passes and false failures.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Build at least five sanitized failure/counter-failure classes: narrowed authoring,
  rendered-product versus code/test proxy, wrong runtime/artifact, checklist-complete but
  outcome-incomplete Epic, and bounded work that must avoid gold-plating.
- R2 — Keep held-out prompts separate from implementation fixtures and record exact model, prompt,
  harness, evaluator, run identity and result artifacts.
- R3 — Run multiple trials and grade preserved intent, explicit de-scoping, capability coverage,
  exact outcome proof, unnecessary scope and approval burden.
- R4 — Record false-pass/failure analysis, disagreements and tested-surface limitations.
- R5 — Demonstrate the full gate triggers for material work and a compact path remains practical
  for a bounded Fix.

## Acceptance Criteria (Verifiable)

- AC1: A bounded-Fix counter-case completes with compact Intent and proportionate proof while
  material Epic/authoring/migration/replacement claims receive full evaluation. Covers parent AC10.
- AC2: The sanitized corpus contains at least five distinct classes, no private transcript or
  proprietary content, and expected under-delivery plus anti-gold-plating verdicts. Covers AC11.
- AC3: Multiple held-out trials record exact harness/model/evaluator identity and grade all six
  required axes with preserved raw/structured results. Covers parent AC12.
- AC4: The evaluation report documents false passes/failures and limits claims to tested surfaces.
  Covers parent AC12.
- AC5: Behavioural evidence remains distinct from deterministic unit/template/parser tests.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use sanitized generalized scenarios, not copied private transcripts.
- Include a bounded anti-gold-plating case so larger output is not rewarded automatically.
- Behavioural claims name the tested model/harness scope and do not generalize beyond it.

## Validation Plan

- Audit fixture text for identifiers, paths, proper nouns and proprietary details.
- Run deterministic grader contract tests before agent trials.
- Execute multiple held-out trials per case and preserve run/evaluator identity.
- Independently sample passes, failures and disagreements for grader validity.
- Run focused/full suites, strict Doctor and `git diff --check` alongside behavioural evidence.
