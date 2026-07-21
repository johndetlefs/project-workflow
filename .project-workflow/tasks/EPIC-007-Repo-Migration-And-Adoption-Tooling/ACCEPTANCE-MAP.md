# Acceptance Map

- Epic: EPIC-007
- Last updated: 2026-07-10

| Parent AC | Summary | Child Coverage | Evidence State | Deferral State | Status |
| --- | --- | --- | --- | --- | --- |
| AC1 | A dry-run command reports stale helper/capability state for repositories whose local helper lacks current commands, without mutating repository files. | None | None | None | Unmapped |
| AC2 | A dry-run command reports workflow debt grouped by severity and type: blockers, current warnings, legacy warnings, accepted warnings, stale generated assets, and safe mechanical fixes. | None | None | None | Unmapped |
| AC3 | The migration plan lists exact next actions and distinguishes automatic fixes from owner-confirmed decisions. | None | None | None | Unmapped |
| AC4 | An apply command can perform low-risk mechanical repairs without overwriting user-owned unmarked content. | None | None | None | Unmapped |
| AC5 | Batch accepted-warning support can add selected warning fingerprints with reasons and leaves changed or unselected warnings visible. | None | None | None | Unmapped |
| AC6 | Sequential ID allocation or backlog write collision risk is addressed by locking, retry validation, or a documented/validated unique-ID migration path. | None | None | None | Unmapped |
| AC7 | Backlog promotion to epic creates `EPIC-CONTRACT.md` and all other current epic-init artifacts, and doctor does not warn about missing current epic artifacts immediately after promotion. | None | None | None | Unmapped |
| AC8 | Migration/adoption tooling preserves existing tracker rows, task docs, epic docs, backlog rows, guidance, and config values unless an explicit generated marker or managed block allows refresh. | None | None | None | Unmapped |
| AC9 | Tests cover dry-run behavior, apply behavior, stale helper detection, missing epic artifact repair, accepted-warning batching, and collision prevention or detection. | None | None | None | Unmapped |

## Notes

- This is a working coverage map derived from requirements, the epic tracker, deferrals, and child task evidence.
- `ACCEPTANCE-AUDIT.md` remains the closeout evidence artifact.
