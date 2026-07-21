# Requirements

## Summary

- Task: TASK-026
- Title: Collision-Resistant ID Generation
- Last updated: 2026-06-25

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: No
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-21
- Approval note / source: Owner message on 2026-07-21: both 26 and 27 are verified as working; complete and push through to main.
- Approved artifact identity: sha256:5b96a88af043cce02a774ad2847969356410b3277fd92ef19c783d588be06a7f

## Goal

Allow team repos to opt into branch-friendly workflow IDs so parallel task, epic,
and backlog creation does not routinely collide during merges.

## Non-Goals

- Do not migrate or rewrite existing numeric IDs.
- Do not add a centralized ID allocation service.
- Do not change the default behavior for existing repos.
- Do not replace tracker order, priority, or status with ID ordering.

## Users & Context

- Maintainers and agents use project-workflow in local Git branches.
- Individual developers benefit from sequential IDs, but teams can create the same
  next numeric ID independently on different branches.
- Workflow IDs are load-bearing because they appear in tracker rows, task folders,
  branch names, backlog promotion references, requirements, implementation docs,
  and epic child rows.

## Requirements (Outcome-Focused)

- Existing repos keep sequential IDs unless configuration opts into unique IDs.
- Repos can configure ID generation separately for tasks, epics, and backlog rows.
- Unique task IDs keep the configured prefix and use a short uppercase base36
  suffix such as `WF-K7F3Q`.
- Unique epic IDs use the existing `EPIC` prefix and the same short suffix.
- Unique backlog IDs use the existing `BL` prefix and the same short suffix.
- Unique ID generation checks existing local workflow state and regenerates if a
  candidate is already used.
- Validation accepts both legacy numeric IDs and configured unique IDs where
  workflow references are valid.

## Acceptance Criteria (Verifiable)

- AC1: With no ID generation config, task, epic, and backlog creation continue to
  use existing sequential IDs.
- AC2: With `id_generation` configured to `unique`, new task, epic, and backlog
  IDs use a 5-character uppercase base36 suffix and keep the appropriate prefix.
- AC3: Unique ID generation scans existing tracker rows, epic trackers, backlog
  rows, and workflow task folders before accepting a candidate.
- AC4: Doctor/backlog validation accepts configured unique promoted references and
  still detects duplicate or malformed workflow IDs.
- AC5: README and generated agent guidance describe the unique ID mode clearly.

## Open Questions (Answer Needed)

- None. Owner accepted 5-character base36 unique IDs with local collision checks.

## Decisions (Resolved)

- Add a repo config option instead of changing the default.
- Use `secrets` for unique ID generation.
- Use uppercase base36 characters `0-9A-Z`.
- Default unique suffix length is 5, with a config override available for larger repos.

## Validation Plan

- Run focused unit tests for sequential compatibility, unique ID generation, collision
  retry behavior, backlog promotion references, and doctor validation.
- Run the full test suite if feasible.
- Run `project doctor` after tracker and task-doc changes.

## Legacy Adoption

- Adopted legacy work: Yes
- Adopted by: John Detlefs
- Adoption date: 2026-07-21
- Adoption source: Owner message on 2026-07-21: both 26 and 27 are verified as working; complete and push through to main.
- Evidence refreshed after adoption: Yes
- Evidence trust note: Existing evidence was refreshed after adoption.
