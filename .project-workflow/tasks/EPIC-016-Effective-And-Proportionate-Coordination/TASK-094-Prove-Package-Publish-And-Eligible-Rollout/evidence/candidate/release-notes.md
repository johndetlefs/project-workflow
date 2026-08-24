# project-workflow 0.7.0

### Added

- Added one owner-facing Coordinator that carries approved intent through requirements, planning,
  proportionate execution, independent QA, and delivery while keeping Delegate as the compatible
  execution graph.
- Added compact contract-version-2 coordination state with explicit context loading, source-bound
  drift decisions at five lifecycle boundaries, and an earliest sufficient outcome checkpoint.
- Added sanitized behavioural evaluations for drift prevention, Clarify routing, context choice,
  fan-out, stopping behaviour, and preservation of required quality controls.

### Changed

- Changed Clarify to resolve material ambiguity at intake, after planning, or at a detected drift
  boundary without becoming a periodic reviewer or creating another QA loop.
- Changed execution-surface selection so every added context, agent, task, or handoff must earn its
  overhead through a named dependency, risk, authority, or evidence need.
- Changed QA completion so one preserved `Changes Requested` verdict can close through named
  affected validation and an explicit resolved disposition without commissioning a second review.

### Fixed

- Fixed stale coordination decisions remaining usable after source or repository authority changed.
- Fixed long-running work drifting through narrowing, omission, proxy substitution, stale context,
  or unverified worker returns without a deterministic lifecycle block.
- Fixed post-proof continuation that could repeat broad validation or review after sufficient proof
  had already passed.
