# Epic Retro

- Epic: EPIC-020
- Title: Release Structural Cleanup And Upgrade All Projects
- Last updated: 2026-08-29

## Lessons

- Release proof must remain split into candidate, integration, trusted publication, public
  retrieval, and consumer adoption gates. Each caught a different failure class and none could
  truthfully substitute for the next.
- A previous uncommitted managed-asset rollout makes the next clean-root upgrade ineligible even
  when the dirty paths appear workflow-related. Long-term maintainability requires each consumer
  repository to reconcile its workflow upgrade under that repository's own commit authority.
- Codex saved projects are not a complete installation inventory. A manifest scan found three
  additional roots, including one duplicate authority and two unregistered repositories.
- Restricted environments need writable task-local UV and GitHub attestation caches; cache setup
  failure must be separated from package or provenance failure.

## Follow-up Tasks

- Reconcile the existing dirty workflow and application state in each of the 14 blocked roots
  under that repository's own authority, then rerun public 0.9.1 plan/fingerprint/apply/no-op and
  Doctor validation. Do not create duplicate Project Workflow task state for those repositories.
- Decide which Healthdirect GPT checkout is canonical before any future workflow mutation there.
- Decide whether the Avoca Interiors and Shopify Theme manifest roots should be registered as Codex
  projects or retired from the active project estate.

## Deferrals

- None. The 14 unchanged roots satisfy the approved safety disposition rather than deferring an
  EPIC-020 acceptance criterion; their actual upgrades require later repository-specific work.

## Missed In-Scope Work

- None. Release, public verification, complete inventory, the one safe current-root result, and
  exact blockers for every unsafe root are retained. Consumer reconciliation was explicitly out of
  scope and was not smuggled into this release.
