# Epic Contract

## Summary

- Epic: EPIC-018
- Title: Cross-Host Bounded Execution And Release Control
- Last updated: 2026-08-28

## Sources of Truth

- Owner meaning and approval boundary: REQUIREMENTS.md and the Project Workflow approval thread
  created for EPIC-018.
- Stable product outcomes and proportionality constraints: .project-workflow/CONSTITUTION.md.
- Current lifecycle, Coordinator, and execution-surface foundation:
  ../EPIC-016-Effective-And-Proportionate-Coordination/.
- Current verification-campaign, candidate, typed-receipt, one-QA, and release projection
  foundation: ../EPIC-017-Proportionate-Verification-Lifecycle/.
- Current post-proof stopping foundation:
  ../FIX-008-Bound-Continuation-And-Validation-Scope/ and
  ../FIX-009-Enforce-Proportionate-Post-Proof-Validation/.
- Current Project Workflow implementation baseline:
  e795602a591cee0ef1c9b1bb50164749a85d0085 on fetched origin/main.
- Prototype evidence only: local Project Workflow branch codex/enforced-execution-envelope at
  bd78627b47c90c492cbf844231c92e4843786f94.
- Current host contracts:
  https://developers.openai.com/codex/app-server,
  https://developers.openai.com/codex/hooks,
  https://code.claude.com/docs/en/hooks, and
  https://code.claude.com/docs/en/cli-reference.
- Triggering evidence class: the sanitized 145-path, roughly 87-minute release recurrence and the
  AC15 cross-host journey. No private transcript is a runtime or package dependency.

## Invalid Substitutes

- Another instruction, prompt, checklist, approval step, or status field saying that agents should
  stop.
- Merging FIX-010 unchanged, exposing project-enforce as the portable public product, or treating
  one local Codex canary as cross-host proof.
- A separate enforcement repository, service, or workflow writer that owns its own candidate,
  findings, QA, or release truth.
- A universal token/time/test number presented as proportionate control.
- A stop rule that leaves material findings or required proof for the owner to resolve manually.
- Repeating broad QA after correction instead of retaining one findings set and validating affected
  proof.
- Calling every mutable implementation/test revision a release candidate.
- Treating a failed or exhausted envelope as a pass, completion, or release authorization.
- A release command that can edit source, install fixes, commission QA, or mint a successor
  candidate.
- Static Codex or Claude assets, fake hooks, mocked CLI output, or package presence without a real
  supported-host journey.
- Claiming that a repository-local hook covers untrusted repositories, disabled plugins, user
  shells, hosted surfaces, or managed policy that prevents the hook.
- Host-metric normalization that presents Codex tokens, Claude dollar budget, turns, or elapsed time
  as interchangeable.
- Project Workflow production code, workflow state, or managed assets placed in Strategic Advisor.

## Invariants

- Project Workflow remains the only product owner, repository owner, Coordinator, lifecycle,
  verification campaign, QA verdict, candidate authority, and shared-state writer.
- Read-only and cheap deterministic work does not launch another model or require campaign
  ceremony.
- Material work in a supported trusted installation cannot mutate, validate broadly, remediate QA,
  promote a candidate, or release outside the controlled path.
- The worker cannot amend its sealed execution identity, write scope, permitted operations, proof
  obligations, or finite limits.
- Limits pause or block and keep missing proof visible; they never manufacture a pass.
- One independent QA pass creates one durable findings set. In-scope remediation is automatic and
  bounded; only affected proof and unresolved findings are rechecked; a second broad QA is
  prohibited.
- Continuation requires named material progress. An identical or no-progress repeat is denied.
- Working revisions, verification candidates, and release candidates have distinct semantics.
- Release candidate promotion occurs only after all required implementation, verification, QA, and
  affected-proof obligations pass.
- Release runs predeclared operations against one clean frozen candidate and has no source repair,
  QA, or replacement-candidate authority.
- Host adapters enforce the same decisions and receipt meanings but may use different native units
  and mechanisms.
- Unsupported or unknown binding host capability fails closed for material work and cannot be
  advertised as supported.
- Codex and Claude Code are the minimum initial supported hosts. No other host inherits the claim.
- All shipped core and adapter assets come from the Project Workflow repository and package.
- Automated, host-runtime, package, merge, publication, installation, adoption, effectiveness, and
  owner-acceptance proof remain separate.

## Artifact Targets

- Versioned host-neutral execution-envelope, progress, candidate, capability, and typed-receipt
  schemas integrated with the 0.8.0 Coordinator and verification campaign.
- Deterministic material-work router plus host-neutral project execute and project release CLI
  surfaces.
- Immutable envelope supervisor/controller with aggregate progress, denial, interruption, and
  terminal receipt behavior.
- One QA findings/remediation campaign integrated with affected-proof validation and no-recursive-
  QA enforcement.
- Working-revision, verification-candidate, release-candidate, and fixed release state/commands.
- Codex adapter and managed installation assets using current supported Codex programmatic/hook
  mechanisms.
- Claude Code adapter and managed installation assets using current supported print-mode,
  streaming, permission/tool, hook, budget/turn, and timeout mechanisms.
- Capability preflight, status, Doctor, diagnostics, disable/uninstall, and truthful unsupported
  state.
- FIX-010 disposition map covering every prototype file, behavior, test, CLI, hook, and repository
  backstop.
- Sanitized cross-host conformance corpus, real Codex and Claude Code canary receipts, recurrence
  journey, package/fresh/upgrade/no-op/disable evidence, and explicit delivery boundary.
- Aligned source, generated assets, README, CHANGELOG, package metadata, tests, schemas, and
  repository-local mirrors.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1, AC2 | Define Host-Neutral Execution And Candidate Contract | Source/dependency scan plus lifecycle/campaign singularity tests. |
| AC3, AC4 | Define Host-Neutral Execution And Candidate Contract | Direct read-only countercases, material bypass denials, immutable-limit and blocked-proof receipts. |
| AC5, AC7 | Define Host-Neutral Execution And Candidate Contract; Enforce Proportionate QA Remediation And Fixed Release | Working-revision/candidate-lineage tests, progress requirements, and exact blocked disposition. |
| AC6 | Enforce Proportionate QA Remediation And Fixed Release | One-QA findings ledger, automatic correction, affected-proof, no-progress, and invocation-count evidence. |
| AC8 | Enforce Proportionate QA Remediation And Fixed Release; Prove Cross-Host Conformance And Delivery Boundary | Clean candidate, once-only operations, failure termination, bounded infrastructure recovery, and prohibited-authority tests. |
| AC9 | Refactor FIX-010 Into The Codex Adapter | Real supported Codex canary, subordinate aggregation, interruption, receipt, and install evidence. |
| AC10 | Build The Claude Code Adapter | Real supported Claude Code canary, hook/budget/turn/tool/timeout receipt, and install evidence. |
| AC11 | Build The Claude Code Adapter; Prove Cross-Host Conformance And Delivery Boundary | Cross-host state, denial, candidate, proof, and receipt conformance matrix. |
| AC12 | Define Host-Neutral Execution And Candidate Contract; both host adapters | Unsupported/version/trust/policy fixtures and truthful capability/status results. |
| AC13 | Both host adapters; Prove Cross-Host Conformance And Delivery Boundary | Retained-package fresh/upgrade/no-op/disable journeys and Doctor activation state. |
| AC14 | Refactor FIX-010 Into The Codex Adapter; Prove Cross-Host Conformance And Delivery Boundary | Complete prototype disposition map plus source/package scans rejecting retained lock-in assumptions. |
| AC15 | Prove Cross-Host Conformance And Delivery Boundary | Sanitized recurrence journey with exact model, QA, proof, candidate, release, and loop counts. |
| AC16 | Prove Cross-Host Conformance And Delivery Boundary | Proof-layer ledger and local-only delivery receipt that stops before external actions. |
