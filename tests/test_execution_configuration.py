from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from project_workflow import cli as workflow_cli

PROJECT = [sys.executable, "-m", "project_workflow.cli"]
ROOT = Path(__file__).parents[1]


def run_project(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [*PROJECT, *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


def fixture_repo(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "repo"
    root.mkdir()
    initialized = run_project(root, "init", "--agent", "codex")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    scaffolded = run_project(
        root,
        "task",
        "init",
        "--title",
        "Configured Execution",
        "--update-tracker",
        "--status",
        "In Progress",
    )
    assert scaffolded.returncode == 0, scaffolded.stdout + scaffolded.stderr
    task_dir = root / ".project-workflow/tasks/TASK-001-Configured-Execution"
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nRun one configured bounded execution.\n",
        encoding="utf-8",
    )
    run_git(root, "init")
    run_git(root, "config", "user.email", "test@example.com")
    run_git(root, "config", "user.name", "Project Workflow Test")
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "Fixture source")
    source_revision = run_git(root, "rev-parse", "HEAD")
    coordinated = run_project(
        root,
        "coordinate",
        "init",
        "--id",
        "TASK-001",
        "--phase",
        "implementation",
        "--source-revision",
        source_revision,
        "--loaded-package-version",
        workflow_cli.CURRENT_PACKAGE_VERSION,
        "--loaded-asset-version",
        str(workflow_cli.CURRENT_ASSET_VERSION),
        "--loaded-contract-version",
        str(workflow_cli.COORDINATION_CONTRACT_VERSION),
        "--context-id",
        "execution-config-test",
        "--next-action",
        "Configure bounded execution.",
        "--material-verification",
        "no",
    )
    assert coordinated.returncode == 0, coordinated.stdout + coordinated.stderr
    return root, source_revision


def fake_codex(tmp_path: Path, *, complete_contract: bool = True) -> Path:
    executable = tmp_path / "bin" / "codex"
    executable.parent.mkdir(parents=True, exist_ok=True)
    help_output = (
        "printf '%s\\n' '--listen' 'stdio://'\n"
        if complete_contract
        else "printf '%s\\n' 'unsupported'\n"
    )
    exec_output = (
        "printf '%s\\n' '--output-schema' '--json'\n"
        if complete_contract
        else "printf '%s\\n' 'unsupported'\n"
    )
    executable.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = "--version" ]; then\n'
        "  printf '%s\\n' 'codex-cli fixture'\n"
        'elif [ "$1" = "app-server" ] && [ "$2" = "--help" ]; then\n'
        f"  {help_output}"
        'elif [ "$1" = "exec" ] && [ "$2" = "--help" ]; then\n'
        f"  {exec_output}"
        "else\n"
        "  exit 2\n"
        "fi\n",
        encoding="utf-8",
    )
    executable.chmod(0o700)
    return executable


def operator_config(executable: Path) -> dict[str, object]:
    native_units = {
        "elapsed-seconds": "seconds",
        "agent-budget": "tokens",
        "turns": "turns",
        "tool-calls": "tool-calls",
        "test-invocations": "test-invocations",
        "identical-retries": "identical-retries",
        "worker-launches": "worker-launches",
        "changed-paths": "changed-paths",
        "write-scope": "write-scope",
    }
    return {
        "schema_version": workflow_cli.EXECUTION_OPERATOR_CONFIG_SCHEMA_VERSION,
        "host": "codex",
        "executable": str(executable),
        "trust": "trusted-local",
        "model": "fixture-model",
        "prompt": "Create src/canary.txt with the exact text configured.\n",
        "allowed_write_paths": ["src/canary.txt"],
        "permitted_operations": ["material-execution"],
        "proof_obligations": ["exact-canary-content", "sealed-scope"],
        "limits": {
            unit: {"maximum": index * 10, "native_unit": native_unit}
            for index, (unit, native_unit) in enumerate(native_units.items(), start=1)
        },
        "allowed_tools": ["apply_patch"],
        "allowed_command_patterns": [],
        "test_command_patterns": [],
        "required_changed_paths": ["src/canary.txt"],
    }


def write_config(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "execution-config.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def test_public_configuration_is_sealed_idempotent_disableable_and_inspectable(
    tmp_path: Path,
) -> None:
    root, source_revision = fixture_repo(tmp_path)
    executable = fake_codex(tmp_path)
    config_path = write_config(tmp_path, operator_config(executable))

    configured = run_project(
        root,
        "execution",
        "configure",
        "--id",
        "TASK-001",
        "--config",
        str(config_path),
        "--format",
        "json",
    )
    assert configured.returncode == 0, configured.stdout + configured.stderr
    configured_payload = json.loads(configured.stdout)
    assert configured_payload["capability_state"] == "verified"
    assert configured_payload["mutated"] is True
    assert configured_payload["model_invocations"] == 0

    coordination_path = (
        root / ".project-workflow/tasks/TASK-001-Configured-Execution/COORDINATION.json"
    )
    state = json.loads(coordination_path.read_text(encoding="utf-8"))
    control = workflow_cli._execution_validate_control(
        state["execution_control"], work_id="TASK-001"
    )
    assert control["source_revision"] == source_revision
    assert control["sealed_identity"] == configured_payload["sealed_identity"]
    assert all(
        detail["state"] == "verified" for detail in control["capability"]["controls"].values()
    )

    before_noop = coordination_path.read_bytes()
    noop = run_project(
        root,
        "execution",
        "configure",
        "--id",
        "TASK-001",
        "--config",
        str(config_path),
        "--format",
        "json",
    )
    assert noop.returncode == 0, noop.stdout + noop.stderr
    assert json.loads(noop.stdout)["mutated"] is False
    assert coordination_path.read_bytes() == before_noop

    status = run_project(root, "execution", "status", "--id", "TASK-001", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    assert json.loads(status.stdout)["state"] == "inspectable"

    capability = control["capability"]
    candidates = control["candidates"]
    assert isinstance(capability, dict)
    assert isinstance(candidates, dict)
    receipt = {
        "schema_version": workflow_cli.EXECUTION_CONTROL_SCHEMA_VERSION,
        "kind": "codex-adapter",
        "work_id": "TASK-001",
        "sealed_identity": control["sealed_identity"],
        "capability_identity": workflow_cli._execution_hash(capability),
        "phase": control["phase"],
        "candidate_identity": candidates["working_revision"],
        "proof_obligations_identity": workflow_cli._execution_hash(control["proof_obligations"]),
        "source_revision": source_revision,
        "operation": "material-execution",
        "outcome": "pass",
        "native_metrics": {unit: 0 for unit in workflow_cli.EXECUTION_REQUIRED_LIMIT_UNITS},
        "evidence_identity": "fixture-evidence",
        "receipt_identity": "pending",
    }
    receipt["receipt_identity"] = workflow_cli._execution_hash(
        {key: value for key, value in receipt.items() if key != "receipt_identity"}
    )
    state["execution_control"]["receipts"].append(receipt)
    workflow_cli._execution_validate_control(state["execution_control"], work_id="TASK-001")
    coordination_path.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    disabled = run_project(root, "execution", "disable", "--id", "TASK-001", "--format", "json")
    assert disabled.returncode == 0, disabled.stdout + disabled.stderr
    assert json.loads(disabled.stdout)["capability_state"] == "disabled"
    disabled_state = json.loads(coordination_path.read_text(encoding="utf-8"))
    assert disabled_state["execution_control"]["receipts"] == []
    assert (
        disabled_state["execution_control_history"][0]["receipts"][0]["receipt_identity"]
        == receipt["receipt_identity"]
    )
    blocked = run_project(root, "execution", "status", "--id", "TASK-001", "--format", "json")
    assert blocked.returncode == 2
    assert "adapter is disabled" in json.loads(blocked.stdout)["reason"]

    reenabled = run_project(
        root,
        "execution",
        "configure",
        "--id",
        "TASK-001",
        "--config",
        str(config_path),
        "--format",
        "json",
    )
    assert reenabled.returncode == 0, reenabled.stdout + reenabled.stderr
    assert json.loads(reenabled.stdout)["mutated"] is True

    executable.write_text(executable.read_text(encoding="utf-8") + "# tampered\n", encoding="utf-8")
    tampered = run_project(root, "execution", "status", "--id", "TASK-001", "--format", "json")
    assert tampered.returncode == 2
    assert "identity does not match" in json.loads(tampered.stdout)["reason"]


def test_unsupported_probe_is_retained_as_a_truthful_non_passing_control(tmp_path: Path) -> None:
    root, _source_revision = fixture_repo(tmp_path)
    executable = fake_codex(tmp_path, complete_contract=False)
    config_path = write_config(tmp_path, operator_config(executable))

    configured = run_project(
        root,
        "execution",
        "configure",
        "--id",
        "TASK-001",
        "--config",
        str(config_path),
        "--format",
        "json",
    )
    assert configured.returncode == 2
    payload = json.loads(configured.stdout)
    assert payload["capability_state"] == "unsupported"
    assert "App Server stdio contract is unavailable" in payload["reason"]
    status = run_project(root, "execution", "status", "--id", "TASK-001", "--format", "json")
    assert status.returncode == 2
    assert "binding-capability-gap" in json.loads(status.stdout)["reason"]


def test_configuration_rejects_wrong_native_unit_without_mutating_state(tmp_path: Path) -> None:
    root, _source_revision = fixture_repo(tmp_path)
    executable = fake_codex(tmp_path)
    config = operator_config(executable)
    config["limits"]["agent-budget"]["native_unit"] = "usd-micros"
    config_path = write_config(tmp_path, config)

    coordination_path = (
        root / ".project-workflow/tasks/TASK-001-Configured-Execution/COORDINATION.json"
    )
    before = coordination_path.read_bytes()
    rejected = run_project(
        root,
        "execution",
        "configure",
        "--id",
        "TASK-001",
        "--config",
        str(config_path),
        "--format",
        "json",
    )
    assert rejected.returncode == 1
    assert "must use native unit `tokens`" in rejected.stderr
    assert coordination_path.read_bytes() == before


def test_configuration_never_grants_worker_write_authority_over_coordination(
    tmp_path: Path,
) -> None:
    root, _source_revision = fixture_repo(tmp_path)
    executable = fake_codex(tmp_path)
    config = operator_config(executable)
    config["allowed_write_paths"] = ["**"]
    config_path = write_config(tmp_path, config)

    rejected = run_project(
        root,
        "execution",
        "configure",
        "--id",
        "TASK-001",
        "--config",
        str(config_path),
    )
    assert rejected.returncode == 1
    assert "must not grant worker authority over COORDINATION.json" in rejected.stderr
