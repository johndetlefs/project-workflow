# Requirements

## Summary

- Task: TASK-101
- Title: Refactor FIX-010 Into The Codex Adapter
- Parent AC Coverage: AC3, AC4, AC8, AC9, AC12, AC13, AC14
- Last updated: 2026-08-28
- Intent contract: full

## Intent

Turn the verified local FIX-010 mechanisms into Project Workflow's subordinate Codex adapter. A
trusted, supported Codex installation must enforce the existing host-neutral envelope and return
typed core receipts, while unsupported, untrusted, disabled or incompatible Codex surfaces remain
truthfully blocked.

## Intent Spine

- OC1 — Completion capability: One current Codex App Server turn executes through the already
  sealed Project Workflow authority and returns an exact input-bound terminal receipt.
- OC2 — Material capabilities: Current-host capability preflight; synchronous hook enforcement;
  App Server lifecycle, token and elapsed interruption; aggregate tool/test/worker/write accounting;
  source/scope closeout; package assets; status/Doctor truth; complete FIX-010 disposition.
- OC3 — Success journey: A trusted disposable repository configures one Codex adapter, executes one
  material turn through `project execute`, observes hook activation and App Server events, stops at
  completion or a finite boundary, and persists one receipt in Coordinator-owned state.
- OC4 — Successful-but-wrong result: A green mock, static plugin, raw `codex exec`, copied
  `project-enforce` surface, unverified hook, unbound receipt, arbitrary 80,000-token rule, or
  Codex-only lifecycle truth is presented as supported bounded execution.
- OC5 — Exclusions: Claude Code, cross-host equivalence, publication, consumer install/adoption,
  owner acceptance, untrusted repository hooks, Codex cloud/hosted tools and managed policy that
  disables required hooks remain outside this child proof.
- OC6 — Assumptions: Local `codex-cli 0.145.0-alpha.30` exposes the current App Server methods,
  token events, synchronous hooks and interrupt path; exact support is capability-negotiated, never
  inferred from package presence.
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

- AC3, AC4: owner `Define Host-Neutral Execution And Candidate Contract`; required evidence: Direct read-only countercases, material bypass denials, immutable-limit and blocked-proof receipts.
- AC8: owner `Enforce Proportionate QA Remediation And Fixed Release; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Clean candidate, once-only operations, failure termination, bounded infrastructure recovery, and prohibited-authority tests.
- AC9: owner `Refactor FIX-010 Into The Codex Adapter`; required evidence: Real supported Codex canary, subordinate aggregation, interruption, receipt, and install evidence.
- AC12: owner `Define Host-Neutral Execution And Candidate Contract; both host adapters`; required evidence: Unsupported/version/trust/policy fixtures and truthful capability/status results.
- AC13: owner `Both host adapters; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Retained-package fresh/upgrade/no-op/disable journeys and Doctor activation state.
- AC14: owner `Refactor FIX-010 Into The Codex Adapter; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Complete prototype disposition map plus source/package scans rejecting retained lock-in assumptions.

## Goal

Provide the real Codex mechanism behind the host-neutral execution controller without importing
FIX-010's separate public product, repository-wide constant budget or release lifecycle.

## Non-Goals

- Do not restore `project-enforce`, FIX-010's release executor, or its repository-local fixed token
  backstop as public architecture.
- Do not claim Claude Code or cross-host support, package publication, installation, adoption,
  hosted Codex coverage or owner acceptance.
- Do not let adapter state replace `COORDINATION.json`, the host-neutral envelope, verification
  campaign, QA findings, candidate authority or fixed release controller.

## Users & Context

Project Workflow Coordinators need to dispatch an approved material execution through a local
Codex runtime while retaining exact limits, source, write scope, proof obligations and terminal
evidence in Project Workflow state.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1 — Add a Codex adapter whose input is the current validated host-neutral execution control;
  host-specific policy is sealed inside the capability configuration and cannot widen core scope.
- R2 — Probe exact Codex executable/version and required App Server/hook behavior. Unknown,
  unsupported, disabled, untrusted or policy-blocked capability returns a precise non-passing state.
- R3 — Run App Server through its initialize/thread/turn event contract, use synchronous
  `SessionStart`, `PreToolUse` and `PostToolUse` hooks, and interrupt on finite token or elapsed
  authority. Hook absence or malformed events fail closed.
- R4 — Atomically reserve aggregate tool, test, identical retry, worker and changed-path authority
  before execution where the host exposes it; verify Git source and write scope after tool calls and
  at closeout.
- R5 — Convert host-native counts and terminal outcome into the existing typed receipt schema,
  bind it to sealed capability/source/candidate/proof identity, and persist it through the
  Coordinator-owned state writer.
- R6 — Keep `project execute --id` read-only when no sealed adapter configuration exists; when one
  current Codex adapter is configured, dispatch that exact path without raw-host bypass.
- R7 — Package only subordinate Codex adapter/diagnostic assets. Do not expose `project-enforce`, a
  second release command or a static hook that claims control outside the supervised path.
- R8 — Add status and Doctor evidence for active, disabled, incompatible and untrusted Codex
  states, plus deterministic protocol/hook tests and one real current-Codex canary receipt.
- R9 — Record an adopt/refactor/replace/retire disposition for every FIX-010 file and behavior and
  scan source/package assets for retired public naming, fixed 80,000-token rules and broad lock-in.

## Acceptance Criteria (Verifiable)

- AC1: The Codex capability probe verifies the exact executable/version/configuration and every
  binding control or blocks with the missing capability visible.
- AC2: A real supported Codex App Server canary activates the synchronous hook, runs one bounded
  material turn, aggregates host-native usage, and persists one core typed receipt.
- AC3: Tool, test, identical retry, worker, write-scope, token and elapsed boundaries interrupt or
  deny without bypass; hook absence, malformed messages and source/scope drift fail closed.
- AC4: `project execute` dispatches only from the sealed host-neutral control and Project Workflow
  remains the sole writer of coordination, receipt and lifecycle truth.
- AC5: Package assets contain the subordinate adapter and truthful diagnostics; disabled,
  incompatible, untrusted and unavailable states do not advertise Codex support.
- AC6: Every FIX-010 file and behavior has an explicit disposition, and scans prove no public
  `project-enforce`, universal 80,000-token rule or prototype release architecture remains.
- AC7: Tests and evidence distinguish deterministic simulation, real local Codex runtime, package
  presence, publication, installation, adoption and owner acceptance.

## Open Questions (Answer Needed)

- None inside the approved child. Cross-host equivalence and external delivery remain TASK-103.

## Decisions (Resolved)

- Use current App Server events for lifecycle/token/interrupt supervision and synchronous session
  hooks for pre/post tool enforcement.
- Keep adapter configuration inside the sealed capability identity and translate only typed native
  metrics into the host-neutral receipt.
- Retain FIX-010's atomic counter, scope parsing, App Server and adversarial test ideas; retire its
  public CLI, fixed project budget, standalone release executor and Codex-owned product naming.
- Treat official OpenAI documentation and locally generated current protocol schemas as the host
  contract; do not depend on undocumented prototype assumptions without a current probe.

## Validation Plan

- Focused deterministic adapter tests cover capability negotiation, hook denial/reservation,
  interruption, malformed events, source/scope closeout, typed receipt persistence and status.
- Generate the installed Codex App Server schema and compare required methods/fields; validate
  packaged adapter assets and retained-prototype scans.
- Run one bounded real Codex canary in a disposable clean repository. TASK-103 retains the complete
  dual-host conformance, package journey and recurrence proof.
