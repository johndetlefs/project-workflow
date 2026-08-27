# Requirements

## Summary

- Task: TASK-098
- Title: Prove Generic And Optional-Consumer Journeys
- Parent AC Coverage: AC4, AC5, AC8, AC10, AC11, AC12, AC13, AC15
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Prove through actual invocation counts and failure/counter-failure journeys that the complete
generic lifecycle stops costly loops without undercooking proof or coupling Project Workflow to an
optional consumer.

## Intent Spine

- OC1 — Completion capability: maintainers can reproduce the exact bounded journey and inspect
  generic plus optional-consumer evidence before any delivery claim.
- OC2 — Material capabilities: sanitized behavioural matrix; controllable fake verifier;
  invocation/receipt accounting; package/managed parity; optional-consumer conformance; one QA per
  child; intent/acceptance audits; and delivery-boundary receipts.
- OC3 — Success journey: incomplete preflight invokes zero work; failed canary invokes zero full
  cases; corrected candidate runs one planned full campaign and one QA; evaluator regrade invokes
  zero target calls; unchanged delivery invokes no new verification.
- OC4 — Successful-but-wrong result: mocked decisions pass without subprocess counts, cheap tasks
  acquire ceremony, limits waive proof, unknown impact skips full assurance, product identifiers
  leak into generic source, or repository tests are called released/adopted evidence.
- OC5 — Exclusions: no private transcript, live full paid certification, merge, publication,
  installation, owner acceptance, or wider rollout without separate authority.
- OC6 — Assumptions: fake-verifier behavior can deterministically prove orchestration; optional
  consumer focused tests prove runner controls but not live semantic effectiveness.
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

- AC4: owner `TASK-095, TASK-098`; required evidence: Incomplete-candidate release fixture with zero verifier invocations.
- AC5: owner `TASK-096, TASK-098`; required evidence: Deterministic and real fake-verifier invocation counts proving fail-fast stage blocking.
- AC8: owner `TASK-096, TASK-097, TASK-098`; required evidence: Product/evaluator/provider/harness currentness, retry, resume, regrade, and fallback receipts.
- AC10: owner `TASK-096, TASK-098`; required evidence: One retained QA verdict, affected-validation closure, and no campaign expansion or second QA.
- AC11: owner `TASK-096, TASK-098`; required evidence: Managed/package parity, Doctor/status, fresh/upgrade journey, and historical-state counter-tests.
- AC12: owner `TASK-098`; required evidence: Complete sanitized failure/counter-failure behavioural matrix.
- AC13: owner `TASK-098`; required evidence: Disposable fake-verifier journey with exact target/full/QA/regrade/delivery counts.
- AC15: owner `TASK-097, TASK-098`; required evidence: Sanitized optional-combination journey and package/source no-coupling proof.

## Goal

Make the complete feature falsifiable at the actual execution boundary and retain honest evidence
that it is comprehensive but not coupled or overbuilt.

## Non-Goals

- No private or proprietary task content in generic fixtures.
- No universal token or cost-saving claim.
- No additional QA after the retained verdict and affected disposition.
- No merge, release, package publication, installation, or broader consumer rollout.

## Users & Context

- Owners deciding whether the expensive-loop failure is actually fixed.
- Maintainers validating package and optional-consumer behavior.
- Independent reviewers challenging underproof, overprocessing and coupling.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Build a sanitized deterministic fake verifier that records stage, candidate, case, target,
  evaluator, outcome, elapsed/call counters and checkpoint identity.
- R2 — Exercise incomplete release preflight, failed canary stop, corrected affected/full campaign,
  one QA, evaluator-only regrade and unchanged delivery with exact invocation assertions.
- R3 — Exercise diagnostic bounds, limit pause, provider/harness resume, stale receipt rejection and
  unknown-impact full fallback.
- R4 — Exercise cheap deterministic/no-adapter/manual and high-assurance countercases so the generic
  lifecycle neither overprocesses nor skips proof.
- R5 — Scan all Project Workflow product/package/fixture source for prohibited consumer-specific
  identity and prove optional integration through only generic capabilities/receipts.
- R6 — Run managed-asset parity, focused suites, frozen full locked suite, package journeys, status
  and strict Doctor at the proof layers actually affected.
- R7 — Run one independent adversarial QA per completed child, preserve Changes Requested, close
  findings only through affected validation, and run Epic intent/acceptance audits.
- R8 — Retain exact generic and optional-consumer source identities plus explicit implemented,
  validated, QA, merge, release, installation and adoption boundaries.

## Acceptance Criteria (Verifiable)

- AC1: Incomplete release preflight invokes zero verifier calls and reports the required campaign.
  Covers parent AC4.
- AC2: Failed canary causes zero full target calls; corrected candidate runs one planned full
  campaign; evaluator regrade causes zero target calls; unchanged delivery causes zero new
  verification. Covers parent AC5, AC8, AC13.
- AC3: One retained QA verdict closes through affected validation and no second QA or campaign
  expansion occurs. Covers parent AC10.
- AC4: Local/package/generated assets, status/Doctor, focused and frozen full suites pass with exact
  evidence identities and historical countercases. Covers parent AC11.
- AC5: Sanitized matrix covers all required failure and counter-failure classes, including cheap
  work, limit non-waiver and unknown-impact fallback. Covers parent AC12.
- AC6: Source/package scans contain no prohibited consumer identity; optional consumer remains
  standalone and combines only through generic capability/receipt artifacts. Covers parent AC15.
- AC7: Epic intent/acceptance audits map every parent AC to current child evidence and retain honest
  external-delivery boundaries. Covers parent AC4, AC11, AC12, AC13, AC15.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Actual invocation counts are required; prose/status-only evidence is invalid.
- The fake verifier owns generic orchestration proof; the optional consumer owns standalone runner
  conformance.
- One full locked suite occurs only after the generic candidate is frozen.
- Delivery beyond local QA/closeout remains unauthorized.

## Validation Plan

- Execute deterministic journey scripts/tests and retain exact invocation/receipt JSON.
- Run focused then one frozen full Project Workflow suite, package parity/journeys and strict Doctor.
- Inspect optional-consumer receipts and repository validation without substituting them for generic
  package proof.
- Run independent QA, affected dispositions, intent audit, acceptance audit and closeout gates.
