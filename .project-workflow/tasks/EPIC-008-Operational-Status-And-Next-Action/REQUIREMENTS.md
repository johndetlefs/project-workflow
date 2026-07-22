# Requirements

## Summary

- Task: EPIC-008
- Title: Operational Status And Next Action
- Last updated: 2026-07-22
- Source discussion: On 2026-07-22 the owner asked to start the next portfolio item after refreshing from `origin/main`. The strategic backlog identifies BL-004 as next.

## Backlog Source

- ID: BL-004
- Title: Operational Status And Next Action
- Type: Epic Candidate
- Priority: High
- Status before promotion: Accepted
- Outcome: Make the true state of active work, workflow installation, repository schema, release or integration, evidence strength, blockers, and the next required action understandable in one interaction.
- Notes: Next product outcome after the immutable release foundation. Absorbs warning explanation and lifecycle-language usability rather than adding isolated diagnostic commands.

## User Story

As a repository owner, contributor, or coding agent arriving at a project-workflow repository, I want one trustworthy operational summary of what is installed, what work is active, what is actually proven, what is blocked, and what should happen next, so I can continue delivery without reconstructing state from several Markdown files, CLI commands, Git metadata, and external-looking claims.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: Repository owner
- Approval date: 2026-07-22
- Approval note / source: Codex conversation 2026-07-22: that sounds excellent; let's get started on that
- Approved artifact identity: sha256:94f010e6ad347b35e6fc7367f57ef26548a893d7b868a978c2e106b26823278a

## Goal

Provide one canonical, non-mutating `project status` interaction that turns existing repository-native truth into a concise operational answer and a deterministic next action.

The answer must distinguish workflow health from delivery progress, declared state from proof, completed in-repository work from integration or release, and agent-remediable work from owner decisions. It must expose the source behind each material conclusion and must say `unknown` or `not recorded` when the repository cannot prove a claim.

## Non-Goals

- Do not create a hosted dashboard, control plane, database, daemon, or background monitor.
- Do not introduce configurable solo, team, or governed assurance profiles; BL-019 owns progressive assurance and authenticated authority.
- Do not design extension/plugin boundaries or split the CLI into modules; BL-009 owns the extension platform and modular architecture.
- Do not coordinate parent workspaces or multiple repositories; BL-017 owns workspace and multi-repository coordination.
- Do not query every external Git, CI, registry, deployment, issue-tracker, or identity provider in this Epic. Status may report durable receipts or references already recorded in the repository, but must not convert them into a fresh external verification claim.
- Do not replace `.project-workflow/TRACKER.md`, Epic trackers, requirements, evidence records, acceptance maps, manifests, or release receipts with a second status store.
- Do not silently repair state, change lifecycle status, accept warnings, approve requirements, refresh evidence, merge branches, publish releases, or perform another recommended action.
- Do not remove or rename existing lifecycle statuses in the first version; explain their operational meaning and next transition while preserving compatibility.
- Do not make accepted historical warnings dominate the normal summary when they do not affect the next action, but keep their existence and review path visible.

## Users & Context

- Repository owners need to know whether work is merely drafted, approved, ready, implemented, validated, integrated, released, or blocked.
- Contributors and agents need a concrete next command or named owner decision without reverse-engineering lifecycle gates.
- Reviewers need to see why a status or next-action conclusion is justified and which artifact owns the claim.
- Existing evidence on 2026-07-22: `project doctor` provides versioned human and JSON health findings, but the top-level CLI has no `status` command. Installation identity lives in `.project-workflow/manifest.json`; execution state is split between the global tracker and Epic trackers; approval and QA evidence live in task documents; parent coverage lives in acceptance maps and audits; stronger proof lives in `EVIDENCE.json` and referenced artifacts; release identity may live in a task-local receipt; and Git integration state is separate again.
- Product risk: a passing Doctor can be mistaken for completed or delivered work, a `Complete` tracker row can be mistaken for merged or released work, and a prose claim or recorded URL can be mistaken for currently verified external state.

## Definitions

- Operational snapshot: a point-in-time, read-only projection derived from authoritative repository and Git sources, not a persisted competing status record.
- Active work: non-terminal global tracker rows plus non-terminal child rows owned by active Epics.
- Health finding: a Doctor diagnostic about workflow structure or compatibility. Health is one input to operational status, not a synonym for delivery state.
- Blocker: a condition that prevents the next valid lifecycle or delivery action. It must name the affected item, responsible party, source artifact, and remediation or decision path.
- Proof state: what the repository currently demonstrates for a claim, including missing, declared, repository-validated, or supported by a recorded external/runtime evidence artifact. This Epic reports provenance; BL-019 owns broader assurance policy and authenticated authority levels.
- Delivery state: the separately reported in-repository, integration, release, or deployment state. A later state is not inferred from an earlier one.
- Next action: the highest-priority safe step justified by current sources, expressed as an executable command when mechanical or as a named decision/evidence request when owner or external action is required.

## Requirements (Outcome-Focused)

- R1. Add `project status` as the canonical non-mutating operational summary for the current repository, with an optional work-item selector for focused diagnosis.
- R2. Build the summary as a projection over existing authoritative sources. Do not introduce a new manually maintained lifecycle or delivery-state file.
- R3. Report installed package, managed-asset, and repository-schema identity; compatibility/upgrade state; current Git branch or detached state; and whether the inspected helper can establish those facts.
- R4. Identify active global tasks, Fixes, Epics, and Epic children; explain each displayed lifecycle state in operational language; and surface conflicting, duplicate, missing, or stale ownership records instead of guessing.
- R5. Report requirements approval, readiness, implementation, QA/review, parent acceptance coverage, structured proof recipes, and referenced evidence separately so one weak or missing layer cannot be hidden by another passing layer.
- R6. Distinguish in-repository completion from branch integration, release, publication, deployment, or other external delivery. Report later delivery states only when an explicit source/receipt supports them, include that source, and otherwise report `unknown` or `not recorded`.
- R7. Reuse Doctor's finding evaluation and stable codes for workflow health, including accepted and legacy counts, without presenting a warning as the operational blocker unless it affects the selected next action.
- R8. Resolve one primary next action through documented deterministic precedence. Blocking safety or compatibility failures come first, followed by required owner decisions, missing workflow gates/evidence, the next legal lifecycle action for active work, and finally backlog selection when no execution item is active.
- R9. Every next action must identify why it was selected, the source artifacts that justify it, the responsible party (`agent`, `owner`, or `external authority`), and either an exact supported command or a concrete decision/evidence request. Status itself must never execute the action.
- R10. When multiple items are actionable at the same precedence, use a stable ordering and show concise secondary actions so repeated runs over unchanged state return the same primary answer.
- R11. Provide concise human output and a versioned JSON schema generated from the same operational model. The two formats must agree on identity, selected work, health, proof, blockers, delivery state, sources, and next action.
- R12. Fail safely on malformed or contradictory current state: return a stable finding and repair direction, retain all discoverable facts, and do not manufacture a clean summary from partial parsing.
- R13. Keep packaged CLI, generated local helper, managed agent guidance, README examples, and tests behaviorally aligned. The installed local helper must identify when its own version limits the status answer and direct the user to the canonical version-pinned upgrade path.

## Acceptance Criteria (Verifiable)

- AC1: From a valid initialized repository, one `project status` invocation returns a non-mutating summary containing installation/schema identity, Git state, selected active work, health, approval/readiness/QA/proof state, blockers, delivery state, source artifacts, and one primary next action.
- AC2: Fixture tests prove status reads the global tracker plus active Epic trackers without creating competing state, finds every non-terminal owned item, and reports duplicate, orphaned, missing, or contradictory records as stable findings rather than selecting silently between them.
- AC3: Current, stale, pre-versioned, unsupported, and helper-limited repository fixtures produce truthful package/asset/schema compatibility conclusions and exact upgrade direction consistent with `project doctor` and canonical version-pinned `project upgrade` guidance.
- AC4: Draft, unapproved, approved, ready, in-progress, testing, review, complete, deferred, and blocked work fixtures report operational meaning and the next legal gate without changing lifecycle vocabulary or mutating any workflow artifact.
- AC5: Evidence fixtures independently vary requirements approval, readiness, implementation rows, QA verdicts, parent AC coverage, `EVIDENCE.json` claims, and referenced artifacts; status reports each layer separately and never upgrades a weaker layer because another layer passes.
- AC6: A tracker-complete branch with no integration record, an integrated commit with no release receipt, a repository-recorded release receipt, and an unverified external URL produce distinct delivery conclusions. No fixture is called integrated, released, published, or deployed without the source required for that exact claim.
- AC7: A documented precedence table and regression fixtures prove that unchanged input produces the same primary next action, that blocking compatibility/safety failures outrank ordinary progress, that owner decisions are not mislabeled as agent actions, and that a supported exact command is emitted whenever the action is mechanical.
- AC8: Human and `--format json` output are projections of one model and agree across golden fixtures. JSON includes a schema version plus stable codes/fields for sources, responsible party, proof and delivery states, blockers, primary action, and secondary actions.
- AC9: Status performs no repository or Git mutation in success, warning, malformed-state, and failure fixtures; before/after tree and Git-state comparisons remain identical.
- AC10: Accepted historical warnings remain counted and inspectable but do not displace a higher-value current next action unless their underlying condition blocks it; strict/current blocking findings remain explicit.
- AC11: README and managed agent guidance teach when to use status versus Doctor, upgrade, tracker lifecycle, QA, and external verification. Packaged/local-helper parity tests, focused status tests, backlog validation, strict Doctor, and the full suite pass with the Homebrew UVX packaging test executed rather than skipped.

## Open Questions (Answer Needed)

- None in the proposed envelope. The first version intentionally uses repository-recorded Git and delivery receipts and reports unknown external state rather than adding live platform adapters.

## Decisions (Resolved)

- Use `project status` for the canonical read-only interaction; keep `project doctor` focused on structural and compatibility diagnosis.
- Produce one repository-wide answer by default and allow an optional work-item selector for focused diagnosis.
- Treat the operational answer as a derived projection, never a second status store.
- Use the current lifecycle vocabulary in machine output while adding plain-language meaning in human output.
- Report proof layers and delivery stages separately rather than collapsing them into one confidence score.
- Prefer explicit `unknown` or `not recorded` over inference from tracker completion, branch state, URLs, or prose.
- Reuse Doctor findings and compatibility logic instead of creating parallel health rules.
- Return one deterministic primary action plus concise secondary actions; do not execute them from status.
- Keep live external verification, authenticated authority, and configurable assurance policy in BL-019, and keep platform adapter architecture in BL-009.

## Validation Plan

- Create table-driven repository fixtures covering new/current, stale, pre-versioned, unsupported, malformed, contradictory, helper-limited, and accepted-warning states.
- Create lifecycle fixtures for standalone tasks, Fixes, Epics, and Epic children at every supported stage, including no active work and multiple equally actionable items.
- Independently vary approval, implementation, QA, parent coverage, structured claim, evidence-artifact, integration, and release-receipt state to prove the model does not collapse distinct claims.
- Snapshot human and JSON outputs from the same fixtures and assert semantic equivalence, stable ordering, stable codes, source paths, responsible parties, and exact supported commands.
- Hash repository files and capture Git state before and after every status path to prove non-mutation.
- Run focused tests, packaged/generated helper parity checks, backlog validation, `project doctor --strict`, `git diff --check`, and `PATH="/opt/homebrew/bin:$PATH" .venv/bin/pytest -q` with the UVX packaging test passing rather than skipping.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Define Operational Status Read Model And Source Precedence | AC1, AC2, AC5, AC6, AC8 | Define the shared typed projection, authoritative source map, contradictions, proof layers, delivery stages, and versioned JSON contract. |
| Add Installation, Git, And Active-Work Inspection | AC1, AC2, AC3, AC4, AC9 | Read manifest/compatibility, helper capability, Git state, global tracker, Epic trackers, and lifecycle meaning without mutation. |
| Add Proof, Health, And Delivery-State Classification | AC1, AC5, AC6, AC10 | Reuse Doctor evaluation and classify approval, readiness, QA, coverage, structured evidence, integration, and receipt-backed delivery without overclaiming. |
| Build Deterministic Next-Action Resolver | AC4, AC7, AC10 | Implement documented precedence, responsibility, reasons, exact mechanical commands, owner/external requests, stable tie-breaking, and secondary actions. |
| Deliver Human And JSON Status CLI With Packaged Parity | AC1, AC8, AC9, AC11 | Add the command, focused selector, concise rendering, safe failures, packaged/generated helper parity, and CLI regression coverage. |
| Document And Prove End-To-End Operational Journeys | AC2, AC3, AC4, AC5, AC6, AC7, AC9, AC10, AC11 | Exercise realistic repository histories, verify non-mutation and truthful next actions, and document how status relates to existing commands and external verification. |
