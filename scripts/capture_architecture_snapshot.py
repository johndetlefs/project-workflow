#!/usr/bin/env python3
"""Capture canonical module and adapter ownership evidence as deterministic JSON."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts/runtime-modules.txt"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_paths() -> list[Path]:
    return [
        ROOT / line.strip()
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def internal_dependencies(path: Path, names: set[str]) -> list[str]:
    dependencies: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.module:
                dependency = node.module.split(".", 1)[0]
                if dependency in names:
                    dependencies.add(dependency)
            elif (node.module or "").startswith("project_workflow."):
                dependency = (node.module or "").split(".")[1]
                if dependency in names:
                    dependencies.add(dependency)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("project_workflow."):
                    dependency = alias.name.split(".")[1]
                    if dependency in names:
                        dependencies.add(dependency)
    return sorted(dependencies)


def top_level_definitions(path: Path) -> list[str]:
    return sorted(
        node.name
        for node in ast.parse(path.read_text(encoding="utf-8")).body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    )


def adapter_common_imports(path: Path) -> list[str]:
    imported = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and (node.module or "").endswith("adapter_common"):
            imported.extend(alias.name for alias in node.names)
    return sorted(set(imported))


def payload() -> dict[str, object]:
    paths = runtime_paths()
    names = {path.stem for path in paths}
    order = {path.stem: index for index, path in enumerate(paths)}
    modules = []
    definition_owners: dict[str, list[str]] = {}
    for path in paths:
        definitions = top_level_definitions(path)
        for name in definitions:
            definition_owners.setdefault(name, []).append(path.stem)
        dependencies = internal_dependencies(path, names)
        modules.append(
            {
                "name": path.stem,
                "path": path.relative_to(ROOT).as_posix(),
                "line_count": len(path.read_text(encoding="utf-8").splitlines()),
                "top_level_definition_count": len(definitions),
                "dependencies": dependencies,
                "dependencies_precede_module": all(
                    order[dependency] < order[path.stem] for dependency in dependencies
                ),
                "sha256": sha256(path),
            }
        )
    duplicates = {name: owners for name, owners in definition_owners.items() if len(owners) > 1}
    package = ROOT / "src/project_workflow"
    common = package / "adapter_common.py"
    codex = package / "codex_adapter.py"
    claude = package / "claude_adapter.py"
    template = package / "templates/workflow.py"
    helper = ROOT / ".project-workflow/cli/workflow.py"
    adapter_records = []
    for path in (common, codex, claude):
        installed = ROOT / ".project-workflow/cli" / path.name
        adapter_records.append(
            {
                "name": path.stem,
                "line_count": len(path.read_text(encoding="utf-8").splitlines()),
                "sha256": sha256(path),
                "installed_sha256": sha256(installed),
                "installed_matches_source": path.read_bytes() == installed.read_bytes(),
                "common_imports": adapter_common_imports(path),
            }
        )
    return {
        "schema_version": 1,
        "runtime_manifest": MANIFEST.relative_to(ROOT).as_posix(),
        "runtime_module_count": len(modules),
        "runtime_modules": modules,
        "duplicate_top_level_definitions": duplicates,
        "dependency_order_valid": all(record["dependencies_precede_module"] for record in modules),
        "entry_module_under_2000_lines": modules[-1]["line_count"] < 2_000,
        "domain_modules_under_5000_lines": all(
            record["line_count"] < 5_000 for record in modules[:-1]
        ),
        "generated_runtime": {
            "template_sha256": sha256(template),
            "installed_helper_sha256": sha256(helper),
            "byte_identical": template.read_bytes() == helper.read_bytes(),
        },
        "adapters": adapter_records,
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
