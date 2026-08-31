# Requirements

## Summary

- Task: TASK-103
- Title: Prove Cross-Host Conformance And Delivery Boundary
- Parent AC Coverage: AC5, AC6, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15, AC16
- Last updated: 2026-08-31
- Intent contract: full

## Intent

Prove that the released Project Workflow execution controls can be installed and used through real supported Codex and Claude Code journeys, with bounded execution, truthful host status, and retained receipts. Make the Codex path usable first without weakening the approved cross-host outcome or confusing repository-local Project Workflow skills with a permanently active marketplace plugin.

## Intent Spine

- OC1 — Completion capability: An operator can install or upgrade the released package, establish a sealed execution envelope through a supported path, run material work under the selected host adapter, and receive a finite passing or precisely blocked receipt.
- OC2 — Material capabilities: Exact-package install and upgrade journeys, current-host capability diagnosis, successful and interrupted real canaries, cross-host state and receipt conformance, recurrence proof, and explicit delivery-layer accounting.
- OC3 — Success journey: A disposable repository installs the retained release, loads the correct host assets, proves no-op upgrade and disable behaviour, runs `project execute` through a verified current host, changes only sealed paths, stops at its limits, and retains an input-bound core receipt.
- OC4 — Successful-but-wrong result: Package presence, a plugin listing, repository-local skill discovery, mocked hooks, or one unrestricted canary appears green while the released operator journey remains unusable, inactive, unbounded, or falsely advertised.
- OC5 — Exclusions: No permanent global Project Workflow skill duplication, no always-on unsealed execution hook, no unsupported-host claim, no second workflow owner, and no inferred push, merge, publication, portfolio rollout, or owner acceptance.
- OC6 — Assumptions: Current Codex supports local skills, plugins, App Server, and lifecycle hooks; persistent plugin hooks require separate trust, while Project Workflow's material control is activated only inside a sealed `project execute` run. Claude remains unsupported until its exact executable, authentication, hooks, permissions, and runtime canary pass.
- OC7 — Authority source: Parent Epic intent and approved decomposition row, reinforced by the owner's 2026-08-31 instruction to move forward and get the integration running properly.

## Owner Approval

- Intent reviewed and accurately reflected: Yes — inherited unchanged from the approved parent Epic envelope
- Requirements reviewed by owner: Yes — inherited unchanged from the approved parent Epic envelope
- Acceptance criteria reviewed by owner: Yes — inherited unchanged from the approved parent Epic envelope
- Approved for decomposition: Yes — matching approved child row
- Approved for implementation: Yes — matching approved child row and explicit owner continuation
- Approved scope envelope: Parent Epic AC5, AC6, AC8-AC16 with Codex-first sequential execution
- Approved by: John Detlefs
- Approval date: 2026-08-31
- Approval note / source: Parent Epic approval plus “move forward ... have it all up and running properly as quickly as possible”
- Approved artifact identity: Inherited from the current parent Epic intent audit; refresh after this child plan is recorded

## Child Charter

- Project Workflow remains the sole workflow authority and shared-state writer.
- Direct cheap work uses zero model calls; material work uses supported, sealed host execution.
- A worker cannot amend its own source, scope, permissions, limits, required proof, or release authority.
- Limits are finite, use host-native units, and block rather than waive remaining obligations.
- Implementation, verification, QA, delivery, and release candidates remain distinct proof layers.
- One independent QA findings set is produced for the candidate; repeat review loops and candidate repair during release are prohibited.
- No-progress retries are denied and unsupported host capabilities fail closed with a precise blocker.
- Codex and Claude Code are the minimum conformance targets, but one unavailable host does not falsify independently proven behaviour on the other.
- Runtime adapters and managed host assets are package-owned and generated copies must remain in parity.

### Invalid Substitutes

- A plugin-list entry without a usable sealed execution journey.
- Permanent global skill duplication or an always-on hook merely to make the integration appear installed.
- Static, mocked, or package-presence evidence in place of a real host journey.
- One successful edit as proof of interruption, aggregate-limit, or release behaviour.
- Treating a missing Claude runtime as a Codex failure, or treating a passing Codex run as Claude proof.
- Repeat QA, candidate churn, release repair, or unit normalisation that hides native host semantics.
- Strategic Advisor or another workflow becoming the owner of Project Workflow code or state.

## Goal

Turn the shipped execution-control implementation from package and test evidence into an operator-usable, current-host journey with exact-candidate proof.

## Non-Goals

- Publishing a universal marketplace plugin.
- Replacing repository-local Project Workflow skills with a global copy.
- Claiming Claude support before its real host proof passes.
- Push, merge, publication, portfolio rollout, or owner acceptance without separate authority.

## Users & Context

The owner and Project Workflow adopters need a public, inspectable way to establish execution authority and run the packaged adapters without manually fabricating internal JSON or hashes.

## Repository Scope

- Primary repository: `.`
- Additional proof surfaces: disposable temporary repositories containing no durable workflow truth.

## Requirements (Outcome-Focused)

- R1 — Document and enforce the correct Codex installation model: repository-local skills and managed CLI assets for normal workflow use, with the execution-control hook activated ephemerally only by a sealed `project execute` run.
- R2 — Provide a supported, inspectable, host-neutral operator path to create or diagnose sealed execution authority without private APIs, hand-computed hashes, or manual coordination-state fabrication.
- R3 — Prove fresh install, upgrade, no-op upgrade, disable, re-enable, asset parity, Doctor, and status behaviour from the exact package candidate for each supported host.
- R4 — Run real current-host success and interruption canaries with scope enforcement, aggregate limits, hook observations, and retained input-bound receipts.
- R5 — Prove shared cross-host state and receipt semantics while retaining native host units and truthful unsupported states.
- R6 — Prove recurrence proportionality: zero model calls for direct cheap work, no pre-promotion churn, one QA lineage, one delivery candidate, and terminal release behaviour.
- R7 — Maintain an explicit ledger separating source, automated, package, host-runtime, integration, release, adoption, and owner-acceptance proof.
- R8 — Report an unavailable host as a precise blocker while allowing independently supported host work to progress.

## Acceptance Criteria (Verifiable)

- AC1: Source, package metadata, and operator documentation agree on the Codex installation and activation model; a marketplace plugin listing is neither required nor accepted as runtime proof. Covers parent AC12, AC14, and AC16.
- AC2: From the exact package candidate, a disposable Codex repository can complete fresh install, upgrade, no-op upgrade, disable, re-enable, parity, Doctor, status, authority configuration, and execute preflight without manual internal-state fabrication. Covers parent AC13 and AC16.
- AC3: Current Codex completes one real successful canary and one real interrupted canary with verified hooks, native aggregate accounting, sealed scope, and retained core receipts. Covers parent AC8, AC9, and AC12.
- AC4: Claude Code completes the equivalent exact-package journey and canaries, or the task retains a current precise unsupported-capability blocker without weakening Codex proof. Covers parent AC10, AC12, and AC13.
- AC5: Codex and Claude Code share canonical lifecycle, terminal-state, observation, limit, and receipt semantics while retaining native host units. Covers parent AC11.
- AC6: A recurrence harness proves the proportionality and terminal-delivery invariants without repeated QA or candidate churn. Covers parent AC5, AC6, AC8, and AC15.
- AC7: Retained artifacts identify the exact source, package, configuration, prompt, host executable, limits, changed paths, observations, receipts, and delivery layer for every material claim. Covers parent AC14 and AC16.

## Open Questions (Answer Needed)

None. Host availability is an observed capability result, not an unresolved product decision.

## Decisions (Resolved)

- Execute Codex proof first and reconcile Claude independently.
- Keep the subordinate hook ephemeral and sealed; do not add a permanently active global hook.
- Add the smallest host-neutral configuration or diagnosis surface required to remove manual state fabrication.
- Produce one independent QA findings set for the frozen candidate.

## Validation Plan

- Focused unit and integration tests for configuration, sealing, diagnosis, adapters, limits, and receipts.
- Exact wheel and source-distribution build with managed-asset parity checks.
- Disposable fresh-install, upgrade, no-op, disable, re-enable, Doctor, and status journeys.
- Real current Codex success and interruption canaries.
- Current Claude executable, authentication, hook, permission, and runtime probe followed by canaries when supported.
- Cross-host conformance and recurrence harnesses.
- One locked full regression run and one independent QA review of the frozen candidate.
