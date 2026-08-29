# Releasing Project Workflow

This runbook governs public releases. It is version-neutral: the editable version authority is
`src/project_workflow/_version.py`, and every candidate, tag, workflow pin, artifact, receipt, and
public verification must resolve to that same version.

## Release States And Authority

- A local build is a build, not a release candidate.
- A candidate is a reviewed commit on `main` whose locked checks, source contract, distribution
  inspection, and disposable package journeys pass against one source identity.
- A published release exists only after the protected tag workflow publishes the exact wheel and
  sdist through the GitHub `pypi` environment and exposes the same files and receipts on GitHub.
- The repository owner controls merge, tag creation, environment approval, and the matching PyPI
  trusted-publisher registration. No PyPI API token belongs in GitHub.

## Prepare The Versioned Source

Choose the intended semantic version as `X.Y.Z`, then update and review all version-owned surfaces:

1. `src/project_workflow/_version.py`.
2. `CURRENT_PACKAGE_VERSION` in `src/project_workflow/contracts.py`, followed by runtime generation.
3. `.project-workflow/manifest.json` and the new `CHANGELOG.md` heading.
4. Exact-version installation examples and the tag/version pins in `.github/workflows/ci.yml` and
   `.github/workflows/release.yml`.
5. Any version-specific compatibility baseline explicitly changed by the release.

The release source contract fails when these identities disagree.

## Validate One Candidate

From a clean worktree at the reviewed commit, set `VERSION` and `TAG` to the intended values:

```bash
export PATH="/opt/homebrew/bin:$PATH"
export VERSION="X.Y.Z"
export TAG="v$VERSION"
uv sync --locked --extra dev --python 3.10
uv lock --check
uv run --locked ruff check src/project_workflow/*.py scripts tests
uv run --locked ruff format --check src/project_workflow/*.py scripts tests
uv run --locked mypy src/project_workflow/*.py
uv run --locked pytest -q
uv run --locked python scripts/build_runtime_bundle.py --check
uv run --locked python scripts/release_contract.py check-source \
  --version "$VERSION" --tag "$TAG" --clean
uv run --locked python -m build --no-isolation
```

Build exactly once. Inspect that wheel and sdist, create the release receipt and `SHA256SUMS`, then
exercise the exact wheel through fresh-init, current-upgrade, legacy-upgrade, no-op, Doctor, and
representative lifecycle journeys. Do not rebuild between review, attestation, and publication.

## Trusted Publisher Setup

One time only:

1. Create a protected GitHub environment named `pypi`.
2. In PyPI, register the `project-workflow` trusted publisher for owner `johndetlefs`, repository
   `project-workflow`, workflow `release.yml`, and environment `pypi`.
3. Keep the repository, workflow, environment, and OIDC subject exact. A mismatch must fail closed.

## Publish

After the candidate is merged and its required `main` CI run passes:

```bash
git tag --annotate "$TAG" --message "project-workflow $VERSION"
git push origin "$TAG"
```

The release workflow requires a new immutable tag on reviewed `main` history, a clean source
contract, a locked environment, passing static/tests/package journeys, and public version
availability. Approve the protected `pypi` deployment only after the build, inspection, and
attestation job passes.

## Verify The Public Release Independently

Download the GitHub Release bundle and PyPI distributions independently. Compare filenames, sizes,
SHA-256 values, the release receipt, and `SHA256SUMS`, then run:

```bash
uvx --from "project-workflow==$VERSION" project --version
python scripts/verify_package_journeys.py \
  --from "project-workflow==$VERSION" --version "$VERSION"
gh attestation verify "project_workflow-$VERSION-py3-none-any.whl" \
  --repo johndetlefs/project-workflow
```

Record the PyPI page, GitHub Release, tag commit, workflow run, attestation, receipt, digests, and
journey output in the release work item's evidence.

## Abort And Recovery

- Before pushing a tag, fix the candidate normally and rerun the entire candidate path.
- If the tag workflow fails before any registry accepts an artifact, first prove no public artifact
  or release exists. Only then may the owner delete the failed remote tag and create a corrected one.
- Never move or reuse a public tag or version. If publication partially succeeds, retain the public
  identity, repair only from the retained exact bundle where valid, or issue a new version.
- Yanking is an owner decision for a harmful release, not a way to overwrite files.

Release, publication, rollout, adoption, and owner acceptance remain distinct proof gates.
