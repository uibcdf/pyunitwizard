import itertools

import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError
from tests.helpers import loaded_libraries


FORMS = ("pint", "openmm.unit", "unyt", "astropy.units")


def _make_quantity(form: str, value: float, unit_name: str):
    if form == "pint":
        return puw.forms.api_pint.make_quantity(value, unit_name)
    if form == "openmm.unit":
        openmm_unit = pytest.importorskip("openmm.unit")
        return value * getattr(openmm_unit, unit_name)
    if form == "unyt":
        unyt = pytest.importorskip("unyt")
        return value * getattr(unyt, unit_name)
    if form == "astropy.units":
        astropy_units = pytest.importorskip("astropy.units")
        return value * getattr(astropy_units, unit_name)
    raise ValueError(f"Unsupported form {form}")


@pytest.mark.parametrize("source_form,target_form", [
    pair for pair in itertools.product(FORMS, FORMS) if pair[0] != pair[1]
])
def test_quantity_conversion_matrix_preserves_value_unit_and_dimensionality(source_form, target_form):
    with loaded_libraries(list(FORMS)):
        source_q = _make_quantity(source_form, 2.5, "meter")
        converted = puw.convert(source_q, to_form=target_form)

        assert puw.get_form(converted) == target_form
        assert puw.are_compatible(source_q, converted)

        source_m = puw.convert(source_q, to_form="pint", to_unit="meter")
        converted_m = puw.convert(converted, to_form="pint", to_unit="meter")
        assert puw.get_value(converted_m) == pytest.approx(puw.get_value(source_m))

        assert puw.get_dimensionality(source_q) == puw.get_dimensionality(converted)


@pytest.mark.parametrize("source_form,target_form", [
    pair for pair in itertools.product(FORMS, FORMS) if pair[0] != pair[1]
])
def test_unit_conversion_matrix_preserves_dimensionality(source_form, target_form):
    with loaded_libraries(list(FORMS)):
        source_q = _make_quantity(source_form, 1.0, "meter")
        source_unit = puw.get_unit(source_q)
        converted_unit = puw.convert(source_unit, to_form=target_form)

        assert puw.is_unit(converted_unit)
        assert puw.are_compatible(source_unit, converted_unit)
        assert puw.get_dimensionality(source_unit) == puw.get_dimensionality(converted_unit)


@pytest.mark.parametrize("parser_name", ["pint", "astropy.units"])
def test_string_parse_supported_backends(parser_name):
    with loaded_libraries(list(FORMS)):
        out = puw.convert("3 meter", parser=parser_name, to_form=parser_name)
        assert puw.is_quantity(out)
        assert puw.get_form(out) == parser_name
        assert puw.get_value(puw.convert(out, to_form="pint", to_unit="meter")) == pytest.approx(3.0)


@pytest.mark.parametrize("parser_name", ["openmm.unit", "unyt"])
def test_string_parse_unsupported_backends_raise_explicit_error(parser_name):
    with loaded_libraries(list(FORMS)):
        with pytest.raises(LibraryWithoutParserError):
            puw.convert("3 meter", parser=parser_name, to_form="pint")
