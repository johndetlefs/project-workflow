# Fix

## Summary

- Fix: FIX-004
- Title: Backlog Epic Promotion Creates Current Epic Artifacts
- Status: N/A
- Created: 2026-07-21

## Report

- Observed or requested: Promoting an accepted backlog row to an Epic creates the Epic folder and most current scaffold artifacts but omits `EPIC-CONTRACT.md`.
- Expected: Backlog-to-Epic promotion creates the same current required Epic artifacts as `epic init`, including a non-placeholder `EPIC-CONTRACT.md`, so the new Epic starts from valid workflow state.
- Affected users or systems: Repository owners and agents that promote accepted Epic candidates from `.project-workflow/BACKLOG.md` into executable workflow state.
- Delivered baseline: EPIC-005 delivered backlog promotion; EPIC-006 later made a non-placeholder Epic contract mandatory before decomposition, child approval/scaffolding, or lifecycle advancement. Both originating work items are Complete.
- Report evidence: On clean `main` at `86ba892`, an isolated Codex-mode repository promoted accepted `BL-001` to `EPIC-001`; the folder lacked `EPIC-CONTRACT.md`, and Doctor immediately reported `PW_EPIC_CONTRACT_INVALID`. Source inspection confirms `cmd_backlog_promote` omits the contract write while `cmd_epic_init` creates it.

## Routing

- Decision: Fix
- Rationale: This is one bounded scaffold-parity defect against completed backlog-promotion and Epic-contract behavior, not a new product outcome or a set of independent workstreams.
- Related work state: EPIC-005 and EPIC-006 are Complete; BL-016 was Accepted for this correction.
- Bounded correction: Yes; add the missing current Epic artifact and regression coverage without changing backlog or Epic lifecycle semantics.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: Every backlog-promoted Epic starts with a known workflow warning and cannot satisfy the current contract gate without manual repair, undermining deterministic promotion and blocking clean preparation of the next accepted Epic.
- Urgency: High before promoting BL-017, the accepted next strategic Epic candidate.
- Owner: Repository owner

## Related Work

- Originating work: EPIC-005, EPIC-006
- External links: None

## Risk

- Risk level: Low
- Risks: A narrowly patched scaffold could still drift from `epic init`; an over-broad refactor could change unrelated promotion behavior or overwrite user-owned files.
- Rollback or containment: Keep the change additive and confined to new Epic scaffolding, retain existing backlog-source and tracker assertions, and revert the scaffold addition if promotion regressions appear.

## Requirements

- Backlog promotion to Epic must create a non-placeholder `EPIC-CONTRACT.md` using the same current template and Epic identity as `epic init`.
- Promotion must preserve the existing backlog-source section in `REQUIREMENTS.md`, Epic tracker row, backlog history, status transition, and all other current scaffold artifacts.
- The canonical CLI source, packaged scaffold template, and checked-in local helper must remain behaviorally and byte-for-byte aligned where parity is required.
- The correction must be covered by a focused regression that proves both artifact creation and clean Doctor behavior for a newly promoted Epic.

## Acceptance Criteria

- AC1: Promoting an accepted backlog row with `backlog promote --to epic` creates `EPIC-CONTRACT.md` in the new Epic folder with the allocated Epic ID, promoted title, and no template placeholders.
- AC2: The promoted Epic still contains `REQUIREMENTS.md`, `TRACKER.md`, `DEFERRALS.md`, `AMENDMENTS.md`, `RETRO.md`, and `ACCEPTANCE-MAP.md`; its requirements retain the backlog-source record, its global tracker row points to the Epic requirements, and the backlog row becomes `Promoted` with the allocated Epic ID.
- AC3: Doctor run immediately after promotion reports no missing or invalid Epic-contract finding for the promoted Epic.
- AC4: Existing task promotion, direct `epic init`, duplicate-promotion rejection, and backlog validation behavior remain unchanged.
- AC5: Focused promotion/Doctor tests, source-template-local CLI parity checks, the complete test suite with the UVX packaging test enabled, backlog validation, strict Doctor, and diff checks all pass.

## Open Questions

- OQ1: Should FIX-004 enforce strict scaffold parity with `epic init`, or expand into a warning-free Epic-creation redesign?
  - Conflict: `epic init` creates an intentionally incomplete `EPIC-CONTRACT.md`; Doctor reports five `PW_EPIC_CONTRACT_INVALID` warnings until the owner records real sources, invalid substitutes, invariants, artifact targets, and proof ownership. Approved AC1 currently forbids placeholders and AC3 forbids any invalid-contract finding, so those ACs conflict with both direct-init parity and the rule against inventing owner authority.
  - Why it matters: Strict parity is a bounded additive Fix. Producing a warning-free promoted Epic requires authoritative contract inputs or changed Doctor timing/severity, which is a material product decision outside the approved Fix envelope.
  - Option A (recommended): Create the same contract scaffold as `epic init`; amend AC1 to require correct identity and template parity, and AC3 to prohibit only the missing-contract finding while retaining expected incomplete-contract warnings until owner completion.
  - Option B: Expand scope to make newly created Epics warning-free by designing authoritative contract capture or changing Doctor semantics; promote FIX-004 to a Task before implementation.

## Resolved Decisions

- Route BL-016 as a normal Fix because it is a single bounded post-completion defect.
- Treat EPIC-005 and EPIC-006 as immutable originating work and link them rather than reopening either Epic.
- Keep implementation scope to current scaffold parity and regression proof; shared scaffold refactoring is not required unless the implementation demonstrates it is the smallest safe way to preserve the invariant.
- No visual, deployed-runtime, external-contract, or responsive proof recipe is triggered; repository artifact and executable CLI evidence are the authoritative validation sources.

## Owner Approval

- Status: Amendment required after OQ1 evidence
- Approved by: Repository owner
- Approval source: Codex task response on 2026-07-21: "All good, let's go ahead please."
- Approved scope: Requirements and AC1-AC5 in this Fix, including the stated non-goals and validation plan.
- Approved at: 2026-07-21
- Drift detected: Direct `epic init` proof shows that approved AC1 and AC3 cannot both hold without inventing contract authority or changing Doctor semantics; implementation paused before code changes.

## Fix Plan

- Scope: Add the missing current Epic contract to backlog-to-Epic promotion and strengthen the promotion regression to prove artifact identity, preserved backlog/tracker behavior, and clean Doctor output.
- Non-goals: Do not add backlog-to-Fix promotion, change ID allocation, redesign Epic lifecycle gates, modularize the CLI, alter existing Epic history, or broaden this into general scaffold architecture work.
- Affected target: `cmd_backlog_promote`, its maintained CLI mirrors, and backlog-promotion/Doctor regression coverage.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Triage was preserved on `codex/roadmap-renovation-and-smoke-bomb`; no PR; isolated reproduction and source inspection are recorded in this Fix.
- Verification plan: Extend the existing backlog-to-Epic promotion test to assert the complete required artifact set and contract contents, run Doctor against the promoted fixture and reject `PW_EPIC_CONTRACT_INVALID`, retain adjacent promotion tests, verify all CLI mirrors, then run `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`, backlog validation, strict Doctor, compilation/parity checks, and `git diff --check`.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | codex/roadmap-renovation-and-smoke-bomb | None | Isolated reproduction on `86ba892`; strategic value review closed implementation as Deferred |

## Verification

- Delivered scope: Evidence-led reproduction, contract-gate analysis, and disposition only; no implementation code was changed.
- Verification result: Direct `epic init` proof established that scaffold parity would still leave the owner-authored contract incomplete, so the correction would not deliver the stated warning-free or unblock outcome.
- Adjacent behavior checked: Backlog history and the originating completed Epics remain unchanged; current backlog validation and Doctor pass after closeout.
- Original acceptance criteria result: Not applicable
- Regression evidence: Not applicable; the proposed correction was deliberately not implemented.
- Residual risk: Backlog-promoted Epics still require the owner to create and complete the current contract before gated progression. This is explicit workflow work, not treated as an urgent standalone defect.

## Outcome

- Disposition: Deferred
- Decision: Verified direct epic creation intentionally produces an owner-completed contract scaffold. Adding that same incomplete artifact during backlog promotion would improve parity but would neither remove the contract gate nor materially unblock users; defer until a broader epic-creation design demonstrates sufficient value.
- Closed by: Repository owner and Codex
- Closed date: 2026-07-22
- Promoted to: None
