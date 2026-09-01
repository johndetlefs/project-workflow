# Requirements

## Summary

- Task: TASK-117
- Title: Release Architecture Control 0.10.0
- Last updated: 2026-09-01
- Intent contract: full

## Intent

Publish the completed architecture-control capability as Project Workflow 0.10.0 through the
repository's trusted release path, then independently prove the exact public GitHub and PyPI
artifacts without claiming Claude runtime support or consumer adoption.

## Intent Spine

- OC1 — Completion capability: Project Workflow 0.10.0 is immutably tagged on reviewed `main`,
  published through trusted GitHub Actions to PyPI and GitHub Releases, and independently verified.
- OC2 — Material capabilities: Version-owned source is coherent; the reviewed candidate passes
  locked static, test, generation, build and exact-package gates; hosted CI and release jobs pass;
  public files, receipts, attestations and package journeys resolve to the same release.
- OC3 — Success journey: Prepare one clean 0.10.0 candidate, merge it after hosted CI, create the
  immutable `v0.10.0` tag on that `main` commit, let the protected workflow publish once, then
  install and exercise the public exact version from an isolated directory.
- OC4 — Successful-but-wrong result: A tag or release page exists but was not built from reviewed
  `main`, PyPI and GitHub contain different artifacts, current source still declares 0.9.2, the
  package journey fails, or generated parity is substituted for real publication proof.
- OC5 — Exclusions: No consumer rollout or repository upgrades; no Claude runtime or cross-host
  certification; no tag movement, artifact replacement, manual PyPI upload, unrelated feature work,
  or claim of owner acceptance beyond the explicit release authority.
- OC6 — Assumptions: 0.10.0 is the appropriate backward-compatible minor version for the new
  architecture capability; GitHub `pypi` environment and trusted-publisher configuration remain
  valid; registry/provider interruptions are distinguished from product failures.
- OC7 — Authority source: Owner instruction in this task on 2026-09-01: “let's push a release,
  please,” following local EPIC-021 closeout.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: No
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-09-01
- Approval note / source: Codex task owner reply on 2026-09-01: Yep, go for it.
- Approved artifact identity: sha256:22208d9a00548c13d476186e976d2b84e94a41e949c5402e186d99e5ee0a6a0b

## Goal

Make the architecture-control capability installable as the current public Project Workflow
release with source, hosted, registry and exact-package proof bound to one immutable version.

## Non-Goals

- Do not modify or upgrade consumer repositories.
- Do not claim authenticated Claude discovery, invocation or cross-host support.
- Do not add architecture features, restructure the implementation, or widen EPIC-021.
- Do not bypass the protected release workflow, reuse a public version, or move a tag.
- Do not treat publication as adoption or owner acceptance.

## Users & Context

Project Workflow maintainers and public users who need the architecture-control feature through the
normal package and repository release channels.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Release version is 0.10.0 and every current version-owned source, manifest, workflow pin,
  installation example and changelog heading agrees.
- The release preparation follows the established `RELEASING.md` and `docs/architecture.md`
  contracts without changing structural responsibilities or dependency direction.
- The exact candidate passes locked source, generated-parity, static, full-suite, build,
  distribution-receipt and exact-wheel journey validation before integration.
- The candidate is pushed to its existing branch, reviewed through a pull request, and merged only
  after required hosted checks pass.
- The immutable `v0.10.0` tag is created only on the verified `main` merge commit and pushed once.
- The protected release workflow publishes the attested wheel and sdist to PyPI and the same files,
  receipts and checksums to GitHub Releases.
- Public verification uses independently downloaded/isolated surfaces and records exact tag,
  workflow, artifact digests, attestation and package-journey evidence.
- Release notes retain the honest Claude runtime blocker and distinguish release from adoption.

## Acceptance Criteria (Verifiable)

- AC1: `release_contract.py check-source --version 0.10.0 --tag v0.10.0 --clean` passes on the clean
  release candidate and all current version-owned surfaces resolve to 0.10.0.
- AC2: Locked documentation, Architect/runtime generation, Ruff, Ruff format, mypy and all tests
  pass on the exact candidate.
- AC3: One wheel/sdist build produces a verified release receipt and SHA256SUMS, and the exact wheel
  passes the repository's package journeys before integration.
- AC4: The candidate pull request targets current `main`, required hosted CI passes, and the merged
  `main` commit contains the complete TASK-117 and EPIC-021 source.
- AC5: `v0.10.0` points to that reviewed `main` commit and the protected release workflow publishes
  successfully without rebuilding or replacing a public identity outside the declared workflow.
- AC6: PyPI and GitHub Release expose the expected 0.10.0 files and matching authoritative digests,
  GitHub attestation verifies, and isolated `uvx` plus public exact-version package journeys pass.
- AC7: Release notes and closeout make no Claude/cross-host runtime, rollout, deployment, adoption,
  or owner-acceptance claim; no consumer repository is mutated.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Use 0.10.0 because architecture control is a backward-compatible public capability added after
  0.9.2; do not misclassify it as a patch.
- The owner confirmed the meaning-first 0.10.0 release synopsis on 2026-09-01 with “Yep, go for it.”
- Architecture impact is `local`: release-owned version and workflow pins follow the established
  release pattern and do not alter the structural contract in `docs/architecture.md`.
- Use the existing `codex/architecture-control` branch and one PR; do not manufacture a second
  implementation branch or rebuild the already reviewed feature separately.
- Publication and public verification are in scope; consumer adoption remains a later decision.

## Validation Plan

- AC1: Run the source contract against version 0.10.0 and inspect all changed version-owned files.
- AC2: Run every contributor quality gate and the complete locked suite.
- AC3: Build once, create and verify the candidate receipt, and run exact-wheel package journeys.
- AC4: Inspect PR base/head/source, required GitHub checks and the eventual `main` merge identity.
- AC5: Inspect the immutable tag and release workflow, including protected publication jobs.
- AC6: Verify public PyPI/GitHub artifacts, checksums, attestation, isolated `uvx` and public package
  journeys against 0.10.0.
- AC7: Diff release notes and inspect Git/consumer boundaries; generated assets or local packages are
  invalid substitutes for hosted/public proof.
