## User Story

As the owner, I want every existing Codex Project Workflow installation upgraded safely so that Delegate is available across active projects without clobbering repository work.

## Parent AC Coverage

- AC5, AC6, AC7

## Child Charter

### Inherited Invariants

- The reviewed source, tag, wheel, source distribution, release assets, and public package are traceable to one 0.4.0 release identity.
- Historical completed-task evidence is not rewritten to simulate current version alignment.
- Consumer user-owned files and unrelated Git changes are preserved.
- Only canonical project authority roots are upgraded; workspace child repositories do not gain duplicate workflow state.
- No consumer project is called upgraded if it is blocked, partially mutated, or not validated.

### Invalid Substitutes

- A green source test suite without exact built/public artifact checks.
- A tag or GitHub Release without PyPI publication and fresh installation proof.
- A saved Codex project name without a canonical root manifest.
- A source-checkout upgrade, copied managed files, or an unreviewed nested workflow copy in place of public-package upgrade.
- A successful upgrade command without scoped diff and Doctor validation.

### Artifact Targets

- PyPI `project-workflow==0.4.0`.
- GitHub Release `v0.4.0` with wheel, source distribution, hashes/provenance, and release notes.
- A clean, validated Project Workflow `main` lineage.
- Per-project installed 0.4.0 managed assets for every eligible Codex project.
- Parent release/rollout receipt and acceptance audit.

### Parent AC Proof Ownership

- AC5: owner `TASK-067`; required evidence: Codex project inventory and per-project disposition
- AC6: owner `TASK-067`; required evidence: Per-project plan/apply/diff/manifest/helper/Doctor validation
- AC7: owner `TASK-068`; required evidence: Consolidated receipt and parent acceptance audit

## Acceptance Criteria

- [ ] AC1: Every saved project is inventoried and every installed authority root is upgraded or explicitly blocked.
- [ ] AC2: Every applied upgrade has expected scoped changes, version 0.4.0, preserved user content, and passing Doctor.
- [ ] AC3: The consolidated machine-readable receipt ties every disposition to exact release and validation evidence.

## Validation

- AC1 / parent AC5: live saved-project inventory plus root/manifest/Git classification.
- AC2 / parent AC6: per-root plan/apply/diff/version/helper/Doctor records.
- AC3 / parent AC7: retained `evidence/release-rollout-receipt.json` and parent acceptance audit.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Inventory Codex projects | Classify every saved project before mutation. | AC1: exhaustive dispositions | Compare receipt to live inventory | To Do |
| 2 | Upgrade eligible roots | Plan and apply public 0.4.0 only where safety gates pass. | AC2: scoped validated upgrades | Inspect diffs, versions, helpers, and Doctor | To Do |
| 3 | Retain rollout receipt | Consolidate release, inventory, project validation, and blocker evidence. | AC3: complete machine-readable proof | Validate JSON and parent audit mapping | To Do |

## Parent AC Evidence

- AC5, AC6, AC7: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-069
- Title: Inventory and upgrade every eligible Codex Project Workflow installation, then retain the consolidated rollout receipt
- Created: 2026-08-20
