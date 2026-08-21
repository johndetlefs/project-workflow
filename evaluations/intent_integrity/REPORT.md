# Intent Integrity Behavioural Evaluation

## Claim

Within the tested local Codex CLI surface, two release trials recovered the requested outcome,
rejected five under-delivery/proxy candidates, routed the bounded copy correction through compact
controls, proposed no unrelated scope, and requested no additional approvals. This is behavioural
evidence for the recorded model and harness only; it is not proof of universal agent reliability.

## Tested Surface And Identity

- Date: 2026-08-21 (Australia/Sydney)
- Runner: OpenAI Codex CLI `0.145.0-alpha.30`, `codex exec --ephemeral`
- Model/provider: `gpt-5.6-terra` / OpenAI
- Reasoning effort: high
- Sandbox/approval: read-only / never
- Corpus: `cases.json`, SHA-256
  `cfd161417da05fa568024c5d4413bba1d0d6d90f55616126111175793aaa8cd2`
- Output schema: `output.schema.json`, SHA-256
  `81e2dcc50591f48279dd4dfb3e5e6e2073f8f07a969806385092d78f2b4aefb8`
- Expectations: `expectations.json`, SHA-256
  `be0a08f267f4493a2e934b298959114aeb779594e91a5c44591a99c57b7a8690`
- Final evaluator: `grade_results.py`, SHA-256
  `f31eb8213b40848ad8b7413d934a7f2b4b5a05b2a1e8144edcf9bce68a2344e5`
- Exact trial prompts: `prompts.json`, SHA-256
  `8e6490e4382aa4c9013f324771e1e0820c0e5848900208fe67c4fbc5da838712`
- Per-trial runtime, prompt, session and raw-result binding: `runs.json`, SHA-256
  `858f471cee4ede1991bee1074963099a9ed184bac32edf348ca14e6377e5a4f5`
- Trial 1 session: `01a021e8-4311-7b70-aa9b-3e82635efffc`
- Trial 2 session: `01a02256-0535-7060-9c99-444adf69722c`
- Trial 3 session: `01a021ec-a256-7b80-ae34-4eb467b24732`
- Run identity binds the exact prompt, runtime, session ID, raw-result hash and current evaluator.

| Trial | Role | Raw result SHA-256 | Final grade |
| ----- | ---- | ----------------- | ----------- |
| `trial-1` | calibration | `91ca20add254e7e6eba59f9be9170f9b7bc515fdc2d0ed570d166e9ab10f460f` | expected disagreement |
| `trial-2` | release repeat 1 | `0bf975dcb8e9149fea6f2a784f65bbdcb010174a07465dc59be091bf014d9739` | pass, 6/6 cases |
| `trial-3` | release repeat 2 | `ce88a048c7c74de84fc8339fbd83183ed7b9ed8da228de856805775777675959` | pass, 6/6 cases |

## Six-Axis Result

Both release repeats passed preserved intent, explicit de-scoping, capability coverage, exact
outcome proof, unnecessary scope and approval burden for every case. They selected `full` plus
`changes-requested` for the five materially incomplete candidates and `compact` plus `proceed` for
the bounded label correction. Every decision used zero approval requests.

## Calibration, False Passes And False Failures

- Trial 1 correctly treated the bounded work as compact and did not recommend gold-plating, but it
  placed examples of work to avoid in `unnecessary_scope`. The first grader treated that field as
  proposed work and failed the result. This was a schema/prompt ambiguity, not behavioural
  over-delivery. The release prompts define the field as extra work actually recommended; trials 2
  and 3 then returned an empty list.
- The initial proof scorer required the literal word `unchanged`. Trial 2 instead said to confirm
  that no behaviour or layout changes were included. That semantic pass was initially scored as a
  false failure. The expectation now tests `label` and `behaviour`, while the scorer still requires
  material-token coverage.
- A provenance-refresh trial used the equally valid spelling `behavior`. The evaluator now
  normalizes that spelling to `behaviour`; a focused regression test prevents this lexical false
  failure without weakening the required label-and-behaviour coverage.
- Trial 3 left one `explicit_descoping` array empty but its rationale explicitly said the checklist
  could pass without the invitation-to-join journey. The evaluator already permits explicit loss
  language in either the dedicated field or rationale; `without` was added to that bounded lexical
  vocabulary. Manual review confirmed the omitted journey was named.
- No final false passes were found in the six cases. This does not estimate a population false-pass
  rate; the corpus is deliberately small and adversarial.

## Evidence Boundaries

- The corpus is sanitized synthetic input, not a replay of a private task or proprietary project.
- Trials 2 and 3 are repeated executions on one model family and one local CLI version, not multiple
  independent model providers or host products.
- The lexical grader establishes inspectable minimum coverage; it does not prove semantic
  equivalence. Human disagreement review remains required.
- Structural unit/template/parser tests prove deterministic workflow behavior and are reported
  separately. They do not substitute for these agent trials, and these trials do not substitute for
  package, upgrade, consumer, deployment, owner-acceptance or commercial proof.
