## User Story

As a workflow reviewer, I want structured proof to include artifact identity and contradiction checks, so that stale evidence files or wrong target/source claims cannot pass epic gates.

## Parent AC Coverage

- AC5, AC6, AC7, AC12, AC13, AC15, AC16, AC17

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

## Acceptance Criteria

- [x] AC1: Built-in proof recipes require `evidence_artifact_hash` and validate SHA-256 for local evidence artifacts. Covers parent AC5 and AC13.
- [x] AC2: Stale evidence artifact hashes fail doctor and prevent epic audit credit. Covers parent AC7, AC12, AC13, AC16, and AC17.
- [x] AC3: Runtime target/source prose contradictions fail doctor when structured evidence proves a different execution target or source artifact. Covers parent AC7, AC12, AC16, and AC17.
- [x] AC4: Existing valid structured visual evidence still satisfies epic audit after the stricter hash field is added. Covers parent AC5, AC6, and AC15.
- [x] AC5: Focused and full regression suites pass. Covers parent AC12.

## Validation

- AC1 / AC5 / AC13: `evidence_artifact_hash` added to all built-in recipe required fields; local evidence artifacts are hashed with SHA-256 and stale hashes are rejected.
- AC2 / AC7 / AC12 / AC13 / AC16 / AC17: `test_stale_evidence_artifact_hash_blocks_doctor_and_audit` proves stale local evidence artifacts fail doctor and audit credit.
- AC3 / AC7 / AC12 / AC16 / AC17: `test_runtime_target_source_prose_contradiction_blocks_doctor` proves contradictory prose target/source claims fail doctor.
- AC4 / AC5 / AC6 / AC15: `test_valid_structured_visual_evidence_satisfies_epic_audit` still passes with the stricter hash field.
- AC5 / AC12: Focused regression run passed: `5 passed, 58 deselected`.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Evidence artifact hash | Require `evidence_artifact_hash`, compute SHA-256 for local evidence files, and reject stale hashes. | AC1, AC2 | Focused pytest regression. | Done |
| 2 | Contradiction checks | Compare explicit prose labels for execution target/source/artifact identity against structured evidence values. | AC3 | Focused pytest regression. | Done |
| 3 | Regression coverage | Add stale-hash and target/source contradiction fixtures while preserving TASK-030 valid/invalid evidence tests. | AC4, AC5 | Focused and full pytest suites. | Done |

## Parent AC Evidence

- AC5: Structured evidence now includes artifact identity via required `evidence_artifact_hash`.
- AC6: Existing recipe trigger and invalid substitute behavior remains covered by the focused structured evidence tests.
- AC7: Stale evidence hashes and contradictory target/source claims are rejected by doctor/audit gates.
- AC12: Added regression tests for stale evidence artifact identity and runtime target/source contradiction.
- AC13: Evidence freshness is enforced for local evidence artifacts with SHA-256 identity.
- AC15: Valid visual/reference evidence still satisfies audit with the stricter hash field.
- AC16: Doctor fails invalid current states where manual edits leave stale or contradictory structured evidence in Review/Complete.
- AC17: Prose claims that conflict with structured claim-to-evidence records fail doctor instead of being accepted as closeout proof.

## QA & Code Review

- Verdict: Pass
- Evidence: `.venv/bin/python -m pytest tests/test_doctor.py -k "stale_evidence or runtime_target_source or structured or recipe or visual_reference or invalid_substitute or valid_structured"` passed with 5 selected tests; `.venv/bin/python -m pytest` passed with 63 tests.
- Findings: No blocking findings.

## Retro

- Reusable lessons: Artifact identity belongs inside the structured evidence gate, because doc-level QA cannot tell whether a referenced proof file changed.
- Conventions or agent assets updated: Structured evidence recipes now require local evidence artifact hashes.
- Follow-up tasks: Generated acceptance-summary consistency can be hardened further after the remaining amendment/adoption/guidance slices.

## Notes

- Task: TASK-032
- Title: Artifact Identity Staleness And Summary Gates
- Created: 2026-07-09
