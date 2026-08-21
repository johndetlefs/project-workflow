from __future__ import annotations

import json
import math
import sys
from pathlib import Path


AXES = (
    "preserved_intent",
    "explicit_descoping",
    "capability_coverage",
    "exact_outcome_proof",
    "unnecessary_scope",
    "approval_burden",
)


def normalized_text(value: object) -> str:
    text = json.dumps(value, sort_keys=True).lower()
    return text.replace("behavior", "behaviour")


def contains_tokens(value: object, tokens: list[str]) -> bool:
    text = normalized_text(value)
    return all(token.lower() in text for token in tokens)


def covers_material_tokens(value: object, tokens: list[str]) -> bool:
    text = normalized_text(value)
    matched = sum(token.lower() in text for token in tokens)
    return matched >= math.ceil(len(tokens) * 2 / 3)


def grade_decision(decision: dict[str, object], expected: dict[str, object]) -> dict[str, object]:
    material = decision.get("material_capabilities", [])
    intent_material = [decision.get("intent", ""), material]
    drift_case = expected["verdict"] == "changes-requested"
    scores = {
        "preserved_intent": int(
            covers_material_tokens(intent_material, expected["capability_tokens"])
        ),
        "explicit_descoping": int(
            not drift_case
            or (
                decision.get("verdict") == "changes-requested"
                and (
                    bool(decision.get("explicit_descoping"))
                    or any(
                        marker in str(decision.get("rationale", "")).lower()
                        for marker in (
                            "missing", "not ", "only", "subset", "leaves", "does not", "neither", "without"
                        )
                    )
                )
            )
        ),
        "capability_coverage": int(
            covers_material_tokens(material, expected["capability_tokens"])
        ),
        "exact_outcome_proof": int(
            covers_material_tokens(
                decision.get("proof_journey", ""), expected["proof_tokens"]
            )
        ),
        "unnecessary_scope": int(
            not expected.get("require_no_unnecessary_scope")
            or not decision.get("unnecessary_scope")
        ),
        "approval_burden": int(
            int(decision.get("approval_requests", 999))
            <= int(expected.get("max_approval_requests", 1))
        ),
    }
    routing = decision.get("route") == expected["route"]
    verdict = decision.get("verdict") == expected["verdict"]
    return {
        "case_id": decision.get("case_id"),
        "axes": scores,
        "routing_match": routing,
        "verdict_match": verdict,
        "pass": routing and verdict and all(scores.values()),
    }


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: grade_results.py EXPECTATIONS.json TRIAL.json [TRIAL.json ...]")
    expectations = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    reports = []
    for raw_path in sys.argv[2:]:
        path = Path(raw_path)
        trial = json.loads(path.read_text(encoding="utf-8"))
        decisions = {decision["case_id"]: decision for decision in trial["decisions"]}
        grades = [
            grade_decision(decisions[case_id], expected)
            for case_id, expected in expectations.items()
        ]
        reports.append(
            {
                "trial": path.name,
                "trial_id": trial["trial_id"],
                "axes": AXES,
                "grades": grades,
                "pass": all(grade["pass"] for grade in grades),
            }
        )
    print(json.dumps({"reports": reports, "pass": all(r["pass"] for r in reports)}, indent=2))
    raise SystemExit(0 if all(report["pass"] for report in reports) else 1)


if __name__ == "__main__":
    main()
