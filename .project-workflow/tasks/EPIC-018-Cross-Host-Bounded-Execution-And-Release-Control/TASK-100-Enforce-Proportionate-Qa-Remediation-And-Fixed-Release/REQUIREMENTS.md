# Requirements

## Summary

- Task: TASK-100
- Title: Enforce Proportionate QA Remediation And Fixed Release
- Parent AC Coverage: AC4, AC5, AC6, AC7, AC8, AC15
- Last updated: 2026-08-28
- Intent contract: full

## Intent

Give the Coordinator one durable QA findings campaign that authorizes bounded in-scope correction,
rejects recursive or no-progress remediation, promotes exactly one sufficiently proven candidate,
and executes a terminal fixed-candidate release without repair or replacement authority.

## Intent Spine

- OC1 — Completion capability: one independent QA verdict becomes one durable findings set;
  authorized corrections close through affected proof, then one exact candidate may be promoted and
  subjected to one terminal release attempt.
- OC2 — Material capabilities: versioned QA/remediation and fixed-release state; finding identity,
  scope and disposition; one-QA invocation accounting; progress-aware continuation; authoritative
  promotion; clean source/artifact verification; once-only operations; typed terminal receipts.
- OC3 — Success journey: a multi-finding QA verdict is recorded once; two in-scope findings receive
  changed-source/evidence corrections and affected proof; no second broad QA runs; one release
  candidate is promoted; every declared release operation runs once against unchanged inputs.
- OC4 — Successful-but-wrong result: findings exist only in prose, correction can repeat unchanged,
  a whole-change QA is commissioned again, promotion trusts self-attestation, or release edits
  source, repairs a failure, retries product failure, or creates a successor candidate.
- OC5 — Exclusions: no host launch mechanics, real Codex/Claude support claim, package publication,
  merge, consumer installation, or owner acceptance in this child.
- OC6 — Assumptions: the existing verification projection and independent QA record remain the
  authorities; host adapters later execute exact authorized corrections; infrastructure retry is
  allowed only once for unchanged inputs and never waives failed proof.
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
- AC5, AC7: owner `Define Host-Neutral Execution And Candidate Contract; Enforce Proportionate QA Remediation And Fixed Release`; required evidence: Working-revision/candidate-lineage tests, progress requirements, and exact blocked disposition.
- AC6: owner `Enforce Proportionate QA Remediation And Fixed Release`; required evidence: One-QA findings ledger, automatic correction, affected-proof, no-progress, and invocation-count evidence.
- AC8: owner `Enforce Proportionate QA Remediation And Fixed Release; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Clean candidate, once-only operations, failure termination, bounded infrastructure recovery, and prohibited-authority tests.
- AC15: owner `Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Sanitized recurrence journey with exact model, QA, proof, candidate, release, and loop counts.

## Goal

Close the loop between one independent QA verdict and a frozen releasable candidate without creating
another QA scheduler or letting release become a repair loop.

## Non-Goals

- Do not run Codex or Claude Code or claim host enforcement.
- Do not rerun broad QA after correction; retain the original verdict and findings.
- Do not make a release failure mutable or authorize source repair.
- Do not perform any external release, push, merge, publication, installation, or rollout.

## Users & Context

- Coordinators need routine in-scope findings resolved without another owner checkpoint.
- QA reviewers need one verdict to remain authoritative rather than becoming a recurring worker.
- Release operators need one clean candidate and predeclared operations with terminal outcomes.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1: Store one versioned QA campaign in existing coordination state with exactly one broad-QA
  invocation, a source-bound verdict identity, named material findings, correction and affected-
  proof receipts, and a derived non-passing/ready state.
- R2: Only sealed, unresolved, material, in-scope findings may authorize remediation. Continuation
  requires changed source or evidence; identical/no-progress repeats and exhausted authority block.
- R3: Retain the original QA verdict. Corrections close findings through affected proof and must not
  commission a second broad QA or a whole-suite rerun unless the existing impact authority requires it.
- R4: Promote one release candidate only when implementation, current verification, QA, affected
  proof, source identity, and artifact identity are authoritative and passing.
- R5: A fixed release plan contains one candidate, clean source identity, content-addressed
  artifacts, finite elapsed authority, predeclared argv operations, and at most one unchanged-input
  infrastructure retry per operation.
- R6: Release verifies source/artifacts before and after every operation, runs without a shell,
  terminates on product/source failure, rejects repair/QA/replacement operations, and writes one
  typed input-bound receipt with exact invocation and retry counts.
- R7: Status and Doctor derive the same campaign, promotion, and release blocker/next action without
  launching a model or mutating state during inspection.

## Acceptance Criteria (Verifiable)

- AC1: One QA verdict records multiple source-bound findings once; a second broad-QA record is denied.
- AC2: Authorized in-scope correction plus affected proof closes findings; unknown, out-of-scope,
  identical, no-progress, and exhausted-limit attempts remain non-passing with one precise blocker.
- AC3: Working failures create no release-candidate churn; promotion occurs once and only from the
  current delivery-ready verification/QA authority and exact source/artifact identity.
- AC4: Fixed release runs every predeclared operation once against a clean frozen candidate, permits
  only one unchanged-input infrastructure retry, and emits exact terminal counts.
- AC5: Source/artifact mutation, repair/QA/replacement operation names, product-failure retry, second
  release attempt, and candidate substitution are rejected without creating another candidate.
- AC6: Status, Doctor, campaign receipts, and focused fixtures prove one QA invocation, affected-only
  continuation, one promoted candidate, one terminal release attempt, and no recursive loop.

## Open Questions (Answer Needed)

- None. Host-specific correction execution remains adapter work; external delivery remains separately
  authorized after the Epic's proof gates.

## Decisions (Resolved)

- The QA campaign and fixed release are extensions of COORDINATION state, not new trackers.
- Release commands are argv arrays executed without a shell; repair, QA, and candidate-management
  operations are invalid even when declared.
- Infrastructure retry is classified explicitly and is never available for product/source failure.
- This child proves the controller with disposable repositories and fake operations only.

## Validation Plan

- Run focused state, no-progress, promotion, clean-candidate, once-only, mutation, retry, terminal-
  receipt, status and Doctor fixtures; rerun the affected execution/coordination/verification/status
  suite; run strict Doctor and independent adversarial QA.
