from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src/project_workflow"
GENERATOR = ROOT / "scripts/build_runtime_bundle.py"
MANIFEST = ROOT / "scripts/runtime-modules.txt"
GENERATED_OUTPUTS = (
    ROOT / "src/project_workflow/templates/workflow.py",
    ROOT / ".project-workflow/cli/workflow.py",
)


def runtime_modules() -> list[Path]:
    return [
        ROOT / line.strip()
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def internal_dependencies(source: str, module_names: set[str]) -> set[str]:
    dependencies: set[str] = set()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.module:
                dependency = node.module.split(".", 1)[0]
                if dependency in module_names:
                    dependencies.add(dependency)
            elif (node.module or "").startswith("project_workflow."):
                dependency = (node.module or "").split(".")[1]
                if dependency in module_names:
                    dependencies.add(dependency)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("project_workflow."):
                    dependency = alias.name.split(".")[1]
                    if dependency in module_names:
                        dependencies.add(dependency)
    return dependencies


def cycle_in(graph: dict[str, set[str]]) -> tuple[str, ...] | None:
    active: list[str] = []
    complete: set[str] = set()

    def visit(node: str) -> tuple[str, ...] | None:
        if node in active:
            start = active.index(node)
            return tuple(active[start:] + [node])
        if node in complete:
            return None
        active.append(node)
        for dependency in sorted(graph.get(node, set())):
            cycle = visit(dependency)
            if cycle:
                return cycle
        active.pop()
        complete.add(node)
        return None

    for node in sorted(graph):
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def test_runtime_manifest_entries_are_unique_python_modules() -> None:
    paths = runtime_modules()
    assert paths
    assert len(paths) == len(set(paths))
    assert all(path.is_file() and path.suffix == ".py" for path in paths)


def test_runtime_manifest_conforms_to_documented_module_authority() -> None:
    paths = runtime_modules()
    architecture = (ROOT / "docs/architecture.md").read_text(encoding="utf-8")
    assert len(paths) <= 12
    for path in paths:
        assert f"| {path.name} |" in architecture, path


def test_generated_runtime_is_current() -> None:
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert GENERATED_OUTPUTS[0].read_bytes() == GENERATED_OUTPUTS[1].read_bytes()


def test_runtime_generator_is_deterministic() -> None:
    spec = importlib.util.spec_from_file_location("runtime_bundle", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.build_bundle() == module.build_bundle()


def test_runtime_modules_do_not_import_cli() -> None:
    for path in runtime_modules():
        if path.name == "cli.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = [
            node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        assert not any(
            (isinstance(node, ast.ImportFrom) and (node.module or "").endswith("cli"))
            or (
                isinstance(node, ast.Import)
                and any(alias.name.endswith(".cli") for alias in node.names)
            )
            for node in imports
        ), path


def test_runtime_module_graph_is_acyclic() -> None:
    paths = runtime_modules()
    names = {path.stem for path in paths}
    graph = {
        path.stem: internal_dependencies(path.read_text(encoding="utf-8"), names) for path in paths
    }
    assert cycle_in(graph) is None, graph


def test_runtime_module_dependencies_follow_manifest_order() -> None:
    paths = runtime_modules()
    names = {path.stem for path in paths}
    order = {path.stem: index for index, path in enumerate(paths)}
    for path in paths:
        dependencies = internal_dependencies(path.read_text(encoding="utf-8"), names)
        assert all(order[dependency] < order[path.stem] for dependency in dependencies), (
            path,
            dependencies,
        )


def test_architecture_helpers_reject_forbidden_graphs() -> None:
    assert internal_dependencies("from .cli import main\n", {"cli"}) == {"cli"}
    assert cycle_in({"a": {"b"}, "b": {"a"}}) == ("a", "b", "a")


def test_deliberate_dependency_direction_violation_is_mechanically_visible() -> None:
    order = {"contracts": 0, "repository": 1, "lifecycle": 2}
    forbidden = internal_dependencies(
        "from .lifecycle import task_ready\n",
        set(order),
    )
    assert forbidden == {"lifecycle"}
    assert not all(order[dependency] < order["repository"] for dependency in forbidden)


def test_generated_helper_is_dependency_free() -> None:
    result = subprocess.run(
        [sys.executable, "-I", str(GENERATED_OUTPUTS[1]), "--version"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "project 0.10.0"


def test_runtime_module_size_budget_after_extraction() -> None:
    paths = runtime_modules()
    if paths == [PACKAGE / "cli.py"]:
        return
    for path in paths:
        limit = 2_000 if path.name == "cli.py" else 5_000
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count < limit, f"{path}: {line_count} lines exceeds {limit}"
