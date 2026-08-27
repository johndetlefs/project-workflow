# Requirements

## Summary

- Task: TASK-097
- Title: Add Standalone Reference-Consumer Runner Controls
- Parent AC Coverage: AC9, AC14
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Make the reference consumer's live behavioural runner independently safe and cost-bounded, while
optionally exposing the generic verification capability/receipt boundary without importing or
requiring Project Workflow.

## Intent Spine

- OC1 — Completion capability: a standalone maintainer can select, bound, stop, resume, and regrade
  live evaluation work with truthful typed receipts; a Coordinator may optionally consume the same
  generic output.
- OC2 — Material capabilities: current 0.7.0 managed workflow guidance; case/metadata/failed/affected
  filters; fail-fast/max-failures; target-call/elapsed limits; content-addressed checkpoints;
  telemetry; typed outcomes; bounded infrastructure retry; transcript-only regrade; and generic
  capabilities/receipt JSON.
- OC3 — Success journey: selected canaries stop on product failure; a corrected run resumes only
  current work; evaluator-only change regrades stored transcripts with zero target calls; standalone
  and optional-contract invocations produce the same result.
- OC4 — Successful-but-wrong result: flags exist but the runner still loops all cases, checkpoints
  are path-only/stale, target calls occur during regrade, or standalone execution imports/requires
  Project Workflow.
- OC5 — Exclusions: no Project Workflow product code, schema, prompt or tests change here; no live
  paid full-suite certification is required to prove deterministic runner controls.
- OC6 — Assumptions: retained transcripts/checkpoints can exercise regrade and resume; live-model
  semantics remain a separate expensive proof boundary.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
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

- One 0.7.0 Coordinator and the existing lifecycle remain authoritative.
- Operational verification state is derived from inspectable evidence and never performs work.
- Every materially expensive campaign is bound to one exact candidate, proof contract, mode, ordered stages, limits, and current receipts.
- Required assurance is never traded away for lower usage, elapsed time, or ceremony.
- Certification stops at a blocking product failure; extended investigation is a separate bounded diagnostic decision.
- Later stages never run after an earlier blocking stage.
- Proof reuse is input-specific; unknown material impact fails safely toward broader proof.
- One independent QA verdict remains separate from implementation and Coordinator verification.
- Neither Project Workflow nor a verifier requires the other. Optional compatibility is expressed only through a generic command/JSON boundary.
- Product-specific dogfood evidence is sanitized before it becomes generic package behavior.
- Merge, release, installation, adoption, owner acceptance, and effectiveness remain separate proof gates and authorities.

### Invalid Substitutes

- Another instruction saying to avoid unnecessary QA without executable stage/failure controls.
- Installing Project Workflow 0.7.0 without adding the missing pre-proof campaign capability.
- Adding only reference-consumer runner flags while Project Workflow still cannot govern costly verification.
- Adding a second lifecycle, tracker, review scheduler, execution graph, or generalized platform.
- Treating a release request as authority to silently implement or launch unbounded certification.
- Treating a canary, subset, diagnostic run, stale receipt, or QA prose as complete certification.
- Treating a cost/time limit as evidence that missing or failed proof passed.
- Rerunning target execution after an evaluator-only change when retained outputs are current.
- Static schemas, prompts, status text, or mocked decisions without actual invocation-count proof.
- Any Project Workflow runtime branch, import, schema field, prompt, fixture identifier, or package dependency that names or requires Strategic Advisor.
- Any reference-consumer change that makes its standalone runner depend on Project Workflow.

### Artifact Targets

- Generic campaign schema/state and deterministic operational projection integrated with existing Coordinator/status/Doctor surfaces.
- Progressive stage, failure-mode, campaign-limit, currentness, resume, and one-QA enforcement.
- Framework-neutral optional verifier capability and receipt contract plus manual/no-adapter path.
- Aligned local CLI, package source, templates, Codex/Claude/Copilot/Cursor guidance, README, and validation assets.
- Sanitized behavioural corpus and disposable fake-verifier journey with invocation-count receipts.
- Independent reference-consumer branch with standalone runner controls and optional generic output.
- Sanitized optional-combination dogfood receipt and explicit package/repository/delivery boundary.

### Parent AC Proof Ownership

- AC9: owner `TASK-095, TASK-097, TASK-098`; required evidence: Generic source scan, no-adapter/manual path, fake adapter, standalone consumer, and optional conformance proof.
- AC14: owner `TASK-097`; required evidence: Standalone reference-consumer runner tests, validation, checkpoints, telemetry, and generic optional output.

## Goal

Ensure the observed unbounded runner behavior is mechanically impossible while preserving the
consumer as a standalone product and keeping optional integration generic.

## Non-Goals

- No Project Workflow import or runtime dependency.
- No consumer name or case identity added to Project Workflow product source.
- No change to Strategic Advisor recommendation policy or behavioural acceptance thresholds.
- No public release, active installation replacement, or wider rollout in this child.

## Users & Context

- Strategic Advisor maintainers running costly live behavioural evaluation.
- Coordinators optionally consuming generic capabilities/receipts.
- Standalone users who do not use Project Workflow.

## Repository Scope

- Primary repository: `/Users/johndetlefs/repos/strategic-advisor` via a fresh independent worktree.
- Repositories touched: Strategic Advisor only for product/runtime changes; Project Workflow owns
  this coordination record but receives no consumer-specific product change.

## Requirements (Outcome-Focused)

- R1 — Upgrade the independent Strategic Advisor worktree to current Project Workflow 0.7.0 managed
  guidance using the canonical reviewed upgrade path; do not treat that adoption as proof of runner
  correctness.
- R2 — Add exact case, metadata, previously failing, and affected-scope selection with stable
  ordering and empty/unknown selection errors.
- R3 — Add certification fail-fast/max-failures plus target-call and elapsed campaign limits. Limit
  exhaustion/checkpoint state must be explicit and non-passing.
- R4 — Make checkpoints content-addressed by source/runtime, spec/case, model/host/config, target
  output and evaluator inputs as applicable; resume only current completed work.
- R5 — Record per-case target/adjudicator call counts, elapsed time, outcome class and retry/regrade
  disposition.
- R6 — Distinguish product/assertion, evaluator, provider and harness failures. Retry transient
  infrastructure once within the declared plan; never auto-retry a product failure.
- R7 — Support evaluator-only regrade from retained transcripts/results with zero target calls.
- R8 — Expose generic capabilities and final receipt JSON using no Project Workflow import. Keep all
  controls directly usable through the standalone CLI.
- R9 — Add deterministic runner tests and repository validation; use retained/synthetic outputs for
  expensive-boundary proof.

## Acceptance Criteria (Verifiable)

- AC1: Project Workflow 0.7.0 managed assets are adopted in the independent worktree, while source
  inspection and standalone tests prove zero Project Workflow import/runtime dependency. Covers
  parent AC9.
- AC2: Selection supports exact, metadata, previously failing and affected cases with deterministic
  order and stable invalid-selection errors. Covers parent AC14.
- AC3: Fail-fast/max-failures, target-call and elapsed limits stop before further target work and
  retain explicit non-passing checkpoint state. Covers parent AC14.
- AC4: Content-addressed resume accepts current completed work and rejects stale source/spec/model/
  target inputs. Covers parent AC14.
- AC5: Typed outcomes and telemetry distinguish target/adjudicator calls, elapsed time, product,
  evaluator, provider and harness failure plus bounded retry. Covers parent AC14.
- AC6: Evaluator-only regrade over retained outputs records zero target calls and updated evaluator
  identity. Covers parent AC14.
- AC7: Standalone invocation and optional generic capabilities/receipt output pass together without
  importing or requiring Project Workflow. Covers parent AC9 and AC14.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Strategic Advisor remains standalone.
- Optional integration is command/JSON only.
- Deterministic retained-output proof precedes any separately justified live-model campaign.
- Project Workflow adoption and runner correctness are separate claims.

## Validation Plan

- Focused deterministic runner tests for every selection, limit, checkpoint, typed outcome,
  telemetry, retry, regrade, standalone, and generic-output requirement.
- Run Strategic Advisor repository validation and source/import scans.
- Retain exact branch/source and adoption proof; do not claim live semantic certification.
