# Acceptance Audit

- Epic: EPIC-013
- Last updated: 2026-08-20

| Parent AC | Summary | Child Rows | Evidence | Deferral | Verdict |
| --- | --- | --- | --- | --- | --- |
| AC1 | All current release identity authorities and current-use documentation consistently identify version 0.5.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged. | TASK-073 (Complete) | TASK-073: parent AC evidence recorded; TASK-073: QA pass | None | Pass |
| AC2 | The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys. | TASK-074 (Complete) | TASK-074: parent AC evidence recorded; TASK-074: QA pass | None | Pass |
| AC3 | The reviewed feature lineage is integrated into `main`; `v0.5.0` is an annotated tag on that exact main lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without divergent rebuilds. | TASK-075 (Complete) | TASK-075: parent AC evidence recorded; TASK-075: QA pass | None | Pass |
| AC4 | Public verification proves `project-workflow==0.5.0` installs fresh, reports 0.5.0, exposes the capability-aware Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance. | TASK-076 (Complete) | TASK-076: parent AC evidence recorded; TASK-076: QA pass | None | Pass |
| AC5 | Every project in the current Codex saved-project inventory has a recorded disposition, and every project with a canonical Project Workflow installation is either upgraded from public 0.5.0 or retained unchanged with a concrete safety blocker. | TASK-077 (Complete) | TASK-077: parent AC evidence recorded; TASK-077: QA pass | None | Pass |
| AC6 | Every successful consumer upgrade preserves user-owned content, produces only expected managed/schema changes, reports package version 0.5.0, and passes its applicable Doctor/upgrade validation. | TASK-078 (Complete) | TASK-078: parent AC evidence recorded; TASK-078: QA pass | None | Pass |
| AC7 | A retained rollout receipt maps every acceptance criterion to exact commits, release URLs or artifact identities, inventory evidence, per-project validation, and any unresolved adoption boundary. | TASK-079 (Complete) | TASK-079: parent AC evidence recorded; TASK-079: QA pass | None | Pass |
