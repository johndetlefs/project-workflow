# Fix

## Summary

- Fix: FIX-008
- Title: Bound Continuation And Validation Scope
- Status: Complete
- Created: 2026-08-21
- Intent contract: compact

## Intent

Make Project Workflow stop implementation and review once the approved intent and required proof
are satisfied, while still reopening genuinely material defects. Limit revalidation to the proof
layer affected by a change so rigor does not turn into low-value repeated work.

## Report

- Observed or requested: The owner reported recurring overly granular investigation and validation
  after useful outcome proof had already been obtained.
- Expected: Agents stop after the approved completion envelope passes, reopen only for material
  findings, route adjacent improvements to follow-up, and rerun only affected proof layers.
- Affected users or systems: Project Workflow owners and agents using implementation and QA guidance.
- Delivered baseline: EPIC-014 intent-integrity controls and FIX-007 are complete in the current
  uncommitted local candidate.
- Report evidence: Owner review in the current Codex task; EPIC-014 R10/AC10-AC12; FIX-007 closeout
  showed a material correction followed by release-grade validation despite no release request.

## Routing

- Decision: Fix
- Rationale: One post-completion process defect with one guidance/evaluation correction and no new
  lifecycle, schema, approval or product decision.
- Related work state: EPIC-014 and FIX-007 Complete
- Bounded correction: Add continuation materiality and affected-proof validation boundaries to the
  existing Implement/QA guidance, plus a sanitized counter-scenario regression.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: Agents can consume owner time and tokens on non-material follow-on work or repeat broad
  validation after the approved outcome is already proven.
- Urgency: Normal; correct before the EPIC-014 candidate is released.
- Owner: Project Workflow maintainer

## Related Work

- Originating work: EPIC-014 Intent Integrity And Outcome Proof
- External links: None

## Risk

- Risk level: Medium
- Risks: A stopping rule could reintroduce under-delivery if it treats a material contradiction as
  optional, or could remain ineffective if it is only aspirational prose.
- Rollback or containment: Revert the bounded guidance/evaluation changes. Material owner-outcome,
  false-claim, required-lifecycle and safety/data risks remain explicit reopen conditions.

## Fix Plan

- Scope: Add a concise sufficiency/materiality rule to existing Implement and QA assets for Codex,
  Claude Code, Cursor and GitHub Copilot; add sanitized regressions that reject both overcooking a
  non-material post-pass finding and ignoring a material contradiction.
- Non-goals: No new CLI lifecycle state, schema, approval field, dashboard, evidence document stack,
  full Epic, live model-trial claim, release, publication or rollout.
- Affected target: Packaged and repository-local Implement/QA agent guidance and intent-integrity
  behavioural-evaluation fixtures/tests.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Branch `codex/intent-integrity-outcome-proof`; no PR; focused test
  and strict Doctor evidence will be recorded here.
- Verification plan: Run focused host-asset and intent-behaviour tests, confirm source/local mirror
  alignment, run the full suite once because packaged agent assets changed, then strict Doctor and
  `git diff --check`. Do not rebuild or rerun release package journeys.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/intent-integrity-outcome-proof` | None | Focused tests, one full-suite pass, strict Doctor and diff inspection |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof`; no PR | Focused policy/host tests 4/4; full suite 426/426; strict Doctor and `git diff --check` pass | Local candidate only; no commit, merge, release, publication or rollout | `tests/test_continuation_sufficiency.py`; `evaluations/intent_integrity/continuation-cases.json`; Implement/QA source and local mirrors |

## Verification

- Delivered scope: Implement and QA guidance now stop after the current completion envelope passes,
  reopen only for explicit material conditions, route non-material findings to follow-up, and bind
  revalidation to the affected proof layer. Two sanitized scenarios preserve both sides.
- Verification result: Pass. Focused policy and four-host install tests passed 4/4; the complete
  repository suite passed 426/426 once; source/local prompt mirrors are byte-identical; skill
  mirrors differ only by the generated ownership marker; strict Doctor and diff hygiene pass.
- Adjacent behavior checked: Disposable Codex, Claude Code, Cursor and GitHub Copilot installs all
  receive the policy in both Implement and QA assets. Existing intent-integrity trials and all
  workflow tests remain green.
- Original acceptance criteria result: Pass — EPIC-014 R10 and AC10-AC12 now cover continuation
  sufficiency as well as initial routing/gold-plating behavior.
- Regression evidence: `test_continuation_cases_reject_both_overcooking_and_premature_stopping`,
  packaged/local parity coverage, four-host installation coverage, and the 426-test full suite.
- Residual risk: The fixtures prove the shipped contract and discriminate the two counter-cases;
  they do not claim live-model behavior improvement. Reassess that at the next release evaluation,
  without reopening this Fix or running release-grade package journeys now.

## Outcome

- Disposition: Fixed
- Decision: Project Workflow now stops after sufficient intent and proof, reopens only for material findings, and revalidates only affected proof layers.
- Closed by: Codex
- Closed date: 2026-08-21
- Promoted to: None
