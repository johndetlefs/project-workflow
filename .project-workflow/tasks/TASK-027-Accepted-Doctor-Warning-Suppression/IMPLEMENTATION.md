## User Story

As a maintainer, I want to explicitly accept known doctor warnings, so routine
validation output stays focused on new or actionable issues.

## Acceptance Criteria

- [x] AC1: A warning with a matching accepted fingerprint is hidden from default `doctor` output and does not fail `doctor --strict`.
- [x] AC2: `doctor --show-accepted` prints accepted warnings separately.
- [x] AC3: A warning with the same legacy class but a different fingerprint is still shown.
- [x] AC4: Config parsing accepts a simple list of fingerprints and an object list with optional reason text.
- [x] AC5: README and generated guidance document the accepted-warning workflow.

## Validation

- AC1: `test_doctor_hides_accepted_warning_fingerprints_and_shows_on_request` covers default suppression and strict mode.
- AC2: `test_doctor_hides_accepted_warning_fingerprints_and_shows_on_request` covers `--show-accepted`.
- AC3: `test_doctor_string_accepted_fingerprint_does_not_hide_different_warning` covers non-matching warnings.
- AC4: Tests cover string and object accepted-warning entries.
- AC5: README, changelog, Codex guidance, and Cursor guidance updated. `./.project-workflow/cli/workflow doctor` and `./.project-workflow/cli/workflow doctor --show-accepted` verified.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Extend config | Add accepted doctor warning config parsing and fingerprint helpers. | AC1, AC4 | Config tests pass. | Done |
| 2 | Filter doctor output | Hide accepted warnings by default, preserve strict behavior for unaccepted issues, and add `--show-accepted`. | AC1, AC2, AC3 | Doctor tests pass. | Done |
| 3 | Document workflow | Explain how to accept fingerprints and audit accepted warnings. | AC5 | README/guidance review and doctor pass. | Done |

## QA & Code Review

- Verdict: Pending.
- Evidence: Pending implementation and validation.
- Findings: Pending.

## Retro

- Reusable lessons: Pending.
- Conventions or agent assets updated: Pending.
- Follow-up tasks: Pending.

## Notes

- Task: TASK-027
- Title: Accepted Doctor Warning Suppression
- Created: 2026-06-25
