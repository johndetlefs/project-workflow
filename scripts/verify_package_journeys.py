#!/usr/bin/env python3
"""Exercise packaged init and upgrade behavior in disposable repositories."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


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
    env["UV_TOOL_BIN_DIR"] = env.get(
        "UV_TOOL_BIN_DIR", "/tmp/project-workflow-release-uv-tool-bin"
    )
    command = [uvx, "--from", args.package_source, "project"]
    evidence: dict[str, Any] = {"version": args.version, "source": args.package_source}

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
            version_output = run(command + ["--version"], fresh, env).strip()
            if version_output != f"project {args.version}":
                raise RuntimeError(f"runtime version mismatch: {version_output}")
            doctor_output = run(
                [str(fresh / ".project-workflow/cli/workflow"), "doctor"], fresh, env
            )
            commit_all(fresh, env)
            upgrade_output = run(
                command + ["upgrade", "--agent", agent, "--yes"], fresh, env
            )
            verify_manifest(fresh, args.version)
            verify_delegate_asset(fresh, agent)
            fresh_evidence[agent] = {
                "init": init_output.strip().splitlines()[-1],
                "doctor": doctor_output.strip().splitlines()[-1],
                "upgrade": upgrade_output.strip().splitlines()[-1],
            }

        legacy = temp_path / "legacy"
        shutil.copytree(ROOT / "tests/fixtures/legacy-unversioned", legacy)
        legacy_delegate = legacy / ".agents/skills/project-delegate/SKILL.md"
        legacy_delegate.parent.mkdir(parents=True)
        owner_delegate = b"# Owner Delegate Contract\n\nPreserve these exact bytes.\n"
        legacy_delegate.write_bytes(owner_delegate)
        initialize_git(legacy, env)
        commit_all(legacy, env)
        legacy_output = run(command + ["upgrade", "--agent", "codex", "--yes"], legacy, env)
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
                    "upgrade": legacy_output.strip().splitlines()[-1],
                    "doctor": legacy_doctor.strip().splitlines()[-1],
                    "owner_collision_preserved": True,
                    "owner_sha256": hashlib.sha256(owner_delegate).hexdigest(),
                    "pending_delegate_sha256": hashlib.sha256(
                        pending_delegate.read_bytes()
                    ).hexdigest(),
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
