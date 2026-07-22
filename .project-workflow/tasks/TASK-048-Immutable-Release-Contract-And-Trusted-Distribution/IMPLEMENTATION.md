## User Story

As a project-workflow maintainer or adopter, I want every published release to resolve to one immutable and verifiable source, package, compatibility, evidence, and install identity, so that I can install, upgrade, audit, and correct releases without guessing what mutable repository state produced them.

## Goal

Deliver and prove the first governed `project-workflow` release, version `0.2.0`, through a repeatable GitHub Actions pipeline that publishes one validated artifact set to PyPI and GitHub Releases with traceable source, compatibility, CI, digest, and install identity.

## Approach

- Replace duplicated package versions with one importable source version and mechanically validate tag, changelog, package metadata, runtime identity, and generated manifest consumers against it.
- Commit `uv.lock`; use locked Python 3.10 environments locally and in CI while keeping consumer dependencies unconstrained by the maintainer lock.
- Add a repository-owned release-contract tool that validates candidates, inspects built artifacts, emits the machine-readable receipt and digest file, and rejects reused or contradictory identities.
- Add ordinary CI for pull requests and `main`, plus a tag-triggered release workflow that validates and builds once, attests the exact distributions, publishes those bytes through PyPI OIDC, and attaches the same files and receipt to a GitHub Release.
- Configure the external GitHub/PyPI authority only after the reviewed workflow identity exists. Use the `pypi` GitHub environment as the explicit publication boundary.
- Prove the final public artifact independently with version-pinned `uvx` init and upgrade journeys, then record structured external-contract, deployed-artifact, and runtime-source evidence before QA.

## Phases

1. Release identity and reproducible development foundation.
2. Candidate validation, receipt generation, and negative regression coverage.
3. CI, trusted publication, attestations, and release documentation.
4. External authority configuration and first live `0.2.0` publication.
5. Independent public verification, QA/code review, completion, and retro.

## Acceptance Criteria

- [ ] AC1: A validated release command or workflow emits the complete machine-readable release receipt and rejects missing or mismatched identity.
- [ ] AC2: One authoritative package version agrees with package metadata, runtime identity, manifests, tag, and changelog.
- [ ] AC3: Publication is gated by the full locked repository validation on the reviewed `main` commit with UVX enabled.
- [ ] AC4: One wheel and one source distribution are built, inspected, digested, and promoted without rebuilding.
- [ ] AC5: PyPI publication uses short-lived GitHub OIDC through an owner-controlled environment and no long-lived publishing secret.
- [ ] AC6: Existing versions, reused or moved tags, dirty release state, and digest mismatch fail closed.
- [ ] AC7: Canonical init and upgrade documentation uses the immutable released package version and rejects mutable Git source as release guidance.
- [ ] AC8: Clean disposable repositories prove packaged init, upgrade, version, manifest, managed assets, and Doctor behavior against the same receipt.
- [ ] AC9: `uv.lock`, Codex setup, and CI provide a clean locked Python 3.10 environment and detect lock drift.
- [ ] AC10: The release runbook defines states, authority, recovery, and evidence without undocumented local state.
- [ ] AC11: Public PyPI and GitHub `0.2.0` artifacts, tag, receipt, digests, CI, changelog, commands, and independent install proof resolve to one identity.

## Validation

- AC1-AC2, AC6-AC7: Focused release-contract unit and CLI tests, including negative identity and mutable-command fixtures.
- AC3, AC9: Locked CI and local `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`; assert the UVX case executes and `uv lock --check` passes.
- AC4: Build wheel and source distribution once, inspect archives and metadata, compute SHA-256 digests, and verify the receipt against unchanged files.
- AC5: Inspect GitHub workflow permissions/environment and PyPI trusted-publisher identity; verify the successful OIDC publish run contains no repository publication secret.
- AC8: Install the built and then public package in clean disposable repositories; run init, representative upgrade, version/manifest checks, parity checks, and Doctor.
- AC10: Execute the documented maintainer sequence from a clean clone/candidate with no unstated local files.
- AC11: Verify PyPI JSON/files, GitHub tag/release assets, GitHub attestation, workflow run, receipt, digests, and version-pinned public `uvx` commands against the same commit.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Establish authoritative version and locked environment | Introduce the single `0.2.0` version source, commit `uv.lock`, update Codex setup to locked sync, remove stale generated packaging metadata, and add lock/version consistency checks. | AC2, AC9: package/runtime/manifest version agrees and clean Python 3.10 setup plus lock check passes. | Create a clean worktree, let Codex setup run, execute the Test action, and confirm `git status` stays clean. | Done |
| 2 | Build release-contract tooling and regressions | Add candidate validation, artifact inspection, SHA-256 generation, release receipt creation/verification, immutable tag/version rules, documentation pin checks, and focused negative tests. | AC1, AC2, AC6, AC7: valid candidates emit a complete deterministic receipt; contradictory or reused identities fail closed. | Run focused tests and invoke the tool against valid and deliberately invalid fixtures. | Done |
| 3 | Add locked CI and one-build release workflow | Add pull-request/main CI and a `v*` tag workflow that validates reviewed main ancestry, builds once, uploads/attests artifacts, publishes via PyPI OIDC, and creates the GitHub Release from the same bytes. | AC3, AC4, AC5, AC6: required checks gate publication; artifact digests remain stable across jobs; only OIDC publication is permitted. | Inspect workflow permissions and a successful candidate/release run; compare downloaded workflow, PyPI, and GitHub files by SHA-256. | Done |
| 4 | Prove packaged init and upgrade journeys | Add disposable-repository verification for wheel/staged/public installs, current version and manifest identity, fresh init, representative legacy/current upgrade, asset parity, and Doctor. | AC4, AC8: the exact built artifact satisfies the packaged user journeys and identity checks. | Run the verifier first against `dist/`, then against `project-workflow==0.2.0` after publication. | Done |
| 5 | Publish release documentation and changelog contract | Create the release runbook; cut the `0.2.0` changelog entry; replace canonical mutable installs with version-pinned commands; document states, authority, receipts, abort, and forward-fix behavior. | AC7, AC10: documentation is pinned, executable from a clean clone, and explicit about candidate versus public release state. | Follow the runbook through validation and confirm automated documentation checks reject unpinned canonical commands. | Done |
| 6 | Configure trusted external authorities | Create/protect the GitHub `pypi` environment and register the matching pending PyPI trusted publisher for repository `johndetlefs/project-workflow` and workflow `release.yml`, without adding a publication secret. | AC5, AC10: GitHub and PyPI identities match the workflow and retain an owner-controlled approval boundary. | Inspect GitHub environment settings and PyPI publisher configuration before triggering the release. | In Progress |
| 7 | Publish and independently verify `0.2.0` | Merge the reviewed change, create the immutable `v0.2.0` tag, approve the governed publish, verify public PyPI/GitHub artifacts and attestation, and run clean public init/upgrade proof. Proof recipes: external-contract-alignment, deployed-artifact-alignment, runtime-target-source. Evidence: release receipt, digests, workflow/attestation URLs, registry files, clean journey logs, and task-local `EVIDENCE.json`. | AC5, AC8, AC11: every public identity and exact target/source proof resolves to one release receipt. | Install via the canonical public commands in disposable repositories and independently compare reported identities and downloaded hashes. | To Do |
| 8 | Run QA, closeout, and retro | Review code, workflows, permissions, tests, docs, live evidence, and residual risk by AC; complete only after the public proof passes, then record durable release lessons. | AC1-AC11: no blocking findings, complete evidence mapping, clean Doctor, and explicit completed public outcome. | Review the QA matrix, live release links, and retro updates. | To Do |

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-048
- Title: Immutable Release Contract And Trusted Distribution
- Created: 2026-07-22
