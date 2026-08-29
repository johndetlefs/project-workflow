#!/usr/bin/env python3
"""Build the dependency-free repository-local workflow runtime deterministically."""

from __future__ import annotations

import argparse
import ast
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts/runtime-modules.txt"
TEMPLATE = ROOT / "src/project_workflow/templates/workflow.py"
SOURCE_MIRROR = ROOT / ".project-workflow/cli/workflow.py"
GENERATED_MARKER = "# project-workflow:generated"
PROVENANCE = "# source-manifest: scripts/runtime-modules.txt"


def manifest_paths() -> tuple[Path, ...]:
    entries = []
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        path = ROOT / value
        if not path.is_file():
            raise ValueError(f"Runtime manifest entry does not exist: {value}")
        entries.append(path)
    if not entries:
        raise ValueError("Runtime manifest must contain at least one source module.")
    return tuple(entries)


def _top_level_removals(source: str) -> set[int]:
    tree = ast.parse(source)
    removals: set[int] = set()
    for index, node in enumerate(tree.body):
        remove = False
        if (
            index == 0
            and isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            remove = True
        elif isinstance(node, ast.ImportFrom) and node.module == "__future__":
            remove = True
        elif isinstance(node, ast.ImportFrom) and (
            node.level > 0 or (node.module or "").startswith("project_workflow")
        ):
            remove = True
        if remove:
            removals.update(range(node.lineno, node.end_lineno + 1))
    return removals


def canonical_module_text(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    removals = _top_level_removals(source)
    lines = source.splitlines()
    kept = [
        line
        for number, line in enumerate(lines, start=1)
        if number not in removals and not (number == 1 and line.startswith("#!"))
    ]
    while kept and not kept[0].strip():
        kept.pop(0)
    while kept and not kept[-1].strip():
        kept.pop()
    return "\n".join(kept) + "\n"


def build_bundle() -> str:
    paths = manifest_paths()
    manifest_hash = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    sections = [
        "#!/usr/bin/env python3\n",
        '"""Generated dependency-free Project Workflow runtime. Do not edit directly."""\n',
        "from __future__ import annotations\n\n",
        f"{GENERATED_MARKER}\n",
        f"{PROVENANCE}\n",
        f"# manifest-sha256: {manifest_hash}\n\n",
    ]
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        sections.append(f"# --- begin {relative} ---\n")
        sections.append(canonical_module_text(path))
        sections.append(f"# --- end {relative} ---\n\n")
    return "".join(sections).rstrip("\n") + "\n"


def expected_outputs() -> tuple[Path, Path]:
    return TEMPLATE, SOURCE_MIRROR


def check() -> int:
    expected = build_bundle()
    stale = [
        path.relative_to(ROOT).as_posix()
        for path in expected_outputs()
        if not path.is_file() or path.read_text(encoding="utf-8") != expected
    ]
    if stale:
        print("Generated runtime is stale:")
        for path in stale:
            print(f"- {path}")
        return 1
    print("Generated runtime is current.")
    return 0


def write() -> int:
    content = build_bundle()
    for path in expected_outputs():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    SOURCE_MIRROR.chmod(SOURCE_MIRROR.stat().st_mode | 0o111)
    print(f"Wrote {TEMPLATE.relative_to(ROOT)}")
    print(f"Wrote {SOURCE_MIRROR.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    return check() if args.check else write()


if __name__ == "__main__":
    sys.exit(main())
