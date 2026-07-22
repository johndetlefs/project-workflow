from __future__ import annotations

import importlib.util
import io
import json
import tarfile
import urllib.error
import zipfile
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "release_contract", REPO_ROOT / "scripts/release_contract.py"
)
assert SPEC and SPEC.loader
release_contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_contract)


def source_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    version_path = tmp_path / "_version.py"
    version_path.write_text('__version__ = "0.2.0"\n')
    mirror_paths = tuple(tmp_path / name for name in ("cli.py", "template.py", "workflow.py"))
    mirror = 'CURRENT_PACKAGE_VERSION = "0.2.0"\n'
    for path in mirror_paths:
        path.write_text(mirror)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps({"package_version": "0.2.0"}))
    (tmp_path / "CHANGELOG.md").write_text("## 0.2.0 - 2026-07-22\n")
    docs = "\n".join(
        (
            "uvx --from project-workflow==0.2.0 project init",
            "uvx --from project-workflow==0.2.0 project upgrade",
        )
    )
    for path in (
        tmp_path / "README.md",
        tmp_path / "AGENTS.md",
        tmp_path / ".project-workflow/cli/README.md",
        tmp_path / "src/project_workflow/codex/AGENTS.md",
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(docs)
    (tmp_path / "uv.lock").write_text("version = 1\n")
    monkeypatch.setattr(release_contract, "ROOT", tmp_path)
    monkeypatch.setattr(release_contract, "VERSION_PATH", version_path)
    monkeypatch.setattr(release_contract, "MIRROR_PATHS", mirror_paths)
    monkeypatch.setattr(release_contract, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(release_contract, "CHANGELOG_PATH", tmp_path / "CHANGELOG.md")
    return tmp_path


def artifact_fixture(tmp_path: Path, version: str = "0.2.0") -> Path:
    dist = tmp_path / "dist"
    dist.mkdir()
    metadata = f"Name: project-workflow\nVersion: {version}\n\n"
    wheel = dist / f"project_workflow-{version}-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(f"project_workflow-{version}.dist-info/METADATA", metadata)
        archive.writestr(
            f"project_workflow-{version}.dist-info/entry_points.txt",
            "[console_scripts]\nproject = project_workflow.cli:main\n",
        )
        for name in (
            "project_workflow/__init__.py",
            "project_workflow/_version.py",
            "project_workflow/cli.py",
            "project_workflow/templates/workflow",
            "project_workflow/templates/workflow.py",
            "project_workflow/codex/AGENTS.md",
            "project_workflow/codex/skills/project-task/SKILL.md",
        ):
            archive.writestr(name, "fixture\n")
    sdist = dist / f"project_workflow-{version}.tar.gz"
    with tarfile.open(sdist, "w:gz") as archive:
        content = metadata.encode()
        info = tarfile.TarInfo(f"project_workflow-{version}/PKG-INFO")
        info.size = len(content)
        archive.addfile(info, io.BytesIO(content))
    return dist


def test_source_contract_accepts_one_consistent_identity(tmp_path, monkeypatch):
    source_fixture(tmp_path, monkeypatch)
    assert release_contract.validate_source(
        expected_version="0.2.0", tag="v0.2.0", clean=False
    ) == "0.2.0"


@pytest.mark.parametrize("tag", ["v0.1.2", "0.2.0", "v0.2.1"])
def test_source_contract_rejects_mismatched_tag(tmp_path, monkeypatch, tag):
    source_fixture(tmp_path, monkeypatch)
    with pytest.raises(release_contract.ContractError, match="does not match"):
        release_contract.validate_source(expected_version="0.2.0", tag=tag, clean=False)


def test_source_contract_rejects_mutable_guidance(tmp_path, monkeypatch):
    source_fixture(tmp_path, monkeypatch)
    (tmp_path / "README.md").write_text(
        "uvx --from git+https://github.com/johndetlefs/project-workflow.git project init\n"
    )
    with pytest.raises(release_contract.ContractError, match="mutable"):
        release_contract.validate_source(expected_version="0.2.0", tag="v0.2.0", clean=False)


def test_distributions_require_exact_metadata_and_digests(tmp_path):
    dist = artifact_fixture(tmp_path)
    artifacts = release_contract.distributions(dist, "0.2.0")
    assert [item["kind"] for item in artifacts] == ["wheel", "sdist"]
    assert all(len(item["sha256"]) == 64 for item in artifacts)
    with pytest.raises(release_contract.ContractError, match="metadata mismatch"):
        release_contract.distributions(dist, "0.2.1")


def test_verify_receipt_rejects_changed_artifact(tmp_path):
    dist = artifact_fixture(tmp_path)
    receipt = {
        "schema_version": 1,
        "project": "project-workflow",
        "version": "0.2.0",
        "tag": "v0.2.0",
        "commit": "a" * 40,
        "asset_version": 1,
        "repository_schema_version": 1,
        "changelog_heading": "## 0.2.0 - 2026-07-22",
        "commands": {
            "init": "uvx --from project-workflow==0.2.0 project init",
            "upgrade": "uvx --from project-workflow==0.2.0 project upgrade",
        },
        "repository": "johndetlefs/project-workflow",
        "workflow": {"run_id": "1", "run_url": "https://example.invalid/1"},
        "artifacts": release_contract.distributions(dist, "0.2.0"),
    }
    receipt_path = tmp_path / "release-receipt.json"
    receipt_path.write_text(json.dumps(receipt))
    release_contract.verify_receipt(receipt_path, dist)
    with (next(dist.glob("*.whl"))).open("ab") as handle:
        handle.write(b"changed")
    with pytest.raises(release_contract.ContractError, match="digests"):
        release_contract.verify_receipt(receipt_path, dist)


def test_public_availability_rejects_existing_version(monkeypatch):
    class ExistingResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

    monkeypatch.setattr(release_contract.urllib.request, "urlopen", lambda *args, **kwargs: ExistingResponse())
    with pytest.raises(release_contract.ContractError, match="already exists"):
        release_contract.check_public_availability("0.2.0")


def test_public_availability_accepts_registry_404(monkeypatch):
    def not_found(*args, **kwargs):
        raise urllib.error.HTTPError(args[0], 404, "Not Found", {}, None)

    monkeypatch.setattr(release_contract.urllib.request, "urlopen", not_found)
    release_contract.check_public_availability("0.2.0")
