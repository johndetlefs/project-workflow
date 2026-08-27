# Epic Retro

- Epic: EPIC-017
- Title: Proportionate Verification Lifecycle
- Last updated: 2026-08-27

## Lessons

- Project Workflow 0.7.0's sufficient-proof stop gate was necessary but not sufficient: it could stop repeated QA only after proof existed, while materially expensive pre-QA verification still needed a durable candidate/scope/stage/limit contract.
- Materiality and scope must be stored before implementation, not supplied transiently at preflight; otherwise a required campaign can be omitted or redefined at Review.
- Currentness must bind the ordered receipt ledger and consumer checkpoint fields that can change an outcome. Per-record self-hashes and positive-path fixtures did not cover rehashing, stage relabelling, session replacement, or runtime-read tampering.
- A preserved independent `Changes Requested` verdict plus one affected validation disposition is the stopping mechanism. Commissioning a second QA would recreate the loop this Epic exists to prevent.
- Project Workflow and Strategic Advisor remain independent products. Their optional interoperability is a generic command/JSON capability and receipt boundary, with standalone/manual paths on both sides.

## Follow-up Tasks

- Strategic Advisor EPIC-007 owns consumer-specific reconciliation and adoption against the released Project Workflow 0.8.0 contract. It remains independent and is not a closure dependency for this generic product Epic.

## Deferrals

- No parent acceptance criterion was deferred. Separate owner authority was subsequently granted for delivery: PR #23 merged, `v0.8.0` was published to PyPI and GitHub, and the public package journey passed.

## Missed In-Scope Work

- None identified. The final acceptance audit maps all 15 parent acceptance criteria to complete child evidence with no gaps.
