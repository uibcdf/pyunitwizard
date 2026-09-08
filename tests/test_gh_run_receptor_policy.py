from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / ".github" / "gh-run-receptor.yaml"


def test_composite_conda_publication_uses_release_profile():
    """Do not infer a GitHub-visible platform matrix from a composite action."""
    config = CONFIG_PATH.read_text(encoding="utf-8")
    workflow = "path: .github/workflows/build_and_upload_conda_packages.yaml"
    rule = config.split(workflow, maxsplit=1)[1].split("  - match:", maxsplit=1)[0]

    assert "profile: release" in rule
    assert "expected_platforms" not in rule
