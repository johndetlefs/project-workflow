# Requirements

## Summary

- Task: EPIC-006
- Title: Epic Control Gates For Requirement Drift Prevention
- Last updated: 2026-07-09
- Status: Approved for decomposition
- Clarification status: Second clarification pass accepted by owner on 2026-07-09; requirements and ACs approved for decomposition.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-09
- Approval note / source: Owner approved EPIC-006 requirements and authority envelope in Codex thread on 2026-07-09
- Approved artifact identity: sha256:8aed49b7b59254ee33b09710f157fc88a392907b91a7a1f1efdd7b2479560053

## Goal

Add a small, enforceable epic-control layer to project-workflow so long-running epics and their child tasks cannot drift from owner-approved requirements, controlling sources of truth, artifact identity, or valid evidence.

The workflow must block common model failure modes: starting work before requirements are confirmed, child tasks self-certifying parent acceptance criteria, implementation drifting from the stated source of truth, quality review against code rather than the delivered user-facing artifact, proof against the wrong artifact or environment, reactive fixes without explicit scope control, and closeout summaries that contradict the actual evidence.

The triggering Knowledge Graph widget epic is a regression example, not a domain-specific requirement. The solution must generalize to any project-workflow epic or task where the owner says "build something that matches this," "verify this deployed/runtime behavior," or "prove this exact target/source path."

The solution must stay enforcement-first and avoid creating a large passive documentation system. The value must come from lifecycle gates, structured evidence, proof recipes, doctor failures, drift detection, and bounded owner authority, not from extra prose or repeated approval prompts.

The primary success condition is that a model cannot advance a task or epic by satisfying the shape of workflow artifacts while still proving the wrong thing. The gates must make invalid substitutes explicit and reject them at the lifecycle transition where they would otherwise become misleading status.

The workflow must not shift the burden of drift prevention onto the owner. Owner approval confirms the requirements and authority envelope; after that, the workflow should mechanically detect whether work remains inside that envelope. Repeated "approve this too" prompts are a failure mode because they create approval fatigue and make blind approval more likely.

## Non-Goals

- Do not add broad bureaucracy to ordinary standalone tasks that are not crossing gated lifecycle points.
- Do not require every small task to use epic contracts, proof recipes, or evidence JSON.
- Do not make doctor rely only on file presence when the real risk is stale, contradictory, or invalid evidence.
- Do not trust inferred legacy evidence as closeout proof without an explicit refresh.
- Do not solve visual diffing, browser automation, or deployment verification perfectly in this epic; define enforceable recipes and minimal structured evidence first.
- Do not remove existing project-workflow Markdown usability. Human-readable docs remain, but structured evidence is the source of truth for gates.
- Do not hard-code ChatGPT, MCP, widget, playground, or deployment-provider concepts into the core model. Use those only as examples or regression fixtures for general proof recipes.
- Do not solve drift by making the owner approve every child task, lifecycle transition, or ordinary implementation step.
- Do not use approval prompts as a substitute for mechanical drift detection, provenance checks, structured evidence, or doctor failures.

## Users & Context

- Project owners need agents to stop starting implementation before requirements and acceptance criteria have been reviewed and approved.
- Project owners need fewer, higher-quality approval moments, not repeated approval fatigue.
- Agents need mechanical gates that keep the controlling requirement, source of truth, and proof obligation active during long epics.
- Future epic child tasks need inherited constraints so each child executes a slice of the epic rather than becoming an independent interpretation of the goal.
- Review/closeout needs to trust structured proof from the correct proof owner, not generic task prose.
- Existing repositories may already contain open and closed epics/tasks without these controls, so adoption must be safe and explicit.

## Requirements (Outcome-Focused)

- Add an owner approval envelope to task and epic requirements. Work must not begin from unreviewed requirements, but once requirements, ACs, and decomposition authority are owner-approved, agents may scaffold and implement child work inside that envelope without asking for approval at every ordinary step. Fresh owner approval is required only when work crosses a material-change boundary. New work should use CLI approval commands; legacy/adopted work may preserve a manual approval block.
- Make drift detection the normal enforcement mechanism after approval. Gates should compare current work against the approved requirements, decomposition plan, source-of-truth constraints, artifact identity, proof obligations, and structured evidence before deciding whether work can advance.
- Require owner input only for material scope decisions: approving initial requirements/ACs, approving the decomposition authority envelope, accepting deviations, changing source-of-truth interpretation, changing artifact identity, changing proof obligations, adding/removing child work outside the plan, or closing with explicit deferrals.
- Make owner approvals freshness-bound. Approval records must identify the approved requirements/AC artifact and become stale when requirements, acceptance criteria, epic contracts, or approved decomposition plans materially change.
- Add a small epic contract for new epics. The contract must define sources of truth, invalid substitutes, invariants, proof owners for parent ACs, and artifact targets.
- Add a first-class decomposition plan for epics. The workflow must not rely on freeform parser output or agent-invented child rows as the controlling decomposition. A single owner-reviewed decomposition plan may authorize all matching child rows; per-row owner approval is not required for unchanged rows inside that approved plan. Rows outside the approved plan require an amendment.
- Add child charter inheritance for epic children. Scaffolded child tasks must inherit relevant parent ACs, invariants, invalid substitutes, proof recipes, and artifact identity constraints from the epic contract.
- Add structured evidence support. Gates and closeout must trust structured evidence over prose summaries.
- Add domain-general proof recipes for recurring high-risk evidence types: visual reference fidelity, external contract alignment, deployed/published artifact alignment, runtime target/source verification, and responsive/multi-context visual behavior.
- Add a pre-implementation calibration checkpoint for visual/reference-fidelity work. The checkpoint must name the reference artifact, delivered artifact, required states/viewports/contexts, known differences, invalid substitutes, and any owner-approved deviations before implementation begins.
- Add proof-recipe trigger rules. Requirements, ACs, task titles, epic contracts, and material claims that require visual/reference fidelity, runtime/deployment/source proof, external contract alignment, or multi-context behavior must select the corresponding proof recipe before Review or Complete. Agents must not be allowed to satisfy those claims with generic validation evidence.
- Add a structured claim-to-evidence ledger for material claims. Claims that can satisfy acceptance criteria must be declared in structured evidence; unsupported prose claims must not count toward closeout, and contradictory prose must fail doctor/status gates.
- Add proof ownership gates. Parent ACs can only be satisfied by assigned proof owners using valid structured evidence; implementation tasks must not self-certify visual, deploy, or browser verification ACs unless explicitly assigned as the proof owner.
- Add artifact identity gates. Visual/reference-fidelity claims must name both the reference artifact and the delivered user-facing artifact. Runtime/deployment/integration claims must name the execution target and the source/artifact under test. Evidence against a surrogate artifact or a related environment must not satisfy the claim.
- Add invalid-substitute enforcement. Each proof recipe must define evidence that is explicitly invalid for that recipe, and doctor/status/closeout must reject those substitutions rather than treating them as partial proof.
- Add controlled amendment flow for mid-epic defects, newly discovered work, scope changes, and owner-approved deviations. New child work or reactive fixes that affect parent ACs, source-of-truth interpretation, artifact identity, proof requirements, or child ownership must be tied to an amendment or an existing child owner.
- Add child-creation controls for epics. New epic child rows must come from decomposition or a recorded amendment; manually added child rows without provenance must warn in legacy epics and fail in new/adopted epics before approval, scaffold, Review, or Complete.
- Add drift audit checks after child completion or before the next gated epic transition. Drift checks must identify whether the child preserved the source of truth, introduced new behavior, used invalid substitute evidence, or requires an amendment.
- Add legacy adoption for pre-existing epics/tasks. Closed legacy work should not break, open legacy work should warn until a gated transition, and adopted inferred evidence must be marked untrusted until refreshed.
- Add doctor enforcement for missing approvals, missing/stale contracts, missing/stale child charters, invalid proof ownership, incomplete proof recipes, invalid substitute evidence, stale evidence after artifact changes, contradictory target/source claims, stale generated summaries, and unapproved mid-epic child/scope changes.
- Make gate enforcement state-based, not command-only. Supported CLI lifecycle commands must block invalid transitions, and doctor/validate must also fail invalid current states caused by manual tracker/doc edits.
- Make approval prompts bounded. Gates must fail with a specific drift reason or evidence gap; they must not ask for generic owner approval when the work is unchanged and inside the approved envelope.
- Update prompts, Codex skills, templates, and README guidance so agents follow the gates naturally.
- Add regression tests modeled on generalized failure classes, including wrong-artifact visual proof, runtime target/source contradiction, implementation self-certifying visual ACs, child work started without owner approval, reactive fix without amendment, and legacy closeout without adoption. The Knowledge Graph incident may be used as a fixture example for these general classes.

## Acceptance Criteria (Verifiable)

- AC1: Tasks and epics cannot move into implementation planning, implementation, decomposition, child approval, or scaffolding through supported CLI lifecycle commands until `REQUIREMENTS.md` records an explicit owner approval envelope for requirements and acceptance criteria, with a bounded discovery exception. Work inside the approved envelope must not require repeated owner approval.
- AC2: New epics require `EPIC-CONTRACT.md` before decomposition, child approval/scaffolding, or movement into `In Progress`; legacy epics use the adoption path.
- AC3: `epic scaffold-child` injects a child charter that carries relevant parent ACs, invariants, invalid substitutes, proof recipes, and artifact targets from the epic contract.
- AC4: Parent AC satisfaction is gated by proof ownership. Epic audit/closeout must not accept parent AC proof from a child that is not assigned as the proof owner for that AC and recipe.
- AC5: Structured evidence records exist for proof recipes. Visual/reference-fidelity claims require recipe-specific fields such as commit, timestamp, reference artifact, delivered artifact, comparison method, and evidence artifact path. Runtime/deployment/integration claims require execution target, source/artifact under test, observation method, and positive proof that the target actually used that source.
- AC6: Proof-recipe trigger rules select required recipes from requirements, ACs, epic contracts, child charters, and material claims; invalid substitute evidence is rejected for triggered recipes.
- AC7: Doctor fails on stale, missing, invalid-substitute, or contradictory evidence, including target/source contradictions such as prose claiming one environment/source pair while structured evidence proves a different pair, and generated summaries that no longer match structured evidence.
- AC8: Mid-epic new child work, reactive defect fixes, and material scope changes require an amendment record before related child work can advance through gated transitions.
- AC9: New epic child rows must have decomposition or amendment provenance before approval/scaffolding/review/complete gates; manually added unprovenanced rows are blocked for new/adopted epics.
- AC10: Pre-existing epics/tasks have a safe adoption path. Closed legacy epics warn only; open legacy epics must adopt before gated transitions; inferred evidence is marked untrusted until refreshed.
- AC11: Project prompts, Codex skills, generated templates, and README guidance describe and route agents through owner approval, epic contracts, child charters, proof recipes, amendments, adoption, and closeout gates.
- AC12: Automated tests cover generalized drift failures, using the Knowledge Graph incident only as one regression fixture where helpful, and prove the new doctor/status gates reject them.
- AC13: Owner approvals are freshness-bound. Approval commands record the approved artifact identity, and doctor/status gates reject stale approvals after material changes to requirements, acceptance criteria, epic contracts, or approved decomposition plans.
- AC14: Epic decomposition is owner-controlled without being per-row bureaucratic. Child rows for new/adopted epics must come from an approved decomposition plan or amendment, and `epic approve`/`epic scaffold-child` must reject rows outside the approved plan or amendment. Matching rows inside an approved decomposition plan do not require separate owner approval.
- AC15: Visual/reference-fidelity work requires pre-implementation calibration plus post-implementation comparison against the delivered user-facing artifact. QA against code, unit tests, build output, surrogate surfaces, or an uncalibrated reference cannot satisfy the recipe.
- AC16: Gated lifecycle validity is state-based. Doctor/validate fails invalid current states even if they were created by manual tracker/doc edits rather than supported CLI commands.
- AC17: Material claims that satisfy ACs must be represented in a structured claim-to-evidence ledger. Unsupported prose claims are ignored for closeout, and prose that conflicts with structured evidence fails doctor/status gates.
- AC18: Approval prompts are bounded to material owner decisions. Doctor/status/closeout gates must fail with concrete drift reasons or evidence gaps, not require fresh owner approval for unchanged child work that remains inside the approved authority envelope.

## Proposed Child Work

These rows are proposed for decomposition after owner approval. Once the decomposition plan is approved, matching child rows may be approved, scaffolded, and implemented without separate per-row owner approval. Fresh owner review is required only for material changes, new/deviating rows, changed parent AC coverage, changed source-of-truth interpretation, changed artifact identity, changed proof obligations, or owner-approved deviations.

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Approved Scope Authority Gate | AC1, AC11, AC12, AC13, AC16, AC18 | Add approval envelope parsing, CLI approval commands for new work, approval freshness, manual block support for legacy/adoption, lifecycle blocking, bounded discovery exception, bounded approval prompts, prompt/skill guidance, and tests. |
| Epic Contract Model | AC2, AC4, AC11, AC12 | Add `EPIC-CONTRACT.md` template/schema for sources of truth, invalid substitutes, invariants, proof owners, and artifact targets. |
| Decomposition Plan And Authority Gate | AC9, AC11, AC12, AC14, AC16, AC18 | Add first-class decomposition plan support, plan-level owner approval evidence, rejection of rows outside the approved authority envelope, and state checks for child rows created outside decomposition/amendment. |
| Structured Evidence And Proof Recipes | AC5, AC6, AC7, AC12, AC15, AC17 | Define child-local structured evidence, generated epic evidence index, built-in recipes, trigger rules, claim-to-evidence ledger, and invalid-substitute enforcement for visual reference fidelity, external contract alignment, deployed/published artifact alignment, runtime target/source verification, and responsive/multi-context visual behavior. |
| Child Charter Inheritance And Proof Ownership | AC3, AC4, AC12, AC14 | Update child scaffolding/status gates so children inherit epic constraints and cannot self-certify parent ACs they do not own. |
| Artifact Identity Staleness And Summary Gates | AC5, AC6, AC7, AC12, AC13, AC15, AC16, AC17 | Enforce reference/delivered artifact identity, runtime target/source identity, approval/evidence freshness, contradiction checks, and generated-summary consistency in doctor/status/closeout. |
| Epic Amendment Child Provenance And Drift Audit Flow | AC8, AC9, AC12, AC14 | Add amendment records, child-row provenance, and drift audit checks for reactive fixes, new scope, deviations, and child completion. |
| Legacy Adoption Path | AC10, AC12 | Add safe adoption for pre-existing open/closed epics/tasks and mark inferred old evidence untrusted until refreshed. |
| Prompt Skill Template And README Updates | AC1, AC2, AC3, AC5, AC6, AC8, AC10, AC11, AC13, AC14, AC15, AC17, AC18 | Update generated guidance so agents use the gates without making ordinary tasks unnecessarily heavy or creating approval fatigue. |
| Regression Fixture Suite | AC1-AC18 | Add tests for generalized drift failures, with Knowledge Graph-derived cases used only as regression fixtures, plus legacy adoption cases. |

## Open Questions (Answer Needed)

- None blocking. Owner review is required because the second clarification pass materially changed approval freshness, decomposition ownership, visual calibration, and claim-to-evidence requirements.

## Decisions (Resolved)

- This work is an epic, not a standalone task, because it changes workflow structure, CLI gates, doctor behavior, templates, prompts, skills, tests, and legacy behavior.
- The solution must be enforcement-first. Passive documentation is not an acceptable fix.
- The solution must be drift-first, not approval-first. Approval establishes the boundary; gates and evidence enforce the boundary.
- Approval fatigue is a product failure. If ordinary in-scope child work requires repeated owner approval, the workflow has overfit to ceremony rather than preventing drift.
- Structured evidence must be more trusted than prose summaries for closeout and doctor checks.
- Existing closed legacy work must not be broken by new gates.
- Open legacy work must not be allowed to close under new standards using untrusted inferred evidence.
- Child tasks should execute slices of the epic, not reinterpret the epic source of truth.
- New work should use explicit CLI approval commands for requirements/AC approval; manual approval blocks remain supported for legacy/adoption.
- Any explicit owner message approving requirements/ACs may be recorded as approval when the approval source is captured. Doctor must fail placeholder or agent-only approval notes.
- Requirement/AC approval is not permanent. Material edits to requirements, ACs, epic contracts, or approved decomposition plans stale the approval and require renewed owner review before gated lifecycle movement.
- Unchanged work inside the approved authority envelope does not need renewed approval. It needs valid provenance, fresh evidence, and no drift findings.
- `EPIC-CONTRACT.md` is mandatory for new epics after this change and should remain small.
- Epic decomposition must be a controlled artifact. The current parser-style `epic decompose` behavior is insufficient by itself because it can generate plausible but wrong child rows from prose; this epic must add or adapt CLI support so an owner-reviewed decomposition plan is the source for proposed rows.
- Child row approval is authority validation, not repeated owner approval. The workflow must prevent an agent from inventing a child row, approving it, scaffolding it, and claiming inherited parent coverage; it should not require the owner to approve every unchanged child row that already appears in the approved decomposition plan.
- Discovery before approval may read, inspect, and write findings only. Temporary local artifacts under `.tmp` are allowed only when explicitly permitted by the requirement. Product source changes are not allowed under the discovery exception.
- Structured evidence is child-local and authoritative. Epic closeout uses a generated epic-level evidence index.
- Structured material claims are the closeout input. Prose summaries may explain evidence, but cannot satisfy acceptance criteria unless backed by a structured claim/evidence record.
- Built-in proof recipes require CLI/helper-generated evidence. Manual evidence is allowed only as untrusted adoption or unsupported-proof metadata and cannot satisfy closeout by itself.
- The first built-in proof recipes are `visual-reference-fidelity`, `external-contract-alignment`, `deployed-artifact-alignment`, `runtime-target-source`, and `responsive-visual-behavior`.
- Evidence freshness stores the git commit and relevant artifact hash when available.
- Visual/reference-fidelity recipes have two gates: calibration before implementation and comparison before Review/Complete.
- New gates fail for new/adopted managed work and warn for legacy work until a gated transition.
- Adoption covers both epics and tasks: `project epic adopt` and `project task adopt`.
- The current CLI does not yet have `epic amend`, `epic adopt`, or `task adopt`; adding those commands or equivalent supported command paths is in scope.
- Amendments are required only when a mid-epic change affects parent ACs, source-of-truth interpretation, artifact identity, proof requirements, or child ownership.
- Gates should ask the user for approval only when an amendment/deviation/deferral decision is needed. Otherwise they should tell the agent what drift or evidence gap must be fixed.
- `epic closeout` must ignore prose claims unless backed by valid structured evidence; generated acceptance maps/audits must be checked against structured evidence for stale or contradictory summaries; no separate closeout command is required initially.
- Visual/reference-fidelity is domain-general. Valid proof must compare the reference artifact against the delivered user-facing artifact in an appropriate viewer/browser/rendering context. Code review, unit tests, build success, or proof against a surrogate artifact are invalid substitutes.
- Runtime target/source verification is domain-general. Valid proof must identify the execution target, the source/artifact under test, observation method, and positive proof that the target actually used that source. A related service running, a deploy succeeding, a tunnel existing, or a different environment passing is not enough.
- Proof recipes are triggered by claims and acceptance criteria, not only by task type. If a task claims visual fidelity, runtime/deployment correctness, external contract alignment, or responsive/multi-context behavior, the corresponding recipe is required even if the task was not originally categorized that way.
- New epic child rows need provenance. For new/adopted epics, child rows must be created by `epic decompose` or `epic amend`; direct tracker edits are legacy-only and cannot advance through gated transitions until adopted or amended. Provenance plus match to the approved decomposition plan is enough for ordinary child work to proceed.

## Validation Plan

- Run targeted unit tests for approval parsing, epic contract parsing, child charter generation, evidence recipe validation, proof ownership, amendment/adoption flows, and doctor failures.
- Run existing doctor/status/epic lifecycle tests to prove backwards-compatible behavior.
- Add fixtures that simulate the generalized failure classes from the Knowledge Graph incident:
  - implementation child self-certifies visual parent AC;
  - visual proof references a surrogate review surface while the delivered artifact differs;
  - prose claims one runtime target/source pair while structured evidence proves another;
  - a related service/tunnel/deploy exists but no evidence proves the runtime target used that source;
  - a visual/reference-fidelity AC is reviewed using code/tests without rendered comparison;
  - child advances without owner-approved requirements;
  - requirements/ACs change after approval and the stale approval is rejected;
  - agent-generated decomposition rows advance without owner-approved decomposition authority;
  - unchanged in-envelope child work is allowed without repeated owner approval;
  - approval prompt fatigue is avoided by failing with a specific drift/evidence reason instead of generic approval needed;
  - reactive defect fix advances without amendment;
  - manual tracker/doc edits create an invalid gated state that doctor catches;
  - visual/reference-fidelity work starts without calibration;
  - manual epic child row without decomposition/amendment provenance advances in a new/adopted epic;
  - generated acceptance map/audit prose contradicts structured evidence;
  - legacy open epic attempts closeout without adoption.
- Run `./.project-workflow/cli/workflow doctor`.
- Run the repository test suite.
