# Epic Retro

- Epic: EPIC-006
- Title: Epic Control Gates For Requirement Drift Prevention
- Last updated: 2026-07-09

## Lessons

- Requirements drift prevention needs gates at the point of action: approval envelopes, decomposition authority, proof ownership, structured evidence, and lifecycle checks mattered more than adding more prose.
- Guidance must be updated across every agent entry point. README-only guidance is not enough when agents use prompt templates, Codex skills, generated managed blocks, or Cursor rules.
- Generated artifacts must be validated against the same gates that later consume them. TASK-036 caught and fixed a scaffolded `EVIDENCE.json` shape that used a comma-separated `parent_ac` value the validator could not credit per parent AC.
- Approval fatigue is itself a drift risk. The implemented model records a bounded owner-approved envelope and then asks for fresh owner input only for material changes, amendments, deviations, proof-obligation changes, artifact identity changes, or deferrals.

## Follow-up Tasks

- None.

## Deferrals

- None.

## Missed In-Scope Work

- None. One in-scope defect was found during closeout: scaffolded multi-AC `EVIDENCE.json` records were not individually creditable. It was fixed in TASK-036 and covered by regression tests before epic closeout.
