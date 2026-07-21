# Acceptance Map

- Epic: EPIC-007
- Last updated: 2026-07-21

| Parent AC | Summary | Child Coverage | Evidence State | Deferral State | Status |
| --- | --- | --- | --- | --- | --- |
| AC1 | A managed repository metadata artifact records package, asset, and repository-schema versions plus applied migration IDs; recognized pre-versioned repositories receive a deterministic legacy classification rather than being treated as current. | TASK-040 (Complete), TASK-044 (Approved), TASK-045 (Proposed) | None | None | Mapped - evidence pending |
| AC2 | Doctor can emit stable machine-readable findings containing a code, severity, affected artifact, remediation ownership, and mechanical-upgrade eligibility, while preserving concise human-readable output. | TASK-041 (Complete), TASK-046 (Proposed) | None | None | Mapped - evidence pending |
| AC3 | Running `project upgrade` against each supported historical fixture produces an ordered, machine-readable and human-readable plan with current/target versions, migration IDs, exact target files, preconditions, blockers, and owner decisions, and causes no repository file changes. | TASK-042 (Complete), TASK-045 (Proposed), TASK-046 (Proposed) | None | None | Mapped - evidence pending |
| AC4 | `project upgrade --apply` applies exactly the validated mechanical plan only when worktree, version, and input-hash preconditions still match; dirty, stale, unsupported, or unrecognized state is rejected without mutation. | TASK-042 (Complete), TASK-043 (Complete) | None | None | Mapped - evidence pending |
| AC5 | Canonical `project init` refreshes managed assets, reports detected asset/schema state, and directs behind repositories to `project upgrade` without claiming that user-owned repository state was migrated. | TASK-040 (Complete), TASK-041 (Complete), TASK-044 (Approved), TASK-046 (Proposed) | None | None | Mapped - evidence pending |
| AC6 | Migration application is atomic and idempotent: injected failure leaves no partial file changes, successful apply matches the predicted diff, and a second apply at the target version is a no-op. | TASK-043 (Complete), TASK-045 (Proposed) | None | None | Mapped - evidence pending |
| AC7 | Upgrade fixtures prove that existing tracker rows, task/Epic docs, backlog rows, guidance, config values, approvals, deferrals, evidence, and unmarked content are preserved unless an explicit versioned migration owns the changed field. | TASK-040 (Complete), TASK-043 (Complete), TASK-045 (Proposed) | None | None | Mapped - evidence pending |
| AC8 | Missing approvals, stale evidence, accepted warnings, and unresolved product decisions remain visible as named owner-owned follow-up and are never automatically converted into passing evidence or authority. | TASK-041 (Complete), TASK-042 (Complete), TASK-043 (Complete), TASK-045 (Proposed) | None | None | Mapped - evidence pending |
| AC9 | Targeted historical-fixture, stale-plan, dirty-worktree, unsupported-version, atomic-failure, preservation, idempotency, init-integration, doctor-output, and generated-helper parity tests pass together with the full project-workflow suite and strict doctor validation. | TASK-045 (Proposed), TASK-046 (Proposed) | None | None | Mapped - evidence pending |

## Notes

- This is a working coverage map derived from requirements, the epic tracker, deferrals, and child task evidence.
- `ACCEPTANCE-AUDIT.md` remains the closeout evidence artifact.
