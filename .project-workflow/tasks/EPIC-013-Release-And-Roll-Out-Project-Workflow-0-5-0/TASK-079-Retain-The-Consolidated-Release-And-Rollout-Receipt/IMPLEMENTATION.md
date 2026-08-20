## User Story

As the release owner, I want one durable release-and-rollout receipt so that the final adoption boundary is explicit and auditable.

## Parent AC Coverage

- AC7

## Child Charter

### Inherited Invariants

- The reviewed source, tag, wheel, source distribution, release assets, and public package are traceable to one 0.5.0 release identity.
- Historical completed-task evidence is not rewritten to simulate current version alignment.
- Consumer user-owned files and unrelated Git changes are preserved.
- Only canonical project authority roots are upgraded; workspace children do not gain duplicate workflow state.
- No consumer project is called upgraded if it is blocked, partially mutated, or not validated.

### Invalid Substitutes

- A green source test suite without exact built/public artifact checks.
- A tag or GitHub Release without PyPI publication and fresh installation proof.
- A saved Codex project name without a canonical root manifest.
- A source-checkout upgrade, copied managed files, or an unreviewed nested workflow copy in place of public-package upgrade.
- A successful upgrade command without scoped diff and Doctor validation.

### Artifact Targets

- PyPI `project-workflow==0.5.0`.
- GitHub Release `v0.5.0` with wheel, source distribution, hashes/provenance, and release notes.
- A clean, validated Project Workflow `main` lineage.
- Per-project installed 0.5.0 managed assets for every eligible Codex project.
- Parent release/rollout receipt and acceptance audit.

### Parent AC Proof Ownership

- AC7: owner `TASK-077`; required evidence: Consolidated receipt and parent acceptance audit

## Acceptance Criteria

- [ ] AC1: Covers parent AC7 when the receipt is complete, identity-bound, sanitized, and accepted by the parent audit.

## Validation

- AC1 / parent AC7: Validate receipt schema/content, evidence paths, AC mapping, and parent acceptance audit.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/EPIC-012-delegate-executor-lifecycle | Planned validation recorded in this task | Pending release/adoption stage | Coordinator command output and retained evidence |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Retain rollout receipt | Consolidate exact release identities, public proof, project dispositions, validations, and blockers into one receipt. | AC1: The receipt is complete, identity-bound, sanitized, and accepted by the parent audit. | Inspect the JSON receipt and parent acceptance audit. | To Do | | .project-workflow/tasks/EPIC-013-Release-And-Roll-Out-Project-Workflow-0-5-0/evidence | No | bounded-return |

## Parent AC Evidence

- AC7: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-079
- Title: Retain the consolidated release and rollout receipt
- Created: 2026-08-20
