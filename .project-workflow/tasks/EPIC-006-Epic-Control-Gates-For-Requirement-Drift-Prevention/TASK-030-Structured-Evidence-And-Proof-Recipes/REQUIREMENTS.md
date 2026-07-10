# Requirements

## Summary

- Task: TASK-030
- Title: Structured Evidence And Proof Recipes
- Parent AC Coverage: AC5, AC6, AC7, AC12, AC15, AC17
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
- AC15: owner `TASK-030, TASK-032`; required evidence: Visual calibration and delivered-artifact comparison recipe tests.
- AC17: owner `TASK-030, TASK-032`; required evidence: Structured claim-to-evidence ledger and contradictory prose checks.

## Goal

Add a structured evidence layer for high-risk proof claims so epic children cannot satisfy parent acceptance criteria with prose, generic QA, or evidence from the wrong artifact/source.

The child outcome is that proof-recipe-triggered work has a machine-readable `EVIDENCE.json` ledger, recipe-specific required fields, invalid-substitute rejection, status/doctor/audit gates, and regression tests proving visual/reference-fidelity claims cannot advance with QA prose alone.

## Non-Goals

- Do not build perfect visual diff, browser automation, deployment verification, or source attestation tooling.
- Do not require structured evidence for ordinary work that does not trigger a proof recipe.
- Do not make `EVIDENCE.json` a replacement for human-readable QA notes; it is the gate input for material proof claims.
- Do not hard-code ChatGPT, MCP, widget, playground, or deployment-provider concepts into the core model.

## Users & Context

- Agents need a concrete proof format when a task claims visual fidelity, external contract alignment, deployed artifact alignment, runtime target/source correctness, or responsive/multi-context behavior.
- Reviewers need unsupported claims to fail before Review, Complete, audit, or closeout.
- Owners need drift prevention without approving every child transition manually.

## Requirements (Outcome-Focused)

- Define child-local `EVIDENCE.json` as the structured claim-to-evidence ledger for proof-recipe-triggered work.
- Add built-in recipes for `visual-reference-fidelity`, `external-contract-alignment`, `deployed-artifact-alignment`, `runtime-target-source`, and `responsive-visual-behavior`.
- Each recipe must require fields that identify the claim, parent AC, commit, timestamp, relevant artifact/source/target identity, proof method, and evidence artifact.
- Trigger recipes from requirements and material claims, including explicit recipe IDs and common high-risk wording such as matching a reference visual or proving runtime target/source usage.
- Reject invalid substitutes instead of treating them as partial evidence. Examples include code review, unit tests, build output, surrogate surfaces, related environments, service-running claims, tunnels, and deploy success without target/source proof.
- Gate `Review` and `Complete` for supported task and epic-child lifecycle commands when triggered recipes lack valid structured evidence.
- Make `epic audit` refuse parent AC credit when triggered structured evidence is missing, stale-shaped, contradictory, or an invalid substitute.
- Make `doctor` fail invalid current `Review`/`Complete` states caused by manual edits.
- Keep ordinary non-triggered work lightweight; scaffolded evidence files must not force evidence completion unless a proof recipe is triggered.
- Update agent-facing README and skill guidance so QA does not substitute prose for structured proof.

## Acceptance Criteria (Verifiable)

- AC1: `EVIDENCE.json` exists as the structured evidence ledger for recipe-triggered child work and supports recipe-specific required fields. Covers parent AC5.
- AC2: Proof-recipe trigger rules require structured evidence before Review/Complete for visual/reference-fidelity claims. Covers parent AC6 and AC15.
- AC3: Invalid substitutes are rejected by status/audit/doctor gates. Covers parent AC6 and AC7.
- AC4: Epic audit only gives parent AC credit when recipe-triggered claims have valid structured evidence from the assigned child. Covers parent AC5 and AC17.
- AC5: Doctor fails invalid Review/Complete states created outside supported lifecycle commands. Covers parent AC7 and AC17.
- AC6: Regression tests cover missing structured evidence, invalid substitute evidence, and valid structured evidence for generalized visual/reference proof drift. Covers parent AC12.
- AC7: Non-triggered ordinary work remains lightweight and is not forced to complete scaffolded evidence records. Covers parent AC6.

## Open Questions (Answer Needed)

- None blocking. This child implements minimal structured evidence and proof recipes; deeper artifact freshness and contradiction checks are assigned to TASK-032.

## Decisions (Resolved)

- Structured evidence is child-local and stored in `EVIDENCE.json`.
- Recipe-triggered claims must have passing structured claim records; QA prose alone cannot satisfy them.
- Evidence artifact paths are validated when they are local paths; URLs are accepted as externally hosted proof references.
- The first implementation intentionally uses lightweight JSON validation and keyword/explicit-recipe triggers rather than introducing a database or heavy schema dependency.
- Scaffolded `EVIDENCE.json` does not make ordinary work heavier unless requirements or claims trigger a recipe.

## Validation Plan

- Run focused recipe/evidence regression tests.
- Run the full pytest suite.
- Move TASK-030 through `epic status` gates to prove the new structured evidence satisfies its own triggered recipes.
- Run `epic audit --epic-id EPIC-006` and `doctor`.
