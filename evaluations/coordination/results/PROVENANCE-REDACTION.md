# Evaluation Provenance Redaction

Date: 2026-08-24

The first three retained evaluation runs correctly used sanitized synthetic scenarios, but their
recorded command arrays contained the maintainer's absolute workspace path for the output schema
and ephemeral `/var/folders/.../last.json` paths. No scenario, contract response, grade, usage value,
prompt hash, or response hash contained or required those paths.

The 13 retained JSON artifacts were mechanically redacted as one bounded privacy correction:

- the absolute output-schema path became `evaluations/coordination/output-schema.json`;
- every ephemeral last-message path became `<ephemeral-output-path>`.

Collection identity before redaction:
`sha256:1c4fe8759c97f7729279cd24f504b0a51ff49212c7efd962a5128a514374dbe5`

Collection identity after redaction:
`sha256:b3ad139ad50ec0b3b631fd866c4ded9eb644b844dad6db0097edbaa9312910fb`

The collection hash covers each path relative to `evaluations/coordination/results`, a NUL
separator, exact file bytes, and a closing NUL, ordered by path. The evaluator now records these
sanitized forms at creation, and `tests/test_coordination_evaluations.py` rejects retained absolute
personal or ephemeral paths.
