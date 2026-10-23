"""Offline generator guard: changed original ontology bytes cannot be admitted."""

import runpy
from pathlib import Path

import pytest


def test_changed_original_vocabulary_is_rejected_before_rdf_loading(tmp_path):
    source = Path(__file__).parents[1] / "devtools" / "extract_quantity_vocabulary.py"
    tool = runpy.run_path(str(source))
    (tmp_path / "qudt-units.ttl").write_text("changed ontology")
    with pytest.raises(ValueError, match="Original vocabulary identity mismatch: qudt-units.ttl"):
        tool["extract"](tmp_path)
