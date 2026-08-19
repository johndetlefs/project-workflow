# TASK-064 Validation — 2026-08-19

## Outcome

TASK-064 found no source defect at the exact requested base `f864c0f7ab3fce89fe7817481ea020c422ec6b28`. The complete locked suite, focused compatibility gates, strict Doctor, exact-wheel package journeys, release contract, privacy scans, and retained live-receipt audit passed. The sanitized machine-readable result is `delegation-validation-receipt.json` with SHA-256 `d65c20d39d3be977f2306a54f6a17c42385b2edb41bdff3a120b0dc647d93814`.

The evidence preserves one material boundary: the retained Task and Epic native journeys ran on exact ancestor commits `9c3d9bd` and `62e56d6`, respectively. They did not run on final HEAD, and their historical wheel binaries are not retained for reinspection. Their committed source/helper hashes reproduce exactly, their recorded package identities are internally consistent, and final HEAD is separately covered by the newly built and installed wheel. No final-wheel native replay is claimed or authorised.

## Exact Source And Package Identity

- Checkout: detached HEAD at `f864c0f7ab3fce89fe7817481ea020c422ec6b28`, matching the requested committed base on `codex/EPIC-010-delegate-execution-orchestrator`.
- Source, generated helper, local helper, and installed final-wheel CLI SHA-256: `4ec02dd5feab8db158cc0946a2295a0b61729edb6b663dcd0fb6c508a8894414`.
- Wheel: `project_workflow-0.3.0-py3-none-any.whl`, SHA-256 `99c55448c0d795cffe588008b0bf35c830d1688f8c44c464c530cc1247971d57`, 39 entries.
- Source distribution: `project_workflow-0.3.0.tar.gz`, SHA-256 `7522d2110f8936a64c5a6fe488bafddf6173dc6beb20a9297a0fa312e1f9c298`, 80 entries.
- Common/GitHub Delegate prompt SHA-256: `6ba2b5188c07eff3de0f77926cb5df75f73c22eedf58dc705d9e1b7cd43dabf8`.
- Packaged Codex Delegate skill SHA-256: `9f4fa0621c4be835030585880adcaa9369cc26cdcd7421cbdc8fa28e7ea76d9c`; installed managed copy `aaff9fa1864fa055bd123369c56744eb1a54a121ae20bd2075efc7e1239f3352` differs only by the generated marker.
- Manifest: package `0.3.0`, manifest version 1, managed asset version 2, repository schema version 1.

## Validation Results

| Gate | Exact command or method | Result |
| --- | --- | --- |
| Declared environment | `uv sync --locked --extra dev --python 3.10` with repository-declared temporary UV cache | Pass on CPython 3.10.20 |
| Focused Delegate/lifecycle/workspace/upgrade/release | `.venv/bin/pytest -q tests/test_delegation.py tests/test_delegate_task_mode.py tests/test_delegate_epic_mode.py tests/test_delegate_host_assets.py tests/test_doctor.py tests/test_workspace_mode.py tests/test_release_contract.py` | Pass: 287/287 in 52.06s |
| Complete locked suite | `PATH=/opt/homebrew/bin:$PATH .venv/bin/pytest -q` | Pass: 377/377 in 55.45s; UVX path enabled |
| Negative lifecycle and legacy subset | Explicit Task Testing, installed console, Epic-child Testing, QA/Complete, parent closeout, six-column Task, and four-column Epic cases | Pass: 16/16 in 3.90s |
| Strict Doctor | `./.project-workflow/cli/workflow doctor --strict` | Pass: no visible issue; 69 accepted warnings hidden |
| Compilation | `.venv/bin/python -m compileall -q src tests` | Pass |
| Mirror identity | `cmp` across source/generated/local Python helpers and common/GitHub Delegate prompt | Pass |
| Release source contract | `scripts/release_contract.py check-source --version 0.3.0 --tag v0.3.0 --clean` | Pass |
| Build and immutable release receipt | `python -m build`, `build-receipt`, then `verify-receipt` | Pass; exact artifacts listed above |
| Exact-wheel install | Fresh Python 3.10 venv plus `uv pip install` from the built wheel | Pass; `project 0.3.0`; installed CLI hash equals source |
| Four-host package journey | `scripts/verify_package_journeys.py --from <exact wheel> --version 0.3.0` | Pass: Codex, GitHub Copilot, Claude Code, and Cursor fresh init, Doctor, and no-op upgrade |
| Legacy package journey | Same exact-wheel script against `tests/fixtures/legacy-unversioned` | Pass: owner bytes preserved, managed update retained as `.new`, expected two owner-owned findings |
| Privacy and inventories | Git ignore/tracked-file checks plus wheel/sdist name/content scans | Pass: no runtime payload, live receipt, current task/thread identity, or owner home path packaged |
| Read-only plan/status | Final-HEAD human and JSON `delegate plan` plus strict `status`, followed by Git inspection | Pass: schema version 1, matching graph/provenance/concurrency, no runtime state or Git mutation |
| Diff integrity | `git diff --check` | Pass |

One direct exact-wheel install first selected UV's sandbox-inaccessible home cache. Repeating the same install with the repository-declared temporary `UV_CACHE_DIR` passed; this was environment setup evidence and required no source change.

## Retained Native Receipt Audit

### Task Mode

- Receipt SHA-256: `cdfb979cfb3675afdfba1ca4ddc8348ca67e81263a934f672a2fc904fb65fee2`.
- Exact implementation commit: `9c3d9bd177fa9c5d881221010bc9a4b34217f79e`, a direct ancestor of final HEAD.
- Git-reproduced source and helper SHA-256: `48ff24a747ebeb5ccf9b70b5744b9959d41aff61df822e8262ae40b580866331`, matching the receipt.
- Recorded wheel SHA-256: `83ab8c6db140a47918840d0eebd3c6b991201ff44ed37dab1ab0e6829427bece`.
- Observed journey: overlap rejected before launch; two disjoint bounded subagents; requested three bounded to observed capacity two; dependent wait; coordinator rejection of a false worker validation; explicit corrected retry; coordinator-only shared mutation; Testing rejected until every row was Done; zero unjustified duplicate launches.
- Boundary: broader shared-premise/orphan/restart combinations are deterministic coverage. No persistent Codex task or final-HEAD native replay is claimed.

### Epic Mode

- Receipt SHA-256: `33042b3d2d64ba1104a89d5374864b6f8c2d78f868c5fe98963c891f927c30aa`.
- Exact implementation commit: `62e56d68732b354c269bec9be928a81c63379e69`, a direct ancestor of final HEAD.
- Git-reproduced source and helper SHA-256: `b468a24ec872c7b25e4c8af5d2a937d0582481b50fb9ed721cf3ec95ed91f945`, matching the receipt.
- Recorded wheel SHA-256: `fc33165f924983a219d5ed85a6b2fc55bc134e6a5736290087ad03ffe0436fe2`.
- Observed journey: authority/capability negative creation gates; two independent persistent tasks in distinct isolated worktrees; dependency delayed until coordinator verification; monitoring pause/resume with create count unchanged; exact base/scope/hash/validation inspection; dependent creation after verified predecessors; read-only blocked parent closeout; zero unjustified duplicate creations.
- Diagnostic disclosure: seven earlier diagnostic native tasks and three authoritative native tasks are retained in the receipt; only the final three support the passing journey.
- Capacity boundary: two concurrent persistent tasks prove a host lower bound of two. The host exposed no numeric maximum; the coordinator chose a cap of two.
- Resume boundary: the live observation proves monitor pause/resume without duplicate creation. Distinct coordinator-process restart, injected failure/orphan cases, and final-HEAD native replay are not claimed as live observations.

Both receipts assert that native task/agent/host IDs, handles, cursors, client setup IDs, transcripts, credentials, and native worktree names/paths were not retained. Structural checks confirmed every sanitization flag and found no tracked runtime file.

## Parent AC Crosswalk

| Parent AC | Result | Evidence boundary |
| --- | --- | --- |
| AC4 | Pass | Final-HEAD human/JSON plan and status agree and remain read-only. |
| AC10 | Pass | Final failure/state matrices plus Task live failure/retry evidence; unrelated/shared-premise variants are deterministic coverage. |
| AC11 | Pass | Coordinator verification gates dependencies in code, tests, and both native receipts. |
| AC12 | Pass | Persist/resume/orphan tests plus live no-duplicate monitoring resume; no live distinct coordinator-process restart claim. |
| AC14 | Pass | Sixteen targeted negative cases keep Testing, QA, Review, Complete, and parent closeout independent. |
| AC15 | Pass | Tri-state dated capability/fallback matrix passed; no untested host runtime support is inferred. |
| AC16 | Pass | Asset v2, exact mirrors, fingerprints, four-host installs, no-op upgrades, rollback coverage, and `.new` collision preservation passed. |
| AC17 | Pass | 377 locked tests plus Doctor, compilation, workspace, Smoke Bomb, build, release, install, package inventory, and legacy journeys passed at final HEAD. |
| AC18 | Pass | Exact-source sanitized Task live receipt covers every required event at `9c3d9bd`; final-wheel native replay is outside the claim. |
| AC19 | Pass | Exact-source authorized Epic live receipt covers every required event at `62e56d6`; final-wheel native replay is outside the claim. |
| AC20 | Pass | Source and exact-wheel installed guidance preserve the positive/negative invocation and lifecycle responsibility distinctions. |

All structured claims use empty `invalid_substitutes`. Tests, packaging, and prose are not substituted for the dated native observations; the native receipts are not substituted for final-HEAD package validation or independent parent closeout.

## Independent QA And Code Review

- Reviewed: exact diff scope, source/receipt/package identities, every Task AC and mapped parent AC, lifecycle bypass surfaces, plan/status mutation, capability provenance, privacy, legacy parsing, installed host assets, release semantics, and proof-language boundaries.
- Corrected during review: the machine-readable receipt initially pointed one directory too shallow to the TASK-061 and TASK-062 retained receipts. Both paths were corrected, existence-checked, and the receipt/EVIDENCE hashes were refreshed.
- Findings: no blocking correctness, scope, privacy, packaging, or lifecycle finding. No source defect was found, so no source or managed asset was changed.
- Proof limitation retained: historical wheel binaries are unavailable for fresh byte inspection and the native runs predate final HEAD. Git-reproduced source/helper identities, receipt consistency, and final-HEAD package validation pass, but a final-wheel native replay is not claimed.
- Verdict: **Pass** for TASK-064's approved evidence-consolidation scope. Parent acceptance audit, deferral decisions, parent retro, lifecycle completion, release, deployment, adoption, effectiveness, and owner acceptance remain coordinator/owner gates.

## Retro

- Reusable lesson: a retained native receipt and a final package validation are separate evidence layers. Record both exact identities and state explicitly when the final package was not replayed through the native host journey.
- Durable asset changes: none. Existing requirements, proof recipes, and Delegate guidance already require this distinction; a one-off task detail was not added to global guidance.
- Follow-up tasks: none created. The parent coordinator should preserve the final-HEAD native-replay boundary in the Epic acceptance audit and release decision.
- Missed in-scope work: none. Parent/global artifacts were intentionally left untouched under the delegation packet.

## Delivery Boundaries

This child changed only TASK-064 documentation and evidence. It did not change source, tests, managed assets, global/Epic trackers, the acceptance map, parent audit, deferrals, parent retro, parent runtime state, another repository, or any external system. It did not push, merge, release, deploy, or contact anyone.
