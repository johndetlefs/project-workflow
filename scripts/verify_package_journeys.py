#!/usr/bin/env python3
"""Exercise packaged init and upgrade behavior in disposable repositories."""

from __future__ import annotations

import argparse
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
        fresh = temp_path / "fresh"
        fresh.mkdir()
        initialize_git(fresh, env)
        init_output = run(command + ["init", "--agent", "codex"], fresh, env)
        verify_manifest(fresh, args.version)
        version_output = run(command + ["--version"], fresh, env).strip()
        if version_output != f"project {args.version}":
            raise RuntimeError(f"runtime version mismatch: {version_output}")
        doctor_output = run([str(fresh / ".project-workflow/cli/workflow"), "doctor"], fresh, env)
        commit_all(fresh, env)
        upgrade_output = run(command + ["upgrade", "--agent", "codex", "--yes"], fresh, env)
        verify_manifest(fresh, args.version)

        legacy = temp_path / "legacy"
        shutil.copytree(ROOT / "tests/fixtures/legacy-unversioned", legacy)
        initialize_git(legacy, env)
        commit_all(legacy, env)
        legacy_output = run(command + ["upgrade", "--agent", "codex", "--yes"], legacy, env)
        verify_manifest(legacy, args.version)
        legacy_doctor = run([str(legacy / ".project-workflow/cli/workflow"), "doctor"], legacy, env)

        evidence.update(
            {
                "fresh": {
                    "init": init_output.strip().splitlines()[-1],
                    "doctor": doctor_output.strip().splitlines()[-1],
                    "upgrade": upgrade_output.strip().splitlines()[-1],
                },
                "legacy": {
                    "upgrade": legacy_output.strip().splitlines()[-1],
                    "doctor": legacy_doctor.strip().splitlines()[-1],
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
