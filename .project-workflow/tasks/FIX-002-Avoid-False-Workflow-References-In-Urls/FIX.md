# Fix

## Summary

- Fix: FIX-002
- Title: Avoid False Workflow References In URLs
- Status: Complete
- Created: 2026-07-20

## Report

- Observed or requested: Strict doctor treats a dashed repository slug inside a valid external URL as a missing local workflow ID.
- Expected: External links remain opaque, while `Originating work` validates only syntactically valid configured task, epic, and Fix IDs against the local tracker.
- Affected users or systems: Maintainers using external issue, commit, pull-request, deployment, or evidence links in Fix records.
- Delivered baseline: TASK-038 introduced local related-work validation and supported external links in the lightweight Fix record.
- Report evidence: A GitHub URL containing `/project-workflow/` produced a missing-reference error for `PROJECT-WORKFLOW` under strict doctor.

## Routing

- Decision: Fix
- Rationale: This is one bounded validator defect against completed TASK-038 behavior, with a narrow parser and regression-test correction.
- Related work state: TASK-038 and FIX-001 are Complete
- Bounded correction: Yes; narrow reference extraction without changing Fix lifecycle or tracker semantics.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: Valid external links can block strict workflow validation and therefore block release completion.
- Urgency: Normal corrective maintenance; a textual workaround exists but violates the intended external-link experience.
- Owner: Repository owner

## Related Work

- Originating work: TASK-038, FIX-001
- External links: https://github.com/johndetlefs/project-workflow/commit/0e9ad3cd8a51ddb3acc07c0608fdceb2da45877a

## Risk

- Risk level: Low
- Risks: Over-filtering could hide a genuinely missing local workflow reference; under-filtering would preserve URL false positives.
- Rollback or containment: Preserve current missing-local-reference checks in regression tests and revert the parser change if those checks regress.

## Fix Plan

- Scope: Inspect only `Originating work` for local references, accept only IDs valid under configured task/epic/Fix namespaces, and add positive and negative regression coverage.
- Non-goals: Do not validate external URLs over the network, alter ID generation, change tracker schemas, or weaken checks for valid missing local IDs.
- Affected target: Fix related-work parsing and doctor validation in the canonical CLI and maintained mirrors.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Branch `codex/FIX-002-ignore-url-slugs-in-related-work`; evidence recorded below.
- Verification plan: Reproduce with dashed URL slugs, prove strict doctor ignores external-link tokens, prove valid configured missing IDs still fail, run full pytest, mirror parity, diff checks, and strict doctor.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | codex/FIX-002-ignore-url-slugs-in-related-work | None | regression pytest, mirror parity, diff check, and strict doctor evidence in this record |

## Verification

- Delivered scope: External-link values are no longer scanned as local workflow references; `Originating work` candidates are filtered through configured task, epic, and Fix ID formats before local tracker validation.
- Verification result: The new integration regression passed, the full 74-test suite passed, strict doctor accepted this record's `/project-workflow/` URL, and both maintained CLI mirrors are byte-identical to the canonical source.
- Adjacent behavior checked: A known configured unique task ID passes; a valid configured missing ID inside an external URL is ignored; the same missing ID in `Originating work` still fails strict doctor; historical integrity and normal Fix lifecycle tests remain green.
- Original acceptance criteria result: TASK-038 AC7 and AC12 now accept intended external links while retaining locally checkable broken-reference validation; AC13-AC14 mirror and regression obligations pass.
- Regression evidence: Focused regression set passed 3/3; `.venv/bin/pytest -q` passed 74/74 in 27.64 seconds; canonical/template/local CLI comparisons returned 0; strict doctor and `git diff --check` passed.
- Residual risk: External URL reachability remains intentionally unvalidated, and arbitrary unconfigured hyphenated labels in `Originating work` are treated as prose rather than local workflow IDs.

## Outcome

- Disposition: Fixed
- Decision: External links remain opaque while configured originating-work references retain local validation.
- Closed by: Codex on owner authorization
- Closed date: 2026-07-20
- Promoted to: None
