## User Story

As a maintainer and owner, I want the exact packaged candidate proven in realistic repositories,
so that local green tests cannot hide missing intent behavior, unsafe upgrades or proxy completion.

## Parent AC Coverage

- AC13, AC14, AC15

## Child Charter

### Inherited Invariants

- Approval asks whether the brief Intent accurately reflects what the owner means; IDs, hashes, requirements and ACs bind and elaborate that approval but never substitute for it.
- The owner outcome and material capability commitments remain visible and traceable through every derived artifact; downstream AC precision cannot supersede a contradicted source intent.
- Material capability reduction is a scope change requiring a plain-language amendment or refreshed approval; implementation detail inside the approved intent envelope remains autonomous.
- Semantic judgments are inspectable and independently reviewable; deterministic gates enforce presence, identity, coverage, freshness and provenance without claiming mathematical proof of meaning.
- Requirements approval stays concise and bounded; the workflow must not solve approval failure by transferring artifact-reading labor back to the owner.
- User-outcome proof matches the claim and normal journey. Lower evidence layers remain useful but cannot satisfy higher user-visible claims.
- Owner acceptance remains separate from automated validation and independent QA where practical usability, feel or taste is material.
- Full intent gates are proportional; low-risk bounded fixes retain a lightweight path and over-delivery outside owner intent is a defect, not a virtue.
- Structured workflow state remains repository-native, agent-operated and compatible with existing repositories through explicit warning/adoption/upgrade behavior.
- Public package, documentation and fixtures remain sanitized and independently usable.
- Implementation, integration, publication, release, rollout, adoption and commercial validation remain distinct proof and authority boundaries.

### Invalid Substitutes

- New headings, longer prompts, parser branches or green unit tests presented as proof that agents preserve owner intent in realistic work.
- An approval hash presented as proof that the approved artifact faithfully represents the owner's requested outcome.
- AC coverage that begins only after the original capability has already been narrowed, proxied or omitted.
- The same implementation agent self-certifying that its interpretation preserved intent without an independently reviewable audit and QA verdict.
- A canary, preview, internal data model, debug-only path, related environment, screenshot, build or test suite presented as completion of a broader user-operable outcome.
- One hand-authored regression prompt or one successful model run presented as behavioural reliability across agents, tasks or releases.
- A maximal implementation or speculative completeness presented as fidelity to a bounded owner request.
- Public documentation or fixture text that reproduces private transcripts, absolute personal paths, proprietary project content or maintainer-only context.
- Local source/self-hosted proof presented as packaged release, consumer upgrade, adoption or commercial validation.

### Artifact Targets

- `REQUIREMENTS.md` Intent Spine and concise semantic approval envelope contract.
- Intent commitment coverage and read-only audit artifacts with freshness/provenance.
- CLI readiness, lifecycle, audit, closeout, Doctor and status enforcement.
- `user-outcome-journey` structured evidence recipe and invalid-substitute validation.
- Intent-aware requirements, planner, clarify, implement, QA, Epic and retro skills/prompts across supported generated agent surfaces.
- Sanitized deterministic fixtures plus held-out multi-trial behavioural evaluations and graders.
- Package/self-hosted parity checks, compatibility/upgrade coverage and exact packaged-artifact disposable journey evidence.
- Current owner-facing dogfood receipt and independent Epic QA/acceptance audit.

### Parent AC Proof Ownership

- AC13, AC14, AC15: owner `TASK-084`; required evidence: Generated/self-hosted/package parity, safe upgrade results, disposable exact-package journey, current dogfood receipt, strict Doctor/full suite, and independent Epic QA.

## Goal

Produce package/managed parity, safe compatibility, exact-package disposable proof, current dogfood
proof and independent Epic review without crossing release authority.

## Approach

Freeze candidate identity, align managed surfaces, test legacy upgrade/no-op behavior, run the
disposable journey, then use EPIC-014 as dogfood and submit all evidence to independent QA.

## Phases

1. Candidate identity, generated/self-hosted parity and package contents.
2. Legacy compatibility and safe upgrade planning.
3. Exact-package disposable journey and green-but-wrong rejection.
4. Current dogfood journey and independent Epic QA.

## Acceptance Criteria

- [x] AC1: Managed/package parity and safe historical compatibility are proven.
- [x] AC2: The disposable exact-package journey rejects proxy completion.
- [x] AC3: The current dogfood journey remains concise and practical.
- [x] AC4: Independent QA verifies every evidence layer and resolves findings.
- [x] AC5: Release, rollout and adoption boundaries remain explicit.

## Validation

- AC1 / parent AC13: `runtime-target-source` exact-wheel hashes/parity, build/package inspection,
  and fingerprinted legacy upgrade/no-op receipts.
- AC2-AC3 / parent AC14: exact-package disposable and `user-outcome-journey` current dogfood
  receipts.
- AC4-AC5 / parent AC15: independent QA, full suite, strict Doctor and authority-boundary review.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/intent-integrity-outcome-proof` | 423 repository tests and `git diff --check` pass; exact wheel SHA-256 `0558c818...` binds 31 package resources, every generated asset across four hosts and all 40 manifest-covered sdist sources; the disposable Epic rejects an actually narrowed preview child after sourced review; the live dogfood packet binds the owner approval turn, exact synopsis, workflow artifacts and blocking QA; legacy plan/apply/no-op preserves historical hashes | Local candidate only; publication/release/rollout unauthorized | `evidence/package-journeys.json`, `evidence/dogfood-journey.json`, `evidence/dogfood-epic-014.md`, `evidence/validation-receipt.md`, retained candidate distributions, and child `EVIDENCE.json` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Align Candidate Surfaces | Synchronize package source, prompts/skills, generated/installed assets and docs. | AC1 | Run hash/parity and package-content checks. | Done | TASK-080, TASK-081, TASK-082, TASK-083 | package/managed assets and parity tests | No | bounded-return |
| 2 | Prove Safe Compatibility | Exercise legacy/current upgrade plan/apply/no-op without invalidating historical work. | AC1 | Review exact plans, preservation hashes and second no-op. | Done | 1 | upgrade fixtures and receipts | No | bounded-return |
| 3 | Run Exact-Package Journey | Install the built candidate in a disposable repo and reject a green-but-wrong implementation. | AC2 | Inspect resulting Intent, audit, proof, QA and closeout state. | Done | 2 | disposable journey artifacts | No | bounded-return |
| 4 | Run Current Dogfood | Exercise EPIC-014 with the candidate and record approval burden, friction and proof boundaries. | AC3 | Review sanitized dogfood receipt against the owner's actual journey. | Done | 3 | dogfood evidence | No | bounded-return |
| 5 | Prepare Independent Epic Review | Bind code, behaviour, exact package identity, structured journeys, initial QA findings and release boundaries into one independently inspectable packet. | AC4, AC5 | Fresh independent QA inspects the packet in Testing; stop before release. | Done | 4 | QA/evidence/retro artifacts | No | bounded-return |

## Parent AC Evidence

- AC13: Retained wheel `sha256:0558c818146f91c90b4c9506806dda40735e7588d7f99640c55706cd5ee600a1`
  and source distribution `sha256:b93fde4cf936f6fce86c9dccc83ad6ef5e61dd0348b3d273dcb2d1d915a018b8`
  bind 31 wheel resources to current source, every generated asset across Codex, Copilot, Claude and
  Cursor, every one of the 40 manifest-covered sdist sources and helper SHA `42daae38...`.
  Fingerprinted legacy apply
  preserved tracker/backlog/guidance/user-note hashes and the owner collision; the second plan is
  `current`.
- AC14: The exact-wheel disposable Epic creates an internally green preview-only child, derives a
  proxy decision from the actual claim scope, result, observations and artifact, and rejects
  readiness while naming the missing complete archive. Restoring the real archive journey then
  passes audit, outcome evidence, adversarial QA, acceptance audit and Epic closeout. The current
  dogfood packet captures the actual Codex task/approval turn, exact meaning-first synopsis output,
  approved requirements fields, current audit and lifecycle artifact identities, plus both blocking
  independent reviews; the narrative receipt is supplementary rather than self-sufficient proof.
- AC15: Publication, tagging, release, merge, rollout and consumer adoption remain unauthorized and
  unproven. The first independent review returned Changes requested with six findings. The second
  returned Changes requested because live dogfood was narrative-only, two packaged tests were not
  parity-bound and one receipt hash was stale. All nine findings are addressed in the current
  packet. Fresh read-only Codex review `01a02279-e6c1-7fa0-a652-4980667e18d4` returned Pass with no
  blockers and independently verified AC13-AC15 against the retained artifacts.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: The exact-wheel receipt records the wrong and restored child identities;
  the current dogfood packet is mechanically captured from the live CLI, owner observation and
  hashed lifecycle artifacts. Independent QA regenerated the packet byte-for-byte and sampled the
  raw approval event, exact synopsis, current audit and package artifacts.
- Reviewer independence: Fresh read-only Codex session
  `01a02279-e6c1-7fa0-a652-4980667e18d4` inspected requirements, diff, raw behavioural trials,
  retained distributions, exact-wheel receipt and dogfood receipt without relying on implementation
  summaries or having write authority.
- Evidence: `evidence/independent-qa.md` records Pass and no blockers for the preserved pre-FIX-007
  candidate; the bounded post-closeout correction then passed 423 repository tests,
  `git diff --check`, strict Doctor, live dogfood regeneration, release-trial grading, retained
  distribution hashes and source/package parity all pass at their stated proof layers.
- Findings: Exact-wheel testing found that proxy rejection omitted the lost capability from its
  lifecycle message; the CLI now surfaces it. Initial independent QA then found that the journey
  supplied a proxy label instead of detecting a wrong child, parity sampled too few assets, the
  wheel was not retained, structured dogfood evidence was absent and trial provenance was
  incomplete. The current candidate retains both distributions, binds all shipped/generated
  surfaces, creates and reviews an actually narrowed child, records structured package/dogfood
  claims, and retains session-bound behavioural trials. A second independent review then required
  inspectable live-dogfood provenance, complete sdist parity and a corrected receipt chain. The
  current candidate now binds those sources directly. Fresh independent QA verified every
  remediation, found no new blocker and answered the core
  adversarial question No within the tested scope. Its read-only sandbox could not independently
  rerun pytest or the write-heavy disposable journey. The reviewed distributions remain retained
  under `evidence/candidate/reviewed-pre-fix/`; FIX-007 has its own fresh full-suite and exact-package
  receipts rather than being misrepresented as part of that earlier independent execution.

## Retro

- Date: 2026-08-21
- Reusable lessons: A blocked proxy is still under-informative if the maintainer cannot see which
  user capability was lost. More importantly, a lifecycle gate responding to an agent-supplied
  `proxy` label does not prove detection: the disposable child itself must be wrong, the review must
  cite its actual outcome fields, and the receipt must retain both wrong and restored identities.
- Conventions or agent assets updated: Release package verifier now checks all generated host
  surfaces and wheel resources, every manifest-covered sdist source, fingerprinted legacy preservation,
  evidence-derived narrowing detection, exact-package Intent approval/audit/evidence/QA and
  closeout. The dogfood capture script binds actual owner observation, synopsis output, workflow
  state and blocking review identities instead of accepting a narrative receipt as outcome proof.
- Follow-up tasks: A separately authorized release must rebuild from the reviewed commit and prove
  publication, trusted release, rollout and consumer adoption; none is part of this Task.
- Missed in-scope work: None. The final independent review verified all nine earlier blocking
  findings as resolved; its read-only execution boundaries remain stated rather than converted into
  unsupported rerun claims.

## Notes

- Task: TASK-084
- Title: Prove Packaging Parity And Real Journeys
- Created: 2026-08-21
