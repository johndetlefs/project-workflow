# Epic Retro

- Epic: EPIC-013
- Title: Release And Roll Out Project Workflow 0.5.0
- Last updated: 2026-08-20

## Lessons

- Release proof must bind four distinct stages: validated candidate, merged/tagged source, public artifacts/provenance, and consumer adoption. A passing candidate does not prove any later stage.
- For adoption, `upgrade --plan` currency and Doctor health are separate evidence. A repository can be correctly upgraded and still retain unrelated owner-owned workflow debt.
- A plan that says an installation is technically upgradeable does not make a dirty active project safe to mutate. Clean-root eligibility remains an independent gate.
- Current Codex project inventory should be the rollout denominator; projects without canonical installations and ChatGPT-only projects need explicit non-install dispositions rather than silent omission.

## Follow-up Tasks

- Upgrade The Moon Is Hollow and johndetlefs from 0.3.0 after their active workflow changes are committed or otherwise resolved.
- Address existing Doctor debt in Mechanics Playground, Daily Checklist, and Client Management within those projects' own priorities; it is not release-regression work.

## Deferrals

- No parent acceptance criterion was deferred. AC5 explicitly permits an installed root to remain unchanged when a concrete safety blocker is retained; the two dirty-root upgrades are adoption follow-ups, not acceptance deferrals.

## Missed In-Scope Work

- None. All 20 saved projects were classified; every safe canonical installation is current; every unsafe installed root has an exact unchanged blocker.
