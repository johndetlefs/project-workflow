# Epic Retro

- Epic: EPIC-018
- Title: Cross-Host Bounded Execution And Release Control
- Last updated: 2026-08-29

## Lessons

- A delivery-sequence exception can authorize merge, publication, and adoption without changing
  the Epic's proof contract. The exception must name the exact proof that remains open and keep the
  parent non-terminal.
- Universal upgrade across dirty worktrees needs a stable baseline that preserves the real index,
  skip-worktree metadata, branches, and owner edits. Exact plan fingerprints plus before/after
  non-target fingerprints allowed the public upgrader to remain authoritative without stashing or
  discarding work.
- A generated `.new` file is a preservation result, not adoption. Historical managed files were
  replaced only after exact public-package or Project Workflow Git-blob provenance was proved, then
  the affected integration was required to return a no-op plan.

## Follow-up Tasks

- TASK-102 remains Blocked until a current authenticated Claude Code executable can run the real
  hook-active canary.
- TASK-103 remains Approved and owns real cross-host conformance plus the remaining delivery-boundary
  proof; v0.9.0 publication and installation do not satisfy those claims.

## Deferrals

- Real Claude runtime proof is deferred by delivery sequence only. AC10 and Claude-dependent AC11,
  AC13, and AC15 remain open; they were not waived.

## Missed In-Scope Work

- None discovered in the v0.9.0 release or adoption envelope. The outstanding real Claude journey
  remains declared in-scope work, not missed work.

## v0.9.0 Release And Adoption

- PR `#25` merged to `main` at `0f02f42b5e5da61e5bef79f8b2cac74203f39182`; annotated tag
  `v0.9.0` points to that merge commit.
- Release workflow `33225374671` passed. PyPI and GitHub publish the same wheel
  `sha256:9e30c52fb70c8d5e86e173a2e5da6566a7f68f2a450718d6c28f25996bb0d82b` and
  sdist `sha256:e426baf1e90c7d8b46158a4492e86663d40fa9a2f21f815527dc07eaa3200829`.
- All 30 persistent physical installations found under the project repositories and Codex
  worktrees report package `0.9.0`, asset `8`, schema `1`. The 29 consumer roots cover 42 installed
  agent integrations and each returns an exact-plan no-op after apply; the Project Workflow source
  root carries the two current authoring integrations, for 44 total.
- Ten roots were dirty before rollout. No real Git index, branch, commit, stash, or unrelated owner
  content was changed or discarded. Five dirty collision sets were proven as earlier public managed
  assets before replacement. Six historical Copilot prompt sets and three legacy CLI pairs were
  likewise proven from canonical Project Workflow Git blobs, replaced with public v0.9.0 assets,
  and re-verified as no-op. The final inventory contains no managed `.new` files.
- Durable evidence: `evidence/v0.9.0-adoption.json`.
- The canonical `project release` preflight was exercised first and correctly failed closed with
  `execution-control-not-configured` and zero model invocations because the Epic is not delivery-ready
  while the Claude proof remains open. Delivery then proceeded only under the owner's explicit
  amendment; no second broad QA campaign was commissioned.
