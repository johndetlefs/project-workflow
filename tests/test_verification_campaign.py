from __future__ import annotations

import json
import os
import subprocess
import sys
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


def fixture_repo(
    tmp_path: Path,
    *,
    material_verification: str = "yes",
    verification_stages: str = "canary,full",
    verification_scope: str = "changed,previously-failing",
) -> Path:
    initialized = run_project(tmp_path, "init", "--agent", "codex")
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    scaffolded = run_project(
        tmp_path,
        "task",
        "init",
        "--title",
        "Bounded Verification",
        "--update-tracker",
        "--status",
        "In Progress",
    )
    assert scaffolded.returncode == 0, scaffolded.stdout + scaffolded.stderr
    task_dir = tmp_path / ".project-workflow/tasks/TASK-001-Bounded-Verification"
    (task_dir / "REQUIREMENTS.md").write_text(
        "# Requirements\n\n## Intent\n\nDeliver one current, bounded candidate.\n",
        encoding="utf-8",
    )
    coordinated_args = [
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
        "Finish implementation.",
        "--material-verification",
        material_verification,
    ]
    if material_verification == "yes":
        coordinated_args.extend(
            (
                "--verification-claims",
                "release-behaviour",
                "--verification-stages",
                verification_stages,
                "--verification-scope",
                verification_scope,
            )
        )
    coordinated = run_project(tmp_path, *coordinated_args)
    assert coordinated.returncode == 0, coordinated.stdout + coordinated.stderr
    return task_dir


def finish_implementation(task_dir: Path) -> None:
    implementation = task_dir / "IMPLEMENTATION.md"
    text = implementation.read_text(encoding="utf-8")
    implementation.write_text(text.replace("| To Do |", "| Done |", 1), encoding="utf-8")


def record_qa_pass(task_dir: Path) -> None:
    implementation = task_dir / "IMPLEMENTATION.md"
    text = implementation.read_text(encoding="utf-8")
    replacements = {
        "- Verdict: ____": "- Verdict: Pass",
        "- Intent adversarial verdict: ____": "- Intent adversarial verdict: Pass",
        "- Could every AC pass while the approved user job remains undone: ____": (
            "- Could every AC pass while the approved user job remains undone: No"
        ),
        "- Intent audit state: ____": "- Intent audit state: current",
        "- Outcome journey evidence: ____": (
            "- Outcome journey evidence: Independent fixture exercised the bounded journey."
        ),
        "- Reviewer independence: ____": (
            "- Reviewer independence: Separate adversarial reviewer inspected current evidence."
        ),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    implementation.write_text(text, encoding="utf-8")


def init_campaign(
    root: Path,
    *,
    candidate: str = "candidate-1",
    mode: str = "certification",
    stages: str = "canary,full",
    extra: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[str]:
    args = [
        "coordinate",
        "verification-init",
        "--id",
        "TASK-001",
        "--candidate-identity",
        candidate,
        "--mode",
        mode,
        "--claims",
        "release-behaviour",
        "--stages",
        stages,
        "--affected-scope",
        "changed,previously-failing",
        "--max-target-calls",
        "100",
        "--max-elapsed-seconds",
        "120",
        "--format",
        "json",
    ]
    if not ("--adapter-kind" in extra and "command" in extra):
        args.extend(
            (
                "--manual-command",
                "fake-verifier --selected-scope changed,previously-failing",
            )
        )
    args.extend(extra)
    return run_project(root, *args)


def record(
    root: Path,
    stage: str,
    outcome: str,
    *,
    target_calls: int,
    artifact: str,
    target_identity: str | None = None,
    evaluator_identity: str = "evaluator-1",
    regrade: bool = False,
    stage_complete: str = "yes",
) -> subprocess.CompletedProcess[str]:
    args = [
        "coordinate",
        "verification-record",
        "--id",
        "TASK-001",
        "--stage",
        stage,
        "--outcome",
        outcome,
        "--scope",
        stage,
        "--runtime-identity",
        "runtime-1",
        "--target-identity",
        target_identity or f"target-{stage}",
        "--evaluator-identity",
        evaluator_identity,
        "--artifact",
        artifact,
        "--target-calls",
        str(target_calls),
        "--elapsed-seconds",
        "1",
        "--stage-complete",
        stage_complete,
        "--format",
        "json",
    ]
    if regrade:
        args.append("--regrade")
    return run_project(root, *args)


def test_incomplete_release_preflight_is_read_only_and_invokes_nothing(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path)
    before = (task_dir / "COORDINATION.json").read_bytes()
    result = run_project(
        tmp_path,
        "coordinate",
        "verification-preflight",
        "--id",
        "TASK-001",
        "--material-verification",
        "yes",
        "--claim",
        "release-behaviour",
        "--stage",
        "canary,full",
        "--scope",
        "changed,previously-failing",
        "--format",
        "json",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["projection"]["operational_state"] == "implementation-required"
    assert payload["required_campaign"]["stages"] == ["canary", "full"]
    assert payload["verifier_invocations"] == 0
    assert payload["mutated"] is False
    assert (task_dir / "COORDINATION.json").read_bytes() == before


def test_cheap_task_needs_no_campaign_ceremony(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path, material_verification="no")
    finish_implementation(task_dir)
    result = run_project(
        tmp_path,
        "coordinate",
        "verification-preflight",
        "--id",
        "TASK-001",
        "--material-verification",
        "no",
        "--format",
        "json",
    )
    payload = json.loads(result.stdout)
    assert payload["projection"]["campaign_required"] is False
    assert payload["projection"]["campaign_present"] is False
    assert payload["projection"]["operational_state"] == "qa-required"
    assert payload["verifier_invocations"] == 0


def test_durable_material_requirement_cannot_be_omitted_or_redefined(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    task_dir = fixture_repo(tmp_path)
    finish_implementation(task_dir)
    status = run_project(tmp_path, "coordinate", "status", "--id", "TASK-001", "--format", "json")
    payload = json.loads(status.stdout)
    assert payload["verification"]["operational_state"] == "verification-required"
    assert payload["verification"]["missing_stages"] == ["canary", "full"]

    mismatched = init_campaign(tmp_path, stages="full")
    assert mismatched.returncode != 0
    assert "durable verification requirement" in mismatched.stderr

    monkeypatch.setattr(workflow_cli, "_task_testing_integrity_issues", lambda _text: ())
    monkeypatch.setattr(
        workflow_cli,
        "_approval_envelope_issues",
        lambda _text, *, require_implementation=False, **_kwargs: [],
    )
    monkeypatch.setattr(workflow_cli, "_task_ready_issues_for_paths", lambda **_kwargs: [])
    monkeypatch.setattr(workflow_cli, "_structured_evidence_issues", lambda **_kwargs: [])
    monkeypatch.setattr(workflow_cli, "_repository_evidence_issues", lambda *_args: [])
    monkeypatch.setattr(
        workflow_cli, "_coordination_boundary_gate_issues", lambda *_args, **_kwargs: []
    )
    tracker = tmp_path / ".project-workflow/TRACKER.md"
    assert workflow_cli._update_global_tracker_row_status(
        root=tmp_path,
        tracker_path=tracker,
        row_id="TASK-001",
        new_status="Testing",
        force=False,
        reason=None,
    ) == ("In Progress", "Testing")
    with pytest.raises(SystemExit) as blocked:
        workflow_cli._update_global_tracker_row_status(
            root=tmp_path,
            tracker_path=tracker,
            row_id="TASK-001",
            new_status="Review",
            force=False,
            reason=None,
        )
    assert "material verification is verification-required" in str(blocked.value)


def test_certification_stops_after_product_failure_and_new_candidate_runs_once(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path)
    finish_implementation(task_dir)
    initialized = init_campaign(tmp_path)
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr

    failed = record(
        tmp_path,
        "canary",
        "product-failure",
        target_calls=1,
        artifact="receipts/canary-fail.json",
    )
    assert failed.returncode == 0, failed.stdout + failed.stderr
    assert json.loads(failed.stdout)["projection"]["operational_state"] == "blocked"
    forbidden = record(
        tmp_path,
        "full",
        "pass",
        target_calls=5,
        artifact="receipts/forbidden-full.json",
    )
    assert forbidden.returncode != 0
    assert "further target work is blocked" in forbidden.stderr

    corrected = init_campaign(tmp_path, candidate="candidate-2", extra=("--force",))
    assert corrected.returncode == 0, corrected.stdout + corrected.stderr
    canary = record(
        tmp_path,
        "canary",
        "pass",
        target_calls=1,
        artifact="receipts/canary-pass.json",
    )
    assert canary.returncode == 0, canary.stdout + canary.stderr
    full = record(
        tmp_path,
        "full",
        "pass",
        target_calls=5,
        artifact="receipts/full-pass.json",
    )
    assert full.returncode == 0, full.stdout + full.stderr
    full_payload = json.loads(full.stdout)
    assert full_payload["projection"]["operational_state"] == "qa-required"
    assert full_payload["projection"]["target_calls"] == 6

    repeated = record(
        tmp_path,
        "full",
        "pass",
        target_calls=5,
        artifact="receipts/repeated-full.json",
    )
    assert repeated.returncode != 0
    assert "further target work is blocked" in repeated.stderr

    record_qa_pass(task_dir)
    ready = run_project(
        tmp_path,
        "coordinate",
        "verification-preflight",
        "--id",
        "TASK-001",
        "--material-verification",
        "yes",
        "--format",
        "json",
    )
    assert json.loads(ready.stdout)["projection"]["operational_state"] == "delivery-ready"
    state = json.loads((task_dir / "COORDINATION.json").read_text(encoding="utf-8"))
    assert len(state["verification_campaign"]["receipts"]) == 2


def test_diagnostic_requires_named_decision_scope_and_finite_limit(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path, verification_stages="canary")
    finish_implementation(task_dir)
    missing = init_campaign(tmp_path, mode="diagnostic", stages="canary")
    assert missing.returncode != 0
    assert "diagnostic_decision" in missing.stderr

    bounded = init_campaign(
        tmp_path,
        mode="diagnostic",
        stages="canary",
        extra=(
            "--diagnostic-decision",
            "determine whether the canary failure is systematic",
            "--max-target-calls",
            "2",
        ),
    )
    assert bounded.returncode == 0, bounded.stdout + bounded.stderr
    reached = record(
        tmp_path,
        "canary",
        "product-failure",
        target_calls=2,
        artifact="receipts/diagnostic-boundary.json",
        stage_complete="no",
    )
    payload = json.loads(reached.stdout)
    assert payload["projection"]["operational_state"] == "blocked"
    assert payload["projection"]["campaign_outcome"] == "limit-reached"
    assert "no pass is implied" in payload["projection"]["next_action"]


def test_completed_stage_cannot_pass_after_exceeding_a_declared_limit(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path, verification_stages="full")
    finish_implementation(task_dir)
    initialized = init_campaign(tmp_path, stages="full", extra=("--max-target-calls", "1"))
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    exceeded = record(
        tmp_path,
        "full",
        "pass",
        target_calls=2,
        artifact="receipts/over-limit.json",
    )
    payload = json.loads(exceeded.stdout)
    assert payload["projection"]["campaign_outcome"] == "limit-reached"
    assert payload["projection"]["operational_state"] == "blocked"
    assert "no pass is implied" in payload["projection"]["next_action"]


def test_evaluator_regrade_reuses_target_and_infrastructure_retry_is_bounded(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path, verification_stages="full")
    finish_implementation(task_dir)
    assert init_campaign(tmp_path, stages="full").returncode == 0
    evaluator_failure = record(
        tmp_path,
        "full",
        "evaluator-failure",
        target_calls=4,
        target_identity="retained-output-1",
        evaluator_identity="evaluator-1",
        artifact="receipts/evaluator-failure.json",
        stage_complete="no",
    )
    assert json.loads(evaluator_failure.stdout)["projection"]["operational_state"] == "blocked"
    regraded = record(
        tmp_path,
        "full",
        "pass",
        target_calls=0,
        target_identity="retained-output-1",
        evaluator_identity="evaluator-2",
        artifact="receipts/evaluator-regrade.json",
        regrade=True,
    )
    regraded_payload = json.loads(regraded.stdout)
    assert regraded_payload["receipt"]["regrade"] is True
    assert regraded_payload["receipt"]["target_calls"] == 0
    assert regraded_payload["projection"]["target_calls"] == 4
    assert regraded_payload["projection"]["operational_state"] == "qa-required"

    assert (
        init_campaign(
            tmp_path, candidate="candidate-infra", stages="full", extra=("--force",)
        ).returncode
        == 0
    )
    first = record(
        tmp_path,
        "full",
        "provider-failure",
        target_calls=0,
        artifact="receipts/provider-1.json",
        stage_complete="no",
    )
    assert json.loads(first.stdout)["projection"]["operational_state"] == "verification-required"
    second = record(
        tmp_path,
        "full",
        "provider-failure",
        target_calls=0,
        artifact="receipts/provider-2.json",
        stage_complete="no",
    )
    assert json.loads(second.stdout)["projection"]["operational_state"] == "blocked"


def test_command_adapter_fails_closed_without_required_generic_controls(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path)
    finish_implementation(task_dir)
    missing = init_campaign(
        tmp_path,
        extra=(
            "--adapter-kind",
            "command",
            "--adapter-command-json",
            '["fake-verifier"]',
            "--adapter-capability",
            "selection",
        ),
    )
    assert missing.returncode != 0
    assert "required controls" in missing.stderr
    required = (
        "request-binding",
        "selection",
        "fail-fast",
        "limits",
        "typed-outcomes",
        "input-bound-receipts",
    )
    extra: list[str] = [
        "--adapter-kind",
        "command",
        "--adapter-command-json",
        '["fake-verifier"]',
    ]
    for capability in required:
        extra.extend(("--adapter-capability", capability))
    accepted = init_campaign(tmp_path, extra=tuple(extra))
    assert accepted.returncode == 0, accepted.stdout + accepted.stderr


def test_fake_command_adapter_proves_actual_fail_fast_invocation_counts(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path)
    finish_implementation(task_dir)
    adapter_script = tmp_path / "fake_verifier.py"
    invocation_log = tmp_path / "invocations.jsonl"
    adapter_script.write_text(
        """import json
import pathlib
import sys

request = json.load(sys.stdin)
log = pathlib.Path(sys.argv[1])
behavior = sys.argv[2]
with log.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps({
        "candidate": request["candidate_identity"],
        "stage": request["stage"],
        "action": request["action"],
    }, sort_keys=True) + "\\n")
outcome = "product-failure" if behavior == "fail" else "pass"
calls = 1 if request["stage"] == "canary" else 4
print(json.dumps({
    "request_identity": (
        "sha256:mismatched" if behavior == "mismatch" else request["request_identity"]
    ),
    "candidate_identity": request["candidate_identity"],
    "source_identity": request["source_identity"],
    "proof_contract_identity": request["proof_contract_identity"],
    "stage": request["stage"],
    "outcome": outcome,
    "scope": request["selected_scope"],
    "runtime_identity": "fake-runtime-1",
    "target_identity": "output-" + request["candidate_identity"] + "-" + request["stage"],
    "evaluator_identity": "fake-evaluator-1",
    "artifact": "receipts/" + request["candidate_identity"] + "-" + request["stage"] + ".json",
    "target_calls": calls,
    "elapsed_seconds": 1,
    "stage_complete": True,
}, sort_keys=True))
""",
        encoding="utf-8",
    )

    def command_extra(behavior: str, *, force: bool = False) -> tuple[str, ...]:
        command = json.dumps([sys.executable, str(adapter_script), str(invocation_log), behavior])
        values: list[str] = [
            "--adapter-kind",
            "command",
            "--adapter-command-json",
            command,
        ]
        for capability in (
            "request-binding",
            "selection",
            "fail-fast",
            "limits",
            "typed-outcomes",
            "input-bound-receipts",
        ):
            values.extend(("--adapter-capability", capability))
        if force:
            values.append("--force")
        return tuple(values)

    first = init_campaign(tmp_path, extra=command_extra("fail"))
    assert first.returncode == 0, first.stdout + first.stderr
    failed = run_project(
        tmp_path,
        "coordinate",
        "verification-run",
        "--id",
        "TASK-001",
        "--runtime-identity",
        "fake-runtime-1",
        "--format",
        "json",
    )
    assert json.loads(failed.stdout)["projection"]["operational_state"] == "blocked"
    blocked = run_project(
        tmp_path,
        "coordinate",
        "verification-run",
        "--id",
        "TASK-001",
        "--runtime-identity",
        "fake-runtime-1",
        "--format",
        "json",
    )
    assert blocked.returncode != 0
    entries = [json.loads(line) for line in invocation_log.read_text().splitlines()]
    assert [entry["stage"] for entry in entries] == ["canary"]

    corrected = init_campaign(
        tmp_path,
        candidate="candidate-2",
        extra=command_extra("pass", force=True),
    )
    assert corrected.returncode == 0, corrected.stdout + corrected.stderr
    for expected_stage in ("canary", "full"):
        result = run_project(
            tmp_path,
            "coordinate",
            "verification-run",
            "--id",
            "TASK-001",
            "--runtime-identity",
            "fake-runtime-1",
            "--format",
            "json",
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert json.loads(result.stdout)["receipt"]["stage"] == expected_stage
    before_delivery = invocation_log.read_bytes()
    record_qa_pass(task_dir)
    delivery = run_project(
        tmp_path,
        "coordinate",
        "verification-preflight",
        "--id",
        "TASK-001",
        "--material-verification",
        "yes",
        "--format",
        "json",
    )
    assert json.loads(delivery.stdout)["projection"]["operational_state"] == "delivery-ready"
    assert invocation_log.read_bytes() == before_delivery
    entries = [json.loads(line) for line in invocation_log.read_text().splitlines()]
    assert [entry["stage"] for entry in entries] == ["canary", "canary", "full"]
    assert sum(entry["stage"] == "full" for entry in entries) == 1


def test_command_adapter_must_bind_the_exact_invocation_request(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path)
    finish_implementation(task_dir)
    adapter_script = tmp_path / "mismatched_verifier.py"
    invocation_log = tmp_path / "mismatched-invocations.txt"
    adapter_script.write_text(
        """import json
import pathlib
import sys

request = json.load(sys.stdin)
with pathlib.Path(sys.argv[1]).open("a", encoding="utf-8") as handle:
    handle.write("invoked\\n")
print(json.dumps({
    "request_identity": "sha256:not-the-request",
    "candidate_identity": request["candidate_identity"],
    "source_identity": request["source_identity"],
    "proof_contract_identity": request["proof_contract_identity"],
    "stage": request["stage"],
    "outcome": "pass",
    "selected_scope": request["selected_scope"],
    "runtime_identity": "runtime-1",
    "target_identity": "target-1",
    "evaluator_identity": "evaluator-1",
    "artifact": "receipt.json",
    "target_calls": 1,
    "elapsed_seconds": 1,
    "stage_complete": True,
}))
""",
        encoding="utf-8",
    )
    extra: list[str] = [
        "--adapter-kind",
        "command",
        "--adapter-command-json",
        json.dumps([sys.executable, str(adapter_script), str(invocation_log)]),
    ]
    for capability in (
        "request-binding",
        "selection",
        "fail-fast",
        "limits",
        "typed-outcomes",
        "input-bound-receipts",
    ):
        extra.extend(("--adapter-capability", capability))
    initialized = init_campaign(tmp_path, extra=tuple(extra))
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr
    first = run_project(
        tmp_path,
        "coordinate",
        "verification-run",
        "--id",
        "TASK-001",
        "--runtime-identity",
        "runtime-1",
        "--format",
        "json",
    )
    assert first.returncode == 0, first.stdout + first.stderr
    first_payload = json.loads(first.stdout)
    assert first_payload["receipt"]["outcome"] == "harness-failure"
    assert first_payload["projection"]["operational_state"] == "verification-required"
    second = run_project(
        tmp_path,
        "coordinate",
        "verification-run",
        "--id",
        "TASK-001",
        "--runtime-identity",
        "runtime-1",
        "--format",
        "json",
    )
    assert second.returncode == 0, second.stdout + second.stderr
    second_payload = json.loads(second.stdout)
    assert second_payload["projection"]["operational_state"] == "blocked"
    third = run_project(
        tmp_path,
        "coordinate",
        "verification-run",
        "--id",
        "TASK-001",
        "--runtime-identity",
        "runtime-1",
        "--format",
        "json",
    )
    assert third.returncode != 0
    assert invocation_log.read_text(encoding="utf-8").splitlines() == [
        "invoked",
        "invoked",
    ]


def test_typed_limit_and_receipt_tampering_fail_closed(tmp_path: Path) -> None:
    task_dir = fixture_repo(tmp_path, verification_stages="full")
    finish_implementation(task_dir)
    assert init_campaign(tmp_path, stages="full").returncode == 0
    limited = record(
        tmp_path,
        "full",
        "limit-reached",
        target_calls=0,
        artifact="receipts/runner-limit.json",
        stage_complete="no",
    )
    payload = json.loads(limited.stdout)
    assert payload["projection"]["campaign_outcome"] == "limit-reached"
    assert payload["projection"]["failures"] == 0
    assert payload["projection"]["operational_state"] == "blocked"

    assert (
        init_campaign(
            tmp_path, candidate="candidate-tamper", stages="full", extra=("--force",)
        ).returncode
        == 0
    )
    passed = record(
        tmp_path,
        "full",
        "pass",
        target_calls=1,
        artifact="receipts/current.json",
    )
    assert passed.returncode == 0
    state_path = task_dir / "COORDINATION.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["verification_campaign"]["receipts"][0]["target_identity"] = "tampered"
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    rejected = run_project(
        tmp_path,
        "coordinate",
        "verification-preflight",
        "--id",
        "TASK-001",
        "--material-verification",
        "yes",
        "--format",
        "json",
    )
    assert rejected.returncode != 0
    assert "receipt_identity is stale or malformed" in rejected.stderr
    receipt = state["verification_campaign"]["receipts"][0]
    receipt["receipt_identity"] = workflow_cli._verification_identity(
        {key: value for key, value in receipt.items() if key != "receipt_identity"}
    )
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    rehashed = run_project(
        tmp_path,
        "coordinate",
        "verification-preflight",
        "--id",
        "TASK-001",
        "--material-verification",
        "yes",
        "--format",
        "json",
    )
    assert rehashed.returncode != 0
    assert "receipt_ledger_identity is stale or malformed" in rehashed.stderr


def test_candidate_source_change_invalidates_receipts_and_unknown_impact_expands_full(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path, verification_stages="full")
    finish_implementation(task_dir)
    assert init_campaign(tmp_path, stages="full").returncode == 0
    passed = record(
        tmp_path,
        "full",
        "pass",
        target_calls=3,
        artifact="receipts/current.json",
    )
    assert passed.returncode == 0
    changed = run_project(
        tmp_path,
        "coordinate",
        "phase",
        "--id",
        "TASK-001",
        "--phase",
        "testing",
        "--source-revision",
        "candidate-source-2",
        "--next-action",
        "Replan affected proof.",
    )
    assert changed.returncode == 0, changed.stdout + changed.stderr
    stale = run_project(
        tmp_path,
        "coordinate",
        "verification-preflight",
        "--id",
        "TASK-001",
        "--material-verification",
        "yes",
        "--format",
        "json",
    )
    stale_payload = json.loads(stale.stdout)
    assert stale_payload["projection"]["operational_state"] == "blocked"
    assert any(
        "candidate source identity changed" in reason
        for reason in stale_payload["projection"]["reasons"]
    )

    unknown_without_full = init_campaign(
        tmp_path,
        candidate="candidate-unknown",
        mode="diagnostic",
        stages="canary",
        extra=(
            "--impact",
            "unknown",
            "--diagnostic-decision",
            "identify affected proof",
            "--max-failures",
            "1",
            "--force",
        ),
    )
    assert unknown_without_full.returncode != 0
    assert "requires the full proof stage" in unknown_without_full.stderr


def test_generic_product_source_contains_no_reference_consumer_identity() -> None:
    root = ROOT
    product_sources = (
        root / ".project-workflow/cli/workflow.py",
        root / "src/project_workflow/cli.py",
        root / "src/project_workflow/templates/workflow.py",
    )
    prohibited = "strategic" + "-advisor"
    for source in product_sources:
        assert prohibited not in source.read_text(encoding="utf-8").lower()


def test_optional_consumer_dogfood_retains_the_complete_bounded_sequence() -> None:
    evidence = json.loads(
        (
            ROOT
            / ".project-workflow/tasks/EPIC-017-Proportionate-Verification-Lifecycle/evidence/optional-consumer-dogfood.json"
        ).read_text(encoding="utf-8")
    )
    assert evidence["schema_version"] == 2
    assert all(evidence["assertions"].values())
    assert [event["event"] for event in evidence["events"]] == [
        "incomplete-preflight",
        "failed-canary",
        "corrected-canary",
        "corrected-full",
        "evaluator-only-regrade",
        "one-qa",
        "unchanged-delivery",
    ]
    assert evidence["events"][0]["verifier_invocations"] == 0
    assert evidence["events"][1]["later_stage_invocations"] == 0
    assert evidence["events"][4]["target_calls"] == 0
    assert evidence["events"][5]["second_qa_commissioned"] is False
    assert evidence["events"][6]["verifier_invocations"] == 0
    assert evidence["standalone_verifier"]["runtime_dependency_required"] is False


def test_managed_hosts_receive_campaign_and_one_qa_boundaries(tmp_path: Path) -> None:
    targets = {
        "codex": (
            ".agents/skills/project-coordinator/SKILL.md",
            ".agents/skills/project-implement/SKILL.md",
            ".agents/skills/project-qa-review/SKILL.md",
        ),
        "claude-code": (
            ".claude/agents/project-coordinator.md",
            ".claude/agents/project-implement.md",
            ".claude/agents/project-qa-review.md",
        ),
        "cursor": (
            ".cursor/agents/project-coordinator.md",
            ".cursor/agents/project-implement.md",
            ".cursor/agents/project-qa-review.md",
        ),
        "github-copilot": (
            ".github/prompts/Coordinator.prompt.md",
            ".github/prompts/Implement.prompt.md",
            ".github/prompts/QAReview.prompt.md",
        ),
    }
    for host, paths in targets.items():
        root = tmp_path / host
        root.mkdir()
        initialized = run_project(root, "init", "--agent", host)
        assert initialized.returncode == 0, initialized.stdout + initialized.stderr
        combined = "\n".join(
            (root / relative_path).read_text(encoding="utf-8") for relative_path in paths
        ).lower()
        assert "verification-preflight" in combined
        assert "diagnostic" in combined
        assert "zero target calls" in combined
        assert "no second qa" in combined or "cannot schedule" in combined


def test_operational_status_and_lifecycle_use_the_campaign_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    task_dir = fixture_repo(tmp_path)
    finish_implementation(task_dir)
    assert init_campaign(tmp_path).returncode == 0
    status = run_project(tmp_path, "status", "--id", "TASK-001", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    payload = json.loads(status.stdout)
    action_codes = {
        payload["primary_action"]["code"],
        *(action["code"] for action in payload["secondary_actions"]),
    }
    assert "PW_STATUS_VERIFICATION_REQUIRED" in action_codes

    monkeypatch.setattr(workflow_cli, "_task_testing_integrity_issues", lambda _text: ())
    monkeypatch.setattr(
        workflow_cli,
        "_approval_envelope_issues",
        lambda _text, *, require_implementation=False, **_kwargs: [],
    )
    monkeypatch.setattr(
        workflow_cli,
        "_task_ready_issues_for_paths",
        lambda **_kwargs: [],
    )
    monkeypatch.setattr(workflow_cli, "_structured_evidence_issues", lambda **_kwargs: [])
    monkeypatch.setattr(workflow_cli, "_repository_evidence_issues", lambda *_args: [])
    monkeypatch.setattr(
        workflow_cli, "_coordination_boundary_gate_issues", lambda *_args, **_kwargs: []
    )
    tracker = tmp_path / ".project-workflow/TRACKER.md"
    assert workflow_cli._update_global_tracker_row_status(
        root=tmp_path,
        tracker_path=tracker,
        row_id="TASK-001",
        new_status="Testing",
        force=False,
        reason=None,
    ) == ("In Progress", "Testing")
    with pytest.raises(SystemExit) as blocked:
        workflow_cli._update_global_tracker_row_status(
            root=tmp_path,
            tracker_path=tracker,
            row_id="TASK-001",
            new_status="Review",
            force=False,
            reason=None,
        )
    assert "material verification is verification-required" in str(blocked.value)

    assert (
        record(
            tmp_path,
            "canary",
            "pass",
            target_calls=1,
            artifact="receipts/gate-canary.json",
        ).returncode
        == 0
    )
    assert (
        record(
            tmp_path,
            "full",
            "pass",
            target_calls=4,
            artifact="receipts/gate-full.json",
        ).returncode
        == 0
    )
    assert workflow_cli._update_global_tracker_row_status(
        root=tmp_path,
        tracker_path=tracker,
        row_id="TASK-001",
        new_status="Review",
        force=False,
        reason=None,
    ) == ("Testing", "Review")


def test_doctor_fails_closed_on_stale_campaign_but_legacy_state_stays_valid(
    tmp_path: Path,
) -> None:
    task_dir = fixture_repo(tmp_path, verification_stages="full")
    finish_implementation(task_dir)
    requirement_issues = workflow_cli.run_doctor(tmp_path)
    assert any(
        "Material verification is verification-required" in issue.message
        for issue in requirement_issues
    )
    assert init_campaign(tmp_path, stages="full").returncode == 0
    changed = run_project(
        tmp_path,
        "coordinate",
        "phase",
        "--id",
        "TASK-001",
        "--phase",
        "testing",
        "--source-revision",
        "new-source",
        "--next-action",
        "Replan current proof.",
    )
    assert changed.returncode == 0
    issues = workflow_cli.run_doctor(tmp_path)
    stale = [issue for issue in issues if "Verification campaign is stale" in issue.message]
    assert len(stale) == 1
    assert stale[0].severity == "error"
    assert stale[0].code == "PW_WORKFLOW_INVALID"
