# Requirements

## Summary

- Task: EPIC-019
- Title: Structural Coherence And Maintainability
- Last updated: 2026-08-29
- Intent contract: full

## Intent

Make Project Workflow straightforward for people and coding agents to understand, change, test,
and release by replacing the monolithic authored implementation and ambiguous documentation
ownership with a small set of explicit canonical modules and documents. Preserve the single public
CLI, dependency-free repository-local workflow, current contracts, and truthful proof boundaries.

## Intent Spine

- OC1 — Completion capability: A maintainer or coding agent can find one canonical source for each
  behaviour or instruction, change one cohesive domain without editing copied runtime files, and
  prove that the packaged and repository-local experiences still match.
- OC2 — Material capabilities: Cohesive production modules, deterministic standalone-runtime
  generation, shared test infrastructure, enforced quality gates, clear documentation authority,
  and evidence-led removal or disposition of obsolete repository debris.
- OC3 — Success journey: A contributor changes one domain module, runs focused tests, static
  checks and bundle generation, then passes the full suite, strict Doctor, source-parity checks,
  build inspection, and disposable exact-package/local-helper journeys without manual mirror edits.
- OC4 — Successful-but-wrong result: The suite is green but the change merely distributes coupling
  across arbitrary micro-modules, leaves generated copies as competing sources, changes public CLI
  or durable schemas, requires an installed package for the local helper, deletes audit evidence,
  preserves stale instructions, or broadens an unproved runtime-support claim.
- OC5 — Exclusions: No workflow lifecycle redesign, new product capability, public release,
  consumer rollout, Claude Code certification, historical-evidence fabrication, or architecture
  split into multiple packages or services.
- OC6 — Assumptions: Python 3.10 remains the minimum runtime; one repository-local dependency-free
  executable remains required; the released v0.9.0 command, schema, package, and proof contracts are
  the behavioural baseline; historical workflow records remain auditable rather than rewritten.
- OC7 — Authority source: Owner instruction in the current Codex task after completion of the
  Project Workflow v0.9.0 release and adoption rollout; released source commit
  `86ca8859eb5e331db2505c2ae7230e2bc0030242` is the implementation baseline.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-29
- Approval note / source: Codex task owner confirmation: Yeah. Let's go. Let's do it.
- Approved artifact identity: sha256:97ffea76213bad7453a037960183d9e4992a801026c7801ad6748e0178c1f0e8

## Goal

Leave Project Workflow with one obvious architecture and one obvious documentation hierarchy that
can grow safely: authored code is modular by responsibility, generated installations are derived
and verifiably identical, tests and quality checks expose regressions at the correct boundary, and
only proven-obsolete material is removed.

## Non-Goals

- Changing the intended Task, Fix, Epic, Coordinator, Delegate, verification, execution-control,
  upgrade, smoke-bomb, status, or Doctor product behaviour.
- Breaking or renaming current public commands, JSON schemas, manifest/schema/asset versions,
  generated paths, supported agent surfaces, or Python 3.10 compatibility.
- Replacing the Python package, standalone local helper, repository-native Markdown records, or
  existing public distribution model.
- Splitting Project Workflow into multiple packages, services, plugins, or an extension framework.
- Setting arbitrary code-coverage targets, introducing a framework, or creating one file per class
  or function merely to reduce line counts.
- Reconstructing approval or evidence for historical work, deleting evidence required by existing
  claims, completing EPIC-018, or claiming an authenticated Claude Code canary.
- Publishing, merging, releasing, or rolling out the cleanup without separate delivery authority.

## Users & Context

- Primary users are maintainers and coding agents changing Project Workflow itself. Today they
  must navigate a 25,583-line authored CLI containing 555 top-level functions and many unrelated
  domains, plus two exact 25,583-line runtime mirrors.
- Contributors depend on the public `project` entry point and repository-local
  `.project-workflow/cli/workflow`; cleanup must reduce source coupling without making adoption
  dependent on a pre-installed package.
- Documentation readers currently encounter strong product guidance but unclear authored/generated
  ownership and at least one materially stale authority: `RELEASING.md` still names 0.6.0 while
  v0.9.0 is public and current.
- Current functional evidence is strong: the release ran 548 tests, package journeys, strict
  Doctor, CI, and a 30-root/44-integration adoption audit. That evidence proves the v0.9.0 baseline,
  not the maintainability of the source layout.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Establish and document a bounded architecture with cohesive domains and explicit dependency
  direction. Prefer roughly six to ten substantial modules over both the current monolith and a
  proliferation of tiny files; any exception must be justified by cohesion or compatibility.
- Keep `project_workflow.cli` as the stable entry point and compatibility facade, with parser and
  dispatch assembly rather than cross-domain business logic. Public names used by tests or known
  integrations must remain available or receive an explicit compatibility re-export.
- Make modular Python sources the only authored implementation. Build
  `src/project_workflow/templates/workflow.py` deterministically as a clearly marked standalone
  artifact and install that same artifact at `.project-workflow/cli/workflow.py`; neither mirror is
  edited by hand.
- Preserve dependency-free operation of the installed repository-local helper and the current
  copied host adapters. Factor genuinely shared adapter behaviour into one canonical source without
  hiding host-specific capability differences or the uncertified Claude runtime boundary.
- Split catch-all tests by product boundary, centralize repeated CLI/project fixtures, and retain
  behavioural coverage and historical compatibility fixtures. Test organization must follow the
  production architecture without coupling every test to private implementation details.
- Lock and run the quality tools the repository claims to use. CI must enforce a clean Ruff check
  and format check plus a clean mypy pass over canonical authored production modules; generated
  duplicate artifacts are verified by parity rather than re-analysed as separate source.
- Define one documentation authority map. Keep the README as a concise product and quick-start
  entry, move contributor architecture and maintenance detail into a small `docs/` set, make the
  release runbook version-derived or version-neutral, and identify generated host assets as derived
  surfaces rather than competing guidance.
- Preserve the Constitution's stable product outcomes unless the cleanup discovers a genuine
  product-level conflict. Do not rewrite it merely to describe implementation architecture.
- Inventory empty folders, ignored build/cache output, stale worktrees/branches, superseded
  prototypes, duplicate binaries, generated copies, and historical workflow artifacts. Remove only
  items proven unnecessary; record why retained historical evidence and active blocked work remain.
- Prevent recurrence with automated architecture, generated-parity, documentation-version, and
  source-of-truth checks that fail when a future change reintroduces manual mirrors, stale release
  identity, forbidden cross-domain imports, or oversized mixed-responsibility entry points.
- Preserve all v0.9.0 public behaviour and truth boundaries, including the distinction between
  implemented, tested, packaged, released, adopted, and runtime-certified states.

## Acceptance Criteria (Verifiable)

- AC1: A checked-in architecture document names each canonical production module, its
  responsibility, allowed dependency direction, public compatibility surface, authored/generated
  status, and the objective rule for adding or splitting a module.
- AC2: `src/project_workflow/cli.py` is a thin entry/compatibility layer below 2,000 lines, no
  canonical authored production module exceeds 5,000 lines without a documented exception, and an
  automated architecture test prevents circular internal imports and domain logic returning to the
  entry module.
- AC3: The standalone `templates/workflow.py` is deterministically generated from canonical
  modules, carries an unambiguous generated marker and provenance, is byte-identical to the
  installed source-repository helper, and a clean regeneration produces no diff.
- AC4: The installed repository-local helper works from a disposable initialized repository with
  no installed `project_workflow` package and preserves the v0.9.0 command tree, JSON schema
  versions, init/upgrade/status/Doctor behaviour, and exit semantics.
- AC5: Shared Codex/Claude adapter mechanisms have one canonical implementation where semantics are
  genuinely identical; host-specific launch, hook, capability, limit, and receipt behaviour stays
  explicit; no test or document claims an authenticated Claude runtime canary.
- AC6: The 6,085-line catch-all Doctor test is split into product-boundary suites, repeated
  subprocess/repository builders are centralized, no replacement catch-all file exceeds 2,000
  lines, and all baseline behavioural and legacy fixtures remain exercised.
- AC7: Ruff check, Ruff format check, and mypy pass from the locked development environment and are
  required by CI alongside the full locked pytest and build/package journey gates. Unused Black or
  mypy configuration is either made real or removed; no aspirational quality configuration remains.
- AC8: README, contributor architecture/maintenance documentation, `RELEASING.md`, compatibility
  policy, AGENTS guidance, packaged prompts/skills, and installed generated surfaces have a tested
  authority hierarchy with no contradictory current version, lifecycle, role, proof, or release
  instruction.
- AC9: Every repository cleanup candidate has a recorded remove/retain/disposition decision.
  Empty local debris and fully superseded worktrees/branches are removed only after uniqueness
  checks; audit records and binary evidence are retained or replaced by equally durable verified
  evidence before deletion.
- AC10: The complete locked test suite passes with no reduction from the 548-test released baseline,
  strict Doctor passes, canonical source/bundle parity passes, source and wheel distributions pass
  inspection, and disposable fresh-init, current-upgrade, legacy-upgrade, and no-op journeys pass.
- AC11: A command-surface snapshot and representative exact-candidate journey compare v0.9.0 with
  the cleanup candidate and find no unapproved command, output-schema, manifest, asset, repository
  schema, generated-path, or lifecycle behaviour change.
- AC12: The final independent QA review explicitly evaluates whether boundaries are cohesive rather
  than merely smaller, whether documentation points in one direction, whether retained material is
  justified, and whether the resulting candidate is structurally and functionally fit for purpose.
- AC13: Completion records local validated source only. Merge, release, publication, consumer
  rollout, owner acceptance, and Claude runtime certification remain separate and unclaimed.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose | Dependencies |
| --- | --- | --- | --- |
| Establish Canonical Architecture And Bundle Contract | AC1, AC2, AC3, AC4, AC11 | Define module boundaries and dependency rules, add the deterministic standalone bundle path, and freeze v0.9.0 public command/schema compatibility before extraction. |  |
| Extract Repository And Delivery Domains | AC2, AC3, AC4, AC10, AC11 | Move configuration, assets, compatibility, status, upgrades, smoke bomb, work-item lifecycle, evidence, and Doctor behaviour behind cohesive modules while keeping the CLI facade stable. | Establish Canonical Architecture And Bundle Contract |
| Extract Coordination Execution And Adapter Foundations | AC2, AC3, AC4, AC5, AC10, AC11 | Separate orchestration, delegation, coordination, verification, and execution control; deduplicate only truly common adapter mechanisms and preserve host truth. | Establish Canonical Architecture And Bundle Contract |
| Rebuild Test And Quality Infrastructure | AC2, AC6, AC7, AC10, AC11 | Split catch-all tests, centralize fixtures, make Ruff and mypy real locked CI gates, and add architecture/parity/compatibility regression checks. | Extract Repository And Delivery Domains; Extract Coordination Execution And Adapter Foundations |
| Unify Documentation Prove Fitness And Dispose Debris | AC8, AC9, AC10, AC11, AC12, AC13 | Establish one documentation hierarchy, correct stale release guidance, complete the evidence-led cleanup inventory, run exact candidate journeys, and perform independent structural/functional QA. | Rebuild Test And Quality Infrastructure |

## Outcome Commitment Coverage

| Commitment | Proposed Child Owners | Parent ACs | Required Disposition |
| --- | --- | --- | --- |
| OC1 — One canonical change path | Architecture; both extraction children; proof/cleanup | AC1-AC5, AC8, AC11 | Every behaviour and instruction has one authored authority and verified derived surfaces. |
| OC2 — Complete maintainability capability | All five children | AC1-AC12 | Source, bundle, adapters, tests, quality, docs, and debris are improved together rather than partially. |
| OC3 — Ordinary contributor journey | Architecture; quality; proof/cleanup | AC3, AC4, AC7, AC10, AC11 | A focused change flows through generation and exact-candidate proof without manual mirror edits. |
| OC4 — Reject green-but-wrong cleanup | All five children | AC2-AC13 | Micro-module sprawl, compatibility drift, fake source authority, proof deletion, and claim broadening fail. |
| OC5 — Preserve scope boundaries | Architecture; proof/cleanup | AC4, AC5, AC8-AC13 | Product behaviour and delivery/runtime claims remain unchanged and separate. |
| OC6 — Preserve deployment assumptions | Architecture; both extraction children | AC3-AC5, AC10, AC11 | The local dependency-free helper and Python 3.10 support remain real. |
| OC7 — Current owner and release authority | Architecture; proof/cleanup | AC8-AC13 | The current task and released v0.9.0 baseline remain inspectable and no later gate is implied. |

## Open Questions (Answer Needed)

- None before meaning approval. Exact module names may change during planning if dependency analysis
  proves a cleaner boundary, but the module budget, entry-facade rule, standalone bundle, public
  compatibility, documentation hierarchy, and proof journey may not drift without an amendment.

## Decisions (Resolved)

- This is an Epic because source architecture, bundle generation, adapters, tests, quality gates,
  documentation, and repository cleanup are coupled but independently verifiable workstreams.
- The strongest smaller rival—extract only the new execution-control code—was rejected because
  status, upgrades, lifecycle, evidence, Doctor, and parser changes would remain coupled through the
  same 25,583-line authored module.
- A maximal granular split was also rejected. The target is a small set of domain modules with
  explicit direction, not one file per command, class, or schema.
- The dependency-free repository-local executable is a product constraint. It remains one generated
  artifact even though canonical authored source becomes modular.
- Line thresholds are guardrails for the entry point and mixed-responsibility regressions, not a
  license to split cohesive code or a substitute for dependency/cohesion review.
- Historical `.project-workflow` evidence is operational history, not product documentation. It
  remains auditable and is excluded from authored-code modularity targets.
- The current Constitution already directs the project toward a coherent core, evidence-pulled
  evolution, and protection against copied-helper sprawl. It needs no implementation-detail rewrite
  unless later evidence reveals a true product conflict.
- Static-analysis configuration must describe checks that actually run. Ruff and mypy currently do
  not pass and are not locked or executed by CI; the cleanup will fix the source and make the gates
  real rather than preserving decorative configuration.
- The superseded FIX-010 prototype branch/worktree is a cleanup candidate, not disposable by
  assumption. Its unique commit must be mapped to the v0.9.0 implementation/evidence before removal.
- Owner approval of this Epic authorizes planning and bounded local implementation only. It does not
  authorize push, merge, release, publication, consumer updates, or claims beyond the evidence.

## Controls

- Falsifier: a normal source change still requires editing a generated workflow mirror by hand.
- Falsifier: `project_workflow.cli` remains the owner of multiple material product domains.
- Falsifier: module count falls while circular imports, wildcard imports, compatibility shims, or
  cross-domain private imports increase.
- Falsifier: exact package or dependency-free local-helper behaviour differs from the v0.9.0
  baseline even though unit tests pass.
- Falsifier: any current instruction still directs a maintainer to 0.6.0 or another stale release,
  conflicting role/lifecycle semantics, or an unproved runtime-support claim.
- Falsifier: cleanup deletes historical proof, unique work, or active blocked state without an
  equally durable disposition.
- Stop condition: preserving standalone behaviour requires a second authored implementation;
  extraction reveals a public compatibility break that cannot be shimmed safely; current tests do
  not establish the baseline; or required proof would force a product/lifecycle redesign.
- Leading indicators: falling authored hotspot size, acyclic imports, one-command regeneration,
  fewer duplicate fixtures, static gates passing in CI, exact command/schema parity, and fewer
  current-source ambiguities.
- Review horizon: after exact wheel and standalone-helper journeys plus independent structural QA,
  before any merge or release decision.

## Validation Plan

- Capture the v0.9.0 command tree, JSON schema/version constants, generated-path inventory, source
  hashes, exact package journey, and repository-local dependency-free journey as baseline evidence.
- Add architecture tests for module size budget, import direction/cycles, thin CLI ownership,
  canonical/derived markers, and deterministic regeneration.
- Run focused tests after each extraction, then the complete locked suite after the candidate is
  frozen; never treat generated duplicate analysis as separate proof.
- Run locked Ruff check, Ruff format check, and mypy over canonical authored production source and
  the maintained test/script scope defined by the architecture contract.
- Build wheel and sdist once, inspect their complete source/resource inventory, and run disposable
  fresh-init, current-upgrade, legacy-upgrade, no-op, status, Doctor, and representative lifecycle
  journeys from the exact wheel.
- Run the installed `.project-workflow/cli/workflow` from a disposable repository with imports of
  the installed `project_workflow` package blocked, proving dependency-free standalone operation.
- Compare the candidate command/schemas/generated paths and representative outputs with v0.9.0;
  require explicit approval for any behavioural delta rather than calling it cleanup.
- Run strict Doctor, intent audit, acceptance audit, diff hygiene, documentation link/version
  checks, and one independent QA review focused on cohesion, necessity, model clarity, and fit for
  purpose.
- Stop with local validated evidence. Do not infer merge, release, publication, adoption, owner
  acceptance, or authenticated Claude Code certification.
