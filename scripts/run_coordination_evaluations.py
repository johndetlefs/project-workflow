#!/usr/bin/env python3
"""Run sanitized baseline/candidate Project Workflow coordination behavior trials."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "evaluations/coordination/scenarios.json"
SCHEMA_PATH = ROOT / "evaluations/coordination/output-schema.json"
CONTRACT_PATHS = (
    "src/project_workflow/codex/skills/project-coordinator/SKILL.md",
    "src/project_workflow/codex/skills/project-clarify/SKILL.md",
    "src/project_workflow/codex/skills/project-planner/SKILL.md",
    "src/project_workflow/codex/skills/project-qa-review/SKILL.md",
)


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def contract_at(reference: str | None) -> str:
    sections: list[str] = []
    for relative in CONTRACT_PATHS:
        if reference is None:
            content = (ROOT / relative).read_text(encoding="utf-8")
        else:
            completed = subprocess.run(
                ("git", "show", f"{reference}:{relative}"),
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            content = (
                completed.stdout
                if completed.returncode == 0
                else f"[Asset absent at {reference}: {relative}]"
            )
        sections.append(f"\n## CONTRACT ASSET: {relative}\n\n{content}")
    return "".join(sections)


def provenance_command(command: tuple[str, ...], output_path: Path) -> list[str]:
    replacements = {
        str(SCHEMA_PATH): str(SCHEMA_PATH.relative_to(ROOT)),
        str(output_path): "<ephemeral-output-path>",
    }
    return [replacements.get(token, token) for token in command[:-1]] + [
        "<prompt-via-stdin>"
    ]


def build_prompt(contract_label: str, contract: str, corpus: dict[str, object]) -> str:
    scenarios = [
        {"id": scenario["id"], "prompt": scenario["prompt"]}
        for scenario in corpus["scenarios"]
    ]
    return f"""You are evaluating one supplied Project Workflow contract.

Apply only the supplied contract to each sanitized scenario independently. Do not use repository
files, personal knowledge, or results from another scenario. Choose exactly one allowed decision,
count how many owner-facing questions, independent-QA actions, and fresh execution contexts you
would create immediately, select exactly two preservation controls from the output schema's global
vocabulary that the response must preserve, and give one short reason. Do not optimize for a
preferred result.
The scenario input intentionally contains no answer key; do not infer a desired comparison result
from the order or identity of the supplied contract.

CONTRACT:
{contract}

SCENARIOS:
{json.dumps(scenarios, indent=2)}

Return exactly one result for every scenario ID in the same order.
"""


def run_trial(
    *, model: str, label: str, contract: str, corpus: dict[str, object], trial: int
) -> tuple[dict[str, object], dict[str, object]]:
    prompt = build_prompt(label, contract, corpus)
    with tempfile.TemporaryDirectory(prefix="pw-coordination-eval-") as temp:
        temp_path = Path(temp)
        output_path = temp_path / "last.json"
        command = (
            "codex",
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--model",
            model,
            "--output-schema",
            str(SCHEMA_PATH),
            "--output-last-message",
            str(output_path),
            "--json",
            "-",
        )
        completed = subprocess.run(
            command,
            cwd=temp_path,
            input=prompt,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            stdout_tail = completed.stdout[-4000:]
            raise RuntimeError(
                f"{label} trial {trial} failed ({completed.returncode}). "
                f"stderr: {completed.stderr[-4000:]} stdout tail: {stdout_tail}"
            )
        response = json.loads(output_path.read_text(encoding="utf-8"))
        usage: dict[str, object] = {}
        event_types: list[str] = []
        for line in completed.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            event_type = str(event.get("type", ""))
            if event_type:
                event_types.append(event_type)
            if isinstance(event.get("usage"), dict):
                usage = event["usage"]
        provenance = {
            "condition": label,
            "trial": trial,
            "model": model,
            "command": provenance_command(command, output_path),
            "prompt_hash": sha256_bytes(prompt.encode("utf-8")),
            "response_hash": sha256_bytes(
                json.dumps(response, sort_keys=True).encode("utf-8")
            ),
            "usage": usage or "not-reported",
            "event_types": sorted(set(event_types)),
        }
        return response, provenance


def grade(corpus: dict[str, object], response: dict[str, object]) -> dict[str, object]:
    scenarios = corpus["scenarios"]
    expected = {item["id"]: item for item in scenarios}
    results = response.get("results", [])
    actual = {
        item.get("id"): item for item in results if isinstance(item, dict) and item.get("id")
    }
    verdicts: list[dict[str, object]] = []
    for scenario_id, scenario in expected.items():
        result = actual.get(scenario_id)
        failures: list[str] = []
        if result is None:
            failures.append("missing result")
        else:
            if result.get("decision") != scenario["expected_decision"]:
                failures.append(
                    f"decision {result.get('decision')} != {scenario['expected_decision']}"
                )
            minimum, maximum = scenario["owner_questions"]
            count = result.get("owner_question_count")
            if not isinstance(count, int) or not minimum <= count <= maximum:
                failures.append(f"owner questions {count} outside [{minimum}, {maximum}]")
            for field in ("qa_actions", "new_contexts"):
                if result.get(field) != scenario[field]:
                    failures.append(f"{field} {result.get(field)} != {scenario[field]}")
            expected_controls = scenario["must_preserve"]
            actual_controls = result.get("preserved_controls")
            if not isinstance(actual_controls, list):
                failures.append("preserved_controls is missing or not a list")
            else:
                alternatives = scenario.get("preservation_alternatives", {})
                accepted_groups = {
                    control: {control, *alternatives.get(control, [])}
                    for control in expected_controls
                }
                missing_controls = [
                    control
                    for control, accepted in accepted_groups.items()
                    if not any(actual in accepted for actual in actual_controls)
                ]
                accepted_controls = set().union(*accepted_groups.values())
                unexpected_controls = [
                    control for control in actual_controls if control not in accepted_controls
                ]
                if missing_controls:
                    failures.append(
                        "missing preservation controls: " + ", ".join(missing_controls)
                    )
                if unexpected_controls:
                    failures.append(
                        "unexpected preservation controls: "
                        + ", ".join(unexpected_controls)
                    )
        verdicts.append(
            {"id": scenario_id, "pass": not failures, "failures": failures}
        )
    return {
        "passed": sum(1 for item in verdicts if item["pass"]),
        "total": len(verdicts),
        "pass": all(item["pass"] for item in verdicts),
        "scenarios": verdicts,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--trials", type=int, default=2)
    parser.add_argument("--baseline-ref", default="origin/main")
    parser.add_argument(
        "--condition", choices=("both", "baseline", "candidate"), default="both"
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.trials < 2:
        raise SystemExit("--trials must be at least 2 for repeated evidence.")

    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    baseline = contract_at(args.baseline_ref)
    candidate = contract_at(None)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    runs: list[dict[str, object]] = []
    selected_conditions = (
        ("baseline", "candidate")
        if args.condition == "both"
        else (args.condition,)
    )
    for label, contract in (("baseline", baseline), ("candidate", candidate)):
        if label not in selected_conditions:
            continue
        for trial in range(1, args.trials + 1):
            response, provenance = run_trial(
                model=args.model,
                label=label,
                contract=contract,
                corpus=corpus,
                trial=trial,
            )
            grading = grade(corpus, response)
            run = {"provenance": provenance, "grade": grading, "response": response}
            run_path = args.output_dir / f"{label}-trial-{trial}.json"
            run_path.write_text(json.dumps(run, indent=2, sort_keys=True) + "\n")
            runs.append({"artifact": run_path.name, **run})

    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "trials_per_condition": args.trials,
        "conditions": list(selected_conditions),
        "corpus": str(CORPUS_PATH.relative_to(ROOT)),
        "corpus_hash": sha256_bytes(CORPUS_PATH.read_bytes()),
        "harness_hash": sha256_bytes(Path(__file__).read_bytes()),
        "candidate_commit": git("rev-parse", "HEAD"),
        "candidate_tracked_diff_hash": sha256_bytes(
            git("diff", "--binary").encode("utf-8")
        ),
        "candidate_contract_hash": sha256_bytes(candidate.encode("utf-8")),
        "baseline_ref": args.baseline_ref,
        "baseline_commit": git("rev-parse", args.baseline_ref),
        "baseline_contract_hash": sha256_bytes(baseline.encode("utf-8")),
        "codex_version": subprocess.run(
            ("codex", "--version"), check=True, capture_output=True, text=True
        ).stdout.strip(),
        "runs": runs,
        "summary": {
            label: {
                "passes": [
                    run["grade"]["passed"]
                    for run in runs
                    if run["provenance"]["condition"] == label
                ],
                "complete_passes": sum(
                    1
                    for run in runs
                    if run["provenance"]["condition"] == label and run["grade"]["pass"]
                ),
            }
            for label in selected_conditions
        },
        "claim_boundary": (
            "Sanitized prompt-following evidence for this model, harness, corpus and candidate; "
            "not universal reliability, billing, credit, or token-savings proof."
        ),
    }
    report_path = args.output_dir / "REPORT.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(report_path)


if __name__ == "__main__":
    main()
