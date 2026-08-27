# Acceptance Map

- Epic: EPIC-017
- Last updated: 2026-08-27

| Parent AC | Summary | Child Coverage | Evidence State | Deferral State | Status |
| --- | --- | --- | --- | --- | --- |
| AC1 | Current 0.7.0 Coordinator/lifecycle/QA authority remains singular; no second mutable | TASK-095 (Complete) | TASK-095: parent AC evidence recorded; TASK-095: QA pass | None | Satisfied |
| AC10 | Exactly one independent QA verdict is retained. QA cannot broaden an expensive campaign; | TASK-096 (Complete), TASK-098 (Complete) | TASK-096: parent AC evidence recorded; TASK-096: QA pass; TASK-098: parent AC evidence recorded; TASK-098: QA pass | None | Satisfied |
| AC11 | Generated/project-local host assets and packaged source remain byte/behavior aligned, and | TASK-096 (Complete), TASK-098 (Complete) | TASK-096: parent AC evidence recorded; TASK-096: QA pass; TASK-098: parent AC evidence recorded; TASK-098: QA pass | None | Satisfied |
| AC12 | Sanitized behavioural and deterministic coverage exercises every R12 failure and | TASK-098 (Complete) | TASK-098: parent AC evidence recorded; TASK-098: QA pass | None | Satisfied |
| AC13 | A disposable fake-verifier journey proves invocation counts: zero full calls after canary | TASK-098 (Complete) | TASK-098: parent AC evidence recorded; TASK-098: QA pass | None | Satisfied |
| AC14 | The Strategic Advisor runner supports case/metadata selection, previously failing/affected | TASK-097 (Complete) | TASK-097: parent AC evidence recorded; TASK-097: QA pass | None | Satisfied |
| AC15 | The sanitized reference-consumer dogfood follows the AC4/AC5/AC8/AC10/AC13 sequence and | TASK-098 (Complete) | TASK-098: parent AC evidence recorded; TASK-098: QA pass | None | Satisfied |
| AC2 | A valid compact campaign records exact candidate, mode, claims, ordered stages, affected | TASK-095 (Complete) | TASK-095: parent AC evidence recorded; TASK-095: QA pass | None | Satisfied |
| AC3 | Status deterministically reports exactly one of `implementation-required`, | TASK-095 (Complete) | TASK-095: parent AC evidence recorded; TASK-095: QA pass | None | Satisfied |
| AC4 | A fixture with incomplete implementation and a release request reports | TASK-095 (Complete), TASK-098 (Complete) | TASK-095: parent AC evidence recorded; TASK-095: QA pass; TASK-098: parent AC evidence recorded; TASK-098: QA pass | None | Satisfied |
| AC5 | A blocking deterministic or canary result prevents affected/full certification. In | TASK-096 (Complete), TASK-098 (Complete) | TASK-096: parent AC evidence recorded; TASK-096: QA pass; TASK-098: parent AC evidence recorded; TASK-098: QA pass | None | Satisfied |
| AC6 | Diagnostic continuation is rejected unless it names the decision enabled, selected scope, | TASK-096 (Complete) | TASK-096: parent AC evidence recorded; TASK-096: QA pass | None | Satisfied |
| AC7 | Limits pause/block rather than pass. Required proof remains visibly missing, and resumption | TASK-096 (Complete) | TASK-096: parent AC evidence recorded; TASK-096: QA pass | None | Satisfied |
| AC8 | Receipt currentness is input-specific: product changes invalidate affected target proof; | TASK-096 (Complete), TASK-098 (Complete) | TASK-096: parent AC evidence recorded; TASK-096: QA pass; TASK-098: parent AC evidence recorded; TASK-098: QA pass | None | Satisfied |
| AC9 | The generic adapter schema and tests contain no Strategic Advisor identifier, repository | TASK-095 (Complete), TASK-097 (Complete) | TASK-095: parent AC evidence recorded; TASK-095: QA pass; TASK-097: parent AC evidence recorded; TASK-097: QA pass | None | Satisfied |

## Notes

- This is a working coverage map derived from requirements, the epic tracker, deferrals, and child task evidence.
- `ACCEPTANCE-AUDIT.md` remains the closeout evidence artifact.
