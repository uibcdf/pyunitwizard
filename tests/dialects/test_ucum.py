"""Actual case-sensitive UCUM conformance at the Sabueso biomedical boundary."""

import json
from pathlib import Path

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import RecordError

pytest.importorskip("ucumvert")
from pyunitwizard.dialects import ucum


@pytest.mark.parametrize(
    "unit,code",
    [
        ("nanomolar", "nmol/L"),
        ("percent", "%"),
        ("meter/second**2", "m/s2"),
        ("dimensionless", "1"),
        ("millimeter", "mm"),
        ("megameter", "Mm"),
    ],
)
def test_actual_provider_verifies_explicit_output_code(unit, code):
    assert ucum.validate_unit(unit, code) == code
    values = np.array([0.0, 2.0, 10.0])
    result = ucum.parse_quantity(values, code, unit=unit, form="pint")
    np.testing.assert_allclose(result.magnitude, values)
    np.testing.assert_array_equal(values, [0, 2, 10])


def test_observed_chembl_values_round_trip_through_negotiated_ucum():
    fixture = Path(__file__).parents[1] / "data" / "sabueso_activity_quantities.json"
    observations = json.loads(fixture.read_text())["observations"]
    assert len(observations) == 343
    for unit, code in [("nanomolar", "nmol/L"), ("percent", "%")]:
        values = np.array([row["value"] for row in observations if row["unit"] == unit])
        assert ucum.validate_unit(unit, code) == code
        quantity = ucum.parse_quantity(values, code, unit=unit, form="pint")
        np.testing.assert_allclose(quantity.magnitude, values, rtol=1e-12)


@pytest.mark.parametrize("code", ["M", "nM", "NM", "", " nm", "nm ", "m^2", "m**2"])
def test_pint_aliases_and_non_ucum_syntax_are_never_accepted(code):
    with pytest.raises(RecordError):
        ucum.parse_quantity(1, code, unit="nanomolar")


@pytest.mark.parametrize(
    "code", ["m{cell}", "{count}", "[IU]", "m[IU]", "[pH]", "dB", "100.m", "10*3.m", "10^3.m", "Cel/s"]
)
def test_unsupported_semantics_cannot_be_erased_by_the_provider(code):
    with pytest.raises(RecordError):
        ucum.parse_quantity(1, code, unit="dimensionless")


@pytest.mark.parametrize("unit,code", [("nanomolar", "mol/L"), ("second", "m"), ("meter", "mm")])
def test_emission_refuses_different_scale_or_dimensions(unit, code):
    with pytest.raises(RecordError):
        ucum.validate_unit(unit, code)


def test_import_converts_actual_ucum_scale_and_requested_backend():
    with puw.context(default_form="unyt", default_parser="pint", standard_units=["meter", "second"]):
        quantity = ucum.parse_quantity([1, 2], "nmol/L", unit="mole / meter**3")
        assert puw.get_form(quantity) == "unyt"
        np.testing.assert_allclose(puw.get_value(quantity), [1e-6, 2e-6])


def test_affine_temperature_and_difference_have_explicit_semantics():
    assert ucum.validate_unit("degree_Celsius", "Cel", units_metadata="temperature: on_scale") == "Cel"
    absolute = ucum.parse_quantity([0, 25], "Cel", unit="kelvin", units_metadata="temperature: on_scale", form="pint")
    difference = ucum.parse_quantity(
        [0, 25], "Cel", unit="kelvin", units_metadata="temperature: difference", form="pint"
    )
    np.testing.assert_allclose(absolute.magnitude, [273.15, 298.15])
    np.testing.assert_allclose(difference.magnitude, [0, 25])
    with pytest.raises(RecordError):
        ucum.parse_quantity(1, "Cel", unit="kelvin")
    with pytest.raises(RecordError):
        ucum.parse_quantity(1, "Cel", unit="delta_degree_Celsius", units_metadata="temperature: on_scale")


def test_foreign_registry_definition_and_nonnumeric_values_are_refused():
    import pint

    foreign = pint.UnitRegistry(on_redefinition="ignore")
    foreign.define("nanomolar = 2e-9 * molar")
    with pytest.raises(RecordError):
        ucum.validate_unit(foreign.Unit("nanomolar"), "nmol/L")
    for value in [None, [True], ["1"], [1j]]:
        with pytest.raises(RecordError):
            ucum.parse_quantity(value, "m", unit="meter")


def test_provider_definitions_do_not_mutate_pint_application_registry():
    import subprocess
    import sys

    code = """
import pint
from pyunitwizard.dialects import ucum
registry = pint.get_application_registry()
before = set(registry._units)
assert ucum.validate_unit('nanomolar', 'nmol/L') == 'nmol/L'
assert set(registry._units) == before
"""
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_catalogue_ucum_codes_agree_with_actual_case_sensitive_provider():
    from pyunitwizard.dialects import vocabulary

    for entry in vocabulary.catalog()["units"].values():
        assert ucum.validate_unit(entry["computing_unit"], entry["ucum"]) == entry["ucum"]


def test_unqualified_provider_angle_alias_cannot_become_a_time_unit():
    # UCUM's apostrophe is an arcminute, whereas ucumvert 0.3.2 maps it to
    # Pint's time minute. Do not advertise unchecked provider atom semantics.
    with pytest.raises(RecordError):
        ucum.validate_unit("minute", "'")


@pytest.mark.parametrize(
    "code,unit",
    [
        ("m", "meter"),
        ("s", "second"),
        ("g", "gram"),
        ("rad", "radian"),
        ("C", "coulomb"),
        ("cd", "candela"),
        ("mol", "mole"),
        ("sr", "steradian"),
        ("Hz", "hertz"),
        ("Bq", "becquerel"),
        ("N", "newton"),
        ("Pa", "pascal"),
        ("J", "joule"),
        ("W", "watt"),
        ("A", "ampere"),
        ("V", "volt"),
        ("F", "farad"),
        ("Ohm", "ohm"),
        ("S", "siemens"),
        ("Wb", "weber"),
        ("T", "tesla"),
        ("H", "henry"),
        ("l", "liter"),
        ("L", "liter"),
        ("%", "percent"),
        ("min", "minute"),
        ("h", "hour"),
        ("d", "day"),
    ],
)
def test_every_admitted_multiplicative_atom_has_named_semantic_conformance(code, unit):
    assert ucum.validate_unit(unit, code) == code
    result = ucum.parse_quantity([0, 1, 2], code, unit=unit, form="pint")
    np.testing.assert_allclose(result.magnitude, [0, 1, 2], rtol=1e-12, atol=0)


@pytest.mark.parametrize(
    "code,unit",
    [("K", "kelvin"), ("Cel", "degree_Celsius")],
)
def test_every_admitted_temperature_atom_has_affine_conformance(code, unit):
    assert ucum.validate_unit(unit, code, units_metadata="temperature: on_scale") == code


@pytest.mark.parametrize("code", ["[degF]", "[degRe]"])
def test_unqualified_bracket_temperature_atoms_are_refused_consistently(code):
    with pytest.raises(RecordError):
        ucum.parse_quantity(0, code, unit="kelvin", units_metadata="temperature: on_scale", form="pint")


def test_finite_numeric_source_scale_cannot_underflow_to_a_zero_physical_unit():
    with pytest.raises(RecordError):
        ucum.parse_quantity(1, "ym99", unit="meter**99", form="pint")
