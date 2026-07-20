---
name: project.fix
description: Route and manage a bounded post-completion correction as a lightweight Fix.
argument-hint: title="..." relatedWork="TASK-001 or Not identified"
agent: agent
---

# Fix

Use a Fix for one bounded correction against a delivered or accepted baseline. A Fix is a
lightweight work-item subtype in the same `.project-workflow/tasks/` directory and global
`TRACKER.md` as tasks and epics; it is not a separate tracking system.

## Route before scaffolding

The agent owns the initial recommendation. The user's label is useful evidence but is not
binding.

- Keep an in-scope correction inside an active task or epic child.
- Use a Fix for one bounded defect, regression, change request, or incident against delivered
  or accepted behavior.
- Use a Task when the request creates a new outcome, requires material product decisions or
  discovery, or contains multiple independent work items.
- Use an Epic when several coordinated outcomes or workstreams are required.
- State the rationale and proceed for a clear, authorized case. Ask one focused question when
  the classification is genuinely ambiguous or materially changes scope/authority.

Do not reopen or rewrite completed work by default. Link it when identifiable. If finding the
origin would require disproportionate archaeology, record `Not identified` plus the delivered
baseline and report evidence.

## Workflow

1. Read `AGENTS.md` and `.project-workflow/guidance.md` when present.
2. Scaffold with:

   `./.project-workflow/cli/workflow fix init --title "<TITLE>"`

3. Complete the single `FIX.md`: report/baseline, routing rationale, classification, risk,
   related work, repo metadata, bounded plan, and verification plan.
4. Classify `Type` as `Defect`, `Regression`, `Change Request`, or `Incident`. `Hotfix` is a
   mode, not a fifth type.
5. Run `fix triage --id <FIX-ID>` to validate the authority/risk packet and move to `Ready`.
   A Hotfix may move directly from `To Do` to `In Progress` only after its emergency safety
   packet is complete.
6. Use `fix status` for `In Progress`, `Testing`, and `Review` transitions.
7. Record verification/regression evidence and residual risk, then use `fix close` from Review.
   Duplicate, rejected, or deferred reports may close directly to `N/A` with an explicit
   disposition, decision, closer, and date instead of delivery evidence.
8. If triage reveals a larger outcome, use `fix promote --to task|epic`; do not stretch the Fix
   envelope.
9. Run `doctor` after lifecycle changes.
10. Do not require a retro for ordinary Fix closeout. Use retro or create an explicit follow-up
    only when the Fix reveals a reusable workflow, process, quality, or prevention gap; never
    reopen the completed originating work for that follow-up.

For a workspace, use canonical component identities/paths for `Primary repo` and `Repos touched`
and keep per-repo branch, PR, and evidence links in `FIX.md`. In a single repo, `.` is sufficient.
