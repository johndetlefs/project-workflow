# Epic Retro

- Epic: EPIC-009
- Title: Workspace Mode And Multi-Repo Coordination
- Last updated: 2026-07-29

## Lessons

- The useful workspace abstraction is small: one optional registry, one authority, independent Git observations, and repository-attributed evidence. It does not require orchestration machinery.
- Path existence is insufficient. Safe registration requires containment after resolution plus an exact, unique Git top-level match.
- Backward compatibility is strongest when legacy top-level status fields remain unchanged and workspace records are additive only when configured.
- Validation evidence and later delivery evidence are different layers. Review requires executed validation and its source, while branch, PR, merge, release, or deployment may truthfully remain not recorded or not authorized.
- Exact-target acceptance can remain non-mutating by injecting the proposed registry in-process, hashing the invoked source, and comparing each target Git root before and after.

## Follow-up Tasks

- Real JohnDetlefs workspace adoption and canonical upgrade remain a separate owner-authorized lifecycle action.
- Expected-branch policy across arbitrary work items remains intentionally out of scope; this epic reports live and recorded branch mismatches where evidence supplies an expected branch.

## Deferrals

- No in-scope acceptance criterion was deferred.
- Child-to-parent workflow discovery, automatic validation execution, cross-repository Git actions, hosted control planes, plugin systems, generalized orchestration, and enterprise governance remain explicit non-goals rather than deferred EPIC-009 work.

## Missed In-Scope Work

- None.
