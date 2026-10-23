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
