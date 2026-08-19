# Decomposition Plan

## Summary

- Epic: EPIC-011
- Status: Approved by parent requirements envelope
- Authority source: Parent REQUIREMENTS.md Owner Approval
- Source requirements identity: sha256:8309fded4e2ea9244129910abdc4e8628c541dac9368408155cb88516af02f23
- Last updated: 2026-08-20

## Authorized Child Rows

| ID | Title | Parent ACs | Source | Dependencies |
|---|---|---|---|---|
| TASK-065 | All current release identity authorities and current-use documentation consistently identify version 0.4.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged | AC1 | Generated from REQUIREMENTS.md |  |
| TASK-066 | The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys | AC2 | Generated from REQUIREMENTS.md |  |
| TASK-067 | A reviewed pull request is merged to `main`; `v0.4.0` is an annotated tag on that exact merged lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without rebuilding divergent artifacts | AC3 | Generated from REQUIREMENTS.md |  |
| TASK-068 | Public verification proves `project-workflow==0.4.0` installs fresh, reports 0.4.0, exposes the Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance | AC4 | Generated from REQUIREMENTS.md |  |

## Authority Rules

- Matching rows inside this plan may be approved and scaffolded without separate per-row owner approval.
- Rows outside this plan require an approved amendment before gated lifecycle movement.
- Matching is by ID, title, and parent AC coverage.
