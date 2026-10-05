"""External reporting errors must remain visible in the CI result."""

from pathlib import Path

import yaml


def test_codecov_uploads_use_isolated_cli_and_fail_on_reporting_errors():
    workflow = yaml.safe_load((Path(__file__).resolve().parents[1] / ".github/workflows/CI.yaml").read_text())
    steps = workflow["jobs"]["test"]["steps"]
    install = next(step for step in steps if step.get("name") == "Install isolated Codecov CLI")
    assert 'python -m venv "$RUNNER_TEMP/codecov-cli"' in install["run"]
    assert '/bin/python" -m pip install codecov-cli' in install["run"]
    uploads = [step for step in steps if step.get("uses", "").startswith("codecov/")]
    assert {step["with"]["files"] for step in uploads} == {"./coverage.xml", "./junit.xml"}
    for step in uploads:
        assert step["with"]["fail_ci_if_error"] is True
        assert step["with"]["binary"] == "${{ runner.temp }}/codecov-cli/bin/codecovcli"
        assert not step.get("continue-on-error", False)
        assert "if" not in step
