import pytest

import pyunitwizard as puw


def test_api_astropy_to_unit_rejects_invalid_type():
    with pytest.raises(TypeError):
        puw.forms.api_astropy_unit._to_unit(123)


def test_api_astropy_parser_and_translation_helpers():
    astropy = pytest.importorskip("astropy.units")

    quantity = puw.forms.api_astropy_unit.string_to_quantity("2 meter")
    assert puw.forms.api_astropy_unit.get_value(quantity) == 2
    assert puw.forms.api_astropy_unit.unit_to_string(puw.forms.api_astropy_unit.get_unit(quantity)) == "m"

    unit = astropy.nm
    openmm_unit = puw.forms.api_astropy_unit.unit_to_openmm_unit(unit)
    assert "nm" in str(openmm_unit).lower() or "nanometer" in str(openmm_unit).lower()
