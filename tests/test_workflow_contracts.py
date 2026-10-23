import hashlib
import tomllib
from pathlib import Path

import pytest
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("platform", ["ubuntu", "macos"])
def test_public_installation_workflows_cover_supported_python_minors(platform):
    path = REPOSITORY_ROOT / ".github" / "workflows" / f"install_{platform}_latest.yaml"
    workflow = yaml.safe_load(path.read_text())
    cells = workflow["jobs"]["test"]["strategy"]["matrix"]["cfg"]
    assert {cell["python-version"] for cell in cells} == {"3.11", "3.12", "3.13", "3.14"}
    inventory = tomllib.loads((REPOSITORY_ROOT / "devtools/dependency_routes.toml").read_text())
    reviewed = {item["path"]: item for item in inventory["workflows"]}
    assert (
        reviewed[path.relative_to(REPOSITORY_ROOT).as_posix()]["sha256"]
        == hashlib.sha256(path.read_bytes()).hexdigest()
    )


def test_scheduled_full_matrix_failures_are_reported_and_recovered():
    workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "CI_full_matrix.yaml").read_text()

    assert "issues: write" in workflow
    assert "needs: full-test" in workflow
    assert "always() && github.event_name == 'schedule'" in workflow
    assert "needs.full-test.result" in workflow
    assert "pyunitwizard-ci-full-matrix-monitor" in workflow
    assert "github.rest.issues.create(" in workflow
    assert "github.rest.issues.createComment(" in workflow
    assert "github.rest.issues.update(" in workflow
    assert 'state: "closed"' in workflow


def test_staged_artifact_profile_executes_new_storage_and_codec_guards():
    path = REPOSITORY_ROOT / ".github/workflows/test_staged_conda_package.yaml"
    workflow = yaml.safe_load(path.read_text())
    job = next(job for job in workflow["jobs"].values() if "strategy" in job)
    setup = next(step for step in job["steps"] if step.get("uses", "").startswith("mamba-org/"))
    arguments = setup["with"]["create-args"]
    assert "zarr=3.1.6" in arguments and "pyarrow=25.0.0" in arguments
    guard = next(
        step for step in job["steps"] if step.get("name") == "Test the installed record and integration contracts"
    )
    script = guard["run"]
    for module in (
        "test_record_arrays.py",
        "test_record_tagged.py",
        "test_record_append.py",
        "test_record_extensions_consumer.py",
    ):
        assert module in script
    assert "tests/storage/test_*.py" in script
    assert "import zarr, pyarrow" in script
    assert "Storage guard skipped" in script
