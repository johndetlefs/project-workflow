from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from project_workflow import cli as workflow_cli
from project_workflow import claude_adapter
from project_workflow import codex_adapter

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


def fixture_repo(tmp_path: Path) -> Path:
    initialized = run_project(tmp_path, "init", "--agent", "codex")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    scaffolded = run_project(
        tmp_path,
        "task",
        "init",
        "--title",
        "Bounded Execution",
        "--update-tracker",
        "--status",
        "In Progress",
    )
    assert scaffolded.returncode == 0, scaffolded.stdout + scaffolded.stderr
    task_dir = tmp_path / ".project-workflow/tasks/TASK-001-Bounded-Execution"
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nDeliver one bounded execution.\n",
        encoding="utf-8",
    )
    coordinated = run_project(
        tmp_path,
        "coordinate",
        "init",
        "--id",
        "TASK-001",
        "--phase",
        "implementation",
        "--source-revision",
        "candidate-source-1",
        "--loaded-package-version",
        workflow_cli.CURRENT_PACKAGE_VERSION,
        "--loaded-asset-version",
        str(workflow_cli.CURRENT_ASSET_VERSION),
        "--loaded-contract-version",
        str(workflow_cli.COORDINATION_CONTRACT_VERSION),
        "--context-id",
        "fixture-context",
        "--next-action",
        "Run bounded implementation.",
        "--material-verification",
        "no",
    )
    assert coordinated.returncode == 0, coordinated.stdout + coordinated.stderr
    return task_dir


def execution_control(
    *,
    host: str = "fake-host-a",
    agent_budget_unit: str = "tokens",
    gap: tuple[str, str] | None = None,
    release_candidate: bool = False,
) -> dict[str, object]:
    limits: dict[str, dict[str, object]] = {}
    for index, unit in enumerate(workflow_cli.EXECUTION_REQUIRED_LIMIT_UNITS, start=1):
        limits[unit] = {
            "state": "verified",
            "maximum": index * 10,
            "consumed": 0,
            "native_unit": agent_budget_unit if unit == "agent-budget" else unit,
            "source": "fixture policy",
        }
    controls = {
        name: {"state": "verified", "unit": name, "source": "fixture adapter"}
        for name in workflow_cli.EXECUTION_REQUIRED_CAPABILITY_CONTROLS
    }
    if gap is not None:
        gap_kind, gap_name = gap
        target = limits if gap_kind == "limit" else controls
        target[gap_name]["state"] = "unsupported"
        if gap_kind == "limit":
            target[gap_name]["maximum"] = None
            target[gap_name]["consumed"] = None
    verification_candidate = {
        "identity": "verification-1",
        "source_revision": "candidate-source-1",
        "proof_identity": "proof-1",
    }
    promoted = (
        {
            "identity": "release-1",
            "source_revision": "candidate-source-1",
            "artifact_identity": workflow_cli._execution_hash({"artifact": "one"}),
            "obligations": {
                name: workflow_cli._execution_hash({"obligation": name})
                for name in ("implementation", "verification", "qa", "affected-proof")
            },
        }
        if release_candidate
        else None
    )
    value: dict[str, object] = {
        "schema_version": workflow_cli.EXECUTION_CONTROL_SCHEMA_VERSION,
        "work_id": "TASK-001",
        "source_revision": "candidate-source-1",
        "phase": "implementation",
        "allowed_write_paths": ["src/**", "tests/**"],
        "permitted_operations": ["material-execution", "release"],
        "proof_obligations": ["focused-tests", "current-intent"],
        "limits": limits,
        "authorized_findings": [],
        "progress": {
            "attempt": 1,
            "finding_id": None,
            "baseline_source_identity": None,
            "baseline_evidence_identity": None,
            "current_source_identity": "candidate-source-1",
            "current_evidence_identity": "evidence-1",
        },
        "candidates": {
            "working_revision": "candidate-source-1",
            "verification_candidate": verification_candidate,
            "release_candidate": promoted,
        },
        "capability": {
            "host": host,
            "version": "fixture-1",
            "configuration_identity": f"{host}-configuration",
            "controls": controls,
        },
        "receipts": [],
        "sealed_identity": "pending",
    }
    value["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(value)
    )
    return value


def execution_receipt(value: dict[str, object]) -> dict[str, object]:
    capability = value["capability"]
    candidates = value["candidates"]
    assert isinstance(candidates, dict)
    receipt: dict[str, object] = {
        "schema_version": 1,
        "kind": "fake-adapter",
        "work_id": "TASK-001",
        "sealed_identity": value["sealed_identity"],
        "capability_identity": workflow_cli._execution_hash(capability),
        "phase": value["phase"],
        "candidate_identity": candidates["working_revision"],
        "proof_obligations_identity": workflow_cli._execution_hash(value["proof_obligations"]),
        "source_revision": "candidate-source-1",
        "operation": "material-execution",
        "outcome": "pass",
        "native_metrics": {"tokens": 20},
        "evidence_identity": "evidence-1",
        "receipt_identity": "pending",
    }
    receipt["receipt_identity"] = workflow_cli._execution_hash(
        {key: item for key, item in receipt.items() if key != "receipt_identity"}
    )
    return receipt


def record_delivery_ready(task_dir: Path) -> None:
    (task_dir / "IMPLEMENTATION.md").write_text(
        "# Implementation Plan\n\n"
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "| --: | ----- | ----------- | ------------------- | ----------------- | ------ |\n"
        "| 1 | Fixture delivery | Exercise authority | AC1 | Fixture | Done |\n\n"
        "## QA & Code Review\n\n"
        "- Verdict: Pass\n",
        encoding="utf-8",
    )


def install_control(task_dir: Path, value: dict[str, object]) -> None:
    path = task_dir / "COORDINATION.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    state["execution_control"] = value
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def codex_capability_settings(tmp_path: Path) -> dict[str, object]:
    executable = tmp_path / "codex"
    executable.write_bytes(b"sealed fixture binary\n")
    executable.chmod(0o700)
    return {
        "schema_version": codex_adapter.CODEX_ADAPTER_SCHEMA_VERSION,
        "adapter_kind": codex_adapter.CODEX_ADAPTER_KIND,
        "enabled": True,
        "trust": "trusted-local",
        "executable": str(executable),
        "executable_identity": "sha256:" + hashlib.sha256(executable.read_bytes()).hexdigest(),
        "expected_version": "codex-cli fixture",
        "model": "fixture-model",
        "prompt": "Complete the bounded fixture.",
        "allowed_tools": ["apply_patch"],
        "allowed_command_patterns": [],
        "test_command_patterns": [],
        "required_changed_paths": [],
    }


def claude_capability_settings(tmp_path: Path) -> dict[str, object]:
    executable = tmp_path / "claude"
    executable.write_bytes(b"sealed claude fixture binary\n")
    executable.chmod(0o700)
    return {
        "schema_version": claude_adapter.CLAUDE_ADAPTER_SCHEMA_VERSION,
        "adapter_kind": claude_adapter.CLAUDE_ADAPTER_KIND,
        "enabled": True,
        "trust": "trusted-local",
        "executable": str(executable),
        "executable_identity": "sha256:" + hashlib.sha256(executable.read_bytes()).hexdigest(),
        "expected_version": "claude-code fixture",
        "model": "fixture-model",
        "prompt": "Complete the bounded fixture.",
        "allowed_tools": ["Edit"],
        "disallowed_tools": ["WebFetch", "WebSearch"],
        "allowed_command_patterns": [],
        "test_command_patterns": [],
        "required_changed_paths": [],
        "required_output_identities": {},
        "required_validation_commands": [],
    }


def test_direct_work_is_zero_call_and_material_bypass_is_denied(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    direct = workflow_cli._execution_control_projection(tmp_path, "TASK-001", "status")
    assert direct == {
        "schema_version": 1,
        "target_id": "TASK-001",
        "operation": "status",
        "route": "direct",
        "state": "ready",
        "reason": "Direct read-only or cheap deterministic work needs no envelope.",
        "next_action": "Run the direct operation without launching an adapter.",
        "model_invocations": 0,
        "mutated": False,
        "executed": False,
    }
    before = (task_dir / "COORDINATION.json").read_bytes()
    denied = run_project(tmp_path, "execute", "--id", "TASK-001", "--format", "json")
    assert denied.returncode == 2
    payload = json.loads(denied.stdout)
    assert payload["state"] == "blocked"
    assert payload["reason"] == "execution-control-not-configured"
    assert payload["model_invocations"] == 0
    assert payload["mutated"] is False
    assert (task_dir / "COORDINATION.json").read_bytes() == before


def test_sealed_identity_and_every_limit_are_immutable() -> None:
    value = execution_control()
    validated = workflow_cli._execution_validate_control(value, work_id="TASK-001")
    assert set(validated["limits"]) == set(workflow_cli.EXECUTION_REQUIRED_LIMIT_UNITS)
    changed = deepcopy(value)
    changed["limits"]["test-invocations"]["maximum"] = 999
    with pytest.raises(ValueError, match="sealed identity"):
        workflow_cli._execution_validate_control(changed, work_id="TASK-001")
    missing = deepcopy(value)
    del missing["limits"]["elapsed-seconds"]
    with pytest.raises(ValueError, match="must contain exactly"):
        workflow_cli._execution_validate_control(missing, work_id="TASK-001")


def test_repeat_requires_named_finding_and_changed_source_or_evidence() -> None:
    value = execution_control()
    value["authorized_findings"] = [
        {
            "id": "finding-1",
            "state": "unresolved",
            "material": True,
            "source_identity": "source-1",
            "evidence_identity": "evidence-1",
        }
    ]
    value["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(value)
    )
    value["progress"] = {
        "attempt": 2,
        "finding_id": "finding-1",
        "baseline_source_identity": "source-1",
        "baseline_evidence_identity": "evidence-1",
        "current_source_identity": "source-1",
        "current_evidence_identity": "evidence-1",
    }
    with pytest.raises(ValueError, match="no changed source or evidence"):
        workflow_cli._execution_validate_control(value, work_id="TASK-001")
    value["progress"]["current_evidence_identity"] = "evidence-2"
    workflow_cli._execution_validate_control(value, work_id="TASK-001")
    unknown = deepcopy(value)
    unknown["progress"]["finding_id"] = "fabricated-finding"
    with pytest.raises(ValueError, match="sealed unresolved material finding"):
        workflow_cli._execution_validate_control(unknown, work_id="TASK-001")


def test_working_failures_do_not_require_release_candidate() -> None:
    working = execution_control(release_candidate=False)
    validated = workflow_cli._execution_validate_control(working, work_id="TASK-001")
    assert validated["candidates"]["release_candidate"] is None
    premature = execution_control(release_candidate=True)
    premature["candidates"]["release_candidate"]["obligations"]["qa"] = "pending"
    with pytest.raises(ValueError, match="proof identities"):
        workflow_cli._execution_validate_control(premature, work_id="TASK-001")
    stale = execution_control()
    stale["candidates"]["verification_candidate"]["source_revision"] = "stale-source"
    with pytest.raises(ValueError, match="verification candidate is stale"):
        workflow_cli._execution_validate_control(stale, work_id="TASK-001")


def test_fake_adapters_keep_native_units_but_share_generic_decisions(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    first_task = fixture_repo(first_root)
    second_task = fixture_repo(second_root)
    install_control(first_task, execution_control(host="fake-codex", agent_budget_unit="tokens"))
    install_control(
        second_task,
        execution_control(host="fake-claude", agent_budget_unit="usd-micros"),
    )
    first = workflow_cli._execution_control_projection(first_root, "TASK-001", "material-execution")
    second = workflow_cli._execution_control_projection(
        second_root, "TASK-001", "material-execution"
    )
    for field in ("route", "state", "reason", "next_action", "model_invocations", "mutated"):
        assert first[field] == second[field]
    assert first["state"] == "preflight-ready"
    first_unit = first["capability"]["host"]
    second_unit = second["capability"]["host"]
    assert (first_unit, second_unit) == ("fake-codex", "fake-claude")
    first_limits = execution_control(agent_budget_unit="tokens")["limits"]
    second_limits = execution_control(agent_budget_unit="usd-micros")["limits"]
    assert first_limits["agent-budget"]["native_unit"] == "tokens"
    assert second_limits["agent-budget"]["native_unit"] == "usd-micros"


@pytest.mark.parametrize(
    ("gap", "expected"),
    [
        (("control", "interruption"), "interruption"),
        (("limit", "agent-budget"), "agent-budget"),
    ],
)
def test_binding_capability_gaps_fail_closed(
    tmp_path: Path, gap: tuple[str, str], expected: str
) -> None:
    task_dir = fixture_repo(tmp_path)
    install_control(task_dir, execution_control(gap=gap))
    result = run_project(tmp_path, "execute", "--id", "TASK-001", "--format", "json")
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["state"] == "blocked"
    assert expected in payload["reason"]
    assert "supported host adapter" in payload["next_action"]


def test_exhausted_limit_preserves_non_passing_blocker(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    control = execution_control()
    control["limits"]["test-invocations"]["consumed"] = control["limits"]["test-invocations"][
        "maximum"
    ]
    control["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(control)
    )
    install_control(task_dir, control)
    result = run_project(tmp_path, "execute", "--id", "TASK-001", "--format", "json")
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["reason"] == "execution-limit-exhausted: test-invocations"
    assert "required proof still visibly incomplete" in payload["next_action"]


def test_release_requires_one_promoted_candidate(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    install_control(task_dir, execution_control(release_candidate=False))
    blocked = run_project(tmp_path, "release", "--id", "TASK-001", "--format", "json")
    assert blocked.returncode == 2
    assert json.loads(blocked.stdout)["reason"] == "release-candidate-not-promoted"
    install_control(task_dir, execution_control(release_candidate=True))
    unauthorized = run_project(tmp_path, "release", "--id", "TASK-001", "--format", "json")
    assert unauthorized.returncode == 2
    assert json.loads(unauthorized.stdout)["reason"].startswith("release-authority-not-current:")
    record_delivery_ready(task_dir)
    ready = run_project(tmp_path, "release", "--id", "TASK-001", "--format", "json")
    assert ready.returncode == 0, ready.stdout + ready.stderr
    assert json.loads(ready.stdout)["state"] == "preflight-ready"


def test_receipt_identity_is_input_bound() -> None:
    control = execution_control()
    receipt = execution_receipt(control)
    workflow_cli._execution_validate_receipt(receipt, "TASK-001")
    control["receipts"] = [receipt]
    workflow_cli._execution_validate_control(control, work_id="TASK-001")
    receipt["native_metrics"] = {"tokens": 21}
    with pytest.raises(ValueError, match="receipt identity"):
        workflow_cli._execution_validate_receipt(receipt, "TASK-001")
    transplanted = execution_control(host="different-host")
    transplanted["receipts"] = [execution_receipt(control)]
    with pytest.raises(ValueError, match="sealed envelope|host capability"):
        workflow_cli._execution_validate_control(transplanted, work_id="TASK-001")


def test_real_git_checkout_rejects_stale_coordinated_source(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True, text=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.com",
            "commit",
            "-m",
            "fixture",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    install_control(task_dir, execution_control())
    projection = workflow_cli._execution_control_projection(
        tmp_path, "TASK-001", "material-execution"
    )
    assert projection["state"] == "blocked"
    assert projection["reason"] == "execution-source-not-current-git-head"


def test_coordinate_status_and_doctor_share_execution_projection(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    install_control(task_dir, execution_control())
    status = run_project(tmp_path, "coordinate", "status", "--id", "TASK-001", "--format", "json")
    assert status.returncode == 0
    payload = json.loads(status.stdout)
    assert payload["execution"]["state"] == "preflight-ready"
    assert payload["next_action"] == payload["execution"]["next_action"]
    issues: list[workflow_cli.DoctorIssue] = []
    workflow_cli._doctor_check_coordination_state(tmp_path, issues)
    assert not [issue for issue in issues if "Material execution" in issue.message]
    install_control(task_dir, execution_control(gap=("control", "interruption")))
    status = run_project(tmp_path, "coordinate", "status", "--id", "TASK-001", "--format", "json")
    payload = json.loads(status.stdout)
    assert payload["next_action"] == payload["execution"]["next_action"]
    issues = []
    workflow_cli._doctor_check_coordination_state(tmp_path, issues)
    execution_issues = [issue for issue in issues if "Material execution" in issue.message]
    assert len(execution_issues) == 1
    assert "interruption" in execution_issues[0].message


def test_managed_cli_copies_are_identical() -> None:
    source = (ROOT / "src/project_workflow/cli.py").read_bytes()
    assert (ROOT / "src/project_workflow/templates/workflow.py").read_bytes() == source
    assert (ROOT / ".project-workflow/cli/workflow.py").read_bytes() == source
    product_text = "\n".join(
        (
            source.decode("utf-8"),
            (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        )
    ).lower()
    for forbidden in ("strategic advisor", "project-enforce", "80,000", "80000"):
        assert forbidden not in product_text


def test_codex_status_and_doctor_fail_closed_for_untrusted_capability(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path)
    settings = codex_capability_settings(tmp_path)
    control = execution_control(host="codex")
    capability = control["capability"]
    assert isinstance(capability, dict)
    capability["version"] = settings["expected_version"]
    capability["settings"] = settings
    capability["configuration_identity"] = workflow_cli._execution_hash(settings)
    control["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(control)
    )
    install_control(task_dir, control)

    ready = workflow_cli._execution_control_projection(tmp_path, "TASK-001", "material-execution")
    assert ready["state"] == "inspectable"
    assert ready["capability_inspection"]["state"] == "inspectable"

    settings["trust"] = "untrusted"
    capability["configuration_identity"] = workflow_cli._execution_hash(settings)
    control["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(control)
    )
    install_control(task_dir, control)
    blocked = workflow_cli._execution_control_projection(tmp_path, "TASK-001", "material-execution")
    assert blocked["state"] == "blocked"
    assert "trust is untrusted" in blocked["reason"]
    issues = []
    workflow_cli._doctor_check_coordination_state(tmp_path, issues)
    assert any("trust is untrusted" in issue.message for issue in issues)


def test_project_execute_persists_one_core_owned_codex_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    task_dir = fixture_repo(tmp_path)
    settings = codex_capability_settings(tmp_path)
    control = execution_control(host="codex")
    capability = control["capability"]
    assert isinstance(capability, dict)
    capability["version"] = settings["expected_version"]
    capability["settings"] = settings
    capability["configuration_identity"] = workflow_cli._execution_hash(settings)
    control["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(control)
    )
    install_control(task_dir, control)
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        codex_adapter,
        "run_codex_adapter",
        lambda root, sealed: {
            "terminal_status": "completed",
            "terminal_reason": "fixture turn completed",
            "native_metrics": {
                "elapsed-seconds": 1,
                "agent-budget": 2,
                "turns": 1,
                "tool-calls": 1,
                "test-invocations": 0,
                "identical-retries": 0,
                "worker-launches": 0,
                "changed-paths": 0,
                "write-scope": 0,
            },
            "evidence_identity": "fixture-runtime-evidence",
        },
    )

    workflow_cli.cmd_execute(argparse.Namespace(id="TASK-001", format="json"))
    payload = json.loads(capsys.readouterr().out)
    assert payload["core_receipt"]["outcome"] == "pass"
    state = json.loads((task_dir / "COORDINATION.json").read_text(encoding="utf-8"))
    receipts = state["execution_control"]["receipts"]
    assert len(receipts) == 1
    validated = workflow_cli._execution_validate_control(
        state["execution_control"], work_id="TASK-001"
    )
    assert (
        validated["receipts"][0]["receipt_identity"] == payload["core_receipt"]["receipt_identity"]
    )


def test_claude_status_is_inspectable_without_claiming_runtime_activation(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    settings = claude_capability_settings(tmp_path)
    control = execution_control(host="claude-code", agent_budget_unit="usd-micros")
    capability = control["capability"]
    assert isinstance(capability, dict)
    capability["version"] = settings["expected_version"]
    capability["settings"] = settings
    capability["configuration_identity"] = workflow_cli._execution_hash(settings)
    control["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(control)
    )
    install_control(task_dir, control)

    projection = workflow_cli._execution_control_projection(
        tmp_path, "TASK-001", "material-execution"
    )

    assert projection["state"] == "inspectable"
    assert projection["capability_inspection"]["classification"] == "inspectable"
    assert "unverified until exact dispatch" in projection["reason"]

    managed_environment = os.environ.copy()
    managed_environment.pop("PYTHONPATH", None)
    managed = subprocess.run(
        [
            "python3",
            ".project-workflow/cli/workflow.py",
            "coordinate",
            "status",
            "--id",
            "TASK-001",
            "--format",
            "json",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        env=managed_environment,
    )
    assert managed.returncode == 0, managed.stdout + managed.stderr
    managed_payload = json.loads(managed.stdout)
    assert managed_payload["execution"]["capability_inspection"]["state"] == "inspectable"
    assert (tmp_path / ".project-workflow/cli/claude_adapter.py").is_file()
    assert (
        tmp_path
        / ".project-workflow/cli/claude_plugin/project-workflow-execution-control/hooks/hooks.json"
    ).is_file()


def test_project_execute_persists_one_core_owned_claude_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    task_dir = fixture_repo(tmp_path)
    settings = claude_capability_settings(tmp_path)
    control = execution_control(host="claude-code", agent_budget_unit="usd-micros")
    capability = control["capability"]
    assert isinstance(capability, dict)
    capability["version"] = settings["expected_version"]
    capability["settings"] = settings
    capability["configuration_identity"] = workflow_cli._execution_hash(settings)
    control["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(control)
    )
    install_control(task_dir, control)
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        claude_adapter,
        "run_claude_adapter",
        lambda root, sealed: {
            "terminal_status": "completed",
            "terminal_reason": "fixture turn completed",
            "native_metrics": {
                "elapsed-seconds": 1,
                "agent-budget": 1_250_000,
                "turns": 2,
                "tool-calls": 1,
                "test-invocations": 0,
                "identical-retries": 0,
                "worker-launches": 0,
                "changed-paths": 0,
                "write-scope": 0,
            },
            "evidence_identity": "fixture-claude-runtime-evidence",
        },
    )

    workflow_cli.cmd_execute(argparse.Namespace(id="TASK-001", format="json"))
    payload = json.loads(capsys.readouterr().out)

    assert payload["core_receipt"]["kind"] == "claude-code-adapter"
    assert payload["core_receipt"]["outcome"] == "pass"
    state = json.loads((task_dir / "COORDINATION.json").read_text(encoding="utf-8"))
    receipts = state["execution_control"]["receipts"]
    assert len(receipts) == 1
    assert receipts[0]["native_metrics"]["agent-budget"] == 1_250_000


def test_project_execute_persists_one_terminal_receipt_when_claude_preflight_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    task_dir = fixture_repo(tmp_path)
    settings = claude_capability_settings(tmp_path)
    control = execution_control(host="claude-code", agent_budget_unit="usd-micros")
    capability = control["capability"]
    assert isinstance(capability, dict)
    capability["version"] = settings["expected_version"]
    capability["settings"] = settings
    capability["configuration_identity"] = workflow_cli._execution_hash(settings)
    control["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(control)
    )
    install_control(task_dir, control)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        claude_adapter,
        "run_claude_adapter",
        lambda *args: (_ for _ in ()).throw(
            claude_adapter.ClaudeAdapterError("plugin preflight unavailable")
        ),
    )

    with pytest.raises(SystemExit) as failure:
        workflow_cli.cmd_execute(argparse.Namespace(id="TASK-001", format="json"))

    assert failure.value.code == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["core_receipt"]["outcome"] == "infrastructure-failure"
    state = json.loads((task_dir / "COORDINATION.json").read_text(encoding="utf-8"))
    receipts = state["execution_control"]["receipts"]
    assert len(receipts) == 1
    assert receipts[0]["outcome"] == "infrastructure-failure"


def test_explicit_failing_evidence_and_blocked_parent_ac_are_not_hidden(
    tmp_path: Path,
) -> None:
    task_dir = tmp_path / "TASK-001"
    task_dir.mkdir()
    requirements = task_dir / "REQUIREMENTS.md"
    implementation = task_dir / "IMPLEMENTATION.md"
    artifact = task_dir / "runtime.json"
    requirements.write_text("# Requirements\n", encoding="utf-8")
    implementation.write_text(
        "## Parent AC Evidence\n\n- AC10: Blocked: real runtime proof remains missing.\n",
        encoding="utf-8",
    )
    artifact.write_text("{}\n", encoding="utf-8")
    (task_dir / "EVIDENCE.json").write_text(
        json.dumps(
            {
                "claims": [
                    {
                        "id": "runtime-blocker",
                        "recipe": "runtime-target-source",
                        "status": "fail",
                        "commit": "fixture",
                        "timestamp": "2026-08-28T00:00:00Z",
                        "parent_ac": "AC10",
                        "claim": "Runtime proof is absent.",
                        "execution_target": "Claude Code runtime",
                        "source_artifact": "candidate",
                        "observation_method": "Inventory",
                        "target_used_source_proof": "No executable available.",
                        "evidence_artifact": "runtime.json",
                        "evidence_artifact_hash": workflow_cli._sha256_file(artifact),
                        "invalid_substitutes": ["mock output"],
                    }
                ]
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    issues = workflow_cli._structured_evidence_issues(
        requirements_path=requirements,
        implementation_path=implementation,
        parent_ac_ids={"AC10"},
        include_explicit_nonpassing=True,
    )

    assert any("no passing claim record" in issue for issue in issues)
    assert not workflow_cli._parent_ac_evidence_present(
        implementation.read_text(encoding="utf-8"), "AC10"
    )
