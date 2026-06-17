# Acceptance Map

## Summary

- Epic: EPIC-003
- Title: Workflow Discipline Gates
- Last updated: 2026-06-17
- Purpose: Track parent acceptance criteria coverage before decomposition so the epic does not repeat the workflow-discipline gap it is meant to fix.

## Coverage Matrix

| Parent AC | Requirement Summary | Proposed Child Coverage | Evidence Status | Closeout Status |
| --- | --- | --- | --- | --- |
| AC1 | Minimum task/epic context rubric is defined. | TASK-011 | TASK-011 QA passed | Satisfied |
| AC2 | Missing blocking context does not silently scaffold work. | TASK-011 | TASK-011 QA passed | Satisfied |
| AC3 | Epic decomposition requires sufficient parent requirements. | TASK-012 | TASK-012 QA passed | Satisfied |
| AC4 | Epic child scaffolds inherit parent context needed for decisions. | TASK-012 | TASK-012 QA passed | Satisfied |
| AC5 | Implementation readiness validation exists for standalone and epic child tasks. | TASK-012 | TASK-012 QA passed | Satisfied |
| AC6 | Status transitions enforce readiness or explicit exceptions. | TASK-012 | TASK-012 QA passed | Satisfied |
| AC7 | `TASK-###` allocation is globally unique across standalone and epic child tasks. | TASK-010 | TASK-010 QA passed | Satisfied |
| AC8 | Doctor/validation gives actionable discipline-gate remediation. | TASK-012, TASK-014 | TASK-012 and TASK-014 QA passed | Satisfied |
| AC9 | Generated docs and agent assets explain the junior-developer lifecycle. | TASK-011, TASK-014 | TASK-011 and TASK-014 QA passed | Satisfied |
| AC10 | Automated fixtures cover vague intake, readiness, discovery exceptions, ID allocation, and compatibility. | TASK-014 | TASK-014 QA passed | Satisfied |
| AC11 | Generated agent guidance defines the owner-directed, agent-operated role split. | TASK-013, TASK-014 | TASK-013 and TASK-014 QA passed | Satisfied |
| AC12 | User-facing docs explain conversational intake rather than manual template completion. | TASK-011, TASK-014 | TASK-011 and TASK-014 QA passed | Satisfied |
| AC13 | Gate failures distinguish repo-gatherable facts, assumptions, and owner-required decisions. | TASK-013, TASK-014 | TASK-013 and TASK-014 QA passed | Satisfied |

## Deferrals

No deferrals approved.

## Closeout Gate

EPIC-003 must not be marked `Complete` until every parent AC above has passing child-task evidence or an owner-approved deferral with a follow-up reference.
