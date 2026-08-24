# Clarify Fitness Baseline

- Epic: EPIC-016
- Date: 2026-08-24
- Candidate baseline: Project Workflow 0.6.0 at `c215b4379c4b38a4efee672c64c2b4b599385d04`
- Scope: read-only assessment of the current Clarify skill and prompt before planning changes

## Current Contract Inspected

- `.agents/skills/project-clarify/SKILL.md`
- `src/project_workflow/prompts/Clarify.prompt.md`
- `.github/prompts/Clarify.prompt.md`
- Planner, Requirements, Implement, QA and managed AGENTS routing around Clarify
- Current test references to Clarify behavior

## Scenario Findings

| Scenario | Current Result | Evidence | Consequence |
| --- | --- | --- | --- |
| Pre-approval material ambiguity | Pass | Clarify records material open questions, asks one at a time, and updates decisions after the answer. | Real product decisions can be resolved without batching owner prompts. |
| Clean bounded request | Pass with unproved behavior | The contract limits questions to matters affecting scope, risk, data, billing or user-visible behavior, but no held-out behavioral test proves it avoids needless questions. | The intended lightweight path exists in prose but is not regression-protected. |
| Post-plan implementation-detail inconsistency | Pass in contract | Clarify resolves in-envelope plan detail autonomously and returns material changes for refreshed approval. | Ordinary planning can proceed without generic owner reapproval. |
| Internally consistent plan that proxies the Intent | Partial | Full-contract Epic children run the parent intent audit and must name the user-visible consequence, but standalone Tasks and Epic parents do not receive an equivalent explicit Intent comparison. | A syntactically consistent proxy can escape Clarify outside the child-specific path. |
| Epic parent without `IMPLEMENTATION.md` | Fail | Both the skill and prompt require an `IMPLEMENTATION.md` User Story and instruct Clarify to stop when it is absent, while an Epic parent lawfully has requirements, contract and decomposition rather than a parent implementation file. | The mandatory post-plan Clarify step is not directly usable for the Epic it is meant to check. |
| Full-contract Epic child | Pass in contract | The skill requires a current parent intent audit and rejects AC consistency as a substitute for Intent fidelity. | Child planning has the correct authority check, subject to behavioral proof. |
| Ambiguous mid-Epic drift | Fail | Clarify has no coordination-boundary trigger or `inside-envelope` / `drift-detected` / `approved-change` routing contract. | The Coordinator cannot use Clarify as a bounded decision aid during long-Epic drift without improvising. |
| User answer already exists in context | Pass | The prompt requires recording the existing answer and not asking again. | Clarify need not manufacture approval fatigue. |

## Test Coverage Finding

Repository search found installation/parity references to Clarify assets but no focused behavioral
scenario suite covering the modes above. Static managed-copy parity is not evidence that Clarify
asks the right question, avoids unnecessary questions, or catches an Intent proxy.

## Disposition

Clarify is useful but not fully fit for the approved Coordinator model. Preserve its material-
question discipline and post-plan autonomy. Correct only the reproduced gaps:

1. Anchor Clarify first to approved `REQUIREMENTS.md` Intent/Intent Spine, using an implementation
   User Story when it exists rather than requiring one for every target.
2. Support three explicit modes: pre-approval ambiguity, post-plan consistency, and Coordinator-
   routed ambiguous drift.
3. Support Epic parents, Epic children and standalone Tasks without inventing a parent
   `IMPLEMENTATION.md`.
4. Keep boundary detection and routine inside-envelope decisions with the Coordinator; invoke
   Clarify only when a material question remains unresolved.
5. Add held-out failure and counter-failure behavior tests before claiming improvement.

No separate Clarify document stack, review loop, periodic invocation, or additional owner approval
stage is justified.
