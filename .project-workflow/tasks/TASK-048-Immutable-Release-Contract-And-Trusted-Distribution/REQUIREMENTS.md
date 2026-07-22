# Requirements

## Summary

- Task: TASK-048
- Title: Immutable Release Contract And Trusted Distribution
- Last updated: 2026-07-22

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Not approved
- Approval date: Not approved
- Approval note / source: Not approved
- Approved artifact identity: Not approved

## Backlog Source

- ID: BL-010
- Title: Immutable Release Contract And Trusted Distribution
- Type: Task Candidate
- Priority: High
- Status before promotion: Accepted
- Outcome: Make every published project-workflow release an immutable, attributable, reproducible contract across version, commit, tag, package, changelog, generated assets, CI result, and canonical install command.
- Notes: Unambiguous next execution item after completed TASK-047. Establish the immutable release and trusted distribution foundation before operational status, assurance, extensions, workspace coordination, or adoption work.

## Goal

Give maintainers and adopters one trustworthy answer to "what exact project-workflow release am I using?" Every published release must bind its human version, source commit, immutable tag, built package, changelog entry, generated assets, repository compatibility contract, CI evidence, and canonical install command into one verifiable release identity.

## Non-Goals

- Do not build the broader operational status and next-action experience owned by BL-004.
- Do not introduce the modular extension platform, assurance profiles, workspace coordination, or adoption programme owned by BL-009, BL-019, BL-017, and BL-020.
- Do not support multiple package registries or installer ecosystems in the first trusted distribution contract.
- Do not claim that historical version `0.1.1` or earlier untagged repository states were published under the new contract.
- Do not require byte-identical builds across operating systems. Reproducibility means locked release inputs and a verifiable digest for the exact published artifacts; cross-platform bit-for-bit reproducibility is separate work unless implementation evidence shows it is low-cost and reliable.
- Do not automate a public release without the repository owner's explicit authorization for that external publication.

## Users & Context

- Repository maintainers need a repeatable release operation that fails closed when version, source, generated assets, tests, documentation, or package contents disagree.
- New adopters need a canonical install command that resolves an immutable released artifact rather than the moving head of `main`.
- Existing adopters need an equally immutable upgrade command and enough release identity to determine what code and schema contract produced their managed assets.
- Reviewers need durable CI and artifact evidence that connects a published version to the exact reviewed commit.
- Current-state evidence on 2026-07-22: the repository has no Git tags or GitHub Actions workflows; canonical README commands install from an unpinned GitHub URL; version `0.1.1` is declared in both `pyproject.toml` and `src/project_workflow/__init__.py`; no dependency lockfile exists; and the PyPI JSON endpoint for `project-workflow` reports no existing project.

## Requirements (Outcome-Focused)

- R1. Define one release identity tuple containing at least package version, full source commit SHA, immutable release tag, asset version, repository schema version, changelog release heading, built wheel and source-distribution filenames, SHA-256 digests, CI run identity, and canonical install and upgrade commands.
- R2. Make the intended release version come from one authoritative repository source, with every runtime, package metadata, manifest, generated asset, and documentation consumer either deriving it or being mechanically checked against it.
- R3. Provide a release validation and publication workflow that starts from a reviewed commit on `main`, rejects dirty, divergent, reused, missing, or internally inconsistent release identities, and cannot silently publish from an arbitrary local checkout.
- R4. Run the complete test suite with the UVX packaging test enabled, CLI mirror/parity checks, package build checks, generated-asset checks, backlog validation, Doctor, and diff hygiene before publication can proceed.
- R5. Build both a wheel and source distribution once in CI, inspect their contents, record their digests, and promote those exact artifacts to the chosen public distribution target without rebuilding them in a later job.
- R6. Publish through short-lived platform identity or trusted publishing rather than a long-lived repository package token. Any required GitHub or registry environment must retain an explicit owner-controlled approval boundary.
- R7. Create a durable release receipt, available from the GitHub release and CI result, that lets a reviewer trace the released version and package digests back to the exact source commit, tag, changelog entry, compatibility versions, and successful validation run.
- R8. Make released tags and versions append-only: the workflow must reject an existing version or tag, documentation must forbid retagging or overwriting a published release, and correction must use a new version.
- R9. Replace canonical unpinned install and upgrade guidance with commands that resolve the chosen immutable package version. Mutable source installs may remain only when clearly labelled as development or unreleased usage.
- R10. Prove the packaged user journey from the built artifact in clean disposable repositories: a fresh `project init`, an existing-repository `project upgrade`, version reporting, installed managed-asset identity, and Doctor/compatibility behavior must all match the release receipt.
- R11. Commit `uv.lock` as the reproducible maintainer and CI dependency resolution, and make the Codex local environment plus CI use locked synchronization with Python 3.10 or another explicitly supported interpreter. The lockfile constrains development and release inputs; it does not constrain downstream library consumers.
- R12. Document the maintainer release sequence, required platform configuration, failure recovery, rollback boundary before publication, forward-fix rule after publication, and the exact evidence that distinguishes a validated candidate from a publicly released version.

## Acceptance Criteria (Verifiable)

- AC1: One documented command or manually approved GitHub workflow invocation validates a proposed release from `main` and produces a machine-readable release receipt containing the complete R1 identity tuple; fixture tests prove missing or mismatched identity fields fail before publication.
- AC2: Package version has one authoritative repository source, and automated checks prove `pyproject` metadata, `project_workflow.__version__`, generated manifest/package identity, tag, and changelog release heading all agree for a release candidate.
- AC3: The release gate runs the full repository validation required by R4 on supported Python, with the UVX test executed rather than skipped, and publication jobs cannot run when any required check fails or when the candidate commit is not the reviewed `main` commit.
- AC4: CI builds one wheel and one source distribution, validates their expected package data and CLI entry point, publishes or stages those exact files without rebuilding, and records SHA-256 digests that match the downloadable artifacts.
- AC5: The chosen public publisher uses trusted, short-lived workload identity with an owner-controlled release environment; repository configuration and documentation contain no long-lived publication credential.
- AC6: A version and tag can be published only once. Automated negative tests or a safe dry run demonstrate rejection of an existing version, moved/reused tag, source/tag mismatch, dirty changelog state, or rebuilt artifact digest mismatch.
- AC7: README and maintainer documentation identify one canonical version-pinned init command and one version-pinned upgrade command. Automated documentation checks reject an unqualified `git+...project-workflow.git` command presented as canonical release usage.
- AC8: Clean disposable-repository tests install the built wheel or staged published artifact, then prove fresh init and legacy/current upgrade behavior, package/version reporting, managed-asset parity, manifest identity, and clean expected Doctor results against the same release receipt.
- AC9: `uv.lock` is committed; a clean Codex worktree setup succeeds with locked Python 3.10 dependencies; the Test action runs all tests; and CI fails if `pyproject.toml` changes would alter the lockfile.
- AC10: The release runbook identifies candidate, approved, published, and failed states; names the owner approval needed for external publication; specifies pre-publication abort and post-publication forward-fix behavior; and can be followed from a clean clone without undocumented local state.
- AC11: If the owner authorizes a real first release in this task, the public package, GitHub release, immutable tag, published digests/attestations, CI result, changelog, and canonical install commands all resolve to the same receipt, and an independent clean install verifies the public artifact. If publication is explicitly deferred, TASK-048 cannot be called publicly delivered and must record that limitation in its closeout disposition.

## Open Questions (Answer Needed)

- OQ1. What is the first trusted public distribution target?
  - Option A (recommended): PyPI `project-workflow` through GitHub Actions trusted publishing, with the same artifacts attached to a GitHub Release. The package name currently returns `Not Found` from the PyPI JSON API, but repository ownership/publisher configuration still requires owner action.
  - Option B: GitHub Releases only, with version-pinned `uvx --from git+...@<tag>` commands and artifact digests. This avoids PyPI setup but leaves installation coupled to Git and provides a weaker Python-package distribution experience.
- OQ2. Must TASK-048 include the first real public release?
  - Option A (recommended): Yes. Build and validate the machinery, then pause at the explicit external-publication gate for owner authorization and prove the contract with one real release.
  - Option B: Deliver only a dry-run/staged release workflow. This proves mechanics but not the public trusted-distribution outcome, so closeout must remain limited rather than claiming live delivery.
- OQ3. What version should inaugurate the contract?
  - Option A (recommended): `0.2.0`, reflecting the substantial new backlog, Fix, Epic control, upgrade, and Smoke Bomb capabilities accumulated since the declared `0.1.1` state.
  - Option B: `0.1.2`, treating the release machinery as a patch-level continuation despite the larger unreleased product change set.

## Decisions (Resolved)

- Keep this as one Task: it delivers one release/distribution outcome, even though validation, packaging, publication, documentation, and live proof are coordinated parts of that outcome.
- Use GitHub `main` as the reviewed source branch and bind every release to a full commit SHA; a human-readable tag alone is not sufficient identity.
- Commit `uv.lock` and use it for maintainer, Codex worktree, test, build, and release dependency resolution. Do not expose the lockfile as a downstream runtime constraint.
- Build artifacts once and promote the same bytes. Rebuilding between validation and publication invalidates the candidate.
- Treat package publication as an external action requiring an explicit owner-controlled gate even after the requirements envelope is approved.
- Preserve version command ownership: `init` remains new-repository-only and `upgrade` remains the atomic existing-repository path.
- Treat built package contents, published artifact digests, CI identity, and clean packaged init/upgrade runs as authoritative proof. Source tests alone and prose-only release claims are invalid substitutes.

## Validation Plan

- Add focused unit/fixture coverage for release identity parsing, version/changelog/tag consistency, duplicate/reused release rejection, artifact digest verification, documentation pinning, and lockfile freshness.
- Run the complete repository suite with `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q` and prove the UVX packaging case executed.
- Build wheel and source distribution in a clean locked environment; inspect archives, verify entry points and package data, install the wheel into disposable repositories, and exercise fresh init plus representative upgrade paths.
- Compare canonical CLI source, packaged scaffold template, and checked-in local helper byte-for-byte wherever the existing parity contract requires it.
- Run backlog validation, Doctor, compile/parity checks, and `git diff --check` before review.
- Record the exact GitHub workflow run, source SHA, tag, package files, SHA-256 digests, attestations, release URL, and registry project/version in the release receipt.
- After owner-authorized publication, install from the public canonical command in a clean disposable repository and compare reported package/asset/schema identity with the receipt. A local wheel, TestPyPI package, mutable branch, or source checkout is not a substitute for this final public-artifact claim.
