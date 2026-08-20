# Epic Retro

- Epic: EPIC-011
- Title: Release And Roll Out Project Workflow 0.4.0
- Last updated: 2026-08-20

## Lessons

- A feature-complete Epic is not automatically a release-ready artifact: semantic version authorities, CI/release pins, public availability, reviewed-main CI, immutable tag ancestry, Trusted Publishing, public installability, and provenance remain separate gates.
- A saved Codex project is not evidence of a Project Workflow installation. Inventory must resolve the saved root and inspect its own manifest before mutation.
- Fingerprint-bound public-package plans make parallel multi-repository upgrades reviewable, but a successful current-version validation does not erase historical Doctor debt; retain both facts.
- Local adoption and remote publication are different states. A committed local main upgrade makes the feature available to local Codex worktrees without implying that consumer remotes were pushed.
- The canonical clean-worktree gate protected real active workflow state in two repositories. Bypassing it, auto-stashing, or committing unrelated owner work would have been worse than an explicit blocked disposition.

## Follow-up Tasks

- After the active `.project-workflow/BACKLOG.md` change in The Moon Is Hollow is integrated or otherwise resolved, rerun its retained 0.4.0 plan and canonical public-package upgrade.
- After the active johndetlefs workflow Epics/tasks are committed and its authority root is clean, rerun its retained 0.4.0 plan and canonical public-package upgrade.
- Reconcile strategic-advisor's pre-existing local-main/origin-main divergence before any remote publication of its local 0.4.0 upgrade commit.
- Push or PR the six local consumer upgrade commits only when the owner separately authorizes remote integration for those repositories.

## Deferrals

- The Moon Is Hollow remains on 0.3.0 at `5c698ed` because one owner-owned backlog modification makes the canonical clean-worktree precondition fail.
- johndetlefs remains on 0.3.0 at `d8c2f48` because 56 active owner-owned workflow changes make the canonical clean-worktree precondition fail.
- Consumer remote pushes are intentionally deferred; the requested local Codex adoption is committed, while cross-repository remote publication was not inferred.

## Missed In-Scope Work

- None unrecorded. All installed roots are either current on 0.4.0 or retained unchanged with an exact blocker and follow-up.
