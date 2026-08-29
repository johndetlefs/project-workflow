# Requirements

## Summary

- Task: TASK-099
- Title: Define Host-Neutral Execution And Candidate Contract
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC5, AC7, AC11, AC12
- Last updated: 2026-08-28
- Intent contract: full

## Intent

Give Project Workflow one host-neutral, source-bound contract that decides which work must enter a
sealed execution path, what finite authority that path has, how progress and candidates are
represented, and what exact evidence a host adapter must return. Preserve the existing Coordinator,
verification campaign, QA verdict, lifecycle, and shared-state writer as the only authorities.

## Intent Spine

- OC1 — Completion capability: the Coordinator can classify a current work item, seal one finite
  execution envelope for material work, distinguish working and promoted candidates, and derive
  the next allowed action or precise blocker from generic receipts without launching a host model
  for read-only inspection.
- OC2 — Material capabilities: versioned execution, progress, candidate, capability, and receipt
  schemas; deterministic routing; immutable typed limits; adapter negotiation; material-bypass
  denial contract; host-neutral execute/release preflight; and status/Doctor projection.
- OC3 — Success journey: read-only and cheap deterministic countercases run directly with zero
  adapter calls; a material action outside the controlled path is denied; a supported fixture
  adapter accepts one sealed envelope, records typed progress, preserves missing proof on a limit,
  and returns a source-bound receipt whose state and candidate meanings are host-independent.
- OC4 — Successful-but-wrong result: schemas or status text exist while raw material calls remain
  allowed, the worker can expand its envelope, host metrics are normalized, working failures create
  release-candidate churn, unsupported capability falls back to prose, or a second lifecycle or
  campaign becomes authoritative.
- OC5 — Exclusions: no broad QA/remediation implementation, release-operation execution, Codex or
  Claude Code host mechanics, real-host support claim, package publication, consumer installation,
  or universal numeric limit in this child.
- OC6 — Assumptions: repositories can declare bounded policy inputs; hosts expose different
  enforceable units; exact capability is negotiated at runtime; and an exhausted or unsupported
  binding control blocks material work without waiving proof.
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

- Project Workflow remains the only product owner, repository owner, Coordinator, lifecycle, verification campaign, QA verdict, candidate authority, and shared-state writer.
- Read-only and cheap deterministic work does not launch another model or require campaign ceremony.
- Material work in a supported trusted installation cannot mutate, validate broadly, remediate QA, promote a candidate, or release outside the controlled path.
- The worker cannot amend its sealed execution identity, write scope, permitted operations, proof obligations, or finite limits.
- Limits pause or block and keep missing proof visible; they never manufacture a pass.
- One independent QA pass creates one durable findings set. In-scope remediation is automatic and bounded; only affected proof and unresolved findings are rechecked; a second broad QA is prohibited.
- Continuation requires named material progress. An identical or no-progress repeat is denied.
- Working revisions, verification candidates, and release candidates have distinct semantics.
- Release candidate promotion occurs only after all required implementation, verification, QA, and affected-proof obligations pass.
- Release runs predeclared operations against one clean frozen candidate and has no source repair, QA, or replacement-candidate authority.
- Host adapters enforce the same decisions and receipt meanings but may use different native units and mechanisms.
- Unsupported or unknown binding host capability fails closed for material work and cannot be advertised as supported.
- Codex and Claude Code are the minimum initial supported hosts. No other host inherits the claim.
- All shipped core and adapter assets come from the Project Workflow repository and package.
- Automated, host-runtime, package, merge, publication, installation, adoption, effectiveness, and owner-acceptance proof remain separate.

### Invalid Substitutes

- Another instruction, prompt, checklist, approval step, or status field saying that agents should stop.
- Merging FIX-010 unchanged, exposing project-enforce as the portable public product, or treating one local Codex canary as cross-host proof.
- A separate enforcement repository, service, or workflow writer that owns its own candidate, findings, QA, or release truth.
- A universal token/time/test number presented as proportionate control.
- A stop rule that leaves material findings or required proof for the owner to resolve manually.
- Repeating broad QA after correction instead of retaining one findings set and validating affected proof.
- Calling every mutable implementation/test revision a release candidate.
- Treating a failed or exhausted envelope as a pass, completion, or release authorization.
- A release command that can edit source, install fixes, commission QA, or mint a successor candidate.
- Static Codex or Claude assets, fake hooks, mocked CLI output, or package presence without a real supported-host journey.
- Claiming that a repository-local hook covers untrusted repositories, disabled plugins, user shells, hosted surfaces, or managed policy that prevents the hook.
- Host-metric normalization that presents Codex tokens, Claude dollar budget, turns, or elapsed time as interchangeable.
- Project Workflow production code, workflow state, or managed assets placed in Strategic Advisor.

### Artifact Targets

- Versioned host-neutral execution-envelope, progress, candidate, capability, and typed-receipt schemas integrated with the 0.8.0 Coordinator and verification campaign.
- Deterministic material-work router plus host-neutral project execute and project release CLI surfaces.
- Immutable envelope supervisor/controller with aggregate progress, denial, interruption, and terminal receipt behavior.
- One QA findings/remediation campaign integrated with affected-proof validation and no-recursive- QA enforcement.
- Working-revision, verification-candidate, release-candidate, and fixed release state/commands.
- Codex adapter and managed installation assets using current supported Codex programmatic/hook mechanisms.
- Claude Code adapter and managed installation assets using current supported print-mode, streaming, permission/tool, hook, budget/turn, and timeout mechanisms.
- Capability preflight, status, Doctor, diagnostics, disable/uninstall, and truthful unsupported state.
- FIX-010 disposition map covering every prototype file, behavior, test, CLI, hook, and repository backstop.
- Sanitized cross-host conformance corpus, real Codex and Claude Code canary receipts, recurrence journey, package/fresh/upgrade/no-op/disable evidence, and explicit delivery boundary.
- Aligned source, generated assets, README, CHANGELOG, package metadata, tests, schemas, and repository-local mirrors.

### Parent AC Proof Ownership

- AC1, AC2: owner `Define Host-Neutral Execution And Candidate Contract`; required evidence: Source/dependency scan plus lifecycle/campaign singularity tests.
- AC3, AC4: owner `Define Host-Neutral Execution And Candidate Contract`; required evidence: Direct read-only countercases, material bypass denials, immutable-limit and blocked-proof receipts.
- AC5, AC7: owner `Define Host-Neutral Execution And Candidate Contract; Enforce Proportionate QA Remediation And Fixed Release`; required evidence: Working-revision/candidate-lineage tests, progress requirements, and exact blocked disposition.
- AC11: owner `Build The Claude Code Adapter; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Cross-host state, denial, candidate, proof, and receipt conformance matrix.
- AC12: owner `Define Host-Neutral Execution And Candidate Contract; both host adapters`; required evidence: Unsupported/version/trust/policy fixtures and truthful capability/status results.

## Goal

Create the stable core contract that later QA/release and host-adapter children can implement
without duplicating lifecycle truth or changing candidate and receipt semantics per host.

## Non-Goals

- Do not implement the one-QA findings/remediation engine or terminal release operations owned by
  TASK-100.
- Do not implement Codex App Server/plugin enforcement or Claude Code hook/CLI enforcement owned by
  TASK-101 and TASK-102.
- Do not claim real-host, package-installation, cross-host, release, merge, adoption, or owner-
  acceptance proof.
- Do not carry `project-enforce`, a fixed 80,000-token limit, or Codex-specific state into the
  public contract.
- Do not require an execution-agent launch for status, Doctor, requirements, inspection, or cheap
  deterministic commands.

## Users & Context

- Coordinators need one deterministic answer about direct versus controlled work and one exact
  next action when execution is blocked.
- Implementers and later host adapters need a sealed, source-bound envelope and generic progress
  and receipt semantics they cannot redefine.
- Owners need ordinary read-only work to stay cheap and missing proof to remain visible when finite
  authority is exhausted.
- Maintainers need status, Doctor, package source, and managed CLI copies to agree without adding a
  second state owner.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Define versioned host-neutral execution-envelope, progress, candidate, capability, and
  typed-receipt contracts. Bind work identity, source identity, phase, write scope, permitted
  operations, proof obligations, finite typed limits, progress, candidate state, and receipt
  currentness without naming a host.
- R2 — Integrate the contracts with the existing 0.8.0 Coordinator and verification campaign.
  `COORDINATION.json`, the tracker lifecycle, one QA verdict, and current verification campaign
  remain authoritative; no second mutable lifecycle, tracker, campaign, scheduler, or writer is
  created.
- R3 — Classify operations deterministically by material effect. Status, Doctor, requirements,
  inspection, and cheap deterministic commands remain direct. Material mutation, broad
  validation, QA remediation, candidate promotion, and release require controlled authority in a
  supported trusted installation. Classification and preflight perform zero model calls.
- R4 — Validate a sealed envelope whose finite units remain typed and host-specific. Required
  identity, allowed paths/operations, proof obligations, worker/tool/test/retry/path/time units,
  and supported host-budget units cannot be changed by a worker. Policy values come from declared
  work/repository inputs or a bounded estimate, never a universal constant.
- R5 — Model named progress and exact blocked disposition. Continuation requires changed source or
  evidence against an unresolved material finding and remaining authority. Limit exhaustion,
  missing proof, unsupported capability, stale source, identical input, and no progress are typed
  non-passing outcomes.
- R6 — Keep working revisions, verification candidates, and release candidates distinct. Working
  check failures do not create rejected release candidates; source changes create current
  successor verification identity; release-candidate promotion remains unavailable until later
  verification and QA obligations pass.
- R7 — Define runtime capability negotiation and an adapter boundary that records required controls
  as verified, unsupported, or unknown for an exact host/version/configuration. Binding gaps fail
  closed for material work; metrics and receipts preserve native units while sharing state,
  denial, candidate, proof, and terminal meanings.
- R8 — Add host-neutral `project execute --id WORK-ID` and `project release --id WORK-ID` preflight
  surfaces that derive authority from current workflow state rather than reconstructing envelopes
  from user flags. Until later children supply eligible execution/release behavior, preflight must
  return the exact missing capability or obligation without starting work.
- R9 — Project the one next action and exact blocker through status and Doctor from current
  envelope, campaign, candidate, capability, and receipt evidence. Inspection remains read-only.
- R10 — Keep packaged CLI source, managed template, repository-local mirror, schemas, documentation,
  and focused failure/counter-failure tests aligned. Product source and package metadata must not
  import or name Strategic Advisor.

## Acceptance Criteria (Verifiable)

- AC1: Source and dependency inspection plus singularity tests prove the new contracts live only in
  Project Workflow and extend the existing Coordinator, lifecycle, campaign, QA verdict, and
  shared-state writer without duplicating any of them. Covers parent AC1 and AC2.
- AC2: Direct status, Doctor, requirements, inspection, and cheap deterministic fixtures record
  zero adapter/model invocations; equivalent material action outside controlled authority returns
  a stable denial and the host-neutral command to use. Covers parent AC3.
- AC3: Valid envelopes round-trip, while mutation or mismatch of work/source identity, write scope,
  operation policy, proof obligations, worker/tool/test/retry/path/time limits, and supported host
  budgets fails closed. Limit hits retain missing proof and never return pass. Covers parent AC4.
- AC4: Candidate-lineage fixtures prove ordinary working failures create zero rejected release
  candidates, source/evidence changes produce current verification succession, and release-
  candidate promotion is impossible before required verification and QA evidence. Covers parent
  AC5.
- AC5: Progress fixtures allow continuation only for a named unresolved material finding plus
  changed source/evidence and remaining authority; identical, no-progress, stale, exhausted,
  unsupported, and unknown cases return one precise non-passing blocker. Covers parent AC7 and
  AC12.
- AC6: Two fake adapters using different native units produce identical routing, state-transition,
  denial, candidate, proof-preservation, and receipt meanings; no host-metric normalization is
  present. Covers the core contract portion of parent AC11 and AC12.
- AC7: `project execute` and `project release` resolve current workflow authority without envelope
  flags, status and Doctor expose the same one next action, repeated inspection is non-mutating,
  and all three managed CLI copies plus package assets remain aligned. Covers parent AC3 and AC12.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- The public contract and commands are host-neutral; adapter launchers and native metrics remain
  internal details.
- The existing coordination and verification state is extended rather than copied.
- Routing is deterministic and model-free.
- Limits are sealed typed policy derived from the current work, not a universal constant.
- This child may prove the adapter contract with fake adapters only; real Codex and Claude Code
  support remains unproven until their dedicated children and TASK-103 pass.
- Release preflight may expose readiness and blockers, but TASK-100 owns release execution.

## Validation Plan

- Add focused schema, routing, envelope immutability, progress, candidate-lineage, capability,
  fake-adapter conformance, CLI preflight, status, Doctor, non-mutation, asset-parity, and source-
  dependency tests.
- Run the parent Intent audit before implementation and after material plan changes.
- Run only the affected focused suite in this child; the frozen-candidate full suite and real-host
  journeys remain later Epic proof gates.
