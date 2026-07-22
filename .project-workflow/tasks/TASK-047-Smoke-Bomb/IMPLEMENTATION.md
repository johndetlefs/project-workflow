## User Story

As an agency or freelance maintainer handing a project to a client, I want to create and review a sanitized branch and export it as a self-contained ZIP, so that the client receives the working project without agency-only workflow baggage and can immediately continue with people or their preferred coding agent.

## Goal

Deliver one safe `project smoke-bomb` path from a reviewed agency worktree to a validated, deterministic client ZIP while preserving useful client README and agent context and leaving the authoritative repository history untouched.

## Approach

- Reuse the upgrade system's plan fingerprint, clean-worktree precondition, safe-target checks, and byte/mode rollback concepts without coupling Smoke Bomb lifecycle to repository upgrade state changes.
- Separate agent judgment from executable guarantees: the `project-smoke-bomb` skill prepares and reviews client-facing context, while the CLI inventories ownership, blocks ambiguity, applies only reviewed transformations, runs explicit validation commands, and exports the exact validated file set.
- Build the ZIP from git's tracked and non-ignored worktree inventory after apply, never from `.git` or an unconstrained recursive directory walk.
- Treat supported client agents as output adapters around one useful canonical client guidance source; remove only provably generated project-workflow agent assets and delimited managed blocks.

## Phases

1. Plan and safety model: define deterministic plan/result schemas, repository and branch identity, ownership classifications, blockers, CLI arguments, and human/JSON output.
2. Sanitization: plan and transactionally apply project-workflow state removal, managed-block transformations, and client-agent instruction adapters with exact preservation and rollback.
3. Validation and export: run reviewed commands, verify guidance and residual references, inventory safe files, and build a deterministic ZIP and manifest.
4. Product integration: add the generated skill, help and README guidance, mirror parity, fixtures, regression coverage, and complete repository validation.

## Acceptance Criteria

- [x] AC1: Planning is deterministic and non-mutating, identifies repository/default-branch risk, and fingerprints the reviewed inputs and actions.
- [x] AC2: The plan exposes exact ownership, guidance, archive, blocker, and validation decisions before mutation.
- [x] AC3: Apply removes only reviewed project-workflow assets and preserves all adjacent user content and repository history.
- [x] AC4: Unsafe, dirty, stale, ambiguous, unconfirmed, or conflicting states fail before mutation with actionable evidence.
- [x] AC5: Mid-apply failures restore exact touched bytes and modes and report rollback status.
- [x] AC6: Post-apply checks prove guidance usefulness, validation success, removal boundaries, archive safety, and classified residual references.
- [x] AC7: Export produces a fingerprint-bound deterministic ZIP and matching machine result without further repository mutation.
- [x] AC8: All four supported agent surfaces, distribution mirrors, documentation, focused tests, and full repository gates pass.

## Validation

- AC1-AC2: Focused plan and JSON-schema assertions over unchanged, default-branch, dedicated-branch, ambiguous, and repeated fixtures.
- AC3-AC5: Exact before/after byte and mode assertions plus injected precondition and rollback failures for every supported source-agent surface.
- AC6-AC7: Real subprocess validation, guidance/link/reference checks, ZIP inventory/SHA assertions, ignored/secret/symlink exclusions, and repeat-export equivalence.
- AC8: Source/template/local parity, generated-skill and package-resource checks, compilation, backlog validation, strict Doctor, and full pytest with explicit Homebrew UVX PATH.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Deterministic handoff plan | Add the Smoke Bomb command contract, repository/default-branch identity, client-agent and validation inputs, exact ownership/actions/blockers, archive intent, fingerprint, and human/JSON preview. | AC1, AC2, AC4: repeated preview is non-mutating and identical; unsafe or ambiguous inputs are actionable blockers. | Run `project smoke-bomb --plan --format json` twice on an unchanged initialized fixture and compare fingerprints and worktree state. | Done |
| 2 | Ownership-safe sanitization | Plan and apply exact project-workflow directory, generated-agent asset, and managed-block removal while retaining or producing reviewed client README and selected agent entry points. | AC2, AC3, AC4: every destructive action has ownership evidence; adjacent user bytes and other branches remain intact. | Review the planned diff, apply it on fixtures for Codex, Claude Code, Cursor, and Copilot, then compare canaries and git history. | Done |
| 3 | Transactional apply and rollback | Bind apply to the reviewed fingerprint and clean state, require confirmation, reject stale or unsafe targets, and restore bytes and modes after injected failures. | AC3, AC4, AC5: apply is exact, precondition failures do not mutate, and partial failures roll back completely. | Run stale-plan, dirty-worktree, symlink, missing-confirmation, and injected-failure tests and inspect rollback results. | Done |
| 4 | Validated deterministic ZIP | Automatically run only reviewed validation commands, verify client guidance and sanitized boundaries, inventory git-visible safe files, and export a deterministic ZIP plus machine-readable identity. | AC6, AC7: failed validation blocks export; successful ZIP excludes `.git`, ignored/transient/unsafe content, matches inventory and SHA, and repeats equivalently. | Inspect ZIP entries and manifest, rerun export unchanged, and intentionally fail validation and secret/symlink fixtures. | Done |
| 5 | Agent workflow and distribution | Add the `project-smoke-bomb` skill, README/help guidance, package resources, maintained CLI mirrors, and cross-agent regression coverage. | AC8: the product surface is usable from canonical install and initialized repositories, with all parity and repository gates passing. | Run focused tests, CLI help, package-resource checks, `cmp`, compilation, backlog validation, strict Doctor, and full pytest with UVX available. | Done |

## Implementation Evidence

- 2026-07-22: 17 focused Smoke Bomb tests passed across Codex, Claude Code, Cursor, and GitHub Copilot source/client surfaces, including deterministic planning, default-branch warning, exact archive inventory, rollback, stale fingerprints, validation failure, validation-time mutation, dirty state, residual references, secret-like files, unsafe targets, parent symlinks, unmarked generated files, preservation of short user content, and repeat-export identity.
- 2026-07-22: `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q` passed all 149 tests with the UVX packaging path available.
- 2026-07-22: canonical source, packaged template, and checked-in local helper are byte-identical; packaged and local Smoke Bomb skills and development prompt mirrors are byte-identical.
- 2026-07-22: compilation, backlog validation, strict Doctor, and `git diff --check` pass.
- 2026-07-22: a manual agency-style demo repository was committed on `main` at `9f3d5d88b8618a847e971ed9be174c80643ccad9`, branched to `smoke-bomb/demo-client`, planned without mutation, and applied with reviewed fingerprint `681f97569dc59214f386cf3230027b194520bbc08c8bef86c16c579898fad558`. The exported ZIP SHA-256 was `c1b35de0ddc687fe53a07499d509d44567823d56ccf2db178074d0dea865ba10`; its exact seven-file inventory matched the plan, contained useful `README.md`, `AGENTS.md`, and `CLAUDE.md`, contained no Git or project-workflow residue, and passed both application tests after independent extraction. The disposable branch showed only the reviewed sanitization diff while `main` retained the full workflow manifest and generated Smoke Bomb skill at the unchanged source commit.

## QA & Code Review

- Date: 2026-07-22
- Reviewed areas: deterministic plan and fingerprint integrity; destructive target ownership; mixed-file and short user-content preservation; parent/final symlink containment; transactional replacement rollback; reviewed shell-command execution; validation-time mutation detection; privacy of validation evidence; Git-visible archive inventory; secret-like and residual-reference blockers; deterministic ZIP identity; all supported source/client agent surfaces; packaged/local distribution parity; README and generated skill/prompt guidance.
- Acceptance evidence: AC1-AC2 pass through repeated non-mutating JSON plans, exact action/inventory assertions, default-branch warning, ownership/source fields, and pre-apply blocker fixtures. AC3-AC5 pass through all-agent apply fixtures, byte/mode and Git-head canaries, dirty/stale/unsafe/unowned target rejection, and injected rollback. AC6-AC7 pass through explicit subprocess validation, failed-validation/no-ZIP behavior, post-validation hash checks, exact inventory, `.git` and workflow exclusion, SHA-256 verification, and repeat-export equivalence. AC8 passes through 17 focused tests, all 149 repository tests with Homebrew UVX available, CLI help, compilation, four byte-for-byte mirror checks, backlog validation, strict Doctor, and `git diff --check`.
- Privacy and security evidence: validation stdout/stderr content is not emitted in the machine result; only byte counts and SHA-256 hashes are retained. Shell commands are only the explicit commands embedded in the owner-reviewed fingerprint. Known secret-like paths and symlink/unsafe targets block before apply. The documented non-goal correctly avoids representing Smoke Bomb as a legal, licensing, security, or DLP audit.
- Manual end-to-end proof: the 2026-07-22 Northstar demo exercised the actual clean-branch → reviewed plan → fingerprinted apply → automatic validation → ZIP → independent extraction and retest journey. The demo ZIP remains at `/private/tmp/project-workflow-smoke-bomb-demo.hGWM74/northstar-client-handoff.zip` with its extracted inspection copy beside it.
- Deferred real-client proof: the 2026-07-23 client repository has not yet been run through plan/apply/export. That target-specific record is still required before claiming the real client handoff itself complete; the synthetic demo proves the product journey but is not a substitute for client-specific security, legal, content, or delivery review.
- Findings: No blocking findings. Review hardening found and resolved development-prompt mirror drift, raw validation-output leakage, short user-agent-file overwrite risk, parent-symlink escape risk, and validation-time mutation of an already planned output.
- Verdict: Pass

## Retro

- Date: 2026-07-22
- Reusable lessons: Broad fixture coverage did not by itself prove the exact operator story the owner described. Destructive and export workflows need both automated edge-case coverage and a realistic disposable-repository journey with the resulting artifact independently inspected. The useful product boundary is the validated client ZIP and its agent onboarding, not merely successful removal of internal files.
- Conventions or agent assets updated: Added the manual-journey proof distinction to `.project-workflow/guidance.md`; added the packaged/local `project-smoke-bomb` skill, Copilot prompt, README command contract, CLI help, and target-agent handoff adapters during implementation.
- Follow-up tasks: None from missed TASK-047 scope. The real 2026-07-23 client handoff remains an operational use of the completed feature, not a substitute product task.
- Missed in-scope work: None. The initially missing manual demo proof was completed before closeout and recorded in QA evidence.

## Notes

- Task: TASK-047
- Title: Smoke Bomb
- Created: 2026-07-22
