# Fix

## Summary

- Fix: FIX-006
- Title: Preserve Wrapped Epic Contract Bullets In Child Charters
- Status: Complete
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
- Branch, PR, and evidence links: GitHub PR #17 merged to `44ac9ac71ae6c0b73cee61c64a86241d39dd8298`; tag `v0.5.1`; release run `32342505251`; public and rollout receipts under `evidence/`.
- Verification plan: Exact parser reproduction; focused scaffold/readiness/Doctor tests; legacy single-line and unrelated Markdown compatibility; full locked pytest; strict Doctor; compilation/mirror/privacy/source contract; build and exact-wheel four-host package journeys; public hashes/provenance/fresh install; fingerprint-bound consumer upgrades and post-plan/Doctor validation.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/FIX-006-wrapped-child-charters` | GitHub PR #17 (merged) | Public 0.5.1 receipt, verification, audit, package journeys, and Codex rollout receipt |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | GitHub PR #17; merge `44ac9ac`; tag `v0.5.1` | Exact parser, 397-test full suite, strict Doctor, source contract, exact-wheel and public package journeys, hashes, receipt, and Sigstore verification pass | Published to PyPI and GitHub Release by run `32342505251`; seven clean installed roots current; two dirty roots retained unchanged | FIX-006 `evidence/` receipts |

## Verification

- Delivered scope: Complete logical-list extraction for Epic contract invariants, invalid substitutes, and artifact targets; exact legacy-fragment diagnostics for active child requirements and implementation docs; 0.5.1 / managed asset 4 release identity; regression, audit, package, and rollout safety evidence.
- Verification result: Pass. The complete locked suite passed 397 tests; strict Doctor reported no issues with 69 accepted historical warnings hidden; all three helper mirrors share SHA-256 `2580660934af4dff7c8eb5c46f7a5c7f6b21ece8a1c2a0fe7c0929c049554d1f`; public wheel and source distribution hashes match the release receipt; public four-host and legacy journeys pass; Sigstore provenance binds the artifacts to `v0.5.1`, commit `44ac9ac`, workflow `Release`, and run `32342505251`; seven clean canonical roots are current and two dirty roots remain unchanged.
- Adjacent behavior checked: Single-line bullets, `-` / `*` / `+` markers, indented and lazy continuations, placeholder filtering, section boundaries, proof-owner filtering, standalone Task scaffolding, active readiness/Doctor rejection and recovery, completed-history non-blocking behavior, future-version compatibility, legacy owner-collision preservation, and complete non-Delegate regression coverage.
- Original acceptance criteria result: Not applicable because FIX-006 corrects a released parser defect rather than reopening an earlier Task or Epic acceptance criterion; the bounded expected behavior is recorded in this Fix report and verification evidence.
- Regression evidence: `tests/test_doctor.py`; `evidence/legacy-charter-audit.json`; `evidence/public-release-receipt.json`; `evidence/public-verification.json`; `evidence/public-package-journeys.json`; `evidence/codex-rollout-receipt.json`; public wheel SHA-256 `8f7a0266d4cf94e55754d95ba16443bb32561945cf405407bd188b058f4a4f72`.
- Residual risk: Existing malformed active charters are diagnosed but not automatically rewritten. The audit found 60 affected children across five projects, including 20 active children; their owning project tasks must restore complete parent bullets before governed advancement. Forty completed children remain preserved historical records. The Moon Is Hollow and johndetlefs remain on 0.3.0 because their canonical roots contain active local workflow changes.

## QA & Code Review

- Date: 2026-08-20
- Reviewed areas: Markdown list parsing and boundary handling; scaffold output in both child documents; readiness and Doctor lifecycle integration; active-versus-completed policy; version and managed-asset authorities; generated-helper parity; release workflow identities; audit privacy and rollout safety.
- Validation evidence: 397 locked tests passed; strict Doctor passed; focused parser/scaffold/integrity tests passed; 0.5.1 source contract and public-availability preflight passed; exact wheel and source distribution built; four-host fresh/init/upgrade plus legacy collision journey passed; `git diff --check` passed.
- Findings: None blocking. The first diagnostic draft was corrected before review from per-bullet output to one actionable finding per document section, preventing large legacy installations from producing unusable Doctor floods.
- Invalid substitutes excluded: Green tests do not claim public publication; local wheel journeys do not claim PyPI/GitHub provenance; the read-only audit does not claim existing child charters were repaired; completed historical documents were not rewritten.
- Verdict: Pass. Reviewed merge, public 0.5.1 release/provenance, and safe Codex rollout are complete within the recorded boundaries.

## Outcome

- Disposition: Fixed
- Decision: Published and rolled out Project Workflow 0.5.1 with complete wrapped Epic-contract bullet inheritance and fail-closed active-child diagnostics.
- Closed by: John Detlefs / Codex
- Closed date: 2026-08-20
- Promoted to: None

## Retro

- Date: 2026-08-20
- Lessons: Structural scaffold tests that assert only headings can miss semantic data loss. Markdown workflow authority must be tested as complete logical items across physical wrapping, section boundaries, generated destinations, and delivered legacy forms.
- Updated assets: Added the parser/scaffold/readiness/Doctor regressions in `tests/test_doctor.py` and the narrow durable convention in `.project-workflow/guidance.md`.
- Follow-up suggestions: No new Project Workflow work item. The 20 affected active consumer children are already visible to their owning workflows through the released Doctor/readiness diagnostic; repair remains child-local and coordinator-owned.
- Missed in-scope work: None. Public provenance, rollout dispositions, dirty-root retention, and the active/completed history boundary are all recorded in FIX-006 evidence.
