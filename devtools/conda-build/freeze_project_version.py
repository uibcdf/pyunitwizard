#!/usr/bin/env python
"""Freeze the Conda coordinate into the ephemeral Python build source."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:[A-Za-z0-9._+-]*)?")
PROJECT_VERSION_MARKER = 'dynamic = ["version"]'


def _without_versioningit_configuration(text: str) -> str:
    """Remove versioningit's build hook after the project version is static."""
    kept: list[str] = []
    skipping = False
    for line in text.splitlines(keepends=True):
        if line.startswith("["):
            skipping = line.startswith("[tool.versioningit")
        if not skipping:
            kept.append(line)
    return "".join(kept)


def freeze_project_version(root: Path, version: str) -> None:
    """Replace dynamic VCS versioning with the immutable Conda coordinate."""
    if VERSION_PATTERN.fullmatch(version) is None:
        raise ValueError(f"Invalid package version: {version!r}")

    pyproject = root / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    if text.count(PROJECT_VERSION_MARKER) != 1:
        raise RuntimeError(
            f"Expected one {PROJECT_VERSION_MARKER!r} marker in {pyproject}"
        )
    frozen = text.replace(PROJECT_VERSION_MARKER, f'version = "{version}"')
    pyproject.write_text(_without_versioningit_configuration(frozen), encoding="utf-8")

    version_file = root / "pyunitwizard" / "_version.py"
    version_file.write_text(f'__version__ = "{version}"\n', encoding="utf-8")


def main() -> None:
    """Freeze the version in the current source tree."""
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    args = parser.parse_args()
    freeze_project_version(Path.cwd(), args.version)


if __name__ == "__main__":
    main()
