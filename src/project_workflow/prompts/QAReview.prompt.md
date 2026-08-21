---
name: project.qa-review
description: Run the QA and code review gate after implementation validation, before completion.
argument-hint: taskId=TASK-330-Superuser scope="review changed work"
agent: agent
---

Use this prompt after `project.implement` has made changes and moved the task or work item to `Testing`.

Purpose:

- Independently verify the implemented work against requirements and acceptance criteria.
- Review the changed code for correctness, maintainability, security, data safety, and scope control.
- Record review results before any task is marked `Complete`.

Reference docs:

- Technical constraints/instructions: [../copilot-instructions.md](../copilot-instructions.md)
- Repo-specific workflow guidance: [../../.project-workflow/guidance.md](../../.project-workflow/guidance.md)
- User story tracker: [../../.project-workflow/TRACKER.md](../../.project-workflow/TRACKER.md)
- Canonical task tracker: `/.project-workflow/tasks/${input:taskId}/IMPLEMENTATION.md`
- Requirements source of truth: `/.project-workflow/tasks/${input:taskId}/REQUIREMENTS.md`
- Project outcomes: [../../.project-workflow/CONSTITUTION.md](../../.project-workflow/CONSTITUTION.md)

Inputs:

- Task: `${input:taskId:TASK-000-Example}`
- Scope: `${input:scope:What changed or what should be reviewed?}`

Defaults and inference:

- If `taskId` is omitted, infer it from the current branch name when possible.
- If `scope` is omitted, review the current uncommitted diff plus the task docs.
- Ask only when the task cannot be inferred safely.

Required workflow:

1. Read `REQUIREMENTS.md`, `IMPLEMENTATION.md`, and the tracker row for the task.
2. Confirm implementation has reached `Testing`. If it has not, stop and direct the user to run `project.implement` first.
3. Run the relevant workflow status command to move the row to `Review` before starting QA/code review:
   - standalone task: `./.project-workflow/cli/workflow task status --id ${input:taskId} --to Review`
   - epic child: `./.project-workflow/cli/workflow epic status --epic-id <EPIC_ID> --id ${input:taskId} --to Review`
4. Inspect the changed files and map each acceptance criterion ID to evidence:
   - automated test, typecheck, lint, build, or script result
   - manual verification result
   - code inspection finding
5. If a requirement, acceptance criterion, child charter, epic contract, or material claim triggers a proof recipe, inspect child-local `EVIDENCE.json` and the referenced evidence artifact before accepting the claim. Visual/reference fidelity requires rendered comparison against the delivered user-facing artifact, not code review, tests, build output, or a surrogate surface. Runtime target/source proof requires the exact target/source pair and positive proof that target used that source.
   For `user-outcome-journey`, verify the exact actor, normal entry point, starting state, material
   operations, resulting artifact/state, observations, source/revision and environment. Reject
   tests, builds, screenshots, internal data, debug-only controls, related environments and a
   canary as sole proof of a broader user job.
6. Run any missing narrow validation that is necessary to support the review. Do not ask the user to manually test behavior that the agent can validate directly with available commands, tests, scripts, browser tools, screenshots, or local tools. Do not rerun broad checks unless they are the most meaningful available check.
7. Review code for:
   - correctness against requirements and decisions
   - unintended scope expansion
   - error handling and edge cases
   - security, permissions, privacy, and data integrity
   - migrations, rollback, observability, and operational risk where relevant
   - tests and documentation appropriate to the change
8. Record results in `IMPLEMENTATION.md` under `## QA & Code Review` with:
   - date
   - reviewer/agent context
   - files or areas reviewed
   - validation evidence
   - a clear distinction between verified evidence and deferred setup, owner-only actions, or unavailable connector/OAuth checks
   - for workspace mode, confirmation that every touched repository has explicit branch/PR,
     validation, delivery, and evidence attribution consistent with read-only repository status
   - findings, if any
   - verdict: `Pass`, `Pass with follow-ups`, or `Changes requested`
   - for an adversarial Intent QA contract: the Intent adversarial verdict, a Yes/No answer to
     whether every AC could pass while the approved job remains undone, current Intent-audit state,
     exact outcome-journey evidence, and reviewer-independence basis. A Yes or unknown answer
     requires `Changes requested`.
9. Run `./.project-workflow/cli/workflow doctor` when available and include any workflow-state warnings or errors in the review output.
10. If issues are found:
   - keep tracker status as `Review` or set it to `Blocked` if the issue prevents safe release
   - list findings first, ordered by severity, with file references where possible
   - do not mark anything `Complete`
11. If review passes:
   - say that QA/code review passed
   - only run the relevant workflow command to mark `Complete` if the user explicitly asked you to complete the task after review
   - otherwise leave status as `Review` and ask for explicit completion approval

Output expectations:

- Findings first when any exist.
- Validation evidence with exact commands or manual checks, reported by AC ID.
- A concise verdict.
- The next step is `project.retro` only after the task is marked `Complete`.

Guardrails:

- Do not mark `Complete` based on implementation validation alone. QA/code review must pass first.
- Do not use this prompt to implement new scope. Small review fixes are allowed only when they directly address review findings and remain within the accepted requirements.
- If review reveals a requirements conflict, route back to `project.clarify` and record the decision before continuing.
- Do not accept unsupported prose claims as closeout evidence. If prose claims contradict structured evidence, report the contradiction as a blocking finding.
- Once the approved Intent, in-scope acceptance criteria, required proof, and QA verdict pass, stop
  review-oriented investigation. Continue or reopen work only when a finding shows the owner
  cannot accomplish the approved Intent, a material delivery claim is false, an explicitly
  required lifecycle stage is blocked, or a material safety, security, privacy, data-integrity, or
  hard-to-reverse risk exists. Route other adjacent improvements and non-material diagnostics to a
  separate follow-up.
- Name the affected proof layer for a blocking finding. Repeat broad or full-suite checks,
  packaging, deployment, or cross-host journeys only when the correction can affect that layer or
  the approved delivery stage requires it; do not repeat them merely for additional reassurance.
- A post-proof `workflow validation impact` decision never commissions another review.
  `unaffected` advances, `affected` permits one validation of the named invalidated proof, and
  `ambiguous` returns one concise question to the owner.
- Run independent QA once when the approved work item requires it. Findings may trigger affected
  validation, but never a fresh open-ended review. Another reviewer invocation requires a new
  material change, an explicit high-consequence requirement, or direct owner authorization.
- For delegated work, independently inspect coordinator-verified worker identity, exact source/worktree,
  allowed diff, validations, evidence, capability/capacity provenance, descendant blocking, privacy,
  and single-writer behavior. Delegate's aggregate report and worker assertions are not QA evidence by
  themselves.
