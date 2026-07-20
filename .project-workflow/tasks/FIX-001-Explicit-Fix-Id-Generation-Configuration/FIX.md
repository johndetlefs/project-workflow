# Fix

## Summary

- Fix: FIX-001
- Title: Explicit Fix ID Generation Configuration
- Status: Complete
- Created: 2026-07-20

## Report

- Observed or requested: The repository's legacy config does not explicitly declare the Fix ID-generation policy.
- Expected: The config explicitly lists `fixes` alongside tasks, epics, and backlog using the repository's current sequential policy.
- Affected users or systems: Maintainers and agents reading `.project-workflow/config.json` to understand ID allocation.
- Delivered baseline: TASK-038 added Fix ID generation with a backward-compatible sequential default when the key is absent.
- Report evidence: `.project-workflow/config.json` lists tasks, epics, and backlog but omits `fixes`; the shipped schema supports all four kinds.

## Routing

- Decision: Fix
- Rationale: This is one bounded post-completion configuration-clarity correction against the TASK-038 delivered baseline.
- Related work state: TASK-038 is Complete
- Bounded correction: Yes; add one explicit config key without changing allocation behavior.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Change Request
- Mode: Normal
- Severity: Low
- Impact: The omitted key can make maintainers reasonably question whether Fix IDs support configurable generation.
- Urgency: Normal maintenance; no runtime failure or data-loss risk.
- Owner: Repository owner

## Related Work

- Originating work: TASK-038
- External links: Commit `cd2b16c`

## Risk

- Risk level: Low
- Risks: A malformed JSON edit could prevent config loading; changing the value could unintentionally alter ID allocation.
- Rollback or containment: Keep the existing `sequential` behavior and revert the single key if validation fails.

## Fix Plan

- Scope: Add `"fixes": "sequential"` to this repository's `id_generation` object.
- Non-goals: Do not switch any work-item kind to unique IDs or change allocator behavior, defaults, templates, or documentation.
- Affected target: `.project-workflow/config.json` in the project-workflow repository.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Branch `codex/FIX-001-explicit-fix-id-generation-config`; direct main push authorized; evidence recorded below.
- Verification plan: Parse through strict doctor, run the focused unique-ID generation test, and confirm the diff changes only the explicit config policy plus Fix records.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | codex/FIX-001-explicit-fix-id-generation-config | None | strict doctor and focused pytest evidence in this record |

## Verification

- Delivered scope: Added the explicit `"fixes": "sequential"` policy to this repository's existing `id_generation` object; no allocator code or defaults changed.
- Verification result: Strict doctor parsed the updated config and reported no issues; the focused unique-ID generation test passed.
- Adjacent behavior checked: The focused fixture exercised unique task, epic, Fix, backlog, and promoted-task allocation together.
- Original acceptance criteria result: TASK-038 AC3, AC12, and AC26 remain satisfied; the change documents existing Fix allocation behavior without changing it.
- Regression evidence: `.venv/bin/pytest -q tests/test_doctor.py -k unique_id_generation_for_task_epic_backlog_and_promotion` passed 1/1; `git diff --check` passed.
- Residual risk: The existing related-work URL parser can mistake dashed repository slugs for workflow IDs; that separate validator issue was not introduced or expanded into this config-only Fix.

## Outcome

- Disposition: Fixed
- Decision: Explicit Fix ID-generation policy recorded without changing allocation behavior.
- Closed by: Codex on owner authorization
- Closed date: 2026-07-20
- Promoted to: None
