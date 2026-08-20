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

- AC5: owner `TASK-069`; required evidence: Codex project inventory and per-project disposition
- AC6: owner `TASK-069`; required evidence: Per-project plan/apply/diff/manifest/helper/Doctor validation
- AC7: owner `TASK-069`; required evidence: Consolidated receipt and parent acceptance audit

## Acceptance Criteria

- [x] AC1: Every saved project is inventoried and every installed authority root is upgraded or explicitly blocked.
- [x] AC2: Every applied upgrade has expected scoped changes, version 0.4.0, preserved user content, and applicable current-version/Doctor validation.
- [x] AC3: The consolidated machine-readable receipt ties every disposition to exact release and validation evidence.

## Validation

- AC1 / parent AC5: live saved-project inventory plus root/manifest/Git classification.
- AC2 / parent AC6: per-root plan/apply/diff/version/helper/Doctor records.
- AC3 / parent AC7: retained `evidence/release-rollout-receipt.json` and parent acceptance audit.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | released `main` at `e9fe9d1`; PR #13 | Public release and source Doctor passed | Released and current | TASK-067/TASK-068 evidence |
| mechanics-playground | local `main` at `9669e96`; not pushed | 0.4.0/current; managed diff exact; legacy Doctor debt retained | Local adoption complete | `evidence/release-rollout-receipt.json` |
| game-foundation | local `main` at `bf68b5e`; not pushed | 0.4.0/current; Doctor clean | Local adoption complete | `evidence/release-rollout-receipt.json` |
| tobys-games | local `main` at `521dd1b`; not pushed | 0.4.0/current; Doctor clean | Local adoption complete | `evidence/release-rollout-receipt.json` |
| strategic-advisor | local divergent `main` at `485a070`; not pushed | 0.4.0/current; Doctor clean | Local adoption complete; remote divergence retained | `evidence/release-rollout-receipt.json` |
| daily-checklist | local `main` at `06eeb9e`; not pushed | 0.4.0/current; managed diff exact; legacy Doctor debt retained | Local adoption complete | `evidence/release-rollout-receipt.json` |
| client-management-app | local `main` at `ecb9c62`; not pushed | 0.4.0/current; managed diff exact; historical Doctor debt retained | Local adoption complete | `evidence/release-rollout-receipt.json` |
| the-moon-is-hollow | `codex/EPIC-001-product-foundation` at `5c698ed`; dirty | Plan only; active backlog change preserved | Blocked unchanged on 0.3.0 | `evidence/release-rollout-receipt.json` |
| johndetlefs | `main` at `d8c2f48`; 56 active workflow changes | Plan only; active Epic/task evidence preserved | Blocked unchanged on 0.3.0 | `evidence/release-rollout-receipt.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Inventory Codex projects | Classify every saved project before mutation. | AC1: exhaustive dispositions | Compare receipt to live inventory | Done |
| 2 | Upgrade eligible roots | Plan and apply public 0.4.0 only where safety gates pass. | AC2: scoped validated upgrades | Inspect diffs, versions, helpers, and Doctor | Done |
| 3 | Retain rollout receipt | Consolidate release, inventory, project validation, and blocker evidence. | AC3: complete machine-readable proof | Validate JSON and parent audit mapping | Done |

## Parent AC Evidence

- AC5: All 18 local and two ChatGPT projects from the live Codex inventory have dispositions. Nine local roots had canonical installations: seven are current on 0.4.0 and two remain explicitly blocked and unchanged.
- AC6: Six public-package upgrades used reviewed fingerprints and changed only planned managed files; the source checkout fast-forwarded to the released main commit. All seven current roots have matching Delegate/helper hashes, no collision `.new` files, clean post-operation worktrees, and recorded Doctor boundaries.
- AC7: `evidence/release-rollout-receipt.json` ties the public release, every saved project, each plan/commit/validation result, and both blockers together.

## QA & Code Review

- Verdict: Pass with explicit safety blockers
- Evidence: Live Codex project inventory, per-root manifests/Git state/plans/apply output/hashes/Doctor summaries, six local upgrade commits, released source checkout, and `evidence/release-rollout-receipt.json`.
- Findings: The Moon Is Hollow and johndetlefs remain on 0.3.0 because active workflow changes make the canonical clean-worktree precondition fail. Consumer commits are local and intentionally not pushed; strategic-advisor retains its pre-existing main/origin divergence.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-069
- Title: Inventory and upgrade every eligible Codex Project Workflow installation, then retain the consolidated rollout receipt
- Created: 2026-08-20
