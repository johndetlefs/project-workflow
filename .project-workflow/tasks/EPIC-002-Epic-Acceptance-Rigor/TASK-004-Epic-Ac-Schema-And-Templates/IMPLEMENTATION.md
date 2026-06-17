## User Story

As a project-workflow maintainer, I want epic and child-task templates to carry parent acceptance-criteria coverage explicitly, so that every epic child task starts with a visible connection back to the parent ACs it is meant to prove.

## Goal

- Update schema, templates, and generated guidance so `TASK-004` satisfies parent epic coverage for EPIC-002 AC1, AC2, AC6, and AC15.

## Parent AC Coverage

- EPIC-002 AC1: Epic requirements templates and agent guidance create stable numbered parent AC IDs.
- EPIC-002 AC2: Epic tracker rows support canonical parent AC coverage.
- EPIC-002 AC6: Epic-managed child implementation and QA templates include parent AC sections.
- EPIC-002 AC15: Root tracker versus epic tracker rules are explicit.

## Acceptance Criteria

- [x] AC1: Covers EPIC-002 AC1 by updating epic requirements templates and generated agent guidance to create stable numbered parent AC IDs by default and preserve IDs across revisions.
- [x] AC2: Covers EPIC-002 AC2 by defining the new epic tracker parent AC coverage field and documenting backward-compatible `Notes` coverage parsing.
- [x] AC3: Covers EPIC-002 AC6 by adding `Parent AC Coverage` and `Parent AC Evidence` sections to epic-managed child docs without adding those sections to standalone task scaffolds.
- [x] AC4: Covers EPIC-002 AC15 by documenting global tracker versus epic tracker ownership rules in generated guidance and user-facing docs.

## Approach

- Change template generation in the package source first, then mirror generated local helper behavior.
- Keep standalone task scaffolds unchanged unless shared helper text must mention epic-specific behavior.
- Update generated Codex skills/prompts and user-facing docs where they describe epic lifecycle and tracker ownership.
- Add focused tests that inspect generated artifact text and schema behavior rather than relying on manual review.

## Phases

### Phase 1

- Update epic requirements/tracker and child scaffold templates to carry parent AC coverage structure.
- Update generated guidance for AC ID stability and tracker ownership.
- Validate with focused unit tests that generated artifacts contain the expected sections and schema.

### Phase 2

- Mirror package-source changes into this repo's installed workflow helper as needed.
- Run parity checks and workflow doctor.
- Record implementation evidence for every child AC and parent AC mapping.

## Tasks

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Stable Epic AC Template | Update epic requirements and generated guidance so parent AC IDs are created and preserved by default. | AC1 / EPIC-002 AC1: generated epic requirements and agent guidance include stable numbered AC instructions. | Run targeted tests or inspect generated epic requirements/guidance for stable AC ID instructions. | Done |
| 2 | Parent AC Tracker Field | Define the canonical parent AC coverage field for new epic tracker rows and document legacy `Notes` support. | AC2 / EPIC-002 AC2: schema/guidance exposes parent AC coverage as first-class and mentions backward compatibility. | Run targeted tests or inspect generated epic tracker schema and docs. | Done |
| 3 | Epic Child Parent Evidence Sections | Update epic-managed child scaffolds to include parent AC coverage/evidence sections without changing standalone task scaffolds. | AC3 / EPIC-002 AC6: epic child docs include parent AC sections; standalone task docs do not. | Run scaffold tests for epic child and standalone task outputs. | Done |
| 4 | Tracker Ownership Guidance | Update docs and generated agent guidance to explain global tracker summary rows versus epic tracker child rows. | AC4 / EPIC-002 AC15: generated guidance and docs state ownership rules clearly. | Inspect generated Codex/Copilot/Cursor assets and README/help text. | Done |

## Validation

- AC1 / EPIC-002 AC1: targeted tests or generated-artifact inspection for stable parent AC IDs and preserve-ID guidance.
- AC2 / EPIC-002 AC2: targeted tests or generated-artifact inspection for parent AC coverage field and legacy `Notes` support documentation.
- AC3 / EPIC-002 AC6: targeted tests comparing epic-managed child scaffolds with standalone task scaffolds.
- AC4 / EPIC-002 AC15: targeted tests or generated-artifact inspection for tracker ownership guidance.

## Parent AC Evidence

- EPIC-002 AC1: Implemented in `src/project_workflow/cli.py`, `src/project_workflow/templates/workflow.py`, `.project-workflow/cli/workflow.py`, `src/project_workflow/codex/AGENTS.md`, `src/project_workflow/codex/skills/project-epic/SKILL.md`, `src/project_workflow/prompts/Epic.prompt.md`, and `.github/prompts/Epic.prompt.md`. Evidence: `tests/test_doctor.py::test_epic_decompose_preserves_source_ac_ids_in_notes` passed as part of `.venv/bin/pytest tests/test_doctor.py`.
- EPIC-002 AC2: Implemented canonical `Parent ACs` epic tracker column plus legacy seven-column support. Evidence: `tests/test_doctor.py::test_epic_decompose_preserves_source_ac_ids_in_notes` and `tests/test_doctor.py::test_doctor_accepts_legacy_epic_tracker_schema` passed.
- EPIC-002 AC6: Implemented epic-child-specific requirements and implementation templates with `Parent AC Coverage` and `Parent AC Evidence`, while standalone task scaffolds remain unchanged. Evidence: `tests/test_doctor.py::test_epic_child_scaffold_carries_parent_ac_sections` passed.
- EPIC-002 AC15: Updated README, generated Codex guidance, generated Copilot prompt mirror, and generated Cursor rule with global tracker versus epic tracker ownership rules. Evidence: `.venv/bin/project doctor` passed with only pre-existing historical QA warnings.

## QA & Code Review

- Date: 2026-06-17
- Reviewed areas: package CLI, generated local workflow template, installed local helper, generated Codex/Copilot/Cursor guidance, README, and fixture tests.
- Validation evidence: `.venv/bin/pytest tests/test_doctor.py` passed with 18 tests; `./.project-workflow/cli/workflow doctor` passed with only pre-existing APP QA warnings; `.venv/bin/project doctor` passed with the same pre-existing warnings; `cmp -s src/project_workflow/templates/workflow.py .project-workflow/cli/workflow.py` returned 0; `cmp -s src/project_workflow/prompts/Epic.prompt.md .github/prompts/Epic.prompt.md` returned 0; `git diff --check` passed.
- AC evidence: AC1 / EPIC-002 AC1 covered by generated epic AC and guidance updates; AC2 / EPIC-002 AC2 covered by `Parent ACs` schema plus legacy tracker support; AC3 / EPIC-002 AC6 covered by epic-child parent coverage/evidence sections and standalone-noise fixture; AC4 / EPIC-002 AC15 covered by README and generated agent guidance.
- Verdict: Pass.
- Findings: None.

## Retro

- Reusable lessons: Self-hosted parity checks caught a stale generated prompt mirror immediately; keep package and installed generated assets aligned as part of every project-workflow behavior change.
- Conventions or agent assets updated: README, Codex `AGENTS.md`, Codex `project-epic` skill, Copilot `Epic.prompt.md`, and Cursor rule all now describe parent AC coverage and tracker ownership.
- Follow-up tasks: Continue with TASK-005 for stronger AC-aware decomposition behavior and unmapped AC reporting.

## Notes

- Task: TASK-004
- Title: Epic AC Schema And Templates
- Created: 2026-06-17
