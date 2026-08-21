## User Story

As an owner, I want Project Workflow to show me its brief understanding of my intent before asking
for approval, so that I can correct the meaning before detailed requirements make a narrowed result
look authoritative.

## Parent AC Coverage

- AC1, AC2, AC10

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

Ship the meaning-first Intent and approval foundation required by parent AC1, AC2 and AC10 without
implementing the later semantic-audit or outcome-proof layers.

## Approach

Extend repository-native requirements templates and readiness parsing first, then align approval
guidance and every managed agent surface. Keep deterministic validation deliberately narrow and
prove proportionality with paired full-gate and bounded-Fix fixtures.

## Phases

1. Define and parse the brief Intent and stable Intent Spine contract.
2. Lead approval guidance with meaning and move IDs/hashes to provenance.
3. Align generated/installed host assets and verify proportional compatibility.

## Acceptance Criteria

- [x] AC1: Triggered Task and Epic scaffolds contain substantive brief Intent and stable Intent
  Spine fields, with unusable structural content blocked.
- [x] AC2: Deterministic validation rejects procedural/circular intent without claiming semantic
  certainty.
- [x] AC3: Owner-facing approval leads with Intent plus capability, boundary and proof synopsis;
  identifiers remain provenance.
- [x] AC4: Bounded Fixes retain a compact path and legacy repositories remain compatible.
- [x] AC5: Package source, managed agent assets and installed self-hosted assets remain aligned.

## Validation

- AC1-AC2 / parent AC1: scaffold/readiness fixture matrix.
- AC3 / parent AC2: approval prompt and CLI output snapshots.
- AC4 / parent AC10: bounded-Fix, full-gate and legacy compatibility fixtures.
- AC5 / parent AC1, AC2, AC10: generated/self-hosted parity plus focused and full tests.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof` | Focused intent, approval, Fix, legacy and host-generation checks plus 403 full tests pass; all five child readiness gates and strict Doctor pass; CLI mirrors are byte-identical | Local implementation candidate only; no release authority | `tests/test_intent_integrity.py`, `tests/test_doctor.py`, CLI SHA-256 parity and strict Doctor output |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define Intent Contract | Add brief Intent and stable Intent Spine templates plus bounded structural validation. | AC1, AC2 | Generate Task/Epic fixtures and run readiness rejection matrix. | Done |  | `src/project_workflow/cli.py`, `src/project_workflow/templates/workflow.py`, `src/project_workflow/templates/*`, focused tests | No | bounded-return |
| 2 | Make Approval Meaning-First | Change requirements approval guidance/output to present Intent and capability/boundary/proof synopsis before provenance. | AC3 | Inspect approval snapshots and verify the recorded hash is not presented as the approval meaning. | Done | 1 | package prompts/skills, installed managed prompts/skills, focused tests | No | bounded-return |
| 3 | Preserve Proportionality | Add full-gate, bounded-Fix and legacy fixtures with explicit trigger behavior. | AC4 | Run paired fixtures and confirm small work avoids Epic-level ceremony. | Done | 1 | `src/project_workflow/cli.py`, helper mirrors, tests | No | bounded-return |
| 4 | Align Managed Surfaces | Regenerate or update supported host assets and self-hosted helpers without semantic drift. | AC5 | Run parity checks across source, generated and installed assets. | Done | 1, 2, 3 | package prompts/skills/templates, `.project-workflow/cli/workflow*`, tests | No | bounded-return |
| 5 | Validate Intent Foundation | Run focused/full tests, strict Doctor and diff validation; record exact proof boundaries. | AC1, AC2, AC3, AC4, AC5 | Review test receipts and confirm behavioural proof remains assigned to TASK-083/084. | Done | 4 | tests and child workflow evidence | No | bounded-return |

## Parent AC Evidence

- AC1: `tests/test_intent_integrity.py` proves Task/Epic/child templates, stable OC1-OC7 fields,
  missing/placeholder/procedural/circular rejection, logical meaning-first synopsis and current
  Codex/Cursor/Claude/GitHub Copilot asset generation.
- AC2: `task approval-summary` and `epic approval-summary` render Intent, completion capability,
  material capabilities, proof journey, green-but-wrong result, exclusions and assumptions before
  asking whether the meaning is accurate; tests prove the synopsis contains no Task ID, AC ID or
  artifact hash and the approval record separately preserves provenance.
- AC10: The compact Fix template/readiness path requires substantive bounded Intent without the
  full Intent Spine, while marker-free historical requirements remain compatible until adoption.

## QA & Code Review

- Date: 2026-08-21
- Verdict: Pass.
- Reviewed areas: Intent templates and parsing, semantic approval synopsis, approval provenance,
  bounded-Fix and legacy behavior, generated host assets, installed mirrors, documentation and
  regression tests.
- Evidence: `pytest -q --tb=short` passed all 403 tests; strict Doctor reported no issues;
  `py_compile` passed for all three CLI copies; `git diff --check` passed; all three CLI files have
  SHA-256 `6d10f175de0b173e3d54d87c84e03ff7bf3633425df51263da82d43297dd3e21`.
- Findings: Review found two fail-open defects before acceptance: an invalid `Intent contract`
  marker could bypass validation, and duplicate OC identifiers could overwrite one another during
  parsing. Both were corrected and covered by negative regression tests. No unresolved blocking
  findings remain. This verdict proves TASK-080's deterministic intent foundation; behavioural
  reliability and real-journey outcome proof remain explicitly owned by TASK-083 and TASK-084.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-080
- Title: Define Intent Spine And Semantic Approval
- Created: 2026-08-21
