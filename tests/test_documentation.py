from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_documentation.py"
SPEC = importlib.util.spec_from_file_location("check_documentation", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
check_documentation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_documentation)


def test_documentation_contract_passes() -> None:
    assert check_documentation.documentation_errors(ROOT) == []


def test_documentation_command_reports_current_contract() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--format", "json"],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "project-workflow-documentation-v1"' in result.stdout
    assert '"ok": true' in result.stdout


def test_local_link_errors_report_missing_targets(tmp_path: Path) -> None:
    errors = check_documentation.local_link_errors(
        tmp_path,
        {Path("README.md"): "[missing](docs/not-there.md)\n[external](https://example.com)"},
    )

    assert errors == ["README.md: local link target does not exist: docs/not-there.md"]
