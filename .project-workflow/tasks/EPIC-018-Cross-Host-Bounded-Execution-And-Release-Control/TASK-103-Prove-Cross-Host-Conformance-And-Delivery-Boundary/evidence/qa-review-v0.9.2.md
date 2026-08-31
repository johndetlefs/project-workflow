# Independent QA Review — v0.9.2 pre-remediation candidate

- Date: 2026-08-31
- Reviewer: separate read-only Codex QA context
- Candidate commit: `620d1d31c7c4460c2ceb557f318aeb199db1ff75`
- Candidate wheel: `sha256:f7eadfcfad517759839ce68b80bf22dc89cf07809a1b9d6daa0fe44fe7e03e54`
- Verdict: **Changes Requested**
- Broad QA invocation: 1 of 1

## Findings

1. High — Worker write authority could include a real Coordinator-owned `COORDINATION.json` path.
   The operator guard used incomplete placeholder matching, while both adapters treated a matching
   coordination path as allowed at tool time and excluded it from Git/change accounting.
2. High — Operator-supplied proof obligations were copied into the sealed control without binding
   the active durable verification requirement, its claims, or proof-contract identity.
3. High — The retained versioned Codex canaries stored only summary receipt fragments. They did not
   retain the complete core receipt and complete sealed inputs needed to recompute its identity.

## Acceptance-criterion assessment at review time

- AC1: Pass.
- AC2: Fail because findings 1 and 2 left authority unsealed.
- AC3: Fail because finding 3 prevented independent receipt verification.
- AC4: Pass; Claude remained precisely unsupported and uncredited.
- AC5: Pass at the structural layer only; no dual-host runtime claim was made.
- AC6: Fail/pending while the findings remained open.
- AC7: Fail because the runtime receipt ledger was incomplete.

## Review boundaries

The candidate version and package wiring were consistent, the retained wheel and sdist matched their
manifests and packaged source, strict Doctor passed, and the Intent audit was current. Those checks
did not clear the three findings. No branch, tag, package, release, rollout, adoption, or owner-
acceptance proof existed at review time. TASK-102 and parent AC10 remained open for Claude runtime
certification.

This verdict is preserved. Resolution must use one affected-validation disposition and must not
commission a second broad QA.
