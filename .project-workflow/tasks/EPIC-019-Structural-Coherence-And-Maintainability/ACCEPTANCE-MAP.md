# Acceptance Map

- Epic: EPIC-019
- Last updated: 2026-08-29

| Parent AC | Summary | Child Coverage | Evidence State | Deferral State | Status |
| --- | --- | --- | --- | --- | --- |
| AC1 | A checked-in architecture document names each canonical production module, its | TASK-104 (Complete) | TASK-104: parent AC evidence recorded; TASK-104: QA pass | None | Satisfied |
| AC10 | The complete locked test suite passes with no reduction from the 548-test released baseline, | TASK-105 (Complete), TASK-106 (Complete), TASK-107 (Complete), TASK-108 (Complete) | TASK-105: parent AC evidence recorded; TASK-105: QA pass; TASK-106: parent AC evidence recorded; TASK-106: QA pass; TASK-107: parent AC evidence recorded; TASK-107: QA pass; TASK-108: parent AC evidence recorded; TASK-108: QA pass | None | Satisfied |
| AC11 | A command-surface snapshot and representative exact-candidate journey compare v0.9.0 with | TASK-104 (Complete), TASK-105 (Complete), TASK-106 (Complete), TASK-107 (Complete), TASK-108 (Complete) | TASK-104: parent AC evidence recorded; TASK-104: QA pass; TASK-105: parent AC evidence recorded; TASK-105: QA pass; TASK-106: parent AC evidence recorded; TASK-106: QA pass; TASK-107: parent AC evidence recorded; TASK-107: QA pass; TASK-108: parent AC evidence recorded; TASK-108: QA pass | None | Satisfied |
| AC12 | The final independent QA review explicitly evaluates whether boundaries are cohesive rather | TASK-108 (Complete) | TASK-108: parent AC evidence recorded; TASK-108: QA pass | None | Satisfied |
| AC13 | Completion records local validated source only. Merge, release, publication, consumer | TASK-108 (Complete) | TASK-108: parent AC evidence recorded; TASK-108: QA pass | None | Satisfied |
| AC2 | `src/project_workflow/cli.py` is a thin entry/compatibility layer below 2,000 lines, no | TASK-104 (Complete), TASK-105 (Complete), TASK-106 (Complete), TASK-107 (Complete) | TASK-104: parent AC evidence recorded; TASK-104: QA pass; TASK-105: parent AC evidence recorded; TASK-105: QA pass; TASK-106: parent AC evidence recorded; TASK-106: QA pass; TASK-107: parent AC evidence recorded; TASK-107: QA pass | None | Satisfied |
| AC3 | The standalone `templates/workflow.py` is deterministically generated from canonical | TASK-104 (Complete), TASK-105 (Complete), TASK-106 (Complete) | TASK-104: parent AC evidence recorded; TASK-104: QA pass; TASK-105: parent AC evidence recorded; TASK-105: QA pass; TASK-106: parent AC evidence recorded; TASK-106: QA pass | None | Satisfied |
| AC4 | The installed repository-local helper works from a disposable initialized repository with | TASK-104 (Complete), TASK-105 (Complete), TASK-106 (Complete) | TASK-104: parent AC evidence recorded; TASK-104: QA pass; TASK-105: parent AC evidence recorded; TASK-105: QA pass; TASK-106: parent AC evidence recorded; TASK-106: QA pass | None | Satisfied |
| AC5 | Shared Codex/Claude adapter mechanisms have one canonical implementation where semantics are | TASK-106 (Complete) | TASK-106: parent AC evidence recorded; TASK-106: QA pass | None | Satisfied |
| AC6 | The 6,085-line catch-all Doctor test is split into product-boundary suites, repeated | TASK-107 (Complete) | TASK-107: parent AC evidence recorded; TASK-107: QA pass | None | Satisfied |
| AC7 | Ruff check, Ruff format check, and mypy pass from the locked development environment and are | TASK-107 (Complete) | TASK-107: parent AC evidence recorded; TASK-107: QA pass | None | Satisfied |
| AC8 | README, contributor architecture/maintenance documentation, `RELEASING.md`, compatibility | TASK-108 (Complete) | TASK-108: parent AC evidence recorded; TASK-108: QA pass | None | Satisfied |
| AC9 | Every repository cleanup candidate has a recorded remove/retain/disposition decision. | TASK-108 (Complete) | TASK-108: parent AC evidence recorded; TASK-108: QA pass | None | Satisfied |

## Notes

- This is a working coverage map derived from requirements, the epic tracker, deferrals, and child task evidence.
- `ACCEPTANCE-AUDIT.md` remains the closeout evidence artifact.
