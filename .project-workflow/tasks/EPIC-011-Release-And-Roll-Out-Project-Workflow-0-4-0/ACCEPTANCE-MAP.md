# Acceptance Map

- Epic: EPIC-011
- Last updated: 2026-08-20

| Parent AC | Summary | Child Coverage | Evidence State | Deferral State | Status |
| --- | --- | --- | --- | --- | --- |
| AC1 | All current release identity authorities and current-use documentation consistently identify version 0.4.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged. | TASK-065 (Complete) | TASK-065: parent AC evidence recorded; TASK-065: QA pass | None | Satisfied |
| AC2 | The exact release candidate passes the complete locked test suite, strict Doctor with no unaccepted visible issue, release-contract checks, artifact verification, and all supported exact-wheel package journeys. | TASK-066 (In Progress) | None | None | Mapped - evidence pending |
| AC3 | A reviewed pull request is merged to `main`; `v0.4.0` is an annotated tag on that exact merged lineage; the release workflow publishes the expected wheel and source distribution to PyPI and GitHub without rebuilding divergent artifacts. | TASK-067 (In Progress) | None | None | Mapped - evidence pending |
| AC4 | Public verification proves `project-workflow==0.4.0` installs fresh, reports 0.4.0, exposes the Delegate assets/commands, matches recorded hashes, and has verifiable GitHub artifact attestation/provenance. | TASK-068 (In Progress) | None | None | Mapped - evidence pending |
| AC5 | Every project in the current Codex saved-project inventory has a recorded disposition, and every project with a canonical Project Workflow installation is either upgraded from the public 0.4.0 package or retained unchanged with a concrete safety blocker. | TASK-069 (In Progress) | None | None | Mapped - evidence pending |
| AC6 | Every successful consumer upgrade preserves user-owned content, produces only expected managed/schema changes, reports package version 0.4.0, and passes its applicable Doctor/upgrade validation. | TASK-069 (In Progress) | None | None | Mapped - evidence pending |
| AC7 | A retained rollout receipt maps every acceptance criterion to exact commits, release URLs or artifact identities, inventory evidence, per-project validation, and any unresolved adoption boundary. | TASK-069 (In Progress) | None | None | Mapped - evidence pending |

## Notes

- This is a working coverage map derived from requirements, the epic tracker, deferrals, and child task evidence.
- `ACCEPTANCE-AUDIT.md` remains the closeout evidence artifact.
