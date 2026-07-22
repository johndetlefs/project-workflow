## User Story

As an owner or agent returning to a repository, I want status to identify the one highest-value safe next action and explain why, so that I can continue without reconstructing workflow precedence or accidentally crossing an authority boundary.

## Parent AC Coverage

- AC4, AC7, AC10

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

- AC4: owner `Inspection; next-action; journey children`; required evidence: Lifecycle-state matrix proving plain-language meaning and the next legal gate for tasks, Fixes, Epics, and children.
- AC7: owner `Next-action; journey children`; required evidence: Published precedence table plus regression matrix proving responsibility, exact commands, stable tie-breaking, and blocker priority.
- AC10: owner `Classification; next-action; journey children`; required evidence: Accepted/current/strict finding fixtures proving historical noise remains inspectable without displacing a real blocker or action.

## Acceptance Criteria

- [x] AC1: Precedence is explicit and compatibility/safety blockers outrank lower-value candidates.
- [x] AC2: Every work kind and lifecycle maps to an exact supported command or concrete responsible-party request.
- [x] AC3: Primary and secondary action ordering is stable, complete, and duplicate-free.
- [x] AC4: The earliest unmet proof layer wins without cross-layer inflation.
- [x] AC5: Accepted warnings do not displace current action; strict/current blockers and authority labels remain correct.
- [x] AC6: Every installation compatibility state yields an exact safe action or request.
- [x] AC7: No-active-work fallback selects recorded backlog intent deterministically or reports no action.
- [x] AC8: Focused/full behavior, payloads, non-mutation, parity, and repository gates pass.

## Validation

- AC1, AC3: exact precedence and permutation/tie-breaking matrix.
- AC2, AC4: lifecycle-by-kind and proof-gap matrices.
- AC5, AC6: Doctor acceptance/strictness plus installation-state matrix.
- AC7: backlog priority/order/malformed/empty fixtures.
- AC8: focused pytest, compilation, source/template/local parity, before/after hashes and Git state, backlog validation, strict Doctor, diff hygiene, and full pytest with Homebrew UVX.

## Goal

Add one pure resolver that turns classified operational state into one sourced primary action and stable secondary actions without executing them.

## Approach

- Define action precedence as a reviewed constant shared by candidate generation and tests.
- Generate immutable action candidates for installation, visible blockers, proof gaps, work lifecycle, delivery follow-up, and backlog fallback.
- Sort once by precedence, discovery order, item ID, and action code; project the first candidate as primary and retain the rest as secondary.
- Reuse existing commands and responsibility boundaries; represent unavailable authority as a concrete request.

## Phases

1. Define precedence/candidate contracts and installation/finding candidates.
2. Add proof and lifecycle candidates for every work kind.
3. Add deterministic backlog/no-action fallback and focused filtering.
4. Prove ordering, authority, non-mutation, and maintained-payload parity.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define resolver precedence and candidates | Publish one precedence contract and internal stable candidate representation. | AC1, AC3 | Assert exact rank names and stable candidate sorting. | Done |
| 2 | Resolve compatibility and current blockers | Produce canonical upgrade/init commands or explicit repair/authority requests without elevating accepted warnings. | AC1, AC5, AC6 | Run installation and Doctor state matrices. | Done |
| 3 | Resolve proof and lifecycle gates | Map the earliest unmet proof plus every work kind/lifecycle to an existing command or concrete request. | AC2, AC4, AC5 | Run work-kind, lifecycle, and independent proof-gap matrices. | Done |
| 4 | Resolve backlog and stable fallbacks | Select backlog intent by priority/file order, support focused scope, and return explicit no-action when empty. | AC3, AC7 | Exercise priority, ordering, malformed, terminal, focused, and empty fixtures. | Done |
| 5 | Prove parity and safety | Add exact payload and non-mutation coverage and run all repository gates. | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8 | Review focused/full output, hashes, Git state, mirrors, Doctor, backlog, and full suite. | Done |

## Parent AC Evidence

- AC4: The lifecycle matrix covers tasks, Fixes, Epics, and Epic children, including legal task `To Do` to `Analysing`, triage, testing, review, completion, blocked, and terminal behavior without rewriting stored states.
- AC7: The precedence constant and 41 action tests prove compatibility, current blockers, owner decisions, proof gates, lifecycle, delivery, backlog, and no-action ordering; repeated inputs preserve source order and duplicate-free secondary actions.
- AC10: Accepted warnings are absent from action inputs while visible strict errors become blocking candidates; actual strict health remains Pass with 69 accepted warnings and does not displace TASK-052 implementation.
- Actual-worktree projection: Primary action is `PW_STATUS_IMPLEMENTATION_REQUIRED` for TASK-052; secondary actions are EPIC-008 Ready plus authorized approval of TASK-053 and TASK-054, in stable precedence/source order.
- No specialized proof recipe applies; `EVIDENCE.json` is empty and deterministic repository fixtures/tests are the required evidence.

## QA & Code Review

- Review date: 2026-07-22
- Reviewed areas: explicit precedence; candidate immutability; installation compatibility; visible/accepted Doctor findings; responsibility assignment; work-kind lifecycle legality; proof-layer ordering; source provenance; exact commands; owner/service requests; stable source-order tie-breaking; item-specific de-duplication; focused selection; backlog priority/order; malformed state; terminal behavior; delivery follow-up; actual-worktree projection; non-mutation; maintained payload parity; child-scope boundaries.
- Verdict: Pass.
- Evidence:
  - AC1: The eight-rank `OPERATIONAL_STATUS_ACTION_PRECEDENCE` contract is asserted exactly; combined fixtures prove installation and current errors outrank work progress while lower-ranked actions remain ordered secondary candidates.
  - AC2: Task, Fix, Epic, and Epic-child matrices cover analysis, readiness, start, testing, review, closeout/completion, triage, scaffold, blocked, and terminal paths using existing commands or named requests. Review caught and corrected the task `To Do` transition to use legal `Analysing` rather than skipping to `Ready`.
  - AC3: Repeated resolution is equal; source order wins before item ID/code; repeated identical items collapse while distinct items with identical delivery requests remain separately actionable after de-duplication was tightened to include action title.
  - AC4: Six independent proof-gap cases select approval, readiness, implementation, QA, parent acceptance, and structured evidence in order, with owner, agent, and service authority preserved.
  - AC5: An accepted warning is absent from visible candidates; a visible strict/current error outranks work and retains the Doctor code/source and correct remediation owner.
  - AC6: Upgradeable, legacy-unversioned, uninitialized, helper-limited, unsupported-future, invalid, and unknown installation states return the canonical command or an explicit owner request with command/request exclusivity.
  - AC7: Backlog fixtures select High before Medium and file order within priority, skip Deferred/promoted rows, preserve file bytes, surface malformed schema, and return explicit no-action for empty state.
  - AC8: 82 focused operational-status tests and Python compilation passed; 240 full-suite tests passed with Homebrew UVX enabled; source/template/local Python payloads are byte-identical; diff hygiene passed.
  - Actual-worktree evidence: strict health is Pass; the resolver selects TASK-052 implementation as primary, followed by EPIC-008 readiness and authorized TASK-053/TASK-054 approval in stable order.
- Findings: None remaining. Two review findings—illegal task `To Do` jump and cross-item delivery de-duplication—were corrected and regression-tested before the Pass verdict.
- Deferred by approved scope: CLI parser/rendering, final snapshot composition, public documentation, and end-to-end operator journeys remain owned by TASK-053 and TASK-054.

## Retro

- Retro date: 2026-07-22
- Reusable lessons: Candidate generation plus one stable sort keeps precedence out of renderers; exact existing transitions must be checked against the workflow transition map, not inferred from lifecycle names; de-duplication identities must preserve distinct affected items; accepted Doctor warnings should disappear from action inputs but remain counted in health; no-action and malformed-focus results should be explicit records rather than `None`.
- Conventions or agent assets updated: Resolver constants, typed candidates, and 42 focused action tests now encode these status-specific rules. No broader managed-agent guidance changed because TASK-053/TASK-054 already own public command guidance and operator journeys.
- Follow-up tasks: Continue EPIC-008 with approved TASK-053 CLI composition and rendering. No separate backlog or Fix item was needed.
- Missed in-scope work: None.

## Notes

- Task: TASK-052
- Title: Build Deterministic Next-Action Resolver
- Created: 2026-07-22
- Scope is unchanged from the approved parent decomposition; implementation authority is inherited from the EPIC-008 approval envelope.
