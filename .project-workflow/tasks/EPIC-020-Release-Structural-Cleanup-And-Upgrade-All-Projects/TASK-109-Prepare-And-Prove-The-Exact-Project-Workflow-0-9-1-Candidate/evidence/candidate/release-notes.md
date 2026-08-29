# project-workflow 0.9.1

### Changed

- Replaced the authored 25,583-line CLI monolith with cohesive, acyclic runtime domains, a bounded
  compatibility facade, and one deterministic manifest-driven standalone runtime without changing
  the public v0.9 command or schema contract.
- Split the catch-all Doctor tests into product-boundary suites, centralized only shared fixtures,
  and made locked Ruff, Ruff format, mypy, architecture, documentation, full-suite, and package
  journey checks part of both CI and release validation.
- Replaced the oversized README and stale release guidance with a small authority-led documentation
  hierarchy covering architecture, use, contribution, maintenance, and release ownership.

### Fixed

- Kept a completed Task or Epic's retained verification campaign inspectable from terminal global
  tracker state so Doctor and delivery projection do not lose exact-candidate proof after closeout.
- Removed dead distribution globs and stale current-version guidance while retaining historical
  workflow records, exact release artifacts, blocked proof obligations, and unique work.
