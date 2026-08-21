# Epic Retro

- Epic: EPIC-014
- Title: Intent Integrity And Outcome Proof
- Last updated: 2026-08-21

## Lessons

- Put the one- or two-sentence owner Intent first and ask whether that meaning is accurate. IDs,
  hashes, AC ranges and task lists can preserve provenance, but asking the owner to approve them is
  not evidence that the agent understood the requested outcome.
- Treat the Intent as the governing meaning across requirements, decomposition, implementation and
  QA. Deterministic gates can enforce identity, coverage, freshness and lifecycle consequences; they
  cannot turn an agent-authored semantic classification into truth.
- A green-but-wrong regression must contain an actually narrowed downstream result and derive its
  verdict from the recorded outcome fields. Injecting a `proxy` label only proves that a gate obeys
  the label.
- Outcome proof must be independently inspectable. Retain exact candidate distributions, bind every
  shipped and manifest-covered source, capture real approval/lifecycle observations mechanically,
  and preserve blocking review reports as part of the remediation history.
- Independent QA materially improved this Epic: two Changes-requested reviews exposed nine false-
  pass risks before the final read-only review returned Pass with no blockers.

## Follow-up Tasks

- A separately authorized release task should rebuild from the reviewed commit, repeat exact-package
  checks, publish through the trusted release path, and prove consumer upgrades/adoption separately.
- Monitor future real tasks and behavioural evaluation runs for new under-delivery or gold-plating
  patterns; add sanitized cases only when observed evidence justifies them.

## Deferrals

- None inside the approved local implementation envelope. Merge, tag, publication, release, rollout,
  consumer adoption, final owner acceptance and commercial validation were explicitly outside this
  Epic's delivery authority and remain unproven.

## Missed In-Scope Work

- None. All fifteen parent ACs pass the generated acceptance audit, all five children are Complete,
  and the final independent review verified all nine earlier blocking findings as resolved.
