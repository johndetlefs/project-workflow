## User Story

As a Project Workflow maintainer, I want one clean and exactly proven 0.9.1 candidate, so that the
release cannot publish a different source or untested distribution.

## Parent AC Coverage

- AC1, AC2

## Child Charter

### Inherited Invariants

- Public commands, schemas, lifecycle semantics, asset version 8, and repository schema remain compatible with 0.9.0; only package version/current pins and approved maintenance content change.
- Reviewed source, merge lineage, tag, public wheel/sdist, GitHub release, and provenance identify one immutable 0.9.1 release.
- EPIC-019 evidence and historical workflow records are preserved; release evidence is additive.
- Publication passes before consumer mutation, and every upgrade uses public `project-workflow==0.9.1` rather than the source checkout.
- Only clean, unambiguous canonical authority roots are eligible; user-owned content and unrelated work remain untouched.
- Consumer diffs are not committed, pushed, merged, released, or deployed by this Epic.
- No project is reported upgraded when blocked, partially applied, stale, or unvalidated.
- TASK-102 remains blocked until the exact authenticated Claude canary exists.

### Invalid Substitutes

- EPIC-019's local wheel offered as a public 0.9.1 release.
- A branch push, PR, tag, GitHub run, or PyPI page offered alone as complete release proof.
- Rebuilding or changing the candidate between reviewed source, tag, trusted publication, and public verification without a new immutable version.
- A project label, nested helper copy, or stale saved path offered as a canonical installation.
- A successful upgrade command without clean-root preflight, reviewed fingerprint, no-op re-plan, scoped diff, exact version, and Doctor evidence.
- Forced mutation of dirty, active, detached, ambiguous, nested, or unreconciled consumer state.
- Package or fixture proof offered as authenticated Claude Code runtime certification.

### Artifact Targets

- One clean reviewed 0.9.1 source commit and retained candidate receipt.
- PyPI `project-workflow==0.9.1` and GitHub Release `v0.9.1` with verified wheel, sdist, hashes, receipt, package journeys, and attestations.
- Independent public-install and upgrade journey receipt.
- Complete local project inventory with one disposition per entry.
- Validated 0.9.1 managed assets at every eligible canonical consumer root.
- Consolidated machine-readable release/rollout receipt plus parent acceptance audit.

### Parent AC Proof Ownership

- AC1: owner `TASK-109`; required evidence: Coherent version scan, generated parity, source contract, package inventory, and diff hygiene
- AC2: owner `TASK-109`; required evidence: Locked gates, complete suite, strict Doctor, exact build/journeys, retained EPIC-019 QA, and candidate receipt

## Acceptance Criteria

- [ ] AC1: Current release identity is coherently 0.9.1 and historical evidence is preserved.
- [ ] AC2: The clean source commit passes every locked source and workflow gate.
- [ ] AC3: One retained wheel/sdist set passes inspection and exact-package journeys.
- [ ] AC4: EPIC-019 QA remains applicable and the candidate is not yet represented as published.

## Validation

- AC1 / parent AC1: version and current-guidance scan, manifest/source contract, generated parity.
- AC2 / parent AC1-AC2: locked static/documentation/architecture/full-suite/Doctor checks on clean
  committed source.
- AC3 / parent AC2: build once, inspect distributions, exact-wheel package journeys and hashes.
- AC4 / parent AC2: diff-versus-QA impact review and retained delivery boundary.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Align 0.9.1 release identity | Update canonical version, current pins, changelog, workflows, tests, and deterministic runtime without rewriting history. | AC1 | Run source/version scan and generated-runtime check. | To Do |  | version sources; current docs; CI/release workflows; tests; generated runtime | No | bounded-return |
| 2 | Commit and prove clean source | Commit the complete candidate, then run locked documentation, architecture, Ruff, format, mypy, pytest, Doctor, and clean source-contract gates. | AC2, AC4 | Inspect clean Git identity and retained gate results. | To Do | 1 | repository source; task evidence | No | bounded-return |
| 3 | Build and exercise exact distributions | Build once, inspect wheel/sdist contents, run exact-package journeys, and retain hashes and receipts. | AC3 | Compare candidate receipt to executed wheel identity. | To Do | 2 | dist; task evidence | No | bounded-return |
| 4 | Seal candidate handoff | Confirm EPIC-019 QA remains current, record the unpublished boundary, and return exact identities to TASK-110. | AC4 | Review source/artifact/QA identity and delivery state. | To Do | 2, 3 | task evidence | No | bounded-return |

## Parent AC Evidence

- AC1, AC2: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: ____
- Intent adversarial verdict: ____
- Could every AC pass while the approved user job remains undone: ____
- Intent audit state: ____
- Outcome journey evidence: ____
- Reviewer independence: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-109
- Title: Prepare and prove the exact Project Workflow 0.9.1 candidate
- Created: 2026-08-29
