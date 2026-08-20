## Local Tooling

- Homebrew `uvx` is installed at `/opt/homebrew/bin/uvx`. The Codex app may omit `/opt/homebrew/bin` from `PATH`; check the explicit path and prepend it before claiming UVX is unavailable or allowing the UVX packaging test to skip.

<!-- project-workflow:start -->
## Project Workflow

This repository uses project-workflow. Keep workflow state in `.project-workflow/BACKLOG.md`, `.project-workflow/TRACKER.md`, and `.project-workflow/tasks/`.

- Read repo-specific workflow guidance from `.project-workflow/guidance.md`.
- Use `.project-workflow/BACKLOG.md` for optional future intent before work is promoted into task or epic execution state. Promoted rows stay in the backlog; active execution status belongs in trackers and task/epic docs.
- Read task ID namespace, generation config, and optional parent-workspace registry from `.project-workflow/config.json`.
- In workspace mode, run workflow commands from the parent authority root, keep the only live workflow state there, and use registered repository IDs in task scope and evidence. Status Git inspection is read-only and never authorizes cross-repository mutation.
- To initialize a new repository, run `uvx --from project-workflow==0.4.0 project init` from the repository root with `--agent codex`, `--agent cursor`, `--agent claude-code`, or `--agent github-copilot`.
- To upgrade an existing repository, run `uvx --from project-workflow==0.4.0 project upgrade` with its agent mode. Authorized non-interactive agents add `--yes`; human invocation confirms before upgrade applies managed assets plus repository schema together. Do not run init first.
- Use `./.project-workflow/cli/workflow` for supported backlog, Fix, task, epic, and validation commands.
- Run `./.project-workflow/cli/workflow status` for a read-only operational summary and sourced next action. Use `--id <WORK-ID>` to focus active work, `--repository <REPOSITORY-ID>` to focus one registered workspace repository, `--strict` to make visible Doctor warnings blocking, and `--format json` for schema-versioned output. Status does not replace Doctor diagnosis, canonical upgrade, lifecycle gates, QA, Git integration, or service verification, and never executes its recommended action.
- Route one bounded post-completion correction to a Fix, new outcomes or multiple independent items to a Task, and coordinated workstreams to an Epic. The user's label is evidence, not a binding classification. Fixes use one `FIX.md`, the shared tasks directory, and the global tracker; do not create a separate Fix tracker.
- Before planning, record one owner approval envelope with `task approve-requirements` or `epic approve-requirements`; unchanged work inside that envelope should proceed without repeated approval prompts, while drift, stale requirements, or evidence gaps must be fixed or amended.
- After requirements approval, run Planner, post-plan Clarify, `task ready`, and move new tasks to `Ready` autonomously unless material drift or exceptional risk requires owner input. `Plan Confirmed` remains legacy-compatible.
- For pre-existing work, use `task adopt` or `epic adopt`; pre-adoption inferred evidence stays untrusted until refreshed.
- For epics, `epic decompose` writes `DECOMPOSITION.md`; child rows must match that plan before approval, scaffold, readiness, or status advancement.
- Use `epic amend` for owner-approved mid-epic child rows outside the decomposition plan; direct tracker edits outside decomposition/amendment authority remain blocked.
- New/adopted epics require non-placeholder `EPIC-CONTRACT.md` before decomposition, child approval/scaffolding, or movement into Ready/In Progress.
- If requirements or claims trigger visual/reference, external contract, deployed artifact, runtime target/source, or responsive visual proof, fill child-local `EVIDENCE.json`; QA prose, tests, builds, or surrogate artifacts are invalid substitutes.
- Use `./.project-workflow/cli/workflow task status --id <TASK-ID> --to <STATUS>` for tracker lifecycle changes.
- Keep version command ownership explicit: init creates a new installation, Doctor diagnoses without mutation, and canonical UVX upgrade refreshes managed assets and transforms repository schema in one reviewed transaction. Use `upgrade --plan` and fingerprinted apply for automation.
- For a sanitized client handoff, use canonical `project smoke-bomb` from a clean dedicated worktree to review exact removal, run explicit validations, preserve useful client agent guidance, and export a ZIP without Git or workflow internals.
- Delegate coordinates existing approved rows for exactly one Task or Epic. Select the lightest sufficient coordinator, subagent, persistent-task, or peer-team surface from approved Execution Needs rather than Task-versus-Epic kind. Resolve surface-specific isolation, monitoring, reconciliation, retirement, and capacity capabilities as runtime-observed `verified`, `unsupported`, or `unknown`; only verified capability plus current-host authority authorizes native launch, otherwise use a safe coordinator/sequential fallback or block. Never hard-code worker capacity.
- The coordinator alone writes shared workflow state and verifies worker identity, source, scope, validation, and evidence before satisfying dependencies. A failure blocks its descendants; unrelated branches continue only while shared premises remain valid. Temporary visible subordinate tasks retire only after verified durable disposition; Codex maps retirement to reversible archival, while attention-bearing work stays visible. Delegate never replaces Implement, independent QA, Epic closeout, owner acceptance, or delivery proof.
- Run `./.project-workflow/cli/workflow doctor` after tracker or task-doc changes.
<!-- project-workflow:end -->
