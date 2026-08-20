# Fix

## Summary

- Fix: FIX-006
- Title: Preserve Wrapped Epic Contract Bullets In Child Charters
- Status: Review
- Created: 2026-08-20

## Report

- Observed or requested: Public Project Workflow 0.5.0 copies only the first physical line of a wrapped Epic-contract bullet into generated child charters, silently dropping indented continuation lines.
- Expected: `epic scaffold-child` must preserve each complete top-level bullet from `Invariants`, `Invalid Substitutes`, and `Artifact Targets` in both child `REQUIREMENTS.md` and `IMPLEMENTATION.md`; readiness and Doctor must reject the identifiable legacy truncated form before active implementation advances.
- Affected users or systems: All Project Workflow repositories using Epic child scaffolding with line-wrapped contract bullets; versions 0.2.0 through 0.5.0 contain the parser defect.
- Delivered baseline: Public `project-workflow==0.5.0`, tag `v0.5.0`, source commit `fdd4e15c621cb6805e1455d0658c60ee24b92b0c`.
- Report evidence: Thread `01a01d9d-15f5-7373-8e93-0cfd6633393f`; exact Water Epic contract reproduction; `_contract_section_bullets` at `src/project_workflow/cli.py`; originating commit `272945eefc78031d53153eee57a79e4eb85e401a`.

## Routing

- Decision: Fix
- Rationale: One delivered parser/integrity defect has a single compatible correction and no new product decision. It does not reopen EPIC-012 or EPIC-013.
- Related work state: Project Workflow 0.5.0 release and rollout are Complete; the defect was first observed by the active Mechanics Playground Water Epic.
- Bounded correction: Preserve wrapped list-item continuations, detect the exact legacy truncation signature in active child charters, prove compatibility, publish 0.5.1, and upgrade safe installed roots.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: High
- Impact: Child plans can silently lose inherited safety constraints, invalid-substitute boundaries, and artifact requirements while all current structural gates still pass.
- Urgency: Immediate patch before further 0.5.0 Epic child implementation proceeds.
- Owner: John Detlefs / Project Workflow maintainer

## Related Work

- Originating work: Epic drift-prevention scaffolding introduced by commit `272945eefc78031d53153eee57a79e4eb85e401a`; observed during Mechanics Playground EPIC-013.
- External links: Public release `v0.5.0`; reporting Codex thread `01a01d9d-15f5-7373-8e93-0cfd6633393f`.

## Risk

- Risk level: Medium
- Risks: A permissive Markdown parser could merge unrelated prose or nested lists; a broad historical Doctor rule could create false blockers in completed preserved work; release/upgrade steps could overwrite active consumer changes.
- Rollback or containment: Keep parsing limited to flat contract-section list items, test lazy/indented continuations and section boundaries, diagnose only the exact legacy fragment in active child charters, retain completed history read-only, and upgrade only clean canonical roots through fingerprint-bound public plans.

## Fix Plan

- Scope: Fix contract bullet extraction; add active-child readiness and Doctor integrity diagnostics; add regression/audit coverage; keep the three CLI mirrors byte-identical; publish Project Workflow 0.5.1 with managed asset version 4; upgrade every safe current Codex installation.
- Non-goals: Replanning or editing the active Water Epic, rewriting completed child charters automatically, changing Delegate executor selection, adding general Markdown/CommonMark rendering, repairing unrelated consumer Doctor debt, or pushing consumer repositories.
- Affected target: `epic scaffold-child`, `epic ready-child`, active Epic child lifecycle/Doctor checks, packaged/generated CLI assets, and public 0.5.1 adoption.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: `codex/FIX-006-wrapped-child-charters`; PR and public release evidence to be recorded before Review.
- Verification plan: Exact parser reproduction; focused scaffold/readiness/Doctor tests; legacy single-line and unrelated Markdown compatibility; full locked pytest; strict Doctor; compilation/mirror/privacy/source contract; build and exact-wheel four-host package journeys; public hashes/provenance/fresh install; fingerprint-bound consumer upgrades and post-plan/Doctor validation.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/FIX-006-wrapped-child-charters` | Pending | FIX-006 evidence and public 0.5.1 receipt |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/FIX-006-wrapped-child-charters`; PR pending | Exact parser, focused/full suite, strict Doctor, package/release/public checks pending | Source, public package, and safe local adoption are separate gates | FIX-006 command output and retained release/rollout receipt |

## Verification

- Delivered scope: Complete logical-list extraction for Epic contract invariants, invalid substitutes, and artifact targets; exact legacy-fragment diagnostics for active child requirements and implementation docs; 0.5.1 / managed asset 4 release identity; regression, audit, package, and rollout safety evidence.
- Verification result: Candidate pass. The complete locked suite passed 397 tests; strict Doctor reported no issues with 69 accepted historical warnings hidden; source contract identified 0.5.1; all three helper mirrors share SHA-256 `2580660934af4dff7c8eb5c46f7a5c7f6b21ece8a1c2a0fe7c0929c049554d1f`; the exact local wheel passed fresh and upgrade journeys for all four supported host modes. Public release and consumer adoption remain delivery steps after reviewed merge.
- Adjacent behavior checked: Single-line bullets, `-` / `*` / `+` markers, indented and lazy continuations, placeholder filtering, section boundaries, proof-owner filtering, standalone Task scaffolding, active readiness/Doctor rejection and recovery, completed-history non-blocking behavior, future-version compatibility, legacy owner-collision preservation, and complete non-Delegate regression coverage.
- Original acceptance criteria result: Not applicable
- Regression evidence: `tests/test_doctor.py`; `evidence/legacy-charter-audit.json`; `evidence/package-journeys.json`; exact local wheel SHA-256 `82cbbd111a0ce37fc8632534543b55447c8856cb21fdbf1bcd7826b2f96634e2`.
- Residual risk: Existing malformed active charters are diagnosed but not automatically rewritten. The audit found 60 affected children across five projects, including 20 active children; their owning project tasks must restore complete parent bullets before governed advancement. Forty completed children remain preserved historical records. Public publication, provenance, and safe consumer rollout are not yet claimed at this candidate-review stage.

## QA & Code Review

- Date: 2026-08-20
- Reviewed areas: Markdown list parsing and boundary handling; scaffold output in both child documents; readiness and Doctor lifecycle integration; active-versus-completed policy; version and managed-asset authorities; generated-helper parity; release workflow identities; audit privacy and rollout safety.
- Validation evidence: 397 locked tests passed; strict Doctor passed; focused parser/scaffold/integrity tests passed; 0.5.1 source contract and public-availability preflight passed; exact wheel and source distribution built; four-host fresh/init/upgrade plus legacy collision journey passed; `git diff --check` passed.
- Findings: None blocking. The first diagnostic draft was corrected before review from per-bullet output to one actionable finding per document section, preventing large legacy installations from producing unusable Doctor floods.
- Invalid substitutes excluded: Green tests do not claim public publication; local wheel journeys do not claim PyPI/GitHub provenance; the read-only audit does not claim existing child charters were repaired; completed historical documents were not rewritten.
- Verdict: Pass for reviewed merge and release execution. Keep FIX-006 in Review until public 0.5.1 verification and safe consumer rollout are complete.

## Outcome

- Disposition: Pending
- Decision: ____
- Closed by: ____
- Closed date: ____
- Promoted to: None
