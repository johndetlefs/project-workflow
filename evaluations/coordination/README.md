# Coordination behavioural evaluation

This retained corpus tests both under-processing (intent drift, proxy substitution, stale context,
missing owner authority) and over-processing (unearned context splits, redundant questions,
recursive QA). It contains sanitized synthetic scenarios rather than private task transcripts.

Run at least two isolated trials for both the baseline ref and current candidate:

```bash
.venv/bin/python scripts/run_coordination_evaluations.py \
  --model <exact-model-id> \
  --trials 2 \
  --baseline-ref origin/main \
  --output-dir <retained-output-directory>
```

Each call receives only the selected contract assets and the corpus. It runs ephemerally in a
disposable directory with project and user rules disabled. The report retains model, Codex version,
candidate/baseline identity, prompt/response/harness/corpus hashes, per-scenario grading and any
reported usage. Results are scoped to that exact model, harness, corpus and candidate; they do not
prove universal reliability, a bill, account credits, or token savings.

The model must also select exactly two controls from one global preservation vocabulary. The
deterministic grader compares those controls with each scenario's private `must_preserve` values.
The prompt does not expose the scenario-specific answer key, while the exact-two schema prevents a
response from selecting every control; duplicate selections still fail the private expected-set
comparison. A correct routing decision therefore cannot pass while
silently dropping the capability, authority, return-verification, or stop condition that matters.
Where two global controls express the same scenario-specific obligation, the corpus may declare a
private `preservation_alternatives` equivalence. The grader accepts only those explicit alternatives;
an adjacent but non-equivalent control still fails. This prevents arbitrary wording from becoming
a false negative without converting free-text reasons into a subjective grader.

After a retained baseline run, an affected candidate-contract correction may use
`--condition candidate` to repeat only candidate trials. Compare it with the retained baseline only
when corpus and baseline contract hashes match, the baseline prompt is unchanged, and the retained
responses reproduce the same grades under the current grader; record those checks in the analysis.
If the grader adds a new required response field, do not claim that an older baseline proves that
new dimension. Compare only unchanged dimensions and treat the stricter candidate run as additional
candidate evidence unless the baseline is explicitly rerun.
