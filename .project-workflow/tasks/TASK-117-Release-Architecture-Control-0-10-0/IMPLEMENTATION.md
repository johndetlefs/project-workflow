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
- [x] AC4: Hosted PR checks pass and reviewed `main` contains the complete release candidate.
- [x] AC5: Immutable `v0.10.0` on reviewed `main` publishes successfully through the protected workflow.
- [x] AC6: Public GitHub/PyPI artifacts, digests, attestation, isolated version and journeys verify.
- [x] AC7: Release evidence retains the Claude/no-adoption/no-owner-acceptance boundaries.

## Validation

- AC1: Clean source contract passed at `09bcd3e20e5775f0765f82caa5934044fc914596` for version 0.10.0 and tag `v0.10.0`.
- AC2: Documentation, Architect/runtime generation, Ruff, Ruff format, mypy and 592/592 locked tests passed on 2026-09-01.
- AC3: One local build produced wheel `sha256:81bb4f3c516b885fd40c1190aa1c48fb99acfd4db4430c6679c2a526dae63622` and sdist `sha256:5607ffbcd6903aec5c7c8179550a041feda33721ce6f97bd6c80e4f21a6be9d0`; receipt verification and exact-wheel journeys passed.
- AC4: PR #31 passed hosted CI and merged head `ea99b35` into `main` at `0f9b200`; the required `main` CI run 33471192826 passed.
- AC5: Annotated tag `v0.10.0` resolves to `0f9b200`; protected release run 33471322579 passed build, attestation, trusted PyPI publication and GitHub Release creation.
- AC6: Public GitHub/PyPI wheel and sdist are byte-identical at `sha256:61dff0118f01dc047c127d26cd225b0ffacfc65d01a1163d5363cab424334541` and `sha256:3b9a9ccc430f35e47ad25e6e5219d45f2f7a946566af78736fe25fa752e43205`; receipt, both attestations, isolated `uvx` and exact public-wheel journeys passed.
- AC7: Changelog and release receipt retain Codex-only Project Architect proof, the exact Claude blocker, no consumer adoption and no owner-acceptance claim; repository inspection found no consumer mutation.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | PR #31 merged at `0f9b200`; `v0.10.0` | Local, hosted main, release workflow and independent public verification pass | PyPI and GitHub Release 0.10.0 published; no rollout | `EVIDENCE.json`; `evidence/release-verification-v0.10.0.json`; release run 33471322579 |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Prepare coherent 0.10.0 source | Update version authority, current pins and changelog; regenerate managed runtime. | AC1, AC7 | Source contract and diff inspection pass. | Done | | Version-owned source, current docs, workflows, generated runtime, workflow task docs | No | bounded-return |
| 2 | Certify one local candidate | Run locked quality gates, build once, retain receipt and exercise the exact wheel. | AC2, AC3 | All local candidate gates pass against one commit and artifact set. | Done | 1 | Validation output and task evidence | No | bounded-return |
| 3 | Review and integrate | Push the existing branch, require hosted PR CI and merge the reviewed candidate to main; retain independent adversarial QA as the final completion gate. | AC4, AC7 | PR checks and merge ancestry prove integration. | Done | 2 | Task QA/evidence, branch, PR | No | bounded-return |
| 4 | Publish immutable release | Tag the verified main commit once and let the protected workflow publish through trusted PyPI and GitHub jobs. | AC5, AC7 | Tag and release workflow pass without alternate publication. | Done | 3 | Tag and hosted release state | No | bounded-return |
| 5 | Verify public release | Independently compare public artifacts/receipts, verify attestation, and run isolated exact-version journeys. | AC6, AC7 | Public 0.10.0 proof packet passes and retains explicit boundaries. | Done | 4 | EVIDENCE.json and release verification receipt | No | bounded-return |

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: Release run 33471322579, GitHub Release `v0.10.0`, PyPI 0.10.0,
  `evidence/release-verification-v0.10.0.json`, and independently downloaded exact-wheel journeys.
- Reviewer independence: Read-only Codex reviewer session
  `01a05b55-ffdc-7ae1-8810-75c229bd2565`; no filesystem, Git, workflow or external mutations.
- Evidence: Every AC, current source/tag/PR/provider state, release job logs, retained candidate and
  public receipts/checksums/journeys, attestations, Doctor and the Claude/no-adoption boundaries.
- Findings: Pass with one follow-up. Provider-observed publication and exact public-artifact proof
  prevent a local-build or release-page proxy from satisfying the approved job. AC5 and AC6 require
  the immutable tag workflow, trusted publication, public matching artifacts and isolated journeys.
  One medium non-blocking documentation defect: `RELEASING.md` used a package spec where
  `verify_package_journeys.py` requires an exact wheel path. Corrected during closeout. Validation
  impact: documentation-only and unaffected for the already published 0.10.0 artifacts; the
  documentation checker is rerun after the correction. Original QA verdict retained.

## Architecture Conformance

- Authority identity: Not required for local classification; authority is `docs/architecture.md`.
- Candidate: git:09bcd3e20e5775f0765f82caa5934044fc914596
- Mechanical checks: candidate=git:09bcd3e20e5775f0765f82caa5934044fc914596; receipt=.project-workflow/tasks/TASK-117-Release-Architecture-Control-0-10-0/evidence/local-candidate-receipt-v0.10.0.json
- Deviations: None; source follows the existing release boundary without structural change.
- Verdict: Pass

## Retro

- Date: 2026-09-01
- Reusable lessons: A pre-integration candidate build proves the reviewed source but does not own
  the authoritative public digests after merge; retain both identities and let the tagged workflow
  receipt own publication. Treat protected-environment approval as a distinct owner-controlled
  release gate. When attestation verification cannot initialise its verifier, classify it as
  infrastructure and permit one bounded retry before diagnosing the artifact; both exact public
  distributions passed that retry. Package-journey verification must use an exact downloaded wheel,
  not a registry requirement string.
- Conventions or agent assets updated: `RELEASING.md` now binds `WHEEL` to the independently
  downloaded PyPI artifact and uses that exact path for package journeys and attestation.
- Follow-up tasks: None required for this release. Authenticated Claude discovery/invocation and
  consumer adoption remain separate future decisions, not deferred work inside TASK-117.
- Missed in-scope work: None. The stale runbook example was corrected during closeout and its
  documentation contract passed; it did not affect the already published artifacts.

## Notes

- Task: TASK-117
- Title: Release Architecture Control 0.10.0
- Created: 2026-09-01
