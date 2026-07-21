# Requirements

## Summary

- Task: TASK-041
- Title: Add Structured Doctor Findings
- Parent AC Coverage: AC2, AC5, AC8
- Last updated: 2026-07-21

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Child Charter

### Inherited Invariants

- `project init` creates new installations; `project doctor` owns diagnosis; canonical UVX `project upgrade` refreshes managed assets and transforms existing repository state in one transaction.
- Explicit `--plan` mode is non-mutating; normal human upgrade confirms before apply and authorized agents use `--yes`.
- Apply requires confirmation or an explicit automation flag, a clean worktree, a supported source version, and fresh version/hash preconditions.
- The first release applies the complete validated mechanical plan or no changes.
- Migration IDs are immutable and ordered.
- Successful migrations are idempotent; reapplying at the target schema is a no-op.
- Atomic failure cannot leave partial file changes.
- User-owned and unmarked content is preserved.
- Existing project history, approvals, deferrals, evidence, accepted warnings, and unresolved decisions are never silently rewritten into current passing state.
- Unsupported or unrecognized state blocks with a stable finding and concrete next action.
- Human output and machine-readable output describe the same findings and plan.
- Packaged and generated command behavior must remain aligned.

### Invalid Substitutes

- A successful `project init` run is not proof that durable repository state was upgraded.
- A clean old helper or old doctor result is not proof that the repository uses the current schema.
- Package version alone is not a substitute for separate asset and repository-schema versions.
- An agent-authored prose summary is not a substitute for a deterministic machine-readable upgrade plan.
- A passing plan is not proof that apply produced the predicted diff.
- Tests against only freshly initialized repositories are not historical upgrade evidence.
- Backups or Git availability do not permit overwriting user-owned content.
- Accepted warnings, inferred approvals, or stale evidence are not upgraded authority or proof.
- Best-effort partial changes are not an acceptable substitute for atomic application.

### Artifact Targets

- Managed repository metadata at `.project-workflow/manifest.json`
- Upgrade command, plan model, migration registry, and apply engine in `src/project_workflow/cli.py` with behavioral parity in `src/project_workflow/templates/workflow.py`
- Stable structured doctor and upgrade-plan output schemas
- Historical repository fixtures and focused regression coverage under `tests/`
- Generated agent guidance under `src/project_workflow/prompts/`, `src/project_workflow/codex/`, and `src/project_workflow/cursor/`
- README and changelog documentation for init, doctor, and upgrade responsibilities
- EPIC-007 child requirements, implementation plans, evidence, QA, acceptance map/audit, and closeout artifacts

### Parent AC Proof Ownership

- AC2: owner `Add Structured Doctor Findings, Align Documentation And Generated Agent Assets`; required evidence: Tests and captured output proving stable finding codes and equivalent human/machine-readable fields.
- AC5: owner `Define Repository Version Manifest And Compatibility Policy, Integrate Init Version Detection And Upgrade Direction`; required evidence: New/existing init fixtures proving init-only creation and no-mutation upgrade direction, plus canonical upgrade asset refresh.
- AC8: owner `Add Structured Doctor Findings, Build Deterministic Upgrade Planner, Build Safe Transactional Upgrade Apply`; required evidence: Fixtures proving owner-owned approval/evidence/decision gaps remain visible and unchanged after plan/apply.

## Goal

Make Doctor findings deterministic and consumable by humans, agents, and CI without changing what Doctor validates or allowing machine-readable output to drift from human output.

## Non-Goals

- Adding repository-version findings before command integration; TASK-044 owns init state handling and upgrade direction.
- Implementing upgrade plans, migrations, or repair behavior.
- Changing current validation rules, accepted-warning identities, strict-mode semantics, or exit codes.
- Automatically resolving missing approvals, stale evidence, deferrals, or owner decisions.
- Redesigning every existing validation message or assigning one unique code per message instance.

## Users & Context

- Humans need concise Doctor output that explains what failed, who owns remediation, and whether project-workflow can address it mechanically.
- Agents and CI need deterministic JSON rather than parsing prose or fingerprints.
- Existing accepted-warning fingerprints are repository history and must remain valid.
- Owner-owned approval, evidence, deferral, and decision gaps must remain visible and must never be labeled mechanically upgradeable.

## Requirements (Outcome-Focused)

- Extend every `DoctorIssue` with a stable finding code, remediation owner, and mechanical-upgrade eligibility while retaining severity, affected path, and message.
- Use a documented, finite finding-code catalog. Dynamic task IDs, paths, and message details must not alter the finding code.
- Support `project doctor --format json` and the `validate` alias with a versioned deterministic JSON envelope containing root, strict mode, status, summary counts, and all findings.
- Include original and effective severity, affected artifact, message, remediation owner, mechanical eligibility, accepted state, accepted reason, legacy state, and fingerprint for each JSON finding.
- Render human and JSON output from the same `DoctorIssue` objects and acceptance/blocking calculations.
- Preserve default human output, warning acceptance, `--show-accepted`, strict-mode promotion, and process exit behavior.
- Classify approval, evidence, deferral, and unresolved-decision findings as owner-owned and not mechanically upgradeable.
- Classify managed generated-asset drift as project-workflow-owned and mechanically addressable; do not imply that user-owned repository state can be repaired.
- Keep packaged CLI, generated template, and checked-in local helper behavior aligned.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC AC2: every Doctor finding exposes a stable code, severity, affected artifact, remediation owner, mechanical-upgrade eligibility, message, and fingerprint.
- AC2: Covers parent AC AC2: `doctor --format json` emits a versioned deterministic envelope whose status, counts, accepted state, and blocking findings match human output and exit behavior for clean, warning, strict, error, legacy, and accepted-warning fixtures.
- AC3: Covers parent AC AC8: missing approvals, stale or missing evidence, incomplete deferrals, and unresolved owner decisions are labeled `owner`, remain visible unless explicitly accepted under existing rules, and are never mechanically upgradeable.
- AC4: Covers parent AC AC5: managed generated-asset drift is distinguishable from owner-owned repository state and can be labeled project-workflow-owned without claiming that Doctor mutates repository state.
- AC5: Covers parent ACs AC2, AC5, AC8: existing human-output assertions, accepted-warning fingerprints, strict behavior, and exit codes remain backward-compatible.
- AC6: Covers parent AC AC2: source, packaged template, and local generated helper remain behaviorally aligned, and targeted tests plus the full suite and strict Doctor pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Add `--format human|json`, defaulting to `human`; do not add a separate diagnostic command.
- Keep fingerprints as finding-instance suppression identities and add codes as stable finding categories; neither substitutes for the other.
- Use remediation owners `project-workflow`, `agent`, and `owner`.
- Include accepted findings in JSON with `accepted: true` even when human output hides them, so machine output is complete and auditable.
- Derive both renderers from one evaluation result containing visible, accepted, blocking, current, and legacy finding partitions.
- Keep repository compatibility classification available but defer Doctor integration until TASK-044 establishes init state behavior and upgrade direction.

## Validation Plan

- Add exact JSON-schema assertions for clean and mixed finding sets.
- Compare human and JSON finding codes, fingerprints, counts, effective severities, accepted state, and exit codes across representative fixtures.
- Assert owner-owned approval/evidence gaps are non-mechanical and generated drift is project-workflow-owned.
- Re-run existing Doctor tests unchanged to prove backward-compatible human behavior and accepted-warning fingerprints.
- Run generated local-helper JSON output, full pytest, source/template parity, Python compilation, and strict Doctor.
