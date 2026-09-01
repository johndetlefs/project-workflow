# Requirements

## Summary

- Task: TASK-115
- Title: Generate Project Architect Host Entrypoints
- Parent AC Coverage: AC3, AC4, AC9, AC10, AC11
- Last updated: 2026-09-01
- Intent contract: full

## Intent

Provide one host-neutral Project Architect semantic source that deterministically generates Codex
and Claude entrypoints, while proving generated parity separately from each real host's discovery
and invocation capability.

## Intent Spine

- OC1 — Completion capability: Both host formats derive from one canonical semantic contract.
- OC2 — Material capabilities: Deterministic generation, drift rejection, packaging and host discovery.
- OC3 — Success journey: Generated checks pass; Codex invokes the installed skill; Claude is canaried or honestly blocked.
- OC4 — Successful-but-wrong result: Files exist and match but neither supported host discovers them.
- OC5 — Exclusions: No duplicate authored host truth, consumer adoption, release or false Claude claim.
- OC6 — Assumptions: Codex CLI is authenticated; Claude availability must be observed, not assumed.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Yes, inherited unchanged from parent approval
- Requirements reviewed by owner: Yes, through the approved parent envelope
- Acceptance criteria reviewed by owner: Yes, through the approved parent envelope
- Approved for decomposition: Inherited
- Approved for implementation: Yes
- Approved scope envelope: EPIC-021 unchanged generated-host capability
- Approved by: John Detlefs
- Approval date: 2026-09-01
- Approval note / source: Originating task `01a05a3b-dea4-7330-a0ca-93f34c5e2cb9`
- Approved artifact identity: Inherited from current EPIC-021 intent audit

## Child Charter

- Project Architect is subordinate to Coordinator and never writes shared workflow state.
- One canonical prompt owns semantics; host files are generated derivatives.
- Generation parity and real-host invocation are separate claims.
- Package membership, mocks, generated files or unauthenticated commands do not prove Claude use.

## Goal

Ship maintainable Project Architect host assets with honest, host-specific capability evidence.

## Non-Goals

- No lifecycle enforcement implementation; TASK-114 owns it.
- No Claude-support claim if a real authenticated Claude executable is unavailable.
- No push, release, plugin publication or consumer adoption.

## Users & Context

Codex and Claude users initializing Project Workflow in a repository.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Author Project Architect semantics only in `prompts/Architect.prompt.md`.
- Generate packaged/repository Codex and packaged Claude derivatives deterministically.
- Fail CI when any generated derivative drifts.
- Install discoverable Codex and Claude assets through their existing init paths.
- Run real, separate host canaries and retain exact blockers without substituting generation proof.

## Acceptance Criteria (Verifiable)

- AC1: A deterministic checker regenerates both host formats from the canonical source and catches one-copy drift.
- AC2: Codex and Claude init fixtures discover semantically equivalent Project Architect entrypoints.
- AC3: A real authenticated Codex session discovers and invokes `$project-architect` against this candidate.
- AC4: A real authenticated Claude canary passes, or exact executable/auth blocker evidence is retained with no parity claim.
- AC5: Generated assets keep Coordinator ownership, proportionate classification, optional ADRs and repository-specific constraints.

## Open Questions (Answer Needed)

- None; Claude runtime availability is an evidence result, not a requirements question.

## Decisions (Resolved)

- The prompt is canonical; packaged Codex/Claude and installed Codex copies are generated.
- Host installation fixtures prove discovery shape, while actual CLI sessions prove real invocation.

## Validation Plan

- Run generator check, drift unit tests, Codex/Claude init tests, package inventory, and separate real-host canaries.
