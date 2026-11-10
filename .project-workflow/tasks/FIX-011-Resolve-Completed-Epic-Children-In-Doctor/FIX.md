# Fix

## Summary

- Fix: FIX-011
- Title: Resolve completed epic children in Doctor
- Status: Complete
- Created: 2026-11-11
- Intent contract: compact

## Intent

Restore Doctor and verification inspection for completed epic children, preserving their parent ownership and proof. Closing a child must not make its existing coordination evidence unresolvable.

## Report

- Observed or requested: Doctor cannot resolve a completed epic child after closing Massey TASK-009.
- Expected: Completed children remain inspectable while normal status lists remain active-only.
- Affected users or systems: Repositories using epic children with coordination verification state.
- Delivered baseline: Project Workflow 0.10.0, source 9bdcf26.
- Report evidence: Owner reported Massey TASK-009 closeout; source _verification_work_item_layers falls back only to global rows.

## Routing

- Decision: Fix
- Rationale: One bounded defect in already delivered lifecycle lookup.
- Related work state: Not identified
- Bounded correction: Resolve terminal epic children through authoritative trackers without changing lifecycle gates.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: Doctor reports invalid coordination evidence after valid child closure.
- Urgency: Normal; prepare review before any new release.
- Owner: John Detlefs

## Related Work

- Originating work: Not identified
- External links: None

## Risk

- Risk level: Low
- Risks: Incorrectly broadening active status or silently selecting duplicate work IDs.
- Rollback or containment: Revert this isolated branch; no consumer installations are changed.

## Fix Plan

- Scope: Lifecycle lookup, regression tests and generated runtime mirrors.
- Non-goals: No unrelated feature or warning cleanup. Owner subsequently authorized 0.10.1 release, safe consumer upgrades and Massey closure; preserve active work.
- Affected target: Verification projection and Doctor for terminal epic children.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: codex/fix-completed-epic-child-lookup; review pending.
- Verification plan: Reproduce terminal child failure, exercise active and terminal parents and duplicate IDs, confirm active-only status unchanged, run quality gates and one full suite, verify a disposable Massey workflow copy, obtain independent QA.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | codex/fix-completed-epic-child-lookup | Draft review pending | Tests and Outcome Journey below |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/fix-completed-epic-child-lookup | 594 tests and all contributor gates pass | Candidate only, not merged or released | Regression tests and Outcome Journey below |

## Verification

- Delivered scope: Terminal-aware authoritative lifecycle lookup for verification and Doctor; active-only status remains unchanged.
- Verification result: 594 tests passed in 101.77s, including UVX packaging; lint, formatting, mypy, documentation, generated-runtime parity and diff checks passed. Doctor clean with 69 accepted historical warnings hidden.
- Adjacent behavior checked: Completed children under active/completed parents retain provenance; duplicate global/epic IDs fail closed; global terminal lookup remains covered; active-only summaries exclude completed children.
- Original acceptance criteria result: Not applicable
- Regression evidence: New terminal epic-child test failed before implementation with the reported missing-item error and passes after correction; 33 focused verification/status tests pass; actual disposable consumer closure journey passes (below).
- Residual risk: Implementation passed; public release and consumer adoption require the separate evidence below.

## Outcome

- Disposition: Fixed
- Decision: Owner accepted independently reviewed regression-tested correction and authorized release; release and adoption proof tracked separately.
- Closed by: John Detlefs via Vimes
- Closed date: 2026-11-11
- Promoted to: None

## Outcome Journey

- Baseline: canonical consumer snapshot b66d596, copied with workflow and referenced docs to a disposable directory. Live consumer files and installed runtime were not modified.
- Candidate command: `project epic status --epic-id EPIC-001 --id TASK-009 --to Complete` using candidate source changed Review to Complete through the normal gates and refreshed the acceptance map.
- Candidate Doctor after closure: no issues found.
- Released 0.10.0 bundled Doctor on the same completed snapshot: exactly one blocking error, `Operational lifecycle contains 0 work items named TASK-009; exactly one is required`.
- Repeated Complete request is rejected by the existing Review-only closure gate; no force or gate bypass was used.
- This proves the restored closure/inspection journey, not publication, installation, rollout, or owner acceptance of a new release.

## QA & Code Review

- Verdict: Pass
- Reviewer: Independent read-only reviewer, separate from implementation.
- Reviewed scope: Canonical lookup, collector opt-in, provenance, default active status, duplicate-ID safety and generated mirrors.
- Evidence: Independent terminal regression run: 3 passed; Doctor clean with 69 accepted warnings hidden; diff hygiene and generated mirror parity passed. Full-suite condition satisfied by 594 passing tests.
- Findings: None.
- Delivery boundary: Review only. Owner accepted the fix and authorized merge, release and safe rollout on 2026-11-11.

## Authorized Release And Adoption

- Owner direction: ship the tested fix, publish a release, bring applicable projects to current main and update Project Workflow while preserving work still in progress.
- Version: 0.10.1, a backward-compatible defect patch with no schema change.
- Source integration: PR #33 merged to main at 6e7d232.
- Plan: prepare coherent version-owned source; pass locked checks, distribution receipt and exact-wheel journeys; independent bounded release review; merge after hosted CI; tag reviewed main and publish through protected trusted workflow.
- Public proof: compare PyPI and GitHub exact artifacts, receipt and attestations; run isolated exact-version package journeys.
- Adoption: inventory canonical roots, coordinate with Git parity audit, preserve dirty/in-flight roots, use exact public package and fingerprinted upgrade plans, verify no-op follow-up plans and Doctor separately.
- Consumer closure: upgrade clean Massey canonical root, close TASK-009 through existing gates, verify Doctor, preserve Git evidence.
- Stop conditions: failed proof, changed source, ambiguous root, dirty work or protected environment approval requirement. No destructive cleanup or overwriting local changes.
- Release status: Published and independently verified. Clean-root rollout is tracked separately; dirty/in-progress roots are preserved.

## Independent Release Review

- Reviewed candidate: e648244.
- Original verdict: Changes requested.
- Finding: README relabelled historical v0.10.0 Codex runtime certification as v0.10.1 without matching certification evidence.
- Correction: Preserve v0.10.0 as the historical certified baseline and explicitly make no new host-runtime certification claim for the patch.
- Findings disposition: Resolved.
- Affected proof: README/package metadata and final exact distribution identity; runtime implementation and tests unchanged.
- Affected validation verdict: Pass. Corrected source/documentation contract and rebuilt final candidate receipt/exact-wheel journeys passed; final hosted CI passed all locked checks.
- Second QA commissioned: No.
- Other reviewed release surfaces: coherent versions, workflow pins, generated parity, historical changelog and source ancestry passed.
- Environment retry: Initial local exact-wheel journey saw inherited RUST_LOG INFO lines in version output; retry unsets that diagnostic variable without changing package or gates.

## Published Release Receipt

- Version: 0.10.1.
- Reviewed release PR: https://github.com/johndetlefs/project-workflow/pull/34 .
- Immutable tag/main commit: v0.10.1 at d1e478bd92852b7dfc7b7886ca9a654c7251a24c.
- Main CI: https://github.com/johndetlefs/project-workflow/actions/runs/42921096694 passed.
- Trusted release workflow: https://github.com/johndetlefs/project-workflow/actions/runs/42921581052 passed build, attestation, PyPI and GitHub publication.
- Public release: https://github.com/johndetlefs/project-workflow/releases/tag/v0.10.1 .
- Public package: https://pypi.org/project/project-workflow/0.10.1/ .
- Independent verification: PyPI wheel and sdist are byte-identical to GitHub Release files and match the authoritative public receipt. Wheel attestation verification passed against the repository identity.
- Isolated public install: `uvx --no-cache --no-config --isolated --from project-workflow==0.10.1 project --version` reports `project 0.10.1`.
- Public exact-wheel journeys: fresh initialization for four guidance modes, current/legacy/no-op upgrades, Doctor and representative lifecycle journeys passed; see `evidence/0.10.1/public-package-journeys.json`.
- Artifact identities: wheel `308ae12dacee95bc61b29f381cf45c26b816d0a2f9ed7c8348010d914334c1a4`; sdist `e67a15f4f0aad231e609d8e4c196ebba3bad7727635c448e4cc9a014980cc143`.
- Local candidate and authoritative public archives are separate build identities. Public checks bind the exact attested release artifacts, not the earlier local archive bytes.
- Consumer adoption: preserve per-root upgrade plan, no-op plan and Doctor evidence separately from publication; existing local changes and active work are not overwritten.
