# EPIC-016 Behavioural Evaluation Analysis

Date: 2026-08-24
Model: `gpt-5.4`
Codex CLI: `0.145.0-alpha.30`

## Retained Runs

- `EPIC-016-run-001` is invalid effectiveness evidence because its prompt leaked the answer key.
- `EPIC-016-run-002` is the answer-key-free paired baseline and early candidate. Baseline and
  candidate each scored `10/12` and `11/12` under the original routing/process grader. It exposed a
  real unnecessary owner question for clear proxy drift.
- `EPIC-016-run-003` scored `12/12` and `11/12` after that Clarify correction, but independent QA
  proved its contract hash predates the reviewed candidate and its grader ignored preservation
  obligations. It remains historical evidence for that exact contract only.
- `EPIC-016-run-004` introduced the strict preservation-aware grader. Initial attempts exposed an
  incompatible model cache and an unsupported `uniqueItems` response-schema keyword. After the
  harness was made observable and compatible, the two current-then candidate trials scored `7/12`
  and `8/12`. Both incorrectly continued when repository files were current but the physical
  context had not loaded the current contract.
- `EPIC-016-run-005` is the affected candidate-only rerun after the owning behavioral correction. Candidate
  contract `sha256:57d3ba916838d1264724737107c337cf96675631035538641b2cc674044c859c`,
  prompt `sha256:765a6fb588305153dbd23b6889e6eadae028c4946b4d26087234ef7d1a43088e`,
  corpus `sha256:a1bbe2f625e9e30b1acb6bfa662f9d5d999cbfeb3f997241087b55abcab6e403`.
  The strict scores are `10/12` and `9/12`; all 12 routing decisions are correct in both trials.
  A later deterministic completion-gate correction updated QA resolution guidance after this hash;
  its affected proof is the retained-Changes-Requested lifecycle regression, not another broad
  behavioral run.

## QA Corrections

The final harness requires exactly two globally enumerated preservation controls and privately
checks them against each scenario's `must_preserve` obligations. Explicit private alternatives are
allowed only where two controls entail the same scenario-specific obligation; missing obligations,
adjacent controls and duplicate selections still fail counter-tests. The prompt receives no
scenario-specific answer key. Harness
`sha256:9dbe3054623b7826bc08a5c439057013121affc2a5296dbf5738b8a45c216c73` and schema
`sha256:59e358e7ca9d10521e7fe3e478e34c797155a836d41de208572cb26a4a9474eb`.

The contract now makes three previously implicit consequences explicit:

- repository upgrade without an explicit physical-context load blocks as
  `contract-load-required`; it does not force an unearned fresh context;
- an ambiguous affected branch remains blocked while its one material owner question is answered;
- autonomous inside-envelope continuation removes generic reapproval, not the existing later QA
  gate.

Run 005 proves the stale-context correction in both trials and retains the Water drift, bounded
topology, owner-only proof and no-recursive-QA routing decisions.

## Residual Variance

Run 005 has no wrong routing decision, context count, QA action, or drift/stop action. Its strict
deductions are retained rather than tuned away:

- one trial omitted `existing QA later` from its two metadata controls, although the contract and
  lifecycle keep that QA gate;
- both trials selected `one focused question` plus `affected branch waits` for mid-Epic ambiguity
  rather than also selecting the redundant `drift-ambiguity` label; the decision and reason both
  identified the ambiguity;
- one Water response selected the editable/restore controls but omitted the descendant-block label;
  `drift-detected` still blocks through the deterministic lifecycle gate;
- one owner-only response chose `await-owner-judgment` with both owner-only controls but counted no
  literal question.

These are evidence of model/output variability, not universal reliability. They remain visible in
the strict score. They do not invalidate the feature claim because the required next action was
correct in every scenario and the omitted action consequences are independently enforced rather
than entrusted to the explanatory labels.

## Comparison Boundary

The retained Run 002 baseline remains useful only for unchanged routing, owner-question, QA and
context dimensions. It was not asked for preservation controls, so it is not assigned a score on
that newer dimension and was not rerun. Run 005 therefore establishes current-candidate behaviour;
it does not manufacture a strict baseline comparison.

| Evidence | Trial scores | Correct routing decisions | Complete strict trials |
| --- | --- | ---: | ---: |
| Retained baseline, old dimensions | `10/12`, `11/12` | retained old grader | not comparable |
| Run 004, strict pre-correction | `7/12`, `8/12` | `11/12`, `11/12` | `0/2` |
| Run 005, strict corrected candidate | `10/12`, `9/12` | `12/12`, `12/12` | `0/2` |

## Usage And Verdict Boundary

Run 005 reported 33,398 input tokens (3,840 cached), 3,922 output tokens and 2,279 reasoning-output
tokens. These are raw per-call telemetry, not a bill, credit balance or stable savings estimate.

The behavioral candidate has repeated, answer-key-free evidence for correct coordination decisions,
including the prior QA blocker. The later QA-completion delta has deterministic lifecycle proof
that a retained Changes Requested verdict resolves once without another QA. Together with grader
counter-tests, this is sufficient for the feature claim without pretending every later documentation
sentence was rerun through the model. It does not prove perfect model explanations, universal
reliability, publication, adoption, billing, credits, or token savings.
