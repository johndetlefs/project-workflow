# TASK-108 Adversarial Structural And Functional QA

- Verdict: Pass after one bounded remediation pass
- Review mode: Separate adversarial pass in the current Coordinator context. No delegated reviewer
  was launched because current system policy forbids unrequested subagents.
- Source: `86ca8859eb5e331db2505c2ae7230e2bc0030242+working-tree-candidate`
- Delivery boundary: Local validated source only

## Falsifiers Examined

| Question | Evidence | Verdict |
| --- | --- | --- |
| Were files merely made smaller while coupling remained? | Ten manifest-ordered runtime modules have acyclic imports, no duplicate top-level definitions, no domain-to-CLI imports, explicit owners, and a 1,245-line entry facade. | Pass |
| Was the monolith replaced with micro-module sprawl? | The smallest shared runtime owner is a justified 169-line adapter primitive module; the main domains range from 1,459 to 4,654 lines and change for distinct reasons. | Pass |
| Are generated helpers still competing authored sources? | One manifest and generator produce both 26,018-line standalone targets; hashes are byte-identical and `--check` passes. | Pass |
| Does documentation point models in one direction? | README is 134 lines, detailed operations live in focused documents, the authority matrix assigns each truth type one owner, all links/current pins pass, and command syntax points to help. | Pass |
| Did cleanup delete unique work or proof? | The disposition ledger retains the active Claude canary worktree, the unique enforcement commit, 16 exact binary candidates, all workflow history, and the locked environment; only a merged recoverable local branch was removed before final output cleanup. | Pass |
| Did compatibility or ordinary use regress? | 561 tests pass; command/schema snapshot has no behavioural delta; the exact wheel passes four-agent init, current and legacy upgrade, no-op, Doctor, intent lifecycle, and import-blocked local-helper journeys. | Pass |
| Is the product claim broader than the evidence? | Evidence stops at local validated source and preserves the unauthenticated Claude canary as blocked. | Pass |

## Findings And Disposition

1. The old test contract forced delegation, status, and upgrade manuals back into README. Resolved by
   moving those assertions to the owning focused documents and preserving only README routing and
   proof boundaries. The full suite then passed.
2. `MANIFEST.in` requested nonexistent Python files from `evaluations/coordination`, causing a noisy
   setuptools warning. Resolved by removing only the dead `*.py` glob, rebuilding once, and rerunning
   the exact-wheel journeys; the final build is warning-free.
3. The parent Epic contract named proof owners by descriptive aliases even though closeout requires
   exact child IDs, leaving complete evidence unmapped. Resolved by replacing every alias with its
   decomposition-authorized `TASK-*` owner IDs; the regenerated acceptance audit is the affected
   validation.
4. After the parent reached Complete, Doctor could no longer project its retained verification
   campaign because coordination looked only at active work items. Resolved by falling back to the
   terminal global tracker row, with a focused regression plus 52 affected and 561 full passing
   tests; strict Doctor is clean on the completed Epic.

## Residual Boundaries

- `lifecycle.py` is the largest authored domain at 4,654 lines. It remains under the enforced 5,000
  line guardrail and is cohesive around work-item lifecycle, intent, evidence, readiness, and proof.
  Split only if a future change establishes a distinct reason to change, not to chase a smaller
  number.
- `project_workflow.cli` intentionally forwards maintained v0.9.0 compatibility names while new
  source imports canonical owners directly. This is a compatibility facade, not a second owner.
- EPIC-018/TASK-102 still lacks an authenticated hook-active Claude Code canary. Package and fixture
  proof do not close that runtime claim.

On the reviewed local candidate, Project Workflow is structurally coherent, maintainable, and
functionally fit for its repository-native intent, subject to the explicit delivery/runtime proof
boundaries above.
