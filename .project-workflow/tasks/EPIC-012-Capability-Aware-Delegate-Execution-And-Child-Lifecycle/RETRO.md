# Epic Retro

- Epic: EPIC-012
- Title: Capability-Aware Delegate Execution And Child Lifecycle
- Last updated: 2026-08-20

## Lessons

- Task-versus-Epic is the wrong executor boundary. Route each unit from explicit work properties and current host capability, then schedule it independently.
- In-session subagents are the normal choice for bounded return-only work. Persistent visible tasks are justified by durability, direct owner steering, or required isolation—not by Epic membership.
- Verification, durable disposition, and retirement are separate coordinator-observed states. An existing visible handle must remain reconcilable even when new-task authority has expired or free creation capacity is zero.
- Host-reported capacity means currently free child slots. Active-slot accounting belongs against the immutable plan/request budget and must not be subtracted from free runtime capacity twice.
- Successful temporary Codex tasks should archive after verified durable disposition; unresolved, retained, promoted, owner-steered, or unverified work remains visible.

## Follow-up Tasks

- Optional future validation: exercise the native Claude Code, GitHub Copilot, and Cursor adapters when those host runtimes are available. Current delivery is syntax-, package-, init-, Doctor-, and upgrade-validated only for those hosts.

## Deferrals

- None.

## Missed In-Scope Work

- None identified by independent QA or the passing acceptance audit.
