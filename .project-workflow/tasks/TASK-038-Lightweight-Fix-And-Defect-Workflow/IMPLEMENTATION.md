## User Story

As a project-workflow maintainer, I want post-completion corrective work to use
a lightweight, linked Fix record, so completed tasks remain historically
accurate while defects, regressions, bounded changes, and incidents can be
triaged, delivered, verified, and closed with proportionate evidence.

## Goal

Deliver Fix as a lightweight work-item subtype that shares the existing task
directory, global tracker, status vocabulary, validation infrastructure, and
workspace model while using one proportionate `FIX.md` artifact.

## Approach

- Reserve `FIX-###` as the kind discriminator so the existing four-column global
  tracker does not require a new `Type` column or migration.
- Add purpose-specific Fix commands as a thin interface over shared ID,
  tracker, lifecycle, doctor, and workspace helpers.
- Dispatch validation and transition rules by work-item kind so full tasks keep
  their current requirements/plan gates and Fixes use triage plus closeout
  evidence gates.
- Keep Fix artifacts under `.project-workflow/tasks/` and do not introduce a
  second tracker, index, or artifact tree.
- Correct standalone-task approval timing so owner approval validates and
  fingerprints requirements before planning, matching the established epic
  authority model.
- Make Planner and post-plan Clarify autonomous derivation/consistency phases;
  keep `task ready` as the combined machine gate and use `Ready` for new work
  while preserving `Plan Confirmed` compatibility.
- Preserve bounded authority: approved delivery work may continue inside the
  envelope, while material drift, exceptional action authority, optional
  risk-triggered plan review, and final completion return to the owner.

## Phases

1. **Shared work-item model:** add reserved Fix identity, the single-file
   scaffold, shared global-tracker registration, and workspace-aware metadata.
2. **Lifecycle and evidence gates:** add triage, normal/hotfix transitions,
   promotion, verification/regression closeout, and kind-aware doctor rules.
3. **Authority and autonomous handoff:** separate requirements approval from
   plan readiness, automate Planner/Clarify/Ready progression, preserve bounded
   stop conditions, and align standalone tasks, epics, and Fix triage.
4. **Product integration and proof:** update generated agents, templates, CLI
   help, documentation, init-refresh behavior, and regression coverage.

## Acceptance Criteria

- [x] AC1: Linked completed work remains byte- and status-unchanged by default.
- [x] AC2: Guidance routes in-flight corrections to active scope and later corrections to Fixes.
- [x] AC3: Fix CLI commands allocate `FIX-###`, create one shared-tracker row, and scaffold one Fix artifact.
- [x] AC4: Defect, Regression, Change Request, Incident, and Hotfix mode remain distinct.
- [x] AC5: A Fix uses one `tasks/FIX-*/FIX.md` with the required sections.
- [x] AC6: Normal triage requires the specified classification, impact, authority, and context fields.
- [x] AC7: Related work and repository/external links are recorded without mutating completed work.
- [x] AC8: Closeout requires delivered scope/disposition, verification, regression, original-AC results where applicable, residual risk, and decision.
- [x] AC9: Hotfix acceleration requires the minimum emergency safety packet and retains closeout evidence.
- [x] AC10: Oversized Fixes promote traceably to tasks/epics without rewriting the Fix.
- [x] AC11: Workspace mode reuses component identities and records repository-specific delivery/evidence links.
- [x] AC12: Kind-aware lifecycle and doctor validation enforce valid states, evidence, and local references.
- [x] AC13: Packaged/generated CLI, agent guidance, templates, and documentation remain synchronized.
- [x] AC14: Automated coverage proves behavior, failure paths, shared-registry use, and init-refresh parity.
- [x] AC15: Retro is optional unless the Fix reveals a reusable process/prevention gap.
- [x] AC16: Global `TRACKER.md` remains the only authoritative execution registry; no Fix index/tree is created.
- [x] AC17: Fix triage replaces full task approval/planning gates, with promotion when the boundary is exceeded.
- [x] AC18: Standalone requirements approval validates requirements/ACs without requiring an implementation plan.
- [x] AC19: Requirements approval precedes planning; Planner and post-plan Clarify run autonomously unless material or explicitly risk-gated review is needed.
- [x] AC20: In-envelope plan changes preserve approval; material envelope changes stale the requirements identity and require focused reapproval.
- [x] AC21: `task ready` joins current approval, resolved questions, complete AC-mapped planning, validation, and clarification consistency.
- [x] AC22: New work uses `Ready` after the gate while legacy `Plan Confirmed` remains compatible.
- [x] AC23: Approved delivery work continues autonomously inside scope but stops at bounded authority, material drift, or final completion checkpoints.
- [x] AC24: Epic parent requirements/AC/decomposition-boundary approval, agent-derived contracts/child plans, and Fix triage follow the same proportionate authority model.
- [x] AC25: Agent-owned natural-language routing distinguishes active corrections, bounded baseline Fixes, Tasks, and Epics from evidence; clear cases proceed, material ambiguity asks once, and missing historical task identity does not block a justified Fix.
- [x] AC26: Fresh and legacy-repository packaged `project init`/UVX upgrade paths install and safely refresh all Fix and authority-flow CLI, templates, generated guidance, and managed instructions idempotently.

## Validation

- AC1, AC7: Compare the completed source task/epic status and artifact hashes before and after a linked Fix lifecycle.
- AC2, AC15, AC17: Inspect and fixture-test generated guidance for routing, lightweight triage, promotion, and conditional retro behavior.
- AC3, AC5, AC16: Run Fix scaffolding fixtures and assert one global tracker row plus one `tasks/FIX-*/FIX.md`, with no Fix index or top-level Fix tree.
- AC4, AC6: Exercise all classifications, Hotfix mode, valid triage, and missing/invalid triage fields.
- AC8, AC9, AC12: Exercise normal and hotfix status/closeout transitions with passing and failing evidence records.
- AC10: Promote a Fix to task and epic fixtures and verify reciprocal immutable links and terminal disposition.
- AC11: Exercise single-repository defaults and workspace component/repository matrices.
- AC13, AC14: Run focused tests, help smoke tests, generated/local parity checks, init twice, init-refresh fixtures, full test suite, and strict doctor.
- AC18, AC20: Approve complete requirements with a missing/placeholder plan, then prove only requirements-envelope changes stale the identity.
- AC19: Prove planning is blocked before approval and Planner/Clarify proceed after approval without generic human plan confirmation.
- AC21, AC22: Exercise readiness failures/success, new `Ready` transitions, and legacy `Plan Confirmed` compatibility.
- AC23: Exercise autonomous continuation and stop conditions for bounded/setup-only scope, material drift, exceptional authority, optional plan review, and final completion.
- AC24: Exercise epic parent approval, agent-derived contract/child planning, material amendment return, and Fix triage as proportional authority variants.
- AC25: Exercise natural-language labels versus evidence, active/completed/new/discovery/multi-item/multi-workstream routing, clear automatic decisions, ambiguous owner questions, and unidentified originating work with recorded baseline proof.
- AC26: Run local packaged/UVX-equivalent fresh-init and legacy-refresh fixtures twice; assert Fix commands/templates/guidance, managed-block refresh, generated markers, `*.new` preservation, and source/generated parity.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Shared Fix Work-Item Scaffold | Add reserved `FIX-###` allocation, one `tasks/FIX-*/FIX.md` template, and one global-tracker row using shared work-item helpers without a Fix registry/tree. | AC3, AC5, AC16: `fix init` creates only the approved identity, artifact, and shared tracker state. | Run scaffold fixtures; inspect paths and tracker diff; assert absent `.project-workflow/FIXES.md` and `.project-workflow/fixes/`. | Complete |
| 2 | Classification, Triage, And Lifecycle | Add Fix classification/Hotfix mode, required triage fields, existing-vocabulary transitions, non-success dispositions, and the minimum hotfix safety gate. | AC2, AC4, AC6, AC9, AC12, AC17: kind-aware commands accept valid flows and reject missing authority/risk or illegal transitions. | Run table-driven normal, blocked, N/A, and hotfix lifecycle fixtures plus CLI help smoke tests. | Complete |
| 3 | Related Work, Promotion, And Historical Integrity | Link originating/related work, preserve completed artifacts/status, and promote oversized Fixes to a task/epic with reciprocal traceability. | AC1, AC2, AC7, AC10, AC17: completed history stays unchanged and promotion preserves both records. | Hash completed fixture artifacts before/after; run task/epic promotion fixtures and inspect links/dispositions. | Complete |
| 4 | Verification, Regression, And Closeout Gates | Require delivered outcome/disposition, verification, adjacent regression checks, original AC results where applicable, residual risk, and explicit closeout; route reusable gaps to optional retro/follow-up. | AC8, AC9, AC12, AC15: `fix close` blocks incomplete proof and completes proportionate valid evidence without mandatory retro boilerplate. | Run passing/failing closeout fixtures, including not-applicable evidence reasons and repeatable-process-gap guidance. | Complete |
| 5 | Workspace-Aware Fix Metadata | Reuse configured workspace components and single-repo defaults for primary repo, repos touched, branches, PRs, deployments, and evidence links. | AC11, AC12: workspace Fixes require valid component/repository metadata while single-repo Fixes remain concise. | Run single-repo and multi-repo fixtures with valid, missing, and inconsistent component references. | Complete |
| 6 | Generated Assets, Documentation, And Regression Suite | Synchronize packaged/local CLI, templates, agent skills/prompts/rules, README/CLI docs, canonical UVX-equivalent fresh install and legacy refresh behavior, doctor, and focused/full regression coverage. | AC2, AC3, AC4, AC5, AC6, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC17, AC26: installed, upgraded, generated, and source behavior remain aligned and all supported/failure paths are covered. | Run focused tests, packaged/UVX-equivalent fresh init, legacy refresh, CLI help smoke tests, init twice, managed-block/`*.new` preservation checks, parity checks, full suite, and `doctor --strict`. | Complete |
| 7 | Requirements Authority And Autonomous Phase Handoff | Make standalone requirements approval plan-independent, require approval before planning, run Planner/Clarify autonomously inside the envelope, gate readiness mechanically, adopt `Ready` for new work, preserve `Plan Confirmed`, and encode bounded stop/reapproval rules across task, epic, and Fix guidance. | AC18, AC19, AC20, AC21, AC22, AC23, AC24: approval timing, identity freshness, autonomous handoff, compatibility, and proportional authority are enforced and documented. | Run standalone task approval/readiness/status fixtures, legacy compatibility tests, autonomous/stop-condition guidance checks, and epic/Fix authority regression cases. | Complete |
| 8 | Agent-Owned Intake And Work-Item Routing | Add guidance and tests that route natural-language requests from workflow state, baseline evidence, boundedness, decision/discovery needs, and coordinated work-item count; record rationale, avoid exhaustive archaeology, and ask only on material ambiguity. | AC2, AC4, AC10, AC17, AC25: active corrections stay in scope, bounded baseline corrections become Fixes, larger work promotes, and user jargon never substitutes for evidence. | Run routing fixtures covering explicit/misleading labels, clear and ambiguous cases, legacy baselines, Tasks, Fixes, and Epics. | Complete |

## Implementation Evidence

- Shared Fix model: `FIX-###`/unique IDs, one `tasks/FIX-*/FIX.md`, one global tracker row, and no second registry/tree are covered by executable fixtures.
- Lifecycle: normal triage, Hotfix safety bypass, Blocked/N/A rules, all classifications, non-delivery dispositions, verification gates, and closeout are covered by CLI fixtures.
- Traceability: linked completed-task bytes/status remain unchanged; task and epic promotion preserve reciprocal source links and terminal Fix disposition.
- Workspace: configured component IDs/paths and per-repository branch/PR/evidence rows are validated, with `.` remaining the concise single-repo default.
- Authority: requirements approval succeeds with a placeholder plan, `Analysing` is approval-gated, new work uses `Ready`, and legacy `Plan Confirmed` remains tested.
- Distribution: local UVX installs and refreshes prove Fix CLI/skills/managed guidance delivery, marked-file refresh, managed-block replacement, `*.new` preservation, and repeat-run idempotence.
- Validation commands: `.venv/bin/pytest -q`, `.venv/bin/python -m project_workflow.cli doctor --strict`, CLI/template SHA-256 parity, and prompt mirror parity.

## QA & Code Review

- Date: 2026-07-20
- Reviewed areas: Fix identity/scaffolding, classification and lifecycle gates,
  closeout and promotion, historical integrity, workspace metadata, task
  authority/readiness changes, generated assets, Codex installation, tests, and
  documentation.
- AC1-AC12 and AC15-AC17 evidence: executable lifecycle, classification,
  hotfix, promotion, completed-history hash, workspace, closeout, doctor, and
  single-registry fixtures in `tests/test_doctor.py` passed.
- AC13-AC14 and AC26 evidence: canonical CLI, packaged template, and installed
  local CLI are byte-identical; prompt mirrors match; fresh local UVX install,
  legacy refresh, collision preservation, and idempotence fixtures passed.
- AC18-AC24 evidence: standalone approval without a populated plan,
  requirements hash freshness, readiness gating, `Ready` lifecycle,
  `Plan Confirmed` compatibility, and generated task/epic/Fix authority
  guidance fixtures passed.
- AC25 evidence: generated guidance consistently records evidence-backed
  active/Fix/Task/Epic routing, material ambiguity handling, and the
  no-archaeology fallback for unidentified originating work.
- Validation: `.venv/bin/pytest -q` passed 73/73 tests in 31.16 seconds;
  `./.project-workflow/cli/workflow doctor --strict` reported no issues;
  `git diff --check` passed.
- Findings: None.
- Deferred or owner-only validation: None.
- Verdict: Pass.

## Retro

- Date: 2026-07-20
- Reusable lessons: model a lightweight workflow as a subtype on shared ID,
  tracker, lifecycle, and validation infrastructure unless separate ownership or
  scale provides evidence for another registry; route work from baseline,
  boundedness, decisions, and workstream count rather than accepting user labels
  as authoritative; keep owner approval at the requirements/AC envelope and use
  machine readiness for autonomous downstream phases.
- Conventions or agent assets updated: packaged and installed Codex `AGENTS.md`
  and `project-*` skills, GitHub prompts, Cursor rules, CLI templates, README,
  and strict doctor/init-refresh coverage now encode these conventions.
- Follow-up tasks: None identified.
- Missed in-scope work: None.

## Notes

- Task: TASK-038
- Title: Lightweight Fix And Defect Workflow
- Created: 2026-07-20
