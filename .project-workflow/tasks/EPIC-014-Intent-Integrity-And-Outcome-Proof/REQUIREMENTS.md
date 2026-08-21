# Requirements

## Summary

- Task: EPIC-014
- Title: Intent Integrity And Outcome Proof
- Last updated: 2026-08-21
- Proposal state: Evidence-backed draft awaiting one concise owner approval
- Intent contract: full

## Intent

Make Project Workflow stop agents from watering down what the owner asked for into the easiest
narrow result they can defend. State the owner's intent plainly before approval, then hold
requirements, planning, implementation and QA accountable to that intent—not merely to
internally consistent documents and checklists.

## Problem Statement

Project Workflow can preserve a requirements artifact, map its acceptance criteria through
decomposition, collect strong evidence, and close an Epic while the delivered product still
does not perform the material job the owner asked for. The current controls protect work from
drifting after approval, but they do not adequately detect an agent narrowing, proxying, or
omitting the owner's outcome before or during requirements and decomposition.

The triggering regression class is an authoring programme that delivered truthful preview and
one editable canary while leaving the level materially unauthorable. The implementation and
evidence were substantial, but the approved child contract had silently reduced "author the
level" to "prove one bounded control." This is a general failure class, not a game-specific
requirement.

## Intent Spine

- OC1 — Completion capability: preserve the plain-language `## Intent` above as the primary
  meaning against which all derived requirements, plans, tasks, evidence and completion claims are
  judged, while showing the owner what completion will and will not enable and the exact journey
  that will prove the outcome.
- OC2 — Material capabilities: preserve source intent, expose assumptions and exclusions, trace
  outcome commitments through decomposition, detect silent narrowing, require outcome-level
  proof, and retain independent owner acceptance where it is genuinely required.
- OC3 — Success journey: a realistic user request is captured, planned, decomposed, implemented and
  reviewed; if downstream artifacts reduce the requested capability to a canary, preview,
  internal representation, subset, or surrogate, the workflow blocks before implementation or
  completion and explains the exact lost capability.
- OC4 — Successful-but-wrong result: every generated document, AC mapping, test, build,
  evidence record and Doctor gate passes while the user still cannot perform the requested job.
- OC5 — Exclusions: the workflow does not guarantee perfect semantic interpretation, force
  exhaustive scope, require owner approval for every child or implementation detail, or add a
  heavyweight document stack to ordinary bounded fixes.
- OC6 — Assumptions: the owner's stated outcome is authoritative; semantic fidelity
  requires reviewable judgment as well as deterministic traceability; and outcome proof must
  match the product claim rather than merely demonstrate related implementation activity.
- OC7 — Authority source: owner direction in Codex on 2026-08-21 following direct inspection of a
  completed Project Workflow Epic whose green gates certified a materially narrowed outcome.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-21
- Approval note / source: Codex owner confirmation on 2026-08-21: revised plain-language Intent is approved; proceed (clerical full-contract schema normalization only)
- Approved artifact identity: sha256:46cb105a43fe2f700b5b239a64f628a8fb7730fe6b7471910740d4b6b37f81e5

## Goal

Add a proportionate intent-integrity layer to Project Workflow so the original owner outcome
remains a first-class, inspectable authority from conversational intake through requirements,
decomposition, implementation, QA, closeout and retrospective. The workflow must detect and
block material capability loss, proxy substitution, silent de-scoping and outcome-free
completion while preserving autonomous execution inside a genuinely approved envelope.

## Non-Goals

- Do not create a general-purpose product-management suite, transcript archive, semantic proof
  engine, or guarantee that a model can never misunderstand a user.
- Do not replace concrete requirements, stable AC IDs, Epic contracts, structured evidence,
  proof recipes, code review, or owner acceptance.
- Do not require every small Fix or mechanical task to add extensive intent artifacts or run a
  heavyweight user journey.
- Do not solve the failure by adding generic prose that Doctor checks only for presence.
- Do not make the same agent's self-attestation sufficient proof that its interpretation
  preserved the owner's outcome.
- Do not treat maximal scope, gold-plating, or speculative completeness as intent fidelity.
- Do not expose private task transcripts or maintainer-specific project content in the public
  package, fixtures, documentation, or evaluation corpus.
- Do not publish, release, roll out, or upgrade consumer repositories under this Epic without
  separate delivery authority.

## Users & Context

- Owners provide outcomes and product judgment conversationally and need one high-quality,
  low-cognitive-load approval moment rather than a large artifact whose most consequential
  omissions are difficult to see.
- Implementing agents need a compact statement of the job, capabilities, exclusions and success
  journey that survives context compaction and child delegation.
- Planners and coordinators need to know when a canary, pilot, preview, subset or architectural
  seam is a legitimate stage and when it is an unapproved reduction of the requested outcome.
- QA reviewers need authority to reject an implementation that satisfies every AC while still
  failing the original user job.
- Maintainers need real regression evaluations showing that the workflow changes agent
  behaviour, not merely that new headings and parser branches exist.

## Repository Scope

- Primary repository: .
- Repositories touched: .
- Historical downstream failures may inform sanitized fixtures, but no downstream repository is
  mutated or made a competing workflow authority by this Epic.

## Requirements (Outcome-Focused)

- R1 — Make every triggered task and Epic begin with a one- or two-sentence plain-language
  `## Intent` that states what the owner is actually trying to achieve. Extend it with a compact
  Intent Spine containing the capability available at completion, material capability
  commitments, the exact success journey, successful-but-wrong results, explicit exclusions,
  assumptions and authority source. Both stay in `REQUIREMENTS.md`; the workflow must not create
  another mandatory owner-authored document.
- R2 — Make requirements approval lead with the exact plain-language Intent and ask whether it
  accurately reflects what the owner means. Supporting detail then states "you will be able to,"
  "you still will not be able to," material assumptions/exclusions, and the journey that will
  prove completion. The owner approves the meaning once; artifact identity binds that approval
  to the reviewed version but is not presented as the substance of what the owner approved.
- R3 — Preserve stable outcome commitments from the Intent Spine through parent ACs, proposed
  child work, decomposition, child requirements, implementation tasks, proof ownership and
  closeout. Every material capability must be implemented, explicitly excluded, or governed by
  an owner-approved amendment/deferral.
- R4 — Add a read-only intent audit that compares the Intent Spine with requirements, ACs,
  non-goals, decomposition, child charters and implementation plans. It must classify material
  commitments as preserved, narrowed, replaced by proxy, omitted, broadened, amended or
  explicitly deferred, and report source locations and the user-visible consequence.
- R5 — Treat material reductions such as full capability to canary, authoring to preview,
  user-operable behavior to hidden internal data, all to subset, ordinary journey to debug-only
  path, or delivered outcome to evidence-only report as scope changes. They require a recorded
  amendment or refreshed owner approval; unchanged technical refinement does not.
- R6 — Add deterministic traceability and state gates around the semantic audit: required intent
  fields, stable commitment IDs, coverage, audit freshness, amendment/deferral provenance,
  reviewer identity, and lifecycle enforcement must be machine-checkable even though semantic
  judgment remains reviewable rather than falsely deterministic.
- R7 — Add a `user-outcome-journey` proof recipe for user-visible product and workflow claims.
  It must identify the normal entry point, actor, starting state, material operations, resulting
  state/artifact, outcome observations, source/revision, environment, and invalid substitutes.
- R8 — Make independent QA review both the approved AC envelope and the preserved Intent Spine.
  The reviewer must explicitly answer whether every AC could pass while the user job remains
  undone and must return Changes requested when the answer is yes.
- R9 — Keep owner acceptance separate where taste, practical usability, gameplay feel, or another
  owner-only judgment is part of the claimed outcome. Automated and independent review may make
  work ready for owner acceptance but may not manufacture it.
- R10 — Apply the stronger controls proportionately. Epics, material user-facing workflows,
  authoring/migration/replacement work, and completeness claims trigger the full gate. Bounded
  fixes and mechanical changes use the smallest sufficient intent and proof shape.
- R11 — Build sanitized regression fixtures and behavioural evaluations from multiple real
  failure classes: narrowed authoring, rendered-product versus code/test proxy, wrong runtime or
  delivered artifact, checklist-complete but outcome-incomplete Epic, and an over-broad agent
  that must avoid gold-plating a genuinely bounded request.
- R12 — Run repeated agent trials or an equivalent behaviourally meaningful evaluation across
  the supported agent guidance before claiming improvement. Template/parser unit tests remain
  necessary but are invalid as sole proof that models preserve intent.
- R13 — Surface intent-integrity state and the next action through Doctor/status without turning
  inferred semantic confidence into a false deterministic pass. Unknown or review-required
  states must remain explicit.
- R14 — Update package source, generated prompts and skills, installed managed assets,
  documentation, fixtures and self-hosted parity together. Existing repositories must retain a
  safe warning/adoption/upgrade path rather than being broken by a new mandatory schema.
- R15 — Prove the completed workflow in a disposable realistic repository and through at least
  one current user-facing dogfood journey. The proof must inspect the resulting requirements,
  decomposition, audit, implementation result and closeout decision, including a deliberate
  successful-but-wrong candidate that the workflow rejects.

## Acceptance Criteria (Verifiable)

- AC1: New task and Epic requirements templates and agent guidance create a substantive one- or
  two-sentence plain-language Intent plus a compact Intent Spine with stable outcome-commitment
  IDs. Readiness rejects placeholder, procedural, circular or missing intent and material fields
  only when the configured task class triggers the intent-integrity gate.
- AC2: The approval workflow leads with the exact Intent and asks the owner to confirm that it
  accurately reflects what they mean. It then concisely states what the user will and will not be
  able to do, material assumptions/exclusions, and the exact success journey; approval is
  freshness-bound to the full requirements artifact without presenting document IDs as the thing
  the owner is substantively approving or requiring repeated approval for unchanged work.
- AC3: Epic decomposition and child scaffolding preserve every triggered outcome commitment in a
  validated coverage map linking commitment, parent AC, child owner and required outcome proof;
  unmapped material commitments block readiness.
- AC4: A read-only intent audit reports preserved, narrowed, proxy, omitted, broadened, amended
  and deferred classifications with source locations and user-visible consequences across
  requirements, ACs, decomposition, child charters and implementation plans.
- AC5: The generalized narrowed-authoring fixture is blocked when "meaningfully author the
  level" becomes truthful preview plus one bounded control, even if all downstream AC mappings,
  tests, evidence and artifact hashes are internally consistent.
- AC6: A material reduction cannot advance through readiness, Review or Complete without an
  owner-approved amendment or refreshed approval that plainly identifies the lost capability;
  routine implementation detail inside the intent envelope does not trigger approval fatigue.
- AC7: `user-outcome-journey` is a built-in structured proof recipe with validated fields,
  artifact freshness and invalid substitutes. Tests, builds, screenshots, internal data,
  debug-only controls, related environments and one canary capability cannot satisfy a claimed
  end-user job by themselves.
- AC8: Independent QA guidance and gates require an intent-level adversarial verdict in addition
  to AC-by-AC evidence. QA blocks a fixture where every AC passes but the normal user journey
  cannot accomplish the requested job.
- AC9: Lifecycle, audit, closeout, Doctor and status distinguish implemented, outcome-proven,
  ready for owner acceptance, owner accepted, integrated, released and deployed states without
  laundering one into another.
- AC10: Proportionality fixtures prove that a bounded low-risk Fix can proceed with a compact
  minimal intent record while Epic, authoring, migration, replacement, completeness and material
  user-facing claims receive the full gate.
- AC11: Sanitized regression coverage includes at least five distinct failure/counter-failure
  classes, preserves no private transcript or downstream proprietary content, and demonstrates
  both under-delivery rejection and gold-plating avoidance.
- AC12: Behavioural evaluations run multiple trials from held-out realistic prompts and grade
  at least: preserved intent, explicit de-scoping, capability coverage, exact outcome proof,
  unnecessary scope, and approval burden. The release claim records model/harness scope and does
  not generalize beyond tested surfaces.
- AC13: Package source, generated prompts/skills/templates, the installed self-hosted helper and
  documentation remain parity-checked; upgrade planning is reviewable and existing completed
  historical work remains valid.
- AC14: A disposable repository journey proves intake through closeout, including rejection of a
  deliberately green-but-wrong implementation, and a current dogfood journey proves the same
  controls remain practical for an actual owner/operator.
- AC15: Independent QA/code review verifies the implementation and behavioural evidence; no
  publication, release, consumer rollout, or claim that agent under-delivery is solved occurs
  without separate release authority and evidence from the exact packaged artifact.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose | Dependencies |
| --- | --- | --- | --- |
| Define Intent Spine And Semantic Approval | AC1, AC2, AC10 | Add the compact source-of-intent contract, proportional triggers and low-cognitive-load owner approval envelope without adding a separate mandatory document stack. |  |
| Build Intent Audit And Narrowing Gates | AC3, AC4, AC5, AC6 | Add commitment traceability, cross-artifact semantic audit output, material reduction/amendment classification, lifecycle enforcement and the narrowed-authoring regression. | TASK-080 |
| Add Outcome Journey Proof And Independent Review | AC7, AC8, AC9 | Add the user-outcome proof recipe, intent-aware QA verdict and lifecycle distinctions for outcome proof and owner acceptance. | TASK-080, TASK-081 |
| Create Behavioural Regression Evals | AC10, AC11, AC12 | Build sanitized realistic cases, held-out multi-trial evaluation, grading and counter-cases for under-delivery, proxy completion, approval burden and gold-plating. | TASK-080, TASK-081, TASK-082 |
| Prove Packaging Parity And Real Journeys | AC13, AC14, AC15 | Update managed surfaces, prove safe upgrade/self-hosted parity, run disposable and live dogfood journeys, and perform independent Epic QA without releasing. | TASK-080, TASK-081, TASK-082, TASK-083 |

## Outcome Commitment Coverage

| Commitment | Child Owners | Parent ACs | Required Disposition |
| --- | --- | --- | --- |
| OC1 — Govern all derived work by the approved Intent | TASK-080, TASK-081, TASK-082, TASK-083, TASK-084 | AC1-AC15 | Every child traces its scope and proof back to the Intent; internal consistency cannot override it. |
| OC2 — Concise capability and proof envelope | TASK-080, TASK-084 | AC1-AC2, AC14 | Implemented and demonstrated in disposable and dogfood journeys. |
| OC3 — Preserve, trace and prove material capabilities | TASK-080, TASK-081, TASK-082, TASK-084 | AC1-AC9, AC13-AC15 | Implemented across source contract, audit, proof, QA and packaged parity. |
| OC4 — Block narrowing in the real journey | TASK-081, TASK-082, TASK-084 | AC3-AC9, AC14 | Implemented and demonstrated before readiness and completion. |
| OC5 — Reject internally green but outcome-wrong work | TASK-081, TASK-083, TASK-084 | AC5-AC6, AC8, AC11-AC12, AC14 | Rejected in deterministic fixtures, behavioural trials and the packaged journey. |
| OC6 — Preserve proportionality | TASK-080, TASK-083, TASK-084 | AC10-AC15 | Demonstrated for both a bounded Fix and full-gate work without widening release authority. |
| OC7 — Combine semantic judgment with claim-matched proof | TASK-080, TASK-081, TASK-082, TASK-083 | AC1-AC12 | Implemented without presenting semantic confidence as deterministic truth. |

## Delivery Sequence

1. Owner confirms or corrects the plain-language Intent and its concise capability, boundary and
   proof explanation. Artifact identifiers are recorded for provenance, not used as a substitute
   for meaningful approval.
2. Run Planner and post-plan Clarify, then decompose exactly TASK-080 through TASK-084.
3. Implement the Intent Spine and approval semantics before writing enforcement around them.
4. Implement the audit/narrowing gates, then outcome proof and independent review.
5. Build behavioural evaluations against the resulting workflow and use failures to revise the
   earliest owning artifact rather than weakening graders.
6. Prove proportionality, compatibility, packaged parity and realistic journeys.
7. Stop at release and rollout boundaries unless separately authorized.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Treat this as an Epic because it spans intake, requirements, approval UX, decomposition,
  lifecycle gates, evidence recipes, QA, behavioural evaluation, packaging and compatibility.
- Put a one- or two-sentence plain-language Intent before the detailed contract and make it the
  governing approval meaning; IDs, hashes and artifact fields preserve provenance but do not
  replace comprehension or consent.
- The owner confirmed on 2026-08-21 that the revised plain-language Intent is materially more
  useful, accurately reflects the requested direction, and should proceed. This confirmation is
  the approval meaning; the detailed requirements and acceptance criteria bind its implementation
  and proof without replacing it.
- Extend the existing `REQUIREMENTS.md` with a compact Intent Spine rather than add another
  mandatory owner-authored document.
- Treat the original owner outcome as authority alongside, not beneath, derived ACs.
- Combine semantic review with deterministic traceability; do not claim a parser can prove
  meaning.
- Require outcome-level proof when the claim is user-visible, but keep small bounded work light.
- Use real failure classes as sanitized evaluation fixtures and include an anti-gold-plating
  counter-case.
- Keep implementation authority, owner acceptance, integration, publication, release and rollout
  as separate gates.

## Validation Plan

- Run focused unit/property tests for templates, parsing, stable commitment IDs, coverage,
  approval freshness, audit classifications, amendments, deferrals, evidence validation,
  lifecycle gates, Doctor/status and legacy compatibility.
- Inspect every generated Codex/Copilot/Cursor skill and prompt entry point for equivalent intent
  preservation and review behavior.
- Run sanitized fixture journeys covering all AC11 failure classes and verify both fail-closed and
  non-triggered proportional paths.
- Run multiple held-out behavioural trials using the real supported agent harnesses, preserve
  exact prompt/model/harness/evaluator identity, and independently inspect false passes/failures.
- Run the complete repository test suite, strict Doctor, package build/install parity, canonical
  UVX packaging test, and `git diff --check`.
- Exercise the exact packaged artifact in a disposable repository from conversational intake
  through safe closeout, then run one current owner-facing dogfood journey.
- Record independent QA separately from owner acceptance and any later release/rollout proof.
