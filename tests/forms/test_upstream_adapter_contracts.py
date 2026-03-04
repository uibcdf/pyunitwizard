import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError


def _blank_dimensionality():
    return {"[L]": 0, "[M]": 0, "[T]": 0, "[K]": 0, "[mol]": 0, "[A]": 0, "[Cd]": 0}


def test_openmm_quantity_private_value_contract():
    openmm_unit = pytest.importorskip("openmm.unit")

    q = openmm_unit.Quantity(2.0, openmm_unit.nanometer)
    assert hasattr(q, "_value")
    assert puw.forms.api_openmm_unit.get_value(q) == q._value


def test_unyt_to_pint_contract_used_by_adapter():
    unyt = pytest.importorskip("unyt")
    pint = pytest.importorskip("pint")

    q_unyt = 2.0 * unyt.nanometer / unyt.picosecond
    q_pint = puw.forms.api_unyt.quantity_to_pint(q_unyt)

    assert isinstance(q_pint, pint.Quantity)
    assert q_pint.magnitude == pytest.approx(2.0)
    assert str(q_pint.units) == "nanometer / picosecond"


def test_astropy_decompose_si_bases_contract_used_by_adapter():
    astropy_units = pytest.importorskip("astropy.units")

    q = 3.0 * astropy_units.m / astropy_units.s
    dimensionality = puw.forms.api_astropy_unit.dimensionality(q)
    expected = _blank_dimensionality()
    expected["[L]"] = 1.0
    expected["[T]"] = -1.0

    assert dimensionality == expected


def test_pint_string_parser_contract():
    pint = pytest.importorskip("pint")

    q = puw.forms.api_pint.string_to_quantity("3 meter")
    assert isinstance(q, pint.Quantity)
    assert q.magnitude == pytest.approx(3.0)
    assert str(q.units) == "meter"


def test_openmm_roundtrip_through_pint_contract():
    openmm_unit = pytest.importorskip("openmm.unit")

    q_openmm = 1.25 * openmm_unit.nanometer / openmm_unit.picosecond
    q_pint = puw.forms.api_openmm_unit.quantity_to_pint(q_openmm)
    q_openmm_back = puw.forms.api_pint.quantity_to_openmm_unit(q_pint)

    assert puw.forms.api_openmm_unit.compatibility(q_openmm, q_openmm_back)
    assert puw.forms.api_openmm_unit.get_value(q_openmm_back) == pytest.approx(1.25)


def test_astropy_roundtrip_through_pint_contract():
    astropy_units = pytest.importorskip("astropy.units")

    q_astropy = 7.0 * astropy_units.kg
    q_pint = puw.forms.api_astropy_unit.quantity_to_pint(q_astropy)
    q_astropy_back = puw.forms.api_pint.quantity_to_astropy_units(q_pint)

    assert puw.forms.api_astropy_unit.compatibility(q_astropy, q_astropy_back)
    assert puw.forms.api_astropy_unit.get_value(q_astropy_back) == pytest.approx(7.0)
    assert puw.forms.api_astropy_unit.unit_to_string(
        puw.forms.api_astropy_unit.get_unit(q_astropy_back)
    ) == "kg"


def test_unyt_roundtrip_through_pint_contract():
    unyt = pytest.importorskip("unyt")

    q_unyt = 4.5 * unyt.m
    q_pint = puw.forms.api_unyt.quantity_to_pint(q_unyt)
    q_unyt_back = puw.forms.api_pint.quantity_to_unyt(q_pint)

    assert puw.forms.api_unyt.compatibility(q_unyt, q_unyt_back)
    assert puw.forms.api_unyt.get_value(q_unyt_back) == pytest.approx(4.5)


def test_non_parser_backends_keep_explicit_parser_errors():
    pytest.importorskip("openmm.unit")
    pytest.importorskip("unyt")

    with pytest.raises(LibraryWithoutParserError):
        puw.forms.api_openmm_unit.string_to_quantity("2 meter")
    with pytest.raises(LibraryWithoutParserError):
        puw.forms.api_openmm_unit.string_to_unit("meter")
    with pytest.raises(LibraryWithoutParserError):
        puw.forms.api_unyt.string_to_quantity("2 meter")
    with pytest.raises(LibraryWithoutParserError):
        puw.forms.api_unyt.string_to_unit("meter")
