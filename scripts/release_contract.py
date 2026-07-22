#!/usr/bin/env python3
"""Validate and record project-workflow release identities.

The tool intentionally uses only the standard library so that candidate checks
can run before development dependencies are installed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile
from email.parser import Parser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = ROOT / "src/project_workflow/_version.py"
MIRROR_PATHS = (
    ROOT / "src/project_workflow/cli.py",
    ROOT / "src/project_workflow/templates/workflow.py",
    ROOT / ".project-workflow/cli/workflow.py",
)
MANIFEST_PATH = ROOT / ".project-workflow/manifest.json"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
PINNED_COMMAND = "uvx --from project-workflow=={version} project {command}"
MUTABLE_COMMAND = "uvx --from git+https://github.com/johndetlefs/project-workflow.git"


class ContractError(RuntimeError):
    """A release identity or artifact violates the release contract."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_version() -> str:
    match = re.search(
        r'^__version__ = "([0-9]+\.[0-9]+\.[0-9]+)"$',
        VERSION_PATH.read_text(),
        re.MULTILINE,
    )
    if not match:
        raise ContractError(f"invalid authoritative version file: {VERSION_PATH}")
    return match.group(1)


def _git(*args: str) -> str:
    return subprocess.check_output(("git", *args), cwd=ROOT, text=True).strip()


def validate_source(*, expected_version: str | None, tag: str | None, clean: bool) -> str:
    version = source_version()
    if expected_version and expected_version != version:
        raise ContractError(f"expected version {expected_version}, source declares {version}")
    if tag and tag != f"v{version}":
        raise ContractError(f"tag {tag} does not match v{version}")

    mirror_bytes = MIRROR_PATHS[0].read_bytes()
    for path in MIRROR_PATHS:
        text = path.read_text()
        match = re.search(r'^CURRENT_PACKAGE_VERSION = "([^"]+)"$', text, re.MULTILINE)
        if not match or match.group(1) != version:
            raise ContractError(f"version mirror mismatch: {path}")
    for path in MIRROR_PATHS[1:]:
        if path.read_bytes() != mirror_bytes:
            raise ContractError(f"managed CLI mirror differs from {MIRROR_PATHS[0]}: {path}")

    manifest = json.loads(MANIFEST_PATH.read_text())
    if manifest.get("package_version") != version:
        raise ContractError("manifest package_version does not match source version")
    if f"## {version} -" not in CHANGELOG_PATH.read_text():
        raise ContractError(f"CHANGELOG.md has no {version} release heading")

    current_docs = (
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / ".project-workflow/cli/README.md",
        ROOT / "src/project_workflow/codex/AGENTS.md",
    )
    combined_docs = ""
    for path in current_docs:
        text = path.read_text()
        combined_docs += text
        if MUTABLE_COMMAND in text:
            raise ContractError(f"{path} contains mutable canonical release guidance")
    for command in ("init", "upgrade"):
        expected = PINNED_COMMAND.format(version=version, command=command)
        if expected not in combined_docs:
            raise ContractError(f"current documentation is missing canonical command: {expected}")

    lock_path = ROOT / "uv.lock"
    if not lock_path.is_file():
        raise ContractError("uv.lock is required")
    if clean and _git("status", "--porcelain"):
        raise ContractError("release candidate worktree is dirty")
    return version


def _metadata_from_wheel(path: Path) -> dict[str, str]:
    with zipfile.ZipFile(path) as archive:
        archive_names = set(archive.namelist())
        names = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(names) != 1:
            raise ContractError(f"wheel must contain one METADATA file: {path.name}")
        required_package_files = {
            "project_workflow/__init__.py",
            "project_workflow/_version.py",
            "project_workflow/cli.py",
            "project_workflow/templates/workflow",
            "project_workflow/templates/workflow.py",
            "project_workflow/codex/AGENTS.md",
            "project_workflow/codex/skills/project-task/SKILL.md",
        }
        missing = required_package_files - archive_names
        if missing:
            raise ContractError(f"wheel is missing required package data: {sorted(missing)}")
        entry_points = [
            name for name in archive_names if name.endswith(".dist-info/entry_points.txt")
        ]
        if len(entry_points) != 1 or "project = project_workflow.cli:main" not in archive.read(
            entry_points[0]
        ).decode():
            raise ContractError(f"wheel has invalid project CLI entry point: {path.name}")
        return dict(Parser().parsestr(archive.read(names[0]).decode()).items())


def _metadata_from_sdist(path: Path) -> dict[str, str]:
    with tarfile.open(path, "r:gz") as archive:
        members = [
            member
            for member in archive.getmembers()
            if member.name.endswith("/PKG-INFO") and member.name.count("/") == 1
        ]
        if len(members) != 1:
            raise ContractError(f"sdist must contain one PKG-INFO file: {path.name}")
        extracted = archive.extractfile(members[0])
        if extracted is None:
            raise ContractError(f"cannot read PKG-INFO: {path.name}")
        return dict(Parser().parsestr(extracted.read().decode()).items())


def distributions(dist: Path, version: str) -> list[dict[str, Any]]:
    wheels = sorted(dist.glob("*.whl"))
    sdists = sorted(dist.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ContractError("dist must contain exactly one wheel and one source distribution")
    result: list[dict[str, Any]] = []
    for kind, path, metadata in (
        ("wheel", wheels[0], _metadata_from_wheel(wheels[0])),
        ("sdist", sdists[0], _metadata_from_sdist(sdists[0])),
    ):
        if metadata.get("Name") != "project-workflow" or metadata.get("Version") != version:
            raise ContractError(f"artifact metadata mismatch: {path.name}")
        result.append(
            {
                "filename": path.name,
                "kind": kind,
                "sha256": sha256(path),
                "size": path.stat().st_size,
            }
        )
    return result


def write_receipt(args: argparse.Namespace) -> None:
    version = validate_source(expected_version=args.version, tag=args.tag, clean=args.clean)
    if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
        raise ContractError("commit must be a full 40-character lowercase Git SHA")
    artifacts = distributions(args.dist, version)
    manifest = json.loads(MANIFEST_PATH.read_text())
    changelog_heading = next(
        line for line in CHANGELOG_PATH.read_text().splitlines() if line.startswith(f"## {version} -")
    )
    receipt = {
        "schema_version": 1,
        "project": "project-workflow",
        "version": version,
        "tag": args.tag,
        "commit": args.commit,
        "asset_version": manifest["asset_version"],
        "repository_schema_version": manifest["schema_version"],
        "changelog_heading": changelog_heading,
        "commands": {
            "init": PINNED_COMMAND.format(version=version, command="init"),
            "upgrade": PINNED_COMMAND.format(version=version, command="upgrade"),
        },
        "repository": args.repository,
        "workflow": {
            "run_id": args.run_id,
            "run_url": args.run_url,
        },
        "artifacts": artifacts,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    receipt_path = args.output / "release-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    sums = "".join(f"{item['sha256']}  {item['filename']}\n" for item in artifacts)
    (args.output / "SHA256SUMS").write_text(sums)
    changelog = CHANGELOG_PATH.read_text()
    release_match = re.search(
        rf"^## {re.escape(version)} - [^\n]+\n(?P<body>.*?)(?=^## |\Z)",
        changelog,
        re.MULTILINE | re.DOTALL,
    )
    if not release_match:
        raise ContractError(f"cannot extract release notes for {version}")
    (args.output / "release-notes.md").write_text(
        f"# project-workflow {version}\n\n{release_match.group('body').strip()}\n"
    )
    print(receipt_path)


def verify_receipt(receipt_path: Path, dist: Path) -> None:
    receipt = json.loads(receipt_path.read_text())
    required = {
        "schema_version",
        "project",
        "version",
        "tag",
        "commit",
        "asset_version",
        "repository_schema_version",
        "changelog_heading",
        "commands",
        "repository",
        "workflow",
        "artifacts",
    }
    if set(receipt) != required or receipt["schema_version"] != 1:
        raise ContractError("receipt fields or schema version are invalid")
    version = receipt["version"]
    if receipt["project"] != "project-workflow" or receipt["tag"] != f"v{version}":
        raise ContractError("receipt project, version, and tag do not agree")
    if not re.fullmatch(r"[0-9a-f]{40}", receipt["commit"]):
        raise ContractError("receipt commit is not a full Git SHA")
    if receipt["commands"] != {
        "init": PINNED_COMMAND.format(version=version, command="init"),
        "upgrade": PINNED_COMMAND.format(version=version, command="upgrade"),
    }:
        raise ContractError("receipt canonical commands do not match its version")
    if not str(receipt["changelog_heading"]).startswith(f"## {version} -"):
        raise ContractError("receipt changelog heading does not match its version")
    if not all(receipt["workflow"].get(field) for field in ("run_id", "run_url")):
        raise ContractError("receipt workflow identity is incomplete")
    actual = distributions(dist, version)
    if actual != receipt["artifacts"]:
        raise ContractError("receipt artifact digests do not match files")
    print(f"verified project-workflow {version}: {receipt_path}")


def check_public_availability(version: str) -> None:
    url = f"https://pypi.org/pypi/project-workflow/{version}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            if response.status == 200:
                raise ContractError(f"project-workflow {version} already exists on PyPI")
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise ContractError(f"cannot establish PyPI version availability: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise ContractError(f"cannot establish PyPI version availability: {exc.reason}") from exc
    print(f"available: project-workflow {version} is not present on PyPI")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check-source")
    check.add_argument("--version")
    check.add_argument("--tag")
    check.add_argument("--clean", action="store_true")

    build = commands.add_parser("build-receipt")
    build.add_argument("--version", required=True)
    build.add_argument("--tag", required=True)
    build.add_argument("--commit", required=True)
    build.add_argument("--repository", required=True)
    build.add_argument("--run-id", required=True)
    build.add_argument("--run-url", required=True)
    build.add_argument("--dist", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--clean", action="store_true")

    verify = commands.add_parser("verify-receipt")
    verify.add_argument("--receipt", type=Path, required=True)
    verify.add_argument("--dist", type=Path, required=True)
    availability = commands.add_parser("check-public-availability")
    availability.add_argument("--version", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "check-source":
            print(validate_source(expected_version=args.version, tag=args.tag, clean=args.clean))
        elif args.command == "build-receipt":
            write_receipt(args)
        elif args.command == "verify-receipt":
            verify_receipt(args.receipt, args.dist)
        else:
            check_public_availability(args.version)
    except (ContractError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"release contract failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
