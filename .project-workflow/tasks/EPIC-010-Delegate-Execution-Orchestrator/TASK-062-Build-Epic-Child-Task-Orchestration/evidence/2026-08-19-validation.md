# TASK-062 Validation — 2026-08-19

## Identity

- Authorized branch: `codex/TASK-062-epic-child-orchestration`
- Exact implementation revision exercised live and packaged: `62e56d68732b354c269bec9be928a81c63379e69`
- Exact committed coordinator base: `d53ac2f49aa5dc60a10a7c3b3172f4327c43b0ce`
- Declared environment: locked Python 3.10 environment from `.codex/environments/environment.toml` and `uv.lock`
- Source, generated helper, local helper, and installed-wheel `cli.py` SHA-256: `b468a24ec872c7b25e4c8af5d2a937d0582481b50fb9ed721cf3ec95ed91f945`

## Child AC Crosswalk

| Child AC | Exact requirement | Proof |
|---|---|---|
| AC1 | Only approved children matching decomposition identity and parent AC coverage enter the graph. | Real EPIC-010 resolver plus decomposition/AC drift and omitted-Complete-dependency regressions. |
| AC2 | Persistent creation requires explicit authority and verified current-host support. | Authority/capability/source/capacity matrices emit zero intents; live native calls occur only under the approved envelope. |
| AC3 | Packets name exact authority, dependencies, scope, validation/evidence, forbidden actions, and stop conditions. | Packet serialization regression and bounded live child packets. |
| AC4 | Eligibility respects coordinator verification and available persistent-task capacity with explicit reduction/fallback reporting. | Capacity shrink/no-expand and eligibility-reason regressions; two concurrent live tasks prove host capacity at least two. |
| AC5 | Coordinator verification controls dependency release and failure classifications. | Exact identity/scope/diff/evidence/collision/failure tests plus live predecessor inspection before TASK-063 creation. |
| AC6 | Reconciliation reuses handles, orphans missing handles, and prevents duplicates. | Persist/resume/retry/orphan/canonical-precedence/privacy round trips plus same-handle/cursor live resume with unchanged create count. |
| AC7 | Child QA/Complete and parent closeout gates remain independent. | Lifecycle boundary regressions and read-only closeout result of 70 audit plus 4 retro gaps. |
| AC8 | Retained current-Codex journey proves authorized isolation, concurrency, dependency delay, resume, and blocked closeout. | Sanitized `epic-mode-live-run.json` tied to the exact implementation/package identity. |

## Automated Validation

| Check | Exact command or method | Result |
|---|---|---|
| Focused Epic/delegation | `PATH=/opt/homebrew/bin:$PATH UV_CACHE_DIR=${TMPDIR%/}/project-workflow-uv-cache uv run --locked --python 3.10 pytest -q tests/test_delegate_epic_mode.py tests/test_delegation.py tests/test_delegate_task_mode.py` | Pass: 103 tests |
| Full locked suite | `PATH=/opt/homebrew/bin:$PATH UV_CACHE_DIR=${TMPDIR%/}/project-workflow-uv-cache uv run --locked --python 3.10 pytest -q` | Pass: 365 tests in 50.40s; independent QA repeated 365/365 in 50.72s with UVX path enabled |
| Strict Doctor | `./.project-workflow/cli/workflow doctor --strict` | Pass: no issues; 69 repository-accepted warnings hidden |
| Compilation | Locked Python 3.10 `python -m compileall -q src/project_workflow tests` | Pass |
| Mirror identity | `cmp -s` and SHA-256 across all three Python helpers | Pass: byte-identical at `b468a24e...f945` |
| Diff integrity | `git diff --check` plus independent scope review from `d53ac2f` | Pass |
| Focused child validations | Same-task locked tests in the three authoritative proof worktrees | Pass: 19, 38, and 46 tests |
| Build | `git archive 62e56d6...` to a disposable tree, then `uv build` | Pass: wheel and sdist built from the exact committed revision |
| Wheel install | Fresh Python 3.10 venv plus `uv pip install` of the built wheel and `project --help` | Pass |
| Installed source identity | Hash installed `site-packages/project_workflow/cli.py` and template helper | Pass: both equal committed helper hash |
| Package inspection | Inspected 39 wheel and 79 sdist entries | Pass: no runtime delegation state, TASK-062 evidence, native identity, transcript, credential, `.env`, or cache entry packaged |
| Runtime privacy | Unknown/private field, unsafe handle, stable issue-code, duplicate identity, and failed/orphaned round-trip regressions; committed evidence search | Pass |
| Parent closeout read model | `_epic_audit_rows` and `_epic_retro_issues`; mutating closeout command not invoked | Blocked: 20 parent AC rows, 70 audit gaps, 4 retro gaps; no parent artifact changed |

## Built Artifact Identity

- Wheel: `project_workflow-0.3.0-py3-none-any.whl`
- Wheel SHA-256: `fc33165f924983a219d5ed85a6b2fc55bc134e6a5736290087ad03ffe0436fe2`
- Source distribution: `project_workflow-0.3.0.tar.gz`
- Source distribution SHA-256: `040603012cf44fcbe9dcf8423c7c745c487944e38a852d0d5697fb1ed92401eb`
- Installed wheel `project_workflow/cli.py` SHA-256: `b468a24ec872c7b25e4c8af5d2a937d0582481b50fb9ed721cf3ec95ed91f945`

## Live Current-Codex Epic Journey

The retained sanitized receipt is `epic-mode-live-run.json`. Its final SHA-256 is recorded in `EVIDENCE.json`.

- Negative projections for absent/unknown authority, partial or mismatched plan/runtime capability observations, and zero capacity emitted zero persistent intents; the adapter made zero native create calls for those paths.
- Two authorized independent tasks became active concurrently in distinct isolated worktrees at exact commit `62e56d6...`; the host proves capacity of at least two, not a numeric maximum.
- The coordinator selected an effective child cap of two from requested concurrency three. TASK-063 did not exist during the independent phase.
- Monitoring paused after initial opaque cursors and resumed with the same two task/host/cursor aliases; both cursors advanced, with create count unchanged at two.
- Fresh worktrees initially lacked the dev extra. The same native tasks used the declared locked dev setup and reran the exact commands; no native task was recreated.
- Coordinator Git inspection—not worker summaries—verified exact base, detached checkout, distinct worktree, sole path, bytes/newline/hash, focused validation, scope, and boundaries for both predecessors.
- TASK-063 was created only after both coordinator verifications and passed the same inspection in a third worktree.
- Final authoritative attempts were one each, final create count was three, and unjustified duplicate count was zero.
- Read-only parent inspection remained blocked at 70 audit and 4 retro gaps. No parent/global tracker, acceptance map, lifecycle, delegation runtime, audit, deferral, or retro artifact was mutated.

## Diagnostic Corrections and Task Accounting

Three bounded diagnostic runs preceded the authoritative run:

1. Two tasks at `4bd18b5...` exposed detached native checkout identity; no dependent was created.
2. Three tasks at `b115d75...` exposed shared detached identity across distinct worktrees and uncommitted-at-base proof diffs.
3. Two tasks at `0ab4415...` were stopped before the dependent when independent review found plan/runtime capability split-brain.

The session therefore created seven diagnostic and three authoritative native tasks, ten total. Every diagnostic finding changed the implementation and is excluded from passing AC19 counts. This exceeds the hoped-for minimum, but retaining the failed discoveries is more accurate than presenting an earlier known-defective run as proof.

## Independent QA and Code Review

- Reviewer: independent read-only QA agent, 2026-08-19.
- Code snapshot verdict: Pass; no remaining code findings after the plan/runtime binding, reconciliation, root identity, collision, retry, privacy, duplicate-state, and CLI error-boundary corrections.
- Independent checks: focused 103/103, full locked 365/365, strict Doctor, compileall, `git diff --check`, both mirror comparisons, and scope diff from `d53ac2f` all passed.
- Evidence and final-doc verdict: recorded in `IMPLEMENTATION.md` after final hash/privacy inspection.

## Proof Boundaries

- The authoritative live run proves the dated current-Codex creation, isolation, at-least-two concurrency, dependency delay, monitoring resume, no duplicate creation, coordinator verification, and blocked closeout journey only.
- Deterministic tests prove the wider failure, collision, recovery, privacy, hostile-token, orphan, and canonical-precedence matrix.
- The fresh wheel was built, installed, and inspected locally; it was not published.
- No proof worktree change was staged, committed, integrated, pushed, merged, released, or deployed.
- No parent/global workflow artifact was changed, and no person or external service was contacted.
- Other host adapters, parent Epic acceptance, owner acceptance, release, deployment, adoption, and effectiveness remain outside TASK-062 proof.
