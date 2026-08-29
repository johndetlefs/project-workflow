# Requirements

## Summary

- Task: TASK-111
- Title: Verify the public Project Workflow 0.9.1 release
- Parent AC Coverage: AC4
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Independently retrieve Project Workflow 0.9.1 from PyPI and GitHub, verify artifact identity and
attestations, and exercise the public exact-version package in disposable fresh and upgrade
journeys before any consumer installation changes.

## Intent Spine

- OC1 — Completion capability: Anyone can obtain 0.9.1 publicly and reproduce its version, assets,
  installation, upgrade, Doctor, and representative lifecycle results.
- OC2 — Material capabilities: Independent downloads, hash comparison, metadata, attestations,
  exact public uvx execution, fresh/current/legacy/no-op journeys, Doctor, and lifecycle proof.
- OC3 — Success journey: Download from both channels, compare receipt/hashes/provenance, run public
  version and full disposable package journeys, then record the public checkpoint for rollout.
- OC4 — Successful-but-wrong result: GitHub assets exist but PyPI differs, local cached/source
  artifacts are exercised instead of public bytes, or version output substitutes for managed asset
  and upgrade behaviour.
- OC5 — Exclusions: No consumer mutation, no republishing, no source change, and no Claude live
  runtime certification.
- OC6 — Assumptions: Public registries and GitHub attestations are reachable after TASK-110 passes.
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

- AC4: owner `TASK-111`; required evidence: Public PyPI/GitHub hashes, attestations, version/assets, and disposable exact-version journeys

## Goal

Prove the exact package consumers will install is publicly obtainable, authentic, and operational.

## Non-Goals

- Source modification, publication repair, existing consumer mutation, and owner acceptance.

## Users & Context

Consumer upgrades must use public 0.9.1, so availability and behaviour require proof independent of
the release job and local candidate.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Download GitHub Release and PyPI distributions independently and compare filenames, sizes,
  hashes, receipt, source/tag identity, and attestations.
- Run `uvx --from project-workflow==0.9.1 project --version` without source checkout authority.
- Run the repository's public exact-package journeys across all supported agent modes and upgrade
  states, including dependency-free helper and representative lifecycle behaviour.
- Record a passing public outcome checkpoint before TASK-112 may mutate any consumer.

## Acceptance Criteria (Verifiable)

- AC1: PyPI and GitHub wheel/sdist bytes and release metadata agree with the trusted receipt and
  verified tag/source attestation. Covers parent AC4.
- AC2: Public exact-version execution reports 0.9.1 and disposable fresh/current/legacy/no-op,
  Doctor, lifecycle, and helper journeys pass across supported agent modes. Covers parent AC4.
- AC3: Evidence proves public sources were used and records the passing rollout checkpoint without
  claiming consumer adoption. Covers parent AC4.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Public verification must use fresh downloads and exact version constraints.

## Validation Plan

- Compare downloads/receipt/hashes/attestations and run exact public uvx plus the disposable public
  package journey suite.
