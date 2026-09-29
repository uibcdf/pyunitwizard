"""The nightly recovery must retain skipped commits until a full matrix passes."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from urllib.error import URLError

SPEC = importlib.util.spec_from_file_location(
    "ci_backlog", Path(__file__).resolve().parents[1] / "devtools/ci_backlog.py"
)
assert SPEC is not None and SPEC.loader is not None
ci_backlog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ci_backlog)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def test_skipped_commit_stays_due_after_ordinary_commits(tmp_path, monkeypatch):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "CI test")
    git(tmp_path, "config", "user.email", "ci@example.invalid")
    git(tmp_path, "commit", "--allow-empty", "-qm", "full matrix passed")
    anchor = git(tmp_path, "rev-parse", "HEAD")
    git(tmp_path, "commit", "--allow-empty", "-qm", "fast iteration [skip ci]")
    skipped = git(tmp_path, "rev-parse", "HEAD")
    git(tmp_path, "commit", "--allow-empty", "-qm", "ordinary change")
    head = git(tmp_path, "rev-parse", "HEAD")
    monkeypatch.chdir(tmp_path)

    assert ci_backlog.skipped_commits_after(anchor, head) == [skipped]
    assert ci_backlog.skipped_commits_after(head, head) == []
    assert ci_backlog.SKIP_MARKER.search("message\n\nskip-checks: true")


def test_only_an_executed_full_linux_matrix_clears_debt(monkeypatch):
    def fake_api(path, _token):
        if "/runs?" in path:
            assert "status=success" not in path
            return {
                "workflow_runs": [
                    {
                        "id": 3,
                        "event": "schedule",
                        "head_sha": "failed",
                        "conclusion": "failure",
                    },
                    {
                        "id": 2,
                        "event": "workflow_dispatch",
                        "head_sha": "probe",
                        "conclusion": "success",
                    },
                    {
                        "id": 1,
                        "event": "schedule",
                        "head_sha": "green",
                        "conclusion": "success",
                    },
                ]
            }
        probe = "/runs/2/" in path
        return {
            "jobs": [
                {
                    "name": f"Full test on ubuntu-latest, Python {version}",
                    "conclusion": "success",
                    "steps": [
                        {
                            "name": "Run tests",
                            "conclusion": "skipped" if probe and version == "3.13" else "success",
                        }
                    ],
                }
                for version in ci_backlog.PYTHON_VERSIONS
            ]
        }

    monkeypatch.setattr(ci_backlog, "api_json", fake_api)
    monkeypatch.setattr(ci_backlog, "is_ancestor", lambda *_: True)
    assert ci_backlog.last_full_success("uibcdf/pyunitwizard", "head", "token") == "green"


def test_uncertain_api_triggers_full_matrix(tmp_path, monkeypatch, capsys):
    output = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_REPOSITORY", "uibcdf/pyunitwizard")
    monkeypatch.setenv("GITHUB_SHA", "head")
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    monkeypatch.setattr(
        ci_backlog,
        "last_full_success",
        lambda *_: (_ for _ in ()).throw(URLError("offline")),
    )

    assert ci_backlog.main() == 0
    assert "running full matrix" in capsys.readouterr().out
    assert "run_full=true" in output.read_text(encoding="utf-8")
