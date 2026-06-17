## User Story

As a workflow owner, I want agents to gather a minimum set of conversational requirements before downstream work, so vague prompts do not become under-specified tasks or epics.

## Parent AC Coverage

- EPIC-003 AC1: Minimum task/epic context rubric is defined.
- EPIC-003 AC2: Missing blocking context does not silently scaffold downstream work.
- EPIC-003 AC9: Generated docs and agent assets explain the junior-developer lifecycle.
- EPIC-003 AC12: User-facing docs explain conversational intake rather than manual template completion.

## Acceptance Criteria

- [x] AC1: Covers EPIC-003 AC1 by adding the minimum context rubric to README, Task prompt, Requirements prompt, and Codex task/requirements skills.
- [x] AC2: Covers EPIC-003 AC2 by documenting stop/clarify behavior when blocking context is missing.
- [x] AC3: Covers EPIC-003 AC9 by updating generated workflow guidance with readiness and intake lifecycle steps.
- [x] AC4: Covers EPIC-003 AC12 by stating that owners provide context conversationally while agents maintain workflow artifacts.

## Validation

- AC1: Guidance now names problem/opportunity, outcome, actor/system, scope, acceptance signal, constraints, priority/risk, and examples.
- AC2: Requirements prompt and skills instruct agents to stop, ask focused questions, or record discovery/accepted risk.
- AC3: Tests assert generated agent assets include readiness guidance.
- AC4: README and prompts state that manual template completion is not the normal path.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Minimum Context Rubric | Document required owner context for tasks and epics. | AC1: Minimum context appears in user-facing and generated guidance. | Inspect README and prompts. | Done |
| 2 | Clarification Behavior | Tell agents to ask targeted questions or record discovery when context is missing. | AC2: Missing context no longer silently proceeds downstream. | Inspect Requirements prompt and skills. | Done |
| 3 | Conversational Owner Path | Make owner-as-PM/BA conversational intake explicit and align generated lifecycle guidance. | AC3, AC4: Docs avoid manual-template-first language and generated guidance names the readiness lifecycle. | Inspect README, prompts, and generated guidance. | Done |

## Parent AC Evidence

- EPIC-003 AC1: Minimum context rubric added to README, Task prompt, Requirements prompt, and project-task/project-requirements skills.
- EPIC-003 AC2: Requirements guidance now stops on missing discovery context and records bounded discovery work explicitly.
- EPIC-003 AC9: Generated guidance mentions readiness and intake lifecycle steps.
- EPIC-003 AC12: README and prompts state the owner supplies context conversationally and the agent operates artifacts.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: README, Task prompt, Requirements prompt, Planner/Implement/Epic prompt touchpoints, Codex skills, Cursor rules.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 30 tests after guidance assertions.
- Findings: None.
- Verdict: Pass.

## Retro

- Reusable lessons: Intake quality should be framed as owner conversation plus agent artifact maintenance.
- Conventions or agent assets updated: README, prompts, Codex skills, Cursor rules.
- Follow-up tasks: None.
- Missed in-scope work: None.
