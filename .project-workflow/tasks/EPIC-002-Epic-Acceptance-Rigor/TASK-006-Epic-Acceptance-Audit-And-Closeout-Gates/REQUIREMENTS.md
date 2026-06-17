# Requirements

## Summary

- Task: TASK-006
- Title: Epic Acceptance Audit And Closeout Gates
- Parent Epic: EPIC-002 | Epic Acceptance Rigor
- Parent AC Coverage: EPIC-002 AC7, AC8, AC9, AC13, AC17
- Last updated: 2026-06-17

## Goal

Add epic-level audit and closeout commands so every parent AC is summarized with mapped child tasks, evidence, verdict, and gap status before an epic can be safely closed.

## Non-Goals

- Full owner-approved deferral modeling; that belongs to TASK-007.
- General task/epic status command expansion; that belongs to TASK-008.
- Final documentation sweep and fixture expansion beyond this command behavior; that belongs to TASK-009.

## Users & Context

- Maintainers need a single epic-level artifact instead of hunting through child task docs.
- Agents need a closeout command that refuses to treat child completion as sufficient.
- Reviewers need child task completion to surface whether parent AC evidence is present.

## Requirements (Outcome-Focused)

- `epic audit` generates or refreshes `ACCEPTANCE-AUDIT.md` inside the epic folder.
- The audit maps every parent AC to child rows, child statuses, evidence summaries, and verdicts.
- `epic closeout` validates the audit and blocks closeout when parent ACs are unmapped, missing evidence, missing pass verdicts, or still pending.
- Closeout does not mark the global epic row `Complete` unless explicitly requested and all gates pass.
- Audit output gives users a single epic-level evidence summary.

## Acceptance Criteria (Verifiable)

- AC1: Covers EPIC-002 AC7 when `epic audit` writes an `ACCEPTANCE-AUDIT.md` table summarizing every parent AC, mapped child rows, evidence, deferral, and verdict.
- AC2: Covers EPIC-002 AC8 when `epic closeout` exits non-zero and lists blocking gaps for unmapped ACs, non-complete children, missing parent AC evidence, or missing pass QA verdicts.
- AC3: Covers EPIC-002 AC9 when `epic closeout` validates by default and only updates the global epic tracker row to `Complete` when `--complete` is explicitly provided and all gates pass.
- AC4: Covers EPIC-002 AC13 when the generated audit summarizes evidence at the epic level instead of relying only on scattered child docs.
- AC5: Covers EPIC-002 AC17 when closeout treats epic-managed child completion without parent AC evidence as blocking.

## Open Questions (Answer Needed)

- None for this task. Structured owner deferrals are deferred to TASK-007.

## Decisions (Resolved)

- Decision: `epic audit` is iterative and `epic closeout` is enforcing.
  - Context: Users need to inspect gaps before final closeout.
  - Chosen: `epic audit` writes the artifact and reports warnings; `epic closeout` blocks on gaps.
  - Why: This supports early visibility without making audit generation cumbersome.

## Validation Plan

- Add fixture tests for passing audit/closeout and failing closeout.
- Verify closeout without `--complete` does not mutate global status.
- Verify closeout with `--complete` only mutates global status when all gates pass.
- Run focused tests and doctor checks.
