# Fix

## Summary

- Fix: FIX-005
- Title: Harden Workspace Journey Proof
- Status: Complete
- Created: 2026-07-29

## Report

- Observed or requested: EPIC-009 was closed with AC11 described as a disposable CLI journey from declaration through handoff, but the retained evidence only summarized isolated fixture tests. Workspace-specific coverage also omitted an operationally unavailable registered repository, and closeout records contained a test-count inconsistency plus an apparent approval inconsistency requiring schema verification.
- Expected: Retain a genuine disposable CLI lifecycle journey with generated artifacts and before/after Git evidence, directly cover unavailable repository status, make every EPIC-009 closeout claim match the proof, and preserve the correct Epic approval semantics.
- Affected users or systems: The owner relying on Project Workflow workspace mode and reviewers relying on EPIC-009 acceptance evidence.
- Delivered baseline: EPIC-009 on `codex/BL-017-workspace-mode`, based on `9c329aaa6a66ccba62c25c704ea071419cbe7911`, with the workspace implementation locally complete.
- Report evidence: Owner review on 2026-07-29; `tests/test_workspace_mode.py`; EPIC-009 AC11, TASK-059 validation plan, `EVIDENCE.json`, and `evidence/final-validation.json`.

## Routing

- Decision: Fix
- Rationale: One bounded post-completion proof and regression correction; no workspace architecture or product outcome changes.
- Related work state: EPIC-009 Complete locally; not committed, pushed, merged, released, deployed, or adopted in the JohnDetlefs workspace.
- Bounded correction: Add the missing journey and unavailable-state proof, repair the evidence record, and refresh EPIC-009 audit/closeout.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: The implementation may be sound, but acceptance evidence currently overstates operator-journey coverage.
- Urgency: Resolve before committing or releasing BL-017.
- Owner: Project Workflow maintainer

## Related Work

- Originating work: EPIC-009 Workspace Mode And Multi-Repo Coordination
- External links: None

## Risk

- Risk level: Low
- Risks: Integration-fixture lifecycle requirements may expose a real workflow defect; evidence edits could become stale if source changes afterward.
- Rollback or containment: Revert this bounded Fix while retaining the existing EPIC-009 implementation for further review.

## Fix Plan

- Scope: Add one subprocess-driven disposable workspace journey through task creation, approval/readiness, status, repository evidence, Testing, Review, Complete, and handoff inspection; add unavailable-repository regression coverage; retain journey artifacts and Git-state receipt; correct EPIC-009 proof records.
- Non-goals: No workspace redesign, real JohnDetlefs mutation/adoption, automatic validation runner, cross-repository Git actions, push, merge, release, or deployment.
- Affected target: Project Workflow tests and EPIC-009/FIX-005 evidence artifacts.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: `codex/BL-017-workspace-mode`; PR not created; FIX-005 evidence directory and EPIC-009 TASK-059 evidence.
- Verification plan: Run the retained CLI journey, focused workspace tests, compilation/parity, full locked Python 3.10 suite, package build, structured-evidence validation, Doctor, Fix lifecycle gates, and refreshed EPIC-009 audit/closeout.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/BL-017-workspace-mode` | Not created | FIX-005 and EPIC-009 TASK-059 evidence artifacts |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/BL-017-workspace-mode`; PR #10 merged to `main` at `7c42360aaad43f209a651ad48fdffe23c6a7a303` | 14 focused workspace cases, retained CLI journey, 262-test locked suite, compilation, Ruff, package build, backlog validation, Doctor, parity, diff check, public package journeys, artifact identity, and SLSA provenance passed | Included in public `v0.3.0` on PyPI and GitHub Release; no JohnDetlefs repository mutation or adoption/deployment was performed | `evidence/disposable-cli-journey.json`; EPIC-009 TASK-059 `evidence/release-0.3.0.json`, `evidence/final-validation.json`, and `EVIDENCE.json` |

## Verification

- Delivered scope: Added subprocess-driven CLI lifecycle proof, retained generated handoff artifacts, direct unavailable-repository status coverage, and corrected EPIC-009 evidence counts/claims.
- Verification result: Pass. The actual CLI completed init, approval, readiness, focused status, Testing, Review, and Complete across a disposable parent/next/email workspace; all retained hashes match.
- Adjacent behavior checked: Single-repository compatibility, registry safety, child-authority rejection, dirty/detached/branch-mismatch status, evidence gates, upgrade preservation, release contract, package build, and the full regression suite.
- Original acceptance criteria result: EPIC-009 AC11 now has the required retained CLI journey; AC7 now directly covers unavailable repository status; AC12 remains bounded read-only real-target proof.
- Regression evidence: `tests/test_workspace_mode.py` has 14 passing cases; the complete Python 3.10 suite has 262 passing tests.
- Residual risk: Real JohnDetlefs adoption and mutation remain intentionally unproven and require separate owner authority. The parent Epic approval field remains correctly `No` for direct implementation because the approved scope envelope authorizes unchanged child implementation.

## QA & Code Review

- Date: 2026-07-29
- Reviewed areas: Subprocess journey isolation, generated-helper invocation, repository scope/evidence lifecycle gates, Git non-mutation comparisons, unavailable status handling, retained artifact hashes, EPIC-009 structured evidence, package parity, and proof boundaries.
- Validation evidence: 14 focused cases and 262 full-suite tests passed; Ruff, compilation, build, backlog validation, diff check, Doctor, source/helper parity, retained-artifact hash verification, and structured-evidence validation passed.
- Findings: None blocking. The apparent Epic approval inconsistency was disproven by source inspection and is documented as correct schema behavior.
- Verdict: Pass.

## Outcome

- Disposition: Fixed
- Decision: Replaced aggregated fixture claims with a retained generated-helper lifecycle journey, added unavailable-repository regression coverage, and corrected EPIC-009 evidence.
- Closed by: Codex for repository owner
- Closed date: 2026-07-29
- Promoted to: None

## Retro

- Date: 2026-07-29
- Reusable lesson: When an acceptance criterion names an end-to-end operator journey, retain the actual CLI command sequence, resulting workflow artifacts, repository-state comparisons, and source/helper identity; a matrix of isolated fixtures is supporting regression evidence, not a substitute.
- Durable guidance: `.project-workflow/guidance.md` already owns this exact automated-fixture versus manual-journey distinction, so no duplicate guidance change was added.
- Follow-up: Real JohnDetlefs workspace adoption remains a separate owner-authorized lifecycle action.
- Missed in-scope work: None remains after FIX-005.
