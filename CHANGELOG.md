# Changelog

All notable changes to this project are documented in this file.

## 0.1.1 - 2026-02-26

### Fixed

- Fixed `workflow task init` crash when `--update-tracker` is used without `--create-branch`.
- Hardened branch output handling so branch name is only referenced after successful branch creation.
- Updated packaged scaffold template so new installs receive the fix via `project init`.
