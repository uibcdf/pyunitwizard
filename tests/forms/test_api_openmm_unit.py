import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError


def test_api_openmm_compatibility_accepts_units():
    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    assert puw.forms.api_openmm_unit.compatibility(openmm_unit.meter, openmm_unit.centimeter)


def test_api_openmm_parser_stubs_raise():
    with pytest.raises(LibraryWithoutParserError):
        puw.forms.api_openmm_unit.string_to_quantity("1 meter")
    with pytest.raises(LibraryWithoutParserError):
        puw.forms.api_openmm_unit.string_to_unit("meter")


def test_api_openmm_unit_translation_helpers():
    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    unit = openmm_unit.nanometer

    unyt_unit = puw.forms.api_openmm_unit.unit_to_unyt(unit)
    assert str(unyt_unit) == "nm"

    astropy_unit = puw.forms.api_openmm_unit.unit_to_astropy_units(unit)
    assert "m" in str(astropy_unit)
