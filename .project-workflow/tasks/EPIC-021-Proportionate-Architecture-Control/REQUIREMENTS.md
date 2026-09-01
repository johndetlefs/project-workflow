# Requirements

## Summary

- Task: EPIC-021
- Title: Proportionate Architecture Control
- Last updated: 2026-09-01
- Intent contract: full
- Architecture impact: material

## Intent

Project Workflow must make materially architecture-affecting work design against an explicit,
repository-appropriate structural contract before implementation, then make implementation and QA
check conformance. Small changes that follow established patterns must remain cheap and direct.

## Intent Spine

- OC1 — Completion capability: Project Workflow can classify architecture impact, establish or
  update repository-owned architectural truth for material work, fail closed on missing or stale
  decisions, and carry conformance through planning, implementation and QA.
- OC2 — Material capabilities: proportionate `no`/`local`/`material` classification; a Project
  Architect capability subordinate to the Coordinator; an architecture spine and optional ADRs;
  readiness, implementation and QA gates; project-appropriate mechanical constraints; and one
  canonical semantic source for Codex and Claude entrypoints.
- OC3 — Success journey: a cheap/local change proceeds by citing an established pattern without new
  architecture ceremony, while a material change records current architecture effect and contract
  authority before Ready, is implemented against that contract, and produces mechanical plus QA
  conformance evidence.
- OC4 — Successful-but-wrong result: files and prompts exist and tests pass, but material work can
  still become Ready with a missing/stale contract, a dependency or ownership violation escapes,
  small work gains needless ceremony, or generated host assets are mistaken for real-host support.
- OC5 — Exclusions: no Strategic Advisor Technical Advisor, universal atomic-design or file/folder
  prescription, heavyweight phase for every task, duplicate host truth, consumer-repository
  mutation/adoption, or external delivery action.
- OC6 — Assumptions: repositories differ, so the spine defines required concerns rather than one
  topology; measurable constraints are valuable only when chosen for that repository; authenticated
  host discovery is distinct from generated parity.
- OC7 — Authority source: originating Strategic Advisor task `01a05a3b-dea4-7330-a0ca-93f34c5e2cb9`,
  where the exact bounded proposal was presented and the owner replied, “Yeah, let's do it, making
  sure you create the next one inside the project workflow project, please.” The delegated envelope
  authorizes local requirements, planning, implementation, validation, QA and closeout, but not
  push, merge, release, deployment, rollout or cross-project adoption.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-09-01
- Approval note / source: Strategic Advisor task 01a05a3b-dea4-7330-a0ca-93f34c5e2cb9 unchanged approved meaning; post-plan correction only replaced a malformed decomposition table with the four already-approved workstreams.
- Approved artifact identity: sha256:e62ea5a691642ce5277eb87b2655de90a8b9833bcf69391dfd5a23252afde0f4

## Goal

Add a proportionate architecture-control capability that prevents architecture drift where the
consequence is material without slowing ordinary changes that already fit established structure.

## Non-Goals

- Add a Technical Advisor or any duplicate architecture capability to Strategic Advisor.
- Prescribe atomic design, universal file-size/module-count limits, folder layouts, or a single
  architecture style across repositories.
- Require ADRs, a separate architecture phase, or new architecture artifacts for every task.
- Keep duplicate semantic architecture truth in Codex, Claude, prompts, or generated runtime copies.
- Restructure, initialize, upgrade or otherwise mutate GPT App, Game Foundation, COF, or any other
  consumer repository.
- Push, merge, release, publish, deploy or roll out this capability.
- Claim Claude support from generated assets, mocks, package inspection or an unauthenticated shim.

## Users & Context

The primary user is a repository owner using Project Workflow through the Coordinator. Agents need a
clear, repository-owned structural boundary before making material changes, while owners need small
work to remain proportionate and delivery claims to remain honest across hosts.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Classify each current-contract Task or Epic child as `no`, `local`, or `material` architecture
  impact, with a reason and the architecture authority used.
- `no` and `local` work may proceed without creating or updating architecture artifacts when it
  follows an identified established pattern and does not cross a material boundary.
- `material` work must invoke the Project Architect capability through the existing Coordinator.
  Project Architect is a subordinate capability, never another owner-facing role or shared-state
  writer.
- The repository-owned architecture spine must cover responsibilities, dependency direction,
  canonical source ownership, shared-state boundaries, extension points and measurable constraints.
- ADRs are optional records for substantial individual trade-offs; they do not replace the spine.
- Material implementation plans must identify their architectural effect, affected boundaries,
  required spine/ADR decisions, and conformance proof.
- Readiness must fail closed when required material architecture authority is missing, placeholder,
  stale, or inconsistent with the plan.
- Implementation and independent QA must check the exact candidate against the current architecture
  contract and record conformance or named deviations.
- Repository-appropriate measurable constraints must become tests or CI checks where mechanical
  enforcement is feasible; no universal constraint is supplied as product policy.
- One canonical semantic source must generate semantically equivalent Codex and Claude Project
  Architect entrypoints, and deterministic parity checks must reject hand-edited or stale copies.
- Codex and Claude discovery/invocation must be proven separately on real authenticated hosts before
  cross-host support is claimed. An unavailable Claude runtime remains an explicit blocker.
- Project Workflow must dogfood the capability against `docs/architecture.md`, including a cheap
  local case, a missing/stale material-contract case, and a deliberate dependency/ownership
  violation caught mechanically.

## Acceptance Criteria (Verifiable)

- AC1: Current-contract Task and Epic-child planning records exactly one architecture-impact value
  (`no`, `local`, or `material`), its reason, and its architecture authority.
- AC2: A representative cheap/local change that cites an established pattern reaches readiness
  without a new spine, ADR, Architect invocation, or material-architecture proof campaign.
- AC3: Material work routes the Project Architect capability through the Coordinator and records a
  current architecture decision before implementation; the capability never becomes an
  owner-facing role or competing workflow-state writer.
- AC4: The architecture spine contract requires responsibilities, dependency direction, canonical
  source ownership, shared-state boundaries, extension points and measurable constraints, while
  explicitly rejecting universal topology and ceremony.
- AC5: Material plans identify architectural effect, affected boundaries, current spine/ADR
  authority, measurable constraints and conformance proof; ADRs remain optional except when the
  material trade-off needs a durable individual decision record.
- AC6: `task ready` and `epic ready-child` fail closed for a material classification whose required
  architecture authority is missing, placeholder, stale or inconsistent with the plan, while
  preserving the cheap/local path in AC2.
- AC7: Implement and QA contracts require architecture-conformance evidence for material work, and
  Review/Complete reject missing conformance or unresolved deviation evidence.
- AC8: A project can bind its selected measurable architecture constraints to repository tests or CI
  without Project Workflow imposing universal file-size, module-count or folder-layout limits.
- AC9: One canonical semantic Project Architect source deterministically generates both Codex and
  Claude entrypoints; a parity check passes on current outputs and fails on a deliberate one-copy
  edit.
- AC10: A real Codex-host canary proves discovery and invocation of the generated Project Architect
  entrypoint against the current candidate.
- AC11: A separate authenticated Claude-host canary proves discovery and invocation against the
  current candidate, or the Epic retains an exact blocker and makes no Claude/cross-host parity
  claim.
- AC12: Project Workflow dogfood records pass evidence for a local established-pattern change,
  fail-closed evidence for missing and stale material authority, and mechanical rejection of a
  deliberate dependency or ownership violation against `docs/architecture.md`.
- AC13: Local closeout explicitly distinguishes implemented, validated and QA-reviewed source from
  unapproved push, merge, release, deployment, consumer adoption and owner acceptance; no consumer
  repository is mutated.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose | Dependencies |
| --- | --- | --- | --- |
| Define Proportionate Architecture Contract | AC1, AC2, AC3, AC4, AC5, AC8 | Define impact classification, the subordinate Architect contract, repository spine requirements, optional ADR boundary and project-selected mechanical constraints. |  |
| Enforce Architecture Lifecycle Conformance | AC1, AC2, AC5, AC6, AC7, AC8 | Carry architecture impact and authority through plans, fail material readiness closed, and require exact-candidate implementation/QA conformance. | Define Proportionate Architecture Contract |
| Generate Project Architect Host Entrypoints | AC3, AC4, AC9, AC10, AC11 | Generate Codex and Claude Project Architect entrypoints from one canonical semantic source, enforce parity, and keep each real-host canary separate. | Define Proportionate Architecture Contract |
| Dogfood Architecture Control And Closeout | AC2, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13 | Prove the integrated cheap/material/violation journeys against Project Workflow, run available real-host canaries and independent QA, and retain the local-only/Claude boundary. | Enforce Architecture Lifecycle Conformance; Generate Project Architect Host Entrypoints |

## Open Questions (Answer Needed)

- None. The approved outcome, proportionality boundary, host-proof boundary, repository ownership
  and external-delivery exclusions are explicit.

## Decisions (Resolved)

- This is an Epic because the repository contract, lifecycle gates, canonical host generation and
  integrated dogfood/canary evidence are coupled but independently verifiable workstreams.
- `docs/architecture.md` is Project Workflow's existing implementation-architecture authority and
  will be extended rather than duplicated.
- This Epic is itself material architecture work. It uses a recorded bootstrap decision: establish
  the current spine/contract before production-behavior changes, because the new classification and
  readiness gate cannot govern work retroactively.
- Architecture impact is an explicit planning contract, not a universal separate lifecycle phase.
- Staleness is bound to an architecture authority identity, so prose saying “reviewed” without the
  current digest cannot satisfy material readiness.
- Codex/Claude semantic generation and real-host invocation are separate proof layers. Claude
  unavailability may block AC11 while leaving local implementation and truthful partial closeout
  possible; it cannot be waived or mocked.
- The implementation remains within this repository and local branch. Consumer adoption is a
  separate future owner decision.

## Controls

- Falsifier: a local established-pattern change is blocked solely because it lacks new architecture
  documentation.
- Falsifier: material work reaches Ready with a missing, placeholder, stale or mismatched authority.
- Falsifier: a source-ownership or dependency-direction violation passes all mechanical checks.
- Falsifier: changing one generated host entrypoint does not fail deterministic parity.
- Falsifier: installed text or package contents are reported as real-host discovery/invocation.
- Stop condition: implementation requires consumer-repository mutation, a universal architecture
  prescription, external delivery, or an unsupported claim about Claude.
- Review horizon: after integrated local dogfood, exact candidate validation and independent QA,
  before any push, merge, release or adoption decision.

## Validation Plan

- Exercise readiness fixtures for `no`, `local` and `material`, including missing, placeholder,
  stale and current architecture authority.
- Add focused lifecycle tests proving plans and QA evidence carry architecture conformance.
- Extend `tests/test_architecture.py` with a deliberate dependency/source-ownership violation and
  project-selected constraint checks.
- Generate both host entrypoints from one canonical source, run deterministic generation/parity,
  then deliberately alter a disposable copy and prove the check fails.
- Run focused architecture/lifecycle/host-asset tests, generated runtime check, locked static checks,
  full locked pytest, build/package inventory where affected, and strict Doctor.
- Run a real Codex discovery/invocation canary. Run a separate authenticated Claude canary only if
  that capability actually exists; otherwise record the exact unavailable-runtime evidence.
- Record independent QA by AC ID and preserve the local-only delivery boundary.
