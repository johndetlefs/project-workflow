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

- [x] AC1: Covers parent AC5 when every inventoried project has an evidence-backed disposition and every eligible installed root is upgraded.

## Validation

- AC1 / parent AC5: Record inventory roots, manifests, Git state, upgrade plans/results, and post-upgrade version/Doctor status.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| Codex saved-project inventory | Current inventory observed 2026-08-20 | 20/20 projects classified; 9 canonical installations: 6 upgraded, 1 already current, 2 blocked dirty and unchanged | Adoption complete within safety boundary | `evidence/release-rollout-receipt.json`; child `EVIDENCE.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Inventory and upgrade | Classify all current Codex projects and apply the public canonical upgrade to every eligible installed authority root. | AC1: every inventoried project has an evidence-backed disposition and every eligible installed root is upgraded. | Review the per-project disposition list and upgrade outputs. | Done | | Current Codex project roots with canonical .project-workflow manifests | No | bounded-return |

## Parent AC Evidence

- AC5: All 20 current saved projects have a retained disposition. Six clean consumer roots were upgraded from public 0.5.0, Project Workflow was already current at released main, nine local roots had no canonical installation, two ChatGPT projects had no local root, and the two dirty installed roots were left unchanged with exact blockers. Structured runtime/source evidence passes in `EVIDENCE.json`.

## QA & Code Review

- Verdict: Pass (2026-08-20)
- Evidence: Live Codex schema-v2 project inventory, manifest/Git inspection for all local roots, exact plan fingerprints, post-action status, and consolidated receipt.
- Findings: No release blocker. The Moon Is Hollow and johndetlefs remain deliberately on 0.3.0 until their active workflow changes are cleanly resolved.

## Retro

- Reusable lessons: A technically upgradeable plan is not sufficient authority to mutate a dirty project; eligibility also requires a clean, unambiguous root.
- Conventions or agent assets updated: None; existing upgrade safeguards already encode the rule.
- Follow-up tasks: Upgrade the two blocked roots in their own active work context after their workflow changes are committed or otherwise resolved.

## Notes

- Task: TASK-077
- Title: Every project in the current Codex saved-project inventory has a recorded disposition, and every project with a canonical Project Workflow installation is either upgraded from public 0.5.0 or retained unchanged with a concrete safety blocker
- Created: 2026-08-20
