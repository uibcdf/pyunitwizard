#!/usr/bin/env python

"""Remove generated autosummary stub trees from the API reference pages.

Sphinx regenerates these stubs on every build, so they are transient artifacts.
Deleting them before a build is what keeps pages for removed API symbols from
surviving in the rendered site.
"""

import shutil
from pathlib import Path
from typing import List

# Resolved from this file, not from the current working directory, so the
# script behaves the same whether it is invoked as `python docs/clean_api.py`
# or from a `docs/` Makefile target.
API_DIRECTORY = Path(__file__).resolve().parent / "api"


def delete_autosummary_dirs(root_dir: Path) -> List[Path]:
    """Delete every ``autosummary`` directory below `root_dir`.

    Parameters
    ----------
    root_dir : pathlib.Path
        Directory tree to scan. A missing directory is not an error: there is
        simply nothing generated to remove.

    Returns
    -------
    list of pathlib.Path
        Directories that were removed, in the order they were found.
    """

    removed = []

    for autosummary_dir in sorted(root_dir.rglob("autosummary")):
        if not autosummary_dir.is_dir():
            continue
        print(f"Deleting directory: {autosummary_dir}")
        shutil.rmtree(autosummary_dir)
        removed.append(autosummary_dir)

    return removed


if __name__ == "__main__":
    if not delete_autosummary_dirs(API_DIRECTORY):
        print(f"No autosummary directories to delete under {API_DIRECTORY}")
