from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_scheduled_full_matrix_failures_are_reported_and_recovered():
    workflow = (
        REPOSITORY_ROOT / ".github" / "workflows" / "CI_full_matrix.yaml"
    ).read_text()

    assert "issues: write" in workflow
    assert "needs: full-test" in workflow
    assert "always() && github.event_name == 'schedule'" in workflow
    assert "needs.full-test.result" in workflow
    assert "pyunitwizard-ci-full-matrix-monitor" in workflow
    assert "github.rest.issues.create(" in workflow
    assert "github.rest.issues.createComment(" in workflow
    assert "github.rest.issues.update(" in workflow
    assert 'state: "closed"' in workflow
