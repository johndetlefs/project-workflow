---
name: project.smoke-bomb
description: Prepare a reviewed, sanitized client ZIP from an agency-owned project-workflow repository.
argument-hint: clientAgent=codex output=../client-handoff.zip validation="npm test"
agent: agent
---

Use this prompt when the user asks for a Smoke Bomb or sanitized client handoff.

Read the repository README, agent instructions, `.project-workflow/guidance.md`, and active delivery state. Recommend a disposable handoff branch but leave Git branch operations under user control. Prepare substantive client-facing human and agent context without inventing undocumented knowledge.

Run `project smoke-bomb` in plan mode with the intended client-agent target, explicit reviewed validation commands, and a ZIP output path outside the repository. Review and resolve every action, ownership decision, blocker, warning, archive exclusion, and plan fingerprint. Apply only the exact reviewed fingerprint, using `--yes` only with user authority.

Report the exported ZIP path and SHA-256, validation results, selected client-agent instructions, and archive inventory. The ZIP—not the agency repository or its history—is the handoff artifact. Do not bypass secret-like path, unsafe file, ambiguous ownership, missing guidance, dirty-worktree, or residual-reference blockers. Smoke Bomb does not replace legal, security, license, or data-loss-prevention review.
