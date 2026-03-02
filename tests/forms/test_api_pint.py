import pyunitwizard as puw


def test_api_pint_compatibility_accepts_units():
    ureg = puw.forms.api_pint.ureg
    assert puw.forms.api_pint.compatibility(ureg.meter, ureg.centimeter)


def test_api_pint_string_to_unit_and_translation_helpers():
    api = puw.forms.api_pint
    ureg = api.ureg

    unit = api.string_to_unit("meter")
    assert str(unit) == "meter"

    unyt_unit = api.unit_to_unyt(ureg.nanometer)
    assert str(unyt_unit) == "nm"

    astropy_unit = api.unit_to_astropy_units(ureg.nanometer)
    assert "nm" in str(astropy_unit).lower() or "nanometer" in str(astropy_unit).lower()
