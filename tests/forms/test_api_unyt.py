import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError


def test_api_unyt_parser_stubs_raise():
    with pytest.raises(LibraryWithoutParserError):
        puw.forms.api_unyt.string_to_quantity("1 m")
    with pytest.raises(LibraryWithoutParserError):
        puw.forms.api_unyt.string_to_unit("m")


def test_api_unyt_unit_translation_helpers():
    unyt = puw.forms.api_unyt.unyt
    unit = unyt.nm

    pint_unit = puw.forms.api_unyt.unit_to_pint(unit)
    assert str(pint_unit) == "nanometer"

    openmm_unit = puw.forms.api_unyt.unit_to_openmm_unit(unit)
    assert "nm" in str(openmm_unit).lower() or "nanometer" in str(openmm_unit).lower()
