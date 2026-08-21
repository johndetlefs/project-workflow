# Requirements

## Summary

- Task: EPIC-015
- Title: Release And Roll Out Project Workflow 0.6.0
- Last updated: 2026-08-21
- Intent contract: full

## Intent

Publish the completed intent-integrity and continuation-sufficiency work as Project Workflow 0.6.0
on reviewed `main`, prove the exact public release, and then upgrade every existing canonical
Project Workflow installation that can be changed safely. Leave non-installed, dirty, detached or
ambiguous projects untouched with an explicit disposition instead of forcing adoption.

## Intent Spine

- OC1 — Completion capability: Project Workflow 0.6.0 is publicly installable from PyPI, its tag
  and GitHub Release are on the reviewed `main` lineage, and every safe canonical consumer reports
  an upgraded validated installation or a concrete blocker.
- OC2 — Material capabilities: Prepare one coherent versioned candidate; validate source and
  built artifacts; integrate through reviewed GitHub checks; publish and verify the
  exact public artifacts; inventory all saved projects; safely upgrade eligible installed roots;
  retain a complete release and rollout receipt.
- OC3 — Success journey: Review and merge the candidate, tag the exact main commit, observe the
  trusted release workflow publish the same wheel and sdist, verify a fresh public installation,
  then plan/apply/validate upgrades only at clean canonical authority roots.
- OC4 — Successful-but-wrong result: Source tests pass but the tag/public artifact diverges, a
  release is claimed before public verification, a non-canonical or dirty project is mutated, or
  an upgrade is called successful without manifest/diff/Doctor evidence.
- OC5 — Exclusions: Do not install into projects without Project Workflow, overwrite dirty or
  owner-owned work, push consumer commits, deploy consumer applications, rewrite historical
  evidence, or claim universal live-model behavior from fixture coverage.
- OC6 — Assumptions: `origin/main` remains the release base, trusted publishing remains available,
  and consumer eligibility is rechecked immediately before mutation. The public exact-version
  package, not this checkout, is the consumer upgrade authority.
- OC7 — Authority source: Owner request in the current Codex task on 2026-08-21 to release the
  accepted candidate to `main` and update every project that already has Project Workflow.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-21
- Approval note / source: Current Codex task 2026-08-21: explicitly approved building the three-outcome post-proof stop gate and completing the 0.6.0 release
- Approved artifact identity: sha256:b98e6dd36817729280a5387a7121a8c5d7bc9495b658e8fd8e8e67c7dbe3ae0c

## Goal

Release the accepted EPIC-014, FIX-007 and FIX-008 work as Project Workflow 0.6.0 and roll that
public exact-version package into every eligible canonical installation in the current saved-project
inventory.

## Non-Goals

- Reopening or redefining the accepted intent-integrity and sufficiency behavior.
- Installing Project Workflow into projects without a canonical root manifest.
- Mutating dirty, detached, ambiguous, nested or structurally unsafe consumer roots.
- Committing, pushing, merging or deploying consumer-project changes.
- Treating local tests, a tag, or a successful upgrade command as a substitute for exact public
  artifact, scoped diff and Doctor evidence.
- Expanding this release into unrelated Project Workflow features or consumer application work.

## Users & Context

The owner uses Codex across 20 currently saved project entries. The read-only 2026-08-21 snapshot
contains nine local canonical Project Workflow installations: six clean roots currently eligible in
principle and three dirty roots that must remain unchanged unless they become clean before rollout.
The remaining local, non-Git and ChatGPT projects are inventory dispositions, not installation
targets.

## Repository Scope

- Primary repository: .
- Repositories touched: the Project Workflow source repository plus each currently saved local
  project whose root `.project-workflow/manifest.json` proves a canonical installation and whose
  immediate pre-mutation safety check passes. Current installed roots are Mechanics Playground,
  Game Foundation, Toby's Games, The Moon Is Hollow, Strategic Advisor, Daily Checklist,
  johndetlefs, Project Workflow and Client Management App.

## Requirements (Outcome-Focused)

- Prepare one 0.6.0 release candidate whose version authorities, generated/local mirrors, managed
  assets, changelog, README, CI and release workflow agree.
- Validate the final exact candidate with the complete locked suite, strict Doctor, release
  contract, built wheel/sdist inspection, exact-wheel four-host journeys and current behavioral
  fixtures. After sufficient proof passes, stop; an actual later change records one unaffected,
  affected or ambiguous impact decision, and an affected decision permits one named validation
  pass without creating or reopening independent QA.
- Integrate through a reviewed GitHub PR and passing CI; tag the exact resulting `main` lineage as
  `v0.6.0`; publish the same artifacts through trusted publishing and GitHub Release.
- Verify public PyPI and GitHub artifacts, hashes, provenance/attestation and a fresh exact-version
  installation before any consumer upgrade.
- Re-read the current Codex saved-project inventory and classify every entry. Upgrade only existing
  canonical roots that are clean, unambiguous and safe at mutation time, using the public 0.6.0
  package's canonical agent-mode upgrade.
- Preserve user-owned content and unrelated changes. Record dirty, detached, ambiguous, failed-plan
  and non-installed projects without mutation.
- Retain a machine-readable rollout receipt with source commit, PR/CI, tag, release URLs, public
  artifact hashes, inventory snapshot and every project disposition/validation result.

## Acceptance Criteria (Verifiable)

- AC1: All release identity authorities and current-use documentation consistently identify 0.6.0;
  packaged and repository-local agent assets align; required CLI mirrors remain byte-identical;
  historical completed evidence is not rewritten.
- AC2: The exact final candidate passes the complete locked suite, strict Doctor, release-contract
  checks, wheel/sdist inspection, all four exact-wheel host journeys and current
  intent/continuation behavioral fixtures. After that proof, status stops unless one recorded
  affected change names an invalidated proof layer; one passing affected validation returns to the
  next delivery step and cannot generate another review action for the same change identity.
- AC3: A reviewed PR with passing required checks is merged into `main`; annotated tag `v0.6.0`
  identifies that exact main lineage; the trusted release workflow publishes one coherent wheel,
  sdist and GitHub release bundle without divergent rebuilds.
- AC4: Public verification proves `project-workflow==0.6.0` installs fresh, reports 0.6.0, contains
  the intent-integrity and sufficiency assets, matches recorded public hashes, and has verifiable
  GitHub provenance/attestation.
- AC5: Every entry in the refreshed saved-project inventory has a disposition; every existing
  canonical Project Workflow root is either upgraded from public 0.6.0 or retained unchanged with
  a concrete current safety blocker.
- AC6: Every successful consumer upgrade preserves user-owned content, contains only expected
  managed/schema changes, reports 0.6.0, passes no-op re-plan and applicable Doctor validation, and
  is not committed, pushed or deployed by this Epic.
- AC7: A retained release/rollout receipt maps AC1-AC6 to exact commits, PR/checks, tag/release URLs,
  public artifact identities, inventory evidence, per-project results and unresolved boundaries.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose | Dependencies |
| --- | --- | --- | --- |
| Prepare the coherent Project Workflow 0.6.0 release identity | AC1 | Align every current release authority without rewriting historical evidence. |  |
| Validate the exact 0.6.0 release candidate | AC2 | Prove the final source and built artifacts before integration. | TASK-085 |
| Integrate, tag and publish Project Workflow 0.6.0 | AC3 | Merge the reviewed candidate and publish that exact main lineage. | TASK-086 |
| Verify the public 0.6.0 artifacts and fresh installation | AC4 | Prove the publicly obtainable release rather than the local build. | TASK-087 |
| Inventory and safely upgrade every eligible canonical installation, then retain the rollout receipt | AC5, AC6, AC7 | Apply the public package only where safe and retain complete per-project evidence. | TASK-088 |

## Open Questions (Answer Needed)

- None. The owner requested reviewed integration, public release and safe adoption across every
  existing Project Workflow installation.

## Decisions (Resolved)

- 0.6.0 is the proposed semantic version because intent-integrity, outcome-proof and continuation-
  sufficiency controls are substantive backward-compatible workflow functionality.
- EPIC-014/FIX-007/FIX-008 own feature acceptance; EPIC-015 owns version preparation, final candidate
  validation, integration, publication, public verification and adoption.
- The public exact-version package is the only consumer upgrade authority.
- Dirty, detached, ambiguous or failed-plan consumers fail closed and remain unchanged.
- Release work and consumer rollout remain separate proof gates even though this Epic coordinates
  them sequentially.

## Validation Plan

- AC1: version scans, changelog/README/workflow inspection, skill/prompt parity and CLI mirror hashes.
- AC2: locked full suite, strict Doctor, release contract, deterministic builds, distribution
  inspection, exact-wheel four-host journeys, behavioral fixtures and the stop-gate regression
  proving that passed affected validation cannot generate another review action.
- AC3: PR diff/review/check evidence, merge ancestry, annotated tag identity and release workflow.
- AC4: PyPI metadata/download, GitHub release assets/hashes, attestation verification and disposable
  exact-version installation.
- AC5-AC6: refreshed Codex inventory, root manifest/branch/status classification, canonical public
  upgrade plan/apply/no-op plan, scoped diff, manifest/helper and Doctor evidence per eligible root.
- AC7: retained machine-readable release/rollout receipt and parent acceptance audit.
