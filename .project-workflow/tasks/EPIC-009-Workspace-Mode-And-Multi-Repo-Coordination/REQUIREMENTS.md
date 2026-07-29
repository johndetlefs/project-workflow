# Requirements

## Summary

- Task: EPIC-009
- Title: Workspace Mode And Multi-Repo Coordination
- Last updated: 2026-07-29
- Source discussion: On 2026-07-29 the owner confirmed the config-based, parent-authority direction and asked to continue with requirements before implementation.
- Starting point: `9c329aaa6a66ccba62c25c704ea071419cbe7911` on the dedicated `codex/BL-017-workspace-mode` branch.

## Backlog Source

- ID: BL-017
- Title: Workspace Mode And Multi-Repo Coordination
- Type: Epic Candidate
- Priority: High
- Status before promotion: Accepted
- Outcome: Make project-workflow explicitly support parent workspace/control repositories with nested implementation repos and parent-owned folders, so agents can coordinate backlog, tasks, branches, validation, evidence, and sub-agent handoffs from one live workflow source of truth.
- Notes: Scale outcome after operational clarity, progressive assurance, and modular extension boundaries. The parent-workspace model must coordinate nested repositories without inventing a second source of truth or weakening repository ownership.

## User Story

As the owner of a product workspace whose authoritative Project Workflow state lives in a parent Git repository while implementation spans that parent plus nested, independently versioned repositories, I want Project Workflow to understand the workspace boundary, repository ownership, touched repositories, Git state, validation, and delivery evidence, so that one parent workflow can coordinate real work without child trackers, hidden repository state, or agent-improvised handoff conventions.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: Repository owner
- Approval date: 2026-07-29
- Approval note / source: Codex conversation 2026-07-29: approved EPIC-009 requirements, AC1-AC15, contract, decomposition, and proof plan; let's get on with it
- Approved artifact identity: sha256:467e8f05831c2a06aab3fbddbe72e79f9ee2f4d95f594453f70f8a96cd2afb85

## Goal

Add a small, first-class workspace mode that extends the existing `.project-workflow/config.json` contract with an optional repository registry and workflow authority, then makes Doctor, task/Epic gates, and `project status` use that declaration.

The first production acceptance case is `/Users/johndetlefs/repos/johndetlefs`: the parent repository owns the only live Project Workflow state and also owns implementation folders, while `next/` and `email/` are nested independent Git repositories. The feature must make this topology explicit and verifiable without mutating any JohnDetlefs repository during EPIC-009 discovery or acceptance inspection.

## Non-Goals

- Do not create child `.project-workflow/` trackers, backlogs, or task stores.
- Do not create a hosted control plane, database, daemon, background monitor, or centralized multi-project service.
- Do not add automatic cross-repository branch creation, checkout, commit, push, pull request, merge, release, or deployment.
- Do not add generalized orchestration, sub-agent machinery, plugins, adapters, extension ecosystems, or enterprise governance.
- Do not automatically run arbitrary repository validation commands in the first version. Validation execution remains explicit and repository-owned; Project Workflow validates and reports the resulting attribution and evidence.
- Do not transparently discover and operate the parent workflow when the local helper is invoked from a child repository in the first version. Canonical operation remains from the declared workspace root, with existing `--root` support where applicable.
- Do not treat every folder in a workspace as a repository. The registry describes actual Git repository boundaries; parent-owned folders remain owned by the parent repository.
- Do not modify, upgrade, branch, commit, push, merge, release, or deploy `/Users/johndetlefs/repos/johndetlefs`, `next/`, or `email/` as part of EPIC-009 without separate explicit authority.

## Users & Context

- The immediate user is the owner operating the real JohnDetlefs.com workspace through Codex.
- The parent repository currently relies on `AGENTS.md` and `.project-workflow/guidance.md` to declare that it owns the only live workflow state and that `next/` and `email/` are independent repositories.
- Existing JohnDetlefs task documents manually record `Primary repo`, `Repos touched`, workflow ownership, and branch/PR notes, but the CLI does not validate those names against a repository registry or require evidence attribution consistently.
- A current `project status --root /Users/johndetlefs/repos/johndetlefs` inspection reports the parent Git state only. It does not report the Git state of `next/` or `email/`, even when an active task's implementation belongs there.
- This creates concrete burdens and error paths:
  - an agent must reconstruct repository boundaries from prose on every task;
  - a clean or known parent state can conceal a dirty, detached, divergent, or wrong-branch child repository;
  - misspelled or incomplete repository attribution is not mechanically rejected;
  - branch, pull request, validation, and delivery claims can be recorded without a consistent repository owner;
  - a child tracker can compete with the parent authority unless a human notices;
  - handoff requires manually reconciling several Git roots before the delivery state is trustworthy.
- Existing single-repository installations must remain simple and compatible when no workspace declaration is present.

## Definitions

- Workspace root: the directory containing the authoritative `.project-workflow/` installation and the optional workspace declaration.
- Workflow authority repository: the one registered Git repository that owns the live `.project-workflow/` state.
- Registered repository: a stable repository ID and workspace-relative path that resolves to an actual Git root inside the workspace.
- Primary repository: the registered repository owning the main implementation outcome for a work item.
- Repositories touched: every registered repository expected to receive tracked changes for the work item, including the authority repository when its tracked workflow state is part of the Git delivery.
- Repository evidence: repository-attributed branch/HEAD, pull request or integration state, validation command/result, and delivery evidence. Missing evidence remains missing or not recorded; it is never inferred.

## Proposed Workspace Declaration

The first version extends the existing `.project-workflow/config.json` rather than introducing a second configuration file:

```json
{
  "workspace": {
    "authority_repository": "workspace",
    "repositories": [
      {
        "id": "workspace",
        "path": ".",
        "role": "control"
      },
      {
        "id": "next",
        "path": "next",
        "role": "implementation"
      },
      {
        "id": "email",
        "path": "email",
        "role": "implementation"
      }
    ]
  }
}
```

The authority repository may also own implementation files and parent-owned folders. `role` describes its workspace responsibility; it does not forbid implementation in that repository.

## Requirements (Outcome-Focused)

- R1. Extend the existing workflow config with an optional, versioned workspace declaration containing one authority repository and a registry of stable repository IDs, workspace-relative paths, and roles.
- R2. Treat the absence of a workspace declaration as the existing single-repository mode with `.` as the implicit authority and repository. Existing repositories must not need config edits merely to keep working.
- R3. Validate workspace declarations fail-closed: IDs and paths must be unique; the authority must be registered; paths must be relative, remain inside the workspace after resolution, and identify distinct Git roots; malformed, missing, symlink-escaped, duplicated, nested-without-Git, or out-of-workspace targets must produce stable findings and repair direction.
- R4. Enforce one live workflow authority. A registered non-authority repository containing live `.project-workflow/` state must be reported as a competing source of truth. Historical archives owned by the authority repository are not live child state.
- R5. Add a consistent repository-scope section to new task, Fix, and Epic-child artifacts with a registered primary repository and registered repositories touched. Cross-repository work must name all delivery repositories before implementation readiness can pass.
- R6. Keep the workflow authority visible separately from implementation ownership, while including its Git/delivery evidence when tracked authority-repository changes are part of the work item's delivery.
- R7. Validate repository scope at workflow gates. The primary repository must be registered and included in repositories touched; unknown, duplicate, missing, or contradictory repository attribution must block readiness or later evidence credit with stable findings.
- R8. Extend the existing read-only operational model so `project status` reports the workspace authority and repository-scoped Git facts for the repositories relevant to the selected or active work: path, Git root, branch or detached state, HEAD, upstream, and clean/dirty state.
- R9. A workspace-aware status must not summarize the parent repository as if it represented the whole work item. Dirty, detached, unavailable, missing, or mismatched touched repositories must remain visible and attributable without automatically changing them.
- R10. Support a repository-focused status view using a stable registered repository ID while preserving the existing work-item selector, human output, JSON output, deterministic ordering, source provenance, and non-mutating behavior.
- R11. Record validation and delivery evidence by repository. Each touched repository must be able to show the command or method used, result, evidence source, branch/PR or explicit not-applicable/not-authorized state, and integration/delivery state without inferring a later stage from an earlier one.
- R12. Do not require a pull request, merge, release, or deployment merely to call repository implementation complete. Require the actual state to be explicit per repository and preserve `not recorded`, `not authorized`, or equivalent bounded states when that lifecycle action is outside scope.
- R13. Make Doctor and status distinguish configuration validity, workflow authority, work-item repository scope, live Git observation, recorded validation evidence, and recorded delivery evidence. One passing layer must not inflate another.
- R14. Keep the packaged CLI, generated local helper, config template, repository schema/upgrade path, README, and managed agent guidance aligned. Upgrade must preserve user-owned config and existing workflow state while adding workspace-capable managed behavior.
- R15. Prove the feature against a disposable realistic three-repository workspace shaped like JohnDetlefs.com and use the real JohnDetlefs workspace only as a read-only topology/status acceptance target unless separate mutation authority is granted.

## Acceptance Criteria (Verifiable)

- AC1: A valid config can declare the parent workspace repository as authority plus `next/` and `email/` as nested independent Git repositories, and the parsed model exposes stable IDs, resolved paths, roles, and the single authority.
- AC2: No-workspace config fixtures retain existing single-repository Doctor, task, Epic, status, and upgrade behavior without requiring new task metadata retroactively.
- AC3: Invalid registry fixtures for duplicate IDs/paths, missing authority, non-Git paths, path escape, symlink escape, missing repositories, and competing live child workflow state produce stable findings with exact source paths and repair direction.
- AC4: New task, Fix, and Epic-child scaffolds contain a consistent repository-scope contract; readiness passes for valid single- and multi-repository scope and fails for missing, unknown, duplicate, or primary-not-touched repository IDs.
- AC5: A cross-repository task covering the authority repository and `next/` cannot reach readiness with only prose guidance or incomplete repository attribution, while a child-only implementation task still reports the parent authority separately without inventing child workflow state.
- AC6: From a disposable workspace with three independent Git roots, one `project status` invocation reports the authority plus repository-scoped branch/detached, HEAD, upstream, and clean/dirty facts for every repository relevant to selected work.
- AC7: Regression fixtures prove a clean parent cannot conceal a dirty, detached, missing, unavailable, or wrong-branch touched repository; the finding and next action name the exact registered repository and never perform Git mutation.
- AC8: Human and versioned JSON status output are projections of the same workspace model, support focused work-item and repository selection, retain deterministic ordering/provenance, and preserve existing single-repository fields compatibly.
- AC9: Repository evidence fixtures independently vary validation, branch/PR, integration, release, and deployment records for each touched repository; status and lifecycle gates keep those claims separate and never promote one repository's evidence to another.
- AC10: Before/after hashes and Git-state captures prove workspace validation, Doctor, status, malformed-state handling, and failure paths do not mutate the authority or child repositories.
- AC11: A disposable JohnDetlefs-shaped manual journey declares `workspace`, `next`, and `email`, creates a parent-owned cross-repository work item, surfaces independently varied Git state, records per-repository validation/delivery evidence, and completes the intended readiness/status/handoff journey without creating child trackers or performing unauthorized Git delivery.
- AC12: Read-only inspection of `/Users/johndetlefs/repos/johndetlefs` confirms the real parent/`next`/`email` topology and demonstrates the current parent-only status boundary; no acceptance step writes to those repositories without explicit authority.
- AC13: Upgrade fixtures prove existing current, legacy-unversioned, and workspace-declared repositories preserve user content and receive aligned config/schema/helper behavior; packaged/local-helper parity and deterministic upgrade guarantees remain intact.
- AC14: README and managed agent guidance explain workspace declaration, authority, repository scope, status inspection, validation evidence, delivery boundaries, parent-root invocation, and why child trackers or automatic cross-repo Git actions remain invalid.
- AC15: Focused workspace tests, existing operational-status/Doctor/upgrade tests, backlog validation, strict Doctor, compilation/parity checks, `git diff --check`, and the full Python 3.10 locked suite pass with the Homebrew UVX packaging path executed rather than skipped.

## Open Questions (Answer Needed)

- None in the proposed envelope. The owner resolved the initial design choices on 2026-07-29 by accepting the existing-config model, evidence-aware validation without an automatic runner, separate visibility for workflow authority, and parent-root invocation for the first version.

## Decisions (Resolved)

- Extend `.project-workflow/config.json`; do not introduce a separate workspace configuration file.
- Use stable repository IDs and workspace-relative paths, with one explicitly registered authority repository.
- Keep single-repository mode implicit and backward compatible when `workspace` is absent.
- Keep validation execution repository-owned and explicit in the first version; Project Workflow validates and reports attribution/evidence rather than becoming an arbitrary command runner.
- Show workflow authority separately from primary implementation ownership, but include authority-repository Git/delivery evidence when its tracked changes are part of the work item.
- Keep canonical operation at the parent workspace root for the first version; transparent child-to-parent discovery is deferred unless real use proves it necessary.
- Extend the existing `project status`, Doctor, readiness, and evidence model instead of creating a parallel workspace status store.
- Preserve repository ownership and human authority: workspace awareness is read-only coordination and validation, not permission for cross-repository Git or delivery mutation.

## Validation Plan

- Add table-driven config parsing and Doctor fixtures for valid, absent, malformed, duplicate, missing, escaped, symlinked, non-Git, and competing-authority workspace declarations.
- Create disposable Git workspaces with a parent authority and two nested independent repositories; independently vary branch, detached, HEAD, upstream, clean/dirty, missing, and unavailable state.
- Create task/Fix/Epic-child fixtures that independently vary primary repository, repositories touched, authority involvement, validation evidence, PR/integration state, and later delivery receipts.
- Assert human/JSON semantic equivalence, deterministic repository ordering, stable codes, source paths, responsible parties, and exact non-mutating next actions.
- Capture filesystem hashes and Git state for every registered repository before and after Doctor/status/error paths.
- Exercise a manual disposable JohnDetlefs-shaped workflow journey from declaration through readiness, status, repository evidence, QA, and handoff; inspect the resulting artifacts independently.
- Re-run read-only topology and current-status inspection against `/Users/johndetlefs/repos/johndetlefs` without writing to its parent, `next/`, or `email/` repositories.
- Run focused tests, all existing regression tests, config/backlog validation, strict Doctor, packaged/generated-helper parity, compilation, `git diff --check`, and `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q`.
- Proof boundary: fixture automation proves breadth and failure handling; the disposable manual journey proves the intended operator experience; read-only JohnDetlefs inspection proves the real topology/current gap but does not prove deployment, adoption, or mutation of that workspace.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Define Backward-Compatible Workspace Registry | AC1, AC2, AC3, AC13 | Extend config/schema/upgrade behavior with one authority and safe registered Git roots while preserving ordinary single-repository operation. |
| Enforce Workflow Authority And Repository Scope | AC3, AC4, AC5 | Add consistent work-item repository metadata and gate invalid scope or competing child workflow state. |
| Add Workspace-Aware Git And Status Inspection | AC6, AC7, AC8, AC10 | Extend the shared read-only operational model and human/JSON output with repository-scoped Git facts and focused selection. |
| Attribute Validation And Delivery Evidence By Repository | AC5, AC9, AC10 | Keep validation, branch/PR, integration, release, and deployment evidence explicit and isolated per touched repository. |
| Prove Upgrade, Guidance, And Real Workspace Journey | AC11, AC12, AC13, AC14, AC15 | Deliver aligned managed assets and prove the disposable end-to-end journey plus the bounded read-only JohnDetlefs acceptance inspection. |
