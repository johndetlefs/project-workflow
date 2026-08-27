## User Story

As a Strategic Advisor maintainer, I want the live runner to select, bound, stop, resume and regrade
work standalone, so that costly evaluation cannot silently become an unbounded release loop.

## Parent AC Coverage

- AC9, AC14

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

## Acceptance Criteria

- [x] AC1: Current workflow guidance is adopted without a runtime dependency. Covers parent AC9.
- [x] AC2: Exact/metadata/failed/affected selection is deterministic and validated. Covers parent AC14.
- [x] AC3: Failure/call/time limits stop and checkpoint non-passing work. Covers parent AC14.
- [x] AC4: Content-addressed resume rejects stale inputs. Covers parent AC14.
- [x] AC5: Typed outcomes, retry and per-case telemetry are truthful. Covers parent AC14.
- [x] AC6: Evaluator regrade uses retained outputs with zero target calls. Covers parent AC14.
- [x] AC7: Standalone and generic optional output both pass without imports. Covers parent AC9, AC14.

## Validation

- AC1-AC7 / parent AC9, AC14: canonical 0.7.0 upgrade/no-op proof, deterministic runner tests,
  repository validation, standalone execution, generic receipt, and import/dependency scan.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| `/Users/johndetlefs/repos/strategic-advisor` | `codex/proportionate-verification-runner` at `82b44a0aabe81662917c44b8e99d3a2a6fd021c4`, from `6d65830f` | Canonical 0.7.0 upgrade/no-op; 17 focused runner tests, 188-test full suite and seven validation scopes pass | Local commit only; no push/merge/release/install authorized | `tests/test_run_drift_smoke_live.py`; standalone/generic runner receipt; source scan. Doctor retains pre-existing TASK-030 owner evidence error `5a72e9e18b52ab71`. |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Adopt Current Workflow Guidance | Upgrade the independent consumer worktree to Project Workflow 0.7.0 and verify the no-op plan separately from repository health. | AC1 | Run canonical upgrade and no-op plan/Doctor evidence. | Done | TASK-095, TASK-096 | Strategic Advisor managed workflow assets | No | bounded-return |
| 2 | Add Selection And Limits | Implement deterministic case/metadata/failed/affected selection, fail-fast/max-failures, call/time limits and explicit non-passing checkpoint state. | AC2, AC3 | Run focused synthetic runner fixtures. | Done | 1 | Strategic Advisor live runner and tests | No | bounded-return |
| 3 | Bind Resume And Outcomes | Add content-addressed checkpoints, per-case telemetry, typed failures and bounded infrastructure retry. | AC4, AC5 | Run stale/current resume and failure-type fixtures. | Done | 2 | Strategic Advisor live runner and tests | No | bounded-return |
| 4 | Add Regrade And Generic Output | Regrade retained transcripts without target calls and expose optional generic capabilities/receipt JSON while preserving standalone CLI. | AC6, AC7 | Run regrade counters, standalone invocation and dependency scan. | Done | 2, 3 | Strategic Advisor runner, tests and docs | No | bounded-return |
| 5 | Validate Independent Consumer | Run focused and repository validation and retain exact source/adoption/decoupling receipts. | AC1-AC7 | Inspect validation and sanitized receipts; do not claim release. | Done | 1, 2, 3, 4 | Strategic Advisor evidence and implementation notes | No | bounded-return |

## Parent AC Evidence

- AC9, AC14: Strategic Advisor upgraded independently to 0.7.0 managed guidance; runner remains outside the shipped skill runtime and imports no Project Workflow code. Selection, fail-fast, explicit limits, content-addressed resume, typed telemetry/retry, request binding and zero-target regrade pass 17 focused and 188 full tests.

## Validation Impact

- Baseline proof: Independent QA Changes Requested for TASK-097 on 2026-08-27
- Change summary: Reset limit accounting for evaluator-only regrade, bound generic stage and complete session/read evidence into checkpoint identity, normalized malformed prior failures, and added every missing limit/currentness countercase.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-017 Coordinator
- Change identity: sha256:09485989161fb1d63b437cc5870f09e7f7b10d4e6c909defb509c89596fb1fb7

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: current
- Outcome journey evidence: The reviewer accepted standalone/no-dependency operation and typed finite controls, then reproduced failed-output regrade exhaustion, stage relabelling, mutable session/read evidence and unstable malformed-failure handling.
- Reviewer independence: Isolated read-only `codex exec` reviewer session `24674`; it did not author or modify the candidate, run paid/live campaigns, or rerun broad suites.
- Evidence: Independent QA transcript `/private/tmp/sa-epic017-qa.txt`; pure zero-cost counterprobes; affected runner tests and repository validation; frozen local source commit `82b44a0aabe81662917c44b8e99d3a2a6fd021c4`.
- Findings: High - retained product-failure telemetry blocked evaluator-only regrade. High - adapter stage was omitted from the stored campaign identity. High - session ID and successful runtime reads were not content-addressed. High - parent Intent audit was stale. Medium - malformed prior failing IDs escaped as `TypeError`. Medium - elapsed and diagnostic failure limits lacked focused fixtures.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Failed-output regrade now makes zero target calls; stage changes fail currentness; session/read tampering fails closed; malformed prior failures are typed; target, elapsed and diagnostic failure caps all stop non-passing. 17 focused tests, 188 full tests and all seven validation scopes pass.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-097
- Title: Add Standalone Reference-Consumer Runner Controls
- Created: 2026-08-27
