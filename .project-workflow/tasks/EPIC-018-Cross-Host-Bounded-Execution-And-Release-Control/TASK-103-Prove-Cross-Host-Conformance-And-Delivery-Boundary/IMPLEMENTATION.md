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
| `.` | `codex/task-103-cross-host-conformance` from `origin/main` at `e299b0155d284764c29f3b1269f11323887792fc` | implementation through QA-remediation commit `f419d5a`; retained final evidence follows that source | exact local v0.9.2 wheel `sha256:461f3ec65261bf6d5d7971a06f88c73fb71a98de16724b67f76e556ed7533069`; not yet merged or published | `evidence/package-manifest-v0.9.2-final.json`, complete exact-wheel Codex controls/receipts, package journeys, affected validation, and preserved independent QA |

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
- Parent AC10 remains explicitly unproved under TASK-102 because no Claude executable is installed;
  AMD-002 removes it from this task's Codex-only release ownership without converting it to a pass.
- Merge, publication, rollout, adoption, and owner acceptance remain uncredited.

## QA

- Candidate reviewed: commit `620d1d31c7c4460c2ceb557f318aeb199db1ff75`; exact pre-remediation
  v0.9.2 wheel `sha256:f7eadfcfad517759839ce68b80bf22dc89cf07809a1b9d6daa0fe44fe7e03e54`.
- Successor candidate: source commit `f419d5a1264cad251d7c70cae6ace9a776d64048`; exact v0.9.2
  wheel `sha256:461f3ec65261bf6d5d7971a06f88c73fb71a98de16724b67f76e556ed7533069`.
- Reviewer independence: separate ephemeral read-only Codex QA context; no source or workflow-state
  mutation was permitted.
- Original verdict: **Changes Requested**. Preserved in `evidence/qa-review-v0.9.2.md`.
- Findings: worker authority could include Coordinator-owned coordination state; active proof
  obligations were not bound to durable verification authority; retained canary artifacts omitted
  the complete core receipts and exact sealed inputs required for independent identity validation.
- Intent adversarial verdict: the reviewed AC set could appear green while the approved user job
  remained unsafe or unproved because authority state could be mutated and receipts could not be
  independently verified.
- Current Intent audit at review: pass/current,
  `sha256:c9da28048d5bef4f79a259582d8d662190190dc0445a2fcbcd0578355e17d544`.
- Workflow validation impact: **affected** for `qa-review`, execution configuration, shared adapter
  path enforcement, proof-authority binding, the exact package, and real Codex receipts.
- Findings disposition: **Resolved**. Shared runtime authorization now hard-denies coordination
  state; active controls derive and require durable proof-contract/claim obligations; both final
  canaries retain the exact configuration, full sealed control, full core receipt, observations,
  source, package, and output identities.
- Affected validation verdict: **Pass**. Fifty-four focused tests, documentation, generated parity,
  Ruff, formatting, mypy, exact-package journeys, both real Codex canaries, and canonical
  validation of both retained controls/receipts passed. The user job cannot still remain undone
  through the three named QA gaps: **No**.
- Disposition: the original Changes Requested verdict is closed through the passing affected-
  validation record in `evidence/task103-validation-v0.9.2-final.json`; it is not replaced by a
  fictional second review verdict.
- QA invocation count: 1
- Second QA commissioned: No

## Retrospective

- Durable conventions: pending completion evidence
- Follow-up work: only evidence-backed residuals may be recorded

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
