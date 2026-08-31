from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from project_workflow import codex_adapter


def codex_settings(tmp_path: Path, **overrides: object) -> dict[str, object]:
    executable = tmp_path / "codex"
    executable.write_bytes(b"sealed codex fixture\n")
    executable.chmod(0o700)
    settings: dict[str, object] = {
        "schema_version": codex_adapter.CODEX_ADAPTER_SCHEMA_VERSION,
        "adapter_kind": codex_adapter.CODEX_ADAPTER_KIND,
        "enabled": True,
        "trust": "trusted-local",
        "executable": str(executable),
        "executable_identity": "sha256:" + hashlib.sha256(executable.read_bytes()).hexdigest(),
        "expected_version": "codex-cli fixture",
        "model": "fixture-model",
        "prompt": "Make the bounded fixture change.",
        "allowed_tools": ["Bash", "apply_patch"],
        "allowed_command_patterns": [r"git status --short"],
        "test_command_patterns": [],
        "required_changed_paths": [],
    }
    settings.update(overrides)
    return settings


def clean_repo(tmp_path: Path) -> Path:
    root = tmp_path / "workspace"
    root.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    (root / "README.md").write_text("candidate\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
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


def test_git_source_check_excludes_coordinator_state_but_not_product_changes(
    tmp_path: Path,
) -> None:
    root = clean_repo(tmp_path)
    coordination = root / ".project-workflow/tasks/TASK-001-Test/COORDINATION.json"
    coordination.parent.mkdir(parents=True)
    (coordination.parent / "REQUIREMENTS.md").write_text("# Fixture\n", encoding="utf-8")
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
            "workflow item",
        ],
        cwd=root,
        check=True,
    )
    coordination.write_text("{}\n", encoding="utf-8")
    assert codex_adapter._git_changed_paths(root) == set()

    (root / "README.md").write_text("changed\n", encoding="utf-8")
    nested = root / "src" / "canary.txt"
    nested.parent.mkdir()
    nested.write_text("canary\n", encoding="utf-8")
    assert codex_adapter._git_changed_paths(root) == {"README.md", "src/canary.txt"}


def adapter_control(root: Path, settings: dict[str, object]) -> dict[str, object]:
    maxima = {
        "elapsed-seconds": 30,
        "agent-budget": 10,
        "turns": 1,
        "tool-calls": 3,
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
            "native_unit": "tokens" if name == "agent-budget" else name,
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
            "configuration_identity": codex_adapter._identity(settings),
            "settings": settings,
        },
        "sealed_identity": "fixture-sealed-control",
    }


def test_read_only_inspection_never_executes_configured_binary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def reject_execution(*args: object, **kwargs: object) -> None:
        raise AssertionError("read-only inspection executed configured code")

    monkeypatch.setattr(subprocess, "run", reject_execution)
    settings = codex_settings(tmp_path)

    inspected = codex_adapter.inspect_codex_capability(settings)

    assert inspected["state"] == "inspectable"
    assert inspected["configuration_identity"] == codex_adapter._identity(settings)


def test_inspection_rejects_unsealed_or_misnamed_executable(tmp_path: Path) -> None:
    settings = codex_settings(tmp_path)
    executable = Path(str(settings["executable"]))
    executable.write_bytes(b"changed executable\n")
    assert codex_adapter.inspect_codex_capability(settings)["state"] == "unsupported"

    misnamed = tmp_path / "helper"
    misnamed.write_bytes(b"fixture\n")
    misnamed.chmod(0o700)
    settings["executable"] = str(misnamed)
    settings["executable_identity"] = "sha256:" + hashlib.sha256(misnamed.read_bytes()).hexdigest()
    with pytest.raises(codex_adapter.CodexAdapterError, match="codex binary"):
        codex_adapter.validate_codex_settings(settings)


def test_material_probe_checks_current_codex_contract(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = codex_settings(tmp_path)
    executable = str(settings["executable"])
    observed: list[list[str]] = []

    def fake_run(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        observed.append(argv)
        if argv == [executable, "--version"]:
            return subprocess.CompletedProcess(argv, 0, "codex-cli fixture\n", "")
        if argv == [executable, "app-server", "--help"]:
            return subprocess.CompletedProcess(argv, 0, "--listen stdio://", "")
        if argv == [executable, "exec", "--help"]:
            return subprocess.CompletedProcess(argv, 0, "--output-schema --json", "")
        raise AssertionError(f"unexpected probe command: {argv}")

    monkeypatch.setattr(subprocess, "run", fake_run)

    probed = codex_adapter.probe_codex_capability(settings)

    assert probed["state"] == "verified"
    assert observed == [
        [executable, "--version"],
        [executable, "app-server", "--help"],
        [executable, "exec", "--help"],
    ]


def test_hook_reserves_retries_workers_and_write_scope_atomically(tmp_path: Path) -> None:
    root = clean_repo(tmp_path)
    settings = codex_settings(
        tmp_path,
        allowed_tools=["exec_command", "apply_patch", "spawn_agent"],
        allowed_command_patterns=[r"pytest -q", r"git status --short"],
        test_command_patterns=[r"pytest -q"],
    )
    control = adapter_control(root, settings)

    retry_state = tmp_path / "retry.sqlite3"
    codex_adapter._initialize_state(retry_state, control)
    event = {"tool_name": "exec_command", "tool_input": {"cmd": "pytest -q"}}
    assert codex_adapter._reserve_pre_tool(control, settings, retry_state, root, event) is None
    denied = codex_adapter._reserve_pre_tool(control, settings, retry_state, root, event)
    assert denied == "Codex identical test retry authority is exhausted."
    sticky = codex_adapter._reserve_pre_tool(
        control,
        settings,
        retry_state,
        root,
        {"tool_name": "exec_command", "tool_input": {"cmd": "git status --short"}},
    )
    assert sticky == denied

    worker_state = tmp_path / "worker.sqlite3"
    codex_adapter._initialize_state(worker_state, control)
    worker = codex_adapter._reserve_pre_tool(
        control,
        settings,
        worker_state,
        root,
        {"tool_name": "spawn_agent", "tool_input": {"message": "expand scope"}},
    )
    assert worker == "Codex worker-launch authority is exhausted."

    patch_state = tmp_path / "patch.sqlite3"
    codex_adapter._initialize_state(patch_state, control)
    outside = codex_adapter._reserve_pre_tool(
        control,
        settings,
        patch_state,
        root,
        {
            "tool_name": "apply_patch",
            "tool_input": {"input": "*** Begin Patch\n*** Update File: README.md\n*** End Patch"},
        },
    )
    assert outside == "Codex patch exceeds sealed write scope: README.md"

    absolute_state = tmp_path / "absolute.sqlite3"
    codex_adapter._initialize_state(absolute_state, control)
    allowed = codex_adapter._reserve_pre_tool(
        control,
        settings,
        absolute_state,
        root,
        {
            "tool_name": "apply_patch",
            "tool_input": {
                "input": (
                    "*** Begin Patch\n*** Add File: "
                    f"{root / 'src/canary.txt'}\n+candidate\n*** End Patch"
                )
            },
        },
    )
    assert allowed is None
    assert codex_adapter._state_snapshot(absolute_state)["changed_paths"] == ["src/canary.txt"]

    scope_state = tmp_path / "scope.sqlite3"
    codex_adapter._initialize_state(scope_state, control)
    (root / "outside.txt").write_text("unexpected\n", encoding="utf-8")
    codex_adapter._post_tool_check(control, scope_state, root)
    snapshot = codex_adapter._state_snapshot(scope_state)
    assert snapshot["status"] == "blocked"
    assert snapshot["reason"] == "Codex tool changed paths outside sealed scope: outside.txt"


def test_hook_rejects_event_from_workspace_outside_sealed_root(tmp_path: Path) -> None:
    root = clean_repo(tmp_path)
    outside = tmp_path / "other-workspace"
    outside.mkdir()
    settings = codex_settings(tmp_path)
    control = adapter_control(root, settings)
    control["adapter_workspace_root"] = str(root.resolve())

    assert codex_adapter._event_workspace_root(control, {"cwd": str(root)}) == root
    with pytest.raises(codex_adapter.CodexAdapterError, match="sealed workspace root"):
        codex_adapter._event_workspace_root(control, {"cwd": str(outside)})


def test_runtime_hook_inventory_fails_closed_when_one_binding_hook_is_missing(
    tmp_path: Path,
) -> None:
    root = clean_repo(tmp_path)

    class MissingHookRpc:
        def request(
            self,
            method: str,
            params: dict[str, object],
            request_id: int,
            timeout: float,
        ) -> dict[str, object]:
            assert method == "hooks/list"
            assert params == {"cwds": [str(root)]}
            return {
                "data": [
                    {
                        "hooks": [
                            {
                                "eventName": name,
                                "enabled": True,
                                "command": "sealed-hook",
                            }
                            for name in ("sessionStart", "preToolUse")
                        ]
                    }
                ]
            }

    with pytest.raises(codex_adapter.CodexAdapterError, match="postToolUse"):
        codex_adapter._verify_runtime_hooks(MissingHookRpc(), root, "sealed-hook", 1)


def test_adapter_ephemeral_state_is_removed_after_early_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = clean_repo(tmp_path)
    settings = codex_settings(tmp_path)
    control = adapter_control(root, settings)
    state_dir = tmp_path / "adapter-state"

    def create_state_dir(*, prefix: str) -> str:
        assert prefix == "project-workflow-codex-"
        state_dir.mkdir()
        return str(state_dir)

    monkeypatch.setattr(codex_adapter.tempfile, "mkdtemp", create_state_dir)
    control["capability"] = {}

    with pytest.raises(codex_adapter.CodexAdapterError):
        codex_adapter.run_codex_adapter(root, control)
    assert not state_dir.exists()


def test_adapter_ephemeral_state_is_removed_for_any_inner_lifecycle_exception(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = clean_repo(tmp_path)
    control = adapter_control(root, codex_settings(tmp_path))
    state_dir = tmp_path / "adapter-lifecycle-state"

    def create_state_dir(*, prefix: str) -> str:
        assert prefix == "project-workflow-codex-"
        state_dir.mkdir()
        return str(state_dir)

    def fail_inner(
        root_value: Path, control_value: dict[str, object], state_value: Path
    ) -> dict[str, object]:
        assert root_value == root
        assert control_value == control
        assert state_value == state_dir
        raise codex_adapter.CodexAdapterError("fixture lifecycle failure")

    monkeypatch.setattr(codex_adapter.tempfile, "mkdtemp", create_state_dir)
    monkeypatch.setattr(codex_adapter, "_run_codex_adapter", fail_inner)

    with pytest.raises(codex_adapter.CodexAdapterError, match="lifecycle failure"):
        codex_adapter.run_codex_adapter(root, control)
    assert not state_dir.exists()


def test_app_server_supervisor_interrupts_on_native_token_limit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = clean_repo(tmp_path)
    settings = codex_settings(tmp_path)
    control = adapter_control(root, settings)

    monkeypatch.setenv("OPENAI_API_KEY", "fixture-key")
    monkeypatch.setattr(
        codex_adapter,
        "probe_codex_capability",
        lambda value: {
            "state": "verified",
            "host": "codex",
            "version": settings["expected_version"],
            "configuration_identity": codex_adapter._identity(settings),
            "controls": {},
            "reason": "fixture",
        },
    )
    monkeypatch.setattr(
        codex_adapter,
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
        },
    )

    class FakeRpc:
        def __init__(self, argv: list[str], **kwargs: object) -> None:
            assert argv == [
                str(settings["executable"]),
                "--enable",
                "hooks",
                "app-server",
                "--listen",
                "stdio://",
            ]
            self.process = SimpleNamespace(poll=lambda: None)
            self.stderr: list[str] = []
            self.interrupted = False
            self.delivered_usage = False
            environment = kwargs["env"]
            assert isinstance(environment, dict)
            hooks = json.loads(
                (Path(str(environment["CODEX_HOME"])) / "hooks.json").read_text(encoding="utf-8")
            )
            permission_config = (Path(str(environment["CODEX_HOME"])) / "config.toml").read_text(
                encoding="utf-8"
            )
            assert 'default_permissions = "project-workflow-sealed"' in permission_config
            assert "[permissions.project-workflow-sealed.network]" in permission_config
            assert "enabled = false" in permission_config
            self.hook_command = hooks["hooks"]["SessionStart"][0]["hooks"][0]["command"]

        def request(
            self,
            method: str,
            params: dict[str, object],
            request_id: int,
            timeout: float,
        ) -> dict[str, object]:
            if method == "initialize":
                assert params["capabilities"] == {"experimentalApi": True}
                return {}
            if method == "thread/start":
                assert params["config"] == {"bypass_hook_trust": True}
                assert params["runtimeWorkspaceRoots"] == [str(root)]
                assert params["permissions"] == "project-workflow-sealed"
                return {"thread": {"id": "thread-fixture"}}
            if method == "hooks/list":
                return {
                    "data": [
                        {
                            "hooks": [
                                {
                                    "eventName": name,
                                    "enabled": True,
                                    "command": self.hook_command,
                                }
                                for name in (
                                    "sessionStart",
                                    "preToolUse",
                                    "postToolUse",
                                )
                            ]
                        }
                    ]
                }
            if method == "turn/start":
                assert params["runtimeWorkspaceRoots"] == [str(root)]
                assert params["permissions"] == "project-workflow-sealed"
                return {"turn": {"id": "turn-fixture"}}
            raise AssertionError(f"unexpected request: {method}")

        def send(
            self,
            method: str,
            params: dict[str, object],
            request_id: int | None = None,
        ) -> None:
            if method == "turn/interrupt":
                self.interrupted = True

        def receive(self, timeout: float) -> dict[str, object] | None:
            if not self.delivered_usage:
                self.delivered_usage = True
                return {
                    "method": "thread/tokenUsage/updated",
                    "params": {"tokenUsage": {"total": {"totalTokens": 11}}},
                }
            if self.interrupted:
                return {
                    "method": "turn/completed",
                    "params": {"turn": {"id": "turn-fixture", "status": "interrupted"}},
                }
            return None

        def stop(self) -> None:
            return None

    monkeypatch.setattr(codex_adapter, "_JsonRpcProcess", FakeRpc)

    result = codex_adapter.run_codex_adapter(root, control)

    assert result["terminal_status"] == "interrupted"
    assert result["terminal_reason"] == "Codex token authority is exhausted."
    assert result["hook_active"] is True
    assert result["native_metrics"]["agent-budget"] == 11
    assert result["final_source_revision"] == control["source_revision"]
    assert result["final_changed_paths"] == []


def test_remaining_authority_includes_prior_typed_receipts() -> None:
    control = {
        "limits": {
            "tool-calls": {
                "state": "verified",
                "maximum": 5,
                "consumed": 1,
            }
        },
        "receipts": [
            {"native_metrics": {"tool-calls": 2}},
            {"native_metrics": {"tool-calls": 1}},
        ],
    }

    assert codex_adapter._maximum(control, "tool-calls") == 1
    control["receipts"].append({"native_metrics": {"tool-calls": 1}})
    assert codex_adapter._maximum(control, "tool-calls") == 0


def test_packaged_plugin_is_subordinate_and_prototype_surfaces_are_absent() -> None:
    root = Path(__file__).parents[1]
    plugin = root / "src/project_workflow/codex_plugin/project-workflow-execution-control"
    assert (plugin / ".codex-plugin/plugin.json").is_file()
    handler = plugin / "scripts/project-workflow-codex-hook"
    assert handler.is_file()
    assert handler.stat().st_mode & 0o111
    shipped = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (root / "src/project_workflow").rglob("*")
        if path.is_file() and path.suffix in {".py", ".json", ".md", ""}
    ).lower()
    assert "limit_tokens = 80000" not in shipped
    assert "project-workflow-enforcement" not in shipped
    assert "console_scripts.project-enforce" not in shipped
