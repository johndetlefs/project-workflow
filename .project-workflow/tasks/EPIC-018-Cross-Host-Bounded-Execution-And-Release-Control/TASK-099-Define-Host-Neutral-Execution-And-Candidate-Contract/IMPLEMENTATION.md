## User Story

As a Project Workflow Coordinator, I want one sealed host-neutral execution and candidate contract,
so that material work is bounded consistently across hosts while direct read-only work stays cheap.

## Goal

Deliver the generic routing, envelope, progress, candidate, capability, receipt, preflight, status,
and Doctor foundation required by the later QA/release and host-adapter children without creating a
second lifecycle or claiming real-host enforcement.

## Approach

- Extend current 0.8.0 coordination and verification authority with compact execution references
  and derived projection rather than introducing an execution tracker or copied campaign.
- Keep generic executable contracts in packaged Project Workflow source; keep repository-local and
  managed CLI copies aligned for workflow status, Doctor, and generated assets.
- Separate deterministic classification/preflight from adapter execution so direct countercases
  incur zero model calls and unsupported material capability fails closed.
- Prove host neutrality with two fake adapters that use different native units but must return the
  same generic decisions and receipt meanings.

## Phases

1. Define and validate compact core contracts and current-state integration.
2. Add deterministic routing, sealed policy, progress, and candidate-lineage rules.
3. Add host-neutral command preflight, capability negotiation, status, and Doctor projection.
4. Align packaged/managed assets and run focused adversarial validation.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC5, AC7, AC11, AC12

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

## Acceptance Criteria

- [x] AC1: Project Workflow owns one generic contract extending the existing Coordinator/lifecycle/campaign/QA authorities with no Strategic Advisor dependency. Covers parent AC1 and AC2.
- [x] AC2: Direct read-only and cheap deterministic fixtures make zero adapter/model calls; unauthorized material actions return a stable controlled-path denial. Covers parent AC3.
- [x] AC3: Envelope identity, scope, operations, proof, and every supported finite unit are immutable and non-waiving. Covers parent AC4.
- [x] AC4: Working, verification, and release-candidate lineage remains distinct and blocks premature promotion. Covers parent AC5.
- [x] AC5: Named-progress continuation and unsupported/stale/exhausted countercases return one precise non-passing blocker. Covers parent AC7 and AC12.
- [x] AC6: Two fake adapters with different native units conform to identical generic decisions and receipt meanings. Covers the core contract portion of parent AC11 and AC12.
- [x] AC7: Host-neutral execute/release preflight, status, Doctor, and managed assets agree and repeated inspection is non-mutating. Covers parent AC3 and AC12.

## Validation

- AC1-AC7 / parent AC1, AC2, AC3, AC4, AC5, AC7, AC11, AC12: 13 focused execution-
  contract tests and the exact-current 218-test affected coordination, verification, status, and
  Doctor suite pass; all three managed CLI copies share SHA-256 `904c11a8dbfe...`; direct EPIC-018 preflight returned a
  stable zero-call/non-mutating block; parent Intent audit was current at implementation start.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/cross-host-execution-control` from `c1426f2c` | 218 affected tests pass; new-test Ruff clean; source compiles; managed CLI copies byte-identical | Local implementation only; no push/merge/release authorized | `tests/test_execution_control_contract.py`; pytest receipt from 2026-08-28; direct EPIC-018 preflight before/after SHA-256 `06315f59...` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define Core Contracts | Add versioned envelope, progress, candidate, capability, and typed-receipt validation bound to existing coordination and verification identity. | AC1, AC3, AC4, AC5, AC6 | Run valid, malformed, mutation, stale-source, and singular-authority contract fixtures. | Done |  | Packaged execution-control source and focused tests | No | bounded-return |
| 2 | Route Material Effects | Classify direct versus controlled operations deterministically and derive sealed finite policy from current work/repository inputs without model calls or universal constants. | AC2, AC3, AC5 | Run direct zero-call countercases and unauthorized material write/test/release denials. | Done | 1 | Execution router, policy validation, fixture configuration, tests | No | bounded-return |
| 3 | Track Progress And Candidates | Enforce named-progress continuation and distinct working, verification, and release-candidate lineage while preserving missing proof on every stop. | AC3, AC4, AC5 | Run working-failure, succession, premature-promotion, identical-input, no-progress, and exhausted-limit fixtures. | Done | 1, 2 | Execution state/projection and candidate-lineage tests | No | bounded-return |
| 4 | Negotiate Adapter Capability | Define exact host/version/configuration capability preflight and prove generic state/receipt equivalence with two fake adapters using different native units. | AC5, AC6 | Run verified, unsupported, unknown, stale-version, and cross-unit fake-adapter conformance fixtures. | Done | 1, 2, 3 | Adapter contract, capability/receipt schemas, conformance tests | No | bounded-return |
| 5 | Add Host-Neutral Preflight And Projection | Add `project execute --id` and `project release --id` preflight plus matching read-only status and Doctor next-action/blocker projection without exposing envelope flags. | AC2, AC5, AC7 | Exercise command, human/JSON status, Doctor, repeated non-mutation, and no-capability failure journeys. | Done | 1, 2, 3, 4 | Packaged CLI, local/template mirrors, status/Doctor, CLI tests | No | bounded-return |
| 6 | Align Assets And Adversarial Proof | Align generated CLI/package/docs surfaces and prove source ownership, no Strategic Advisor/runtime host coupling, exact parity, and all failure/counter-failure paths. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Run focused TASK-099 suite, managed-asset parity, source/dependency scans, parent Intent audit, strict Doctor, and diff hygiene. | Done | 1, 2, 3, 4, 5 | Managed assets, package metadata/docs as required, focused tests, task evidence | No | bounded-return |

## Parent AC Evidence

- AC1, AC2: Project Workflow-only source/dependency scan passes and the execution contract extends
  existing coordination state; no second tracker, lifecycle, campaign, QA verdict, or writer was
  added.
- AC3: Direct operations return zero model calls; `project execute --id EPIC-018` denied missing
  sealed authority with exit 2 and byte-identical coordination state before/after.
- AC4: Sealed identity and exact typed-limit mutation/missing-unit countertests pass; every gap is
  non-passing.
- AC5, AC7: Working/candidate lineage, named-progress, stale Git source, no-progress, premature-
  promotion, and precise blocker fixtures pass.
- AC11, AC12: Fake Codex-like token and Claude-like USD units remain distinct while generic route,
  state, denial, candidate, proof, and receipt semantics match; unsupported controls fail closed.
- Structured recipe evidence: not triggered for this fake-adapter/core-contract child; real host
  runtime/source and user-outcome journeys remain TASK-101 through TASK-103 obligations.

## Validation Impact

- Baseline proof: Independent QA Changes Requested for TASK-099 on 2026-08-28
- Change summary: Bound release readiness to current verification and QA authority, added consumed finite-limit state and sealed unresolved material findings, bound receipts to the exact envelope/capability/phase/candidate/proof set, and aligned status with Doctor next action.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-018 Coordinator
- Change identity: sha256:205936e70bc8cb5c0f173427f2ce3ac5bea7cb096f6f6813795f188e14976dec

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: current
- Outcome journey evidence: The reviewer confirmed useful generic structure and non-mutating preflight, then reproduced self-attested release readiness, a fabricated progress finding, receipt transplantation across host configurations, and divergent status/Doctor next actions.
- Reviewer independence: Fresh ephemeral read-only Codex session `01a04609-2f7e-7261-a2e1-f04ac149f6b7`; it had no implementation role and made no file changes. The independent verdict is preserved after remediation and no second QA was commissioned.
- Evidence: Independent QA report `/tmp/epic018-task099-qa.txt`; reviewer source inspection and pure adversarial probes; affected validation of the exact remediated checkout on 2026-08-28.
- Findings: High - release readiness trusted self-declared obligation strings. High - progress did not require a real unresolved material finding or consumed-limit state. High - receipts were transferable across envelopes/configurations. Medium - status and Doctor diverged on the exact next action.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Release preflight now requires the existing verification/QA projection to be delivery-ready; limits carry consumed authority and exhaust non-passing; repeats require one sealed unresolved material finding; receipts bind to the exact sealed envelope, capability, phase, candidate, and proof set; status and Doctor share the execution next action. All 13 focused tests and the exact-current 218-test affected suite pass, the new test file is Ruff-clean, source compiles, all three CLI copies are byte-identical at SHA-256 `904c11a8dbfe4004b991d4bd0b09ec5355b92e96ee1198f3a997127c44231ebb`, and `git diff --check` passes.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-099
- Title: Define Host-Neutral Execution And Candidate Contract
- Created: 2026-08-28
