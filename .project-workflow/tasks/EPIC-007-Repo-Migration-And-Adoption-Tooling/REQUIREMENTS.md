# Requirements

## Summary

- Task: EPIC-007
- Title: Repo Migration And Adoption Tooling
- Last updated: 2026-07-10

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Not approved
- Approval date: Not approved
- Approval note / source: Not approved
- Approved artifact identity: Not approved

## Backlog Source

- ID: BL-003
- Title: Repo Migration And Adoption Tooling
- Type: Epic Candidate
- Priority: High
- Status before promotion: Accepted
- Outcome: Give agents one guided way to detect stale installs, legacy workflow debt, missing config, stale helper versions, old schemas, missing approval envelopes, and evidence gaps, then produce or apply a safe migration plan.
- Notes: Top recommendation from comprehensive project-workflow review; first needle mover.

## Goal

Enable an agent to bring an existing repository onto the current project-workflow contract without guessing, hand-editing many files, or losing historical workflow evidence.

The owner-facing outcome is a guided migration/adoption flow that first proves what is stale or missing, then proposes concrete safe actions, and only applies changes through explicit, auditable commands.

## Non-Goals

- Do not build a dashboard or external service.
- Do not automatically import or transform roadmap/backlog documents outside `.project-workflow/BACKLOG.md`.
- Do not silently approve historical warnings, requirements, or evidence.
- Do not redesign all lifecycle statuses in this epic.
- Do not modularize the entire CLI in this epic, except where small extraction is necessary for migration tooling.
- Do not replace the canonical `project init` refresh path; migration tooling should orchestrate or explain it.

## Users & Context

- Primary user: an owner or agent working in a repository that already has `.project-workflow/` but may have stale generated helpers, old templates, missing config, legacy prefixes, old epic schemas, or historical doctor warnings.
- Secondary user: a project-workflow maintainer dogfooding the migration path across sibling repositories such as `daily-checklist`, `client-management-app`, `shopify-theme`, `avoca-interiors`, `toby`, and `johndetlefs`.
- Current evidence: sibling repos showed stale local helpers that lacked `doctor`, blocking structured-evidence errors in visual/layout repos, missing configs/guidance in older installs, and current/legacy warnings that require a safer adoption path.
- Additional evidence from this epic setup: parallel sequential backlog additions produced a duplicate `BL-004`, and backlog promotion to epic created `EPIC-007` without `EPIC-CONTRACT.md`.

## Requirements (Outcome-Focused)

- Provide a dry-run migration/adoption audit for an initialized repository.
- Detect stale local helper capability/version state and explain the canonical refresh action.
- Detect missing or outdated user-owned workflow support files, including `.project-workflow/config.json`, `.project-workflow/guidance.md`, and `.project-workflow/BACKLOG.md`, without overwriting existing user content.
- Detect generated-asset drift, pending `*.new` files, old command surfaces, old epic schemas, missing epic contracts, missing decomposition authority, missing approval envelopes, and structured-evidence gaps.
- Group findings into current blockers, current warnings, legacy warnings, accepted warnings, stale-install issues, and safe follow-up candidates.
- Produce an ordered migration plan with exact commands or file actions and a clear distinction between dry-run output, safe automatic fixes, and owner-confirmed decisions.
- Provide an apply path for low-risk mechanical fixes, such as refreshing generated assets, adding missing generated/current epic artifacts, and creating missing default support files.
- Preserve all user-owned task, epic, backlog, guidance, and tracker content unless an explicit generated marker or managed block allows refresh.
- Provide an ergonomic path to batch review and accept historical doctor warnings with reasons, while keeping changed warnings visible.
- Prevent or mitigate sequential ID allocation collisions during migration/backlog operations, or explicitly recommend unique ID generation for concurrent workflows.
- Ensure backlog promotion to epic creates the same current required artifact set as `epic init`.
- Leave evidence-heavy claims blocked until real evidence is refreshed or explicitly adopted as untrusted.
- Include tests that exercise stale helper detection, missing artifact repair, batch warning acceptance, collision handling, and dry-run/apply behavior.

## Acceptance Criteria (Verifiable)

- AC1: A dry-run command reports stale helper/capability state for repositories whose local helper lacks current commands, without mutating repository files.
- AC2: A dry-run command reports workflow debt grouped by severity and type: blockers, current warnings, legacy warnings, accepted warnings, stale generated assets, and safe mechanical fixes.
- AC3: The migration plan lists exact next actions and distinguishes automatic fixes from owner-confirmed decisions.
- AC4: An apply command can perform low-risk mechanical repairs without overwriting user-owned unmarked content.
- AC5: Batch accepted-warning support can add selected warning fingerprints with reasons and leaves changed or unselected warnings visible.
- AC6: Sequential ID allocation or backlog write collision risk is addressed by locking, retry validation, or a documented/validated unique-ID migration path.
- AC7: Backlog promotion to epic creates `EPIC-CONTRACT.md` and all other current epic-init artifacts, and doctor does not warn about missing current epic artifacts immediately after promotion.
- AC8: Migration/adoption tooling preserves existing tracker rows, task docs, epic docs, backlog rows, guidance, and config values unless an explicit generated marker or managed block allows refresh.
- AC9: Tests cover dry-run behavior, apply behavior, stale helper detection, missing epic artifact repair, accepted-warning batching, and collision prevention or detection.

## Open Questions (Answer Needed)

- Should the primary command be named `project migrate`, `project adopt-repo`, or a subcommand under `doctor`?
- Should apply-mode fixes be all-or-nothing, selectable by fix ID, or grouped by category?
- Should accepted-warning batch edits live in this epic or be split into a child task that may ship independently?
- Should local helper version metadata be solved in this epic or as a separate child task from `BL-005`?

## Decisions (Resolved)

- Start with dry-run-first migration/adoption tooling as the first implementation direction.
- Treat stale helper detection, missing current epic artifacts, accepted-warning ergonomics, and ID allocation collision safety as in-scope because they were proven during review or backlog setup.
- Keep full CLI modularization, status vocabulary simplification, and helper distribution redesign as separate backlog items.
- Preserve generic roadmap/backlog import as out of scope; keep `BL-001` as a later exploration.

## Validation Plan

- Use fixture repositories initialized from older helper shapes to verify stale-helper and command-surface detection.
- Use temporary repos with missing config/guidance/backlog/current epic artifacts to verify dry-run and apply behavior.
- Use current sibling-repo findings as scenario references, without mutating sibling repos during tests.
- Run the full pytest suite plus targeted new tests for each acceptance criterion.
- Run `project doctor` and `project doctor --strict` on the project-workflow repo after migration changes.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Define Migration Command Shape And Dry-Run Report | AC1, AC2, AC3 | Establish the CLI surface, report categories, and no-mutation audit behavior. |
| Add Helper Version And Capability Detection | AC1, AC3 | Identify stale local helpers and explain canonical refresh actions. |
| Implement Safe Mechanical Repair Apply Path | AC3, AC4, AC7, AC8 | Add selected low-risk fixes such as missing support files and missing current epic artifacts. |
| Add Batch Accepted-Warning Review Support | AC2, AC5, AC8 | Let users accept known historical warnings with reasons while preserving changed warnings. |
| Harden Sequential ID And Backlog Write Safety | AC6, AC8 | Prevent duplicate IDs or validate/retry after concurrent writes. |
| Add Migration Fixtures And Regression Tests | AC1, AC2, AC4, AC5, AC6, AC7, AC9 | Cover old helper shapes, stale artifacts, warning batching, and collision behavior. |
