from __future__ import annotations

import io
import importlib.util
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_package_journeys", ROOT / "scripts/verify_package_journeys.py"
)
assert SPEC and SPEC.loader
journeys = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(journeys)


def disposable_epic(tmp_path: Path) -> tuple[Path, Path]:
    epic_dir = tmp_path / "EPIC-001-Prove-Export-Journey"
    child_dir = epic_dir / "TASK-001-Deliver-Complete-Export-Journey"
    child_dir.mkdir(parents=True)
    (epic_dir / "REQUIREMENTS.md").write_text(
        journeys.parent_requirements(), encoding="utf-8"
    )
    (child_dir / "REQUIREMENTS.md").write_text(
        journeys.child_requirements(), encoding="utf-8"
    )
    return epic_dir, child_dir


def test_sourced_reviewer_detects_actual_green_but_wrong_child(tmp_path: Path) -> None:
    epic_dir, child_dir = disposable_epic(tmp_path)
    (child_dir / "IMPLEMENTATION.md").write_text(
        journeys.green_but_wrong_implementation(), encoding="utf-8"
    )
    journeys.write_preview_evidence(child_dir)

    review = journeys.review_export_intent_alignment(epic_dir)

    assert review["classification"] == "proxy"
    assert review["lost_capability"] == (
        "The member cannot open the complete exported archive."
    )
    assert review["checks"] == {
        "complete_archive_created": False,
        "complete_archive_opened": False,
        "ordinary_settings_route": True,
    }
    assert review["sources"]["child_implementation_sha256"]
    assert review["review_artifact_sha256"]


def test_sourced_reviewer_recognizes_restored_complete_journey(tmp_path: Path) -> None:
    epic_dir, child_dir = disposable_epic(tmp_path)
    (child_dir / "IMPLEMENTATION.md").write_text(
        journeys.child_implementation(), encoding="utf-8"
    )
    journeys.write_outcome_evidence(child_dir)

    review = journeys.review_export_intent_alignment(epic_dir)

    assert review["classification"] == "preserved"
    assert review["lost_capability"] == ""
    assert all(review["checks"].values())


def test_generated_asset_parity_includes_exact_ownership_marker_position() -> None:
    marked_skill = journeys._generated_bytes(
        ".agents/skills/project-example/SKILL.md",
        b"---\nname: example\n---\n\n# Example\n",
    ).decode("utf-8")
    marked_wrapper = journeys._generated_bytes(
        ".project-workflow/cli/workflow",
        b"#!/bin/sh\nexec python workflow.py\n",
    ).decode("utf-8")

    assert marked_skill.startswith(
        "---\nname: example\n---\n<!-- project-workflow:generated -->\n\n# Example\n"
    )
    assert marked_wrapper.startswith(
        "#!/bin/sh\n# project-workflow:generated\nexec python workflow.py\n"
    )
    assert journeys._agent_name("SmokeBomb.prompt.md") == "project-smokebomb"
    assert journeys._agent_name("QAReview.prompt.md") == "project-qa-review"


def test_sdist_member_lookup_uses_exact_archive_relative_path(tmp_path: Path) -> None:
    archive_path = tmp_path / "candidate.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        for name, content in (
            ("project-workflow-0.7.0/README.md", b"root readme"),
            ("project-workflow-0.7.0/evaluations/coordination/README.md", b"nested readme"),
        ):
            info = tarfile.TarInfo(name)
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))

    with tarfile.open(archive_path, "r:gz") as archive:
        assert journeys._sdist_member_bytes(archive, "README.md") == b"root readme"
