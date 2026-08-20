# Requirements

## Summary

- Task: EPIC-013
- Title: Release And Roll Out Project Workflow 0.5.0
- Last updated: 2026-08-20

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-20
- Approval note / source: Codex owner request on 2026-08-20: close EPIC-012, publish the new release, and upgrade all eligible Codex projects
- Approved artifact identity: sha256:aee5409ecaa9091873e64af3e1ce53a97ff9fea714c2070a6f49c772953c0569

## Goal

Publish the completed EPIC-012 Delegate executor/lifecycle work as Project Workflow 0.5.0, integrate the reviewed source into `main`, and upgrade every currently saved Codex project with an eligible canonical Project Workflow installation.

## Non-Goals

- Reopening or redefining the accepted EPIC-012 feature requirements.
- Claiming native runtime behavior for a host that EPIC-012 did not verify.
- Installing Project Workflow into projects that do not already contain a canonical installation.
- Overwriting user-owned files, unrelated dirty changes, or duplicate nested workflow copies.
- Pushing consumer-project commits or deploying consumer applications merely because their local installation was upgraded.

## Users & Context

The owner uses Codex across multiple saved local projects. Project Workflow 0.4.0 is the latest public package, while the accepted capability-aware Delegate implementation is present only on the reviewed feature lineage. Publication and adoption must preserve the separation between validated source, released artifacts, and locally upgraded consumers.

## Repository Scope

- Primary repository: .
- Repositories touched: the Project Workflow source repository plus each currently saved Codex project root whose own `.project-workflow/manifest.json` proves a canonical installation. The exact consumer set is discovered and recorded before mutation.

## Requirements (Outcome-Focused)

- Prepare one 0.5.0 release candidate whose version authorities, generated mirrors, managed assets, changelog, documentation, CI, and release workflow agree.
- Validate the exact candidate with the complete locked test suite, strict Doctor, source/release contract, built artifacts, and exact-wheel package journeys before integration.
- Integrate the reviewed candidate to `main`, tag that exact main lineage as `v0.5.0`, and publish the same artifacts through the existing Trusted Publishing and GitHub Release workflow.
- Verify public PyPI and GitHub artifacts, hashes, provenance/attestation, and a fresh exact-version installation before declaring the release available.
- Inventory current saved Codex projects and classify each as installed authority root, no installation, non-Git root, dirty/conflicting, already current, or otherwise blocked.
- For every eligible installed authority root, use the public 0.5.0 package's canonical Codex-mode upgrade, preserve user-owned content, and validate the resulting manifest, managed assets, generated helper, and Doctor result.
- Keep each consumer repository's changes scoped and reviewable; do not bypass the clean-worktree guard or infer remote publication authority.
- Retain a machine-readable rollout receipt identifying the inventory snapshot, exact public package, per-project disposition, validation result, and any explicit blocker.

## Acceptance Criteria (Verifiable)

- AC1: All current release identity authorities and current-use documentation consistently identify version 0.5.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged.
- AC2: The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys.
- AC3: The reviewed feature lineage is integrated into `main`; `v0.5.0` is an annotated tag on that exact main lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without divergent rebuilds.
- AC4: Public verification proves `project-workflow==0.5.0` installs fresh, reports 0.5.0, exposes the capability-aware Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance.
- AC5: Every project in the current Codex saved-project inventory has a recorded disposition, and every project with a canonical Project Workflow installation is either upgraded from public 0.5.0 or retained unchanged with a concrete safety blocker.
- AC6: Every successful consumer upgrade preserves user-owned content, produces only expected managed/schema changes, reports package version 0.5.0, and passes its applicable Doctor/upgrade validation.
- AC7: A retained rollout receipt maps every acceptance criterion to exact commits, release URLs or artifact identities, inventory evidence, per-project validation, and any unresolved adoption boundary.

## Proposed Child Work

| ID | Title | Parent ACs | Dependencies |
| --- | --- | --- | --- |
| TASK-073 | Prepare the consistent Project Workflow 0.5.0 release identity | AC1 |  |
| TASK-074 | Validate the exact 0.5.0 release candidate and package journeys | AC2 | TASK-073 |
| TASK-075 | Integrate, tag, and publish Project Workflow 0.5.0 | AC3 | TASK-074 |
| TASK-076 | Verify the public 0.5.0 artifacts and fresh install | AC4 | TASK-075 |
| TASK-077 | Inventory and upgrade every eligible Codex Project Workflow installation and retain the rollout receipt | AC5, AC6, AC7 | TASK-076 |

## Open Questions (Answer Needed)

- None. The owner explicitly requested closeout, release publication, and upgrade of every current Codex project that can safely be upgraded.

## Decisions (Resolved)

- 0.5.0 is the correct semantic version because the capability-aware executor model and subordinate lifecycle are substantive backward-compatible functionality.
- EPIC-012 acceptance is the feature-completion authority; EPIC-013 owns only release preparation, publication, public verification, and adoption.
- Saved projects without a root installation are inventory results, not installation targets.
- Dirty, detached, ambiguous, or failed-plan repositories fail closed and remain unchanged until their blocker is resolved.
- The public exact-version package, not this source checkout, is the consumer upgrade authority.

## Validation Plan

- AC1-AC2: version scans, mirror hashes, strict Doctor, complete pytest suite, release-contract scripts, built-artifact verification, and exact-wheel host journeys.
- AC3-AC4: main/tag ancestry, GitHub Actions release evidence, PyPI metadata/fresh UVX install, GitHub Release asset hashes, and attestation verification.
- AC5-AC6: current Codex project inventory plus read-only root/branch/status/manifest classification; canonical `upgrade --plan`; controlled `upgrade --yes`; before/after Git diff, manifest, helper, and Doctor checks.
- AC7: `evidence/release-rollout-receipt.json` and the parent acceptance audit.
