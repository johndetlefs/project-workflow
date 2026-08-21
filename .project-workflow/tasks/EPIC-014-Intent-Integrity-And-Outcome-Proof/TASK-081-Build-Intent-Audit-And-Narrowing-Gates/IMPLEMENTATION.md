## User Story

As an owner, I want Project Workflow to identify exactly where my requested capability was
narrowed or replaced, so that an internally consistent proxy cannot advance as completion.

## Parent AC Coverage

- AC3, AC4, AC5, AC6

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

Implement the intent coverage/audit model and lifecycle narrowing gates after TASK-080 establishes
the source contract.

## Approach

Build deterministic commitment identity/coverage first, layer reviewable semantic classifications
over sourced artifacts, then enforce only material unresolved reductions at lifecycle boundaries.

## Phases

1. Commitment coverage and audit artifact model.
2. Classification and material-consequence rules.
3. Lifecycle, Doctor/status and amendment enforcement.
4. Narrowed-authoring and compatibility validation.

## Acceptance Criteria

- [x] AC1: Triggered outcome commitments have complete validated coverage.
- [x] AC2: Read-only audit classifications are sourced and consequence-aware.
- [x] AC3: The narrowed-authoring fixture is rejected despite green downstream artifacts.
- [x] AC4: Material reductions block gated lifecycle states unless properly amended.
- [x] AC5: Doctor/status and legacy behavior remain truthful and compatible.

## Validation

- AC1 / parent AC3: coverage-map parser and missing-owner/proof fixtures.
- AC2 / parent AC4: classification/source/consequence snapshots and non-mutation checks.
- AC3 / parent AC5: generalized narrowed-authoring regression.
- AC4 / parent AC6: lifecycle/amendment/freshness matrix.
- AC5 / parent AC3-AC6: Doctor/status/legacy focused and full regression.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof` | 11 intent-integrity tests and the 408-test full suite pass; strict Doctor, CLI parity, py_compile and diff checks pass | Local implementation candidate only; no release authority | `INTENT-AUDIT.json`, `epic intent-audit`, lifecycle/Doctor/status gates and `tests/test_intent_integrity.py` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Build Commitment Coverage | Parse stable outcome commitments and validate parent/child/proof disposition coverage. | AC1 | Run complete, missing, duplicate and wrapped-commitment fixtures. | Done | TASK-080 | CLI source/mirrors and focused tests | No | bounded-return |
| 2 | Add Read-Only Intent Audit | Produce sourced classifications and user-visible capability consequences without mutation. | AC2 | Inspect human/JSON audit snapshots and tracked-tree hashes. | Done | 1 | CLI source/mirrors, audit artifacts and tests | No | bounded-return |
| 3 | Enforce Material Narrowing | Gate readiness, Review and Complete on unresolved material reductions with amendment freshness. | AC4 | Run lifecycle/amendment/deferral matrix. | Done | 2 | CLI lifecycle/Doctor/status and tests | No | bounded-return |
| 4 | Reproduce Narrowed Authoring | Add the sanitized green-but-wrong authoring fixture and preserved/broadened counter-cases. | AC3 | Verify the proxy candidate is rejected with the lost capability named. | Done | 2, 3 | sanitized fixtures and tests | No | bounded-return |
| 5 | Validate Audit Compatibility | Run focused/full tests, parity, strict Doctor and legacy journeys. | AC1, AC2, AC3, AC4, AC5 | Review receipts and explicit semantic-judgment boundary. | Done | 4 | tests and child evidence | No | bounded-return |

## Parent AC Evidence

- AC3: `INTENT-AUDIT.json` requires every OC commitment to map parent ACs, matching child owners,
  disposition, required outcome proof, source/target locations and user-visible consequence; the
  EPIC-014 dogfood audit currently reports complete sourced coverage.
- AC4: `epic intent-audit` emits human and JSON `preserved`, `narrowed`, `proxy`, `omitted`,
  `broadened`, `amended`, `deferred` and `unknown` classifications without mutation, with explicit
  current/stale/unknown/review-required/changes-requested state and next action.
- AC5: The sanitized narrowed-authoring fixture records truthful preview plus one canary control,
  green downstream claims and the missing meaningful-authoring capability; it is classified proxy
  and blocked as changes-requested.
- AC6: Child readiness, Review and Complete plus Epic Ready/In Progress gates require a current
  audit. Material drift needs a plain, owner-identified, freshness-bound amendment and disposition;
  marker-free historical requirements retain their legacy-compatible path.

## QA & Code Review

- Date: 2026-08-21
- Verdict: Pass.
- Evidence: Focused audit tests pass; the full 408-test suite passes; strict Doctor reports no
  issues; all CLI copies are byte-identical; status reports `intent current`; the audit command is
  demonstrably read-only and the EPIC-014 dogfood map is current.
- Findings: Review caught three integration defects before acceptance: the new Doctor code and
  operational source kind were initially unregistered, the self-dogfood parent lacked the full
  contract marker/schema labels, and source/target locations were not existence-checked. All were
  corrected with regression coverage. Semantic classifications remain explicit reviewer judgment;
  deterministic code validates identity, coverage, provenance, freshness and lifecycle only.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-081
- Title: Build Intent Audit And Narrowing Gates
- Created: 2026-08-21
