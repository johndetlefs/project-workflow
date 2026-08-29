from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "coordination_eval", ROOT / "scripts/run_coordination_evaluations.py"
)
assert SPEC and SPEC.loader
evaluation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluation)


def test_sanitized_corpus_covers_under_and_over_processing_countercases() -> None:
    corpus = json.loads((ROOT / "evaluations/coordination/scenarios.json").read_text())
    scenarios = corpus["scenarios"]
    assert len(scenarios) >= 9
    classes = {scenario["class"] for scenario in scenarios}
    assert "under-processing" in classes
    assert "over-processing-countercase" in classes
    assert "recursive-review-countercase" in classes
    assert sum(1 for scenario in scenarios if scenario["class"].startswith("clarify")) >= 6
    serialized = json.dumps(corpus).lower()
    for forbidden in (
        "/users/",
        "johndetlefs",
        "toby's games",
        "mechanics playground",
        "token allocation",
    ):
        assert forbidden not in serialized


def test_grader_rejects_underprocessing_and_overprocessing() -> None:
    corpus = json.loads((ROOT / "evaluations/coordination/scenarios.json").read_text())
    correct = {
        "results": [
            {
                "id": scenario["id"],
                "decision": scenario["expected_decision"],
                "owner_question_count": scenario["owner_questions"][0],
                "qa_actions": scenario["qa_actions"],
                "new_contexts": scenario["new_contexts"],
                "preserved_controls": scenario["must_preserve"],
                "reason": "Uses the controlling authority.",
            }
            for scenario in corpus["scenarios"]
        ]
    }
    passed = evaluation.grade(corpus, correct)
    assert passed["pass"] is True

    wrong = json.loads(json.dumps(correct))
    wrong["results"][0]["decision"] = "continue-inside-envelope"
    wrong["results"][1]["owner_question_count"] = 1
    wrong["results"][-1]["qa_actions"] = 1
    failed = evaluation.grade(corpus, wrong)
    assert failed["pass"] is False
    failures = {result["id"]: result["failures"] for result in failed["scenarios"]}
    assert failures["clarify-material-preapproval"]
    assert failures["clarify-clean-bounded"]
    assert failures["proof-passed-stop"]


def test_grader_rejects_missing_or_invented_preservation_controls() -> None:
    corpus = json.loads((ROOT / "evaluations/coordination/scenarios.json").read_text())
    response = {
        "results": [
            {
                "id": scenario["id"],
                "decision": scenario["expected_decision"],
                "owner_question_count": scenario["owner_questions"][0],
                "qa_actions": scenario["qa_actions"],
                "new_contexts": scenario["new_contexts"],
                "preserved_controls": scenario["must_preserve"],
                "reason": "Uses the controlling authority.",
            }
            for scenario in corpus["scenarios"]
        ]
    }
    response["results"][0]["preserved_controls"] = [
        "one focused question",
        "existing QA later",
    ]
    graded = evaluation.grade(corpus, response)
    assert graded["pass"] is False
    first = graded["scenarios"][0]
    assert first["id"] == "clarify-material-preapproval"
    assert "missing preservation controls: record decision before planning" in first["failures"]
    assert "unexpected preservation controls: existing QA later" in first["failures"]

    response["results"][0]["preserved_controls"] = [
        "one focused question",
        "one focused question",
    ]
    duplicate = evaluation.grade(corpus, response)
    assert duplicate["pass"] is False
    assert (
        "missing preservation controls: record decision before planning"
        in duplicate["scenarios"][0]["failures"]
    )


def test_grader_accepts_only_declared_non_leaking_preservation_alternatives() -> None:
    corpus = json.loads((ROOT / "evaluations/coordination/scenarios.json").read_text())
    response = {
        "results": [
            {
                "id": scenario["id"],
                "decision": scenario["expected_decision"],
                "owner_question_count": scenario["owner_questions"][0],
                "qa_actions": scenario["qa_actions"],
                "new_contexts": scenario["new_contexts"],
                "preserved_controls": scenario["must_preserve"],
                "reason": "Uses the controlling authority.",
            }
            for scenario in corpus["scenarios"]
        ]
    }
    clean = next(item for item in response["results"] if item["id"] == "clarify-clean-bounded")
    clean["preserved_controls"] = ["continue autonomously", "existing QA later"]
    assert evaluation.grade(corpus, response)["pass"] is True

    clean["preserved_controls"] = ["continue autonomously", "smallest sufficient surface"]
    failed = evaluation.grade(corpus, response)
    clean_grade = next(
        item for item in failed["scenarios"] if item["id"] == "clarify-clean-bounded"
    )
    assert "missing preservation controls: existing QA later" in clean_grade["failures"]


def test_model_prompt_excludes_grader_answer_key() -> None:
    corpus = json.loads((ROOT / "evaluations/coordination/scenarios.json").read_text())
    prompt = evaluation.build_prompt("candidate", "CONTRACT SENTINEL", corpus)
    assert "CONTRACT SENTINEL" in prompt
    assert "expected_decision" not in prompt
    assert "owner_questions" not in prompt
    assert "qa_actions" not in prompt
    assert "new_contexts" not in prompt
    assert "must_preserve" not in prompt
    assert "preservation_alternatives" not in prompt
    for scenario in corpus["scenarios"]:
        assert json.dumps(scenario["must_preserve"]) not in prompt
    assert "contract labelled candidate" not in prompt


def test_provenance_and_retained_results_exclude_absolute_personal_paths() -> None:
    output_path = Path("/private/tmp/pw-eval/last.json")
    command = (
        "codex",
        "exec",
        "--output-schema",
        str(evaluation.SCHEMA_PATH),
        "--output-last-message",
        str(output_path),
        "-",
    )
    recorded = evaluation.provenance_command(command, output_path)
    serialized_command = json.dumps(recorded).lower()
    assert str(ROOT).lower() not in serialized_command
    assert "/private/tmp" not in serialized_command
    assert "evaluations/coordination/output-schema.json" in recorded
    assert "<ephemeral-output-path>" in recorded

    results_root = ROOT / "evaluations/coordination/results"
    for artifact in results_root.glob("EPIC-016-run-*/*.json"):
        serialized = artifact.read_text().lower()
        assert "/users/" not in serialized
        assert "/var/folders/" not in serialized
        assert "johndetlefs" not in serialized
