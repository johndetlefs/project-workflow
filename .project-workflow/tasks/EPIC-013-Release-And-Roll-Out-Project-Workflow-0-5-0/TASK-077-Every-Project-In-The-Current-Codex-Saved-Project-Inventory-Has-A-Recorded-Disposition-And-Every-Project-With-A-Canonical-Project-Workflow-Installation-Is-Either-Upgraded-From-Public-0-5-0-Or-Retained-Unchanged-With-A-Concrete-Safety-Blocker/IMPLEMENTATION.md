## User Story

As the owner, I want every current Codex project accounted for so that 0.5.0 adoption is comprehensive without trampling active work.

## Parent AC Coverage

- AC5

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

- AC5: owner `TASK-077`; required evidence: Codex project inventory and per-project disposition

## Acceptance Criteria

- [ ] AC1: Covers parent AC5 when every inventoried project has an evidence-backed disposition and every eligible installed root is upgraded.

## Validation

- AC1 / parent AC5: Record inventory roots, manifests, Git state, upgrade plans/results, and post-upgrade version/Doctor status.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/EPIC-012-delegate-executor-lifecycle | Planned validation recorded in this task | Pending release/adoption stage | Coordinator command output and retained evidence |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Inventory and upgrade | Classify all current Codex projects and apply the public canonical upgrade to every eligible installed authority root. | AC1: every inventoried project has an evidence-backed disposition and every eligible installed root is upgraded. | Review the per-project disposition list and upgrade outputs. | To Do | | Current Codex project roots with canonical .project-workflow manifests | No | bounded-return |

## Parent AC Evidence

- AC5: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-077
- Title: Every project in the current Codex saved-project inventory has a recorded disposition, and every project with a canonical Project Workflow installation is either upgraded from public 0.5.0 or retained unchanged with a concrete safety blocker
- Created: 2026-08-20
