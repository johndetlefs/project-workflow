# Project Workflow CLI (local)

This folder contains a small helper CLI for the repo’s AI workflow.

Goals:

- Keep workflow scaffolding **out of** `package.json` scripts.
- Keep it **co-located** with the workflow artifacts (`.project-workflow/`), so it’s easy to use and later extract.

## Usage

From the repo root:

```bash
./.project-workflow/cli/workflow task init --title "Super Admin Access" --update-tracker
```

Create a git branch (requires a clean working tree):

```bash
./.project-workflow/cli/workflow task init --title "Super Admin Access" --update-tracker --create-branch --base-branch develop
```

Customize folder name suffix:

```bash
./.project-workflow/cli/workflow task init --title "Super Admin Access" --folder-suffix Superuser --update-tracker
```

Move a task through the lifecycle:

```bash
./.project-workflow/cli/workflow task approve-requirements --id TASK-001 --approved-by "Product Owner" --source "Owner approved requirements in planning thread"
./.project-workflow/cli/workflow task status --id TASK-001 --to "In Progress"
./.project-workflow/cli/workflow task status --id TASK-001 --to Testing
./.project-workflow/cli/workflow task status --id TASK-001 --to Review
./.project-workflow/cli/workflow task status --id TASK-001 --to Complete
```

Illegal non-complete transitions require an audit reason:

```bash
./.project-workflow/cli/workflow task status --id TASK-001 --to Testing --force --reason "Recovering imported tracker state"
```

`Complete` is only allowed from `Review` and requires non-placeholder `## QA & Code Review` evidence.

Create and manage proposal-first epics:

```bash
./.project-workflow/cli/workflow epic init --title "Checkout Reliability"
./.project-workflow/cli/workflow epic approve-requirements --epic-id EPIC-001 --approved-by "Product Owner" --source "Owner approved epic requirements and decomposition boundary"
./.project-workflow/cli/workflow epic decompose --epic-id EPIC-001 --limit 5 --type Task
./.project-workflow/cli/workflow epic approve --epic-id EPIC-001 --id TASK-014
./.project-workflow/cli/workflow epic scaffold-child --epic-id EPIC-001 --id TASK-014
```

Approval is an authority envelope, not a repeated prompt. Once requirements/ACs and the epic boundary are approved, unchanged work inside that envelope should proceed; stale requirements, out-of-envelope work, and evidence gaps should fail with concrete drift reasons.

New/adopted epics also require a non-placeholder `EPIC-CONTRACT.md` before decomposition, child approval/scaffolding, or movement into `Ready`/`In Progress`. The contract records sources of truth, invalid substitutes, invariants, artifact targets, and parent AC proof owners.

`epic decompose` also writes `DECOMPOSITION.md`, the approved child-row authority plan. `epic approve`, `epic scaffold-child`, `epic ready-child`, `epic status`, and `doctor` reject active child rows whose ID, title, or parent AC coverage does not match that plan. Matching rows inside the plan do not need separate per-row owner approval.

`epic amend` records an owner-approved row in `AMENDMENTS.md` and appends the matching Proposed child row. Use it for mid-epic reactive fixes or new child work that is outside the approved decomposition plan. Direct tracker edits outside decomposition/amendment authority remain blocked.

`task adopt` and `epic adopt` bring pre-existing work under the current approval gates. Adoption writes a `Legacy Adoption` block and treats pre-adoption inferred evidence as untrusted until refreshed; use `--evidence-refreshed` only after rerunning the relevant proof.

`epic scaffold-child` copies parent AC coverage plus a contract-derived `Child Charter` into child requirements and implementation docs, and creates child-local `EVIDENCE.json`.

When requirements or material claims trigger a proof recipe, QA prose is not enough. `epic status` blocks `Review`/`Complete`, `epic audit` refuses parent AC credit, and `doctor` fails invalid current states until `EVIDENCE.json` has passing structured claim records for the triggered recipe. Built-in recipes include `visual-reference-fidelity`, `external-contract-alignment`, `deployed-artifact-alignment`, `runtime-target-source`, and `responsive-visual-behavior`.

Invalid substitutes are rejected. Visual/reference fidelity needs evidence against the delivered user-facing artifact, not code review, tests, build output, or surrogate surfaces. Runtime target/source claims need the exact execution target, source/artifact under test, observation method, and positive proof that the target used that source.

Validate workflow state:

```bash
./.project-workflow/cli/workflow doctor
./.project-workflow/cli/workflow validate --strict
```

`doctor` and `validate` are equivalent. Use `--strict` when safety warnings should fail automation.

## Branch naming

Default branch format:

- `feature/<ID>-<kebab-case-title>`

Example:

- `feature/TASK-001-super-admin-access`

## Packaged CLI

This repo also exposes the packaged console script:

```bash
project task init --title "Super Admin Access" --update-tracker
project task status --id TASK-001 --to "In Progress"
project doctor
```

For refreshing an initialized repository, prefer the canonical UVX command from the target repository root:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init
```

Use bare `project init` only when the package is intentionally installed locally and known to be current. Re-running init from the latest package refreshes marked generated workflow assets and managed host-file blocks. Unmarked existing files are preserved; project-workflow writes the new generated content beside them as `*.new` for review.

The in-repo script is intentionally dependency-free (stdlib only) so initialized projects can keep using the local workflow helper without installing the package.
