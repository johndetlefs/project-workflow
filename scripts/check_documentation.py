#!/usr/bin/env python3
"""Check the current Project Workflow documentation contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = Path("src/project_workflow/_version.py")
REQUIRED_DOCUMENTS = (
    Path("README.md"),
    Path("RELEASING.md"),
    Path("COMPATIBILITY.md"),
    Path("AGENTS.md"),
    Path(".project-workflow/CONSTITUTION.md"),
    Path(".project-workflow/guidance.md"),
    Path(".project-workflow/cli/README.md"),
    Path("docs/architecture.md"),
    Path("docs/authority.md"),
    Path("docs/contributing.md"),
    Path("docs/maintenance.md"),
    Path("docs/using-project-workflow.md"),
)
CURRENT_GUIDANCE = tuple(path for path in REQUIRED_DOCUMENTS if "CONSTITUTION" not in path.name)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
VERSION_RE = re.compile(r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']')
PIN_RE = re.compile(r"project-workflow==(\d+\.\d+\.\d+)")


def read_version(root: Path) -> str:
    match = VERSION_RE.search((root / VERSION_PATH).read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"Could not read version from {VERSION_PATH}")
    return match.group(1)


def read_documents(root: Path) -> dict[Path, str]:
    return {
        path: (root / path).read_text(encoding="utf-8")
        for path in REQUIRED_DOCUMENTS
        if (root / path).is_file()
    }


def local_link_errors(root: Path, documents: dict[Path, str]) -> list[str]:
    errors: list[str] = []
    for source, text in documents.items():
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip().strip("<>")
            if not target or target.startswith(("#", "mailto:", "http://", "https://")):
                continue
            path_text = unquote(target.split("#", 1)[0])
            if not path_text:
                continue
            resolved = (
                root / path_text.lstrip("/")
                if path_text.startswith("/")
                else root / source.parent / path_text
            )
            if not resolved.exists():
                errors.append(f"{source}: local link target does not exist: {raw_target}")
    return errors


def documentation_errors(root: Path) -> list[str]:
    errors: list[str] = []
    missing = [str(path) for path in REQUIRED_DOCUMENTS if not (root / path).is_file()]
    errors.extend(f"required current document is missing: {path}" for path in missing)
    if missing or not (root / VERSION_PATH).is_file():
        if not (root / VERSION_PATH).is_file():
            errors.append(f"version authority is missing: {VERSION_PATH}")
        return errors

    version = read_version(root)
    documents = read_documents(root)
    errors.extend(local_link_errors(root, documents))

    line_limits = {Path("README.md"): 250, Path("RELEASING.md"): 250}
    line_limits.update({path: 300 for path in REQUIRED_DOCUMENTS if path.parent == Path("docs")})
    for path, limit in line_limits.items():
        line_count = len(documents[path].splitlines())
        if line_count > limit:
            errors.append(f"{path}: {line_count} lines exceeds the {limit}-line focused-doc limit")

    for path in CURRENT_GUIDANCE:
        text = documents[path]
        for pinned_version in PIN_RE.findall(text):
            if pinned_version != version:
                errors.append(
                    f"{path}: installation pin {pinned_version} does not match package {version}"
                )

    expected_commands = (
        f"project-workflow=={version} project init",
        f"project-workflow=={version} project upgrade",
    )
    for path in (Path("README.md"), Path("docs/maintenance.md")):
        for command in expected_commands:
            if command not in documents[path]:
                errors.append(f"{path}: missing current immutable command: {command}")

    required_terms: dict[Path, tuple[str, ...]] = {
        Path("docs/authority.md"): (
            "CONSTITUTION.md",
            "AGENTS.md",
            "project --help",
            "README.md",
            ".project-workflow/tasks/",
            "Generated",
        ),
        Path("docs/architecture.md"): (
            "scripts/runtime-modules.txt",
            "src/project_workflow/templates/workflow.py",
            ".project-workflow/cli/workflow.py",
        ),
        Path("RELEASING.md"): (
            "src/project_workflow/_version.py",
            "ruff check",
            "mypy",
            "pytest",
            "verify_package_journeys.py",
            "Release, publication, rollout, adoption, and owner acceptance",
        ),
    }
    for path, terms in required_terms.items():
        for term in terms:
            if term not in documents[path]:
                errors.append(f"{path}: missing authority term: {term}")

    if re.search(r"current release (?:is|remains)", documents[Path("RELEASING.md")], re.I):
        errors.append(
            "RELEASING.md: release procedure must not freeze a historical current version"
        )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    errors = documentation_errors(root)
    payload = {
        "contract": "project-workflow-documentation-v1",
        "documents": len(REQUIRED_DOCUMENTS),
        "errors": errors,
        "ok": not errors,
        "version": read_version(root) if (root / VERSION_PATH).is_file() else None,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif errors:
        print("Documentation contract failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    else:
        print(
            f"Documentation contract passed: {payload['documents']} current documents, "
            f"version {payload['version']}."
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
