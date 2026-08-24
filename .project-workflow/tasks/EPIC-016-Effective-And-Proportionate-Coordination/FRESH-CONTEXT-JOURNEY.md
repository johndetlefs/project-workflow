# Fresh-Context Journey

- Epic: EPIC-016
- Date: 2026-08-24
- Disposable root: `/private/tmp/pw-coordinator-core-journey.BmPfQF`
- Physical context: ephemeral Codex task `01a0320c-493b-7161-93fd-8374428659eb`
- Model: `gpt-5.4`
- Codex CLI: `0.145.0-alpha.30`

## Claim Boundary

This is one disposable context-transfer canary for Coordinator contract version `2`. It proves the
named fresh physical context could load a compact packet, verify exact authority and current
contract state, make the bounded change, record both named boundaries, and return a structured
receipt without parent conversation, owner interruption, another context, or QA. It is not a
universal reliability, billing, credit, or token-savings claim.

## Bounded Authority

- Packet: `HANDOFF.json`, sha256
  `8bfa2cad84a617fd2c98a50a775db00bbf5539ebf358bfd081b388893740759d`.
- Requirements authority: sha256
  `901cb682a7c93f36e2c6002e936bbd939c5a0ce5ac032653104064eccf01781d`.
- Allowed mutation: `fresh-context-canary.txt` and the one task's `COORDINATION.json` only.
- Invalid substitutes: parent-repository inspection, parent conversation/personal memory, another
  task/agent/QA/review, or broader mutation.

## Result

- Structured receipt: sha256
  `e5b9b567b5c83bd219dae100aa0256b124f28c28929b435710a82d3873a201eb`.
- `status`: `completed`.
- Authority hash match: `true`.
- Preflight: `current`.
- Changed paths: the allowed canary and coordination state only.
- Decisions: `before-unit-start:inside-envelope` and
  `unit-return-or-dependency-join:inside-envelope`.
- Owner questions: `0`; new contexts created: `0`; QA actions: `0`.
- Canary content: `Coordinator Core fresh-context handoff passed.`; sha256
  `cc88694a825ec8f36753db36dbdc51569a7630d5b1daf3a9efb76e39c800a617`.
- Final compact coordination state: sha256
  `7038aa98001e2eec6ded139d68b8c8ec24ecf7843474ee405b2f20f7c5899999`.

The first boundary invocation omitted required `--affected-units` and failed closed. The fresh
context read the CLI contract, retried with exact subject ownership, and then completed. No result
is inferred from the failed invocation.

## Observed Context Cost

The Codex run reported 231,944 input tokens, including 206,976 cached input tokens, plus 2,142
output tokens. These are host-observed run counters, not invoice, credit, or portable cost figures.
They materially disprove the assumption that a fresh task is inherently inexpensive: eliminating
parent conversation does not eliminate system, tool, skill, and repository startup context. The
Coordinator must therefore keep a current fit-for-purpose physical context when no named isolation,
authority, evidence, or delivery benefit outweighs transfer overhead.
