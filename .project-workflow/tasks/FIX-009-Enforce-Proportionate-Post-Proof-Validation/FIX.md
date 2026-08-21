# Fix

## Summary

- Fix: FIX-009
- Title: Enforce Proportionate Post-Proof Validation
- Status: Review
- Created: 2026-08-21
- Intent contract: compact

## Intent

After a proof gate has passed, make Project Workflow invalidate only the proof layers a later
change can materially affect and direct the agent to the smallest sufficient revalidation. Prevent
both automatic full re-review and unproved continuation by stopping briefly when impact is unclear.

## Report

- Observed or requested: The 0.6.0 release candidate passed its complete automated, package and
  four-host validation matrix, but the workflow still prompted an unbounded independent
  adversarial review instead of deciding which proof had actually been invalidated.
- Expected: A compact, governed impact decision records `unaffected`, `affected`, or `ambiguous`.
  Unaffected proof advances, affected proof is validated once, and ambiguity asks one owner
  question. The decision never creates or reopens QA.
- Affected users or systems: Project Workflow owners and agents continuing after a proof gate.
- Delivered baseline: FIX-008 supplies advisory sufficiency guidance and two static fixtures, but
  no executable scope decision. EPIC-015/TASK-086 exposes the resulting whole-review default.
- Report evidence: Owner-observed dogfood failure in the current Codex task; FIX-008 residual risk;
  TASK-086 pending broad independent-QA language; current operational `qa-review` action.

## Routing

- Decision: Fix
- Rationale: This is one post-completion workflow regression with one stop mechanism and one
  focused regression family. It does not create a new product outcome or evidence-document stack;
  the owner approved the three-outcome stop gate on 2026-08-21.
- Related work state: FIX-008 Complete; EPIC-015/TASK-086 Review and release work paused
- Bounded correction: Add one deterministic validation-impact decision, reuse the existing proof
  layers and QA section, scope the operational next action from that decision, and exercise the
  exact green-release continuation failure.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Regression
- Mode: Normal
- Severity: High
- Impact: Agents can waste substantial owner time and tokens on broad duplicate review, or respond
  by skipping validation that a material change actually invalidated.
- Urgency: Correct and prove before continuing the 0.6.0 integration lifecycle.
- Owner: Project Workflow maintainer

## Related Work

- Originating work: FIX-008 Bound Continuation And Validation Scope; EPIC-015 Release And Roll Out Project Workflow 0.6.0
- External links: None

## Risk

- Risk level: High
- Risks: Semantic impact can still be misclassified, and raw host calls remain outside workflow
  enforcement. The stop gate therefore asks once when ambiguous and never authorizes review.
- Rollback or containment: Revert the compact command/status/template changes. Ambiguous impact
  remains fail-closed, and existing QA requirements remain authoritative until the decision passes.

## Fix Plan

- Scope: Add a compact `validation impact` command with only unaffected, affected and ambiguous
  outcomes; record it in the existing work-item document; permit one named affected validation;
  make passed validation terminate continuation for the same change identity; prohibit the impact
  decision from creating or reopening QA; update focused regressions and managed guidance.
- Non-goals: No generalized evidence ledger, new proof-layer taxonomy, automatic semantic inference
  from paths, host-level tool authorization, consumer rollout, or re-review of EPIC-014.
- Affected target: CLI decision engine and operational action resolver; task/epic-child templates;
  packaged and repository-local Implement/QA guidance; focused behavioral tests.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Branch `codex/intent-integrity-outcome-proof`; no PR or external
  delivery action is authorized by this Fix.
- Verification plan: Run decision-engine and operational-action tests, the exact release dogfood
  regression, managed-asset parity/install tests, strict Doctor and diff hygiene. Run the full suite
  once only because CLI and packaged managed assets change; do not rebuild release artifacts or
  repeat four-host package journeys until the impact decision says that layer is affected.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/intent-integrity-outcome-proof` | None | Focused tests, one full-suite pass, strict Doctor and diff inspection |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof`; no PR | 79/79 focused stop-gate/status tests; final locked suite pending; CLI mirrors and diff hygiene pass | Local candidate only; no integration, release, publication or rollout | `tests/test_continuation_sufficiency.py`; `tests/test_operational_status_actions.py`; `evaluations/intent_integrity/continuation-cases.json`; TASK-086 `Validation Impact` |

## Verification

- Delivered scope: One deterministic validation-impact command records the passing baseline, exact
  later change, unaffected/affected/ambiguous outcome, invalidated proof layers, validation verdict
  and stable change identity in the existing work-item document. It contains no QA scope.
- Verification result: Focused stop-gate/status coverage passes 79/79; source/template/local CLI
  hashes match; affected-pending requests one named validation, affected-pass and unaffected return
  no continuation action on repeated evaluation, and ambiguity asks the owner once.
- Adjacent behavior checked: Validation impact cannot waive the existing QA gate, cannot generate a
  review action, and malformed or incoherent decisions fail closed.
- Original acceptance criteria result: FIX-008's stop/reopen and affected-layer boundaries remain,
  but their previously advisory enforcement gap is corrected by this executable decision.
- Regression evidence: Seven sanitized continuation cases; three-outcome invalid-input matrix;
  compact command recording; repeated affected-pass stop regression; managed four-host policy
  installation. One final full-suite and package pass remains before release.
- Residual risk: Project Workflow cannot prevent arbitrary raw host tool calls outside its governed
  commands. It can stop recommending them and prohibit them in managed guidance. Because packaged
  CLI and guidance changed, final release artifacts and package journeys must be rebuilt once.

## Outcome

- Disposition: Pending
- Decision: ____
- Closed by: ____
- Closed date: ____
- Promoted to: None

## Validation Impact

- Baseline proof: FIX-008 complete with 426/426 and advisory sufficiency policy
- Change summary: Replace recursive review scheduling with a three-outcome stop gate
- Impact: affected
- Invalidated proof layers: implementation
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: Codex
- Change identity: sha256:fa36e38a49ca9fc4e5734cd216616acf5a3aa3884671b942c374512de4a3de5a
