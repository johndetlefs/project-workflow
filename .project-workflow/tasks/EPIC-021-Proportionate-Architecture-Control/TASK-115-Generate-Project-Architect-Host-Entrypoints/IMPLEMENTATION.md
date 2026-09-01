## User Story

As a Project Workflow host user, I want Codex and Claude Project Architect entrypoints generated
from one source, so that host discovery cannot create competing architecture semantics.

## Parent AC Coverage

- AC3, AC4, AC9, AC10, AC11

## Architecture Impact

- Classification: material
- Reason: This task adds a canonical semantic source, generated host adapters, packaged assets and CI parity enforcement.
- Architecture authority: docs/architecture.md
- Authority identity: sha256:f8327a14f96b2765b7e99eb744d218d0e0076cbec66ea3632761cb0a9cbe7737
- Architect invocation: project-architect:codex:01a05b1c-f694-7fc2-8346-0316d5564e83
- Architect decision identity: sha256:9409ca8ea215738fedc8dd2a44b824c46300ee3e9e9072999985ebfba16b50fe
- Affected boundaries: prompt ownership; Codex skill discovery; Claude agent discovery; package assets; CI checks.
- Architecture decision: Author semantics only in Architect.prompt.md and deterministically generate all host derivatives.
- Measurable constraints: Byte-current generated outputs, shared semantic clauses, init discovery and distinct real-host receipts.
- Conformance plan: Run generator drift tests, both init journeys and separate authenticated host canaries.

## Acceptance Criteria

- [x] AC1: One canonical source deterministically generates both host formats and one-copy drift fails.
- [x] AC2: Codex and Claude init fixtures install discoverable, semantically equivalent entrypoints.
- [x] AC3: Real Codex discovers and invokes the repository-installed `$project-architect`.
- [x] AC4: Claude executable availability is checked separately and its exact blocker retained without a parity claim.
- [x] AC5: Host semantics preserve Coordinator ownership and proportionate repository-specific decisions.

## Validation

- AC1-AC2: `build_architect_entrypoints.py --check` and `test_architect_host_assets.py` pass.
- AC3: Authenticated Codex CLI session `01a05b05-1afc-7750-a47d-15e1dda7fb12` discovered and invoked the installed skill.
- AC4: `command -v claude` returned no path and `claude --version` returned command not found; no Claude invocation claim is made.
- AC5: Generated output equality and required semantic-clause assertions pass.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/architecture-control; no PR | Generator, init fixtures, exact-package journeys and provisional real Codex canary pass; Claude unavailable | Local working tree only | CANARY-CODEX.md; CANARY-CLAUDE-BLOCKER.md; tests/test_architect_host_assets.py |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Author canonical semantics | Define the subordinate proportionate Architect contract once. | AC5 | Inspect canonical prompt. | Done | | prompts/Architect.prompt.md | No | bounded-return |
| 2 | Generate and enforce adapters | Generate Codex/Claude derivatives and fail drift in CI. | AC1, AC2 | Run generator and init tests. | Done | 1 | build_architect_entrypoints.py; host assets; CI | No | bounded-return |
| 3 | Run separate host canaries | Invoke Codex and independently probe Claude capability. | AC3, AC4 | Inspect durable receipts. | Done | 2 | child evidence | No | bounded-return |

## Parent AC Evidence

- AC3-AC4: Canonical semantics keep Architect subordinate and cover all six spine concerns.
- AC9: Generator check binds three derived outputs and CI enforces it.
- AC10: Codex session receipt records the exact discovered skill path and classification response.
- AC11: The approved unavailable-executable branch is evidenced exactly and no Claude parity claim is made.

## Validation Impact

- Baseline proof: integrated-qa:01a05b11-1112-7103-b9f5-f8e763952092
- Change summary: Added deliberate one-copy drift proof and campaign-bound Codex canary while retaining the Claude blocker.
- Impact: affected
- Invalidated proof layers: qa-review
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: Coordinator
- Change identity: sha256:e040db5107422e678ebca2958dea2a507d8706112faba28e22d6f36c46540081

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Changes Requested
- Could every AC pass while the approved user job remains undone: Yes
- Findings disposition: Resolved
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: No
- Affected validation evidence: Disposable one-copy drift test passes; exact-package host assets pass; governed Codex session `01a05b27-afa4-7e81-a935-75b2596f570a` is campaign-bound.
- Second QA commissioned: No
- Intent audit state: current
- Outcome journey evidence: Init fixtures and separate real-host receipts bind the exact candidate while retaining the Claude blocker.
- Reviewer independence: Ephemeral read-only Codex reviewer `01a05b11-1112-7103-b9f5-f8e763952092` made no mutations.
- Evidence: Parent `QA-INTEGRATED.md`; `CANARY-CODEX.md`; `CANARY-CLAUDE-BLOCKER.md`; exact-candidate `VERIFICATION-RECEIPT.md`.
- Findings: Original Changes Requested is preserved; host-generation and current Codex proof findings are resolved without a Claude support claim.

## Architecture Conformance

- Authority identity: sha256:f8327a14f96b2765b7e99eb744d218d0e0076cbec66ea3632761cb0a9cbe7737
- Candidate: git:3e34317a847f24ff64581c78d246adff93e29e27
- Mechanical checks: candidate=git:3e34317a847f24ff64581c78d246adff93e29e27; receipt=.project-workflow/tasks/EPIC-021-Proportionate-Architecture-Control/TASK-116-Dogfood-Architecture-Control-And-Closeout/VERIFICATION-RECEIPT.md
- Deviations: Claude runtime unavailable; resolved as the explicitly approved honest-blocker branch, with no Claude parity claim.
- Verdict: Pass

## Retro

- Reusable lessons: Generated-file parity and real-host capability require separate receipts.
- Conventions or agent assets updated: Canonical Architect prompt, generated host assets and CI check.
- Follow-up tasks: Authenticated Claude canary after a supported Claude runtime becomes available.

## Notes

- Task: TASK-115
- Title: Generate Project Architect Host Entrypoints
- Created: 2026-09-01
