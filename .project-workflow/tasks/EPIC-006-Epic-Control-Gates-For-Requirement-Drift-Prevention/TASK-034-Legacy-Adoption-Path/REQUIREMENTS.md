# Requirements

## Summary

- Task: TASK-034
- Title: Legacy Adoption Path
- Parent AC Coverage: AC10, AC12
- Last updated: 2026-07-09

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Child Charter

### Inherited Invariants

- Parent AC IDs remain stable.
- Approved child rows must match ID, title, and parent AC coverage in `DECOMPOSITION.md`.
- Missing or placeholder contract sections are not valid authority for new/adopted epics.
- Legacy epics without approval envelopes warn until adoption rather than blocking unrelated current work.

### Invalid Substitutes

- Tracker rows without matching `DECOMPOSITION.md` authority.
- Prose summaries that are not backed by child implementation evidence.
- Legacy warnings from unadopted old epics as proof that new/adopted epics satisfy gates.
- Generic owner approval prompts when the work remains inside the approved authority envelope.

### Artifact Targets

- `.project-workflow/cli/workflow.py`
- `src/project_workflow/cli.py`
- `src/project_workflow/templates/workflow.py`
- `tests/test_doctor.py`
- `README.md`
- `.project-workflow/cli/README.md`
- `src/project_workflow/codex/skills/project-epic/SKILL.md`

### Parent AC Proof Ownership

- AC10: owner `TASK-034`; required evidence: Legacy adoption commands and untrusted inferred evidence handling.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.

## Goal

Add explicit adoption commands for pre-existing tasks and epics so old work can be brought under the new drift gates without silently trusting old evidence or breaking closed legacy history.

## Non-Goals

- Do not automatically rewrite all existing legacy tasks or epics.
- Do not treat pre-adoption evidence as refreshed proof.
- Do not remove existing legacy warning behavior for historical closed work.
- Do not implement a full migration assistant; this child adds safe command paths and gate behavior.

## Users & Context

- Maintainers may have open tasks/epics created before approval envelopes, contracts, decomposition plans, amendments, or structured evidence existed.
- Agents need a supported path for old work instead of hand-editing approval blocks or ignoring warnings.
- Owners need old evidence marked untrusted unless proof is actually refreshed.

## Requirements (Outcome-Focused)

- Add `task adopt` to record owner approval plus a `Legacy Adoption` block for pre-existing standalone tasks.
- Add `epic adopt` to record owner approval plus a `Legacy Adoption` block for pre-existing epics and ensure `AMENDMENTS.md` exists.
- Adoption must record approver, adoption source, adoption date, and whether evidence was refreshed.
- Adoption must default pre-adoption inferred evidence to untrusted.
- Completion gates must reject adopted standalone tasks whose adoption says evidence was not refreshed.
- Doctor must warn on Review/Complete adopted work whose evidence is still marked untrusted.
- Approval artifact freshness must ignore adoption metadata so adding or refreshing adoption does not stale the approved requirements identity.
- Guidance must route agents through adoption commands for old work.
- Regression tests must cover task adoption, untrusted evidence blocking, refreshed evidence completion, epic adoption, and amendment-log creation.

## Acceptance Criteria (Verifiable)

- AC1: `task adopt` records owner approval and `Legacy Adoption` metadata for pre-existing standalone tasks. Covers parent AC10.
- AC2: `epic adopt` records owner approval and `Legacy Adoption` metadata for pre-existing epics and ensures `AMENDMENTS.md` exists. Covers parent AC10.
- AC3: Adopted work defaults pre-adoption inferred evidence to untrusted until refreshed. Covers parent AC10.
- AC4: Completion gates block unrefreshed adopted task evidence, and refreshed adoption allows completion. Covers parent AC10.
- AC5: Regression tests cover adoption behavior. Covers parent AC12.

## Open Questions (Answer Needed)

- None blocking. Adoption is explicit owner-approved scope; refreshing evidence remains the agent's responsibility before using old proof for completion.

## Decisions (Resolved)

- `Legacy Adoption` metadata is separate from `Owner Approval`.
- Approval artifact identity excludes both `Owner Approval` and `Legacy Adoption` blocks.
- `task adopt` approves implementation scope for standalone tasks.
- `epic adopt` approves decomposition scope for epics and creates `AMENDMENTS.md` if missing.
- `--evidence-refreshed` is explicit; default adoption marks old evidence untrusted.

## Validation Plan

- Run focused adoption regression tests.
- Run full pytest suite.
- Move TASK-034 through epic status gates.
- Run EPIC-006 audit and doctor.
