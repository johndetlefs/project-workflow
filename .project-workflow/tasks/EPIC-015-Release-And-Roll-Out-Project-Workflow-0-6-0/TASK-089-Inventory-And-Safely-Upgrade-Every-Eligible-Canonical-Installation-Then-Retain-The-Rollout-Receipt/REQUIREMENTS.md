# Requirements

## Summary

- Task: TASK-089
- Title: Inventory and safely upgrade every eligible canonical installation, then retain the rollout receipt
- Parent AC Coverage: AC5, AC6, AC7
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Classify every currently saved project, upgrade each safe canonical Project Workflow installation from the proven public 0.6.0 package, and retain exact results while leaving unsafe or non-installed projects untouched.

## Intent Spine

- OC1 — Completion capability: Every saved project has a disposition and every safe canonical installation is validated at 0.6.0.
- OC2 — Material capabilities: Fresh inventory, preflight safety, public-package plan/apply, scoped diff, no-op plan, Doctor and machine-readable receipt.
- OC3 — Success journey: Re-read inventory, recheck each root, mutate only eligible roots, validate each result and record all dispositions.
- OC4 — Successful-but-wrong result: Adoption count rises by installing into non-consumers, touching dirty roots or accepting unvalidated partial upgrades.
- OC5 — Exclusions: Do not commit, push, deploy, clean user work, create duplicate authorities or force blocked upgrades.
- OC6 — Assumptions: TASK-088 proves public 0.6.0 and eligibility can change until immediately before mutation.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
- Requirements reviewed by owner: Inherited from parent epic envelope when unchanged
- Acceptance criteria reviewed by owner: Inherited from parent epic envelope when unchanged
- Approved for decomposition: Not applicable
- Approved for implementation: Yes, inherited from parent epic envelope
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-21
- Approval note / source: Owner explicitly requested updates to every project that has Project Workflow.
- Approved artifact identity: Inherited from current parent requirements identity

## Goal

Complete safe, evidence-backed adoption across the current saved-project estate.

## Non-Goals

- Installing Project Workflow in non-consumers, mutating blocked roots, or integrating consumer diffs.

## Users & Context

The owner has multiple concurrent repositories whose user-owned changes and authority boundaries must be preserved.

## Repository Scope

- Primary repository: .
- Repositories touched: Only saved local roots with canonical manifests and passing immediate safety checks.

## Requirements (Outcome-Focused)

- Give every saved project an explicit current disposition.
- Upgrade only clean, attached, unambiguous canonical roots using public project-workflow==0.6.0.
- Prove preservation, expected diff, version 0.6.0, no-op re-plan and applicable Doctor per successful root.
- Retain a machine-readable release and rollout receipt mapping parent evidence and unresolved boundaries.

## Acceptance Criteria (Verifiable)

- AC1: The refreshed inventory and receipt cover every project; every eligible canonical root is validated at 0.6.0; every blocked/non-installed root is unchanged with a concrete disposition; no consumer changes are committed, pushed or deployed.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Safety is rechecked immediately before each upgrade and any ambiguity fails closed.

## Validation Plan

- Snapshot inventory, branch/status/root/manifest before mutation, run exact public plan/apply/no-op plan, inspect scoped diff and run Doctor, then verify blocked roots remained untouched.
