## User Story

As a Project Workflow user, I want architecture control published through the normal trusted
release channels, so that I can install and use the capability from an immutable verified version.

## Architecture Impact

- Classification: local
- Reason: Version preparation, reviewed integration, immutable tagging and trusted publication
  follow the established release pattern without changing structural responsibilities, dependency
  direction, source ownership, shared-state boundaries, extension points or architecture limits.
- Architecture authority: docs/architecture.md
- Authority identity: Not required for local classification.
- Architect invocation: Not required for local classification.
- Architect decision identity: Not required for local classification.
- Affected boundaries: Version authority, current documentation, CI/release pins, changelog,
  distribution artifacts and hosted publication evidence.
- Architecture decision: Preserve the existing source/build/publish boundaries in RELEASING.md and
  docs/architecture.md; release the reviewed capability as one backward-compatible minor version.
- Measurable constraints: Release source contract, generated parity, locked quality gates, one-build
  receipt, exact-wheel journeys, immutable tag ancestry, public checksums and attestation.
- Conformance plan: Run the canonical local gates on one clean candidate, require hosted PR/release
  checks, and independently verify public artifacts before completion.

## Acceptance Criteria

- [x] AC1: Every current version-owned surface and the clean source contract identify 0.10.0.
- [x] AC2: Locked documentation, generation, static analysis and all tests pass.
- [x] AC3: One candidate wheel/sdist build has a verified receipt and passing exact-wheel journeys.
- [ ] AC4: Hosted PR checks pass and reviewed `main` contains the complete release candidate.
- [ ] AC5: Immutable `v0.10.0` on reviewed `main` publishes successfully through the protected workflow.
- [ ] AC6: Public GitHub/PyPI artifacts, digests, attestation, isolated version and journeys verify.
- [ ] AC7: Release evidence retains the Claude/no-adoption/no-owner-acceptance boundaries.

## Validation

- AC1: Clean source contract passed at `09bcd3e20e5775f0765f82caa5934044fc914596` for version 0.10.0 and tag `v0.10.0`.
- AC2: Documentation, Architect/runtime generation, Ruff, Ruff format, mypy and 592/592 locked tests passed on 2026-09-01.
- AC3: One local build produced wheel `sha256:81bb4f3c516b885fd40c1190aa1c48fb99acfd4db4430c6679c2a526dae63622` and sdist `sha256:5607ffbcd6903aec5c7c8179550a041feda33721ce6f97bd6c80e4f21a6be9d0`; receipt verification and exact-wheel journeys passed.
- AC4: GitHub PR identity, merge ancestry and required CI status.
- AC5: Tag ancestry and protected release workflow status.
- AC6: Independent public downloads, checksums, attestation, isolated `uvx` and package journeys.
- AC7: Release-note/diff review and repository-scope inspection.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/architecture-control at `09bcd3e`; PR pending | Source/static/592 tests/one-build receipt/exact-wheel journeys pass | Not released | `evidence/local-candidate-receipt-v0.10.0.json`; `evidence/local-package-journeys-v0.10.0.json`; public EVIDENCE.json pending |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Prepare coherent 0.10.0 source | Update version authority, current pins and changelog; regenerate managed runtime. | AC1, AC7 | Source contract and diff inspection pass. | Done | | Version-owned source, current docs, workflows, generated runtime, workflow task docs | No | bounded-return |
| 2 | Certify one local candidate | Run locked quality gates, build once, retain receipt and exercise the exact wheel. | AC2, AC3 | All local candidate gates pass against one commit and artifact set. | Done | 1 | Validation output and task evidence | No | bounded-return |
| 3 | Review and integrate | Run independent adversarial QA, push the existing branch, require hosted PR CI and merge the reviewed candidate to main. | AC4, AC7 | PR checks and merge ancestry prove integration. | To Do | 2 | Task QA/evidence, branch, PR | No | bounded-return |
| 4 | Publish immutable release | Tag the verified main commit once and let the protected workflow publish through trusted PyPI and GitHub jobs. | AC5, AC7 | Tag and release workflow pass without alternate publication. | To Do | 3 | Tag and hosted release state | No | bounded-return |
| 5 | Verify public release | Independently compare public artifacts/receipts, verify attestation, and run isolated exact-version journeys. | AC6, AC7 | Public 0.10.0 proof packet passes and retains explicit boundaries. | To Do | 4 | EVIDENCE.json and release verification receipt | No | bounded-return |

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: ____
- Intent adversarial verdict: ____
- Could every AC pass while the approved user job remains undone: ____
- Intent audit state: ____
- Outcome journey evidence: ____
- Reviewer independence: ____
- Evidence: ____
- Findings: ____

## Architecture Conformance

- Authority identity: Not required for local classification; authority is `docs/architecture.md`.
- Candidate: git:09bcd3e20e5775f0765f82caa5934044fc914596
- Mechanical checks: candidate=git:09bcd3e20e5775f0765f82caa5934044fc914596; receipt=.project-workflow/tasks/TASK-117-Release-Architecture-Control-0-10-0/evidence/local-candidate-receipt-v0.10.0.json
- Deviations: None; source follows the existing release boundary without structural change.
- Verdict: Pass

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-117
- Title: Release Architecture Control 0.10.0
- Created: 2026-09-01
