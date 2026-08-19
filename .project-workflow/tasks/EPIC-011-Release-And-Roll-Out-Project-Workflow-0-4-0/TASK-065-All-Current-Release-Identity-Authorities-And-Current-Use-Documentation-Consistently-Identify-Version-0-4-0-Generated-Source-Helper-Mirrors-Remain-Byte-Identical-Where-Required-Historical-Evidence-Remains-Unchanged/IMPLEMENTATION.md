## User Story

As the Project Workflow maintainer, I want one consistent 0.4.0 release candidate so that the completed Delegate feature can be published without version or artifact ambiguity.

## Parent AC Coverage

- AC1

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

- AC1: owner `TASK-065`; required evidence: Version scan, mirror parity, changelog/docs/workflow diff

## Acceptance Criteria

- [x] AC1: Every current release authority identifies 0.4.0, required mirrors match, and historical evidence remains untouched.

## Validation

- AC1 / parent AC1: version scan, mirror comparison, release-contract source check, and reviewed diff.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/EPIC-010-delegate-execution-orchestrator`; PR pending | `check-source --version 0.4.0 --tag v0.4.0`, mirror comparisons, version scan, `git diff --check` passed | Release candidate prepared; not yet merged or published | Current diff and command output on 2026-08-20 |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Prepare 0.4.0 identity | Update canonical version authorities, release workflows, changelog, and current-use documentation while preserving history. | AC1 / parent AC1: all current identities and mirrors agree | Run version scan and source contract check | Done |

## Parent AC Evidence

- AC1: Source, three CLI mirrors, manifest, CI/release workflows, current docs, and deterministic test expectations agree on 0.4.0; the only retained 0.3.0 current-scope scan hit is the historical changelog heading.

## QA & Code Review

- Verdict: Pass
- Evidence: `check-source` reported 0.4.0; both mirror comparisons returned identical; PyPI availability check confirmed 0.4.0 absent; `git diff --check` passed.
- Findings: None.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-065
- Title: All current release identity authorities and current-use documentation consistently identify version 0.4.0; generated source/helper mirrors remain byte-identical where required; historical evidence remains unchanged
- Created: 2026-08-20
