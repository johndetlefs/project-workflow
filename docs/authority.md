# Documentation And Source Authority

Project Workflow has one authority for each kind of truth. More detailed material explains its
owning contract; it does not silently redefine another surface.

| Question | Authority |
| --- | --- |
| What durable product outcomes and principles govern decisions? | `.project-workflow/CONSTITUTION.md` |
| What must an agent do in this repository? | `AGENTS.md` and `.project-workflow/guidance.md` |
| What command and option exists now? | `project --help` and `.project-workflow/cli/README.md` |
| How is the package structured, maintained, supported, or released? | The matching focused document under `docs/`, `COMPATIBILITY.md`, or `RELEASING.md` |
| Where does a new reader start? | `README.md` |
| What was decided, attempted, or proved for a work item? | `.project-workflow/tasks/` and evaluation results |

Task records can explain why a change happened, but they are not current product instructions.
README is orientation, not command authority. If two current surfaces make incompatible claims,
repair the one speaking outside its ownership; escalate only a real product-outcome conflict to the
Constitution owner.

## Authored And Generated Surfaces

Canonical authored product assets live under `src/project_workflow/`:

- runtime domain modules and explicit host adapters;
- prompt and skill sources;
- host plugin sources and Cursor rules;
- the dependency-free launcher template.

The runtime module order is declared in `scripts/runtime-modules.txt`. The generator writes
`src/project_workflow/templates/workflow.py` and the source repository's
`.project-workflow/cli/workflow.py`. Installed agent files, managed instruction blocks, local CLI
copies, and adapter copies are derivatives. Change their canonical source or supported generator;
do not maintain a second authored implementation in an installed path.

Repository-owned data includes backlog and tracker content, requirements, implementation records,
approvals, evidence, retrospectives, accepted warning reasons, configuration, and local guidance.
Upgrade may transform declared schema or managed assets, but it does not convert repository-owned
history into package-owned instruction.

## Resolving Uncertainty

1. Use `project status` for sourced operational truth and the next safe action.
2. Use `project doctor` for workflow structure and compatibility diagnosis.
3. Use `project --help` for syntax rather than copying an old task's command.
4. Use `COMPATIBILITY.md` for supported repository states and `RELEASING.md` only for public release.
5. Preserve uncertainty as unknown or blocked when the authoritative evidence layer is absent.

This hierarchy deliberately separates stable outcomes from implementation architecture. The
Constitution therefore stays small and changes only for a product-level conflict, not a module
move, test split, or documentation reorganization.
