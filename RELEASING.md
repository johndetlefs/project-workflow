# Releasing project-workflow

This runbook governs public releases. The current release is `0.2.0`; all commands and identities
below are intentionally immutable.

## Authority and release states

- The source version in `src/project_workflow/_version.py` is the editable authority. Package
  metadata reads it dynamically. Dependency-free generated workflow helpers mirror it and are
  checked byte-for-byte.
- A **candidate** is a reviewed `main` commit for which locked tests, source-contract checks,
  artifact inspection, and disposable package journeys pass. It is not public.
- A **published release** exists only after the tag workflow publishes through the protected
  GitHub `pypi` environment, PyPI accepts the exact wheel and sdist via OIDC, and GitHub Releases
  exposes those same bytes with the receipt and digests.
- The repository owner controls branch review, immutable tag creation, the GitHub environment,
  and the matching PyPI trusted-publisher registration. No PyPI API token belongs in GitHub.

## Candidate validation

From a clean clone of the reviewed commit, with Homebrew available on macOS:

```bash
export PATH="/opt/homebrew/bin:$PATH"
uv sync --locked --extra dev --python 3.10
uv lock --check
uv run --locked pytest -q
python scripts/release_contract.py check-source --version 0.2.0 --tag v0.2.0 --clean
uv run --locked python -m build --no-isolation
```

The release workflow repeats the full locked validation and builds exactly once. It then inspects
the archives, creates `release-receipt.json` and `SHA256SUMS`, runs the wheel through fresh-init,
current-upgrade, and legacy-upgrade journeys, attests the files, and uploads one workflow bundle.
Inspect workflow annotations as part of closeout. Treat action-runtime deprecation warnings as
future-pipeline maintenance: update to the current reviewed SHA pin and revalidate the workflow,
but never move or rebuild an already published tag to silence a later tooling warning.

## One-time trusted-publisher setup

1. In GitHub, create an environment named `pypi`. Keep deployment authority owner-controlled;
   configure a required reviewer where the repository plan supports it.
2. In PyPI, create a pending trusted publisher for project name `project-workflow`, owner
   `johndetlefs`, repository `project-workflow`, workflow `release.yml`, and environment `pypi`.
3. Do not create a PyPI API token or repository publication secret.

The exact repository, workflow, and environment values are part of the OIDC identity. A mismatch
fails publication rather than falling back to another credential.

## Publish

After the candidate is merged and its required `main` CI run passes:

```bash
git tag --annotate v0.2.0 --message "project-workflow 0.2.0"
git push origin v0.2.0
```

The workflow rejects any other tag identity, commits outside `main`, dirty source state, lock
drift, failed tests, archive mismatch, or digest change. Approve the `pypi` environment deployment
only after its build and attestation job passes.

## Independent public verification

Download the GitHub Release bundle and the PyPI files independently. Verify `SHA256SUMS`, then
compare filenames, sizes, and SHA-256 values with `release-receipt.json`. Run:

```bash
uvx --from project-workflow==0.2.0 project --version
python scripts/verify_package_journeys.py --from project-workflow==0.2.0 --version 0.2.0
gh attestation verify project_workflow-0.2.0-py3-none-any.whl --repo johndetlefs/project-workflow
```

Record the public PyPI page, GitHub Release, tag commit, successful workflow run, attestation,
receipt, digests, and disposable journey output in the task-local evidence file.

## Abort and recovery

- Before a tag is pushed, fix the candidate normally and rerun CI.
- If the tag workflow fails before either registry accepts an artifact, delete the failed remote
  tag only after confirming no public artifact or release exists; correct the source and create a
  new tag from the corrected reviewed commit.
- Never move or reuse a public tag or version. PyPI files are immutable and versions cannot be
  overwritten. If PyPI accepts `0.2.0` but a later step fails, preserve `v0.2.0`, repair the GitHub
  Release from the retained workflow bundle when identity is unchanged, or make the next source
  correction as `0.2.1`.
- A yanked PyPI release remains part of history; yanking is an owner decision for harmful releases,
  not a mechanism for replacing files.
