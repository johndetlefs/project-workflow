# Epic Retro

- Epic: EPIC-007
- Title: Versioned Repository Upgrade System
- Last updated: 2026-07-21

## Lessons

- Repository compatibility needs separate package, generated-asset, and durable schema versions; a single package version cannot describe whether a repository is current.
- Public command ownership must match user intent: `init` creates, `doctor` diagnoses, and canonical `upgrade` refreshes managed assets plus durable schema in one reviewed transaction.
- Internal asset and schema boundaries are valuable for versioning and tests, but they must not become mandatory user choreography.
- A safe apply contract must bind both expected inputs and predicted outputs to the reviewed plan fingerprint, then recheck repository state immediately before writing.
- The first legacy migration is strongest when it changes only the new managed manifest and proves all pre-existing workflow and user-owned content remains byte-for-byte unchanged.
- Epic proof-owner contracts must identify owners by stable work-item ID. Human-readable titles alone cannot satisfy machine-enforced ownership.

## Follow-up Tasks

- BL-009 retains CLI modularization; the source/template/generated-helper parity model is correct but the growing single-file implementation increases maintenance cost.
- BL-010 retains package, changelog, tag, and release-version hygiene for publication of the delivered contract.
- BL-014 retains the longer-term generated-helper distribution strategy.

## Deferrals

- No approved EPIC-007 acceptance criterion was deferred. Adjacent scope remains explicitly outside the Epic under BL-006, BL-007, BL-009, BL-010, BL-014, and BL-016.

## Missed In-Scope Work

- None identified by the passing acceptance audit, full regression suite, strict Doctor, backlog validation, compilation, or packaged/generated parity checks.
