# TASK-063 Validation — 2026-08-19

## Exact source and artifacts

- Authorized base: `ee02a83c95d90b265837d68d2871c40d2efc9915`.
- Frozen implementation commit: `16c158c0c0db4a990459e138f347a14ac7a9308d`.
- Delivery boundary: local detached commit only; no push, merge, release, deployment, external contact, or cross-repository mutation was authorized or performed.
- Wheel: `project_workflow-0.3.0-py3-none-any.whl`, SHA-256 `c6b9288e7ec18ffa4149651a285fb605f998c5e3d7853fb54c5ec10746cc48e8`.
- Source distribution: `project_workflow-0.3.0.tar.gz`, SHA-256 `3c829eaf8bf4c5ecdb6a1dc94c787157a94be8e94f7955dc21f366e002aed0dc`.
- Shared CLI source, packaged template, local helper, and wheel `project_workflow/cli.py`: byte-identical SHA-256 `4ec02dd5feab8db158cc0946a2295a0b61729edb6b663dcd0fb6c508a8894414`.
- Packaged Codex Delegate skill and wheel copy: SHA-256 `9f4fa0621c4be835030585880adcaa9369cc26cdcd7421cbdc8fa28e7ea76d9c`; installed managed copy differs only by the generated marker and has SHA-256 `aaff9fa1864fa055bd123369c56744eb1a54a121ae20bd2075efc7e1239f3352`.
- Common/GitHub Delegate prompt mirror: byte-identical SHA-256 `6ba2b5188c07eff3de0f77926cb5df75f73c22eedf58dc705d9e1b7cd43dabf8`.

## Acceptance crosswalk

| Child AC | Implemented contract | Exact proof |
| --- | --- | --- |
| AC1 | Tri-state `verified` / `unsupported` / `unknown` capability matrix, dated provenance, observed child capacity, Task-only subagent path, stronger Epic persistent/reconciliation gate, and explicit coordinator fallback. | `tests/test_delegation.py`, `tests/test_delegate_epic_mode.py`, and `tests/test_delegate_host_assets.py`; focused 273/273 and full 377/377 pass. |
| AC2 | Common/GitHub prompt, Codex skill, Claude/Cursor native transforms, Planner, Epic, Implement, QA, Cursor rule, and AGENTS guidance carry one bounded authority/packet/verification contract without cross-host placeholders. | Four-host fresh package journey and deterministic native-asset/placeholder tests. |
| AC3 | Delegation handles stay under ignored runtime state; package inventories omit runtime/task evidence/secrets; Smoke Bomb redacts and blocks hostile ignored runtime without leaking names/content. | `git check-ignore`, 39-entry wheel and 80-entry sdist scans, and hostile Smoke Bomb privacy regression. |
| AC4 | Asset version 2 aligns init, plan/apply fingerprinting, rollback, no-op, exact source/generated mirrors, Doctor/release validation, and owner-owned `.new` collision preservation. | Four-host exact-wheel journey; legacy fixture preserves owner SHA and creates pending managed SHA in `evidence/package-journey.json`. |
| AC5 | README and installed guidance distinguish one Task or Epic, implementation rows, Epic child Tasks, host executors, Implement, independent QA, lifecycle, and delivery boundaries with positive/negative examples. | Semantic asset tests, Doctor, release contract, fresh installs, and direct source/install inspection. |

## Validation results

| Gate | Result |
| --- | --- |
| Focused locked suite | Pass: 273/273 in 40.98s |
| Full locked suite | Pass: 377/377 in 53.12s |
| Independent cache-free focused review | Pass: 122/122 before final evidence review; code/asset findings fixed |
| Strict Doctor | Pass: no issues; 69 accepted warnings hidden |
| Compile | Pass: `python -m compileall -q src tests` |
| Source release contract | Pass: version/tag `0.3.0` / `v0.3.0` |
| Build | Pass: exact-commit wheel and sdist built from the locked source |
| Mirrors and diff | Pass: three CLI copies byte-identical; common/GitHub Delegate prompt identical; installed Codex skill exact after managed-marker normalization; `git diff --check` clean |
| Four-host package journey | Pass: fresh init, Doctor, and no-op upgrade for Codex, GitHub Copilot, Claude Code, and Cursor |
| Legacy upgrade | Pass: asset-v1/unversioned upgrade, fingerprint/apply/rollback coverage, owner collision preserved, managed update retained as `.new` |
| Privacy | Pass: ignored runtime path verified; wheel/sdist inventories exclude runtime delegation state, TASK-063 evidence, `.env`, credentials, and private transcript names; hostile Smoke Bomb test passed |

## Parent AC evidence

- AC6: Epic persistent execution requires explicit authority and dated verified persistent-task, isolated-worktree, monitoring, reconciliation, and available-capacity observations; incomplete gates create no persistent executor. Current-session subagent support is confined to Task rows and is not generalized to other hosts or sessions.
- AC7: All host guidance preserves exact unit/target identity, ACs, dependencies, repository/write scope, validation/evidence, forbidden shared-state/delivery actions, stop conditions, base, and return format; coordinator verification—not a worker assertion—releases dependencies.
- AC9: Effective child concurrency is computed from requested concurrency, observed available capacity excluding the coordinator, eligibility, dependencies, and collision-free parallel scope; no fixed worker count remains.
- AC13: Runtime handles and private content remain ignored and excluded from packages/Smoke Bomb output while this canonical, sanitized validation record remains reviewable.
- AC15: Unsupported and unknown capabilities fail closed for native paths. Task rows may use an explicitly reported coordinator/sequential fallback; Epic children never fall through to current-session subagents.
- AC16: Managed asset version 2, exact mirrors, fresh init, Doctor, and no-op upgrade pass for all four hosts. The shared upgrade mechanism's fingerprint/rollback behavior passes deterministic coverage, and the retained Codex legacy fixture separately proves owner-owned collision preservation through `.new`.
- AC20: README, AGENTS, prompts, skills, Cursor rules, and generated assets now use one semantic contract in host-native syntax and preserve Implement, Delegate, independent QA, lifecycle, and closeout boundaries.

## Proof boundaries

- The current session observed bounded subagent tooling for its own review only. This does not claim general Codex capacity or persistent-task support, and it proves no Claude, Cursor, or GitHub Copilot runtime capability.
- Four-host initialization, generated syntax, semantic tests, and package journeys prove managed-asset delivery and fail-closed contracts, not native orchestration support on those hosts.
- The legacy journey's two owner-owned Doctor findings are the required preserved collision and pending `.new` update, not upgrade failure.
- Parent/global trackers, Epic acceptance map, Epic lifecycle, parent delegation runtime state, release, deployment, adoption, effectiveness, and owner acceptance remain with the parent coordinator or later authorized gates.
