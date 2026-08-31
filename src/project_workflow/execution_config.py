"""Public operator configuration for sealed Project Workflow execution."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import cast

from .contracts import (
    EXECUTION_CONTROL_SCHEMA_VERSION,
    EXECUTION_OPERATOR_CONFIG_SCHEMA_VERSION,
    EXECUTION_PHASES,
    EXECUTION_REQUIRED_CAPABILITY_CONTROLS,
    EXECUTION_REQUIRED_LIMIT_UNITS,
)
from .coordination import (
    _coordination_load_state,
    _coordination_preflight_payload,
    _coordination_required_text,
    _coordination_write_state,
    _execution_control_projection,
    _execution_copy,
    _execution_hash,
    _execution_sealed_payload,
    _execution_validate_control,
    _print_execution_projection,
)


def _execution_operator_string_list(
    value: object, field_name: str, *, empty: bool = False
) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"execution configuration `{field_name}` must be a string list")
    normalized = [item.strip() for item in value]
    if any(not item for item in normalized) or len(normalized) != len(set(normalized)):
        raise ValueError(
            f"execution configuration `{field_name}` contains an empty or duplicate value"
        )
    if not empty and not normalized:
        raise ValueError(f"execution configuration `{field_name}` must not be empty")
    return normalized


def _execution_operator_config(path: Path) -> dict[str, object]:
    try:
        value: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read execution configuration {path}: {exc}") from exc
    required = {
        "schema_version",
        "host",
        "executable",
        "trust",
        "model",
        "prompt",
        "allowed_write_paths",
        "permitted_operations",
        "proof_obligations",
        "limits",
        "allowed_tools",
    }
    optional = {
        "allowed_command_patterns",
        "test_command_patterns",
        "required_changed_paths",
        "disallowed_tools",
        "required_output_identities",
        "required_validation_commands",
    }
    if not isinstance(value, dict):
        raise ValueError("execution configuration must contain a JSON object")
    missing = sorted(required - set(value))
    unexpected = sorted(set(value) - required - optional)
    if missing or unexpected:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if unexpected:
            details.append("unexpected: " + ", ".join(unexpected))
        raise ValueError(
            "execution configuration has an invalid shape (" + "; ".join(details) + ")"
        )
    if value.get("schema_version") != EXECUTION_OPERATOR_CONFIG_SCHEMA_VERSION:
        raise ValueError(
            "execution configuration schema_version must be "
            f"{EXECUTION_OPERATOR_CONFIG_SCHEMA_VERSION}"
        )
    host = value.get("host")
    if host not in {"codex", "claude-code"}:
        raise ValueError("execution configuration host must be codex or claude-code")
    executable = Path(_coordination_required_text(value.get("executable"), "executable"))
    if not executable.is_absolute():
        raise ValueError("execution configuration executable must be an absolute path")
    expected_name = "codex" if host == "codex" else "claude"
    if executable.name != expected_name:
        raise ValueError(f"execution configuration executable must name `{expected_name}`")
    for field_name in ("trust", "model", "prompt"):
        _coordination_required_text(value.get(field_name), field_name)
    allowed_write_paths = _execution_operator_string_list(
        value.get("allowed_write_paths"), "allowed_write_paths", empty=True
    )
    for raw_path in allowed_write_paths:
        candidate = Path(raw_path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("allowed_write_paths must stay within the repository")
        coordination_samples = (
            ".project-workflow/tasks/TASK-000/COORDINATION.json",
            ".project-workflow/tasks/EPIC-000/TASK-000/COORDINATION.json",
        )
        if any(fnmatch.fnmatchcase(sample, raw_path) for sample in coordination_samples):
            raise ValueError(
                "allowed_write_paths must not grant worker authority over COORDINATION.json"
            )
    permitted_operations = _execution_operator_string_list(
        value.get("permitted_operations"), "permitted_operations"
    )
    if permitted_operations != ["material-execution"]:
        raise ValueError(
            "the public adapter currently permits exactly `material-execution`; "
            "candidate and release authority use their owning commands"
        )
    proof_obligations = _execution_operator_string_list(
        value.get("proof_obligations"), "proof_obligations"
    )
    allowed_tools = _execution_operator_string_list(value.get("allowed_tools"), "allowed_tools")
    allowed_command_patterns = _execution_operator_string_list(
        value.get("allowed_command_patterns", []), "allowed_command_patterns", empty=True
    )
    test_command_patterns = _execution_operator_string_list(
        value.get("test_command_patterns", []), "test_command_patterns", empty=True
    )
    required_changed_paths = _execution_operator_string_list(
        value.get("required_changed_paths", []), "required_changed_paths", empty=True
    )
    disallowed_tools = _execution_operator_string_list(
        value.get("disallowed_tools", []), "disallowed_tools", empty=True
    )
    required_validation_commands = _execution_operator_string_list(
        value.get("required_validation_commands", []),
        "required_validation_commands",
        empty=True,
    )
    raw_output_identities = value.get("required_output_identities", {})
    if not isinstance(raw_output_identities, dict) or any(
        not isinstance(key, str) or not isinstance(identity, str)
        for key, identity in raw_output_identities.items()
    ):
        raise ValueError("required_output_identities must be a string-to-string object")
    if host == "codex" and (
        disallowed_tools or raw_output_identities or required_validation_commands
    ):
        raise ValueError(
            "disallowed_tools, required_output_identities, and required_validation_commands "
            "are Claude Code configuration fields"
        )
    raw_limits = value.get("limits")
    if not isinstance(raw_limits, dict) or set(raw_limits) != set(EXECUTION_REQUIRED_LIMIT_UNITS):
        raise ValueError(
            "execution configuration limits must contain exactly: "
            + ", ".join(EXECUTION_REQUIRED_LIMIT_UNITS)
        )
    expected_native_units = {
        "elapsed-seconds": "seconds",
        "agent-budget": "tokens" if host == "codex" else "usd-micros",
        "turns": "turns",
        "tool-calls": "tool-calls",
        "test-invocations": "test-invocations",
        "identical-retries": "identical-retries",
        "worker-launches": "worker-launches",
        "changed-paths": "changed-paths",
        "write-scope": "write-scope",
    }
    limits: dict[str, dict[str, object]] = {}
    for unit in EXECUTION_REQUIRED_LIMIT_UNITS:
        raw = raw_limits.get(unit)
        if not isinstance(raw, dict) or set(raw) != {"maximum", "native_unit"}:
            raise ValueError(f"execution configuration limit `{unit}` is malformed")
        maximum = raw.get("maximum")
        if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
            raise ValueError(f"execution configuration limit `{unit}` must be a positive integer")
        native_unit = _coordination_required_text(
            raw.get("native_unit"), f"limits.{unit}.native_unit"
        )
        if native_unit != expected_native_units[unit]:
            raise ValueError(
                f"execution configuration limit `{unit}` must use native unit "
                f"`{expected_native_units[unit]}` for {host}"
            )
        limits[unit] = {"maximum": maximum, "native_unit": native_unit}
    return {
        **value,
        "executable": str(executable),
        "allowed_write_paths": allowed_write_paths,
        "permitted_operations": permitted_operations,
        "proof_obligations": proof_obligations,
        "allowed_tools": allowed_tools,
        "allowed_command_patterns": allowed_command_patterns,
        "test_command_patterns": test_command_patterns,
        "required_changed_paths": required_changed_paths,
        "disallowed_tools": disallowed_tools,
        "required_output_identities": dict(raw_output_identities),
        "required_validation_commands": required_validation_commands,
        "limits": limits,
    }


def _execution_observed_version(executable: Path, host: str) -> str:
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError(f"{host} executable is unavailable or not executable: {executable}")
    try:
        result = subprocess.run(
            [str(executable), "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"cannot inspect {host} executable version: {exc}") from exc
    observed = (result.stdout if host == "codex" else result.stdout or result.stderr).strip()
    if result.returncode != 0 or not observed:
        raise ValueError(f"cannot inspect {host} executable version")
    return observed


def _execution_adapter_settings(
    config: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    host = str(config["host"])
    executable = Path(str(config["executable"]))
    executable_identity = "sha256:" + hashlib.sha256(executable.read_bytes()).hexdigest()
    expected_version = _execution_observed_version(executable, host)
    common: dict[str, object] = {
        "enabled": True,
        "trust": config["trust"],
        "executable": str(executable),
        "executable_identity": executable_identity,
        "expected_version": expected_version,
        "model": config["model"],
        "prompt": config["prompt"],
        "allowed_tools": config["allowed_tools"],
        "allowed_command_patterns": config["allowed_command_patterns"],
        "test_command_patterns": config["test_command_patterns"],
        "required_changed_paths": config["required_changed_paths"],
    }
    if host == "codex":
        try:
            from project_workflow.codex_adapter import (
                CODEX_ADAPTER_KIND,
                CODEX_ADAPTER_SCHEMA_VERSION,
                probe_codex_capability,
                validate_codex_settings,
            )
        except ModuleNotFoundError:
            from codex_adapter import (  # type: ignore
                CODEX_ADAPTER_KIND,
                CODEX_ADAPTER_SCHEMA_VERSION,
                probe_codex_capability,
                validate_codex_settings,
            )

        settings = {
            **common,
            "schema_version": CODEX_ADAPTER_SCHEMA_VERSION,
            "adapter_kind": CODEX_ADAPTER_KIND,
        }
        settings = dict(validate_codex_settings(settings))
        return settings, probe_codex_capability(settings)
    try:
        from project_workflow.claude_adapter import (
            CLAUDE_ADAPTER_KIND,
            CLAUDE_ADAPTER_SCHEMA_VERSION,
            probe_claude_capability,
            validate_claude_settings,
        )
    except ModuleNotFoundError:
        from claude_adapter import (  # type: ignore
            CLAUDE_ADAPTER_KIND,
            CLAUDE_ADAPTER_SCHEMA_VERSION,
            probe_claude_capability,
            validate_claude_settings,
        )

    settings = {
        **common,
        "schema_version": CLAUDE_ADAPTER_SCHEMA_VERSION,
        "adapter_kind": CLAUDE_ADAPTER_KIND,
        "disallowed_tools": config["disallowed_tools"],
        "required_output_identities": config["required_output_identities"],
        "required_validation_commands": config["required_validation_commands"],
    }
    settings = dict(validate_claude_settings(settings))
    return settings, probe_claude_capability(settings)


def _execution_configure_payload(
    root: Path, target_id: str, config_path: Path
) -> tuple[dict[str, object], dict[str, object]]:
    coordination = _coordination_load_state(root, target_id)
    preflight = _coordination_preflight_payload(root, target_id, coordination)
    if preflight["contract_state"] not in {"current", "compatible"}:
        raise ValueError("coordination contract is stale; load the current contract first")
    source_revision = str(coordination["source_revision"])
    git_result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if git_result.returncode != 0 or git_result.stdout.strip() != source_revision:
        raise ValueError("coordination source_revision must match the current Git HEAD")
    phase = str(coordination["phase"])
    if phase not in EXECUTION_PHASES:
        raise ValueError(f"coordination phase `{phase}` cannot own material execution")
    config = _execution_operator_config(config_path)
    settings, probe = _execution_adapter_settings(config)
    capability_state = "verified" if probe.get("state") == "verified" else "unsupported"
    reason = str(probe.get("reason", "Capability probe returned no reason."))
    controls = {
        name: {
            "state": capability_state,
            "unit": name,
            "source": f"{config['host']} capability probe: {reason}",
        }
        for name in EXECUTION_REQUIRED_CAPABILITY_CONTROLS
    }
    configured_limits = cast(dict[str, dict[str, object]], config["limits"])
    limits = {
        unit: {
            "state": "verified",
            "maximum": configured_limits[unit]["maximum"],
            "consumed": 0,
            "native_unit": configured_limits[unit]["native_unit"],
            "source": f"operator configuration: {config_path.name}",
        }
        for unit in EXECUTION_REQUIRED_LIMIT_UNITS
    }
    configured_proof = cast(list[str], config["proof_obligations"])
    configured_paths = cast(list[str], config["allowed_write_paths"])
    configured_operations = cast(list[str], config["permitted_operations"])
    proof_obligations = list(configured_proof)
    baseline_evidence = _execution_hash(
        {"source_revision": source_revision, "proof_obligations": proof_obligations}
    )
    control: dict[str, object] = {
        "schema_version": EXECUTION_CONTROL_SCHEMA_VERSION,
        "work_id": target_id,
        "source_revision": source_revision,
        "phase": phase,
        "allowed_write_paths": list(configured_paths),
        "permitted_operations": list(configured_operations),
        "proof_obligations": proof_obligations,
        "limits": limits,
        "authorized_findings": [],
        "progress": {
            "attempt": 1,
            "finding_id": None,
            "baseline_source_identity": None,
            "baseline_evidence_identity": None,
            "current_source_identity": source_revision,
            "current_evidence_identity": baseline_evidence,
        },
        "candidates": {
            "working_revision": source_revision,
            "verification_candidate": None,
            "release_candidate": None,
        },
        "capability": {
            "host": config["host"],
            "version": settings["expected_version"],
            "configuration_identity": _execution_hash(settings),
            "controls": controls,
            "settings": settings,
        },
        "receipts": [],
        "sealed_identity": "pending",
    }
    control["sealed_identity"] = _execution_hash(_execution_sealed_payload(control))
    return _execution_validate_control(control, work_id=target_id), probe


def _print_execution_configuration(payload: dict[str, object], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(f"Execution configuration: {payload['target_id']}")
    print(f"Host: {payload['host']}")
    print(f"Capability: {payload['capability_state']}")
    print(f"Reason: {payload['reason']}")
    print(f"Sealed identity: {payload['sealed_identity']}")
    print(f"Mutated: {'yes' if payload['mutated'] else 'no'}")
    print("Model invocations: 0")


def _execution_archive_current(
    coordination: dict[str, object], control: dict[str, object]
) -> dict[str, object]:
    updated = _execution_copy(coordination)
    raw_history = updated.get("execution_control_history", [])
    if not isinstance(raw_history, list):
        raise ValueError("execution_control_history must be a list")
    history = [_execution_copy(item) for item in raw_history if isinstance(item, dict)]
    snapshot_identity = _execution_hash(control)
    if all(_execution_hash(item) != snapshot_identity for item in history):
        history.append(_execution_copy(control))
    updated["execution_control_history"] = history
    return updated


def cmd_execution_configure(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        coordination = _coordination_load_state(root, args.id)
        control, probe = _execution_configure_payload(root, args.id, Path(args.config).resolve())
        existing_raw = coordination.get("execution_control")
        existing = (
            _execution_validate_control(existing_raw, work_id=args.id)
            if existing_raw is not None
            else None
        )
        if isinstance(existing, dict) and existing["sealed_identity"] == control["sealed_identity"]:
            mutated = False
            sealed_identity = existing["sealed_identity"]
        else:
            updated = (
                _execution_archive_current(coordination, existing)
                if isinstance(existing, dict)
                else _execution_copy(coordination)
            )
            updated["execution_control"] = control
            _coordination_write_state(root, args.id, updated)
            mutated = True
            sealed_identity = control["sealed_identity"]
        capability = control["capability"]
        assert isinstance(capability, dict)
        payload = {
            "schema_version": EXECUTION_OPERATOR_CONFIG_SCHEMA_VERSION,
            "target_id": args.id,
            "host": capability["host"],
            "version": capability["version"],
            "capability_state": probe.get("state"),
            "reason": probe.get("reason"),
            "configuration_identity": capability["configuration_identity"],
            "sealed_identity": sealed_identity,
            "mutated": mutated,
            "executed": False,
            "model_invocations": 0,
        }
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_EXECUTION_CONFIG_INVALID: {exc}") from exc
    _print_execution_configuration(payload, args.format)
    if payload["capability_state"] != "verified":
        raise SystemExit(2)


def cmd_execution_disable(args: argparse.Namespace) -> None:
    root = Path.cwd()
    try:
        coordination = _coordination_load_state(root, args.id)
        control = _execution_validate_control(
            coordination.get("execution_control"), work_id=args.id
        )
        capability = control["capability"]
        assert isinstance(capability, dict)
        settings = capability.get("settings")
        if not isinstance(settings, dict):
            raise ValueError("configured execution authority has no packaged adapter settings")
        if settings.get("enabled") is False:
            mutated = False
        else:
            updated_control = _execution_copy(control)
            updated_capability = updated_control["capability"]
            assert isinstance(updated_capability, dict)
            updated_settings = updated_capability["settings"]
            assert isinstance(updated_settings, dict)
            updated_settings["enabled"] = False
            updated_capability["configuration_identity"] = _execution_hash(updated_settings)
            updated_capability["controls"] = {
                name: {
                    "state": "unsupported",
                    "unit": name,
                    "source": "operator disabled the packaged adapter",
                }
                for name in EXECUTION_REQUIRED_CAPABILITY_CONTROLS
            }
            updated_control["sealed_identity"] = _execution_hash(
                _execution_sealed_payload(updated_control)
            )
            updated_control["receipts"] = []
            _execution_validate_control(updated_control, work_id=args.id)
            updated_coordination = _execution_archive_current(coordination, control)
            updated_coordination["execution_control"] = updated_control
            _coordination_write_state(root, args.id, updated_coordination)
            control = updated_control
            capability = updated_capability
            mutated = True
        payload = {
            "schema_version": EXECUTION_OPERATOR_CONFIG_SCHEMA_VERSION,
            "target_id": args.id,
            "host": capability["host"],
            "capability_state": "disabled",
            "reason": "Packaged host adapter is disabled in the sealed authority.",
            "configuration_identity": capability["configuration_identity"],
            "sealed_identity": control["sealed_identity"],
            "mutated": mutated,
            "executed": False,
            "model_invocations": 0,
        }
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PW_EXECUTION_DISABLE_INVALID: {exc}") from exc
    _print_execution_configuration(payload, args.format)


def cmd_execution_status(args: argparse.Namespace) -> None:
    payload = _execution_control_projection(Path.cwd(), args.id, "material-execution")
    _print_execution_projection(payload, args.format)
    if payload["state"] == "blocked":
        raise SystemExit(2)
