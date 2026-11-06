"""Archival discovery must retain pending releases without publishing anything."""

from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CALLER = ROOT / ".github/workflows/zenodo_archival.yaml"


def _workflow():
    return yaml.safe_load(CALLER.read_text())


def test_archival_recovery_keeps_a_fixed_cutoff_and_exact_tag_routes():
    workflow = _workflow()
    events = workflow.get("on", workflow.get(True))
    assert events["release"]["types"] == ["published"]
    assert events["schedule"] == [{"cron": "17 */6 * * *"}]
    manual = events["workflow_dispatch"]["inputs"]["tag"]
    assert manual["type"] == "string" and manual["default"] == ""
    assert manual["required"] is False
    settings = workflow["jobs"]["verify"]["with"]
    assert settings["since"] == "2026-11-05T00:00:00Z"
    cutoff = datetime.fromisoformat(settings["since"].replace("Z", "+00:00"))
    assert cutoff.tzinfo == timezone.utc
    assert "${{" not in settings["since"]
    assert "github.event.release.tag_name" in settings["tag"]
    assert "inputs.tag" in settings["tag"] and "|| ''" in settings["tag"]


def test_archival_caller_uses_read_only_immutable_shared_verifier():
    workflow = _workflow()
    assert workflow["permissions"] == {"contents": "read"}
    assert list(workflow["jobs"]) == ["verify"]
    job = workflow["jobs"]["verify"]
    assert job["uses"] == (
        "uibcdf/molsyssuite/.github/workflows/verify-zenodo-releases.yaml@20628bd5dba6d759669b0d444fe657eb1edad33f"
    )
    assert job["with"]["concept-doi"] == "10.5281/zenodo.8088374"
    assert "steps" not in job and "secrets" not in job
    assert "runs-on" not in job
