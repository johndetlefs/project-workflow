#!/usr/bin/env python3
"""Capture a deterministic Project Workflow test inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASED_BASELINE_COUNT = 548


def collect_node_ids() -> list[str]:
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-o", "addopts="],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stdout + completed.stderr)
    node_ids = sorted(
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("tests/") and "::" in line
    )
    if not node_ids:
        raise SystemExit("pytest collection returned no test node IDs")
    return node_ids


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    node_ids = collect_node_ids()
    test_files = sorted((ROOT / "tests").glob("test_*.py"))
    file_inventory = {
        path.relative_to(ROOT).as_posix(): len(path.read_text(encoding="utf-8").splitlines())
        for path in test_files
    }
    encoded_nodes = "\n".join(node_ids).encode("utf-8")
    payload = {
        "schema_version": 1,
        "released_baseline": {
            "version": "0.9.0",
            "collected_tests": RELEASED_BASELINE_COUNT,
            "source": "TASK-104 evidence/v0.9.0-compatibility-baseline.json",
        },
        "candidate": {
            "collected_tests": len(node_ids),
            "node_id_sha256": hashlib.sha256(encoded_nodes).hexdigest(),
            "test_file_count": len(test_files),
            "maximum_test_file_lines": max(file_inventory.values()),
            "all_test_files_below_2000_lines": all(
                line_count < 2_000 for line_count in file_inventory.values()
            ),
            "files": file_inventory,
        },
        "comparison": {
            "minimum_required": RELEASED_BASELINE_COUNT,
            "candidate_minus_released": len(node_ids) - RELEASED_BASELINE_COUNT,
            "preserved_or_increased": len(node_ids) >= RELEASED_BASELINE_COUNT,
        },
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Captured {len(node_ids)} test node IDs in {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
