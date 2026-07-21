<!-- project-workflow:start -->
## Project Workflow

This repository uses project-workflow. Keep workflow state in `.project-workflow/BACKLOG.md`, `.project-workflow/TRACKER.md`, and `.project-workflow/tasks/`.

- Read repo-specific workflow guidance from `.project-workflow/guidance.md`.
- Use `.project-workflow/BACKLOG.md` for optional future intent before work is promoted into task or epic execution state. Promoted rows stay in the backlog; active execution status belongs in trackers and task/epic docs.
- Read task ID namespace and generation config from `.project-workflow/config.json`.
- To install or refresh project-workflow itself, run `uvx --from git+https://github.com/johndetlefs/project-workflow.git project init` from the repository root; add `--agent codex`, `--agent cursor`, `--agent claude-code`, or `--agent github-copilot` when selecting a mode. Do not use bare `project init` unless the package is intentionally installed and known to be current.
- Use `./.project-workflow/cli/workflow` for supported backlog, Fix, task, epic, and validation commands.
- Route one bounded post-completion correction to a Fix, new outcomes or multiple independent items to a Task, and coordinated workstreams to an Epic. The user's label is evidence, not a binding classification. Fixes use one `FIX.md`, the shared tasks directory, and the global tracker; do not create a separate Fix tracker.
- Before planning, record one owner approval envelope with `task approve-requirements` or `epic approve-requirements`; unchanged work inside that envelope should proceed without repeated approval prompts, while drift, stale requirements, or evidence gaps must be fixed or amended.
- After requirements approval, run Planner, post-plan Clarify, `task ready`, and move new tasks to `Ready` autonomously unless material drift or exceptional risk requires owner input. `Plan Confirmed` remains legacy-compatible.
- For pre-existing work, use `task adopt` or `epic adopt`; pre-adoption inferred evidence stays untrusted until refreshed.
- For epics, `epic decompose` writes `DECOMPOSITION.md`; child rows must match that plan before approval, scaffold, readiness, or status advancement.
- Use `epic amend` for owner-approved mid-epic child rows outside the decomposition plan; direct tracker edits outside decomposition/amendment authority remain blocked.
- New/adopted epics require non-placeholder `EPIC-CONTRACT.md` before decomposition, child approval/scaffolding, or movement into Ready/In Progress.
- If requirements or claims trigger visual/reference, external contract, deployed artifact, runtime target/source, or responsive visual proof, fill child-local `EVIDENCE.json`; QA prose, tests, builds, or surrogate artifacts are invalid substitutes.
- Use `./.project-workflow/cli/workflow task status --id <TASK-ID> --to <STATUS>` for tracker lifecycle changes.
- Keep version command ownership explicit: init refreshes managed assets, Doctor diagnoses without mutation, and upgrade transforms repository schema. Review `upgrade` first; apply only with `--apply --plan-fingerprint <SHA256>` in a clean worktree.
- Run `./.project-workflow/cli/workflow doctor` after tracker or task-doc changes.
<!-- project-workflow:end -->
