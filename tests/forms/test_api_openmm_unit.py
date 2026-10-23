import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError
from pyunitwizard.forms import api_openmm_unit


def test_api_openmm_compatibility_accepts_units():
    openmm_unit = api_openmm_unit.openmm_unit
    assert api_openmm_unit.compatibility(openmm_unit.meter, openmm_unit.centimeter)


def test_api_openmm_parser_stubs_raise():
    with pytest.raises(LibraryWithoutParserError):
        api_openmm_unit.string_to_quantity("1 meter")
    with pytest.raises(LibraryWithoutParserError):
        api_openmm_unit.string_to_unit("meter")


def test_api_openmm_unit_translation_helpers():
    openmm_unit = api_openmm_unit.openmm_unit
    unit = openmm_unit.nanometer

    unyt_unit = api_openmm_unit.unit_to_unyt(unit)
    assert str(unyt_unit) == "nm"

    astropy_unit = api_openmm_unit.unit_to_astropy_units(unit)
    assert "m" in str(astropy_unit)


@pytest.mark.parametrize(
    "source_unit,target_unit,factor",
    [("angstrom", "nanometer", 0.1), ("ampere", "ampere", 1.0), ("angstrom/picosecond", "meter/second", 100.0)],
)
def test_openmm_to_unyt_preserves_unit_meaning(source_unit, target_unit, factor):
    pytest.importorskip("unyt")
    pytest.importorskip("openmm.unit")
    values = np.array([[1.0, 2.0, -3.0]], dtype=np.float64)
    with puw.context(default_form="pint", default_parser="pint"):
        source = puw.quantity(values, source_unit, form="openmm.unit")
        translated = puw.convert(source, to_form="unyt")
        explicit = puw.convert(source, to_form="unyt", to_unit=target_unit)
        np.testing.assert_allclose(puw.get_value(translated, to_unit=target_unit), values * factor)
        np.testing.assert_allclose(puw.get_value(explicit), values * factor)
        assert np.asarray(puw.get_value(explicit)).shape == values.shape
        assert puw.get_dimensionality(translated) == puw.get_dimensionality(source)


def test_openmm_angstrom_unit_reaches_unyt_as_length():
    unyt = pytest.importorskip("unyt")
    pytest.importorskip("openmm.unit")
    with puw.context(default_form="pint", default_parser="pint"):
        source = puw.unit("angstrom", form="openmm.unit")
        translated = puw.convert(source, to_form="unyt", to_type="unit")
        assert translated.dimensions == unyt.dimensions.length
        assert translated.get_conversion_factor(unyt.nm)[0] == pytest.approx(0.1)
