## User Story

As the Project Workflow owner, I want independent release-grade proof of Delegate's behavior and boundaries so that I can rely on it without mistaking prompts, tests, or packaging for actual orchestration.

## Parent AC Coverage

- AC4, AC10, AC11, AC12, AC14, AC15, AC16, AC17, AC18, AC19, AC20

## Child Charter

### Inherited Invariants

- One delegation run targets exactly one approved Epic or Task.
- Delegate executes existing authority; it does not create scope, approve requirements, or add unplanned children/work items.
- Coordinated standalone Tasks require an Epic; arbitrary Task batches are rejected.
- Epic child Tasks and Task implementation rows remain distinct execution units with distinct executor choices.
- Persistent Codex task creation requires explicit owner authority and verified host support.
- The coordinator is the single writer of shared workflow state and target lifecycle.
- Workers operate inside explicit write/repository scopes and never gain push, merge, release, deployment, external-contact, or cross-repository authority from delegation.
- Dependencies are satisfied by coordinator-verified results, not worker assertion alone.
- Concurrency never exceeds available host capacity and unsafe file overlap is never parallelized.
- A failed unit blocks its descendants; unrelated work continues only while the shared baseline remains valid.
- Canonical workflow artifacts remain the durable authority; machine-local execution handles remain ignored and contain no credentials or private transcripts.
- Task `Testing`, child completion, Epic closeout, and final completion remain gated by existing implementation, evidence, QA, audit, deferral, retro, and owner-authority rules.
- Unsupported host behavior fails closed or degrades explicitly; the system never fabricates support or parity.
- Existing non-delegated behavior remains backward compatible.

### Invalid Substitutes

- A prompt or skill that says work was delegated without observed worker launches, dependency behavior, monitoring, and returned evidence.
- Repository fixtures or mocked scheduler tests presented as proof of current Codex task, worktree, subagent, interruption, or resume behavior.
- A worker's completion claim without coordinator inspection of scope, changes, validation, and required evidence.
- A Task moved to `Testing` while required implementation rows remain incomplete.
- Multiple workers editing shared trackers, implementation-plan status, acceptance maps, evidence indexes, or lifecycle state.
- A fixed configured worker count presented as proof that host capacity was respected.
- Committed task IDs, agent IDs, cursors, leases, credentials, private transcripts, or other machine-local runtime state.
- Generated/source asset parity presented as proof that every supported host can perform persistent or parallel orchestration.
- Unit tests, builds, Doctor, QA prose, or related environments substituted for `external-contract-alignment` or `runtime-target-source` evidence.
- Delegate's own aggregate report substituted for independent QA, Epic acceptance audit, owner-only acceptance, integration, release, deployment, adoption, or effectiveness.

### Artifact Targets

- Host-neutral delegation graph, validation, state-transition, reconciliation, and reporting implementation under `src/project_workflow/` with mirrored helper behavior where required.
- A `project delegate` CLI family with read-only planning/status and controlled runtime-state operations, including schema-versioned JSON.
- Updated Task planning and Epic decomposition metadata for dependencies, Task-row write scope, and parallel safety with backward-compatible migration/upgrade behavior.
- Ignored machine-local delegation runtime state with no competing tracked lifecycle authority.
- Updated Codex `project-delegate` skill, other host Delegate prompts/agents, Planner, Implement, Epic, QA, AGENTS guidance, README, packaged resources, and generated/source mirrors.
- Focused deterministic tests, complete regression coverage, strict Doctor, build/package checks, and upgrade plan/apply/rollback evidence.
- Retained disposable Task-mode and Epic-mode runtime journey artifacts tied to the exact source revision, installed package, host, target repository/worktree, and observation method.

### Parent AC Proof Ownership

- AC4: owner `Delegation Graph child`; required evidence: Human/JSON snapshots and schema tests proving deterministic graph, readiness, eligibility, blocking, executor, concurrency, provenance, and read-only behavior.
- AC10: owner `Task and Epic Orchestration children`; required evidence: Failure-injection tests and live run evidence for descendant blocking, independent continuation, shared-premise halt, safe in-flight completion, and terminal classifications.
- AC11: owner `Task and Epic Orchestration children`; required evidence: Integration/reconciliation tests and retained examples where verified results release dependencies while collision/out-of-scope results do not.
- AC12: owner `Delegation Graph, Task Orchestration, and Epic Orchestration children`; required evidence: Interruption/resume and orphan tests plus live proof of no duplicate worker or Codex task launch.
- AC14: owner `Task and Epic Orchestration children`; required evidence: Lifecycle/QA/closeout regression tests and live evidence that Delegate cannot self-complete Task or Epic delivery.
- AC15: owner `Host Alignment child`; required evidence: Capability-matrix tests and unvalidated-host scenarios proving fail-closed or explicit sequential fallback with truthful claims.
- AC16: owner `Host Alignment child`; required evidence: Generated/source mirror checks, init/upgrade plan/apply/rollback tests, fresh install inspection, and package asset parity.
- AC17: owner `End-To-End Proof child`; required evidence: Complete locked regression, strict Doctor, compilation/build/package results, and non-delegated journey checks.
- AC18: owner `Task Orchestration and End-To-End Proof children`; required evidence: Retained disposable current-Codex Task-mode journey matching every AC18 condition and tied to exact runtime/source identity.
- AC19: owner `Epic Orchestration and End-To-End Proof children`; required evidence: Retained disposable current-Codex Epic-mode journey matching every AC19 condition and tied to exact runtime/source identity.
- AC20: owner `Host Alignment and End-To-End Proof children`; required evidence: README/AGENTS/skill/prompt/install inspection plus positive and negative invocation examples verified against implemented behavior.

## Acceptance Criteria

- [x] AC1: Every mapped Delegate behavior has valid retained evidence and no prohibited proof substitution. Parent AC4, AC10-AC16, AC20.
- [x] AC2: Full locked regression, strict Doctor, build/package/release and non-Delegate compatibility gates pass. Parent AC17.
- [x] AC3: Exact-source current-Codex Task-mode proof satisfies every required live event. Parent AC18.
- [x] AC4: Exact-source authorised current-Codex Epic-mode proof satisfies every required live event. Parent AC19.
- [x] AC5: Privacy and cross-host claim boundaries pass source/distribution/evidence inspection. Parent AC12, AC15, AC16.
- [x] AC6: Independent QA, documentation verification, and parent closeout handoff remain separate and complete. Parent AC14, AC20.

## Validation

- AC1: Parent-to-child evidence matrix and invalid-substitute audit.
- AC2: Focused suites, full locked suite, strict Doctor, compilation, build/package, release contract, helper parity, and representative legacy journeys.
- AC3: Independent inspection/repetition of Task live receipt identity, worker events, scopes, hashes, dependency/failure timing, and lifecycle gate.
- AC4: Independent inspection/repetition of Epic live receipt authority, creation/worktrees, concurrency, dependency wait, reconciliation counts, and closeout rejection.
- AC5: Git/sdist/wheel/generated/Smoke Bomb/evidence privacy scans and host-claim wording audit.
- AC6: QA verdict, docs example checks, retro, acceptance audit, deferrals, and governed closeout results.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | Detached at `f864c0f7ab3fce89fe7817481ea020c422ec6b28`, the exact requested `codex/EPIC-010-delegate-execution-orchestrator` base; no PR | 287 focused, 377 full locked, 16 negative/legacy, strict Doctor, compile, release, exact-wheel install, four-host/legacy package journey, privacy, and read-only surfaces passed | Child-local evidence only; no push, merge, release, deployment, adoption, or effectiveness claim | `evidence/delegation-validation-receipt.json` and `evidence/2026-08-19-validation.md` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Evidence And Invalid-Substitute Audit | Map every parent AC to exact child evidence and reject prompt-only, fixture-only, lower-layer, private, stale, or overbroad claims. | AC1 | Review the evidence matrix against the Epic contract. | Done |
| 2 | Deterministic And Legacy Regression | Run focused Delegate suites, representative non-Delegate journeys, the full locked suite, strict Doctor, compilation, build/package/release, and mirror gates. | AC2 | Inspect exact commands/results and compare legacy behavior. | Done |
| 3 | Task Live-Proof Review | Inspect or repeat the exact integrated current-Codex Task-mode journey and runtime-target-source claim. Depends on rows 1-2. | AC3 | Match every AC18 event to sanitised observed evidence. | Done |
| 4 | Epic Live-Proof Review | Inspect or repeat the exact integrated authorised current-Codex Epic-mode journey and host-contract/runtime claims. Depends on rows 1-2. | AC4 | Match every AC19 event to sanitised observed evidence. | Done |
| 5 | Privacy And Host-Claim Audit | Scan Git/distributions/generated/Smoke Bomb/evidence and verify untested-host fallback wording. Depends on rows 2-4. | AC5 | Review inventories, hostile-content tests, and dated capability provenance. | Done |
| 6 | Independent QA And Closeout Handoff | Run independent child QA, documentation verification, and child retro; prepare the parent audit/deferral/closeout handoff without mutating coordinator-owned parent state. Depends on rows 1-5. | AC1, AC2, AC3, AC4, AC5, AC6 | Review QA verdict, remaining proof boundaries, and coordinator handoff. | Done |

## Parent AC Evidence

- AC4: Final-HEAD human/JSON plan and status prove deterministic graph, readiness, executor, concurrency, dated provenance, and read-only behavior.
- AC10: Final state/failure matrices and the retained Task failure/retry observation prove descendant-aware failure and safe continuation boundaries.
- AC11: Final tests and both retained receipts require coordinator verification before dependency release.
- AC12: Persist/resume/orphan/no-duplicate tests plus live monitoring resume pass. No distinct live coordinator-process restart is claimed.
- AC14: Targeted negative lifecycle proofs keep Testing, QA, Review, Complete, and parent closeout independent from Delegate.
- AC15: Tri-state dated capabilities and explicit fallback/fail-closed behavior pass without inferring untested host runtime support.
- AC16: Managed asset v2, helpers/prompts/skills, fingerprints, four-host exact-wheel journeys, rollback coverage, and `.new` collision behavior pass.
- AC17: 377/377 locked tests, strict Doctor, compile, build, release contract, exact-wheel install, workspace, Smoke Bomb, privacy, and non-Delegate journeys pass at `f864c0f`.
- AC18: The sanitized Task live receipt covers every required event at exact commit `9c3d9bd` and reproducible source/helper hash `48ff24a`; final-HEAD native replay is outside the claim.
- AC19: The sanitized authorized Epic live receipt covers every required event at exact commit `62e56d6` and reproducible source/helper hash `b468a24`; final-HEAD native replay is outside the claim.
- AC20: Source and installed guidance preserve positive/negative invocation examples and exact role/lifecycle distinctions.
- Structured evidence: `EVIDENCE.json` has one passing claim for every mapped parent AC, plus the required external-contract claim, and every `invalid_substitutes` list is empty.

## QA & Code Review

- Verdict: Pass for the approved TASK-064 evidence-consolidation scope.
- Evidence: Independent second-pass review of exact diff scope, identities, all child/parent AC mappings, 287 focused tests, 377 full tests, 16 targeted lifecycle/legacy tests, strict Doctor, compilation, mirrors, release receipt, exact-wheel install, four-host/legacy journeys, package inventories, privacy scans, plan/status immutability, and both live receipts. Detailed record: `evidence/2026-08-19-validation.md`.
- Findings: One evidence pointer defect was fixed during review: the receipt's TASK-061/TASK-062 relative paths were one directory too shallow. No blocking correctness, scope, privacy, packaging, documentation, or lifecycle finding remains; no source defect found. Proof boundary retained: historical live-run wheel binaries were not retained and neither native journey ran at final HEAD, so final-wheel native replay is not claimed. Parent lifecycle, acceptance audit, deferrals, retro, release, deployment, adoption, effectiveness, and owner acceptance remain separate coordinator/owner gates.

## Retro

- Reusable lessons: Keep exact native-host receipts and final package validation as separate proof layers; record both identities and state explicitly when the final package was not replayed through the native journey.
- Conventions or agent assets updated: None. Existing proof recipes and Delegate guidance already own the distinction; no one-off task detail was added globally.
- Follow-up tasks: None created. The parent coordinator should preserve the final-HEAD native-replay boundary during acceptance audit and release decision. No in-scope work was missed.

## Notes

- Task: TASK-064
- Title: Prove End-To-End Delegation And Backward Compatibility
- Created: 2026-08-19
- Executed: 2026-08-19 from exact committed base `f864c0f7ab3fce89fe7817481ea020c422ec6b28`.
- Coordinator boundary: child-local implementation/evidence/QA/retro updated; parent/global trackers, acceptance map, acceptance audit, deferrals, parent retro, parent lifecycle, and delegation runtime state left untouched.
