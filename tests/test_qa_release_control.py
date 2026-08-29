from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

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


def fixture_repo(tmp_path: Path) -> Path:
    assert run_project(tmp_path, "init", "--agent", "codex").returncode == 0
    assert (
        run_project(
            tmp_path,
            "task",
            "init",
            "--title",
            "Bounded Release",
            "--update-tracker",
            "--status",
            "In Progress",
        ).returncode
        == 0
    )
    task_dir = tmp_path / ".project-workflow/tasks/TASK-001-Bounded-Release"
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nBound QA and fixed release.\n", encoding="utf-8"
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
        "qa-release-fixture",
        "--next-action",
        "Run bounded QA remediation.",
        "--material-verification",
        "no",
    )
    assert coordinated.returncode == 0, coordinated.stdout + coordinated.stderr
    return task_dir


def finding(finding_id: str, scope: str = "src/app.py") -> dict[str, object]:
    return {
        "id": finding_id,
        "severity": "high",
        "material": True,
        "scope": [scope],
        "source_identity": "source-before",
        "evidence_identity": "evidence-before",
        "state": "unresolved",
        "correction_identity": None,
        "affected_proof_identity": None,
    }


def execution_control(*finding_ids: str) -> dict[str, object]:
    limits = {
        unit: {
            "state": "verified",
            "maximum": index * 10,
            "consumed": 0,
            "native_unit": "tokens" if unit == "agent-budget" else unit,
            "source": "fixture policy",
        }
        for index, unit in enumerate(workflow_cli.EXECUTION_REQUIRED_LIMIT_UNITS, start=1)
    }
    controls = {
        name: {"state": "verified", "unit": name, "source": "fixture adapter"}
        for name in workflow_cli.EXECUTION_REQUIRED_CAPABILITY_CONTROLS
    }
    value: dict[str, object] = {
        "schema_version": workflow_cli.EXECUTION_CONTROL_SCHEMA_VERSION,
        "work_id": "TASK-001",
        "source_revision": "candidate-source-1",
        "phase": "qa-remediation",
        "allowed_write_paths": ["src/**", "tests/**"],
        "permitted_operations": ["qa-remediation", "candidate-promotion", "release"],
        "proof_obligations": ["affected-proof", "current-qa"],
        "limits": limits,
        "authorized_findings": [
            {
                "id": finding_id,
                "state": "unresolved",
                "material": True,
                "source_identity": "source-before",
                "evidence_identity": "evidence-before",
            }
            for finding_id in finding_ids
        ],
        "progress": {
            "attempt": 1,
            "finding_id": None,
            "baseline_source_identity": None,
            "baseline_evidence_identity": None,
            "current_source_identity": "candidate-source-1",
            "current_evidence_identity": "evidence-before",
        },
        "candidates": {
            "working_revision": "candidate-source-1",
            "verification_candidate": {
                "identity": "verification-1",
                "source_revision": "candidate-source-1",
                "proof_identity": "proof-1",
            },
            "release_candidate": None,
        },
        "capability": {
            "host": "fixture-host",
            "version": "fixture-1",
            "configuration_identity": "fixture-configuration",
            "controls": controls,
        },
        "receipts": [],
        "sealed_identity": "pending",
    }
    value["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(value)
    )
    return value


def add_execution_receipt(
    control: dict[str, object],
    *,
    kind: str,
    evidence_identity: str,
) -> str:
    candidates = control["candidates"]
    assert isinstance(candidates, dict)
    capability = control["capability"]
    assert isinstance(capability, dict)
    receipt: dict[str, object] = {
        "schema_version": workflow_cli.EXECUTION_CONTROL_SCHEMA_VERSION,
        "kind": kind,
        "work_id": control["work_id"],
        "sealed_identity": control["sealed_identity"],
        "capability_identity": workflow_cli._execution_hash(capability),
        "phase": control["phase"],
        "candidate_identity": candidates["working_revision"],
        "proof_obligations_identity": workflow_cli._execution_hash(control["proof_obligations"]),
        "source_revision": control["source_revision"],
        "operation": "qa-remediation",
        "outcome": "pass",
        "native_metrics": {"test_invocations": 1},
        "evidence_identity": evidence_identity,
        "receipt_identity": "pending",
    }
    receipt["receipt_identity"] = workflow_cli._execution_hash(
        {key: item for key, item in receipt.items() if key != "receipt_identity"}
    )
    receipts = control["receipts"]
    assert isinstance(receipts, list)
    receipts.append(receipt)
    return str(receipt["receipt_identity"])


def ready_campaign(control: dict[str, object], *finding_ids: str) -> dict[str, object]:
    campaign = workflow_cli._execution_create_qa_campaign(
        work_id="TASK-001",
        source_revision="candidate-source-1",
        verdict_identity="qa-verdict-1",
        findings=[finding(finding_id) for finding_id in finding_ids],
    )
    for index, finding_id in enumerate(finding_ids, start=1):
        current_evidence = f"evidence-after-{index}"
        correction_receipt = add_execution_receipt(
            control, kind="remediation", evidence_identity=current_evidence
        )
        affected_receipt = add_execution_receipt(
            control, kind="affected-proof", evidence_identity=f"affected-proof-{index}"
        )
        campaign = workflow_cli._execution_record_remediation(
            campaign,
            control,
            finding_id=finding_id,
            current_source_identity="candidate-source-1",
            current_evidence_identity=current_evidence,
        )
        campaign = workflow_cli._execution_close_finding(
            campaign,
            control,
            finding_id=finding_id,
            correction_identity=correction_receipt,
            affected_proof_identity=affected_receipt,
        )
    return campaign


def test_one_qa_campaign_retains_multiple_findings_and_denies_second_qa() -> None:
    campaign = workflow_cli._execution_create_qa_campaign(
        work_id="TASK-001",
        source_revision="candidate-source-1",
        verdict_identity="qa-verdict-1",
        findings=[finding("finding-1"), finding("finding-2")],
    )
    assert campaign["broad_qa_invocations"] == 1
    assert campaign["state"] == "findings-open"
    second = deepcopy(campaign)
    second["broad_qa_invocations"] = 2
    second["campaign_identity"] = workflow_cli._execution_hash(
        {key: item for key, item in second.items() if key != "campaign_identity"}
    )
    with pytest.raises(ValueError, match="exactly one broad QA"):
        workflow_cli._execution_validate_qa_campaign(second, "TASK-001")


def test_remediation_requires_sealed_scope_and_material_progress() -> None:
    campaign = workflow_cli._execution_create_qa_campaign(
        work_id="TASK-001",
        source_revision="candidate-source-1",
        verdict_identity="qa-verdict-1",
        findings=[finding("finding-1")],
    )
    control = execution_control("finding-1")
    with pytest.raises(ValueError, match="no material source or evidence progress"):
        workflow_cli._execution_record_remediation(
            campaign,
            control,
            finding_id="finding-1",
            current_source_identity="source-before",
            current_evidence_identity="evidence-before",
        )
    unsealed = execution_control()
    with pytest.raises(ValueError, match="not sealed"):
        workflow_cli._execution_record_remediation(
            campaign,
            unsealed,
            finding_id="finding-1",
            current_source_identity="source-after",
            current_evidence_identity="evidence-after",
        )
    out_of_scope_campaign = workflow_cli._execution_create_qa_campaign(
        work_id="TASK-001",
        source_revision="candidate-source-1",
        verdict_identity="qa-verdict-1",
        findings=[finding("finding-1", "outside/file.py")],
    )
    with pytest.raises(ValueError, match="outside the sealed write scope"):
        workflow_cli._execution_record_remediation(
            out_of_scope_campaign,
            control,
            finding_id="finding-1",
            current_source_identity="source-after",
            current_evidence_identity="evidence-after",
        )


def test_affected_proof_closes_findings_without_second_qa() -> None:
    control = execution_control("finding-1", "finding-2")
    campaign = ready_campaign(control, "finding-1", "finding-2")
    assert campaign["state"] == "ready-for-promotion"
    assert campaign["broad_qa_invocations"] == 1
    assert len(campaign["remediation_attempts"]) == 2
    assert all(item["state"] == "resolved" for item in campaign["findings"])


def test_remediation_fails_closed_on_phase_limits_and_unbound_proof() -> None:
    campaign = workflow_cli._execution_create_qa_campaign(
        work_id="TASK-001",
        source_revision="candidate-source-1",
        verdict_identity="qa-verdict-1",
        findings=[finding("finding-1")],
    )
    control = execution_control("finding-1")
    correction_receipt = add_execution_receipt(
        control, kind="remediation", evidence_identity="evidence-after"
    )
    exhausted = deepcopy(control)
    exhausted["limits"]["test-invocations"]["consumed"] = exhausted["limits"]["test-invocations"][
        "maximum"
    ]
    exhausted["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(exhausted)
    )
    exhausted["receipts"] = []
    with pytest.raises(ValueError, match="exhausted"):
        workflow_cli._execution_record_remediation(
            campaign,
            exhausted,
            finding_id="finding-1",
            current_source_identity="candidate-source-1",
            current_evidence_identity="evidence-after",
        )
    wrong_phase = deepcopy(control)
    wrong_phase["phase"] = "implementation"
    wrong_phase["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(wrong_phase)
    )
    wrong_phase["receipts"] = []
    with pytest.raises(ValueError, match="qa-remediation phase"):
        workflow_cli._execution_record_remediation(
            campaign,
            wrong_phase,
            finding_id="finding-1",
            current_source_identity="candidate-source-1",
            current_evidence_identity="evidence-after",
        )
    recorded = workflow_cli._execution_record_remediation(
        campaign,
        control,
        finding_id="finding-1",
        current_source_identity="candidate-source-1",
        current_evidence_identity="evidence-after",
    )
    with pytest.raises(ValueError, match="affected-proof receipt"):
        workflow_cli._execution_close_finding(
            recorded,
            control,
            finding_id="finding-1",
            correction_identity=correction_receipt,
            affected_proof_identity=workflow_cli._execution_hash({"forged": True}),
        )


def record_delivery_ready(task_dir: Path) -> None:
    (task_dir / "IMPLEMENTATION.md").write_text(
        "# Implementation Plan\n\n"
        "## Task List\n\n"
        "| ID | Title | Description | Acceptance Criteria | User Verification | Status |\n"
        "| --: | ----- | ----------- | ------------------- | ----------------- | ------ |\n"
        "| 1 | Fixture | Deliver | AC1 | Fixture | Done |\n\n"
        "## QA & Code Review\n\n- Verdict: Pass\n",
        encoding="utf-8",
    )


def test_promotion_requires_current_authority_and_is_single_candidate(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    state_path = task_dir / "COORDINATION.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    control = execution_control("finding-1")
    state["execution_control"] = control
    state["execution_qa"] = ready_campaign(control, "finding-1")
    artifact_one = workflow_cli._execution_hash({"artifact": "one"})
    artifact_two = workflow_cli._execution_hash({"artifact": "two"})
    with pytest.raises(ValueError, match="delivery-ready"):
        workflow_cli._execution_promote_release_candidate(
            tmp_path, "TASK-001", state, artifact_identity=artifact_one
        )
    record_delivery_ready(task_dir)
    promoted = workflow_cli._execution_promote_release_candidate(
        tmp_path, "TASK-001", state, artifact_identity=artifact_one
    )
    release_candidate = promoted["candidates"]["release_candidate"]
    assert release_candidate["artifact_identity"] == artifact_one
    state["execution_control"] = promoted
    assert (
        workflow_cli._execution_promote_release_candidate(
            tmp_path, "TASK-001", state, artifact_identity=artifact_one
        )["candidates"]["release_candidate"]["identity"]
        == release_candidate["identity"]
    )
    with pytest.raises(ValueError, match="different release candidate"):
        workflow_cli._execution_promote_release_candidate(
            tmp_path, "TASK-001", state, artifact_identity=artifact_two
        )


def git_candidate(tmp_path: Path) -> tuple[str, str]:
    (tmp_path / "candidate.txt").write_text("candidate\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.com",
            "commit",
            "-m",
            "candidate",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    digest = "sha256:" + hashlib.sha256((tmp_path / "candidate.txt").read_bytes()).hexdigest()
    return revision, digest


def fixed_release_plan(
    revision: str, artifact_identity: str, operations: list[dict[str, object]]
) -> dict[str, object]:
    plan: dict[str, object] = {
        "schema_version": workflow_cli.FIXED_RELEASE_SCHEMA_VERSION,
        "work_id": "TASK-001",
        "candidate_identity": "release-candidate-1",
        "source_revision": revision,
        "artifacts": {"candidate.txt": artifact_identity},
        "operations": operations,
        "elapsed_limit_seconds": 20,
        "infrastructure_retry_limit": 1,
        "attempt": {
            "state": "not-started",
            "operation_invocations": {},
            "infrastructure_retries": 0,
        },
        "terminal_receipt": None,
        "plan_identity": "pending",
    }
    plan["plan_identity"] = workflow_cli._execution_hash(
        {
            key: item
            for key, item in plan.items()
            if key not in {"plan_identity", "terminal_receipt", "attempt"}
        }
    )
    return plan


def operation(
    name: str, argv: list[str], *, infrastructure_exit_codes: list[int] | None = None
) -> dict[str, object]:
    return {
        "name": name,
        "kind": "verify",
        "argv": argv,
        "timeout_seconds": 5,
        "infrastructure_exit_codes": infrastructure_exit_codes or [],
    }


def test_fixed_release_runs_each_operation_once_and_is_terminal(tmp_path: Path) -> None:
    revision, artifact = git_candidate(tmp_path)
    plan = fixed_release_plan(
        revision,
        artifact,
        [
            operation("verify-one", [sys.executable, "-c", "raise SystemExit(0)"]),
            operation("verify-two", [sys.executable, "-c", "raise SystemExit(0)"]),
        ],
    )
    persisted: list[dict[str, object]] = []
    updated, receipt = workflow_cli._execution_run_fixed_release(
        tmp_path, plan, lambda value: persisted.append(deepcopy(value))
    )
    assert receipt["status"] == "pass"
    assert receipt["operation_invocations"] == {"verify-one": 1, "verify-two": 1}
    assert receipt["infrastructure_retries"] == 0
    assert receipt["qa_invocations"] == 0
    assert receipt["source_repairs"] == 0
    assert receipt["replacement_candidates"] == 0
    with pytest.raises(ValueError, match="already consumed"):
        workflow_cli._execution_run_fixed_release(tmp_path, updated, lambda value: None)
    assert persisted[0]["attempt"]["state"] == "running"
    assert persisted[-1]["attempt"]["state"] == "terminal"


def test_fixed_release_consumes_attempt_before_operation_and_denies_crash_retry(
    tmp_path: Path,
) -> None:
    revision, artifact = git_candidate(tmp_path)
    plan = fixed_release_plan(
        revision,
        artifact,
        [operation("publish", [sys.executable, "-c", "raise SystemExit(0)"])],
    )
    persisted: list[dict[str, object]] = []

    def crash_after_consumption(value: dict[str, object]) -> None:
        persisted.append(deepcopy(value))
        attempt = value["attempt"]
        assert isinstance(attempt, dict)
        invocations = attempt["operation_invocations"]
        assert isinstance(invocations, dict)
        if invocations.get("publish") == 1:
            raise RuntimeError("simulated controller crash")

    with pytest.raises(RuntimeError, match="simulated controller crash"):
        workflow_cli._execution_run_fixed_release(tmp_path, plan, crash_after_consumption)
    recovered = persisted[-1]
    assert recovered["attempt"]["state"] == "running"
    assert recovered["attempt"]["operation_invocations"] == {"publish": 1}
    with pytest.raises(ValueError, match="already consumed"):
        workflow_cli._execution_run_fixed_release(tmp_path, recovered, lambda value: None)


def test_fixed_release_rejects_forged_receipt_and_missing_candidate_identity(
    tmp_path: Path,
) -> None:
    (tmp_path / "candidate.txt").write_text("candidate\n", encoding="utf-8")
    artifact = "sha256:" + hashlib.sha256((tmp_path / "candidate.txt").read_bytes()).hexdigest()
    plan = fixed_release_plan(
        "fabricated-source",
        artifact,
        [operation("publish", [sys.executable, "-c", "raise SystemExit(0)"])],
    )
    _, receipt = workflow_cli._execution_run_fixed_release(tmp_path, plan, lambda value: None)
    assert receipt["status"] == "fail"
    assert "readable Git source identity" in receipt["reason"]
    forged = deepcopy(plan)
    forged["attempt"] = {
        "state": "terminal",
        "operation_invocations": {"publish": 1},
        "infrastructure_retries": 0,
    }
    forged["terminal_receipt"] = {
        "status": "pass",
        "receipt_identity": "forged",
    }
    with pytest.raises(ValueError, match="invalid shape"):
        workflow_cli._execution_validate_fixed_release(forged, "TASK-001")
    empty_artifacts = deepcopy(plan)
    empty_artifacts["artifacts"] = {}
    empty_artifacts["plan_identity"] = workflow_cli._execution_hash(
        {
            key: item
            for key, item in empty_artifacts.items()
            if key not in {"plan_identity", "terminal_receipt", "attempt"}
        }
    )
    with pytest.raises(ValueError, match="non-empty"):
        workflow_cli._execution_validate_fixed_release(empty_artifacts, "TASK-001")


def test_public_release_persists_consumed_and_terminal_state(tmp_path: Path) -> None:
    assert run_project(tmp_path, "init", "--agent", "codex").returncode == 0
    assert (
        run_project(
            tmp_path,
            "task",
            "init",
            "--title",
            "Bounded Release",
            "--update-tracker",
            "--status",
            "In Progress",
        ).returncode
        == 0
    )
    task_dir = tmp_path / ".project-workflow/tasks/TASK-001-Bounded-Release"
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nRelease one fixed candidate.\n", encoding="utf-8"
    )
    record_delivery_ready(task_dir)
    revision, artifact = git_candidate(tmp_path)
    coordinated = run_project(
        tmp_path,
        "coordinate",
        "init",
        "--id",
        "TASK-001",
        "--phase",
        "release",
        "--source-revision",
        revision,
        "--loaded-package-version",
        workflow_cli.CURRENT_PACKAGE_VERSION,
        "--loaded-asset-version",
        str(workflow_cli.CURRENT_ASSET_VERSION),
        "--loaded-contract-version",
        str(workflow_cli.COORDINATION_CONTRACT_VERSION),
        "--context-id",
        "public-release-fixture",
        "--next-action",
        "Run the fixed release.",
        "--material-verification",
        "no",
    )
    assert coordinated.returncode == 0, coordinated.stdout + coordinated.stderr
    control = execution_control()
    control["source_revision"] = revision
    control["phase"] = "release"
    candidates = control["candidates"]
    assert isinstance(candidates, dict)
    candidates["working_revision"] = revision
    candidates["verification_candidate"] = {
        "identity": "verification-1",
        "source_revision": revision,
        "proof_identity": "proof-1",
    }
    artifacts = {"candidate.txt": artifact}
    artifact_identity = workflow_cli._execution_hash(artifacts)
    candidates["release_candidate"] = {
        "identity": "release-candidate-1",
        "source_revision": revision,
        "artifact_identity": artifact_identity,
        "obligations": {
            name: workflow_cli._execution_hash({"obligation": name})
            for name in ("implementation", "verification", "qa", "affected-proof")
        },
    }
    control["sealed_identity"] = workflow_cli._execution_hash(
        workflow_cli._execution_sealed_payload(control)
    )
    plan = fixed_release_plan(
        revision,
        artifact,
        [operation("publish", ["/usr/bin/true"])],
    )
    plan["artifacts"] = artifacts
    plan["plan_identity"] = workflow_cli._execution_hash(
        {
            key: item
            for key, item in plan.items()
            if key not in {"plan_identity", "terminal_receipt", "attempt"}
        }
    )
    state_path = task_dir / "COORDINATION.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["execution_control"] = control
    state["fixed_release"] = plan
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    released = run_project(tmp_path, "release", "--id", "TASK-001", "--format", "json")
    assert released.returncode == 0, released.stdout + released.stderr
    receipt = json.loads(released.stdout)
    assert receipt["status"] == "pass"
    persisted = json.loads(state_path.read_text(encoding="utf-8"))["fixed_release"]
    assert persisted["attempt"] == {
        "state": "terminal",
        "operation_invocations": {"publish": 1},
        "infrastructure_retries": 0,
    }
    assert persisted["terminal_receipt"]["receipt_identity"] == receipt["receipt_identity"]


def test_fixed_release_allows_one_unchanged_infrastructure_retry(tmp_path: Path) -> None:
    revision, artifact = git_candidate(tmp_path)
    marker = tmp_path.parent / f"{tmp_path.name}-retry-marker"
    script = (
        "from pathlib import Path; import sys; p=Path(sys.argv[1]); "
        "first=not p.exists(); p.write_text('seen'); raise SystemExit(75 if first else 0)"
    )
    plan = fixed_release_plan(
        revision,
        artifact,
        [
            operation(
                "publish",
                [sys.executable, "-c", script, str(marker)],
                infrastructure_exit_codes=[75],
            )
        ],
    )
    _, receipt = workflow_cli._execution_run_fixed_release(tmp_path, plan, lambda value: None)
    assert receipt["status"] == "pass"
    assert receipt["operation_invocations"] == {"publish": 2}
    assert receipt["infrastructure_retries"] == 1


def test_fixed_release_rejects_mutation_and_prohibited_authority(tmp_path: Path) -> None:
    revision, artifact = git_candidate(tmp_path)
    mutate = "from pathlib import Path; Path('candidate.txt').write_text('changed\\n')"
    plan = fixed_release_plan(
        revision,
        artifact,
        [operation("verify", [sys.executable, "-c", mutate])],
    )
    _, receipt = workflow_cli._execution_run_fixed_release(tmp_path, plan, lambda value: None)
    assert receipt["status"] == "fail"
    assert "candidate worktree is dirty" in receipt["reason"]
    assert receipt["source_repairs"] == 0
    prohibited = fixed_release_plan(
        revision,
        artifact,
        [operation("qa-review", [sys.executable, "-c", "raise SystemExit(0)"])],
    )
    with pytest.raises(ValueError, match="repair, QA, or candidate"):
        workflow_cli._execution_validate_fixed_release(prohibited, "TASK-001")


def test_product_failure_is_not_retried(tmp_path: Path) -> None:
    revision, artifact = git_candidate(tmp_path)
    plan = fixed_release_plan(
        revision,
        artifact,
        [
            operation(
                "verify",
                [sys.executable, "-c", "raise SystemExit(2)"],
                infrastructure_exit_codes=[75],
            )
        ],
    )
    _, receipt = workflow_cli._execution_run_fixed_release(tmp_path, plan, lambda value: None)
    assert receipt["status"] == "fail"
    assert receipt["operation_invocations"] == {"verify": 1}
    assert receipt["infrastructure_retries"] == 0


def test_status_projects_single_qa_next_action_without_mutation(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    state_path = task_dir / "COORDINATION.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["execution_control"] = execution_control("finding-1")
    state["execution_qa"] = workflow_cli._execution_create_qa_campaign(
        work_id="TASK-001",
        source_revision="candidate-source-1",
        verdict_identity="qa-verdict-1",
        findings=[finding("finding-1")],
    )
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    before = state_path.read_bytes()
    result = run_project(tmp_path, "coordinate", "status", "--id", "TASK-001", "--format", "json")
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["qa_campaign"]["broad_qa_invocations"] == 1
    assert payload["next_action"] == payload["qa_campaign"]["next_action"]
    assert state_path.read_bytes() == before


def test_managed_cli_copies_remain_identical() -> None:
    template = (ROOT / "src/project_workflow/templates/workflow.py").read_bytes()
    assert (ROOT / ".project-workflow/cli/workflow.py").read_bytes() == template
    assert b"# project-workflow:generated" in template
    assert b"# source-manifest: scripts/runtime-modules.txt" in template
