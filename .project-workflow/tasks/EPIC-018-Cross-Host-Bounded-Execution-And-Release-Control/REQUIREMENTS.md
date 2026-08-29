# Requirements

## Summary

- Task: EPIC-018
- Title: Cross-Host Bounded Execution And Release Control
- Last updated: 2026-08-29
- Proposal state: Implementation substantially complete; v0.9.0 delivery authorized with real Claude Code runtime proof pending
- Intent contract: full

## Intent

Make Project Workflow mechanically bound material agent implementation, proportionate QA
remediation, verification, and release so useful delivery cannot expand into an open-ended
test-fix-review-release loop. The capability belongs to Project Workflow and must work through
truthful host adapters, initially Codex and Claude Code, without imposing constant model overhead
on read-only or cheap work.

## Intent Spine

- OC1 — Completion capability: one Project Workflow Coordinator can route a material work item
  through a finite host-enforced execution envelope, one proportionate QA/remediation campaign, an
  exact frozen release candidate, and a terminal release attempt; routine failures are handled
  inside the approved scope without asking the owner to supervise the loop.
- OC2 — Material capabilities: a host-neutral execution-control contract; deterministic material
  work routing; immutable finite limits; progress-aware QA findings and remediation; working
  revision, verification-candidate, and release-candidate separation; fixed-candidate release;
  typed receipts; capability negotiation; Codex and Claude Code adapters; package/upgrade assets;
  status and Doctor projection; and real cross-host conformance evidence.
- OC3 — Success journey: read-only diagnosis runs directly; an attempted material mutation outside
  the controlled path is denied; implementation performs focused checks inside one sealed
  envelope; one QA pass records named findings; in-scope corrections and affected proof close those
  findings without another broad QA; one release candidate is then frozen and released once
  without source repair, replacement-candidate creation, or recursive closeout.
- OC4 — Successful-but-wrong result: Project Workflow ships persuasive guidance, a Codex-only
  launcher, or arbitrary stop counts while raw host calls can bypass the control; every test
  failure is labelled a rejected release candidate; QA repeatedly rescans the whole change; limits
  waive required proof; release can edit source or mint another candidate; or Claude support is
  claimed from copied prompt assets without a real Claude Code journey.
- OC5 — Exclusions: no universal token target; no reduction of required proof; no owner checkpoint
  for routine in-scope QA corrections; no second lifecycle, QA scheduler, verification campaign, or
  workflow writer; no standalone enforcement product; no requirement that every read-only or cheap
  command launch an agent; and no first-release enforcement claim for Cursor, GitHub Copilot, or
  unsupported hosted surfaces.
- OC6 — Assumptions: supported hosts expose different enforceable units; deterministic routing and
  receipt checks should add no model call; host/runtime features can change and must be negotiated
  at execution time; Project Workflow 0.8.0 remains the lifecycle and verification authority; and
  an exhausted limit pauses or blocks work without turning missing proof into a pass.
- OC7 — Authority source: owner direction in the 2026-08-27 to 2026-08-28 release-recurrence
  review; Project Workflow 0.8.0 main at e795602a591cee0ef1c9b1bb50164749a85d0085;
  EPIC-016, EPIC-017, FIX-008, and FIX-009; the local FIX-010 prototype at
  bd78627b47c90c492cbf844231c92e4843786f94; current Codex App Server documentation; and current
  Claude Code hooks and CLI documentation.

## Owner-Authorized Release Decision — 2026-08-29

- The owner explicitly authorizes committing, pushing, merging, tagging, publishing, and upgrading
  every accessible Project Workflow installation to v0.9.0, including repositories with dirty
  working trees, provided unrelated work is preserved.
- Delivery may proceed before the real authenticated Claude Code canary. This changes delivery
  sequencing only: it does not satisfy, waive, or narrow AC10, the Claude-dependent portion of
  AC11/AC13/AC15, or the Epic's final cross-host conformance claim.
- The v0.9.0 package may ship the Claude Code adapter and managed assets, but release notes,
  status, Doctor, and adoption reporting must describe that adapter as packaged and fail-closed,
  not runtime-certified or proven supported, until the real canary passes.
- TASK-102 and TASK-103 remain open at their truthful proof boundary after publication and
  adoption. EPIC-018 must not close until the outstanding real-host evidence is completed or the
  owner separately approves an explicit parent-AC deferral.
- The preserved independent QA verdict and its affected remediation evidence remain the one broad
  QA campaign. Release and rollout reuse that proof and run exact-candidate/package/adoption checks;
  they do not commission recursive broad QA.
- Source: this Codex owner thread, 2026-08-29: "Release it ... update it in every single project,
  even with dirty trees ... with the understanding that we haven't yet done tests in Claude."

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-29
- Approval note / source: Owner instruction in this task on 2026-08-29: release v0.9.0 and update every project, including dirty trees, while retaining the outstanding real Claude test and avoiding recursive QA.
- Approved artifact identity: sha256:770cf0843fc8f4c3c6f3b8a67324463fd9eea0928c97bee908c605d5341b9531

## Goal

Close the remaining host-execution gap after Project Workflow 0.8.0. Existing workflow state can
describe proportionate execution and verification, but an ordinary agent process can still retain
authority to investigate, edit, retest, re-review, repair, release, and close out after the useful
result. The result of this Epic must be enforceable product behavior in Project Workflow, not
another instruction telling an agent to stop.

## Strategic Architecture Review

### Decision

Adopt a host-neutral Project Workflow control plane with host adapters shipped and versioned from
the Project Workflow repository. Codex and Claude Code are the minimum supported adapters. Adapter
assets may use each host's plugin, hook, CLI, or supervisor mechanisms, but they are not separate
products and they do not own workflow or candidate truth.

### Evidence And Diagnosis

| ID | Status | Proposition | Decision implication |
| --- | --- | --- | --- |
| E1 | Observation | Project Workflow 0.8.0 main is clean at e795602 and already owns Coordinator, verification-campaign, one-QA, affected-proof, and release-state contracts. | Extend these contracts; do not create a parallel lifecycle. |
| E2 | Observation | FIX-008 and FIX-009 explicitly leave arbitrary raw host tool calls outside executable control. | Guidance and workflow next-action logic alone cannot close the recurrence. |
| E3 | Observation | The local FIX-010 prototype adds 2,061 lines across 19 files, including a 1,154-line Codex-specific supervisor, project-enforce CLI, Codex plugin hooks, fixed-candidate release logic, and 24 focused passing tests. | Reuse verified mechanisms and tests, but refactor the public architecture before integration. |
| E4 | Report supported by retained release records | The triggering release arc covered 145 paths and about 87 minutes, with most time and scope after the core behavioral result. | End-to-end execution authority, not only individual test policy, is the binding constraint. |
| E5 | Observation | Current Codex App Server exposes programmatic thread/turn events; Claude Code exposes blocking PreToolUse hooks, subagent hook coverage, print-mode budget/turn limits, tool restrictions, and streaming output. | Equivalent properties are feasible through different host mechanisms and units. |
| E6 | Unknown until implementation proof | The exact installed Claude Code runtime, version, authentication, and managed-policy behavior available for the final canary. | Provision and verify a real supported runtime before claiming Claude support; absence in one shell is setup evidence, not product infeasibility. |

### Competing Paths

| Path | Disposition | Reason |
| --- | --- | --- |
| Merge FIX-010 substantially unchanged | Rejected | It exposes a Codex-specific public product surface and does not prove the same contract in Claude Code. |
| Build a separate enforcement service or repository | Rejected | It splits workflow, candidate, packaging, and release authority and adds an operating boundary not earned by the problem. |
| Project Workflow core plus host adapters | Selected | It keeps lifecycle truth singular while allowing each host to enforce equivalent properties with native mechanisms. |

### Readiness

- Ready for owner approval: the product home, initial host scope, lifecycle boundaries, proof
  journey, invalid substitutes, and migration direction are resolved.
- Not yet ready to claim implementation or host support: that requires owner approval,
  decomposition, implementation, and real Codex and Claude Code conformance journeys.
- Binding constraint: a worker-controlled process can currently continue or broaden work after the
  useful result because no immutable end-to-end host envelope owns its remaining authority.
- Leverage point: one host-neutral sealed contract that both host adapters must enforce and report.
- Opportunity cost: this is a material Project Workflow programme, but the simpler Codex-only and
  prose-only rivals leave the demonstrated recurrence open.

## Non-Goals

- Do not merge the current FIX-010 candidate wholesale or preserve project-enforce as the public
  architecture merely because it already exists.
- Do not replace Project Workflow 0.8.0 Coordinator, intent audit, coordination state,
  verification campaign, validation-impact decision, one independent QA gate, or tracker
  lifecycle.
- Do not normalize Codex tokens, Claude dollars, turns, tool calls, or elapsed time into one false
  cross-host cost metric.
- Do not set one universal numeric ceiling for every repository or task.
- Do not let any execution limit waive required proof, close a material finding, or certify a
  release.
- Do not turn routine deterministic status, Doctor, planning, or read-only diagnosis into a model
  run.
- Do not send ordinary in-scope QA correction choices back to the owner.
- Do not claim enforcement in untrusted repositories, unsupported host versions, disabled hooks,
  raw user shells, or hosted surfaces that have not passed the capability and conformance gates.
- Do not release, publish, install into consumers, or retire the prototype branch without separate
  current delivery authority after implementation proof.

## Users & Context

- Owners need material work to stop because the product has mechanically exhausted or satisfied
  its authority, not because the owner remembered the right stop prompt.
- Coordinators need one execution path that automatically handles routine implementation and QA
  correction while returning only genuine scope, intent, risk, authority, or unsatisfied-proof
  decisions.
- Implementers need focused validation while work is mutable, without every failed check becoming
  a rejected release candidate.
- QA reviewers need one complete pass and a durable findings set; they must not become a recurring
  scheduler.
- Maintainers need Project Workflow to ship truthful Codex and Claude Code integration without
  coupling the core state model to either host.
- Projects using other hosts or no Project Workflow must remain unaffected unless and until a
  supported adapter is installed and activated.

## Repository Scope

- Primary repository: . (Project Workflow product source, CLI, schemas, managed assets, tests,
  packaging, documentation, and sanitized conformance evidence).
- Prototype evidence source: local Project Workflow branch codex/enforced-execution-envelope at
  bd78627b47c90c492cbf844231c92e4843786f94.
- Repositories touched during implementation: Project Workflow only, except disposable canary
  repositories and explicitly authorized host configuration used to prove installation.
- Strategic Advisor is a source of triggering evidence only. It receives no Project Workflow
  implementation, workflow state, or runtime dependency from this Epic.

## Candidate And Campaign Definitions

- Working revision: mutable implementation state inside a sealed execution envelope. Failed
  focused checks here are findings, not rejected release candidates.
- Verification candidate: an exact source identity bound to the existing 0.8.0 verification
  campaign. A source change creates a successor identity while retaining only still-current proof.
- QA remediation campaign: one QA verdict, one durable findings ledger, automatic bounded
  in-scope correction, and affected-proof closure. It never commissions a second broad QA.
- Release candidate: the exact clean source/artifact identity promoted only after required
  implementation, verification, QA, and affected-proof obligations pass.
- Release attempt: terminal execution over one release candidate. It can pass, fail, or report a
  bounded unchanged-input infrastructure retry; it cannot edit source, repair findings, or create
  another candidate.

## Requirements (Outcome-Focused)

- R1 — Project Workflow owns the complete capability in its repository and package. The core must
  not import or name Strategic Advisor, and no implementation or workflow artifacts for this Epic
  may be placed in Strategic Advisor.
- R2 — Extend Project Workflow 0.8.0 rather than duplicate it. Existing Coordinator, lifecycle,
  verification campaign, one-QA verdict, validation-impact decision, evidence, status, and delivery
  boundaries remain authoritative.
- R3 — Define a versioned host-neutral execution contract containing work identity, source
  identity, phase, allowed write paths, permitted operations, applicable proof obligations,
  immutable finite limits, progress state, candidate state, and typed receipt requirements. Host
  metrics remain typed rather than falsely normalized.
- R4 — Route by material effect, not by conversation location. Read-only inspection, status,
  Doctor, requirements discussion, and cheap deterministic commands remain direct. Material
  implementation, validation, QA remediation, candidate promotion, and release must enter the
  controlled path in supported trusted installations. Routing and hook checks perform no model
  invocation.
- R5 — Seal finite limits outside worker authority for observable units supported by the active
  host, including elapsed time, agent budget or turns, tool calls, test invocations, identical
  retries, worker launches, changed paths, and write scope where available. Values come from
  declared repository/work-item policy, known history, or a bounded estimate rather than a
  universal constant. Reaching a limit blocks or pauses with missing proof visible; the worker
  cannot amend the envelope or convert the stop into a pass.
- R6 — Integrate one proportionate QA remediation campaign. One broad independent QA pass creates a
  stable findings ledger; the Coordinator automatically batches authorized in-scope corrections,
  reruns only affected proof, and rechecks only unresolved named findings. A repeated broad QA,
  a fresh reviewer for the same finding set, or a no-progress repeat is denied. Continuation
  requires a named material finding with changed source/evidence and remaining envelope authority.
- R7 — Keep working revisions, verification candidates, and release candidates distinct. Focused
  implementation failures update working state rather than producing candidate-rejected churn.
  Candidate succession preserves input-current proof, groups QA corrections under the same
  remediation campaign, and promotes exactly one frozen release candidate only after all required
  obligations pass.
- R8 — Provide fixed-candidate release control integrated with existing campaign and release
  contracts. It checks clean source and retained artifact identities, runs only predeclared
  operations, records each operation once, permits only the existing bounded unchanged-input
  infrastructure recovery, and terminates without source edits, repair, new QA, or replacement-
  candidate authority.
- R9 — Expose host-neutral user commands and status as project execute --id WORK-ID and project
  release --id WORK-ID. The current workflow item supplies phase, candidate, proof, and envelope
  authority; the user does not reconstruct those as launcher flags. Host-specific launchers, hooks,
  and subprocess flags are internal adapter details and must not become a second public lifecycle.
- R10 — Implement a Codex adapter using currently supported Codex programmatic and hook surfaces.
  It must enforce the generic contract, include subordinate agent/tool activity in aggregate
  limits where observable, deny material bypass in the supported trusted configuration, interrupt
  at terminal boundaries, and emit generic receipts. Native rollout budgets may be defense in
  depth but cannot replace the full envelope.
- R11 — Implement a Claude Code adapter using supported print-mode, streaming, permission/tool,
  hook, and external timeout mechanisms. At minimum it must bind max-budget-usd and subagent spend
  where supported, max turns, write/tool policy, PreToolUse/PostToolUse events, subordinate
  activity, elapsed time, and generic receipts. Unsupported versions or managed policies fail
  closed for material work.
- R12 — Negotiate capabilities before material execution. Required controls are recorded as
  verified, unsupported, or unknown for the exact host/version/configuration. Unsupported binding
  controls block material execution with one actionable setup result; they do not silently fall
  back to prose. Cursor, GitHub Copilot, hosted variants, and other hosts remain explicitly outside
  the initial enforcement claim.
- R13 — Derive status and Doctor findings from current envelope, campaign, candidate, adapter, and
  receipt evidence. Show the one next action and exact blocker without starting work, creating
  another lifecycle, or asking the owner to manage routine failures.
- R14 — Package the core and both adapters from the Project Workflow repository. Fresh init,
  canonical upgrade, no-op upgrade, uninstall/disable, legacy preservation, generated-asset
  parity, and documentation must truthfully describe when enforcement is active and what it
  cannot cover.
- R15 — Prove property equivalence through real Codex and Claude Code canaries, not only unit tests
  or copied guidance. Both hosts must exercise direct read-only work, denied material bypass,
  focused implementation checks, duplicate-test denial, one QA finding/remediation path, affected
  proof, recursive-QA denial, release-candidate freeze, one release attempt, and terminal receipts.
- R16 — Mine FIX-010 for validated mechanisms and regressions, then explicitly disposition every
  prototype surface. Remove or replace Codex-only public naming, unscoped repository backstops,
  inactive plugin assumptions, and any behavior that cannot satisfy the generic contract.

## Acceptance Criteria (Verifiable)

- AC1: All production source, workflow state, managed assets, tests, and package metadata for the
  capability live in Project Workflow. A source scan and dependency inspection show no Strategic
  Advisor product/runtime branch or dependency.
- AC2: One versioned core contract extends the 0.8.0 Coordinator and verification campaign without
  adding a second mutable lifecycle, tracker, QA scheduler, campaign, candidate authority, or
  shared-state writer.
- AC3: Read-only status, Doctor, inspection, and cheap deterministic counter-fixtures execute
  without launching a model or creating an envelope. In a supported trusted install, equivalent
  material write/test/release attempts outside the controlled path are denied with the sourced
  command that should be used.
- AC4: Envelope tests prove immutable work/source identity, write scope, changed-path count, worker
  count, tool/test count, identical retry, elapsed, and available host-budget limits. Limit hits
  preserve missing proof and return blocked/paused rather than pass.
- AC5: A working-revision fixture can fail and correct focused tests without recording rejected
  release candidates. One verification/QA remediation lineage retains only current proof and
  produces one frozen release candidate after all required findings and proof pass.
- AC6: One independent QA pass can report multiple material findings; automatic authorized
  correction and affected proof close them. Invocation and receipt counts prove zero second broad
  QA calls, zero whole-suite reruns unless impact requires them, and denial of identical or
  no-progress remediation repeats.
- AC7: A material finding that cannot be corrected inside scope, proof, risk, authority, or the
  sealed aggregate envelope returns one precise blocker to the Coordinator. It does not silently
  stop as complete and does not offload routine fix choices to the owner.
- AC8: Release accepts only the clean frozen candidate and predeclared operations. The successful
  fixture runs each operation once; product/source failure terminates; unchanged-input
  infrastructure recovery remains bounded; and every attempted source edit, repair, QA launch, or
  replacement candidate is rejected.
- AC9: A real supported Codex canary demonstrates the complete AC3-AC8 journey, aggregates
  observable subordinate activity, interrupts at the envelope boundary, and emits receipts
  matching the generic schema.
- AC10: A real supported Claude Code canary demonstrates the same AC3-AC8 properties using current
  Claude mechanisms, including blocking tool hooks and print-mode budget/turn controls, and emits
  receipts matching the generic schema.
- AC11: A cross-host conformance suite asserts identical state transitions, denial/continuation
  decisions, candidate semantics, proof preservation, and receipt meanings while allowing
  host-specific units and telemetry.
- AC12: Unsupported, disabled, untrusted, stale-version, and managed-policy host fixtures fail
  closed for binding material controls and remain truthful about read-only availability. No
  unsupported host is advertised as enforced.
- AC13: Fresh Codex and Claude Code installation, upgrade, no-op, disable/uninstall, and packaged-
  asset parity journeys pass from retained artifacts; Doctor reports whether enforcement is
  active for the exact host/configuration.
- AC14: Every FIX-010 file and behavior has an explicit adopt/refactor/replace/retire disposition.
  The public package does not depend on project-enforce naming, a repository-local 80,000-token
  constant, or an installed-but-inactive plugin assumption.
- AC15: A sanitized recurrence journey proves the observable outcome: no model overhead on
  read-only work; no million pre-candidate rejection records; one QA/remediation campaign; one
  frozen release candidate; one terminal release attempt; no recursive repair/review/release loop;
  and concise blocked state when required proof remains.
- AC16: Automated, host-runtime, package, release, merge, installation, adoption, and owner-
  acceptance claims remain separate. Completing this Epic cannot itself authorize push, merge,
  publication, consumer rollout, or owner acceptance.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose | Dependencies |
| --- | --- | --- | --- |
| Define Host-Neutral Execution And Candidate Contract | AC1, AC2, AC3, AC4, AC5, AC7, AC11, AC12 | Extend 0.8.0 with the generic envelope, routing, progress, candidate, capability, receipt, status, and Doctor contracts without another lifecycle. |  |
| Enforce Proportionate QA Remediation And Fixed Release | AC4, AC5, AC6, AC7, AC8, AC15 | Implement the single findings/remediation campaign, affected-proof continuation, release-candidate promotion, and terminal fixed-candidate release behavior. | Define Host-Neutral Execution And Candidate Contract |
| Refactor FIX-010 Into The Codex Adapter | AC3, AC4, AC8, AC9, AC12, AC13, AC14 | Mine the verified prototype, implement current Codex enforcement, package/activate it truthfully, and retire Codex-only public architecture. | Define Host-Neutral Execution And Candidate Contract; Enforce Proportionate QA Remediation And Fixed Release |
| Build The Claude Code Adapter | AC3, AC4, AC8, AC10, AC11, AC12, AC13 | Implement current Claude Code launch, hook, aggregate-limit, capability, packaging, and receipt behavior against the same generic contract. | Define Host-Neutral Execution And Candidate Contract; Enforce Proportionate QA Remediation And Fixed Release |
| Prove Cross-Host Conformance And Delivery Boundary | AC5, AC6, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16 | Run focused and adversarial tests, real dual-host canaries, package journeys, one independent QA per child, recurrence dogfood, and explicit delivery-state evidence. | Refactor FIX-010 Into The Codex Adapter; Build The Claude Code Adapter |

## Outcome Commitment Coverage

| Commitment | Proposed Child Owners | Parent ACs | Required Disposition |
| --- | --- | --- | --- |
| OC1 — Bounded completion path | Core contract; QA/release; cross-host proof | AC2-AC10, AC15 | Material work reaches delivery or one truthful blocker through finite authority. |
| OC2 — Complete portable capability | All five children | AC1-AC16 | Each named core, adapter, packaging, and proof capability is implemented or explicitly unsupported. |
| OC3 — Success journey | QA/release; both adapters; cross-host proof | AC3-AC15 | Invocation and receipt evidence proves the full ordinary journey on Codex and Claude Code. |
| OC4 — Reject plausible but ineffective substitutes | Core contract; cross-host proof | AC2-AC15 | Bypass, candidate churn, recursive QA, proof waiver, repair-capable release, and fake host support all fail. |
| OC5 — Preserve proportionate quality and scope | All five children | AC2-AC16 | Cheap/read-only work stays cheap, required proof remains required, and unsupported hosts stay outside the claim. |
| OC6 — Honest host limits and terminal behavior | Core contract; both adapters; QA/release | AC3-AC13 | Host-specific units remain typed, sealed limits stop without passing, and capability gaps fail closed. |
| OC7 — Current authority and evidence | Core contract; prototype refactor; cross-host proof | AC1, AC9-AC16 | Owner approval, current source, official host contracts, prototype disposition, and delivery receipts remain inspectable. |

## Open Questions (Answer Needed)

- None before approval. The owner has selected Project Workflow as the product home, required Codex
  and Claude Code at minimum, rejected constant overhead, and required proportionate QA rather than
  a simple stop rule.
- Numeric limit calibration is deliberately not an owner guess at this stage. It must be derived
  during implementation from declared work scope, supported host units, suite history, and bounded
  canaries, while preserving the non-waiving invariants above.

## Decisions (Resolved)

- EPIC-018 is a new coordinated programme, not another bounded Fix: it adds a portable core,
  two host adapters, QA/remediation behavior, release control, packaging, and cross-host proof.
- Project Workflow is the only product and repository owner. Strategic Advisor remains evidence,
  not implementation scope.
- The selected architecture is one host-neutral core plus Project Workflow-owned host adapters.
- EPIC-016's exclusion of arbitrary universal usage caps remains intact. EPIC-018 adds sealed,
  work-specific, non-waiving finite authority derived from declared scope and observable host
  capability.
- EPIC-017 remains the materially expensive verification-campaign authority. EPIC-018 bounds the
  wider host execution that can otherwise implement, diagnose, remediate, re-review, and release
  around that campaign.
- Codex and Claude Code are the minimum first-release supported hosts; other hosts are not implied.
- Public commands are host-neutral; project-enforce is prototype terminology only.
- Read-only and cheap deterministic work do not incur an execution-agent launch.
- Finite limits are task/configuration evidence, not one arbitrary universal number, and never
  waive proof.
- QA is proportionate: one broad pass, a durable findings set, automatic in-scope correction,
  affected proof only, no second broad QA, and no-progress denial.
- Working failures are not release-candidate rejections. Release candidate is a late promotion
  after verification and QA obligations pass.
- Release is terminal and fixed-candidate. It has no repair, QA, or replacement-candidate authority.
- The current FIX-010 branch is a prototype source to refactor and disposition, not a merge-ready
  solution.
- Owner approval of this Epic authorizes later planning and bounded implementation only after the
  approval is recorded. Push, merge, publication, installation, consumer rollout, and owner
  acceptance remain separate authorities.

## Controls

- Falsifier: a supported host can perform a material write, broad QA, or release operation outside
  the controlled path without a denied receipt.
- Falsifier: ordinary focused test failures create release-candidate churn before the promotion
  gate.
- Falsifier: limits cause required proof or material findings to be treated as passed.
- Falsifier: one QA finding set can commission another whole-change QA or unbounded remediation.
- Falsifier: release changes source, repairs a defect, or creates a successor candidate.
- Stop condition: a required host capability is unknown/unsupported, official host behavior has
  drifted, the generic core requires host-specific product state, or the implementation would
  weaken 0.8.0 proof/QA guarantees.
- Leading indicators: denied material bypasses; zero model launches for read-only countercases;
  zero repeated broad-QA calls; bounded finding-to-affected-proof transitions; one promoted release
  candidate; one terminal release attempt; and complete typed receipts.
- Review horizon: after both real host canaries and the sanitized recurrence journey pass, before
  any merge, package release, or consumer installation decision.

## Validation Plan

- Run focused schema, routing, envelope, progress, candidate, QA, release, status, and Doctor tests.
- Retain and adapt FIX-010 adversarial cases, including identical test denial, write scope,
  subordinate activity, wall time, host budget, and fixed release.
- Add working-revision/candidate-promotion tests that assert ordinary failing checks create zero
  rejected release-candidate records.
- Run the complete QA findings/remediation journey with exact broad-QA, affected-proof, correction,
  and no-progress invocation counts.
- Run real supported Codex and Claude Code canaries in disposable repositories with equivalent
  inputs and compare state/receipt semantics.
- Run fresh install, upgrade, no-op, disable/uninstall, generated-asset parity, package build, and
  retained-artifact journeys for both adapters.
- Run the complete locked Project Workflow suite once after the candidate is frozen, one
  independent adversarial QA per child, intent/acceptance audits, strict Doctor, and diff hygiene.
- Stop with local validated evidence. Do not infer merge, release, installation, adoption, or owner
  acceptance.
