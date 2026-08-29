## User Story

As a Project Workflow Coordinator, I want one bounded QA/remediation and fixed-release controller,
so that routine findings close without recursive QA and release cannot become another repair loop.

## Parent AC Coverage

- AC4, AC5, AC6, AC7, AC8, AC15

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

## Acceptance Criteria

- [x] AC1: One source-bound independent QA verdict creates one durable multi-finding ledger and denies a second broad QA.
- [x] AC2: Only sealed unresolved in-scope findings can continue through changed-source/evidence correction and affected proof; invalid/no-progress/exhausted cases block precisely.
- [x] AC3: Current authoritative implementation, verification, QA and affected proof promote exactly one source/artifact-bound release candidate.
- [x] AC4: One fixed release executes predeclared argv operations once, with only one unchanged-input infrastructure retry, and returns exact terminal counts.
- [x] AC5: Mutation, repair/QA/replacement authority, product-failure retry, second attempt and candidate substitution fail closed.
- [x] AC6: Status, Doctor and retained receipts agree on the bounded journey and show no recursive QA/release loop.

## Validation

- AC1-AC6 / parent AC4, AC5, AC6, AC7, AC8, AC15: 14 focused QA/release tests and
  the exact-current 232-test affected execution, coordination, verification, status and Doctor
  suite pass. The affected Ruff scope is clean, source compiles, `git diff --check` passes, and all
  three managed CLI copies share SHA-256
  `4f461c94f4d3a6faff909971b75bf0ab6fabc7840d2565f2b7477accd804ae6b`.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/cross-host-execution-control` from `c1426f2c` | 232 affected tests pass; affected Ruff scope is clean; source compiles; managed CLI copies byte-identical | Local implementation and disposable fixed-release fixtures only; no push/merge/publication/install authorized | `tests/test_qa_release_control.py`; public CLI persistence fixture; affected pytest receipt from 2026-08-28; CLI SHA-256 `4f461c94f4d3...` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define QA Campaign State | Add one source-bound findings ledger, one-QA accounting, derived blockers and input-bound receipts in existing coordination state. | AC1, AC2, AC6 | Run multiple-finding, duplicate-QA, malformed and state-projection fixtures. | Done | | Packaged/managed CLI and focused tests | No | bounded-return |
| 2 | Enforce Bounded Remediation | Authorize only sealed unresolved in-scope findings, require progress, record correction/affected proof and reject identical, unknown, broad or exhausted repeats. | AC1, AC2, AC6 | Run success, out-of-scope, identical/no-progress, exhausted and no-recursive-QA fixtures. | Done | 1 | QA campaign transitions and tests | No | bounded-return |
| 3 | Bind Candidate Promotion | Derive one candidate promotion from existing current implementation/verification/QA/affected-proof authority plus exact source/artifact identities. | AC3, AC6 | Run premature, stale, duplicate and successful promotion fixtures. | Done | 1, 2 | Candidate transition and tests | No | bounded-return |
| 4 | Execute Fixed Release | Validate clean candidate/artifacts and execute predeclared argv operations once without shell, repair, QA or successor-candidate authority. | AC4, AC5 | Run success, mutation, prohibited-operation, product failure and second-attempt fixtures. | Done | 3 | Fixed release controller and tests | No | bounded-return |
| 5 | Bound Infrastructure Retry And Receipts | Permit one unchanged-input infrastructure retry, terminate every other failure, and bind receipt identity to candidate, plan, inputs and exact counts. | AC4, AC5, AC6 | Run unchanged retry, changed-input denial, retry exhaustion and receipt tamper fixtures. | Done | 4 | Release receipts and tests | No | bounded-return |
| 6 | Align Projection And Proof | Align CLI copies/docs/status/Doctor, run focused and affected validation, current Intent audit, strict Doctor and independent QA. | AC1, AC2, AC3, AC4, AC5, AC6 | Run exact affected suite, asset parity, diff hygiene and adversarial review. | Done | 1, 2, 3, 4, 5 | Managed assets, docs, task evidence | No | bounded-return |

## Parent AC Evidence

- AC4, AC5: Typed consumed limits and sealed finding authority from TASK-099 now feed the one-QA
  campaign; ordinary remediation never creates release candidates.
- AC6, AC7: Two material findings close from one verdict through input-bound correction and
  affected-proof receipts. Duplicate QA, unknown/unsealed/out-of-scope/no-progress findings,
  wrong phase and exhausted authority fail with precise non-passing errors.
- AC8: Disposable clean Git candidates and the public `project release` surface prove durable
  consumption before invocation and one terminal receipt. One infrastructure exit is retried once;
  interruption, forged receipts, non-Git source, empty/unbound artifacts, product failure, source
  mutation, prohibited QA/repair naming, and a second attempt fail without repair or replacement.
- AC15: Focused receipts assert exactly one broad-QA invocation, zero release QA invocations, one
  candidate identity, one terminal attempt, exact operation counts, zero source repairs and zero
  replacement candidates. The complete sanitized real-host recurrence journey remains TASK-103.
- Structured recipe evidence: not triggered for this generic controller/fake-operation child; real
  host runtime, packaged activation and broader outcome-journey claims remain TASK-101 to TASK-103.

## Validation Impact

- Baseline proof: d85c387882aa3a51c5187a9d4ae1ff832a6132ad471a114833154f516ffd9927
- Change summary: Resolved the five independent QA findings with durable pre-invocation release consumption, typed terminal receipts, fail-closed Git and artifact binding, sealed remediation limits, and input-bound promotion proof
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: Coordinator affected remediation 2026-08-28
- Change identity: sha256:14d83bba5b0130f300a4a69abe2a9a3b389b826885b662d9faa747c538b4986d

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: current
- Outcome journey evidence: The reviewer reproduced a non-Git release pass, a forged terminal-pass projection, replayable release after interruption, remediation beyond exhausted authority, and promotion from opaque proof labels.
- Reviewer independence: Fresh ephemeral read-only Codex session `01a04625-d09d-7043-89c8-c53c4bad3210`; it had no implementation role and made no file changes. The independent verdict is preserved after remediation and no second QA was commissioned.
- Evidence: Independent QA report `/tmp/epic018-task100-qa.txt`; reviewer source inspection and two non-writing adversarial probes; affected validation of the exact remediated checkout on 2026-08-28.
- Findings: High - release attempt/operation consumption was not durable before subprocess execution. High - terminal receipts were untyped and forgeable. High - Git, artifact and promoted-candidate identity checks failed open. High - remediation did not enforce phase, permission or exhausted limits. High - affected-proof closure and candidate promotion accepted self-attested labels.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Release now persists running and per-operation consumption before invocation, rejects every resumed consumed attempt, and persists one typed hash-bound terminal receipt through the public CLI. Git/source readability, non-empty content-addressed artifacts and promoted artifact-set identity fail closed. QA remediation requires the sealed phase, permission, remaining limits, one attempt per finding, and passing input-bound remediation/affected-proof receipts. Promotion binds current coordinated source and derives implementation, verification, QA and affected-proof identities from authoritative proof. All 14 focused tests and the exact-current 232-test affected suite pass; source compiles, the affected Ruff scope is clean, all three CLI copies are byte-identical at SHA-256 `4f461c94f4d3a6faff909971b75bf0ab6fabc7840d2565f2b7477accd804ae6b`, and `git diff --check` passes.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-100
- Title: Enforce Proportionate QA Remediation And Fixed Release
- Created: 2026-08-28
