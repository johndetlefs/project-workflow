# Requirements

## Summary

- Task: TASK-109
- Title: Prepare and prove the exact Project Workflow 0.9.1 candidate
- Parent AC Coverage: AC1, AC2
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Prepare one coherent Project Workflow 0.9.1 maintenance identity and certify one clean exact
candidate that contains EPIC-019's accepted structural work without changing the public v0.9
contract or reopening its completed independent QA.

## Intent Spine

- OC1 — Completion capability: The release branch contains one coherent 0.9.1 identity and a clean
  retained candidate whose exact wheel and sdist are ready for reviewed integration.
- OC2 — Material capabilities: Version alignment, changelog/current-doc pins, generated runtime,
  static/documentation/architecture gates, complete tests, Doctor, source contract, build inventory,
  exact-package journeys, and candidate receipt.
- OC3 — Success journey: Update canonical version authorities, regenerate once, pass cheap-to-full
  source proof, commit the source, validate the clean commit, build once, inspect and exercise those
  exact artifacts, then freeze their hashes for TASK-110.
- OC4 — Successful-but-wrong result: A dirty or uncommitted source is called releasable, 0.9.0 pins
  remain in current guidance, generated copies drift, historical evidence is rewritten, or a
  rebuilt artifact replaces the one actually journey-tested.
- OC5 — Exclusions: No public push/merge/tag/publication in this child, no consumer mutation, no
  product redesign, no repeated broad QA, and no Claude runtime certification claim.
- OC6 — Assumptions: 0.9.1 is the correct compatible maintenance version and EPIC-019's passing QA
  remains current unless a release-only edit changes product behaviour.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Child Charter

### Inherited Invariants

- Public commands, schemas, lifecycle semantics, asset version 8, and repository schema remain compatible with 0.9.0; only package version/current pins and approved maintenance content change.
- Reviewed source, merge lineage, tag, public wheel/sdist, GitHub release, and provenance identify one immutable 0.9.1 release.
- EPIC-019 evidence and historical workflow records are preserved; release evidence is additive.
- Publication passes before consumer mutation, and every upgrade uses public `project-workflow==0.9.1` rather than the source checkout.
- Only clean, unambiguous canonical authority roots are eligible; user-owned content and unrelated work remain untouched.
- Consumer diffs are not committed, pushed, merged, released, or deployed by this Epic.
- No project is reported upgraded when blocked, partially applied, stale, or unvalidated.
- TASK-102 remains blocked until the exact authenticated Claude canary exists.

### Invalid Substitutes

- EPIC-019's local wheel offered as a public 0.9.1 release.
- A branch push, PR, tag, GitHub run, or PyPI page offered alone as complete release proof.
- Rebuilding or changing the candidate between reviewed source, tag, trusted publication, and public verification without a new immutable version.
- A project label, nested helper copy, or stale saved path offered as a canonical installation.
- A successful upgrade command without clean-root preflight, reviewed fingerprint, no-op re-plan, scoped diff, exact version, and Doctor evidence.
- Forced mutation of dirty, active, detached, ambiguous, nested, or unreconciled consumer state.
- Package or fixture proof offered as authenticated Claude Code runtime certification.

### Artifact Targets

- One clean reviewed 0.9.1 source commit and retained candidate receipt.
- PyPI `project-workflow==0.9.1` and GitHub Release `v0.9.1` with verified wheel, sdist, hashes, receipt, package journeys, and attestations.
- Independent public-install and upgrade journey receipt.
- Complete local project inventory with one disposition per entry.
- Validated 0.9.1 managed assets at every eligible canonical consumer root.
- Consolidated machine-readable release/rollout receipt plus parent acceptance audit.

### Parent AC Proof Ownership

- AC1: owner `TASK-109`; required evidence: Coherent version scan, generated parity, source contract, package inventory, and diff hygiene
- AC2: owner `TASK-109`; required evidence: Locked gates, complete suite, strict Doctor, exact build/journeys, retained EPIC-019 QA, and candidate receipt

## Goal

Produce the exact clean 0.9.1 source and distributions that later release actions may publish
without guessing which code or artifact was reviewed.

## Non-Goals

- GitHub integration, tag creation, trusted publication, public verification, and consumer rollout.
- New runtime capabilities or changes to existing public command/schema contracts.
- Re-running independent structural QA when release-only changes preserve its candidate semantics.

## Users & Context

Project Workflow maintainers need a clean immutable release candidate after EPIC-019 stopped at a
validated working-tree candidate. The public release must not be assembled from that dirty state.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Align every current package and documentation identity to 0.9.1 while leaving historical release
  evidence and the frozen 0.9.0 compatibility baseline unchanged.
- Commit the complete structural work and version preparation, then validate the clean commit from
  the locked Python 3.10 environment.
- Build one wheel/sdist set, inspect membership and metadata, and execute all supported package
  journeys from the exact wheel.
- Retain source commit, artifact hashes, validation results, EPIC-019 QA identity, and explicit
  not-yet-published boundary in child evidence.

## Acceptance Criteria (Verifiable)

- AC1: All current version authorities, managed guidance, CI/release pins, changelog, manifest, and
  generated runtime consistently identify 0.9.1 while historical records and the 0.9.0
  compatibility baseline remain unchanged. Covers parent AC1.
- AC2: A clean committed source passes locked documentation, architecture, Ruff, format, mypy,
  deterministic-runtime, complete pytest, strict Doctor, and clean release-source checks. Covers
  parent AC1 and AC2.
- AC3: Exactly one wheel/sdist set from that commit passes inventory inspection and exact-wheel
  fresh/current/legacy/no-op/Doctor/lifecycle/helper journeys, with hashes retained. Covers parent
  AC2.
- AC4: Retained QA and compatibility evidence demonstrates release-only changes did not alter the
  approved EPIC-019 outcome, and delivery remains unpushed/unpublished until TASK-110. Covers parent
  AC2.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Treat 0.9.0 references in historical records and compatibility baselines as evidence, not stale
  current pins.
- Build once after the clean source commit; later release verification must identify that lineage
  even though trusted CI may create the public distributions.

## Validation Plan

- Run version/document/source scans, deterministic generation, locked static gates, complete tests,
  strict Doctor, clean release contract, one build/inventory pass, exact package journeys, and
  compare the retained EPIC-019 QA scope against the release-only diff.
