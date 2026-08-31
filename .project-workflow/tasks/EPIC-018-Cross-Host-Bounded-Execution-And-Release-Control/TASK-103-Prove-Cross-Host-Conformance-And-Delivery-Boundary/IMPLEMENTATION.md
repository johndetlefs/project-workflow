# Implementation Plan

## Summary

- Task: TASK-103
- Parent Epic: EPIC-018
- Delivery shape: sequential, bounded-return
- Candidate policy: one frozen implementation candidate followed by one independent QA findings set

## User Story

As a Project Workflow owner using Codex, I want the released execution controls to be installed, diagnosable, and proven through real bounded host journeys so material work is governed rather than merely described.

## Goal

Deliver an exact-package operator path and real-host proof, making Codex operational first while retaining truthful cross-host status.

## Approach

Keep repository-local skills as the normal Codex integration and activate the execution-control hook only inside a sealed run. Add the smallest public, host-neutral surface needed to create and diagnose that seal, then validate the exact package through disposable install and real-host journeys. Keep source, package, runtime, release, adoption, and owner-acceptance evidence separate.

## Phases

1. Align the contract and close the operator-path gap.
2. Prove exact-package Codex install, success, and interruption journeys.
3. Prove Claude Code or retain a precise current blocker, then reconcile conformance.
4. Run recurrence, package, full-regression, Doctor, and one independent QA gate.

## Parent AC Coverage

- Parent AC5, AC6: proportional recurrence and finite delivery.
- Parent AC8, AC9: agent and aggregate bounded execution.
- Parent AC11, AC12: structural cross-host conformance and truthful capability diagnosis. Parent
  AC10 remains open under TASK-102.
- Parent AC13, AC14, AC16: install, upgrade, proof-layer ledger, and retained exact-candidate evidence.
- Parent AC15: terminal release state and no repair during release.

## Acceptance Criteria

- [x] AC1: Installation and activation documentation matches runtime ownership and does not substitute plugin listing for proof.
- [x] AC2: The exact candidate supports a complete Codex install and authority-configuration journey without private state fabrication.
- [x] AC3: Real Codex success and interruption canaries produce sealed, input-bound receipts.
- [x] AC4: Claude Code equivalently passes or produces a precise current unsupported blocker.
- [x] AC5: Cross-host state and receipt semantics conform without erasing native units.
- [x] AC6: Recurrence proves proportionality, one QA lineage, one candidate, and terminal delivery.
- [x] AC7: Every claim is tied to exact source, package, runtime, and delivery-layer evidence.

## Validation

- AC1-AC2: focused documentation, command, schema, sealing, tamper, disable, status, Doctor, package-member, and generated-parity checks.
- AC3: exact-package real Codex success and interruption canaries with retained configuration, protocol observations, source identity, changed paths, metrics, evidence identity, and core receipts.
- AC4-AC5: exact current Claude capability probe and, when supported, equivalent canaries plus canonical cross-host state and receipt comparisons.
- AC6: sanitized recurrence fixtures for direct zero-call work, pre-promotion revisions, one QA lineage, one candidate, and terminal release.
- AC7: exact source/package/runtime hashes and explicit delivery-layer ledger, followed by one locked full regression and one independent QA review.

## Repository Evidence

| Repository | Source | Initial state | Delivery state | Evidence |
|---|---|---|---|---|
| `.` | PR #29 merged to `main` at `1a69bffdc674700b10b99a586c9a957d67ac1f74`; annotated tag `v0.9.2` | exact local candidate proof, one preserved independent QA findings set, and passing affected remediation proof | public Codex-certified 0.9.2 release; PyPI and GitHub hashes agree; one eligible consumer upgraded, one already current, and thirteen blocked roots unchanged | `evidence/release-rollout-v0.9.2.json`; exact-package controls/receipts; release run `33349932156` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Align Installation Contract | Make source and docs consistently describe repository skills, managed CLI, and ephemeral sealed hooks. | AC1, AC7 | Inspect public docs and exact package members. | Done | | Source, docs, tests | No | bounded-return |
| 2 | Close Operator Configuration Gap | Add the public host-neutral surface that creates, seals, disables, and diagnoses execution authority without manual hashes or private JSON. | AC2, AC5, AC7 | Run command, schema, tamper, disable, status, and Doctor fixtures. | Done | 1 | Core, CLI, generated copies, docs, tests | No | bounded-return |
| 3 | Prove Exact-Package Codex Journey | Build exact artifacts and run fresh install, upgrade, no-op, disable/re-enable, parity, Doctor/status, success, and interruption journeys. | AC2, AC3, AC7 | Inspect retained fingerprints, observations, changed paths, metrics, and receipts. | Done | 2 | Disposable proof repositories and task evidence | No | bounded-return |
| 4 | Prove Or Block Claude Code | Run the equivalent current-host journey and canaries or retain a precise capability blocker. | AC4, AC5, AC7 | Inspect executable, version, authentication, hook, permission, and runtime evidence. | Done | 2 | Disposable proof repositories and task evidence | No | bounded-return |
| 5 | Prove Conformance And Recurrence | Compare canonical cross-host semantics and run the proportionality recurrence harness. | AC5, AC6, AC7 | Inspect state comparisons and no-churn assertions. | Done | 3, 4 | Tests and task evidence | No | bounded-return |
| 6 | Freeze And Validate Candidate | Run generated parity, affected suites, exact package validation, locked full regression, and strict Doctor once. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Inspect the canonical validation campaign. | Done | 3, 4, 5 | Source, generated copies, tests, package, task evidence | No | bounded-return |
| 7 | Prepare Independent QA And Delivery Accounting | Freeze one candidate and its proof-layer ledger for the single QA findings set. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Review the QA record and delivery boundary. | Done | 6 | Task evidence and workflow state | No | bounded-return |

## Parent AC Evidence

- Parent AC5, AC8, AC9, AC11, AC12, AC13, AC14, AC15 and AC16 have current source, package,
  deterministic, or real-Codex evidence recorded in child-local artifacts.
- Parent AC6: one independent Changes Requested report is retained, all three findings have a
  passing affected-validation disposition, and no second broad QA was commissioned.
- Parent AC10 remains explicitly unproved under TASK-102 because no Claude executable is installed;
  AMD-002 removes it from this task's Codex-only release ownership without converting it to a pass.
- Merge and publication are proved at `1a69bff` / `v0.9.2`; release run `33349932156` published
  the same public wheel and sdist to PyPI and GitHub Release.
- Rollout accounting covers all 20 current Codex project entries and all 15 discovered manifests.
  Project Workflow was already current, `johndetlefs` was upgraded from the public exact version
  with a reviewed fingerprint and no-op re-plan, and thirteen dirty or ambiguous roots remained
  unchanged with matching pre/post status hashes.
- Owner acceptance remains uncredited. TASK-102, parent AC10, and EPIC-018 remain open for the
  authenticated Claude runtime proof excluded by AMD-002.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: current
- Outcome journey evidence: The exact package, real Codex success and interruption journeys,
  public release, isolated public install, and safe all-project rollout are retained in child-local
  evidence.
- Reviewer independence: One separate ephemeral read-only Codex QA context reviewed commit
  `620d1d31c7c4460c2ceb557f318aeb199db1ff75`; no source or workflow-state mutation was permitted.
- Evidence: The original report is preserved in `evidence/qa-review-v0.9.2.md`; the successor
  package and affected proof are retained in `evidence/task103-validation-v0.9.2-final.json` and
  `evidence/release-rollout-v0.9.2.json`.
- Findings: Worker authority could include Coordinator-owned coordination state; active proof
  obligations were not bound to durable verification authority; retained canary artifacts omitted
  the complete core receipts and exact sealed inputs required for independent identity validation.
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Shared runtime authorization hard-denies coordination state,
  active controls derive and require durable proof-contract and claim obligations, both final
  canaries retain complete sealed inputs and canonical receipts, 54 focused tests and all affected
  quality/package gates passed, and the successor was merged, publicly released and safely adopted
  wherever eligible.
- Second QA commissioned: No
- QA invocation count: 1
- Candidate reviewed: commit `620d1d31c7c4460c2ceb557f318aeb199db1ff75`; exact pre-remediation
  wheel `sha256:f7eadfcfad517759839ce68b80bf22dc89cf07809a1b9d6daa0fe44fe7e03e54`.
- Successor candidate: source commit `f419d5a1264cad251d7c70cae6ace9a776d64048`; exact local wheel
  `sha256:461f3ec65261bf6d5d7971a06f88c73fb71a98de16724b67f76e556ed7533069`.
- Disposition: The preserved Changes Requested verdict is closed through affected validation; it is
  not overwritten by a fictional second review.

## Retro

- Date: 2026-08-31
- Lessons: Codex installation health is repository-local skill discovery plus an exact sealed-run
  receipt, not a permanent marketplace-plugin row. The supported adapter must continue to create and
  remove its hook inside the supervised execution context.
- Lessons: Public availability needs an isolated resolver check. The first in-repository `uvx`
  attempt inherited local resolver context and returned a false missing-version result even though
  PyPI JSON and the simple index exposed 0.9.2; `--no-cache --no-config --isolated` proved the
  package correctly.
- Lessons: The attested tag workflow rebuilt and validated the exact public distribution. Its public
  archive hashes differ from the retained pre-merge candidate, so release evidence must bind both
  layers explicitly rather than describing them as the same file.
- Lessons: "Upgrade all projects" means one exact disposition per project and manifest root. It
  does not authorize overwriting dirty, stale, active-branch, duplicate-authority, or unregistered
  repositories; thirteen such roots retained byte-identical status hashes.
- Updated assets: `.project-workflow/guidance.md` now owns isolated public-package verification and
  public-artifact identity guidance; `docs/execution-control.md` already owns the non-global-plugin
  activation contract; this task retains the release and rollout receipt.
- Follow-up suggestions: TASK-102 remains the only Project Workflow host-certification follow-up.
  Each of the thirteen blocked consumer roots needs reconciliation under its own repository
  authority before rerunning the public fingerprinted upgrade.
- Missed in-scope work: None. The Codex-only release, publication, activation proof, complete estate
  accounting, and safe eligible adoption are retained. Owner acceptance and Claude certification
  were not part of the completed boundary and remain unclaimed.

## Notes

- No parallel worker surface is justified: the operator-path change, exact-package proof, and host canaries share one candidate and are sequentially dependent.
- AMD-002 authorizes TASK-103 to complete the Codex-only v0.9.2 release boundary after one
  independent QA and exact release/adoption proof. TASK-102 and EPIC-018 remain open for real Claude
  runtime certification.

## Validation Impact

- Baseline proof: sha256:2d2cb7b200e381ef7a13594460054e7880cda984c1f909a4504d240eab52e827
- Change summary: Resolve all three preserved QA findings through shared coordination-path denial, durable proof-authority binding, and complete exact-package Codex receipt evidence.
- Impact: affected
- Invalidated proof layers: qa-review, structured-evidence
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-018 Coordinator
- Change identity: sha256:53c885baa608982dd1f146317f07f44b9166bda2a1e80e78b4429d4001a884f1
