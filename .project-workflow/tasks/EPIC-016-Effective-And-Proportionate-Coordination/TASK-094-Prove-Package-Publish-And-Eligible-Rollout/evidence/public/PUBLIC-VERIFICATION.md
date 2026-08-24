# Project Workflow 0.7.0 Public Verification

- Reviewed integration: PR #21, feature head `0335e4559088bfa3c8afacfa8c04e21b1fe245a6`,
  merge commit `ce255f4c8533ccedc39939f5369f67bcf294face`.
- Release identity: annotated tag `v0.7.0` peels to the merge commit; release workflow run
  `32696346077` completed all build, attestation, PyPI and GitHub Release jobs successfully.
- Trusted release bundle: the workflow ran the complete locked suite, built once at the tag, checked
  the receipt, exercised the exact built wheel, attested the release files, and passed the same
  downloaded bundle to PyPI and GitHub Release.
- Wheel SHA-256: `20f259cb8bf58f61c3c72d5cdabfc4c9a96b1ef803b61379ebcbd99629115c26`.
- Source distribution SHA-256:
  `82d0e3ba666881f92e4276ffa1077265ed68d1374f87f0ffb148575f24ed1fe6`.
- Public retrieval: PyPI and GitHub Release downloads are byte-identical for both distributions and
  match `release-receipt.json` and `SHA256SUMS`.
- Provenance: GitHub CLI cryptographically verified both public downloads against GitHub's
  downloaded Sigstore trusted root. The SLSA statement binds the subjects to release workflow
  `.github/workflows/release.yml`, tag `v0.7.0`, and source commit
  `ce255f4c8533ccedc39939f5369f67bcf294face`.
- Fresh public journey: `uvx --from project-workflow==0.7.0 project --version` reported `project
  0.7.0`; a disposable fresh Codex repository installed asset version 6, created canonical
  Coordinator and Delegate compatibility assets, initialized contract version 2 coordination, and
  passed Doctor with no issues.
- Proof boundary: the earlier local candidate artifacts are rehearsal evidence and have different
  archive bytes. The production identity is the trusted bundle built once and validated at the exact
  reviewed tag, then published unchanged to both public channels. No consumer repository was
  installed or upgraded.

Public locations:

- GitHub Release: <https://github.com/johndetlefs/project-workflow/releases/tag/v0.7.0>
- PyPI: <https://pypi.org/project/project-workflow/0.7.0/>
- Release workflow: <https://github.com/johndetlefs/project-workflow/actions/runs/32696346077>
