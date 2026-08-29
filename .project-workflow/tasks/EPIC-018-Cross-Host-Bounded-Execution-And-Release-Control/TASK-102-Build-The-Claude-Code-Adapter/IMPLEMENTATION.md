## User Story

As a Project Workflow Coordinator, I want one verified Claude Code adapter to enforce the same sealed
material-work decisions and receipt meanings, so that Claude is a truthful supported host without
owning another workflow or pretending its native units are Codex units.

## Parent AC Coverage

- AC3, AC4, AC8, AC10, AC11, AC12, AC13

## Child Charter

### Inherited Invariants

- Project Workflow remains the only product owner, repository owner, Coordinator, lifecycle, verification campaign, QA verdict, candidate authority, and shared-state writer.
- Read-only and cheap deterministic work does not launch another model or require campaign ceremony.
- Material work in a supported trusted installation cannot mutate, validate broadly, remediate QA, promote a candidate, or release outside the controlled path.
- The worker cannot amend its sealed execution identity, write scope, permitted operations, proof obligations, or finite limits.
- Limits pause or block and keep missing proof visible; they never manufacture a pass.
- One independent QA pass creates one durable findings set. In-scope remediation is automatic and bounded; only affected proof and unresolved findings are rechecked; a second broad QA is prohibited.
- Continuation requires named material progress. An identical or no-progress repeat is denied.
- Working revisions, verification candidates, and release candidates have distinct semantics.
- Release candidate promotion occurs only after all required implementation, verification, QA, and affected-proof obligations pass.
- Release runs predeclared operations against one clean frozen candidate and has no source repair, QA, or replacement-candidate authority.
- Host adapters enforce the same decisions and receipt meanings but may use different native units and mechanisms.
- Unsupported or unknown binding host capability fails closed for material work and cannot be advertised as supported.
- Codex and Claude Code are the minimum initial supported hosts. No other host inherits the claim.
- All shipped core and adapter assets come from the Project Workflow repository and package.
- Automated, host-runtime, package, merge, publication, installation, adoption, effectiveness, and owner-acceptance proof remain separate.

### Invalid Substitutes

- Another instruction, prompt, checklist, approval step, or status field saying that agents should stop.
- Merging FIX-010 unchanged, exposing project-enforce as the portable public product, or treating one local Codex canary as cross-host proof.
- A separate enforcement repository, service, or workflow writer that owns its own candidate, findings, QA, or release truth.
- A universal token/time/test number presented as proportionate control.
- A stop rule that leaves material findings or required proof for the owner to resolve manually.
- Repeating broad QA after correction instead of retaining one findings set and validating affected proof.
- Calling every mutable implementation/test revision a release candidate.
- Treating a failed or exhausted envelope as a pass, completion, or release authorization.
- A release command that can edit source, install fixes, commission QA, or mint a successor candidate.
- Static Codex or Claude assets, fake hooks, mocked CLI output, or package presence without a real supported-host journey.
- Claiming that a repository-local hook covers untrusted repositories, disabled plugins, user shells, hosted surfaces, or managed policy that prevents the hook.
- Host-metric normalization that presents Codex tokens, Claude dollar budget, turns, or elapsed time as interchangeable.
- Project Workflow production code, workflow state, or managed assets placed in Strategic Advisor.

### Artifact Targets

- Versioned host-neutral execution-envelope, progress, candidate, capability, and typed-receipt schemas integrated with the 0.8.0 Coordinator and verification campaign.
- Deterministic material-work router plus host-neutral project execute and project release CLI surfaces.
- Immutable envelope supervisor/controller with aggregate progress, denial, interruption, and terminal receipt behavior.
- One QA findings/remediation campaign integrated with affected-proof validation and no-recursive- QA enforcement.
- Working-revision, verification-candidate, release-candidate, and fixed release state/commands.
- Codex adapter and managed installation assets using current supported Codex programmatic/hook mechanisms.
- Claude Code adapter and managed installation assets using current supported print-mode, streaming, permission/tool, hook, budget/turn, and timeout mechanisms.
- Capability preflight, status, Doctor, diagnostics, disable/uninstall, and truthful unsupported state.
- FIX-010 disposition map covering every prototype file, behavior, test, CLI, hook, and repository backstop.
- Sanitized cross-host conformance corpus, real Codex and Claude Code canary receipts, recurrence journey, package/fresh/upgrade/no-op/disable evidence, and explicit delivery boundary.
- Aligned source, generated assets, README, CHANGELOG, package metadata, tests, schemas, and repository-local mirrors.

### Parent AC Proof Ownership

- AC3, AC4: owner `Define Host-Neutral Execution And Candidate Contract`; required evidence: Direct read-only countercases, material bypass denials, immutable-limit and blocked-proof receipts.
- AC8: owner `Enforce Proportionate QA Remediation And Fixed Release; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Clean candidate, once-only operations, failure termination, bounded infrastructure recovery, and prohibited-authority tests.
- AC10: owner `Build The Claude Code Adapter`; required evidence: Real supported Claude Code canary, hook/budget/turn/tool/timeout receipt, and install evidence.
- AC11: owner `Build The Claude Code Adapter; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Cross-host state, denial, candidate, proof, and receipt conformance matrix.
- AC12: owner `Define Host-Neutral Execution And Candidate Contract; both host adapters`; required evidence: Unsupported/version/trust/policy fixtures and truthful capability/status results.
- AC13: owner `Both host adapters; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Retained-package fresh/upgrade/no-op/disable journeys and Doctor activation state.

## Acceptance Criteria

- [x] AC1: Exact executable, version, trust, configuration and binding Claude capabilities are
  inspectable, verified at dispatch or blocked precisely.
- [x] AC2: Package-owned blocking hooks bind the sealed workspace and enforce aggregate tool,
  command, test, retry, worker and changed-path scope with sticky denial.
- [x] AC3: Print-mode stream supervision applies explicit Claude-native budget, turn, elapsed and
  tool limits and terminates finitely with typed terminal semantics.
- [x] AC4: `project execute` dispatches current sealed Claude settings and core persists exactly one
  input-bound receipt without adapter-owned shared state.
- [x] AC5: Package assets and status/Doctor truthfully distinguish inspectable, verified-at-dispatch,
  disabled, incompatible, untrusted, unavailable and policy-blocked states.
- [ ] AC6: One real supported Claude Code canary activates hooks, makes exactly the required scoped
  change, preserves source and records native metrics plus one core receipt.
- [x] AC7: Documentation and evidence preserve runtime/package/install/delivery/acceptance boundaries
  and leave full cross-host equivalence to TASK-103.

## Validation

- AC1-AC5 and AC7 / parent AC3, AC4, AC8, AC11, AC12, AC13: 31 focused Claude/control tests and
  all 548 repository tests pass. The three managed CLI copies are byte-identical at
  `sha256:583fdc8bc1f0...`. Wheel/sdist build and member inspection pass; the retained wheel contains
  the adapter, managed CLI source, companion adapter, plugin manifest, hooks and mode-0755 handler.
  Fresh init and standalone managed-CLI fixtures prove the local adapter chain without relying on
  the repository virtual environment. Current official CLI, hook, plugin, permission and
  managed-policy contracts were inspected before remediation.
- AC6 / parent AC10: Blocked precisely. No `claude` executable exists on PATH, standard local,
  Homebrew, active Node-global, or application locations, and no supported authentication variable
  is present. No real canary or runtime-support claim was fabricated. See
  `evidence/runtime-capability.json`.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/cross-host-execution-control` from `c1426f2c` | 31 focused and 548 full-suite tests pass; wheel/sdist build and required-member/mode/source inspection pass; fresh managed CLI loads standalone; runtime inventory proves Claude unavailable | Local working-tree candidate and retained package proof only; no real Claude canary, push, merge, publication, installation or adoption | `tests/test_claude_adapter.py`; `tests/test_execution_control_contract.py`; `EVIDENCE.json`; `evidence/task102-validation.json`; `evidence/package-manifest.json`; `evidence/runtime-capability.json`; `evidence/independent-qa.txt` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define Claude Capability Contract | Add exact settings plus read-only inspection and material probe without weakening generic authority. | AC1, AC5 | Run supported, missing, disabled, incompatible, untrusted and policy-blocked fixtures. | Done | | Claude adapter schema and tests | No | bounded-return |
| 2 | Implement Blocking Hook Controller | Add package-owned hook handling for sealed workspace, tools, commands, tests, retries, workers, writes and terminal state. | AC2, AC4 | Run malformed input, external workspace, scope, duplicate retry and subordinate-tool countercases. | Done | 1 | Claude hook controller/plugin and tests | No | bounded-return |
| 3 | Implement Print-Mode Supervisor | Launch current stream-json print mode with explicit allowed tools, max turns, max budget, hook events and timeout; parse native terminal output. | AC1, AC3 | Run stream lifecycle, max-turn, max-budget, retry, timeout, malformed output and process failure fixtures. | Done | 1, 2 | Claude subprocess supervisor and tests | No | bounded-return |
| 4 | Integrate Execute And Core Receipt | Route sealed Claude settings through `project execute` and persist one typed core-owned receipt. | AC3, AC4, AC7 | Run CLI success/block, source/scope drift, missing required output and receipt identity cases. | Done | 1, 2, 3 | CLI, managed copies, coordination and tests | No | bounded-return |
| 5 | Package And Diagnose Adapter | Ship Claude plugin/hook assets and add truthful status/Doctor capability projection and documentation. | AC1, AC5, AC7 | Validate plugin structure, build/inspect archives and run state projection fixtures. | Done | 1, 2, 3, 4 | Package metadata, assets, docs and tests | No | bounded-return |
| 6 | Prove Current Claude Child | Run focused/affected suites, retain package inspection, and attempt a real Claude canary only when the exact runtime is supported; otherwise retain the precise blocker. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Inspect exact runtime receipt and proof boundaries or the precise unsupported blocker. | Done | 1, 2, 3, 4, 5 | Validation and child evidence | No | bounded-return |

## Parent AC Evidence

- AC3, AC4: Sealed hook/limit countercases and public execute/core receipt fixtures pass with
  distinct Claude USD-micro, turn and elapsed units.
- AC8: The adapter exports only subordinate inspection/probe/hook/execute behavior and has no
  release, candidate-promotion, repair or QA authority.
- AC10: Blocked: one real supported Claude Code canary remains required, but no exact local runtime
  or authentication is available. Mocked output and package presence were explicitly rejected.
- AC11: Claude-side receipt/state semantics pass deterministically; full real cross-host equivalence
  remains TASK-103 and is blocked by the same missing runtime.

### Owner-Authorized v0.9.0 Delivery Boundary — 2026-08-29

- The owner authorized v0.9.0 merge, publication, and installation rollout before the real Claude
  Code canary. This is a delivery-sequence decision, not affected proof for AC10.
- The Claude adapter and managed assets may ship as packaged, fail-closed capability. They must not
  be reported as runtime-certified or proven supported until an authenticated current Claude Code
  journey exercises the required hook, permission, budget, turn, timeout, output, and receipt path.
- The preserved independent QA report remains the only broad QA invocation. Source findings have
  affected remediation proof; the real-runtime blocker remains open without recursive QA.
- AC12: Disabled, untrusted, tampered, unavailable, stale-version, missing-flag/authentication and
  missing-hook fixtures report non-support without read-only model or executable calls.
- AC13: Retained package assets and executable mode pass; installation/activation and full
  fresh/upgrade/no-op/disable journeys remain TASK-103.

## Validation Impact

- Baseline proof: independent-qa-sha256:2694dbc03c0c0ce2e5a8df9eb7dac1e0a2548c8bf3df23666b2b82ca4c6015ff
- Change summary: Remediated fail-open permissions and hook activation, managed interpreter/assets, process-tree cleanup, terminal failure receipts, semantic output proof, truthful Status/Doctor projection, and hook-authority documentation.
- Impact: affected
- Invalidated proof layers: implementation, qa-review, structured-evidence
- Required validation: affected-proof-layer
- Validation verdict: pass
- Decided by: EPIC-018 Coordinator; preserved QA session 01a046b7-431e-7143-940a-29136a66f041
- Change identity: sha256:bec65aba0780f21f1a8de79957fb6d1cf7a29b29087e620a079fc4a30281de8f

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested
- Intent adversarial verdict: Fail
- Could every AC pass while the approved user job remains undone: Yes
- Intent audit state: current
- Outcome journey evidence: Deterministic source, managed-install and retained-package proof passes, but no executable/authenticated Claude runtime exists for the required real hook-active public `project execute` canary.
- Reviewer independence: One separate read-only Codex QA session `01a046b7-431e-7143-940a-29136a66f041` reviewed the candidate; no second QA was commissioned.
- Evidence: Original report `evidence/independent-qa.txt` at `sha256:2694dbc03c0c0ce2e5a8df9eb7dac1e0a2548c8bf3df23666b2b82ca4c6015ff`; affected validation `evidence/task102-validation.json`; package manifest and runtime inventory.
- Findings: Original Blocker/Critical/High/Medium findings are preserved verbatim in the independent report. Eight source/contract findings were remediated; the missing real Claude runtime canary remains open.
- Findings disposition: Open — source findings resolved by affected validation; required Claude runtime/authentication and real canary remain unavailable.
- Affected validation verdict: Pass
- Could every AC pass after affected validation while the approved user job remains undone: Yes — AC6 and parent AC10 still require the real Claude journey.
- Affected validation evidence: 31 focused tests pass in 6.63s; all 548 repository tests pass in 110.35s; retained wheel `sha256:be1beec0...` and sdist `sha256:d7346036...` pass member/source/mode inspection; strict Doctor now isolates the real-runtime evidence blocker.
- Second QA commissioned: No

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-102
- Title: Build The Claude Code Adapter
- Created: 2026-08-28
