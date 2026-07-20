# Requirements

## Summary

- Task: TASK-038
- Title: Lightweight Fix And Defect Workflow
- Last updated: 2026-07-20
- Source discussion: Codex thread `019f49d9-eb5d-7dd3-a877-79f1ddc80b75`

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: No
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: Owner
- Approval date: 2026-07-20
- Approval note / source: Owner approved AC1-AC26 and authorized implementation in Codex task 019f7d25-b271-77d3-a05d-3e19cf0cf846 on 2026-07-20, including agent-owned routing and canonical UVX upgrade coverage
- Approved artifact identity: sha256:4fe37f431c15e05e12d4580d9c7cc1b912c5a2c48481bc523cbc927e1e71f702

## Goal

Add a lightweight, first-class Fix workflow for defects, regressions, bounded
change requests, and incidents discovered after related work is complete. The
workflow must preserve the historical accuracy of completed tasks while making
corrective work easy to triage, trace, verify, and close without imposing the
full task or epic artifact set.

## Non-Goals

- Reopening, rewriting, or retroactively expanding completed task or epic scope
  by default.
- Moving corrections discovered while a task is still active out of that task.
- Replacing a full task or epic when corrective work is large, exploratory, or
  materially changes product scope.
- Replacing external incident-management, on-call, release-management, or
  service-management systems.
- Delivering full multi-repository orchestration in this task; this task only
  needs a metadata model that can represent multi-repository/workspace work in
  the future.
- Implementing any individual product defect as part of this workflow task.
- Removing the owner from product outcomes, scope, acceptance criteria, material
  risk decisions, amendments, or final completion authority.
- Requiring the owner to manually invoke or generically approve Planner,
  Clarify, Ready, or each implementation work item when work remains inside a
  current approved scope envelope.
- Treating a plan, an implementation request, agent silence, or agent confidence
  as a substitute for explicit owner approval of requirements and ACs.

## Users & Context

- Maintainers and coding agents need a low-overhead path for corrective work
  discovered after a task or epic reached `Complete`.
- Owners and reviewers need completed records to remain trustworthy historical
  statements while still being able to follow later corrective work.
- Operators may need an expedited incident or hotfix path, but urgency must not
  erase risk, verification, regression, or closeout evidence.
- Teams may eventually apply one Fix across a workspace containing multiple
  repositories, branches, pull requests, deployments, and evidence sources.
- Owners need one high-leverage checkpoint before implementation mechanics can
  anchor the solution, without being asked to operate every downstream workflow
  phase manually.
- Agents need an unambiguous authority handoff: requirements define the approved
  outcome boundary; planning and clarification derive and verify how to deliver
  inside it; readiness mechanically proves that derivation before coding.

## User Story

As a project-workflow maintainer, I want post-completion corrective work to use
a lightweight, linked Fix record, so completed tasks remain historically
accurate while defects, regressions, bounded changes, and incidents can be
triaged, delivered, verified, and closed with proportionate evidence.

## Requirements (Outcome-Focused)

- Preserve completed task and epic records as historical truth. A Fix may link
  to completed work, but creating or progressing the Fix must not edit the
  completed item's approved scope, evidence, or `Complete` status by default.
- Keep corrections inside an active task or epic when they are discovered
  before that work completes and remain within its approved scope envelope.
- Provide a first-class Fix record for corrective work discovered after
  completion, rather than treating it as an untyped backlog row or requiring a
  full task scaffold in every case.
- Give Fixes reserved `FIX-###` identities so the work-item kind remains
  unambiguous without adding a new tracker column or a second registry. Expose a
  supported CLI surface centered on `fix init`, `fix triage`, `fix status`, and
  `fix close`, implemented on the shared work-item infrastructure.
- Classify each Fix so readers can distinguish:
  - **Defect:** delivered behavior does not meet the applicable expected or
    approved behavior.
  - **Regression:** behavior that previously worked or was verified no longer
    works after a later change.
  - **Change request:** a bounded change to previously accepted behavior rather
    than a failure to meet it.
  - **Incident:** active or recent operational impact requiring coordinated or
    time-sensitive response. A **hotfix** is an expedited delivery mode for an
    incident or high-urgency Fix, not a substitute for the underlying type.
- Make intake agent-operated rather than dependent on user workflow jargon. The
  user may call work a bug, Fix, task, feature, or simply describe the desired
  correction; that label is evidence but is not authoritative routing. The agent
  must apply and briefly record this evidence-backed gateway before scaffolding:
  - an in-scope correction to active work remains in the active task/epic;
  - a bounded correction against an existing delivered or accepted baseline is
    a Fix, including bounded Defect, Regression, Change Request, or Incident
    work;
  - a new outcome, substantial discovery, material unresolved product or
    architecture decision, or multiple independently planned work items is a
    Task;
  - multiple coordinated outcomes/workstreams require an Epic.
- For clear routing, let the agent state the rationale concisely and proceed
  when the user has authorized execution. Ask the owner one focused question
  only when the boundary is genuinely ambiguous or materially changes scope or
  authority. If an explicit user label conflicts with evidence, explain and
  recommend the better route rather than silently obeying or overriding it.
- Link originating work when it can be identified proportionately, but do not
  require exhaustive historical archaeology before creating a Fix. When no
  originating workflow record can be identified, record `Related Work: Not
  identified` plus the delivered/accepted baseline and evidence supporting the
  Fix classification.
- Keep the default Fix artifact set materially lighter than the task/epic flow,
  using one canonical `FIX.md` record rather than separate requirements and
  implementation documents. The recommended artifact lives at
  `.project-workflow/tasks/FIX-<NNN>-<Suffix>/FIX.md` and contains `Report`,
  `Classification`, `Related Work`, `Risk`, `Fix Plan`, `Verification`, and
  `Outcome` sections.
- Capture enough intake and triage context to decide what should happen next,
  including the observed issue, expected behavior or requested outcome,
  affected users/systems, classification, `Low`/`Medium`/`High`/`Critical`
  severity, impact, urgency, risk, owner, current state, and supporting
  screenshot/log/link evidence when available.
- Keep Fixes in the existing global `.project-workflow/TRACKER.md` and reuse the
  existing status vocabulary through the lightweight lifecycle `To Do` ->
  `Ready` -> `In Progress` -> `Testing` -> `Review` -> `Complete`. `fix triage`
  is the gate from `To Do` to `Ready`; `Testing` owns verification/regression
  evidence; `Complete` means verified and closed. `Blocked` remains available,
  while duplicate, rejected, deferred, and promoted Fixes end as `N/A` with an
  explicit disposition and reason.
- Link a Fix to applicable originating and related work without changing that
  work. Links must support task/epic IDs where relevant and allow references to
  issues, incidents, releases, commits, branches, pull requests, deployments,
  and evidence.
- Capture delivery and proof proportionately, including reproduction or
  diagnostic evidence when applicable, a narrow Fix plan, the delivered scope,
  verification results, adjacent-behavior regression evidence, confirmation
  that linked original ACs still pass where applicable, known residual risk,
  and a closeout decision.
- Support an expedited incident/hotfix route without allowing urgency alone to
  bypass risk classification, related-work traceability, verification,
  regression evidence, or explicit closeout. An expedited Fix may move from
  `To Do` directly to `In Progress` only after recording the incident,
  severity/impact, accountable authority, affected target, rollback or
  containment approach, and verification plan.
- Define a clear escalation or promotion boundary so work that is no longer
  lightweight can move to a normal task or epic while retaining links to the
  original Fix and completed work.
- Make the record forward-compatible with multi-repository/workspace use by
  supporting at least a primary repository, repositories touched, and
  per-repository branch/PR/evidence links. These fields are required in
  workspace mode and may remain concise or implicit where a single-repository
  installation supplies an unambiguous default. Reuse workspace component
  identities and repository defaults when workspace mode is configured rather
  than creating a second conflicting repository model.
- Do not require a retro for every Fix. Require or recommend one only when the
  Fix exposes a repeatable workflow, process, quality, or prevention gap worth
  turning into durable guidance or follow-up work.
- Preserve requirements and acceptance criteria as the default human authority
  checkpoint for standalone tasks. `task approve-requirements` must validate
  only a complete, internally consistent `REQUIREMENTS.md` and must not require
  a populated `IMPLEMENTATION.md` before it can record approval.
- Require owner approval before standalone task planning begins. The approved
  artifact identity remains derived only from `REQUIREMENTS.md`, so later plan
  edits inside the approved outcome/AC envelope do not create approval fatigue.
- After approval, let the agent run Planner and post-plan Clarify autonomously.
  Planner must create complete AC coverage and validation obligations; Clarify
  must reconcile the plan with requirements, repository constraints, and proof
  obligations without asking for generic plan confirmation.
- Treat post-plan clarification as two different outcomes:
  - plan-only corrections inside the approved envelope are agent-owned and do
    not require owner reapproval;
  - material changes to requirements, ACs, scope, artifact identity,
    source-of-truth interpretation, proof obligations, or risk authority make
    the approval stale and return to the owner for a focused decision.
- Make `task ready` the combined machine checkpoint after planning and
  clarification. It must require a current requirements approval, no unresolved
  questions, complete AC-to-plan coverage, testable validation, and no material
  requirements/plan conflict.
- Use `Ready` for newly prepared standalone tasks once `task ready` passes;
  retain `Plan Confirmed` only as a backwards-compatible legacy status/alias so
  existing repositories do not require immediate tracker migration.
- When the originating owner request authorizes delivery, let implementation
  begin automatically after readiness without another generic “now implement”
  prompt. Setup-only, discussion-only, requirements-only, or explicitly paused
  requests remain stopped at their requested boundary.
- Keep the owner in the loop for material envelope changes, non-routine external
  or destructive authority, explicitly requested/high-risk plan review, and
  final completion/product acceptance. Plan review is optional by default and
  may be required explicitly in the approved requirements for unusually risky
  work.
- Keep epic behavior aligned with the same authority model: owner approval is at
  parent requirements/ACs and the proposed decomposition boundary; the agent
  derives the epic contract and child plans inside that envelope. Amendments or
  contract/decomposition changes that materially alter scope, source-of-truth,
  artifact, proof, risk, or ownership decisions return to the owner. Fix triage
  remains the proportionate equivalent for lightweight Fix work.
- Expose the workflow consistently through supported repository interfaces,
  generated agent guidance, user-facing documentation, and validation so
  initialized repositories do not drift from packaged behavior.
- Ship every approved Fix and authority-flow change through the packaged
  `project init` refresh path used by the canonical UVX upgrade command:
  `uvx --from git+https://github.com/johndetlefs/project-workflow.git project
  init`. Fresh installs and older initialized repositories must receive the new
  local CLI commands, templates, agent skills/prompts/rules, and managed
  guidance while preserving unmarked host-owned files through the established
  managed-block and `*.new` collision behavior.

## Acceptance Criteria (Verifiable)

- AC1: Creating or progressing a post-completion Fix leaves the related
  completed task/epic status, approved scope, and historical evidence unchanged
  by default, while the Fix links back to that work.
- AC2: Workflow guidance states that an in-scope correction discovered before
  completion remains within the active task/epic, while qualifying corrective
  work discovered after completion uses a Fix record.
- AC3: The supported CLI exposes `fix init`, `fix triage`, `fix status`, and
  `fix close`; `fix init` allocates the next reserved `FIX-###` identity, writes
  one Fix folder under `.project-workflow/tasks/`, adds one row to the existing
  global tracker, and does not scaffold the full task/epic requirements and
  implementation artifact set.
- AC4: The Fix record requires one underlying classification from Defect,
  Regression, Change Request, or Incident, and represents Hotfix separately as
  an expedited delivery mode so the terms are not conflated.
- AC5: The default artifact is one
  `.project-workflow/tasks/FIX-<NNN>-<Suffix>/FIX.md` record with `Report`,
  `Classification`, `Related Work`, `Risk`, `Fix Plan`, `Verification`, and
  `Outcome` sections; normal Fix use does not require a task-style
  `REQUIREMENTS.md` plus `IMPLEMENTATION.md` pair.
- AC6: Triage cannot be considered complete without the observed issue or
  requested outcome, expected behavior where applicable, affected user/system,
  classification, `Low`/`Medium`/`High`/`Critical` severity, impact, urgency,
  risk, owner, disposition, and supporting screenshot/log/link evidence when
  available.
- AC7: A Fix can record originating/related task or epic IDs and external or
  repository-native links without altering the related completed artifacts.
- AC8: A Fix cannot close through the supported workflow unless it records the
  delivered scope or disposition, verification result, adjacent behavior
  checked, linked original AC results where applicable, regression evidence (or
  an explicit reason it is not applicable), residual risk, and closeout
  decision.
- AC9: Incident/hotfix handling may shorten elapsed workflow time but does not
  remove required risk, traceability, verification/regression, and closeout
  evidence. A direct `To Do` -> `In Progress` transition is allowed only when
  the incident, severity/impact, accountable authority, affected target,
  rollback/containment approach, and verification plan are already recorded.
- AC10: The workflow provides a traceable way to promote or supersede a Fix with
  a full task/epic when the lightweight boundary is exceeded, without deleting
  or rewriting the original Fix.
- AC11: In workspace mode a Fix requires a primary repository, all repositories
  touched, and repository-specific branch, pull-request, and evidence links;
  single-repository use remains concise by using unambiguous repository
  defaults. Configured workspace component identities are reused as the source
  of truth rather than duplicated in a Fix-specific repository schema.
- AC12: Workflow validation reports malformed Fix records, invalid
  classifications or lifecycle states, missing required closeout evidence, and
  broken or inconsistent related-work references that can be checked locally.
  The supported success lifecycle is `To Do` -> `Ready` -> `In Progress` ->
  `Testing` -> `Review` -> `Complete`; `Blocked` and terminal `N/A`
  dispositions remain explicit and auditable.
- AC13: Packaged and generated workflow assets, local and packaged CLI behavior,
  agent guidance, and user-facing documentation remain synchronized for the new
  Fix workflow.
- AC14: Automated tests cover creation, classification, active-versus-complete
  routing guidance, completed-history preservation, hotfix evidence gates,
  promotion/escalation, multi-repository metadata, closeout, validation
  failures, one-registry behavior, absence of a separate Fix index, and
  init-refresh parity.
- AC15: Fix closeout does not require a retro by default, but guidance directs
  repeatable workflow/process/quality/prevention gaps into a retro or explicit
  follow-up without reopening the completed originating work.
- AC16: Fixes, standalone tasks, and epics share the existing global tracker as
  the single source of committed execution state. The workflow does not create
  `.project-workflow/FIXES.md`, a second authoritative Fix tracker, or a
  `.project-workflow/fixes/` artifact tree.
- AC17: Fix triage is the lightweight scope-and-authority gate. Normal Fixes do
  not require task-style requirements approval, decomposition, or an
  AC-mapped implementation plan; when a Fix exceeds that boundary it is
  promoted rather than expanded in place.
- AC18: `task approve-requirements` records an owner-approved standalone-task
  scope envelope after validating `REQUIREMENTS.md` completeness, stable ACs,
  resolved/accepted open questions, and approval source; it does not require a
  populated or ready `IMPLEMENTATION.md`.
- AC19: Standalone task planning cannot begin before a current requirements/AC
  approval exists. After approval, Planner and post-plan Clarify run without
  mandatory owner plan confirmation unless the requirements explicitly require
  plan review or a material decision is discovered.
- AC20: Plan and clarification edits that remain inside the approved
  requirements/AC envelope do not stale approval. Any material requirements,
  AC, scope, artifact identity, source-of-truth, proof-obligation, or risk
  authority change does stale the requirements hash and blocks readiness until
  focused owner reapproval is recorded.
- AC21: `task ready` passes only when requirements approval is current, open
  questions are resolved/accepted, every AC is covered by independently
  testable plan work, validation is specified, and no material requirements-plan
  conflict remains. New tasks move to `Ready` only after this gate passes.
- AC22: New standalone task guidance and transitions use `Ready` instead of
  requiring human `Plan Confirmed`; legacy `Plan Confirmed` rows and commands
  remain supported without forcing repository migration.
- AC23: When the originating request authorizes delivery, an agent may proceed
  from Ready through implementation and QA without repeated generic approvals.
  It must stop for material envelope changes, required external/destructive
  authority, explicitly required plan review, or final completion/product
  acceptance; bounded or setup-only requests do not gain broader authority.
- AC24: Epic guidance keeps one owner checkpoint at parent requirements/ACs and
  the proposed decomposition boundary. The agent derives contracts and child
  plans inside that envelope; amendments or material contract/decomposition
  drift return to the owner. Fix triage remains the lightweight authority gate.
- AC25: Natural-language intake does not require the user to name a workflow
  kind. The agent records a concise evidence-backed routing rationale using
  active-vs-completed state, existing delivered/accepted baseline, boundedness,
  discovery/material-decision needs, and number of coordinated work items. Clear
  cases route automatically when execution is authorized; ambiguous/material
  cases ask one focused owner question. A user label is non-binding, and an
  unidentifiable originating task does not block a Fix when the baseline and
  evidence are recorded proportionately.
- AC26: A fresh install and an upgrade of an older initialized repository through
  the packaged `project init` path used by the canonical UVX command install or
  refresh all Fix CLI behavior, `FIX.md` templates, task/epic/Fix authority and
  routing guidance, skills/prompts/rules, and managed host instructions. The
  upgrade remains idempotent, refreshes marked generated files, updates managed
  blocks, and preserves unmarked host-owned files via `*.new` without requiring
  manual copying from the project-workflow source repository.

## Open Questions (Answer Needed)

- None. The owner resolved Q1-Q5 in the task discussion on 2026-07-20 by
  accepting the considered one-registry, lightweight-task-subtype model and its
  associated lifecycle, promotion boundary, and hotfix safety gate. The owner
  also resolved the human-checkpoint model in the same task discussion:
  requirements/AC approval remains the default human authority boundary;
  Planner, post-plan Clarify, and readiness become autonomous downstream gates;
  material drift and final completion return to the owner.

## Decisions (Resolved)

- Completed tasks and epics remain historically accurate and are not edited or
  reopened by default for later corrective work.
- In-flight, in-scope corrections stay inside the active task or epic.
- Post-completion defects, regressions, bounded change requests, and incidents
  receive lightweight first-class Fix records.
- A Fix is a lightweight work-item/task subtype, not a parallel workflow
  registry. Fixes use reserved `FIX-###` identities, live under
  `.project-workflow/tasks/`, and share `.project-workflow/TRACKER.md` with tasks
  and epics.
- The workflow will not add `.project-workflow/FIXES.md` or
  `.project-workflow/fixes/`. A Fix-specific view may be considered later only
  if actual usage proves materially different operational requirements; any
  such view should be derived rather than a second source of truth.
- Fix artifacts use one canonical `FIX.md`; no task-style `REQUIREMENTS.md` plus
  `IMPLEMENTATION.md` pair or formal task approval/decomposition gate is
  required for normal Fixes.
- The agent owns initial Task/Fix/Epic routing from natural-language intake. It
  uses workflow state, baseline evidence, boundedness, discovery/material
  decisions, and work-item coordination—not the user's choice of jargon—as the
  gateway. Clear cases proceed with a stated rationale; ambiguous/material
  cases return one focused question to the owner.
- A related task/epic link is desirable but not mandatory. When proportional
  search cannot identify one, the Fix records `Related Work: Not identified`
  and the baseline/evidence that justifies corrective classification.
- The Fix lifecycle reuses `To Do`, `Ready`, `In Progress`, `Testing`, `Review`,
  `Complete`, `Blocked`, and `N/A`, with kind-aware transition/evidence rules.
- `fix init`, `fix triage`, `fix status`, and `fix close` are a purpose-specific
  user interface over shared ID, tracker, status, doctor, and workspace
  infrastructure rather than a separate state system.
- Only bounded corrective changes with understood scope and proof remain
  Change Request Fixes. Discovery, material product-scope changes, and
  multi-work-item delivery are promoted to a task/epic without rewriting the
  original Fix.
- Hotfix delivery may start before normal triage completes only after the
  minimum incident authority, risk, target, rollback/containment, and
  verification information is recorded; full evidence remains mandatory before
  `Complete`.
- Requirements and AC approval is the standard high-leverage human checkpoint
  for standalone tasks and occurs before planning. Approval hashes only
  `REQUIREMENTS.md`; implementation planning is derived context, not owner
  authority.
- Planner and post-plan Clarify proceed autonomously after approval. The owner
  reviews a plan only when explicitly requested/required by risk or when the
  agent discovers a material decision outside the envelope.
- `task ready` is the machine gate that joins current approval, complete plan
  coverage, validation, and clarification consistency. Newly ready work uses
  `Ready`; `Plan Confirmed` remains a legacy-compatible status rather than a
  mandatory human checkpoint.
- An approved delivery request authorizes autonomous progress inside the
  unchanged envelope; it does not authorize material scope change, destructive
  or external actions outside normal permissions, or final completion without
  the owner.
- Epic parent requirements/AC/decomposition-boundary approval and Fix triage are
  proportionate forms of the same authority model. Agent-derived contracts,
  approved epic children, and normal Fix execution do not add repetitive owner
  checkpoints unless they materially alter the envelope.
- Canonical UVX installation/upgrade is a required delivery surface. Source-only
  behavior is incomplete until packaged `project init` refreshes existing
  consumers safely and fresh installs contain the same Fix and authority model.
- Triage, risk classification, related-work links, verification/regression
  evidence, and closeout are required capabilities.
- The metadata model must leave room for future multi-repository/workspace use.
- Requirements and acceptance criteria remain unapproved until the owner
  explicitly reviews and confirms this draft.

## Validation Plan

- Run focused CLI/unit fixtures for Fix creation, unique ID allocation,
  classification, lifecycle transitions, promotion, evidence gates, and invalid
  records (AC3-AC12, AC14).
- Create a completed task fixture, link a new Fix, progress and close the Fix,
  and prove the completed task's tracked status and approved artifacts are byte
  unchanged (AC1, AC7, AC14).
- Exercise active-task and completed-task scenarios against generated guidance
  and command/help text to verify the routing distinction (AC2, AC14).
- Exercise `fix init`, `fix triage`, `fix status`, and `fix close` across every
  supported transition and non-success disposition (AC3, AC12, AC14).
- Exercise Defect, Regression, Change Request, Incident, and Incident+Hotfix
  examples and assert the taxonomy remains unambiguous (AC4, AC9, AC14).
- Inspect a generated Fix to confirm one canonical artifact contains all
  required triage, links, delivery, verification/regression, risk, and closeout
  fields without creating task-style paired documents (AC5-AC8).
- Exercise single-repository and multi-repository records, including per-repo
  branch, pull-request, and evidence links (AC11, AC14).
- Prove Fix creation and every lifecycle transition update only the existing
  global tracker, store artifacts only under `.project-workflow/tasks/`, and do
  not create a Fix index or Fix artifact tree (AC3, AC14, AC16).
- Prove normal Fix triage/closeout does not invoke task requirements approval or
  implementation-plan readiness gates, while promotion creates and links the
  appropriate full task/epic record (AC10, AC17).
- Run init-refresh fixtures and parity checks across packaged/local CLI,
  templates, agent assets, and documentation (AC13, AC14).
- Verify normal closeout does not require retro content, while a repeatable
  process-gap fixture routes to retro/follow-up guidance (AC15).
- Exercise `task approve-requirements` with complete requirements and a
  placeholder/missing plan; prove approval succeeds and the identity changes
  only when the requirements envelope changes (AC18, AC20).
- Prove planning is blocked before approval, then run Planner and Clarify after
  approval without owner-plan-confirmation text or gates (AC19, AC20).
- Exercise task readiness failures for stale approval, unresolved questions,
  unmapped ACs, placeholders, missing validation, and material requirements-plan
  conflict; prove a valid plan moves through `Ready` (AC21, AC22).
- Exercise legacy `Plan Confirmed` compatibility alongside new `Ready`
  transitions and generated guidance (AC22).
- Exercise autonomous continuation for an approved delivery request and stop
  conditions for setup-only scope, material drift, required external/destructive
  authority, optional high-risk plan review, and final completion (AC23).
- Exercise epic parent approval/child autonomy/amendment behavior and Fix triage
  as proportional variants of the same authority model (AC24).
- Exercise natural-language requests whose user labels agree and disagree with
  evidence; active-task, completed-baseline, new-outcome, discovery, multi-item,
  and multi-workstream cases; clear automatic routing and ambiguous one-question
  routing; and a legacy baseline with no identifiable originating task (AC25).
- Build/install the package locally through a UVX-equivalent packaged execution
  path, initialize a fresh fixture, and refresh a legacy initialized fixture.
  Assert new Fix commands/templates/guidance are present, marked generated files
  and managed blocks update, unmarked files produce reviewable `*.new` output,
  a second refresh is idempotent, and local/generated behavior matches source
  behavior (AC13, AC14, AC26).
- Run the full repository test suite plus `workflow doctor --strict` after
  implementation. No specialized visual, external-contract, deployed-artifact,
  or runtime-target proof recipe is triggered by this requirements draft.
