# Requirements

## Summary

- Task: TASK-032
- Title: Artifact Identity Staleness And Summary Gates
- Parent AC Coverage: AC5, AC6, AC7, AC12, AC13, AC15, AC16, AC17
- Last updated: 2026-07-09

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Child Charter

### Inherited Invariants

- Parent AC IDs remain stable.
- Approved child rows must match ID, title, and parent AC coverage in `DECOMPOSITION.md`.
- Missing or placeholder contract sections are not valid authority for new/adopted epics.
- Legacy epics without approval envelopes warn until adoption rather than blocking unrelated current work.

### Invalid Substitutes

- Tracker rows without matching `DECOMPOSITION.md` authority.
- Prose summaries that are not backed by child implementation evidence.
- Legacy warnings from unadopted old epics as proof that new/adopted epics satisfy gates.
- Generic owner approval prompts when the work remains inside the approved authority envelope.

### Artifact Targets

- `.project-workflow/cli/workflow.py`
- `src/project_workflow/cli.py`
- `src/project_workflow/templates/workflow.py`
- `tests/test_doctor.py`
- `README.md`
- `.project-workflow/cli/README.md`
- `src/project_workflow/codex/skills/project-epic/SKILL.md`

### Parent AC Proof Ownership

- AC5: owner `TASK-030, TASK-032`; required evidence: Structured evidence records and artifact identity fields.
- AC6: owner `TASK-030, TASK-032`; required evidence: Proof-recipe trigger rules and invalid-substitute rejection tests.
- AC7: owner `TASK-030, TASK-032`; required evidence: Stale, missing, substitute, and contradiction evidence tests.
- AC12: owner `TASK-028, TASK-029, TASK-030, TASK-031, TASK-032, TASK-033, TASK-034, TASK-036, TASK-037`; required evidence: Regression tests for generalized drift failures.
- AC13: owner `TASK-028, TASK-032`; required evidence: Approval/evidence freshness and stale artifact identity tests.
- AC15: owner `TASK-030, TASK-032`; required evidence: Visual calibration and delivered-artifact comparison recipe tests.
- AC16: owner `TASK-028, TASK-032, TASK-037`; required evidence: State-based doctor failures for invalid manual states.
- AC17: owner `TASK-030, TASK-032`; required evidence: Structured claim-to-evidence ledger and contradictory prose checks.

## Goal

Extend structured evidence so proof records are tied to concrete artifact identity and fail when the recorded proof becomes stale or contradicts the prose claim being used for Review, Complete, audit, or doctor.

This child focuses on the smallest enforceable layer after TASK-030: local evidence artifacts must carry a matching SHA-256 identity, and runtime/source/artifact claims written in task docs must not contradict structured evidence records.

## Non-Goals

- Do not solve full browser visual diffing, deployment provenance, or remote URL content hashing.
- Do not require hash validation for external URL evidence artifacts that cannot be read locally by doctor.
- Do not implement the full generated-summary stale-audit system here; this child adds the evidence identity and contradiction checks that summary gates will depend on.
- Do not make ordinary non-triggered tasks fill evidence hashes.

## Users & Context

- Agents need proof records that point at the actual evidence artifact, not a stale screenshot/log path whose contents changed after the claim was written.
- Reviewers need doctor and audit to catch prose saying one target/source pair while structured evidence proves another.
- Epic closeout needs material claims to be bound to current proof artifacts before parent AC credit is granted.

## Requirements (Outcome-Focused)

- Add `evidence_artifact_hash` as a required structured evidence field for all built-in proof recipes.
- When `evidence_artifact` is a local path, compute its SHA-256 and reject records whose stored hash no longer matches.
- Treat stale evidence artifact hashes as blocking structured evidence issues in status gates, doctor, and epic audit.
- Detect simple contradictory prose claims for reference artifact, delivered artifact, execution target, source artifact, source/artifact under test, and artifact identity.
- Reject Review/Complete and doctor states where prose claims one artifact/target/source value while structured evidence proves another.
- Preserve TASK-030 behavior: valid structured evidence still satisfies audit, invalid substitutes still fail, and non-triggered work remains lightweight.
- Add focused regression tests for stale local evidence artifact hashes and runtime target/source prose contradictions.

## Acceptance Criteria (Verifiable)

- AC1: Built-in proof recipes require `evidence_artifact_hash` and validate SHA-256 for local evidence artifacts. Covers parent AC5 and AC13.
- AC2: Stale evidence artifact hashes fail doctor and prevent epic audit credit. Covers parent AC7, AC12, AC13, AC16, and AC17.
- AC3: Runtime target/source prose contradictions fail doctor when structured evidence proves a different execution target or source artifact. Covers parent AC7, AC12, AC16, and AC17.
- AC4: Existing valid structured visual evidence still satisfies epic audit after the stricter hash field is added. Covers parent AC5, AC6, and AC15.
- AC5: Focused and full regression suites pass. Covers parent AC12.

## Open Questions (Answer Needed)

- None blocking. Generated acceptance-map/audit summary freshness remains a follow-up surface for the remaining summary-gate work.

## Decisions (Resolved)

- Local evidence artifacts use `sha256:<digest>` identity.
- URL evidence artifacts may record an identity string but are not fetched or hashed by doctor in this child.
- Contradiction detection is intentionally explicit-label based. It catches structured doc claims such as `Execution target: ...` without trying to infer every prose sentence.
- This child enforces evidence identity at the structured evidence layer; broader approval freshness remains owned by TASK-028 and deeper artifact/source freshness remains available for follow-up hardening.

## Validation Plan

- Run focused evidence identity tests.
- Run the full pytest suite.
- Move TASK-032 through `epic status` gates using its own structured evidence.
- Run EPIC-006 audit and doctor.
