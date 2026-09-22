import pytest

pytest.importorskip("astropy.units")

from pyunitwizard.forms import api_astropy_unit


def test_api_astropy_to_unit_rejects_invalid_type():
    with pytest.raises(TypeError):
        api_astropy_unit._to_unit(123)


def test_api_astropy_parser_and_translation_helpers():
    from astropy import units as astropy

    quantity = api_astropy_unit.string_to_quantity("2 meter")
    assert api_astropy_unit.get_value(quantity) == 2
    assert api_astropy_unit.unit_to_string(api_astropy_unit.get_unit(quantity)) == "m"

    unit = astropy.nm
    pint_unit = api_astropy_unit.unit_to_pint(unit)
    assert str(pint_unit) == "nanometer"

    unyt_unit = api_astropy_unit.unit_to_unyt(unit)
    assert str(unyt_unit) == "nm"

    openmm_unit = api_astropy_unit.unit_to_openmm_unit(unit)
    assert "nm" in str(openmm_unit).lower() or "nanometer" in str(openmm_unit).lower()

    assert api_astropy_unit.compatibility(1.0 * astropy.m, 100.0 * astropy.cm)
