# EPIC-016 Consolidated Independent QA

Date: 2026-08-24
Reviewer: local read-only agent `/root/task093_eval_review` (`Helmholtz`)
Implementation owner: Coordinator in the current owner-facing task

## Issued Verdict

- Verdict: Changes Requested
- Intent-adversarial verdict: Fail
- Could every mapped AC pass while the approved user job remained undone: Yes
- Review count: one consolidated independent QA; no second QA was commissioned

## Blocking Findings

1. A lifecycle boundary decision survived a later coordination source revision because the gate
   checked Intent identity but not the recorded repository/source identity.
2. Retained Run 003 evaluated Coordinator contract
   `sha256:7c57de36046d1ff9c4a419a63aca4933509515d54e627ad818b05d44f40b82ad`,
   not the current candidate contract.
3. The deterministic behavioural grader ignored each scenario's `must_preserve` obligations, so a
   correct routing choice could pass while dropping return verification or another required
   capability/authority condition.

## Affected-Validation Disposition

- Finding 1 fixed: boundary decisions now record a hash over the current source revision and
  repository authority. Task and Epic lifecycle regressions reject old decisions after a source
  change and accept a newly recorded current decision.
- Finding 3 fixed structurally: the schema requires exactly two values from a global preservation
  vocabulary; the scenario-specific answer key remains outside the prompt; the grader reports both
  missing and invented controls. Explicit private alternatives cover only declared equivalent
  controls; duplicate, missing and adjacent-control counter-failures remain red.
- Focused affected validation passes `39/39` for source binding, Coordinator/Clarify contract,
  evaluator, user-outcome QA and the actual Review-to-Complete lifecycle. Canonical CLI and both
  distributed copies are byte-identical.
- Finding 2 fixed: Run 005 evaluates current contract
  `sha256:57d3ba916838d1264724737107c337cf96675631035538641b2cc674044c859c`
  twice. Both trials choose the correct routing decision in all 12 cases, including
  `contract-load-required` for the stale physical context. Strict preservation-aware scores remain
  `10/12` and `9/12`; the retained deductions and their deterministic enforcement boundaries are
  analysed in `evaluations/coordination/results/EPIC-016-ANALYSIS.md`.

## Post-Disposition Dogfood Finding

The first completion check exposed a separate deterministic contradiction: lifecycle completion
accepted only a literal independent `Pass`. A preserved `Changes Requested` verdict therefore
could not finish after its named affected validation without either rewriting history or launching
a second QA. The gate now accepts a passing final disposition only when the original verdict and
adversarial answers remain intact, findings are `Resolved`, a valid affected Validation Impact
record includes `qa-review` with verdict `pass`, substantive evidence shows the user job can no
longer remain undone, and `Second QA commissioned: No`. Missing or contradictory fields fail
closed. A full lifecycle regression proves Review-to-Complete on this path.

## Delivery Boundary

All three issued findings are resolved by affected validation. The original reviewer verdict remains
preserved as issued; this disposition is not a second QA or a rewritten reviewer opinion. The
four feature children are Complete and may proceed to the existing release/package child without
rerunning the baseline, the full suite, or independent QA. Publication and rollout remain separate
delivery gates owned by TASK-094.
