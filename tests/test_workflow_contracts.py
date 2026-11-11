import hashlib
import os
import subprocess
import sys
import tomllib
import xml.etree.ElementTree as ET
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
        "test_calorie_interop.py",
    ):
        assert module in script
    assert "tests/storage/test_*.py" in script
    assert "zarr, pyarrow" in script
    assert "ucumvert" in script and "asdf_astropy" in script
    assert "Storage guard skipped" in script


_REQUIRED_INSTALLED_CASES = [
    ("tests.astropy_units.test_calorie_interop", "calorie"),
    ("tests.pint.test_length_rounding", "test_pint_length_boundaries_round_once[nm-nm-nm]"),
    ("tests.test_conversion_branches", "test_pint_string_unit_builds_only_the_requested_quantities"),
    ("tests.test_introspection_probe", "test_filtered_probe_skips_payload_and_follows_live_debug_level"),
    ("tests.test_api_layout", "test_main_compatibility_module_exposes_its_creator_origin[cold]"),
    ("tests.test_api_layout", "test_main_compatibility_module_exposes_its_creator_origin[application_policy]"),
    ("tests.test_ragged_quantities", "test_object_row_construction_retains_rows_and_policy[nm-unequal-pint]"),
    ("tests.test_ragged_quantities", "test_object_row_conversion_preserves_shape_input_and_policy[unequal-pint]"),
    ("tests.test_ragged_quantities", "test_astropy_rejects_object_rows_with_actionable_diagnostic[unequal]"),
    ("tests.test_ragged_quantities", "test_unyt_row_conversion_has_actionable_diagnostic[unequal]"),
    (
        "tests.test_ragged_quantities",
        "test_translation_to_astropy_has_the_same_representation_diagnostic[unequal-pint]",
    ),
    ("tests.test_ragged_quantities", "test_object_rows_translate_between_compatible_containers[pint-pint]"),
]


@pytest.mark.parametrize(
    ("profile", "affected_case", "state"),
    [("baseline", None, "passed")]
    + [("baseline", name, state) for _, name in _REQUIRED_INSTALLED_CASES for state in ("missing", "skipped")]
    + [
        ("openff", "test_openff_object_rows_construct_and_convert", state)
        for state in ("passed", "missing", "skipped")
    ],
)
def test_every_installed_profile_requires_executed_cases(tmp_path, monkeypatch, profile, affected_case, state):
    monkeypatch.setenv("PROFILE", profile)
    workflow = yaml.safe_load((REPOSITORY_ROOT / ".github/workflows/test_staged_conda_package.yaml").read_text())
    job = next(job for job in workflow["jobs"].values() if "strategy" in job)
    script = next(
        step["run"]
        for step in job["steps"]
        if step.get("name") == "Test the installed record and integration contracts"
    )
    guard = script.split("python - <<'PY'\n", 1)[1].split("\nPY", 1)[0]
    suite = ET.Element("testsuite")
    for classname, name in _REQUIRED_INSTALLED_CASES + [
        ("tests.test_ragged_quantities", "test_openff_object_rows_construct_and_convert")
    ]:
        if state == "missing" and name == affected_case:
            continue
        case = ET.SubElement(suite, "testcase", classname=classname, name=name)
        if state == "skipped" and name == affected_case:
            ET.SubElement(case, "skipped", message="provider unavailable")
    ET.ElementTree(suite).write(tmp_path / "installed-contracts.xml")
    result = subprocess.run([sys.executable, "-c", guard], cwd=tmp_path, capture_output=True, text=True)
    assert (result.returncode == 0) is (state == "passed"), result.stderr
    if state != "passed":
        assert affected_case.split("[", 1)[0] in result.stderr.lower()


def test_optional_installed_checks_stop_when_dependency_probe_fails(tmp_path):
    workflow = yaml.safe_load((REPOSITORY_ROOT / ".github/workflows/storage_interop.yaml").read_text())
    script = next(
        step["run"]
        for step in workflow["jobs"]["storage"]["steps"]
        if step.get("name") == "Test installed consumer outside checkout"
    )
    tools = tmp_path / "bin"
    tools.mkdir()
    log = tmp_path / "commands.txt"
    shim = tools / "python"
    shim.write_text(
        f'#!/bin/sh\nprintf "%s\\n" "$*" >> "{log}"\nif [ "$1 $2 $3" = "-m pip check" ]; then exit 42; fi\nexit 0\n'
    )
    shim.chmod(0o755)
    result = subprocess.run(
        ["bash", "-c", script],
        cwd=REPOSITORY_ROOT,
        env={**os.environ, "RUNNER_TEMP": str(tmp_path), "PATH": str(tools) + os.pathsep + os.environ["PATH"]},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 42
    assert "-m pytest" not in log.read_text()
