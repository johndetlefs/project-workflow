#!/usr/bin/env python3
"""Exercise packaged init and upgrade behavior in disposable repositories."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PREFIX = "project_workflow/"
PROMPT_SUFFIX = ".prompt.md"
GENERATED_MARKER = "project-workflow:generated"


def run(command: list[str], cwd: Path, env: dict[str, str]) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return completed.stdout


def run_result(
    command: list[str], cwd: Path, env: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def sha256_path(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def sha256_json(payload: object) -> str:
    rendered = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(rendered)


def _wheel_resources(package_path: Path) -> dict[str, bytes]:
    if package_path.suffix != ".whl":
        raise RuntimeError("package journey parity requires an exact wheel path")
    with zipfile.ZipFile(package_path) as archive:
        return {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}


def _source_package_assets() -> dict[str, Path]:
    source_root = ROOT / "src/project_workflow"
    assets = {
        "project_workflow/templates/workflow.py": source_root / "templates/workflow.py",
        "project_workflow/templates/workflow": source_root / "templates/workflow",
        "project_workflow/codex/AGENTS.md": source_root / "codex/AGENTS.md",
        "project_workflow/cursor/rules/project-workflow.mdc": (
            source_root / "cursor/rules/project-workflow.mdc"
        ),
    }
    for path in sorted(source_root.glob("*.py")):
        assets[f"project_workflow/{path.name}"] = path
    for path in sorted((source_root / "prompts").glob("*.md")):
        assets[f"project_workflow/prompts/{path.name}"] = path
    for path in sorted((source_root / "codex/skills").glob("*/SKILL.md")):
        assets[f"project_workflow/codex/skills/{path.parent.name}/SKILL.md"] = path
    return assets


def _sdist_member_bytes(archive: tarfile.TarFile, relative: str) -> bytes:
    matches = []
    for member in archive.getmembers():
        _, separator, member_relative = member.name.partition("/")
        if separator and member_relative == relative:
            matches.append(member)
    if len(matches) != 1:
        raise RuntimeError(f"sdist must contain exactly one /{relative}: found {len(matches)}")
    extracted = archive.extractfile(matches[0])
    if extracted is None:
        raise RuntimeError(f"cannot read sdist member: {matches[0].name}")
    return extracted.read()


def verify_package_source_parity(package_path: Path) -> dict[str, Any]:
    """Bind every shipped intent surface and sanitized fixture to current source bytes."""
    resources = _wheel_resources(package_path)
    source_assets = _source_package_assets()
    packaged_asset_names = {
        name
        for name in resources
        if name in source_assets
        or name.startswith("project_workflow/prompts/")
        or name.startswith("project_workflow/codex/skills/")
    }
    if packaged_asset_names != set(source_assets):
        missing = sorted(set(source_assets) - packaged_asset_names)
        unexpected = sorted(packaged_asset_names - set(source_assets))
        raise RuntimeError(
            f"wheel/source asset set mismatch; missing={missing}; unexpected={unexpected}"
        )
    manifest: dict[str, str] = {}
    for resource_name, source_path in sorted(source_assets.items()):
        source_bytes = source_path.read_bytes()
        if resources.get(resource_name) != source_bytes:
            raise RuntimeError(f"wheel resource differs from current source: {resource_name}")
        manifest[resource_name] = sha256_bytes(source_bytes)

    helper_bytes = resources["project_workflow/templates/workflow.py"]
    for mirror in (
        ROOT / "src/project_workflow/templates/workflow.py",
        ROOT / ".project-workflow/cli/workflow.py",
    ):
        if mirror.read_bytes() != helper_bytes:
            raise RuntimeError(f"wheel helper differs from generated runtime: {mirror}")

    metadata_names = [name for name in resources if name.endswith(".dist-info/METADATA")]
    if len(metadata_names) != 1:
        raise RuntimeError("wheel must contain exactly one METADATA file")
    metadata = resources[metadata_names[0]].decode("utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if metadata.split("\n\n", 1)[1] != readme:
        raise RuntimeError("wheel long description differs from current README.md")

    sdist_path = next(iter(sorted(package_path.parent.glob("*.tar.gz"))), None)
    if sdist_path is None:
        raise RuntimeError("exact candidate source distribution is missing beside the wheel")
    sdist_sources: dict[str, Path] = {
        name: ROOT / name for name in ("README.md", "LICENSE", "CHANGELOG.md")
    }
    for path in sorted((ROOT / "scripts").rglob("*.py")):
        if "__pycache__" not in path.parts:
            sdist_sources[path.relative_to(ROOT).as_posix()] = path
    for path in sorted((ROOT / "evaluations/intent_integrity").rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            sdist_sources[path.relative_to(ROOT).as_posix()] = path
    for path in sorted((ROOT / "evaluations/coordination").rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            sdist_sources[path.relative_to(ROOT).as_posix()] = path
    for path in sorted((ROOT / "tests").rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            sdist_sources[path.relative_to(ROOT).as_posix()] = path
    with tarfile.open(sdist_path, "r:gz") as archive:
        for relative, source_path in sorted(sdist_sources.items()):
            if _sdist_member_bytes(archive, relative) != source_path.read_bytes():
                raise RuntimeError(f"sdist member differs from current source: {relative}")

    return {
        "wheel_sha256": sha256_path(package_path),
        "sdist_sha256": sha256_path(sdist_path),
        "resource_count": len(manifest),
        "resource_manifest": manifest,
        "resource_manifest_sha256": sha256_json(manifest),
        "readme_sha256": sha256_path(ROOT / "README.md"),
        "sdist_bound_source_count": len(sdist_sources),
    }


def _split_frontmatter(content: str) -> tuple[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, flags=re.DOTALL)
    return (match.group(1), match.group(2)) if match else ("", content)


def _frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", frontmatter, flags=re.MULTILINE)
    return match.group(1).strip().strip('"').strip("'") if match else None


def _agent_name(prompt_name: str) -> str:
    base_name = prompt_name.removesuffix(PROMPT_SUFFIX)
    canonical = {"QAReview": "qa-review"}
    slug = canonical.get(base_name, base_name.lower())
    return f"project-{slug}"


def _render_native_agent(prompt: bytes, prompt_name: str, host: str) -> bytes:
    frontmatter, body = _split_frontmatter(prompt.decode("utf-8"))
    name = _agent_name(prompt_name)
    description = (_frontmatter_value(frontmatter, "description") or name).replace('"', r"\"")
    rendered_body = re.sub(
        r"\$\{input:([A-Za-z][A-Za-z0-9_-]*)(?::[^}]*)?\}",
        lambda match: f"<{match.group(1)}>",
        body,
    )
    rendered = (
        "---\n"
        f"name: {name}\n"
        f'description: "{description}"\n'
        "---\n\n"
        f"Invocation contract ({host}): supply values such as `<taskId>` or `<scope>` "
        "in the user request or current conversation. Treat angle-bracket values as required "
        "request fields, not literal text.\n\n" + rendered_body.lstrip()
    )
    return rendered.encode("utf-8")


def _generated_bytes(relative: str, content: bytes) -> bytes:
    text = content.decode("utf-8")
    if GENERATED_MARKER in text:
        return content
    suffix = Path(relative).suffix
    marker = (
        f"<!-- {GENERATED_MARKER} -->" if suffix in {".md", ".mdc"} else f"# {GENERATED_MARKER}"
    )
    if suffix in {".md", ".mdc"}:
        frontmatter = re.match(r"^(---\n.*?\n---\n)(.*)$", text, flags=re.DOTALL)
        if frontmatter:
            header, body = frontmatter.groups()
            return f"{header}{marker}\n\n{body.lstrip()}".encode()
        return f"{marker}\n\n{text.lstrip()}".encode()
    if text.startswith("#!"):
        first_line, separator, rest = text.partition("\n")
        if separator:
            return f"{first_line}\n{marker}\n{rest}".encode()
    return f"{marker}\n{text.lstrip()}".encode()


def verify_generated_asset_parity(
    path: Path, agent: str, resources: dict[str, bytes]
) -> dict[str, Any]:
    expected: dict[str, bytes] = {
        ".project-workflow/cli/workflow.py": resources["project_workflow/templates/workflow.py"],
        ".project-workflow/cli/workflow": resources["project_workflow/templates/workflow"],
    }
    prompts = {
        name.removeprefix("project_workflow/prompts/"): content
        for name, content in resources.items()
        if name.startswith("project_workflow/prompts/")
    }
    skills = {
        name.removeprefix("project_workflow/codex/skills/"): content
        for name, content in resources.items()
        if name.startswith("project_workflow/codex/skills/")
    }
    if agent == "codex":
        expected.update({f".agents/skills/{name}": content for name, content in skills.items()})
    elif agent == "github-copilot":
        expected.update({f".github/prompts/{name}": content for name, content in prompts.items()})
    elif agent == "claude-code":
        expected.update(
            {
                f".claude/agents/{_agent_name(name)}.md": _render_native_agent(
                    content, name, "Claude Code"
                )
                for name, content in prompts.items()
            }
        )
    elif agent == "cursor":
        expected.update(
            {
                f".cursor/agents/{_agent_name(name)}.md": _render_native_agent(
                    content, name, "Cursor"
                )
                for name, content in prompts.items()
            }
        )
        expected[".cursor/rules/project-workflow.mdc"] = resources[
            "project_workflow/cursor/rules/project-workflow.mdc"
        ]
    else:
        raise RuntimeError(f"unsupported agent for parity verification: {agent}")

    expected = {
        relative: _generated_bytes(relative, content) for relative, content in expected.items()
    }
    manifest: dict[str, str] = {}
    for relative, content in sorted(expected.items()):
        target = path / relative
        if not target.is_file() or target.read_bytes() != content:
            raise RuntimeError(f"generated asset differs from wheel resource: {agent}:{relative}")
        manifest[relative] = sha256_bytes(content)

    host_guidance = path / ("AGENTS.md" if agent == "codex" else ".github/copilot-instructions.md")
    if agent in {"codex", "github-copilot"}:
        guidance = host_guidance.read_text(encoding="utf-8")
        for phrase in (
            "one- or two-sentence plain-language Intent",
            "approval-summary",
            "meaning accurately reflects",
        ):
            if phrase not in guidance:
                raise RuntimeError(f"generated {agent} guidance lacks intent contract: {phrase}")
        manifest[host_guidance.relative_to(path).as_posix()] = sha256_path(host_guidance)

    return {
        "asset_count": len(manifest),
        "manifest": manifest,
        "manifest_sha256": sha256_json(manifest),
    }


def initialize_git(path: Path, env: dict[str, str]) -> None:
    run(["git", "init", "-q"], path, env)
    run(["git", "config", "user.email", "release-verifier@example.invalid"], path, env)
    run(["git", "config", "user.name", "Release Verifier"], path, env)


def commit_all(path: Path, env: dict[str, str]) -> None:
    run(["git", "add", "."], path, env)
    run(["git", "commit", "-qm", "verification fixture"], path, env)


def verify_manifest(path: Path, version: str) -> None:
    manifest = json.loads((path / ".project-workflow/manifest.json").read_text())
    if manifest["package_version"] != version:
        raise RuntimeError(f"manifest version mismatch in {path}")


def verify_delegate_asset(path: Path, agent: str) -> None:
    if agent == "codex":
        delegate = path / ".agents/skills/project-delegate/SKILL.md"
    elif agent == "github-copilot":
        delegate = path / ".github/prompts/Delegate.prompt.md"
    elif agent == "claude-code":
        delegate = path / ".claude/agents/project-delegate.md"
    else:
        delegate = path / ".cursor/agents/project-delegate.md"
    text = delegate.read_text()
    required = (
        "Task or Epic",
        "verified",
        "unsupported",
        "unknown",
        "available child",
        "coordinator",
        "descendants",
        "independent QA",
    )
    missing = [item for item in required if item.lower() not in text.lower()]
    if missing:
        raise RuntimeError(f"Delegate asset is incomplete for {agent}: {missing}")
    if agent in {"claude-code", "cursor"} and "${input:" in text:
        raise RuntimeError(f"Copilot placeholder leaked into {agent} Delegate asset")


def verify_coordinator_asset(path: Path, agent: str) -> None:
    if agent == "codex":
        coordinator = path / ".agents/skills/project-coordinator/SKILL.md"
    elif agent == "github-copilot":
        coordinator = path / ".github/prompts/Coordinator.prompt.md"
    elif agent == "claude-code":
        coordinator = path / ".claude/agents/project-coordinator.md"
    else:
        coordinator = path / ".cursor/agents/project-coordinator.md"
    text = coordinator.read_text()
    required = (
        "owner-facing",
        "one logical Coordinator",
        "smallest sufficient",
        "bounded packets",
        "Clarify",
        "drift-detected",
        "independent QA",
        "Stop after sufficient proof",
    )
    normalized = " ".join(text.split()).lower()
    missing = [item for item in required if item.lower() not in normalized]
    if missing:
        raise RuntimeError(f"Coordinator asset is incomplete for {agent}: {missing}")
    if agent in {"claude-code", "cursor"} and "${input:" in text:
        raise RuntimeError(f"Copilot placeholder leaked into {agent} Coordinator asset")


def verify_intent_assets(path: Path, agent: str) -> str:
    helper = path / ".project-workflow/cli/workflow.py"
    helper_text = helper.read_text(encoding="utf-8")
    for required in (
        "intent-audit",
        "user-outcome-journey",
        "Intent QA contract: adversarial",
        "Could every AC pass while the approved user job remains undone",
    ):
        if required not in helper_text:
            raise RuntimeError(f"packaged helper lacks intent control: {required}")
    requirements_paths = {
        "codex": ".agents/skills/project-requirements/SKILL.md",
        "github-copilot": ".github/prompts/Requirements.prompt.md",
        "claude-code": ".claude/agents/project-requirements.md",
        "cursor": ".cursor/agents/project-requirements.md",
    }
    requirements_skill = path / requirements_paths[agent]
    skill_text = requirements_skill.read_text(encoding="utf-8")
    for required in ("owner confirmation", "Intent Spine", "successful-but-wrong result"):
        if required not in skill_text:
            raise RuntimeError(f"packaged requirements skill lacks intent guidance: {required}")
    return sha256_path(helper)


def parent_requirements() -> str:
    return """# Requirements

## Summary

- Task: EPIC-001
- Title: Prove Export Journey
- Intent contract: full

## Intent

Enable a member to export and open a complete account archive through the ordinary settings route.

## Intent Spine

- OC1 — Completion capability: A member can export and open the archive.
- OC2 — Material capabilities: The ordinary route creates a complete archive.
- OC3 — Success journey: A signed-in member exports and opens the archive.
- OC4 — Successful-but-wrong result: A green preview omits the actual archive.
- OC5 — Exclusions: Do not redesign settings or add export formats.
- OC6 — Assumptions: The disposable repository models the workflow contract.
- OC7 — Authority source: The owner-approved Intent in this file.

## Owner Approval

- Intent reviewed and accurately reflected: No
- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Not approved
- Approval date: Not approved
- Approval note / source: Not approved
- Approved artifact identity: Not approved

## Goal

Prove a complete normal export journey.

## Non-Goals

- Do not redesign settings or add formats.

## Users & Context

- Signed-in members need portable account data.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Preserve the complete export journey and reject preview-only evidence.

## Acceptance Criteria (Verifiable)

- AC1: A member exports and opens the complete archive through the ordinary settings route.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- A preview is not completion.

## Validation Plan

- Exercise the normal journey and inspect the archive result.
"""


def epic_contract() -> str:
    return """# Epic Contract

## Summary

- Epic: EPIC-001
- Title: Prove Export Journey

## Sources of Truth

- Owner-approved Intent and AC1.

## Invalid Substitutes

- A green preview or test without a complete opened archive.

## Invariants

- The ordinary export route and complete archive remain required.

## Artifact Targets

- A child implementation and outcome receipt.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-001 | Normal export journey receipt and adversarial QA. |
"""


def child_requirements() -> str:
    return """# Requirements

## Summary

- Task: TASK-001
- Title: Deliver Complete Export Journey
- Parent AC Coverage: AC1
- Intent contract: full

## Intent

Deliver the parent-approved ordinary export journey and prove that the resulting complete archive
can be opened. A preview or internal success flag is not completion.

## Intent Spine

- OC1 — Completion capability: A member can export and open the archive.
- OC2 — Material capabilities: The normal route creates the complete archive.
- OC3 — Success journey: A signed-in member exports and opens the result.
- OC4 — Successful-but-wrong result: All tasks pass but only a preview exists.
- OC5 — Exclusions: Do not redesign settings or add formats.
- OC6 — Assumptions: This is a disposable exact-package workflow journey.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Child Charter

### Inherited Invariants

- The ordinary export route and complete archive remain required.

### Invalid Substitutes

- A green preview or test without a complete opened archive.

### Artifact Targets

- A child implementation and outcome receipt.

### Parent AC Proof Ownership

- AC1: owner `TASK-001`; required evidence: Normal export journey receipt and adversarial QA.

## Goal

Complete and prove the normal member export journey.

## Non-Goals

- Do not redesign settings or add formats.

## Users & Context

- Signed-in members need portable account data.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- The complete archive is created and opened through the ordinary route.

## Acceptance Criteria (Verifiable)

- AC1: A `user-outcome-journey` proves the member exports and opens the complete archive.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- Preview-only evidence is invalid.

## Validation Plan

- Exercise the normal route and inspect the opened archive.
"""


def child_implementation() -> str:
    return """# Implementation

## User Story

As a signed-in member, I want to export and open my complete archive, so that my account data is portable.

## Parent AC Coverage

- AC1

## Child Charter

### Inherited Invariants

- The ordinary export route and complete archive remain required.

### Invalid Substitutes

- A green preview or test without a complete opened archive.

### Artifact Targets

- A child implementation and outcome receipt.

### Parent AC Proof Ownership

- AC1: owner `TASK-001`; required evidence: Normal export journey receipt and adversarial QA.

## Acceptance Criteria

- [x] AC1: The normal export route creates a complete archive that the member opens.

## Validation

- AC1 / parent AC1: `user-outcome-journey` receipt binds the normal route to the opened archive.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | disposable exact-package repository | Normal route and outcome receipt pass | Local disposable proof only | Child-local structured evidence and opened archive receipt |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Deliver Export | Preserve the complete normal export journey. | AC1 / parent AC1 | Open the exported archive. | Done | | child artifacts | No | bounded-return |

## Parent AC Evidence

- AC1: The normal settings route produced the complete archive and the member opened it; see `EVIDENCE.json` and `evidence/export-journey.txt`.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Outcome journey evidence: The child-local record exercises the normal export and open journey.
- Reviewer independence: The packaged lifecycle gate evaluates the separately authored audit and structured receipt.
- Evidence: Exact-package commands, audit, structured record and outcome artifact.
- Findings: The preview-only candidate was rejected before readiness.

## Retro

- Reusable lessons: Exact outcome proof prevents preview substitution.
- Conventions or agent assets updated: None in the disposable repository.
- Follow-up tasks: None.
"""


def green_but_wrong_implementation() -> str:
    """Return an internally green child that silently narrows archive export to a preview."""
    return (
        child_implementation()
        .replace(
            "As a signed-in member, I want to export and open my complete archive, so that my account data is portable.",
            "As a signed-in member, I want to preview my account export before leaving Settings.",
        )
        .replace(
            "- [x] AC1: The normal export route creates a complete archive that the member opens.",
            "- [x] AC1: The normal export route shows a successful export preview.",
        )
        .replace(
            "- AC1 / parent AC1: `user-outcome-journey` receipt binds the normal route to the opened archive.",
            "- AC1 / parent AC1: `user-outcome-journey` receipt binds the normal route to the preview.",
        )
        .replace(
            "Normal route and outcome receipt pass",
            "Preview route and outcome receipt pass",
        )
        .replace(
            "- AC1: The normal settings route produced the complete archive and the member opened it; see `EVIDENCE.json` and `evidence/export-journey.txt`.",
            "- AC1: The normal settings route produced an export preview; see `EVIDENCE.json` and `evidence/export-preview.txt`.",
        )
        .replace(
            "- Outcome journey evidence: The child-local record exercises the normal export and open journey.",
            "- Outcome journey evidence: The child-local record exercises the export preview journey.",
        )
        .replace(
            "- Findings: The preview-only candidate was rejected before readiness.",
            "- Findings: None; the preview and internal success flag are green.",
        )
    )


def write_outcome_evidence(child_dir: Path) -> None:
    implementation_path = child_dir / "IMPLEMENTATION.md"
    artifact_path = child_dir / "evidence/export-journey.txt"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(
        "A signed-in member opened Settings, selected Export, received the complete account "
        "archive, and opened the archive successfully.\n",
        encoding="utf-8",
    )
    source_revision = sha256_path(implementation_path)
    artifact_hash = sha256_path(artifact_path)
    record = {
        "task_id": "TASK-001",
        "claims": [
            {
                "id": "CLM-001",
                "recipe": "user-outcome-journey",
                "status": "pass",
                "commit": "disposable-exact-package-candidate",
                "timestamp": "2026-08-21T00:00:00Z",
                "parent_ac": "AC1",
                "claim": "A member exports and opens the complete account archive.",
                "claim_scope": "member export and open of complete account archive",
                "journey_scope": "member export and open of complete account archive",
                "actor": "Signed-in member",
                "normal_entry_point": "Account settings > Export",
                "starting_state": "The member has account data available for export.",
                "material_operations": [
                    "Open account settings",
                    "Select Export",
                    "Receive the complete archive",
                    "Open the archive",
                ],
                "resulting_state_or_artifact": "The complete account archive is open.",
                "outcome_observations": [
                    "The ordinary settings route produced the archive.",
                    "The member opened the complete archive.",
                ],
                "source_artifact": "IMPLEMENTATION.md",
                "source_revision": source_revision,
                "artifact_identity": "implementation-" + source_revision.removeprefix("sha256:"),
                "environment": "Disposable exact-package repository normal workflow",
                "invalid_substitute_policy": [
                    "builds",
                    "canary",
                    "debug-only",
                    "internal-data",
                    "related-environment",
                    "screenshots",
                    "tests",
                ],
                "invalid_substitutes": [],
                "owner_acceptance_required": False,
                "owner_acceptance_status": "not-required",
                "evidence_artifact": "evidence/export-journey.txt",
                "evidence_artifact_hash": artifact_hash,
            }
        ],
    }
    (child_dir / "EVIDENCE.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_preview_evidence(child_dir: Path) -> None:
    implementation_path = child_dir / "IMPLEMENTATION.md"
    artifact_path = child_dir / "evidence/export-preview.txt"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(
        "A signed-in member opened Settings, selected Export, and saw a green preview with an "
        "internal success flag. No archive was created or opened.\n",
        encoding="utf-8",
    )
    source_revision = sha256_path(implementation_path)
    record = {
        "task_id": "TASK-001",
        "claims": [
            {
                "id": "CLM-001",
                "recipe": "user-outcome-journey",
                "status": "pass",
                "commit": "disposable-exact-package-candidate",
                "timestamp": "2026-08-21T00:00:00Z",
                "parent_ac": "AC1",
                "claim": "A member sees a successful account export preview.",
                "claim_scope": "member export preview in account settings",
                "journey_scope": "member export preview in account settings",
                "actor": "Signed-in member",
                "normal_entry_point": "Account settings > Export",
                "starting_state": "The member has account data available for export.",
                "material_operations": [
                    "Open account settings",
                    "Select Export",
                    "Observe the preview and internal success flag",
                ],
                "resulting_state_or_artifact": "A green export preview is visible; no archive exists.",
                "outcome_observations": [
                    "The ordinary settings route displayed a preview.",
                    "The implementation reported internal success without an archive.",
                ],
                "source_artifact": "IMPLEMENTATION.md",
                "source_revision": source_revision,
                "artifact_identity": "implementation-" + source_revision.removeprefix("sha256:"),
                "environment": "Disposable exact-package repository normal workflow",
                "invalid_substitute_policy": [
                    "builds",
                    "canary",
                    "debug-only",
                    "internal-data",
                    "related-environment",
                    "screenshots",
                    "tests",
                ],
                "invalid_substitutes": [],
                "owner_acceptance_required": False,
                "owner_acceptance_status": "not-required",
                "evidence_artifact": "evidence/export-preview.txt",
                "evidence_artifact_hash": sha256_path(artifact_path),
            }
        ],
    }
    (child_dir / "EVIDENCE.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def review_export_intent_alignment(epic_dir: Path) -> dict[str, Any]:
    """Review actual child proof fields against the parent's required export capability."""
    child_dir = next(epic_dir.glob("TASK-001-*"))
    evidence_path = child_dir / "EVIDENCE.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    claim = evidence["claims"][0]
    evidence_artifact = child_dir / claim["evidence_artifact"]
    reviewed_fields = {
        "claim": claim["claim"],
        "journey_scope": claim["journey_scope"],
        "normal_entry_point": claim["normal_entry_point"],
        "material_operations": claim["material_operations"],
        "resulting_state_or_artifact": claim["resulting_state_or_artifact"],
        "outcome_observations": claim["outcome_observations"],
        "evidence_artifact_text": evidence_artifact.read_text(encoding="utf-8").strip(),
    }
    proof_text = json.dumps(reviewed_fields, sort_keys=True).lower()
    archive_created = "complete account archive" in proof_text or "complete archive" in proof_text
    archive_opened = bool(
        re.search(r"\bopen(?:ed)?\b[^.]{0,100}\barchive\b", proof_text)
        or re.search(r"\barchive\b[^.]{0,100}\bopen(?:ed)?\b", proof_text)
    )
    denied_archive = bool(
        re.search(r"\bno archive\b[^.]{0,100}\b(?:created|opened|exists)\b", proof_text)
        or re.search(r"\barchive\b[^.]{0,100}\b(?:not|never)\b[^.]{0,50}\bopened\b", proof_text)
    )
    archive_opened = archive_opened and not denied_archive
    normal_route = "account settings" in proof_text and "export" in proof_text
    preserved = archive_created and archive_opened and normal_route
    review = {
        "schema_version": 1,
        "reviewer": "Sourced outcome-alignment reviewer v1",
        "review_scope": "Parent complete archive capability versus actual child outcome fields",
        "parent_capability": (
            "A signed-in member exports and opens the complete account archive through the "
            "ordinary settings route."
        ),
        "classification": "preserved" if preserved else "proxy",
        "lost_capability": ""
        if preserved
        else "The member cannot open the complete exported archive.",
        "checks": {
            "complete_archive_created": archive_created,
            "complete_archive_opened": archive_opened,
            "ordinary_settings_route": normal_route,
        },
        "reviewed_fields": reviewed_fields,
        "sources": {
            "parent_requirements_sha256": sha256_path(epic_dir / "REQUIREMENTS.md"),
            "child_requirements_sha256": sha256_path(child_dir / "REQUIREMENTS.md"),
            "child_implementation_sha256": sha256_path(child_dir / "IMPLEMENTATION.md"),
            "child_evidence_sha256": sha256_path(evidence_path),
            "outcome_artifact_sha256": sha256_path(evidence_artifact),
        },
    }
    review_path = child_dir / "evidence/intent-alignment-review.json"
    review_path.write_text(json.dumps(review, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    review["review_artifact"] = review_path.relative_to(epic_dir).as_posix()
    review["review_artifact_sha256"] = sha256_path(review_path)
    return review


def write_intent_audit_from_review(
    epic_dir: Path,
    command: list[str],
    env: dict[str, str],
    *,
    review: dict[str, Any],
) -> dict[str, Any]:
    classification = str(review["classification"])
    audit_path = epic_dir / "INTENT-AUDIT.json"
    evaluation = json.loads(
        run(
            command + ["epic", "intent-audit", "--epic-id", "EPIC-001", "--format", "json"],
            epic_dir.parents[2],
            env,
        )
    )
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload.update(
        {
            "artifact_identity": evaluation["current_identity"],
            "reviewed_by": str(review["reviewer"]),
            "reviewed_at": "2026-08-21",
            "review_source": (
                f"{review['review_artifact']} ({review['review_artifact_sha256']}); sourced review "
                "of parent Intent and actual child outcome fields."
            ),
            "verdict": "changes-requested" if classification == "proxy" else "pass",
        }
    )
    child_rel = next(epic_dir.glob("TASK-001-*")).name
    for record in payload["commitments"]:
        record.update(
            {
                "classification": classification if record["id"] == "OC3" else "preserved",
                "parent_acs": ["AC1"],
                "child_owners": ["TASK-001"],
                "required_outcome_proof": "Run the normal export route and open the complete archive.",
                "target_locations": [f"{child_rel}/IMPLEMENTATION.md#parent-ac-evidence"],
                "user_visible_consequence": (
                    "The member can export and open the complete archive through the ordinary route."
                    if record["id"] != "OC3" or classification != "proxy"
                    else "The member sees a green preview but cannot open the complete exported archive."
                ),
                "lost_capability": (
                    str(review["lost_capability"])
                    if record["id"] == "OC3" and classification == "proxy"
                    else ""
                ),
                "amendment": None,
            }
        )
    audit_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def verify_exact_package_intent_journey(
    path: Path, command: list[str], env: dict[str, str]
) -> dict[str, Any]:
    run(command + ["epic", "init", "--title", "Prove Export Journey"], path, env)
    epic_dir = path / ".project-workflow/tasks/EPIC-001-Prove-Export-Journey"
    (epic_dir / "REQUIREMENTS.md").write_text(parent_requirements(), encoding="utf-8")
    (epic_dir / "EPIC-CONTRACT.md").write_text(epic_contract(), encoding="utf-8")
    synopsis = run(command + ["epic", "approval-summary", "--epic-id", "EPIC-001"], path, env)
    if not synopsis.startswith("Approval synopsis\n\nIntent\n") or "AC1" in synopsis:
        raise RuntimeError("packaged approval synopsis did not keep meaning ahead of IDs")
    run(
        command
        + [
            "epic",
            "approve-requirements",
            "--epic-id",
            "EPIC-001",
            "--approved-by",
            "Disposable Owner",
            "--source",
            "Disposable owner confirmed the displayed Intent.",
        ],
        path,
        env,
    )
    run(command + ["epic", "ready", "--epic-id", "EPIC-001"], path, env)
    run(command + ["epic", "decompose", "--epic-id", "EPIC-001", "--limit", "1"], path, env)
    run(command + ["epic", "approve", "--epic-id", "EPIC-001", "--id", "TASK-001"], path, env)
    run(
        command + ["epic", "scaffold-child", "--epic-id", "EPIC-001", "--id", "TASK-001"], path, env
    )
    child_dir = next(epic_dir.glob("TASK-001-*"))
    (child_dir / "REQUIREMENTS.md").write_text(child_requirements(), encoding="utf-8")
    (child_dir / "IMPLEMENTATION.md").write_text(green_but_wrong_implementation(), encoding="utf-8")
    write_preview_evidence(child_dir)

    proxy_review = review_export_intent_alignment(epic_dir)
    if proxy_review["classification"] != "proxy" or all(proxy_review["checks"].values()):
        raise RuntimeError("sourced reviewer did not detect the actual preview-only child")
    proxy_audit = write_intent_audit_from_review(epic_dir, command, env, review=proxy_review)
    rejected = run_result(
        command + ["epic", "ready-child", "--epic-id", "EPIC-001", "--id", "TASK-001"],
        path,
        env,
    )
    if rejected.returncode == 0:
        raise RuntimeError("green-but-wrong child unexpectedly passed intent readiness")
    if (
        "changes-requested" not in rejected.stdout
        or "complete exported archive" not in rejected.stdout
    ):
        raise RuntimeError(
            "proxy rejection did not name classification and lost capability:\n" + rejected.stdout
        )

    proxy_child = {
        "implementation_sha256": sha256_path(child_dir / "IMPLEMENTATION.md"),
        "evidence_sha256": sha256_path(child_dir / "EVIDENCE.json"),
        "review_sha256": proxy_review["review_artifact_sha256"],
        "review_checks": proxy_review["checks"],
        "audit_identity": proxy_audit["artifact_identity"],
    }
    (child_dir / "IMPLEMENTATION.md").write_text(child_implementation(), encoding="utf-8")
    write_outcome_evidence(child_dir)
    passing_review = review_export_intent_alignment(epic_dir)
    if passing_review["classification"] != "preserved" or not all(
        passing_review["checks"].values()
    ):
        raise RuntimeError("sourced reviewer did not recognize the restored complete journey")
    passing_audit = write_intent_audit_from_review(epic_dir, command, env, review=passing_review)
    run(command + ["epic", "ready-child", "--epic-id", "EPIC-001", "--id", "TASK-001"], path, env)
    run(command + ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "In Progress"], path, env)
    for status in ("Testing", "Review", "Complete"):
        run(
            command
            + ["epic", "status", "--epic-id", "EPIC-001", "--id", "TASK-001", "--to", status],
            path,
            env,
        )
    audit_output = run(command + ["epic", "audit", "--epic-id", "EPIC-001"], path, env)
    if "acceptance audit passed" not in audit_output.lower():
        raise RuntimeError("packaged Epic acceptance audit did not pass")
    (epic_dir / "RETRO.md").write_text(
        "# Epic Retro\n\n## Lessons\n\nExact outcome evidence rejected the preview proxy.\n\n"
        "## Follow-up Tasks\n\nNone.\n\n## Deferrals\n\nNone.\n\n"
        "## Missed In-Scope Work\n\nNone.\n",
        encoding="utf-8",
    )
    run(command + ["epic", "lifecycle", "--epic-id", "EPIC-001", "--to", "Closeout"], path, env)
    closeout = run(command + ["epic", "closeout", "--epic-id", "EPIC-001", "--complete"], path, env)
    if "complete" not in closeout.lower():
        raise RuntimeError("packaged Epic did not reach complete")
    return {
        "approval_synopsis_sha256": "sha256:" + hashlib.sha256(synopsis.encode()).hexdigest(),
        "audit_identity": passing_audit["artifact_identity"],
        "green_but_wrong_child": proxy_child,
        "proxy_rejection": rejected.stdout.strip().splitlines(),
        "restored_review_sha256": passing_review["review_artifact_sha256"],
        "outcome_evidence_sha256": sha256_path(child_dir / "EVIDENCE.json"),
        "acceptance_audit_sha256": sha256_path(epic_dir / "ACCEPTANCE-AUDIT.md"),
        "global_tracker_sha256": sha256_path(path / ".project-workflow/TRACKER.md"),
        "final_status": "Complete",
        "authority_boundary": "Local exact-package proof only; not published, released, rolled out or adopted.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="package_source", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    uvx = shutil.which("uvx") or "/opt/homebrew/bin/uvx"
    if not Path(uvx).is_file():
        raise RuntimeError("uvx is required")
    env = os.environ.copy()
    env["UV_CACHE_DIR"] = env.get("UV_CACHE_DIR", "/tmp/project-workflow-release-uv-cache")
    env["UV_TOOL_DIR"] = env.get("UV_TOOL_DIR", "/tmp/project-workflow-release-uv-tools")
    env["UV_TOOL_BIN_DIR"] = env.get("UV_TOOL_BIN_DIR", "/tmp/project-workflow-release-uv-tool-bin")
    package_path = Path(args.package_source).resolve()
    command = [uvx, "--from", str(package_path), "project"]
    package_parity = verify_package_source_parity(package_path)
    wheel_resources = _wheel_resources(package_path)
    evidence: dict[str, Any] = {
        "version": args.version,
        "source": package_path.name,
        "source_sha256": sha256_path(package_path),
        "package_parity": package_parity,
    }

    with tempfile.TemporaryDirectory(prefix="project-workflow-journey-") as temp:
        temp_path = Path(temp)
        fresh_evidence: dict[str, Any] = {}
        for agent in ("codex", "github-copilot", "claude-code", "cursor"):
            fresh = temp_path / f"fresh-{agent}"
            fresh.mkdir()
            initialize_git(fresh, env)
            init_output = run(command + ["init", "--agent", agent], fresh, env)
            verify_manifest(fresh, args.version)
            verify_delegate_asset(fresh, agent)
            verify_coordinator_asset(fresh, agent)
            intent_helper_sha256 = verify_intent_assets(fresh, agent)
            generated_parity = verify_generated_asset_parity(fresh, agent, wheel_resources)
            version_output = run(command + ["--version"], fresh, env).strip()
            if version_output != f"project {args.version}":
                raise RuntimeError(f"runtime version mismatch: {version_output}")
            doctor_output = run(
                [str(fresh / ".project-workflow/cli/workflow"), "doctor"], fresh, env
            )
            commit_all(fresh, env)
            upgrade_output = run(command + ["upgrade", "--agent", agent, "--yes"], fresh, env)
            verify_manifest(fresh, args.version)
            verify_delegate_asset(fresh, agent)
            verify_coordinator_asset(fresh, agent)
            fresh_evidence[agent] = {
                "init": init_output.strip().splitlines()[-1],
                "doctor": doctor_output.strip().splitlines()[-1],
                "upgrade": upgrade_output.strip().splitlines()[-1],
                "intent_helper_sha256": intent_helper_sha256,
                "generated_asset_parity": generated_parity,
            }
            if agent == "codex":
                fresh_evidence[agent]["intent_journey"] = verify_exact_package_intent_journey(
                    fresh, command, env
                )

        legacy = temp_path / "legacy"
        shutil.copytree(ROOT / "tests/fixtures/legacy-unversioned", legacy)
        legacy_delegate = legacy / ".agents/skills/project-delegate/SKILL.md"
        legacy_delegate.parent.mkdir(parents=True)
        owner_delegate = b"# Owner Delegate Contract\n\nPreserve these exact bytes.\n"
        legacy_delegate.write_bytes(owner_delegate)
        initialize_git(legacy, env)
        commit_all(legacy, env)
        preserved_paths = (
            ".project-workflow/TRACKER.md",
            ".project-workflow/BACKLOG.md",
            ".project-workflow/guidance.md",
            "USER-NOTES.md",
        )
        preserved_before = {
            relative: sha256_path(legacy / relative) for relative in preserved_paths
        }
        legacy_plan = json.loads(
            run(
                command + ["upgrade", "--agent", "codex", "--plan", "--format", "json"],
                legacy,
                env,
            )
        )
        legacy_apply = json.loads(
            run(
                command
                + [
                    "upgrade",
                    "--agent",
                    "codex",
                    "--apply",
                    "--plan-fingerprint",
                    legacy_plan["plan_fingerprint"],
                    "--format",
                    "json",
                ],
                legacy,
                env,
            )
        )
        preserved_after = {relative: sha256_path(legacy / relative) for relative in preserved_paths}
        if preserved_before != preserved_after:
            raise RuntimeError(
                "legacy upgrade changed historical tracker, backlog, guidance or notes"
            )
        no_op_plan = json.loads(
            run(
                command + ["upgrade", "--agent", "codex", "--plan", "--format", "json"],
                legacy,
                env,
            )
        )
        verify_manifest(legacy, args.version)
        if legacy_delegate.read_bytes() != owner_delegate:
            raise RuntimeError("legacy upgrade overwrote the user-owned Delegate collision")
        pending_delegate = legacy_delegate.with_name("SKILL.md.new")
        if not pending_delegate.is_file():
            raise RuntimeError("legacy upgrade did not retain the generated Delegate .new file")
        pending_text = pending_delegate.read_text()
        if "Task or Epic" not in pending_text or "verified" not in pending_text:
            raise RuntimeError("legacy pending Delegate asset lacks the current semantic contract")
        legacy_doctor = run([str(legacy / ".project-workflow/cli/workflow"), "doctor"], legacy, env)

        evidence.update(
            {
                "fresh": fresh_evidence,
                "legacy": {
                    "plan_fingerprint": legacy_plan["plan_fingerprint"],
                    "apply_status": legacy_apply["status"],
                    "second_plan_repository_state": no_op_plan["repository_state"],
                    "doctor": legacy_doctor.strip().splitlines()[-1],
                    "owner_collision_preserved": True,
                    "owner_sha256": hashlib.sha256(owner_delegate).hexdigest(),
                    "pending_delegate_sha256": hashlib.sha256(
                        pending_delegate.read_bytes()
                    ).hexdigest(),
                    "historical_artifacts_preserved": preserved_after,
                },
            }
        )

    rendered = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
