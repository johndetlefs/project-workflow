# EPIC-014 Dogfood Receipt

- Date: 2026-08-21
- Repository: Project Workflow current candidate worktree
- Journey: Owner Intent approval through sequential child execution and intent-aware closeout gates
- Delivery boundary: Local candidate only; no publication, release, rollout or consumer adoption

## Owner-facing approval

The owner was shown a meaning-first synopsis whose lead was the requested outcome: prevent Project
Workflow from allowing detailed, internally green work to replace the job the owner actually asked
for. The synopsis named completion capability, material capabilities, proof journey,
successful-but-wrong result, exclusions and assumptions before provenance. The owner approved that
meaning once and asked implementation to proceed. No child required a renewed generic approval
inside the unchanged envelope.

## Practical execution

The work ran sequentially because the CLI source and its two exact mirrors share a dependency chain
and overlapping write scope. Delegate was not used; isolated local Codex CLI processes were used
only as held-out behavioural trials and independent QA surfaces, not as workflow implementation
delegates.

The live Epic exercised the controls it introduced:

- TASK-080 made the brief Intent the approval object and kept bounded Fixes compact.
- TASK-081 created the sourced, freshness-bound parent intent audit and narrowing gates.
- TASK-082 required claim-matched normal-journey evidence and adversarial QA wording.
- TASK-083 preserved a failed calibration trial, corrected grader ambiguity, and required two
  repeated release-trial passes rather than promoting one favorable response.
- TASK-084's exact-wheel journey initially blocked for an actionable reason: the workflow rejected
  a proxy but failed to echo the lost capability. The candidate was changed so the gate now names
  that consequence. Independent QA then caught a deeper flaw: the journey supplied the `proxy`
  classification itself while the child artifacts still described the complete result. The final
  journey instead creates an internally green preview-only child, reviews its actual claim scope,
  result, observations and artifact, records the missing archive capability, proves rejection, and
  only then restores the complete journey.

## Friction and burden observed

- The owner approval interaction was concise: one Intent question, not a request to approve Epic,
  AC and Task identifiers.
- Exact QA field wording caught an ambiguous self-review answer in TASK-083. The correction was
  legitimate but showed that agent guidance must distinguish adversarial fixture behavior from the
  delivered task's own completion claim.
- Audit freshness deliberately required refresh after child implementation evidence changed. This
  added agent work but no owner approval request.
- Package proof was materially heavier than unit validation, as intended for a release-candidate
  claim. The compact Fix path remained zero-additional-approval in both behavioural release trials.
- Independent QA generated real corrective work rather than a ceremonial pass: it forced retained
  package artifacts, complete host/resource manifests, structured journey claims and session-bound
  behavioural provenance.
- A second independent review rejected this narrative itself as sufficient dogfood proof. The
  remediation now captures `dogfood-journey.json` from the live workflow CLI and binds the actual
  Codex task and owner approval turn, the exact approval synopsis output, approved requirements,
  current intent audit, every child plan, tracker state and both blocking review identities. This
  narrative is context for that packet, not its source of truth.

## Outcome and proof boundaries

The mechanically captured current journey demonstrates that the candidate workflow can keep the
approved Intent visible, detect stale semantic review, reject a sourced proxy, require exact outcome
evidence and prevent an adversarial QA pass when the owner job could remain undone. It does not prove universal model
reliability, publication, a trusted release, rollout, adoption by existing consumers, owner
acceptance of the final Epic, or commercial validation.
