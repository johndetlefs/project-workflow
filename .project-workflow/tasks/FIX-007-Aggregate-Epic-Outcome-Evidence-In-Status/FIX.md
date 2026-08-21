# Fix

## Summary

- Fix: FIX-007
- Title: Aggregate Epic Outcome Evidence In Status
- Status: Complete
- Created: 2026-08-21
- Intent contract: compact

## Intent

Make Epic operational status report the passing QA, structured outcome proof and owner-acceptance
state already established by its completed children. A parent in Closeout must not ask for new
external evidence when the governed acceptance audit and child evidence already satisfy the claim.

## Report

- Observed or requested: EPIC-014 reached Closeout with all five children Complete and all fifteen
  parent ACs passing, yet focused status reported parent QA `not-recorded`, structured evidence
  `pending`, outcome proof `not-recorded`, and requested external evidence.
- Expected: Epic status aggregates valid completed-child QA and structured proof, reports the
  resulting outcome/acceptance state, and sources the result to child artifacts.
- Affected users or systems: Project Workflow maintainers and agents using focused Epic status to
  choose the next governed action.
- Delivered baseline: EPIC-014 local candidate after its acceptance audit and closeout passed.
- Report evidence: `workflow status --id EPIC-014 --strict --format json` contradicted
  `workflow epic closeout --epic-id EPIC-014 --complete` on the same artifacts.

## Routing

- Decision: Fix
- Rationale: One post-completion status aggregation defect with one implementation path and no new
  product decision.
- Related work state: EPIC-014 Complete; defect found during its final closeout verification.
- Bounded correction: Aggregate child QA, valid structured evidence recipes and outcome/owner-
  acceptance states for Epic work items instead of validating a nonexistent parent IMPLEMENTATION.md.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: Status gives a false external-authority action after governed child evidence and parent
  acceptance already pass, wasting review effort and contradicting closeout.
- Urgency: High before this candidate is released because the defect is in newly added status logic.
- Owner: Project Workflow maintainer

## Related Work

- Originating work: EPIC-014 outcome-state status work and final dogfood closeout
- External links: None

## Risk

- Risk level: Low
- Risks: Incorrect aggregation could accept invalid child evidence, hide pending owner acceptance,
  or change Task/Fix status behavior.
- Rollback or containment: Keep the correction Epic-only; retain existing Task, Fix and Epic-child
  validation paths; fail closed when child documents or evidence are missing or invalid.

## Fix Plan

- Scope: Add one shared Epic-child evidence view, aggregate passing child QA/recipes/outcome state,
  and cover valid, invalid and pending-owner-acceptance cases.
- Non-goals: Change closeout authority, weaken child validation, manufacture owner acceptance, or
  alter publication/release state.
- Affected target: `src/project_workflow/cli.py` and its two byte-identical mirrors, operational
  status tests, exact-package evidence and local Fix records.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Branch `codex/intent-integrity-outcome-proof`; no PR; linked local
  evidence in this Fix and EPIC-014 acceptance/QA artifacts.
- Verification plan: Reproduce the false parent state; add regression coverage for aggregated Pass,
  pending acceptance and invalid evidence; run focused tests, full suite, strict Doctor, mirror
  parity, exact-package journeys and focused status on a Closeout Epic fixture.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/intent-integrity-outcome-proof` | None | FIX-007 regression tests and validation receipt |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof`; no PR | 423 tests pass; focused operational-status set 80/80; strict Doctor and `git diff --check` pass; three CLI mirrors are byte-identical; exact retained wheel journey passes across four hosts | Local candidate only; no commit, merge, publication, release or rollout | `tests/test_user_outcome_journey.py`; EPIC-014 `ACCEPTANCE-AUDIT.md`; TASK-084 `evidence/package-journeys.json`; direct real-artifact classifier output |

## Verification

- Delivered scope: Epic status now aggregates tracker-bound completed-child QA, validates child
  structured evidence before using it, projects outcome/owner-acceptance state from valid journey
  records, and fails closed for missing or stale child proof.
- Verification result: Pass. Against EPIC-014's actual artifacts, every proof layer reports Pass and
  outcome state is `outcome-proven` / `not-required`; the earlier false external-evidence action is
  no longer produced by the classifier.
- Adjacent behavior checked: Task, Fix and Epic-child status paths remain unchanged; pending required
  owner acceptance remains `ready-for-owner-acceptance`; a stale artifact hash yields `invalid` and
  a failing structured-evidence layer; exact-package init/upgrade/legacy/no-op journeys pass.
- Original acceptance criteria result: Pass — EPIC-014 AC9 now distinguishes implemented,
  outcome-proven, owner-acceptance and delivery states at the parent Epic level without requesting
  evidence already satisfied by validated child records.
- Regression evidence: `test_epic_status_aggregates_completed_child_qa_and_outcome_evidence` plus
  79 adjacent operational-status/outcome tests, the 423-test full suite, and the retained exact-
  package receipt `sha256:a43a54d5ee80dbef2e6e6cb2af3dd08039d5fae7bd84484e83c9baf6fcb84d1c`.
- Residual risk: Completed Epics are intentionally absent from active-work status selection, so the
  real EPIC-014 Closeout state is re-evaluated through the same classifier API and covered by a
  disposable Closeout regression rather than by reopening the completed Epic. Publication,
  consumer adoption and broader behavioural reliability remain unproven.

## Outcome

- Disposition: Fixed
- Decision: Epic status now aggregates validated completed-child QA and outcome evidence, preserves pending owner acceptance, and fails closed on invalid child proof.
- Closed by: Codex
- Closed date: 2026-08-21
- Promoted to: None
