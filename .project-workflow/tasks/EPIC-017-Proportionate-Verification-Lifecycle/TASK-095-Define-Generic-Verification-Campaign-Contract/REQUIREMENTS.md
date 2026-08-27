# Requirements

## Summary

- Task: TASK-095
- Title: Define Generic Verification Campaign Contract
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC9
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Give the existing Coordinator one generic, source-bound verification campaign and a truthful
read-only projection of what must happen next, without introducing another lifecycle or naming any
consumer.

## Intent Spine

- OC1 — Completion capability: a Coordinator can record and inspect one current materially
  expensive verification campaign for an exact candidate and derive the next required lifecycle
  action without executing the verifier.
- OC2 — Material capabilities: compact schema; candidate/source identity; campaign mode; claims;
  ordered stages; affected scope; limits; outcome; receipt references; generic optional adapter
  capabilities; and five-state operational projection.
- OC3 — Success journey: incomplete implementation plus a release request projects
  `implementation-required` and visible campaign scope with zero verifier invocations; a valid
  current campaign projects the next required proof or QA/delivery state.
- OC4 — Successful-but-wrong result: a new status field appears but accepts stale/malformed
  campaigns, performs work, creates a second status authority, or contains a consumer-specific
  branch.
- OC5 — Exclusions: no stage execution, proof adjudication, QA changes, runner implementation,
  global proof graph, or consumer dependency in this child.
- OC6 — Assumptions: detailed receipts remain evidence artifacts; missing adapters use manual
  commands or block only when a required control is unsupported.
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

- AC1: owner `TASK-095, TASK-096`; required evidence: Architecture/source inspection and regressions proving one Coordinator/lifecycle and no copied graph.
- AC2: owner `TASK-095, TASK-096`; required evidence: Campaign schema/currentness tests plus malformed/stale/source-mismatch failures.
- AC3: owner `TASK-095`; required evidence: Human/JSON status fixtures deriving each operational result without mutation.
- AC4: owner `TASK-095, TASK-098`; required evidence: Incomplete-candidate release fixture with zero verifier invocations.
- AC9: owner `TASK-095, TASK-097, TASK-098`; required evidence: Generic source scan, no-adapter/manual path, fake adapter, standalone consumer, and optional conformance proof.

## Goal

Define the generic contract that all later enforcement and verifier work can rely on while proving
the 0.7.0 Coordinator and lifecycle remain the sole authority.

## Non-Goals

- No verifier invocation or subprocess orchestration.
- No progressive failure/limit enforcement beyond schema and projection prerequisites.
- No reference-consumer identifiers, imports, fixtures, or paths in product source.
- No package publication or consumer rollout.

## Users & Context

- Coordinators inspecting whether implementation, verification, QA, or delivery is genuinely next.
- Owners receiving a truthful release preflight before expensive proof starts.
- Verifier authors optionally exposing generic capabilities without importing Project Workflow.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Extend `COORDINATION.json` or its existing current-state owner with one compact
  `verification_campaign` object; store references rather than full outputs or another execution
  graph.
- R2 — Validate schema, candidate/source currentness, mode, claims, ordered unique stages, affected
  scope, limits, current outcome, receipt references, and next action. Invalid or stale state fails
  closed with stable Doctor/status findings.
- R3 — Derive exactly one non-mutating operational projection:
  `implementation-required`, `verification-required`, `qa-required`, `delivery-ready`, or
  `blocked`, using existing lifecycle plus campaign evidence.
- R4 — Provide CLI commands to initialize/update/inspect the campaign using fingerprint-bound
  current source and explicit owner/plan authority. Status inspection never invokes an adapter.
- R5 — Define a generic optional adapter capability and receipt schema without importing, naming,
  or requiring any concrete verifier. Preserve a manual/no-adapter path.
- R6 — Align local and packaged CLI/schema/guidance surfaces owned by this contract.

## Acceptance Criteria (Verifiable)

- AC1: Existing Coordinator, tracker, lifecycle and QA status remain unchanged; only one compact
  current campaign is added and no execution graph is copied. Covers parent AC1.
- AC2: Valid campaign state round-trips; malformed, missing-input, stale-source, duplicate-stage,
  and mismatched-candidate state fails closed with stable human/JSON diagnostics. Covers parent AC2.
- AC3: Fixtures derive all five operational projections from inspectable evidence, and repeated
  status calls are byte-for-byte non-mutating. Covers parent AC3.
- AC4: Incomplete implementation plus a release request projects `implementation-required` and
  records zero adapter/verifier invocations. Covers parent AC4.
- AC5: Generic source/schema scans contain no reference-consumer identity or runtime dependency;
  manual/no-adapter and fake-adapter capability fixtures both remain valid. Covers parent AC9.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Operational projection is derived, not a second lifecycle.
- Campaign detail is compact and references existing proof artifacts.
- The adapter contract is optional and framework-neutral.
- Status and Doctor inspect only; execution belongs to the later enforcement child.

## Validation Plan

- Focused schema, CLI, status, Doctor, currentness, non-mutation, no-adapter, fake-adapter, and
  product-source decoupling tests.
- Parent intent audit current before implementation and after any material plan change.
