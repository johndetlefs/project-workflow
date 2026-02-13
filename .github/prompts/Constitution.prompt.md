---
name: project.constitution
description: Create or refine the project's outcome-focused constitution from a brief and repo context.
argument-hint: projectBrief="..." context="..."
agent: agent
---

Use this agent to establish or update the canonical project outcomes document at `/.project-workflow/CONSTITUTION.md`.

Purpose:

- Define **what success means** for this project in user/business terms.
- Keep outcome guidance separate from implementation guidance.
- Ensure technical constraints live in `/.github/copilot-instructions.md` (or repo equivalent), not in the constitution.

Inputs:

- Project brief: `${input:projectBrief:One-paragraph description of the product and intended users}`
- Optional context: `${input:context:Roadmap links, docs, constraints, notes}`

Reference docs to read first (if present):

- `README.md`
- `/.project-workflow/TRACKER.md`
- Existing `/.project-workflow/CONSTITUTION.md`
- `/.github/copilot-instructions.md`
- Common product docs in repo root (`docs/**`, `specs/**`, `product/**`, `roadmap/**`)

Rules:

- `CONSTITUTION.md` is **not** a technical implementation doc.
- Do not put framework choices, folder structure, lint rules, or coding conventions in `CONSTITUTION.md`.
- Keep the constitution stable and outcome-focused; avoid sprint-level details.
- If repo context conflicts with user brief, ask clarifying questions before finalizing.

Workflow (must follow):

1. Discovery + scan

- Read the files above and summarize current product intent in 5–10 bullets.
- If `projectBrief` is missing or too vague, ask the minimum questions needed to proceed.

2. Draft or refine constitution

- Create/update `/.project-workflow/CONSTITUTION.md` using the structure below.
- Preserve useful existing content; improve clarity and remove technical directives.

3. Validate boundaries

- Ensure each section is outcome-oriented and testable at a product level.
- Remove technical implementation instructions from constitution and point those to copilot instructions.

4. Copilot instructions fallback

- If `/.github/copilot-instructions.md` does not exist, explicitly offer to create it.
- If the user accepts, create a minimal technical guidance file with repo conventions/tooling constraints.
- If the user declines, continue and note that technical guidance is currently missing.

Required output artifact:

- Write/update `/.project-workflow/CONSTITUTION.md`.

Use this constitution template (adapt content to project):

```md
# Constitution

## Mission

- <What this project exists to achieve>

## Target Users

- <Primary users>
- <Secondary users>

## Core Outcomes

- <Outcome 1: user/business result>
- <Outcome 2>
- <Outcome 3>

## Non-Goals

- <Explicitly out of scope>

## Product Principles

- <Principle 1>
- <Principle 2>
- <Principle 3>

## Success Signals

- <How we know outcomes are being achieved>

## Decision Filters

- <How to choose between competing options>

## Assumptions & Risks

- <High-level assumptions and product risks>

## Change Log

- <YYYY-MM-DD>: <summary of constitution change>
```

Final response requirements:

- Summarize what changed in `CONSTITUTION.md`.
- Call out any unresolved product questions.
- If copilot instructions are missing, include: “I can create `/.github/copilot-instructions.md` now — proceed?”
