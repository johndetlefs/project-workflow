# project-workflow

Spec-driven development with AI coding agents.

A lightweight workflow framework for using **Cursor**, **OpenAI Codex**, or **GitHub Copilot** to guide feature development from requirements through implementation, QA review, and retro. Works entirely in Markdown—no complex tools or dashboards.

## For the Impatient

If your project is already a git repo and you have Cursor, Codex, or GitHub Copilot in VSCode:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init
```

Then in VSCode, use the installed workflow assets to build features spec-first:

- Copilot: use `/project.*` prompt commands.
- Codex: use the repo-scoped `$project-*` skills or ask Codex to follow `AGENTS.md`.
- Cursor: ask Cursor Agent to follow the project-workflow rule.

---

## Installation

### Prerequisites

- Git repo initialized
- Python 3.10+
- Cursor, OpenAI Codex extension in VSCode, GitHub Copilot extension in VSCode, or any combination
- UV or Python with pip

### One-Time Setup

From your project root:

```bash
uvx --from git+https://github.com/johndetlefs/project-workflow.git project init
```

This creates:

- `.project-workflow/` — Task folders, tracker, and local CLI
- `.cursor/rules/project-workflow.mdc` — Cursor project rule
- `.github/prompts/` — Eight agent definition files used by Copilot custom chat modes
- `AGENTS.md` — Codex project guidance
- `.agents/skills/` — Eight Codex skills matching the workflow steps
- `.project-workflow/TRACKER.md` — Centralized task status tracking

The setup is **idempotent**—safe to run again if you customized files; it asks before overwriting.

To install assets for only selected agent integrations:

```bash
project init --agents cursor
project init --agents codex copilot
project init --agents cursor codex copilot
```

`project init` with no `--agents` installs all supported integrations. The older `--agent copilot|codex|both` option still works for existing scripts, but new usage should prefer `--agents`.

---

## How to Use (The Typical Workflow)

You'll work in a cycle with your coding agent. Here's the pattern for building a new feature:

### 0. **Set Project Outcomes** (recommended once per repo)

In **Copilot chat**, run `/project.constitution` with a brief description of your project.

In **Codex**, invoke `$project-constitution` or ask Codex to establish the project constitution.

In **Cursor**, ask the Agent to establish the project constitution using project-workflow.

This agent scans your repo and creates/updates `.project-workflow/CONSTITUTION.md` as the source of truth for product outcomes (non-technical).

If technical guidance is missing, the agent should offer to create `.github/copilot-instructions.md` for Copilot, update `AGENTS.md` for Codex, or update `.cursor/rules/project-workflow.mdc` for Cursor.

### 1. **Create a Task** (5 min)

In **Copilot chat**, type `/project.scaffold` and answer the quick questions.

In **Codex**, invoke `$project-scaffold` or ask Codex to scaffold a project-workflow task:

In **Cursor**, ask the Agent to scaffold a project-workflow task:

```
Task ID: APP-001
Task title: User Account Export
Create a git branch: yes
```

The agent will generate a task folder under `.project-workflow/tasks/` and update your tracker. Commit this scaffold.

### 2. **Write Requirements** (15–30 min)

In **Copilot chat**, run `/project.requirements`.

In **Codex**, invoke `$project-requirements` or ask Codex to draft requirements for the task:

In **Cursor**, ask the Agent to draft requirements for the task:

```
Task: APP-001
Goal: Allow users to export their account data as PDF
Context: [any relevant links, design docs, constraints]
```

The agent will:

- Ask discovery questions ("What format? Who sees this?")
- Draft a user story
- List acceptance criteria
- Flag ambiguities as open questions

Answer each question iteratively. The agent updates `.project-workflow/tasks/APP-001-*/REQUIREMENTS.md` as you go.

**Stop when:** REQUIREMENTS.md is drafted (even if it has open questions).

### 3. **Create a Plan** (15 min)

In **Copilot chat**, run `/project.planner`.

In **Codex**, invoke `$project-planner` or ask Codex to create the implementation plan:

In **Cursor**, ask the Agent to create the implementation plan:

```
Task: APP-001
Plan focus: API + UI for account export
```

The agent generates:

- A phased approach (e.g., Phase 1: Backend API, Phase 2: UI)
- Implementation task list
- Validation steps for each phase

It updates `.project-workflow/tasks/APP-001-*/IMPLEMENTATION.md` with a task table.

**Output:** You now have a clear roadmap to code against.

### 4. **Clarify for Internal Consistency** (10–20 min, always)

After planning, run `/project.clarify`, invoke `$project-clarify`, or ask Cursor Agent to clarify consistency between REQUIREMENTS.md and IMPLEMENTATION.md:

```
Task: APP-001
Topic: Validate consistency between requirements and plan
```

The agent will:

- Surface conflicts or ambiguous decisions
- Propose options (A/B/C)
- Record chosen decisions in REQUIREMENTS.md
- Keep IMPLEMENTATION.md aligned with confirmed decisions

Run Clarify until there are no unresolved questions or conflicts.

### 5. **Implement & Validate** (varies)

For each work item in the task list, run `/project.implement`, invoke `$project-implement`, or ask Cursor Agent to implement a specific work item:

```
Task: APP-001
Work item: 1
```

The agent will:

- Read your requirements and plan
- Make code changes incrementally
- Run validation (tests, type checks, manual verification)
- Update `.project-workflow/TRACKER.md` with status (`In Progress` → `Testing`)

### 6. **QA & Code Review** (10-30 min)

After implementation reaches `Testing`, run `/project.qa-review`, invoke `$project-qa-review`, or ask Cursor Agent to QA and code review the task:

```
Task: APP-001
Scope: Review the implemented export flow
```

The agent will:

- Map acceptance criteria to validation evidence
- Review changed code for correctness, security, maintainability, and scope control
- Record findings in `.project-workflow/tasks/APP-001-*/IMPLEMENTATION.md`
- Move the tracker to `Review`, then to `Complete` only after review passes and you explicitly approve completion

### 7. **Retro & Update Conventions** (5-15 min)

After the task is `Complete`, run `/project.retro`, invoke `$project-retro`, or ask Cursor Agent to run the project-workflow retro:

```
Task: APP-001
Focus: Conventions, agent guidance, and follow-up tasks
```

The agent will:

- Capture reusable lessons from the completed task
- Update durable conventions, prompts, Codex skills, Cursor rules, or `AGENTS.md` when the task exposed a repeatable gap
- Record the retro in `IMPLEMENTATION.md`
- Propose separate follow-up tasks instead of reopening completed scope

The full loop is: implement, validate, review, complete, and capture durable lessons. The agent keeps everything in sync.

---

## File Structure (After Init)

```
your-project/
├── .project-workflow/
│   ├── TRACKER.md                    # ← Check this to see project status
│   ├── CONSTITUTION.md               # ← Product outcomes (non-technical)
│   ├── cli/
│   │   ├── workflow                  # Advanced: manual task scaffolding
│   │   └── workflow.py
│   └── tasks/
│       ├── APP-001-User-Export/
│       │   ├── IMPLEMENTATION.md      # ← User story, tasks, QA, retro
│       │   └── REQUIREMENTS.md        # ← Goals, specs, decisions (auto-updated)
│       └── APP-002-*/
│           └── ...
├── .github/
│   └── prompts/                      # ← Agent definitions used by Copilot
│       ├── Constitution.prompt.md    # /project.constitution
│       ├── Scaffold.prompt.md        # /project.scaffold
│       ├── Requirements.prompt.md    # /project.requirements
│       ├── Clarify.prompt.md         # /project.clarify
│       ├── Planner.prompt.md         # /project.planner
│       ├── Implement.prompt.md       # /project.implement
│       ├── QAReview.prompt.md        # /project.qa-review
│       └── Retro.prompt.md           # /project.retro
├── .cursor/
│   └── rules/
│       └── project-workflow.mdc      # ← Cursor project rule
├── .agents/
│   └── skills/                       # ← Repo-scoped Codex skills
│       ├── project-constitution/
│       ├── project-scaffold/
│       ├── project-requirements/
│       ├── project-clarify/
│       ├── project-planner/
│       ├── project-implement/
│       ├── project-qa-review/
│       └── project-retro/
├── AGENTS.md                         # ← Codex project guidance
└── [your code]
```

---

## Tips for Best Results

### 📌 Structure Your Workflow

The agents are designed to be used **in order**. Skipping steps = ambiguous code and rework.

1. **Constitution (once)** → 2. **Scaffold** → 3. **Requirements** → 4. **Planner** → 5. **Clarify** → 6. **Implement** → 7. **QA & Code Review** → 8. **Retro**

Always run Clarify after Planner to verify internal consistency before implementation.
Always run QA & Code Review before marking work complete, then run Retro after completion to keep conventions and agent guidance current.

### 📝 Keep Agent Definitions in the Repo

Commit `.github/prompts/`, `.cursor/rules/`, `.agents/skills/`, and `AGENTS.md` so the whole team uses the same workflow. You can customize these files; Copilot uses `.github/prompts/`, Cursor uses `.cursor/rules/`, and Codex uses `AGENTS.md` plus `.agents/skills/`.

### 🔍 Review Generated Docs Before Coding

When `/project.requirements`, `$project-requirements`, Cursor requirements work, `/project.planner`, `$project-planner`, or Cursor planning work finishes:

- Read the generated REQUIREMENTS.md and IMPLEMENTATION.md
- Edit directly if something is wrong
- Your agent will respect your edits on next use

### 🚀 One Feature = One Task ID

Don't mix multiple features under one task. It makes the tracker useless.

Good: `APP-001: User Account Export`
Bad: `APP-001: Export + Billing View + Email Notifications`

### ⚡ Use the TRACKER as Your Source of Truth

`.project-workflow/TRACKER.md` is visible to everyone. Use it to communicate status to your team.

```markdown
| ID      | Title                  | Status      | Docs                                              |
| ------- | ---------------------- | ----------- | ------------------------------------------------- |
| APP-001 | User Account Export    | Complete    | `tasks/APP-001-User-Export/IMPLEMENTATION.md`     |
| APP-002 | Fix login timeout      | In Progress | `tasks/APP-002-Login-Timeout/IMPLEMENTATION.md`   |
| APP-003 | Email retention policy | To Do       | `tasks/APP-003-Email-Retention/IMPLEMENTATION.md` |
```

### Commit Early, Commit Often

- After Scaffold → Commit
- After Requirements → Commit
- After Planner + Clarify alignment → Commit
- After each work item → Commit
- After QA & Code Review → Commit
- After Retro updates → Commit

This keeps your history clean and lets teammates review requirements before coding starts.

---

## Example: Start to Finish

```bash
# 1. Initialize
$ uvx --from git+https://github.com/johndetlefs/project-workflow.git project init
✅ Project workflow initialized

# 2. In Copilot chat: /project.constitution
#    Or in Codex: $project-constitution
#    Or in Cursor: ask Agent to establish the project constitution
# 3. Provide a project brief; the agent scans repo and updates CONSTITUTION.md
# 4. Commit: "docs: establish project constitution"

# 5. In Copilot chat: /project.scaffold
#    Or in Codex: $project-scaffold
#    Or in Cursor: ask Agent to scaffold a project-workflow task
# 6. Answer: ID=APP-001, Title="Dark Mode Support", Branch=yes
# 7. The agent runs: ./.project-workflow/cli/workflow task init ...
# 8. Commit: "scaffold: APP-001 Dark Mode Support"

# 9. In Copilot chat: /project.requirements
#    Or in Codex: $project-requirements
#    Or in Cursor: ask Agent to draft requirements
# 10. Answer discovery questions; the agent updates REQUIREMENTS.md
# 11. Commit: "requirements: APP-001 dark mode draft"

# 12. In Copilot chat: /project.planner
#     Or in Codex: $project-planner
#     Or in Cursor: ask Agent to create the implementation plan
# 13. The agent generates implementation plan and updates IMPLEMENTATION.md with task table

# 14. In Copilot chat: /project.clarify
#     Or in Codex: $project-clarify
#     Or in Cursor: ask Agent to clarify requirements and plan
# 15. Resolve any conflicts/open questions between requirements and plan
# 16. Repeat clarify until consistent
# 17. Commit: "plan+clarify: APP-001 dark mode aligned requirements and plan"

# 18. In Copilot chat: /project.implement
#     Or in Codex: $project-implement
#     Or in Cursor: ask Agent to implement the selected work item
# 19. The agent implements Phase 1, runs tests, updates TRACKER to Testing
# 20. You review changes, commit
# 21. Repeat for Phase 2, 3, ... with the same task ID

# 22. In Copilot chat: /project.qa-review
#     Or in Codex: $project-qa-review
#     Or in Cursor: ask Agent to QA and code review the task
# 23. The agent records findings/evidence and completes only after approval

# 24. In Copilot chat: /project.retro
#     Or in Codex: $project-retro
#     Or in Cursor: ask Agent to run the post-completion retro
# 25. The agent updates durable conventions or agent guidance when needed
```

---

## What Happens Inside the Agent?

When you run an agent command, skill, or Cursor request (for example `/project.requirements`, `$project-requirements`, or “draft requirements for APP-001”) and provide inputs (task ID, goal, etc.), the agent:

1. **Reads** your existing task files (REQUIREMENTS.md, IMPLEMENTATION.md)
2. **Asks** clarifying questions (discovers gaps)
3. **Generates** structured Markdown (requirements, plans, code)
4. **Updates** your local files (you can review before accepting)
5. **Syncs** TRACKER.md with status (To Do → In Progress → Testing → Review → Complete)
6. **Keeps conventions current** with a retro after completion

Everything is **plain text**—you can edit, version control, and code-review it like any other file.

---

## When Things Go Wrong

**"The agent's plan doesn't match my codebase"**

→ Edit REQUIREMENTS.md to clarify constraints, re-run `/project.planner` or `$project-planner`, then run clarify to ensure consistency before implementation.

**"I want to change the requirements mid-way"**

→ Prefer running requirements again so the agent updates REQUIREMENTS.md, then run planner, then clarify, and only then continue with implement. In a pinch, you can edit REQUIREMENTS.md manually first, but still run Planner + Clarify before implementation.

**"My agents keep generating the same output"**

→ Review `.github/prompts/`, `.cursor/rules/`, `.agents/skills/`, and `AGENTS.md`. You can edit those definitions directly; add repo-specific constraints, design patterns, and tooling notes.

**"I want to scaffold a task without using an agent"**

→ Use the local CLI:

```bash
./.project-workflow/cli/workflow task init --id APP-009 --title "Manual Task" --update-tracker
```

---

## Architecture (if you're curious)

- **Copilot prompts** (`/project.*`, defined in `.github/prompts/*.md`) — Structured workflow commands for Copilot chat
- **Cursor rules** (`.cursor/rules/project-workflow.mdc`) — Persistent Cursor Agent guidance for the workflow
- **Codex skills** (`$project-*`, defined in `.agents/skills/project-*/SKILL.md`) — Structured workflow skills for Codex CLI, IDE extension, and app
- **Codex guidance** (`AGENTS.md`) — Project instructions Codex reads before work
- **Tracker** (`.project-workflow/TRACKER.md`) — Single source of truth for project status
- **Constitution** (`.project-workflow/CONSTITUTION.md`) — Product outcome source of truth (non-technical)
- **Task docs** (`.project-workflow/tasks/*/`) — REQUIREMENTS.md (goals) + IMPLEMENTATION.md (plan + user story)
- **Local CLI** (`.project-workflow/cli/`) — Scaffolds new tasks, manages git branches (optional, can be automated via agents)

No database, no external service, no vendor lock-in—just Markdown and git.

---

## License

MIT

---

## Questions?

- 💬 Check [GitHub Issues](https://github.com/johndetlefs/project-workflow/issues)
- 🔧 Customize `.github/prompts/`, `.cursor/rules/`, `.agents/skills/`, and `AGENTS.md` to fit your team's needs
- 📚 Read the [Local CLI docs](.project-workflow/cli/README.md) for advanced task scaffolding
