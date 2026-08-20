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

- AC7: owner `TASK-079`; required evidence: Consolidated receipt and parent acceptance audit

## Acceptance Criteria

- [x] AC1: Covers parent AC7 when the receipt is complete, identity-bound, sanitized, and accepted by the parent audit.

## Validation

- AC1 / parent AC7: Validate receipt schema/content, evidence paths, AC mapping, and parent acceptance audit.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | Release `fdd4e15`; rollout evidence on closeout branch | JSON syntax, SHA-256, 20-row inventory reconciliation, 9-installation reconciliation, and AC1-AC7 key mapping pass | Durable receipt retained for closeout review | `evidence/release-rollout-receipt.json` SHA-256 `c9ed45ab...`; child `EVIDENCE.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Retain rollout receipt | Consolidate exact release identities, public proof, project dispositions, validations, and blockers into one receipt. | AC1: The receipt is complete, identity-bound, sanitized, and accepted by the parent audit. | Inspect the JSON receipt and parent acceptance audit. | Done | | .project-workflow/tasks/EPIC-013-Release-And-Roll-Out-Project-Workflow-0-5-0/evidence | No | bounded-return |

## Parent AC Evidence

- AC7: `evidence/release-rollout-receipt.json` binds public release identity and provenance, candidate/public validation, all 20 Codex project dispositions, all nine canonical installation outcomes, six local upgrade commits, exact blockers, and proof boundaries; its SHA-256 is `c9ed45ab47b081b388a8edf4ce39bbe4b38fddd045ef7b22faff4e2690c91dff`. Structured contract evidence passes in `EVIDENCE.json`.

## QA & Code Review

- Verdict: Pass (2026-08-20)
- Evidence: JSON parser, exact receipt hash, manual reconciliation against live inventory and Git state, and explicit parent AC key mapping.
- Findings: None. The receipt contains paths and commit identities but no task IDs, runtime handles, credentials, or transcripts.

## Retro

- Reusable lessons: One consolidated receipt should record both successful adoption and protected non-adoption; omission is not a safe disposition.
- Conventions or agent assets updated: None.
- Follow-up tasks: None beyond the two explicitly blocked future upgrades and existing consumer Doctor debt.

## Notes

- Task: TASK-079
- Title: Retain the consolidated release and rollout receipt
- Created: 2026-08-20
