from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / ".github" / "gh-run-receptor.yaml"


def test_noarch_conda_publication_uses_conda_profile():
    """Report the one noarch build without inferring a platform matrix."""
    config = CONFIG_PATH.read_text(encoding="utf-8")
    workflow = "path: .github/workflows/build_and_upload_conda_packages.yaml"
    rule = config.split(workflow, maxsplit=1)[1].split("  - match:", maxsplit=1)[0]

    assert "profile: conda" in rule
    assert "package_kind: noarch" in rule
    assert "expected_platforms" not in rule
