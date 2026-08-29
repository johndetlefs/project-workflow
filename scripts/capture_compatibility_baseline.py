#!/usr/bin/env python3
"""Capture the released Project Workflow CLI compatibility surface."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from project_workflow import cli

ROOT = Path(__file__).resolve().parents[1]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parser_surface(parser: argparse.ArgumentParser) -> dict[str, object]:
    options = []
    subcommands: dict[str, object] = {}
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subcommands = {
                name: parser_surface(child) for name, child in sorted(action.choices.items())
            }
            continue
        if action.dest == "help":
            continue
        options.append(
            {
                "choices": list(action.choices) if action.choices is not None else None,
                "dest": action.dest,
                "nargs": action.nargs,
                "option_strings": list(action.option_strings),
                "required": bool(action.required),
            }
        )
    return {
        "options": sorted(options, key=lambda item: (item["dest"], item["option_strings"])),
        "subcommands": subcommands,
    }


def generated_paths() -> list[str]:
    roots = [
        ROOT / ".project-workflow/cli",
        ROOT / ".agents/skills",
        ROOT / ".github/prompts",
    ]
    paths = []
    for base in roots:
        if not base.exists():
            continue
        paths.extend(
            path.relative_to(ROOT).as_posix()
            for path in base.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix not in {".pyc", ".pyo"}
        )
    return sorted(paths)


def git_value(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def payload() -> dict[str, object]:
    template = ROOT / "src/project_workflow/templates/workflow.py"
    mirror = ROOT / ".project-workflow/cli/workflow.py"
    return {
        "schema_version": 1,
        "baseline": {
            "version": "0.9.0",
            "commit": "86ca8859eb5e331db2505c2ae7230e2bc0030242",
            "tag": "v0.9.0",
            "released_test_count": 548,
            "public_wheel_sha256": "9e30c52fb70c8d5e86e173a2e5da6566a7f68f2a450718d6c28f25996bb0d82b",
        },
        "captured_from": {
            "branch": git_value("branch", "--show-current"),
            "head": git_value("rev-parse", "HEAD"),
            "source_cli_sha256": file_sha256(ROOT / "src/project_workflow/cli.py"),
            "template_sha256": file_sha256(template),
            "installed_mirror_sha256": file_sha256(mirror),
        },
        "contracts": {
            "package_version": cli.CURRENT_PACKAGE_VERSION,
            "asset_version": cli.CURRENT_ASSET_VERSION,
            "repository_schema_version": cli.CURRENT_SCHEMA_VERSION,
            "manifest_version": cli.CURRENT_MANIFEST_VERSION,
            "coordination_contract_version": cli.COORDINATION_CONTRACT_VERSION,
            "coordination_schema_version": cli.COORDINATION_SCHEMA_VERSION,
            "execution_control_schema_version": cli.EXECUTION_CONTROL_SCHEMA_VERSION,
            "doctor_output_schema_version": cli.DOCTOR_OUTPUT_SCHEMA_VERSION,
            "operational_status_schema_version": cli.OPERATIONAL_STATUS_SCHEMA_VERSION,
        },
        "command_surface": parser_surface(cli.build_parser()),
        "generated_paths": generated_paths(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
