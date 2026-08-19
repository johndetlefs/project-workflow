# Requirements

## Summary

- Task: EPIC-011
- Title: Release And Roll Out Project Workflow 0.4.0
- Last updated: 2026-08-20

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-20
- Approval note / source: Codex owner request on 2026-08-20: merge completed Delegate work to main, publish a new release, and update every current Codex project that has Project Workflow
- Approved artifact identity: sha256:8309fded4e2ea9244129910abdc4e8628c541dac9368408155cb88516af02f23

## Goal

Publish the completed Delegate execution-orchestrator work as Project Workflow 0.4.0, merge the reviewed source to `main`, and upgrade every saved Codex project that currently has a canonical Project Workflow installation so new work can use Delegate safely.

## Non-Goals

- Replaying the already accepted EPIC-010 implementation or redefining Delegate requirements.
- Claiming native runtime support for hosts that were not verified by EPIC-010.
- Installing Project Workflow into projects that do not already have it.
- Overwriting user-owned files, unrelated dirty changes, or non-authority nested workflow copies.
- Deploying consumer applications or changing their product code.

## Users & Context

The owner uses Codex across multiple saved local projects. Project Workflow 0.3.0 is the latest public package, while the completed Delegate implementation exists only on the EPIC-010 feature branch. The release must preserve source/package parity and the rollout must distinguish actual installed roots from merely saved Codex projects.

## Repository Scope

- Primary repository: .
- Repositories touched: the Project Workflow source repository plus each currently saved Codex project root whose own `.project-workflow/manifest.json` proves an installation. The exact consumer set is discovered and recorded before mutation.

## Requirements (Outcome-Focused)

- Prepare one 0.4.0 release candidate whose version authorities, generated mirrors, managed assets, changelog, documentation, CI, and release workflow agree.
- Validate the exact candidate with the complete locked test suite, strict Doctor, source/release contract, built artifacts, and exact-wheel package journeys before merge.
- Merge the reviewed candidate to `main`, tag that exact main commit as `v0.4.0`, and publish the same artifacts through the existing Trusted Publishing and GitHub Release workflow.
- Verify public PyPI and GitHub artifacts, hashes, provenance/attestation, and a fresh exact-version installation before declaring the release available.
- Inventory current saved Codex projects and classify each as installed authority root, no installation, non-Git root, dirty/conflicting, or otherwise blocked.
- For every eligible installed authority root, use the public 0.4.0 package's canonical upgrade path in Codex agent mode, preserve user-owned content, and validate the resulting manifest, managed assets, generated helper, and Doctor result.
- Keep each consumer repository's changes scoped and reviewable. Do not silently overwrite unrelated work or treat an unintegrated local diff as universal adoption.
- Retain a machine-readable rollout receipt identifying the inventory snapshot, exact public package, per-project disposition, validation result, and any explicit blocker.

## Acceptance Criteria (Verifiable)

- AC1: All current release identity authorities and current-use documentation consistently identify version 0.4.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged.
- AC2: The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys.
- AC3: A reviewed pull request is merged to `main`; `v0.4.0` is an annotated tag on that exact merged lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without rebuilding divergent artifacts.
- AC4: Public verification proves `project-workflow==0.4.0` installs fresh, reports 0.4.0, exposes the Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance.
- AC5: Every project in the current Codex saved-project inventory has a recorded disposition, and every project with a canonical Project Workflow installation is either upgraded from the public 0.4.0 package or retained unchanged with a concrete safety blocker.
- AC6: Every successful consumer upgrade preserves user-owned content, produces only expected managed/schema changes, reports package version 0.4.0, and passes its applicable Doctor/upgrade validation.
- AC7: A retained rollout receipt maps every acceptance criterion to exact commits, release URLs or artifact identities, inventory evidence, per-project validation, and any unresolved adoption boundary.

## Open Questions (Answer Needed)

- None. The owner explicitly requested merge, release, and upgrade of every current Codex project that already has Project Workflow. Consumer repository publication is not inferred beyond the local upgrade unless it is already part of that repository's authorized workflow.

## Decisions (Resolved)

- 0.4.0 is the correct semantic version because Delegate is a substantive backward-compatible feature.
- EPIC-010 acceptance is the feature-completion authority; EPIC-011 owns only release preparation, publication, public verification, and adoption.
- Saved projects without a root installation are inventory results, not installation targets.
- Dirty, detached, ambiguous, or failed-plan repositories fail closed and remain unchanged until their blocker is resolved.
- The public exact-version package, not the source checkout, is the consumer upgrade authority.

## Validation Plan

- AC1-AC2: version scans, mirror hashes, strict Doctor, complete pytest suite, release-contract scripts, built-artifact verification, and exact-wheel host journeys.
- AC3-AC4: GitHub PR/check/merge evidence; tag ancestry; release workflow evidence; PyPI metadata/fresh UVX install; GitHub Release asset hashes and attestation verification.
- AC5-AC6: current Codex saved-project inventory plus read-only root/branch/status/manifest classification; canonical `upgrade --plan`; controlled `upgrade --yes`; before/after Git diff, manifest, helper, and Doctor checks.
- AC7: `.project-workflow/tasks/EPIC-011-Release-And-Roll-Out-Project-Workflow-0-4-0/evidence/release-rollout-receipt.json` and the parent acceptance audit.
