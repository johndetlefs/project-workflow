# Current Claude Code contract inspected

Inspected on 2026-08-28 before implementation:

- CLI reference: <https://code.claude.com/docs/en/cli-reference>
- Headless/print mode: <https://code.claude.com/docs/en/headless>
- Hooks reference: <https://code.claude.com/docs/en/hooks>
- Hooks guide: <https://code.claude.com/docs/en/hooks-guide>
- Plugin reference: <https://code.claude.com/docs/en/plugins-reference>
- Configuration: <https://code.claude.com/docs/en/configuration>
- Permissions: <https://code.claude.com/docs/en/permissions>
- Permission modes: <https://code.claude.com/docs/en/permission-modes>
- Server-managed settings: <https://code.claude.com/docs/en/server-managed-settings>

The adapter is bound to an exact supported version at or above its declared 2.1.217 floor, current
non-interactive print mode, newline-delimited `stream-json`, verbose hook events, explicit
allowed/disallowed tools, `--max-turns`, `--max-budget-usd`, finite process-tree timeout,
package-local `--plugin-dir`, no session persistence, and `dontAsk` permission mode. Exact native
allow rules cover read tools, sealed edit paths and literal Bash commands; regex-only Bash authority
is rejected because Claude native permission rules cannot reproduce it safely. `claude --help` is
not used as a capability oracle because the official CLI reference says help does not enumerate
every flag.

SessionStart supplies context and is used for a model-free activation preflight, but it cannot
block. PreToolUse can deny before execution. PostToolUse/PostToolUseFailure observe after execution,
PostToolBatch can stop the loop before the next model call, and Stop is an observation boundary.
Command-hook failure/timeout can be non-blocking, so hooks are not the sole safety boundary: native
permissions remain restrictive even when a hook fails, while the supervisor records sticky hook
failure and interrupts the process group. The adapter expects `system/init` plus a typed `result`
subtype and requires actual SessionStart state for the material invocation. Managed policy can
prevent ordinary plugin hooks; that case is reported as non-support rather than bypassed or inferred
from static package files.

This record proves the implementation target was checked against current official documentation.
It does not prove a local installation, authentication, plugin activation, or real model journey.
