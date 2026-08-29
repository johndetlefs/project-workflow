# Requirements

## Summary

- Task: EPIC-020
- Title: Release Structural Cleanup And Upgrade All Projects
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Publish the completed structural-coherence work as Project Workflow 0.9.1 from reviewed `main`,
prove the exact public package, and update every existing canonical Project Workflow installation
that can be changed safely. Inventory every current project and leave dirty, active, detached,
ambiguous, or non-installed roots unchanged with an exact disposition rather than forcing them.

## Intent Spine

- OC1 — Completion capability: Maintainers can install one publicly verified 0.9.1 package, and
  every current canonical consumer either reports that exact version with a no-op re-plan and
  Doctor evidence or has a concrete retained safety blocker.
- OC2 — Material capabilities: Align one 0.9.1 identity; prove the exact candidate; integrate it
  through reviewed GitHub checks; tag, publish, and independently verify the public artifacts;
  inventory the current project estate; apply fingerprint-bound upgrades only to eligible roots;
  retain one release-and-rollout receipt.
- OC3 — Success journey: Validate and merge the structural candidate, tag the exact `main` commit,
  observe trusted publication, retrieve and exercise the public package, then plan/apply/no-op
  each safe canonical consumer while preserving user-owned content.
- OC4 — Successful-but-wrong result: Tests pass but a different commit or artifact is published;
  release is claimed before public retrieval; a dirty or ambiguous consumer is modified; or an
  upgrade is called complete without exact-version, diff, no-op-plan, and Doctor proof.
- OC5 — Exclusions: No lifecycle redesign, forced dirty-root upgrade, installation into a
  non-consumer, consumer commit/push/deployment, historical evidence rewrite, owner-acceptance
  claim, or authenticated Claude runtime certification.
- OC6 — Assumptions: 0.9.1 is a backward-compatible maintenance release because public commands
  and schemas remain unchanged; trusted publishing and repository access remain available; the
  public exact-version package is the only rollout authority.
- OC7 — Authority source: John Detlefs's current Codex instruction on 2026-08-29: "Push the release
  please, and update all projects to the latest version."

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-29
- Approval note / source: Current Codex task 2026-08-29: Push the release please, and update all projects to the latest version.
- Approved artifact identity: sha256:4dfaab081e570fa32d700d9db1a92c7b6686239f08c026af8f61591922a1b608

## Goal

Convert EPIC-019's locally validated structural candidate into one immutable public 0.9.1 release
and safely adopt that exact package across the complete current Project Workflow consumer estate.

## Non-Goals

- Changing v0.9 command, schema, lifecycle, or proof semantics beyond the already reviewed terminal
  verification inspection fix.
- Closing or weakening EPIC-018/TASK-102's authenticated Claude Code canary obligation.
- Installing Project Workflow into projects without a canonical root manifest.
- Overwriting dirty, active, detached, ambiguous, nested, or unreconciled consumer state.
- Committing, pushing, merging, releasing, or deploying consumer-project upgrade diffs.
- Treating availability, installation, or owner instruction as owner acceptance or commercial
  adoption evidence.

## Users & Context

The owner uses Project Workflow across multiple local Codex projects. EPIC-019 has completed its
structural and functional QA against released 0.9.0, but its delivery boundary stopped at local
validated source. This Epic owns the new public release and complete current-estate rollout; every
entry must receive a disposition even when safety prevents mutation.

## Repository Scope

- Primary repository: .
- Repositories touched: the Project Workflow source repository plus every current local project
  whose canonical authority root contains `.project-workflow/manifest.json` and passes immediate
  per-root mutation eligibility checks.

## Requirements (Outcome-Focused)

- Prepare one coherent 0.9.1 identity across version source, contracts, manifest, changelog,
  current installation guidance, CI/release workflows, generated runtime, and release tests.
- Prove the exact clean candidate with locked static/documentation/runtime gates, the complete
  suite, strict Doctor, clean release contract, one wheel/sdist build, inventory inspection, and
  exact-package journeys without reopening EPIC-019's completed independent QA.
- Commit and push the reviewed candidate, create and merge a passing PR, tag the exact resulting
  `main` commit, and publish through the protected trusted-release workflow.
- Independently verify PyPI and GitHub Release filenames, hashes, provenance, version output,
  installed assets, fresh init, legacy/current/no-op upgrade, Doctor, and representative lifecycle
  behaviour before consumer mutation.
- Discover the complete current project inventory and resolve one canonical authority root for
  every installed Project Workflow consumer. Recheck Git/worktree/activity state immediately
  before each upgrade.
- Use `project-workflow==0.9.1` to generate a deterministic plan and apply only the reviewed
  fingerprint at eligible clean roots. Re-plan to prove no-op, inspect the scoped diff, verify the
  manifest/helper version, and run applicable Doctor validation.
- Preserve user-owned files and unrelated state. Retain exact blockers for unchanged projects and
  a machine-readable receipt mapping every project and release claim.

## Acceptance Criteria (Verifiable)

- AC1: Every current release identity surface consistently names 0.9.1, generated mirrors are
  current and byte-identical, historical evidence remains unchanged, and source diff hygiene
  passes.
- AC2: One exact candidate commit, wheel, and sdist pass locked Ruff/format/mypy, documentation and
  architecture contracts, deterministic regeneration, the complete suite, strict Doctor, clean
  release-source checks, build inspection, exact-package journeys, and the retained EPIC-019 QA.
- AC3: A reviewed PR with required checks merges the candidate into current `main`; annotated tag
  `v0.9.1` peels to that lineage; the trusted release workflow publishes one coherent bundle and
  GitHub Release without moving or rebuilding the public identity.
- AC4: Independent public retrieval proves PyPI and GitHub artifacts, hashes, attestations, version
  output, managed assets, fresh installation, upgrade journeys, Doctor, and representative
  lifecycle behaviour for `project-workflow==0.9.1`.
- AC5: Every current project inventory entry has a disposition, and every canonical Project
  Workflow installation is either upgraded from the public 0.9.1 package or retained unchanged
  with a concrete current safety blocker.
- AC6: Every successful consumer upgrade used a reviewed fingerprint, preserved owner content,
  contains only expected managed/schema changes, reports 0.9.1, passes a no-op re-plan and
  applicable Doctor validation, and remains uncommitted/unpushed by this Epic.
- AC7: One retained release/rollout receipt maps AC1-AC6 to exact source, PR/checks, tag, workflow,
  public artifact identities, inventory evidence, per-project results, and remaining boundaries.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose | Dependencies |
| --- | --- | --- | --- |
| Prepare and prove the exact Project Workflow 0.9.1 candidate | AC1, AC2 | Align version authority and certify one clean retained candidate without reopening completed structural QA. |  |
| Integrate, tag, and publish Project Workflow 0.9.1 | AC3 | Commit, review, merge, tag, and publish the exact certified source lineage. | TASK-109 |
| Verify the public Project Workflow 0.9.1 release | AC4 | Independently retrieve and exercise the publicly obtainable package and attestations. | TASK-110 |
| Inventory and safely upgrade every Project Workflow installation | AC5, AC6, AC7 | Disposition the complete project estate, apply public fingerprinted upgrades where safe, and consolidate proof. | TASK-111 |

## Open Questions (Answer Needed)

- None. Safety eligibility is an evidence classification, not permission to overwrite a dirty or
  ambiguous project in order to satisfy the word "all."

## Decisions (Resolved)

- 0.9.1 is the semantic version because the release preserves public commands and schemas while
  delivering internal maintainability and one backward-compatible terminal-state bug fix.
- EPIC-019 remains the structural implementation and independent-QA authority; EPIC-020 owns only
  versioning, final exact-candidate proof, integration, publication, verification, and adoption.
- The public exact-version package is the only consumer rollout authority.
- Complete inventory coverage is mandatory; mutation is limited to clean, unambiguous canonical
  roots and blocked entries remain truthful rather than being forced.
- Publication and consumer adoption are separate proof gates coordinated sequentially.

## Validation Plan

- AC1: Version scan, changelog/current-doc inspection, source contract, deterministic generation,
  manifest/package inventory, and diff check.
- AC2: Locked static/doc/architecture/runtime gates, complete suite, strict Doctor, clean release
  contract, one build, artifact receipt, exact-package journeys, and retained QA identity.
- AC3: PR review/checks, merge ancestry, annotated tag identity, trusted workflow, and release
  bundle evidence.
- AC4: Independent PyPI/GitHub download hashes, attestation verification, exact public `uvx`
  version and disposable fresh/current/legacy/no-op/Doctor/lifecycle journeys.
- AC5-AC6: Complete inventory, canonical-root/Git/activity preflight, public-package plan,
  fingerprint apply, no-op plan, scoped diff, manifest/helper and Doctor evidence per eligible root.
- AC7: Machine-readable consolidated release/rollout receipt and parent acceptance audit.
