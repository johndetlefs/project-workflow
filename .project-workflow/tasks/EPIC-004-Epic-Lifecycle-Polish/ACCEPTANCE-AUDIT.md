# Acceptance Audit

- Epic: EPIC-004
- Last updated: 2026-06-17

| Parent AC | Summary | Child Rows | Evidence | Deferral | Verdict |
| --- | --- | --- | --- | --- | --- |
| AC1 | New epics start with an `ACCEPTANCE-MAP.md` or equivalent maintained acceptance-map artifact that lists parent AC IDs, summaries, child coverage, evidence state, deferral state, and current status; generated templates/docs/tests prove the artifact exists from epic start. | TASK-015 (Complete) | TASK-015: parent AC evidence recorded; TASK-015: QA pass | None | Pass |
| AC2 | `epic closeout` prints a concise human/agent-friendly summary covering total parent ACs, pass/fail/deferred counts, missing mappings, missing evidence, missing QA, deferrals, follow-ups, and next actions, while still writing the detailed audit file. | TASK-016 (Complete) | TASK-016: parent AC evidence recorded; TASK-016: QA pass | None | Pass |
| AC3 | Epic closeout blocks completion unless a lightweight epic retro is recorded, with sections for lessons, follow-up tasks, deferrals, missed in-scope work, and a permitted explicit "none" entry; generated guidance and tests cover the required retro behavior. | TASK-017 (Complete) | TASK-017: parent AC evidence recorded; TASK-017: QA pass | None | Pass |
| AC4 | A minimal epic status lifecycle exists for global epic rows where useful, with CLI-supported transitions or validation for `Analysing`, `Ready`, `In Progress`, `Closeout`, and `Complete`; transitions must not bypass readiness, audit, retro, or closeout gates. | TASK-018 (Complete) | TASK-018: parent AC evidence recorded; TASK-018: QA pass | None | Pass |
| AC5 | Doctor or validation output separates legacy/historical warnings from current actionable issues, with tests proving old APP/EPIC-002-style artifacts remain visible but do not obscure EPIC-003-or-newer gate failures. | TASK-019 (Complete) | TASK-019: parent AC evidence recorded; TASK-019: QA pass | None | Pass |
