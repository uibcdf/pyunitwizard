"""The owner invokes shared contracts without weakening its publication gates."""

from __future__ import annotations

import importlib.util
import subprocess
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "pyunitwizard_dependency_preflight", ROOT / "devtools/check_dependency_routes.py"
)
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


def test_inventory_keeps_general_purposes_and_preserves_scientific_bounds():
    data = tomllib.loads((ROOT / "devtools/dependency_routes.toml").read_text())
    assert data["schema"] == "molsyssuite.dependency-routes@2"
    assert data["shared_tool"]["commit"] == "20628bd5dba6d759669b0d444fe657eb1edad33f"
    assert len(data["recipes"]) == 1
    assert len(data["environments"]) == 9
    assert len(data["workflows"]) == 12
    assert data["source_routes"] == []
    text = (ROOT / "devtools/conda-envs/openff_env.yaml").read_text()
    assert "python >=3.12,<3.15" in text
    assert "pint >=0.24,<0.26" in text
    assert "argdigest =0.14.0" in text


def test_provider_identity_and_modified_tools_are_refused(tmp_path):
    tool = tmp_path / "devtools/scripts/dependency_routes.py"
    tool.parent.mkdir(parents=True)
    tool.write_text("# tool fixture\n")
    for arguments in (
        ["init", "-q"],
        ["add", "devtools"],
        ["-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"],
    ):
        subprocess.run(["git", *arguments], cwd=tmp_path, check=True, capture_output=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    assert preflight.checked_tool(tmp_path, commit) == tool
    with pytest.raises(ValueError, match="expected"):
        preflight.checked_tool(tmp_path, "0" * 40)
    tool.write_text("# changed provider\n")
    with pytest.raises(ValueError, match="modified"):
        preflight.checked_tool(tmp_path, commit)


def test_native_candidate_profile_requires_all_workflows_and_jobs():
    plan = tomllib.loads((ROOT / "devtools/conda-build/release_plan.toml").read_text())
    preflight.required_jobs(plan)
    assert sum(len(jobs) for jobs in plan["gate_jobs"].values()) == 29
    for change in ("missing", "empty"):
        bad = dict(plan)
        bad["gate_jobs"] = dict(plan["gate_jobs"])
        workflow = plan["required_workflows"][0]
        if change == "missing":
            del bad["gate_jobs"][workflow]
        else:
            bad["gate_jobs"][workflow] = {}
        with pytest.raises(ValueError, match="executed"):
            preflight.required_jobs(bad)


def test_source_workflows_execute_default_qualification_before_tests_or_builds():
    before = {
        "CI.yaml": "- name: Run tests",
        "CI_full_matrix.yaml": "- name: Run tests",
        "release_gates.yaml": "- name: Run full test suite",
        "openff_interop.yaml": "- name: Run full suite with optional backend",
        "storage_interop.yaml": "- name: Run full suite with optional providers",
    }
    for filename, marker in before.items():
        text = (ROOT / ".github/workflows" / filename).read_text()
        assert text.index("- name: Check dependency contract") < text.index(marker)
        assert "--declared-only" not in text
        assert "20628bd5dba6d759669b0d444fe657eb1edad33f" in text
    for filename in ("openff_interop.yaml", "storage_interop.yaml"):
        assert "channel_priority: strict" in (ROOT / ".github/workflows" / filename).read_text()


def test_candidate_qualification_precedes_all_publication_actions():
    text = (ROOT / ".github/workflows/build_and_upload_conda_packages.yaml").read_text()
    check = text.index("- name: Check candidate dependency contract and executed source gates")
    assert check < text.index("- name: Build, test, and upload the staging candidate")
    assert check < text.index("- name: Build, test, and upload the unstaged release")
    assert "--candidate-sha" in text
    assert "dependency-candidate-" in text


def test_helper_cannot_report_an_offline_review_as_installed_qualification():
    with pytest.raises(ValueError, match="qualification"):
        preflight.require_qualification({"qualification": "declared-only"}, candidate=False)
    preflight.require_qualification({"qualification": "declared-only"}, candidate=True)


def test_native_candidate_source_is_bound_before_any_gate_query(monkeypatch):
    monkeypatch.setattr(preflight, "source_head", lambda root: "1" * 40)
    with pytest.raises(ValueError, match="candidate"):
        preflight.verify_candidate(ROOT, ROOT, "0" * 40, {})


def test_default_invocation_preserves_provider_failure_exit(monkeypatch, capsys):
    monkeypatch.setattr(preflight, "checked_tool", lambda root, commit: Path("tool.py"))
    monkeypatch.setattr(
        preflight.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 7, "bad runtime floor", ""),
    )
    monkeypatch.setattr(preflight.sys, "argv", ["preflight", "--suite-root", "."])
    assert preflight.main() == 7
    assert "bad runtime floor" in capsys.readouterr().err


def test_native_failure_cannot_qualify_a_candidate(monkeypatch):
    monkeypatch.setattr(preflight, "source_head", lambda root: "1" * 40)
    plan = tomllib.loads((ROOT / "devtools/conda-build/release_plan.toml").read_text())

    def run(command, **kwargs):
        if command[0] == "git":
            return subprocess.CompletedProcess(command, 0)
        assert "input" in kwargs
        return subprocess.CompletedProcess(command, 1, "", "no successful executed native jobs")

    monkeypatch.setattr(preflight.subprocess, "run", run)
    with pytest.raises(ValueError, match="executed native jobs"):
        preflight.verify_candidate(ROOT, ROOT, "1" * 40, plan)
