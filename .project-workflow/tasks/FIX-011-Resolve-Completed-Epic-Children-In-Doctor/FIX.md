# Fix

## Summary

- Fix: FIX-011
- Title: Resolve completed epic children in Doctor
- Status: Review
- Created: 2026-11-11
- Intent contract: compact

## Intent

Restore Doctor and verification inspection for completed epic children, preserving their parent ownership and proof. Closing a child must not make its existing coordination evidence unresolvable.

## Report

- Observed or requested: Doctor cannot resolve a completed epic child after closing Massey TASK-009.
- Expected: Completed children remain inspectable while normal status lists remain active-only.
- Affected users or systems: Repositories using epic children with coordination verification state.
- Delivered baseline: Project Workflow 0.10.0, source 9bdcf26.
- Report evidence: Owner reported Massey TASK-009 closeout; source _verification_work_item_layers falls back only to global rows.

## Routing

- Decision: Fix
- Rationale: One bounded defect in already delivered lifecycle lookup.
- Related work state: Not identified
- Bounded correction: Resolve terminal epic children through authoritative trackers without changing lifecycle gates.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: Doctor reports invalid coordination evidence after valid child closure.
- Urgency: Normal; prepare review before any new release.
- Owner: John Detlefs

## Related Work

- Originating work: Not identified
- External links: None

## Risk

- Risk level: Low
- Risks: Incorrectly broadening active status or silently selecting duplicate work IDs.
- Rollback or containment: Revert this isolated branch; no consumer installations are changed.

## Fix Plan

- Scope: Lifecycle lookup, regression tests and generated runtime mirrors.
- Non-goals: No release, version bump, repository upgrades, Massey workflow mutations or unrelated warning cleanup.
- Affected target: Verification projection and Doctor for terminal epic children.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: codex/fix-completed-epic-child-lookup; review pending.
- Verification plan: Reproduce terminal child failure, exercise active and terminal parents and duplicate IDs, confirm active-only status unchanged, run quality gates and one full suite, verify a disposable Massey workflow copy, obtain independent QA.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | codex/fix-completed-epic-child-lookup | Draft review pending | Tests and Outcome Journey below |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/fix-completed-epic-child-lookup | 594 tests and all contributor gates pass | Candidate only, not merged or released | Regression tests and Outcome Journey below |

## Verification

- Delivered scope: Terminal-aware authoritative lifecycle lookup for verification and Doctor; active-only status remains unchanged.
- Verification result: 594 tests passed in 101.77s, including UVX packaging; lint, formatting, mypy, documentation, generated-runtime parity and diff checks passed. Doctor clean with 69 accepted historical warnings hidden.
- Adjacent behavior checked: Completed children under active/completed parents retain provenance; duplicate global/epic IDs fail closed; global terminal lookup remains covered; active-only summaries exclude completed children.
- Original acceptance criteria result: Not applicable
- Regression evidence: New terminal epic-child test failed before implementation with the reported missing-item error and passes after correction; 33 focused verification/status tests pass; actual disposable consumer closure journey passes (below).
- Residual risk: Unreleased candidate only. Existing installations retain the defect until a separately approved release and upgrade; no release or consumer upgrade is authorized now.

## Outcome

- Disposition: Pending
- Decision: ____
- Closed by: ____
- Closed date: ____
- Promoted to: None

## Outcome Journey

- Baseline: canonical consumer snapshot b66d596, copied with workflow and referenced docs to a disposable directory. Live consumer files and installed runtime were not modified.
- Candidate command: `project epic status --epic-id EPIC-001 --id TASK-009 --to Complete` using candidate source changed Review to Complete through the normal gates and refreshed the acceptance map.
- Candidate Doctor after closure: no issues found.
- Released 0.10.0 bundled Doctor on the same completed snapshot: exactly one blocking error, `Operational lifecycle contains 0 work items named TASK-009; exactly one is required`.
- Repeated Complete request is rejected by the existing Review-only closure gate; no force or gate bypass was used.
- This proves the restored closure/inspection journey, not publication, installation, rollout, or owner acceptance of a new release.

## QA & Code Review

- Verdict: Pass
- Reviewer: Independent read-only reviewer, separate from implementation.
- Reviewed scope: Canonical lookup, collector opt-in, provenance, default active status, duplicate-ID safety and generated mirrors.
- Evidence: Independent terminal regression run: 3 passed; Doctor clean with 69 accepted warnings hidden; diff hygiene and generated mirror parity passed. Full-suite condition satisfied by 594 passing tests.
- Findings: None.
- Delivery boundary: Review only. Owner acceptance, merge and release remain pending.
