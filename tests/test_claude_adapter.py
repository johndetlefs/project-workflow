from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from project_workflow import claude_adapter


def claude_settings(tmp_path: Path, **overrides: object) -> dict[str, object]:
    executable = tmp_path / "claude"
    executable.write_bytes(b"sealed claude fixture\n")
    executable.chmod(0o700)
    settings: dict[str, object] = {
        "schema_version": claude_adapter.CLAUDE_ADAPTER_SCHEMA_VERSION,
        "adapter_kind": claude_adapter.CLAUDE_ADAPTER_KIND,
        "enabled": True,
        "trust": "trusted-local",
        "executable": str(executable),
        "executable_identity": "sha256:" + hashlib.sha256(executable.read_bytes()).hexdigest(),
        "expected_version": "2.1.217 (Claude Code)",
        "model": "fixture-model",
        "prompt": "Make the bounded fixture change.",
        "allowed_tools": ["Bash", "Edit", "Write"],
        "disallowed_tools": ["WebFetch", "WebSearch"],
        "allowed_command_patterns": [r"git status --short", r"pytest -q"],
        "test_command_patterns": [r"pytest -q"],
        "required_changed_paths": [],
        "required_output_identities": {},
        "required_validation_commands": [],
    }
    settings.update(overrides)
    return settings


def clean_repo(tmp_path: Path) -> Path:
    root = tmp_path / "workspace"
    root.mkdir()
    (root / "src").mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    (root / "README.md").write_text("candidate\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-qm",
            "candidate",
        ],
        cwd=root,
        check=True,
    )
    return root


def adapter_control(root: Path, settings: dict[str, object]) -> dict[str, object]:
    maxima = {
        "elapsed-seconds": 30,
        "agent-budget": 2_000_000,
        "turns": 3,
        "tool-calls": 4,
        "test-invocations": 2,
        "identical-retries": 0,
        "worker-launches": 0,
        "changed-paths": 1,
        "write-scope": 0,
    }
    limits = {
        name: {
            "state": "verified",
            "maximum": maximum,
            "consumed": 0,
            "native_unit": (
                "usd-micros"
                if name == "agent-budget"
                else "turns" if name == "turns" else name
            ),
            "source": "fixture",
        }
        for name, maximum in maxima.items()
    }
    source_revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    return {
        "source_revision": source_revision,
        "allowed_write_paths": ["src/**"],
        "limits": limits,
        "receipts": [],
        "capability": {
            "configuration_identity": claude_adapter._identity(settings),
            "settings": settings,
        },
        "sealed_identity": "fixture-sealed-control",
        "proof_obligations": [],
    }


def test_read_only_inspection_never_executes_configured_binary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def reject_execution(*args: object, **kwargs: object) -> None:
        raise AssertionError("read-only inspection executed configured code")

    monkeypatch.setattr(subprocess, "run", reject_execution)
    settings = claude_settings(tmp_path)

    inspected = claude_adapter.inspect_claude_capability(settings)

    assert inspected["state"] == "inspectable"
    assert inspected["classification"] == "inspectable"
    assert inspected["configuration_identity"] == claude_adapter._identity(settings)


@pytest.mark.parametrize(
    ("overrides", "classification"),
    [
        ({"enabled": False}, "disabled"),
        ({"trust": "untrusted"}, "untrusted"),
    ],
)
def test_inspection_reports_precise_non_support_states(
    tmp_path: Path, overrides: dict[str, object], classification: str
) -> None:
    inspected = claude_adapter.inspect_claude_capability(
        claude_settings(tmp_path, **overrides)
    )
    assert inspected["state"] == "unsupported"
    assert inspected["classification"] == classification


def test_material_probe_checks_cli_and_auth_without_a_model_request(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = claude_settings(tmp_path)
    executable = str(settings["executable"])
    observed: list[list[str]] = []

    def fake_run(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        observed.append(argv)
        if argv == [executable, "--version"]:
            return subprocess.CompletedProcess(argv, 0, "2.1.217 (Claude Code)\n", "")
        if argv == [executable, "auth", "status"]:
            return subprocess.CompletedProcess(argv, 0, "authenticated\n", "")
        raise AssertionError(f"unexpected probe command: {argv}")

    monkeypatch.setattr(subprocess, "run", fake_run)

    probed = claude_adapter.probe_claude_capability(settings)

    assert probed["state"] == "verified"
    assert observed == [
        [executable, "--version"],
        [executable, "auth", "status"],
    ]


def test_hook_enforces_write_command_retry_worker_and_workspace_scope(tmp_path: Path) -> None:
    root = clean_repo(tmp_path)
    settings = claude_settings(tmp_path, allowed_tools=["Bash", "Edit", "Agent"])
    control = adapter_control(root, settings)

    write_state = tmp_path / "write.sqlite3"
    claude_adapter._initialize_state(write_state, control)
    assert (
        claude_adapter._reserve_pre_tool(
            control,
            settings,
            write_state,
            root,
            {"tool_name": "Edit", "tool_input": {"file_path": str(root / "src/a.py")}},
        )
        is None
    )
    denied_write = claude_adapter._reserve_pre_tool(
        control,
        settings,
        write_state,
        root,
        {"tool_name": "Edit", "tool_input": {"file_path": str(root / "README.md")}},
    )
    assert denied_write == "Claude write exceeds sealed scope: README.md"

    retry_state = tmp_path / "retry.sqlite3"
    claude_adapter._initialize_state(retry_state, control)
    test_event = {"tool_name": "Bash", "tool_input": {"command": "pytest -q"}}
    assert claude_adapter._reserve_pre_tool(control, settings, retry_state, root, test_event) is None
    assert claude_adapter._reserve_pre_tool(
        control, settings, retry_state, root, test_event
    ) == "Claude identical test retry authority is exhausted."

    worker_state = tmp_path / "worker.sqlite3"
    claude_adapter._initialize_state(worker_state, control)
    assert claude_adapter._reserve_pre_tool(
        control,
        settings,
        worker_state,
        root,
        {"tool_name": "Agent", "tool_input": {"prompt": "expand scope"}},
    ) == "Claude worker-launch authority is exhausted."

    sealed = {**control, "adapter_workspace_root": str(root.resolve())}
    outside = tmp_path / "outside"
    outside.mkdir()
    assert claude_adapter._event_workspace_root(sealed, {"cwd": str(root)}) == root
    with pytest.raises(claude_adapter.ClaudeAdapterError, match="sealed workspace root"):
        claude_adapter._event_workspace_root(sealed, {"cwd": str(outside)})


def test_print_supervisor_uses_native_limits_and_requires_hook_activation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = clean_repo(tmp_path)
    settings = claude_settings(tmp_path)
    control = adapter_control(root, settings)
    monkeypatch.setattr(
        claude_adapter,
        "probe_claude_capability",
        lambda value: {
            "state": "verified",
            "host": "claude-code",
            "version": settings["expected_version"],
            "configuration_identity": claude_adapter._identity(settings),
            "controls": {},
            "reason": "fixture",
        },
    )
    monkeypatch.setattr(
        claude_adapter,
        "_state_snapshot",
        lambda path: {
            "status": "running",
            "reason": "",
            "hook_active": True,
            "tool_calls": 1,
            "test_invocations": 0,
            "worker_launches": 0,
            "changed_paths": [],
            "identical_retries": 0,
            "hook_events": [{"event_name": "SessionStart"}],
        },
    )
    monkeypatch.setattr(claude_adapter, "_run_hook_preflight", lambda *args: None)

    class FakeStream:
        def __init__(self, argv: list[str], **kwargs: object) -> None:
            self.argv = argv
            self.stderr: list[str] = []
            self.protocol_events = [{"type": "system", "subtype": "init"}]
            self.messages = [
                {
                    "type": "system",
                    "subtype": "init",
                    "session_id": "session-fixture",
                    "plugin_errors": [],
                },
                {
                    "type": "result",
                    "subtype": "success",
                    "is_error": False,
                    "session_id": "session-fixture",
                    "total_cost_usd": 1.25,
                    "num_turns": 2,
                    "usage": {"input_tokens": 10, "output_tokens": 5},
                },
            ]
            assert "--output-format" in argv and "stream-json" in argv
            assert argv[argv.index("--max-turns") + 1] == "3"
            assert argv[argv.index("--max-budget-usd") + 1] == "2"
            assert "--include-hook-events" in argv
            assert "--plugin-dir" in argv
            assert "--allowedTools" in argv
            assert "--disallowedTools" in argv
            assert argv[argv.index("--permission-mode") + 1] == "dontAsk"
            assert "bypassPermissions" not in argv
            env = kwargs["env"]
            assert isinstance(env, dict)
            assert env["PROJECT_WORKFLOW_CLAUDE_CONTROL"]
            assert env["PROJECT_WORKFLOW_CLAUDE_STATE"]

        def receive(self, timeout: float) -> dict[str, object] | None:
            return self.messages.pop(0) if self.messages else None

        def poll(self) -> int | None:
            return None

        def stop(self) -> None:
            return None

    monkeypatch.setattr(claude_adapter, "_StreamProcess", FakeStream)

    result = claude_adapter.run_claude_adapter(root, control)

    assert result["terminal_status"] == "completed"
    assert result["hook_active"] is True
    assert result["session_id"] == "session-fixture"
    assert result["native_metrics"]["agent-budget"] == 1_250_000
    assert result["native_metrics"]["turns"] == 2


def test_successful_stream_without_hook_activation_is_not_supported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = clean_repo(tmp_path)
    settings = claude_settings(tmp_path)
    control = adapter_control(root, settings)
    monkeypatch.setattr(
        claude_adapter,
        "probe_claude_capability",
        lambda value: {
            "state": "verified",
            "version": settings["expected_version"],
            "configuration_identity": claude_adapter._identity(settings),
        },
    )
    monkeypatch.setattr(
        claude_adapter,
        "_state_snapshot",
        lambda path: {
            "status": "running",
            "reason": "",
            "hook_active": False,
            "tool_calls": 0,
            "test_invocations": 0,
            "worker_launches": 0,
            "changed_paths": [],
            "identical_retries": 0,
            "hook_events": [],
        },
    )
    monkeypatch.setattr(claude_adapter, "_run_hook_preflight", lambda *args: None)

    class FakeStream:
        stderr: list[str] = []
        protocol_events: list[dict[str, object]] = []

        def __init__(self, argv: list[str], **kwargs: object) -> None:
            self.messages = [
                {"type": "system", "subtype": "init", "plugin_errors": []},
                {
                    "type": "result",
                    "subtype": "success",
                    "total_cost_usd": 0,
                    "num_turns": 1,
                },
            ]

        def receive(self, timeout: float) -> dict[str, object] | None:
            return self.messages.pop(0) if self.messages else None

        def poll(self) -> int | None:
            return None

        def stop(self) -> None:
            return None

    monkeypatch.setattr(claude_adapter, "_StreamProcess", FakeStream)
    result = claude_adapter.run_claude_adapter(root, control)
    assert result["terminal_status"] == "failed"
    assert "hook activation was not observed" in result["terminal_reason"]


def test_successful_stream_with_wrong_required_output_is_not_completed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = clean_repo(tmp_path)
    settings = claude_settings(
        tmp_path,
        required_output_identities={"src/result.txt": "sha256:" + "0" * 64},
    )
    control = adapter_control(root, settings)
    control["proof_obligations"] = ["semantic-output"]
    monkeypatch.setattr(
        claude_adapter,
        "probe_claude_capability",
        lambda value: {
            "state": "verified",
            "version": settings["expected_version"],
            "configuration_identity": claude_adapter._identity(settings),
        },
    )
    monkeypatch.setattr(claude_adapter, "_run_hook_preflight", lambda *args: None)
    monkeypatch.setattr(
        claude_adapter,
        "_state_snapshot",
        lambda path: {
            "status": "running",
            "reason": "",
            "hook_active": True,
            "tool_calls": 0,
            "test_invocations": 0,
            "worker_launches": 0,
            "changed_paths": [],
            "identical_retries": 0,
            "hook_events": [{"event_name": "SessionStart"}],
        },
    )

    class FakeStream:
        stderr: list[str] = []
        protocol_events: list[dict[str, object]] = []

        def __init__(self, argv: list[str], **kwargs: object) -> None:
            self.messages = [
                {"type": "system", "subtype": "init", "plugin_errors": []},
                {
                    "type": "result",
                    "subtype": "success",
                    "total_cost_usd": 0,
                    "num_turns": 1,
                },
            ]

        def receive(self, timeout: float) -> dict[str, object] | None:
            return self.messages.pop(0) if self.messages else None

        def poll(self) -> int | None:
            return None

        def stop(self) -> None:
            return None

    monkeypatch.setattr(claude_adapter, "_StreamProcess", FakeStream)

    result = claude_adapter.run_claude_adapter(root, control)

    assert result["terminal_status"] == "interrupted"
    assert "required" in result["terminal_reason"].lower()


def test_ephemeral_state_is_removed_after_any_lifecycle_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = clean_repo(tmp_path)
    control = adapter_control(root, claude_settings(tmp_path))
    state_dir = tmp_path / "adapter-state"

    def create_state_dir(*, prefix: str) -> str:
        assert prefix == "project-workflow-claude-"
        state_dir.mkdir()
        return str(state_dir)

    monkeypatch.setattr(claude_adapter.tempfile, "mkdtemp", create_state_dir)
    monkeypatch.setattr(
        claude_adapter,
        "_run_claude_adapter",
        lambda *args: (_ for _ in ()).throw(claude_adapter.ClaudeAdapterError("fixture")),
    )

    with pytest.raises(claude_adapter.ClaudeAdapterError, match="fixture"):
        claude_adapter.run_claude_adapter(root, control)
    assert not state_dir.exists()


def test_packaged_claude_plugin_is_subordinate_and_executable() -> None:
    root = Path(__file__).parents[1]
    plugin = root / "src/project_workflow/claude_plugin/project-workflow-execution-control"
    assert (plugin / ".claude-plugin/plugin.json").is_file()
    hooks = (plugin / "hooks/hooks.json").read_text(encoding="utf-8")
    assert all(
        name in hooks
        for name in (
            "SessionStart",
            "PreToolUse",
            "PostToolUse",
            "PostToolUseFailure",
            "PostToolBatch",
            "Stop",
        )
    )
    handler = plugin / "scripts/project-workflow-claude-hook"
    assert handler.stat().st_mode & 0o111
    environment = os.environ.copy()
    environment.pop("PROJECT_WORKFLOW_CLAUDE_PYTHON", None)
    environment.pop("PROJECT_WORKFLOW_CLAUDE_ADAPTER", None)
    missing_interpreter = subprocess.run(
        [str(handler)],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )
    assert missing_interpreter.returncode == 2
    assert "project execute" in (plugin / "README.md").read_text(encoding="utf-8")


def test_native_permissions_are_path_and_exact_command_scoped(tmp_path: Path) -> None:
    settings = claude_settings(tmp_path, allowed_tools=["Read", "Edit", "Bash"])
    rules = claude_adapter._native_permission_rules(
        settings, {"allowed_write_paths": ["src/**"]}
    )
    assert rules == [
        "Read",
        "Edit(/src/**)",
        "Bash(git status --short)",
        "Bash(pytest -q)",
    ]
    regex_settings = claude_settings(
        tmp_path,
        allowed_tools=["Bash"],
        allowed_command_patterns=[r"pytest .*"],
    )
    with pytest.raises(claude_adapter.ClaudeAdapterError, match="exact literal commands"):
        claude_adapter._native_permission_rules(regex_settings, {"allowed_write_paths": []})
    worker_settings = claude_settings(tmp_path, allowed_tools=["Agent"])
    with pytest.raises(claude_adapter.ClaudeAdapterError, match="no fail-closed"):
        claude_adapter._native_permission_rules(worker_settings, {"allowed_write_paths": []})


def test_stream_process_terminates_descendants_and_drains_terminal_output(tmp_path: Path) -> None:
    child_script = (
        "import json,subprocess,sys,time;"
        "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']);"
        "print(json.dumps({'type':'fixture','pid':child.pid}),flush=True);"
        "time.sleep(60)"
    )
    process = claude_adapter._StreamProcess(
        [sys.executable, "-c", child_script], cwd=tmp_path, env=os.environ.copy()
    )
    message = process.receive(3)
    assert message is not None
    child_pid = int(message["pid"])
    process.stop()
    child_alive = True
    for _ in range(20):
        try:
            os.kill(child_pid, 0)
        except ProcessLookupError:
            child_alive = False
            break
        time.sleep(0.05)
    assert not child_alive

    result_script = (
        "import json;"
        "print(json.dumps({'type':'result','subtype':'success','num_turns':1}),flush=True)"
    )
    completed = claude_adapter._StreamProcess(
        [sys.executable, "-c", result_script], cwd=tmp_path, env=os.environ.copy()
    )
    completed.process.wait(timeout=3)
    completed.stop()
    drained = completed.drain()
    assert any(item.get("type") == "result" for item in drained)
