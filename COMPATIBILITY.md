# Project Workflow Compatibility Policy

Project-workflow versions three independent contracts:

- **Package version** identifies the installed project-workflow release.
- **Asset version** identifies generated helpers, prompts, skills, rules, templates, and managed instruction blocks.
- **Repository schema version** identifies durable `.project-workflow/` artifact shapes.

Versioned repositories record these values in the project-workflow-owned
`.project-workflow/manifest.json`. User configuration remains in
`.project-workflow/config.json`; the manifest does not make project-workflow the owner of
trackers, backlog content, task or Epic records, approvals, evidence, guidance, or unmarked
repository content.

## Compatibility States

- `current`: asset and repository schema versions match the installed contract.
- `upgradeable`: a recognized, supported version is behind the installed contract.
- `legacy-unversioned`: recognizable project-workflow state exists without a manifest.
- `unsupported-future`: the repository uses a manifest, asset, or schema version newer than the installed CLI understands.
- `invalid`: the manifest is malformed, ambiguous, or names an unknown older contract.
- `not-initialized`: no manifest or recognizable project-workflow installation exists.

Classification is read-only. Missing or malformed metadata is never repaired or interpreted as
current during inspection.

## Support Window

The compatibility baseline is the recognized pre-versioned repository shape, represented as
repository schema version `0`. Project-workflow supports that baseline and every repository
schema version introduced after it until support is deliberately removed in a documented
breaking release.

Migration IDs are ordered and immutable. A future release may append migrations but must not
rename or reinterpret an ID already recorded by a repository.

Removing a schema from the support window requires all of the following:

1. A breaking package release.
2. A changelog entry naming the removed source schema and last supporting release.
3. A stable unsupported-state result with a concrete recovery path.
4. Historical fixtures retained for the last release that supported the removed schema.

`project init` owns managed-asset installation and refresh, `project doctor` owns diagnosis, and
`project upgrade` owns repository-schema transformation. Refreshing generated assets does not by
itself upgrade durable repository state.
