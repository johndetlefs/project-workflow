# Requirements

## Summary

- Task: TASK-027
- Title: Accepted Doctor Warning Suppression
- Last updated: 2026-06-25

## Goal

Allow repositories to permanently acknowledge known doctor warnings so accepted
legacy or intentional workflow debt no longer appears in normal doctor output.

## Non-Goals

- Do not hide new warnings by broad category.
- Do not change strict-mode behavior for unaccepted warnings.
- Do not remove the existing legacy-warning classification.
- Do not require a separate database, generated cache, or remote service.

## Users & Context

- Maintainers use `project doctor` as a routine validation gate.
- Some historical workflow artifacts are known and accepted, but recurring legacy
  warnings create noise in every status report.
- Suppression must be explicit, reviewable, and tied to stable warning
  fingerprints so future warnings still surface.

## Requirements (Outcome-Focused)

- Repos can list accepted doctor warnings in `.project-workflow/config.json`.
- Accepted warnings are matched by stable fingerprints derived from issue path
  and message.
- Normal `doctor` output omits accepted warnings from the visible warning list
  and from failure calculations.
- `doctor --show-accepted` displays accepted warnings for audit.
- Doctor output reports how many warnings were hidden when accepted warnings are
  suppressed.
- Accepted-warning config is tolerant of optional notes/reasons for humans.
- Documentation explains how to discover and add accepted warning fingerprints.

## Acceptance Criteria (Verifiable)

- AC1: A warning with a matching accepted fingerprint is hidden from default
  `doctor` output and does not fail `doctor --strict`.
- AC2: `doctor --show-accepted` prints accepted warnings separately.
- AC3: A warning with the same legacy class but a different fingerprint is still
  shown.
- AC4: Config parsing accepts a simple list of fingerprints and an object list
  with optional reason text.
- AC5: README and generated guidance document the accepted-warning workflow.

## Clarify Pass

- Scope clarified: suppression is per exact warning fingerprint, not per warning
  class, prefix, path glob, or severity.
- Audit clarified: accepted warnings are hidden by default but available with
  `doctor --show-accepted`.
- Strict mode clarified: accepted warnings do not block strict mode; unaccepted
  warnings still behave exactly as before.
- Config clarified: use `.project-workflow/config.json` because it is already the
  user-owned repo workflow config. Keep entries human-reviewable and support
  optional reasons.
- Risk clarified: if a warning message changes due to improved validation, it
  intentionally reappears until the owner re-accepts the new fingerprint.

## Open Questions (Answer Needed)

- None. Owner requested accepted legacy warnings to be permanently hidden from
  normal reports, with a pragmatic explicit-acknowledgement approach.

## Decisions (Resolved)

- Add config-backed accepted warning fingerprints.
- Suppress only exact fingerprint matches.
- Add `doctor --show-accepted` for audit visibility.
- Print a concise hidden-count summary when accepted warnings are omitted.

## Validation Plan

- Add focused tests for accepted warning suppression, strict mode, audit output,
  and unmatched warning visibility.
- Run the full test suite.
- Run `project doctor` after workflow/task-doc changes.
