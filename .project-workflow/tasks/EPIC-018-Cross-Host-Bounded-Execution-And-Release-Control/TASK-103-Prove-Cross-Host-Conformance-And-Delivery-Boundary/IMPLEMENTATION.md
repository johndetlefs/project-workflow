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
- [ ] AC6: Recurrence proves proportionality, one QA lineage, one candidate, and terminal delivery.
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
| `.` | `codex/task-103-cross-host-conformance` from `origin/main` at `e299b0155d284764c29f3b1269f11323887792fc` | implementation commit `4316548` plus AMD-002/version candidate | exact local v0.9.2 wheel `sha256:f7eadfcfad517759839ce68b80bf22dc89cf07809a1b9d6daa0fe44fe7e03e54`; not yet merged or published | `evidence/package-manifest-v0.9.2.json`, exact-wheel real Codex canaries, package journeys, full validation, and proof-layer ledger |

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

- Candidate: exact local v0.9.2 wheel `sha256:f7eadfcfad517759839ce68b80bf22dc89cf07809a1b9d6daa0fe44fe7e03e54`
- Findings set: not commissioned
- Disposition: Testing. AMD-002 removes parent AC10 from this task's release ownership while keeping
  TASK-102 blocked truthfully. Exact 0.9.2 package, Codex runtime, recurrence, and validation proof
  pass; parent AC6 and Review remain pending the one independent QA findings set.
- QA invocation count: 0
- Second QA commissioned: No

## Retrospective

- Durable conventions: pending completion evidence
- Follow-up work: only evidence-backed residuals may be recorded

## Notes

- No parallel worker surface is justified: the operator-path change, exact-package proof, and host canaries share one candidate and are sequentially dependent.
- AMD-002 authorizes TASK-103 to complete the Codex-only v0.9.2 release boundary after one
  independent QA and exact release/adoption proof. TASK-102 and EPIC-018 remain open for real Claude
  runtime certification.
