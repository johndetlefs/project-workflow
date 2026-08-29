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

- [x] AC1: Current release identity is coherently 0.9.1 and historical evidence is preserved.
- [x] AC2: The clean source commit passes every locked source and workflow gate.
- [x] AC3: One retained wheel/sdist set passes inspection and exact-package journeys.
- [x] AC4: EPIC-019 QA remains applicable and the candidate is not yet represented as published.

## Validation

- AC1 / parent AC1: version and current-guidance scan, manifest/source contract, generated parity.
- AC2 / parent AC1-AC2: locked static/documentation/architecture/full-suite/Doctor checks on clean
  committed source.
- AC3 / parent AC2: build once, inspect distributions, exact-wheel package journeys and hashes.
- AC4 / parent AC2: diff-versus-QA impact review and retained delivery boundary.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/structural-coherence-cleanup`; source commit `3289ff9cfbe5f7c7f85fe9e2a9fe242c46c076e3`; no PR yet | Locked static/docs/runtime gates, 561 tests, strict Doctor, clean source contract, build receipt, and exact-wheel journeys passed | Local committed candidate only; not pushed, merged, tagged, published, publicly verified, or rolled out | `EVIDENCE.json`; `evidence/candidate/validation-summary.json`; `evidence/candidate/release-receipt.json`; `evidence/candidate/package-journeys.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Align 0.9.1 release identity | Update canonical version, current pins, changelog, workflows, tests, and deterministic runtime without rewriting history. | AC1 | Run source/version scan and generated-runtime check. | Done |  | version sources; current docs; CI/release workflows; tests; generated runtime | No | bounded-return |
| 2 | Commit and prove clean source | Commit the complete candidate, then run locked documentation, architecture, Ruff, format, mypy, pytest, Doctor, and clean source-contract gates. | AC2, AC4 | Inspect clean Git identity and retained gate results. | Done | 1 | repository source; task evidence | No | bounded-return |
| 3 | Build and exercise exact distributions | Build once, inspect wheel/sdist contents, run exact-package journeys, and retain hashes and receipts. | AC3 | Compare candidate receipt to executed wheel identity. | Done | 2 | dist; task evidence | No | bounded-return |
| 4 | Seal candidate handoff | Confirm EPIC-019 QA remains current, record the unpublished boundary, and return exact identities to TASK-110. | AC4 | Review source/artifact/QA identity and delivery state. | Done | 2, 3 | task evidence | No | bounded-return |

## Parent AC Evidence

- AC1: commit `3289ff9cfbe5f7c7f85fe9e2a9fe242c46c076e3` passes the coherent 0.9.1
  version scan, deterministic runtime, documentation contract, static gates, strict Doctor, and
  clean release-source contract. Historical 0.9.0 evidence remains unchanged.
- AC2: all 561 tests pass in 85.57 seconds; exact wheel
  `sha256:a373a837ed7913856e156f21ce5a49675a044b9e8aa1e6c7c9b7ebffa8e012a2` and sdist
  `sha256:e19caa282816e79629a710c219bca9d48e950f7080590eead5f68367a7f133cc` pass
  receipt verification and complete package journeys. EPIC-019 QA hash remains
  `sha256:838eb069e88a7d9940e0203d701afdb0507a5f8937d8f76ee8b8d6aff39735a1`.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Intent QA rationale: The clean-source identity, retained artifacts, and package journeys prove
  the bounded candidate job without substituting for the still-pending release and rollout
  children. The larger owner job remains visibly open in TASK-110 through TASK-112.
- Outcome journey evidence: The exact wheel
  `sha256:a373a837ed7913856e156f21ce5a49675a044b9e8aa1e6c7c9b7ebffa8e012a2`
  passed all four installed-agent fresh, current, legacy, no-op, Doctor, lifecycle, and helper
  journeys; the sdist is `sha256:e19caa282816e79629a710c219bca9d48e950f7080590eead5f68367a7f133cc`.
- Reviewer independence: A distinct read-only adversarial pass was performed after implementation
  and campaign completion. System policy prohibited delegating to a separate subagent, so reviewer
  independence is procedural rather than a separate execution context.
- Evidence: `evidence/candidate/validation-summary.json`, `evidence/candidate/release-receipt.json`,
  `evidence/candidate/package-journeys.json`, clean `git show --check`, artifact hash recheck, and
  a post-commit diff proving that only EPIC-020 workflow evidence changed after the source commit.
- Findings: No blocking or non-blocking findings. Publication, public provenance, and consumer
  adoption remain deliberately unproven and assigned to later children.

## Retro

- Reusable lessons: Commit before candidate certification so clean-source proof and artifact source
  identity cannot be inferred from a dirty worktree.
- Conventions or agent assets updated: Current package pins, changelog, generated runtime, tests,
  CI, and release workflow now agree on 0.9.1.
- Follow-up tasks: TASK-110 owns push, reviewed integration, tag, and trusted publication.

## Notes

- Task: TASK-109
- Title: Prepare and prove the exact Project Workflow 0.9.1 candidate
- Created: 2026-08-29
