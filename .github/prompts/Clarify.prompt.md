---
name: project.clarify
description: Resolve one material ambiguity before approval, after planning, or at a Coordinator-owned drift boundary.
argument-hint: workItemId=TASK-330-or-EPIC-014 mode=pre-approval-or-post-plan-or-drift-ambiguity topic="..."
agent: agent
---
<!-- project-workflow:generated -->

Use this prompt only in one of three modes:

- `pre-approval`: resolve material product or authority questions before requirements approval;
- `post-plan`: compare a Task plan or Epic decomposition with approved Intent and proof;
- `drift-ambiguity`: classify one concrete ambiguity routed by the Coordinator.

Read repository instructions, `.project-workflow/guidance.md`, the Constitution, and
`/.project-workflow/tasks/${input:workItemId}/REQUIREMENTS.md`. Treat its substantive `## Intent`
or `## Intent Spine` and approved requirements as authority. For an Epic parent, also read
`EPIC-CONTRACT.md` and `DECOMPOSITION.md` when present; parent `IMPLEMENTATION.md` is not required.
For a Task or Epic child, read its User Story and implementation plan when present.

Stop for Requirements only when neither substantive Requirements Intent nor a usable User Story
exists. Reuse relevant owner answers already in conversation or repository evidence; never ask the
owner to repeat them.

Cross-check only ambiguity that could materially affect outcome, scope, safety, security, billing,
data correctness, authority, validation, proof, or user-visible behaviour.

In `pre-approval` mode:

1. Write each material question to `REQUIREMENTS.md` before asking, with why it matters and 2-4
   actionable options.
2. Ask one unresolved material question at a time unless the owner requests batching.
3. Record each answer immediately, preserve AC IDs, and align any existing plan. Do not generate a
   full plan; Planner owns planning.

In `post-plan` mode:

1. Compare the plan or decomposition with Intent, boundaries, ACs, and proof obligations.
2. Resolve implementation-detail inconsistencies inside the approved envelope autonomously.
3. Treat a clear narrowing, omission, or proxy substitution against unchanged approved Intent as
   `drift-detected`; restore the approved capability without asking the owner to repeat it.
4. Return to the owner only for an unresolved material choice or a genuine proposed change to
   requirements, ACs, proof, artifact identity, scope, or authority.
5. When a Task is clean, run `task ready`, move it to `Ready`, and continue when implementation is
   authorised. For an Epic parent, return clean to the Coordinator; Epic lifecycle commands retain
   ownership.

In `drift-ambiguity` mode, return exactly one classification to the Coordinator:

- `inside-envelope`: authority clearly covers the work; continue;
- `drift-detected`: work narrows, broadens, substitutes a proxy, or changes authority/proof;
- `approved-change`: a current owner-approved amendment covers it.

Name the controlling requirement and user-visible consequence. When current authority cannot
classify a material ambiguity, ask the owner one focused question before returning a classification;
do not prematurely label it drift or an approved change.

For a full-contract Epic parent or child, run the parent `epic intent-audit` read-only. Treat stale,
unknown, review-required, or changes-requested as a real coverage gap; AC consistency is not Intent
fidelity.

Clarify does not monitor boundaries, launch work, run QA, create review loops, or write shared
tracker/evidence/lifecycle state. It is boundary-triggered, not periodic. The Coordinator owns drift
detection and state changes.

Return the mode, authority inspected, ambiguity and material consequence, classification or
decision, files aligned, and whether owner input is genuinely required.
