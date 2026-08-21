from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
EVAL_DIR = ROOT / "evaluations" / "intent_integrity"


def load_grader():
    spec = importlib.util.spec_from_file_location(
        "intent_integrity_grader", EVAL_DIR / "grade_results.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_corpus_has_six_sanitized_distinct_failure_and_counter_cases() -> None:
    payload = json.loads((EVAL_DIR / "cases.json").read_text(encoding="utf-8"))
    cases = payload["cases"]
    assert len(cases) == 6
    assert len({case["case_id"] for case in cases}) == 6
    text = json.dumps(payload).lower()
    forbidden = (
        "/users/",
        "johndetlefs",
        "toby",
        "ocean winch",
        "performance by design",
        "01a01d9d-15f5-7373-8e93-0cfd6633393f",
    )
    assert not any(value in text for value in forbidden)
    assert "bounded-fix-no-gold-plating" in {case["case_id"] for case in cases}


def test_grader_covers_all_six_axes_and_rejects_gold_plating() -> None:
    grader = load_grader()
    expected = json.loads((EVAL_DIR / "expectations.json").read_text(encoding="utf-8"))[
        "bounded-fix-no-gold-plating"
    ]
    good = {
        "case_id": "bounded-fix-no-gold-plating",
        "intent": "Correct the Export label and preserve the accepted export behaviour.",
        "route": "compact",
        "material_capabilities": ["Correct label", "Export behaviour unchanged"],
        "explicit_descoping": [],
        "proof_journey": "Open settings, observe the corrected label, and confirm behaviour is unchanged.",
        "invalid_substitutes": ["A broad redesign"],
        "unnecessary_scope": [],
        "approval_requests": 0,
        "verdict": "proceed",
        "rationale": "This is a bounded correction inside the accepted outcome.",
    }
    good_grade = grader.grade_decision(good, expected)
    assert set(good_grade["axes"]) == set(grader.AXES)
    assert good_grade["pass"] is True

    gold_plated = dict(good)
    gold_plated["unnecessary_scope"] = ["Redesign settings", "Add a new export format"]
    assert grader.grade_decision(gold_plated, expected)["pass"] is False


def test_grader_treats_behavior_and_behaviour_as_equivalent() -> None:
    grader = load_grader()
    expected = json.loads((EVAL_DIR / "expectations.json").read_text(encoding="utf-8"))[
        "bounded-fix-no-gold-plating"
    ]
    decision = {
        "case_id": "bounded-fix-no-gold-plating",
        "intent": "Correct the Export label and preserve export behavior.",
        "route": "compact",
        "material_capabilities": ["Correct Export label", "Preserve behavior"],
        "explicit_descoping": [],
        "proof_journey": "Inspect the corrected label and confirm export behavior is unchanged.",
        "invalid_substitutes": [],
        "unnecessary_scope": [],
        "approval_requests": 0,
        "verdict": "proceed",
        "rationale": "This is the bounded requested correction.",
    }

    assert grader.grade_decision(decision, expected)["pass"] is True


def test_grader_rejects_proxy_completion_even_when_route_is_full() -> None:
    grader = load_grader()
    expected = json.loads((EVAL_DIR / "expectations.json").read_text(encoding="utf-8"))[
        "narrowed-authoring"
    ]
    proxy = {
        "case_id": "narrowed-authoring",
        "intent": "Provide a level preview with one launch control.",
        "route": "full",
        "material_capabilities": ["Preview", "Launch speed"],
        "explicit_descoping": [],
        "proof_journey": "Open the preview and change launch speed.",
        "invalid_substitutes": [],
        "unnecessary_scope": [],
        "approval_requests": 1,
        "verdict": "proceed",
        "rationale": "The planned checks are green for the narrowed work.",
    }
    grade = grader.grade_decision(proxy, expected)
    assert grade["verdict_match"] is False
    assert grade["axes"]["capability_coverage"] == 0
    assert grade["pass"] is False


def test_preserved_release_trials_pass_all_six_cases_and_calibration_is_retained() -> None:
    grader = load_grader()
    expectations = json.loads(
        (EVAL_DIR / "expectations.json").read_text(encoding="utf-8")
    )
    results = EVAL_DIR / "results"
    trials = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(results.glob("trial-*.json"))
    }
    assert set(trials) == {"trial-1", "trial-2", "trial-3"}
    assert all(len(trial["decisions"]) == 6 for trial in trials.values())

    reports = {}
    for trial_id, trial in trials.items():
        decisions = {decision["case_id"]: decision for decision in trial["decisions"]}
        reports[trial_id] = [
            grader.grade_decision(decisions[case_id], expected)
            for case_id, expected in expectations.items()
        ]

    assert not all(grade["pass"] for grade in reports["trial-1"])
    assert all(grade["pass"] for grade in reports["trial-2"])
    assert all(grade["pass"] for grade in reports["trial-3"])


def test_run_manifest_binds_every_raw_trial_to_prompt_runtime_and_evaluator() -> None:
    manifest = json.loads((EVAL_DIR / "runs.json").read_text(encoding="utf-8"))
    runtime = manifest["shared_runtime"]
    assert runtime["model"] == "gpt-5.6-terra"
    assert runtime["runner"] == "OpenAI Codex CLI 0.145.0-alpha.30"
    assert runtime["evaluator_sha256"]
    assert {trial["trial_id"] for trial in manifest["trials"]} == {
        "trial-1",
        "trial-2",
        "trial-3",
    }
    prompts = json.loads((EVAL_DIR / "prompts.json").read_text(encoding="utf-8"))
    assert all(
        re.fullmatch(r"[0-9a-f-]{36}", trial["session_id"])
        for trial in manifest["trials"]
    )
    for name in ("cases", "output_schema", "expectations"):
        filename = {
            "cases": "cases.json",
            "output_schema": "output.schema.json",
            "expectations": "expectations.json",
        }[name]
        assert runtime[f"{name}_sha256"] == hashlib.sha256(
            (EVAL_DIR / filename).read_bytes()
        ).hexdigest()
    assert runtime["evaluator_sha256"] == hashlib.sha256(
        (EVAL_DIR / "grade_results.py").read_bytes()
    ).hexdigest()
    for trial in manifest["trials"]:
        assert trial["prompt_sha256"] == hashlib.sha256(
            prompts[trial["trial_id"]].encode("utf-8")
        ).hexdigest()
        assert trial["raw_result_sha256"] == hashlib.sha256(
            (EVAL_DIR / trial["raw_result"]).read_bytes()
        ).hexdigest()
