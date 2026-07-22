# Requirements

## Summary

- Task: TASK-047
- Title: Smoke Bomb
- Last updated: 2026-07-22

## Backlog Source

- ID: BL-018
- Title: Smoke Bomb
- Type: Task Candidate
- Priority: High
- Status before promotion: Accepted
- Outcome: Provide a deliberate, previewable, and recoverable repository handoff that removes proven project-workflow-owned internals while preserving the client-facing context future people and agents need to continue safely.
- Notes: Immediate execution priority for the 2026-07-23 client handoff. One-repository task: dry-run, ownership-safe cleanup, retained guidance, transactional apply, and post-cleanup proof.

## Overview

Smoke Bomb prepares a sanitized client handover from an agency- or freelancer-owned git repository. A maintainer normally creates a disposable handoff branch, reviews and applies the cleanup there, validates the sanitized tree, and exports that exact tree as a ZIP without git history or agency-only workflow state. The agency's normal branches remain the authoritative full repository.

The client deliverable is not a stripped bare codebase. It must retain the product, a useful human README, and conventional agent instructions containing enough verified project context for the client's chosen coding agent to orient itself and continue safely.

## User Story

As an agency or freelance maintainer handing a project to a client, I want to create and review a sanitized branch and export it as a self-contained ZIP, so that the client receives the working project without agency-only workflow baggage and can immediately continue with people or their preferred coding agent.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: No
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: Repository owner
- Approval date: 2026-07-22
- Approval note / source: Codex task response on 2026-07-22: 'Yep, that's perfect. Let's go. Let's get started on that, please.'
- Approved artifact identity: sha256:0c1105622344ac75ba8e3338df2ae8efb77595af6d8f9002c3d22cc45264aabf

## Goal

Let a maintainer produce a validated, self-contained client ZIP from a disposable sanitized view of an agency-owned repository without damaging the authoritative repository or losing the practical context needed for people and general-purpose coding agents to continue safely.

## Non-Goals

- General source-code cleanup, refactoring, or client-delivery preparation beyond project-workflow handoff.
- Rewriting git history, changing remotes, deleting branches, or cleaning more than one repository in one transaction.
- Requiring, creating, pushing, merging, or deleting a Smoke Bomb branch automatically; a dedicated branch is the recommended operating pattern but remains under normal git ownership.
- Removing user-authored guidance merely because it mentions project-workflow.
- Hiding historical project-workflow references that are useful, immutable, or outside the current worktree.
- Replacing the client's issue tracker, documentation system, or preferred agent workflow.
- Making the cleanup irreversible or applying it without review of the exact target state.
- Treating the sanitized ZIP as a replacement for the agency's full repository, history, or contractual archival obligations.
- Guaranteeing that the project contains no secrets, licensed material, personal information, or client-inappropriate intellectual property; Smoke Bomb must block known unsafe paths and unresolved findings, but it does not replace security, legal, or data-loss-prevention review.

## Users & Context

- Primary user: an agency or freelance maintainer preparing a sanitized copy of a repository for a client who should not inherit project-workflow's internal planning state, local CLI, generated skills, prompts, rules, git metadata, or other agency-only delivery material.
- Continuing users: client developers and coding agents who still need concise repository purpose, setup, architecture pointers, validation commands, delivery notes, and known follow-up work after project-workflow is gone.
- Source-of-truth context: the agency-owned repository and its normal branches remain intact. A dedicated Smoke Bomb branch is recommended as a disposable, reviewable cleanup surface, but the workflow does not make branch policy decisions for the user.
- Deliverable context: the primary client artifact is a ZIP of the validated sanitized worktree, not the branch or `.git` repository itself.
- Immediate context: the first real handoff is planned for 2026-07-23, so the workflow must be safe enough for a real repository while remaining deliberately narrow.

## Requirements (Outcome-Focused)

- Provide a public `project smoke-bomb` workflow and a generated `project-smoke-bomb` agent skill that guide the same supported behavior; the command remains the source of executable truth.
- Operate on exactly one git worktree root per run and refuse to plan, apply, or export when repository identity is ambiguous.
- Produce a deterministic, non-mutating plan before any cleanup. The plan must identify the repository commit and current branch, whether that branch appears to be the repository's default branch, selected client agent targets, every proposed deletion or managed-block transformation, every retained or generated handoff artifact, archive exclusions, blockers, validation actions, and a fingerprint over the reviewed inputs and actions.
- Recommend a dedicated branch such as `smoke-bomb/<client-or-handoff>` and prominently warn when running on the detected default branch, but do not create or enforce branch naming, commits, pushes, merges, or deletion.
- Classify a deletion as safe only when project-workflow ownership is established by a known managed path, an exact generated asset or managed marker, and—where project-workflow supports user modification or mixed ownership—content-aware preservation rules. Path naming alone is not sufficient for ambiguous or mixed-ownership files.
- Remove project-workflow's internal state and locally generated execution surface when ownership is proven, including `.project-workflow`, the local helper, generated `project-*` agent assets for the selected mode, and project-workflow-managed host-file blocks. Remove empty generated directories only when doing so cannot affect user-owned content.
- Preserve all content outside the approved plan. For mixed-ownership host files such as `AGENTS.md` or agent instruction files, remove only the delimited project-workflow block and preserve surrounding bytes apart from the minimum newline normalization required by that transformation.
- Preserve or produce a useful client-facing `README.md` covering the repository's purpose, setup, important architecture pointers, validation and delivery commands, and known operational constraints. Preserve useful existing README content and require explicit review of proposed transformations; do not replace it with a generic template or invent missing operational knowledge.
- Preserve or produce at least one conventional client-facing agent instruction file for the client agent targets selected in the reviewed plan. The instructions must contain concise verified repository context, important paths, working and validation commands, safety constraints, and continuation notes, without project-workflow lifecycle instructions or agency-only planning history.
- Support common client agent conventions—including `AGENTS.md` for Codex-compatible use and the relevant native instruction surface for Claude Code, Cursor, or GitHub Copilot—without forcing every agent's files into every ZIP. Shared guidance should have one canonical client-facing source with thin target-specific entry points where practical.
- Derive client-facing guidance only from retained repository artifacts and reviewed project-workflow guidance. The plan must show the source of each synthesized section and surface missing or conflicting knowledge for human resolution before apply.
- Make apply an explicit second step that requires a clean worktree, the reviewed plan fingerprint, and interactive confirmation; authorized non-interactive agents must additionally pass `--yes`. A stale plan, changed branch or commit, changed target content, unsafe target, symlink, unreadable file, or unresolved ownership conflict must block before mutation.
- Apply the approved transformations as one recoverable transaction. If any write, delete, or validation precondition fails during mutation, restore the exact pre-apply bytes and modes for every touched path and report whether rollback succeeded.
- After successful apply and validation, export the exact sanitized worktree as a deterministic ZIP at an explicit output path. The archive must exclude `.git`, the archive itself, project-workflow internals, agency-only files identified by the reviewed plan, ignored transient/build/secret material unless explicitly included, and any path outside the repository root.
- Include an archive manifest in the machine-readable result with the source repository identity, reviewed plan fingerprint, sanitized tree state, archive path and SHA-256, included path inventory, exclusions and reasons, selected client agent targets, and validation result. Do not embed confidential source content in the result.
- Refuse export if the sanitized worktree differs from the applied and validated plan, required client guidance is missing or unresolved, an unsafe file type or secret-safety blocker is detected, validation has failed, or the output path could be included recursively in the archive.
- Be idempotent: after successful apply, repeated validation and export of the unchanged sanitized tree must make no repository changes and must produce the same archive contents and manifest identity.
- Report a concise human result and a machine-readable result containing repository identity, plan fingerprint, branch warning state, applied actions, retained or blocked paths, client guidance, validation results, rollback state, archive identity, and residual project-workflow references.
- Validate the final handoff state without treating string absence alone as proof: confirm planned paths and managed blocks are gone, retained canary files are byte-identical, client README and agent instructions contain no unresolved placeholders or broken introduced links, git reports only the reviewed handoff diff, configured target-repository validation commands pass, the ZIP contains exactly the validated allowed inventory and no `.git` metadata, and any remaining project-workflow references are explicitly classified as retained client-useful content.
- Keep canonical source, packaged templates, checked-in local helper, generated agent assets, documentation, and regression coverage aligned under the repository's existing distribution invariants.

## Acceptance Criteria (Verifiable)

- AC1: On a clean initialized fixture containing generated assets, mixed-ownership host instructions, user-modified workflow guidance, user canaries, product files, and an agency-owned default branch, `project smoke-bomb` produces a deterministic plan with no worktree mutation, warns without blocking on the default branch, and returns an identical fingerprint on an unchanged second run.
- AC2: The plan lists repository and branch identity, client agent targets, exact delete and transform actions, proposed README and agent-instruction changes, archive inclusions and exclusions, ownership and derivation evidence, retained files, blockers, and validations; ambiguous ownership or conflicting client guidance is preserved and blocks apply with a concrete resolution.
- AC3: Applying the exact reviewed fingerprint on a dedicated handoff branch removes only proven project-workflow-owned files and managed blocks, preserves user canaries and surrounding mixed-file content, writes the reviewed client-facing README and selected agent instructions, and leaves git with exactly the planned diff without altering any other branch or repository history.
- AC4: Dirty-worktree, wrong-root, stale-fingerprint, changed-content, symlink, unreadable-target, missing-confirmation, and unresolved-conflict cases fail before mutation with actionable output.
- AC5: An injected failure after mutation begins restores all touched paths, bytes, and executable modes; the result identifies rollback success or any path that could not be restored.
- AC6: Post-apply validation proves removal of planned assets and blocks, byte preservation of retained canaries, useful resolved README and client-agent instructions, successful configured repository checks, exact archive inventory, absence of `.git`, secret-safety and transient exclusions, and explicit classification of any residual project-workflow references.
- AC7: Export produces a client ZIP and machine-readable manifest bound to the reviewed plan and validated sanitized tree, with a SHA-256 and selected client agent targets; repeated export of the unchanged tree produces equivalent archive contents and makes no repository changes.
- AC8: Codex, Claude Code, Cursor, and GitHub Copilot fixtures prove the selected client-facing instruction surface remains useful while project-workflow-generated surfaces and adjacent user content are handled correctly; focused tests, source-template-local parity, archive-safety checks, backlog validation, strict Doctor before cleanup, full tests with the UVX packaging path enabled, compilation, and diff checks pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- This is a Task because it delivers one coherent repository-handoff outcome; workspace-wide and multi-repository cleanup remains outside scope.
- “Smoke Bomb” is the deliberate product name. The executable entry point is `project smoke-bomb`, and the agent-facing skill is `project-smoke-bomb`.
- The agency-owned repository remains authoritative. A disposable Smoke Bomb branch is the recommended review surface, but branch creation and policy remain ordinary user-controlled git operations.
- The primary client deliverable is a validated ZIP of the sanitized worktree without `.git` metadata, not transfer of the agency repository or its Smoke Bomb branch.
- A useful README and at least one client-selected conventional agent instruction file are required deliverables. `HANDOFF.md` is not mandatory; additional handoff documentation is created only when the reviewed repository context warrants it.
- Smoke Bomb automatically runs only the target repository validation commands explicitly included in the reviewed plan and refuses ZIP export if any command fails; it never infers or silently adds arbitrary commands.
- Preview and apply use the versioned upgrade system's proven deterministic-plan, reviewed-fingerprint, clean-worktree, and transactional rollback principles rather than a separate destructive-action model.
- Useful repo-specific knowledge is extracted into client-facing guidance before internal workflow state is removed; deletion without a usable continuation artifact is not success.
- Repository-local fixture evidence is required for implementation correctness. A real client repository dry-run and apply record is required before claiming the immediate client handoff itself complete, but client content must not be committed to this repository.

## Validation Plan

- Build isolated git fixtures for each supported source and client agent mode with default and dedicated branches, generated, user-owned, mixed-ownership, ambiguous, dirty, stale-plan, symlink, rollback-failure, secret-like, ignored-transient, unsafe-file-type, archive-output, and already-clean states.
- Assert plan payloads and fingerprints, branch warnings, exact before/after path bytes and modes, failure timing, rollback restoration, README and client-agent usefulness, archive inventory and SHA-256, `.git` absence, idempotence, residual-reference classification, and machine/human result agreement.
- Run focused Smoke Bomb tests, source/template/local parity and compilation checks, `./.project-workflow/cli/workflow backlog validate`, strict Doctor before cleanup, and `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q` so the packaging test cannot silently skip for PATH reasons.
- For the 2026-07-23 target repository, capture repository root, dedicated handoff branch, source commit, clean precondition, selected client agent targets, reviewed plan fingerprint, explicit owner apply confirmation, post-apply validation, final diff, archive SHA-256 and inventory summary without copying confidential client content into project-workflow evidence.
