## User Story

As an owner, agent, or reviewer, I want clear status guidance and realistic journey evidence, so that I can use the command correctly and distinguish repository proof from later delivery claims.

## Parent AC Coverage

- AC2, AC3, AC4, AC5, AC6, AC7, AC9, AC10, AC11

## Child Charter

### Inherited Invariants

- `project status` is read-only in every success, warning, and failure path.
- Existing workflow artifacts remain the only lifecycle and evidence stores; status is a derived projection.
- Current workflow health, work lifecycle, proof state, and delivery state remain separate dimensions.
- Later delivery stages are never inferred from earlier stages.
- Every material conclusion and recommended action retains source provenance.
- One unchanged input state produces the same primary action and stable secondary ordering.
- A mechanical action names an exact supported command; an owner or external action names the required decision or evidence and is never mislabeled as agent-remediable.
- Safety and compatibility blockers outrank ordinary progress, but accepted historical noise does not hide the next meaningful current action.
- Malformed or contradictory state remains visible and cannot be collapsed into a clean summary.
- Status does not approve, accept, repair, mutate, transition, merge, publish, deploy, or run the action it recommends.
- Packaged CLI and generated local helper use the same operational model and remain behaviorally aligned.
- The first version is single-repository and repository-native; live platform verification and assurance policy remain explicit extension points for later Epics.

### Invalid Substitutes

- A passing Doctor result is not proof that work is implemented, reviewed, integrated, released, or deployed.
- A `Complete` tracker row is not proof that its branch was merged or that an artifact was released or deployed.
- Requirements approval, a completed implementation checklist, a QA paragraph, and a structured runtime claim are distinct proof layers and cannot substitute for one another.
- An accepted warning is not a repaired condition, and its suppression from normal Doctor output is not evidence that it disappeared.
- A clean worktree, current branch, tag name, URL, or prose statement is not by itself a verified integration, publication, deployment, or runtime claim.
- A local package version or manifest is not proof that the same version is currently public in a registry.
- A recorded external URL or receipt is not a fresh live verification unless the evidence explicitly records the target, source, observation, and result required for that claim.
- Agent inference is not a substitute for a missing source artifact; the status must report `unknown`, `not recorded`, or a contradiction.
- Human and JSON renderers may not implement separate status or next-action rules.

### Artifact Targets

- Shared operational-status projection, source records, state enums/codes, contradiction handling, and next-action resolver in `src/project_workflow/cli.py`
- Equivalent generated helper behavior in `src/project_workflow/templates/workflow.py` and checked-in local helper parity
- `project status` human renderer, optional focused work-item selection, and versioned JSON schema
- Table-driven lifecycle, proof, delivery, compatibility, malformed-state, ordering, and non-mutation fixtures under `tests/`
- README command guidance plus managed Codex, Cursor, Claude Code, and GitHub Copilot assets explaining status boundaries and next-action use
- EPIC-008 child requirements, implementation plans, evidence, QA, acceptance map/audit, and closeout artifacts

### Parent AC Proof Ownership

- AC2: owner `Read model; inspection; journey children`; required evidence: Tracker/Epic fixture matrix proving complete discovery plus stable contradiction findings without a second status store.
- AC3: owner `Inspection; journey children`; required evidence: Current, stale, legacy, unsupported, and helper-limited fixture outputs matching Doctor and canonical upgrade direction.
- AC4: owner `Inspection; next-action; journey children`; required evidence: Lifecycle-state matrix proving plain-language meaning and the next legal gate for tasks, Fixes, Epics, and children.
- AC5: owner `Read model; classification; journey children`; required evidence: Independently varied proof-layer fixtures showing no cross-layer inflation and exact source provenance.
- AC6: owner `Read model; classification; journey children`; required evidence: Repository-complete, integrated, receipt-backed released, and unknown-delivery fixtures with distinct non-inferred conclusions.
- AC7: owner `Next-action; journey children`; required evidence: Published precedence table plus regression matrix proving responsibility, exact commands, stable tie-breaking, and blocker priority.
- AC9: owner `Inspection; CLI; journey children`; required evidence: Before/after repository hashes and Git-state captures across success, warning, malformed, and failure paths.
- AC10: owner `Classification; next-action; journey children`; required evidence: Accepted/current/strict finding fixtures proving historical noise remains inspectable without displacing a real blocker or action.
- AC11: owner `CLI; journey children`; required evidence: README and generated-agent guidance review, packaged/helper parity, focused/full tests, backlog validation, strict Doctor, and executed UVX packaging proof.

## Acceptance Criteria

- [x] AC1: README and generated agent guidance teach status usage and boundaries.
- [x] AC2: A disposable initialized Git journey proves the checked-in helper and non-mutation.
- [x] AC3: Automated matrices retain parent AC2-AC10 evidence without invalid substitutes.
- [x] AC4: Parity, full validation, Epic audit, and closeout gates pass.
- [x] AC5: Handoff distinguishes repository completion from later delivery and adoption.

## Validation

- AC1: generated-asset and README review/tests.
- AC2: disposable Git repository with human/JSON captures plus before/after hashes and Git identity.
- AC3: focused operational test suites and acceptance-map review.
- AC4: parity, compilation, backlog, strict Doctor, full pytest with Homebrew UVX, Epic audit/closeout.
- AC5: explicit handoff limitations and delivery-state output.

## Goal

Document and independently exercise the completed operational-status product before Epic closeout.

## Approach

- Add concise README examples and generated managed guidance.
- Extend durable tests only where documentation/generation or a realistic journey lacks protection.
- Run and record one disposable Git-backed local-helper journey.
- Refresh acceptance artifacts and close only if every gate passes.

## Phases

1. Document command use and boundaries.
2. Prove generated guidance and disposable operator journey.
3. Refresh acceptance evidence and run repository-wide closeout gates.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Document status usage | Add README and generated-agent guidance for formats, focus, strictness, sources, and command boundaries. | AC1, AC5 | Review exact generated and source documentation. | Done |
| 2 | Prove realistic local-helper journey | Exercise initialized active work through human/JSON status in disposable Git state and compare before/after identity. | AC2, AC3 | Inspect captured semantic assertions and non-mutation results. | Done |
| 3 | Close acceptance evidence | Run parity, focused/full validation, acceptance audit, and Epic closeout gates; record limitations. | AC3, AC4, AC5 | Review gates, audit, and handoff. | Done |

## Parent AC Evidence

- AC2, AC3, AC4: Inspection and lifecycle matrices cover global/current/legacy Epic sources, contradictions, compatibility, and every stored lifecycle meaning/next gate without a second state store.
- AC5: Independent six-layer proof matrices and actual TASK-054 output preserve approval, readiness, implementation, QA, parent acceptance, and structured evidence without cross-layer inflation.
- AC6: Delivery fixtures distinguish non-terminal, repository-complete, Git-integrated, released, verified publication, and verified deployment; a URL alone remains release-only and malformed/missing receipts stay partial.
- AC7: The published eight-rank precedence and 42 resolver tests prove stable responsibility, commands/requests, tie-breaking, blockers, backlog, and no-action behavior.
- AC9: CLI subprocess hashes plus the separate disposable Git journey preserved HEAD, porcelain status, and the hash of every non-Git file across human and JSON status calls.
- AC10: Strict-warning fixtures change warning to fail/blocker while accepted warnings stay counted/hidden; the actual worktree retains 69 accepted warnings without displacing TASK-054.
- AC11: README, managed block, Codex, Cursor, and source Copilot guidance explain status boundaries; the checked-in helper completed the journey; source/template/local payloads remain aligned.
- Manual journey: Initialized a disposable Codex-mode repository, committed its baseline, created TASK-001, then ran the checked-in human and JSON helper. Both reported dirty Git, declared proof, unrecorded delivery, and owner requirements approval as primary. HEAD, porcelain output, and complete non-Git file hash were unchanged.
- Delivery limitation: This branch contains repository-complete implementation evidence only after merge. It is not yet integrated, released as a later package version, publicly published, deployed, or independently adopted; no such claim is made.
- No specialized proof recipe applies; `EVIDENCE.json` remains empty.

## QA & Code Review

- Review date: 2026-07-22
- Reviewed areas: README command clarity; status/Doctor/upgrade/lifecycle/QA/delivery boundaries; generated managed block; Codex/Cursor/source-Copilot guidance; init-generated local helper; disposable Git journey; human/JSON agreement; owner/agent authority; proof/delivery separation; before/after safety; accepted/strict warning coverage; generated payload parity; Epic evidence and handoff limitations.
- Verdict: Pass.
- Evidence:
  - AC1: Documentation tests assert README, managed block, Codex, and Cursor guidance all contain status, focus, strict, JSON, Doctor, upgrade, and QA boundaries; source Copilot guidance protects the implementation contract.
  - AC2: Both the durable subprocess test and a separate manual disposable Git journey initialized the workflow, committed a baseline, created active work, and invoked the generated local helper in human/JSON modes. They agreed on TASK-001, declared proof, unrecorded delivery, owner approval, and sources.
  - AC3: 90 operational-status tests cover model, inspection, classification, resolver, CLI, strict/current/accepted findings, compatibility, malformed state, lifecycle, delivery, ordering, focus, and non-mutation. No fixture is used as evidence of public release or deployment.
  - AC4: 248 full-suite tests passed with Homebrew UVX enabled; the generated-helper journey passed; source/template/local Python payloads match; compilation, backlog, strict Doctor, diff hygiene, acceptance audit, and closeout are run as final gates.
  - AC5: README and handoff explicitly separate repository completion, Git integration, release, publication, deployment, and adoption. The current branch is not claimed as merged, published, deployed, or independently adopted.
- Findings: None. The documentation assertion found and corrected one missing reusable `--id <WORK-ID>` form before the Pass verdict.
- Deferred outside Epic completion: Merge/integration, a future package release, public publication, deployment, and independent adopter evidence require later delivery authority and are not implied by this repository-complete state.

## Retro

- Retro date: 2026-07-22
- Reusable lessons: Documentation should teach command boundaries, not only syntax; reusable placeholders belong beside concrete examples; generated-helper evidence must execute the installed artifact; a realistic dirty-worktree journey catches authority and mutation mistakes that isolated model tests cannot; repository completion must be handed off separately from later delivery/adoption.
- Conventions or agent assets updated: README, generated managed host guidance, packaged Codex/Cursor guidance, source Copilot contract, and durable local-helper journey coverage now teach and protect status usage.
- Follow-up tasks: Run EPIC-008 acceptance audit and closeout now that all children are Complete. No separate backlog or Fix item was needed.
- Missed in-scope work: None.

## Notes

- Task: TASK-054
- Title: Document And Prove End-To-End Operational Journeys
- Created: 2026-07-22
- Scope is unchanged from the approved parent decomposition; implementation authority is inherited from the EPIC-008 approval envelope.
