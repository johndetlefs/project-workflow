# project-workflow 0.6.0

### Added

- Added one- or two-sentence plain-language Intent and stable outcome commitments to current Task and Epic requirements, with meaning-first approval summaries that ask the owner to confirm the requested outcome rather than approve IDs and hashes.
- Added sourced Epic intent audits, semantic narrowing classifications, current-identity lifecycle gates, child outcome-proof ownership, adversarial QA checks, deterministic behavioral fixtures, and inspectable end-to-end dogfood evidence.
- Added packaged four-host journeys and source/package parity checks for the intent-integrity contract, including current and legacy upgrade paths.

### Changed

- Changed readiness, status, QA and closeout evidence so green implementation proxies cannot substitute for the approved user outcome; Epic status now aggregates child-owned outcome evidence and preserves explicit validation boundaries.
- Added continuation sufficiency and materiality gates so post-pass work stops when the approved outcome is proven, while material contradictions still reopen the relevant validation layer.

### Fixed

- Fixed status projections that could obscure missing Epic-level outcome proof behind otherwise complete child lifecycle state.
- Fixed continuation guidance that could over-expand a bounded review into low-value deep dives after sufficient proof had already been obtained.
- Fixed historical structured-evidence checks so retained wheel members or recorded ancestor commits remain verifiable after later source revisions instead of forcing completed proof to track a moving file.
