# Decomposition Plan

## Summary

- Epic: EPIC-013
- Status: Approved by parent requirements envelope
- Authority source: Parent REQUIREMENTS.md Owner Approval
- Source requirements identity: sha256:aee5409ecaa9091873e64af3e1ce53a97ff9fea714c2070a6f49c772953c0569
- Last updated: 2026-08-20

## Authorized Child Rows

| ID | Title | Parent ACs | Source | Dependencies | Execution Needs |
|---|---|---|---|---|---|
| TASK-073 | All current release identity authorities and current-use documentation consistently identify version 0.5.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged | AC1 | Generated from REQUIREMENTS.md |  | bounded-return |
| TASK-074 | The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys | AC2 | Generated from REQUIREMENTS.md |  | bounded-return |
| TASK-075 | The reviewed feature lineage is integrated into `main`; `v0.5.0` is an annotated tag on that exact main lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without divergent rebuilds | AC3 | Generated from REQUIREMENTS.md |  | bounded-return |
| TASK-076 | Public verification proves `project-workflow==0.5.0` installs fresh, reports 0.5.0, exposes the capability-aware Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance | AC4 | Generated from REQUIREMENTS.md |  | bounded-return |
| TASK-077 | Every project in the current Codex saved-project inventory has a recorded disposition, and every project with a canonical Project Workflow installation is either upgraded from public 0.5.0 or retained unchanged with a concrete safety blocker | AC5 | Generated from REQUIREMENTS.md |  | bounded-return |

## Authority Rules

- Matching rows inside this plan may be approved and scaffolded without separate per-row owner approval.
- Rows outside this plan require an approved amendment before gated lifecycle movement.
- Matching is by ID, title, and parent AC coverage.
