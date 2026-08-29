# Acceptance Map

- Epic: EPIC-020
- Last updated: 2026-08-29

| Parent AC | Summary | Child Coverage | Evidence State | Deferral State | Status |
| --- | --- | --- | --- | --- | --- |
| AC1 | Every current release identity surface consistently names 0.9.1, generated mirrors are | TASK-109 (Complete) | TASK-109: parent AC evidence recorded; TASK-109: QA pass | None | Satisfied |
| AC2 | One exact candidate commit, wheel, and sdist pass locked Ruff/format/mypy, documentation and | TASK-109 (Complete) | TASK-109: parent AC evidence recorded; TASK-109: QA pass | None | Satisfied |
| AC3 | A reviewed PR with required checks merges the candidate into current `main`; annotated tag | TASK-110 (In Progress) | None | None | Mapped - evidence pending |
| AC4 | Independent public retrieval proves PyPI and GitHub artifacts, hashes, attestations, version | TASK-111 (In Progress) | None | None | Mapped - evidence pending |
| AC5 | Every current project inventory entry has a disposition, and every canonical Project | TASK-112 (In Progress) | None | None | Mapped - evidence pending |
| AC6 | Every successful consumer upgrade used a reviewed fingerprint, preserved owner content, | TASK-112 (In Progress) | None | None | Mapped - evidence pending |
| AC7 | One retained release/rollout receipt maps AC1-AC6 to exact source, PR/checks, tag, workflow, | TASK-112 (In Progress) | None | None | Mapped - evidence pending |

## Notes

- This is a working coverage map derived from requirements, the epic tracker, deferrals, and child task evidence.
- `ACCEPTANCE-AUDIT.md` remains the closeout evidence artifact.
