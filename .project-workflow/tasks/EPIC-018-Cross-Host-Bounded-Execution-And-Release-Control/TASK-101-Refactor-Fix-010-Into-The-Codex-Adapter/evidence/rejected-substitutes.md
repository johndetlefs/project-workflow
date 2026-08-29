# Rejected TASK-101 substitutes

The passing runtime claim does not rely on any of these substitutes:

- deterministic tests without a real host turn;
- hook discovery without SessionStart activation;
- a completed App Server turn without the exact required workspace change;
- package presence without activation and runtime evidence;
- publication, installation, adoption or owner-acceptance inference.

During implementation, earlier disposable canaries exposed both hook-trust propagation and
required-change closeout defects. Their non-passing receipts remain described in the task's QA
history and are not used as passing evidence. The retained passing claim is bound only to the final
hook-active canary, exact changed path and bytes, stable source identity and core-owned passing
receipt recorded in `real-codex-canary.json`.
