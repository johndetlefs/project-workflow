# Requirements

## Summary

- Task: TASK-116
- Title: Dogfood Architecture Control And Closeout
- Parent AC Coverage: AC2, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13
- Last updated: 2026-09-01
- Intent contract: full

## Intent

Prove the complete bounded architecture-control outcome against Project Workflow itself, retain
the honest host proof boundary, obtain independent adversarial QA, and close the Epic locally
without treating implementation as release or consumer adoption.

## Intent Spine

- OC1 — Completion capability: A fixed local candidate passes contract, lifecycle, parity and dogfood proof.
- OC2 — Material capabilities: Integrated journeys, host receipts, full checks, independent QA and acceptance audit.
- OC3 — Success journey: Cheap local passes; stale material and deliberate violation fail; current material conforms.
- OC4 — Successful-but-wrong result: Green unit tests mask lifecycle bypass, generated-only host proof, or consumer mutation.
- OC5 — Exclusions: No push, merge, release, deployment, external adoption or automatic restructuring.
- OC6 — Assumptions: Claude may remain unavailable and must remain an explicit blocker.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Yes, inherited unchanged from parent approval
- Requirements reviewed by owner: Yes, through the approved parent envelope
- Acceptance criteria reviewed by owner: Yes, through the approved parent envelope
- Approved for decomposition: Inherited
- Approved for implementation: Yes
- Approved scope envelope: EPIC-021 local proof and closeout only
- Approved by: John Detlefs
- Approval date: 2026-09-01
- Approval note / source: Originating task `01a05a3b-dea4-7330-a0ca-93f34c5e2cb9`
- Approved artifact identity: Inherited from current EPIC-021 intent audit

## Child Charter

- Dogfood proves Project Workflow's selected architecture, not a universal prescription.
- Host generation, Codex invocation and Claude invocation are three distinct proof claims.
- Coordinator is the sole workflow writer; independent QA is read-only.
- No consumer repository or external delivery system may change.

## Goal

Produce a locally closed, auditable exact candidate with no inflated delivery or host claims.

## Non-Goals

- No consumer changes, release artifacts, publication, deployment, push or merge.

## Users & Context

The Project Workflow owner deciding whether this capability is implemented and structurally sound.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Bind dogfood to `docs/architecture.md` and its exact digest.
- Retain executable lifecycle, dependency, parity and host receipts.
- Run all repository contributor gates and an independent adversarial review.
- Map every parent AC to exact evidence and keep external delivery/adoption explicitly unperformed.

## Acceptance Criteria (Verifiable)

- AC1: Integrated proof covers cheap/local, missing/stale material, exact conformance and deliberate violation cases.
- AC2: Generated host parity and real Codex invocation pass; Claude separately passes or has an exact honest blocker.
- AC3: Project Workflow's selected module/dependency/source constraints and full repository gates pass.
- AC4: Independent QA cannot identify an in-envelope bypass or false claim in the remediated candidate.
- AC5: Acceptance audit maps AC2/6/7/8/9/10/11/12/13 and confirms no consumer or external delivery mutation.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Unavailable Claude capability satisfies only the explicit blocker branch of AC11, never host parity.
- Consumer adoption remains a future owner decision.

## Validation Plan

- Run focused and full locked checks, package/init journeys, generated parity, real Codex canary, Claude availability/auth canary, Doctor, and one integrated independent QA review.
