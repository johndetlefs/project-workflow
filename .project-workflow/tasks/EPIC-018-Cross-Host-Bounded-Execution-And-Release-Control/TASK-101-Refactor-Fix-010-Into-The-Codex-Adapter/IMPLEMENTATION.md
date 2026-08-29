## User Story

As a Project Workflow Coordinator, I want the host-neutral controller to dispatch through one
verified Codex adapter, so that Codex mechanically enforces the approved envelope without owning a
second workflow or release product.

## Parent AC Coverage

- AC3, AC4, AC8, AC9, AC12, AC13, AC14

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
- AC9: owner `Refactor FIX-010 Into The Codex Adapter`; required evidence: Real supported Codex canary, subordinate aggregation, interruption, receipt, and install evidence.
- AC12: owner `Define Host-Neutral Execution And Candidate Contract; both host adapters`; required evidence: Unsupported/version/trust/policy fixtures and truthful capability/status results.
- AC13: owner `Both host adapters; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Retained-package fresh/upgrade/no-op/disable journeys and Doctor activation state.
- AC14: owner `Refactor FIX-010 Into The Codex Adapter; Prove Cross-Host Conformance And Delivery Boundary`; required evidence: Complete prototype disposition map plus source/package scans rejecting retained lock-in assumptions.

## Acceptance Criteria

- [x] AC1: Exact Codex executable/version/configuration and binding capabilities are verified or
  blocked precisely.
- [x] AC2: One real Codex App Server canary activates hooks, completes or interrupts finitely, and
  persists one input-bound core receipt.
- [x] AC3: Aggregate tool/test/retry/worker/write/token/elapsed limits plus hook/source/scope failures
  deny or interrupt without bypass.
- [x] AC4: `project execute` dispatches only from sealed current control and Coordinator state remains
  authoritative.
- [x] AC5: Packaged adapter assets and status/Doctor truthfully distinguish active, disabled,
  incompatible, untrusted and unavailable states.
- [x] AC6: Complete FIX-010 disposition and source/package scans remove prototype public naming,
  constant-budget and release-ownership assumptions.
- [x] AC7: Evidence preserves deterministic/runtime/package/delivery/acceptance boundaries.

## Validation

- AC1-AC7 / parent AC3, AC4, AC8, AC9, AC12, AC13, AC14: 40 focused adapter/control/
  QA-release tests and the exact-current 321-test affected execution, coordination, verification,
  status, Doctor and package suite pass. Ruff is clean for the affected Python scope; the plugin
  validator passes; the wheel/sdist build succeeds; the retained wheel includes the three expected
  plugin assets with the hook executable at mode 0755 and excludes retired prototype surfaces.
  Installed Codex `0.145.0-alpha.30` completed one real hook-active canary with one allowed and
  required changed path, stable source, native bounded metrics, evidence identity
  `sha256:bee66a6a95f1...`, and core receipt `sha256:5d9ca12728b1...`. The three managed CLI copies
  are byte-identical at SHA-256 `a7603cf42cb550dd35a45e3d6036a1cca5b1bb30c08d73d45d9d0b5a639eeb5e`.
  The retained canary used the immediately preceding CLI identity `f1e35ee...`; the only later CLI
  change was evidence grading, so the runtime output was regraded with zero additional target calls.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/cross-host-execution-control` from `c1426f2c` | 321 affected tests pass; affected Ruff and plugin validation pass; retained wheel/sdist validate; exact installed-Codex workspace-root-bound canary passes | Local working-tree implementation and retained runtime/package artifacts only; no push, merge, publication, installation or adoption | `tests/test_codex_adapter.py`; `tests/test_execution_control_contract.py`; `FIX-010-DISPOSITION.md`; `evidence/real-codex-canary.json`; wheel `sha256:3f3167a5cd11...`; sdist `sha256:789e98d041eb...` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define Codex Capability Contract | Add sealed adapter settings and exact current-host capability preflight without weakening generic authority. | AC1, AC4, AC5 | Run supported, missing, disabled, incompatible and untrusted capability fixtures. | Done | | Core capability schema, adapter module and tests | No | bounded-return |
| 2 | Implement Hook Enforcement | Refactor atomic counter, command/write scope, identical retry, worker and post-tool Git checks from FIX-010 into a subordinate hook handler. | AC3, AC4 | Run pre/post hook adversarial fixtures including malformed input and hook absence. | Done | 1 | Codex hook controller and tests | No | bounded-return |
| 3 | Implement App Server Supervisor | Drive current initialize/thread/turn events, monitor token/time, interrupt finitely and translate terminal host results. | AC1, AC2, AC3 | Validate current generated protocol schema and simulated lifecycle/interrupt cases. | Done | 1, 2 | Codex App Server client and tests | No | bounded-return |
| 4 | Integrate Project Execute And Receipts | Dispatch sealed Codex settings through `project execute`, persist one typed receipt and derive consumed limit state from receipts. | AC2, AC4, AC7 | Run public CLI success/block fixtures and receipt-tamper/current-source cases. | Done | 1, 2, 3 | CLI, managed copies, coordination state and tests | No | bounded-return |
| 5 | Package And Diagnose Adapter | Add package-owned subordinate hook/plugin assets plus active/disabled/incompatible/untrusted status and Doctor evidence. | AC1, AC5, AC7 | Build/inspect package and run status/Doctor capability fixtures. | Done | 1, 2, 3, 4 | Package metadata, managed assets, docs and tests | No | bounded-return |
| 6 | Disposition FIX-010 | Map all 19 files and every prototype behavior to adopt/refactor/replace/retire, then scan source/package outputs for forbidden lock-in. | AC6, AC7 | Run complete map and forbidden-name/fixed-budget/release-owner scans. | Done | 1, 2, 3, 4, 5 | Disposition record, docs and scan tests | No | bounded-return |
| 7 | Prove Current Codex Child | Run focused/affected tests, current protocol schema check, one bounded real Codex canary, Intent audit, Doctor and one independent QA. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Inspect exact runtime receipt and proof boundaries. | Done | 1, 2, 3, 4, 5, 6 | Validation and child evidence | No | bounded-return |

## Parent AC Evidence

- AC3, AC4: The sealed Codex capability is subordinate to the TASK-099 core contract. Read-only
  inspection executes no configured code; material dispatch probes the exact binary and all native
  results become one core-owned input-bound receipt.
- AC8: TASK-101 adds no release executor, candidate promotion or repair authority; FIX-010 release
  behavior is explicitly retired in favor of TASK-100's host-neutral fixed-release control.
- AC9: Installed Codex `0.145.0-alpha.30` ran the canonical hook-active disposable canary through
  `project execute`, produced only `src/canary.txt`, preserved source identity and persisted one
  passing receipt. The runtime-target-source claim is retained in `EVIDENCE.json`.
- AC12, AC13: Missing, disabled, untrusted, tampered and version-stale capability fixtures block;
  status/Doctor inspection is model-free. Wheel inspection proves package presence only, not
  installation or activation.
- AC14: `FIX-010-DISPOSITION.md` covers all 19 prototype files and every retained/replaced/retired
  behavior. Source and retained-wheel scans reject its fixed 80,000-token rule, public
  `project-enforce` entry point and independent enforcement-package naming.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: The remediated exact installed-Codex canary completed through `project execute`, recorded SessionStart/PreToolUse/PostToolUse, changed exactly `src/canary.txt`, preserved source `dc53d174...`, and persisted receipt `sha256:c45a4166093e...`.
- Reviewer independence: A separate ephemeral read-only Codex reviewer produced `evidence/independent-qa.txt` (`sha256:caefddf675d2...`) without changing source, evidence or workflow state.
- Evidence: 40 focused and 321 affected tests pass; `evidence/package-manifest.json` binds the retained final wheel/sdist; `evidence/real-codex-canary.json` binds the control, events, output and receipt; no second broad QA was run.
- Findings: The retained initial verdict was Changes Requested. One bounded remediation fixed and regression-tested High workspace-root trust, High capability overclaim and High retained-proof gaps, plus Medium lifecycle cleanup; the Medium AC9 overclaim was narrowed to the actual canary while aggregate/interruption/release proof remains TASK-103. No second broad QA was run.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-101
- Title: Refactor FIX-010 Into The Codex Adapter
- Created: 2026-08-28
